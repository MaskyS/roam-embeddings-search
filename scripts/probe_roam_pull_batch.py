#!/usr/bin/env python3
"""Probe Roam pull-many metadata batch sizes."""

import argparse
import asyncio
import os
import random
import statistics
import sys
import time
from typing import Iterable, List, Sequence

import httpx

METADATA_SELECTOR = (
    "[:block/uid :create/time :edit/time "
    "{:block/children [:block/uid :create/time :edit/time {:block/children ...}]}]"
)

QUERY_ALL_PAGES = """[:find ?uid :where [?e :node/title] [?e :block/uid ?uid]]"""


class ProbeResult:
    __slots__ = ("batch_size", "requests", "avg_ms", "p95_ms", "bytes_avg", "note")

    def __init__(self, batch_size: int, requests: int, avg_ms: float, p95_ms: float, bytes_avg: float, note: str | None = None) -> None:
        self.batch_size = batch_size
        self.requests = requests
        self.avg_ms = avg_ms
        self.p95_ms = p95_ms
        self.bytes_avg = bytes_avg
        self.note = note

    def to_row(self) -> str:
        note = f" {self.note}" if self.note else ""
        return (
            f"batch={self.batch_size:>4} | reqs={self.requests:>3} | "
            f"avg={self.avg_ms:6.1f}ms | p95={self.p95_ms:6.1f}ms | "
            f"bytes~{self.bytes_avg:8.0f}{note}"
        )


async def fetch_all_page_uids(client: httpx.AsyncClient) -> List[str]:
    response = await client.post("q", json={"query": QUERY_ALL_PAGES})
    response.raise_for_status()
    payload = response.json()
    rows = payload.get("result", [])
    return [row[0] for row in rows if row]


def chunked(seq: Sequence[str], size: int) -> Iterable[Sequence[str]]:
    for idx in range(0, len(seq), size):
        yield seq[idx : idx + size]


async def pull_metadata(client: httpx.AsyncClient, uids: Sequence[str], timeout: float) -> tuple[bool, float, int, str | None]:
    if not uids:
        return True, 0.0, 0, None

    eids = " ".join(f'[:block/uid "{uid}"]' for uid in uids)
    payload = {"eids": f"[{eids}]", "selector": METADATA_SELECTOR}

    start = time.perf_counter()
    try:
        response = await client.post("pull-many", json=payload, timeout=timeout)
    except httpx.TimeoutException:
        return False, (time.perf_counter() - start) * 1000.0, 0, "timeout"
    except httpx.HTTPError as exc:  # network/connection error
        return False, (time.perf_counter() - start) * 1000.0, 0, f"http_error:{exc}"

    elapsed_ms = (time.perf_counter() - start) * 1000.0
    if response.status_code != 200:
        snippet = response.text[:200].replace("\n", " ")
        return False, elapsed_ms, len(response.content), f"status={response.status_code} body={snippet}"

    return True, elapsed_ms, len(response.content), None


async def probe_batches(
    min_batch: int,
    max_batch: int,
    step: int,
    sample_uids: Sequence[str],
    client: httpx.AsyncClient,
    timeout: float,
) -> List[ProbeResult]:
    results: List[ProbeResult] = []
    total_pages = len(sample_uids)

    for batch_size in range(min_batch, max_batch + 1, step):
        slices = list(chunked(sample_uids, batch_size))
        timings: List[float] = []
        sizes: List[int] = []
        note: str | None = None
        for chunk in slices:
            ok, elapsed_ms, bytes_count, err = await pull_metadata(client, chunk, timeout)
            if not ok:
                note = err or "unknown_error"
                timings.append(elapsed_ms)
                sizes.append(bytes_count)
                break
            timings.append(elapsed_ms)
            sizes.append(bytes_count)

        requests = len(timings)
        avg_ms = statistics.mean(timings) if timings else 0.0
        p95_ms = statistics.quantiles(timings, n=20)[18] if len(timings) >= 20 else max(timings, default=0.0)
        bytes_avg = statistics.mean(sizes) if sizes else 0.0

        if note and note.startswith("status=429"):
            note = f"{note} (rate limit?)"
        if note and total_pages < batch_size and "status" in note:
            note = f"{note} (batch>{total_pages})"

        results.append(ProbeResult(batch_size, requests, avg_ms, p95_ms, bytes_avg, note))
        if note:
            # Stop escalating batch sizes once we encounter an error.
            break

    return results


async def async_main(args: argparse.Namespace) -> int:
    token = os.environ.get("ROAM_API_TOKEN")
    graph = os.environ.get("ROAM_GRAPH_NAME")
    if not token or not graph:
        print("ROAM_API_TOKEN and ROAM_GRAPH_NAME must be set in the environment", file=sys.stderr)
        return 2

    headers = {
        "X-Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    base_url = f"https://api.roamresearch.com/api/graph/{graph}/"
    async with httpx.AsyncClient(base_url=base_url, headers=headers, follow_redirects=True, timeout=args.timeout) as client:
        print("Fetching page UIDs…", file=sys.stderr)
        uids = await fetch_all_page_uids(client)
        if not uids:
            print("No page UIDs returned; aborting", file=sys.stderr)
            return 1

        print(f"Total pages discovered: {len(uids)}", file=sys.stderr)
        if args.sample_pages and args.sample_pages < len(uids):
            random.Random(args.seed).shuffle(uids)
            sample_uids = uids[: args.sample_pages]
        else:
            sample_uids = uids

        print(f"Sampling {len(sample_uids)} pages for probe", file=sys.stderr)

        results = await probe_batches(
            args.min_batch,
            args.max_batch,
            args.step,
            sample_uids,
            client,
            args.request_timeout,
        )

    print("\n=== Roam pull-many metadata probe ===")
    print(
        "For selector without block strings; all times in milliseconds."
    )
    for result in results:
        print(result.to_row())

    final = results[-1]
    if final.note:
        print(f"\nStopped early due to error at batch {final.batch_size}: {final.note}")
    return 0


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe Roam pull-many metadata batch sizes")
    parser.add_argument("--min-batch", type=int, default=50, help="Smallest batch size to test")
    parser.add_argument("--max-batch", type=int, default=500, help="Largest batch size to test")
    parser.add_argument("--step", type=int, default=50, help="Increment between batch sizes")
    parser.add_argument("--sample-pages", type=int, default=500, help="Number of page UIDs to sample for the probe")
    parser.add_argument("--seed", type=int, default=1234, help="Random seed for sampling")
    parser.add_argument("--timeout", type=float, default=30.0, help="Base client timeout in seconds")
    parser.add_argument(
        "--request-timeout",
        type=float,
        default=15.0,
        help="Per-request timeout for pull-many calls in seconds",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    return asyncio.run(async_main(args))


if __name__ == "__main__":
    raise SystemExit(main())

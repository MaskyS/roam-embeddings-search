#!/usr/bin/env python3
"""Basic semantic sync smoke tests against a live Roam graph."""

import argparse
import asyncio
import os
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

# Ensure backend package is importable when the script is run directly
SCRIPT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_ROOT)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from backend.sync_semantic import (  # noqa: E402
    CONFIG,
    MetadataPassResult,
    SyncConfig,
    get_all_page_uids,
    run_metadata_pass,
)


@dataclass
class FakeWeaviateAdapter:
    """Minimal adapter stub for metadata pass tests."""

    states: Dict[str, Dict[str, any]]

    async def fetch_existing_page_state(self, uid: str) -> Dict[str, any]:
        return self.states.get(uid, {})


async def gather_sample_uids(sample_pages: int) -> List[str]:
    all_uids = await get_all_page_uids()
    if not all_uids:
        raise RuntimeError("No page UIDs returned from Roam")
    if sample_pages and sample_pages < len(all_uids):
        return all_uids[:sample_pages]
    return all_uids


def build_state_from_metadata(metadata: MetadataPassResult, *, skew_ms: int = 0) -> Dict[str, Dict[str, any]]:
    states: Dict[str, Dict[str, any]] = {}
    for uid, meta in metadata.metadata_map.items():
        if meta.max_edit_time is None:
            continue
        adjusted_time = meta.max_edit_time + skew_ms
        states[uid] = {
            "page_objects": [
                {
                    "properties": {
                        "last_synced_edit_time": str(adjusted_time),
                        "content_hash": "test",
                    }
                }
            ],
            "chunk_objects": [],
            "last_synced_edit_time": str(adjusted_time),
            "content_hash": "test",
        }
    return states


async def test_since_filter(uids: List[str], config: SyncConfig) -> None:
    print("[test] metadata pass with future --since should skip everything")
    future_ts = int(time.time() * 1000) + 60_000
    adapter = FakeWeaviateAdapter(states={})
    result = await run_metadata_pass(uids, since=future_ts, adapter=adapter, config=config)
    assert not result.remaining_uids, "Expected all pages to be filtered by --since"
    print(f"  -> filtered {result.stats_delta.get('metadata_filtered', 0)} pages as expected")


async def test_state_skip(uids: List[str], config: SyncConfig) -> None:
    print("[test] metadata pass filters pages already synced at same edit time")
    adapter = FakeWeaviateAdapter(states={})
    baseline = await run_metadata_pass(uids, since=None, adapter=adapter, config=config)
    states_equal = build_state_from_metadata(baseline)
    adapter_equal = FakeWeaviateAdapter(states=states_equal)
    result = await run_metadata_pass(uids, since=None, adapter=adapter_equal, config=config)
    assert not result.remaining_uids, "Expected no remaining pages when edit times match"
    filtered = result.stats_delta.get("metadata_filtered", 0)
    print(f"  -> metadata filtered {filtered} pages (expected {len(uids)})")


async def test_state_detects_changes(uids: List[str], config: SyncConfig) -> None:
    print("[test] metadata pass keeps pages when last synced edit time is stale")
    adapter = FakeWeaviateAdapter(states={})
    baseline = await run_metadata_pass(uids, since=None, adapter=adapter, config=config)
    stale_states = build_state_from_metadata(baseline, skew_ms=-10_000)
    adapter_stale = FakeWeaviateAdapter(states=stale_states)
    result = await run_metadata_pass(uids, since=None, adapter=adapter_stale, config=config)
    assert result.remaining_uids, "Expected pages to remain when edit time is older"
    print(f"  -> {len(result.remaining_uids)} pages remain for full sync (expected {len(uids)})")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Semantic sync smoke tests against a live Roam graph")
    parser.add_argument("--sample-pages", type=int, default=150, help="Number of pages to sample for metadata tests")
    parser.add_argument("--metadata-batch", type=int, default=CONFIG.metadata_batch_size, help="Temporary metadata batch size override")
    args = parser.parse_args()

    required_env = ("ROAM_GRAPH_NAME", "ROAM_API_TOKEN")
    missing = [key for key in required_env if not os.getenv(key)]
    if missing:
        raise SystemExit(f"Missing required environment variables: {', '.join(missing)}")

    sample_uids = await gather_sample_uids(args.sample_pages)
    print(f"Collected {len(sample_uids)} UIDs for testing")

    config = SyncConfig(
        batch_size=CONFIG.batch_size,
        metadata_batch_size=args.metadata_batch,
        metadata_state_concurrency=CONFIG.metadata_state_concurrency,
        collection_name=CONFIG.collection_name,
        weaviate_http_host=CONFIG.weaviate_http_host,
        weaviate_http_port=CONFIG.weaviate_http_port,
        weaviate_http_secure=CONFIG.weaviate_http_secure,
        weaviate_grpc_host=CONFIG.weaviate_grpc_host,
        weaviate_grpc_port=CONFIG.weaviate_grpc_port,
        weaviate_grpc_secure=CONFIG.weaviate_grpc_secure,
        chunker_url=CONFIG.chunker_url,
        chunker_retries=CONFIG.chunker_retries,
        chunker_retry_delay=CONFIG.chunker_retry_delay,
        sync_version=CONFIG.sync_version,
        uuid_namespace=CONFIG.uuid_namespace,
        chunker_group_size=CONFIG.chunker_group_size,
        chunker_concurrency=CONFIG.chunker_concurrency,
        voyage_concurrency=CONFIG.voyage_concurrency,
        weaviate_write_concurrency=CONFIG.weaviate_write_concurrency,
        roam_requests_per_minute=CONFIG.roam_requests_per_minute,
    )

    await test_since_filter(sample_uids, config)
    await test_state_skip(sample_uids, config)
    await test_state_detects_changes(sample_uids, config)

    print("All metadata tests passed")


if __name__ == "__main__":
    asyncio.run(main())

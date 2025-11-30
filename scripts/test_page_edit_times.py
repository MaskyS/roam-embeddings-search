#!/usr/bin/env python3
"""Probe Roam page vs block edit timestamps by appending blocks."""

import argparse
import asyncio
import os
import secrets
import string
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import httpx

PULL_SELECTOR = (
    "[:block/uid :node/title :block/string :create/time :edit/time "
    "{:block/children [:block/uid :block/string :create/time :edit/time {:block/children ...}]}]"
)


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Environment variable {name} is required")
    return value


def ms_to_iso(value: Optional[int]) -> str:
    if value is None:
        return "null"
    return datetime.fromtimestamp(value / 1000, tz=timezone.utc).isoformat()


def flatten_children(node: Dict[str, Any], depth: int = 0) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    children = node.get(":block/children") or []
    if not isinstance(children, list):
        return results
    for child in children:
        if not isinstance(child, dict):
            continue
        entry = {
            "uid": child.get(":block/uid"),
            "string": child.get(":block/string"),
            "edit_time": child.get(":edit/time"),
            "create_time": child.get(":create/time"),
            "depth": depth,
        }
        results.append(entry)
        results.extend(flatten_children(child, depth + 1))
    return results


async def create_page(client: httpx.AsyncClient, title: str) -> None:
    payload = {"action": "create-page", "page": {"title": title}}
    response = await client.post("write", json=payload)
    response.raise_for_status()


def generate_uid() -> str:
    alphabet = string.ascii_letters + string.digits + "-_"
    return "".join(secrets.choice(alphabet) for _ in range(9))


async def create_block(client: httpx.AsyncClient, parent_uid: str, text: str, *, uid: Optional[str] = None) -> str:
    block_uid = uid or generate_uid()
    payload = {
        "action": "create-block",
        "location": {"parent-uid": parent_uid, "order": "last"},
        "block": {"string": text, "uid": block_uid},
    }
    response = await client.post("write", json=payload)
    response.raise_for_status()
    return block_uid


async def update_block(client: httpx.AsyncClient, block_uid: str, text: str) -> None:
    payload = {
        "action": "update-block",
        "block": {"uid": block_uid, "string": text},
    }
    response = await client.post("write", json=payload)
    response.raise_for_status()


async def query_page_uid(client: httpx.AsyncClient, title: str) -> str:
    escaped = title.replace("\\", "\\\\").replace("\"", "\\\"")
    query = (
        "[:find ?uid"
        " :where [?e :node/title \"" + escaped + "\"]"
        "        [?e :block/uid ?uid]]"
    )
    payload = {"query": query}
    response = await client.post("q", json=payload)
    response.raise_for_status()
    data = response.json()
    rows = data.get("result") or []
    if not rows:
        raise RuntimeError(f"No UID found for page '{title}'")
    return rows[0][0]


async def pull_page(client: httpx.AsyncClient, page_uid: str) -> Dict[str, Any]:
    payload = {"eid": f"[:block/uid \"{page_uid}\"]", "selector": PULL_SELECTOR}
    response = await client.post("pull", json=payload)
    response.raise_for_status()
    data = response.json()
    result = data.get("result")
    if not result:
        raise RuntimeError(f"Pull returned no data for page {page_uid}")
    return result


async def run(args: argparse.Namespace) -> None:
    token = args.token or require_env("ROAM_API_TOKEN")
    graph = args.graph or require_env("ROAM_GRAPH_NAME")
    base_url = f"https://api.roamresearch.com/api/graph/{graph}/"
    headers = {
        "X-Authorization": f"Bearer {token}",
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    page_title = args.page_title or f"{args.page_prefix}-{int(time.time())}"

    async with httpx.AsyncClient(base_url=base_url, headers=headers, follow_redirects=True, timeout=30.0) as client:
        print(f"Creating page '{page_title}'…")
        await create_page(client, page_title)
        if args.post_create_wait:
            print(f"Waiting {args.post_create_wait} seconds for page to register…")
            await asyncio.sleep(args.post_create_wait)
        page_uid = await query_page_uid(client, page_title)
        print(f"Page UID: {page_uid}")

        print("Pulling initial page snapshot…")
        initial = await pull_page(client, page_uid)
        page_edit_initial = initial.get(":edit/time")
        print(f"Initial page edit time: {ms_to_iso(page_edit_initial)}")

        first_text = args.first_block or "First automated block"
        print("Appending first block…")
        first_uid = await create_block(client, page_uid, first_text)

        if args.wait_seconds:
            print(f"Waiting {args.wait_seconds} seconds…")
            await asyncio.sleep(args.wait_seconds)

        second_text = args.second_block or "Second automated block"
        print("Appending second block…")
        await create_block(client, page_uid, second_text)

        if args.post_append_wait:
            print(f"Waiting {args.post_append_wait} seconds before update…")
            await asyncio.sleep(args.post_append_wait)

        if args.update_block:
            print("Updating first block text…")
            await update_block(client, first_uid, args.update_block)
            if args.post_update_wait:
                print(f"Waiting {args.post_update_wait} seconds after update…")
                await asyncio.sleep(args.post_update_wait)

        print("Pulling final page snapshot…")
        final = await pull_page(client, page_uid)
        page_edit_final = final.get(":edit/time")
        children = flatten_children(final)

        print("\n=== Results ===")
        print(f"Page title: {page_title}")
        print(f"Page UID: {page_uid}")
        print(f"Initial page edit time : {ms_to_iso(page_edit_initial)}")
        print(f"Final page edit time   : {ms_to_iso(page_edit_final)}")
        print("\nChild blocks:")
        if not children:
            print("  (none)")
        else:
            for child in children:
                label = child.get("string") or "(no text)"
                label = label.replace("\n", " ").strip()
                if len(label) > 60:
                    label = label[:57] + "…"
                depth = child.get("depth", 0)
                indent = "  " * depth
                print(
                    f"{indent}- UID {child['uid']} | edit {ms_to_iso(child['edit_time'])} | create {ms_to_iso(child['create_time'])} | text '{label}'"
                )

        if args.keep_page:
            print("\nPage retained (use Roam UI to delete if desired).")
        else:
            print("\nTo remove the page afterwards, delete it manually in Roam.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare Roam page edit times vs appended blocks")
    parser.add_argument("--graph", help="Roam graph name (falls back to ROAM_GRAPH_NAME)")
    parser.add_argument("--token", help="Roam API token (falls back to ROAM_API_TOKEN)")
    parser.add_argument("--page-title", help="Explicit page title to use")
    parser.add_argument("--page-prefix", default="test-page", help="Prefix for generated page title")
    parser.add_argument("--first-block", help="Text for the first appended block")
    parser.add_argument("--second-block", help="Text for the second appended block")
    parser.add_argument("--wait-seconds", type=float, default=5.0, help="Delay between block appends")
    parser.add_argument("--post-append-wait", type=float, default=0.0, help="Delay after second append before optional update")
    parser.add_argument("--post-update-wait", type=float, default=0.0, help="Delay after update before final pull")
    parser.add_argument("--update-block", help="If provided, update the first block text to this value before final pull")
    parser.add_argument("--post-create-wait", type=float, default=1.0, help="Delay after page creation before querying UID")
    parser.add_argument("--keep-page", action="store_true", help="Do not suggest deleting the test page")
    return parser.parse_args()


if __name__ == "__main__":
    asyncio.run(run(parse_args()))

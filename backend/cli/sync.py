"""Thin CLI wrapper around the semantic sync orchestrator."""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from typing import Any, Awaitable, Callable, Dict, Optional

import structlog
import typer
from tqdm.auto import tqdm

# Add backend to path to allow local imports
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.config import CONFIG, SyncConfig
from sync.orchestrator import run_sync
from sync.state.run_state import SyncRunParams

from common.logging import configure_logging
configure_logging(json=True)

LOGGER = structlog.get_logger(__name__)


async def sync_semantic_graph(
    clear_existing: bool = False,
    test_limit: Optional[int] = None,
    recreate_collection: bool = False,
    state_file: Optional[str] = None,
    resume: bool = False,
    since: Optional[int] = None,
    config: SyncConfig = CONFIG,
    status_cb: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None,
    completion_cb: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None,
) -> Dict[str, Any]:
    """Run the semantic sync orchestrator with the provided options."""

    resolved_state_path = os.path.abspath(state_file) if state_file else None

    params = SyncRunParams(
        config=config,
        since=since,
        test_limit=test_limit,
        resume=resume,
        clear_existing=clear_existing,
        recreate_collection=recreate_collection,
        state_file=resolved_state_path,
        status_callback=status_cb,
        completion_callback=completion_cb,
    )

    voyage_timeout = float(os.getenv("VOYAGE_TIMEOUT", "60"))

    def _load_env_settings() -> Dict[str, Any]:
        return {
            "roam_graph_name": os.getenv("ROAM_GRAPH_NAME") or os.getenv("roam_graph_name"),
            "roam_api_token": os.getenv("ROAM_API_TOKEN") or os.getenv("roam_api_token"),
            "voyage_api_key": os.getenv("VOYAGEAI_API_KEY") or os.getenv("voyageai_api_key"),
            "voyage_model": os.getenv("VOYAGEAI_CONTEXT_MODEL") or os.getenv("voyageai_context_model") or "voyage-context-3",
        }

    env = _load_env_settings()

    summary = await run_sync(
        params=params,
        roam_graph_name=env["roam_graph_name"],
        roam_api_token=env["roam_api_token"],
        voyage_api_key=env["voyage_api_key"],
        voyage_model=env["voyage_model"],
        voyage_timeout=voyage_timeout,
        logger=LOGGER,
    )

    return summary


class _CLIProgress:
    """Minimal tqdm-based progress reporter for CLI runs."""

    def __init__(self, enable: Optional[bool] = None) -> None:
        # enable: True -> force on, False -> force off, None -> auto
        self._enable = enable
        self._pbar: Optional[tqdm] = None
        self._total: Optional[int] = None

    def _disable_flag(self) -> Optional[bool]:
        if self._enable is None:
            return None  # let tqdm decide based on TTY
        return not self._enable

    async def status_cb(self, payload: Dict[str, Any]) -> None:
        event = payload.get("event")
        if event == "uids_loaded":
            total = payload.get("total_pages") or payload.get("progress", {}).get("total")
            if total:
                self._total = int(total)
                self._pbar = tqdm(total=self._total, unit="page", desc="loading uids", disable=self._disable_flag())
        elif event == "chunker_ready":
            if self._pbar:
                dur = payload.get("duration")
                if dur is not None:
                    self._pbar.set_postfix(chunker=f"{float(dur):.2f}s")
        elif event == "metadata_filtered":
            if self._pbar:
                rem = payload.get("remaining")
                sk = payload.get("skipped")
                self._pbar.set_postfix(remaining=rem, skipped=sk)
        elif event == "batch_start":
            if self._pbar:
                b = payload.get("batch")
                s = payload.get("page_start")
                e = payload.get("page_end")
                self._pbar.set_description(f"batch {b} pages {s}-{e}")
        elif event == "batch_complete":
            if self._pbar:
                proc = payload.get("processed") or {}
                n = proc.get("processed")
                if isinstance(n, (int, float)):
                    self._pbar.n = int(n)
                    self._pbar.refresh()

    async def completion_cb(self, summary: Dict[str, Any]) -> None:
        if self._pbar:
            processed = summary.get("processed")
            if isinstance(processed, (int, float)) and self._total:
                self._pbar.n = min(int(processed), self._total)
            self._pbar.close()


def main(
    clear: bool = typer.Option(False, "--clear", help="Clear all existing objects before syncing."),
    test: Optional[int] = typer.Option(None, "--test", help="Test mode: only process first N pages."),
    recreate_collection: bool = typer.Option(
        False,
        "--recreate-collection",
        help="Force recreate the collection even if it exists.",
    ),
    state_file: Optional[str] = typer.Option(
        None,
        "--state-file",
        help="Path to persist incremental sync progress.",
    ),
    resume: bool = typer.Option(False, "--resume", help="Resume from a previously saved state file."),
    since: Optional[int] = typer.Option(
        None,
        "--since",
        help="Only process pages whose max edit time is greater than the provided epoch milliseconds.",
    ),
    progress: Optional[bool] = typer.Option(
        None,
        "--progress/--no-progress",
        help="Show a tqdm progress bar (auto by default)",
    ),
) -> None:
    """Sync Roam graph to Weaviate using contextual embeddings."""
    reporter = _CLIProgress(enable=progress)

    asyncio.run(
        sync_semantic_graph(
            clear_existing=clear,
            test_limit=test,
            recreate_collection=recreate_collection,
            state_file=state_file,
            resume=resume,
            since=since,
            status_cb=reporter.status_cb,
            completion_cb=reporter.completion_cb,
        )
    )
    LOGGER.info("Done!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    typer.run(main)

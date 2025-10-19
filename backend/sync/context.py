"""Execution context for semantic sync stages."""

from __future__ import annotations

from dataclasses import dataclass
from structlog.stdlib import BoundLogger

from common.config import SyncConfig
from sync.resources import SyncResources
from clients.roam import RoamClient


@dataclass(frozen=True)
class SyncContext:
    config: SyncConfig
    resources: SyncResources
    roam_client: RoamClient
    logger: BoundLogger


"""Error taxonomy for semantic sync operations.

Defines a hierarchy of exceptions to enable proper error handling:
- TransientError: Network issues, rate limits → retry
- InvalidInputError: Bad data, missing fields → log + skip
- SystemError: Database down, service unavailable → abort sync
- ConfigurationError: Missing API keys, bad config → fail fast
"""

from __future__ import annotations

from typing import Optional


class SemanticSyncError(Exception):
    """Base exception for all semantic sync errors."""

    def __init__(self, message: str, *, context: Optional[dict] = None) -> None:
        super().__init__(message)
        self.message = message
        self.context = context or {}


class TransientError(SemanticSyncError):
    """Recoverable errors that should be retried.

    Examples:
    - Network timeouts
    - HTTP 429 rate limits
    - HTTP 5xx server errors
    - Temporary service unavailability
    """

    pass


class InvalidInputError(SemanticSyncError):
    """Invalid or corrupt data that should be skipped.

    Examples:
    - Missing required fields (no :block/uid)
    - Malformed data structures
    - Invalid UIDs
    - Corrupt metadata
    """

    pass


class SystemError(SemanticSyncError):
    """Unrecoverable system failures that should abort the sync.

    Examples:
    - Database connection lost
    - Weaviate cluster down
    - Chunker service unavailable
    - Disk full
    """

    pass


class ConfigurationError(SemanticSyncError):
    """Configuration issues that prevent sync from starting.

    Examples:
    - Missing API keys
    - Invalid configuration values
    - Incompatible settings
    """

    pass


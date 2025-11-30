"""Retry helpers for external service calls."""

from __future__ import annotations

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from common.errors import TransientError


# Errors that are considered transient and should trigger retries
TRANSIENT_ERRORS = (
    TransientError,
    httpx.ConnectError,
    httpx.ReadTimeout,
    httpx.HTTPStatusError,
)


def transient_retry(tries: int = 3, max_wait: float = 4.0):
    """
    Decorator factory for retrying on transient errors with exponential backoff.

    Works with both sync and async functions (tenacity handles this automatically).

    Args:
        tries: Maximum number of attempts (default: 3)
        max_wait: Maximum wait time between retries in seconds (default: 4.0)

    Returns:
        A retry decorator configured for transient errors.

    Example:
        @transient_retry()
        async def fetch_data():
            ...

        @transient_retry(tries=5, max_wait=10.0)
        async def fetch_with_more_retries():
            ...
    """
    return retry(
        stop=stop_after_attempt(tries),
        wait=wait_exponential(max=max_wait),
        retry=retry_if_exception_type(TRANSIENT_ERRORS),
        reraise=True,
    )


def should_retry_http_status(exc: BaseException) -> bool:
    """
    Check if an HTTP error should be retried based on status code.

    Retryable status codes:
        - 429: Too Many Requests (rate limit)
        - 500, 502, 503, 504: Server errors

    Args:
        exc: The exception to check

    Returns:
        True if the error is retryable
    """
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in (429, 500, 502, 503, 504)
    return isinstance(exc, TRANSIENT_ERRORS)

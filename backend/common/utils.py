"""Utility helpers shared across backend modules."""

from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable, Optional, Sequence, Type

from funcy import decorator


def async_retry(
    *,
    tries: int = 3,
    timeout: float | Callable[[int], float] = 0.0,
    errors: Sequence[Type[BaseException]] = (Exception,),
    filter_errors: Optional[Callable[[BaseException], bool]] = None,
) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:

    @decorator
    async def wrapper(call):
        attempt = 0
        while True:
            try:
                return await call()
            except tuple(errors) as exc:  # type: ignore[arg-type]
                if filter_errors and not filter_errors(exc):
                    raise
                attempt += 1
                if attempt >= tries:
                    raise
                delay = timeout(attempt) if callable(timeout) else timeout
                if delay:
                    await asyncio.sleep(delay)

    return wrapper


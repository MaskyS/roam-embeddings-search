"""Shared structlog configuration for the backend services."""

from __future__ import annotations

import logging
import os
import structlog


def configure_logging(*, json: bool = True, level: int | str = None) -> None:
    """Configure structlog and stdlib logging.

    Args:
        json: If True, use JSONRenderer, else ConsoleRenderer.
        level: Optional log level to set on root logger. Defaults to INFO or env LOG_LEVEL.
    """
    if level is None:
        level_name = os.getenv("LOG_LEVEL", "INFO").upper()
        level = getattr(logging, level_name, logging.INFO)

    logging.basicConfig(level=level, format="%(message)s")

    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.format_exc_info,
    ]
    if json:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


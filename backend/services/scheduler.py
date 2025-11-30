"""
Scheduler service for automatic daily syncs.

Uses APScheduler to run daily sync jobs at a configured time.
"""

from __future__ import annotations

import asyncio
import os
from datetime import datetime
from typing import Any, Callable, Dict, Optional

import pytz
import structlog
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from sync.state.db_persistence import get_scheduler_config, update_scheduler_config, initialise

logger = structlog.get_logger(__name__)


def get_local_timezone() -> str:
    """
    Detect the system's local timezone.

    Returns:
        Timezone name as string (e.g., 'America/Los_Angeles', 'UTC')
    """
    try:
        # Get local timezone from system
        local_tz = datetime.now().astimezone().tzinfo

        # Try to get the timezone name
        # tzname() returns a tuple like ('PST', 'PDT') or just the name
        tz_name = local_tz.tzname(None)

        # Try to map to a pytz timezone
        # If we have a standard timezone name, use it
        if hasattr(local_tz, 'zone'):
            return local_tz.zone

        # For Docker containers and systems without proper timezone info,
        # this will typically return 'UTC'
        logger.info("Detected local timezone", timezone=tz_name)

        # Attempt to find matching pytz timezone
        # Most modern systems will have zone attribute, but fall back to UTC if not
        for tz in pytz.common_timezones:
            try:
                if pytz.timezone(tz).tzname(datetime.now()) == tz_name:
                    return tz
            except:
                continue

        # Default to UTC if we can't determine
        logger.warning("Could not determine local timezone, defaulting to UTC")
        return "UTC"

    except Exception as exc:
        logger.warning("Failed to detect local timezone, defaulting to UTC", error=str(exc))
        return "UTC"

# Global scheduler instance
_scheduler: Optional[AsyncIOScheduler] = None


def get_scheduler() -> Optional[AsyncIOScheduler]:
    """Get the global scheduler instance."""
    return _scheduler


async def execute_auto_sync(sync_trigger_fn: Callable) -> None:
    """
    Execute automatic sync and update status.

    Args:
        sync_trigger_fn: Async function that triggers a sync job
    """
    run_start = datetime.utcnow().isoformat() + "Z"
    logger.info("Auto-sync starting", timestamp=run_start)

    try:
        # Trigger sync with 'since' mode
        await sync_trigger_fn(mode="since")

        # Update last run status
        update_scheduler_config(
            last_auto_run=run_start,
            last_auto_status="success"
        )
        logger.info("Auto-sync completed successfully", timestamp=run_start)

    except Exception as exc:
        error_msg = str(exc)
        logger.error("Auto-sync failed", error=error_msg, timestamp=run_start)

        # Update last run status with failure
        update_scheduler_config(
            last_auto_run=run_start,
            last_auto_status=f"failed: {error_msg}"
        )


def _schedule_job(scheduler: AsyncIOScheduler, config: Dict[str, Any], sync_trigger_fn: Callable) -> None:
    """Schedule the sync job based on configuration."""
    if not config.get("enabled", False):
        logger.info("Auto-sync is disabled, not scheduling job")
        return

    schedule_time = config.get("schedule_time", "02:00")
    timezone_str = config.get("timezone", "UTC")

    try:
        # Parse time (HH:MM format)
        hour, minute = schedule_time.split(":")
        hour = int(hour)
        minute = int(minute)

        # Create cron trigger for daily execution at specified time
        timezone = pytz.timezone(timezone_str)
        trigger = CronTrigger(
            hour=hour,
            minute=minute,
            timezone=timezone
        )

        # Schedule the job
        scheduler.add_job(
            execute_auto_sync,
            trigger=trigger,
            args=[sync_trigger_fn],
            id="daily_auto_sync",
            replace_existing=True,
            name="Daily Automatic Sync"
        )

        logger.info(
            "Auto-sync scheduled",
            time=schedule_time,
            timezone=timezone_str,
            next_run=scheduler.get_job("daily_auto_sync").next_run_time
        )

    except Exception as exc:
        logger.error("Failed to schedule auto-sync job", error=str(exc))


async def initialize_scheduler(sync_trigger_fn: Callable) -> AsyncIOScheduler:
    """
    Initialize and start the APScheduler.

    Args:
        sync_trigger_fn: Async function to trigger sync (e.g., calls /sync/start API)

    Returns:
        AsyncIOScheduler instance
    """
    global _scheduler

    # Ensure database is initialized
    initialise()

    # Read configuration from environment or database
    default_enabled = os.getenv("AUTO_SYNC_ENABLED", "false").lower() == "true"
    default_time = os.getenv("AUTO_SYNC_TIME", "02:00")
    # Auto-detect system's local timezone instead of requiring configuration
    default_timezone = get_local_timezone()

    # Get or create scheduler config
    config = get_scheduler_config()

    # Update with environment defaults if not set
    if config.get("enabled") is False and default_enabled:
        config = update_scheduler_config(
            enabled=default_enabled,
            schedule_time=default_time,
            timezone=default_timezone
        )

    # Create scheduler
    _scheduler = AsyncIOScheduler(timezone=pytz.UTC)

    # Schedule job if enabled
    _schedule_job(_scheduler, config, sync_trigger_fn)

    # Start scheduler
    _scheduler.start()
    logger.info("Scheduler initialized and started")

    return _scheduler


async def shutdown_scheduler() -> None:
    """Gracefully shutdown the scheduler."""
    global _scheduler

    if _scheduler and _scheduler.running:
        logger.info("Shutting down scheduler")
        _scheduler.shutdown(wait=True)
        _scheduler = None
        logger.info("Scheduler shut down successfully")


async def reschedule_job(config: Dict[str, Any], sync_trigger_fn: Callable) -> None:
    """
    Reschedule the auto-sync job with new configuration.

    Args:
        config: Updated scheduler configuration
        sync_trigger_fn: Async function to trigger sync
    """
    global _scheduler

    if not _scheduler:
        logger.warning("Scheduler not initialized, cannot reschedule")
        return

    # Remove existing job if present
    if _scheduler.get_job("daily_auto_sync"):
        _scheduler.remove_job("daily_auto_sync")
        logger.info("Removed existing auto-sync job")

    # Schedule new job if enabled
    _schedule_job(_scheduler, config, sync_trigger_fn)

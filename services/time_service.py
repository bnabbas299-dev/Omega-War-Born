"""
Time Service — Phase 2
Manages scheduled game ticks: income collection, event triggers, upkeep.
Integrates with python-telegram-bot's JobQueue.
"""

from __future__ import annotations

from telegram.ext import Application

# Tick interval in seconds (default: every 60 minutes)
TICK_INTERVAL_SECONDS: int = 3600


async def economy_tick(context) -> None:
    """
    Scheduled job: collect income and pay upkeep for all registered players.
    (Stub — implement in Phase 2)
    """
    pass


async def event_tick(context) -> None:
    """
    Scheduled job: trigger random global events.
    (Stub — implement in Phase 2)
    """
    pass


def register_jobs(app: Application) -> None:
    """
    Register all scheduled jobs with the bot's JobQueue.
    Call this from main.py after building the Application.
    (Stub — implement in Phase 2)
    """
    # Example (uncomment in Phase 2):
    # app.job_queue.run_repeating(economy_tick, interval=TICK_INTERVAL_SECONDS, first=10)
    # app.job_queue.run_repeating(event_tick,   interval=TICK_INTERVAL_SECONDS, first=30)
    pass

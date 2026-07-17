"""
Time Service — scheduled game jobs.
"""

from __future__ import annotations

from telegram.ext import Application
from services.building_service import get_all_in_progress, mark_completed_and_update, CATALOG

CONSTRUCTION_CHECK_INTERVAL = 60   # seconds


async def construction_completion_job(context) -> None:
    """
    Runs every minute.
    Finds all finished construction items, completes them, and notifies leaders.
    """
    finished_rows = get_all_in_progress()
    if not finished_rows:
        return

    for row in finished_rows:
        queue_id    = row["id"]
        country_id  = row["country_id"]
        building_key = row["building_name"]
        leader_id   = row["leader_id"]

        info = CATALOG.get(building_key)
        if not info:
            continue

        mark_completed_and_update(queue_id, country_id, building_key)

        if leader_id:
            try:
                await context.bot.send_message(
                    chat_id=leader_id,
                    text=(
                        "🏗 پروژه تکمیل شد!\n\n"
                        f"{info['emoji']} {info['name']}\n\n"
                        "✅ ساختمان به کشور شما اضافه شد."
                    ),
                )
            except Exception:
                pass  # Player may have blocked the bot


def register_jobs(app: Application) -> None:
    app.job_queue.run_repeating(
        construction_completion_job,
        interval=CONSTRUCTION_CHECK_INTERVAL,
        first=10,
    )

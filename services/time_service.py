"""
Time Service — scheduled game jobs.
  • construction_completion_job  — Phase 6, checks construction_queue every 60 s
  • production_completion_job    — Phase 8, checks production_queue every 60 s
"""

from __future__ import annotations

from telegram.ext import Application
from services.building_service    import get_all_in_progress, mark_completed_and_update, CATALOG
from services.production_service  import get_all_in_progress_global, finish_production, FACTORY_CATALOG
from services.technology_service  import get_all_finished_global, finish_research, SPECIAL_TECH_CATALOG

CHECK_INTERVAL = 60   # seconds


# ── Construction completion (Phase 6) ─────────────────────────────────────────

async def construction_completion_job(context) -> None:
    """Checks construction_queue every minute, notifies leaders on completion."""
    finished_rows = get_all_in_progress()
    if not finished_rows:
        return

    for row in finished_rows:
        queue_id     = row["id"]
        country_id   = row["country_id"]
        building_key = row["building_name"]
        leader_id    = row["leader_id"]

        info = CATALOG.get(building_key)
        if not info:
            continue

        mark_completed_and_update(queue_id, country_id, building_key)

        if leader_id:
            try:
                await context.bot.send_message(
                    chat_id=leader_id,
                    text=(
                        "🏗 پروژه ساختمانی تکمیل شد!\n\n"
                        f"{info['emoji']} {info['name']}\n\n"
                        "✅ ساختمان به کشور شما اضافه شد."
                    ),
                )
            except Exception:
                pass


# ── Production completion (Phase 8) ──────────────────────────────────────────

async def production_completion_job(context) -> None:
    """Checks production_queue every minute, completes finished items, notifies leaders."""
    finished_rows = get_all_in_progress_global()
    if not finished_rows:
        return

    for row in finished_rows:
        queue_id  = row["id"]
        leader_id = row["leader_id"]

        completed = finish_production(queue_id)
        if not completed:
            continue

        if not leader_id:
            continue

        if completed["queue_type"] == "factory":
            fac_info = FACTORY_CATALOG.get(completed["item_key"], {})
            fac_name = fac_info.get("name", completed["item_name"])
            text = (
                "🏭 ساخت کارخانه تکمیل شد!\n\n"
                f"{SEP}\n\n"
                f"🏗 {fac_name}\n\n"
                f"✅ کارخانه به کشور شما اضافه شد.\n\n"
                f"{SEP}"
            )
        else:
            text = (
                "✅ تولید تکمیل شد.\n\n"
                f"{SEP}\n\n"
                f"📦 تجهیز: {completed['item_name']}\n"
                f"🔢 تعداد: {completed['quantity']:,}\n"
                f"🏭 کارخانه: {_factory_label(completed['factory_type'])}\n\n"
                f"{SEP}"
            )

        try:
            await context.bot.send_message(chat_id=leader_id, text=text)
        except Exception:
            pass


# ── Research completion (Phase 9) ─────────────────────────────────────────────

async def research_completion_job(context) -> None:
    """Checks research_queue every minute, completes finished items, notifies leaders."""
    finished_rows = get_all_finished_global()
    if not finished_rows:
        return

    for row in finished_rows:
        queue_id  = row["id"]
        leader_id = row["leader_id"]

        completed = finish_research(queue_id)
        if not completed:
            continue

        if not leader_id:
            continue

        if completed["research_type"] == "level_upgrade":
            item_key = completed["item_key"]
            target   = int(item_key.replace("level_", "")) if item_key.startswith("level_") else "?"
            text = (
                "📈 ارتقاء سطح فناوری تکمیل شد!\n\n"
                f"{SEP}\n\n"
                f"🔬 سطح فناوری جدید: {target}\n\n"
                f"✅ فناوری کشور شما ارتقاء یافت.\n\n"
                f"{SEP}"
            )
        else:
            spec = SPECIAL_TECH_CATALOG.get(completed["item_key"], {})
            name = spec.get("name", completed["item_name"])
            text = (
                "✅ تحقیق تکمیل شد.\n\n"
                f"{SEP}\n\n"
                f"🔬 فناوری: {name}\n\n"
                f"اکنون فعال است.\n\n"
                f"{SEP}"
            )

        try:
            await context.bot.send_message(chat_id=leader_id, text=text)
        except Exception:
            pass


SEP = "━━━━━━━━━━━━━━"


def _factory_label(factory_type: str | None) -> str:
    if not factory_type:
        return "—"
    return FACTORY_CATALOG.get(factory_type, {}).get("name", factory_type)


# ── Job registration ──────────────────────────────────────────────────────────

def register_jobs(app: Application) -> None:
    app.job_queue.run_repeating(
        construction_completion_job,
        interval=CHECK_INTERVAL,
        first=10,
    )
    app.job_queue.run_repeating(
        production_completion_job,
        interval=CHECK_INTERVAL,
        first=15,
    )
    app.job_queue.run_repeating(
        research_completion_job,
        interval=CHECK_INTERVAL,
        first=20,
    )

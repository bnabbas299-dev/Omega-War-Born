"""
Buildings handler — Phase 6
Handles all bld_* callbacks:
  bld_list          → show building catalog
  bld_info_{key}    → show building detail + confirm / cancel
  bld_buy_{key}     → execute construction
  bld_cancel        → back to list
  bld_queue         → active construction queue
"""

from telegram import Update
from telegram.ext import ContextTypes

from models.player import Player
from services.building_service import (
    CATALOG,
    start_construction,
    get_active_queue,
    remaining_label_and_pct,
    format_duration,
)
from utils.keyboards import (
    MAIN_MENU_KEYBOARD,
    building_list_keyboard,
    confirm_keyboard,
)

_NOT_REGISTERED = (
    "⚠️ شما هنوز کشوری انتخاب نکرده‌اید.\n"
    "لطفاً ابتدا /start را بزنید."
)


# ── Entry points (called directly from menu.py) ───────────────────────────────

async def show_building_list(query, country_id: int) -> None:
    await query.message.reply_text(
        "🏗 ساخت‌وساز\n\n"
        "یک ساختمان را برای مشاهده جزئیات و شروع ساخت انتخاب کنید:",
        reply_markup=building_list_keyboard(),
    )


async def show_queue(query, country_id: int) -> None:
    items = get_active_queue(country_id)
    if not items:
        await query.message.reply_text(
            "📋 پروژه‌های در حال ساخت\n\n"
            "در حال حاضر هیچ پروژه‌ای در صف ساخت وجود ندارد.",
            reply_markup=MAIN_MENU_KEYBOARD,
        )
        return

    lines = ["📋 پروژه‌های در حال ساخت\n"]
    for i, row in enumerate(items, 1):
        key   = row["building_name"]
        info  = CATALOG.get(key, {})
        name  = info.get("name", key)
        emoji = info.get("emoji", "🏗")
        label, pct = remaining_label_and_pct(row)

        bar_filled = int(pct / 10)
        bar        = "█" * bar_filled + "░" * (10 - bar_filled)

        lines.append(
            f"{i}. {emoji} {name}\n"
            f"   ⏱ باقی‌مانده: {label}\n"
            f"   📊 [{bar}] {pct}%\n"
            f"   🔄 وضعیت: در حال ساخت\n"
        )

    await query.message.reply_text(
        "\n".join(lines),
        reply_markup=MAIN_MENU_KEYBOARD,
    )


# ── Callback dispatcher ───────────────────────────────────────────────────────

async def buildings_callback_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data
    user = query.from_user

    # Auth check
    player = Player.get(user.id)
    if not player or not player.is_registered:
        await query.message.reply_text(_NOT_REGISTERED, reply_markup=MAIN_MENU_KEYBOARD)
        return

    country_id: int = player.country_id  # type: ignore[assignment]
    player.touch()

    # ── Back to list ─────────────────────────────────────────────────────────
    if data == "bld_list" or data == "bld_cancel":
        await show_building_list(query, country_id)
        return

    # ── Queue ────────────────────────────────────────────────────────────────
    if data == "bld_queue":
        await show_queue(query, country_id)
        return

    # ── Building info ─────────────────────────────────────────────────────────
    if data.startswith("bld_info_"):
        key = data[len("bld_info_"):]
        await _show_building_info(query, key)
        return

    # ── Confirm purchase ──────────────────────────────────────────────────────
    if data.startswith("bld_buy_"):
        key = data[len("bld_buy_"):]
        await _confirm_purchase(query, country_id, key)
        return


# ── Private helpers ───────────────────────────────────────────────────────────

async def _show_building_info(query, building_key: str) -> None:
    info = CATALOG.get(building_key)
    if not info:
        await query.message.reply_text("❌ ساختمان شناخته‌شده نیست.")
        return

    price_b   = info["price"] / 1_000_000_000
    tech_text = f"سطح {info['tech_req']}" if info["tech_req"] > 0 else "بدون نیاز"
    duration  = format_duration(info["build_minutes"])

    text = (
        f"{info['emoji']} {info['name']}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"💰 قیمت: {price_b:g} میلیارد دلار\n"
        f"🔬 نیاز فناوری: {tech_text}\n"
        f"⏱ مدت ساخت: {duration}\n\n"
        f"📋 مزایا:\n{info['benefit']}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"آیا ساخت این پروژه را تأیید می‌کنید؟"
    )

    await query.message.reply_text(
        text,
        reply_markup=confirm_keyboard(building_key),
    )


async def _confirm_purchase(query, country_id: int, building_key: str) -> None:
    result = start_construction(country_id, building_key)

    if not result["success"]:
        await query.message.reply_text(
            f"❌ خطا در شروع ساخت:\n\n{result['message']}",
            reply_markup=building_list_keyboard(),
        )
        return

    await query.message.reply_text(
        f"✅ ساخت آغاز شد!\n\n"
        f"🏗 {result['name']}\n"
        f"⏱ مدت: {result['duration']}\n"
        f"🕐 پایان: {result['finish_time']}\n\n"
        f"پس از تکمیل، اعلان دریافت خواهید کرد.",
        reply_markup=MAIN_MENU_KEYBOARD,
    )

"""
Technology handler — Phase 9
🔬 فناوری و تحقیقات

Callback prefixes owned here:
  tch_research         → special tech research catalog
  tch_item_{key}       → start researching a special tech
  tch_mytech           → show my technologies
  tch_upgrade          → show level upgrade menu
  tch_upgrade_now      → start level upgrade
  tch_active           → show active research queue
  tch_back_menu        → back to technology submenu
"""

from __future__ import annotations
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from models.player import Player
from services.technology_service import (
    SPECIAL_TECH_CATALOG,
    LEVEL_UPGRADES,
    MAX_LEVEL,
    get_active_research,
    get_tech_status,
    start_research,
    check_requirements,
)
from utils.keyboards import MAIN_MENU_KEYBOARD

SEP  = "━━━━━━━━━━━━━━"
SEP2 = "━━━━━━━━━━━━━━━━━━━━━━"

_NOT_REG = (
    "⚠️ ابتدا باید کشوری انتخاب کنید.\n"
    "دستور /start را بزنید."
)


# ── Sub-menu keyboard ─────────────────────────────────────────────────────────

def _tech_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔬 شروع تحقیق",           callback_data="tch_research")],
        [InlineKeyboardButton("📖 فناوری‌های من",        callback_data="tch_mytech")],
        [InlineKeyboardButton("📈 ارتقاء سطح فناوری",   callback_data="tch_upgrade")],
        [InlineKeyboardButton("🧪 تحقیقات فعال",         callback_data="tch_active")],
        [InlineKeyboardButton("⬅ بازگشت",                callback_data="menu_back")],
    ])


def _back_to_tech_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅ بازگشت به فناوری", callback_data="tch_back_menu")],
    ])


# ── Entry (called from menu.py) ───────────────────────────────────────────────

async def show_technology_menu(query, country_id: int) -> None:
    await query.message.reply_text(
        "🔬 فناوری و تحقیقات\n\n"
        "یک بخش را انتخاب کنید:",
        reply_markup=_tech_menu_keyboard(),
    )


# ── Main dispatcher ───────────────────────────────────────────────────────────

async def technology_callback_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data
    user = query.from_user

    player = Player.get(user.id)
    if not player or not player.is_registered:
        await query.message.reply_text(_NOT_REG, reply_markup=MAIN_MENU_KEYBOARD)
        return

    player.touch()
    country_id: int = player.country_id  # type: ignore[assignment]

    if data == "tch_back_menu":
        await show_technology_menu(query, country_id)
        return

    if data == "tch_research":
        await _show_research_catalog(query, country_id)
        return

    if data.startswith("tch_item_"):
        key = data[len("tch_item_"):]
        await _handle_start_special_research(query, country_id, key)
        return

    if data == "tch_mytech":
        await _show_my_technologies(query, country_id)
        return

    if data == "tch_upgrade":
        await _show_upgrade_menu(query, country_id)
        return

    if data == "tch_upgrade_now":
        await _handle_level_upgrade(query, country_id)
        return

    if data == "tch_active":
        await _show_active_research(query, country_id)
        return


# ── Research catalog ──────────────────────────────────────────────────────────

async def _show_research_catalog(query, country_id: int) -> None:
    status = get_tech_status(country_id)
    tech   = status["tech"]
    level  = int(tech.get("technology_level", 1))

    lines = [f"🔬 شروع تحقیق\n{SEP2}\n"]
    rows  = []

    for key, info in SPECIAL_TECH_CATALOG.items():
        col        = info["db_col"]
        is_unlocked = bool(tech.get(col, 0))
        tech_ok    = level >= info["tech_req"]

        if is_unlocked:
            status_str = "✅ فعال"
            lock       = " ✅"
        elif not tech_ok:
            status_str = f"🔒 نیاز: سطح {info['tech_req']}"
            lock       = " 🔒"
        else:
            status_str = "قابل تحقیق"
            lock       = ""

        lines.append(
            f"{info['name']}\n"
            f"   💰 {_fmt_price(info['price'])}  |  ⏱ {info['minutes']} دقیقه  |  {status_str}"
        )

        if not is_unlocked:
            rows.append([
                InlineKeyboardButton(
                    f"{info['name']}{lock}",
                    callback_data=f"tch_item_{key}",
                )
            ])

    rows.append([InlineKeyboardButton("⬅ بازگشت", callback_data="tch_back_menu")])

    await query.message.reply_text(
        "\n".join(lines),
        reply_markup=InlineKeyboardMarkup(rows),
    )


# ── Start special research ────────────────────────────────────────────────────

async def _handle_start_special_research(query, country_id: int, key: str) -> None:
    info = SPECIAL_TECH_CATALOG.get(key)
    if not info:
        await query.message.reply_text("❌ فناوری شناخته‌شده نیست.")
        return

    result = start_research(country_id, key, "special_tech")

    if not result["success"]:
        await query.message.reply_text(
            _research_error(result, info.get("name", key)),
            reply_markup=_back_to_tech_keyboard(),
        )
        return

    h, m   = divmod(info["minutes"], 60)
    t_str  = _fmt_duration(h, m)

    await query.message.reply_text(
        f"✅ تحقیق آغاز شد.\n\n"
        f"{SEP}\n\n"
        f"🔬 فناوری: {info['name']}\n"
        f"💡 تأثیر: {info['effect']}\n"
        f"💰 هزینه: {_fmt_price(result['cost'])}\n"
        f"⏱ مدت تحقیق: {t_str}\n"
        f"💵 بودجه باقی‌مانده: {_fmt_price(result['remaining'])}\n\n"
        f"⏳ در حال تحقیق\n\n"
        f"{SEP}",
        reply_markup=_back_to_tech_keyboard(),
    )


# ── My technologies ───────────────────────────────────────────────────────────

async def _show_my_technologies(query, country_id: int) -> None:
    status = get_tech_status(country_id)
    tech   = status["tech"]
    level  = int(tech.get("technology_level", 1))

    lines = [
        f"📖 فناوری‌های من\n{SEP2}\n",
        f"🔬 سطح فناوری فعلی: {level}\n",
    ]

    for key, info in SPECIAL_TECH_CATALOG.items():
        col        = info["db_col"]
        is_unlocked = bool(tech.get(col, 0))
        flag       = "✅ فعال" if is_unlocked else "❌ غیرفعال"
        lines.append(f"{info['name']}\n   {flag}")

    await query.message.reply_text(
        "\n".join(lines),
        reply_markup=_back_to_tech_keyboard(),
    )


# ── Level upgrade menu ────────────────────────────────────────────────────────

async def _show_upgrade_menu(query, country_id: int) -> None:
    status = get_tech_status(country_id)
    tech   = status["tech"]
    level  = int(tech.get("technology_level", 1))

    if level >= MAX_LEVEL:
        await query.message.reply_text(
            f"📈 ارتقاء سطح فناوری\n\n"
            f"🏆 شما به بالاترین سطح فناوری ({MAX_LEVEL}) رسیده‌اید!",
            reply_markup=_back_to_tech_keyboard(),
        )
        return

    target = level + 1
    info   = LEVEL_UPGRADES[target]
    h, m   = divmod(info["minutes"], 60)
    t_str  = _fmt_duration(h, m)

    # Check if already upgrading
    active = get_active_research(country_id)
    already = any(r["research_type"] == "level_upgrade" for r in active)

    if already:
        await query.message.reply_text(
            f"📈 ارتقاء سطح فناوری\n\n"
            f"⚠️ یک ارتقاء سطح در حال انجام است.\n"
            f"لطفاً پس از اتمام دوباره تلاش کنید.",
            reply_markup=_back_to_tech_keyboard(),
        )
        return

    await query.message.reply_text(
        f"📈 ارتقاء سطح فناوری\n{SEP2}\n\n"
        f"سطح فعلی: {level}\n"
        f"سطح بعدی: {target}\n\n"
        f"💰 هزینه: {_fmt_price(info['price'])}\n"
        f"⏱ زمان: {t_str}\n\n"
        f"آیا ارتقاء را تأیید می‌کنید؟",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ تأیید",  callback_data="tch_upgrade_now"),
                InlineKeyboardButton("❌ لغو",    callback_data="tch_back_menu"),
            ]
        ]),
    )


async def _handle_level_upgrade(query, country_id: int) -> None:
    status = get_tech_status(country_id)
    tech   = status["tech"]
    level  = int(tech.get("technology_level", 1))

    if level >= MAX_LEVEL:
        await query.message.reply_text("❌ شما به حداکثر سطح فناوری رسیده‌اید.")
        return

    target     = level + 1
    item_key   = f"level_{target}"
    result     = start_research(country_id, item_key, "level_upgrade")

    if not result["success"]:
        await query.message.reply_text(
            _research_error(result, f"ارتقاء سطح {target}"),
            reply_markup=_back_to_tech_keyboard(),
        )
        return

    info  = LEVEL_UPGRADES[target]
    h, m  = divmod(info["minutes"], 60)
    t_str = _fmt_duration(h, m)

    await query.message.reply_text(
        f"✅ ارتقاء سطح فناوری آغاز شد.\n\n"
        f"{SEP}\n\n"
        f"📈 سطح {level} → {target}\n"
        f"💰 هزینه: {_fmt_price(result['cost'])}\n"
        f"⏱ مدت: {t_str}\n"
        f"💵 بودجه باقی‌مانده: {_fmt_price(result['remaining'])}\n\n"
        f"⏳ در حال پیشرفت\n\n"
        f"{SEP}",
        reply_markup=_back_to_tech_keyboard(),
    )


# ── Active research queue ─────────────────────────────────────────────────────

async def _show_active_research(query, country_id: int) -> None:
    rows = get_active_research(country_id)

    if not rows:
        await query.message.reply_text(
            "🧪 تحقیقات فعال\n\n"
            "هیچ تحقیقی در حال انجام نیست.",
            reply_markup=_back_to_tech_keyboard(),
        )
        return

    now   = datetime.utcnow()
    lines = [f"🧪 تحقیقات فعال\n{SEP2}\n"]

    for r in rows:
        try:
            finish = datetime.strptime(r["finish_time"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            finish = now

        remaining_secs = max(0, int((finish - now).total_seconds()))
        lines.append(
            f"🔬 {r['item_name']}\n"
            f"⏳ {_fmt_remaining(remaining_secs)} باقی مانده\n"
            f"{SEP}"
        )

    await query.message.reply_text(
        "\n".join(lines),
        reply_markup=_back_to_tech_keyboard(),
    )


# ── Formatters ────────────────────────────────────────────────────────────────

def _fmt_price(price: float) -> str:
    if price >= 1_000_000_000_000:
        return f"{price / 1_000_000_000_000:g} تریلیون دلار"
    if price >= 1_000_000_000:
        return f"{price / 1_000_000_000:g} میلیارد دلار"
    if price >= 1_000_000:
        return f"{price / 1_000_000:g} میلیون دلار"
    return f"{price:,.0f} دلار"


def _fmt_duration(h: int, m: int) -> str:
    if h and m:
        return f"{h} ساعت و {m} دقیقه"
    if h:
        return f"{h} ساعت"
    return f"{m} دقیقه"


def _fmt_remaining(secs: int) -> str:
    if secs <= 0:
        return "تکمیل شده"
    h, rem = divmod(secs, 3600)
    m, s   = divmod(rem, 60)
    if h and m:
        return f"{h} ساعت و {m} دقیقه"
    if h:
        return f"{h} ساعت"
    if m:
        return f"{m} دقیقه"
    return f"{s} ثانیه"


def _research_error(result: dict, item_name: str) -> str:
    err = result.get("error")
    if err == "budget":
        return (
            f"❌ بودجه کافی نیست.\n\n"
            f"💸 هزینه: {_fmt_price(result.get('cost', 0))}\n"
            f"🏦 بودجه فعلی: {_fmt_price(result.get('budget', 0))}"
        )
    if err == "tech":
        return (
            f"❌ سطح فناوری کافی نیست.\n\n"
            f"🔬 نیاز: سطح {result.get('need', '?')}\n"
            f"📊 سطح فعلی: {result.get('have', '?')}"
        )
    if err == "already_unlocked":
        return f"✅ این فناوری قبلاً فعال شده است."
    if err == "duplicate":
        return f"⚠️ این تحقیق در حال انجام است."
    if err == "max_level":
        return f"🏆 شما به حداکثر سطح فناوری رسیده‌اید."
    if err == "wrong_target":
        return f"❌ امکان شروع تحقیق وجود ندارد."
    return "❌ امکان شروع تحقیق وجود ندارد."

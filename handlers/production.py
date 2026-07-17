"""
Production handler — Phase 8
🏭 کارخانه و تولید

Callback prefixes owned here:
  prd_build_factory  → factory catalog
  prd_factory_{key}  → buy/start building factory
  prd_equipment      → show available equipment (factories-gated)
  prd_item_{key}     → item detail card + ask for quantity
  prd_queue          → active production queue
  prd_myfactories    → owned factories + under-construction

Quantity input: pending_production in context.user_data;
picked up by handlers/input_router.py → production_quantity_handler().
"""

from __future__ import annotations
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from models.player import Player
from services.production_service import (
    FACTORY_CATALOG,
    PRODUCTION_CATALOG,
    build_factory,
    start_production,
    get_active_productions,
    get_owned_factories,
    check_technology,
)
from utils.keyboards import MAIN_MENU_KEYBOARD

SEP  = "━━━━━━━━━━━━━━"
SEP2 = "━━━━━━━━━━━━━━━━━━━━━━"

_NOT_REG = (
    "⚠️ ابتدا باید کشوری انتخاب کنید.\n"
    "دستور /start را بزنید."
)


# ── Sub-menu keyboard ─────────────────────────────────────────────────────────

def _production_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏗 ساخت کارخانه",       callback_data="prd_build_factory")],
        [InlineKeyboardButton("⚙ تولید تجهیزات",       callback_data="prd_equipment")],
        [InlineKeyboardButton("📦 صف تولید",            callback_data="prd_queue")],
        [InlineKeyboardButton("🏭 کارخانه‌های من",     callback_data="prd_myfactories")],
        [InlineKeyboardButton("⬅ بازگشت",              callback_data="menu_back")],
    ])


def _back_to_prod_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅ بازگشت به تولید", callback_data="prd_back_menu")],
    ])


# ── Entry (called from menu.py) ───────────────────────────────────────────────

async def show_production_menu(query, country_id: int) -> None:
    await query.message.reply_text(
        "🏭 کارخانه و تولید\n\n"
        "یک بخش را انتخاب کنید:",
        reply_markup=_production_menu_keyboard(),
    )


# ── Main dispatcher ───────────────────────────────────────────────────────────

async def production_callback_handler(
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

    if data == "prd_back_menu":
        await show_production_menu(query, country_id)
        return

    if data == "prd_build_factory":
        await _show_factory_catalog(query, country_id)
        return

    if data.startswith("prd_factory_"):
        key = data[len("prd_factory_"):]
        await _handle_build_factory(query, country_id, key)
        return

    if data == "prd_equipment":
        await _show_equipment_menu(query, country_id)
        return

    if data.startswith("prd_item_"):
        key = data[len("prd_item_"):]
        await _show_item_detail(query, context, key, country_id)
        return

    if data == "prd_queue":
        await _show_queue(query, country_id)
        return

    if data == "prd_myfactories":
        await _show_my_factories(query, country_id)
        return


# ── Factory catalog ───────────────────────────────────────────────────────────

async def _show_factory_catalog(query, country_id: int) -> None:
    rows = []
    for key, info in FACTORY_CATALOG.items():
        tech_ok, _ = check_technology(country_id, info["tech_req"])
        lock = "" if tech_ok else " 🔒"
        rows.append([
            InlineKeyboardButton(
                f"{info['name']}{lock}  |  {_fmt_price(info['price'])}",
                callback_data=f"prd_factory_{key}",
            )
        ])
    rows.append([InlineKeyboardButton("⬅ بازگشت", callback_data="prd_back_menu")])

    lines = [f"🏗 ساخت کارخانه\n{SEP2}\n"]
    for key, info in FACTORY_CATALOG.items():
        h, m = divmod(info["build_minutes"], 60)
        time_str = f"{h} ساعت" if m == 0 else f"{h} ساعت و {m} دقیقه" if h else f"{m} دقیقه"
        lines.append(
            f"{info['name']}\n"
            f"💰 {_fmt_price(info['price'])}  |  🔬 فناوری {info['tech_req']}  |  ⏱ {time_str}"
        )

    await query.message.reply_text(
        "\n".join(lines),
        reply_markup=InlineKeyboardMarkup(rows),
    )


async def _handle_build_factory(query, country_id: int, factory_key: str) -> None:
    info = FACTORY_CATALOG.get(factory_key)
    if not info:
        await query.message.reply_text("❌ کارخانه شناخته‌شده نیست.")
        return

    result = build_factory(country_id, factory_key)

    if not result["success"]:
        await query.message.reply_text(
            _factory_error(result, info),
            reply_markup=_back_to_prod_keyboard(),
        )
        return

    h, m   = divmod(info["build_minutes"], 60)
    t_str  = f"{h} ساعت" if m == 0 else f"{h} ساعت و {m} دقیقه" if h else f"{m} دقیقه"

    await query.message.reply_text(
        f"✅ ساخت کارخانه آغاز شد.\n\n"
        f"{SEP}\n\n"
        f"🏗 {info['name']}\n"
        f"💰 هزینه: {_fmt_price(result['cost'])}\n"
        f"⏱ زمان ساخت: {t_str}\n"
        f"💵 بودجه باقی‌مانده: {_fmt_price(result['remaining'])}\n\n"
        f"⏳ در حال ساخت\n\n"
        f"{SEP}",
        reply_markup=_back_to_prod_keyboard(),
    )


# ── Equipment menu ────────────────────────────────────────────────────────────

async def _show_equipment_menu(query, country_id: int) -> None:
    owned = {r["factory_type"] for r in get_owned_factories(country_id)}

    if not owned:
        await query.message.reply_text(
            "⚙ تولید تجهیزات\n\n"
            "❌ شما هنوز کارخانه‌ای ندارید.\n"
            "ابتدا یک کارخانه بسازید.",
            reply_markup=_back_to_prod_keyboard(),
        )
        return

    # Group available items by factory
    factory_order = ["military", "armor", "aircraft", "shipyard", "missile", "electronics"]
    sections: dict[str, list[tuple[str, dict]]] = {}
    for key, info in PRODUCTION_CATALOG.items():
        ft = info["factory"]
        if ft in owned:
            sections.setdefault(ft, []).append((key, info))

    # Build text + buttons
    lines  = [f"⚙ تولید تجهیزات\n{SEP2}\n"]
    rows   = []
    for ft in factory_order:
        items = sections.get(ft)
        if not items:
            continue
        fac_name = FACTORY_CATALOG.get(ft, {}).get("name", ft)
        lines.append(f"\n{fac_name}")
        for key, info in items:
            ppu = info["price_per_unit"]
            mpu = info["minutes_per_unit"]
            lines.append(
                f"  {info['name']}\n"
                f"     💰 {_fmt_price(ppu)} / واحد  |  ⏱ {mpu} دقیقه / واحد"
            )
            rows.append([
                InlineKeyboardButton(
                    info["name"],
                    callback_data=f"prd_item_{key}",
                )
            ])

    rows.append([InlineKeyboardButton("⬅ بازگشت", callback_data="prd_back_menu")])

    await query.message.reply_text(
        "\n".join(lines),
        reply_markup=InlineKeyboardMarkup(rows),
    )


async def _show_item_detail(
    query, context: ContextTypes.DEFAULT_TYPE, key: str, country_id: int
) -> None:
    info = PRODUCTION_CATALOG.get(key)
    if not info:
        await query.message.reply_text("❌ تجهیز شناخته‌شده نیست.")
        return

    # Store pending state for input_router
    context.user_data["pending_production"] = {
        "prod_key":   key,
        "country_id": country_id,
    }

    fac_name = FACTORY_CATALOG.get(info["factory"], {}).get("name", info["factory"])

    await query.message.reply_text(
        f"{info['name']}\n\n"
        f"{SEP}\n\n"
        f"🏭 کارخانه: {fac_name}\n"
        f"💰 قیمت واحد: {_fmt_price(info['price_per_unit'])}\n"
        f"⏱ زمان تولید: {info['minutes_per_unit']} دقیقه / واحد\n\n"
        f"{SEP}\n\n"
        f"🔢 تعداد را وارد کنید."
    )


# ── Production queue ──────────────────────────────────────────────────────────

async def _show_queue(query, country_id: int) -> None:
    rows = get_active_productions(country_id)

    if not rows:
        await query.message.reply_text(
            "📦 صف تولید\n\n"
            "هیچ موردی در صف تولید نیست.",
            reply_markup=_back_to_prod_keyboard(),
        )
        return

    now = datetime.utcnow()
    lines = [f"📦 صف تولید\n{SEP2}\n"]

    for r in rows:
        try:
            finish = datetime.strptime(r["finish_time"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            finish = now

        remaining_secs = max(0, int((finish - now).total_seconds()))
        time_str       = _fmt_remaining(remaining_secs)
        qty_str        = f"×{r['quantity']}" if r["queue_type"] == "equipment" else ""

        lines.append(
            f"{r['item_name']} {qty_str}\n"
            f"⏳ {time_str} باقی مانده\n"
            f"{SEP}"
        )

    await query.message.reply_text(
        "\n".join(lines),
        reply_markup=_back_to_prod_keyboard(),
    )


# ── My factories ──────────────────────────────────────────────────────────────

async def _show_my_factories(query, country_id: int) -> None:
    owned = get_owned_factories(country_id)
    active = get_active_productions(country_id)

    # Filter only factory-type productions
    under_construction = [r for r in active if r["queue_type"] == "factory"]

    if not owned and not under_construction:
        await query.message.reply_text(
            "🏭 کارخانه‌های من\n\n"
            "شما هنوز کارخانه‌ای ندارید.",
            reply_markup=_back_to_prod_keyboard(),
        )
        return

    now = datetime.utcnow()
    lines = [f"🏭 کارخانه‌های من\n{SEP2}\n"]

    # Completed factories
    if owned:
        lines.append("✅ کارخانه‌های فعال:\n")
        for r in owned:
            fac = FACTORY_CATALOG.get(r["factory_type"], {})
            name = fac.get("name", r["factory_type"])
            lines.append(f"{name} ×{r['count']}")

    # Under construction
    if under_construction:
        lines.append(f"\n🏗 در حال ساخت:\n")
        for r in under_construction:
            try:
                finish = datetime.strptime(r["finish_time"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                finish = now
            remaining_secs = max(0, int((finish - now).total_seconds()))
            lines.append(
                f"{r['item_name']}\n"
                f"⏳ در حال ساخت — {_fmt_remaining(remaining_secs)} باقی مانده"
            )

    await query.message.reply_text(
        "\n".join(lines),
        reply_markup=_back_to_prod_keyboard(),
    )


# ── Quantity message handler (called by input_router) ─────────────────────────

async def production_quantity_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    pending = context.user_data.get("pending_production")
    if not pending:
        return

    text = (update.message.text or "").strip()

    if not text.isdigit() or int(text) == 0:
        await update.message.reply_text(
            "⚠️ لطفاً یک عدد صحیح بزرگ‌تر از صفر وارد کنید.\n"
            "برای لغو به منوی اصلی بازگردید.",
            reply_markup=MAIN_MENU_KEYBOARD,
        )
        context.user_data.pop("pending_production", None)
        return

    quantity   = int(text)
    prod_key   = pending["prod_key"]
    country_id = pending["country_id"]
    context.user_data.pop("pending_production", None)

    result = start_production(country_id, prod_key, quantity)

    if not result["success"]:
        await update.message.reply_text(
            _prod_error(result),
            reply_markup=MAIN_MENU_KEYBOARD,
        )
        return

    info  = PRODUCTION_CATALOG[prod_key]
    h, m  = divmod(result["minutes"], 60)
    t_str = f"{h} ساعت و {m} دقیقه" if h and m else (f"{h} ساعت" if h else f"{m} دقیقه")

    await update.message.reply_text(
        f"✅ سفارش تولید ثبت شد.\n\n"
        f"{SEP}\n\n"
        f"📦 تجهیز: {result['name']}\n"
        f"🔢 تعداد: {result['quantity']:,}\n"
        f"💰 هزینه کل: {_fmt_price(result['total_cost'])}\n"
        f"⏱ زمان تولید: {t_str}\n"
        f"💵 بودجه باقی‌مانده: {_fmt_price(result['remaining'])}\n\n"
        f"⏳ در حال تولید\n\n"
        f"{SEP}",
        reply_markup=MAIN_MENU_KEYBOARD,
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


def _factory_error(result: dict, info: dict) -> str:
    err = result.get("error")
    if err == "budget":
        return (
            f"❌ بودجه کافی نیست.\n\n"
            f"💰 هزینه: {_fmt_price(result['cost'])}\n"
            f"🏦 بودجه فعلی: {_fmt_price(result['budget'])}"
        )
    if err == "tech":
        return (
            f"❌ سطح فناوری کافی نیست.\n\n"
            f"🔬 نیاز: سطح {result['need']}\n"
            f"📊 سطح فعلی: {result['have']}"
        )
    return "❌ خطای نامشخص."


def _prod_error(result: dict) -> str:
    err = result.get("error")
    if err == "no_factory":
        return (
            f"❌ کارخانه مورد نیاز ندارید.\n\n"
            f"🏭 نیاز: {result.get('factory_name', '—')}\n"
            f"ابتدا این کارخانه را بسازید."
        )
    if err == "budget":
        return (
            f"❌ بودجه کافی نیست.\n\n"
            f"💸 هزینه کل: {_fmt_price(result['cost'])}\n"
            f"🏦 بودجه فعلی: {_fmt_price(result['budget'])}"
        )
    if err == "qty_zero":
        return "❌ تعداد باید بیشتر از صفر باشد."
    return "❌ خطای نامشخص."

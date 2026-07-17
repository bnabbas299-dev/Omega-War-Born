"""
Market handler — Phase 7 (Persian Edition)
All text in Persian. Inline keyboard throughout.

Callback prefixes owned by this handler:
  mkt_cat_{category}   — show items in a category
  mkt_item_{key}       — show item detail + prompt for quantity
  mkt_back_cats        — back to category list

Quantity input: user_data["pending_market"] tracks the pending purchase;
quantity_message_handler() in main.py intercepts the user's reply.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from models.player import Player
from services.market_service import (
    MARKET_CATALOG,
    CATEGORIES,
    buy_item,
)
from utils.keyboards import MAIN_MENU_KEYBOARD

SEP = "━━━━━━━━━━━━━━"

_NOT_REG = (
    "⚠️ ابتدا باید کشوری انتخاب کنید.\n"
    "دستور /start را بزنید."
)


# ── Keyboards ─────────────────────────────────────────────────────────────────

def _category_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(label, callback_data=f"mkt_cat_{cat}")]
        for cat, label in CATEGORIES.items()
    ]
    rows.append([InlineKeyboardButton("⬅ بازگشت", callback_data="menu_back")])
    return InlineKeyboardMarkup(rows)


def _items_keyboard(category: str) -> InlineKeyboardMarkup:
    items = [
        (key, info)
        for key, info in MARKET_CATALOG.items()
        if info["category"] == category
    ]
    rows = []
    # Two items per row
    for i in range(0, len(items), 2):
        pair = items[i : i + 2]
        rows.append([
            InlineKeyboardButton(info["name"], callback_data=f"mkt_item_{key}")
            for key, info in pair
        ])
    rows.append([
        InlineKeyboardButton("⬅ بازگشت به دسته‌ها", callback_data="mkt_back_cats")
    ])
    return InlineKeyboardMarkup(rows)


# ── Entry (called from menu.py) ───────────────────────────────────────────────

async def show_market(query, country_id: int) -> None:
    await query.message.reply_text(
        "🛒 فروشگاه جهانی MBN\n\n"
        "یک دسته را انتخاب کنید:",
        reply_markup=_category_keyboard(),
    )


# ── Main callback dispatcher ──────────────────────────────────────────────────

async def market_callback_handler(
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

    # ── Back to categories ────────────────────────────────────────────────────
    if data == "mkt_back_cats":
        await query.message.reply_text(
            "🛒 فروشگاه جهانی MBN\n\nیک دسته را انتخاب کنید:",
            reply_markup=_category_keyboard(),
        )
        return

    # ── Category selected ─────────────────────────────────────────────────────
    if data.startswith("mkt_cat_"):
        cat = data[len("mkt_cat_"):]
        await _show_category(query, cat)
        return

    # ── Item selected ─────────────────────────────────────────────────────────
    if data.startswith("mkt_item_"):
        key = data[len("mkt_item_"):]
        await _show_item(query, context, key, country_id)
        return


# ── Category listing ──────────────────────────────────────────────────────────

async def _show_category(query, category: str) -> None:
    label = CATEGORIES.get(category)
    if not label:
        await query.message.reply_text("❌ دسته‌بندی نامعتبر است.")
        return

    items = [
        (key, info)
        for key, info in MARKET_CATALOG.items()
        if info["category"] == category
    ]

    # Build summary list
    lines = [f"{label}\n{SEP}\n"]
    for key, info in items:
        lines.append(
            f"{info['name']}\n"
            f"   💰 {_fmt_price(info['price'])}"
            f"   |   🔬 فناوری {info['tech_req']}"
        )

    await query.message.reply_text(
        "\n".join(lines),
        reply_markup=_items_keyboard(category),
    )


# ── Item detail ───────────────────────────────────────────────────────────────

async def _show_item(
    query,
    context: ContextTypes.DEFAULT_TYPE,
    key: str,
    country_id: int,
) -> None:
    info = MARKET_CATALOG.get(key)
    if not info:
        await query.message.reply_text("❌ تجهیزات شناخته‌شده نیست.")
        return

    # Store pending state — quantity_message_handler will pick it up
    context.user_data["pending_market"] = {
        "item_key":   key,
        "country_id": country_id,
    }

    tech_text = f"سطح {info['tech_req']}" if info["tech_req"] > 0 else "بدون نیاز"

    await query.message.reply_text(
        f"{info['name']}\n\n"
        f"{SEP}\n\n"
        f"💰 قیمت واحد: {_fmt_price(info['price'])}\n"
        f"🔬 نیاز فناوری: {tech_text}\n\n"
        f"{SEP}\n\n"
        f"🔢 تعداد مورد نیاز را وارد کنید."
    )


# ── Quantity message handler (registered in main.py) ─────────────────────────

async def quantity_message_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Fires on every plain-text message.
    Only acts when user_data["pending_market"] is set.
    """
    pending = context.user_data.get("pending_market")
    if not pending:
        return

    text = (update.message.text or "").strip()

    if not text.isdigit() or int(text) == 0:
        await update.message.reply_text(
            "⚠️ لطفاً یک عدد صحیح بزرگ‌تر از صفر وارد کنید.\n"
            "برای لغو به منوی اصلی بازگردید.",
            reply_markup=MAIN_MENU_KEYBOARD,
        )
        context.user_data.pop("pending_market", None)
        return

    quantity   = int(text)
    item_key   = pending["item_key"]
    country_id = pending["country_id"]

    # Clear state before DB call to prevent double-submit
    context.user_data.pop("pending_market", None)

    result = buy_item(country_id, item_key, quantity)

    if not result["success"]:
        await update.message.reply_text(
            _error_text(result),
            reply_markup=MAIN_MENU_KEYBOARD,
        )
        return

    await update.message.reply_text(
        _receipt(result),
        reply_markup=MAIN_MENU_KEYBOARD,
    )


# ── Text helpers ──────────────────────────────────────────────────────────────

def _fmt_price(price: float) -> str:
    if price >= 1_000_000_000_000:
        return f"{price / 1_000_000_000_000:g} تریلیون دلار"
    if price >= 1_000_000_000:
        return f"{price / 1_000_000_000:g} میلیارد دلار"
    if price >= 1_000_000:
        return f"{price / 1_000_000:g} میلیون دلار"
    return f"{price:,.0f} دلار"


def _error_text(result: dict) -> str:
    err = result.get("error")
    if err == "budget":
        return (
            "❌ بودجه کافی نیست.\n\n"
            f"💸 هزینه کل: {result['total_cost']:,.0f} دلار\n"
            f"🏦 بودجه فعلی: {result['budget']:,.0f} دلار"
        )
    if err == "tech":
        return (
            "❌ سطح فناوری شما کافی نیست.\n\n"
            f"🔬 نیاز: سطح {result['need']}\n"
            f"📊 سطح فعلی: {result['have']}"
        )
    if err == "qty_zero":
        return "❌ تعداد باید بیشتر از صفر باشد."
    return "❌ خطای نامشخص. لطفاً دوباره تلاش کنید."


def _receipt(r: dict) -> str:
    return (
        f"✅ خرید با موفقیت انجام شد.\n\n"
        f"{SEP}\n\n"
        f"📦 تجهیز: {r['name']}\n"
        f"🔢 تعداد: {r['quantity']:,}\n"
        f"💰 هزینه کل: {r['total_cost']:,.0f} دلار\n"
        f"💵 بودجه باقی‌مانده: {r['remaining']:,.0f} دلار\n\n"
        f"{SEP}"
    )

"""
Market handler — Phase 7
MBN Global Market: category browsing, item selection, quantity input, purchase flow.

Callback flow:
  menu_market          → category keyboard
  mkt_cat_{cat}        → items in category
  mkt_item_{key}       → item detail card + "enter quantity" prompt
  [user types number]  → quantity_message_handler processes the purchase
  mkt_back_cats        → back to category list
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

SEP = "━━━━━━━━━━━━━━━━━━━━━━"

_NOT_REGISTERED = (
    "⚠️ شما هنوز کشوری انتخاب نکرده‌اید.\n"
    "لطفاً ابتدا /start را بزنید."
)


# ── Keyboards ─────────────────────────────────────────────────────────────────

def _categories_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(meta["label"], callback_data=meta["callback"])]
        for meta in CATEGORIES.values()
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
    for i in range(0, len(items), 2):
        pair = items[i:i + 2]
        rows.append([
            InlineKeyboardButton(
                f"{info['emoji']} {info['name_en']}",
                callback_data=f"mkt_item_{key}",
            )
            for key, info in pair
        ])
    rows.append([InlineKeyboardButton("⬅ بازگشت به دسته‌ها", callback_data="mkt_back_cats")])
    return InlineKeyboardMarkup(rows)


# ── Entry point (called from menu.py) ────────────────────────────────────────

async def show_market(query, country_id: int) -> None:
    await query.message.reply_text(
        "🛒 فروشگاه جهانی MBN\n\n"
        "یک دسته را انتخاب کنید:",
        reply_markup=_categories_keyboard(),
    )


# ── Callback dispatcher ───────────────────────────────────────────────────────

async def market_callback_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data
    user = query.from_user

    player = Player.get(user.id)
    if not player or not player.is_registered:
        await query.message.reply_text(_NOT_REGISTERED, reply_markup=MAIN_MENU_KEYBOARD)
        return

    player.touch()
    country_id: int = player.country_id  # type: ignore[assignment]

    # ── Back to categories ────────────────────────────────────────────────────
    if data == "mkt_back_cats":
        await query.message.reply_text(
            "🛒 فروشگاه جهانی MBN\n\nیک دسته را انتخاب کنید:",
            reply_markup=_categories_keyboard(),
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


# ── Private helpers ───────────────────────────────────────────────────────────

async def _show_category(query, category: str) -> None:
    if category == "factories":
        await query.message.reply_text(
            "🏗 Factories\n\n🔧 این دسته به زودی اضافه می‌شود.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅ بازگشت به دسته‌ها", callback_data="mkt_back_cats")]
            ]),
        )
        return

    cat_meta = CATEGORIES.get(category)
    if not cat_meta:
        return

    items = [
        (key, info)
        for key, info in MARKET_CATALOG.items()
        if info["category"] == category
    ]
    if not items:
        await query.message.reply_text(
            f"{cat_meta['label']}\n\nدر این دسته موردی یافت نشد.",
            reply_markup=_categories_keyboard(),
        )
        return

    # Build item list as text
    lines = [f"{cat_meta['label']}\n\n{SEP}\n"]
    for key, info in items:
        price_fmt = _fmt_price(info["price"])
        lines.append(
            f"{info['emoji']} {info['name_en']}\n"
            f"   💰 {price_fmt}  |  🔬 Tech {info['tech_req']}"
        )

    await query.message.reply_text(
        "\n".join(lines),
        reply_markup=_items_keyboard(category),
    )


async def _show_item(query, context: ContextTypes.DEFAULT_TYPE, key: str, country_id: int) -> None:
    info = MARKET_CATALOG.get(key)
    if not info:
        await query.message.reply_text("❌ مورد شناخته‌شده نیست.")
        return

    price_fmt = _fmt_price(info["price"])
    tech_text = f"سطح {info['tech_req']}" if info["tech_req"] > 0 else "بدون نیاز"

    # Save pending state so the message handler knows what's being bought
    context.user_data["pending_market"] = {
        "item_key":   key,
        "country_id": country_id,
    }

    await query.message.reply_text(
        f"{info['emoji']} {info['name_fa']}  ({info['name_en']})\n\n"
        f"{SEP}\n\n"
        f"💰 قیمت واحد: {price_fmt}\n"
        f"🔬 نیاز فناوری: {tech_text}\n\n"
        f"{SEP}\n\n"
        f"📦 چند واحد می‌خواهید بخرید؟\n"
        f"عدد را تایپ کنید:"
    )


# ── Quantity message handler (registered in main.py) ─────────────────────────

async def quantity_message_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Intercepts plain-text messages when a market purchase is pending.
    Validates the quantity, runs buy_item(), sends the receipt.
    """
    pending = context.user_data.get("pending_market")
    if not pending:
        return  # Not a market reply — ignore

    text = (update.message.text or "").strip()
    if not text.isdigit():
        await update.message.reply_text(
            "⚠️ لطفاً یک عدد صحیح وارد کنید.\nخرید لغو شد.",
            reply_markup=MAIN_MENU_KEYBOARD,
        )
        context.user_data.pop("pending_market", None)
        return

    quantity = int(text)
    item_key   = pending["item_key"]
    country_id = pending["country_id"]

    # Clear state before processing
    context.user_data.pop("pending_market", None)

    result = buy_item(country_id, item_key, quantity)

    if not result["success"]:
        await update.message.reply_text(
            result["message"],
            reply_markup=MAIN_MENU_KEYBOARD,
        )
        return

    receipt = _build_receipt(result)
    await update.message.reply_text(receipt, reply_markup=MAIN_MENU_KEYBOARD)


# ── Formatters ────────────────────────────────────────────────────────────────

def _fmt_price(price: float) -> str:
    if price >= 1_000_000_000:
        b = price / 1_000_000_000
        return f"{b:g} میلیارد دلار"
    if price >= 1_000_000:
        m = price / 1_000_000
        return f"{m:g} میلیون دلار"
    return f"{price:,.0f} دلار"


def _build_receipt(result: dict) -> str:
    return (
        f"{SEP}\n\n"
        f"✅ خرید موفق!\n\n"
        f"📦 تجهیزات: {result['name']}\n"
        f"🔢 تعداد: {result['quantity']:,}\n"
        f"💰 قیمت واحد: {_fmt_price(result['unit_price'])}\n"
        f"💵 هزینه کل: {result['total_cost']:,.0f} دلار\n"
        f"🏦 بودجه باقی‌مانده: {result['remaining']:,.0f} دلار\n\n"
        f"{SEP}"
    )

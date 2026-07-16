"""
Main menu dispatcher.
Routes every menu_ callback to the correct section.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from models.player import Player
from models.country import Country
from utils.keyboards import MAIN_MENU_KEYBOARD, COUNTRY_KEYBOARD
from utils.panel_builder import build_country_panel

_NOT_REGISTERED = (
    "⚠️ شما هنوز کشوری انتخاب نکرده‌اید.\n"
    "لطفاً ابتدا /start را بزنید."
)
_COMING_SOON = "🔧 این بخش به زودی پیاده‌سازی می‌شود."

BACK_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("⬅ بازگشت به منوی اصلی", callback_data="menu_back")],
])


async def menu_callback_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data
    user = query.from_user

    # ── Back to menu ─────────────────────────────────────────────────────────
    if data == "menu_back":
        await query.message.reply_text("🎮 منوی اصلی:", reply_markup=MAIN_MENU_KEYBOARD)
        return

    # ── Select country ───────────────────────────────────────────────────────
    if data == "menu_select_country":
        player = Player.get(user.id)
        if player and player.is_registered:
            await query.message.reply_text(
                "✅ شما قبلاً کشوری انتخاب کرده‌اید.", reply_markup=MAIN_MENU_KEYBOARD
            )
        else:
            await query.message.reply_text(
                "🌍 لطفاً کشور خود را انتخاب کنید:", reply_markup=COUNTRY_KEYBOARD
            )
        return

    # ── All other sections require registration ──────────────────────────────
    player = Player.get(user.id)
    if not player or not player.is_registered:
        await query.message.reply_text(_NOT_REGISTERED, reply_markup=MAIN_MENU_KEYBOARD)
        return

    player.touch()

    # ── Enter game ───────────────────────────────────────────────────────────
    if data == "menu_enter":
        country = Country.get_by_id(player.country_id)  # type: ignore[arg-type]
        name = country.country_name if country else "—"
        await query.message.reply_text(
            f"🎮 وارد بازی شدید.\n🏛 کشور فعال: {name}",
            reply_markup=MAIN_MENU_KEYBOARD,
        )

    # ── Country panel ─────────────────────────────────────────────────────────
    elif data == "menu_country_panel":
        await _send_country_panel(query, player.country_id)  # type: ignore[arg-type]

    # ── Placeholder sections ──────────────────────────────────────────────────
    elif data == "menu_economy":
        await query.message.reply_text(f"💰 اقتصاد\n\n{_COMING_SOON}", reply_markup=MAIN_MENU_KEYBOARD)
    elif data == "menu_industry":
        await query.message.reply_text(f"🏭 صنعت\n\n{_COMING_SOON}", reply_markup=MAIN_MENU_KEYBOARD)
    elif data == "menu_market":
        await query.message.reply_text(f"🛒 فروشگاه جهانی\n\n{_COMING_SOON}", reply_markup=MAIN_MENU_KEYBOARD)
    elif data == "menu_military":
        await query.message.reply_text(f"🪖 ارتش\n\n{_COMING_SOON}", reply_markup=MAIN_MENU_KEYBOARD)
    elif data == "menu_operations":
        await query.message.reply_text(f"⚔️ عملیات نظامی\n\n{_COMING_SOON}", reply_markup=MAIN_MENU_KEYBOARD)
    elif data == "menu_diplomacy":
        await query.message.reply_text(f"🤝 دیپلماسی\n\n{_COMING_SOON}", reply_markup=MAIN_MENU_KEYBOARD)
    elif data == "menu_technology":
        await query.message.reply_text(f"🔬 فناوری\n\n{_COMING_SOON}", reply_markup=MAIN_MENU_KEYBOARD)
    elif data == "menu_news":
        await query.message.reply_text(f"📰 اخبار جهان\n\n{_COMING_SOON}", reply_markup=MAIN_MENU_KEYBOARD)
    elif data == "menu_leaderboard":
        await query.message.reply_text(f"🏆 رتبه‌بندی\n\n{_COMING_SOON}", reply_markup=MAIN_MENU_KEYBOARD)


# ── Country panel helper ──────────────────────────────────────────────────────

async def _send_country_panel(query, country_id: int) -> None:
    """Load all country data from SQLite and send the full panel."""
    country   = Country.get_by_id(country_id)
    eco       = Country.get_economy(country_id)
    buildings = Country.get_buildings(country_id)
    resources = Country.get_resources(country_id)
    technology = Country.get_technology(country_id)
    military  = Country.get_military(country_id)
    alliances = Country.get_alliance_names(country_id)

    if not country:
        await query.message.reply_text(
            "❌ اطلاعات کشور یافت نشد.", reply_markup=MAIN_MENU_KEYBOARD
        )
        return

    messages = build_country_panel(
        country, eco, buildings, resources, technology, military, alliances
    )

    # Send all sections; attach the back button only to the last message
    for i, text in enumerate(messages):
        is_last = (i == len(messages) - 1)
        await query.message.reply_text(
            text,
            reply_markup=BACK_BUTTON if is_last else None,
        )

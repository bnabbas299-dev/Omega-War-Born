"""
Main menu dispatcher.
Routes menu_ callbacks to the appropriate section message.
"""

from telegram import Update
from telegram.ext import ContextTypes

from models.player import Player
from utils.keyboards import MAIN_MENU_KEYBOARD

_NOT_REGISTERED = "لطفاً ابتدا /start را بزنید و کشور خود را انتخاب کنید."

# Map callback_data → (display title, emoji)
_SECTION_MAP = {
    "menu_profile":     ("پروفایل",      "🏠"),
    "menu_economy":     ("اقتصاد",       "🏦"),
    "menu_buildings":   ("ساختمان‌ها",   "🏗"),
    "menu_military":    ("ارتش",         "🪖"),
    "menu_market":      ("بازار",        "🛒"),
    "menu_diplomacy":   ("دیپلماسی",    "🤝"),
    "menu_research":    ("تحقیقات",      "🔬"),
    "menu_war":         ("جنگ",          "⚔️"),
    "menu_events":      ("رویدادها",     "📰"),
    "menu_leaderboard": ("رتبه‌بندی",    "🏆"),
    "menu_map":         ("نقشه جهان",    "🌍"),
    "menu_settings":    ("تنظیمات",      "⚙️"),
}


async def menu_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    user = query.from_user
    player = Player.get(user.id)

    if not player or not player.is_registered:
        await query.message.reply_text(_NOT_REGISTERED)
        return

    data = query.data

    if data == "menu_back":
        await query.message.reply_text(
            "🎮 منوی اصلی:", reply_markup=MAIN_MENU_KEYBOARD
        )
        return

    section = _SECTION_MAP.get(data)
    if not section:
        return

    title, emoji = section
    await query.message.reply_text(
        f"{emoji} بخش {title} به زودی پیاده‌سازی می‌شود.",
        reply_markup=MAIN_MENU_KEYBOARD,
    )

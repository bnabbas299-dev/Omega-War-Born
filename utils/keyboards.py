"""
All InlineKeyboardMarkup definitions.
Add new keyboards here as new systems are implemented.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# ── Country selection ────────────────────────────────────────────────────────

COUNTRY_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🇮🇷 ایران",    callback_data="country_iran"),
        InlineKeyboardButton("🇺🇸 آمریکا",   callback_data="country_usa"),
    ],
    [
        InlineKeyboardButton("🇷🇺 روسیه",   callback_data="country_russia"),
        InlineKeyboardButton("🇮🇱 اسرائیل", callback_data="country_israel"),
    ],
])

# ── Main game menu ───────────────────────────────────────────────────────────

MAIN_MENU_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🎮 ورود به بازی",      callback_data="menu_enter"),
        InlineKeyboardButton("🌍 انتخاب کشور",       callback_data="menu_select_country"),
    ],
    [
        InlineKeyboardButton("🏛 پنل کشور",          callback_data="menu_country_panel"),
        InlineKeyboardButton("💰 اقتصاد",             callback_data="menu_economy"),
    ],
    [
        InlineKeyboardButton("🏭 صنعت",              callback_data="menu_industry"),
        InlineKeyboardButton("🛒 فروشگاه جهانی",    callback_data="menu_market"),
    ],
    [
        InlineKeyboardButton("🪖 ارتش",              callback_data="menu_military"),
        InlineKeyboardButton("⚔️ عملیات نظامی",      callback_data="menu_operations"),
    ],
    [
        InlineKeyboardButton("🤝 دیپلماسی",         callback_data="menu_diplomacy"),
        InlineKeyboardButton("🔬 فناوری",            callback_data="menu_technology"),
    ],
    [
        InlineKeyboardButton("📰 اخبار جهان",        callback_data="menu_news"),
        InlineKeyboardButton("🏆 رتبه‌بندی",         callback_data="menu_leaderboard"),
    ],
])

# ── Back to main menu ────────────────────────────────────────────────────────

BACK_TO_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 بازگشت به منو", callback_data="menu_back")],
])

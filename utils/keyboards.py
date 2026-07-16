"""
All InlineKeyboardMarkup definitions for the bot.
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
        InlineKeyboardButton("🏠 پروفایل",    callback_data="menu_profile"),
        InlineKeyboardButton("🏦 اقتصاد",     callback_data="menu_economy"),
    ],
    [
        InlineKeyboardButton("🏗 ساختمان‌ها", callback_data="menu_buildings"),
        InlineKeyboardButton("🪖 ارتش",       callback_data="menu_military"),
    ],
    [
        InlineKeyboardButton("🛒 بازار",      callback_data="menu_market"),
        InlineKeyboardButton("🤝 دیپلماسی",  callback_data="menu_diplomacy"),
    ],
    [
        InlineKeyboardButton("🔬 تحقیقات",    callback_data="menu_research"),
        InlineKeyboardButton("⚔️ جنگ",        callback_data="menu_war"),
    ],
    [
        InlineKeyboardButton("📰 رویدادها",   callback_data="menu_events"),
        InlineKeyboardButton("🏆 رتبه‌بندی",  callback_data="menu_leaderboard"),
    ],
    [
        InlineKeyboardButton("🌍 نقشه جهان",  callback_data="menu_map"),
        InlineKeyboardButton("⚙️ تنظیمات",    callback_data="menu_settings"),
    ],
])

# ── Back button (reusable) ───────────────────────────────────────────────────

BACK_TO_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 بازگشت به منو", callback_data="menu_back")],
])

# ── Country name map ─────────────────────────────────────────────────────────

COUNTRY_NAMES: dict[str, str] = {
    "country_iran":   "🇮🇷 ایران",
    "country_usa":    "🇺🇸 آمریکا",
    "country_russia": "🇷🇺 روسیه",
    "country_israel": "🇮🇱 اسرائیل",
}

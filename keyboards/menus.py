from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Country selection (shown at /start)
COUNTRY_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🇮🇷 ایران", callback_data="country_iran"),
        InlineKeyboardButton("🇺🇸 آمریکا", callback_data="country_usa"),
    ],
    [
        InlineKeyboardButton("🇷🇺 روسیه", callback_data="country_russia"),
        InlineKeyboardButton("🇮🇱 اسرائیل", callback_data="country_israel"),
    ],
])

# Main game menu (shown after registration)
MAIN_MENU_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🏠 پروفایل", callback_data="menu_profile"),
        InlineKeyboardButton("🏦 اقتصاد",  callback_data="menu_economy"),
    ],
    [
        InlineKeyboardButton("🪖 ارتش",    callback_data="menu_army"),
        InlineKeyboardButton("🤝 اتحاد",   callback_data="menu_alliance"),
    ],
    [
        InlineKeyboardButton("📰 اخبار",   callback_data="menu_news"),
        InlineKeyboardButton("🌍 نقشه جهان", callback_data="menu_map"),
    ],
    [
        InlineKeyboardButton("⚙ تنظیمات", callback_data="menu_settings"),
    ],
])

# Human-readable country names
COUNTRY_NAMES: dict[str, str] = {
    "country_iran":   "🇮🇷 ایران",
    "country_usa":    "🇺🇸 آمریکا",
    "country_russia": "🇷🇺 روسیه",
    "country_israel": "🇮🇱 اسرائیل",
}

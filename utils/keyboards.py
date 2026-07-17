"""
All InlineKeyboardMarkup definitions.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from services.building_service import CATALOG

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
        InlineKeyboardButton("🌅 پایان روز",              callback_data="menu_end_day"),
    ],
    [
        InlineKeyboardButton("🎮 ورود به بازی",            callback_data="menu_enter"),
        InlineKeyboardButton("🌍 انتخاب کشور",             callback_data="menu_select_country"),
    ],
    [
        InlineKeyboardButton("🏛 پنل کشور",                callback_data="menu_country_panel"),
        InlineKeyboardButton("💰 اقتصاد",                   callback_data="menu_economy"),
    ],
    [
        InlineKeyboardButton("🏗 ساخت‌وساز",              callback_data="menu_construction"),
        InlineKeyboardButton("📋 پروژه‌های در حال ساخت",  callback_data="menu_queue"),
    ],
    [
        InlineKeyboardButton("🏭 کارخانه و تولید",        callback_data="menu_production"),
        InlineKeyboardButton("🛒 فروشگاه جهانی",          callback_data="menu_market"),
    ],
    [
        InlineKeyboardButton("🪖 ارتش",                    callback_data="menu_military"),
        InlineKeyboardButton("⚔️ عملیات نظامی",            callback_data="menu_operations"),
    ],
    [
        InlineKeyboardButton("🤝 دیپلماسی",               callback_data="menu_diplomacy"),
        InlineKeyboardButton("🔬 فناوری و تحقیقات",      callback_data="menu_technology"),
    ],
    [
        InlineKeyboardButton("📰 اخبار جهان",              callback_data="menu_news"),
        InlineKeyboardButton("🏆 رتبه‌بندی",               callback_data="menu_leaderboard"),
    ],
])

# ── Back to main menu ────────────────────────────────────────────────────────

BACK_TO_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("⬅ بازگشت به منوی اصلی", callback_data="menu_back")],
])


# ── Building list keyboard (generated from catalog) ──────────────────────────

def building_list_keyboard() -> InlineKeyboardMarkup:
    keys   = list(CATALOG.keys())
    rows   = []
    for i in range(0, len(keys), 2):
        pair = keys[i:i + 2]
        rows.append([
            InlineKeyboardButton(
                f"{CATALOG[k]['emoji']} {CATALOG[k]['name']}",
                callback_data=f"bld_info_{k}",
            )
            for k in pair
        ])
    rows.append([InlineKeyboardButton("⬅ بازگشت به منوی اصلی", callback_data="menu_back")])
    return InlineKeyboardMarkup(rows)


def confirm_keyboard(building_key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ تایید",  callback_data=f"bld_buy_{building_key}"),
            InlineKeyboardButton("❌ لغو",    callback_data="bld_cancel"),
        ],
    ])

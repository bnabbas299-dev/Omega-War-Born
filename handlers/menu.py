"""
Placeholder handlers for main-menu buttons.
Each section will be expanded in future updates.
"""
from telegram import Update
from telegram.ext import ContextTypes

from keyboards.menus import MAIN_MENU_KEYBOARD
from models.player import Player


_COMING_SOON = "🔧 این بخش به زودی اضافه می‌شود."


async def menu_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data
    user = query.from_user
    player = Player.get(user.id)

    if not player or not player.is_registered:
        await query.message.reply_text("لطفاً ابتدا /start را بزنید و کشور خود را انتخاب کنید.")
        return

    if data == "menu_profile":
        text = (
            f"🏠 پروفایل فرمانده\n\n"
            f"👤 نام: {player.first_name}\n"
            f"🏛 کشور: {player.country or '—'}\n\n"
            f"💰 سرمایه: {player.money:,}\n"
            f"🪙 طلا: {player.gold:,}\n"
            f"🛢 نفت: {player.oil:,}\n"
            f"🌾 غذا: {player.food:,}\n"
            f"👥 جمعیت: {player.population:,}\n"
            f"⚔ قدرت نظامی: {player.army_power:,}\n"
            f"🛰 فناوری: سطح {player.technology}\n"
            f"🕊 دیپلماسی: {player.diplomacy}\n"
            f"📅 تاریخ ورود: {player.join_date}"
        )
    elif data == "menu_economy":
        text = f"🏦 اقتصاد\n\n{_COMING_SOON}"
    elif data == "menu_army":
        text = f"🪖 ارتش\n\n{_COMING_SOON}"
    elif data == "menu_alliance":
        text = f"🤝 اتحاد\n\n{_COMING_SOON}"
    elif data == "menu_news":
        text = f"📰 اخبار\n\n{_COMING_SOON}"
    elif data == "menu_map":
        text = f"🌍 نقشه جهان\n\n{_COMING_SOON}"
    elif data == "menu_settings":
        text = f"⚙ تنظیمات\n\n{_COMING_SOON}"
    else:
        return

    await query.message.reply_text(text, reply_markup=MAIN_MENU_KEYBOARD)

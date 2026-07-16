"""
Country selection callback handler.
Completes player registration and shows the main menu.
"""

from telegram import Update
from telegram.ext import ContextTypes

from models.player import Player
from utils.keyboards import COUNTRY_NAMES, COUNTRY_KEYBOARD, MAIN_MENU_KEYBOARD
from utils.formatters import fmt, tech_level


def _confirmation_text(player: Player, country_label: str) -> str:
    return (
        f"✅ کشور شما با موفقیت ثبت شد.\n\n"
        f"🏛 کشور: {country_label}\n\n"
        f"💰 سرمایه: {fmt(player.money)}\n"
        f"🪙 طلا: {fmt(player.gold)}\n"
        f"🛢 نفت: {fmt(player.oil)}\n"
        f"🌾 غذا: {fmt(player.food)}\n"
        f"👥 جمعیت: {fmt(player.population)}\n"
        f"⚔ قدرت نظامی: {fmt(player.army_power)}\n"
        f"🛰 فناوری: {tech_level(player.technology)}"
    )


async def country_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data
    if data not in COUNTRY_NAMES:
        return

    user = query.from_user
    player = Player.get(user.id)

    if not player:
        player = Player.create(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
        )

    if player.is_registered:
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text(
            "✅ شما قبلاً کشور خود را انتخاب کرده‌اید.",
            reply_markup=MAIN_MENU_KEYBOARD,
        )
        return

    player.register_country(data)
    country_label = COUNTRY_NAMES[data]

    await query.edit_message_text(text=_confirmation_text(player, country_label))
    await query.message.reply_text(
        "🎮 به دنیای OMEGAWARBORN خوش آمدید، فرمانده!\nاز منوی زیر شروع کنید:",
        reply_markup=MAIN_MENU_KEYBOARD,
    )

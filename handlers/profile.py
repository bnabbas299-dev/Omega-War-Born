"""
Profile section handler.
Displays the player's full stats and account information.
"""

from telegram import Update
from telegram.ext import ContextTypes

from models.player import Player
from utils.keyboards import MAIN_MENU_KEYBOARD, COUNTRY_NAMES
from utils.formatters import fmt, tech_level, diplomacy_label


def _profile_text(player: Player) -> str:
    country = COUNTRY_NAMES.get(player.country or "", player.country or "—")
    return (
        f"🏠 پروفایل فرمانده\n"
        f"{'─' * 28}\n"
        f"👤 نام: {player.first_name}\n"
        f"🆔 شناسه: {player.telegram_id}\n"
        f"🏛 کشور: {country}\n"
        f"📅 تاریخ ورود: {player.join_date}\n\n"
        f"📊 منابع\n"
        f"{'─' * 28}\n"
        f"💰 سرمایه: {fmt(player.money)}\n"
        f"🪙 طلا: {fmt(player.gold)}\n"
        f"🛢 نفت: {fmt(player.oil)}\n"
        f"🌾 غذا: {fmt(player.food)}\n"
        f"👥 جمعیت: {fmt(player.population)}\n\n"
        f"⚔️ نظامی و فناوری\n"
        f"{'─' * 28}\n"
        f"⚔ قدرت نظامی: {fmt(player.army_power)}\n"
        f"🛰 فناوری: {tech_level(player.technology)}\n"
        f"🕊 دیپلماسی: {diplomacy_label(player.diplomacy)}"
    )


async def profile_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    player = Player.get(query.from_user.id)
    if not player or not player.is_registered:
        await query.message.reply_text("لطفاً ابتدا /start را بزنید.")
        return

    await query.message.reply_text(_profile_text(player), reply_markup=MAIN_MENU_KEYBOARD)

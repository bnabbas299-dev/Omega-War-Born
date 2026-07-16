"""
Leaderboard section handler.
Shows the top 10 players ranked by army power.
"""

from telegram import Update
from telegram.ext import ContextTypes

from models.player import Player
from utils.keyboards import MAIN_MENU_KEYBOARD, COUNTRY_NAMES
from utils.formatters import fmt


def _leaderboard_text(players: list[Player]) -> str:
    if not players:
        return "🏆 رتبه‌بندی\n\nهنوز هیچ بازیکنی ثبت‌نام نکرده است."

    medals = ["🥇", "🥈", "🥉"]
    lines = ["🏆 برترین فرماندهان جهان\n" + "─" * 28]

    for i, p in enumerate(players):
        rank = medals[i] if i < 3 else f"{i + 1}."
        country = COUNTRY_NAMES.get(p.country or "", "")
        lines.append(
            f"{rank} {p.first_name} {country}\n"
            f"   ⚔ قدرت نظامی: {fmt(p.army_power)}"
        )

    return "\n".join(lines)


async def leaderboard_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    players = Player.top(10)
    await query.message.reply_text(
        _leaderboard_text(players), reply_markup=MAIN_MENU_KEYBOARD
    )

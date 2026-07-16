"""
War section handler. (Phase 2 — stub)
Will manage attack declarations, battle resolution, and war reports.
"""

from telegram import Update
from telegram.ext import ContextTypes

from utils.keyboards import MAIN_MENU_KEYBOARD

_PLACEHOLDER = (
    "⚔️ بخش جنگ\n\n"
    "این بخش در فاز ۲ پیاده‌سازی می‌شود.\n"
    "شامل: اعلان جنگ، شبیه‌سازی نبرد، غارت منابع و گزارش‌های جنگی."
)


async def war_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(_PLACEHOLDER, reply_markup=MAIN_MENU_KEYBOARD)

"""
Market section handler. (Phase 2 — stub)
Will manage player-to-player resource trading and global market prices.
"""

from telegram import Update
from telegram.ext import ContextTypes

from utils.keyboards import MAIN_MENU_KEYBOARD

_PLACEHOLDER = (
    "🛒 بخش بازار\n\n"
    "این بخش در فاز ۲ پیاده‌سازی می‌شود.\n"
    "شامل: خرید و فروش منابع، سفارش‌های باز و قیمت‌های جهانی."
)


async def market_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(_PLACEHOLDER, reply_markup=MAIN_MENU_KEYBOARD)

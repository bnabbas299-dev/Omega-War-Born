"""
Research section handler. (Phase 2 — stub)
Will manage technology trees and research unlocks.
"""

from telegram import Update
from telegram.ext import ContextTypes

from utils.keyboards import MAIN_MENU_KEYBOARD

_PLACEHOLDER = (
    "🔬 بخش تحقیقات\n\n"
    "این بخش در فاز ۲ پیاده‌سازی می‌شود.\n"
    "شامل: درخت فناوری، آزمایشگاه‌ها و باز کردن قابلیت‌های جدید."
)


async def research_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(_PLACEHOLDER, reply_markup=MAIN_MENU_KEYBOARD)

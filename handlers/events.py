"""
Events section handler. (Phase 2 — stub)
Will display global events, disasters, and special opportunities.
"""

from telegram import Update
from telegram.ext import ContextTypes

from utils.keyboards import MAIN_MENU_KEYBOARD

_PLACEHOLDER = (
    "📰 بخش رویدادها\n\n"
    "این بخش در فاز ۲ پیاده‌سازی می‌شود.\n"
    "شامل: رویدادهای جهانی، بلایای طبیعی و فرصت‌های ویژه."
)


async def events_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(_PLACEHOLDER, reply_markup=MAIN_MENU_KEYBOARD)

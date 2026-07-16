"""
Diplomacy section handler. (Phase 2 — stub)
Will manage alliances, treaties, embargoes, and peace deals.
"""

from telegram import Update
from telegram.ext import ContextTypes

from utils.keyboards import MAIN_MENU_KEYBOARD

_PLACEHOLDER = (
    "🤝 بخش دیپلماسی\n\n"
    "این بخش در فاز ۲ پیاده‌سازی می‌شود.\n"
    "شامل: اتحادها، پیمان‌ها، تحریم‌ها و توافق‌های صلح."
)


async def diplomacy_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(_PLACEHOLDER, reply_markup=MAIN_MENU_KEYBOARD)

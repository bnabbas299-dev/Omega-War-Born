"""
Admin command handler. (Phase 2 — stub)
Restricted to authorised admin Telegram IDs defined in config.
"""

from telegram import Update
from telegram.ext import ContextTypes

# Add authorised admin Telegram IDs here
ADMIN_IDS: set[int] = set()


async def admin_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if user.id not in ADMIN_IDS:
        await update.message.reply_text("⛔ دسترسی ندارید.")
        return

    await update.message.reply_text(
        "🛡 پنل ادمین\n\n"
        "دستورات موجود:\n"
        "/admin — این پنل\n\n"
        "قابلیت‌های بیشتر در فاز ۲ اضافه می‌شود."
    )

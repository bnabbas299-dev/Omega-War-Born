"""
OMEGA WARBORN — main entry point.
Registers all handlers and starts the bot in polling mode.
"""

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

from config import BOT_TOKEN
from database import initialize_database

from handlers.start       import start_handler
from handlers.country     import country_callback_handler
from handlers.menu        import menu_callback_handler
from handlers.admin       import admin_command_handler


def main() -> None:
    initialize_database()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ── Commands ─────────────────────────────────────────────────────────────
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("admin", admin_command_handler))

    # ── Registration ─────────────────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(country_callback_handler, pattern=r"^country_"))

    # ── All menu_ callbacks (single dispatcher handles every section) ─────────
    app.add_handler(CallbackQueryHandler(menu_callback_handler, pattern=r"^menu_"))

    print("🚀 OMEGA WARBORN bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

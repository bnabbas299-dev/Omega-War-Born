"""
OMEGA WARBORN — main entry point.
"""

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

from config import BOT_TOKEN
from database import initialize_database

from handlers.start       import start_handler
from handlers.country     import country_callback_handler
from handlers.menu        import menu_callback_handler
from handlers.buildings   import buildings_callback_handler
from handlers.admin       import admin_command_handler
from services.time_service import register_jobs


def main() -> None:
    initialize_database()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ── Commands ──────────────────────────────────────────────────────────────
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("admin", admin_command_handler))

    # ── Registration ──────────────────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(country_callback_handler, pattern=r"^country_"))

    # ── Main menu ─────────────────────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(menu_callback_handler, pattern=r"^menu_"))

    # ── Construction ──────────────────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(buildings_callback_handler, pattern=r"^bld_"))

    # ── Scheduled jobs ────────────────────────────────────────────────────────
    register_jobs(app)

    print("🚀 OMEGA WARBORN bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

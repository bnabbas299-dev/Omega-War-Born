"""
OMEGA WARBORN — main entry point.
"""

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from database import initialize_database

from handlers.start        import start_handler
from handlers.country      import country_callback_handler
from handlers.menu         import menu_callback_handler
from handlers.buildings    import buildings_callback_handler
from handlers.market       import market_callback_handler
from handlers.production   import production_callback_handler
from handlers.technology   import technology_callback_handler
from handlers.input_router import text_message_router
from handlers.admin        import admin_command_handler
from services.time_service import register_jobs


def main() -> None:
    initialize_database()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ── Commands ──────────────────────────────────────────────────────────────
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("admin", admin_command_handler))

    # ── Callback query handlers (most-specific prefix first) ──────────────────
    app.add_handler(CallbackQueryHandler(country_callback_handler,    pattern=r"^country_"))
    app.add_handler(CallbackQueryHandler(buildings_callback_handler,  pattern=r"^bld_"))
    app.add_handler(CallbackQueryHandler(market_callback_handler,     pattern=r"^mkt_"))
    app.add_handler(CallbackQueryHandler(production_callback_handler,  pattern=r"^prd_"))
    app.add_handler(CallbackQueryHandler(technology_callback_handler, pattern=r"^tch_"))
    app.add_handler(CallbackQueryHandler(menu_callback_handler,       pattern=r"^menu_"))

    # ── Plain-text messages — routed to whichever flow is pending ─────────────
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_message_router)
    )

    # ── Scheduled jobs ────────────────────────────────────────────────────────
    register_jobs(app)

    print("🚀 OMEGA WARBORN bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

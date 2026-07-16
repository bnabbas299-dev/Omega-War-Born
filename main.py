"""
OMEGA WARBORN — main entry point.
Registers all handlers and starts the bot in polling mode.
"""

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

from config import BOT_TOKEN
from database import init_db

# ── Handlers ────────────────────────────────────────────────────────────────
from handlers.start       import start_handler
from handlers.country     import country_callback_handler
from handlers.menu        import menu_callback_handler
from handlers.profile     import profile_callback_handler
from handlers.economy     import economy_callback_handler
from handlers.buildings   import buildings_callback_handler
from handlers.military    import military_callback_handler
from handlers.market      import market_callback_handler
from handlers.diplomacy   import diplomacy_callback_handler
from handlers.research    import research_callback_handler
from handlers.war         import war_callback_handler
from handlers.events      import events_callback_handler
from handlers.leaderboard import leaderboard_callback_handler
from handlers.admin       import admin_command_handler


def main() -> None:
    # Initialise database tables on startup
    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ── Command handlers ─────────────────────────────────────────────────
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("admin", admin_command_handler))

    # ── Registration flow ────────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(country_callback_handler,     pattern=r"^country_"))

    # ── Main menu ────────────────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(menu_callback_handler,        pattern=r"^menu_"))

    # ── Section handlers ─────────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(profile_callback_handler,     pattern=r"^profile_"))
    app.add_handler(CallbackQueryHandler(economy_callback_handler,     pattern=r"^economy_"))
    app.add_handler(CallbackQueryHandler(buildings_callback_handler,   pattern=r"^buildings_"))
    app.add_handler(CallbackQueryHandler(military_callback_handler,    pattern=r"^military_"))
    app.add_handler(CallbackQueryHandler(market_callback_handler,      pattern=r"^market_"))
    app.add_handler(CallbackQueryHandler(diplomacy_callback_handler,   pattern=r"^diplomacy_"))
    app.add_handler(CallbackQueryHandler(research_callback_handler,    pattern=r"^research_"))
    app.add_handler(CallbackQueryHandler(war_callback_handler,         pattern=r"^war_"))
    app.add_handler(CallbackQueryHandler(events_callback_handler,      pattern=r"^events_"))
    app.add_handler(CallbackQueryHandler(leaderboard_callback_handler, pattern=r"^leaderboard_"))

    print("🚀 OMEGA WARBORN bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

from config import BOT_TOKEN
from database.setup import init_db
from handlers.start import start_handler
from handlers.registration import country_callback_handler
from handlers.menu import menu_callback_handler


def main() -> None:
    # Initialise database on startup
    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_handler))

    # Callback queries — registration (country selection)
    app.add_handler(CallbackQueryHandler(country_callback_handler, pattern=r"^country_"))

    # Callback queries — main menu sections
    app.add_handler(CallbackQueryHandler(menu_callback_handler, pattern=r"^menu_"))

    print("OMEGAWARBORN bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

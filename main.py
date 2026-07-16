from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN

WELCOME_MESSAGE = (
    "🌍⚔️ به OMEGAWARBORN خوش آمدید ⚔️🌍\n\n"
    "🏛 به میدان نبردی خوش آمدید که سرنوشت جهان در آن رقم می‌خورد.\n"
    "🌐 فرماندهی این جهان در اختیار MBN Global Command است.\n\n"
    "🛡 کشور خود را انتخاب کنید.\n"
    "🤝 اتحادهای قدرتمند تشکیل دهید.\n"
    "👑 سرنوشت ملت خود را رقم بزنید.\n"
    "🔥 تاریخ را از نو بنویسید.\n\n"
    "🚨 هر تصمیم، آینده جهان را تغییر می‌دهد.\n"
    "💥 هر نبرد، موازنه قدرت را دگرگون می‌کند.\n"
    "🌍 تنها یک قدرت، بر جهان سلطه خواهد یافت.\n\n"
    "⏳ شمارش معکوس به پایان رسید...\n"
    "⚔️ جنگ، از همین لحظه آغاز می‌شود."
)

COUNTRY_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🇮🇷 ایران", callback_data="country_iran"),
        InlineKeyboardButton("🇺🇸 آمریکا", callback_data="country_usa"),
    ],
    [
        InlineKeyboardButton("🇷🇺 روسیه", callback_data="country_russia"),
        InlineKeyboardButton("🇮🇱 اسرائیل", callback_data="country_israel"),
    ],
])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=COUNTRY_KEYBOARD,
    )


def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("OMEGAWARBORN bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

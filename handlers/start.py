from telegram import Update
from telegram.ext import ContextTypes

from keyboards.menus import COUNTRY_KEYBOARD, MAIN_MENU_KEYBOARD
from models.player import Player

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

ALREADY_REGISTERED_MESSAGE = (
    "⚔️ خوش برگشتید، فرمانده!\n\n"
    "از منوی زیر ادامه دهید:"
)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    player = Player.get(user.id)

    if player and player.is_registered:
        # Returning player — show main menu
        await update.message.reply_text(
            ALREADY_REGISTERED_MESSAGE,
            reply_markup=MAIN_MENU_KEYBOARD,
        )
        return

    if not player:
        # First visit — create an unregistered profile
        Player.create(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
        )

    # Show welcome + country selection
    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=COUNTRY_KEYBOARD,
    )

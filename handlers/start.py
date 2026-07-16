"""
/start command handler.
Creates a new player profile on first visit; returns returning players to the main menu.
"""

from telegram import Update
from telegram.ext import ContextTypes

from models.player import Player
from utils.keyboards import COUNTRY_KEYBOARD, MAIN_MENU_KEYBOARD

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


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    player = Player.get(user.id)

    if player and player.is_registered:
        await update.message.reply_text(
            f"⚔️ خوش برگشتید، فرمانده {player.first_name}!\n\nاز منوی زیر ادامه دهید:",
            reply_markup=MAIN_MENU_KEYBOARD,
        )
        return

    if not player:
        Player.create(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
        )

    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=COUNTRY_KEYBOARD)

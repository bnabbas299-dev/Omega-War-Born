from telegram import Update
from telegram.ext import ContextTypes

from keyboards.menus import COUNTRY_NAMES, COUNTRY_KEYBOARD, MAIN_MENU_KEYBOARD
from models.player import Player


def _format_number(n: int) -> str:
    return f"{n:,}"


def _build_confirmation(player: Player, country_label: str) -> str:
    return (
        f"✅ کشور شما با موفقیت ثبت شد.\n\n"
        f"🏛 کشور: {country_label}\n\n"
        f"💰 سرمایه: {_format_number(player.money)}\n"
        f"🪙 طلا: {_format_number(player.gold)}\n"
        f"🛢 نفت: {_format_number(player.oil)}\n"
        f"🌾 غذا: {_format_number(player.food)}\n"
        f"👥 جمعیت: {_format_number(player.population)}\n"
        f"⚔ قدرت نظامی: {_format_number(player.army_power)}\n"
        f"🛰 فناوری: سطح {player.technology}"
    )


async def country_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data  # e.g. "country_iran"

    if data not in COUNTRY_NAMES:
        return

    user = query.from_user
    player = Player.get(user.id)

    if not player:
        # Edge case: callback arrived without a prior /start
        player = Player.create(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
        )

    if player.is_registered:
        # Already registered — silently ignore duplicate selections
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text(
            "✅ شما قبلاً کشور خود را انتخاب کرده‌اید.",
            reply_markup=MAIN_MENU_KEYBOARD,
        )
        return

    # Register country
    player.register_country(data)
    country_label = COUNTRY_NAMES[data]

    confirmation = _build_confirmation(player, country_label)

    # Replace the country-selection message with the confirmation
    await query.edit_message_text(
        text=confirmation,
        reply_markup=None,
    )

    # Send the main menu as a new message
    await query.message.reply_text(
        "🎮 به دنیای OMEGAWARBORN خوش آمدید، فرمانده!\nاز منوی زیر شروع کنید:",
        reply_markup=MAIN_MENU_KEYBOARD,
    )

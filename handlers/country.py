"""
Country selection callback handler.
Validates uniqueness, inserts all starting data, and shows the main menu.
"""

from telegram import Update
from telegram.ext import ContextTypes

from models.player import Player
from models.country import Country, AVAILABLE_COUNTRIES
from utils.keyboards import COUNTRY_KEYBOARD, MAIN_MENU_KEYBOARD


def _confirmation_text(country_label: str) -> str:
    return (
        "✅ کشور شما با موفقیت ثبت شد.\n\n"
        f"🏛 کشور: {country_label}\n\n"
        "💰 بودجه: 500 میلیارد دلار\n"
        "👥 جمعیت: 50 میلیون نفر\n"
        "😊 رضایت مردم: 80٪\n"
        "⭐ محبوبیت دولت: 75٪\n"
        "🔬 فناوری: سطح 1\n"
        "🏭 صنعت: سطح پایه"
    )


async def country_callback_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data  # e.g. "country_iran"

    if data not in AVAILABLE_COUNTRIES:
        return

    user = query.from_user

    # ── Ensure player row exists ─────────────────────────────────────────────
    player = Player.get(user.id)
    if not player:
        player = Player.create(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
        )

    # ── Already registered ───────────────────────────────────────────────────
    if player.is_registered:
        await query.answer("✅ شما قبلاً کشور خود را انتخاب کرده‌اید.", show_alert=True)
        await query.message.reply_text(
            "🎮 منوی اصلی:", reply_markup=MAIN_MENU_KEYBOARD
        )
        return

    country_label = AVAILABLE_COUNTRIES[data]
    # Strip flag + space to get the bare Persian name for DB storage
    country_name = country_label.split(" ", 1)[1]

    # ── Country uniqueness check ─────────────────────────────────────────────
    if Country.is_taken(country_name):
        await query.answer("❌ این کشور قبلاً انتخاب شده است.", show_alert=True)
        await query.edit_message_text(
            "❌ این کشور قبلاً انتخاب شده است.\n\n"
            "🌍 لطفاً کشور دیگری انتخاب کنید:",
            reply_markup=COUNTRY_KEYBOARD,
        )
        return

    # ── Create country + all satellite rows ──────────────────────────────────
    country = Country.create(
        country_name=country_name,
        leader_telegram_id=user.id,
    )

    # ── Link player → country ────────────────────────────────────────────────
    player.set_country(country.id)

    # ── Confirmation message ─────────────────────────────────────────────────
    await query.edit_message_text(text=_confirmation_text(country_label))

    # ── Main menu ────────────────────────────────────────────────────────────
    await query.message.reply_text(
        "🎮 به OMEGAWARBORN خوش آمدید، فرمانده!\nاز منوی زیر شروع کنید:",
        reply_markup=MAIN_MENU_KEYBOARD,
    )

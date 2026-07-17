"""
Input Router — unified plain-text message dispatcher.

Checks user_data for any pending interactive flow and routes to the
correct handler. Registered as the sole MessageHandler in main.py.

Priority order:
  1. pending_market      → market quantity purchase
  2. pending_production  → production quantity order
  (future flows go here)
"""

from telegram import Update
from telegram.ext import ContextTypes

from handlers.market     import quantity_message_handler as _market_qty
from handlers.production import production_quantity_handler as _prod_qty


async def text_message_router(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if context.user_data.get("pending_market"):
        await _market_qty(update, context)
    elif context.user_data.get("pending_production"):
        await _prod_qty(update, context)
    # No pending state → silently ignore

"""
Market Service — Phase 2
Handles player-to-player resource trading and global price tracking.
"""

from __future__ import annotations

from models.player import Player

# Base global prices (money per unit) — will be dynamic in Phase 2
BASE_PRICES: dict[str, int] = {
    "gold": 5000,
    "oil":  200,
    "food": 50,
}


class MarketService:
    """All market and trading operations."""

    @staticmethod
    def get_price(resource: str) -> int:
        """Return current market price for a resource."""
        return BASE_PRICES.get(resource, 0)

    @staticmethod
    def post_order(seller: Player, resource: str, quantity: int, price: int) -> dict:
        """
        Create an open sell order on the market.
        Returns result dict with success flag and order_id.
        (Stub — implement in Phase 2)
        """
        return {"success": False, "message": "Not implemented yet."}

    @staticmethod
    def fill_order(buyer: Player, order_id: int) -> dict:
        """
        Buyer purchases an existing open order.
        Returns result dict.
        (Stub — implement in Phase 2)
        """
        return {"success": False, "message": "Not implemented yet."}

    @staticmethod
    def cancel_order(seller: Player, order_id: int) -> dict:
        """
        Cancel an open sell order.
        (Stub — implement in Phase 2)
        """
        return {"success": False, "message": "Not implemented yet."}

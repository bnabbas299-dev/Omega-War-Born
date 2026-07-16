"""
Military Service — Phase 2
Handles unit recruitment, upkeep, and army power calculations.
"""

from __future__ import annotations

from models.player import Player


class MilitaryService:
    """All military-related operations."""

    UNIT_TYPES: dict[str, dict] = {
        "infantry":  {"cost": 500,   "power": 1,  "upkeep": 10},
        "tank":      {"cost": 5000,  "power": 10, "upkeep": 100},
        "aircraft":  {"cost": 20000, "power": 40, "upkeep": 400},
        "navy":      {"cost": 15000, "power": 30, "upkeep": 300},
    }

    @staticmethod
    def recruit(player: Player, unit_type: str, quantity: int) -> dict:
        """
        Recruit units for a player.
        Returns result dict with success flag and message.
        (Stub — implement in Phase 2)
        """
        return {"success": False, "message": "Not implemented yet."}

    @staticmethod
    def calculate_army_power(player: Player) -> int:
        """
        Sum all unit contributions to return total army power.
        (Stub — implement in Phase 2)
        """
        return player.army_power

    @staticmethod
    def pay_upkeep(player: Player) -> int:
        """
        Deduct upkeep costs from player's money.
        Returns total upkeep paid.
        (Stub — implement in Phase 2)
        """
        return 0

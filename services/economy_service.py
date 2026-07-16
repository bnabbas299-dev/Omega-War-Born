"""
Economy Service — Phase 2
Handles income calculation, tax collection, and resource production cycles.
"""

from __future__ import annotations

from models.player import Player


class EconomyService:
    """All economy-related calculations and transactions."""

    @staticmethod
    def calculate_income(player: Player) -> dict[str, int]:
        """
        Calculate per-tick resource income for a player.
        Returns a dict of resource deltas.
        (Stub — implement in Phase 2)
        """
        return {
            "money": 0,
            "gold":  0,
            "oil":   0,
            "food":  0,
        }

    @staticmethod
    def collect_taxes(player: Player) -> int:
        """
        Collect taxes based on population and technology level.
        Returns amount collected.
        (Stub — implement in Phase 2)
        """
        return 0

    @staticmethod
    def apply_income_tick(player: Player) -> None:
        """
        Apply one income tick to a player's resources.
        Called by TimeService on each scheduled interval.
        (Stub — implement in Phase 2)
        """
        pass

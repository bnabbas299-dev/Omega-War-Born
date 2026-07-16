"""
Battle Service — Phase 2
Handles attack declarations, battle simulation, and loot distribution.
"""

from __future__ import annotations

from models.player import Player


class BattleService:
    """Simulates battles between two players."""

    @staticmethod
    def can_attack(attacker: Player, defender: Player) -> tuple[bool, str]:
        """
        Validate whether an attack is permitted.
        Returns (allowed, reason_if_not).
        (Stub — implement in Phase 2)
        """
        return False, "سیستم جنگ هنوز پیاده‌سازی نشده است."

    @staticmethod
    def simulate(attacker: Player, defender: Player) -> dict:
        """
        Run battle simulation and return result dict.
        Keys: winner_id, loser_id, loot, battle_log.
        (Stub — implement in Phase 2)
        """
        return {
            "winner_id":  None,
            "loser_id":   None,
            "loot":       {},
            "battle_log": [],
        }

    @staticmethod
    def apply_result(result: dict, attacker: Player, defender: Player) -> None:
        """
        Apply battle outcome (resource transfer, army losses, war log entry).
        (Stub — implement in Phase 2)
        """
        pass

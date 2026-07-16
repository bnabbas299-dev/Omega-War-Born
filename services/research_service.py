"""
Research Service — Phase 2
Handles technology tree progression and research unlocks.
"""

from __future__ import annotations

from models.player import Player

# Technology tree definition — extend in Phase 2
TECH_TREE: dict[str, dict] = {
    "agriculture":   {"cost": 10000, "unlocks": ["advanced_farming"], "effect": {"food": 500}},
    "metallurgy":    {"cost": 15000, "unlocks": ["steel_production"],  "effect": {"army_power": 20}},
    "engineering":   {"cost": 20000, "unlocks": ["advanced_buildings"],"effect": {}},
    "cryptography":  {"cost": 25000, "unlocks": ["secure_comms"],      "effect": {}},
    "nuclear":       {"cost": 500000,"unlocks": ["nuke"],               "effect": {"army_power": 1000}},
}


class ResearchService:
    """Manages technology progression."""

    @staticmethod
    def available_techs(player: Player) -> list[str]:
        """
        Return list of tech names the player can currently research.
        (Stub — implement in Phase 2)
        """
        return list(TECH_TREE.keys())

    @staticmethod
    def start_research(player: Player, tech_name: str) -> dict:
        """
        Begin researching a technology.
        Returns result dict with success flag.
        (Stub — implement in Phase 2)
        """
        return {"success": False, "message": "Not implemented yet."}

    @staticmethod
    def apply_tech_effects(player: Player, tech_name: str) -> None:
        """
        Apply the stat bonuses of a completed technology.
        (Stub — implement in Phase 2)
        """
        pass

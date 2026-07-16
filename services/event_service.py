"""
Event Service — Phase 2
Generates and broadcasts global and player-specific random events.
"""

from __future__ import annotations

import random
from models.player import Player

# Event catalogue — extend freely in Phase 2
EVENT_CATALOGUE: list[dict] = [
    {
        "type":        "economic_boom",
        "name":        "رونق اقتصادی",
        "description": "اقتصاد جهانی رونق گرفت! درآمد همه بازیکنان ۲۰٪ افزایش یافت.",
        "effect":      {"money": 100000},
        "scope":       "global",
    },
    {
        "type":        "drought",
        "name":        "خشکسالی",
        "description": "خشکسالی شدید! ذخایر غذایی کاهش یافت.",
        "effect":      {"food": -1000},
        "scope":       "global",
    },
    {
        "type":        "oil_discovery",
        "name":        "کشف نفت",
        "description": "منابع جدید نفتی کشف شد!",
        "effect":      {"oil": 2000},
        "scope":       "player",
    },
]


class EventService:
    """Generates and applies random events."""

    @staticmethod
    def trigger_random_event() -> dict | None:
        """
        Pick and return a random global event.
        Returns None if no event fires this tick.
        (Stub — implement in Phase 2)
        """
        if random.random() < 0.05:  # 5% chance per tick
            return random.choice(
                [e for e in EVENT_CATALOGUE if e["scope"] == "global"]
            )
        return None

    @staticmethod
    def apply_event(player: Player, event: dict) -> None:
        """
        Apply an event's effect to a player.
        (Stub — implement in Phase 2)
        """
        pass

    @staticmethod
    def log_event(player_id: int | None, event: dict) -> None:
        """
        Write event to the events table.
        (Stub — implement in Phase 2)
        """
        pass

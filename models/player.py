from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Optional

from database.connection import get_connection


class Player:
    """Represents a game player and provides all DB operations."""

    def __init__(self, row: sqlite3.Row) -> None:
        self.telegram_id: int = row["telegram_id"]
        self.username: Optional[str] = row["username"]
        self.first_name: str = row["first_name"]
        self.country: Optional[str] = row["country"]
        self.money: int = row["money"]
        self.gold: int = row["gold"]
        self.oil: int = row["oil"]
        self.food: int = row["food"]
        self.population: int = row["population"]
        self.army_power: int = row["army_power"]
        self.technology: int = row["technology"]
        self.diplomacy: str = row["diplomacy"]
        self.join_date: str = row["join_date"]
        self.is_registered: bool = bool(row["is_registered"])

    # ------------------------------------------------------------------ #
    # Queries
    # ------------------------------------------------------------------ #

    @staticmethod
    def get(telegram_id: int) -> Optional["Player"]:
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT * FROM players WHERE telegram_id = ?", (telegram_id,)
            ).fetchone()
            return Player(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def create(telegram_id: int, username: Optional[str], first_name: str) -> "Player":
        """Insert a new unregistered player and return it."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        conn = get_connection()
        with conn:
            conn.execute(
                """
                INSERT INTO players
                    (telegram_id, username, first_name, join_date)
                VALUES (?, ?, ?, ?)
                """,
                (telegram_id, username, first_name, now),
            )
        conn.close()
        return Player.get(telegram_id)  # type: ignore[return-value]

    def register_country(self, country: str) -> None:
        """Set the player's country and mark registration complete."""
        conn = get_connection()
        with conn:
            conn.execute(
                "UPDATE players SET country = ?, is_registered = 1 WHERE telegram_id = ?",
                (country, self.telegram_id),
            )
        conn.close()
        self.country = country
        self.is_registered = True

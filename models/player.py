"""
Player model — all database operations for the players table.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Optional

from database import get_connection


class Player:
    """Represents a single player row with typed attributes."""

    def __init__(self, row: sqlite3.Row) -> None:
        self.telegram_id: int        = row["telegram_id"]
        self.username: Optional[str] = row["username"]
        self.first_name: str         = row["first_name"]
        self.country: Optional[str]  = row["country"]
        self.money: int              = row["money"]
        self.gold: int               = row["gold"]
        self.oil: int                = row["oil"]
        self.food: int               = row["food"]
        self.population: int         = row["population"]
        self.army_power: int         = row["army_power"]
        self.technology: int         = row["technology"]
        self.diplomacy: str          = row["diplomacy"]
        self.join_date: str          = row["join_date"]
        self.is_registered: bool     = bool(row["is_registered"])

    # ── Queries ─────────────────────────────────────────────────────────────

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
    def create(
        telegram_id: int,
        username: Optional[str],
        first_name: str,
    ) -> "Player":
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        conn = get_connection()
        with conn:
            conn.execute(
                """
                INSERT INTO players (telegram_id, username, first_name, join_date)
                VALUES (?, ?, ?, ?)
                """,
                (telegram_id, username, first_name, now),
            )
        conn.close()
        return Player.get(telegram_id)  # type: ignore[return-value]

    # ── Mutations ────────────────────────────────────────────────────────────

    def register_country(self, country_key: str) -> None:
        conn = get_connection()
        with conn:
            conn.execute(
                "UPDATE players SET country = ?, is_registered = 1 WHERE telegram_id = ?",
                (country_key, self.telegram_id),
            )
        conn.close()
        self.country = country_key
        self.is_registered = True

    def update_resources(self, **fields: int) -> None:
        """Generic resource update — pass keyword args matching column names."""
        if not fields:
            return
        cols = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [self.telegram_id]
        conn = get_connection()
        with conn:
            conn.execute(
                f"UPDATE players SET {cols} WHERE telegram_id = ?", values
            )
        conn.close()
        for k, v in fields.items():
            setattr(self, k, v)

    @staticmethod
    def top(limit: int = 10) -> list["Player"]:
        """Return top players by army_power for the leaderboard."""
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM players WHERE is_registered = 1 "
                "ORDER BY army_power DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [Player(r) for r in rows]
        finally:
            conn.close()

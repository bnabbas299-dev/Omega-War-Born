"""
Player model — database operations for the players table.
"""

from __future__ import annotations

import sqlite3
from typing import Optional

from database import get_connection


class Player:
    """Typed wrapper around a players row."""

    def __init__(self, row: sqlite3.Row) -> None:
        self.telegram_id: int        = row["telegram_id"]
        self.username: Optional[str] = row["username"]
        self.first_name: str         = row["first_name"]
        self.country_id: Optional[int] = row["country_id"]
        self.join_date: str          = row["join_date"]
        self.last_online: str        = row["last_online"]
        self.is_admin: bool          = bool(row["is_admin"])
        self.is_banned: bool         = bool(row["is_banned"])

    @property
    def is_registered(self) -> bool:
        """True when the player has chosen a country."""
        return self.country_id is not None

    # ── Queries ──────────────────────────────────────────────────────────────

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
        conn = get_connection()
        with conn:
            conn.execute(
                """
                INSERT INTO players (telegram_id, username, first_name)
                VALUES (?, ?, ?)
                """,
                (telegram_id, username, first_name),
            )
        conn.close()
        return Player.get(telegram_id)  # type: ignore[return-value]

    # ── Mutations ─────────────────────────────────────────────────────────────

    def set_country(self, country_id: int) -> None:
        conn = get_connection()
        with conn:
            conn.execute(
                "UPDATE players SET country_id = ? WHERE telegram_id = ?",
                (country_id, self.telegram_id),
            )
        conn.close()
        self.country_id = country_id

    def touch(self) -> None:
        """Update last_online to now."""
        conn = get_connection()
        with conn:
            conn.execute(
                "UPDATE players SET last_online = strftime('%Y-%m-%d %H:%M:%S','now') "
                "WHERE telegram_id = ?",
                (self.telegram_id,),
            )
        conn.close()

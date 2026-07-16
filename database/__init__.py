"""
database package — connection and schema initialisation.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "game.db")


def get_connection() -> sqlite3.Connection:
    """Return a new SQLite connection with row_factory set."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """
    Create all game tables on startup.
    Add new CREATE TABLE blocks here as new systems are implemented.
    """
    conn = get_connection()
    with conn:

        # ── Players ──────────────────────────────────────────────────────
        conn.execute("""
            CREATE TABLE IF NOT EXISTS players (
                telegram_id   INTEGER PRIMARY KEY,
                username      TEXT,
                first_name    TEXT    NOT NULL,
                country       TEXT,
                money         INTEGER DEFAULT 5000000,
                gold          INTEGER DEFAULT 1000,
                oil           INTEGER DEFAULT 5000,
                food          INTEGER DEFAULT 5000,
                population    INTEGER DEFAULT 1000000,
                army_power    INTEGER DEFAULT 100,
                technology    INTEGER DEFAULT 1,
                diplomacy     TEXT    DEFAULT 'Neutral',
                join_date     TEXT    NOT NULL,
                is_registered INTEGER DEFAULT 0
            )
        """)

        # ── Buildings  (Phase 2) ─────────────────────────────────────────
        conn.execute("""
            CREATE TABLE IF NOT EXISTS buildings (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id   INTEGER NOT NULL REFERENCES players(telegram_id),
                building    TEXT    NOT NULL,
                level       INTEGER DEFAULT 1,
                built_at    TEXT    NOT NULL
            )
        """)

        # ── Military units  (Phase 2) ────────────────────────────────────
        conn.execute("""
            CREATE TABLE IF NOT EXISTS military (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id   INTEGER NOT NULL REFERENCES players(telegram_id),
                unit_type   TEXT    NOT NULL,
                quantity    INTEGER DEFAULT 0
            )
        """)

        # ── Market orders  (Phase 2) ─────────────────────────────────────
        conn.execute("""
            CREATE TABLE IF NOT EXISTS market_orders (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                seller_id   INTEGER NOT NULL REFERENCES players(telegram_id),
                resource    TEXT    NOT NULL,
                quantity    INTEGER NOT NULL,
                price       INTEGER NOT NULL,
                created_at  TEXT    NOT NULL,
                is_open     INTEGER DEFAULT 1
            )
        """)

        # ── Alliances  (Phase 2) ─────────────────────────────────────────
        conn.execute("""
            CREATE TABLE IF NOT EXISTS alliances (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL UNIQUE,
                leader_id   INTEGER NOT NULL REFERENCES players(telegram_id),
                created_at  TEXT    NOT NULL
            )
        """)

        # ── Alliance memberships  (Phase 2) ──────────────────────────────
        conn.execute("""
            CREATE TABLE IF NOT EXISTS alliance_members (
                alliance_id INTEGER NOT NULL REFERENCES alliances(id),
                player_id   INTEGER NOT NULL REFERENCES players(telegram_id),
                joined_at   TEXT    NOT NULL,
                PRIMARY KEY (alliance_id, player_id)
            )
        """)

        # ── War log  (Phase 2) ───────────────────────────────────────────
        conn.execute("""
            CREATE TABLE IF NOT EXISTS war_log (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                attacker_id INTEGER NOT NULL REFERENCES players(telegram_id),
                defender_id INTEGER NOT NULL REFERENCES players(telegram_id),
                result      TEXT    NOT NULL,
                loot        TEXT,
                fought_at   TEXT    NOT NULL
            )
        """)

        # ── Research  (Phase 2) ──────────────────────────────────────────
        conn.execute("""
            CREATE TABLE IF NOT EXISTS research (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id     INTEGER NOT NULL REFERENCES players(telegram_id),
                tech_name     TEXT    NOT NULL,
                level         INTEGER DEFAULT 1,
                researched_at TEXT    NOT NULL
            )
        """)

        # ── Events log  (Phase 2) ────────────────────────────────────────
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id   INTEGER REFERENCES players(telegram_id),
                event_type  TEXT    NOT NULL,
                description TEXT,
                occurred_at TEXT    NOT NULL
            )
        """)

    conn.close()

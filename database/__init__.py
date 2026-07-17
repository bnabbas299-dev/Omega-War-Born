"""
OMEGA WARBORN — Database Package
=================================
Single source of truth for all schema definitions.

Usage:
    from database import get_connection, initialize_database
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "game.db")


# ── Connection ───────────────────────────────────────────────────────────────

def get_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


# ── Schema ───────────────────────────────────────────────────────────────────

_SCHEMA = """
CREATE TABLE IF NOT EXISTS countries (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name          TEXT    NOT NULL UNIQUE,
    leader_id             INTEGER,
    budget                REAL    NOT NULL DEFAULT 0,
    population            INTEGER NOT NULL DEFAULT 0,
    active_population     INTEGER NOT NULL DEFAULT 0,
    available_recruits    INTEGER NOT NULL DEFAULT 0,
    economy_level         TEXT    NOT NULL DEFAULT 'سطح پایه',
    military_level        TEXT    NOT NULL DEFAULT 'سطح پایه',
    technology_level      INTEGER NOT NULL DEFAULT 1,
    industry_level        TEXT    NOT NULL DEFAULT 'سطح پایه',
    public_satisfaction   INTEGER NOT NULL DEFAULT 50,
    government_popularity INTEGER NOT NULL DEFAULT 50,
    global_reputation     TEXT    NOT NULL DEFAULT 'پایه',
    energy_security       TEXT    NOT NULL DEFAULT 'پایه',
    food_security         TEXT    NOT NULL DEFAULT 'پایه',
    current_day           INTEGER NOT NULL DEFAULT 0,
    created_at            TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
    updated_at            TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
);
CREATE INDEX IF NOT EXISTS idx_countries_leader ON countries(leader_id);

CREATE TABLE IF NOT EXISTS players (
    telegram_id  INTEGER PRIMARY KEY,
    username     TEXT,
    first_name   TEXT    NOT NULL,
    country_id   INTEGER REFERENCES countries(id) ON DELETE SET NULL,
    join_date    TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
    last_online  TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
    is_admin     INTEGER NOT NULL DEFAULT 0,
    is_banned    INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_players_country     ON players(country_id);
CREATE INDEX IF NOT EXISTS idx_players_last_online ON players(last_online);

CREATE TABLE IF NOT EXISTS resources (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id  INTEGER NOT NULL UNIQUE REFERENCES countries(id) ON DELETE CASCADE,
    oil         REAL    NOT NULL DEFAULT 0,
    gas         REAL    NOT NULL DEFAULT 0,
    steel       REAL    NOT NULL DEFAULT 0,
    iron        REAL    NOT NULL DEFAULT 0,
    uranium     REAL    NOT NULL DEFAULT 0,
    food        REAL    NOT NULL DEFAULT 0,
    water       REAL    NOT NULL DEFAULT 0,
    electricity REAL    NOT NULL DEFAULT 0,
    updated_at  TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
);

CREATE TABLE IF NOT EXISTS buildings (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id           INTEGER NOT NULL UNIQUE REFERENCES countries(id) ON DELETE CASCADE,
    civil_factory        INTEGER NOT NULL DEFAULT 0,
    military_factory     INTEGER NOT NULL DEFAULT 0,
    aircraft_factory     INTEGER NOT NULL DEFAULT 0,
    shipyard             INTEGER NOT NULL DEFAULT 0,
    missile_factory      INTEGER NOT NULL DEFAULT 0,
    armor_factory        INTEGER NOT NULL DEFAULT 0,
    electronics_factory  INTEGER NOT NULL DEFAULT 0,
    power_plant          INTEGER NOT NULL DEFAULT 0,
    refinery             INTEGER NOT NULL DEFAULT 0,
    research_center      INTEGER NOT NULL DEFAULT 0,
    satellite_center     INTEGER NOT NULL DEFAULT 0,
    warehouse            INTEGER NOT NULL DEFAULT 0,
    logistics_center     INTEGER NOT NULL DEFAULT 0,
    hospital             INTEGER NOT NULL DEFAULT 0,
    university           INTEGER NOT NULL DEFAULT 0,
    economic_tower       INTEGER NOT NULL DEFAULT 0,
    highway              INTEGER NOT NULL DEFAULT 0,
    railway              INTEGER NOT NULL DEFAULT 0,
    smart_city           INTEGER NOT NULL DEFAULT 0,
    national_park        INTEGER NOT NULL DEFAULT 0,
    updated_at           TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
);

CREATE TABLE IF NOT EXISTS military (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id          INTEGER NOT NULL UNIQUE REFERENCES countries(id) ON DELETE CASCADE,
    soldiers            INTEGER NOT NULL DEFAULT 0,
    tanks               INTEGER NOT NULL DEFAULT 0,
    armored_vehicles    INTEGER NOT NULL DEFAULT 0,
    artillery           INTEGER NOT NULL DEFAULT 0,
    rocket_launchers    INTEGER NOT NULL DEFAULT 0,
    air_defense         INTEGER NOT NULL DEFAULT 0,
    radars              INTEGER NOT NULL DEFAULT 0,
    fighters            INTEGER NOT NULL DEFAULT 0,
    helicopters         INTEGER NOT NULL DEFAULT 0,
    drones              INTEGER NOT NULL DEFAULT 0,
    support_aircraft    INTEGER NOT NULL DEFAULT 0,
    warships            INTEGER NOT NULL DEFAULT 0,
    submarines          INTEGER NOT NULL DEFAULT 0,
    patrol_boats        INTEGER NOT NULL DEFAULT 0,
    missiles            INTEGER NOT NULL DEFAULT 0,
    army_experience     TEXT    NOT NULL DEFAULT 'تازه‌کار',
    updated_at          TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
);

CREATE TABLE IF NOT EXISTS technology (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id        INTEGER NOT NULL UNIQUE REFERENCES countries(id) ON DELETE CASCADE,
    technology_level  INTEGER NOT NULL DEFAULT 1,
    military_ai       INTEGER NOT NULL DEFAULT 0,
    cyber_security    INTEGER NOT NULL DEFAULT 0,
    satellite_network INTEGER NOT NULL DEFAULT 0,
    quantum_lab       INTEGER NOT NULL DEFAULT 0,
    updated_at        TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
);

CREATE TABLE IF NOT EXISTS economy (
    id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id             INTEGER NOT NULL UNIQUE REFERENCES countries(id) ON DELETE CASCADE,
    daily_tax_income       REAL    NOT NULL DEFAULT 0,
    daily_industry_income  REAL    NOT NULL DEFAULT 0,
    daily_export_income    REAL    NOT NULL DEFAULT 0,
    daily_maintenance      REAL    NOT NULL DEFAULT 0,
    last_income_collection TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
    updated_at             TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
);

CREATE TABLE IF NOT EXISTS alliances (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    alliance_name  TEXT    NOT NULL UNIQUE,
    leader_country INTEGER NOT NULL REFERENCES countries(id) ON DELETE RESTRICT,
    description    TEXT,
    created_at     TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
    updated_at     TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
);
CREATE INDEX IF NOT EXISTS idx_alliances_leader ON alliances(leader_country);

CREATE TABLE IF NOT EXISTS alliance_members (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    alliance_id INTEGER NOT NULL REFERENCES alliances(id)  ON DELETE CASCADE,
    country_id  INTEGER NOT NULL REFERENCES countries(id)  ON DELETE CASCADE,
    joined_at   TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
    UNIQUE (alliance_id, country_id)
);
CREATE INDEX IF NOT EXISTS idx_alliance_members_country  ON alliance_members(country_id);
CREATE INDEX IF NOT EXISTS idx_alliance_members_alliance ON alliance_members(alliance_id);

CREATE TABLE IF NOT EXISTS wars (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    attacker   INTEGER NOT NULL REFERENCES countries(id) ON DELETE RESTRICT,
    defender   INTEGER NOT NULL REFERENCES countries(id) ON DELETE RESTRICT,
    status     TEXT    NOT NULL DEFAULT 'active' CHECK(status IN ('active','ceasefire','ended')),
    winner     INTEGER REFERENCES countries(id),
    start_date TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
    end_date   TEXT,
    UNIQUE (attacker, defender, start_date)
);
CREATE INDEX IF NOT EXISTS idx_wars_attacker ON wars(attacker);
CREATE INDEX IF NOT EXISTS idx_wars_defender ON wars(defender);
CREATE INDEX IF NOT EXISTS idx_wars_status   ON wars(status);

CREATE TABLE IF NOT EXISTS construction_queue (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id    INTEGER NOT NULL REFERENCES countries(id) ON DELETE CASCADE,
    building_name TEXT    NOT NULL,
    start_time    TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
    finish_time   TEXT    NOT NULL,
    status        TEXT    NOT NULL DEFAULT 'in_progress'
                          CHECK(status IN ('pending','in_progress','completed','cancelled'))
);
CREATE INDEX IF NOT EXISTS idx_construction_country ON construction_queue(country_id);
CREATE INDEX IF NOT EXISTS idx_construction_status  ON construction_queue(status);
CREATE INDEX IF NOT EXISTS idx_construction_finish  ON construction_queue(finish_time);

CREATE TABLE IF NOT EXISTS purchase_history (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id    INTEGER NOT NULL REFERENCES countries(id) ON DELETE CASCADE,
    item_name     TEXT    NOT NULL,
    quantity      INTEGER NOT NULL DEFAULT 1,
    price         REAL    NOT NULL DEFAULT 0,
    purchase_time TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
);
CREATE INDEX IF NOT EXISTS idx_purchase_country ON purchase_history(country_id);
CREATE INDEX IF NOT EXISTS idx_purchase_time    ON purchase_history(purchase_time);

CREATE TABLE IF NOT EXISTS battle_history (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    war_id           INTEGER NOT NULL REFERENCES wars(id) ON DELETE CASCADE,
    battle_result    TEXT    NOT NULL,
    casualties       TEXT,
    equipment_losses TEXT,
    battle_date      TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
);
CREATE INDEX IF NOT EXISTS idx_battle_history_war  ON battle_history(war_id);
CREATE INDEX IF NOT EXISTS idx_battle_history_date ON battle_history(battle_date);

CREATE TABLE IF NOT EXISTS world_events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL,
    description TEXT,
    effect      TEXT,
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
);
CREATE INDEX IF NOT EXISTS idx_world_events_date ON world_events(created_at);

CREATE TABLE IF NOT EXISTS world_news (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT NOT NULL,
    content    TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
);
CREATE INDEX IF NOT EXISTS idx_world_news_date ON world_news(created_at);

CREATE TABLE IF NOT EXISTS factories (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id   INTEGER NOT NULL REFERENCES countries(id) ON DELETE CASCADE,
    factory_type TEXT    NOT NULL,
    count        INTEGER NOT NULL DEFAULT 1,
    created_at   TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now')),
    updated_at   TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now')),
    UNIQUE(country_id, factory_type)
);
CREATE INDEX IF NOT EXISTS idx_factories_country ON factories(country_id);

CREATE TABLE IF NOT EXISTS production_queue (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id   INTEGER NOT NULL REFERENCES countries(id) ON DELETE CASCADE,
    queue_type   TEXT    NOT NULL CHECK(queue_type IN ('factory','equipment')),
    item_key     TEXT    NOT NULL,
    item_name    TEXT    NOT NULL,
    quantity     INTEGER NOT NULL DEFAULT 1,
    cost         REAL    NOT NULL DEFAULT 0,
    military_col TEXT,
    factory_type TEXT,
    start_time   TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now')),
    finish_time  TEXT    NOT NULL,
    status       TEXT    NOT NULL DEFAULT 'in_progress'
                         CHECK(status IN ('in_progress','completed','cancelled')),
    notified     INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_pq_country ON production_queue(country_id);
CREATE INDEX IF NOT EXISTS idx_pq_status  ON production_queue(status);
CREATE INDEX IF NOT EXISTS idx_pq_finish  ON production_queue(finish_time);

CREATE TABLE IF NOT EXISTS production_history (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id   INTEGER NOT NULL REFERENCES countries(id) ON DELETE CASCADE,
    queue_type   TEXT    NOT NULL,
    item_key     TEXT    NOT NULL,
    item_name    TEXT    NOT NULL,
    quantity     INTEGER NOT NULL DEFAULT 1,
    cost         REAL    NOT NULL DEFAULT 0,
    factory_type TEXT,
    completed_at TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now'))
);
CREATE INDEX IF NOT EXISTS idx_ph_country ON production_history(country_id);
"""

# ── Migrations ────────────────────────────────────────────────────────────────
# New columns added to existing tables after initial release.
# Safe to re-run on every startup.

_BUILDING_MIGRATIONS = {
    "hospital":       "INTEGER NOT NULL DEFAULT 0",
    "university":     "INTEGER NOT NULL DEFAULT 0",
    "economic_tower": "INTEGER NOT NULL DEFAULT 0",
    "highway":        "INTEGER NOT NULL DEFAULT 0",
    "railway":        "INTEGER NOT NULL DEFAULT 0",
    "smart_city":     "INTEGER NOT NULL DEFAULT 0",
    "national_park":  "INTEGER NOT NULL DEFAULT 0",
}


def _run_migrations(conn: sqlite3.Connection) -> None:
    existing = {row["name"] for row in conn.execute("PRAGMA table_info(buildings)")}
    for col, defn in _BUILDING_MIGRATIONS.items():
        if col not in existing:
            conn.execute(f"ALTER TABLE buildings ADD COLUMN {col} {defn}")
            print(f"[DB] Migration: added buildings.{col}")


# ── Public API ────────────────────────────────────────────────────────────────

def initialize_database() -> None:
    conn = get_connection()
    try:
        conn.executescript(_SCHEMA)
        conn.commit()
        _run_migrations(conn)
        conn.commit()
        print("[DB] Database initialised successfully.")
    except sqlite3.Error as exc:
        print(f"[DB] Initialisation error: {exc}")
        raise
    finally:
        conn.close()


init_db = initialize_database

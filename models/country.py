"""
Country model — database operations for countries and all linked tables.
"""

from __future__ import annotations

import sqlite3
from typing import Optional

from database import get_connection

# ── Canonical country list ────────────────────────────────────────────────────

AVAILABLE_COUNTRIES: dict[str, str] = {
    "country_iran":   "🇮🇷 ایران",
    "country_usa":    "🇺🇸 آمریکا",
    "country_russia": "🇷🇺 روسیه",
    "country_israel": "🇮🇱 اسرائیل",
}

# ── Official starting values ──────────────────────────────────────────────────

_COUNTRY_DEFAULTS = dict(
    budget                = 500_000_000_000,
    population            = 50_000_000,
    active_population     = 50_000_000,
    available_recruits    = 0,
    economy_level         = "سطح پایه",
    military_level        = "سطح پایه",
    technology_level      = 1,
    industry_level        = "سطح پایه",
    public_satisfaction   = 80,
    government_popularity = 75,
    global_reputation     = "پایه",
    energy_security       = "پایه",
    food_security         = "پایه",
    current_day           = 0,
)

_RESOURCES_DEFAULTS = dict(
    oil         = 2_000_000,
    gas         = 3_000_000,
    steel       = 20_000,
    iron        = 50_000,
    uranium     = 1_000,
    food        = 500_000,
    water       = 5_000_000,
    electricity = 5_000,
)

_BUILDINGS_DEFAULTS = dict(
    civil_factory       = 5,
    military_factory    = 3,
    aircraft_factory    = 0,
    shipyard            = 0,
    missile_factory     = 0,
    armor_factory       = 0,
    electronics_factory = 0,
    power_plant         = 3,
    refinery            = 2,
    research_center     = 1,
    satellite_center    = 0,
    warehouse           = 1,
    logistics_center    = 1,
)

_ECONOMY_DEFAULTS = dict(
    daily_tax_income      = 2_000_000_000,
    daily_industry_income = 1_000_000_000,
    daily_export_income   = 500_000_000,
    daily_maintenance     = 0,
)

_TECHNOLOGY_DEFAULTS = dict(
    technology_level  = 1,
    military_ai       = 0,
    cyber_security    = 0,
    satellite_network = 0,
    quantum_lab       = 0,
)

_MILITARY_DEFAULTS = dict(
    soldiers         = 0,
    tanks            = 0,
    armored_vehicles = 0,
    artillery        = 0,
    rocket_launchers = 0,
    air_defense      = 0,
    radars           = 0,
    fighters         = 0,
    helicopters      = 0,
    drones           = 0,
    support_aircraft = 0,
    warships         = 0,
    submarines       = 0,
    patrol_boats     = 0,
    missiles         = 0,
    army_experience  = "تازه‌کار",
)


# ── Model ─────────────────────────────────────────────────────────────────────

class Country:
    """Typed wrapper around a countries row."""

    def __init__(self, row: sqlite3.Row) -> None:
        self.id: int                    = row["id"]
        self.country_name: str          = row["country_name"]
        self.leader_id: Optional[int]   = row["leader_id"]
        self.budget: float              = row["budget"]
        self.population: int            = row["population"]
        self.active_population: int     = row["active_population"]
        self.available_recruits: int    = row["available_recruits"]
        self.economy_level: str         = row["economy_level"]
        self.military_level: str        = row["military_level"]
        self.technology_level: int      = row["technology_level"]
        self.industry_level: str        = row["industry_level"]
        self.public_satisfaction: int   = row["public_satisfaction"]
        self.government_popularity: int = row["government_popularity"]
        self.global_reputation: str     = row["global_reputation"]
        self.energy_security: str       = row["energy_security"]
        self.food_security: str         = row["food_security"]
        self.current_day: int           = row["current_day"]

    # ── Single-row queries ────────────────────────────────────────────────────

    @staticmethod
    def get_by_id(country_id: int) -> Optional["Country"]:
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT * FROM countries WHERE id = ?", (country_id,)
            ).fetchone()
            return Country(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def get_by_name(country_name: str) -> Optional["Country"]:
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT * FROM countries WHERE country_name = ?", (country_name,)
            ).fetchone()
            return Country(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def is_taken(country_name: str) -> bool:
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT id FROM countries WHERE country_name = ?", (country_name,)
            ).fetchone()
            return row is not None
        finally:
            conn.close()

    # ── Linked-table queries ──────────────────────────────────────────────────

    @staticmethod
    def get_economy(country_id: int) -> Optional[sqlite3.Row]:
        conn = get_connection()
        try:
            return conn.execute(
                "SELECT * FROM economy WHERE country_id = ?", (country_id,)
            ).fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_buildings(country_id: int) -> Optional[sqlite3.Row]:
        conn = get_connection()
        try:
            return conn.execute(
                "SELECT * FROM buildings WHERE country_id = ?", (country_id,)
            ).fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_resources(country_id: int) -> Optional[sqlite3.Row]:
        conn = get_connection()
        try:
            return conn.execute(
                "SELECT * FROM resources WHERE country_id = ?", (country_id,)
            ).fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_technology(country_id: int) -> Optional[sqlite3.Row]:
        conn = get_connection()
        try:
            return conn.execute(
                "SELECT * FROM technology WHERE country_id = ?", (country_id,)
            ).fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_military(country_id: int) -> Optional[sqlite3.Row]:
        conn = get_connection()
        try:
            return conn.execute(
                "SELECT * FROM military WHERE country_id = ?", (country_id,)
            ).fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_alliance_names(country_id: int) -> list[str]:
        """Return the names of alliances this country belongs to."""
        conn = get_connection()
        try:
            rows = conn.execute(
                """
                SELECT a.alliance_name
                FROM alliances a
                JOIN alliance_members am ON am.alliance_id = a.id
                WHERE am.country_id = ?
                """,
                (country_id,),
            ).fetchall()
            return [r["alliance_name"] for r in rows]
        finally:
            conn.close()

    # ── Creation ──────────────────────────────────────────────────────────────

    @staticmethod
    def create(country_name: str, leader_telegram_id: int) -> "Country":
        """
        Insert the country and all linked satellite rows in one transaction.
        """
        conn = get_connection()
        try:
            with conn:
                cursor = conn.execute(
                    """
                    INSERT INTO countries (
                        country_name, leader_id,
                        budget, population, active_population, available_recruits,
                        economy_level, military_level, technology_level,
                        industry_level, public_satisfaction, government_popularity,
                        global_reputation, energy_security, food_security, current_day
                    ) VALUES (
                        :country_name, :leader_id,
                        :budget, :population, :active_population, :available_recruits,
                        :economy_level, :military_level, :technology_level,
                        :industry_level, :public_satisfaction, :government_popularity,
                        :global_reputation, :energy_security, :food_security, :current_day
                    )
                    """,
                    {"country_name": country_name, "leader_id": leader_telegram_id,
                     **_COUNTRY_DEFAULTS},
                )
                cid = cursor.lastrowid

                conn.execute(
                    """INSERT INTO resources
                       (country_id,oil,gas,steel,iron,uranium,food,water,electricity)
                       VALUES(:country_id,:oil,:gas,:steel,:iron,:uranium,:food,:water,:electricity)""",
                    {"country_id": cid, **_RESOURCES_DEFAULTS},
                )
                conn.execute(
                    """INSERT INTO buildings
                       (country_id,civil_factory,military_factory,aircraft_factory,
                        shipyard,missile_factory,armor_factory,electronics_factory,
                        power_plant,refinery,research_center,satellite_center,
                        warehouse,logistics_center)
                       VALUES(:country_id,:civil_factory,:military_factory,:aircraft_factory,
                        :shipyard,:missile_factory,:armor_factory,:electronics_factory,
                        :power_plant,:refinery,:research_center,:satellite_center,
                        :warehouse,:logistics_center)""",
                    {"country_id": cid, **_BUILDINGS_DEFAULTS},
                )
                conn.execute(
                    """INSERT INTO economy
                       (country_id,daily_tax_income,daily_industry_income,
                        daily_export_income,daily_maintenance)
                       VALUES(:country_id,:daily_tax_income,:daily_industry_income,
                        :daily_export_income,:daily_maintenance)""",
                    {"country_id": cid, **_ECONOMY_DEFAULTS},
                )
                conn.execute(
                    """INSERT INTO technology
                       (country_id,technology_level,military_ai,
                        cyber_security,satellite_network,quantum_lab)
                       VALUES(:country_id,:technology_level,:military_ai,
                        :cyber_security,:satellite_network,:quantum_lab)""",
                    {"country_id": cid, **_TECHNOLOGY_DEFAULTS},
                )
                conn.execute(
                    """INSERT INTO military
                       (country_id,soldiers,tanks,armored_vehicles,artillery,
                        rocket_launchers,air_defense,radars,fighters,helicopters,
                        drones,support_aircraft,warships,submarines,patrol_boats,
                        missiles,army_experience)
                       VALUES(:country_id,:soldiers,:tanks,:armored_vehicles,:artillery,
                        :rocket_launchers,:air_defense,:radars,:fighters,:helicopters,
                        :drones,:support_aircraft,:warships,:submarines,:patrol_boats,
                        :missiles,:army_experience)""",
                    {"country_id": cid, **_MILITARY_DEFAULTS},
                )

            return Country.get_by_id(cid)  # type: ignore[return-value]
        finally:
            conn.close()

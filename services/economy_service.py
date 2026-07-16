"""
Economy Service — Phase 5
Handles daily income collection, building maintenance calculation, and day progression.
"""

from __future__ import annotations

from database import get_connection

# ── Official MBN building maintenance costs (per unit, per day) ──────────────

BUILDING_MAINTENANCE: dict[str, int] = {
    "civil_factory":       50_000_000,
    "military_factory":    75_000_000,
    "aircraft_factory":   120_000_000,
    "shipyard":           150_000_000,
    "missile_factory":    100_000_000,
    "armor_factory":       80_000_000,
    "electronics_factory": 90_000_000,
    "power_plant":         30_000_000,
    "refinery":            50_000_000,
    "research_center":     40_000_000,
    "satellite_center":    70_000_000,
    "warehouse":           10_000_000,
    "logistics_center":    20_000_000,
}


# ── Public API ────────────────────────────────────────────────────────────────

def collect_daily_income(country_id: int) -> dict:
    """
    Load income values from the economy table and return a breakdown dict.

    Returns:
        {
            "tax":      float,
            "industry": float,
            "exports":  float,
            "total":    float,
        }
    """
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT daily_tax_income, daily_industry_income, daily_export_income "
            "FROM economy WHERE country_id = ?",
            (country_id,),
        ).fetchone()

        if not row:
            return {"tax": 0, "industry": 0, "exports": 0, "total": 0}

        tax      = float(row["daily_tax_income"])
        industry = float(row["daily_industry_income"])
        exports  = float(row["daily_export_income"])

        return {
            "tax":      tax,
            "industry": industry,
            "exports":  exports,
            "total":    tax + industry + exports,
        }
    finally:
        conn.close()


def calculate_daily_maintenance(country_id: int) -> float:
    """
    Sum maintenance costs across all owned buildings using official MBN rates.
    Writes the result into the economy table and returns the total.

    Returns:
        Total daily maintenance cost (float).
    """
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM buildings WHERE country_id = ?", (country_id,)
        ).fetchone()

        if not row:
            return 0.0

        total: float = sum(
            BUILDING_MAINTENANCE[building] * int(row[building])
            for building in BUILDING_MAINTENANCE
        )

        with conn:
            conn.execute(
                "UPDATE economy SET daily_maintenance = ?, "
                "updated_at = strftime('%Y-%m-%d %H:%M:%S','now') "
                "WHERE country_id = ?",
                (total, country_id),
            )

        return total
    finally:
        conn.close()


def next_day(country_id: int) -> dict:
    """
    Advance the game by one day for the given country:
      1. Collect income (from economy table).
      2. Calculate maintenance (from buildings table, writes to economy).
      3. Update budget and current_day in the countries table.

    Returns a report dict:
        {
            "day":            int,      # new current_day after increment
            "income":         dict,     # from collect_daily_income()
            "maintenance":    float,
            "budget_before":  float,
            "budget_after":   float,
        }
    """
    # Step 1: current state
    conn = get_connection()
    try:
        country_row = conn.execute(
            "SELECT budget, current_day FROM countries WHERE id = ?",
            (country_id,),
        ).fetchone()
    finally:
        conn.close()

    if not country_row:
        raise ValueError(f"Country {country_id} not found.")

    budget_before = float(country_row["budget"])
    current_day   = int(country_row["current_day"])

    # Step 2: calculate income and maintenance
    income      = collect_daily_income(country_id)
    maintenance = calculate_daily_maintenance(country_id)

    # Step 3: compute new values
    budget_after = budget_before + income["total"] - maintenance
    new_day      = current_day + 1

    # Step 4: persist
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                "UPDATE countries "
                "SET budget = ?, current_day = ?, "
                "    updated_at = strftime('%Y-%m-%d %H:%M:%S','now') "
                "WHERE id = ?",
                (budget_after, new_day, country_id),
            )
    finally:
        conn.close()

    return {
        "day":           new_day,
        "income":        income,
        "maintenance":   maintenance,
        "budget_before": budget_before,
        "budget_after":  budget_after,
    }

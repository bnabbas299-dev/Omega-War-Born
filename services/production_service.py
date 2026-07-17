"""
Production Service — Phase 8
Handles factory construction and military equipment production.
"""

from __future__ import annotations
from datetime import datetime, timedelta

from database import get_connection

# ── Factory catalog ───────────────────────────────────────────────────────────

FACTORY_CATALOG: dict[str, dict] = {
    "military": {
        "name":          "🏭 کارخانه نظامی",
        "price":         10_000_000_000,
        "tech_req":      1,
        "build_minutes": 120,
    },
    "armor": {
        "name":          "🛡 کارخانه زرهی",
        "price":         15_000_000_000,
        "tech_req":      2,
        "build_minutes": 120,
    },
    "missile": {
        "name":          "🚀 کارخانه موشک‌سازی",
        "price":         20_000_000_000,
        "tech_req":      3,
        "build_minutes": 180,
    },
    "electronics": {
        "name":          "🛰 کارخانه الکترونیک",
        "price":         18_000_000_000,
        "tech_req":      3,
        "build_minutes": 180,
    },
    "aircraft": {
        "name":          "✈ کارخانه هواپیماسازی",
        "price":         30_000_000_000,
        "tech_req":      4,
        "build_minutes": 300,
    },
    "shipyard": {
        "name":          "🚢 کارخانه کشتی‌سازی",
        "price":         40_000_000_000,
        "tech_req":      5,
        "build_minutes": 360,
    },
}

# ── Production catalog ────────────────────────────────────────────────────────
# price_per_unit: cost per single unit (cheaper than market — player built a factory)
# minutes_per_unit: production time per unit

PRODUCTION_CATALOG: dict[str, dict] = {

    # ── Military Factory ──────────────────────────────────────────────────
    "prod_vehicle": {
        "name":             "🚙 خودرو تاکتیکی",
        "factory":          "military",
        "price_per_unit":   5_000_000,
        "minutes_per_unit": 10,
        "military_col":     "armored_vehicles",
    },
    "prod_truck": {
        "name":             "🚛 کامیون نظامی",
        "factory":          "military",
        "price_per_unit":   8_000_000,
        "minutes_per_unit": 10,
        "military_col":     "armored_vehicles",
    },
    "prod_soldier": {
        "name":             "👥 سرباز",
        "factory":          "military",
        "price_per_unit":   100_000,
        "minutes_per_unit": 1,
        "military_col":     "soldiers",
    },

    # ── Armor Factory ─────────────────────────────────────────────────────
    "prod_tank": {
        "name":             "🪖 تانک",
        "factory":          "armor",
        "price_per_unit":   50_000_000,
        "minutes_per_unit": 30,
        "military_col":     "tanks",
    },
    "prod_apc": {
        "name":             "🛡 نفربر APC",
        "factory":          "armor",
        "price_per_unit":   30_000_000,
        "minutes_per_unit": 20,
        "military_col":     "armored_vehicles",
    },
    "prod_ifv": {
        "name":             "🛡 IFV",
        "factory":          "armor",
        "price_per_unit":   40_000_000,
        "minutes_per_unit": 25,
        "military_col":     "armored_vehicles",
    },

    # ── Aircraft Factory ──────────────────────────────────────────────────
    "prod_fighter": {
        "name":             "✈ جنگنده",
        "factory":          "aircraft",
        "price_per_unit":   300_000_000,
        "minutes_per_unit": 120,
        "military_col":     "fighters",
    },
    "prod_helicopter": {
        "name":             "🚁 بالگرد",
        "factory":          "aircraft",
        "price_per_unit":   150_000_000,
        "minutes_per_unit": 90,
        "military_col":     "helicopters",
    },
    "prod_drone_air": {
        "name":             "🛩 پهپاد",
        "factory":          "aircraft",
        "price_per_unit":   25_000_000,
        "minutes_per_unit": 20,
        "military_col":     "drones",
    },

    # ── Shipyard ──────────────────────────────────────────────────────────
    "prod_warship": {
        "name":             "🚢 ناو",
        "factory":          "shipyard",
        "price_per_unit":   1_000_000_000,
        "minutes_per_unit": 360,
        "military_col":     "warships",
    },
    "prod_submarine": {
        "name":             "🌊 زیردریایی",
        "factory":          "shipyard",
        "price_per_unit":   2_000_000_000,
        "minutes_per_unit": 600,
        "military_col":     "submarines",
    },
    "prod_patrol": {
        "name":             "🚤 قایق رزمی",
        "factory":          "shipyard",
        "price_per_unit":   40_000_000,
        "minutes_per_unit": 30,
        "military_col":     "patrol_boats",
    },

    # ── Missile Factory ───────────────────────────────────────────────────
    "prod_t_missile": {
        "name":             "🚀 موشک تاکتیکی",
        "factory":          "missile",
        "price_per_unit":   30_000_000,
        "minutes_per_unit": 15,
        "military_col":     "missiles",
    },
    "prod_c_missile": {
        "name":             "🚀 موشک کروز",
        "factory":          "missile",
        "price_per_unit":   150_000_000,
        "minutes_per_unit": 30,
        "military_col":     "missiles",
    },
    "prod_ballistic": {
        "name":             "🚀 موشک بالستیک",
        "factory":          "missile",
        "price_per_unit":   500_000_000,
        "minutes_per_unit": 60,
        "military_col":     "missiles",
    },

    # ── Electronics Factory ───────────────────────────────────────────────
    "prod_recon_drone": {
        "name":             "🛩 پهپاد شناسایی",
        "factory":          "electronics",
        "price_per_unit":   10_000_000,
        "minutes_per_unit": 15,
        "military_col":     "drones",
    },
    "prod_combat_drone": {
        "name":             "🛩 پهپاد رزمی",
        "factory":          "electronics",
        "price_per_unit":   25_000_000,
        "minutes_per_unit": 25,
        "military_col":     "drones",
    },
}


# ── Service functions ─────────────────────────────────────────────────────────

def check_budget(country_id: int, total_cost: float) -> tuple[bool, float]:
    """Return (has_enough, current_budget)."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT budget FROM countries WHERE id = ?", (country_id,)
        ).fetchone()
        budget = float(row["budget"]) if row else 0.0
        return budget >= total_cost, budget
    finally:
        conn.close()


def check_technology(country_id: int, tech_req: int) -> tuple[bool, int]:
    """Return (meets_requirement, current_level)."""
    if tech_req <= 0:
        return True, 0
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT technology_level FROM technology WHERE country_id = ?",
            (country_id,),
        ).fetchone()
        level = int(row["technology_level"]) if row else 0
        return level >= tech_req, level
    finally:
        conn.close()


def check_factory_requirements(country_id: int, factory_type: str) -> tuple[bool, int]:
    """Return (has_factory, count). True when the country owns ≥1 of this type."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT count FROM factories WHERE country_id = ? AND factory_type = ?",
            (country_id, factory_type),
        ).fetchone()
        count = int(row["count"]) if row else 0
        return count > 0, count
    finally:
        conn.close()


def check_resources(country_id: int) -> dict:
    """Return the resource row for the country (for future use)."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM resources WHERE country_id = ?", (country_id,)
        ).fetchone()
        return dict(row) if row else {}
    finally:
        conn.close()


def get_active_productions(country_id: int) -> list[dict]:
    """Return all in-progress queue rows for this country, ordered by finish_time."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM production_queue "
            "WHERE country_id = ? AND status = 'in_progress' "
            "ORDER BY finish_time ASC",
            (country_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def build_factory(country_id: int, factory_key: str) -> dict:
    """
    Start construction of a factory.
    Returns result dict — check result["success"].
    """
    info = FACTORY_CATALOG.get(factory_key)
    if not info:
        return {"success": False, "error": "unknown"}

    tech_ok, tech_level = check_technology(country_id, info["tech_req"])
    if not tech_ok:
        return {"success": False, "error": "tech", "need": info["tech_req"], "have": tech_level}

    budget_ok, budget = check_budget(country_id, info["price"])
    if not budget_ok:
        return {"success": False, "error": "budget", "cost": info["price"], "budget": budget}

    now        = datetime.utcnow()
    finish_at  = now + timedelta(minutes=info["build_minutes"])
    finish_str = finish_at.strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    try:
        with conn:
            conn.execute(
                "UPDATE countries SET budget = budget - ?, "
                "updated_at = strftime('%Y-%m-%d %H:%M:%S','now') WHERE id = ?",
                (info["price"], country_id),
            )
            conn.execute(
                "INSERT INTO production_queue "
                "(country_id, queue_type, item_key, item_name, quantity, cost, finish_time) "
                "VALUES (?, 'factory', ?, ?, 1, ?, ?)",
                (country_id, factory_key, info["name"], info["price"], finish_str),
            )
    finally:
        conn.close()

    return {
        "success":    True,
        "name":       info["name"],
        "cost":       info["price"],
        "remaining":  budget - info["price"],
        "finish_str": finish_str,
        "minutes":    info["build_minutes"],
    }


def start_production(country_id: int, prod_key: str, quantity: int) -> dict:
    """
    Enqueue equipment production.
    Returns result dict — check result["success"].
    """
    info = PRODUCTION_CATALOG.get(prod_key)
    if not info:
        return {"success": False, "error": "unknown"}

    if quantity <= 0:
        return {"success": False, "error": "qty_zero"}

    # Factory check
    has_factory, fcount = check_factory_requirements(country_id, info["factory"])
    if not has_factory:
        fac_name = FACTORY_CATALOG.get(info["factory"], {}).get("name", info["factory"])
        return {"success": False, "error": "no_factory", "factory_name": fac_name}

    total_cost    = info["price_per_unit"] * quantity
    total_minutes = info["minutes_per_unit"] * quantity

    budget_ok, budget = check_budget(country_id, total_cost)
    if not budget_ok:
        return {"success": False, "error": "budget", "cost": total_cost, "budget": budget}

    now        = datetime.utcnow()
    finish_at  = now + timedelta(minutes=total_minutes)
    finish_str = finish_at.strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    try:
        with conn:
            conn.execute(
                "UPDATE countries SET budget = budget - ?, "
                "updated_at = strftime('%Y-%m-%d %H:%M:%S','now') WHERE id = ?",
                (total_cost, country_id),
            )
            conn.execute(
                "INSERT INTO production_queue "
                "(country_id, queue_type, item_key, item_name, quantity, cost, "
                " military_col, factory_type, finish_time) "
                "VALUES (?, 'equipment', ?, ?, ?, ?, ?, ?, ?)",
                (
                    country_id, prod_key, info["name"], quantity, total_cost,
                    info["military_col"], info["factory"], finish_str,
                ),
            )
    finally:
        conn.close()

    return {
        "success":      True,
        "name":         info["name"],
        "quantity":     quantity,
        "total_cost":   total_cost,
        "remaining":    budget - total_cost,
        "minutes":      total_minutes,
        "finish_str":   finish_str,
    }


def cancel_production(queue_id: int, country_id: int) -> dict:
    """
    Cancel a queued production order and refund 50% of the cost.
    Only items still in_progress can be cancelled.
    """
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM production_queue WHERE id = ? AND country_id = ? AND status = 'in_progress'",
            (queue_id, country_id),
        ).fetchone()
        if not row:
            return {"success": False, "error": "not_found"}

        refund = row["cost"] * 0.5
        with conn:
            conn.execute(
                "UPDATE production_queue SET status = 'cancelled' WHERE id = ?",
                (queue_id,),
            )
            conn.execute(
                "UPDATE countries SET budget = budget + ?, "
                "updated_at = strftime('%Y-%m-%d %H:%M:%S','now') WHERE id = ?",
                (refund, country_id),
            )
        return {"success": True, "refund": refund, "name": row["item_name"]}
    finally:
        conn.close()


def finish_production(queue_id: int) -> dict | None:
    """
    Complete a single production_queue entry.
    - factory  → upsert into factories
    - equipment → increment military column
    Logs to production_history. Returns the completed row dict or None.
    """
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM production_queue WHERE id = ? AND status = 'in_progress'",
            (queue_id,),
        ).fetchone()
        if not row:
            return None

        row = dict(row)
        with conn:
            if row["queue_type"] == "factory":
                conn.execute(
                    "INSERT INTO factories (country_id, factory_type, count) "
                    "VALUES (?, ?, 1) "
                    "ON CONFLICT(country_id, factory_type) DO UPDATE "
                    "SET count = count + 1, updated_at = strftime('%Y-%m-%d %H:%M:%S','now')",
                    (row["country_id"], row["item_key"]),
                )
            else:
                col = row["military_col"]
                conn.execute(
                    f"UPDATE military SET {col} = {col} + ?, "
                    f"updated_at = strftime('%Y-%m-%d %H:%M:%S','now') "
                    f"WHERE country_id = ?",
                    (row["quantity"], row["country_id"]),
                )

            conn.execute(
                "INSERT INTO production_history "
                "(country_id, queue_type, item_key, item_name, quantity, cost, factory_type) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    row["country_id"], row["queue_type"], row["item_key"],
                    row["item_name"], row["quantity"], row["cost"], row["factory_type"],
                ),
            )
            conn.execute(
                "UPDATE production_queue SET status = 'completed', notified = 1 WHERE id = ?",
                (queue_id,),
            )
        return row
    finally:
        conn.close()


def get_all_in_progress_global() -> list[dict]:
    """
    Return every in_progress production_queue row whose finish_time has passed.
    Joins countries to get leader_id for notifications.
    """
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT pq.*, c.leader_id "
            "FROM production_queue pq "
            "JOIN countries c ON c.id = pq.country_id "
            "WHERE pq.status = 'in_progress' "
            "AND pq.finish_time <= strftime('%Y-%m-%d %H:%M:%S','now')"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_owned_factories(country_id: int) -> list[dict]:
    """Return all owned factory rows for a country."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT factory_type, count FROM factories WHERE country_id = ? ORDER BY factory_type",
            (country_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

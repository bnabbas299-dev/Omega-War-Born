"""
Technology Service — Phase 9
Handles technology level upgrades and special technology research.
"""

from __future__ import annotations
from datetime import datetime, timedelta

from database import get_connection

# ── Level upgrade catalog ─────────────────────────────────────────────────────
# Key = target level (2–10)

LEVEL_UPGRADES: dict[int, dict] = {
    2:  {"price": 5_000_000_000,   "minutes": 30},
    3:  {"price": 8_000_000_000,   "minutes": 45},
    4:  {"price": 12_000_000_000,  "minutes": 60},
    5:  {"price": 18_000_000_000,  "minutes": 120},
    6:  {"price": 25_000_000_000,  "minutes": 180},
    7:  {"price": 35_000_000_000,  "minutes": 300},
    8:  {"price": 50_000_000_000,  "minutes": 360},
    9:  {"price": 70_000_000_000,  "minutes": 480},
    10: {"price": 100_000_000_000, "minutes": 600},
}

MAX_LEVEL = 10

# ── Special technology catalog ────────────────────────────────────────────────
# db_col: column in the 'technology' table that is set to 1 on unlock
# tech_req: minimum technology_level to start research

SPECIAL_TECH_CATALOG: dict[str, dict] = {
    "military_ai": {
        "name":     "🤖 هوش مصنوعی نظامی",
        "name_en":  "Military AI",
        "effect":   "+۱۰٪ عملکرد ارتش",
        "price":    10_000_000_000,
        "minutes":  120,
        "tech_req": 3,
        "db_col":   "military_ai",
    },
    "cyber_security": {
        "name":     "💻 امنیت سایبری",
        "name_en":  "Cyber Security",
        "effect":   "+۲۰٪ دفاع سایبری",
        "price":    8_000_000_000,
        "minutes":  90,
        "tech_req": 2,
        "db_col":   "cyber_security",
    },
    "satellite_network": {
        "name":     "🛰 شبکه ماهواره‌ای",
        "name_en":  "Satellite Network",
        "effect":   "افزایش توان اطلاعاتی",
        "price":    12_000_000_000,
        "minutes":  120,
        "tech_req": 3,
        "db_col":   "satellite_network",
    },
    "quantum_lab": {
        "name":     "⚛ آزمایشگاه کوانتوم",
        "name_en":  "Quantum Lab",
        "effect":   "+۲۵٪ سرعت تحقیق",
        "price":    20_000_000_000,
        "minutes":  240,
        "tech_req": 5,
        "db_col":   "quantum_lab",
    },
    "industrial_automation": {
        "name":     "🏭 اتوماسیون صنعتی",
        "name_en":  "Industrial Automation",
        "effect":   "+۱۵٪ سرعت تولید",
        "price":    15_000_000_000,
        "minutes":  180,
        "tech_req": 4,
        "db_col":   "industrial_automation",
    },
    "smart_energy_grid": {
        "name":     "⚡ شبکه انرژی هوشمند",
        "name_en":  "Smart Energy Grid",
        "effect":   "+۱۰٪ بازدهی انرژی",
        "price":    10_000_000_000,
        "minutes":  120,
        "tech_req": 3,
        "db_col":   "smart_energy_grid",
    },
    "national_intelligence": {
        "name":     "🌐 شبکه اطلاعات ملی",
        "name_en":  "National Intelligence Network",
        "effect":   "افزایش موفقیت جاسوسی",
        "price":    18_000_000_000,
        "minutes":  240,
        "tech_req": 4,
        "db_col":   "national_intelligence_network",
    },
}


# ── Helper queries ────────────────────────────────────────────────────────────

def _get_tech_row(country_id: int, conn):
    return conn.execute(
        "SELECT * FROM technology WHERE country_id = ?", (country_id,)
    ).fetchone()


def _get_budget(country_id: int, conn) -> float:
    row = conn.execute(
        "SELECT budget FROM countries WHERE id = ?", (country_id,)
    ).fetchone()
    return float(row["budget"]) if row else 0.0


def _is_already_researching(country_id: int, item_key: str, conn) -> bool:
    row = conn.execute(
        "SELECT id FROM research_queue "
        "WHERE country_id = ? AND item_key = ? AND status = 'in_progress'",
        (country_id, item_key),
    ).fetchone()
    return row is not None


# ── Service functions ─────────────────────────────────────────────────────────

def open_research() -> dict:
    """Return catalogs for the UI."""
    return {"specials": SPECIAL_TECH_CATALOG, "levels": LEVEL_UPGRADES}


def check_requirements(
    country_id: int,
    item_key: str,
    research_type: str,
) -> dict:
    """
    Validate all preconditions for starting research.
    Returns {"ok": True} or {"ok": False, "error": reason_key, ...extra}.
    """
    conn = get_connection()
    try:
        tech  = _get_tech_row(country_id, conn)
        level = int(tech["technology_level"]) if tech else 1

        if research_type == "level_upgrade":
            target = int(item_key.replace("level_", ""))
            if level >= MAX_LEVEL:
                return {"ok": False, "error": "max_level"}
            if target != level + 1:
                return {"ok": False, "error": "wrong_target"}
            info = LEVEL_UPGRADES.get(target)
            if not info:
                return {"ok": False, "error": "unknown"}

            if _is_already_researching(country_id, item_key, conn):
                return {"ok": False, "error": "duplicate"}

            budget = _get_budget(country_id, conn)
            if budget < info["price"]:
                return {"ok": False, "error": "budget", "cost": info["price"], "budget": budget}

        else:  # special_tech
            info = SPECIAL_TECH_CATALOG.get(item_key)
            if not info:
                return {"ok": False, "error": "unknown"}

            if level < info["tech_req"]:
                return {"ok": False, "error": "tech", "need": info["tech_req"], "have": level}

            # Already unlocked?
            col = info["db_col"]
            if tech and tech[col]:
                return {"ok": False, "error": "already_unlocked"}

            if _is_already_researching(country_id, item_key, conn):
                return {"ok": False, "error": "duplicate"}

            budget = _get_budget(country_id, conn)
            if budget < info["price"]:
                return {"ok": False, "error": "budget", "cost": info["price"], "budget": budget}

        return {"ok": True}
    finally:
        conn.close()


def start_research(
    country_id: int,
    item_key: str,
    research_type: str,
) -> dict:
    """
    Enqueue a research item.
    Returns result dict — check result["success"].
    """
    check = check_requirements(country_id, item_key, research_type)
    if not check["ok"]:
        return {"success": False, **check}

    if research_type == "level_upgrade":
        target = int(item_key.replace("level_", ""))
        info   = LEVEL_UPGRADES[target]
        name   = f"ارتقاء سطح فناوری به سطح {target}"
        cost   = info["price"]
        mins   = info["minutes"]
    else:
        info = SPECIAL_TECH_CATALOG[item_key]
        name = info["name"]
        cost = info["price"]
        mins = info["minutes"]

    now        = datetime.utcnow()
    finish_at  = now + timedelta(minutes=mins)
    finish_str = finish_at.strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    try:
        budget = _get_budget(country_id, conn)
        with conn:
            conn.execute(
                "UPDATE countries SET budget = budget - ?, "
                "updated_at = strftime('%Y-%m-%d %H:%M:%S','now') WHERE id = ?",
                (cost, country_id),
            )
            conn.execute(
                "INSERT INTO research_queue "
                "(country_id, research_type, item_key, item_name, cost, finish_time) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (country_id, research_type, item_key, name, cost, finish_str),
            )
        return {
            "success":   True,
            "name":      name,
            "cost":      cost,
            "remaining": budget - cost,
            "minutes":   mins,
            "finish_str": finish_str,
        }
    finally:
        conn.close()


def unlock_technology(country_id: int, tech_key: str) -> None:
    """Set the special tech column to 1 and record in technology_unlocks."""
    info = SPECIAL_TECH_CATALOG.get(tech_key)
    if not info:
        return
    col = info["db_col"]
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                f"UPDATE technology SET {col} = 1, "
                f"updated_at = strftime('%Y-%m-%d %H:%M:%S','now') "
                f"WHERE country_id = ?",
                (country_id,),
            )
            conn.execute(
                "INSERT OR IGNORE INTO technology_unlocks (country_id, tech_key) VALUES (?, ?)",
                (country_id, tech_key),
            )
    finally:
        conn.close()


def finish_research(queue_id: int) -> dict | None:
    """
    Complete one research_queue entry.
    - level_upgrade  → increment technology_level in both tables
    - special_tech   → call unlock_technology()
    Logs to research_history. Returns the completed row dict or None.
    """
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM research_queue WHERE id = ? AND status = 'in_progress'",
            (queue_id,),
        ).fetchone()
        if not row:
            return None
        row = dict(row)
    finally:
        conn.close()

    country_id    = row["country_id"]
    research_type = row["research_type"]
    item_key      = row["item_key"]

    conn = get_connection()
    try:
        with conn:
            if research_type == "level_upgrade":
                conn.execute(
                    "UPDATE technology SET technology_level = technology_level + 1, "
                    "updated_at = strftime('%Y-%m-%d %H:%M:%S','now') "
                    "WHERE country_id = ?",
                    (country_id,),
                )
                conn.execute(
                    "UPDATE countries SET technology_level = technology_level + 1, "
                    "updated_at = strftime('%Y-%m-%d %H:%M:%S','now') "
                    "WHERE id = ?",
                    (country_id,),
                )
            else:
                # unlock the specific column
                info = SPECIAL_TECH_CATALOG.get(item_key)
                if info:
                    col = info["db_col"]
                    conn.execute(
                        f"UPDATE technology SET {col} = 1, "
                        f"updated_at = strftime('%Y-%m-%d %H:%M:%S','now') "
                        f"WHERE country_id = ?",
                        (country_id,),
                    )
                    conn.execute(
                        "INSERT OR IGNORE INTO technology_unlocks (country_id, tech_key) "
                        "VALUES (?, ?)",
                        (country_id, item_key),
                    )

            conn.execute(
                "INSERT INTO research_history "
                "(country_id, research_type, item_key, item_name, cost) "
                "VALUES (?, ?, ?, ?, ?)",
                (country_id, research_type, item_key, row["item_name"], row["cost"]),
            )
            conn.execute(
                "UPDATE research_queue SET status = 'completed', notified = 1 WHERE id = ?",
                (queue_id,),
            )
        return row
    finally:
        conn.close()


def cancel_research(queue_id: int, country_id: int) -> dict:
    """Cancel a queued research and refund 50%."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM research_queue "
            "WHERE id = ? AND country_id = ? AND status = 'in_progress'",
            (queue_id, country_id),
        ).fetchone()
        if not row:
            return {"success": False, "error": "not_found"}
        refund = row["cost"] * 0.5
        with conn:
            conn.execute(
                "UPDATE research_queue SET status = 'cancelled' WHERE id = ?", (queue_id,)
            )
            conn.execute(
                "UPDATE countries SET budget = budget + ?, "
                "updated_at = strftime('%Y-%m-%d %H:%M:%S','now') WHERE id = ?",
                (refund, country_id),
            )
        return {"success": True, "refund": refund, "name": row["item_name"]}
    finally:
        conn.close()


def get_active_research(country_id: int) -> list[dict]:
    """Return all in-progress research rows for a country, ordered by finish_time."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM research_queue "
            "WHERE country_id = ? AND status = 'in_progress' "
            "ORDER BY finish_time ASC",
            (country_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_tech_status(country_id: int) -> dict:
    """Return technology row + list of unlocked special tech keys."""
    conn = get_connection()
    try:
        tech = conn.execute(
            "SELECT * FROM technology WHERE country_id = ?", (country_id,)
        ).fetchone()
        unlocks = conn.execute(
            "SELECT tech_key FROM technology_unlocks WHERE country_id = ?", (country_id,)
        ).fetchall()
        return {
            "tech": dict(tech) if tech else {},
            "unlocked": {r["tech_key"] for r in unlocks},
        }
    finally:
        conn.close()


def get_all_finished_global() -> list[dict]:
    """Return research_queue rows whose finish_time has passed, with leader_id."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT rq.*, c.leader_id "
            "FROM research_queue rq "
            "JOIN countries c ON c.id = rq.country_id "
            "WHERE rq.status = 'in_progress' "
            "AND rq.finish_time <= strftime('%Y-%m-%d %H:%M:%S','now')"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

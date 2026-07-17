"""
Building Service — Phase 6
Handles construction: catalog lookup, validation, queue management,
and automatic completion processing.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from database import get_connection

# ── Building catalog ──────────────────────────────────────────────────────────
# All monetary values in absolute numbers (not billions).
# build_minutes: construction duration in minutes.
# tech_req: minimum technology_level required (0 = no requirement).

CATALOG: dict[str, dict] = {
    "military_factory": {
        "name":          "کارخانه نظامی",
        "emoji":         "🏭",
        "price":         10_000_000_000,
        "tech_req":      1,
        "build_minutes": 120,
        "benefit":       "تولید تجهیزات نظامی و افزایش توان رزمی کشور",
        "maintenance":   75_000_000,
    },
    "aircraft_factory": {
        "name":          "کارخانه هواپیماسازی",
        "emoji":         "✈",
        "price":         30_000_000_000,
        "tech_req":      4,
        "build_minutes": 300,
        "benefit":       "تولید جنگنده، بالگرد و هواپیمای پشتیبانی هوایی",
        "maintenance":   120_000_000,
    },
    "shipyard": {
        "name":          "کارخانه کشتی‌سازی",
        "emoji":         "🚢",
        "price":         40_000_000_000,
        "tech_req":      5,
        "build_minutes": 360,
        "benefit":       "ساخت ناو، زیردریایی و قایق‌های رزمی دریایی",
        "maintenance":   150_000_000,
    },
    "missile_factory": {
        "name":          "کارخانه موشک‌سازی",
        "emoji":         "🚀",
        "price":         20_000_000_000,
        "tech_req":      3,
        "build_minutes": 180,
        "benefit":       "تولید موشک‌های بالستیک و سیستم‌های راکتی",
        "maintenance":   100_000_000,
    },
    "armor_factory": {
        "name":          "کارخانه زرهی",
        "emoji":         "🛡",
        "price":         15_000_000_000,
        "tech_req":      2,
        "build_minutes": 120,
        "benefit":       "تولید تانک، خودروی زرهی و پوشش حفاظتی نیروها",
        "maintenance":   80_000_000,
    },
    "electronics_factory": {
        "name":          "کارخانه الکترونیک",
        "emoji":         "🛰",
        "price":         18_000_000_000,
        "tech_req":      3,
        "build_minutes": 180,
        "benefit":       "تولید رادار، سیستم‌های الکترونیک و تجهیزات پیشرفته",
        "maintenance":   90_000_000,
    },
    "power_plant": {
        "name":          "نیروگاه",
        "emoji":         "⚡",
        "price":         8_000_000_000,
        "tech_req":      0,
        "build_minutes": 120,
        "benefit":       "تأمین برق کشور و افزایش ظرفیت تولید انرژی",
        "maintenance":   30_000_000,
    },
    "refinery": {
        "name":          "پالایشگاه",
        "emoji":         "🛢",
        "price":         10_000_000_000,
        "tech_req":      0,
        "build_minutes": 120,
        "benefit":       "پالایش نفت خام و تولید سوخت و فرآورده‌های پتروشیمی",
        "maintenance":   50_000_000,
    },
    "warehouse": {
        "name":          "انبار",
        "emoji":         "📦",
        "price":         3_000_000_000,
        "tech_req":      0,
        "build_minutes": 30,
        "benefit":       "افزایش ظرفیت ذخیره‌سازی منابع ملی",
        "maintenance":   10_000_000,
    },
    "logistics_center": {
        "name":          "مرکز لجستیک",
        "emoji":         "🚛",
        "price":         5_000_000_000,
        "tech_req":      0,
        "build_minutes": 60,
        "benefit":       "بهینه‌سازی زنجیره تأمین و کاهش هزینه توزیع منابع",
        "maintenance":   20_000_000,
    },
    "satellite_center": {
        "name":          "مرکز کنترل ماهواره",
        "emoji":         "📡",
        "price":         25_000_000_000,
        "tech_req":      5,
        "build_minutes": 360,
        "benefit":       "کنترل ماهواره، جمع‌آوری اطلاعات و ارتباطات پیشرفته",
        "maintenance":   70_000_000,
    },
    "hospital": {
        "name":          "بیمارستان",
        "emoji":         "🏥",
        "price":         5_000_000_000,
        "tech_req":      0,
        "build_minutes": 120,
        "benefit":       "بهبود سلامت عمومی و افزایش رضایت مردم",
        "maintenance":   0,
    },
    "university": {
        "name":          "دانشگاه",
        "emoji":         "🎓",
        "price":         8_000_000_000,
        "tech_req":      0,
        "build_minutes": 180,
        "benefit":       "پیشرفت علمی و کاهش زمان انجام تحقیقات",
        "maintenance":   0,
    },
    "economic_tower": {
        "name":          "برج اقتصادی",
        "emoji":         "🏙",
        "price":         12_000_000_000,
        "tech_req":      0,
        "build_minutes": 240,
        "benefit":       "افزایش درآمد اقتصادی و رونق تجارت داخلی",
        "maintenance":   0,
    },
    "highway": {
        "name":          "بزرگراه",
        "emoji":         "🛣",
        "price":         15_000_000_000,
        "tech_req":      0,
        "build_minutes": 300,
        "benefit":       "توسعه زیرساخت و کاهش هزینه‌های لجستیکی",
        "maintenance":   0,
    },
    "railway": {
        "name":          "راه‌آهن",
        "emoji":         "🚆",
        "price":         18_000_000_000,
        "tech_req":      0,
        "build_minutes": 360,
        "benefit":       "حمل‌ونقل ارزان، توسعه تجارت و انتقال سریع نیرو",
        "maintenance":   0,
    },
    "smart_city": {
        "name":          "شهر هوشمند",
        "emoji":         "🌆",
        "price":         25_000_000_000,
        "tech_req":      0,
        "build_minutes": 480,
        "benefit":       "افزایش جمعیت فعال، بهره‌وری و رضایت شهروندان",
        "maintenance":   0,
    },
    "national_park": {
        "name":          "پارک ملی",
        "emoji":         "🌿",
        "price":         2_000_000_000,
        "tech_req":      0,
        "build_minutes": 60,
        "benefit":       "محیط‌زیست پاک و افزایش محبوبیت دولت",
        "maintenance":   0,
    },
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _now_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def _parse_dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)


def format_duration(minutes: int) -> str:
    if minutes < 60:
        return f"{minutes} دقیقه"
    h, m = divmod(minutes, 60)
    if m == 0:
        return f"{h} ساعت"
    return f"{h} ساعت و {m} دقیقه"


def format_remaining(finish_time_str: str) -> tuple[str, int]:
    """Return (human_label, pct_complete)."""
    now  = datetime.now(timezone.utc)
    end  = _parse_dt(finish_time_str)
    diff = end - now
    secs_left = int(diff.total_seconds())

    if secs_left <= 0:
        return "تکمیل شده ✅", 100

    h, rem = divmod(secs_left, 3600)
    m       = rem // 60
    label   = f"{h} ساعت و {m} دقیقه" if h else f"{m} دقیقه"
    return label, min(99, 0)   # pct calculated separately


def remaining_label_and_pct(row) -> tuple[str, int]:
    """Return (remaining_time_label, completion_pct) for a queue row."""
    now        = datetime.now(timezone.utc)
    start      = _parse_dt(row["start_time"])
    end        = _parse_dt(row["finish_time"])
    total_secs = max(1, (end - start).total_seconds())
    elapsed    = (now - start).total_seconds()
    pct        = int(min(100, (elapsed / total_secs) * 100))

    secs_left  = int((end - now).total_seconds())
    if secs_left <= 0:
        return "تکمیل شده ✅", 100

    h, rem = divmod(secs_left, 3600)
    m       = rem // 60
    label   = f"{h}h {m}m" if h else f"{m}m"
    return label, pct


# ── Service functions ─────────────────────────────────────────────────────────

def get_active_queue(country_id: int) -> list:
    """Return all in_progress construction items for a country."""
    conn = get_connection()
    try:
        return conn.execute(
            "SELECT * FROM construction_queue "
            "WHERE country_id = ? AND status = 'in_progress' "
            "ORDER BY finish_time ASC",
            (country_id,),
        ).fetchall()
    finally:
        conn.close()


def can_build(country_id: int, building_key: str) -> tuple[bool, str]:
    """
    Validate whether a country can start this construction.
    Returns (allowed: bool, reason: str).
    """
    info = CATALOG.get(building_key)
    if not info:
        return False, "ساختمان شناخته‌شده نیست."

    conn = get_connection()
    try:
        country = conn.execute(
            "SELECT budget FROM countries WHERE id = ?", (country_id,)
        ).fetchone()
        if not country:
            return False, "کشور یافت نشد."

        if float(country["budget"]) < info["price"]:
            from utils.panel_builder import _f
            short  = f'{info["price"] / 1_000_000_000:.1f} میلیارد'
            have   = f'{float(country["budget"]) / 1_000_000_000:.1f} میلیارد'
            return False, (
                f"💰 بودجه کافی نیست.\n"
                f"قیمت: {short}\nبودجه فعلی: {have}"
            )

        if info["tech_req"] > 0:
            tech = conn.execute(
                "SELECT technology_level FROM technology WHERE country_id = ?",
                (country_id,),
            ).fetchone()
            level = int(tech["technology_level"]) if tech else 0
            if level < info["tech_req"]:
                return False, (
                    f"🔬 سطح فناوری کافی نیست.\n"
                    f"نیاز: سطح {info['tech_req']} — فعلی: سطح {level}"
                )

        return True, ""
    finally:
        conn.close()


def start_construction(country_id: int, building_key: str) -> dict:
    """
    Deduct budget, insert into construction_queue, log to purchase_history.
    Returns result dict with success flag.
    """
    ok, reason = can_build(country_id, building_key)
    if not ok:
        return {"success": False, "message": reason}

    info       = CATALOG[building_key]
    price      = info["price"]
    minutes    = info["build_minutes"]
    now        = datetime.now(timezone.utc)
    finish     = now + timedelta(minutes=minutes)
    now_str    = now.strftime("%Y-%m-%d %H:%M:%S")
    finish_str = finish.strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    try:
        with conn:
            conn.execute(
                "UPDATE countries SET budget = budget - ?, "
                "updated_at = ? WHERE id = ?",
                (price, now_str, country_id),
            )
            conn.execute(
                "INSERT INTO construction_queue "
                "(country_id, building_name, start_time, finish_time, status) "
                "VALUES (?, ?, ?, ?, 'in_progress')",
                (country_id, building_key, now_str, finish_str),
            )
            conn.execute(
                "INSERT INTO purchase_history "
                "(country_id, item_name, quantity, price, purchase_time) "
                "VALUES (?, ?, 1, ?, ?)",
                (country_id, info["name"], price, now_str),
            )
        return {
            "success":     True,
            "name":        info["name"],
            "finish_time": finish_str,
            "duration":    format_duration(minutes),
        }
    except Exception as exc:
        return {"success": False, "message": str(exc)}
    finally:
        conn.close()


def complete_finished_constructions(country_id: int) -> list[str]:
    """
    Check for finished items, increment building counts, mark completed.
    Returns list of completed building display names.
    """
    now_str = _now_str()
    conn = get_connection()
    try:
        done = conn.execute(
            "SELECT id, building_name FROM construction_queue "
            "WHERE country_id = ? AND status = 'in_progress' AND finish_time <= ?",
            (country_id, now_str),
        ).fetchall()

        completed_names: list[str] = []
        for row in done:
            key  = row["building_name"]
            info = CATALOG.get(key)
            if not info:
                continue

            with conn:
                conn.execute(
                    f"UPDATE buildings SET {key} = {key} + 1, "
                    f"updated_at = ? WHERE country_id = ?",
                    (now_str, country_id),
                )
                conn.execute(
                    "UPDATE construction_queue SET status = 'completed' WHERE id = ?",
                    (row["id"],),
                )
            completed_names.append(info["name"])

        return completed_names
    finally:
        conn.close()


def get_all_in_progress() -> list:
    """Return all in-progress queue rows across all countries (for the job)."""
    now_str = _now_str()
    conn = get_connection()
    try:
        return conn.execute(
            """
            SELECT cq.id, cq.country_id, cq.building_name,
                   c.leader_id
            FROM construction_queue cq
            JOIN countries c ON c.id = cq.country_id
            WHERE cq.status = 'in_progress' AND cq.finish_time <= ?
            """,
            (now_str,),
        ).fetchall()
    finally:
        conn.close()


def mark_completed_and_update(queue_id: int, country_id: int, building_key: str) -> None:
    """Used by the background job to atomically complete one item."""
    now_str = _now_str()
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                f"UPDATE buildings SET {building_key} = {building_key} + 1, "
                f"updated_at = ? WHERE country_id = ?",
                (now_str, country_id),
            )
            conn.execute(
                "UPDATE construction_queue SET status = 'completed' WHERE id = ?",
                (queue_id,),
            )
    finally:
        conn.close()

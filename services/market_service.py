"""
Market Service — Phase 7 (Persian Edition)
MBN Global Market: 75 items across 7 categories.
"""

from __future__ import annotations

from database import get_connection

# ── Market catalog ────────────────────────────────────────────────────────────
# price:        absolute USD value
# tech_req:     minimum technology_level (0 = no requirement)
# category:     used to group items in the menu
# military_col: column in the military table that receives quantity

MARKET_CATALOG: dict[str, dict] = {

    # ════════════════════════════════════════════════════════════════════════
    # 🪖  تجهیزات زمینی
    # ════════════════════════════════════════════════════════════════════════

    "tactical_vehicle": {
        "name":        "🚙 خودروی تاکتیکی",
        "price":       20_000_000,
        "tech_req":    1,
        "category":    "ground",
        "military_col": "armored_vehicles",
    },
    "recon_vehicle": {
        "name":        "🚙 خودروی شناسایی",
        "price":       40_000_000,
        "tech_req":    2,
        "category":    "ground",
        "military_col": "armored_vehicles",
    },
    "military_truck": {
        "name":        "🚛 کامیون نظامی",
        "price":       30_000_000,
        "tech_req":    1,
        "category":    "ground",
        "military_col": "armored_vehicles",
    },
    "armored_ambulance": {
        "name":        "🚑 آمبولانس زرهی",
        "price":       60_000_000,
        "tech_req":    2,
        "category":    "ground",
        "military_col": "armored_vehicles",
    },
    "apc": {
        "name":        "🛡 نفربر APC",
        "price":       90_000_000,
        "tech_req":    2,
        "category":    "ground",
        "military_col": "armored_vehicles",
    },
    "ifv": {
        "name":        "🛡 IFV",
        "price":       140_000_000,
        "tech_req":    3,
        "category":    "ground",
        "military_col": "armored_vehicles",
    },
    "mrap": {
        "name":        "🛡 MRAP",
        "price":       120_000_000,
        "tech_req":    3,
        "category":    "ground",
        "military_col": "armored_vehicles",
    },
    "t72": {
        "name":        "🪖 تانک T-72",
        "price":       80_000_000,
        "tech_req":    2,
        "category":    "ground",
        "military_col": "tanks",
    },
    "t90m": {
        "name":        "🪖 تانک T-90M",
        "price":       160_000_000,
        "tech_req":    4,
        "category":    "ground",
        "military_col": "tanks",
    },
    "leopard2a7": {
        "name":        "🪖 Leopard 2A7",
        "price":       180_000_000,
        "tech_req":    4,
        "category":    "ground",
        "military_col": "tanks",
    },
    "m1a2": {
        "name":        "🪖 M1A2 Abrams",
        "price":       190_000_000,
        "tech_req":    4,
        "category":    "ground",
        "military_col": "tanks",
    },
    "k2": {
        "name":        "🪖 K2 Black Panther",
        "price":       220_000_000,
        "tech_req":    5,
        "category":    "ground",
        "military_col": "tanks",
    },
    "merkava4": {
        "name":        "🪖 Merkava Mk.4",
        "price":       250_000_000,
        "tech_req":    6,
        "category":    "ground",
        "military_col": "tanks",
    },
    "challenger3": {
        "name":        "🪖 Challenger 3",
        "price":       240_000_000,
        "tech_req":    6,
        "category":    "ground",
        "military_col": "tanks",
    },
    "leclerc": {
        "name":        "🪖 Leclerc XLR",
        "price":       230_000_000,
        "tech_req":    5,
        "category":    "ground",
        "military_col": "tanks",
    },
    "t14": {
        "name":        "🪖 T-14 Armata",
        "price":       300_000_000,
        "tech_req":    7,
        "category":    "ground",
        "military_col": "tanks",
    },
    "kf51": {
        "name":        "🪖 KF51 Panther",
        "price":       400_000_000,
        "tech_req":    8,
        "category":    "ground",
        "military_col": "tanks",
    },

    # ════════════════════════════════════════════════════════════════════════
    # ✈  جنگنده‌ها
    # ════════════════════════════════════════════════════════════════════════

    "f16": {
        "name":        "✈ F-16",
        "price":       900_000_000,
        "tech_req":    5,
        "category":    "fighters",
        "military_col": "fighters",
    },
    "gripen": {
        "name":        "✈ Gripen",
        "price":       950_000_000,
        "tech_req":    5,
        "category":    "fighters",
        "military_col": "fighters",
    },
    "rafale": {
        "name":        "✈ Rafale",
        "price":       1_200_000_000,
        "tech_req":    6,
        "category":    "fighters",
        "military_col": "fighters",
    },
    "eurofighter": {
        "name":        "✈ Eurofighter Typhoon",
        "price":       1_300_000_000,
        "tech_req":    6,
        "category":    "fighters",
        "military_col": "fighters",
    },
    "f15ex": {
        "name":        "✈ F-15EX",
        "price":       1_100_000_000,
        "tech_req":    6,
        "category":    "fighters",
        "military_col": "fighters",
    },
    "mig35": {
        "name":        "✈ MiG-35",
        "price":       700_000_000,
        "tech_req":    5,
        "category":    "fighters",
        "military_col": "fighters",
    },
    "su30": {
        "name":        "✈ Su-30",
        "price":       600_000_000,
        "tech_req":    4,
        "category":    "fighters",
        "military_col": "fighters",
    },
    "su35": {
        "name":        "✈ Su-35",
        "price":       850_000_000,
        "tech_req":    5,
        "category":    "fighters",
        "military_col": "fighters",
    },
    "su57": {
        "name":        "✈ Su-57",
        "price":       1_500_000_000,
        "tech_req":    7,
        "category":    "fighters",
        "military_col": "fighters",
    },
    "j10c": {
        "name":        "✈ J-10C",
        "price":       600_000_000,
        "tech_req":    5,
        "category":    "fighters",
        "military_col": "fighters",
    },
    "j20": {
        "name":        "✈ J-20",
        "price":       1_400_000_000,
        "tech_req":    7,
        "category":    "fighters",
        "military_col": "fighters",
    },
    "f35": {
        "name":        "✈ F-35",
        "price":       1_500_000_000,
        "tech_req":    7,
        "category":    "fighters",
        "military_col": "fighters",
    },
    "f22": {
        "name":        "✈ F-22",
        "price":       2_000_000_000,
        "tech_req":    8,
        "category":    "fighters",
        "military_col": "fighters",
    },
    "kaan": {
        "name":        "✈ KAAN",
        "price":       1_200_000_000,
        "tech_req":    6,
        "category":    "fighters",
        "military_col": "fighters",
    },

    # ════════════════════════════════════════════════════════════════════════
    # 🚁  بالگردها
    # ════════════════════════════════════════════════════════════════════════

    "uh60": {
        "name":        "🚁 UH-60 Black Hawk",
        "price":       100_000_000,
        "tech_req":    3,
        "category":    "helicopters",
        "military_col": "helicopters",
    },
    "ah64": {
        "name":        "🚁 AH-64 Apache",
        "price":       400_000_000,
        "tech_req":    5,
        "category":    "helicopters",
        "military_col": "helicopters",
    },
    "mi17": {
        "name":        "🚁 Mi-17",
        "price":       80_000_000,
        "tech_req":    2,
        "category":    "helicopters",
        "military_col": "helicopters",
    },
    "mi28": {
        "name":        "🚁 Mi-28",
        "price":       350_000_000,
        "tech_req":    5,
        "category":    "helicopters",
        "military_col": "helicopters",
    },
    "ka52": {
        "name":        "🚁 Ka-52",
        "price":       450_000_000,
        "tech_req":    5,
        "category":    "helicopters",
        "military_col": "helicopters",
    },
    "ch47": {
        "name":        "🚁 CH-47 Chinook",
        "price":       150_000_000,
        "tech_req":    3,
        "category":    "helicopters",
        "military_col": "helicopters",
    },

    # ════════════════════════════════════════════════════════════════════════
    # 🤖  پهپادها
    # ════════════════════════════════════════════════════════════════════════

    "shahed136": {
        "name":        "🛩 شاهد ۱۳۶",
        "price":       20_000_000,
        "tech_req":    2,
        "category":    "drones",
        "military_col": "drones",
    },
    "shahed149": {
        "name":        "🛩 شاهد ۱۴۹ غزه",
        "price":       50_000_000,
        "tech_req":    3,
        "category":    "drones",
        "military_col": "drones",
    },
    "mq9": {
        "name":        "🛩 MQ-9 Reaper",
        "price":       200_000_000,
        "tech_req":    5,
        "category":    "drones",
        "military_col": "drones",
    },
    "tb2": {
        "name":        "🛩 Bayraktar TB2",
        "price":       80_000_000,
        "tech_req":    3,
        "category":    "drones",
        "military_col": "drones",
    },
    "akinci": {
        "name":        "🛩 Akıncı",
        "price":       150_000_000,
        "tech_req":    4,
        "category":    "drones",
        "military_col": "drones",
    },
    "wing_loong": {
        "name":        "🛩 Wing Loong II",
        "price":       100_000_000,
        "tech_req":    4,
        "category":    "drones",
        "military_col": "drones",
    },
    "ch5": {
        "name":        "🛩 CH-5",
        "price":       120_000_000,
        "tech_req":    4,
        "category":    "drones",
        "military_col": "drones",
    },

    # ════════════════════════════════════════════════════════════════════════
    # 🚢  نیروی دریایی
    # ════════════════════════════════════════════════════════════════════════

    "patrol_boat": {
        "name":        "🚤 قایق گشتی",
        "price":       50_000_000,
        "tech_req":    2,
        "category":    "navy",
        "military_col": "patrol_boats",
    },
    "fast_boat": {
        "name":        "🚤 قایق رزمی سریع",
        "price":       120_000_000,
        "tech_req":    3,
        "category":    "navy",
        "military_col": "patrol_boats",
    },
    "support_ship": {
        "name":        "🚢 کشتی پشتیبانی",
        "price":       500_000_000,
        "tech_req":    4,
        "category":    "navy",
        "military_col": "warships",
    },
    "corvette": {
        "name":        "⚓ ناوچه",
        "price":       800_000_000,
        "tech_req":    5,
        "category":    "navy",
        "military_col": "warships",
    },
    "destroyer": {
        "name":        "⚓ ناوشکن",
        "price":       3_000_000_000,
        "tech_req":    6,
        "category":    "navy",
        "military_col": "warships",
    },
    "cruiser": {
        "name":        "⚓ رزم‌ناو",
        "price":       5_000_000_000,
        "tech_req":    7,
        "category":    "navy",
        "military_col": "warships",
    },
    "diesel_sub": {
        "name":        "🌊 زیردریایی دیزل",
        "price":       2_000_000_000,
        "tech_req":    5,
        "category":    "navy",
        "military_col": "submarines",
    },
    "adv_sub": {
        "name":        "🌊 زیردریایی پیشرفته",
        "price":       6_000_000_000,
        "tech_req":    7,
        "category":    "navy",
        "military_col": "submarines",
    },
    "nuclear_sub": {
        "name":        "⚛ زیردریایی هسته‌ای",
        "price":       15_000_000_000,
        "tech_req":    9,
        "category":    "navy",
        "military_col": "submarines",
    },
    "light_carrier": {
        "name":        "🛳 ناو هواپیمابر سبک",
        "price":       20_000_000_000,
        "tech_req":    8,
        "category":    "navy",
        "military_col": "warships",
    },
    "carrier": {
        "name":        "🛳 ناو هواپیمابر",
        "price":       50_000_000_000,
        "tech_req":    9,
        "category":    "navy",
        "military_col": "warships",
    },

    # ════════════════════════════════════════════════════════════════════════
    # 🚀  موشک‌ها
    # ════════════════════════════════════════════════════════════════════════

    "tactical_missile": {
        "name":        "🚀 موشک تاکتیکی",
        "price":       100_000_000,
        "tech_req":    3,
        "category":    "missiles",
        "military_col": "missiles",
    },
    "cruise_missile": {
        "name":        "🚀 موشک کروز",
        "price":       500_000_000,
        "tech_req":    5,
        "category":    "missiles",
        "military_col": "missiles",
    },
    "tomahawk": {
        "name":        "🚀 Tomahawk",
        "price":       700_000_000,
        "tech_req":    6,
        "category":    "missiles",
        "military_col": "missiles",
    },
    "atacms": {
        "name":        "🚀 ATACMS",
        "price":       900_000_000,
        "tech_req":    6,
        "category":    "missiles",
        "military_col": "missiles",
    },
    "storm_shadow": {
        "name":        "🚀 Storm Shadow",
        "price":       800_000_000,
        "tech_req":    6,
        "category":    "missiles",
        "military_col": "missiles",
    },
    "prsm": {
        "name":        "🚀 PrSM",
        "price":       1_000_000_000,
        "tech_req":    7,
        "category":    "missiles",
        "military_col": "missiles",
    },
    "brahmos": {
        "name":        "🚀 BrahMos",
        "price":       1_500_000_000,
        "tech_req":    8,
        "category":    "missiles",
        "military_col": "missiles",
    },
    "iskander": {
        "name":        "🚀 Iskander-M",
        "price":       1_200_000_000,
        "tech_req":    7,
        "category":    "missiles",
        "military_col": "missiles",
    },
    "kalibr": {
        "name":        "🚀 Kalibr",
        "price":       1_000_000_000,
        "tech_req":    7,
        "category":    "missiles",
        "military_col": "missiles",
    },
    "kinzhal": {
        "name":        "🚀 Kinzhal",
        "price":       2_000_000_000,
        "tech_req":    8,
        "category":    "missiles",
        "military_col": "missiles",
    },
    "df21": {
        "name":        "🚀 DF-21",
        "price":       1_800_000_000,
        "tech_req":    7,
        "category":    "missiles",
        "military_col": "missiles",
    },
    "df26": {
        "name":        "🚀 DF-26",
        "price":       2_500_000_000,
        "tech_req":    8,
        "category":    "missiles",
        "military_col": "missiles",
    },
    "ballistic": {
        "name":        "🚀 موشک بالستیک",
        "price":       1_500_000_000,
        "tech_req":    7,
        "category":    "missiles",
        "military_col": "missiles",
    },

    # ════════════════════════════════════════════════════════════════════════
    # 🛡  پدافند هوایی
    # ════════════════════════════════════════════════════════════════════════

    "nasams": {
        "name":        "🛡 NASAMS",
        "price":       1_800_000_000,
        "tech_req":    6,
        "category":    "air_defense",
        "military_col": "air_defense",
    },
    "patriot": {
        "name":        "🛡 Patriot",
        "price":       2_500_000_000,
        "tech_req":    7,
        "category":    "air_defense",
        "military_col": "air_defense",
    },
    "iron_dome": {
        "name":        "🛡 Iron Dome",
        "price":       2_000_000_000,
        "tech_req":    7,
        "category":    "air_defense",
        "military_col": "air_defense",
    },
    "davids_sling": {
        "name":        "🛡 David's Sling",
        "price":       2_200_000_000,
        "tech_req":    7,
        "category":    "air_defense",
        "military_col": "air_defense",
    },
    "hq9": {
        "name":        "🛡 HQ-9",
        "price":       2_500_000_000,
        "tech_req":    7,
        "category":    "air_defense",
        "military_col": "air_defense",
    },
    "pantsir": {
        "name":        "🛡 Pantsir-S1",
        "price":       1_500_000_000,
        "tech_req":    6,
        "category":    "air_defense",
        "military_col": "air_defense",
    },
    "s300": {
        "name":        "🛡 S-300",
        "price":       2_000_000_000,
        "tech_req":    6,
        "category":    "air_defense",
        "military_col": "air_defense",
    },
    "s400": {
        "name":        "🛡 S-400",
        "price":       3_000_000_000,
        "tech_req":    8,
        "category":    "air_defense",
        "military_col": "air_defense",
    },
    "s500": {
        "name":        "🛡 S-500",
        "price":       5_000_000_000,
        "tech_req":    9,
        "category":    "air_defense",
        "military_col": "air_defense",
    },
    "thaad": {
        "name":        "🛡 THAAD",
        "price":       4_000_000_000,
        "tech_req":    9,
        "category":    "air_defense",
        "military_col": "air_defense",
    },
}

# ── Category metadata (display order preserved) ───────────────────────────────

CATEGORIES: dict[str, str] = {
    "ground":      "🪖 تجهیزات زمینی",
    "fighters":    "✈ جنگنده‌ها",
    "helicopters": "🚁 بالگردها",
    "drones":      "🤖 پهپادها",
    "navy":        "🚢 نیروی دریایی",
    "missiles":    "🚀 موشک‌ها",
    "air_defense": "🛡 پدافند هوایی",
}


# ── Service functions ─────────────────────────────────────────────────────────

def open_market() -> dict:
    """Return the full market catalog."""
    return MARKET_CATALOG


def check_budget(country_id: int, total_cost: float) -> tuple[bool, float]:
    """Return (has_enough, current_budget)."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT budget FROM countries WHERE id = ?", (country_id,)
        ).fetchone()
        budget = float(row["budget"]) if row else 0.0
        return (budget >= total_cost, budget)
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
        return (level >= tech_req, level)
    finally:
        conn.close()


def register_purchase(
    country_id: int,
    item_key: str,
    quantity: int,
    total_cost: float,
) -> None:
    """
    Atomic transaction:
      1. Deduct budget from countries.
      2. Increment the correct military column.
      3. Log to purchase_history.
    """
    info = MARKET_CATALOG[item_key]
    col  = info["military_col"]

    conn = get_connection()
    try:
        with conn:
            conn.execute(
                "UPDATE countries SET budget = budget - ?, "
                "updated_at = strftime('%Y-%m-%d %H:%M:%S','now') "
                "WHERE id = ?",
                (total_cost, country_id),
            )
            conn.execute(
                f"UPDATE military SET {col} = {col} + ?, "
                f"updated_at = strftime('%Y-%m-%d %H:%M:%S','now') "
                f"WHERE country_id = ?",
                (quantity, country_id),
            )
            conn.execute(
                "INSERT INTO purchase_history "
                "(country_id, item_name, quantity, price, purchase_time) "
                "VALUES (?, ?, ?, ?, strftime('%Y-%m-%d %H:%M:%S','now'))",
                (country_id, info["name"], quantity, total_cost),
            )
    finally:
        conn.close()


def buy_item(country_id: int, item_key: str, quantity: int) -> dict:
    """
    Full purchase pipeline.
    Returns a result dict — always check result["success"] first.
    """
    if item_key not in MARKET_CATALOG:
        return {"success": False, "error": "item_unknown"}

    if quantity <= 0:
        return {"success": False, "error": "qty_zero"}

    info       = MARKET_CATALOG[item_key]
    unit_price = info["price"]
    total_cost = unit_price * quantity

    tech_ok, tech_level = check_technology(country_id, info["tech_req"])
    if not tech_ok:
        return {
            "success":   False,
            "error":     "tech",
            "need":      info["tech_req"],
            "have":      tech_level,
        }

    budget_ok, budget = check_budget(country_id, total_cost)
    if not budget_ok:
        return {
            "success":    False,
            "error":      "budget",
            "total_cost": total_cost,
            "budget":     budget,
        }

    register_purchase(country_id, item_key, quantity, total_cost)

    return {
        "success":    True,
        "name":       info["name"],
        "quantity":   quantity,
        "unit_price": unit_price,
        "total_cost": total_cost,
        "remaining":  budget - total_cost,
    }

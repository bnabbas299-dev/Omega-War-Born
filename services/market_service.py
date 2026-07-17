"""
Market Service — Phase 7
MBN Global Market: catalog, validation, purchase execution, and inventory update.
"""

from __future__ import annotations

from database import get_connection

# ── Market catalog ────────────────────────────────────────────────────────────
# price: absolute value in dollars
# tech_req: minimum technology_level
# military_col: column in the military table that receives quantity

MARKET_CATALOG: dict[str, dict] = {

    # ── Ground Forces — Vehicles ──────────────────────────────────────────
    "tactical_vehicle": {
        "name_fa":     "خودرو تاکتیکی",
        "name_en":     "Tactical Vehicle",
        "emoji":       "🚙",
        "price":       20_000_000,
        "tech_req":    1,
        "category":    "ground",
        "military_col": "armored_vehicles",
    },
    "recon_vehicle": {
        "name_fa":     "خودرو شناسایی",
        "name_en":     "Recon Vehicle",
        "emoji":       "🚗",
        "price":       40_000_000,
        "tech_req":    2,
        "category":    "ground",
        "military_col": "armored_vehicles",
    },
    "military_truck": {
        "name_fa":     "کامیون نظامی",
        "name_en":     "Military Truck",
        "emoji":       "🚛",
        "price":       30_000_000,
        "tech_req":    1,
        "category":    "ground",
        "military_col": "armored_vehicles",
    },
    "armored_ambulance": {
        "name_fa":     "آمبولانس زرهی",
        "name_en":     "Armored Ambulance",
        "emoji":       "🚑",
        "price":       60_000_000,
        "tech_req":    2,
        "category":    "ground",
        "military_col": "armored_vehicles",
    },
    "apc": {
        "name_fa":     "نفربر زرهی (APC)",
        "name_en":     "APC",
        "emoji":       "🛡",
        "price":       90_000_000,
        "tech_req":    2,
        "category":    "ground",
        "military_col": "armored_vehicles",
    },
    "ifv": {
        "name_fa":     "خودرو رزمی پیاده (IFV)",
        "name_en":     "IFV",
        "emoji":       "🪖",
        "price":       140_000_000,
        "tech_req":    3,
        "category":    "ground",
        "military_col": "armored_vehicles",
    },
    "mrap": {
        "name_fa":     "خودرو مقاوم در برابر مین (MRAP)",
        "name_en":     "MRAP",
        "emoji":       "🛻",
        "price":       120_000_000,
        "tech_req":    3,
        "category":    "ground",
        "military_col": "armored_vehicles",
    },

    # ── Ground Forces — Tanks ─────────────────────────────────────────────
    "t90m": {
        "name_fa":     "تانک T-90M",
        "name_en":     "T-90M",
        "emoji":       "🪖",
        "price":       160_000_000,
        "tech_req":    4,
        "category":    "ground",
        "military_col": "tanks",
    },
    "leopard_2a7": {
        "name_fa":     "تانک Leopard 2A7",
        "name_en":     "Leopard 2A7",
        "emoji":       "🪖",
        "price":       180_000_000,
        "tech_req":    4,
        "category":    "ground",
        "military_col": "tanks",
    },
    "m1a2_abrams": {
        "name_fa":     "تانک M1A2 Abrams",
        "name_en":     "M1A2 Abrams",
        "emoji":       "🪖",
        "price":       190_000_000,
        "tech_req":    4,
        "category":    "ground",
        "military_col": "tanks",
    },
    "k2_black_panther": {
        "name_fa":     "تانک K2 Black Panther",
        "name_en":     "K2 Black Panther",
        "emoji":       "🪖",
        "price":       220_000_000,
        "tech_req":    5,
        "category":    "ground",
        "military_col": "tanks",
    },
    "merkava_mk4": {
        "name_fa":     "تانک Merkava Mk4",
        "name_en":     "Merkava Mk4",
        "emoji":       "🪖",
        "price":       250_000_000,
        "tech_req":    6,
        "category":    "ground",
        "military_col": "tanks",
    },
    "t14_armata": {
        "name_fa":     "تانک T-14 Armata",
        "name_en":     "T-14 Armata",
        "emoji":       "🪖",
        "price":       300_000_000,
        "tech_req":    7,
        "category":    "ground",
        "military_col": "tanks",
    },
    "kf51_panther": {
        "name_fa":     "تانک KF51 Panther",
        "name_en":     "KF51 Panther",
        "emoji":       "🪖",
        "price":       400_000_000,
        "tech_req":    8,
        "category":    "ground",
        "military_col": "tanks",
    },

    # ── Air Force — Drones ────────────────────────────────────────────────
    "recon_drone": {
        "name_fa":     "پهپاد شناسایی",
        "name_en":     "Recon Drone",
        "emoji":       "🛩",
        "price":       30_000_000,
        "tech_req":    2,
        "category":    "air",
        "military_col": "drones",
    },
    "combat_drone": {
        "name_fa":     "پهپاد رزمی",
        "name_en":     "Combat Drone",
        "emoji":       "🛩",
        "price":       80_000_000,
        "tech_req":    3,
        "category":    "air",
        "military_col": "drones",
    },
    "heavy_drone": {
        "name_fa":     "پهپاد سنگین",
        "name_en":     "Heavy Drone",
        "emoji":       "🛩",
        "price":       250_000_000,
        "tech_req":    5,
        "category":    "air",
        "military_col": "drones",
    },

    # ── Air Force — Helicopters ───────────────────────────────────────────
    "transport_helicopter": {
        "name_fa":     "بالگرد ترابری",
        "name_en":     "Transport Helicopter",
        "emoji":       "🚁",
        "price":       150_000_000,
        "tech_req":    3,
        "category":    "air",
        "military_col": "helicopters",
    },
    "attack_helicopter": {
        "name_fa":     "بالگرد تهاجمی",
        "name_en":     "Attack Helicopter",
        "emoji":       "🚁",
        "price":       400_000_000,
        "tech_req":    5,
        "category":    "air",
        "military_col": "helicopters",
    },
    "heavy_helicopter": {
        "name_fa":     "بالگرد سنگین",
        "name_en":     "Heavy Helicopter",
        "emoji":       "🚁",
        "price":       600_000_000,
        "tech_req":    6,
        "category":    "air",
        "military_col": "helicopters",
    },

    # ── Air Force — Fighters ──────────────────────────────────────────────
    "f16": {
        "name_fa":     "جنگنده F-16",
        "name_en":     "F-16",
        "emoji":       "✈",
        "price":       900_000_000,
        "tech_req":    5,
        "category":    "air",
        "military_col": "fighters",
    },
    "gripen": {
        "name_fa":     "جنگنده Gripen",
        "name_en":     "Gripen",
        "emoji":       "✈",
        "price":       950_000_000,
        "tech_req":    5,
        "category":    "air",
        "military_col": "fighters",
    },
    "rafale": {
        "name_fa":     "جنگنده Rafale",
        "name_en":     "Rafale",
        "emoji":       "✈",
        "price":       1_200_000_000,
        "tech_req":    6,
        "category":    "air",
        "military_col": "fighters",
    },
    "eurofighter": {
        "name_fa":     "جنگنده Eurofighter",
        "name_en":     "Eurofighter",
        "emoji":       "✈",
        "price":       1_300_000_000,
        "tech_req":    6,
        "category":    "air",
        "military_col": "fighters",
    },
    "f35": {
        "name_fa":     "جنگنده F-35",
        "name_en":     "F-35",
        "emoji":       "✈",
        "price":       1_500_000_000,
        "tech_req":    7,
        "category":    "air",
        "military_col": "fighters",
    },
    "f22": {
        "name_fa":     "جنگنده F-22",
        "name_en":     "F-22",
        "emoji":       "✈",
        "price":       2_000_000_000,
        "tech_req":    8,
        "category":    "air",
        "military_col": "fighters",
    },

    # ── Navy ──────────────────────────────────────────────────────────────
    "patrol_boat": {
        "name_fa":     "قایق گشت‌زنی",
        "name_en":     "Patrol Boat",
        "emoji":       "🚤",
        "price":       50_000_000,
        "tech_req":    2,
        "category":    "navy",
        "military_col": "patrol_boats",
    },
    "fast_combat_boat": {
        "name_fa":     "قایق رزمی سریع",
        "name_en":     "Fast Combat Boat",
        "emoji":       "🚤",
        "price":       120_000_000,
        "tech_req":    3,
        "category":    "navy",
        "military_col": "patrol_boats",
    },
    "support_ship": {
        "name_fa":     "کشتی پشتیبانی",
        "name_en":     "Support Ship",
        "emoji":       "🚢",
        "price":       500_000_000,
        "tech_req":    4,
        "category":    "navy",
        "military_col": "warships",
    },
    "frigate": {
        "name_fa":     "فریگات",
        "name_en":     "Frigate",
        "emoji":       "🚢",
        "price":       1_000_000_000,
        "tech_req":    5,
        "category":    "navy",
        "military_col": "warships",
    },
    "destroyer": {
        "name_fa":     "ناوشکن",
        "name_en":     "Destroyer",
        "emoji":       "🚢",
        "price":       3_000_000_000,
        "tech_req":    6,
        "category":    "navy",
        "military_col": "warships",
    },
    "cruiser": {
        "name_fa":     "ناو رزمی",
        "name_en":     "Cruiser",
        "emoji":       "🚢",
        "price":       5_000_000_000,
        "tech_req":    7,
        "category":    "navy",
        "military_col": "warships",
    },
    "diesel_submarine": {
        "name_fa":     "زیردریایی دیزلی",
        "name_en":     "Diesel Submarine",
        "emoji":       "🌊",
        "price":       2_000_000_000,
        "tech_req":    5,
        "category":    "navy",
        "military_col": "submarines",
    },
    "advanced_submarine": {
        "name_fa":     "زیردریایی پیشرفته",
        "name_en":     "Advanced Submarine",
        "emoji":       "🌊",
        "price":       6_000_000_000,
        "tech_req":    7,
        "category":    "navy",
        "military_col": "submarines",
    },
    "aircraft_carrier": {
        "name_fa":     "ناو هواپیمابر",
        "name_en":     "Aircraft Carrier",
        "emoji":       "🚢",
        "price":       50_000_000_000,
        "tech_req":    9,
        "category":    "navy",
        "military_col": "warships",
    },

    # ── Missiles ──────────────────────────────────────────────────────────
    "tactical_missile": {
        "name_fa":     "موشک تاکتیکی",
        "name_en":     "Tactical Missile",
        "emoji":       "🚀",
        "price":       100_000_000,
        "tech_req":    3,
        "category":    "missiles",
        "military_col": "missiles",
    },
    "cruise_missile": {
        "name_fa":     "موشک کروز",
        "name_en":     "Cruise Missile",
        "emoji":       "🚀",
        "price":       500_000_000,
        "tech_req":    5,
        "category":    "missiles",
        "military_col": "missiles",
    },
    "tomahawk": {
        "name_fa":     "موشک Tomahawk",
        "name_en":     "Tomahawk",
        "emoji":       "🚀",
        "price":       700_000_000,
        "tech_req":    6,
        "category":    "missiles",
        "military_col": "missiles",
    },
    "atacms": {
        "name_fa":     "موشک ATACMS",
        "name_en":     "ATACMS",
        "emoji":       "🚀",
        "price":       900_000_000,
        "tech_req":    6,
        "category":    "missiles",
        "military_col": "missiles",
    },
    "ballistic_missile": {
        "name_fa":     "موشک بالستیک",
        "name_en":     "Ballistic Missile",
        "emoji":       "🚀",
        "price":       1_500_000_000,
        "tech_req":    7,
        "category":    "missiles",
        "military_col": "missiles",
    },
    "brahmos": {
        "name_fa":     "موشک BrahMos",
        "name_en":     "BrahMos",
        "emoji":       "🚀",
        "price":       1_500_000_000,
        "tech_req":    8,
        "category":    "missiles",
        "military_col": "missiles",
    },

    # ── Air Defense ───────────────────────────────────────────────────────
    "nasams": {
        "name_fa":     "سامانه NASAMS",
        "name_en":     "NASAMS",
        "emoji":       "🛡",
        "price":       1_800_000_000,
        "tech_req":    6,
        "category":    "air_defense",
        "military_col": "air_defense",
    },
    "iron_dome": {
        "name_fa":     "سامانه Iron Dome",
        "name_en":     "Iron Dome",
        "emoji":       "🛡",
        "price":       2_000_000_000,
        "tech_req":    7,
        "category":    "air_defense",
        "military_col": "air_defense",
    },
    "patriot": {
        "name_fa":     "سامانه Patriot",
        "name_en":     "Patriot",
        "emoji":       "🛡",
        "price":       2_500_000_000,
        "tech_req":    7,
        "category":    "air_defense",
        "military_col": "air_defense",
    },
    "s400": {
        "name_fa":     "سامانه S-400",
        "name_en":     "S-400",
        "emoji":       "🛡",
        "price":       3_000_000_000,
        "tech_req":    8,
        "category":    "air_defense",
        "military_col": "air_defense",
    },
    "thaad": {
        "name_fa":     "سامانه THAAD",
        "name_en":     "THAAD",
        "emoji":       "🛡",
        "price":       4_000_000_000,
        "tech_req":    9,
        "category":    "air_defense",
        "military_col": "air_defense",
    },
}

# ── Category metadata ─────────────────────────────────────────────────────────

CATEGORIES: dict[str, dict] = {
    "ground":      {"label": "🪖 Ground Forces",  "callback": "mkt_cat_ground"},
    "air":         {"label": "✈ Air Force",        "callback": "mkt_cat_air"},
    "navy":        {"label": "🚢 Navy",             "callback": "mkt_cat_navy"},
    "missiles":    {"label": "🚀 Missiles",         "callback": "mkt_cat_missiles"},
    "air_defense": {"label": "🛡 Air Defense",     "callback": "mkt_cat_air_defense"},
    "factories":   {"label": "🏗 Factories",        "callback": "mkt_cat_factories"},
}


# ── Service functions ─────────────────────────────────────────────────────────

def open_market() -> dict:
    """Return the full market catalog."""
    return MARKET_CATALOG


def check_budget(country_id: int, total_cost: float) -> tuple[bool, float]:
    """
    Return (has_enough: bool, current_budget: float).
    """
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
    """
    Return (meets_requirement: bool, current_level: int).
    """
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
    Deduct budget, update military inventory, log to purchase_history.
    All in one atomic transaction.
    """
    info = MARKET_CATALOG[item_key]
    col  = info["military_col"]

    conn = get_connection()
    try:
        with conn:
            conn.execute(
                "UPDATE countries SET budget = budget - ?, "
                "updated_at = strftime('%Y-%m-%d %H:%M:%S','now') WHERE id = ?",
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
                (country_id, info["name_fa"], quantity, total_cost),
            )
    finally:
        conn.close()


def buy_item(country_id: int, item_key: str, quantity: int) -> dict:
    """
    Full purchase pipeline.
    Returns a result dict with success flag, message, and receipt data.
    """
    if item_key not in MARKET_CATALOG:
        return {"success": False, "message": "❌ تجهیزات شناخته‌شده نیست."}

    if quantity <= 0:
        return {"success": False, "message": "❌ تعداد باید بیشتر از صفر باشد."}

    info       = MARKET_CATALOG[item_key]
    unit_price = info["price"]
    total_cost = unit_price * quantity

    # Tech check
    tech_ok, tech_level = check_technology(country_id, info["tech_req"])
    if not tech_ok:
        return {
            "success": False,
            "message": (
                f"❌ سطح فناوری کافی نیست.\n"
                f"نیاز: سطح {info['tech_req']} — فعلی: سطح {tech_level}"
            ),
        }

    # Budget check
    budget_ok, budget = check_budget(country_id, total_cost)
    if not budget_ok:
        return {
            "success": False,
            "message": (
                f"❌ بودجه کافی نیست.\n"
                f"هزینه کل: {total_cost:,.0f}\nبودجه فعلی: {budget:,.0f}"
            ),
        }

    # Execute
    register_purchase(country_id, item_key, quantity, total_cost)

    remaining = budget - total_cost
    return {
        "success":    True,
        "name":       info["name_fa"],
        "quantity":   quantity,
        "unit_price": unit_price,
        "total_cost": total_cost,
        "remaining":  remaining,
    }

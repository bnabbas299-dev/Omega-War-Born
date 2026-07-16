"""
Shared formatting helpers used across the bot.
"""


def fmt(n: int | float) -> str:
    """Format a number with comma separators."""
    return f"{n:,}"


def tech_level(level: int) -> str:
    return f"سطح {level}"


def diplomacy_label(status: str) -> str:
    labels = {
        "Neutral":  "🕊 خنثی",
        "Allied":   "🤝 متحد",
        "War":      "⚔️ در جنگ",
        "Embargo":  "🚫 تحریم",
    }
    return labels.get(status, status)

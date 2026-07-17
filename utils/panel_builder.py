"""
Panel text builders.
Assembles multi-section displays dynamically from DB rows.
Each public function returns a list of strings guaranteed ≤ 4096 chars each.
"""

from __future__ import annotations

import sqlite3
from typing import Optional

SEP = "━━━━━━━━━━━━━━━━━━━━━━"


def _n(value) -> str:
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return str(value) if value is not None else "۰"


def _f(value) -> str:
    try:
        return f"{float(value):,.0f}"
    except (TypeError, ValueError):
        return str(value) if value is not None else "۰"


def _col(row, key: str, default=0):
    """Safe column access — returns default if column doesn't exist yet."""
    try:
        return row[key]
    except (IndexError, KeyError):
        return default


def _tech_flag(value: int) -> str:
    return "✅ فعال" if value else "❌ غیرفعال"


def _alliance_block(alliances: list[str]) -> str:
    if not alliances:
        return "(No alliances yet)"
    return "\n".join(f"• {a}" for a in alliances)


def _split_messages(sections: list[str]) -> list[str]:
    messages: list[str] = []
    current = ""
    for section in sections:
        candidate = (current + "\n\n" + section).strip() if current else section
        if len(candidate) <= 4096:
            current = candidate
        else:
            if current:
                messages.append(current)
            current = section
    if current:
        messages.append(current)
    return messages


# ═══════════════════════════════════════════════════════════════
# COUNTRY PANEL SECTIONS
# ═══════════════════════════════════════════════════════════════

def _section_header(country) -> str:
    return (
        f"📅 روز بازی: {country.current_day}\n"
        f"📌 کشور: {country.country_name}\n\n"
        f"{SEP}\n\n"
        f"📊 شاخص‌های ملی\n\n"
        f"💰 اقتصاد: {country.economy_level}\n"
        f"🪖 قدرت نظامی: {country.military_level}\n"
        f"🔬 فناوری: سطح {country.technology_level}\n"
        f"🏭 صنعت: {country.industry_level}\n"
        f"😊 رضایت مردم: {country.public_satisfaction}%\n"
        f"⭐ محبوبیت دولت: {country.government_popularity}%\n"
        f"🌍 اعتبار جهانی: {country.global_reputation}\n"
        f"⚡ امنیت انرژی: {country.energy_security}\n"
        f"🍞 امنیت غذایی: {country.food_security}"
    )


def _section_finance(country, eco: sqlite3.Row) -> str:
    return (
        f"{SEP}\n\n"
        f"💵 وضعیت مالی\n\n"
        f"💰 بودجه فعلی:\n{_f(country.budget)}\n\n"
        f"📥 درآمد روزانه\n\n"
        f"💰 مالیات:\n{_f(eco['daily_tax_income'])}\n\n"
        f"🏭 صنعت:\n{_f(eco['daily_industry_income'])}\n\n"
        f"🌍 صادرات:\n{_f(eco['daily_export_income'])}\n\n"
        f"📉 هزینه نگهداری:\n{_f(eco['daily_maintenance'])}"
    )


def _section_population(country) -> str:
    return (
        f"{SEP}\n\n"
        f"👥 جمعیت\n\n"
        f"👥 جمعیت کل:\n{_n(country.population)}\n\n"
        f"👷 جمعیت فعال:\n{_n(country.active_population)}\n\n"
        f"🪖 نیروی قابل جذب:\n{_n(country.available_recruits)}"
    )


def _section_buildings(b: sqlite3.Row) -> str:
    return (
        f"{SEP}\n\n"
        f"🏭 ساختمان‌ها\n\n"
        f"🏭 کارخانه غیرنظامی:\n{_n(_col(b,'civil_factory'))}\n\n"
        f"🏭 کارخانه نظامی:\n{_n(_col(b,'military_factory'))}\n\n"
        f"✈ کارخانه هواپیماسازی:\n{_n(_col(b,'aircraft_factory'))}\n\n"
        f"🚢 کارخانه کشتی‌سازی:\n{_n(_col(b,'shipyard'))}\n\n"
        f"🚀 کارخانه موشک‌سازی:\n{_n(_col(b,'missile_factory'))}\n\n"
        f"🛡 کارخانه زرهی:\n{_n(_col(b,'armor_factory'))}\n\n"
        f"🛰 کارخانه الکترونیک:\n{_n(_col(b,'electronics_factory'))}\n\n"
        f"⚡ نیروگاه:\n{_n(_col(b,'power_plant'))}\n\n"
        f"🛢 پالایشگاه:\n{_n(_col(b,'refinery'))}\n\n"
        f"🔬 مرکز تحقیق:\n{_n(_col(b,'research_center'))}\n\n"
        f"📡 مرکز کنترل ماهواره:\n{_n(_col(b,'satellite_center'))}\n\n"
        f"📦 انبار:\n{_n(_col(b,'warehouse'))}\n\n"
        f"🚛 مرکز لجستیک:\n{_n(_col(b,'logistics_center'))}\n\n"
        f"🏥 بیمارستان:\n{_n(_col(b,'hospital'))}\n\n"
        f"🎓 دانشگاه:\n{_n(_col(b,'university'))}\n\n"
        f"🏙 برج اقتصادی:\n{_n(_col(b,'economic_tower'))}\n\n"
        f"🛣 بزرگراه:\n{_n(_col(b,'highway'))}\n\n"
        f"🚆 راه‌آهن:\n{_n(_col(b,'railway'))}\n\n"
        f"🌆 شهر هوشمند:\n{_n(_col(b,'smart_city'))}\n\n"
        f"🌿 پارک ملی:\n{_n(_col(b,'national_park'))}"
    )


def _section_resources(r: sqlite3.Row) -> str:
    return (
        f"{SEP}\n\n"
        f"⛽ منابع\n\n"
        f"🛢 نفت:\n{_n(r['oil'])}\n\n"
        f"⛽ گاز:\n{_n(r['gas'])}\n\n"
        f"⚙ فولاد:\n{_n(r['steel'])}\n\n"
        f"🪨 سنگ آهن:\n{_n(r['iron'])}\n\n"
        f"🔋 اورانیوم:\n{_n(r['uranium'])}\n\n"
        f"🌾 غذا:\n{_n(r['food'])}\n\n"
        f"💧 آب:\n{_n(r['water'])}\n\n"
        f"⚡ برق:\n{_n(r['electricity'])}"
    )


def _section_technology(t: sqlite3.Row) -> str:
    return (
        f"{SEP}\n\n"
        f"🔬 فناوری\n\n"
        f"سطح فناوری:\n{t['technology_level']}\n\n"
        f"Military AI:\n{_tech_flag(t['military_ai'])}\n\n"
        f"Cyber Security:\n{_tech_flag(t['cyber_security'])}\n\n"
        f"Satellite Network:\n{_tech_flag(t['satellite_network'])}\n\n"
        f"Quantum Lab:\n{_tech_flag(t['quantum_lab'])}"
    )


def _section_military(m: sqlite3.Row) -> str:
    return (
        f"{SEP}\n\n"
        f"🪖 تجهیزات نظامی\n\n"
        f"👥 سرباز:\n{_n(m['soldiers'])}\n\n"
        f"🪖 تانک:\n{_n(m['tanks'])}\n\n"
        f"🚙 خودرو زرهی:\n{_n(m['armored_vehicles'])}\n\n"
        f"🎯 توپخانه:\n{_n(m['artillery'])}\n\n"
        f"🚀 راکت‌انداز:\n{_n(m['rocket_launchers'])}\n\n"
        f"🛡 پدافند:\n{_n(m['air_defense'])}\n\n"
        f"📡 رادار:\n{_n(m['radars'])}\n\n"
        f"✈ جنگنده:\n{_n(m['fighters'])}\n\n"
        f"🚁 بالگرد:\n{_n(m['helicopters'])}\n\n"
        f"🛩 پهپاد:\n{_n(m['drones'])}\n\n"
        f"🛩 هواپیمای پشتیبانی:\n{_n(m['support_aircraft'])}\n\n"
        f"🚢 ناو:\n{_n(m['warships'])}\n\n"
        f"🌊 زیردریایی:\n{_n(m['submarines'])}\n\n"
        f"🚤 قایق رزمی:\n{_n(m['patrol_boats'])}\n\n"
        f"🚀 موشک:\n{_n(m['missiles'])}\n\n"
        f"🎖 تجربه ارتش:\n{m['army_experience']}"
    )


def _section_diplomacy(alliances: list[str]) -> str:
    return (
        f"{SEP}\n\n"
        f"🤝 روابط خارجی\n\n"
        f"🟢 متحدان:\n{_alliance_block(alliances)}\n\n"
        f"🔴 دشمنان:\n(None)\n\n"
        f"📜 قراردادها:\n(None)\n\n"
        f"{SEP}"
    )


def build_country_panel(
    country,
    eco: Optional[sqlite3.Row],
    buildings: Optional[sqlite3.Row],
    resources: Optional[sqlite3.Row],
    technology: Optional[sqlite3.Row],
    military: Optional[sqlite3.Row],
    alliances: list[str],
) -> list[str]:
    sections = [
        _section_header(country),
        _section_finance(country, eco) if eco else f"{SEP}\n\n💵 وضعیت مالی\n\nاطلاعات موجود نیست",
        _section_population(country),
        _section_buildings(buildings) if buildings else f"{SEP}\n\n🏭 ساختمان‌ها\n\nاطلاعات موجود نیست",
        _section_resources(resources) if resources else f"{SEP}\n\n⛽ منابع\n\nاطلاعات موجود نیست",
        _section_technology(technology) if technology else f"{SEP}\n\n🔬 فناوری\n\nاطلاعات موجود نیست",
        _section_military(military) if military else f"{SEP}\n\n🪖 تجهیزات نظامی\n\nاطلاعات موجود نیست",
        _section_diplomacy(alliances),
    ]
    return _split_messages(sections)


# ═══════════════════════════════════════════════════════════════
# END-OF-DAY REPORT
# ═══════════════════════════════════════════════════════════════

def build_end_day_report(report: dict) -> str:
    income      = report["income"]
    maintenance = report["maintenance"]
    day         = report["day"]
    b_before    = report["budget_before"]
    b_after     = report["budget_after"]
    net         = income["total"] - maintenance
    surplus_emoji = "📈" if net >= 0 else "📉"
    net_label     = "مازاد روزانه" if net >= 0 else "کسری روزانه"

    return (
        f"🌅 روز {day} به پایان رسید\n\n"
        f"{SEP}\n\n"
        f"📥 درآمد روزانه\n\n"
        f"  💰 مالیات:         {_f(income['tax'])}\n"
        f"  🏭 صنعت:           {_f(income['industry'])}\n"
        f"  🌍 صادرات:         {_f(income['exports'])}\n"
        f"  ─────────────────────\n"
        f"  📊 جمع درآمد:      {_f(income['total'])}\n\n"
        f"{SEP}\n\n"
        f"📉 هزینه‌های روزانه\n\n"
        f"  🔧 نگهداری:        {_f(maintenance)}\n\n"
        f"{SEP}\n\n"
        f"  {surplus_emoji} {net_label}:  {_f(abs(net))}\n\n"
        f"{SEP}\n\n"
        f"💵 بودجه قبل از روز:\n"
        f"  {_f(b_before)}\n\n"
        f"💵 بودجه بعد از روز:\n"
        f"  {_f(b_after)}\n\n"
        f"{SEP}"
    )

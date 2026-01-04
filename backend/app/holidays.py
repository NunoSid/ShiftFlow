from datetime import date, timedelta
from typing import Dict, List

from .constants import PORTUGAL_FIXED_HOLIDAYS


def _easter_sunday(year: int) -> date:
    """Anonymous Gregorian algorithm."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def generate_national_holidays(year: int) -> Dict[date, str]:
    holidays: Dict[date, str] = {}
    for month, day in PORTUGAL_FIXED_HOLIDAYS:
        holidays[date(year, month, day)] = "Feriado Nacional"

    easter = _easter_sunday(year)
    holidays[easter] = "Domingo de Páscoa"
    holidays[easter - timedelta(days=2)] = "Sexta-feira Santa"
    holidays[easter + timedelta(days=60)] = "Corpo de Deus"
    return holidays


def month_holidays(year: int, month: int, manual: List[Dict]) -> List[Dict]:
    nat = generate_national_holidays(year)
    records: Dict[int, Dict] = {}
    for d, label in nat.items():
        if d.year == year and d.month == month:
            records[d.day] = {"day": d.day, "label": label, "type": "NACIONAL"}

    for entry in manual:
        if entry["year"] != year or entry["month"] != month:
            continue
        action = entry.get("action", "ADD").upper()
        if action == "REMOVE":
            records.pop(entry["day"], None)
        else:
            records[entry["day"]] = {
                "day": entry["day"],
                "label": entry["label"],
                "type": "MANUAL",
            }
    return [records[key] for key in sorted(records)]


def is_holiday(year: int, month: int, day: int, manual: List[Dict]) -> bool:
    nat = generate_national_holidays(year)
    test_date = date(year, month, day)
    removed = any(
        entry.get("action", "ADD") == "REMOVE"
        and entry["year"] == year
        and entry["month"] == month
        and entry["day"] == day
        for entry in manual
    )
    if test_date in nat and not removed:
        return True
    return any(
        entry.get("action", "ADD") != "REMOVE"
        and entry["year"] == year
        and entry["month"] == month
        and entry["day"] == day
        for entry in manual
    )

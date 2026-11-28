"""
numbers_only: a time and the meal's own numbers, no food named, so no items and the food API is not asked.

    OhioT1DM   an XML <meal> event {ts "26-05-2025 07:15:00" (day first), type, carbs}
    dubosson   a 5-minute row {time, calories, balance, quality, ...}

The event keeps its time and its own total (s01-D19, D23): a meal with no food named still has its 60 g.
"""
from .common import clock, meal_word, stated_total

PROFILES = [("ts", {"col": "ts", "dayfirst": True}, "type"),     # OhioT1DM
            ("time", {"col": "time"}, None)]                     # dubosson, and any row with a "time"


def fits(rows) -> bool:
    return any(col in rows.columns for col, _, _ in PROFILES)


def make(rows) -> dict:
    col, t, kind_col = next(p for p in PROFILES if p[0] in rows.columns)
    kind = meal_word(rows.iloc[0][kind_col]) if kind_col and kind_col in rows.columns else None
    return {"input": {"start": clock(rows, **t), "end": None, "logged_at": None, "meal_type": kind,
                      "total": stated_total(rows), "items": None, "timeline": None},
            "asks": [], "meal": "",
            "step": "no food named, so no items: the event keeps its time and its own total"}

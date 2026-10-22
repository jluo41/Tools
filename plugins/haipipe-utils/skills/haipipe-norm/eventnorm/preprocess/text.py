"""
text: words. Two shapes today, told apart by their columns.

    Shanghai   one row, "Dietary intake" a cell of foods a line with grams, "饮食" the same lines in Chinese,
               "Date" local time in Shanghai (+08:00)
    typed      one row {"text": "Banana\\nMilk 250 ml", "time"?: "2026-10-21 08:05 -04:00"}: a food a line, an
               amount in g or ml at its end; the time as written, when given

A sentence ("I ate a huge apple two hours ago") is one line, so it is asked whole and misses: the step that finds
the foods, the amounts and the time in a sentence is not built yet (s01-D30).
"""
import re

from .common import clock, lines_to_items, step_text

SHANGHAI = {"name": "Dietary intake", "zh": "饮食", "time": "Date", "zone": "+08:00"}
STAMP = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}( [+-]\d{2}:\d{2})?$")


def fits(rows) -> bool:
    return SHANGHAI["name"] in rows.columns or "text" in rows.columns


def make(rows) -> dict:
    if SHANGHAI["name"] in rows.columns:
        cell = rows.iloc[0][SHANGHAI["name"]]
        zh = rows.iloc[0][SHANGHAI["zh"]] if SHANGHAI["zh"] in rows.columns else None
        items, asks, skipped = lines_to_items(cell, zh)
        start = clock(rows, SHANGHAI["time"], zone=SHANGHAI["zone"])
        head = f"one cell → {len(items)} items, each with its grams" + (f" and its {SHANGHAI['zh']} line" if zh else "")
        meal = "; ".join(rows[SHANGHAI["name"]].astype(str).str.strip())
    else:
        cell = rows.iloc[0]["text"]
        items, asks, skipped = lines_to_items(cell)
        t = str(rows.iloc[0].get("time") or "").strip()
        start = t if STAMP.match(t) else clock(rows, "time") if t else None
        head = f"{len(str(cell or '').strip().splitlines())} line(s) → {len(items)} item{'s' * (len(items) != 1)}"
        meal = str(cell or "").strip()
    return {"input": {"start": start, "end": None, "logged_at": None, "meal_type": None, "total": None,
                      "items": items or None, "timeline": None},
            "asks": asks, "meal": meal, "step": step_text(1, items, skipped, head)}

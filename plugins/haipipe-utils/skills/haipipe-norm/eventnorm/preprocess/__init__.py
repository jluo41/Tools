"""
The preprocess step: raw, as it arrives, to the input JSON, a file a raw type (s01 ⑦ ②). raw["type"] picks the file;
inside it, the columns pick the source's shape. Each returns

    {"input": {start, end, logged_at, meal_type, total, items, timeline},
     "asks":  the text each item is asked with,
     "meal":  the meal as one string (what the total is asked with),
     "step":  what the step did, in one line}
"""
from . import app_log, numbers_only, photo, text
from .common import frame

STEPS = {"app_log": app_log, "text": text, "photo": photo, "numbers_only": numbers_only}


def preprocess(raw: dict) -> dict:
    kind = (raw or {}).get("type")
    if kind not in STEPS:
        raise ValueError(f"raw.type {kind!r} is not one of {sorted(STEPS)}")
    rows = frame(raw)
    step = STEPS[kind]
    if not step.fits(rows):
        raise ValueError(f"raw.type {kind!r}: these columns are no shape this step reads: {list(rows.columns)[:12]}")
    return step.make(rows)

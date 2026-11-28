"""
The still preprocess step: raw, as it arrives, to the input JSON (b51 s17's engine 1). raw["type"] picks the step:

    minutes    minute rows, typed or sent: a "time", or "from" and "to" for every minute between ("to" not included);
               its steps (a stretch's, shared evenly by its minutes), its bpm (worn), or worn: true, and its sleep
               level. A bare 'HH:MM' is on raw["day"].
    mcphases   mcPhases' own rows, each naming its file: steps.csv (a repeated minute keeps its largest copy, as s05),
               heart_rate.csv (a reading in a minute says worn), sleep.csv (its levels, minute by minute)

The span is raw["start"] to raw["end"] when given, else the whole hours the step and heart-rate rows touch. A minute
in the span that no row names: no steps, not worn, out of bed (so unknown).

Lifted from b51 s07's drawing builder (studio/_build/topic_frames.py: mc_day, still_hour_counts), where it ran first.
"""
import re

from ..preprocess.common import frame
from .schema import LEVELS, RAW_TYPES

DAY = re.compile(r"^day\s+(\d+)(?:\s+(\d{1,2}):(\d{2}))?$")
CLOCK = re.compile(r"^(\d{1,2}):(\d{2})(?::\d{2})?$")


def minute_of(text, day=None) -> tuple:
    """'day 3 10:07' -> (3, 607, 'study'); '2026-10-27 10:07' -> (its date's ordinal, 607, 'date'); a bare '10:07'
    is on `day` ('day 3' or '2026-10-27')."""
    import pandas as pd
    s = str(text or "").strip()
    if CLOCK.match(s):
        if not day:
            raise ValueError(f"time {s!r} has no day: give raw.day ('day 3' or '2026-10-27') or a full time")
        s = f"{day} {s}"
    m = DAY.match(s)
    if m and m.group(2) is not None:
        return int(m.group(1)), int(m.group(2)) * 60 + int(m.group(3)), "study"
    t = pd.to_datetime(s, errors="coerce")
    if pd.isna(t):
        raise ValueError(f"time {s!r} is not a time: 'day 3 10:07', '2026-10-27 10:07' or 'HH:MM' on raw.day")
    return t.toordinal(), t.hour * 60 + t.minute, "date"


def label(idx: int, style: str, hour: bool = False) -> str:
    """A minute's index back to its words: 'day 3 10:07' or '2026-10-27 10:07'; with hour, its hour's start."""
    import datetime as dt
    d, m = divmod(idx, 1440)
    m = m - m % 60 if hour else m
    head = f"day {d}" if style == "study" else dt.date.fromordinal(d).isoformat()
    return f"{head} {m // 60:02d}:{m % 60:02d}"


def number(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return None if x != x else x


def truth(v) -> bool:
    return str(v).strip().lower() in ("true", "1", "yes", "on")


def grid(lo: int, hi: int) -> dict:
    return {i: {"steps": None, "worn": False, "level": None} for i in range(lo, hi)}


def span(raw: dict, idxs, style: str, day=None) -> tuple:
    """raw's own start and end, else the whole hours its minutes touch."""
    if raw.get("start") and raw.get("end"):
        (d0, m0, _), (d1, m1, _) = minute_of(raw["start"], day), minute_of(raw["end"], day)
        lo, hi = d0 * 1440 + m0, d1 * 1440 + m1
        if hi <= lo:
            raise ValueError("raw.end is not after raw.start")
        return lo, hi
    if not idxs:
        raise ValueError("raw holds no minute with a time")
    return min(idxs) - min(idxs) % 60, max(idxs) - max(idxs) % 60 + 60


def minutes(rows, raw: dict) -> dict:
    """Minute rows to the timeline: a row's time, or every minute from its 'from' to before its 'to'."""
    day, pts, style = raw.get("day"), {}, None
    for r in rows.to_dict("records"):
        r = {k: v for k, v in r.items() if v is not None and v == v}
        if r.get("from"):
            (d0, m0, style), (d1, m1, _) = minute_of(r["from"], day), minute_of(r.get("to") or r["from"], day)
            idxs = range(d0 * 1440 + m0, max(d1 * 1440 + m1, d0 * 1440 + m0 + 1))
        elif r.get("time"):
            d, m, style = minute_of(r["time"], day)
            idxs = [d * 1440 + m]
        else:
            raise ValueError('raw.type "minutes": each row needs a "time", or "from" and "to"')
        lvl = str(r["sleep"]).strip().lower() if r.get("sleep") else None
        if lvl and lvl not in LEVELS:
            raise ValueError(f"sleep level {r['sleep']!r}: one of {sorted(LEVELS)}")
        worn = number(r.get("bpm")) is not None or truth(r.get("worn", ""))
        n = number(r.get("steps"))
        each, extra = divmod(int(n), len(idxs)) if n is not None else (None, 0)
        for k, i in enumerate(idxs):
            p = pts.setdefault(i, {"steps": None, "worn": False, "level": None})
            if each is not None:                                # a stretch's steps, shared evenly, the rest early
                p["steps"] = max(p["steps"] or 0, each + (k < extra))
            p["worn"] = p["worn"] or worn
            p["level"] = lvl or p["level"]
    lo, hi = span(raw, list(pts), style, day)
    tl = grid(lo, hi)
    tl.update({i: p for i, p in pts.items() if lo <= i < hi})
    return {"timeline": tl, "style": style, "step": f"{len(rows):,} minute rows: {hi - lo:,} minutes, "
                                                    f"{sum(p['worn'] for p in tl.values()):,} worn"}


def mcphases(rows, raw: dict) -> dict:
    """mcPhases' three files to the timeline, as s07's builder reads them (mc_day)."""
    import ast
    import pandas as pd
    if "file" not in rows.columns:
        raise ValueError('raw.type "mcphases": each row names its "file": steps.csv, heart_rate.csv or sleep.csv')
    at = lambda r: int(r["day_in_study"]) * 1440 + int(r["timestamp"][:2]) * 60 + int(r["timestamp"][3:5])
    st = rows[rows["file"] == "steps.csv"]
    hr = rows[rows["file"] == "heart_rate.csv"]
    sl = rows[rows["file"] == "sleep.csv"]
    steps = {}
    for r in st.to_dict("records"):                          # a minute sent twice keeps its largest count
        v = number(r.get("steps"))
        steps[at(r)] = max(steps.get(at(r), 0), int(v or 0))
    worn = {at(r) for r in hr.to_dict("records")}
    levels = {}
    for r in sl.to_dict("records"):
        lv = r.get("levels")
        data = (ast.literal_eval(lv) if isinstance(lv, str) else lv or {}).get("data") or []
        if not data:
            continue
        first = pd.Timestamp(data[0]["dateTime"]).normalize()
        for seg in data:
            t = pd.Timestamp(seg["dateTime"])
            d = int(r["sleep_start_day_in_study"]) + (t.normalize() - first).days
            for k in range(int(seg["seconds"]) // 60):
                levels[d * 1440 + t.hour * 60 + t.minute + k] = seg["level"]
    lo, hi = span({**raw, "day": None}, list(steps) + list(worn) or list(levels), "study")
    tl = grid(lo, hi)
    for i, v in steps.items():
        if lo <= i < hi:
            tl[i]["steps"] = v
    for i in worn:
        if lo <= i < hi:
            tl[i]["worn"] = True
    for i, v in levels.items():
        if lo <= i < hi:
            tl[i]["level"] = v
    step = (f"mcPhases rows: {len(st):,} step, {len(hr):,} heart-rate, {len(sl):,} sleep; "
            f"{hi - lo:,} minutes, {len(steps):,} with a step row, {sum(p['worn'] for p in tl.values()):,} worn")
    return {"timeline": tl, "style": "study", "step": step}


def preprocess(raw: dict) -> dict:
    """raw {"type", "rows", "day"?, "start"?, "end"?} to {"timeline": {minute index: point}, "style", "step"}."""
    typ = (raw or {}).get("type")
    if typ not in RAW_TYPES:
        raise ValueError(f"raw.type must be one of {sorted(RAW_TYPES)}, not {typ!r}")
    rows = frame(raw)
    return minutes(rows, raw) if typ == "minutes" else mcphases(rows, raw)

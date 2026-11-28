"""
The stress preprocess step: raw, as it arrives, to the input JSON (b51 s18's engine 1). raw["type"] picks the step:

    readings    a Garmin's readings, one a minute (AI-READI: 1,087,115 of 1,087,980 gaps are one minute): each lands
                in its own minute; a minute read twice keeps its last reading. A time ending in Z or +00:00 is UTC and
                raw["offset"] (minutes, local minus UTC) moves it to local; AI-READI names only a zone word ("pst"),
                so with no offset the times stay UTC and the step says so.
    day_score   mcPhases' rows of one day: the copies of a day are one; a day with no READY row has no score

The span of readings is raw["start"] to raw["end"] when given, else the whole hours the readings touch. A minute of
the span no reading names is unknown (no_reading).
"""
from ..preprocess.common import frame
from ..still.preprocess import label, minute_of, number
from .schema import DAY_PARTS, DAY_READY, DIRECTION, RAW_TYPES


def reading(r: dict) -> tuple:
    """(time text, value) of one row: {time, value}, or AI-READI's nested row."""
    if isinstance(r.get("stress"), dict):
        return (r.get("effective_time_frame") or {}).get("date_time"), r["stress"].get("value")
    return r.get("time") or r.get("date_time") or r.get("at"), r.get("value", r.get("stress"))


def readings(raw: dict) -> dict:
    import pandas as pd
    rows = raw.get("rows")
    if not isinstance(rows, list) or not rows or not all(isinstance(r, dict) for r in rows):
        raise ValueError('raw.rows must be a list of readings, each {"time", "value"}')
    off = raw.get("offset")
    off = None if off is None else int(number(off) or 0)
    tl, style, twice, utc = {}, None, 0, False
    for r in rows:
        t, v = reading(r)
        v = number(v)
        if t is None or v is None:
            raise ValueError(f"a reading needs a time and a value: {r}")
        if not -2 <= v <= 100:
            raise ValueError(f"value {v:g}: a Garmin stress level is 0 to 100, -1 (not measured) or -2 (active)")
        s = str(t).strip()
        z = s.endswith("Z") or s.endswith("+00:00")
        if z:
            ts = pd.to_datetime(s, utc=True, errors="coerce")
            if pd.isna(ts):
                raise ValueError(f"time {s!r} is not a time")
            utc = utc or off is None
            s = (ts.tz_localize(None) + pd.Timedelta(minutes=off or 0)).strftime("%Y-%m-%d %H:%M")
        d, m, style = minute_of(s, raw.get("day"))
        i = d * 1440 + m
        twice += i in tl
        tl[i] = int(v)
    lo, hi = min(tl), max(tl) + 1
    if raw.get("start"):
        d, m, _ = minute_of(raw["start"], raw.get("day"))
        lo = d * 1440 + m
    else:
        lo -= lo % 60
    if raw.get("end"):
        d, m, _ = minute_of(raw["end"], raw.get("day"))
        hi = d * 1440 + m
    else:
        hi += -hi % 60
    if hi <= lo:
        raise ValueError("raw.end must be after raw.start")
    n = len(tl)
    tl = {i: tl.get(i) for i in range(lo, hi)}                # None: a minute no reading names
    inside = sum(v is not None for v in tl.values())
    step = (f"{n:,} readings, each in its own minute" + (f", {inside:,} of them in the span" if inside != n else "") + (f", {twice:,} minutes read twice kept at their last" if twice else "") +
            (f"; times moved from UTC by {off} minutes" if off is not None else
             "; times are UTC, no offset given" if utc else "") +
            f"; {hi - lo - sum(v is not None for v in tl.values()):,} minutes of the span have no reading")
    return {"timeline": tl, "style": style, "step": step, "zone": "local" if off is not None or not utc else "UTC"}


def day_score(raw: dict) -> dict:
    """One person's one day of mcPhases' stress_score.csv: its copies are one row; the score, and its three parts."""
    rows = frame(raw)
    days = {str(d) for d in rows.get("day_in_study", []) if str(d) not in ("None", "nan")}
    if len(days) != 1:
        raise ValueError(f"raw.type 'day_score': the rows of one day, {len(days)} days sent")
    day = int(float(days.pop()))
    ready = rows[rows["status"].isin(DAY_READY)] if "status" in rows else rows.iloc[0:0]
    same = ready.drop_duplicates(subset=[c for c in ready.columns if c not in ("timestamp",)])
    copies = len(rows)
    if same.empty:
        st = sorted(set(rows["status"])) if "status" in rows else []
        return {"day": day, "input": {"start": f"day {day}", "end": f"day {day + 1}", "device": raw.get("device"),
                                      "total": None, "items": None, "timeline": None},
                "step": f"{copies} row{'s' * (copies != 1)} of day {day}, none with a score (status {', '.join(st) or 'missing'})"}
    r = same.sort_values("timestamp").iloc[-1].to_dict() if "timestamp" in same else same.iloc[-1].to_dict()
    total = {"score": int(float(r["stress_score"])), "direction": DIRECTION["day_score"]}
    for k, (got, of) in DAY_PARTS.items():
        g, o = number(r.get(got)), number(r.get(of))
        if o:                                                    # 0 of 0: a row without the premium parts
            total[k] = f"{int(g)} of {int(o)}"
    step = (f"{copies} row{'s' * (copies != 1)} of day {day}" + (f", {copies - 1} of them copies" if len(same) == 1 and copies > 1 else "") +
            (f", {len(same)} different scores: the latest kept" if len(same) > 1 else "") +
            "; a day's score, its hours unknown")
    return {"day": day, "input": {"start": f"day {day}", "end": f"day {day + 1}", "device": raw.get("device") or "Fitbit",
                                  "total": total, "items": None, "timeline": None}, "step": step}


def preprocess(raw: dict) -> dict:
    """raw {"type", "rows", ...} to the minute timeline (readings) or the day's input (day_score); a ValueError names
    what is wrong."""
    typ = (raw or {}).get("type")
    if typ not in RAW_TYPES:
        raise ValueError(f"raw.type must be one of {sorted(RAW_TYPES)}, not {typ!r}")
    return readings(raw) if typ == "readings" else day_score(raw)

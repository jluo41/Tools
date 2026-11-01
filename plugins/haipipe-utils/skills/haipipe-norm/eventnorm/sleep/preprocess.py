"""
The sleep preprocess step: raw, as it arrives, to the input JSON (b51 s16's engine 1). raw["type"] picks the step:

    log    WellDoc SleepEntry rows of one person and device. The longest row is the night, the time in bed. Shorter
           rows that overlap it (in rows, or in raw["pieces"], as s06's files hold them) are its pieces: clipped to
           the night, exact repeats dropped, joined, they are the minutes asleep and the timeline. No pieces: in bed,
           asleep not told, unknown (FitBit, Google, typed into the app).

Returns {"input", "kind", "step", "when": (start, end, zone), "asleep": [(from, to), ...] or None}.
"""
from ..preprocess.common import frame
from ..step.preprocess import device_name, number
from .hours import joined, kind as kind_of, stamp
from .schema import RAW_TYPES, WELLDOC_FMT


def times(r) -> tuple:
    """A WellDoc row's local start and end (UTC plus its offset), its zone and its minutes, to the second."""
    import pandas as pd
    off = int(number(r.get("TimezoneOffset")) or 0)
    when = lambda c: pd.to_datetime(r.get(c), format=WELLDOC_FMT, errors="coerce")
    s, e = when("StartDateTime"), when("EndDateTime")
    if pd.isna(s) or pd.isna(e):
        raise ValueError("raw.type 'log': StartDateTime and EndDateTime must be WellDoc times, '1/23/2023 4:16:52 AM'")
    s, e = s + pd.Timedelta(minutes=off), e + pd.Timedelta(minutes=off)
    zone = f"{'+' if off >= 0 else '-'}{abs(off) // 60:02d}:{abs(off) % 60:02d}"
    return s, e, zone, (e - s).total_seconds() / 60


def hm(t) -> str:
    return f"{t:%H:%M}"


def log(rows, raw: dict) -> dict:
    """The night and its pieces to the input: start, end, device, its own total, items null, the stretches asleep."""
    import pandas as pd
    rs = [r for _, r in rows.iterrows()]
    spans = [times(r) for r in rs]
    i = max(range(len(rs)), key=lambda k: spans[k][3])            # the longest row is the night
    r, (s, e, zone, minutes) = rs[i], spans[i]
    off = r.get("TimezoneOffset")
    extra = [{**p, "TimezoneOffset": p.get("TimezoneOffset", off)} for p in raw.get("pieces") or []]
    cand = [spans[k][:2] for k in range(len(rs)) if k != i and spans[k][3] < minutes] + \
           [times(pd.Series(p))[:2] for p in extra]
    cand = sorted(set(cand))                                       # an exact repeat (same start and end) once
    pieces = [(a, b) for a, b in cand if a < e and b > s]
    asleep = joined([(max(a, s), min(b, e)) for a, b in pieces]) if pieces else None
    total = {"in_bed_min": round(minutes, 1)}
    if asleep:
        total["asleep_min"] = round(sum((b - a).total_seconds() for a, b in asleep) / 60, 1)
        total["awake_in_bed_min"] = round(total["in_bed_min"] - total["asleep_min"], 1)
    else:
        total["unknown_min"] = round(minutes, 1)
    k = kind_of(minutes)
    inp = {"start": stamp(s, zone), "end": stamp(e, zone), "device": device_name(r.get("EntrySourceID")),
           "total": total, "items": None,
           "timeline": [{"from": hm(a), "to": hm(b), "state": "asleep"} for a, b in asleep] if asleep else None}
    step = (f"a {k} of {minutes:.1f} minutes in bed" +
            (f"; {len(pieces)} piece{'s' * (len(pieces) != 1)} inside, joined into {len(asleep)} "
             f"stretch{'es' * (len(asleep) != 1)} asleep; the gaps are awake in bed" if asleep
             else "; no pieces inside: asleep or awake not told, so its minutes are unknown"))
    return {"input": inp, "kind": k, "step": step, "when": (s, e, zone), "asleep": asleep}


def preprocess(raw: dict) -> dict:
    """raw {"type", "rows", "pieces"?} to {"input", "kind", "step", "when", "asleep"}; a ValueError names what is
    wrong."""
    typ = (raw or {}).get("type")
    if typ not in RAW_TYPES:
        raise ValueError(f"raw.type must be one of {sorted(RAW_TYPES)}, not {typ!r}")
    return log(frame(raw), raw)

"""
One sleep event, raw to output (b51 s16): the preprocess step makes the input, and the night is cut at each local
hour, in minutes. Nothing is looked up: items stay null and there is no /normalize (s06-D05, as s15-D03).

    event(raw={"type": "log", "rows": [{...whole row...}], "pieces": [...]})     a night and its pieces
    event(input={"start", "end", "timeline"?: [{"from", "to", "state"}]})        a night made elsewhere
    events(raw={"type": "log", "rows": [...]})                                    one event (a night is one)

A night's input and output are what s06 ② draws (studio/_build/topic_frames.py sleep_night_dict, where this ran
first). Which day a night belongs to (the day it ends, s06 ④) and counting a night two devices log once are j06's
first Task: not here yet.
"""
from ..schema import RAW_DROP
from .hours import kind as kind_of, night_hours, stamp
from .preprocess import preprocess
from .schema import INPUT_KEYS


def shown(raw: dict) -> dict:
    """raw as it came, whose-row columns dropped."""
    return {**{k: v for k, v in raw.items() if k != "rows"},
            "rows": [{k: v for k, v in r.items() if k not in RAW_DROP} for r in raw["rows"]]}


def when(text: str):
    """"2023-01-22 23:16 -05:00" -> (its local time, its zone); the zone "" when none is written."""
    import pandas as pd
    if not text or not isinstance(text, str):
        raise ValueError('input.start and input.end must be times, "2023-01-22 23:16 -05:00"')
    head, _, tail = text.strip().rpartition(" ")
    zone = tail if tail[:1] in "+-" and ":" in tail else ""
    t = pd.to_datetime(head if zone else text, errors="coerce")
    if pd.isna(t):
        raise ValueError(f"input time {text!r} is not a time")
    return t, zone


def stretches(timeline, s, e) -> list:
    """An input's timeline {"from": "HH:MM", "to": "HH:MM", "state"} placed on the night: each clock time the first
    one at or after the one before it (from the night's start), clipped to the night; the asleep ones only (a stage
    other than wake counts as asleep)."""
    import pandas as pd
    out, t = [], s
    for p in timeline or []:
        if not isinstance(p, dict) or "from" not in p or "to" not in p:
            raise ValueError('input.timeline must be [{"from": "23:43", "to": "00:46", "state": "asleep"}, ...]')
        ts = []
        for c in (p["from"], p["to"]):
            hh, mm = (int(x) for x in str(c).split(":")[:2])
            x = t.normalize() + pd.Timedelta(hours=hh, minutes=mm)
            if x < t:
                x += pd.Timedelta(days=1)
            ts.append(x)
            t = x
        if str(p.get("state", "asleep")) != "wake":
            a, b = max(ts[0], s), min(ts[1], e)
            if a < b:
                out.append((a, b))
    return out


def event(raw: dict = None, input: dict = None) -> dict:
    """{"raw", "input", "output", "step"}: raw as it came, the input, the output by local hour, and what the preprocess
    step did. A field given in input wins. A ValueError names what is wrong."""
    from .hours import joined
    if not raw and not input:
        raise ValueError('send {"raw": {"type", "rows"}} or {"input": {"start", "end"}}, or both')
    given = {k: v for k, v in (input or {}).items() if k in INPUT_KEYS}
    if given.get("items") is not None:
        raise ValueError("input.items must be null: sleep has nothing to look up")
    out = {"raw": shown(raw) if raw else None}
    if raw:
        pre = preprocess(raw)
        inp, (s, e, zone), asleep = dict(pre["input"]), pre["when"], pre["asleep"]
        step = pre["step"]
    else:
        inp, asleep, step = {k: None for k in INPUT_KEYS}, None, None
    if {"start", "end"} & set(given) or not raw:
        (s, zone), (e, _) = when(given.get("start") or inp.get("start")), when(given.get("end") or inp.get("end"))
        if e <= s:
            raise ValueError("input.end must be after input.start")
    if "timeline" in given or not raw:
        asleep = joined(stretches(given.get("timeline"), s, e)) or None
    inp.update({k: v for k, v in given.items() if k in ("device",)})
    minutes = (e - s).total_seconds() / 60
    total = {"in_bed_min": round(minutes, 1)}
    if asleep:
        total["asleep_min"] = round(sum((b - a).total_seconds() for a, b in asleep) / 60, 1)
        total["awake_in_bed_min"] = round(total["in_bed_min"] - total["asleep_min"], 1)
    else:
        total["unknown_min"] = round(minutes, 1)
    inp.update({"start": stamp(s, zone), "end": stamp(e, zone), "total": total, "items": None,
                "timeline": [{"from": f"{a:%H:%M}", "to": f"{b:%H:%M}", "state": "asleep"} for a, b in asleep]
                if asleep else None})
    if not raw:
        k = kind_of(minutes)
        step = (f"no raw: the input as sent, a {k} of {minutes:.1f} minutes in bed; " +
                (f"{len(asleep)} stretch{'es' * (len(asleep) != 1)} asleep" if asleep else "no timeline: asleep unknown"))
    elif given:
        step += "; given in input: " + ", ".join(given)
    return {**out, "input": {k: inp.get(k) for k in INPUT_KEYS}, "output": night_hours(s, e, asleep, zone),
            "step": step}


def events(raw: dict) -> list:
    """Every event a raw holds: a night and its pieces are one event."""
    if not raw:
        raise ValueError('send {"type", "rows"}')
    return [event(raw=raw)]

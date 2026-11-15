"""
One stress event, raw to output (b51 s18): the preprocess step makes the minute timeline, each minute gets one level,
and each hour's minutes are added up.

    event(raw={"type": "readings", "rows": [{"time": "2023-11-27 20:28", "value": 74}, ...]})
    event(raw={"type": "day_score", "rows": [{...mcPhases stress_score.csv rows of one day...}]})
    event(input={"timeline": [{"from": "2023-11-27 20:00", "to": "2023-11-27 20:30", "level": "high", "mean": 81}]})

The timeline is stretches: minutes in a row at one level are one {"from", "to", "level", "minutes", "mean"}, "to" not
included. An input sent alone answers with the same minutes; its hour means come from the stretches' means, so an hour
a stretch crosses may differ in its last digit from the raw's.
"""
from ..schema import RAW_DROP
from ..still.preprocess import label, minute_of
from .hours import by_hour, level_of
from .preprocess import preprocess
from .schema import ACTIVE, BANDS, DIRECTION, INPUT_KEYS, LEVELS, NOT_MEASURED, SCORED


def shown(raw: dict) -> dict:
    """raw as it came, whose-row columns dropped."""
    return {**{k: v for k, v in raw.items() if k != "rows"},
            "rows": [{k: v for k, v in r.items() if k not in RAW_DROP} for r in raw["rows"]]}


def stretches(tl: dict, style: str) -> list:
    """The minutes as stretches at one level, each with its minutes and the mean of its scores (null when not scored);
    a minute no reading names is its own unknown stretch, why: no_reading."""
    out = []
    for i in sorted(tl):
        lvl, why = level_of(tl[i])
        if out and out[-1]["_end"] == i and out[-1]["level"] == lvl and out[-1]["_why"] == why:
            out[-1]["_end"] = i + 1
            out[-1]["_vs"].append(tl[i])
            continue
        out.append({"_start": i, "_end": i + 1, "level": lvl, "_why": why, "_vs": [tl[i]]})
    rows = []
    for s in out:
        vs = s["_vs"]
        row = {"from": label(s["_start"], style), "to": label(s["_end"], style), "level": s["level"],
               "minutes": s["_end"] - s["_start"],
               "mean": round(sum(vs) / len(vs), 1) if s["level"] in SCORED else None}
        if s["_why"]:
            row["why"] = s["_why"]
        rows.append(row)
    return rows


def totals(tl: dict) -> dict:
    lv = [level_of(v) for v in tl.values()]
    scored = [v for v, (l, _) in zip(tl.values(), lv) if l in SCORED]
    return {"minutes": len(tl), "readings": sum(v is not None for v in tl.values()),
            **{f"{s}_min": sum(l == s for l, _ in lv) for s in LEVELS},
            "mean": round(sum(scored) / len(scored), 1) if scored else None, "direction": DIRECTION["readings"]}


def from_input(inp: dict) -> tuple:
    """An input's timeline back to minutes: stretches {from, to, level, mean}; a scored stretch needs its mean."""
    pts = inp.get("timeline")
    if not isinstance(pts, list) or not pts:
        raise ValueError("input.timeline must be its minutes, stretches {from, to, level, mean}: "
                         "an hour's totals alone cannot say which minutes were which")
    mid = {name: (lo + hi) // 2 for name, lo, hi in BANDS}
    tl, style = {}, None
    for p in pts:
        d0, m0, style = minute_of(p.get("from") or p.get("at"))
        lo = d0 * 1440 + m0
        hi = lo + 1
        if p.get("from"):
            d1, m1, _ = minute_of(p.get("to"))
            hi = d1 * 1440 + m1
        lvl = p.get("level")
        if lvl not in LEVELS:
            raise ValueError(f"level {lvl!r}: one of {list(LEVELS)}")
        if lvl in SCORED:
            v = p.get("mean")
            v = mid[lvl] if v is None else float(v)
            if level_of(round(v))[0] != lvl:
                raise ValueError(f"mean {v:g} is not in the {lvl} band")
        else:
            v = ACTIVE if lvl == "active" else None if p.get("why") == "no_reading" else NOT_MEASURED
        for i in range(lo, max(hi, lo + 1)):
            tl[i] = v
    return tl, style


def event(raw: dict = None, input: dict = None) -> dict:
    """{"raw", "input", "output", "step"}: raw as it came, the input (its minutes as stretches, or its day), the
    output by local hour (or by its day), and what the preprocess step did. An input's timeline wins over raw's. A
    ValueError names what is wrong."""
    if not raw and not input:
        raise ValueError('send {"raw": {"type", "rows"}} or {"input": {"timeline"}}, or both')
    given = {k: v for k, v in (input or {}).items() if k in INPUT_KEYS}
    if given.get("items") is not None:
        raise ValueError("input.items must be null: a score has no words to describe")
    zone = None
    if given.get("timeline"):
        tl, style = from_input(given)
        step = "the input's timeline as sent" + ("; raw shown, not read" if raw else "")
    elif raw and raw.get("type") == "day_score":
        pre = preprocess(raw)
        tot = pre["input"]["total"]
        out = {pre["input"]["start"]: {"grain": "day", **tot}} if tot else None
        return {"raw": shown(raw), "input": pre["input"], "output": out, "step": pre["step"]}
    else:
        pre = preprocess(raw) if raw else None
        if pre is None:
            raise ValueError("input.timeline must be its minutes, stretches {from, to, level, mean}")
        tl, style, step, zone = pre["timeline"], pre["style"], pre["step"], pre["zone"]
    lo, hi = min(tl), max(tl) + 1
    inp = {"start": label(lo, style), "end": label(hi, style), "device": given.get("device") or (raw or {}).get("device"),
           "total": totals(tl), "items": None, "timeline": stretches(tl, style)}
    if zone:
        inp["zone"] = zone
    return {"raw": shown(raw) if raw else None, "input": inp, "output": by_hour(tl, style), "step": step}

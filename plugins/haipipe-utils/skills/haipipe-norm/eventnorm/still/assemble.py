"""
One still event, raw to output (b51 s17): the preprocess step makes the minute timeline, and each hour's minutes are
split four ways by the rule.

    event(raw={"type": "minutes", "day": "2026-10-27", "rows": [{"from": "10:00", "to": "10:40", "bpm": 72, "steps": 0}]})
    event(raw={"type": "mcphases", "rows": [{"file": "steps.csv", ...}, {"file": "heart_rate.csv", ...}, ...]})
    event(input={"timeline": [{"from": "day 3 10:00", "to": "day 3 11:00", "steps": 0, "worn": true, "level": null}]})

An input needs its timeline: an hour's totals alone cannot say which minutes held the steps. The timeline is stretches,
as sleep's: minutes in a row with the same steps, worn and level are one {"from", "to", ...}, "to" not included; a
point {"at", ...} is one minute.
"""
from ..schema import RAW_DROP
from .hours import by_hour
from .preprocess import label, minute_of, preprocess
from .schema import ASLEEP_LEVELS, AWAKE_LEVELS, INPUT_KEYS, LEVELS, RESTLESS_LEVELS, RULE_NOTE, STILL_MAX_STEPS


def shown(raw: dict) -> dict:
    """raw as it came, whose-row columns dropped."""
    return {**{k: v for k, v in raw.items() if k != "rows"},
            "rows": [{k: v for k, v in r.items() if k not in RAW_DROP} for r in raw["rows"]]}


def totals(tl: dict) -> dict:
    ps = list(tl.values())
    lv = lambda s: sum(p["level"] in s for p in ps)
    return {"minutes": len(ps), "asleep_min": lv(ASLEEP_LEVELS), "restless_min": lv(RESTLESS_LEVELS),
            "awake_in_bed_min": lv(AWAKE_LEVELS), "hr_min": sum(bool(p["worn"]) for p in ps),
            "steps": sum(p["steps"] or 0 for p in ps), "step_rows": sum(p["steps"] is not None for p in ps)}


def stretches(tl: dict, style: str) -> list:
    """The minutes as stretches: minutes in a row with the same steps, worn and level are one, "to" not included."""
    out = []
    for i in sorted(tl):
        p = tl[i]
        if out and out[-1]["_end"] == i and all(out[-1][k] == p[k] for k in ("steps", "worn", "level")):
            out[-1]["_end"] = i + 1
            continue
        out.append({"_start": i, "_end": i + 1, **p})
    return [{"from": label(s.pop("_start"), style), "to": label(s.pop("_end"), style), **s} for s in out]


def from_input(inp: dict) -> tuple:
    """An input's timeline back to minutes: stretches {from, to, steps, worn, level}, or points {at, ...}."""
    pts = inp.get("timeline")
    if not isinstance(pts, list) or not pts:
        raise ValueError("input.timeline must be its minutes, stretches {from, to, steps, worn, level}: "
                         "an hour's totals alone cannot say which minutes held the steps")
    tl, style = {}, None
    for p in pts:
        d0, m0, style = minute_of(p.get("from") or p.get("at"))
        lo = d0 * 1440 + m0
        hi = lo + 1
        if p.get("from"):
            d1, m1, _ = minute_of(p.get("to"))
            hi = d1 * 1440 + m1
        lvl = p.get("level")
        if lvl is not None and lvl not in LEVELS:
            raise ValueError(f"level {lvl!r}: one of {sorted(LEVELS)}, or null out of bed")
        for i in range(lo, max(hi, lo + 1)):
            tl[i] = {"steps": None if p.get("steps") is None else int(p["steps"]), "worn": bool(p.get("worn")),
                     "level": lvl}
    return tl, style


def event(raw: dict = None, input: dict = None, still_max_steps: int = None) -> dict:
    """{"raw", "input", "output", "step", "rule"}: raw as it came, the input (its minutes), the output by local hour,
    what the preprocess step did, and the rule used. An input's timeline wins over raw's. A ValueError names what is
    wrong."""
    if not raw and not input:
        raise ValueError('send {"raw": {"type", "rows"}} or {"input": {"start", "end", "timeline"}}, or both')
    given = {k: v for k, v in (input or {}).items() if k in INPUT_KEYS}
    if given.get("items") is not None:
        raise ValueError("input.items must be null: a minute has no words to describe")
    rule = STILL_MAX_STEPS if still_max_steps is None else int(still_max_steps)
    if rule < 0:
        raise ValueError("still_max_steps must be 0 or more")
    if given.get("timeline"):
        tl, style = from_input(given)
        step = "the input's timeline as sent" + ("; raw shown, not read" if raw else "")
    else:
        pre = preprocess(raw) if raw else from_input(given)
        tl, style, step = pre["timeline"], pre["style"], pre["step"]
    lo, hi = min(tl), max(tl) + 1
    inp = {"start": label(lo, style), "end": label(hi, style), "device": given.get("device"),
           "total": totals(tl), "items": None,
           "timeline": stretches(tl, style)}
    return {"raw": shown(raw) if raw else None, "input": inp, "output": by_hour(tl, style, rule), "step": step,
            "rule": {"still_max_steps": rule, "note": RULE_NOTE if still_max_steps is None else "as sent"}}

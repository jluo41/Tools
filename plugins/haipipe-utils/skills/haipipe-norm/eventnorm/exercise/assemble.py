"""
One exercise event, raw to output (b51 s12): the preprocess step makes the input, describe-exercise describes its one
item (the Compendium's MET for its words, asked with its minutes and nothing else: the agreed call), and the event is
set out by local hour, each hour its own part (s02-D23).

    event(raw={"type": "device_code", "rows": [{...}]})                 the preprocess step makes the input
    event(input={"start": ..., "end": ..., "items": [{"activity": "Walking"}]})   an input made elsewhere
    event(raw=..., input={...})                                         both: a field given in input wins

One event holds one activity (s02-D06). A MET the source gives is used as it comes (s02-D11); only an activity's words
are looked up. A row that is no event (a day total, an Other with no minutes) or a stream no rule finds a workout in
answers with input and output null, and the step says why.
"""
from ..schema import RAW_DROP
from .hours import exercise_hours, intensity, stream_hours, whole
from .preprocess import preprocess
from .schema import INPUT_KEYS


def plain(v):
    """A value as JSON holds it: numpy numbers made Python's, NaN made null."""
    if hasattr(v, "item"):
        v = v.item()
    return None if isinstance(v, float) and v != v else v


def describe(activity: str, minutes) -> dict:
    """describe-exercise, asked the words and the minutes (no vendor, no weight: s02-D04): its whole answer."""
    from exnorm import normalize
    kw = {"minutes": [minutes]} if minutes is not None else {}
    return {k: plain(v) for k, v in normalize([activity], **kw)[0].items()}


def item_of(it: dict, minutes) -> dict:
    """An input item described: a MET the source gives as it comes (DEVICE), else the Compendium's for its words."""
    if it.get("met") is not None:
        met = float(it["met"])
        return {"id": it["id"], "activity": it.get("activity"), "code": None, "heading": None, "met": met,
                "intensity": intensity(met), "conf": "DEVICE", "source": "device"}
    a = describe(it["activity"], minutes)
    met = a.get("METValue")
    return {"id": it["id"], "activity": it["activity"], "code": a.get("ActivityCode"), "heading": a.get("MajorHeading"),
            "met": met, "intensity": intensity(met), "conf": a.get("ExerciseConf"),
            "source": (a.get("ExerciseSource") or "").split(":")[0] or None}


def items_of(items):
    """Items made elsewhere, checked: a list of one {"activity", "met"?}; it gets an id when it has none."""
    if items is None:
        return None
    if not isinstance(items, list) or not all(isinstance(it, dict) and (str(it.get("activity") or "").strip()
                                                                        or it.get("met") is not None) for it in items):
        raise ValueError('input.items must be a list of {"activity": "...", "met"?: number}')
    if len(items) > 1:
        raise ValueError("one exercise event holds one activity (s02-D06): send one item")
    return [{"id": it.get("id") or f"i{k + 1}", "activity": it.get("activity"), "met": it.get("met")}
            for k, it in enumerate(items)]


def span(start, end):
    """Minutes between a start and an end, both "YYYY-MM-DD HH:MM[ ±zone]"; None when either is missing."""
    import pandas as pd
    if not start or not end:
        return None
    m = (pd.Timestamp(end[:16]) - pd.Timestamp(start[:16])).total_seconds() / 60
    return whole(m) if m > 0 else None


def event(raw: dict = None, input: dict = None) -> dict:
    """{"raw", "input", "output", "step"}: raw as it came (whose-row columns dropped), the input, the output by local
    hour, and what the preprocess step did. A ValueError names what is wrong with what was sent."""
    if not raw and not input:
        raise ValueError('send {"raw": {"type", "rows"}} or {"input": {"start", "items", ...}}, or both')
    pre = preprocess(raw) if raw else {"input": {}, "kind": None, "step": "no raw: the input as sent"}
    shown = {**{k: v for k, v in raw.items() if k != "rows"},
             "rows": [{k: v for k, v in r.items() if k not in RAW_DROP} for r in raw["rows"]]} if raw else None
    given = {k: v for k, v in (input or {}).items() if k in INPUT_KEYS}
    if pre["input"] is None and not given:                      # no event: a day total, a stream with no workout
        return {"raw": shown, "input": None, "output": None, "step": pre["step"]}
    inp = {k: (pre["input"] or {}).get(k) for k in INPUT_KEYS}
    if "items" in given:
        given["items"] = items_of(given["items"])
    inp.update(given)
    step = pre["step"] + ("; given in input: " + ", ".join(given) if given and raw else "")
    st = pre.get("stream")
    if st and not given:                                        # a stream's workout: each hour from its own samples
        if st["rows_met"]:
            item = {"id": "i1", "activity": st["named"], "code": None, "heading": None, "met": st["met"],
                    "intensity": intensity(st["met"]), "conf": st["conf"], "source": st["source"]}
            met = st["met"]
        elif st["named"]:
            item = item_of({"id": "i1", "activity": st["named"]}, st["minutes"])
            met = item["met"]
        else:
            item = {"id": "i1", "activity": None, "code": None, "heading": None, "met": None, "intensity": None,
                    "conf": "MISS", "source": None}
            met = None
        out = stream_hours(st["bout"], st["line"], item, met, st["rows_met"], st["have"], st["zone"])
        return {"raw": shown, "input": inp, "output": out, "step": step}
    total = inp.get("total") or {}
    minutes = pre.get("minutes", total.get("minutes"))
    if minutes is None:
        minutes = span(inp.get("start"), inp.get("end"))
    if minutes is not None and inp.get("start") and not inp.get("end"):
        from .preprocess import plus
        inp["end"] = plus(inp["start"], minutes)
    items = [item_of(it, minutes) for it in inp["items"]] if inp.get("items") else None
    met = items[0]["met"] if items else None
    out = exercise_hours(inp.get("start"), inp.get("end"), minutes, met, total, items)
    return {"raw": shown, "input": inp, "output": out, "step": step}

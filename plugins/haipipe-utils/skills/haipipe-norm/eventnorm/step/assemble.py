"""
One step event, raw to output (b51 s15): the preprocess step makes the input, and the event is set out by local hour.
Nothing describes a count further: items stay null and there is no /normalize (s15-D03, as s12-D08).

    event(raw={"type": "log", "rows": [{...one StepEntry row...}]})          a logged row, shared by hour
    event(raw={"type": "steps_stream", "rows": [...], "zone": "-05:00"})     a stream, each hour its own samples
    event(input={"start": "2022-06-29 16:56 -05:00", "end": "...", "total": {"steps": 128}})   an input made elsewhere
    events(raw={"type": "log", "rows": [...many...]})                         each row its own event

A logged row's input and output are what s05 ② draws (studio/_build/topic_frames.py span_event_dict, where this ran
first). Counting a day once (a day's total beside its hours, two devices, a row sent again) is j05's first Task: not
here yet (s15 Open 1).
"""
from ..schema import RAW_DROP
from .hours import kind as kind_of, log_hours, stamp, stream_hours
from .preprocess import preprocess
from .schema import INPUT_KEYS


def shown(raw: dict) -> dict:
    """raw as it came, whose-row columns dropped."""
    return {**{k: v for k, v in raw.items() if k != "rows"},
            "rows": [{k: v for k, v in r.items() if k not in RAW_DROP} for r in raw["rows"]]}


def when(text: str):
    """"2022-06-29 16:56 -05:00" -> (its local time, its zone); the zone "" when none is written."""
    import pandas as pd
    if not text or not isinstance(text, str):
        raise ValueError('input.start and input.end must be times, "2022-06-29 16:56 -05:00"')
    head, _, tail = text.strip().rpartition(" ")
    zone = tail if tail[:1] in "+-" and ":" in tail else ""
    t = pd.to_datetime(head if zone else text, errors="coerce")
    if pd.isna(t):
        raise ValueError(f"input time {text!r} is not a time")
    return t, zone


def total_of(given: dict, minutes: float) -> dict:
    """An input's total checked: its minutes from start and end, its numbers kept when above 0."""
    out = {"minutes": round(minutes, 1)}
    for k, v in (given or {}).items():
        if k != "minutes" and isinstance(v, (int, float)) and v > 0:
            out[k] = v
    return out


def event(raw: dict = None, input: dict = None) -> dict:
    """{"raw", "input", "output", "step"} (and "walks" for a stream): raw as it came, the input, the output by local
    hour, and what the preprocess step did. A field given in input wins. A ValueError names what is wrong."""
    if not raw and not input:
        raise ValueError('send {"raw": {"type", "rows"}} or {"input": {"start", "end", "total"}}, or both')
    given = {k: v for k, v in (input or {}).items() if k in INPUT_KEYS}
    if given.get("items") is not None:
        raise ValueError("input.items must be null: a count has no words to describe")
    pre = preprocess(raw) if raw else {"input": {}, "kind": None, "step": "no raw: the input as sent"}
    out = {"raw": shown(raw) if raw else None}
    if pre["input"] is None:
        return {**out, "input": None, "output": None, "step": pre["step"]}
    if pre["kind"] == "stream":
        inp = {**pre["input"], **{k: v for k, v in given.items() if k in ("device",)}}
        hours = stream_hours(pre["samples"], when(inp["start"])[1])
        return {**out, "input": inp, "output": hours, "step": pre["step"], "walks": pre["walks"]}
    inp = {k: pre["input"].get(k) for k in INPUT_KEYS}
    inp.update(given)
    if "when" in pre and not ({"start", "end"} & set(given)):
        s, e, zone = pre["when"]                               # the raw's own times, to the second
    else:
        (s, zone), (e, _) = when(inp.get("start")), when(inp.get("end"))
        if e < s:
            raise ValueError("input.end is before input.start")
        inp["start"], inp["end"] = stamp(s, zone), stamp(e, zone)
    inp["total"] = total_of(inp.get("total"), (e - s).total_seconds() / 60)
    step = pre["step"] + ("; given in input: " + ", ".join(given) if given and raw else "")
    if not raw:
        k = kind_of(inp["total"]["minutes"])
        step = f"no raw: the input as sent, {'an' if k == 'hour' else 'a'} {k}"
    return {**out, "input": inp, "output": log_hours(s, e, zone, inp["total"]), "step": step}


def events(raw: dict) -> list:
    """Every event a raw holds: a log's every row its own event, in the order sent; a stream is one event."""
    if not raw:
        raise ValueError('send {"type", "rows"}')
    if raw.get("type") != "log":
        return [event(raw=raw)]
    return [event(raw={**raw, "rows": [r]}) for r in raw.get("rows") or []]

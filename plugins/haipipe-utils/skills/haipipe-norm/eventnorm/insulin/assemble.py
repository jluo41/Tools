"""
One insulin event, raw to output (b51 s14): medication's preprocess step makes the input, each drug is asked of the
insulin chain (describe-medication names it, describe-insulin finds its insulin and curve, as j04 t02 asks it), and the
event is set out by local hour as j04 t03 froze ext_insulin_event:

    a dose        spread over the hours it acts: a point every 30 minutes from its onset to its end, up to its peak and
                  down to its end, flat when it has no peak; each hour's share is its points' action
    a rate        a pump's basal, units an hour: shared by minutes from its start to its end; with no end it stays in
                  its start's hour, units unknown (the freeze holds a basal to the next basal of its file, which one
                  event cannot see)
    no curve      an insulin the chain names but gives no curve (an intravenous dose) stays in its start's hour

A drug the chain does not call insulin is left out; an event with no insulin has no output.

    event(raw={"type": "app_id", "rows": [{...}]})
    event(input={"start": "2024-05-09 06:28 -04:00", "items": [{"drug": "Lyumjev", "dose": 2, "delivery": "mdi"}]})
    event(raw=..., input={...}, dia_hours=4)                    a field given in input wins; the person's DIA ends a curve
"""
from collections import Counter
from functools import lru_cache

from ..medication.assemble import items_of
from ..medication.preprocess import preprocess, total_of
from ..medication.schema import INPUT_KEYS
from ..schema import RAW_DROP

STEP = 30                                                         # minutes between a curve's points


def plain(v):
    if hasattr(v, "item"):
        v = v.item()
    return None if v is None or (isinstance(v, float) and v != v) or str(v) in ("nan", "None", "<NA>") else v


def num(v):
    v = plain(v)
    try:
        return None if v is None else float(v)
    except (TypeError, ValueError):
        return None


@lru_cache(maxsize=20000)
def chain(drug: str, ndc: str = None, delivery: str = None, dia_hours: float = None) -> dict:
    """The insulin chain for one drug, as j04 t02 asks it: describe-medication (its DrugKey, whether it is insulin),
    then describe-insulin (its insulin, class and curve)."""
    from insnorm import normalize as insnorm
    from mednorm import normalize as mednorm
    m = mednorm([drug], doses=[1], ndcs=[ndc or None])[0]
    i = insnorm([m["DrugKey"]], dia_hours=dia_hours, delivery=[delivery or None], raw=[drug], transport="local")[0]
    return {"IsInsulin": plain(m.get("IsInsulin")), **{k: plain(i.get(k)) for k in (
        "InsulinResolved", "InsulinClass", "OnsetMin", "PeakMin", "DurationMin", "PKConf", "PKSource")}}


def clock(start: str):
    """'2021-01-05 10:44 -05:00' -> (Timestamp, '-05:00'); the zone is '' when the raw gives none."""
    import pandas as pd
    date, hm, *zone = start.split(" ")
    return pd.Timestamp(f"{date} {hm}"), (zone[0] if zone else "")


def stamp(t, zone):
    return f"{t:%Y-%m-%d %H:%M}" + (f" {zone}" if zone else "")


def hour_key(t, zone):
    return f"{t:%Y-%m-%d %H}:00" + (f" {zone}" if zone else "")


def curve_points(t0, item: dict) -> list:
    """A dose's action every STEP minutes, as s04's builder draws it (studio/_build/topic_frames.py dose_event_dict)."""
    import pandas as pd
    onset, peak, dur = item["onset_min"] or 0, item["peak_min"], item["duration_min"]
    pts = []
    for m in range(0, int(dur) + 1, STEP):
        if m < onset:
            continue
        if peak is None or peak <= onset:
            w = 1.0
        else:
            w = (m - onset) / (peak - onset) if m <= peak else (dur - m) / max(dur - peak, 1)
        if w > 0:
            pts.append({"at": t0 + pd.Timedelta(minutes=m), "item": item["id"], "action": round(w, 3)})
    whole = sum(p["action"] for p in pts) or 1.0
    for p in pts:
        p["units"] = round(item["units"] * p["action"] / whole, 4) if item["units"] is not None else None
    return pts


def minutes_by_hour(t0, t1, zone) -> dict:
    """{local hour: minutes inside it} from t0 to t1."""
    import pandas as pd
    out, t = {}, t0
    while t < t1:
        nxt = min(t.floor("h") + pd.Timedelta(hours=1), t1)
        k = hour_key(t, zone)
        out[k] = out.get(k, 0.0) + (nxt - t).total_seconds() / 60
        t = nxt
    return out


def spread(inp: dict, dia_hours=None):
    """The input's insulin by local hour -> (output or None, what was done, in a few words)."""
    import pandas as pd
    start = inp.get("start")
    if not start or not inp.get("items"):
        return None, "no start or no drug: no event"
    t_start, zone = clock(start)
    kept = []
    for it in inp["items"]:
        a = chain(str(it.get("drug")), it.get("ndc") or None, it.get("delivery") or None, dia_hours)
        if not (a["InsulinResolved"] or a["IsInsulin"] is True):
            continue
        kept.append({"id": it["id"], "drug": it.get("drug"), "insulin": a["InsulinResolved"],
                     "class": a["InsulinClass"], "onset_min": num(a["OnsetMin"]), "peak_min": num(a["PeakMin"]),
                     "duration_min": num(a["DurationMin"]), "units": None, "rate": None, "unit": it.get("unit"),
                     "delivery": it.get("delivery"), "conf": a["PKConf"],
                     "source": (a["PKSource"] or "").split(":")[0] or None, "_dose": num(it.get("dose"))})
    if not kept:
        return None, "no insulin in it: the chain names none of its drugs"
    dropped = len(inp["items"]) - len(kept)
    rate = "rate" in (inp.get("total") or {})                     # a rate as the input states it (j03's is_rate)
    end, line, how, note = None, None, None, None
    if rate:
        it = kept[0]
        it["rate"], it["unit"] = it.pop("_dose"), "iu/h"
        for k in ("onset_min", "peak_min", "duration_min"):
            it[k] = None                                           # delivered by minutes, not by a curve
        t_end = clock(inp["end"])[0] if inp.get("end") else None
        it["held_until"] = stamp(t_end, zone) if t_end is not None and t_end > t_start else None
        if it["held_until"] is None:
            how, note = "none", "a rate with no end: it stays in its start's hour, units unknown"
            hours = {hour_key(t_start, zone): {"share": 1.0, "units": None}}
        else:
            mins = minutes_by_hour(t_start, t_end, zone)
            whole = sum(mins.values()) or 1.0
            rate_v = it["rate"] or 0.0
            it["units"] = round(rate_v * whole / 60, 4)
            end, how = it["held_until"], "minutes"
            hours = {h: {"share": round(m / whole, 4), "units": round(rate_v * m / 60, 4)} for h, m in mins.items()}
    else:
        for it in kept:
            it["units"] = it.pop("_dose")
        with_curve = [it for it in kept if it["duration_min"]]
        if not with_curve:
            how, note = "none", "insulin, but describe-insulin gives no curve for it (" + \
                ", ".join(sorted({it["source"] or "?" for it in kept})) + ")"
            hours = {hour_key(t_start, zone): {"share": 1.0}}
        else:
            pts = [p for it in with_curve for p in curve_points(t_start, it)]
            weight = "units" if len(with_curve) > 1 and all(it["units"] is not None for it in with_curve) else "action"
            w = Counter()
            for p in pts:
                w[hour_key(p["at"], zone)] += p[weight] or 0.0
            whole = sum(w.values()) or 1.0
            hours = {h: {"share": round(v / whole, 4)} for h, v in sorted(w.items())}
            end = stamp(t_start + pd.Timedelta(minutes=max(it["duration_min"] for it in with_curve)), zone)
            how, line = "action", pts
    total_units = None if any(it["units"] is None for it in kept) else round(sum(it["units"] for it in kept), 4)
    if how == "action" and total_units is not None:
        for h in hours.values():
            h["units"] = round(total_units * h["share"], 4)
    total = {"units": total_units, **({"rate": kept[0]["rate"], "unit": "iu/h"} if rate else {}),
             **({"duration_min": max(it["duration_min"] for it in kept if it["duration_min"])}
                if how == "action" else {})}
    ev = {"start": start, "end": end, "logged_at": inp.get("logged_at"), "total": total,
          "items": [{k: v for k, v in it.items() if not k.startswith("_")} for it in kept], "source": inp.get("source")}
    out = {}
    for h, v in hours.items():
        pts = None
        if line:
            pts = [{"at": f"{p['at']:%Y-%m-%d %H:%M}", "item": p["item"], "action": p["action"],
                    **({"units": p["units"]} if p["units"] is not None else {})}
                   for p in line if hour_key(p["at"], zone) == h]
        out[h] = {**v, **ev, "timeline": pts}
    if note:
        out[next(iter(out))]["note"] = note
    names = ", ".join(dict.fromkeys(f"{it['insulin'] or it['drug']}" for it in kept))
    did = {"action": f"{names}: spread by its curve over {len(out)} hour{'s' * (len(out) != 1)}",
           "minutes": f"{names}: a rate, shared by its minutes over {len(out)} hour{'s' * (len(out) != 1)}",
           "none": f"{names}: {note}"}[how]
    if dropped:
        did += f"; {dropped} drug{'s' * (dropped != 1)} not insulin left out"
    return out, did


def event(raw: dict = None, input: dict = None, dia_hours: float = None) -> dict:
    """{"raw", "input", "output", "step"}: raw as it came (whose-row columns dropped), the input (medication's), the
    output by local hour, and what was done. A ValueError names what is wrong with what was sent."""
    if not raw and not input:
        raise ValueError('send {"raw": {"type", "rows"}} or {"input": {"start", "items", ...}}, or both')
    pre = preprocess(raw) if raw else {"input": {}, "kind": None, "step": "no raw: the input as sent"}
    shown = {**{k: v for k, v in raw.items() if k != "rows"},
             "rows": [{k: v for k, v in r.items() if k not in RAW_DROP} for r in raw["rows"]]} if raw else None
    given = {k: v for k, v in (input or {}).items() if k in INPUT_KEYS}
    inp = {k: (pre["input"] or {}).get(k) for k in INPUT_KEYS}
    if "items" in given:
        given["items"] = items_of(given["items"])
        given.setdefault("total", total_of(given["items"]))
    inp.update(given)
    if inp.get("source") is None:
        inp["source"] = {"kind": "logged"}
    if inp.get("logged_at") is None and not raw:
        inp["logged_at"] = inp.get("start")
    out, did = spread(inp, dia_hours)
    step = pre["step"] + ("; given in input: " + ", ".join(given) if given and raw else "") + "; " + did
    return {"raw": shown, "input": inp, "output": out, "step": step}

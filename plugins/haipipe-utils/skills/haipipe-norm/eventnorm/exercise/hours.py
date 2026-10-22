"""
An exercise event by local hour, each hour its own part (b51 s02-D23; JL 261021: "像你这个东西既然可以分开，我觉得就没必要
再 share 了 … 你就用你的 timeline：你是你的，他们俩去算"). A workout can be cut by the clock, so each hour it touches holds its
own start and end, minutes, MET, MET-minutes, steps, kcal and heart rate; the hours add up to the event. Food keeps its
share (eventnorm/hours.py): a meal cannot be cut by the clock.

    exercise_hours(start, end, minutes, met, stated, items)   a logged event: by its minutes, at its one MET
    stream_hours(samples, item, zone)                         a stream: each hour from its own samples
"""


def whole(m: float):
    """Minutes as a number: whole when they are, else to one place."""
    return int(round(m)) if abs(m - round(m)) < 1e-9 else round(m, 1)


def intensity(met):
    """The Compendium's band for a MET: sedentary up to 1.5, light under 3, moderate under 6, vigorous from 6."""
    return None if met is None else "sedentary" if met <= 1.5 else "light" if met < 3 else \
        "moderate" if met < 6 else "vigorous"


def exercise_total(minutes, met, met_minutes, stated: dict) -> dict:
    """An output's total (s02-D17): minutes, MET and MET-minutes (left out with no MET), and the kcal the raw states,
    carried from the input's total and marked so ("calories_source": "input"); our own kcal needs the person's weight."""
    if met_minutes is None and met is not None and minutes is not None:
        met_minutes = round(met * minutes, 1)
    out = {"minutes": minutes, **({"met": met, "met_minutes": met_minutes} if met is not None else {})}
    if (stated or {}).get("calories") is not None:
        out.update({"calories": stated["calories"], "calories_source": "input"})
    return out


def exercise_hours(start: str, end, minutes, met, stated: dict, items) -> dict:
    """A logged event by local hour, each hour its own part: its minutes in that hour, the MET, MET × those minutes,
    and the stated kcal by those minutes (a row gives no finer time, so a steady rate). With no end or no minutes,
    all of it in the start's hour; with no start, one entry, "no time"."""
    import pandas as pd
    if not start:
        return {"no time": {"start": None, "end": end, "total": exercise_total(minutes, met, None, stated),
                            "items": items, "timeline": None}}
    zone = start[16:]
    t0 = pd.Timestamp(start[:16])
    key = lambda h: f"{h:%Y-%m-%d %H}:00{zone}"
    if not end or not minutes:
        return {key(t0.floor("h")): {"start": start, "end": end, "total": exercise_total(minutes, met, None, stated),
                                     "items": items, "timeline": None}}
    t1, out, h = pd.Timestamp(end[:16]), {}, t0.floor("h")
    while h < t1:
        a, b = max(t0, h), min(t1, h + pd.Timedelta(hours=1))
        m = (b - a).total_seconds() / 60
        if m > 0:
            part = {"calories": whole(stated["calories"] * m / minutes)} if (stated or {}).get("calories") is not None \
                else {}
            out[key(h)] = {"start": f"{a:%Y-%m-%d %H:%M}{zone}", "end": f"{b:%Y-%m-%d %H:%M}{zone}",
                           "total": exercise_total(whole(m), met, None, part), "items": items, "timeline": None}
        h += pd.Timedelta(hours=1)
    return out


def stream_hours(bout, line: list, item: dict, met, rows_met: bool, have: list, zone: str = "") -> dict:
    """A stream's workout by local hour, each hour from its own samples (`bout`: t, dur and the numbers; `line`: its
    timeline points, one a sample): amounts summed, MET and heart rate averaged, the item's MET that hour's own when
    the device gives one."""
    import pandas as pd
    fmt = lambda t: t.strftime("%Y-%m-%d %H:%M") + zone
    hours = {}
    for h, g in bout.groupby(bout["t"].dt.floor("h"), sort=True):
        m = float(g["dur"].sum())
        if rows_met:
            mm = round(float((g["met"] * g["dur"]).sum()), 1)
            mt = round(mm / m, 2)
        else:
            mt, mm = met, None if met is None else round(met * m, 1)
        part = {"minutes": whole(m), **({"met_minutes": mm} if rows_met else {}),
                **{n: (int(round(float(g[n].sum()))) if n == "steps" else round(float(g[n].sum()), 1))
                   for n in ("steps", "calories") if n in have}}
        beat = {} if "hr" not in have else {"hr_mean": int(round(float(g["hr"].mean()))),
                                            "hr_max": int(round(float(g["hr"].max())))}
        hours[f"{h:%Y-%m-%d %H}:00{zone}"] = {
            "start": fmt(g["t"].iloc[0]), "end": fmt(g["t"].iloc[-1] + pd.Timedelta(minutes=float(g["dur"].iloc[-1]))),
            "total": {**exercise_total(whole(m), mt, mm, part), **({"steps": part["steps"]} if "steps" in part else {}),
                      **beat},
            "items": [{**item, "met": mt, "intensity": intensity(mt)} if item.get("met") is not None else item],
            "timeline": [line[i] for i in g.index]}
    return hours

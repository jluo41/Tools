"""
Any event by local clock hour: which hours it touches and its share of each (s01-D23; JL 261021: "我们是以 hour 为区间来
描述这个 event"). Lifted from b51 s01's drawing builder (studio/_build/topic_frames.py hour_shares, by_hour); food and
exercise both call `by_hour(event, weight)`, so every event reads the same way.

    hour_shares("2021-04-14 10:30 -04:00", "2021-04-14 12:30 -04:00")
        -> {"2021-04-14 10:00 -04:00": 0.25, "... 11:00 ...": 0.5, "... 12:00 ...": 0.25}

The three cases, in the order a log can give them:
    start only (every cohort today)   the whole event in the start's hour, share 1
    start and end                     shared by minutes
    a timeline (bites, minutes)       shared by its points: each point's `weight`, else one a point
"""


def hour_shares(start, end=None) -> dict:
    """Each local clock hour an event touches -> its share of the event: by minutes when the end is known; the whole
    event in the start's hour when it is not. A key keeps the start's offset: '2021-04-14 07:00 -04:00'."""
    import pandas as pd
    if not start:
        return {}
    date, hm, *zone = start.split(" ")
    key = lambda t: f"{t:%Y-%m-%d %H}:00" + (f" {zone[0]}" if zone else "")
    t0 = pd.Timestamp(f"{date} {hm}")
    t1 = pd.Timestamp(" ".join(end.split(" ")[:2])) if end else None
    if t1 is None or t1 <= t0:
        return {key(t0): 1.0}
    out, t, whole = {}, t0, (t1 - t0).total_seconds()
    while t < t1:
        nxt = min(t.floor("h") + pd.Timedelta(hours=1), t1)
        out[key(t)] = round((nxt - t).total_seconds() / whole, 4)
        t = nxt
    return out


def by_hour(event: dict, weight: str = None):
    """Any event's output keyed by local hour: {"<local hour>": {"share", **event, "timeline": its points in that
    hour}} for each clock hour the event touches. The share is by the timeline when there is one (each point's
    `weight`, such as an exercise minute's met, else one a point), by minutes when the end is known, else the whole
    event in the start's hour. A point's `at` without a date ("07:17:20") is on the start's day. None when the event
    has no start."""
    import pandas as pd
    start, line = event.get("start"), event.get("timeline")
    if not start:
        return None
    date, _, *zone = start.split(" ")
    key = lambda t: f"{t:%Y-%m-%d %H}:00" + (f" {zone[0]}" if zone else "")
    if not line:
        return {h: {"share": sh, **event} for h, sh in hour_shares(start, event.get("end")).items()}
    hours = {}
    for pt in line:
        at = " ".join(str(pt["at"]).split(" ")[:2])
        hours.setdefault(key(pd.Timestamp(at if " " in at else f"{date} {at}")), []).append(pt)
    num = lambda v: float(str(v).split()[0]) if v not in (None, "") else 0.0     # 0.6, or a bite's "0.6 g"
    w = {h: sum(num(pt.get(weight)) if weight else 1.0 for pt in pts) for h, pts in hours.items()}
    whole = sum(w.values()) or 1.0
    return {h: {"share": round(w[h] / whole, 4), **event, "timeline": hours[h]} for h in hours}

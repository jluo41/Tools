"""
A step event by local hour (b51 s05-D02). A logged row says only its total over its span, so each hour it touches
gets its share of the span to the second and the row's whole total, as food's hours do, plus `in_hour`: that hour's
own minutes and its share of the steps. A whole day keeps its day. A stream's hours are summed from its own samples.

    kind(minutes)                      minute, hour, part_day, day: how long a row is (schema.KINDS)
    span_hours(s, e, zone)             each hour a span touches -> (its share, its minutes), to the second
    log_hours(s, e, zone, total)       a logged row's output
    stream_hours(s, zone)              a stream's output: each hour its minutes, steps and moving minutes
"""


def kind(minutes: float) -> str:
    """A logged row's kind by how long it is, to the second (j05)."""
    return "minute" if minutes <= 2 else "hour" if minutes <= 61 else "part_day" if minutes < 1379 else "day"


def stamp(t, zone: str) -> str:
    """A local time as the event JSON writes it: "2022-06-29 16:56 -05:00", bare when there is no zone."""
    return f"{t:%Y-%m-%d %H:%M}" + (f" {zone}" if zone else "")


def hour_key(t, zone: str) -> str:
    return f"{t:%Y-%m-%d %H}:00" + (f" {zone}" if zone else "")


def span_hours(s, e, zone: str) -> dict:
    """Each local clock hour a span touches -> (its share, its minutes), to the second (s05-D02: 16:56:22 to 17:24:41
    is 12.83% and 87.17%, not 4 and 24 whole minutes). A span of no length is all in its start's hour."""
    import pandas as pd
    whole = (e - s).total_seconds()
    if whole <= 0:
        return {hour_key(s, zone): (1.0, 0.0)}
    out, t = {}, s
    while t < e:
        nxt = min(t.floor("h") + pd.Timedelta(hours=1), e)
        sec = (nxt - t).total_seconds()
        out[hour_key(t, zone)] = (round(sec / whole, 4), round(sec / 60, 1))
        t = nxt
    return out


def log_hours(s, e, zone: str, total: dict) -> dict:
    """A logged row's output: a whole day as its day (counted once, its hours unknown), else each hour its share, the
    row's whole total, and in_hour, its own minutes and steps."""
    start, end = stamp(s, zone), stamp(e, zone)
    blk = {"start": start, "end": end, "total": total, "items": None, "timeline": None}
    if kind(total["minutes"]) == "day":
        return {f"{s:%Y-%m-%d}": {"share": 1.0, **blk}}
    out = {}
    for h, (sh, mins) in span_hours(s, e, zone).items():
        own = {"minutes": mins, **({"steps": round(sh * total["steps"])} if total.get("steps") else {})}
        out[h] = {"share": sh, "start": start, "end": end, "total": total, "in_hour": own, "items": None,
                  "timeline": None}
    return out


def stream_hours(s, zone: str) -> dict:
    """A stream's output, each hour from its own samples (`s`: t, dur, steps): its minutes sampled, its steps, and its
    moving minutes (samples with any step), with its timeline points."""
    import pandas as pd
    out = {}
    for h, g in s.groupby(s["t"].dt.floor("h"), sort=True):
        end = g["t"].iloc[-1] + pd.Timedelta(minutes=float(g["dur"].iloc[-1]))
        steps = g["steps"].fillna(0)
        out[hour_key(h, zone)] = {
            "start": stamp(g["t"].iloc[0], zone), "end": stamp(end, zone),
            "total": {"minutes": round(float(g["dur"].sum()), 1), "steps": int(round(float(steps.sum()))),
                      "moving_minutes": round(float(g.loc[steps > 0, "dur"].sum()), 1)},
            "items": None, "timeline": [point(r, zone) for r in g.itertuples()]}
    return out


def point(r, zone: str) -> dict:
    """A timeline point: when, and its steps (null when the device sent none)."""
    v = r.steps
    return {"at": stamp(r.t, zone), "steps": None if v != v else int(round(float(v)))}

"""
A sleep event by local hour (b51 s06-D02, D05; JL 261027: "比如说，他睡了 3 个小时，从两点半睡到 5 点半，那睡到的 hour
就包括 2 点、3 点、4 点、5 点"). Each hour the night touches keeps its own minutes in bed, asleep and awake in bed, to
the second; a night with no pieces keeps its minutes in bed as unknown. A few seconds past an hour is no hour.

    kind(minutes)                       night, nap, piece: how long a row is (schema.KINDS)
    joined(spans)                       overlapping or touching spans joined, so a minute counts once
    minutes_by_hour(spans, zone)        {local hour: minutes}
    night_hours(s, e, asleep, zone)     the output
"""


def kind(minutes: float) -> str:
    """A row's kind by how long it is (j06: a night from 3 hours, a nap from 15 minutes, else a piece)."""
    return "night" if minutes >= 180 else "nap" if minutes >= 15 else "piece"


def stamp(t, zone: str) -> str:
    """A local time as the event JSON writes it: "2023-01-22 23:16 -05:00", bare when there is no zone."""
    return f"{t:%Y-%m-%d %H:%M}" + (f" {zone}" if zone else "")


def joined(spans: list) -> list:
    """Overlapping or touching spans joined, so a minute counts once."""
    out = []
    for a, b in sorted(spans):
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def minutes_by_hour(spans: list, zone: str) -> dict:
    """Spans (local start, end) -> {local hour key: minutes}, to the second."""
    import pandas as pd
    out = {}
    for a, b in spans:
        t = a
        while t < b:
            nxt = min(t.floor("h") + pd.Timedelta(hours=1), b)
            k = f"{t:%Y-%m-%d %H}:00" + (f" {zone}" if zone else "")
            out[k] = round(out.get(k, 0) + (nxt - t).total_seconds() / 60, 1)
            t = nxt
    return {k: m for k, m in out.items() if m > 0}            # a few seconds past the hour is no hour (s06-D05)


def night_hours(s, e, asleep, zone: str) -> dict:
    """The output: each local hour its minutes in bed, asleep and awake in bed; asleep None (no pieces, not told):
    in bed and unknown."""
    in_bed = minutes_by_hour([(s, e)], zone)
    if asleep is None:
        return {h: {"in_bed_min": m, "unknown_min": m} for h, m in in_bed.items()}
    slept = minutes_by_hour(asleep, zone)
    out = {}
    for h, m in in_bed.items():
        a = slept.get(h, 0.0)
        out[h] = {"in_bed_min": m, "asleep_min": a, "awake_in_bed_min": round(m - a, 1)}
    return out

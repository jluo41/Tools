"""
A stress event by local hour (b51 s10): each minute one level (schema.py), each hour its minutes added up.

    level_of(value)            rest, low, medium, high, active or unknown, and why when unknown
    by_hour(timeline, style)   the output: each hour its minutes six ways, adding to its minutes, and the mean of its
                               scored minutes
"""
from ..still.preprocess import label
from .schema import ACTIVE, BANDS, NOT_MEASURED, SCORED


def level_of(v) -> tuple:
    """(level; why, when unknown). None is a minute no reading names."""
    if v is None:
        return "unknown", "no_reading"
    if v == ACTIVE:
        return "active", None
    if v == NOT_MEASURED or v < 0:
        return "unknown", "not_measured"
    for name, lo, hi in BANDS:
        if lo <= v <= hi:
            return name, None
    return "unknown", "not_measured"


def by_hour(timeline: dict, style: str) -> dict:
    out, scores = {}, {}
    for i in sorted(timeline):
        v = timeline[i]
        k = label(i, style, hour=True)
        h = out.setdefault(k, {"minutes": 0, **{f"{s}_min": 0 for s in SCORED}, "active_min": 0, "unknown_min": 0,
                               "unknown_why": {"not_measured": 0, "no_reading": 0}, "scored_min": 0, "mean": None})
        lvl, why = level_of(v)
        h["minutes"] += 1
        h[f"{lvl}_min"] += 1
        if why:
            h["unknown_why"][why] += 1
        if lvl in SCORED:
            h["scored_min"] += 1
            scores.setdefault(k, []).append(v)
    for k, vs in scores.items():
        out[k]["mean"] = round(sum(vs) / len(vs), 1)
    return out

"""
A still event by local hour (b51 s07-D02): each minute one way (schema.py), each hour its minutes added up.

    way(point, max_steps)          asleep, moving, still or unknown, and why when unknown
    by_hour(timeline, style, ...)  the output: each hour its minutes, four ways, adding to its minutes
    way_stretches(timeline, ...)   the same minutes as stretches: minutes in a row spent one way are one
"""
from .preprocess import label
from .schema import ASLEEP_LEVELS, AWAKE_LEVELS, RESTLESS_LEVELS


def way(p: dict, max_steps: int) -> tuple:
    """(one of asleep, moving, still, unknown; why, when unknown)."""
    lvl = p.get("level")
    if lvl in ASLEEP_LEVELS:
        return "asleep", None
    if lvl in RESTLESS_LEVELS:
        return "unknown", "restless"
    if lvl in AWAKE_LEVELS:
        return "still", None                                  # awake in bed
    if (p.get("steps") or 0) > max_steps:
        return "moving", None
    if p.get("worn"):
        return "still", None
    return "unknown", "no_heart_rate"


def by_hour(timeline: dict, style: str, max_steps: int) -> dict:
    out = {}
    for i in sorted(timeline):
        p = timeline[i]
        h = out.setdefault(label(i, style, hour=True),
                           {"minutes": 0, "asleep_min": 0, "moving_min": 0, "still_min": 0, "unknown_min": 0,
                            "unknown_why": {"no_heart_rate": 0, "restless": 0}, "still_no_step_row": 0})
        w, why = way(p, max_steps)
        h["minutes"] += 1
        h[f"{w}_min"] += 1
        if why:
            h["unknown_why"][why] += 1
        if w == "still" and p.get("level") is None and p.get("steps") is None:
            h["still_no_step_row"] += 1                     # read as 0 steps: a minute the step file leaves out
    return out


def way_stretches(timeline: dict, style: str, max_steps: int) -> list:
    """The minutes as stretches by their way (b01 reads a still stretch a row, 261109): minutes in a row spent one way,
    for one reason when unknown, are one {"from", "to", "way", "minutes", "why", "no_step_row"}, "to" not included.
    no_step_row counts a still stretch's minutes the step file leaves out (read as 0 steps)."""
    out = []
    for i in sorted(timeline):
        p = timeline[i]
        w, why = way(p, max_steps)
        bare = int(w == "still" and p.get("level") is None and p.get("steps") is None)
        if out and out[-1]["_end"] == i and out[-1]["way"] == w and out[-1]["why"] == why:
            out[-1]["_end"] = i + 1
            out[-1]["no_step_row"] += bare
            continue
        out.append({"_start": i, "_end": i + 1, "way": w, "why": why, "no_step_row": bare})
    return [{"from": label(s["_start"], style), "to": label(s["_end"], style), "way": s["way"],
             "minutes": s["_end"] - s["_start"], "why": s["why"], "no_step_row": s["no_step_row"]} for s in out]

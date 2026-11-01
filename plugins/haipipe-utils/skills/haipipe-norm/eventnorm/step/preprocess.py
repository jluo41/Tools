"""
The step preprocess step: raw, as it arrives, to the input JSON (b51 s15's engine 1). raw["type"] picks the step:

    log            one WellDoc StepEntry row: its local start and end to the second (UTC plus TimezoneOffset), its
                   kind by how long it is, its own total (a 0 or -1 not given), the device that counted it
    steps_stream   a wearable's steps on a clock, read by exercise's own samples() (MetaboNet, OhioT1DM's Basis): a
                   minute sent twice keeps its largest count (mcPhases 2024 sends 2 to 15 copies); exercise's own
                   rule, runs_of with RULES["steps_stream"], finds its walks, handed to POST /exercise/event

Each returns {"input", "kind", "step", and "when": (start, end, zone) for a log or "samples" for a stream}.
"""
from functools import lru_cache

from ..preprocess.common import frame
from .hours import kind as kind_of, point, stamp
from .schema import HEALTH_CONNECT, RAW_TYPES, STATED, WELLDOC_FMT


@lru_cache(maxsize=1)
def devices() -> dict:
    """EntrySourceID -> the device or app WellDoc's dictionary names (20 AppleHealthKit, 37 Google_Fit, ...); 40 is
    in no dictionary, but every row of it carries a HealthConnectMetaDataId: Android's Health Connect. Empty when the
    dictionary is not on this host."""
    import importlib.util
    from pathlib import Path
    import pandas as pd
    spec = importlib.util.spec_from_file_location("haipipe_norm_paths", Path(__file__).resolve().parents[2] / "paths.py")
    paths = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(paths)
    try:
        f = paths.raw_data_store() / "_WellDocInfo/Dictionary/parsed/EntrySourceID.csv"
        t = pd.read_csv(f)
    except Exception:
        return {}
    return {**{str(k): v for k, v in zip(t["EntrySourceID"], t["vendor"])}, HEALTH_CONNECT: "Health Connect"}


def device_name(sid) -> str:
    """'37' -> 'Google_Fit (37)'; an id no dictionary names stays its number; None when the row names none."""
    k = str(sid or "").strip().replace(".0", "")
    if not k or k == "None":
        return None
    return f"{devices()[k]} ({k})" if k in devices() else f"source {k}"


def number(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return None if x != x else x


def times(r) -> tuple:
    """A WellDoc row's local start and end (UTC plus its offset), its zone and its minutes, to the second."""
    import pandas as pd
    off = int(number(r.get("TimezoneOffset")) or 0)
    when = lambda c: pd.to_datetime(r.get(c), format=WELLDOC_FMT, errors="coerce")
    s, e = when("StartDateTime"), when("EndDateTime")
    if pd.isna(s) or pd.isna(e):
        raise ValueError("raw.type 'log': StartDateTime and EndDateTime must be WellDoc times, '6/29/2022 9:56:22 PM'")
    s, e = s + pd.Timedelta(minutes=off), e + pd.Timedelta(minutes=off)
    zone = f"{'+' if off >= 0 else '-'}{abs(off) // 60:02d}:{abs(off) % 60:02d}"
    return s, e, zone, (e - s).total_seconds() / 60


def log(rows) -> dict:
    """One StepEntry row to the input: start, end, device, its own total; items and timeline null."""
    if len(rows) != 1:
        raise ValueError(f"raw.type 'log': one row an event, {len(rows)} sent (events() takes many)")
    r = rows.iloc[0].to_dict()
    s, e, zone, minutes = times(r)
    total = {"minutes": round(minutes, 1)}
    for k, c in STATED.items():
        v = number(r.get(c))
        if v is not None and v > 0:
            total[k] = int(v) if v == int(v) else v
    k = kind_of(minutes)
    inp = {"start": stamp(s, zone), "end": stamp(e, zone), "device": device_name(r.get("EntrySourceID")),
           "total": total, "items": None, "timeline": None}
    step = f"a logged row of {minutes:.1f} minutes: {'an' if k == 'hour' else 'a'} {k}" + (", counted once, its hours unknown" if k == "day" else
                                                              ", shared by local hour to the second")
    return {"input": inp, "kind": k, "step": step, "when": (s, e, zone)}


def stream(rows, raw: dict) -> dict:
    """A stream to the input: its samples, a minute sent twice kept once at its largest, every sample a timeline
    point, and its walks by exercise's rule."""
    import pandas as pd
    from ..exercise.preprocess import RULES, runs_of, samples
    s, _ = samples(rows, "steps_stream")
    if "steps" not in s:
        raise ValueError("raw.type 'steps_stream': no steps column")
    n = len(s)
    s = s.sort_values(["t", "steps"]).drop_duplicates("t", keep="last").reset_index(drop=True)
    copies = n - len(s)
    zone = str(raw.get("zone") or "")
    if s.empty:
        return {"input": None, "kind": "stream", "step": "a stream with no time read", "samples": s, "walks": []}
    runs = runs_of(s, RULES["steps_stream"])
    last = s.set_index("t")["dur"]
    walks = [{"start": stamp(w.start, zone), "end": stamp(w.end + pd.Timedelta(minutes=float(last[w.end])), zone),
              "minutes": round(float(w.minutes), 1), "steps": int(round(float(w.steps))), "spm": round(float(w.spm), 1),
              "to": "POST /exercise/event"} for w in runs.itertuples()]
    end = s["t"].iloc[-1] + pd.Timedelta(minutes=float(s["dur"].iloc[-1]))
    total = {"minutes": round(float(s["dur"].sum()), 1), "steps": int(round(float(s["steps"].fillna(0).sum())))}
    inp = {"start": stamp(s["t"].iloc[0], zone), "end": stamp(end, zone), "device": raw.get("device"),
           "total": total, "items": None, "timeline": [point(r, zone) for r in s.itertuples()]}
    step = (f"a stream of {len(s):,} samples every {float(s['dur'].iloc[0]):g} min" +
            (f", {copies:,} repeated times kept once at their largest" if copies else "") +
            f"; {len(walks)} walk{'s' * (len(walks) != 1)} of 100 steps a minute for 10 minutes")
    return {"input": inp, "kind": "stream", "step": step, "samples": s, "walks": walks}


def preprocess(raw: dict) -> dict:
    """raw {"type", "rows", "zone"?, "device"?} to {"input", "kind", "step", ...}; a ValueError names what is wrong."""
    typ = (raw or {}).get("type")
    if typ not in RAW_TYPES:
        raise ValueError(f"raw.type must be one of {sorted(RAW_TYPES)}, not {typ!r}")
    rows = frame(raw)
    return log(rows) if typ == "log" else stream(rows, raw)

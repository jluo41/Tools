"""
The exercise preprocess step: raw, as it arrives, to the input JSON (b51 s12's engine 1). raw["type"] picks the step:

    a logged row   device_code, app_list, other, log: one ELogExerciseEntry row, its code named through the code book
                   (ext_exercise_codebook, pinned by EventNormV7); a day total is set aside (s02-D19), an Other kept
                   for its total when it has minutes (s02-D18), a session asked as the book's words
    words          text: "brisk walking 30 min" and when it began
    a study's label  label: a person's rows of a study's workout word (MetaboNet: date, workout_label,
                   workout_duration), pieces of one workout back to back joined; each workout is logged, its MET the
                   Compendium's for the word
    a stream       met_stream, steps_stream, named_stream, strap_stream, motion_stream, lab_stream: a wearable's
                   samples; its rule finds the workout (a MET of 3, 100 steps a minute, the device's word checked
                   against its steps, for 10 minutes; s02-D22, D25), else it stays a stream

Each returns {"input": the input JSON or None when nothing is an event, "kind": what the step found, "step": what it
did, in one line, and for a stream "stream": what the hours and the item need}.
"""
import re
from functools import lru_cache

from ..preprocess.common import clock, frame
from .hours import intensity, whole
from .schema import CODEBOOK_RELEASE, RAW_TYPES

LOGGED = ("device_code", "app_list", "other", "log")
STATED = [("minutes", "ExerciseDuration"), ("calories", "CaloriesBurned"), ("distance_m", "DistanceInMeters")]
KIND = {"daily_rollup": "day_total", "placeholder": "other", "unread": "unread"}   # else by the code's book

# A stream's column shapes: its time (and end), its numbers under one name each, how its MET is scaled, the device's
# word, its clock in minutes when one sample cannot tell it, and who gives its MET.
SHAPES = {
    "met_stream": [{"time": "Timestamp", "values": {"met": "METs", "hr": "HR", "calories": "Calories (Activity)"},
                    "scale": {"met": 0.1}, "sample": 1}],
    "steps_stream": [{"time": "date", "values": {"steps": "steps", "hr": "heartrate", "calories": "calories_burned"},
                      "sample": 5},
                     {"time": "ts", "format": "%d-%m-%Y %H:%M:%S",
                      "values": {"steps": "basis_steps", "hr": "basis_heart_rate"}, "sample": 5}],
    "named_stream": [{"time": "start_date_time", "end": "end_date_time", "utc": True, "zone": "+00:00",
                      "values": {"steps": "base_movement_quantity", "hr": "heart_rate_mean"}, "name": "activity_name"}],
    "strap_stream": [{"time": "time", "values": {"hr": "HR", "motion": "Activity"}, "sample": 5}],
    "motion_stream": [{"time": "ts", "format": "%d-%m-%Y %H:%M:%S", "values": {"motion": "acceleration"}, "sample": 1}],
    "lab_stream": [{"time": "minute", "values": {"met": "METS", "motion": "wristSVM"}, "sample": 1,
                    "conf": "MEASURED", "source": "lab"}],
}
RULES = {"met_stream": {"by": "met", "min": 3, "minutes": 10},
         "steps_stream": {"by": "steps", "min": 100, "minutes": 10},
         "named_stream": {"by": "name", "names": ["walking", "running"], "steps_min": 100, "minutes": 10},
         "strap_stream": None, "motion_stream": None,
         "lab_stream": {"by": "met", "min": 3, "minutes": 10}}


@lru_cache(maxsize=1)
def codebook() -> dict:
    """ext_exercise_codebook at the version CODEBOOK_RELEASE pins: "<code>|<source>" -> its row."""
    import importlib.util
    import pandas as pd
    from pathlib import Path
    here = Path(__file__).resolve()
    spec = importlib.util.spec_from_file_location("haipipe_norm_paths", here.parents[2] / "paths.py")
    paths = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(paths)
    f = paths.release_file("ext_exercise_codebook", release=CODEBOOK_RELEASE)
    if not f:
        raise ValueError(f"no ext_exercise_codebook pinned by {CODEBOOK_RELEASE} on this host")
    t = pd.read_parquet(f)
    return {r["ExerciseCode_original"]: r for r in t.to_dict("records")}


def number(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return None if x != x else x


def stated(r) -> dict:
    """A logged row's own total, as the raw states it (s02-D14): minutes, calories and metres; an empty cell or a 0 is
    "not given" and left out, never 0. ExerciseIntensity never goes in: it is 0 in every row."""
    out = {}
    for name, col in STATED:
        v = number(r.get(col))
        if v is not None and v > 0:
            out[name] = int(v) if v == int(v) else round(v, 1)
    return out


def plus(start: str, minutes) -> str:
    """The end: a start and its minutes, the start's offset kept."""
    import pandas as pd
    t0 = pd.to_datetime(start[:16], errors="coerce")
    if minutes is None or t0 != t0:
        return None
    return (t0 + pd.Timedelta(minutes=minutes)).strftime("%Y-%m-%d %H:%M") + start[16:]


def logged(rows, asked: str) -> dict:
    """One ELogExerciseEntry row: its code named through the code book, its time made local, its own total."""
    if len(rows) != 1:
        raise ValueError(f"raw.type {asked!r}: one logged row is one event; {len(rows)} rows came")
    r = rows.iloc[0].to_dict()
    bare = lambda v: re.sub(r"\.0$", "", str(v or "").strip())  # "23.0" is source 23
    code = f"{bare(r.get('ExerciseType'))}|{bare(r.get('EntrySourceID'))}"
    book = codebook().get(code)
    row_kind = book["RowKind"] if book else "unread"
    kind = KIND.get(row_kind) or ("app_list" if book["Book"] == "welldoc_app" else "device_code")
    v = number(r.get("ExerciseDuration"))
    minutes = None if not v else int(v) if v == int(v) else v   # a 0 is "not given" (s02-D14): no end, no 0 minutes
    start = clock(rows, "ObservationDateTime", offset="TimezoneOffset")
    end = plus(start, minutes) if start else None
    said = f"codebook ({book['Book']}): {code}" if book else f"no codebook row: {code}"
    if row_kind == "daily_rollup":
        return {"input": None, "kind": kind,
                "step": f"{said} is a daily rollup, not a workout, so it is set aside (s02-D19)"}
    if row_kind == "placeholder":
        if not minutes:
            return {"input": None, "kind": kind,
                    "step": f"{said} names no activity, and the row has no minutes, so no time to place it: dropped "
                            "(s02-D18)"}
        return {"input": {"start": start, "end": end, "total": stated(r), "items": None, "timeline": None},
                "kind": kind, "minutes": minutes, "step": f"{said}: the vendor names it only Other; no item, kept for its total (minutes "
                                     "and kcal), no MET (s02-D18)"}
    words = book["Name"] if book and isinstance(book["Name"], str) else str(r.get("ExerciseType"))
    return {"input": {"start": start, "end": end, "total": stated(r),
                      "items": [{"id": "i1", "activity": words, "met": None}], "timeline": None},
            "kind": kind, "minutes": minutes, "step": f"{said} → {words}" if book else f"{said}: the words as typed"}


MINUTES = re.compile(r"(?:\bfor\s+|\babout\s+)?(\d+(?:\.\d+)?)\s*(minutes?|mins?|min|分钟|分)\b", re.I)
HOURS = re.compile(r"(?:\bfor\s+|\babout\s+)?(\d+(?:\.\d+)?)\s*(hours?|hrs?|h|小时)\b", re.I)


# What parts typed words into activities done one after another (JL 261028: "brisk walking 20 min then swimming 30
# min" is two workouts, not one): "then", "followed by", "after that", 然后, a comma or a semicolon; a plain "and" only
# when each side has its own minutes ("walked 20 min and swam 30 min", but "walking and jogging 30 min" is one).
THEN = re.compile(r"\s*(?:,?\s*\b(?:and then|then|followed by|after that|afterwards)\b|[;,+]|[，；、]|然后|之后)\s*", re.I)
AND = re.compile(r"\s+(?:and|&)\s+|和|跟", re.I)


def amount(words: str):
    """The minutes in some words (the first "30 min" or "1 hour") and the words left once they are taken out."""
    for pat, k in ((MINUTES, 1), (HOURS, 60)):
        m = pat.search(words)
        if m:
            return whole(float(m.group(1)) * k), words[:m.start()] + words[m.end():]
    return None, words


def pieces(words: str) -> list:
    """Typed words as (activity, minutes), one a workout, in the order they were done. A piece with no words of its own
    ("brisk walking, 30 min") belongs to the one before it."""
    def amounts(w):
        return sum(len(p.findall(w)) for p in (MINUTES, HOURS))
    parts = []
    for p in (x for x in THEN.split(words) if x and x.strip()):
        parts += [q for q in AND.split(p) if q.strip()] if amounts(p) > 1 else [p]
    made = []
    for p in parts:
        minutes, rest = amount(p)
        activity = re.sub(r"\s+", " ", rest).strip(" ,;:.，；、")
        if not activity and made and made[-1][1] is None:
            made[-1] = (made[-1][0], minutes)
        elif activity or minutes:
            made.append((activity, minutes))
    return made


def text(rows, asked: str, every_workout: bool = False):
    """Words typed or said: the activity and its minutes ("brisk walking 30 min", "swim 1 hour"), and when it began
    (the row's time). Activities done one after another ("brisk walking 20 min then swimming 30 min") are as many
    workouts, back to back from that time, one activity each (s02-D06): with `every_workout` each one, else the
    longest, as a study's labels."""
    r = rows.iloc[0].to_dict()
    words = str(r.get("text") or "").strip()
    if not words:
        raise ValueError('raw.type "text": its row needs "text", the activity and its minutes')
    found = pieces(words) or [("", None)]
    start = str(r.get("time")).strip() if r.get("time") else None
    made = []
    for activity, minutes in found:
        end = plus(start, minutes) if start and minutes else None
        made.append({"input": {"start": start, "end": end, "total": {"minutes": minutes} if minutes else None,
                               "items": [{"id": "i1", "activity": activity, "met": None}] if activity else None,
                               "timeline": None},
                     "kind": "text", "minutes": minutes,
                     "step": f"the words → '{activity}'" + (f", {minutes} minutes" if minutes else ", no minutes")})
        start = end                                             # the next one begins where this one ends
    if len(made) == 1:
        return made if every_workout else made[0]
    if every_workout:
        return [dict(w, step=f"workout {k + 1} of {len(made)}: {w['step']}") for k, w in enumerate(made)]
    k = max(range(len(made)), key=lambda k: (made[k]["minutes"] or 0, -k))   # the longest, the first on a tie
    return dict(made[k], step=f"{len(made)} activities, one after another; the longest kept (events() gives each): "
                              + made[k]["step"])


LABEL = {"time": "date", "word": "workout_label", "minutes": "workout_duration"}


def labels(rows, every_workout: bool = False):
    """A person's workout labels (MetaboNet's harmonized table): each row a word at a time, with its minutes when the
    study gives them, else one tick of the table's clock (BrisT1D logs a word every 5 minutes, T1D-UOM a 15-minute
    piece). A piece that starts where the last of the same word ended is the same workout. Returns the longest
    workout, or with `every_workout` every one in time order; each is logged, like a WellDoc row."""
    import pandas as pd
    miss = [c for c in (LABEL["time"], LABEL["word"]) if c not in rows.columns]
    if miss:
        raise ValueError(f'raw.type "label": its rows need {LABEL["time"]} and {LABEL["word"]}; missing {miss}')
    s = pd.DataFrame({"t": pd.to_datetime(rows[LABEL["time"]], errors="coerce"),
                      "word": rows[LABEL["word"]].fillna("").astype(str).str.strip(),
                      "given": pd.to_numeric(rows.get(LABEL["minutes"]), errors="coerce") if LABEL["minutes"] in rows
                      else float("nan")})
    s = s.dropna(subset=["t"])
    s = s[s["word"] != ""].sort_values("t").reset_index(drop=True)
    if s.empty:
        none = {"input": None, "kind": "label", "step": "no row has a word and a time: no workout"}
        return [none] if every_workout else none
    gap = s["t"].diff().dt.total_seconds() / 60
    tick = float(gap[gap > 0].median()) if (gap > 0).any() else 5.0
    tick = min(max(1.0, round(tick)), 15.0)                     # the table's clock: 5 minutes in MetaboNet
    s["dur"] = s["given"].where(s["given"] > 0, float("nan"))   # a 0 is "not given" (s02-D14)
    s["dur"] = s["dur"].fillna(s["given"].isna().map({True: tick, False: float("nan")}))
    ends = s["t"] + pd.to_timedelta(s["dur"].fillna(0), unit="min")
    cut = (s["word"] != s["word"].shift()) | (s["t"] - ends.shift() > pd.Timedelta(minutes=0.5)) | s["dur"].isna()
    made = []
    for _, g in s.groupby(cut.astype(int).cumsum()):
        start = g["t"].iloc[0].strftime("%Y-%m-%d %H:%M")
        minutes = whole(float(g["dur"].sum())) if g["dur"].notna().all() else None
        said = f"the study's label '{g['word'].iloc[0]}'" + (
            f", {len(g)} pieces back to back joined" if len(g) > 1 else "") + (
            f", {minutes} minute{'s' if minutes != 1 else ''}" if minutes else ", no minutes (a 0 is not given)")
        made.append({"input": {"start": start, "end": plus(start, minutes) if minutes else None,
                               "total": {"minutes": minutes} if minutes else None,
                               "items": [{"id": "i1", "activity": str(g["word"].iloc[0]), "met": None}],
                               "timeline": None},
                     "kind": "label", "minutes": minutes, "step": said})
    if every_workout:
        return [dict(w, step=f"workout {k + 1} of {len(made)}: {w['step']}") for k, w in enumerate(made)]
    return made[max(range(len(made)), key=lambda k: (made[k]["minutes"] or 0, -k))]   # the longest, the first on a tie


def samples(rows, kind: str):
    """A stream's rows as samples: `t` (and `t_end`), `dur` its minutes, each number under one name, `name` the
    device's word. Returns (samples, its shape)."""
    import pandas as pd
    shape = next((s for s in SHAPES[kind] if s["time"] in rows.columns and
                  any(c in rows.columns for c in s["values"].values())), None)
    if shape is None:
        raise ValueError(f"raw.type {kind!r}: these columns are no shape this step reads: {list(rows.columns)[:12]}")
    s = rows.copy()
    if shape.get("utc"):
        s["t"] = pd.to_datetime(s[shape["time"]], utc=True, errors="coerce").dt.tz_localize(None)
    elif shape.get("format"):
        s["t"] = pd.to_datetime(s[shape["time"]], format=shape["format"], errors="coerce")
    else:
        s["t"] = pd.to_datetime(s[shape["time"]], errors="coerce")
    if shape.get("end"):
        s["t_end"] = pd.to_datetime(s[shape["end"]], utc=True, errors="coerce").dt.tz_localize(None)
    for name, col in shape["values"].items():
        if col in s:
            s[name] = pd.to_numeric(s[col], errors="coerce").astype("float64") * float(
                (shape.get("scale") or {}).get(name, 1))
    if shape.get("name"):
        s["name"] = s[shape["name"]]
    s = s.dropna(subset=["t"]).sort_values("t").reset_index(drop=True)
    gap = s["t"].diff().dt.total_seconds().median() / 60 if len(s) > 1 else float("nan")
    sample = max(1.0, float(round(gap))) if gap == gap else float(shape.get("sample", 1))
    s["dur"] = (s["t_end"] - s["t"]).dt.total_seconds() / 60 if "t_end" in s else sample
    return s, shape


def runs_of(s, rule: dict):
    """Every run a rule finds of at least its minutes, the samples joined while each starts where the last ended (one
    word a run when the rule reads the device's word), with its steps a minute when the stream counts steps."""
    import pandas as pd
    by = rule["by"]
    if by not in s:
        return s.iloc[:0]
    on = s["name"].isin(rule["names"]) if by == "name" else \
        s["steps"] >= float(rule["min"]) * s["dur"] if by == "steps" else s[by] >= float(rule["min"])
    ends = s["t"] + pd.to_timedelta(s["dur"], unit="min")
    cut = (on != on.shift()) | (s["t"] - ends.shift() > pd.Timedelta(minutes=0.5))
    if by == "name":
        cut |= s["name"] != s["name"].shift()
    grp = cut.cumsum()
    agg = {"start": ("t", "min"), "end": ("t", "max"), "n": ("t", "size"), "minutes": ("dur", "sum")}
    if "steps" in s:
        agg["steps"] = ("steps", "sum")
    runs = s[on].groupby(grp[on]).agg(**agg)
    runs = runs[runs["minutes"] >= float(rule.get("minutes", 10))]
    if "steps" in runs:
        runs["spm"] = runs["steps"] / runs["minutes"]
    return runs


def stream(rows, kind: str, every_workout: bool = False):
    """A stream: its rule finds the longest workout; it becomes the input (its own amounts summed, a timeline point a
    sample), or, when no rule reads it or none is found, it stays a stream and the step says how far short it falls.
    With `every_workout`, a list: every workout the rule finds, in time order (a freeze's call), or the one no-workout
    answer."""
    s, shape = samples(rows, kind)
    rule = RULES[kind]
    runs = runs_of(s, rule) if rule else None
    every = runs
    if runs is not None and rule.get("steps_min") and "spm" in runs:   # the word must agree with the steps (s02-D25)
        runs = runs[runs["spm"] >= float(rule["steps_min"])]
    if runs is None or runs.empty:
        if not rule:
            why = "no rule finds a workout in it: it stays a stream (s02-D22)"
        elif rule["by"] not in s:                               # the file lacks the column its rule reads
            col = shape["name"] if rule["by"] == "name" else shape["values"].get(rule["by"])
            why = f"it has no {col} column, which its rule reads: no workout can be found; it stays a stream"
        elif rule["by"] == "name":
            best = f"its best run of {rule['minutes']:g} minutes or more is {every['spm'].max():.0f} a minute" \
                if every is not None and len(every) and "spm" in every else f"no run of {rule['minutes']:g} minutes"
            why = (f"the device calls it {' or '.join(rule['names'])}, but never at {rule['steps_min']:g} steps a "
                   f"minute for {rule['minutes']:g} minutes ({best}): not a workout; it stays a stream (s02-D25)")
        else:
            most = s[rule["by"]] / (s["dur"] if rule["by"] == "steps" else 1)
            why = (f"its rule ({rule['by']} {rule['min']:g} or more a minute, for {rule['minutes']:g} minutes) finds no "
                   f"workout: at most {most.max():.0f} a minute in {len(s):,} samples; it stays a stream (s02-D22)")
        none = {"input": None, "kind": kind, "step": why}
        return [none] if every_workout else none
    if every_workout:
        made = [workout(s, shape, kind, p) for _, p in runs.sort_values("start").iterrows()]
        return [dict(w, step=f"workout {k + 1} of {len(made)}: {w['step']}") for k, w in enumerate(made)]
    return workout(s, shape, kind, runs.sort_values(["minutes", "start"], ascending=[False, True]).iloc[0])


def workout(s, shape: dict, kind: str, pick) -> dict:
    """One workout a stream's rule found (`pick`: its start and end): its samples become the input."""
    import pandas as pd
    bout = s[(s["t"] >= pick["start"]) & (s["t"] <= pick["end"])].reset_index(drop=True)
    zone = f" {shape['zone']}" if shape.get("zone") else ""
    fmt = lambda t: t.strftime("%Y-%m-%d %H:%M") + zone
    dur = bout["dur"]
    start, end = fmt(bout["t"].iloc[0]), fmt(bout["t"].iloc[-1] + pd.Timedelta(minutes=float(dur.iloc[-1])))
    minutes = int(round(float(dur.sum())))
    have = [n for n in ("met", "hr", "steps", "calories", "motion") if n in bout and bout[n].notna().any()]
    places = {"met": 1, "hr": 0, "steps": 0, "calories": 1, "motion": 3}
    line = []
    for k in range(len(bout)):                                  # every number the device gives, under one name
        pt = {"at": bout["t"].iloc[k].strftime("%H:%M"), "item": "i1"}
        for n in have:
            v = bout[n].iloc[k]
            if v == v:
                pt[n] = int(round(float(v))) if places[n] == 0 else round(float(v), places[n])
        line.append(pt)
    named = bout["name"].iloc[0] if "name" in bout else None
    rows_met = "met" in have
    met = met_minutes = None
    if rows_met:                                                # the device's or the lab's own MET, as it comes
        met_minutes = round(float((bout["met"] * dur).sum()), 1)
        met = round(met_minutes / minutes, 2)
    own = {"minutes": minutes, **({"met_minutes": met_minutes} if rows_met else {}),
           **{n: (int(round(float(bout[n].sum()))) if n == "steps" else round(float(bout[n].sum()), 1))
              for n in ("steps", "calories") if n in have}}
    spm = own["steps"] / minutes if own.get("steps") and minutes else None
    if rows_met:
        why = ("no activity is named, and none is needed: the device gives a MET each minute, used as it comes "
               "(s02-D11); describe-exercise is not asked") if not shape.get("source") else \
            "a lab measured this MET, a minute each: used as it comes; a ruler for ours"
    elif named:
        why = f"the device names it {named}: the Compendium's MET for that word, asked live"
    else:
        why = (f"found by its steps, {spm:.0f} a minute (100 is brisk walking, about 3 MET); no MET: the device gives "
               "none and names nothing") if spm is not None else "no MET: the device gives none and names nothing"
    return {"input": {"start": start, "end": end, "total": own,
                      "items": [{"id": "i1", "activity": named, "met": None}], "timeline": line},
            "kind": kind, "step": why,
            "stream": {"bout": bout, "line": line, "have": have, "rows_met": rows_met, "named": named, "met": met,
                       "met_minutes": met_minutes, "minutes": minutes, "own": own, "zone": zone,
                       "conf": shape.get("conf", "DEVICE"),
                       "source": f"{shape.get('source', 'device')}:{shape['values'].get('met')}"}}


def kind_of(rows) -> str:
    """A wearable file's stream type, by its columns: the type one of whose shapes has its time column and the most
    of its numbers (a type with a rule first on a tie, in SHAPES' order). A ValueError lists what each type reads."""
    cols = set(rows.columns)
    best, most = None, 0
    for kind, shapes in SHAPES.items():
        for s in shapes:
            n = sum(c in cols for c in s["values"].values()) if s["time"] in cols else 0
            if n > most:
                best, most = kind, n
    if best is None:
        reads = "; ".join(f"{k}: {s['time']} + {', '.join(s['values'].values())}" for k, ss in SHAPES.items()
                          for s in ss)
        raise ValueError(f"no stream type reads these columns {sorted(cols)[:12]}; each reads: {reads}")
    return best


def preprocess(raw: dict, every_workout: bool = False):
    """raw to the input. With `every_workout`, a list: a stream's every workout (a freeze's call); one answer else."""
    kind = (raw or {}).get("type")
    if kind not in RAW_TYPES:
        raise ValueError(f"raw.type {kind!r} is not one of {sorted(RAW_TYPES)}")
    rows = frame(raw)
    one = (lambda pre: [pre]) if every_workout else (lambda pre: pre)
    if kind in LOGGED:
        return one(logged(rows, kind))
    if kind == "text":
        return text(rows, kind, every_workout)
    if kind == "label":
        return labels(rows, every_workout)
    if kind == "wearable":                                      # an uploaded file: its columns say which stream it is
        found = kind_of(rows)
        said = f"a wearable file of {len(rows):,} rows, read as {found} by its columns: "
        pres = stream(rows, found, every_workout)
        return [{**p, "step": said + p["step"]} for p in pres] if every_workout else {**pres, "step": said + pres["step"]}
    return stream(rows, kind, every_workout)

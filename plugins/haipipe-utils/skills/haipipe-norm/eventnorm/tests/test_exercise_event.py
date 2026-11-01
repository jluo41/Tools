"""
Checks for eventnorm.exercise. The hours, the words and the errors need nothing; the examples need the SPACE's tables
and s02's files.

    python skills/haipipe-norm/eventnorm/tests/test_exercise_event.py

THE EXAMPLES. b51 s02 ③ and ④'s events (s02-exercise-api/assets/exercise-events-every-kind.json and
exercise-streams-every-kind.json, written by its drawing builder, where this logic ran first) are sent raw, and the
input and output must come back as those files hold them. The files are read in place, never copied here: their rows
are a cohort's. With no such files on this host, the examples are skipped and say so.

Same shape as food's test_eventnorm.py: PASS/FAIL lines, exit 1 on any FAIL.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))                       # skills/haipipe-norm, so `eventnorm` imports
from eventnorm.exercise import event, events, exercise_hours    # noqa: E402

S02 = "examples-1-data/Proj01-CGM-RawData/work/b51_externalstore/s02-exercise-api/assets/"
FILES = ("exercise-events-every-kind.json", "exercise-streams-every-kind.json")
PASS, FAIL = [], []


def check(name, fn):
    try:
        note = fn()
        PASS.append(name)
        print(f"  PASS  {name}" + (f"  ({note})" if note else ""))
    except Exception as e:
        FAIL.append(name)
        print(f"  FAIL  {name}: {type(e).__name__}: {e}")


def diff(a, b, p=""):
    """The first field where a and b differ, by path; None when none does."""
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            d = diff(a.get(k), b.get(k), f"{p}.{k}")
            if d:
                return d
        return None
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return f"{p}: {len(a)} vs {len(b)} entries"
        return next((d for d in (diff(x, y, f"{p}[{i}]") for i, (x, y) in enumerate(zip(a, b))) if d), None)
    nan = lambda v: v is None or (isinstance(v, float) and math.isnan(v))
    if nan(a) and nan(b):
        return None
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a - b) < 1e-9:
        return None
    return None if a == b else f"{p}: s02 {a!r} vs eventnorm {b!r}"


def t_hours_add_up():
    out = exercise_hours("2022-05-22 17:48 -06:00", "2022-05-22 18:29 -06:00", 41, None, {"calories": 369}, None)
    got = {h: (b["total"]["minutes"], b["total"]["calories"]) for h, b in out.items()}
    want = {"2022-05-22 17:00 -06:00": (12, 108), "2022-05-22 18:00 -06:00": (29, 261)}
    assert got == want, got
    return "41 minutes and 369 kcal split 12/108 and 29/261"


def t_words():
    ev = event(raw={"type": "text", "rows": [{"text": "brisk walking 30 min", "time": "2026-10-22 08:45 -04:00"}]})
    it = ev["input"]["items"][0]
    assert it["activity"] == "brisk walking" and ev["input"]["total"] == {"minutes": 30}, ev["input"]
    hours = {h: b["total"]["minutes"] for h, b in ev["output"].items()}
    assert hours == {"2026-10-22 08:00 -04:00": 15, "2026-10-22 09:00 -04:00": 15}, hours
    return f"'{it['activity']}', 30 minutes, MET {next(iter(ev['output'].values()))['items'][0]['met']}"


def t_words_then():
    """Two activities typed one after another are two workouts back to back, each its own minutes (JL 261028: "brisk
    walking 20 min then swimming 30 min" had come back as one activity, "brisk walking then swimming 30 min")."""
    raw = {"type": "text", "rows": [{"text": "brisk walking 20 min then swimming 30 min", "time": "2026-10-22 08:45 -04:00"}]}
    evs = events(raw)
    got = [(e["input"]["items"][0]["activity"], e["input"]["total"]["minutes"], e["input"]["start"][11:16],
            e["input"]["end"][11:16]) for e in evs]
    assert got == [("brisk walking", 20, "08:45", "09:05"), ("swimming", 30, "09:05", "09:35")], got
    one = event(raw=raw)
    assert one["input"]["items"][0]["activity"] == "swimming" and "2 activities" in one["step"], one["step"]
    for words, want in (("walking and jogging 30 min", [("walking and jogging", 30)]),
                        ("walked 20 min and swam 30 min", [("walked", 20), ("swam", 30)]),
                        ("brisk walking, 30 min", [("brisk walking", 30)])):
        es = events({"type": "text", "rows": [{"text": words, "time": "2026-10-22 08:45 -04:00"}]})
        got = [(e["input"]["items"][0]["activity"], e["input"]["total"]["minutes"]) for e in es]
        assert got == want, (words, got)
    return "20 min walking 08:45-09:05, then 30 min swimming 09:05-09:35; event() keeps the longest"


def t_zero_minutes():
    """A logged workout whose duration is 0 has no minutes: no end, minutes and MET-minutes null, never 0 (t07 r02
    found 4,707 such rows; s02-D14: a 0 is "not given")."""
    row = {"ExerciseType": "1001", "EntrySourceID": "23", "ObservationDateTime": "12/26/2020 1:39:00 PM",
           "TimezoneOffset": "-300", "ExerciseDuration": "0", "CaloriesBurned": "63"}
    ev = event(raw={"type": "log", "rows": [row]})
    assert ev["input"]["end"] is None and "minutes" not in (ev["input"]["total"] or {}), ev["input"]
    (hour, b), = ev["output"].items()
    assert b["total"]["minutes"] is None and b["total"]["met_minutes"] is None and b["total"]["calories"] == 63, b
    return f"one hour, {hour}: minutes null, MET {b['total']['met']}, 63 kcal kept"


def t_day_total():
    row = {"ExerciseType": "20903", "EntrySourceID": "20", "ObservationDateTime": "1/13/2022 5:59:00 AM",
           "TimezoneOffset": "-360", "ExerciseDuration": "24", "CaloriesBurned": "0"}
    ev = event(raw={"type": "log", "rows": [row]})
    assert ev["input"] is None and ev["output"] is None and "daily rollup" in ev["step"], ev["step"]
    return ev["step"]


def t_refusals():
    for body, word in (({}, "send"), ({"raw": {"type": "photo", "rows": [{}]}}, "not one of"),
                       ({"input": {"items": [{"activity": "a"}, {"activity": "b"}]}}, "one activity")):
        try:
            event(**body)
        except ValueError as e:
            assert word in str(e), str(e)
        else:
            raise AssertionError(f"{body} was not refused")
    ev = event(raw={"type": "met_stream", "rows": [{"Timestamp": f"2020-05-05 18:{m:02d}:00", "HR": "120",
                                                     "Intensity": "2"} for m in range(15)]})
    assert ev["input"] is None and "no METs column" in ev["step"], ev["step"]   # 11 CGMacros files (t99 r05)
    return "no body, an unknown raw type, two items; a MET stream with no METs column stays a stream"


def t_examples():
    space = next((p for p in HERE.parents if (p / "env.sh").is_file()), None)
    space = space or next((p for p in Path.cwd().resolve().parents if (p / "env.sh").is_file()), Path.cwd())
    n = 0
    for f in FILES:
        path = space / S02 / f
        if not path.is_file():
            return f"skipped: no {S02}{f} on this host"
        for e in json.loads(path.read_text(encoding="utf-8"))["events"]:
            if not all(isinstance(r, dict) for r in e["raw"].get("rows") or []):
                continue                                        # rows a licence keeps off the board (s02-D27)
            ev = event(raw=e["raw"])
            d = diff(e["input"], ev["input"], "input") or diff(e["output"], ev["output"], "output")
            assert not d, f"{e.get('example')}: {d}"
            n += 1
    return f"{n} examples, input and output as s02's files hold them"


def t_wearable():
    """A stream sent as "wearable" (the try page's upload) finds its own type by its columns and answers as that type."""
    space = next((p for p in HERE.parents if (p / "env.sh").is_file()), None)
    space = space or next((p for p in Path.cwd().resolve().parents if (p / "env.sh").is_file()), Path.cwd())
    path = space / S02 / FILES[1]
    if not path.is_file():
        return f"skipped: no {S02}{FILES[1]} on this host"
    n = 0
    for e in json.loads(path.read_text(encoding="utf-8"))["events"]:
        rows = e["raw"].get("rows") or []
        if not rows or not all(isinstance(r, dict) for r in rows):
            continue
        typed, up = event(raw=e["raw"]), event(raw={**e["raw"], "type": "wearable"})
        d = diff(typed["input"], up["input"], "input") or diff(typed["output"], up["output"], "output")
        assert not d, f"{e['raw']['type']}: {d}"
        assert f"read as {e['raw']['type']}" in up["step"], up["step"]
        n += 1
    try:
        event(raw={"type": "wearable", "rows": [{"when": "2026-10-22 08:00", "pulse": "90"}]})
    except ValueError as e:
        assert "no stream type reads" in str(e), str(e)
    else:
        raise AssertionError("a file no stream type reads was not refused")
    return f"{n} streams found their own type; a file of unknown columns refused"


def t_every_workout():
    """events() gives back every workout a stream holds, in time order; event()'s one (the longest) is among them,
    the same to the field; a logged row gives back its one event."""
    space = next((p for p in HERE.parents if (p / "env.sh").is_file()), None)
    space = space or next((p for p in Path.cwd().resolve().parents if (p / "env.sh").is_file()), Path.cwd())
    path = space / S02 / FILES[1]
    if not path.is_file():
        return f"skipped: no {S02}{FILES[1]} on this host"
    n = found = 0
    for e in json.loads(path.read_text(encoding="utf-8"))["events"]:
        rows = e["raw"].get("rows") or []
        if not rows or not all(isinstance(r, dict) for r in rows):
            continue
        one, every = event(raw=e["raw"]), events(raw=e["raw"])
        starts = [x["input"]["start"] for x in every if x["input"]]
        assert starts == sorted(starts), starts
        if one["input"] is None:
            assert len(every) == 1 and every[0]["input"] is None, len(every)
        else:
            same = [x for x in every if not (diff(one["input"], x["input"]) or diff(one["output"], x["output"]))]
            assert len(same) == 1, f"{e['raw']['type']}: event()'s workout is not one of events()'"
        n += 1
        found += len(starts)
    row = {"ExerciseType": "1001", "EntrySourceID": "23", "ObservationDateTime": "2/24/2022 3:04:13 AM",
           "TimezoneOffset": "-360", "ExerciseDuration": "14"}
    assert len(events(raw={"type": "log", "rows": [row]})) == 1
    return f"{n} streams, {found} workouts in time order, each longest the same as event()'s; a logged row gives one"


def t_labels():
    """A study's workout labels (raw.type "label", MetaboNet's three shapes): one row a workout with its minutes (Loop);
    15-minute pieces back to back, one workout (T1D-UOM); a word every 5 minutes with no minutes (BrisT1D). A 0 is
    not given. The person's id never reaches the raw shown."""
    row = lambda t, w, m=None: {"id": "2301", "date": t, "workout_label": w,
                                **({"workout_duration": m} if m is not None else {})}
    uom = [row(f"2023-10-01 10:{m:02d}:00", "Walking", "15") for m in (0, 15, 30, 45)] + \
        [row("2023-10-01 13:30:00", "Walking", "15")]
    every = events(raw={"type": "label", "rows": uom})
    got = [(e["input"]["start"], e["input"]["end"], e["input"]["total"]) for e in every]
    assert got == [("2023-10-01 10:00", "2023-10-01 11:00", {"minutes": 60}),
                   ("2023-10-01 13:30", "2023-10-01 13:45", {"minutes": 15})], got
    assert all("id" not in r for e in every for r in e["raw"].get("rows", [])) and every[0]["raw"]["rows_sent"] == 5
    bris = [row(f"2023-06-05 08:{m:02d}:00", "Walk") for m in range(5, 35, 5)]
    ev = event(raw={"type": "label", "rows": bris})
    assert ev["input"]["total"] == {"minutes": 30} and "6 pieces" in ev["step"], ev["step"]
    assert all("id" not in r for r in ev["raw"]["rows"])
    loop = event(raw={"type": "label", "rows": [row("2019-10-31 17:25:00", "Running", "29")]})
    (h, b), = loop["output"].items()
    assert b["total"]["minutes"] == 29 and b["items"][0]["met"] is not None, b
    zero = event(raw={"type": "label", "rows": [row("2019-10-31 17:25:00", "Running", "0")]})
    assert zero["input"]["end"] is None and zero["input"]["total"] is None, zero["input"]
    return (f"T1D-UOM's 4 pieces one 60-minute walk; BrisT1D's 6 words 30 minutes; Loop's Running 29 minutes, MET "
            f"{b['items'][0]['met']}; a 0 not given")


if __name__ == "__main__":
    print("eventnorm.exercise")
    for name, fn in (("each hour its own part", t_hours_add_up), ("words to an event", t_words),
                     ("two activities, two workouts", t_words_then),
                     ("a day total is no event", t_day_total), ("a 0 duration is not given", t_zero_minutes), ("what is refused", t_refusals),
                     ("s02's examples", t_examples), ("a wearable file finds its type", t_wearable),
                     ("every workout of a stream", t_every_workout), ("a study's workout labels", t_labels)):
        check(name, fn)
    print(f"{len(PASS)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)

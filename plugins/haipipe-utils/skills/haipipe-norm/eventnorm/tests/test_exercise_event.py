"""
Checks for eventnorm.exercise. The hours, the words and the errors need nothing; the examples need the SPACE's tables
and s02's files.

    python skills/haipipe-norm/eventnorm/tests/test_exercise_event.py

THE EXAMPLES. b51 s02 ③ and ④'s events (studio/s02-exercise-api/assets/exercise-events-every-kind.json and
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
from eventnorm.exercise import event, exercise_hours            # noqa: E402

S02 = "examples-1-data/Proj01-CGM-RawData/work/b51_externalstore/studio/s02-exercise-api/assets/"
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


if __name__ == "__main__":
    print("eventnorm.exercise")
    for name, fn in (("each hour its own part", t_hours_add_up), ("words to an event", t_words),
                     ("a day total is no event", t_day_total), ("what is refused", t_refusals),
                     ("s02's examples", t_examples), ("a wearable file finds its type", t_wearable)):
        check(name, fn)
    print(f"{len(PASS)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)

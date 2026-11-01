"""
Checks for eventnorm.step. The hours, the kinds, a stream and the errors need nothing; the examples need s05's files.

    python skills/haipipe-norm/eventnorm/tests/test_step_event.py

THE EXAMPLES. b51 s05 ② and ③'s events (s05-step-api/assets/step-event-hour.json and
step-events-every-kind.json, written by its drawing builder, where this logic ran first) are sent raw, and the input
and output must come back as those files hold them. The files are read in place, never copied here: their rows are a
cohort's. With no such files on this host, the examples are skipped and say so.

Same shape as test_exercise_event.py: PASS/FAIL lines, exit 1 on any FAIL.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))                       # skills/haipipe-norm, so `eventnorm` imports
from eventnorm.step import event, events, kind, span_hours      # noqa: E402

S05 = "examples-1-data/Proj01-CGM-RawData/work/b51_externalstore/s05-step-api/assets/"
FILES = ("step-event-hour.json", "step-events-every-kind.json")
PASS, FAIL = [], []


def check(name, fn):
    try:
        note = fn()
        PASS.append(name)
        print(f"  PASS  {name}" + (f"  ({note})" if note else ""))
    except Exception as e:
        FAIL.append(name)
        print(f"  FAIL  {name}: {type(e).__name__}: {e}")


def t_shares():
    """s05-D02: 16:56:22 to 17:24:41 is shared to the second, 12.83% and 87.17%, not 4 and 24 whole minutes."""
    import pandas as pd
    out = span_hours(pd.Timestamp("2022-06-29 16:56:22"), pd.Timestamp("2022-06-29 17:24:41"), "-05:00")
    want = {"2022-06-29 16:00 -05:00": (0.1283, 3.6), "2022-06-29 17:00 -05:00": (0.8717, 24.7)}
    assert out == want, out
    return "0.1283 and 0.8717; 3.6 and 24.7 minutes"


def t_kinds():
    """A row's kind by how long it is: a 23-hour clock-change day (1,379.98 minutes) is a day."""
    got = [kind(m) for m in (1, 2, 2.1, 61, 61.1, 1378.9, 1379, 1379.98, 1440)]
    assert got == ["minute"] * 2 + ["hour"] * 2 + ["part_day"] * 2 + ["day"] * 3, got
    return "2 / 61 / 1,379 minutes"


def t_input_only():
    ev = event(input={"start": "2022-06-29 16:56 -05:00", "end": "2022-06-29 17:24 -05:00",
                      "total": {"steps": 128, "calories": -1}})
    assert ev["input"]["total"] == {"minutes": 28.0, "steps": 128}, ev["input"]
    got = {h: (b["share"], b["in_hour"]) for h, b in ev["output"].items()}
    assert got == {"2022-06-29 16:00 -05:00": (0.1429, {"minutes": 4.0, "steps": 18}),
                   "2022-06-29 17:00 -05:00": (0.8571, {"minutes": 24.0, "steps": 110})}, got
    day = event(input={"start": "2025-02-10 00:00 -06:00", "end": "2025-02-10 23:59 -06:00", "total": {"steps": 9000}})
    assert list(day["output"]) == ["2025-02-10"] and day["output"]["2025-02-10"]["share"] == 1.0, day["output"]
    return "a -1 left out; to the minute when sent by the minute; a day stays its day"


def t_refusals():
    for bad, words in (({}, "send"), ({"raw": {"type": "photo", "rows": [{}]}}, "raw.type"),
                       ({"input": {"start": "x", "end": "y"}}, "not a time"),
                       ({"input": {"start": "2022-06-29 16:56", "end": "2022-06-29 16:00"}}, "before"),
                       ({"input": {"start": "2022-06-29 16:56", "end": "2022-06-29 17:00", "items": [{}]}}, "null")):
        try:
            event(**bad)
        except ValueError as e:
            assert words in str(e), (bad, e)
            continue
        raise AssertionError(f"{bad} was not refused")
    return "no body, an unknown type, no time, an end before its start, items"


def stream_rows():
    """Two hours of one-minute samples: a quiet hour, then 12 brisk minutes (110 a minute) at 09:20, the 09:25
    minute also sent again with 0 (a repeat, as mcPhases 2024 sends)."""
    rows = [{"date": f"2024-03-0{d} {h:02d}:{m:02d}:00", "steps": "0"} for d, h in ((5, 8),) for m in range(60)]
    rows += [{"date": f"2024-03-05 09:{m:02d}:00", "steps": "110" if 20 <= m < 32 else "3"} for m in range(60)]
    return rows + [{"date": "2024-03-05 09:25:00", "steps": "0"}]


def t_stream():
    ev = event(raw={"type": "steps_stream", "rows": stream_rows(), "zone": "-05:00", "device": "test"})
    assert "1 repeated time" in ev["step"] and ev["input"]["device"] == "test", ev["step"]
    assert ev["walks"] == [{"start": "2024-03-05 09:20 -05:00", "end": "2024-03-05 09:32 -05:00", "minutes": 12.0,
                            "steps": 1320, "spm": 110.0, "to": "POST /exercise/event"}], ev["walks"]
    h8, h9 = ev["output"]["2024-03-05 08:00 -05:00"]["total"], ev["output"]["2024-03-05 09:00 -05:00"]["total"]
    assert h8 == {"minutes": 60.0, "steps": 0, "moving_minutes": 0.0}, h8
    assert h9 == {"minutes": 60.0, "steps": 1320 + 48 * 3, "moving_minutes": 60.0}, h9
    assert h8["steps"] + h9["steps"] == ev["input"]["total"]["steps"] and len(ev["input"]["timeline"]) == 120
    return "the repeat kept at 110; one walk 09:20 to 09:32; the hours add up"


def t_same_walk_as_exercise():
    """The walk this finds is the workout POST /exercise/event finds in the same stream: one rule, runs_of."""
    from eventnorm.exercise import event as exercise_event
    rows = [r for r in stream_rows()[:-1]]
    walk = event(raw={"type": "steps_stream", "rows": rows})["walks"][0]
    ex = exercise_event(raw={"type": "steps_stream", "rows": rows})["input"]
    assert (ex["start"], ex["end"]) == (walk["start"], walk["end"]), (ex["start"], ex["end"], walk)
    return f"{walk['start']} to {walk['end']} in both"


def t_log_rows():
    rows = [{"StartDateTime": "6/29/2022 9:56:22 PM", "EndDateTime": "6/29/2022 10:24:41 PM",
             "TimezoneOffset": "-300", "NumberOfSteps": "128", "EntrySourceID": "40", "PatientID": "x"}] * 2
    every = events(raw={"type": "log", "rows": rows})
    assert len(every) == 2 and all("PatientID" not in r for e in every for r in e["raw"]["rows"])
    try:
        event(raw={"type": "log", "rows": rows})
    except ValueError as e:
        assert "one row an event" in str(e)
    else:
        raise AssertionError("two rows sent to event() were not refused")
    return "events() one a row; event() refuses two; whose row never shown"


def space():
    """The SPACE holding s05: above this file, else the folder it is run from or above (Tools/ is often a link)."""
    cwd = Path.cwd().resolve()
    return next((p for p in [*HERE.parents, cwd, *cwd.parents] if (p / "env.sh").is_file() and (p / S05).is_dir()),
                None)


def t_examples():
    root = space()
    if root is None:
        return "skipped: no s05 files on this host"
    n = 0
    for f in FILES:
        d = json.loads((root / S05 / f).read_text())
        for ex in d.get("events") or [d]:
            ev = event(raw={"type": "log", "rows": ex["raw"]["rows"]})
            assert ev["input"] == ex["input"], (f, ex["raw"]["type"], ev["input"], ex["input"])
            assert ev["output"] == ex["output"], (f, ex["raw"]["type"])
            n += 1
    return f"{n} s05 rows (a minute, an hour, part of a day, a day): input and output as drawn"


if __name__ == "__main__":
    print("eventnorm.step")
    for name, fn in (("shares to the second", t_shares), ("kinds by length", t_kinds),
                     ("an input made elsewhere", t_input_only), ("what is refused", t_refusals),
                     ("a stream: repeats, walks, hours", t_stream), ("the same walk as exercise", t_same_walk_as_exercise),
                     ("logged rows", t_log_rows), ("s05's examples", t_examples)):
        check(name, fn)
    print(f"{len(PASS)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)

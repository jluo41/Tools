"""
Checks for eventnorm.sleep. The hours, an input alone and the errors need nothing; the examples need s06's files.

    python skills/haipipe-norm/eventnorm/tests/test_sleep_event.py

THE EXAMPLES. b51 s06 ② and ③'s nights (s06-sleep-api/assets/sleep-event-night.json and
sleep-events-every-kind.json, written by its drawing builder, where this logic ran first) are sent raw, and the input
and output must come back as those files hold them. The files are read in place, never copied here: their rows are a
cohort's. With no such files on this host, the examples are skipped and say so.

Same shape as test_step_event.py: PASS/FAIL lines, exit 1 on any FAIL.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))                       # skills/haipipe-norm, so `eventnorm` imports
from eventnorm.sleep import event, minutes_by_hour             # noqa: E402

S06 = "examples-1-data/Proj01-CGM-RawData/work/b51_externalstore/s06-sleep-api/assets/"
PASS, FAIL = [], []


def check(name, fn):
    try:
        note = fn()
        PASS.append(name)
        print(f"  PASS  {name}" + (f"  ({note})" if note else ""))
    except Exception as e:
        FAIL.append(name)
        print(f"  FAIL  {name}: {type(e).__name__}: {e}")


def t_by_hour():
    """JL 261027: asleep 02:30 to 05:30 counts in 02, 03, 04 and 05; a few seconds past an hour is no hour."""
    import pandas as pd
    out = minutes_by_hour([(pd.Timestamp("2023-01-23 02:30"), pd.Timestamp("2023-01-23 05:30"))], "-05:00")
    assert out == {"2023-01-23 02:00 -05:00": 30.0, "2023-01-23 03:00 -05:00": 60.0,
                   "2023-01-23 04:00 -05:00": 60.0, "2023-01-23 05:00 -05:00": 30.0}, out
    out = minutes_by_hour([(pd.Timestamp("2023-01-23 05:00"), pd.Timestamp("2023-01-23 06:00:02"))], "")
    assert list(out) == ["2023-01-23 05:00"], out


def t_input_alone():
    """An input with a timeline: in bed 02:00 to 06:00, asleep 02:30 to 05:30; across midnight works too."""
    ev = event(input={"start": "2023-01-23 02:00 -05:00", "end": "2023-01-23 06:00 -05:00",
                      "timeline": [{"from": "02:30", "to": "05:30", "state": "asleep"}]})
    assert ev["input"]["total"] == {"in_bed_min": 240.0, "asleep_min": 180.0, "awake_in_bed_min": 60.0}, ev["input"]
    assert ev["output"]["2023-01-23 02:00 -05:00"] == {"in_bed_min": 60.0, "asleep_min": 30.0, "awake_in_bed_min": 30.0}
    ev = event(input={"start": "2023-01-22 23:00", "end": "2023-01-23 01:00",
                      "timeline": [{"from": "23:30", "to": "00:30"}]})
    assert ev["input"]["total"]["asleep_min"] == 60.0, ev["input"]
    ev = event(input={"start": "2023-01-22 23:00", "end": "2023-01-23 01:00"})
    assert ev["input"]["total"] == {"in_bed_min": 120.0, "unknown_min": 120.0}, ev["input"]


def t_errors():
    for bad, word in [({}, "send"), ({"raw": {"type": "text", "rows": [{}]}}, "raw.type"),
                      ({"input": {"start": "2023-01-23 02:00", "end": "2023-01-23 01:00"}}, "after"),
                      ({"input": {"start": "2023-01-23 02:00", "end": "2023-01-23 03:00", "items": []}}, "items")]:
        try:
            event(**bad)
        except ValueError as e:
            assert word in str(e), (word, str(e))
        else:
            raise AssertionError(f"no error for {bad}")


def space():
    """The SPACE holding s06: above this file, else the folder it is run from or above (Tools/ is often a link)."""
    cwd = Path.cwd().resolve()
    return next((p for p in [*HERE.parents, cwd, *cwd.parents] if (p / "env.sh").is_file() and (p / S06).is_dir()),
                None)


def examples():
    root = space()
    f = root / S06 / "sleep-events-every-kind.json" if root else None
    if not f or not f.is_file():
        print("  SKIP  s06's examples: no s06-sleep-api/assets on this host")
        return
    night = json.loads((root / S06 / "sleep-event-night.json").read_text())
    cases = [("② night 80124", night)] + [(e["example"], e) for e in json.loads(f.read_text())["events"]]
    for name, want in cases:
        def one(want=want):
            raw = {"type": "log", "rows": want["raw"]["rows"], "pieces": want["raw"]["pieces"]}
            ev = event(raw=raw)
            assert ev["input"] == want["input"], (ev["input"], want["input"])
            assert ev["output"] == want["output"], (ev["output"], want["output"])
            return f"{len(ev['output'])} hours"
        check(f"s06 · {name}", one)


if __name__ == "__main__":
    check("by local hour, minutes", t_by_hour)
    check("an input alone", t_input_alone)
    check("errors name what is wrong", t_errors)
    examples()
    print(f"{len(PASS)} PASS, {len(FAIL)} FAIL")
    sys.exit(1 if FAIL else 0)

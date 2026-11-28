"""
Checks for eventnorm.stress. The levels, typed readings and the errors need nothing; the examples need AI-READI's
Garmin files and mcPhases' stress_score.csv.

    python skills/hai-norm/eventnorm/tests/test_stress_event.py

THE EXAMPLES. b51 s10's numbers. AI-READI person 1069, 2023-11-28 00:00 to 16:00 local (UTC minus 480 minutes): 960
minutes are 475 rest, 89 low, 78 medium, 14 high, 151 active and 153 unknown (148 not measured, 5 with no reading);
10:00 holds 38 scored minutes, mean 64.2. mcPhases id 1, 2022: day 61 is sent 4 times and is one score, 70 (higher is
calmer); day 51 is 4 rows of NO_DATA and has no score. The rows are read in place, never copied here: they are a
cohort's. With neither on this host, the examples are skipped and say so.

Same shape as test_still_event.py: PASS/FAIL lines, exit 1 on any FAIL.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))                       # skills/hai-norm, so `eventnorm` imports
from eventnorm.stress import event, level_of                    # noqa: E402

AIREADI = "_WorkSpace/0-RawDataStore/aireadi-v3/wearable_activity_monitor/stress/garmin_vivosmart5/1069/1069_stress.json"
MCPHASES = "_WorkSpace/0-RawDataStore/mcphases-v1/stress_score.csv"
PASS, FAIL = [], []


def check(name, fn):
    try:
        note = fn()
        PASS.append(name)
        print(f"  PASS  {name}" + (f"  ({note})" if note else ""))
    except Exception as e:
        FAIL.append(name)
        print(f"  FAIL  {name}: {type(e).__name__}: {e}")


def t_levels():
    """One minute, one level: Garmin's bands, -2 active, -1 and no reading unknown."""
    got = [level_of(v) for v in (0, 25, 26, 50, 51, 75, 76, 100, -2, -1, None)]
    assert got == [("rest", None)] * 2 + [("low", None)] * 2 + [("medium", None)] * 2 + [("high", None)] * 2 + \
        [("active", None), ("unknown", "not_measured"), ("unknown", "no_reading")], got
    return "rest, low, medium, high at their edges; active; two kinds of unknown"


def typed():
    rows = [{"time": f"2026-11-09 10:{m:02d}", "value": v} for m, v in ((0, 20), (1, 22), (2, 60), (3, -2), (4, -1), (6, 80))]
    return event(raw={"type": "readings", "rows": rows, "end": "2026-11-09 10:10"})


def t_typed():
    ev = typed()
    h = ev["output"]["2026-11-09 10:00"]
    six = [h[f"{k}_min"] for k in ("rest", "low", "medium", "high", "active", "unknown")]
    assert six == [2, 0, 1, 1, 1, 5] and sum(six) == h["minutes"] == 10, h
    assert h["unknown_why"] == {"not_measured": 1, "no_reading": 4} and (h["scored_min"], h["mean"]) == (4, 45.5), h
    first = ev["input"]["timeline"][0]
    assert (first["level"], first["minutes"], first["mean"]) == ("rest", 2, 21.0), first
    again = event(input={"timeline": ev["input"]["timeline"]})
    assert again["output"] == ev["output"], "the input's timeline answers the same"
    return "2 rest, 1 medium, 1 high, 1 active, 5 unknown; the input alone the same"


def t_utc():
    """A time ending in Z is UTC: raw.offset moves it to local; without one it stays UTC and the step says so."""
    rows = [{"stress": {"value": 74}, "effective_time_frame": {"date_time": "2023-11-27T20:28:03Z"}}]
    local = event(raw={"type": "readings", "offset": -480, "rows": rows})
    assert list(local["output"]) == ["2023-11-27 12:00"] and local["input"]["zone"] == "local", local["output"]
    utc = event(raw={"type": "readings", "rows": rows})
    assert list(utc["output"]) == ["2023-11-27 20:00"] and utc["input"]["zone"] == "UTC" and "UTC" in utc["step"]
    return "AI-READI's own row; 20:28 UTC is 12:28 at minus 480"


def t_errors():
    for bad, word in (({}, "send"), ({"raw": {"type": "x", "rows": [{}]}}, "raw.type"),
                      ({"raw": {"type": "readings", "rows": [{"time": "2026-11-09 10:00", "value": 140}]}}, "0 to 100"),
                      ({"input": {"start": "2026-11-09 10:00", "total": {}}}, "timeline"),
                      ({"input": {"timeline": [{"from": "2026-11-09 10:00", "to": "2026-11-09 10:05", "level": "high",
                                                "mean": 12}]}}, "band"),
                      ({"raw": {"type": "day_score", "rows": [{"day_in_study": "3"}, {"day_in_study": "4"}]}}, "one day")):
        try:
            event(**bad)
        except ValueError as e:
            assert word in str(e), e
        else:
            raise AssertionError(f"{bad} was accepted")
    return "6 refused"


def space(rel: str):
    import os
    for p in [HERE, *HERE.parents, Path(os.environ.get("SPACE_ROOT") or os.getcwd())]:
        if (p / rel).is_file():
            return p
    return None


def t_aireadi(root):
    rows = [r for r in json.loads((root / AIREADI).read_text())["body"]["stress"]
            if r["effective_time_frame"]["date_time"].startswith("2023-11-28")]
    ev = event(raw={"type": "readings", "offset": -480, "rows": rows, "start": "2023-11-28 00:00", "end": "2023-11-28 16:00"})
    o = ev["output"]
    add = lambda k: sum(h[k] for h in o.values())
    six = [add(f"{k}_min") for k in ("rest", "low", "medium", "high", "active", "unknown")]
    assert len(o) == 16 and add("minutes") == 960 and all(h["minutes"] == 60 for h in o.values())
    assert six == [475, 89, 78, 14, 151, 153], six
    assert sum(h["unknown_why"]["no_reading"] for h in o.values()) == 5
    h = o["2023-11-28 10:00"]
    assert (h["scored_min"], h["mean"], h["active_min"]) == (38, 64.2, 18), h
    assert sum(s["minutes"] for s in ev["input"]["timeline"]) == 960
    return f"960 minutes: {six[0]} rest, {six[4]} active, {six[5]} unknown; {len(ev['input']['timeline'])} stretches"


def mc_rows(root: Path, day: int) -> list:
    f = root / MCPHASES
    head = f.open().readline().strip().split(",")
    out = subprocess.run(["grep", "-E", f"^1,2022,[A-Za-z]*,{day},", str(f)], capture_output=True, text=True).stdout
    return [dict(zip(head, ln.split(","))) for ln in out.splitlines()]


def t_mcphases(root):
    ev = event(raw={"type": "day_score", "rows": mc_rows(root, 61)})
    d = ev["output"]["day 61"]
    assert (d["grain"], d["score"], d["sleep"], d["exertion"]) == ("day", 70, "24 of 30", "26 of 40"), d
    assert "calmer" in d["direction"] and "3 of them copies" in ev["step"], ev["step"]
    none = event(raw={"type": "day_score", "rows": mc_rows(root, 51)})
    assert none["output"] is None and none["input"]["total"] is None and "NO_DATA" in none["step"], none["step"]
    return "day 61: 4 rows, one score 70; day 51: NO_DATA, no score"


if __name__ == "__main__":
    print("eventnorm.stress")
    check("one minute, one level", t_levels)
    check("typed readings, and the input alone", t_typed)
    check("a UTC time and its offset", t_utc)
    check("refused with a reason", t_errors)
    root = space(AIREADI)
    if root:
        check("s10: AI-READI 1069, 2023-11-28, 16 hours", lambda: t_aireadi(root))
    else:
        print("  SKIP  the AI-READI example: no aireadi-v3 stress files on this host")
    root = space(MCPHASES)
    if root:
        check("s10: mcPhases id 1, day 61 and day 51", lambda: t_mcphases(root))
    else:
        print("  SKIP  the mcPhases example: no mcphases-v1 on this host")
    print(f"{len(PASS)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)

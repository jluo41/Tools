"""
Checks for eventnorm.still. The rule, typed minutes and the errors need nothing; the examples need mcPhases' files.

    python skills/haipipe-norm/eventnorm/tests/test_still_event.py

THE EXAMPLES. b51 s07 ② and ④'s numbers, made by its drawing builder (studio/_build/topic_frames.py mc_day and
still_hour_counts, where this logic ran first), on mcPhases id 1, 2022, day 3: the whole day is 502 asleep and 280
unknown (252 with no heart rate, 28 restless in bed); 10:00 is worn all 60 minutes with 0 steps in its 4 step rows.
The rows are read in place by grep, never copied here: they are a cohort's. With no mcPhases on this host, the
examples are skipped and say so.

Same shape as test_step_event.py: PASS/FAIL lines, exit 1 on any FAIL.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))                       # skills/haipipe-norm, so `eventnorm` imports
from eventnorm.still import event, way                          # noqa: E402

MCPHASES = "_WorkSpace/0-RawDataStore/mcphases-v1"
PASS, FAIL = [], []


def check(name, fn):
    try:
        note = fn()
        PASS.append(name)
        print(f"  PASS  {name}" + (f"  ({note})" if note else ""))
    except Exception as e:
        FAIL.append(name)
        print(f"  FAIL  {name}: {type(e).__name__}: {e}")


def t_way():
    """s07-D02: one minute, one way."""
    got = [way(p, 0) for p in ({"level": "deep"}, {"level": "restless"}, {"level": "wake"}, {"steps": 12, "worn": False},
                                {"steps": 0, "worn": True}, {"steps": None, "worn": True}, {"steps": None, "worn": False})]
    assert got == [("asleep", None), ("unknown", "restless"), ("still", None), ("moving", None), ("still", None),
                   ("still", None), ("unknown", "no_heart_rate")], got
    assert way({"steps": 12, "worn": True}, 20) == ("still", None)
    return "asleep, restless, awake in bed, a step, worn, no heart rate"


def t_typed():
    ev = event(raw={"type": "minutes", "day": "2026-10-27", "rows": [
        {"from": "10:00", "to": "10:40", "bpm": 72, "steps": 0}, {"from": "10:40", "to": "10:50", "bpm": 95, "steps": 80},
        {"from": "10:50", "to": "11:00"}]})
    h = ev["output"]["2026-10-27 10:00"]
    assert (h["still_min"], h["moving_min"], h["unknown_min"], h["asleep_min"]) == (40, 10, 10, 0), h
    assert h["minutes"] == 60 and ev["input"]["total"]["hr_min"] == 50, ev["input"]["total"]
    again = event(input={"timeline": ev["input"]["timeline"]})
    assert again["output"] == ev["output"], "the input's timeline answers the same"
    return "40 still, 10 moving, 10 unknown; the input alone the same"


def t_errors():
    for bad, word in (({}, "send"), ({"raw": {"type": "x", "rows": [{}]}}, "raw.type"),
                      ({"input": {"start": "day 3 10:00", "total": {}}}, "timeline"),
                      ({"raw": {"type": "minutes", "rows": [{"time": "10:00"}]}}, "no day")):
        try:
            event(**bad)
        except ValueError as e:
            assert word in str(e), e
        else:
            raise AssertionError(f"{bad} was accepted")
    return "4 refused"


def space() -> Path:
    for p in [HERE, *HERE.parents]:
        if (p / "env.sh").is_file() and (p / MCPHASES).is_dir():
            return p
    import os
    s = os.environ.get("SPACE_ROOT") or os.getcwd()
    return Path(s) if (Path(s) / MCPHASES).is_dir() else None


def mc_rows(root: Path, f: str, pattern: str) -> list:
    head = (root / MCPHASES / f).open().readline().strip().split(",")
    out = subprocess.run(["grep", "-E", pattern, str(root / MCPHASES / f)], capture_output=True, text=True).stdout
    return [{"file": f, **dict(zip(head, ln.split(",")))} for ln in out.splitlines()]


def day3(root: Path, start: str, end: str):
    import pandas as pd
    pre = "^1,2022,[A-Za-z]*,3,"
    sl = pd.read_csv(root / MCPHASES / "sleep.csv")
    sl = sl[(sl["id"] == 1) & (sl["study_interval"] == 2022) &
            ((sl["sleep_start_day_in_study"] == 3) | (sl["sleep_end_day_in_study"] == 3))]
    sleep = [{"file": "sleep.csv", **{k: str(v) for k, v in r.items()}} for r in sl.to_dict("records")]
    rows = mc_rows(root, "steps.csv", pre) + mc_rows(root, "heart_rate.csv", pre) + sleep
    return event(raw={"type": "mcphases", "start": start, "end": end, "rows": rows})


def t_day3(root):
    ev = day3(root, "day 3 00:00", "day 4 00:00")
    o = ev["output"]
    add = lambda k: sum(h[k] for h in o.values())
    why = lambda k: sum(h["unknown_why"][k] for h in o.values())
    assert len(o) == 24 and add("minutes") == 1440
    assert (add("asleep_min"), add("unknown_min"), why("no_heart_rate"), why("restless")) == (502, 280, 252, 28), \
        (add("asleep_min"), add("unknown_min"), why("no_heart_rate"), why("restless"))
    assert add("moving_min") + add("still_min") == 658
    return f"502 asleep, 280 unknown; {add('moving_min')} moving and {add('still_min')} still by the 0-step rule"


def t_hour10(root):
    ev = day3(root, "day 3 10:00", "day 3 11:00")
    h = ev["output"]["day 3 10:00"]
    assert ev["input"]["total"]["step_rows"] == 4 and ev["input"]["total"]["hr_min"] == 60, ev["input"]["total"]
    assert (h["still_min"], h["still_no_step_row"], h["unknown_min"]) == (60, 56, 0), h
    return "60 still, 56 of them with no step row"


if __name__ == "__main__":
    print("eventnorm.still")
    check("one minute, one way", t_way)
    check("typed minutes, and the input alone", t_typed)
    check("refused with a reason", t_errors)
    root = space()
    if root:
        check("s07 ④: mcPhases day 3, the whole day", lambda: t_day3(root))
        check("s07 ②: mcPhases day 3, 10:00", lambda: t_hour10(root))
    else:
        print(f"  SKIP  the mcPhases examples: no {MCPHASES} on this host")
    print(f"{len(PASS)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)

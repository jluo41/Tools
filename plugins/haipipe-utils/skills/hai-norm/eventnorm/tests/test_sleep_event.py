"""
Checks for eventnorm.sleep. The hours, an input alone and the errors need nothing; the examples need s06's files.

    python skills/hai-norm/eventnorm/tests/test_sleep_event.py

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
sys.path.insert(0, str(HERE.parents[1]))                       # skills/hai-norm, so `eventnorm` imports
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


def t_cut():
    """nights.cut: a repeat once; the longest is the night and overlapping rows its pieces; Apple's rows with no whole
    row joined when within an hour, and only then."""
    import pandas as pd
    from eventnorm.sleep import cut
    T = lambda h, m=0: pd.Timestamp("2024-01-01") + pd.Timedelta(hours=h, minutes=m)
    g = cut([("a", T(23), T(30)), ("b", T(23), T(30)), ("p1", T(24), T(25)), ("p2", T(26), T(27))])
    assert len(g) == 1 and g[0]["how"] == "whole_row" and g[0]["night"] == "a" and g[0]["pieces"] == ["p1", "p2"], g
    assert g[0]["dropped"] == ["b"], g
    rows = [("x1", T(1), T(1, 10)), ("x2", T(1, 12), T(1, 40)), ("x3", T(2, 20), T(2, 30)), ("y", T(9), T(9, 5))]
    g = cut(rows, join=True)
    assert [(x["how"], x["rows"]) for x in g] == [("joined", ["x1", "x2", "x3"]), ("alone", ["y"])], g
    g = cut(rows)                                                  # a device that writes no pieces: each row alone
    assert [x["how"] for x in g] == ["alone"] * 4, g
    return "a repeat once; pieces in their night; 3 rows joined, the fourth 6.5 hours later alone"


def t_other_device():
    """A row of another device inside a night is not its piece (b01: 6 of 38 pieces were folded across devices)."""
    from eventnorm.sleep import nights
    row = lambda i, src, s, e: {"SleepEntryID": i, "EntrySourceID": src, "StartDateTime": s, "EndDateTime": e,
                                "TimezoneOffset": "0"}
    g = nights([row("1", "1", "1/1/2024 11:00:00 PM", "1/2/2024 6:00:00 AM"),
                row("2", "23", "1/2/2024 1:00:00 AM", "1/2/2024 2:00:00 AM")])
    assert [(x["source"], x["how"], x["rows"]) for x in g] == [("1", "alone", ["1"]), ("23", "alone", ["2"])], g
    return "two devices, two events"


def t_joined_event():
    """Pieces with no whole row, sent with join: one night from the first start to the last end."""
    row = lambda i, s, e: {"SleepEntryID": i, "EntrySourceID": "20", "StartDateTime": s, "EndDateTime": e,
                           "TimezoneOffset": "-300"}
    ev = event(raw={"type": "log", "join": True, "rows": [row("1", "1/2/2024 6:00:00 AM", "1/2/2024 6:10:00 AM"),
                                                          row("2", "1/2/2024 6:20:00 AM", "1/2/2024 7:00:00 AM")]})
    assert ev["input"]["total"] == {"in_bed_min": 60.0, "asleep_min": 50.0, "awake_in_bed_min": 10.0}, ev["input"]
    assert ev["input"]["start"] == "2024-01-02 01:00 -05:00" and len(ev["input"]["timeline"]) == 2, ev["input"]
    return "60 minutes in bed, 50 asleep, 10 awake"


ALS = "_WorkSpace/0-RawDataStore/WellDoc2025ALS/Source/02_19_2025_SleepEntry.csv"


def als_examples():
    """b01's three findings on WellDoc2025ALS, on its own rows (read in place; counts only are printed)."""
    import csv
    from eventnorm.sleep import nights
    cwd = Path.cwd().resolve()
    root = next((p for p in [*HERE.parents, cwd, *cwd.parents] if (p / ALS).is_file()), None)
    if not root:
        print("  SKIP  b01's ALS findings: no WellDoc2025ALS SleepEntry file on this host")
        return
    rows = list(csv.DictReader(open(root / ALS, encoding="utf-8-sig")))
    who = {r["SleepEntryID"]: r["PatientID"] for r in rows}
    of = lambda i: nights([r for r in rows if r["PatientID"] == who[i]])
    find = lambda gs, i: next(g for g in gs if i in g["rows"] or i in g["dropped"])

    def dup():
        g = find(of("123026"), "123026")
        assert sorted(g["rows"] + g["dropped"]) == ["123026", "123053"] and len(g["dropped"]) == 1, g
        return "123026 and 123053 are one event, one of them dropped"

    def other():
        gs = of("56795")
        a, b = find(gs, "56795"), find(gs, "56782")
        assert a is not b and "56782" not in a["pieces"] and a["source"] != b["source"], (a, b)
        return "night 56795 (device 1) does not take 56782 (device 23)"

    def orphan():
        gs = of("54154")
        hows = [find(gs, i)["how"] for i in ("54154", "54657", "54894")]
        assert all(h in ("joined", "alone") for h in hows), hows
        n = sum(g["how"] == "joined" for g in gs)
        return f"54154, 54657, 54894: {', '.join(hows)}; this person has {n} joined nights"

    check("ALS: a row sent again is one event", dup)
    check("ALS: a piece stays with its own device", other)
    check("ALS: Apple's short rows with no night", orphan)


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
    check("one person's rows cut into nights", t_cut)
    check("another device's row is no piece", t_other_device)
    check("pieces with no whole row, joined", t_joined_event)
    examples()
    als_examples()
    print(f"{len(PASS)} PASS, {len(FAIL)} FAIL")
    sys.exit(1 if FAIL else 0)

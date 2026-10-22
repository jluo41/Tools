"""
Checks for eventnorm. The hours and the errors need nothing; the eight meals need the SPACE's tables and s01's file.

    python skills/haipipe-norm/eventnorm/tests/test_eventnorm.py

THE EIGHT. b51 s01 ③'s meals (studio/s01-food-api/assets/food-events-all.json, written by its drawing builder, where
this logic ran first) are sent raw, and the input and output must come back as that file holds them, byte for byte,
but for the differences named in KNOWN, each with its reason. The file is read in place, never copied here: its rows
are a cohort's. With no such file on this host, the eight are skipped and say so.

Same shape as the host's tests: PASS/FAIL lines, exit 1 on any FAIL.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))                       # skills/haipipe-norm, so `eventnorm` imports
from eventnorm import event, hour_shares, by_hour             # noqa: E402

S01 = "examples-1-data/Proj01-CGM-RawData/work/b51_externalstore/studio/s01-food-api/assets/food-events-all.json"
KNOWN = {}  # (the meal's example, the field) -> why the API differs from s01's file. Empty since s01 runs eventnorm
#            itself (261021): the photo's Sugar, once the one entry, is now live in s01's file too
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
    """The fields where a and b differ, by path; NaN in s01's file is read as null (JSON has no NaN)."""
    nan = lambda v: v is None or (isinstance(v, float) and math.isnan(v))
    if nan(a) and nan(b):
        return []
    if isinstance(a, dict) and isinstance(b, dict):
        out = [f"{p}: keys {list(a)} vs {list(b)}"] if list(a) != list(b) else []
        return out + sum((diff(a[k], b[k], f"{p}.{k}".lstrip(".")) for k in a if k in b), [])
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [f"{p}: {len(a)} vs {len(b)}"]
        return sum((diff(x, y, f"{p}[{i}]") for i, (x, y) in enumerate(zip(a, b))), [])
    return [] if a == b else [p]


def t_hours():
    got = hour_shares("2021-04-14 10:30 -04:00", "2021-04-14 12:30 -04:00")
    want = {"2021-04-14 10:00 -04:00": 0.25, "2021-04-14 11:00 -04:00": 0.5, "2021-04-14 12:00 -04:00": 0.25}
    assert got == want, got
    assert hour_shares("2021-04-14 07:17 -04:00") == {"2021-04-14 07:00 -04:00": 1.0}
    return "start and end by minutes; start only, all in its hour"


def t_bites():
    """s01 ④'s breakfast: seven bites, shared by their carbs (text with a unit, as the timeline writes them)."""
    carbs = ["0.60 g", "8.20 g", "0.00 g", "7.18 g", "0.81 g", "14.18 g", "2.40 g"]
    at = ["07:17:20", "07:26:00", "07:34:30", "07:43:00", "07:51:30", "07:58:40", "08:05:10"]
    out = by_hour({"start": "2021-04-14 07:17 -04:00", "end": "2021-04-14 08:05 -04:00",
                   "timeline": [{"at": a, "carbs": c} for a, c in zip(at, carbs)]}, "carbs")
    shares = {h: v["share"] for h, v in out.items()}
    assert shares == {"2021-04-14 07:00 -04:00": 0.9281, "2021-04-14 08:00 -04:00": 0.0719}, shares
    return "0.9281 and 0.0719, as ④ draws them"


def t_errors():
    for bad, word in (({}, "send"), ({"raw": {"type": "fax", "rows": [{}]}}, "not one of"),
                      ({"raw": {"type": "app_log", "rows": []}}, "rows"),
                      ({"raw": {"type": "app_log", "rows": [{"x": "1"}]}}, "no shape"),
                      ({"input": {"items": [{"amount": "1 g"}]}}, "input.items"),
                      ({"input": {"start": "2020-05-01 20:41", "source": {"kind": "guess"}}}, "input.source")):
        try:
            event(**bad)
        except ValueError as e:
            assert word in str(e), (bad, str(e))
        else:
            raise AssertionError(f"{bad} was taken")
    return "six bad requests, each told what is wrong"


def t_typed():
    ev = event(raw={"type": "text", "rows": [{"text": "Banana\nMilk 250 ml", "time": "2026-10-21 08:05 -04:00"}]})
    assert [it["food"] for it in ev["input"]["items"]] == ["Banana", "Milk"], ev["input"]["items"]
    assert ev["input"]["items"][1]["amount"] == "250 ml"
    (hour, h), = ev["output"].items()
    assert hour == "2026-10-21 08:00 -04:00" and h["share"] == 1.0 and h["total"]["source"] == "tables"
    none = event(input={"items": [{"food": "Banana"}]})
    assert list(none["output"]) == ["no time"], list(none["output"])
    carbs = [it["macros"]["carbs"] for it in h["items"]]
    assert h["total"]["macros"]["carbs"] == "39.02 g" and h["total"]["coverage"] == 1.0, h["total"]   # 26.95 + 12.07,
    #   the items' sum (261022); the meal asked as one string gave the milk's 12.07 g alone
    assert h["source"] == {"kind": "logged"}, h["source"]
    return f"typed lines become items {carbs}; total {h['total']['macros']['carbs']}; no time is one entry"


def t_detected():
    src = {"kind": "detected", "rule": "glucose_rise", "rise": "52 mg/dL", "peak": "21:20", "found_at": "21:05"}
    ev = event(input={"start": "2020-05-01 20:41", "source": src})
    (hour, h), = ev["output"].items()
    assert list(h)[-1] == "source" and h["source"] == src, h
    assert h["items"] is None and h["total"] is None, h
    return "a meal a rule found: its start and its source, no items, no total"


def run_eight():
    from paths import space_root                                # skills/haipipe-norm/paths.py
    try:
        f = space_root() / S01
    except RuntimeError:
        f = None
    if not f or not f.is_file():
        print(f"  SKIP  the eight meals: no {S01} on this host")
        return
    meals = json.loads(f.read_text(encoding="utf-8"))["meals"]
    for m in meals:
        def one(m=m):
            give = {"items": m["input"]["items"]} if m["raw"]["type"] == "photo" else None   # the photo API's names
            ev = event(raw=m["raw"], input=give)
            json.dumps(ev, allow_nan=False)                     # strict JSON: no NaN on the wire
            found = diff(ev["input"], m["input"], "input") + diff(ev["output"], m["output"], "output")
            new = [p for p in found if (m["example"], p) not in KNOWN]
            assert not new, new
            known = [KNOWN[(m["example"], p)] for p in found]
            return f"{m['raw']['type']}: same" + (f", but {len(known)} known: {known[0]}" if known else "")
        check(f"s01 ③ · {m['example']}", one)


if __name__ == "__main__":
    check("hour shares", t_hours)
    check("bites share an hour by their carbs", t_bites)
    check("bad requests", t_errors)
    check("typed text and no time", t_typed)
    check("a detected meal", t_detected)
    run_eight()
    print(f"{len(PASS)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)

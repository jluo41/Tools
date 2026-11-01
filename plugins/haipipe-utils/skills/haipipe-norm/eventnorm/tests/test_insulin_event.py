"""
Checks for eventnorm.insulin. The errors need nothing; the rest need the SPACE's tables (describe-medication's and
describe-insulin's, pinned by the release), s04's file and ext_insulin_event. Run from the SPACE root after env.sh:

    python Tools/plugins/haipipe-utils/skills/haipipe-norm/eventnorm/tests/test_insulin_event.py

THE EXAMPLE. b51 s04's Lyumjev dose (s04-insulin-api/assets/insulin-events-every-kind.json, written by its
drawing builder) is sent raw, and its hours and shares must come back as that file holds them. THE PARITY. Rows of
ext_insulin_event (j04 t03), a few of every cohort, curve and delivery, are sent their input JSON (a basal with the end
the freeze found for it), and the output must equal the frozen one; a basal cut by a temporary basal inside it is
counted apart (only its file shows the cut), and a rate with no end may differ only in its note.

Same shape as food's test_eventnorm.py: PASS/FAIL lines, exit 1 on any FAIL.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))                       # skills/haipipe-norm, so `eventnorm` imports
from eventnorm.insulin import event                             # noqa: E402

S04 = Path("examples-1-data/Proj01-CGM-RawData/work/b51_externalstore/s04-insulin-api/assets")
FROZEN = Path("_WorkSpace/ExternalStore/ext_insulin_event/S20261027/df_ext_insulin_event.parquet")
PASS, FAIL = [], []


def check(name, fn):
    try:
        note = fn()
        PASS.append(name)
        print(f"  PASS  {name}" + (f"  ({note})" if note else ""))
    except Exception as e:
        FAIL.append(name)
        print(f"  FAIL  {name}: {type(e).__name__}: {e}")


def t_errors():
    for bad in ({}, {"raw": {"type": "photo", "rows": [{}]}}, {"input": {"items": [{"dose": 5}]}}):
        try:
            event(**bad)
        except ValueError:
            continue
        raise AssertionError(f"no error for {bad}")


def t_s04_dose():
    f = S04 / "insulin-events-every-kind.json"
    if not f.exists():
        return "skipped: no s04 file on this host"
    want = next(e for e in json.loads(f.read_text())["events"] if e["raw"]["rows"][0].get("MeterType") == "1")
    ev = event(raw={"type": "app_id", "rows": want["raw"]["rows"]})
    got = {h: v["share"] for h, v in ev["output"].items()}
    exp = {h: v["share"] for h, v in want["output"].items()}
    assert got == exp, (got, exp)
    return f"{len(got)} hours, shares {list(got.values())}"


def t_rate_and_none():
    ev = event(raw={"type": "pump", "rows": [{"Date": "2021-05-21 16:21:00", "胰岛素泵基础量 (Novolin R, IU / H)": "0.6"}]})
    (h, blk), = ev["output"].items()
    assert blk["units"] is None and blk["share"] == 1.0 and blk["note"], blk
    ev = event(raw={"type": "pump", "rows": [{"Date": "2021-05-21 16:21:00", "胰岛素泵基础量 (Novolin R, IU / H)": "0.6"}]},
               input={"end": "2021-05-21 19:00 +08:00"})
    assert len(ev["output"]) == 3 and abs(sum(v["units"] for v in ev["output"].values()) - 0.6 * 159 / 60) < 1e-3
    ev = event(raw={"type": "app_id", "rows": [{"MedicationID": "241223", "Dose": "1",
                                                "AdministrationDate": "4/14/2023 4:34:00 AM",
                                                "AdministrationTimeZoneOffset": "-240"}]})
    assert ev["output"] is None, ev["step"]
    return "a rate alone stays in its hour; with its end, by minutes; a pill has no insulin event"


def t_parity_frozen():
    import pandas as pd
    if not FROZEN.exists():
        return "skipped: no ext_insulin_event on this host"
    t = pd.read_parquet(FROZEN)
    s = t.groupby(["cohort", "curve", "delivery"], dropna=False).head(15)
    n, cut, bad = 0, 0, []
    for r in s.to_dict("records"):
        inp, frozen = json.loads(r["input_json"]), json.loads(r["output_json"])
        if r["is_rate"] and r["curve"] == "minutes":
            inp["end"] = next(iter(frozen.values()))["items"][0].get("held_until")
        live = json.loads(json.dumps(event(input=inp)["output"]))
        if r["is_rate"] and r["curve"] == "none":
            for d in (live, frozen):
                next(iter(d.values())).pop("note", None)
        n += 1
        if live != frozen:
            it = next(iter(frozen.values()))["items"][0]
            whole = (pd.Timestamp(it["held_until"].split(" +")[0].split(" -")[0]) -
                     pd.Timestamp(" ".join(r["start"].split(" ")[:2]))).total_seconds() / 3600 if it.get("held_until") else None
            if r["is_rate"] and whole and abs(it["units"] - it["rate"] * whole) > 1e-3:
                cut += 1                                           # a temporary basal inside it: only the file shows it
            else:
                bad.append(r["event_id"])
    assert not bad, f"{len(bad)} of {n} differ, first {bad[:3]}"
    return f"{n - cut} of {n} answer as frozen; {cut} basals cut by a temporary basal inside them"


if __name__ == "__main__":
    for name, fn in [("errors", t_errors), ("s04's dose", t_s04_dose), ("a rate, no curve, no insulin", t_rate_and_none),
                     ("parity with ext_insulin_event", t_parity_frozen)]:
        check(name, fn)
    print(f"{len(PASS)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)

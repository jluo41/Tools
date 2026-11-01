"""
Checks for eventnorm.medication. The errors need nothing; the rest need the SPACE's tables (describe-medication's
FDA table and WellDoc's catalog, pinned by the release) and s03's files. Run from the SPACE root after env.sh:

    python Tools/plugins/haipipe-utils/skills/haipipe-norm/eventnorm/tests/test_medication_event.py

THE EXAMPLES. b51 s03 ②'s dose (s03-medication-api/assets/medication-event-pill.json, written by its drawing
builder, where a dose first became an event) is sent raw, and its time, hour, item and answer must come back as that
file holds them. Every raw type is sent once with a row as its file holds it. THE PARITY. Every WellDoc id the catalog
names is asked through the event door, and its answer must equal the one frozen in ext_medication_resolved for the
same request (the catalog's name and NDC): ingredient, NDC, insulin, how sure.

Same shape as food's test_eventnorm.py: PASS/FAIL lines, exit 1 on any FAIL.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))                       # skills/haipipe-norm, so `eventnorm` imports
from eventnorm.medication import event                          # noqa: E402

S03 = Path("examples-1-data/Proj01-CGM-RawData/work/b51_externalstore/s03-medication-api/assets")
LLY = Path("_WorkSpace/0-RawDataStore/WellDoc2025LLY/Source/02_19_2025_MedAdministration.csv")
PASS, FAIL = [], []


def check(name, fn):
    try:
        note = fn()
        PASS.append(name)
        print(f"  PASS  {name}" + (f"  ({note})" if note else ""))
    except Exception as e:
        FAIL.append(name)
        print(f"  FAIL  {name}: {type(e).__name__}: {e}")


def one(ev):
    """The event's one hour and its first item."""
    (h, blk), = ev["output"].items()
    return h, blk, blk["items"][0]


def t_errors():
    for bad in ({}, {"raw": {"type": "photo", "rows": [{}]}}, {"input": {"items": [{"dose": 5}]}}):
        try:
            event(**bad)
        except ValueError:
            continue
        raise AssertionError(f"no error for {bad}")


def t_s03_pill():
    f = S03 / "medication-event-pill.json"
    if not f.exists() or not LLY.exists():
        return "skipped: no s03 file or LLY raw on this host"
    want = json.loads(f.read_text())
    ev = event(raw={"type": "app_id", "rows": want["raw"]["rows"]})
    assert ev["input"]["start"] == want["input"]["start"], (ev["input"]["start"], want["input"]["start"])
    (wh, wb), = want["output"].items()
    h, blk, it = one(ev)
    assert h == wh, (h, wh)
    wi = wb["items"][0]
    for k in ("ingredient", "brand", "class", "form", "route", "ndc", "dose", "insulin", "conf"):
        assert it[k] == wi[k], (k, it[k], wi[k])
    return f"{it['ingredient']} at {h}, {it['conf']}"


def t_every_type():
    got = []
    ev = event(raw={"type": "text", "rows": [{"Date": "2021-06-15 08:00:00",
                                               "Non-insulin hypoglycemic agents": "metformin 0.5 g, acarbose 50 mg"}]})
    its = ev["input"]["items"]
    assert [(i["drug"], i["dose"], i["unit"]) for i in its] == [("metformin", 500, "mg"), ("acarbose", 50, "mg")], its
    assert ev["input"]["start"] == "2021-06-15 08:00 +08:00" and ev["input"]["total"] == {"doses": 2}
    got.append("several: 2 drugs")
    ev = event(raw={"type": "text", "rows": [{"text": "Janumet 50/1000 mg, metformin 500 mg", "time": "2026-10-28 08:00"}]})
    its = ev["input"]["items"]                                   # a two-part dose: the pill kept, no dose (261028)
    assert [(i["drug"], i["dose"]) for i in its] == [("Janumet", None), ("metformin", 500)], its
    assert "50/1000 mg" in ev["step"], ev["step"]
    ev = event(raw={"type": "text", "rows": [{"Date": "2021-06-15 08:00:00",
                                               "Insulin dose - s.c.": "insulin glargine, 14 IU, Humulin 70/30, 12 IU"}]})
    assert [(i["drug"], i["dose"]) for i in ev["input"]["items"]] == [("insulin glargine", 14), ("Humulin 70/30", 12)]
    got.append("a two-part dose and a second insulin kept")
    ev = event(raw={"type": "text", "rows": [{"Date": "2021-06-15 08:00:00", "Insulin dose - i.v.":
                                               "500ml 0.9% sodium chloride, 12 IU Novolin R, 10 ml 10% potassium "
                                               "chloride"}]})
    assert [(i["drug"], i["dose"], i["delivery"]) for i in ev["input"]["items"]] == [("Novolin R", 12, "iv")]
    got.append("i.v.: the insulin only")
    ev = event(raw={"type": "pump", "rows": [{"Date": "2021-05-21 16:21:00", "胰岛素泵基础量 (Novolin R, IU / H)": "0.6"}]})
    assert ev["input"]["total"] == {"rate": 0.6, "unit": "iu/h"}, ev["input"]["total"]
    assert ev["input"]["items"][0]["delivery"] == "pump_basal"
    got.append("pump basal: a rate")
    ev = event(raw={"type": "class_word", "rows": [{"element": "bolus", "ts_begin": "04-07-2027 04:30:28",
                                                     "ts_end": "04-07-2027 04:30:28", "type": "normal", "dose": "1.2",
                                                     "insulin_type": "Humalog"}]})
    h, blk, it = one(ev)
    assert h == "2027-07-04 04:00" and it["insulin"] is True and blk["total"]["dose"] == 1.2, (h, it)
    got.append(f"OhioT1DM bolus: {it['ingredient']}")
    ev = event(raw={"type": "class_word", "rows": [{"element": "temp_basal", "ts_begin": "04-07-2027 23:50:00",
                                                     "ts_end": "05-07-2027 00:20:00", "value": "1.6"}]})
    assert list(ev["output"].values())[0]["share"] == round(10 / 30, 4) and len(ev["output"]) == 2, ev["output"]
    got.append("temp basal: shared by minutes")
    return "; ".join(got)


def t_parity_frozen():
    """Every catalog-named WellDoc request answers through the door as ext_medication_resolved froze it."""
    import glob
    import pandas as pd
    lex = sorted(glob.glob("_WorkSpace/ExternalStore/ext_med_lexicon/S*/*.parquet"))
    res = sorted(glob.glob("_WorkSpace/ExternalStore/ext_medication_resolved/S*/*.parquet"))
    if not lex or not res:
        return "skipped: no ext_med_lexicon or ext_medication_resolved on this host"
    lex, res = pd.read_parquet(lex[-1]), pd.read_parquet(res[-1])
    frozen = {r["MedicationRequest_original"]: r for r in res.to_dict("records")}
    n, bad = 0, []
    for mid, name, ndc in zip(lex["MedicationID_original"], lex["MedicationName"], lex["NDC"]):
        key = f"|{name}|{ndc if isinstance(ndc, str) else ''}|"
        if key not in frozen:
            continue
        mid = str(int(float(mid)))
        it = one(event(raw={"type": "app_id", "rows": [{"MedicationID": mid, "Dose": "1",
                                                        "AdministrationDate": "1/1/2024 12:00:00 PM",
                                                        "AdministrationTimeZoneOffset": "0"}]}))[2]
        f = frozen[key]
        same = lambda a, b: (a is None and (b is None or b != b)) or a == b
        if not (same(it["ingredient"], f["Ingredient"]) and same(it["ndc"], f["NDC"])
                and same(it["insulin"], f["IsInsulin"]) and it["conf"] == f["MedConf"]):
            bad.append((mid, it["ingredient"], f["Ingredient"], it["conf"], f["MedConf"]))
        n += 1
    assert not bad, f"{len(bad)} of {n} differ, first {bad[:3]}"
    return f"{n} of {n} catalog ids answer as frozen"


if __name__ == "__main__":
    for name, fn in [("errors", t_errors), ("s03's pill", t_s03_pill), ("every raw type", t_every_type),
                     ("parity with ext_medication_resolved", t_parity_frozen)]:
        check(name, fn)
    print(f"{len(PASS)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)

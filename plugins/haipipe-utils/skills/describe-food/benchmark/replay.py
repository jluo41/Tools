"""
BEHAVE for describe-food: replay every frozen contract specimen.

THIS NOUN'S SPECIMENS ARE NOT REQUEST/RESPONSE PAIRS. Exercise and medication
froze what their live door answered, so replaying those is a straight field
comparison. Food's five were hand-written on 260818 as a foodrec/v1 record, and
NOTHING EMITS foodrec/v1 -- grep the tree. They describe a target, not an
output, so most of a specimen is not this door's to answer:

    meal.*                 the cohort's row, handed IN, never computed
    totals.*               the cohort's OWN recorded columns. "Just Carbs;
    items[].nutrients      dinner" carries carb_g 45.0 with totals_basis
    coverage.resolved      'user_reported' -- the app wrote that 45, and the
    items[].match          door is given the string alone. Grading it would
                           grade a column the door never sees.

What the door DOES own is the decomposition, and that is exactly the layer
whose gate-B defect stayed invisible because no test called it. So two checks:

    DECOMPOSE   split_meal(raw_text) -> the specimen's items[] kind/text/grams
    SILENCE     the door writes a number IFF the specimen says the door is the
                totals source (totals_basis == 'item_sum'). Rule 4: a value
                that was not measured is not invented.

Everything else is reported as UNGRADED rather than quietly skipped.

CODE LIVES IN GIT, DATA DOES NOT. Runs land under _FoodInfo/6-benchmark/runs/.

    python replay.py            # print, write a run file
    python replay.py --dry      # print only
"""
import datetime
import glob
import json
import os
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve()
SKILL = HERE.parent.parent                      # describe-food/
sys.path.insert(0, str(SKILL))

from foodnorm import NUTRIENTS, normalize, split_meal   # noqa: E402

XINFO = pathlib.Path(
    os.environ.get("EVENTNORM_ROOT")
    or (SKILL.parents[4] / "_WorkSpace/0-RawDataStore/0-EventNorm")
) / "_FoodInfo"
CONTRACT = XINFO / "4-contract"
RUNS = XINFO / "6-benchmark" / "runs"

UNGRADED = ["meal.*", "totals.*", "items[].match", "items[].nutrients",
            "coverage.resolved", "coverage.items_sum_agrees"]


def _stated_grams(item):
    """The specimen's quantity, but only when it is grams the ROW stated.
    CGMacros' 'percent_consumed' is a portion eaten, not a mass, and the door
    is never told it."""
    q = item.get("quantity")
    if not isinstance(q, dict) or q.get("unit") != "g" or q.get("basis") != "stated":
        return None
    return q.get("value")


def check_decompose(spec):
    want = [(i["kind"], i["text"], _stated_grams(i)) for i in spec["items"]]
    got = [(c.kind, c.name, c.amount_g) for c in split_meal(spec["meal"]["raw_text"])]
    diffs = []
    for n, (w, g) in enumerate(zip(want, got)):
        if w != g:
            diffs.append({"item": n, "want": list(w), "got": list(g)})
    if len(want) != len(got):
        diffs.append({"item": "count", "want": len(want), "got": len(got),
                      "got_items": [[c.kind, c.name, c.amount_g]
                                    for c in split_meal(spec["meal"]["raw_text"])][len(want):]})
    return diffs


def check_silence(spec):
    """A number may appear only where the door is the declared source."""
    door_is_source = spec["coverage"].get("totals_basis") == "item_sum"
    out = normalize([spec["meal"]["raw_text"]])[0]
    wrote = [n for n in NUTRIENTS if out.get(n) is not None]
    if door_is_source and not wrote:
        return [{"expected": "numbers", "got": "silence",
                 "note": "totals_basis is item_sum, so the door is the source"}]
    if not door_is_source and wrote:
        return [{"expected": "silence", "got": wrote,
                 "note": f"totals_basis is {spec['coverage'].get('totals_basis')!r}; "
                         "the door is not the source of this row's totals"}]
    return []


def main():
    files = sorted(glob.glob(str(CONTRACT / "[0-9]*.json")))
    if not files:
        sys.exit(f"no specimens under {CONTRACT}")

    cases, n_pass = [], 0
    for f in files:
        spec = json.load(open(f))
        name = pathlib.Path(f).stem
        d_diffs = check_decompose(spec)
        s_diffs = check_silence(spec)
        ok = not d_diffs and not s_diffs
        n_pass += ok
        cases.append({"case": name, "pass": ok,
                      "decompose": d_diffs, "silence": s_diffs,
                      "raw_text": spec["meal"]["raw_text"],
                      "totals_basis": spec["coverage"].get("totals_basis")})
        print(f"  {'✅' if ok else '❌'} {name}")
        for d in d_diffs:
            print(f"       DECOMPOSE item {d['item']}: want {d['want']}  got {d['got']}")
        for d in s_diffs:
            print(f"       SILENCE expected {d['expected']}, got {d['got']}  ({d['note']})")

    run = {
        "noun": "food",
        "metric": "BEHAVE",
        "what_it_measures": "DECOMPOSE (split_meal vs the specimen's items) and "
                            "SILENCE (no number where the door is not the source)",
        "what_it_does_not": "the specimen's totals. They are the cohort's own "
                            "columns, and nothing emits foodrec/v1. "
                            "See 6-benchmark/README.md",
        "ungraded_fields": UNGRADED,
        "ran_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "cases_total": len(cases),
        "cases_pass": n_pass,
        "cases": cases,
    }
    print(f"\n  BEHAVE {n_pass}/{len(cases)}   (ungraded: {', '.join(UNGRADED)})")

    if "--dry" not in sys.argv:
        RUNS.mkdir(parents=True, exist_ok=True)
        stamp = datetime.date.today().strftime("%y%m%d")
        out = RUNS / f"{stamp}-behave.json"
        out.write_text(json.dumps(run, indent=2, ensure_ascii=False) + "\n")
        print(f"  wrote {out}")
    return 0 if n_pass == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())

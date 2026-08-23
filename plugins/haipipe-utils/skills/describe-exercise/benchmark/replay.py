"""
BEHAVE for describe-exercise: replay every frozen contract specimen.

A specimen in `_ExerciseInfo/4-contract/` is a real row plus the response the
live API gave it on the day it was frozen. Nothing has ever read them back.
This does, field by field, and that is the only number this noun can report
without a gold: not "is the MET right" -- there is no MET gold -- but "does the
door still answer the way it answered when a person looked at it and agreed".

CODE LIVES IN GIT, DATA DOES NOT. The scorecard is written under
_WorkSpace/0-RawDataStore/0-EventNorm/_ExerciseInfo/6-benchmark/runs/, the same
rule 2-corpus already states for itself.

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
SKILL = HERE.parent.parent                      # describe-exercise/
sys.path.insert(0, str(SKILL))

from exnorm import normalize                    # noqa: E402
from exnorm.constants import _find_bank         # noqa: E402  (walks up to the store)

XINFO = pathlib.Path(
    os.environ.get("EVENTNORM_ROOT")
    or (SKILL.parents[4] / "_WorkSpace/0-RawDataStore/0-EventNorm")
) / "_ExerciseInfo"
CONTRACT = XINFO / "4-contract"
RUNS = XINFO / "6-benchmark" / "runs"

TOL = 1e-6


def _same(want, got):
    """None must stay None. A number that drifts is a change, not a rounding."""
    if want is None or got is None:
        return want is None and got is None
    if isinstance(want, bool) or isinstance(got, bool):
        return bool(want) == bool(got)
    if isinstance(want, (int, float)) and isinstance(got, (int, float)):
        return abs(float(want) - float(got)) <= TOL * max(1.0, abs(float(want)))
    return str(want) == str(got)


def replay_one(spec):
    req = spec["request"]
    got = normalize(
        [req["activity"]],
        minutes=[req["minutes"]] if req.get("minutes") is not None else None,
        weight_kg=[req["weight_kg"]] if req.get("weight_kg") is not None else None,
        source_ids=[req["source_id"]] if req.get("source_id") is not None else None,
    )[0]
    diffs = []
    for k, want in spec["response"].items():
        if k not in got:
            diffs.append({"field": k, "want": want, "got": "<ABSENT>"})
        elif not _same(want, got[k]):
            diffs.append({"field": k, "want": want, "got": got[k]})
    extra = sorted(set(got) - set(spec["response"]))
    return diffs, extra, got


def main():
    files = sorted(glob.glob(str(CONTRACT / "[0-9]*.json")))
    if not files:
        sys.exit(f"no specimens under {CONTRACT}")

    cases, n_pass = [], 0
    for f in files:
        spec = json.load(open(f))
        name = pathlib.Path(f).stem
        diffs, extra, _ = replay_one(spec)
        ok = not diffs
        n_pass += ok
        cases.append({"case": name, "pass": ok, "diffs": diffs,
                      "fields_not_frozen": extra,
                      "why": spec.get("_why_this_row")})
        mark = "✅" if ok else "❌"
        print(f"  {mark} {name}")
        for d in diffs:
            print(f"       {d['field']}: want {d['want']!r}  got {d['got']!r}")
        if extra:
            print(f"       (not frozen: {', '.join(extra)})")

    run = {
        "noun": "exercise",
        "metric": "BEHAVE",
        "what_it_measures": "frozen contract specimens replayed against the live door",
        "what_it_does_not": "accuracy. this noun has no MET gold; see 6-benchmark/README.md",
        "bank": str(_find_bank()),
        "ran_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "cases_total": len(cases),
        "cases_pass": n_pass,
        "cases": cases,
    }
    print(f"\n  BEHAVE {n_pass}/{len(cases)}")

    if "--dry" not in sys.argv:
        RUNS.mkdir(parents=True, exist_ok=True)
        stamp = datetime.date.today().strftime("%y%m%d")
        out = RUNS / f"{stamp}-behave.json"
        out.write_text(json.dumps(run, indent=2, ensure_ascii=False) + "\n")
        print(f"  wrote {out}")
    return 0 if n_pass == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())

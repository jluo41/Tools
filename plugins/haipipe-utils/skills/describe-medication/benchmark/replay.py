"""
BEHAVE for describe-medication: replay every frozen contract specimen.

This is the ONLY number this noun can report about identity today. There is no
drug-identity gold anywhere: 871 MedicationIDs and nobody has hand-checked one.
`ndc_vs_name_overlap` in _stats.json counts whether two paths CONTRADICT each
other, which is not whether either is right. So BEHAVE answers the one question
that IS answerable -- does the door still answer as it did when a person read
the answer and agreed -- and the README says plainly what it leaves open.

CODE LIVES IN GIT, DATA DOES NOT. Runs land under _MedInfo/6-benchmark/runs/.

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
SKILL = HERE.parent.parent                      # describe-medication/
sys.path.insert(0, str(SKILL))

from mednorm import normalize                   # noqa: E402

XINFO = pathlib.Path(
    os.environ.get("EVENTNORM_ROOT")
    or (SKILL.parents[4] / "_WorkSpace/0-RawDataStore/0-EventNorm")
) / "_MedInfo"
CONTRACT = XINFO / "4-contract"
RUNS = XINFO / "6-benchmark" / "runs"

TOL = 1e-6


def _same(want, got):
    if want is None or got is None:
        return want is None and got is None
    if isinstance(want, bool) or isinstance(got, bool):
        return bool(want) == bool(got)
    if isinstance(want, (int, float)) and isinstance(got, (int, float)):
        return abs(float(want) - float(got)) <= TOL * max(1.0, abs(float(want)))
    return str(want) == str(got)


def replay_one(spec):
    req = spec["request"]
    # The door takes payloads as JSON STRINGS; the specimen froze the object.
    payload = req.get("payload")
    got = normalize(
        [req["item"]],
        doses=[req["dose"]] if req.get("dose") is not None else None,
        payloads=[json.dumps(payload)] if payload is not None else None,
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
                      "fields_not_frozen": extra, "why": spec.get("why")})
        print(f"  {'✅' if ok else '❌'} {name}")
        for d in diffs:
            print(f"       {d['field']}: want {d['want']!r}  got {d['got']!r}")
        if extra:
            print(f"       (not frozen: {', '.join(extra)})")

    run = {
        "noun": "medication",
        "metric": "BEHAVE",
        "what_it_measures": "frozen contract specimens replayed against the live door",
        "what_it_does_not": "identity accuracy. no drug-identity gold exists; "
                            "see 6-benchmark/README.md",
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

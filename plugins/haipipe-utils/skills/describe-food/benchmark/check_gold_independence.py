#!/usr/bin/env python3
"""
Prove -- or refuse -- the one assumption every food ruler rests on: THAT THE
GOLD AND THE ANSWER DO NOT COME FROM THE SAME PLACE.

Exercise's version of this file tests one failure mode, a vendor reading a MET
off a table. Food has THREE, and all three were found by being fooled first.

    1  WRITTEN BY THE DOOR
       Shanghai's macro columns were produced by this resolver. Grading them
       returns our own answer. Detected by the frame's own NutritionSource
       column, so it needs no arithmetic at all.

    2  SAME TABLE
       Our USDA sqlite ships `survey_fndds_food`, one row per FNDDS code. The
       FNDDS corpus's gold IS a row of the bank. Scored 0.31 carb MAE with a
       median of exactly 0.00 before the holdout existed.

    3  SAME UPSTREAM VENDOR -- the one that took a probe to find
       The T0 observed bank does not hold a patient's opinion of 'banana'. It
       holds FatSecret's number for the string 'banana', and FatSecret supplied
       the patient's label too. So splitting PATIENTS does not split SOURCES:
       WellDoc's train-bank x test-gold probe still matched 79.5% of units to
       within 0.01 g.

THE TEST, and why it is two numbers and not one
================================================================================
Independent estimators of the same food disagree. They disagree by a few grams,
not by nothing. So:

    exact share      fraction of units matching to within 0.01 g of carbohydrate
    median abs err   the middle disagreement

    median == 0.00                 ->  half the answers ARE the gold. Fatal.
    exact share >= 0.30            ->  agreement this tight is identity, not
                                       agreement. Fatal.

The thresholds are not free parameters. Measured 260822 on this board:

    E3_OFF                4.0% exact, median 6.53   independent
    E2_N5K                8.6% exact, median 3.61   independent
    E1_FNDDS             17.3% exact, median 3.05   independent (holdout bank)
    WellDoc _split_probe 79.5% exact, median 0.00   CONTAMINATED

17.3% and 79.5% are not close, and 0.30 sits between them with room on both
sides. FNDDS is the highest clean reading because the observed bank genuinely
holds some of these strings -- which is the door working, not a leak.

A GATE THAT HAS NEVER FIRED IS NOT A GATE, so this one carries a POSITIVE
CONTROL: it re-resolves FNDDS against the PRODUCTION bank, where
`survey_fndds_food` is still present, and REQUIRES that reading to fail. If the
control passes, the detector is broken and the whole run is void.

    source .venv/bin/activate && source env.sh
    python check_gold_independence.py            # exits 1 on contamination
    python check_gold_independence.py --no-control
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

ROOT = pathlib.Path("/home/jluo41/WellDoc-SPACE")
INFO = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_FoodInfo"
CORPUS = INFO / "2-corpus"
OUT = INFO / "6-benchmark"

EXACT_TOL = 0.01         # g of carbohydrate. Below this, two answers are one.
EXACT_SHARE_MAX = 0.30   # above this, agreement is identity
MIN_N = 20               # a set smaller than this cannot be judged


def score(d):
    """One gradeable set -> the two numbers, and nothing else."""
    e = (d.resolved_Carbs - d.gold_Carbs).abs().dropna()
    if len(e) < MIN_N:
        return dict(n=int(len(e)), verdict="TOO_SMALL")
    exact = float((e < EXACT_TOL).mean())
    med = float(e.median())
    bad = []
    if med == 0.0:
        bad.append("median disagreement is exactly zero")
    if exact >= EXACT_SHARE_MAX:
        bad.append(f"{exact:.1%} of units match to within {EXACT_TOL} g")
    return dict(n=int(len(e)), exact_share=round(exact, 4),
                median_abs_err=round(med, 3), mae=round(float(e.mean()), 3),
                verdict="CONTAMINATED" if bad else "INDEPENDENT", because=bad)


def positive_control():
    """Re-resolve FNDDS against the bank that still holds survey_fndds_food.

    This reading MUST come back CONTAMINATED. It is the only thing in this file
    that proves the detector can detect.
    """
    import tempfile
    src = pd.read_parquet(CORPUS / "FNDDS-2021-2023/units.parquet")
    code = (
        "import sys,pandas as pd\n"
        f"sys.path.insert(0,{str(HERE.parent)!r})\n"
        "from foodnorm import normalize\n"
        f"u=pd.read_parquet({str(CORPUS / 'FNDDS-2021-2023/units.parquet')!r})\n"
        "r=pd.DataFrame(normalize(u.unit_text.tolist()))\n"
        "u['resolved_Carbs']=pd.to_numeric(r['Carbs'],errors='coerce').values\n"
        f"u.to_parquet({'/tmp/_fndds_control.parquet'!r},index=False)\n")
    env = {k: v for k, v in os.environ.items() if k != "FOODNORM_DB"}
    r = subprocess.run([sys.executable, "-c", code], env=env,
                       capture_output=True, text=True)
    if r.returncode:
        return dict(verdict="CONTROL_FAILED_TO_RUN", stderr=r.stderr[-500:])
    d = pd.read_parquet("/tmp/_fndds_control.parquet")
    s = score(d)
    s["bank"] = "production (survey_fndds_food PRESENT)"
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-control", action="store_true")
    a = ap.parse_args()

    report, rulers_bad = {}, []

    # ── test 1: written by the door. No arithmetic; the frame says so. ───────
    written = []
    for f in sorted(CORPUS.glob("*/units.parquet")):
        u = pd.read_parquet(f)
        if (u.gold_tier == "CIRCULAR").any():
            written.append(f.parent.name)
    report["written_by_the_door"] = written
    print(f"test 1  written by the door : {written or 'none'}")

    # ── tests 2 and 3: the two numbers, on every gradeable set on the board ──
    print(f"\ntest 2+3  {'set':<40s}{'n':>7}{'exact':>8}{'median':>9}{'MAE':>9}  verdict")
    print("-" * 88)
    sets = {}
    for f in sorted(CORPUS.glob("*/*.parquet")):
        if f.name == "units.parquet":
            continue
        d = pd.read_parquet(f)
        if "gold_Carbs" not in d:
            continue
        key = f"{f.parent.name}/{f.name}"
        s = sets[key] = score(d)
        is_ruler = not f.name.startswith("_")
        s["is_ruler"] = is_ruler
        if s["verdict"] == "CONTAMINATED" and is_ruler:
            rulers_bad.append(key)
        if s["verdict"] == "TOO_SMALL":
            print(f"        {key:<40s}{s['n']:>7}{'--':>8}{'--':>9}{'--':>9}  TOO_SMALL")
        else:
            print(f"        {key:<40s}{s['n']:>7,d}{s['exact_share']:>8.1%}"
                  f"{s['median_abs_err']:>9.2f}{s['mae']:>9.2f}  {s['verdict']}"
                  + ("" if is_ruler else "   (probe, not a ruler)"))
    report["sets"] = sets

    # ── the positive control ────────────────────────────────────────────────
    ctl_ok = True
    if not a.no_control:
        print("\npositive control  FNDDS against the PRODUCTION bank "
              "(survey_fndds_food present)")
        c = positive_control()
        report["positive_control"] = c
        ctl_ok = c.get("verdict") == "CONTAMINATED"
        if "exact_share" in c:
            print(f"        n={c['n']:,d}  exact={c['exact_share']:.1%}  "
                  f"median={c['median_abs_err']:.2f}  -> {c['verdict']}")
        print("        " + ("detector FIRES on a known leak -- gate is live"
                            if ctl_ok else
                            "⚠️ CONTROL DID NOT FIRE. The detector is broken and "
                            "every reading above is void."))

    verdict = ("DETECTOR_BROKEN" if not ctl_ok else
               "CONTAMINATED" if rulers_bad else "INDEPENDENT")
    report["verdict"] = verdict
    report["contaminated_rulers"] = rulers_bad
    report["thresholds"] = dict(exact_tol_g=EXACT_TOL,
                                exact_share_max=EXACT_SHARE_MAX, min_n=MIN_N)
    print(f"\nVERDICT: {verdict}")
    if rulers_bad:
        print(f"  contaminated rulers: {rulers_bad}")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "gold_independence.json").write_text(json.dumps(report, indent=2))
    print(f"wrote {OUT / 'gold_independence.json'}")
    return 0 if verdict == "INDEPENDENT" else 1


if __name__ == "__main__":
    sys.exit(main())

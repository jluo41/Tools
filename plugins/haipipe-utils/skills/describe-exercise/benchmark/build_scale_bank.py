"""
Build the frozen scale bank exnorm/scale.py reads.

WHAT A FACTOR IS
================================================================================
    factor = median( MET_device / MET_compendium )

over the rows allowed by that tier's fence. A factor of 0.82 says this vendor's
app consistently reports less energy than the Compendium predicts for the same
named activity; multiplying by it moves our answer toward what the device
actually measured on real people.

THE FENCE IS THE WHOLE DESIGN (haipipe-norm rule 11)
================================================================================
A bank built from the board is a second path to the label. Each tier needs a
fence that keeps the fit away from the rows it will be scored on, and the two
tiers need DIFFERENT fences:

    device   fence = the PATIENT SPLIT. Fit on train patients, scored on
             patients the fit never saw. A vendor factor is a property of the
             vendor, so it generalises across people and this fence is honest.

    person   fence = TIME, and nothing else will do. The patient-hash split
             leaves a test patient with ZERO training rows, so a personal factor
             could only ever be fit on the very rows it is scored on. That is
             not a weak measurement, it is the same circularity that inflated
             describe-food to r 0.988. The fence comes from
             `2-corpus/person_split.parquet`: only a patient's own FIRST bouts
             may be fit, and only their later ones may be scored.

A PERSON'S FACTOR IS NOT AVAILABLE TO EVERY PERSON, AND THAT IS THE POINT
================================================================================
163 of 421 patients with a gradeable bout never log enough of them to earn one.
They are not a rounding error, they are 39% of the people, and they are exactly
who the device tier is for. A ladder whose top rung reaches 61% of the board is
why the lower rungs are not optional.

WHY THE BUILDER READS METReference AND NOT METValue
================================================================================
Once a bank exists, normalize() returns the ADJUSTED MET. Fitting the next bank
on that would compound the factor on every rebuild until it ran away. METReference
always carries the Compendium's own published number, which is the only thing a
factor may be measured against.

    source .venv/bin/activate && source env.sh
    python build_scale_bank.py
    python build_scale_bank.py --dry        # print, write nothing
"""
import argparse
import datetime
import pathlib
import subprocess
import sys

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from exnorm import normalize                                   # noqa: E402
from exnorm.constants import SCALE_MAX, SCALE_MIN              # noqa: E402

ROOT = pathlib.Path("/home/jluo41/WellDoc-SPACE")
CORPUS = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_ExerciseInfo/2-corpus"
OUT = ROOT / "_WorkSpace/ExternalStore/exnorm_scale"

MIN_ROWS = 100          # below this a vendor factor is one clinic's habit
MIN_PATIENTS = 15       # and below this it is a handful of people
MIN_CALIB = 5           # a person needs this many of their own bouts to earn one
MIN_CALIB_PA = 2        # and this many OF THAT ACTIVITY for the narrowest rung


def _head():
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True).stdout.strip()
    except Exception:
        return "unknown"


def device_rows(as_of: str):
    """One row per EntrySourceID, fit on TRAIN patients only."""
    g = pd.read_parquet(CORPUS / "gold_index.parquet")
    g = g[(g["shape"] == "session") & (g["label"] == "device_met")].copy()

    res = pd.DataFrame(normalize(list(g.ExerciseType.astype(str)),
                                 source_ids=list(g.EntrySourceID)))
    # METReference, never METValue. See the module docstring.
    g["comp"] = pd.to_numeric(res.METReference, errors="coerce").values
    # The COMPENDIUM code, not the vendor's. It is what the door looks the
    # narrowest rung up by, and it usefully merges vendor codes that mean the
    # same activity: Validic 1001 and Nokia 1001 are both walking, and one
    # person's walks should not be split across two keys.
    g["code"] = res.ActivityCode.values
    g = g[g.comp.gt(0) & g.MET_device.notna() & g.EntrySourceID.notna()]

    tr = g[g.split == "train"].copy()
    tr["ratio"] = tr.MET_device / tr.comp

    out = []
    for sid, d in tr.groupby("EntrySourceID"):
        n, npat = len(d), d.PatientID.nunique()
        if n < MIN_ROWS or npat < MIN_PATIENTS:
            print(f"    skip source {int(sid):<3d} n={n:<6,d} patients={npat:<4d}"
                  f"  (needs {MIN_ROWS} rows and {MIN_PATIENTS} patients)")
            continue
        f = float(np.clip(d.ratio.median(), SCALE_MIN, SCALE_MAX))
        out.append(dict(kind="device", key=str(int(sid)), factor=round(f, 4),
                        n=n, n_patients=npat, as_of=as_of,
                        fence="patient_split:train"))
    return pd.DataFrame(out), g


def person_rows(as_of: str, g: pd.DataFrame):
    """One row per patient, fit ONLY on their own earliest bouts.

    `g` already carries METReference. The split file says which rows the fence
    lets this tier see; a row not marked `calib` is invisible here, whatever
    patient-split it belongs to, because the fence for this tier is time."""
    cal = _calib(g)
    if cal is None:
        print("    no person_split.parquet -- run build_person_split.py first")
        return pd.DataFrame()

    out = []
    for (coh, pid), d in cal.groupby(["cohort", "PatientID"]):
        if len(d) < MIN_CALIB:
            continue
        f_ = float(np.clip(d.ratio.median(), SCALE_MIN, SCALE_MAX))
        out.append(dict(kind="person", key=str(pid), factor=round(f_, 4),
                        n=len(d), n_patients=1, as_of=as_of,
                        fence=f"time:<={str(d.calib_until.max())[:10]}"))
    return pd.DataFrame(out)


def _calib(g: pd.DataFrame):
    """The rows the TIME fence lets a personal tier see, with their ratio."""
    f = CORPUS / "person_split.parquet"
    if not f.exists():
        return None
    sp = pd.read_parquet(f)
    sp = sp[sp.person_split == "calib"]
    key = ["cohort", "PatientID", "ExerciseEntryID"]
    g = g.copy()
    for c in ("PatientID", "ExerciseEntryID"):
        g[c] = g[c].astype(str)
        sp[c] = sp[c].astype(str)
    cal = g.merge(sp[key + ["calib_until"]], on=key, how="inner")
    cal["ratio"] = cal.MET_device / cal.comp
    return cal


def person_activity_rows(as_of: str, cal: pd.DataFrame):
    """One row per (patient, COMPENDIUM code). The narrowest rung, and the one
    with the least material: a person's first five bouts rarely cover more than
    two activities, so this rung is thin by construction and the ladder below it
    carries most of the traffic."""
    out = []
    for (pid, code), d in cal[cal.code.notna()].groupby(["PatientID", "code"]):
        if len(d) < MIN_CALIB_PA:
            continue
        f_ = float(np.clip(d.ratio.median(), SCALE_MIN, SCALE_MAX))
        out.append(dict(kind="person_activity", key=f"{pid}|{code}",
                        factor=round(f_, 4), n=len(d), n_patients=1, as_of=as_of,
                        fence=f"time:<={str(d.calib_until.max())[:10]}"))
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    as_of = datetime.datetime.now().strftime("%Y-%m-%d")
    print("building the scale bank\n  DEVICE tier (fence: train patients only)")
    dev, g = device_rows(as_of)
    for r in dev.itertuples(index=False):
        print(f"    source {r.key:<3s} factor {r.factor:5.3f}   "
              f"n={r.n:<6,d} patients={r.n_patients}")

    print("\n  PERSON tier (fence: each patient's own earliest bouts)")
    per = person_rows(as_of, g)
    if len(per):
        print(f"    {len(per):,} patients earned a factor")
        print(f"    median {per.factor.median():.3f}  "
              f"p10 {per.factor.quantile(.1):.3f}  p90 {per.factor.quantile(.9):.3f}")
        print(f"    clipped at the band edge: {int(((per.factor <= SCALE_MIN) | (per.factor >= SCALE_MAX)).sum())}")

    print("\n  PERSON_ACTIVITY tier (fence: the same, narrowed to one activity)")
    cal = _calib(g)
    pa = person_activity_rows(as_of, cal) if cal is not None else pd.DataFrame()
    if len(pa):
        print(f"    {len(pa):,} (patient, compendium code) pairs, "
              f">= {MIN_CALIB_PA} calib bouts each")
        print(f"    median {pa.factor.median():.3f}  "
              f"p10 {pa.factor.quantile(.1):.3f}  p90 {pa.factor.quantile(.9):.3f}")

    dev = pd.concat([d for d in (dev, per, pa) if len(d)], ignore_index=True)

    if a.dry:
        print("\n  --dry, nothing written")
        return

    OUT.mkdir(parents=True, exist_ok=True)
    dev.to_parquet(OUT / "scale.parquet", index=False)
    d_only = dev[dev.kind == "device"]
    p_only = dev[dev.kind == "person"]
    pa_only = dev[dev.kind == "person_activity"]
    (OUT / "README.md").write_text(README.format(
        as_of=as_of, head=_head(), n=len(dev), minr=MIN_ROWS, minp=MIN_PATIENTS,
        minc=MIN_CALIB, n_person=len(p_only), n_pa=len(pa_only),
        mincpa=MIN_CALIB_PA,
        pmed=(p_only.factor.median() if len(p_only) else float("nan")),
        p10=(p_only.factor.quantile(.1) if len(p_only) else float("nan")),
        p90=(p_only.factor.quantile(.9) if len(p_only) else float("nan")),
        table="\n".join(
            f"  {r.key:<6s}{r.factor:>8.3f}{r.n:>10,d}{r.n_patients:>10d}   {r.fence}"
            for r in d_only.itertuples(index=False))))
    print(f"\n  wrote {OUT}/scale.parquet  ({len(d_only)} device + "
          f"{len(p_only)} person + {len(pa_only)} person_activity)")


README = """\
# exnorm_scale

The frozen scale bank `exnorm/scale.py` reads. GENERATED by
`describe-exercise/benchmark/build_scale_bank.py`; do not hand-edit.

Built {as_of} at `{head}`. {n} rows, all DEVICE tier.

```text
  key      factor       n   patients   fence
  ────────────────────────────────────────────────────────
{table}
```

A factor is `median(MET_device / MET_compendium)` over the rows its fence
allows. It says how far this vendor's own calorie model sits from the
Compendium's prediction for the same named activity.

A key needs {minr} rows and {minp} patients to earn a factor. Below that the
number is one clinic's habit rather than a vendor's behaviour, and the row is
skipped so the tier falls through to `population`.

## The person tier

{n_person} patients earned one: factor median {pmed:.3f}, p10 {p10:.3f}, p90 {p90:.3f}.

Its fence is TIME and comes from `2-corpus/person_split.parquet`. A patient's
factor is fit on their own FIRST {minc} gradeable bouts and may be scored only on
bouts after that; the `fence` column records the exact cut-off date per person.
The patient-hash split is irrelevant to this tier and is deliberately ignored --
a personal factor is not supposed to generalise to other people.

163 of 421 patients never log enough bouts to earn one and always fall through
to `device`. That is 39% of the people, and it is why the lower rungs of the
ladder are not optional.

## The person_activity tier

{n_pa} (patient, Compendium code) pairs, each with at least {mincpa} calibration
bouts OF THAT ACTIVITY. Keyed on the Compendium code rather than the vendor's,
so one person's walks are not split across Validic 1001 and Nokia 1001.

It is thin by construction: a person's first {minc} bouts cover one activity for
94 patients and two for 89, so most people can never populate more than a couple
of pairs. The rung above a thin rung is not wasted -- it is the reason the
ladder falls through instead of failing.
"""


if __name__ == "__main__":
    main()

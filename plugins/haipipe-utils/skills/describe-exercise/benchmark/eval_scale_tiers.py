"""
Score the scale ladder on rows every tier's fence allows.

WHY run.py CANNOT ANSWER THIS
================================================================================
`run.py` scores every row of the patient-hash test split, and 5 of every
patient's bouts are the ones their own factor was fit on. Scoring the person
tier there would read its own calibration back as accuracy. This file scores
ONLY rows marked `eval` in `2-corpus/person_split.parquet` -- after each
patient's own cut-off -- so all three configurations are judged on identical
rows that no fence was allowed to see.

THE THREE CONFIGURATIONS ARE THE SAME DOOR, THREE BANKS
================================================================================
    population   no bank on disk. What a caller who passes nothing still gets.
    device       the vendor rows only. No personal history, no cold start.
    person       device plus the per-patient rung.
    ladder       every rung, person_activity on top.

The four are CUMULATIVE, so each line of the table is the one above it plus one
rung, and the difference between two lines is what that rung is worth.

Nothing in exnorm is monkey-patched to produce these; each run points the door
at a different frozen bank with `scale_path`, which is the same mechanism an
A/B against a newer bank would use.

    source .venv/bin/activate && source env.sh
    python eval_scale_tiers.py
"""
import json
import pathlib
import sys
import tempfile

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from exnorm import normalize                                   # noqa: E402

ROOT = pathlib.Path("/home/jluo41/WellDoc-SPACE")
CORPUS = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_ExerciseInfo/2-corpus"
BENCH = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_ExerciseInfo/6-benchmark"
BANK = ROOT / "_WorkSpace/ExternalStore/exnorm_scale/scale.parquet"


def eval_rows():
    g = pd.read_parquet(CORPUS / "gold_index.parquet")
    g = g[(g["shape"] == "session") & (g["label"] == "device_met")].copy()
    sp = pd.read_parquet(CORPUS / "person_split.parquet")
    key = ["cohort", "PatientID", "ExerciseEntryID"]
    for c in ("PatientID", "ExerciseEntryID"):
        g[c] = g[c].astype(str)
        sp[c] = sp[c].astype(str)
    d = g.merge(sp[key + ["person_split", "bout_rank"]], on=key, how="inner")
    return d[d.person_split == "eval"].reset_index(drop=True)


def banks(tmp: pathlib.Path):
    """Four files the door can be pointed at, each the previous plus one rung."""
    full = pd.read_parquet(BANK)
    out, keep = {}, []
    for name, kinds in (("population", []),
                        ("device", ["device"]),
                        ("person", ["device", "person"]),
                        ("ladder", ["device", "person", "person_activity"])):
        f = tmp / f"{name}.parquet"
        full[full.kind.isin(kinds)].to_parquet(f, index=False)
        out[name] = f
    return out


def score(d: pd.DataFrame, path) -> dict:
    res = pd.DataFrame(normalize(list(d.ExerciseType.astype(str)),
                                 source_ids=list(d.EntrySourceID),
                                 person_ids=list(d.PatientID),
                                 scale_path=str(path)))
    p = pd.to_numeric(res.METValue, errors="coerce")
    ok = p.notna() & d.MET_device.notna()
    t, p = d.MET_device[ok], p[ok]
    e = p - t
    return {"scored": int(ok.sum()),
            "mae": round(float(e.abs().mean()), 3),
            "r": round(float(np.corrcoef(t, p)[0, 1]), 3),
            "bias": round(float(e.mean()), 3),
            "within_1": round(float((e.abs() <= 1).mean()), 4),
            "within_2": round(float((e.abs() <= 2).mean()), 4),
            "tiers": {k: int(v) for k, v in
                      res.METScale[ok.values].value_counts().items()}}


def main():
    d = eval_rows()
    print(f"scored on person_split == 'eval' only: {len(d):,} rows, "
          f"{d.PatientID.nunique()} patients\n")

    with tempfile.TemporaryDirectory() as td:
        out = {k: score(d, p) for k, p in banks(pathlib.Path(td)).items()}

    print(f"{'config':12s}{'scored':>8s}{'MAE':>7s}{'r':>7s}{'bias':>7s}"
          f"{'±1':>8s}{'±2':>8s}   tiers used")
    print("-" * 82)
    for k in ("population", "device", "person", "ladder"):
        m = out[k]
        print(f"{k:12s}{m['scored']:>8,d}{m['mae']:>7.2f}{m['r']:>7.3f}"
              f"{m['bias']:>7.2f}{m['within_1']:>8.1%}{m['within_2']:>8.1%}   "
              + " ".join(f"{a}={b:,}" for a, b in sorted(m["tiers"].items())))

    (BENCH / "runs" / "scale_tiers.json").write_text(json.dumps(
        {"scored_on": "person_split==eval", "rows": int(len(d)),
         "patients": int(d.PatientID.nunique()), "configs": out}, indent=1))
    print(f"\n  wrote {BENCH}/runs/scale_tiers.json")


if __name__ == "__main__":
    main()

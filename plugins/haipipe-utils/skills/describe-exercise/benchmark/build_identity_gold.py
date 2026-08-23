"""
I1_IDENTITY: the hand-gold worksheet, prefilled but never ticked.

WHAT THIS ANSWERS THAT NOTHING ELSE DOES
================================================================================
The row benchmark grades a MET and cannot tell two failures apart: the wrong
Compendium entry, and the right entry on a person who is not the population
average. Only a hand label separates them, and a hand label needs a person.

THE MACHINE'S HALF AND THE PERSON'S HALF ARE DIFFERENT COLUMNS
================================================================================
This file writes `proposed_code` and never `gold_code`. It ranks candidates,
it says which ones it doubts and why, and it stops. A machine may not tick its
own answer as gold; doing so would make I1 the resolver grading itself, which
is the same circularity rule 11 already bans for banks.

THE DEVICE MET IS A WITNESS, NOT A JUDGE
================================================================================
Where a unit has enough rows, its back-solved device MET is shown beside every
candidate's Compendium MET. It cannot decide the naming -- 'Walk' and 'Hike'
sit two tenths apart -- but a candidate three METs away from what the device
measured is worth a second look, and the worksheet says so.

    source .venv/bin/activate && source env.sh
    python build_identity_gold.py                # mcphases-v1
    python build_identity_gold.py --corpus WellDoc
"""
import argparse
import pathlib
import sys

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from exnorm import met_db                                      # noqa: E402

ROOT = pathlib.Path("/home/jluo41/WellDoc-SPACE")
CORPUS = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_ExerciseInfo/2-corpus"

TRUSTED = {"ALIAS", "CODEBOOK", "EXACT"}
K = 5
MET_DOUBT = 1.5          # candidate this far from the device MET -> look again
MIN_MET_N = 30


def worksheet(corpus: str) -> pd.DataFrame:
    u = pd.read_parquet(CORPUS / corpus / "units.parquet")
    out = []
    for _, r in u.iterrows():
        dev = r.met_device_median if r.met_device_n >= MIN_MET_N else np.nan
        cands = met_db.search(str(r.unit_text), k=K)

        # The resolver's own pick, restated as a candidate so the person is
        # comparing like with like rather than reading two different shapes.
        picked = str(r.resolved_code) if pd.notna(r.resolved_code) else None
        best_by_met = None
        if pd.notna(dev) and cands:
            best_by_met = min(cands, key=lambda c: abs(c["met_value"] - dev))

        # THE REFERENCE, NOT THE SCALED MET. Since the scale tier shipped,
        # METValue has already been pulled toward what the device measured --
        # comparing THAT to the device would be asking whether the correction
        # worked, when the question here is whether the ENTRY is right. The
        # published Compendium number is the only fair thing to hold up.
        ref = r.resolved_met_ref if "resolved_met_ref" in u.columns else r.resolved_met

        why = []
        if r.resolved_conf not in TRUSTED:
            why.append(f"conf={r.resolved_conf}")
        if pd.notna(dev) and pd.notna(ref) and abs(float(ref) - dev) > MET_DOUBT:
            why.append(f"Compendium says {float(ref):.1f}, device says {dev:.1f}")
        if best_by_met and picked and best_by_met["activity_code"] != picked \
                and pd.notna(dev) \
                and abs(best_by_met["met_value"] - dev) + MET_DOUBT \
                < abs(float(ref or 0) - dev):
            why.append(f"{best_by_met['activity_code']} fits the device better")

        out.append(dict(
            unit=r.unit, unit_text=r.unit_text, row_weight=int(r.row_weight),
            n_patients=int(r.n_patients),
            device_met=round(float(dev), 2) if pd.notna(dev) else None,
            device_met_n=int(r.met_device_n),
            proposed_code=picked,
            proposed_activity=r.resolved_activity,
            proposed_met=ref,
            proposed_conf=r.resolved_conf,
            candidates=[f"{c['activity_code']}|{c['met_value']}|"
                        f"{c['activity_description']}" for c in cands],
            needs_review=bool(why),
            review_because="; ".join(why),
            # ---- the person's columns. Written by a person, never here. ----
            gold_code=None, gold_alts=None, gold_ambiguous=None, gold_note=None,
        ))
    w = pd.DataFrame(out).sort_values("row_weight", ascending=False)
    return w.reset_index(drop=True)


SHEET = """\
# I1_IDENTITY -- {corpus}

{n} units. **{n_rev} need a person**; the rest the resolver answered with a
trusted confidence and a device MET that does not argue with it.

Fill `gold_code` in `I1_IDENTITY.parquet`. Leave a unit blank and it stays
UNLABELLED, which is a legitimate answer and is not a zero. Set
`gold_ambiguous = True` where more than one code is genuinely right --
`Treadmill` is the standing example: walking and running are both correct and
the log does not say which.

`proposed_code` is this script's ranking. It is NOT gold and must not be
copied into `gold_code` without reading the candidates.

```text
  device_met   the back-solved MET this unit actually shows, when it rests
               on >= {minn} rows. A witness, not a judge.
  candidates   code | Compendium MET | description
```

## Needs a person

{review}

## The resolver's answer looks right

{rest}

GENERATED by `describe-exercise/benchmark/build_identity_gold.py`.
The `gold_*` columns are a person's and are never written by that script.
"""


def _block(df, show_cands):
    if not len(df):
        return "_(none)_\n"
    out = []
    for _, r in df.iterrows():
        dev = f"{r.device_met}" if r.device_met is not None else "--"
        out.append(f"### `{r.unit_text}`  ·  {r.row_weight:,} rows  ·  "
                   f"{r.n_patients} patients  ·  device MET {dev}")
        out.append("")
        if r.review_because:
            out.append(f"> ⚠️ {r.review_because}")
            out.append("")
        out.append("```text")
        out.append(f"  proposed  {r.proposed_code or '--':>7s}  "
                   f"{str(r.proposed_met or '--'):>5s}  {r.proposed_activity}"
                   f"   [{r.proposed_conf}]")
        if show_cands:
            for c in r.candidates:
                code, met, desc = c.split("|", 2)
                mark = " <" if code == str(r.proposed_code) else "  "
                out.append(f"  cand      {code:>7s}  {met:>5s}  {desc}{mark}")
        out.append("```")
        out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="mcphases-v1")
    a = ap.parse_args()

    w = worksheet(a.corpus)
    folder = CORPUS / a.corpus
    w.to_parquet(folder / "I1_IDENTITY.parquet", index=False)

    rev = w[w.needs_review]
    (folder / "I1_IDENTITY.md").write_text(SHEET.format(
        corpus=a.corpus, n=len(w), n_rev=len(rev), minn=MIN_MET_N,
        review=_block(rev, True), rest=_block(w[~w.needs_review], False)))

    print(f"  {a.corpus}: {len(w)} units, {len(rev)} need a person")
    for _, r in rev.iterrows():
        print(f"    {r.unit_text:<18s} {r.row_weight:>7,d} rows  {r.review_because}")
    print(f"  wrote {folder}/I1_IDENTITY.parquet + .md")


if __name__ == "__main__":
    main()

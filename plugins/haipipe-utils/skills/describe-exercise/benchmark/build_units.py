"""
The UNIT INVENTORY of describe-exercise, one folder per corpus.

WHY THIS FILE EXISTS
================================================================================
`freeze.py` builds a ROW index: 136,555 events, one row each. That answers
"how often", never "how many different things are we asked to resolve". The
second question is the one a person can act on, because its answer is small:
180 distinct units against 136,555 rows.

MEMBERSHIP IS 'THIS CORPUS HAS EXERCISE CONTENT', NOT 'THIS CORPUS HAS AN
ANSWER'. OhioT1DM contributes one unit, the word "Unknown", and no gold at
all. It still gets a folder, because a reader must be able to tell 'we looked
and there was nothing to grade' from 'we never looked'. The corpora with no
exercise content at all are named in `_empty.md` for the same reason.

WHAT A UNIT IS DIFFERS BY CORPUS, AND THE TABLE SAYS SO
================================================================================
    id            a vendor's numeric code. Only unique WITH its source:
                  code 1001 from Validic is not code 1001 from Apple.
    name_string   free text the app or the person wrote.
    class_word    a single category word standing in for every bout.

CODE LIVES IN GIT, DATA DOES NOT. Everything written here lands under
_WorkSpace/0-RawDataStore/0-EventNorm/_ExerciseInfo/2-corpus/.

    source .venv/bin/activate && source env.sh
    python build_units.py
"""
import json
import pathlib
import sys

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))          # describe-exercise/

from spec import _weights, MIN_KG, MAX_KG, MAX_MINUTES        # noqa: E402
from taxonomy import MIN_MET, MAX_MET                          # noqa: E402
from exnorm import normalize                                   # noqa: E402

ROOT = pathlib.Path("/home/jluo41/WellDoc-SPACE")
SOURCE_STORE = ROOT / "_WorkSpace/1-SourceStore"
OUT = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_ExerciseInfo/2-corpus"

MIN_MET_N = 30          # below this a per-unit MET median is not worth reading


# ── what each corpus is, and where its exercise content actually sits ────────
# aireadi-v3 is the one that had to be looked for: its Exercise.parquet is
# empty and its named activity rides on Steps.parquet, which no earlier pass
# of this benchmark opened.
CORPORA = [
    dict(name="WellDoc", unit_is_a="id",
         cohorts=["WellDoc2022CGM", "WellDoc2025ALS",
                  "WellDoc2025CVS", "WellDoc2025LLY"],
         frame="Exercise", text="ExerciseType", src="EntrySourceID",
         dur="ExerciseDuration", kcal="CaloriesBurned"),
    dict(name="mcphases-v1", unit_is_a="name_string",
         cohorts=["mcphases-v1"],
         frame="Exercise", text="ExerciseType", src="EntrySourceID",
         dur="ExerciseDuration", kcal="CaloriesBurned"),
    dict(name="aireadi-v3", unit_is_a="name_string",
         cohorts=["aireadi-v3"],
         frame="Steps", text="ActivityName", src=None,
         dur="DurationMinutes", kcal=None),
    dict(name="OhioT1DM", unit_is_a="class_word",
         cohorts=["OhioT1DM"],
         frame="Exercise", text="ExerciseType", src="EntrySourceID",
         dur="ExerciseDuration", kcal="CaloriesBurned"),
]

# Looked at, nothing there. The reason is recorded so nobody re-checks blind.
EMPTY = [
    ("Shanghai",           "Exercise table present, 0 rows"),
    ("dubosson",           "Exercise table present, 0 rows"),
    ("aireadi-noimage-v2", "Exercise table present, 0 rows; no Steps frame either"),
    ("WellDoc2026Libre",   "Exercise table present, 0 rows"),
    ("mimiciv-3.1",        "no exercise frame of any kind"),
    ("CGMacros",           "Exercise table present, 0 rows -- but see the note below"),
]


def _load(c):
    """Every cohort of one corpus, stacked, with a uniform column naming."""
    frames = []
    for coh in c["cohorts"]:
        for f in sorted(SOURCE_STORE.glob(f"{coh}/@*/{c['frame']}.parquet")):
            d = pd.read_parquet(f)
            if not len(d):
                continue
            out = pd.DataFrame({
                "cohort": coh,
                "PatientID": d["PatientID"].astype(str),
                "text": d[c["text"]].astype(str),
                "src": (pd.to_numeric(d[c["src"]], errors="coerce")
                        if c["src"] and c["src"] in d else np.nan),
                "minutes": (pd.to_numeric(d[c["dur"]], errors="coerce")
                            if c["dur"] and c["dur"] in d else np.nan),
                "kcal": (pd.to_numeric(d[c["kcal"]], errors="coerce")
                         if c["kcal"] and c["kcal"] in d else np.nan),
            })
            out["kg"] = out.PatientID.map(
                {str(k): v for k, v in _weights(coh).items()})
            frames.append(out)
    return pd.concat(frames, ignore_index=True) if frames else None


def _met_device(d):
    """The same back-solve the row benchmark grades against, so the two agree."""
    ok = (d.kg.between(MIN_KG, MAX_KG) & d.kcal.gt(0)
          & d.minutes.between(1, MAX_MINUTES))
    met = d.kcal * 200.0 / (3.5 * d.kg * d.minutes)
    return met.where(ok & met.between(MIN_MET, MAX_MET))


def _unit_key(d):
    """A code means nothing without its vendor; free text means itself."""
    has = d.src.notna()
    return np.where(has,
                    "src" + d.src.fillna(0).astype(float).astype(int).astype(str)
                    + ":" + d.text,
                    d.text)


def _resolve(units, srcs):
    """Ask the resolver each DISTINCT thing once. 180 calls, not 136,555."""
    r = normalize(list(units),
                  source_ids=[None if pd.isna(s) else s for s in srcs])
    return pd.DataFrame(r)


def build_one(c):
    d = _load(c)
    if d is None or not len(d):
        return None
    d["met_device"] = _met_device(d)
    d["unit"] = _unit_key(d)

    g = d.groupby("unit", sort=False)
    u = pd.DataFrame({
        "unit": g.size().index,
        "unit_text": g.text.first().values,
        "source_id": g.src.first().values,
        "row_weight": g.size().values,
        "n_patients": g.PatientID.nunique().values,
        "n_cohorts": g.cohort.nunique().values,
        "met_device_n": g.met_device.count().values,
        "met_device_median": g.met_device.median().values,
        "met_device_cv": (g.met_device.std() / g.met_device.mean()).values,
    })

    res = _resolve(u.unit_text, u.source_id)
    u["resolved_conf"] = res.ExerciseConf.values
    u["resolved_code"] = res.ActivityCode.values
    u["resolved_activity"] = res.ActivityResolved.values
    # BOTH. Since the scale tier shipped, METValue is the best estimate for
    # this unit's source and METReference is the Compendium's published number.
    # A unit table that showed only one of them could not be read against the
    # Compendium OR against the device.
    u["resolved_met"] = pd.to_numeric(res.METValue, errors="coerce").values
    u["resolved_met_ref"] = pd.to_numeric(res.METReference, errors="coerce").values
    u["resolved_scale"] = res.METScale.values
    u["type_source"] = res.TypeSource.values

    # A MISS is not one thing. The resolver REFUSES a daily rollup or a
    # placeholder on purpose -- those rows are not a named bout and there is
    # nothing to resolve. An opaque_code is the only MISS that is a GAP: a
    # vendor code we hold no codebook for. Counting them together would read
    # as a failure rate and would be wrong.
    src = pd.Series(res.ExerciseSource.tolist()).fillna("").astype(str)
    u["verdict"] = np.where(
        u.resolved_conf.isin(TRUSTED).values, "resolved",
        np.where(src.str.contains("opaque_code").values, "gap",
                 np.where(src.str.startswith("not_resolvable").values,
                          "refused", "weak")))

    # A unit only carries a gold when its own MET median rests on enough rows.
    # Everything else is UNLABELLED and says so; it is not a zero.
    graded = u.met_device_n >= MIN_MET_N
    u["gold_met"] = u.met_device_median.where(graded)
    u["gold_tier"] = np.where(graded, "G1", "UNLABELLED")
    u["gold_source"] = np.where(
        graded, "back-solved from vendor kcal + Weight.parquet", "")
    u["corpus"] = c["name"]
    u["unit_is_a"] = c["unit_is_a"]

    return u.sort_values("row_weight", ascending=False).reset_index(drop=True), d


CORPUS_README = """\
# {name}

{blurb}

```text
  rows            {rows:>10,d}
  units           {units:>10,d}      a unit here is a {unit_is_a}
  patients        {pats:>10,d}
  cohorts         {cohorts}

  resolved        {resolved:>9.1%}      of UNITS the resolver answers with a
                              trusted confidence (ALIAS / CODEBOOK / EXACT)
  row-resolved    {rowres:>9.1%}      the same, weighted by how often each
                              unit actually occurs
  units with gold {ngold:>10,d}      MET median on >= {minn} rows
```

`units.parquet` is the inventory: one row per distinct thing this corpus asks
the resolver to resolve, with what it answers today. A `<SET_ID>.parquet` sits
beside it only where a gold exists.

GENERATED by `describe-exercise/benchmark/build_units.py`. Do not hand-edit.
"""

BLURB = {
    "WellDoc": (
        "Four WellDoc cohorts, stacked. Every unit is a vendor's numeric code\n"
        "and is only unique WITH its source: code 1001 from Validic and code\n"
        "1001 from Apple are two different units and are kept apart."),
    "mcphases-v1": (
        "Apple Health workout names, written by the app rather than chosen\n"
        "from a codebook. THE ONLY FREE-TEXT CORPUS with a gradeable gold, so\n"
        "it is where a naming error can actually be seen. Sixteen units."),
    "aireadi-v3": (
        "FOUND 2026-08-22, and missed by every earlier pass: aireadi-v3's\n"
        "Exercise.parquet is empty, and its named activity rides on\n"
        "Steps.parquet instead. Three units over 1,994 patients -- the widest\n"
        "population in the corpus and the narrowest vocabulary. It carries no\n"
        "calories, so it has no MET gold; it is a COVERAGE corpus, not a\n"
        "value one."),
    "OhioT1DM": (
        "One unit, the word 'Unknown', on every one of its rows. No gold, and\n"
        "none is possible. It is here so that a reader can see the shape of a\n"
        "corpus that logs exercise happened and nothing else."),
}

TRUSTED = {"ALIAS", "CODEBOOK", "EXACT"}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows_tbl, summary = [], {}

    for c in CORPORA:
        got = build_one(c)
        if got is None:
            print(f"  {c['name']:14s} -- no rows, skipped")
            continue
        u, d = got
        folder = OUT / c["name"]
        folder.mkdir(exist_ok=True)
        u.to_parquet(folder / "units.parquet", index=False)

        trusted = u.resolved_conf.isin(TRUSTED)
        resolved = float(trusted.mean())
        rowres = float(u.row_weight[trusted].sum() / u.row_weight.sum())
        ngold = int((u.gold_tier == "G1").sum())
        w = u.row_weight.sum()
        share = {"row_" + v: float(u.row_weight[u.verdict == v].sum() / w)
                 for v in ("resolved", "refused", "gap", "weak")}

        if ngold:
            sets = ["I2_VALUE"]
            v = u[u.gold_tier == "G1"].copy()
            v.to_parquet(folder / "I2_VALUE.parquet", index=False)
        else:
            sets = []

        (folder / "README.md").write_text(CORPUS_README.format(
            name=c["name"], blurb=BLURB[c["name"]], rows=len(d), units=len(u),
            pats=int(d.PatientID.nunique()), cohorts=" ".join(c["cohorts"]),
            unit_is_a=c["unit_is_a"], resolved=resolved, rowres=rowres,
            ngold=ngold, minn=MIN_MET_N))

        rows_tbl.append(dict(corpus=c["name"], rows=len(d), units=len(u),
                             unit_is_a=c["unit_is_a"],
                             patients=int(d.PatientID.nunique()),
                             resolved=resolved, rowres=rowres, ngold=ngold,
                             sets=sets, **share))
        summary[c["name"]] = dict(
            rows=len(d), units=len(u), unit_is_a=c["unit_is_a"],
            patients=int(d.PatientID.nunique()),
            units_resolved=round(resolved, 4), rows_resolved=round(rowres, 4),
            rows_refused=round(share["row_refused"], 4),
            rows_gap=round(share["row_gap"], 4),
            rows_weak=round(share["row_weak"], 4),
            units_with_gold=ngold, gold_tier="G1" if ngold else None,
            rulers=sets)
        print(f"  {c['name']:14s} rows={len(d):9,d} units={len(u):4d} "
              f"unit-res={resolved:6.1%}  rows: resolved={share['row_resolved']:6.1%} "
              f"refused={share['row_refused']:6.1%} gap={share['row_gap']:6.1%} "
              f"weak={share['row_weak']:5.1%}  gold={ngold}")

    (OUT / "_units_summary.json").write_text(json.dumps(summary, indent=1))

    tbl = "\n".join(
        f"{r['corpus']:13s}{r['rows']:>10,d}{r['units']:>7d}  "
        f"{r['unit_is_a']:13s}{r['resolved']:>7.1%}"
        f"{r['row_resolved']:>10.1%}{r['row_refused']:>9.1%}"
        f"{r['row_gap']:>6.1%}{r['row_weak']:>6.1%}{r['ngold']:>6d}"
        f"  {' '.join(r['sets']) or '--'}"
        for r in rows_tbl)
    (OUT / "README.md").write_text(ROOT_README.format(
        table=tbl, minn=MIN_MET_N,
        n_corpora=len(rows_tbl), n_empty=len(EMPTY)))

    (OUT / "_empty.md").write_text(EMPTY_MD.format(
        rows="\n".join(f"  {n:20s}{why}" for n, why in EMPTY)))
    print(f"\n  wrote {OUT}")


ROOT_README = """\
# 2-corpus

ONE FOLDER PER CORPUS, NAMED AFTER THE CORPUS. Open the folder and you know
where the data came from without opening a parquet.

MEMBERSHIP IS 'THIS CORPUS HAS EXERCISE CONTENT', NOT 'THIS CORPUS HAS AN
ANSWER'. Having a gold is a property recorded per unit, never the entry
ticket. {n_corpora} corpora are here; {n_empty} more were looked at and are named in
`_empty.md`.

Every folder holds `units.parquet`, the inventory of distinct things this
corpus asks the resolver to resolve, with what it answers today. A folder
holds a `<SET_ID>.parquet` as well only where a gold exists.

```text
corpus            rows  units  unit is a      unit%  ── share of rows ──────────  gold  rulers
                                                     resolved  refused   gap  weak
──────────────────────────────────────────────────────────────────────────────────────────
{table}
```

`unit%` counts VOCABULARY: how much of what this corpus says the resolver
answers with a trusted confidence. The four row shares count TRAFFIC, and
they are split because a MISS is not one thing:

```text
  resolved   answered, trusted
  refused    ON PURPOSE. A daily rollup or a placeholder is not a named bout;
             there is nothing to resolve and saying so is the right answer.
  gap        ⚠️ THE ONLY REAL HOLE: a vendor code we hold no codebook for.
  weak       answered, but the resolver does not trust its own match.
```

Reading `refused` as failure would be the single easiest mistake to make
here. `gap` is the number to drive down.

`gold` counts units whose device-MET median rests on at least {minn} rows.

```text
  DATA ONLY. The code that produces all of this lives in git at
  Tools/plugins/haipipe-utils/skills/describe-exercise/benchmark/

  source .venv/bin/activate && source env.sh
  python .../benchmark/build_units.py               # the inventories
  python .../benchmark/check_gold_independence.py   # the gate
  python .../benchmark/run.py --freeze --full       # the row index + readings
```

`gold_index.parquet` beside these folders is the ROW index, one row per
event, and is what `run.py` grades. The folders are the UNIT view of the same
data. Neither replaces the other.

`person_split.parquet` is a THIRD view and a second fence: each patient's own
gradeable bouts in their own time order, the first 5 marked `calib` and the
rest `eval`. The patient-hash split in `gold_index` asks whether the resolver
holds up on people it never saw; this one asks whether it improves after seeing
THIS person a few times. A personal scale factor can only be measured against
the second, because the first leaves a test patient with no history at all.
Built by `build_person_split.py`, scored by `eval_scale_tiers.py`.
"""

EMPTY_MD = """\
# corpora with no exercise content

Listed, not omitted: a reader must be able to tell 'we looked and there was
nothing' from 'we never looked'. The moment one gains rows it gets a folder
next door with no change to any of this.

```text
{rows}
```

## CGMacros deserves a sentence of its own

Its `Exercise.parquet` is empty, but `Activity.parquet` holds 657,789 rows of
per-minute Fitbit output for 45 patients: heart rate, calories, and a `METs`
column that is a MEASURED intensity, reported in tenths of a MET (a median of
11 is 1.1 MET, a person sitting still).

It is not a corpus, because it asks the resolver nothing -- there is no
activity name anywhere in it. It is a REFERENCE: an independently measured MET
series that could check the back-solve this benchmark's gold depends on. That
is a use for `3-reference/`, not a folder here.
"""


if __name__ == "__main__":
    main()

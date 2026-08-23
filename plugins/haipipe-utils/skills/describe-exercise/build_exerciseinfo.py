"""
Build _ExerciseInfo: one page per cohort, showing what goes IN and what comes OUT.

GENERATED. The producer is this file. Rerun after any Exercise frame is recooked
or any describe-exercise change:

    source .venv/bin/activate && source env.sh
    Tools/plugins/haipipe-utils/skills/describe-exercise/run_server.sh   # in another shell
    python <this file>

Mirrors _FoodInfo/1-per-cohort/, and adds the half food's pages do not have: the
OUTPUT. A food page says what the input looks like and what ground truth exists.
An exercise page says that AND what describe-exercise actually returns for it,
because the whole question here is per-cohort effect, not per-cohort shape.
"""
import glob, json, os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, "Tools/plugins/haipipe-utils/skills/describe-exercise")
from exnorm import normalize
from exnorm.codebooks import SOURCE_VENDOR

OUT = "_WorkSpace/0-RawDataStore/0-EventNorm/_ExerciseInfo"
LB = 0.45359237
ROLLUP = {"20901","20902","20903","20904","20905","20906"}


SECTIONS = [r"""## What the table says, cohort by cohort

```text
  mcphases-v1        100% free text, no vendor codes, no roll-ups.
                     The cleanest exercise data on this machine and the only
                     cohort where nearly every row resolves.

  WellDoc x4         The bulk of the data and the hardest. Two thirds of every
                     WellDoc frame is a daily device roll-up posted at local
                     midnight -- not a bout, and it must not be dosed. The
                     sessions that remain are vendor codes, now decoded through
                     Apple's and Validic's books.
                     Their spread in the MET column is NOT resolver quality; it
                     is how much of each cohort is roll-up.

  OhioT1DM           221 rows, every one of them the string 'Unknown'.
                     Duration is recorded and nothing else. Nothing to resolve,
                     and no code book will ever change that.

  CGMacros           Exercise.parquet is EMPTY -- but the cohort has 657,789
  (empty frame)      rows of minute-level device METs in Activity.parquet,
                     which describe-exercise does not read. The richest
                     intensity data here is the one this table cannot show.

  Shanghai           Exercise tables exist and are empty. No exercise data.
  dubosson
  aireadi x2         Exercise.parquet empty, but aireadi-v3 Steps.parquet
  Libre              carries 2,377,792 rows with an ActivityName. Same gap as
                     CGMacros: real activity data, in the wrong table.
```



## What is NOT in here

```text
  CGMacros/Activity.parquet          657,789 rows, minute-level device METs
  aireadi-v3/Steps.parquet         2,377,792 rows, ActivityName + duration
  AI-READI raw Garmin                    905 patients, never extracted
  WellDoc Step/Steps                 162,394 rows
```

All of it is exercise information, none of it is in an `Exercise` frame, and
`describe-exercise` therefore never sees it. That is the largest single gap in
this folder and it is a plumbing gap, not a resolver gap."""]

# The folder's SHAPE belongs to haipipe-norm, not to this file. Three
# normalizers writing three folders produced three schemas that shared two keys;
# xinfo-v1 is the one shape all four now emit, so a benchmark reading coverage,
# confidence or basis is written once.
import pathlib as _pl
import sys as _sys
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent / "haipipe-norm"))
from xinfo import CohortStats, copy_api_examples, write   # noqa: E402


def body_mass():
    w = {}
    for p in glob.glob("_WorkSpace/1-SourceStore/*/*/Weight.parquet"):
        d = pd.read_parquet(p)
        if "Weight" not in d or "PatientID" not in d:
            continue
        d = d.assign(kg=pd.to_numeric(d["Weight"], errors="coerce") * LB)
        d = d[d.kg.between(30, 300)]
        for pid, g in d.groupby("PatientID"):
            w[pid] = round(float(g.kg.median()), 1)
    return w


def block(lines):
    return "```text\n" + "\n".join(lines) + "\n```\n"


def pct(n, d):
    return f"{n/d:6.1%}" if d else "     -"


def page(coh, d, r, raw_files):
    n = len(d)
    kind = r.TypeSource.str.split("|").str[0]
    got = r.METValue.notna()
    solv = n - kind.isin(["daily_rollup", "placeholder"]).sum()
    L = [f"# {coh}\n"]

    # ---------- INPUT -------------------------------------------------
    L.append(block([
        f"rows in Exercise frame   {n:,}",
        f"patients                 {d.PatientID.nunique():,}",
        f"date span                {d.dt.min().date()} .. {d.dt.max().date()}"
        if d.dt.notna().any() else "date span                unknown",
        f"frame                    {d.__path__.iloc[0]}",
        f"namespace key present    {pct(d.EntrySourceID.notna().sum(), n)}"
        f"  ({d.EntrySourceID.notna().sum():,} rows)",
    ]))

    L.append("## What the input looks like\n")
    istext = ~d.ExerciseType.astype(str).str.fullmatch(r"\d+")
    L.append(block([
        f"free text                {istext.sum():>8,}  {pct(istext.sum(), n)}",
        f"vendor code              {(~istext).sum():>8,}  {pct((~istext).sum(), n)}",
        "",
        "field                     non-null   non-zero",
        f"  ExerciseType           {pct(d.ExerciseType.notna().sum(), n)}          -",
        f"  ExerciseDuration       {pct(pd.to_numeric(d.ExerciseDuration,errors='coerce').notna().sum(), n)}"
        f"   {pct((pd.to_numeric(d.ExerciseDuration,errors='coerce')>0).sum(), n)}",
        f"  CaloriesBurned         {pct(pd.to_numeric(d.CaloriesBurned,errors='coerce').notna().sum(), n)}"
        f"   {pct((pd.to_numeric(d.CaloriesBurned,errors='coerce')>0).sum(), n)}",
        f"  DistanceInMeters       {pct(pd.to_numeric(d.get('DistanceInMeters'),errors='coerce').notna().sum(), n) if 'DistanceInMeters' in d else '     -'}"
        f"   {pct((pd.to_numeric(d.get('DistanceInMeters'),errors='coerce')>0).sum(), n) if 'DistanceInMeters' in d else '     -'}",
        f"  body mass on file      {pct(d.kg.notna().sum(), n)}          -",
    ]))

    if d.EntrySourceID.notna().any():
        L.append("## Who issued the codes\n")
        vc = d.EntrySourceID.value_counts()
        L.append(block([
            f"{SOURCE_VENDOR.get(int(k),'?'):<20} src {int(k):<4} {v:>8,}  {pct(v,n)}"
            for k, v in vc.items()]))

    L.append("## The ten most common inputs\n")
    top = d.ExerciseType.astype(str).value_counts().head(10)
    rows = []
    for t, c in top.items():
        m = d.ExerciseType.astype(str) == t
        res = r[m.values].ActivityResolved.dropna()
        out = res.iloc[0][:44] if len(res) else "-- not resolved --"
        rows.append(f"{t:<20} {c:>7,}  ->  {out}")
    L.append(block(rows))

    # ---------- OUTPUT ------------------------------------------------
    L.append("## What describe-exercise returns\n")
    L.append(block(
        [f"{k:<14} {v:>8,}  {pct(v,n)}" for k, v in kind.value_counts().items()] +
        ["",
         f"MET written    {got.sum():>8,}  {pct(got.sum(),n)} of all rows",
         f"               {got.sum():>8,}  {pct(got.sum(),solv)} of the RESOLVABLE {solv:,}",
         f"kcal written   {r.CaloriesBurnedEst.notna().sum():>8,}  "
         f"{pct(r.CaloriesBurnedEst.notna().sum(),n)}   (needs minutes AND body mass)"]))

    L.append("## Confidence and basis\n")
    L.append(block(
        [f"conf   {k:<8} {v:>8,}" for k, v in r.ExerciseConf.value_counts().items()] + [""] +
        [f"basis  {str(k):<12} {v:>8,}" for k, v in r.ExerciseBasis.value_counts(dropna=False).items()]))

    if got.any():
        L.append("## MET actually produced\n")
        q = r.loc[got, "METValue"]
        L.append(block([
            f"n        {len(q):,}",
            f"min      {q.min():.1f}",
            f"median   {q.median():.1f}",
            f"max      {q.max():.1f}",
            "",
            "most common activities:",
        ] + [f"  {c:>7,}  MET {r.loc[got & (r.ActivityResolved==a), 'METValue'].iloc[0]:>4.1f}  {a[:46]}"
             for a, c in r.loc[got, "ActivityResolved"].value_counts().head(6).items()]))

    # ---------- IN -> OUT, real rows ----------------------------------
    L.append("## Real rows, in and out\n")
    ex = []
    seen = set()
    for i in range(len(d)):
        k = kind.iloc[i]
        if k in seen:
            continue
        seen.add(k)
        din, dout = d.iloc[i], r.iloc[i]
        ex += [
            f"IN   ExerciseType={din.ExerciseType!r}  EntrySourceID="
            f"{'-' if pd.isna(din.EntrySourceID) else int(din.EntrySourceID)}"
            f"  duration={din.ExerciseDuration}  body_mass={din.kg}",
            f"OUT  {dout.ExerciseConf:<6} MET={dout.METValue}  kcal={dout.CaloriesBurnedEst}"
            f"  basis={dout.ExerciseBasis}",
            f"     resolved  {dout.ActivityResolved}",
            f"     source    {dout.ExerciseSource}   /   {dout.TypeSource}",
            "",
        ]
        if len(seen) >= 4:
            break
    L.append(block(ex))

    L.append("## Raw files behind it\n")
    L.append(block(raw_files or ["  (none found)"]))

    # ---------- VERDICT -----------------------------------------------
    L.append("## What this cohort can and cannot support\n")
    v = []
    if got.sum() == 0:
        v.append("NOTHING. Not one row resolves.")
    else:
        v.append(f"{got.sum():,} rows carry an intensity ({pct(got.sum(),solv).strip()} of resolvable).")
    if kind.eq("daily_rollup").sum():
        v.append(f"{kind.eq('daily_rollup').sum():,} rows are DAILY DEVICE ROLL-UPS, not bouts. "
                 "Any per-session analysis must exclude them.")
    if kind.eq("opaque_code").sum():
        v.append(f"{kind.eq('opaque_code').sum():,} rows carry a vendor code with no book on this machine.")
    if r.CaloriesBurnedEst.notna().sum() == 0 and got.sum():
        v.append("NO kcal at all: body mass or duration is missing for every row. "
                 "Intensity only, on the per_minute basis.")
    if d.kg.notna().mean() < 0.5:
        v.append(f"Body mass is on file for only {d.kg.notna().mean():.0%} of rows, "
                 "which is what caps the kcal coverage.")
    L.append(block([f"- {x}" for x in v]))
    return "\n".join(L)


def main():
    os.makedirs(f"{OUT}/1-per-cohort", exist_ok=True)
    W = body_mass()
    stats, pages = [], {}
    for p in sorted(glob.glob("_WorkSpace/1-SourceStore/*/*/Exercise.parquet")):
        coh = p.split("/")[2]
        d = pd.read_parquet(p)
        if len(d) == 0:
            stats.append(CohortStats(noun="exercise", cohort=coh, rows=0)); continue
        if "EntrySourceID" not in d:
            d["EntrySourceID"] = None
        d = d.assign(kg=d.PatientID.map(W), __path__=p,
                     dt=pd.to_datetime(d.ObservationDateTime, errors="coerce", format="mixed"))
        r = pd.DataFrame(normalize(
            d.ExerciseType.astype(str).tolist(),
            minutes=[None if pd.isna(x) else float(x) for x in d.ExerciseDuration],
            weight_kg=[None if pd.isna(x) else float(x) for x in d.kg],
            source_ids=[None if pd.isna(x) else int(x) for x in d.EntrySourceID]))
        raw = sorted(glob.glob(f"_WorkSpace/0-RawDataStore/{coh}/**/*Exercise*", recursive=True))[:6]
        pages[coh] = page(coh, d.reset_index(drop=True), r, raw)
        kind = r.TypeSource.str.split("|").str[0]
        never = kind.isin(["daily_rollup", "placeholder"])
        # A row whose CaloriesBurned the device recorded can have its MET
        # back-solved from kcal, weight and minutes -- an estimate INDEPENDENT
        # of the compendium lookup, and the only thing here that can grade it.
        kcal_logged = pd.to_numeric(d.get("CaloriesBurned"), errors="coerce")
        gradeable = {}
        n_back = int(((kcal_logged > 0) & d.kg.notna()
                      & (pd.to_numeric(d.ExerciseDuration, errors="coerce") > 0)
                      & ~never.values).sum())
        if n_back:
            gradeable["backsolved_met"] = n_back
        stats.append(CohortStats(
            noun="exercise", cohort=coh, rows=len(d),
            patients=int(d.PatientID.nunique()),
            kinds=kind.value_counts().to_dict(),
            denominator={"resolvable": int((~never).sum()),
                         "excluded": kind[never].value_counts().to_dict()},
            coverage={"value_written": int(r.METValue.notna().sum())},
            confidence=r.ExerciseConf.value_counts().to_dict(),
            # GOOD is UNREACHABLE for this noun and that is deliberate: the PA
            # Compendium on this machine is a third-party mirror, not the
            # publisher's file, so retrieve.CONF_CAP caps everything at OK.
            confidence_order=["GOOD", "OK", "ALIAS", "WEAK", "MISS"],
            trusted=["GOOD", "OK", "ALIAS"],
            basis={str(k): int(v) for k, v in
                   r.ExerciseBasis.value_counts(dropna=False).items()},
            gradeable=gradeable))
        print(f"  {coh:20s} {len(d):>7,} in  ->  MET {r.METValue.notna().sum():>6,}")
    n_ex = copy_api_examples(_pl.Path(OUT), _pl.Path(__file__).resolve().parent / "examples" / "api")
    rep = write(
        noun="exercise", emoji="🏃",
        tagline="Every cohort's exercise data, in and out, on one page each.",
        producer="Tools/plugins/haipipe-utils/skills/describe-exercise/build_exerciseinfo.py",
        rerun=("source .venv/bin/activate && source env.sh\n"
               "Tools/plugins/haipipe-utils/skills/describe-exercise/run_server.sh   # another shell\n"
               "python Tools/plugins/haipipe-utils/skills/describe-exercise/build_exerciseinfo.py"),
        dest=OUT, stats=stats, pages=pages, sections=SECTIONS)
    print(f"\nwrote {rep['dest']}  ·  {rep['cohorts']} cohorts  ·  "
          f"{n_ex} api examples  ·  conforming: {not rep['problems']}")
    return stats, pages


if __name__ == "__main__":
    main()

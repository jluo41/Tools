---
name: describe-exercise
description: "Normalize a logged activity (any cohort's dialect, free text or vendor code) to a PA Compendium MET and, when minutes and body mass are known, an estimated kcal. Use when an Exercise ProcName's ExerciseType column needs energy or intensity, when a SourceFn must enrich exercise data, or when a cohort's activity codes must be typed before analysis. Trigger: describe exercise, exercise to MET, activity to calories, resolve ExerciseType, compendium, exnorm, 运动归一化."
metadata:
  version: "0.5.0"
  last_updated: "2026-08-22"
  measured: "98.0% of the resolvable set (41,931 of 42,799); 30.7% of all 136,555 rows, because 64.8% are daily device roll-ups that must not resolve. Held-out MET error, by-patient fence: MAE 1.71 r 0.520 with the device tier (1.89 / 0.440 without). By-time fence, 24,390 rows, cumulative rungs: population 1.70/0.387, device 1.50/0.506, person 1.34/0.608, person_activity 1.30/0.622"
  parked: "103 Validic 9002 rows, the last vendor code with no book; Google_Fit gained one 260822"
---

Skill: describe-exercise
================================================================================

Turn one logged activity into a MET, and -- only when the log stated minutes and
the patient's mass is known -- an estimated kcal, with provenance attached to
every number.

    from exnorm import normalize
    normalize(["Walking"], minutes=30, weight_kg=82)

    curl -sS localhost:8078/normalize -H 'content-type: application/json' \
         -d '{"activity":"Walking","minutes":30,"weight_kg":82}'

Member of the `haipipe-norm` family; read that contract first. Sibling:
`describe-food`.


THE ONE-MINUTE VERSION
--------------------------------------------------------------------------------

```text
  ExerciseType + EntrySourceID, as the cohort wrote them
        │
        ├─ codebooks.py ─ a vendor code becomes a LABEL
        │                   apple    HKWorkoutActivityType, 81 cases
        │                   validic  ExternalExerciseType, 100 codes
        │                   welldoc  InternalExerciseType, 17 codes
        │                 a code is read ONLY in its own issuer's book
        │
        ├─ dialect.py ── types it as one of FOUR things ─────────────────┐
        │                                                                │
        │    session       a bounded bout            41,485  30.4%   ────┤ only
        │    daily_rollup  a device's midnight total 88,467  64.8%   ✋   │ this
        │    placeholder   named nothing              5,289   3.9%   ✋   │ one
        │    opaque_code   a vendor enum, no codebook  1,314   1.0%  ✋   │ goes on
        │                                                                │
        ├─ retrieve.py ── PA Compendium 2024, 1,111 activities ──────────┘
        │                    ALIAS  a person picked this entry  -> value written
        │                    WEAK   fuzzy candidate             -> value WITHHELD
        │                    MISS   nothing                     -> value withheld
        │
        └─ aggregate.py ─ MET × 3.5 × kg / 200 × min = kcal
                          missing minutes or mass -> no kcal, basis says so

  11 fields out, the same 11 on a hit and on a miss:
     values      METValue · ActiveMinutes · CaloriesBurnedEst
     identity    ActivityResolved · ActivityCode · MajorHeading
     provenance  ExerciseSource · ExerciseConf · ExerciseBasis
                 TypeSource · TypeConf   <- how the NAME was obtained:
                    session|text              a patient wrote words
                    session|codebook:apple    read off a vendor enum
```


WHAT IT ACTUALLY DELIVERS, MEASURED
--------------------------------------------------------------------------------

Over all 136,555 Exercise rows in `1-SourceStore`, 2026-08-22:

    of the 42,799 RESOLVABLE rows    40,767 resolve      95.3%
    of all 136,555 rows              40,767 resolve      29.9%

QUOTE THE FIRST NUMBER, and know why. 88,467 rows are daily device roll-ups and
5,289 named nothing; neither should ever carry a MET, so neither belongs in the
denominator of a coverage claim. 29.9% is what a naive `notna().mean()` reports
and it measures the shape of the log, not the quality of the resolver.

Where the 40,767 names came from:

    session|codebook:validic   15,196     WellDoc's data dictionary
    session|codebook:apple     13,786     Apple's HKWorkoutActivityType
    session|text               11,785     a patient's own words

Per cohort: mcphases-v1 96.5%, WellDoc2025ALS 48.9%, WellDoc2025CVS 31.2%,
WellDoc2025LLY 23.1%, WellDoc2022CGM 21.9%, OhioT1DM 0.0% (221 rows, all
'Unknown'). The WellDoc spread is not resolver quality -- it is how much of each
cohort is device roll-up.

Of the 32 distinct free-text values, 28 name an activity and all 28 resolve.
The four that do not are `Other`, `Sports`, `Sport`, `Unknown` -- which name no
activity. There is no third category. That is the useful property here: this
normalizer fails exactly where the log failed, and nowhere else.


THE FIVE RULES, AS THEY LAND HERE
--------------------------------------------------------------------------------

1. ONE DOOR
   `normalize()` and nothing else. It takes `minutes`, `weight_kg` and
   `source_ids` beyond the item list, and each is a SCALE or a KEY -- none can
   change WHICH activity is resolved. Omit them all and it behaves exactly like
   food's door: strings in, records out, on the per_minute basis.

2. TYPE, DO NOT DELETE
   Four kinds, above. A roll-up filtered out would make a cohort read as 9%
   coverage of nothing; typed, it reads as 88,394 rows that were never bouts.

3. TRUSTED ONLY
   ALIAS writes. WEAK and MISS write NULL. The fuzzy tier may NEVER write a
   value -- see PARKED below for why that is a floor and not a knob.

4. BASIS IS A COLUMN
   MET is a rate, kcal is a dose, and the bridge needs both minutes and body
   mass. There is no default body mass anywhere in this package.

       minutes  mass   →  ExerciseBasis   kcal?
       yes      yes       per_session     yes
       yes      no        per_minute      no
       no       yes       per_minute      no
       no       no        per_minute      no

5. PROVENANCE NEVER FOLDS
   Four kinds of not-knowing get four distinct `ExerciseSource` strings:
   `not_resolvable:daily_rollup`, `not_resolvable:opaque_code`,
   `not_resolvable:placeholder`, `compendium2024:no_match`. They have four
   different fixes, so they may not share a column.


THE TWO DEFECTS THIS PACKAGE EXISTS TO PREVENT
--------------------------------------------------------------------------------

**The church supper.** The PA Compendium uses 5-digit activity codes, and three
of them collide with WellDoc's EntrySourceID-20 codes by pure coincidence:

    WellDoc 20050   median 42 min, 242 kcal  │  Compendium 20050  "Eating at church", MET 1.5
    WellDoc 20037   median 32 min, 204 kcal  │  Compendium 20037  "Walking, 2.8-3.4 mph"
    WellDoc 20020   median 30 min, 142 kcal  │  Compendium 20020  "Standing, singing in church"

Joining on the bare integer prices 1,218 real workouts as a church supper. The
join is refused by `dialect.reject_code_join`, which is a raise and not a
comment, and covered by three tests.

**The midnight workout.** Codes 20901/20903/20905 carry 88,394 rows and show
1.04 rows per patient per DAY, only 10 distinct times-of-day across all of them
(every one at 03:59 or 04:59, i.e. local midnight), and CaloriesBurned == 0 in
100.0% of cases. They are daily device summaries. Priced as bouts they claim a
patient did one 11-minute workout every day for four years and never burned a
calorie.


THE CODE BOOKS — WHERE A CODE BECOMES A NAME
--------------------------------------------------------------------------------

`ExerciseType` is a vendor enum and `EntrySourceID` says whose. Measured over
220,528 raw WellDoc rows, that key partitions the 129 distinct codes into four
disjoint spaces (one code, `25`, overlaps, 5,848 rows against 1):

    EntrySourceID           vendor                    codes   book
    ----------------------------------------------------------------------
    20                      AppleHealthKit               54   HKWorkoutActivityType
    23/24/25/34/35/36       Validic (6 vendors, one
                            aggregated enum)             35   ExternalExerciseType
    1/2                     Mobile / Web                 13   InternalExerciseType
    37/40                   Google_Fit                   24   NONE

`codebooks.py` holds all three, transcribed from their sources and nothing else
-- no MET, no policy. A code becomes a LABEL there; `alias_dict.py` turns a
label into a MET. That separation is what lets a book be re-transcribed without
touching a curated judgement.

APPLE'S CODES ARE `20` + THE ENUM, and the evidence is structural, not a hunch.
Of the 54 distinct ns20 codes in `1-SourceStore`, 47 strip to a valid
`HKWorkoutActivityType` case and 7 do not -- and those 7 are exactly
20901..20906 and 20999, one contiguous private band. A wrong hypothesis does not
miss in a single clean block. It was independently corroborated before the enum
was fetched, by back-solving MET from each row's own `CaloriesBurned`:
Spearman rho 0.609, p 0.036, over the 12 codes with n >= 80, with yoga landing
at 2.38 against the compendium's 2.3.

FOUR DIALECTS, ONE PICK. A patient typing `Walk`, Apple's 52, Validic's 1001 and
the app's 100 all fold to `walking` and reach compendium 17190. One curated
entry to maintain instead of four, and `TypeSource` still distinguishes them:
`session|text` versus `session|codebook:apple`.

DECODING IS NOT NAMING. Validic 25 decodes perfectly, to `Other`, 3,308 rows. It
is a placeholder, and `TypeConf` still records that a book was consulted.


PARKED — WHAT THIS CANNOT DO, AND WHY
--------------------------------------------------------------------------------

**Google_Fit, 1,210 rows, 24 codes (`30001`..`30122`).** The one namespace with
no book. Not in WellDoc's dictionary and not obviously a public enum. This is a
KNOWN unknown and is typed `opaque_code`, which is deliberately NOT the same
value as a bank miss.

**Validic code 9002, 103 rows.** Present in the dictionary with a BLANK label.
A gap in the source spreadsheet, not in this package.

**The fuzzy tier may not write a value, and tightening it will not change that.**
'Sports' -- 714 rows -- head-anchors at a perfect score onto 'Sports spectator,
very excited'. The query genuinely does not identify an activity, so no scorer
fixes the class; only a person adding a line to `alias_dict.py` does. Four of
the curated picks exist precisely because the fuzzy top hit was actively wrong,
and `test_exnorm.t_curated_picks_beat_the_fuzzy_tier` will fail if a refactor
ever routes them back through `search()`:

    'cycling'                    -> 'Aquatic cycling, 90+ RPM'
    'mind and body'              -> 'Body weight resistance exercises'
    'preparation and recovery'   -> 'Cooking or food preparation, walking'
    'traditional strength ...'   -> 'Pilates, traditional, mat'

**GOOD is unreachable.** The bank is a third-party mirror of the 2024
Compendium (pacompendium.com returns 403 to non-browser clients). It passes
every available structural check -- 1,111 of the paper's 1,114 activities,
standard 5-digit codes, all 22 major headings -- and it is still not the
publisher's file, so `retrieve.CONF_CAP` caps confidence at OK. See
`_WorkSpace/ExternalStore/pa_compendium/PROVENANCE.md`.

**A bare noun is read as MODERATE effort.** Twelve level-walking entries span
2.3 to 8.5 MET, a 3.7x spread, and 'Walking' picks none of them on evidence.
Every pick and its reason is written out in `alias_dict.py`. It is a defensible
population default and nothing more.

**Two things still on the table, neither blocked by anything.**
`CaloriesBurned` + body mass + minutes back-solves MET for 24,253 WellDoc rows
without any book at all, and CGMacros carries 657,789 rows of device-estimated
MET at one-minute cadence. Both are independent of the naming route and would
cross-check it.


LAYOUT
--------------------------------------------------------------------------------

```text
  describe-exercise/
    exnorm/
      client.py      normalize() + the local|http transport switch
      dialect.py     ExerciseType (+ EntrySourceID) -> a TYPED activity
      codebooks.py   the three vendor enums, transcribed. no MET, no policy
      alias_dict.py  63 curated activity -> compendium picks, each with its why
      met_db.py      the compendium, in memory; exact + fuzzy lookup
      retrieve.py    the ALIAS / WEAK / MISS ladder and the confidence cap
      aggregate.py   MET -> kcal, and the basis column
      enrich.py      the DataFrame path, for a SourceFn holding a whole frame
      constants.py   the vocabulary: four kinds, five confidences, three bases
    server.py        FastAPI: /healthz /normalize /normalize/batch
    run_server.sh    starts it on :8078 from a bare shell
    test_exnorm.py   34 resolver tests
    test_server.py   15 service tests
    examples/        21 real request/response pairs, generated

  _WorkSpace/ExternalStore/pa_compendium/
    compendium_2024.csv   the bank, 1,111 activities
    PROVENANCE.md         where it came from and why GOOD is capped

  _WorkSpace/0-RawDataStore/_WellDocInfo/Dictionary/
    from-gdrive/          WellDoc's own dictionary, mirrored from the shared drive
    parsed/               EntrySourceID + Internal/ExternalExerciseType as CSV
    README.md             what it unlocked, and what it still does not cover
```


HOW TO USE IT
--------------------------------------------------------------------------------

```bash
# as a service (a consumer needs NO python environment)
Tools/plugins/haipipe-utils/skills/describe-exercise/run_server.sh
curl -sS "$EXNORM_URL/normalize/batch" -H 'content-type: application/json' \
  -d '{"activities":["Walking","Yoga"],"minutes":[30,45],"weight_kg":82}'

# in process (env.sh already puts this dir on PYTHONPATH)
python -c "from exnorm import normalize; print(normalize(['Walking'], minutes=30, weight_kg=82))"

# a whole frame
python -c "
import pandas as pd
from exnorm.enrich import enrich_exercise
df = pd.read_parquet('_WorkSpace/1-SourceStore/WellDoc2025ALS/@WellDocDataV251226/Exercise.parquet')
print(enrich_exercise(df, weight_kg=82).ExerciseConf.value_counts())"

# the suites
cd Tools/plugins/haipipe-utils/skills/describe-exercise
PYTHONPATH=. python test_exnorm.py && python test_server.py
```

`EXNORM_URL` (default `http://127.0.0.1:8078`), `EXNORM_TRANSPORT`
(`local` | `http`), `EXNORM_DB`, `EXNORM_MAX_BATCH`, `EXNORM_PORT`.

The service is NOT authenticated and binds 127.0.0.1. Exercise logs are PHI;
put auth in front of it before it listens on anything routable.

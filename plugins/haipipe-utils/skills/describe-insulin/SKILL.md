---
name: describe-insulin
description: "Turn an insulin product name into pharmacokinetic parameters: class, onset, peak, duration. Consumes describe-medication's DrugKey, and also serves cohorts that name only an insulin CLASS (OhioT1DM) or a product the FDA Directory does not list (Shanghai). Use when insulin-on-board or insulin action timing is needed, or when insulin rows must be classified rapid/short/intermediate/long/ultra-long/premix. Trigger: describe insulin, insulin PK, onset peak duration, IOB, insulin on board, DIA, basal bolus, insnorm, 胰岛素药代."
metadata:
  version: "0.1.0"
  last_updated: "2026-08-22"
  measured: "263,417 of 263,491 insulin rows get an action curve or a stated reason not to; on MEPS the molecule is right 93.6% of the time it answers; against 1,831 prescriber-recorded DIAs the table runs 0.5 h short on rapid analogues"
  chain: "consumes describe-medication's DrugKey"
---

Skill: describe-insulin
================================================================================

Turn an insulin product name into the parameters of its action curve.

    from insnorm import normalize
    normalize(["Insulin lispro-aabc"])
    normalize(["basal insulin"], dia_hours=[7.0])      # a per-patient override
    normalize(["Novolin R"], delivery=["iv"])          # the route the log stated

    curl -sS localhost:8080/normalize -H 'content-type: application/json' \
         -d '{"item":"Insulin lispro-aabc"}'

Member of the `haipipe-norm` family, and the second half of a CHAIN with
`describe-medication`.


WHY THIS IS A SEPARATE SKILL AND NOT A LANE INSIDE describe-medication
--------------------------------------------------------------------------------

Not because insulin is special. Because the two skills reach DIFFERENT ROWS.

Measured per cohort in `_InsInfo/README.md`, which is the artifact that settles
this. Insulin rows, what the first half resolved, what this skill resolved, and
the column that matters -- rows ONLY this skill reached:

```text
  cohort              insulin rows   med resolved   ins resolved   ONLY ins
  ──────────────────────────────────────────────────────────────────────────
  WellDoc2025LLY           234,825        234,825        234,825          0
  WellDoc2022CGM            16,939         16,939         16,939          0
  OhioT1DM                   5,026          2,610          5,026      2,416
  Shanghai                   3,490            779          3,416      2,638
  WellDoc2025CVS             2,617          2,617          2,617          0
  WellDoc2025ALS               594            594            594          0
  ──────────────────────────────────────────────────────────────────────────
  TOTAL                    263,491                                    5,054
```

5,054 insulin rows resolve HERE and nowhere in describe-medication. One skill
could not hold that without emitting rows whose identity failed while their
class was known -- a record that contradicts itself.

THIS NUMBER MOVES, AND EVERY MOVE SO FAR WAS A FIX. Do not quote it from here;
`_InsInfo/README.md` recomputes it and `_InsInfo/_seam.json` holds it.

    8,364   the original claim, and simply wrong: it added OhioT1DM's 5,026 to
            ALL 3,338 of Shanghai's insulin rows, as if none of them resolved in
            the first half. 779 do.
    5,445   the first real measurement, once insulin had a folder to count in.
    2,835   after the Ohio SourceFn began carrying `insulin_type` (260822).
            Naming the product moved 2,610 rows from 'only insulin could reach
            this' to 'both halves did' -- the exclusive count going DOWN is the
            chain getting healthier, not the argument getting weaker.
    5,054   after the Shanghai SourceFn began lifting the drug out of the
            COLUMN HEADER (260822). 2,247 of its rows held only a pump rate,
            with 'Novolin R' named once in the header; they resolve here and not
            in the FDA Directory, so the exclusive count went back UP. Same day,
            both directions: the number tracks the data, not the argument.

They are still not siblings a caller picks between: nothing can tell whether
MedicationID 612997 is insulin until it has been resolved, so the ORDER IS
FIXED and the seam is a string.

```text
   raw row ──▶ describe-medication ──▶ DrugKey ──▶ describe-insulin
                                       "insulin lispro"
                                       "Novolin R"
                                       "basal insulin"
```


WHAT COMES BACK IS PARAMETERS, NOT A CURVE
--------------------------------------------------------------------------------

    InsulinClass   rapid | short | intermediate | long | ultra_long | premix
    OnsetMin       time to the start of effect
    PeakMin        time to maximum effect, or NULL when the drug is PEAKLESS
    DurationMin    time until the effect is no longer meaningful
    Biphasic       true for premixes, where one triple is an approximation
    DeliveryMode   the route the LOG stated, echoed back  (rule 9)
    PKBasis        the scale these numbers are ON         (rule 4)
    InsulinResolved · PKSource · PKConf

**A ROUTE CHANGES WHETHER THE NUMBERS APPLY AT ALL**, which is why `PKBasis`
exists as of 260822. This skill used to declare that rule 4 had nothing to
govern -- onset, peak and duration are properties of the drug, not of the dose.
Shanghai's 29 INTRAVENOUS rows falsified that: with no subcutaneous depot there
is no absorption phase, and they were receiving a 4.5-hour subcutaneous curve.

    subcutaneous_bolus       an injection or a pump bolus. the reference case.
    subcutaneous_rate        a pump BASAL. the numbers are right; the scale is a
                             rate in units per hour, not one discrete dose.
    intravenous              NO numbers. rule 3: a confidently wrong duration is
                             worse than a missing one. the DRUG is still named,
                             because knowing the drug and having a usable curve
                             are two facts (rule 5).
    subcutaneous_reference   the log did not state a route. these are the
                             table's reference values, said out loud rather than
                             passed off as this row's route.

**Insulin-on-board is deliberately NOT computed here.** Turning
(onset, peak, duration) into an IOB series is a convolution over a 5-minute
grid, which is a RecordFn's job. A normalizer answers one row with one row; put
the curve in here and the door stops being the family's door.

**PeakMin is NULL, never 0, for glargine and degludec.** They are peakless by
design. A consumer reading 0 would place the maximum effect at the moment of
injection.


WHAT IT DELIVERS, MEASURED
--------------------------------------------------------------------------------

Over the 247,207 rows describe-medication types as insulin, 2026-08-22:

    PK parameters returned    247,193   99.99%
      OK      the label table  246,944
      ALIAS   a combination        239
      MISS                          14   'temporarily suspend insulin
                                          delivery' -- a pump EVENT, not a drug

    rapid       212,061   85.8%
    long         29,387   11.9%
    ultra_long    2,693    1.1%
    short         2,654    1.1%
    premix          388    0.2%

24 distinct drug keys appear across all three dialects and the top 12 cover
99.8%, which is why the bank is a hand-written table and not a download.


CONFIDENCE, AND THE ONE WAY TO REACH GOOD
--------------------------------------------------------------------------------

    GOOD   the caller supplied a DIA measured on THIS patient
    OK     the curated table -- population values from FDA labels
    ALIAS  a combination product resolved to its insulin component
    MISS   not an insulin this table knows

The table's numbers are POPULATION values for a typical subcutaneous dose in a
typical adult, read from FDA prescribing information and cross-read against the
ADA Standards of Care. Real onset and duration move with dose, injection site,
temperature and body composition; a 4-hour rapid-analogue duration is a
3-to-5-hour range wearing one number. Nothing from the table may be stamped
GOOD.

WellDoc's `MedPrescription` carries `DIA` -- a duration of insulin action
measured per patient -- on 15.7% of prescriptions, values 5.0 / 7.0 / 2.0 hours.
Pass it as `dia_hours` and it overrides the DURATION only; onset and peak stay
the table's, and `PKSource` keeps both halves visible
(`patient_dia:7.0h+label_table:basal insulin`).


PARKED
--------------------------------------------------------------------------------

**The IOB convolution.** The thing all of this is for. It belongs in a RecordFn
that reads these parameters and emits a per-5-minute series, the same shape
argued for exercise intensity.

**`InsulinType` in MedRegimen.** Codes 7 / 8 / 9 on 4.4% of schedule rows, with
no codebook on this machine. It would give the prescriber's own classification
to check this table against.

**Concentration.** U-100 vs U-200 vs U-300 changes volume, not units, so it does
not change the dose in IU -- but glargine U-300 has a genuinely flatter and
longer profile than U-100, and only an explicit 'Toujeo' in the name reaches
that row today.


LAYOUT
--------------------------------------------------------------------------------

```text
  describe-insulin/
    insnorm/
      client.py     normalize() + the local|http transport switch
      pk_table.py   17 products, 37 aliases, 2 combinations, each with its cite
      __init__.py
    server.py       FastAPI: /healthz /normalize /normalize/batch
    run_server.sh   starts it on :8080 from a bare shell
    test_insnorm.py 15 resolver tests
    test_server.py  11 service tests
```

Examples for both halves of the chain live in
`../describe-medication/examples/`.


HOW TO USE IT
--------------------------------------------------------------------------------

```bash
Tools/plugins/haipipe-utils/skills/describe-insulin/run_server.sh
curl -sS "$INSNORM_URL/normalize/batch" -H 'content-type: application/json' \
  -d '{"items":["Insulin lispro","Insulin glargine"]}'

python -c "from insnorm import normalize; print(normalize(['basal insulin'], dia_hours=[7]))"

cd Tools/plugins/haipipe-utils/skills/describe-insulin
PYTHONPATH=. python test_insnorm.py && python test_server.py
```

`INSNORM_URL` (default `http://127.0.0.1:8080`), `INSNORM_TRANSPORT`,
`INSNORM_MAX_BATCH`, `INSNORM_PORT`.

NOT authenticated, binds 127.0.0.1. Insulin logs are PHI.

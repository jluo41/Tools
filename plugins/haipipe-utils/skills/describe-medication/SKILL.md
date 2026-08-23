---
name: describe-medication
description: "Normalize a logged medication (any cohort's dialect: a WellDoc MedicationID, an OhioT1DM drug class, a Shanghai free-text string) to an FDA-identified drug with a dose that states its own unit. Use when a Medication ProcName needs a drug name, an NDC, a pharmacologic class, or a dose scale, or when a SourceFn must enrich medication data. Trigger: describe medication, medication to drug name, resolve MedicationID, NDC, RxNorm, dose unit, mednorm, 药物归一化."
metadata:
  version: "0.1.0"
  last_updated: "2026-08-22"
  summary: "The skill IS the library: mednorm/ ships here, reached through normalize() or an HTTP URL."
  measured: "82.8% of 397,204 administrations get an FDA ingredient; 82.7% get a dose unit; 62.2% typed as insulin"
  chain: "emits DrugKey, which describe-insulin consumes"
---

Skill: describe-medication
================================================================================

Turn one logged medication into an FDA-identified drug and a dose that carries
its own unit.

    from mednorm import normalize
    normalize(["612997"], doses=[39])

    curl -sS localhost:8079/normalize -H 'content-type: application/json' \
         -d '{"item":"612997","dose":39}'

Member of the `haipipe-norm` family; read that contract first. Siblings:
`describe-food`, `describe-exercise`, and `describe-insulin`, which is the
second half of a CHAIN with this one.


THE ONE-MINUTE VERSION
--------------------------------------------------------------------------------

```text
  a logged medication row, in one of three dialects
        │
        ├─ dialect.py ── types it ───────────────────────────────────────┐
        │    coded         a WellDoc MedicationID       386,373  97.3%   │
        │    named         a drug string (Shanghai)       5,805   1.5%   │
        │    class_only    a class (OhioT1DM)             5,026   1.3%  ✋ no bank
        │    sentinel      Dose 255 / id 1999999          ~7,100   1.8%  ✋
        │    placeholder   nothing named                                ✋
        │                                                                │
        ├─ bank.py ─── the LEXICON, ours: 871 MedicationID -> name + NDC │
        │              the BANK, FDA's:  115,496 products ───────────────┘
        │
        ├─ retrieve.py ─ A  NDC        -> FDA product            GOOD   11.0%
        │                B  generic    -> NONPROPRIETARYNAME     OK     69.9%
        │                C  brand      -> PROPRIETARYNAME        OK      2.7%
        │                B2 salt-stripped prefix                 ALIAS   0.2%
        │                -  nothing                              MISS
        │
        └─ aggregate.py ─ the dose's unit, decided by the DRUG

  13 fields out, the same 13 on a hit and on a miss:
     values      DoseValue · DoseUnit · DoseBasis
     identity    DrugKey · Ingredient · BrandName · PharmClass
                 DosageForm · Route · NDC
     provenance  MedSource · MedConf · IsInsulin
```


WHAT IT ACTUALLY DELIVERS, MEASURED
--------------------------------------------------------------------------------

Over all 397,204 Medication rows in `1-SourceStore`, 2026-08-22:

    an FDA ingredient name    328,900   82.8%
    a dose with a unit        328,474   82.7%
    typed as insulin          247,207   62.2%

    OhioT1DM            5,026   ingredient   0.0%   insulin 100.0%
    Shanghai            5,805                41.8%           57.9%
    WellDoc2022CGM     89,731                58.7%           10.6%
    WellDoc2025ALS      5,591                77.3%            5.1%
    WellDoc2025CVS     39,758                59.2%            2.0%
    WellDoc2025LLY    251,293                94.4%           90.8%

OhioT1DM's 0.0% is CORRECT, not a failure: it logs a therapeutic class and no
product directory can resolve one. Those rows are typed `class_only`, keep
IsInsulin true, and are served in full by describe-insulin.


THE FIVE RULES, AS THEY LAND HERE
--------------------------------------------------------------------------------

1. ONE DOOR
   `normalize()` takes `doses` and `payloads` beyond the item list. Neither can
   change WHICH drug is resolved: a dose is a quantity, and the payload is where
   two of the three cohorts keep the drug at all.

2. TYPE, DO NOT DELETE
   Five kinds, above. A sentinel dose of 255 is not 255 units.

3. TRUSTED ONLY
   GOOD / OK / ALIAS write an identity; MISS writes null.

4. BASIS IS A COLUMN
   `Dose` is a bare float and NOTHING in the pipeline states its unit. Insulin
   rows have a median dose of 7 and everything else a median of 1, because the
   app asks how many TABLETS were taken. So the unit is decided after the drug
   is known, and when it cannot be decided both DoseUnit and DoseBasis are null.

5. PROVENANCE NEVER FOLDS
   Five distinct `MedSource` prefixes for five different not-knowings:
   `not_resolvable:placeholder`, `not_resolvable:sentinel`, `lexicon:no_such_id`,
   `class_only:<class>`, `fda:no_match`. Different fixes, different values.


DRUGKEY — THE SEAM TO describe-insulin
--------------------------------------------------------------------------------

`Ingredient` is the FDA's word for the drug and is null whenever the Directory
does not list it. `DrugKey` is the best string available: the FDA ingredient
when there is one, otherwise the words the log itself used.

Routing on Ingredient alone would send NOWHERE:

    all 5,026 OhioT1DM rows     they name a class, never a product
    77.7% of Shanghai's insulin 'Novolin R' and 'insulin degludec' are not in
                                the FDA Directory -- 2,711 of the 3,490 rows
                                its sheet column declares as insulin

(This line read 57.9% until _InsInfo measured it. 57.9% is the share of ALL
Shanghai rows TYPED as insulin, not the share of its insulin the Directory
misses; the two were used interchangeably.)

DrugKey is non-null on 100% of insulin rows, and it is what describe-insulin
consumes. This is the same trick describe-food uses when a photo becomes a food
name and rejoins the ordinary path: THE SEAM IS A STRING.


WHY GOOD IS REACHABLE HERE
--------------------------------------------------------------------------------

describe-exercise caps its confidence at OK because its bank is a third-party
mirror. This bank is `accessdata.fda.gov`'s own file, so an NDC that resolves in
it earns GOOD. A NAME match does not, however exact: two products can share a
generic name and differ in salt, strength, route and form.

The Directory lists only CURRENTLY MARKETED products, which is why tier A
reaches 11.0% while 87.4% of rows carry an NDC. The name tiers exist because of
that, not instead of it.


PARKED
--------------------------------------------------------------------------------

**12.6% of rows carry a MedicationID absent from the lexicon.** 47,320 rows.
The lexicon is built from `ImportedMedication`, which covers 871 of the 1,373
ids that appear in administrations. Nothing on this machine names the rest.

**RxNorm is not wired in.** The FDA Directory gives an ingredient and a
pharmacologic class, which is enough to say what a drug IS. RxNorm would add
normalised ingredient identity across brands and strengths (RXCUI) and make two
spellings of the same molecule provably one thing. Its API is free and needs no
key.

**Dose is per-administration only.** `MedRegimen` carries prescribed daily
totals, insulin-to-carb ratios and correction factors, and this skill does not
read them. `DoseBasis` already has `per_day` reserved.


LAYOUT
--------------------------------------------------------------------------------

```text
  describe-medication/
    mednorm/
      client.py      normalize() + the local|http transport switch
      dialect.py     three dialects -> a TYPED item
      bank.py        the FDA bank and our lexicon, in memory
      retrieve.py    the A / B / C / B2 ladder
      aggregate.py   the dose's unit and basis, and IsInsulin
      constants.py   the vocabulary
    server.py        FastAPI: /healthz /normalize /normalize/batch
    run_server.sh    starts it on :8079 from a bare shell
    test_mednorm.py  24 resolver tests
    test_server.py   12 service tests
    examples/        20 real request/response pairs, both skills

  _WorkSpace/ExternalStore/medbank/
    fda_ndc_product.parquet   115,496 FDA products    the BANK
    med_lexicon.parquet       871 MedicationID        the LEXICON
    PROVENANCE.md
```

Rebuild the banks with
`code/scripts/haibuilder/0-external/e14_build_external_medbank.py`.


HOW TO USE IT
--------------------------------------------------------------------------------

```bash
# as a service (a consumer needs NO python environment)
Tools/plugins/haipipe-utils/skills/describe-medication/run_server.sh
curl -sS "$MEDNORM_URL/normalize/batch" -H 'content-type: application/json' \
  -d '{"items":["612997","155744"],"doses":[39,1]}'

# in process (env.sh already puts this dir on PYTHONPATH)
python -c "from mednorm import normalize; print(normalize(['612997'], doses=[39]))"

# the suites
cd Tools/plugins/haipipe-utils/skills/describe-medication
PYTHONPATH=. python test_mednorm.py && python test_server.py
```

`MEDNORM_URL` (default `http://127.0.0.1:8079`), `MEDNORM_TRANSPORT`
(`local` | `http`), `MEDNORM_DB`, `MEDNORM_MAX_BATCH`, `MEDNORM_PORT`.

NOT authenticated, binds 127.0.0.1. Medication logs are PHI.

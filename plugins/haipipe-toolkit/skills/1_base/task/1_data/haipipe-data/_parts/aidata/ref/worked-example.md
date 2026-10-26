Worked example: MIMIC-IV mortality datapoint description
==========================================================

The canonical "good" instance of SKILL.md's mandatory datapoint description.
Based on a REAL asset in this repo — every claim below can be checked on disk:

```
config: examples/Project-EHR-Mimic/tasks/A01_data_pipeline_mimic/
        04_aidata_mimiciv_mortality/configs/run_aidata_mortality.yaml
asset:  _WorkSpace/4-AIDataStore/MimicIV31_MimicAdmissionEntry/
        @v0AIData-MimicMortality/   (train/ validation/ test/ +
        cf_to_cfvocab.json + feat_vocab.json + manifest.json)
```

Use it as a filled-in model, not as content to copy verbatim.

Worked example — MimicMortality (the template's canonical "good" instance)
---------------------------------------------------------------------------

   A datapoint is one hospital ADMISSION of one MIMIC-IV 3.1 patient:
   the trigger `MimicAdmissionEntry` fires at admission time
   (`ObsDT = AdmitTime`, keyed by `PID` + `HadmID`), and the binary
   outcome `Y = hospital_expire_flag` answers "did this patient die
   during THIS hospital stay" (`OutputMimicMortality`, label CaseFn
   `MimicHospExpireFlag`). One patient with 5 admissions contributes
   5 datapoints, each labeled by its own stay's outcome.

   The input features X are 14 CaseFn groups encoded by
   `CatInputMultiCFSparse` into one sparse vector (vocab in
   `cf_to_cfvocab.json` — 15 groups incl. the label CaseFn):
     - MimicPAge / MimicPGender / MimicPRace   — demographics at admission
     - MimicAdmitTimeFeat / MimicAdmitType     — when + what kind of admission
     - MimicLabStatsBf{1d,7d,14d,30d}          — lab-value statistics over
                                                 lookback windows BEFORE ObsDT
     - MimicVitalStatsBf{1d,7d,14d}            — vital-sign statistics, same
     - MimicMedCountBf{7d,30d}                 — medication counts, same

   (All Bf* features are STRICTLY BEFORE the admission timestamp — nothing
   from inside the stay leaks into X; the label is about the stay itself.)

   Selection: no row filters — every triggered admission enters the pool
   (`Split_to_Selection` merely routes rows by their `split` tag).

   INTENTIONALLY NOT FILTERED ON:
     - prior mortality-risk proxies (e.g. previous ICU stays, DNR codes) —
       they are features, not eligibility gates; filtering on them would
       select on outcome correlates and bias the cohort.

   Split policy:
     SplitMethod = RandomByPatient          ← split by PATIENT, not by row,
     Ratio = 70/15/15, random_state = 42       so the same patient's multiple
                                               admissions never straddle
                                               train and test (leakage guard)
     Train: 381,976 rows | Validation: 82,027 | Test: 82,025

   Provenance chain (manifest.json records it end-to-end):
     SourceSet mimiciv-3.1 (SourceFn MIMICIVv31, 29 tables)
       → RecordSet mimiciv-3.1_v3RecSet (80 partitions @i{i}n80)
       → CaseSet @v0CaseSet-MimicAdmissionEntry (per partition)
       → this AIDataSet (partitions auto-discovered and merged, streaming).

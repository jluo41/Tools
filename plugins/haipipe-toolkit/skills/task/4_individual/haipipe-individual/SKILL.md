---
name: haipipe-individual
description: >-
  Per-individual data contract skill: builds and manages a single-individual
  slice of stages 0-2 under
  _WorkSpace/A-User-Store/UserGroup-{dataset}/Subject-{id}. Use to create,
  inspect, or clean per-individual folders, or prepare data for endpoint
  inference. Trigger: individual, per-individual, UserGroup, Subject-ID,
  A-User-Store, sample patient.
argument-hint: "[command] [args...]"
metadata:
  version: "0.1.1"
  last_updated: "2026-07-04"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-individual
======================

Per-individual data contract covering stages 0-2.
One folder per individual, holding just the data needed to serve them via a deployed endpoint.
Stages 3-6 are for model development and never appear per-individual — at inference time the individual calls the endpoint directly.


Why stages 0-2 only
-------------------

  Stage           Role                              Per-individual?
  -----           ----                              ------------
  0-RawDataStore  original dataset files            YES  — individual's raw slice
  1-SourceStore   typed source frames               YES  — individual's rows
  2-RecStore      individual-centered records          YES  — individual's record(s)
  3-CaseStore     cohort cases                      NO   — training-time
  4-AIDataStore   model-ready tensors               NO   — training-time
  5-ModelInstance trained weights                   NO   — training artifact
  6-Endpoint      deployable                        NO   — shared by all individuals

The shipped inference client reads the individual's 1-SourceStore and builds an Endpoint payload.
The shared Endpoint owns preprocessing and model assets; per-individual 2-RecStore remains useful for retrieval/evaluation.


Folder Layout (FLAT — no dataset-name or partition wrappers nested inside)
-------------

  _WorkSpace/A-User-Store/
  ├── UserGroup-OhioT1DM/
  │   ├── Subject-540/
  │   ├── Subject-559/
  │   │   ├── 0-RawDataStore/               ← just the raw file names, flat
  │   │   │   ├── 559-ws-training.xml
  │   │   │   └── 559-ws-testing.xml
  │   │   ├── 1-SourceStore/                ← filtered source tables, flat
  │   │   │   ├── CGM.parquet
  │   │   │   ├── Diet.parquet
  │   │   │   ├── Exercise.parquet
  │   │   │   └── ...
  │   │   ├── 2-RecStore/                   ← filtered records, flat (no @iXnY)
  │   │   │   ├── Human-HmPtt/Human2RawNum.parquet
  │   │   │   ├── Record-HmPtt.CGM5Min/{RecAttr,RecIndex}.parquet
  │   │   │   ├── Record-HmPtt.Diet5Min/...
  │   │   │   └── ...
  │   │   └── manifest.yaml                 ← source_set, rec_set, partition, provenance
  │   └── ...
  ├── UserGroup-mimiciv-3.1/
  │   ├── Subject-10000032/                ← MIMIC partitions (@iXnY) are collapsed
  │   └── ...
  └── UserGroup-WellDoc2022CGM/
      ├── Subject-26/
      └── ...

Flattening rules (build script strips these wrapper segments):
  - dataset-name wrappers inside 1-SourceStore/ (e.g. `OhioT1DM/@OhioT1DMxmlv250302/`)
  - rec-set wrappers inside 2-RecStore/ (e.g. `OhioT1DM_v0RecSet/`)
  - partition wrappers `@iXnY/` (individual's data lives in only one partition anyway)
  - cohort nesting inside 0-RawDataStore/ (e.g. `Source/2018/train/` → flat)

Wrapper names preserved in manifest.yaml for provenance (source_set, rec_set, rec_partitions_found_in), so you can always trace back to the global store that seeded an individual.


Naming Convention
-----------------

  Parent:   UserGroup-{DatasetTag}
  Child:    Subject-{SubjectID}

  DatasetTag matches _WorkSpace/0-RawDataStore/ directory name (short form
  for long names):
    OhioT1DM                         → OhioT1DM
    mimiciv-3.1                      → mimiciv-3.1
    WellDoc2022CGM                   → WellDoc2022CGM

  SubjectID is the dataset's native identifier WITHOUT the dataset prefix
  (the prefix lives on the parent UserGroup-* folder):
    OhioT1DM     → 540, 544, 552, 559, 563, ...
    MIMIC-IV     → 10004235, 10009628, ...  (numeric individual_id)
    WellDoc      → 26, 48, ...              (study's individual number)

  Rationale: dataset-qualifying the PARENT folder instead of every individual
  folder name keeps individual paths short and makes cohort-level operations
  (list all MIMIC individuals, wipe one cohort) trivial.


Commands
--------

  /haipipe-individual                         → dashboard: list existing Subject-* folders
  /haipipe-individual dashboard               → same as above
  /haipipe-individual list [dataset]          → list individuals for one dataset
  /haipipe-individual inspect <Subject-*>     → show folder tree + manifest
  /haipipe-individual build <dataset> <id>    → build one individual folder
  /haipipe-individual build-samples           → build N samples per dataset (config-driven)
  /haipipe-individual clean <Subject-*>       → remove an individual folder (reversible via rebuild)
  /haipipe-individual spec                    → show full per-stage content spec


Sub-skills (inference chain)
----------------------------

Three sibling skills in this bucket consume the Subject-* folders this skill builds:

  /haipipe-individual-inference          serve one Subject-* through a local endpoint (ctx load + predict)
  /haipipe-individual-inference-report   render the inference output as a patient-facing report
  /haipipe-individual-inference-judge    judge report quality (persona panel)

Progression: build (this skill) → inference → report → judge.


Build Logic (what `build` does)
--------------------------------

Given `{dataset, individual_id}`, `fn/build_sample_individuals.py`:

1. Resolves the configured global SourceSet and RecSet and fingerprints the spec,
   builder, and input inventory (absolute path, size, mtime_ns, ctime_ns).
2. Reuses a cache only when that fingerprint and its recorded output inventory match.
   `--force` rebuilds when timestamps are unreliable or an explicit refresh is wanted.
3. Builds in a staging directory beside Subject-<id>. Ohio raw files are copied;
   MIMIC raw data stays pointer-only, and unavailable proprietary raw data is not invented.
4. Filters existing global 1-SourceStore and 2-RecStore parquet files by the
   configured PatientID values. It does not rerun SourceFn or RecordFn pipelines.
   Tables without PatientID and empty slices are omitted. Wrapper/partition flattening
   follows the rules above; duplicate paths within the same build use deterministic
   top-level-first ordering.
5. Writes provenance and output inventory, checks that inputs did not change,
   then replaces managed cache projections. A failed build preserves the previous cache;
   unrelated files outside the managed Store directories are preserved.

Use `--workspace <path-to-_WorkSpace>` to select the builder's Store root.
Input fingerprints use filesystem metadata to avoid rereading entire global datasets;
these are cache invalidation signatures, not cryptographic content attestations.

manifest.yaml schema
--------------------

```yaml
individual_id: "559"
dataset: "OhioT1DM"
dataset_tag: "OhioT1DM"
source_raw_paths:
  - "_WorkSpace/0-RawDataStore/OhioT1DM/559-ws-training.xml"
  - "_WorkSpace/0-RawDataStore/OhioT1DM/559-ws-testing.xml"
source_set: "OhioT1DM_v0"
rec_set: "OhioT1DM_v0RecSet"
built_at: "2026-04-20T14:30:00"
built_by: "build_sample_individuals.py v0.5"
input_fingerprint: "<sha256-of-spec-builder-and-stat-inventory>"
fingerprint_method: "sha256(config+builder+path/size/mtime_ns/ctime_ns)"
output_inventory: {}  # populated with generated relative paths, sizes and mtimes
build_args:
  individual_id_filter: ["559"]
```


Build Contract
--------------

The build MUST be deterministic and reproducible.
A single script (`fn/build_sample_individuals.py`) owns this:

  1. Read sample config (which datasets, which individual IDs, N per dataset).
  2. For each (dataset, individual_id):
     a. Steps 1-5 from Build Logic.
     b. Reuse only if input fingerprint and output inventory match.
  3. Emit a build report (what was built, what was skipped, any errors).

Do NOT hand-edit per-individual folders.
They are derived, not source of truth.
Source of truth = configured global SourceSet + RecSet, optional raw paths, build spec, and builder.


Consumers
---------

  Deployed endpoints (stage 6) read:
    manifest.yaml       → dataset + rec_set identification
    1-SourceStore/      → payload context for the shipped inference client
    2-RecStore/         → optional retrieval/evaluation context
    (NEVER read 3-6 — those don't exist per-individual anyway.)

  Tutorials and demos read:
    0-RawDataStore/     → "here's what one individual's raw data looks like"
    manifest.yaml       → attribution and provenance

  Privacy / deletion:
    rm -rf UserGroup-{DatasetTag}/Subject-{id}/  → wipes ALL derived data for one individual.
    Global stores untouched; re-run build to regenerate.


Relationship to Project-Wide Stores
------------------------------------

  Global _WorkSpace/ stores = BATCH work (training, cohort analysis):
    0-RawDataStore/{dataset}/*   ← whole dataset
    1-SourceStore/{SourceSet}/*  ← all individuals combined
    2-RecStore/{RecSet}/*        ← all records

  Per-individual UserGroup/Subject-*/ = SINGLE-INDIVIDUAL serving:
    0-RawDataStore/             ← one individual's raw slice
    1-SourceStore/              ← one individual's source rows
    2-RecStore/                 ← one individual's record

  A per-individual folder is a VIEW of the global store, scoped to one ID,
  built by filtering the existing global Source/Record outputs.


Rules
-----

  - NEVER create stages 3-6 inside a Subject-*/ folder. Those are not per-individual.
  - NEVER dataset-qualify the child folder name: it is Subject-{id}; the dataset tag lives on the parent UserGroup-{DatasetTag}/ (see Naming Convention).
  - ALWAYS write manifest.yaml — it's the provenance record.
  - If a dataset's raw format can't be cleanly sliced (e.g. proprietary binary),
    record source_raw_paths and raw_materialized in the Subject manifest instead of copying.
  - The build script is the source of truth for how each dataset is sliced.
    Hand-curated individual folders drift and break — do not do it.
  - Individual folders are reproducible: `rm -rf` and re-run `build` must produce
    an equivalent folder (differences only in built_at timestamp).

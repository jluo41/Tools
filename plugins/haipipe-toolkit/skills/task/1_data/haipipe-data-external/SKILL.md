---
name: haipipe-data-external
description: >-
  External-reference specialist: owns the asset model (asset.yaml contract,
  per-asset versions, locks, providers, obs_dt time rule), builds/freezes/
  validates assets in the b51 Block, inspects ExternalStore, and previews
  lookups into Source sets. Called by /haipipe-data. Trigger: external,
  ExternalStore, asset, lookup, freeze, lock, parity, feature store,
  third-party API, NPPES, ADI, NPI lookup, NDC lookup, NCPDP, zip5, zip3,
  engagement snapshot, vendor data.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "0.3.1"
  last_updated: "2026-09-24"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-data-external
=============================

External-reference specialist.
Owns the ExternalStore layer and the asset model: `ref/asset-model.md` is
the single reference for contracts, versions, locks, providers, the obs_dt
time rule, the lookup interface, and the b51 build Block. Read it first.

Externals are versioned reference assets (dimension lookups + engagement snapshots) that feed SourceFn.
They are NOT a sequential rung between Raw and Source: ExternalStore owns acquisition, snapshotting, vocabulary, and release identity; SourceFn owns cohort-scoped attachment into stable ProcessDFs.
RecordFn and CaseFn consume the resulting Source fields rather than reopening ExternalStore independently.

Two asset families live under ExternalStore:

  dimension   vendor-sourced lookup tables, keyed by domain ID
              (ndc, npi, ncpdp, zip3, zip5)

  engagement  cohort-aggregated stats keyed by the same external
              dimensions (ndc_engagement, npi_engagement,
              ncpdp_engagement, zip3_engagement, zip5_engagement,
              patient_engagement)

  Function axis:  dashboard | load | cook | design-chef | review | join | refresh
                  | freeze | lock | parity

---

Commands
--------

```
/haipipe-data-external                            -> dashboard: ExternalStore inventory
/haipipe-data-external dashboard                  -> same
/haipipe-data-external load <asset>               -> load and inspect a built asset
/haipipe-data-external cook <asset>               -> run e{N}_build_external_<asset>.py
/haipipe-data-external design-chef                -> scaffold a new e_build_external_*.py
/haipipe-data-external review <asset>             -> schema + coverage + staleness audit
/haipipe-data-external join <asset> --to <set>    -> preview joining into a Source/Record set
/haipipe-data-external refresh [asset...]         -> rebuild stale assets (raw newer than output)
/haipipe-data-external freeze <asset>             -> freeze a feature-store/API pull as <asset>/S<date>/
/haipipe-data-external lock <LockName>            -> write _locks/<LockName>.yaml (asset -> version)
/haipipe-data-external parity <asset>             -> frozen version vs live provider, same keys
```

Optional flags:

```
--version <version>  pin one asset's version (topic layout), e.g. NPPES202507
--version @{tag}     legacy: pin a release-wide folder such as @260104R4
```

---

Dispatch Table
--------------

After parsing, read these files:

```
Invocation     This skill's ref                  fn doc to read
-------------- --------------------------------- ----------------------------------
(every row)    ref/asset-model.md                (read before the row's own docs)
dashboard      ref/concepts.md +
               ref/asset-catalog.md              ../haipipe-data/fn/fn-0-dashboard.md
load           ref/concepts.md +
               ref/asset-catalog.md              fn/fn-1-load.md
cook           ref/concepts.md                   fn/fn-2-cook.md
design-chef    ref/concepts.md +
               ref/asset-catalog.md +
               ../haipipe-data-source/
                 ref/concepts.md                 fn/fn-3-design-chef.md
review         ref/concepts.md                   fn/fn-review.md
join           ref/concepts.md +
               ref/join-contract.md +
               ../haipipe-data-source/
                 ref/concepts.md                 fn/fn-join.md
refresh        ref/concepts.md                   fn/fn-refresh.md
freeze         ref/asset-model.md                fn/fn-freeze.md
lock           ref/asset-model.md                fn/fn-lock.md
parity         ref/asset-model.md                fn/fn-parity.md
(no fn arg)    ref/concepts.md                   (ref-only mode)
```

Why `design-chef` and `join` also read Source's ref: ExternalFn outputs are consumed downstream by SourceFn/RecordFn -- you need both schemas to design the asset or preview a join.

---

Step-by-Step Protocol
----------------------

Step 0: Read the cross-stage overview FIRST:
        `../haipipe-data/ref/0-overview.md`. Externals do NOT appear as a
        Stage-0 rung in the 6-layer diagram -- they are sideways inputs.
        Mandatory.

Step 1: Parse args after `/haipipe-data-external`.
Extract:
          function  in { dashboard, load, cook, design-chef, review,
                          join, refresh, freeze, lock, parity, (none) }
          extras    asset name, --to <set>, --version <version|@tag>, lock name
        If no args -> dashboard.

Step 2: Read THIS skill's `ref/asset-model.md`, then `ref/concepts.md`
        for stage-0 specifics.

Step 3: Read additional ref/fn docs per the dispatch table above.

Step 4: For `join`, also resolve from `ref/asset-catalog.md`:
          - the asset's primary key
          - the target set's join-ready columns (NPI, NDC, NCPDP, zip5, ...)
        See ref/join-contract.md for match-rate calculation rules.

Step 5: Execute the procedure described by the fn doc, scoped to externals.

Step 6: Return the structured tail (see umbrella SKILL.md) so the
        orchestrator can present a clean summary.

---

ExternalStore layout (for orientation)
---------------------------------------

```
_WorkSpace/ExternalStore/
+-- <asset>/                             <- one folder per topic (npi, zip3, npi_engagement)
|   +-- asset.yaml                       <- contract: key, fields, family, providers
|   +-- @raw/                            <- vendor/API landings for this asset
|   +-- <version>/                       <- built version or frozen snapshot
|       +-- df_<asset>_id.parquet, column_to_<asset>_li.pkl, README.md
|       +-- version.yaml                 <- ValidFromDT, RefPeriod, builder, sha256
+-- _locks/<LockName>.yaml               <- asset -> version pins used by a SourceFn
+-- @{tag}/                              <- LEGACY release-wide folder (e.g. @260104R4), read-only
+-- @raw/, @inference/                   <- legacy shared landings / payload samples
```

Full model: `ref/asset-model.md`. Builders live in the auxiliary `b51` Block
(`j0N_asset_<asset>/t02_build_<Version>/`). Legacy workspaces keep
`code-dev/0-EXTERNAL/e{N}_build_external_*.py` (WellDoc-SPACE) writing into
`@{tag}/`; do not add new assets there.

---

MUST DO / MUST NOT
-------------------

- ALWAYS read `../haipipe-data/ref/0-overview.md` and this skill's
  `ref/concepts.md` before any function execution.
- For `cook` and `refresh`: prerequisite
  `source .venv/bin/activate && source env.sh`.
- For `join`: NEVER actually merge data -- only preview match rates and
  suggest the SourceFn lookup block (`ref/asset-model.md` § SourceFn
  pattern). Real lookups run in SourceFn; RecordFn aligns the resulting
  fields in entity/time and CaseFn derives model-facing features.
- External builders are b51 Task scripts, not generated Fns: there is no
  `code/haifn/fn_external/`. If one ever appears it is generated and
  read-only.
- NEVER overwrite an existing `<asset>/<version>/` or `@{tag}` release without
  explicit user confirmation -- versions are reproducibility anchors.
- Training reads frozen local versions only; a live provider (feature store,
  third-party API) is reached only with env=serve. Freeze first (`freeze`).
- An endpoint ships only its lock's versions, trimmed to the fields training
  looked up and pre-keyed, and loads them once per worker at warmup
  (`ref/asset-model.md` § Serving: the endpoint bundle).
- NEVER bind a `patient_id`-keyed asset to `third_party_api` or
  `local_service` (PHI).
- Every lookup carries `obs_dt`; temporal assets use `leak_policy: strict`.
- Do not build new locks or version.yaml files on top of a legacy `@{tag}`
  folder; rebuild the asset from `@raw/` in b51.

---
name: haipipe-data-external
description: "Stage 0 (External) specialist. Builds, runs, and reviews ExternalFn (currently as e_build_external_*.py scripts); inspects ExternalStore; loads dimension and engagement assets; previews joins into Source/Record sets. Called by /haipipe-data orchestrator. Direct invocation works for stage-scoped work, but /haipipe-data is the recommended entry. Trigger: external, ExternalFn, dimension, lookup, reference, NPPES, ADI, MHI, NPI lookup, NDC lookup, NCPDP, zip5, zip3, engagement features, vendor data."
argument-hint: [function] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-data-external
=============================

Stage 0 specialist. Owns all ExternalFn work and the ExternalStore layer.

Externals are reference assets (dimension lookups + engagement aggregates)
that any cohort-scoped Stage 1-4 chef can pull from. They are NOT a layer
in series with Stages 1-4 -- they are a sideways pantry. RecordFn and
CaseFn declare external dependencies by primary key (NPI, NDC, NCPDP,
zip3, zip5, patient_id).

Two asset families live under ExternalStore:

  dimension   vendor-sourced lookup tables, keyed by domain ID
              (ndc, npi, ncpdp, zip3, zip5)

  engagement  cohort-aggregated stats keyed by the same external
              dimensions (ndc_engagement, npi_engagement,
              ncpdp_engagement, zip3_engagement, zip5_engagement,
              patient_engagement)

  Function axis:  dashboard | load | cook | design-chef | review | join | refresh

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
```

Optional flags:

```
--version @{tag}     pin to a specific ExternalStore release (default: latest)
```

---

Dispatch Table
--------------

After parsing, read these files:

```
Invocation     This skill's ref                  Umbrella's fn doc
-------------- --------------------------------- ----------------------------------
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
(no fn arg)    ref/concepts.md                   (ref-only mode)
```

Why `design-chef` and `join` also read Source's ref: ExternalFn outputs
are consumed downstream by SourceFn/RecordFn -- you need both schemas
to design the asset or preview a join.

---

Step-by-Step Protocol
----------------------

Step 0: Read the cross-stage overview FIRST:
        `../haipipe-data/ref/0-overview.md`. Externals do NOT appear as a
        Stage-0 rung in the 6-layer diagram -- they are sideways inputs.
        Mandatory.

Step 1: Parse args after `/haipipe-data-external`. Extract:
          function  in { dashboard, load, cook, design-chef, review,
                          join, refresh, (none) }
          extras    asset name, --to <set>, --version <release>
        If no args -> dashboard.

Step 2: Read THIS skill's `ref/concepts.md` for stage-0 specifics.

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
+-- @raw/                                <- vendor dumps (NPPES, ZipInfo, drug DB)
+-- @inference/                          <- inference-time payload samples
+-- @{version}/                          <- versioned built assets (e.g. @260104R4)
    +-- {asset}/
        +-- df_{asset}_id.parquet        <- ID-mapped values (primary output)
        +-- column_to_{asset}_li.pkl     <- vocabulary for decoding IDs
        +-- README.md                    <- auto-generated schema + usage
        +-- df_{asset}_raw.parquet       <- (engagement only) pre-ID-mapped raw
```

Versioning: latest release wins by default. Pin with `--version @{tag}`.
Current builders live in `code-dev/0-EXTERNAL/e{N}_build_external_*.py`.

---

MUST DO / MUST NOT
-------------------

- ALWAYS read `../haipipe-data/ref/0-overview.md` and this skill's
  `ref/concepts.md` before any function execution.
- For `cook` and `refresh`: prerequisite
  `source .venv/bin/activate && source env.sh`.
- For `join`: NEVER actually merge data -- only preview match rates and
  suggest a config snippet. Real joins materialize in RecordFn / CaseFn.
- NEVER edit `code/haifn/fn_external/` (does not yet exist in Phase 1;
  if Phase 2 promotion happens, it becomes generated and read-only).
- NEVER overwrite an existing `@{version}` release without explicit user
  confirmation -- releases are reproducibility anchors.

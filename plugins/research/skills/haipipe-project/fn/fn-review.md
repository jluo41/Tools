fn-review: Project Gap Analysis + Docs Generation (Both Tracks)
================================================================

Inspects an existing project against the standard structure defined in
ref/project-structure.md (Track B) and ref/code-structure.md (Track A).
Outputs a gap report with severity tags AND generates/updates docs/ and
scripts/INDEX.md so the project is brought to standard automatically.

Write access policy:
  ALLOWED    docs/              (create folder, generate TODO.md, project-summary stub)
  ALLOWED    scripts/INDEX.md   (create if missing, update entries from existing scripts)
  BLOCKED    config/            (read only — never modify pipeline configs)
  BLOCKED    code/              (read only — never modify generated or library code)
  BLOCKED    code-dev/          (read only — never modify builders)

---

Severity Tags
--------------

  [BLOCK]   Missing structure that prevents pipeline from running at all
  [ERROR]   Present but broken — wrong naming, mismatched script/result pairs
  [WARN]    Deviation from standard — works but inconsistent or incomplete
  [NOTE]    Minor style gap, low priority

---

Step 0: Identify the Target Project
=====================================

If the user provided a path argument: use it directly.

If no path given, auto-detect using this priority order:

  1. Check git status for recently modified files under examples/:
       git status --short | grep "^.M examples/" | head -5
     If exactly one project folder appears -> use it.
     If multiple projects appear -> show them and ask user to pick.

  2. If git status gives no results, check recently modified files:
       find examples/ -maxdepth 3 -newer examples/ -name "*.py" -o -name "*.yaml" | head -10
     Infer project from the most common examples/{PROJECT_ID}/ prefix.

  3. If still ambiguous -> list all Proj* directories under examples/ and ask:
       "Which project would you like to review? (or press Enter to review all)"
     If user says "all" -> run review for each project sequentially, produce one
     combined report with a summary table at the top.

Confirm the project path before proceeding. Set:

  PROJECT_PATH = examples/{PROJECT_ID}/
  PROJECT_ID   = basename of that path

---

Step 1: Validate Project Naming
=================================

Check that PROJECT_ID matches the pattern: Proj{Series}-{Category}-{Num}-{Name}

  [ ] Starts with "Proj"
  [ ] Series is a single uppercase letter
  [ ] Category is a non-empty word (Bench, Model, EHR, etc.)
  [ ] Num is a non-negative integer
  [ ] Name is CamelCase (starts with uppercase, no spaces or underscores)

Violations:
  Pattern mismatch entirely         -> [BLOCK]
  Num missing or non-integer        -> [ERROR]
  Name uses underscores or lowercase -> [WARN]

---

Step 2: Check Four-Part Structure
===================================

Verify each mandatory directory exists:

  [ ] {PROJECT_PATH}/cc-archive/     missing -> [BLOCK]
  [ ] {PROJECT_PATH}/config/         missing -> [BLOCK]
  [ ] {PROJECT_PATH}/scripts/        missing -> [WARN]
  [ ] {PROJECT_PATH}/results/        missing -> [WARN]
  [ ] {PROJECT_PATH}/docs/           missing -> [WARN]

Report any extra top-level directories not in the standard four:
  Extra dirs (e.g., workspace/, materials/, notebooks/) -> [NOTE]
  Propose: "Consider migrating content to the standard layout."

---

Step 3: Review cc-archive/
============================

  [ ] Directory is non-empty (has at least one .md file)
      Empty cc-archive/          -> [WARN] "No session records found."
  [ ] Files follow naming convention {type}_{YYMMDD}_h{HH}_*.md
      Non-conforming filenames   -> [NOTE]
  [ ] No non-.md files present (.py, .yaml, .ipynb, etc.)
      Mixed file types           -> [WARN]

---

Step 4: Review config/
========================

  [ ] Directory is non-empty
      Empty config/              -> [WARN] "No YAML configs found."
  [ ] All files have .yaml extension
      Non-YAML files             -> [WARN]
  [ ] YAML filenames start with stage number prefix (1_, 2_, 3_, 4_, 5_)
      Missing prefix             -> [WARN]

Detect which stages are declared (presence of 1_*.yaml, 2_*.yaml, etc.).
Save as DECLARED_STAGES for Steps 6 and 7.

---

Step 4b: Generate / Update docs/
==================================

This step has WRITE ACCESS to docs/ only.

**If docs/ does not exist — create it:**
  mkdir examples/{PROJECT_ID}/docs/

**If docs/TODO.md does not exist — generate it from scratch:**
  Scan the project to pre-fill the TODO.md template from ref/project-structure.md:
  - Required Files table: mark each standard folder/file as "done" if present, "todo" if missing
  - Track A Stubs table: populate from any build_*.py found in code-dev/ and
    algo/tuner/instance files found in code/hainn/ that reference this project's dataset/model
  - Pipeline Progress table: mark stage as "done" if a non-empty YAML exists for it in config/,
    "n/a" if no YAML and user hasn't declared it, "todo" otherwise
  Write the generated file to docs/TODO.md.
  Report: "[GENERATED] docs/TODO.md created from project scan."

**If docs/TODO.md exists — update it:**
  [ ] TODO.md has a Required Files table       missing table -> [NOTE]
  [ ] TODO.md has a Pipeline Progress table    missing table -> [NOTE]
  Sync Pipeline Progress rows with config/ YAML presence:
    Stage has non-empty YAML but marked "todo" -> upgrade to "done"
  Write updated TODO.md back.
  Report: "[UPDATED] docs/TODO.md — {N} status rows refreshed."

**docs/project-summary.md:**
  [ ] exists    -> [NOTE] "Summary present."
  [ ] missing   -> [NOTE] "No summary yet. Run /haipipe-project summarize when ready."
  Do NOT generate project-summary.md during review — that is fn-summarize.md's job.

---

Step 4c: Generate docs/data-map.md
=====================================

This step has WRITE ACCESS to docs/ only.
Always generate (or regenerate) this file — it is derived entirely from config/ YAMLs,
which are read-only. Overwrite if it already exists.

Source: read all YAML files in config/ to extract FnClass names, dataset names,
        model class, and stage sequence.

Write docs/data-map.md with this fixed format:

```
Data Map: {PROJECT_ID}
=======================
Generated: {YYMMDD}
Source: derived from config/ YAML files

Pipeline Flow
-------------

  {dataset} (raw)
       |
       v  Stage 1 — Source
       |  FnClass:  {SourceFnClass}     [done / stub / missing]
       |  Config:   config/1_source_{dataset}.yaml
       v
  SourceSet ({dataset})
       |
       v  Stage 2 — Record
       |  FnClass:  {RecordFnClass}     [done / stub / missing]
       |  Config:   config/2_record_{dataset}.yaml
       v
  RecordSet ({dataset})
       |
       v  Stage 3 — Case
       |  FnClass:  {CaseFnClass}       [done / stub / missing]
       |  Config:   config/3_case_{dataset}.yaml
       v
  CaseSet ({dataset})
       |
       v  Stage 4 — AIData
       |  FnClass:  {TfmFnClass}        [done / stub / missing]
       |  Config:   config/4_aidata_{dataset}.yaml
       v
  AIDataSet ({dataset})
       |
       v  Stage 5 — Model
       |  ModelClass: {ModelInstanceClass}   [done / stub / missing]
       |  Tuner:      {model_tuner_name}
       |  Config:     config/5_model_{name}.yaml
       v
  ModelInstance ({name})
       |
       v
  results/ (light summaries)
  _WorkSpace/ (heavy outputs)

Stages
------

  | Stage | Status | FnClass / ModelClass | Dataset | Config File |
  |-------|--------|----------------------|---------|-------------|
  | 1 Source  | {status} | {FnClass} | {dataset} | 1_source_{dataset}.yaml |
  | 2 Record  | {status} | {FnClass} | {dataset} | 2_record_{dataset}.yaml |
  | 3 Case    | {status} | {FnClass} | {dataset} | 3_case_{dataset}.yaml   |
  | 4 AIData  | {status} | {FnClass} | {dataset} | 4_aidata_{dataset}.yaml |
  | 5 Model   | {status} | {ModelClass} | {dataset} | 5_model_{name}.yaml |

  Status values:
    done     YAML present + FnClass resolves in code/haifn/ or code/hainn/
    stub     YAML present but FnClass is TODO_* or not found in codebase
    missing  No YAML for this stage
    n/a      Stage not used by this project
```

Omit stages with status "n/a" from the pipeline flow diagram.
If a stage has no YAML, mark the row "missing" and omit from the flow.

Report: "[GENERATED] docs/data-map.md"

---

Step 4d: Generate docs/dependency-report.md
=============================================

This step has WRITE ACCESS to docs/ only.
Always generate (or regenerate). Overwrite if it already exists.

Source: code/INDEX.md (for cross-project reuse info) + config/ YAMLs (for class names)
        + code/haifn/ and code/hainn/ (for implementation status).

Write docs/dependency-report.md with this fixed format:

```
Dependency Report: {PROJECT_ID}
================================
Generated: {YYMMDD}
Source: config/ YAMLs cross-referenced with code/INDEX.md

This project depends on the following Fns and models.
Use this file to understand reuse opportunities and track implementation status.

Pipeline Function Dependencies
--------------------------------

  | FnClass | Stage | Location in code/ | Status | Also used in |
  |---------|-------|-------------------|--------|--------------|
  | {FnClass} | {N} | {path or "not found"} | {done/stub/missing} | {Projects or "only this project"} |
  ...

ML Model Dependencies
----------------------

  | ModelClass | Family | Tuner | Location in code/ | Status | Also used in |
  |------------|--------|-------|-------------------|--------|--------------|
  | {ModelClass} | {family} | {TunerClass} | {path or "not found"} | {done/stub/missing} | {Projects or "only this project"} |

Reuse Opportunities
--------------------
  [List any Fns or models shared with other projects, with a note on what those
   projects do — helps identify if the shared code needs to stay generic]

  {FnClass} — shared with {ProjectList}
    Note: changes to this Fn affect all listed projects.

  [If nothing is shared: "All Fns and models are unique to this project."]

Missing Implementations
------------------------
  [List any FnClass or ModelClass referenced in config/ but not found in code/]

  {FnClass} (Stage {N}) — referenced in config/ but not found in code/haifn/{fn_layer}/
    Action: run /haipipe-data design-chef {N} to implement

  {ModelClass} — referenced in config/ but not found in code/hainn/instance/
    Action: run /haipipe-nn to implement
```

If code/INDEX.md does not exist: note it in the report and populate "Also used in"
as "unknown (code/INDEX.md not found)" rather than failing.

Report: "[GENERATED] docs/dependency-report.md"

---

Step 5: Review scripts/ and results/ Alignment
================================================

Collect all files in scripts/ (excluding .gitkeep and sbatch/ contents):

  SCRIPTS = [basename without extension for each file in scripts/]

Collect all directories in results/ (excluding .gitkeep):

  RESULTS = [dirname for each directory in results/]

Check alignment:

  For each s in SCRIPTS:
    [ ] results/{s}/ exists           missing -> [ERROR] "Script has no result folder."

  For each r in RESULTS:
    [ ] scripts/{r}.* exists (any ext) missing -> [ERROR] "Result folder has no matching script."

Check script naming convention {seq}_{YYMMDD}_{desc}.{ext}:

  [ ] seq is exactly 3 digits, zero-padded       non-conforming -> [WARN]
  [ ] YYMMDD is a 6-digit date                   non-conforming -> [WARN]
  [ ] desc uses underscores (no spaces or dashes) non-conforming -> [NOTE]

---

Step 5b: Generate / Update scripts/INDEX.md
=============================================

This step has WRITE ACCESS to scripts/INDEX.md only.

**If scripts/INDEX.md does not exist — generate it:**
  Scan all files in scripts/ (excluding .gitkeep, sbatch/ contents).
  For each script file, infer:
    Data          from filename desc (e.g. "ohio" -> OhioT1DM) or mark as "unknown"
    Functionality from filename desc (snake_case words after YYMMDD)
    Stage         from filename desc or config/ YAML names (best-effort inference)
    Status        "done" if a matching results/{basename}/ folder exists, else "wip"
  Write scripts/INDEX.md with the inferred table.
  Report: "[GENERATED] scripts/INDEX.md — {N} scripts indexed."

**If scripts/INDEX.md exists — sync it:**
  [ ] Every .py/.sh in scripts/ has an entry    missing -> add row, Status="wip"
  [ ] Every entry has a matching file            orphan  -> mark row with [ORPHAN] note
  [ ] Scripts with results/ folder but Status != "done" -> upgrade to "done"
  Write updated INDEX.md back.
  Report: "[UPDATED] scripts/INDEX.md — {N} rows added/updated."

**Track A example check (read-only):**
  [ ] Every Track A stub has a paired example_{name}.py
      Missing -> [WARN] "Track A stub {stub} has no paired example script."

---

Step 6: Check results/ for Heavy Files
========================================

Scan results/ recursively for file extensions associated with heavy outputs:

  Heavy extensions:
    .pt, .pth, .ckpt, .safetensors    <- model weights
    .npy, .npz                         <- large arrays (check size)
    .pkl, .pickle                      <- pickled objects (check size)
    bin, .h5, .hdf5                    <- binary data

  Any heavy file found -> [ERROR]
    "Heavy file {filename} found in results/. Move to _WorkSpace/."

Check that each result folder contains at least one of:
  report.md, metrics.json, *.md, *.json
  Empty result folder -> [WARN] "Result folder has no summary files."

---

Step 7: Code Sync Check (config ↔ code ↔ code-dev)
=====================================================

Purpose: verify that everything the project's config files reference actually
exists and is implemented in the codebase, and that code-dev/ builders and
code/haifn/ generated files are in sync.

Read code/INDEX.md at the start of this step. Use it to resolve class names
and to note which other projects share the same Fns/models.

Stage map (used throughout Step 7):
  1  ->  code-dev/1-PIPELINE/1-Source-WorkSpace/   code/haifn/fn_source/   FnClass key: SourceFnClass
  2  ->  code-dev/1-PIPELINE/2-Record-WorkSpace/   code/haifn/fn_record/   FnClass key: RecordFnClass
  3  ->  code-dev/1-PIPELINE/3-Case-WorkSpace/     code/haifn/fn_case/     FnClass key: CaseFnClass / TriggerFnClass
  4  ->  code-dev/1-PIPELINE/4-AIData-WorkSpace/   code/haifn/fn_aidata/   FnClass key: TfmFnClass / SplitFnClass
  5  ->  code/hainn/                               code/haifn/fn_model/    FnClass key: ModelInstanceClass


Step 7a — Config → code/haifn/ class resolution
-------------------------------------------------

For each YAML in config/ (for stages 1-4):
  1. Read the YAML file.
  2. Extract the FnClass value (e.g., SourceFnClass: GlucoseSourceFn).
  3. Search the corresponding code/haifn/{fn_layer}/ directory for a file
     containing `class {FnClassName}(`:
       grep -r "class {FnClassName}" code/haifn/{fn_layer}/
  4. Checks:
       [ ] FnClass value is not "TODO_*"
           Still TODO -> [BLOCK] "Config references placeholder class. Implement the Fn first."
       [ ] FnClass file found in code/haifn/{fn_layer}/
           Not found -> [BLOCK] "Class {FnClassName} not found in code/haifn/{fn_layer}/."
       [ ] FnClass is listed in code/INDEX.md
           Not in index -> [WARN] "Class {FnClassName} exists but is not in code/INDEX.md. Update the registry."
       [ ] Other YAML args keys match what the FnClass __init__ accepts
           (scan __init__ signature in the Fn file and compare to YAML args section)
           Mismatch -> [ERROR] "YAML arg '{key}' not found in {FnClassName}.__init__."

  If FnClass found and in INDEX.md: report which other projects use this Fn:
    "FnClass {FnClassName} is shared with: {Projects Using column}"


Step 7b — Config → code/hainn/ model resolution (Stage 5)
----------------------------------------------------------

For 5_model_*.yaml (if present):
  1. Read the YAML. Extract:
       MODEL_CLASS   = ModelInstanceClass value
       TUNER_NAME    = model_tuner_name value
       MODEL_VERSION = modelinstance_version value

  2. Checks on ModelInstanceClass:
       [ ] MODEL_CLASS is not "TODO_*"
           Still TODO -> [BLOCK]
       [ ] code/hainn/instance/ contains a file with `class {MODEL_CLASS}(`
           grep -r "class {MODEL_CLASS}" code/hainn/instance/
           Not found -> [BLOCK] "ModelInstanceClass {MODEL_CLASS} not found in code/hainn/instance/."
       [ ] MODEL_CLASS is listed in code/INDEX.md
           Not in index -> [WARN] "Model not in code/INDEX.md. Update the registry."

  3. Checks on model_tuner_name:
       [ ] TUNER_NAME is not "TODO_*"   -> [BLOCK] if still TODO
       [ ] code/hainn/tuner/ contains a file with `class {TUNER_NAME}(`
           grep -r "class {TUNER_NAME}" code/hainn/tuner/
           Not found -> [BLOCK] "Tuner {TUNER_NAME} not found in code/hainn/tuner/."

  4. Checks on modelinstance_version:
       [ ] Value starts with "@" (e.g., "@v0001-glucose-transformer")
           Missing "@" -> [WARN] "modelinstance_version should start with @"

  5. Check remaining required YAML keys present:
       ModelArgs, TrainingArgs, InferenceArgs, EvaluationArgs,
       aidata_name, aidata_version, modelinstance_name
       Any missing -> [ERROR] "Required YAML key '{key}' missing from 5_model_*.yaml"

  If model found and in INDEX.md: report sharing:
    "Model {MODEL_CLASS} is also used in: {Projects Using column}"


Step 7c — code-dev/ builder ↔ code/haifn/ generated file sync
--------------------------------------------------------------

For each stage in DECLARED_STAGES (stages 1-4 only):
  1. List build_*.py files in code-dev/1-PIPELINE/{N}-*-WorkSpace/:
       BUILDERS = [files matching build_*.py]
  2. For each builder, infer the expected generated Fn file in code/haifn/{fn_layer}/:
       (convention: builder build_{dataset}_source.py -> fn_source/{dataset}_source.py or similar)
  3. Checks:
       [ ] At least one build_*.py exists in the WorkSpace
           None found -> [WARN] "No builder for Stage {N}. Use /haipipe-data design-chef."
       [ ] The corresponding generated file exists in code/haifn/{fn_layer}/
           Not found -> [ERROR] "Builder exists but no generated Fn. Run the builder script."
       [ ] Generated file does not contain only stub content ("pass", "TODO", "raise NotImplementedError")
           Stub-only content -> [WARN] "Generated Fn {file} appears to be a stub. Implement via /haipipe-data design-chef."
       [ ] Generated file was NOT manually edited after generation
           Check: if builder file is newer than generated file by more than 1 day -> [WARN]
           "Builder is newer than generated file — regenerate to stay in sync."


Step 7d — scripts/ import resolution
--------------------------------------

Scan all .py files in scripts/ for haipipe imports:
  grep -n "from haifn\|from hainn\|import haifn\|import hainn" scripts/*.py

For each imported class name found:
  [ ] Class exists in code/haifn/ or code/hainn/
      grep -r "class {ClassName}" code/haifn/ code/hainn/
      Not found -> [ERROR] "Script {script} imports {ClassName} which does not exist in codebase."
  [ ] Class is in code/INDEX.md
      Not in index -> [NOTE] "Imported class {ClassName} not registered in code/INDEX.md."

---

Step 8: Output Gap Report
===========================

Print a structured report:

```
Gap Report: {PROJECT_ID}
=========================
Reviewed: {YYMMDD} h{HH}

Naming
------
  [status]  Project naming convention

Structure
---------
  [status]  cc-archive/
  [status]  config/
  [status]  scripts/
  [status]  results/
  [status]  docs/

docs
----
  [status]  docs/TODO.md
  [status]  docs/project-summary.md

cc-archive
----------
  [status]  ...

config
------
  [status]  ...
  Declared stages: {DECLARED_STAGES}

scripts / INDEX.md
------------------
  [status]  INDEX.md present
  [status]  All scripts indexed
  [status]  All Track A stubs have paired examples

scripts / results alignment
---------------------------
  [status]  Script-result pairs
  [list of mismatches if any]

results (heavy file check)
--------------------------
  [status]  ...

Code Sync
---------
  Config → code/haifn/ (FnClass resolution):
    [status]  Stage 1: {FnClassName} -> {found/missing}
    [status]  Stage 2: {FnClassName} -> {found/missing}
    ...
    Shared Fns (cross-project reuse): {list or "none"}

  Config → code/hainn/ (model resolution):
    [status]  ModelInstanceClass: {MODEL_CLASS} -> {found/missing}
    [status]  Tuner: {TUNER_NAME} -> {found/missing}
    [status]  Required YAML keys -> {ok/list missing keys}
    Shared models (cross-project reuse): {list or "none"}

  code-dev/ ↔ code/haifn/ builder sync:
    [status]  Stage 1 builder -> generated Fn {in-sync/stale/missing}
    [status]  Stage 2 ...

  scripts/ import check:
    [status]  All imported classes resolve -> {ok/list broken imports}

Summary
-------
  BLOCK:  {count}
  ERROR:  {count}
  WARN:   {count}
  NOTE:   {count}

Proposed Actions
----------------
  1. [Highest priority fix]
  2. [Next fix]
  ...
```

If zero issues: print "All checks PASSED. Project is conformant."

---

MUST NOT
---------

- Do NOT modify config/ files — read only, never edit pipeline configs.
- Do NOT modify code/ files — read only, never edit library or generated code.
- Do NOT modify code-dev/ files — read only, never edit builders.
- Do NOT modify scripts/ (except INDEX.md) — never edit experiment scripts.
- Do NOT modify cc-archive/ — session history is append-only via /cc-session-summary.
- Do NOT run any pipeline commands.
- Do NOT propose actions outside the project folder without user confirmation.

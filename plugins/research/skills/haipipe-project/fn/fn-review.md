fn-review: Project Gap Analysis + Docs Generation
===================================================

Inspects an existing project against the standard structure.
Outputs a gap report and generates/updates docs/ and README.md files.

Write access:  docs/ (all files), tasks/README.md, {group}/README.md, {task}/README.md
Read-only:     everything else (config/, code/, code-dev/, cc-archive/, paper/)

Severity tags: [BLOCK] [ERROR] [WARN] [NOTE]

Execution checklist (track progress):
  [ ] Step 0   identify target project
  [ ] Step 1   validate naming + structure
  [ ] Step 2   per-task review
  [ ] Step 3   code sync check
  [ ] Step 4   generate/update docs
  [ ] Step 5   generate/update README.md files
  [ ] Step 6   output gap report

---

Step 0: Identify Target Project
=================================

Follow the auto-detection rules in SKILL.md.
Confirm PROJECT_PATH and PROJECT_ID before proceeding.

---

Step 1: Validate Naming + Structure
=====================================

**Naming:**
  - PROJECT_ID matches Proj{Series}-{Category}-{Num}-{Name}
    Pattern mismatch -> [BLOCK]
    Minor issues (underscore in Name, missing Num) -> [WARN]

**Mandatory:**
  - tasks/ exists ([BLOCK] if missing)

**Optional (absence is fine):**
  - docs/ ([WARN] if missing)
  - paper/ ([NOTE] if missing)
  - cc-archive/ ([NOTE] if missing)

**Legacy detection:**
  - Top-level config/ present -> [NOTE] suggest /haipipe-project organize
  - Top-level results/ present -> [NOTE] suggest /haipipe-project organize
  - Extra top-level dirs -> [NOTE]

**cc-archive/ (if exists):**
  - Non-empty, .md files only, naming convention {type}_{YYMMDD}_h{HH}_*.md

---

Step 2: Per-Group and Per-Task Review
=======================================

**Group-level checks:**
For each group folder in tasks/ (excluding sbatch/):
  - {G}_{group}/README.md exists ([WARN] if missing)
  - Group letter matches its tasks' prefix ([ERROR] if mismatch)
  - No flat task folders directly in tasks/ -- must be inside a group ([WARN])

**Per-task checks:**
For each task folder inside each group:

  **Structure checks:**
    - At least one *.py exists in the task folder ([WARN] if missing)
    - {task}/README.md exists ([WARN] if missing)
    - {task}/config/ exists with its own YAML files ([WARN] if missing)
    - {task}/config/ is not a symlink ([WARN] if symlink — each task owns its own config)
    - YAML files parseable ([ERROR] if not)

  **Run-result alignment:**
    - If runs/ exists: every .sh in runs/ has matching results/{name}/ ([ERROR] if missing)
    - If runs/ exists: every results/{name}/ has matching runs/{name}.sh ([ERROR] if orphaned)
    - If no runs/: results/ may contain flat files or default/ subfolder (OK)

  **Heavy file check in results/:**
    - .pt, .pth, .ckpt, .safetensors, .npy, .pkl, .bin, .h5 -> [ERROR] move to _WorkSpace/

  **Track A example check:**
    - Every Track A stub has a paired example task ([WARN] if missing)

Aggregate DECLARED_STAGES from config/ YAML filenames across all tasks.

---

Step 3: Code Sync Check
=========================

Read code/INDEX.md first.

Stage map for FnClass keys:
  1 -> fn_source/  SourceFnClass     3 -> fn_case/     CaseFnClass
  2 -> fn_record/  RecordFnClass     4 -> fn_aidata/   TfmFnClass
  5 -> code/hainn/instance/          ModelInstanceClass
  6 -> fn_endpoint/                  EndpointFnClass

**Config -> code resolution (stages 1-4):**
  For each FnClass in config/ YAMLs:
    - Not "TODO_*" ([BLOCK] if still placeholder)
    - Class found in code/haifn/{fn_layer}/ ([BLOCK] if missing)
    - Listed in code/INDEX.md ([WARN] if not registered)
    - Report cross-project sharing from code/INDEX.md

**Model resolution (stage 5):**
  For 5_model_*.yaml files:
    - ModelInstanceClass found in code/hainn/instance/ ([BLOCK] if missing)
    - model_tuner_name found in code/hainn/tuner/ ([BLOCK] if missing)
    - Required YAML keys present: ModelArgs, TrainingArgs, InferenceArgs,
      EvaluationArgs, aidata_name, aidata_version, modelinstance_name ([ERROR])

**Endpoint resolution (stage 6):**
  For 6_endpoint_*.yaml files:
    - EndpointFnClass found in code/haifn/fn_endpoint/ ([BLOCK] if missing)
    - Required YAML keys present: EndpointArgs, modelinstance_name,
      modelinstance_version ([ERROR])

**Builder sync (stages 1-4, 6):**
    - build_*.py exists in code-dev/ for each declared stage ([WARN] if missing)
    - Generated file exists in code/haifn/ ([ERROR] if builder exists but no output)

**Import resolution:**
  Scan task .py files for haifn/hainn imports.
  Each imported class must exist in code/ ([ERROR] if broken).

---

Step 4: Generate/Update Docs
==============================

Create docs/ if it does not exist.

**docs/TODO.md** -- create or update:
  Scan project to fill three tables. Sync existing rows (upgrade status only).

  Template:

    # TODO -- {PROJECT_ID}
    # Created: {YYMMDD}
    # Last reviewed: {YYMMDD}

    ## Task Progress

    | Task | Status | Notes |
    |------|--------|-------|
    | cook_modeltuner | done | |
    | cook_modelinstance | wip | Missing LLM results |

    ## Track A Stubs

    | Stub File | Paired Example | Status |
    |-----------|----------------|--------|
    | build_{dataset}_source.py | example_{dataset}_stage1_fn | todo |

    ## Pipeline Progress

    | Stage | Status | Notes |
    |-------|--------|-------|
    | Stage 1 Source | done | |
    | Stage 2 Record | done | |
    | Stage 5 Model  | wip  | |

    Status values: todo | wip | done | n/a

**docs/data-map.md** -- always regenerate (overwrite):
  Derive from task config/ YAMLs cross-referenced with code/.

  Template:

    Data Map: {PROJECT_ID}
    =======================
    Generated: {YYMMDD}

    Pipeline Flow
    -------------

      {dataset} (raw)
           |
           v  Stage 1 -- Source
           |  FnClass:  {SourceFnClass}     [done / stub / missing]
           |  Config:   tasks/{G}_{group}/{task}/config/1_source_{dataset}.yaml
           v
      SourceSet ({dataset})
           |
           v  Stage 2 -- Record
           |  FnClass:  {RecordFnClass}     [done / stub / missing]
           ...
           v
      AIDataSet ({dataset})
           |
           v  Stage 5 -- Model
           |  ModelClass: {ModelInstanceClass}   [done / stub / missing]
           |  Config:     tasks/{G}_{group}/{task}/config/5_model_{name}.yaml
           v
      ModelInstance ({name})  ->  results/ + _WorkSpace/

    Stages
    ------

      | Stage | Status | FnClass / ModelClass | Dataset | Config File |
      |-------|--------|----------------------|---------|-------------|
      | 1 Source | {status} | {FnClass} | {dataset} | tasks/{G}_{group}/{task}/config/... |
      ...

    Status: done (class found), stub (TODO_* or not found), missing (no YAML), n/a
    Omit n/a stages from the pipeline flow diagram.

**docs/dependency-report.md** -- always regenerate (overwrite):
  Cross-reference config/ YAMLs with code/INDEX.md.

  Template:

    Dependency Report: {PROJECT_ID}
    ================================
    Generated: {YYMMDD}

    Pipeline Function Dependencies
    --------------------------------

      | FnClass | Stage | Location in code/ | Status | Also used in |
      |---------|-------|-------------------|--------|--------------|
      | {FnClass} | {N} | {path or "not found"} | {done/stub/missing} | {Projects} |

    ML Model Dependencies
    ----------------------

      | ModelClass | Family | Tuner | Location in code/ | Status | Also used in |
      |------------|--------|-------|-------------------|--------|--------------|

    Reuse Opportunities
    --------------------
      {FnClass} -- shared with {ProjectList}
      [If nothing shared: "All Fns and models are unique to this project."]

    Missing Implementations
    ------------------------
      {FnClass} (Stage {N}) -- not found in code/haifn/
        Action: run /haipipe-data design-chef {N}
      {ModelClass} -- not found in code/hainn/instance/
        Action: run /haipipe-nn

---

Step 5: Generate/Update README.md Files
=========================================

**tasks/README.md** -- create if missing, sync if exists:
  - Status table: every task gets a row (infer description from name and config/)
  - Orphan rows (row without matching folder) marked [ORPHAN]
  - Status synced: stub (no runs) | wip (some results missing) | done (all runs have results)

**{G}_{group}/README.md** -- create if missing, sync task list:
  - Every task in the group gets a row
  - Status synced same as above

**Per-task README.md** -- create if missing, sync runs/ status:
  - Runs table: every .sh in runs/ gets a row
  - Status upgraded to "done" when matching results/ folder exists with content

---

Step 6: Output Gap Report
===========================

Print a structured report grouped by:
  Naming, Structure, Per-Group, Per-Task Config,
  Run-Result Alignment, Heavy Files, Code Sync, Docs.

End with:
  - Summary: BLOCK: N, ERROR: N, WARN: N, NOTE: N
  - Proposed Actions: prioritized fix list
  - If zero issues: "All checks PASSED. Project is conformant."

---

MUST NOT
---------

- Do NOT modify config/ files, code/, code-dev/, or task scripts (except README.md)
- Do NOT run pipeline commands
- Do NOT modify cc-archive/ or paper/

---

Next Steps
-----------

After review:
  - If structure issues found: run /haipipe-project organize to fix layout
  - To see a task-by-task summary: run /haipipe-project overview
  - To generate a project summary: run /haipipe-project summarize

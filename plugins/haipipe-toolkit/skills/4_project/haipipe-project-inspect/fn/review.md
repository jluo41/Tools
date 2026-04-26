fn-review: Project Gap Analysis
===================================================

Inspects an existing project against the standard structure (see
../../haipipe-project/ref/project-structure.md). Outputs a gap report
with severity tags. Read-only — issues are flagged here, fixed by
/haipipe-project organize.

Severity tags: [BLOCK] [ERROR] [WARN] [NOTE]

Execution checklist (track progress):
  [ ] Step 0   identify target project
  [ ] Step 1   validate naming + top-level structure
  [ ] Step 2   project-level diagram/ check
  [ ] Step 3   per-group + per-task review
  [ ] Step 4   per-task diagram/ check
  [ ] Step 5   code sync check
  [ ] Step 6   paper diagram check (if paper/ exists)
  [ ] Step 7   output gap report

The doc surface is diagram/, NOT README.md. Any README.md found at
project, group, or task level is flagged [WARN] with the suggestion
to migrate via /haipipe-project organize --fix migrate-to-diagram.

---

Step 0: Identify Target Project
=================================

Follow the auto-detection rules in SKILL.md.
Confirm PROJECT_PATH and PROJECT_ID before proceeding.

---

Step 1: Validate Naming + Top-Level Structure
================================================

**Naming:**
  - PROJECT_ID matches Proj{Series}-{Category}-{Num}-{Name}
    Pattern mismatch -> [BLOCK]
    Minor issues (underscore in Name, missing Num) -> [WARN]

**Mandatory:**
  - tasks/ exists ([BLOCK] if missing)
  - diagram/ exists ([BLOCK] if missing — every project must have a story)

**Optional (absence is fine):**
  - paper/ ([NOTE] if missing)

**Forbidden at top level:** flag [WARN] each, recommend organize:
  - README.md  (replaced by diagram/)
  - docs/      (replaced by diagram/)
  - cc-archive/ (no longer part of standard layout)
  - _old/       (use git history instead)
  - config/     (must live inside each task)
  - results/    (must live inside each task)

---

Step 2: Project-level diagram/ Check
=======================================

Walk {PROJECT}/diagram/.

**Required .txt sources:**
  - 01-story.txt        ([ERROR] if missing or empty)
  - 02-boundary.txt     ([ERROR] if missing)
  - 03-exploration.txt  ([ERROR] if missing)

**Required canvas:**
  - project.excalidraw  ([ERROR] if missing)

**Freshness check:**
  - project.excalidraw mtime ≥ max mtime of .txt sources
    [WARN] if any .txt is newer than the canvas — canvas is stale,
    re-run /diagram-ascii-canvas.

**Scope discipline (project-level is HIGH-LEVEL ONLY):**
  Scan .txt sources for operational content that does not belong here:
    - status tables for individual tasks  ([WARN] move to {task}/diagram/03-runs)
    - cross-task data-flow diagrams       ([WARN] move to {task}/diagram, or omit)
    - daily progress logs                  ([WARN] move to {task}/diagram/04-progress)
  Project-level diagram is for story / boundary / exploration. If
  operational content has crept in, flag and recommend migration.

---

Step 3: Per-Group and Per-Task Review
=======================================

**Group-level checks:**

For each group folder in tasks/ (excluding sbatch/):
  - {G}_{group}/README.md is FORBIDDEN ([WARN] if exists; recommend remove
    via /haipipe-project organize --fix migrate-to-diagram)
  - Group letter matches its tasks' prefix ([ERROR] if mismatch)
  - No flat task folders directly in tasks/ — must be inside a group ([WARN])

**Per-task structure checks:**

For each task folder inside each group:

  - At least one *.py exists in the task folder ([WARN] if missing)
  - {task}/README.md is FORBIDDEN ([WARN] if exists; recommend migration)
  - {task}/config/ exists with its own YAML files ([WARN] if missing)
  - {task}/config/ is not a symlink ([WARN] if symlink — each task owns its own)
  - YAML files parseable ([ERROR] if not)

**Run-result alignment:**
  - If runs/ exists: every .sh in runs/ has matching results/{name}/ ([ERROR] if missing)
  - If runs/ exists: every results/{name}/ has matching runs/{name}.sh ([ERROR] if orphaned)
  - If no runs/: results/ may contain flat files or default/ subfolder (OK)

**Logging-header check:**
  - Every runs/*.sh begins with the standard logging header
    ([WARN] if missing — recommend organize --fix paired)

**Heavy file check in results/:**
  - .pt, .pth, .ckpt, .safetensors, .npy, .pkl, .bin, .h5
    -> [ERROR] move to _WorkSpace/

**Track A example check:**
  - Every Track A stub has a paired example task ([WARN] if missing)

Aggregate DECLARED_STAGES from config/ YAML filenames across all tasks.

---

Step 4: Per-task diagram/ Check
==================================

For each task folder, walk {task}/diagram/.

**Required .txt sources:**
  - 01-overview.txt   ([ERROR] if missing — replaces task README)
  - 02-design.txt     ([ERROR] if missing)
  - 03-runs.txt       ([ERROR] if missing)
  - 04-progress.txt   ([ERROR] if missing)

**Required canvas:**
  - task.excalidraw   ([ERROR] if missing)

**Freshness check:**
  - task.excalidraw mtime ≥ max mtime of .txt sources
    [WARN] if any .txt is newer — canvas stale, re-bundle.

**Content discipline:**
  - 01-overview.txt has all four sub-blocks (What / Why / Inputs / Outputs)
    [WARN] if any block is empty or "TODO"
  - For Stage 5 tasks (ModelArgs in config/), 02-design.txt MUST contain
    an ASCII forward-pass diagram + architecture sweep table
    ([WARN] if missing)
  - 03-runs.txt runs table reflects actual runs/ folder contents
    [WARN] if a row is missing for an existing runs/*.sh
    [WARN] if a row exists for a deleted runs/*.sh
  - 04-progress.txt has at least one entry ([NOTE] if only the seed line)

---

Step 5: Code Sync Check
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

Step 6: Paper diagram/ Check (if paper/ exists)
=================================================

For each paper/Paper-{Name}-{venue}/:

  **Required .txt sources:**
    - 01-overview.txt    ([WARN] if missing)
    - 02-figure-plan.txt ([WARN] if missing)
    - 03-rebuttal.txt    ([NOTE] only relevant during rebuttal)

  **Required canvas:**
    - paper.excalidraw   ([WARN] if missing)

  **Freshness check:**
    - paper.excalidraw mtime ≥ max mtime of .txt sources

  **paper/ contents discipline:**
    - No eval scripts in paper/      ([ERROR] belong in tasks/C_evaluation/)
    - No raw data / model outputs    ([ERROR] belong in _WorkSpace/)
    - No pipeline configs            ([ERROR] belong in tasks/{task}/config/)

---

Step 7: Output Gap Report
===========================

Print a structured report grouped by:
  Naming, Top-level Structure, Project Diagram, Per-Group, Per-Task,
  Task Diagrams, Code Sync, Paper Diagram (if applicable).

End with:
  - Summary: BLOCK: N, ERROR: N, WARN: N, NOTE: N
  - Proposed Actions: prioritized fix list, with the right organize flag
    for each (e.g., --fix migrate-to-diagram, --fix paired, --fix flat-tasks)
  - If zero issues: "All checks PASSED. Project is conformant."

---

MUST NOT
---------

- Do NOT modify any file. This skill is read-only.
- Do NOT call /diagram-ascii or /diagram-ascii-canvas. Diagram authoring
  belongs to -new and -organize, not -inspect.
- Do NOT run pipeline commands.

---

Next Steps
-----------

After review:
  - Structure issues found:    /haipipe-project organize  (with the suggested --fix)
  - Stale canvases:             user re-runs /diagram-ascii-canvas <path>
  - Task summary view:          /haipipe-project overview
  - Project summary doc:        /haipipe-project summarize

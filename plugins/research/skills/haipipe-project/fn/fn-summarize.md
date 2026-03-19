fn-summarize: Post-Development Summary + Flow Chart
====================================================

Generates a human-readable summary of a completed (or in-progress) project.
Designed to be read by a new person or future self with zero prior context.
Output is brief, jargon-light, and includes a text flow chart.

Writes to: examples/{PROJECT_ID}/docs/project-summary.md

---

Step 0: Identify the Target Project
=====================================

Use the same auto-detection logic as fn-review.md Step 0:
  1. Check git status for recently modified files under examples/
  2. Find most recently modified project if ambiguous
  3. List all projects and ask if still unclear

Confirm path before proceeding.

---

Step 1: Gather Project Facts
==============================

Read the following in parallel. Collect facts into named slots.

  (a) Project identity:
      PROJECT_ID = folder name
      SERIES, CATEGORY, NUM, NAME from parsing the folder name

  (b) scripts/INDEX.md (if exists):
      -> SCRIPTS_TABLE: all scripts, their data, functionality, stage, status

  (c) config/ directory:
      -> DECLARED_STAGES: list of stage numbers from YAML filenames
      -> DATASETS: dataset names from YAML filenames
      -> MODEL_NAME: from 5_model_{name}.yaml (if present)

  (d) task results (inside scripts/*/results/):
      -> RESULT_FOLDERS: list of {task}/{variant} result folder names
      -> KEY_METRICS: read each scripts/*/results/*/metrics.json, extract top metrics
      -> KEY_REPORTS: read each scripts/*/results/*/report.md, extract first paragraph only

  (e) cc-archive/ directory:
      -> SESSION_COUNT: count of cc_*.md + di_*.md files
      -> DATE_RANGE: earliest and latest YYMMDD from filenames

  (f) config/5_model_*.yaml (if exists):
      -> MODEL_CLASS: ModelInstanceClass value
      -> MODEL_VERSION: modelinstance_version value

---

Step 2: Sync scripts/INDEX.md Status
=======================================

Before writing the summary, scan task result folders to update statuses.

For each task in scripts/INDEX.md where Status = "wip" or "stub":
  If scripts/{task}/results/ contains at least one subfolder with report.md or metrics.json:
    Update Status to "done" in scripts/INDEX.md.

Also sync each scripts/{task}/INDEX.md:
  For each run row where Status != "done":
    If scripts/{task}/results/{variant}/ exists with report.md or metrics.json:
      Update Status to "done".

Do NOT downgrade any "done" entries. Only upgrade stub/wip -> done.

Report: "Synced {N} task/run status(es) to done in INDEX.md files."

---

Step 3: Write the Summary
===========================

Write examples/{PROJECT_ID}/docs/project-summary.md with this structure:

```
Project Summary: {PROJECT_ID}
==============================
Generated: {YYMMDD}
Session history: {SESSION_COUNT} CC sessions ({DATE_RANGE})

What This Project Does
----------------------
[2-3 sentences. State: what problem this project addresses, what data it uses,
and what kind of model or analysis it performs. Plain English, no jargon.]

Example:
  This project benchmarks glucose forecasting models on the OhioT1DM dataset.
  It compares a TE-CLM foundation model against baseline statistical models
  using time-series cross-validation.

Pipeline Stages Used
--------------------
  [list only the stages used, one line each]
  Stage 1 (Source):  {dataset} via {SourceFnClass or "existing Fn"}
  Stage 2 (Record):  {dataset} via {RecordFnClass or "existing Fn"}
  Stage 4 (AIData):  {dataset} — {split_strategy if known}
  Stage 5 (Model):   {MODEL_CLASS} v{MODEL_VERSION}

Data
----
  Dataset(s): {DATASETS}
  Source:     {raw data location or "existing SourceSet"}

Key Results
-----------
[Pull from results/*/metrics.json. Show only the 3-5 most important numbers.
Use a simple table. If no metrics found, write "Results pending."]

  Task / Run                     | Key Metric      | Value
  -------------------------------|-----------------|-------
  train_num / phase1_gpu0        | MAE (test)      | 12.3
  train_num / phase1_gpu0        | RMSE (test)     | 18.1
  train_num / phase2_gpu0        | MAE (test)      | 11.8

Tasks
-----
[Copy the scripts/INDEX.md table here, condensed to done/wip tasks only.]

  Task | Description | Stage | Status
  -----|-------------|-------|-------
  train_num | Train TE-CLM num-token model | 5 | done
  train_tkn | Train TE-CLM token model     | 5 | wip

Flow Chart
----------
[ASCII text flow chart. Show: data source -> pipeline stages -> model -> results.
Keep it narrow (max 60 chars wide). No mermaid, no markdown fences.]

  {dataset} (raw)
       |
       v
  [Stage 1] SourceFn: {SourceFnClass}
       |
       v
  [Stage 2] RecordFn: {RecordFnClass}
       |
       v
  [Stage 4] AIData split ({split})
       |
       v
  [Stage 5] {MODEL_CLASS}
             version: {MODEL_VERSION}
       |
       v
  Results: {top metric} = {value}
           See results/ for full report

[If multiple stages are skipped or not used, omit them from the chart.]

How to Pick Up This Project
----------------------------
[3 bullet points max. What does someone need to do to continue this work?]

  - Run: source .venv/bin/activate && source env.sh
  - Check scripts/INDEX.md for script status
  - Review results/project-summary.md (this file) for context
  - Next: {first TODO item from scripts/INDEX.md where Status != done}
```

---

Step 4: Confirm Output
========================

Print:

  Summary written: examples/{PROJECT_ID}/docs/project-summary.md
  INDEX.md updated: {N} status upgrades

  To share this summary:
    cat examples/{PROJECT_ID}/docs/project-summary.md

---

Checkpoints
-----------

Print these after Step 4 (verbatim — no extra analysis needed, Step 2 already synced INDEX.md):

  [CH-1] docs/ files updated?
  "Quick check: open docs/project-summary.md and confirm the flow chart
   reflects the active stages and Key Results has real numbers (not empty)."

  [CH-2] scripts/INDEX.md in sync?
  "Quick check: (1) scripts/INDEX.md has a row for every task subfolder;
   (2) each {task}/INDEX.md has a row for every run in {task}/runs/;
   (3) all status values (stub / wip / done) were just synced in Step 2."

---

MUST NOT
---------

- Do NOT modify config/ YAMLs or scripts/ during summarize — read only (except INDEX.md status).
- Do NOT run any pipeline commands.
- Do NOT write to cc-archive/ (that is for CC session exports, not summaries).
- Do NOT write to results/ — planning and summary docs go to docs/ only.
- Keep the summary SHORT. If results are not available yet, say so in one line.
  Do not pad with speculation.

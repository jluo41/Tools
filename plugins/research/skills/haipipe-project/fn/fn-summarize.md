fn-summarize: Post-Development Summary + Flow Chart
====================================================

Generates a human-readable project summary for someone with zero prior context.
Writes to: examples/{PROJECT_ID}/docs/project-summary.md

---

Step 0: Identify Target Project
=================================

Auto-detect from git status or ask. Confirm path before proceeding.

---

Step 1: Gather Project Facts
==============================

Read in parallel:

  (a) PROJECT_ID, Series, Category from folder name
  (b) tasks/INDEX.md -> all tasks, stages, status
  (c) Task config/ YAMLs -> declared stages, datasets, model name
  (d) Task results/ -> metrics.json values, report.md first paragraphs
  (e) cc-archive/ -> session count, date range
  (f) Model config (5_model_*.yaml) -> ModelClass, version

---

Step 2: Sync INDEX.md Status
==============================

Before writing the summary, upgrade status in tasks/INDEX.md and per-task INDEX.md:
  - If results/ has content for a "stub"/"wip" task/run -> upgrade to "done"
  - Never downgrade "done" entries.

---

Step 3: Write the Summary
===========================

Write examples/{PROJECT_ID}/docs/project-summary.md with these sections:

  **What This Project Does** -- 2-3 plain-English sentences.

  **Pipeline Stages Used** -- One line per active stage with FnClass/ModelClass.

  **Data** -- Dataset names and source.

  **Key Results** -- Top 3-5 metrics from results/*/metrics.json.
  Simple table. If no metrics: "Results pending."

  **Tasks** -- Condensed tasks/INDEX.md (done/wip tasks only).

  **Flow Chart** -- ASCII text flow chart (max 60 chars wide).
  Omit unused stages. Template:

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

  **How to Pick Up This Project** -- 3 bullet points max.
  Include: env setup, where to check status, what to do next.

---

Step 4: Confirm Output
========================

Print paths of written/updated files. Report count of INDEX.md status upgrades.

---

MUST NOT
---------

- Do NOT modify config/ or task scripts (except INDEX.md status)
- Do NOT run pipeline commands
- Do NOT pad with speculation -- if results unavailable, say so in one line

s13 · DataPrep Job UI preview: a prep version worked on inside its Block
========================================================================
view: ui-job

**Tags:** `Job UI`

**Stage:** shaping

**For:** a DataPrep Block's 💼 Jobs section, where a Job (one prep version) is worked on without leaving the Block page, as a screen preview in `delivery/ui/`, for JL to agree and for the workbench code (`servers/workbench/page/job_task_views/focus_jobs.py` and the insight theme's renderer)

**Delivery type:** ui

**UI preview:** Job · insight-dataprep

**Covers:** the four rows on a DataPrep Block (prep version, its Job, Main and Steps, the steps in order); the Job's Main (Overview with the version, 📊 Steps, 🔎 Runs on the Boards that pinned it); a step's view (Goal, Reads and Writes, Checks, Runs)

**Excluded:** the Board Job that runs a prep version (s11-insight-job-preview); the Question Book Job (s12-questionbook-job-preview); the shared frame (b17 `s11-work-job-preview`)

**Why:** what do the four rows and the Main become when a Job is a prep version and a Task is one step of it?

**Topic:** A DataPrep Job is one prep version (`jNN_prep-vK_<slug>`), so row 1 is its `prep:` and row 2 its one Job. Its Tasks are steps run in order, not questions, so row 3 is Main and one 🔧 Steps topic, and row 4 the steps, each marked ✅ once another agent agreed it (`agreed:` in `step.md`). The version runs nowhere in its own Block: a Board Job of three versions runs it in its t01 Run. So Main's Overview shows the version (signed, its hash, the Boards it serves); 📊 Steps lists them with what each reads and writes; 🔎 Runs lists every Board Job that pinned this version, its mark from the t01 Run's `runtime.yaml` and the ready folder it made. A step's view shows its goal, reads and writes, checks, and its line in each of those Runs (the light `metrics.json`, or the first step's experiment card).

**Feeds:** Q01


Files
-----

```text
s13-dataprep-job-preview/
├── s13-dataprep-job-preview.md        this face
├── s13-dataprep-job-preview.html      the views: Page (job-rows, job-overview, job-tasks, job-findings: one page, four marks), Effect (Steps and Runs)
└── delivery/ui/
    ├── steps-and-runs.html            Effect: the version's steps and the Board Jobs that ran it
    ├── prep-job-view-data.py          reads the prep versions, their steps, and the Board Jobs that ran them
    └── prep-job-view-data.js          its output for InsightDataPrep-Example (regenerate, never edit)
```

Regenerate: `python3 delivery/ui/prep-job-view-data.py ../../../insight/InsightDataPrep-Example > delivery/ui/prep-job-view-data.js` (needs PyYAML).


Decided
-------

s13-D01 · Page shows the example DataPrep Block's real Jobs view (Topic rows and Job Main, one address, two marks) and a step's page; Effect keeps only Steps and Runs, which the real page cannot draw yet (JL 261126: "please go ahead and do it")



Open
----

1. Row 3 has one topic (🔧 Steps): keep it, or let row 4 show the steps right under Main?
2. On the real page today a prep Job groups by decade (`j0N`), not by `prep:`; `focus_jobs.job_topic` reads only `release:`. Read `prep:` too?

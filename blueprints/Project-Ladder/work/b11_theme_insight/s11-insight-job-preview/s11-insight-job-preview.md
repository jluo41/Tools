s11 · Insight Job UI preview: a Board Job worked on inside its Board
====================================================================
view: ui-job

**Tags:** `Job UI`

**Stage:** shaping

**For:** the insight Board's 💼 Jobs section, where a Board Job (one question version × one data version, and a prep version when the Board has a DataPrep Block) is worked on without leaving the Board page, as a screen preview in `delivery/ui/`, for JL to agree and for the workbench code (`servers/workbench/page/job_task_views/focus_jobs.py` and the insight theme's renderer)

**Delivery type:** ui

**UI preview:** Job · insight

**Covers:** the four rows on an insight Board (question version, its Jobs by data version, Main and the DIKW levels, the questions at a level); the Job's Main (Overview with the pair, 📊 Tasks folded by level, 🔎 Findings against the previous Job); a question's view (Ask, Segments, Answer, Across Jobs)

**Excluded:** the shared frame, its rows, bands and folds (b17 `s11-work-job-preview`, `servers/workbench/ref/top-view-left-tab-right-content.md`); the stand-alone Job page's Report, Work and Studio (`t02_job_page/` s54, s55, s56); the Question Book Job (s12-questionbook-job-preview); the DataPrep Job (s13-dataprep-job-preview)

**Why:** b17's Topic rows let a person pick a Job and a Task inside the Block; what do those four rows and that Main become when a Job is a question version on a data version and a Task is one question at one DIKW level?

**Topic:** b17 s11 settled the frame: the Block is the one index page, and its 💼 Jobs section has four rows (Job topic, Job, Task topic, Task), a Main with Overview, 📊 Tasks and 🔎 Findings, and a Task view with its folds. An insight Board fills the same rows from its own names. Row 1 is the question version (`release:` on the Job face, `question-v1`), because a Board's Jobs group by the analysis plan, not by decade. Row 2 is its Jobs, one per data version (`j02 · data-v2`, `j01 · data-v1`), and the prep version when a Job pins one (`j03 · data-v2 · prep-v1`), newest first, a closed Job faded. Row 3 is Main, then the DIKW levels the Job's questions use (🗂 Data · D, 📈 Information · I, 🧠 Knowledge · K, 🧭 Wisdom · W, 🎯 Executive · X), read from the Task folder's letter (`t03_I01_outcome-by-arm`). Row 4 is the questions at that level, each with its `answer-status:` mark (✅ answered, 🔶 partial, ⬜ open). On Main, the Overview's middle fold is the pair (question version × data version, and what moved since the previous Job); 📊 Tasks has one fold per level, each question a row whose opening shows its answer and its segment Runs (`r01_full`, `r02_first` …) with each segment's takeaway; 🔎 Findings is the Job's `reports/vs-jNN.md`, held or changed per question. A question's view has four folds: ❓ Ask (its `goal:`), 🧪 Segments (one row per segment Run, its mark from the Run's `status:`), 💬 Answer (`answer:` and `how-sure:`), ↔ Across Jobs (the same question in the other Jobs, and the comparison's row for it).

**Feeds:** Q01 · Q02


Files
-----

```text
s11-insight-job-preview/
├── s11-insight-job-preview.md        this face
├── s11-insight-job-preview.html      the views: Page (job-rows, job-overview, job-tasks, job-findings: one page, four marks), Effect (Segment grid)
└── delivery/ui/
    ├── segment-grid.html             Effect: the Job's questions × segments, one Run each
    ├── insight-job-view-data.py      reads the Board's Jobs, questions, segment Runs and comparison
    └── insight-job-view-data.js      its output for Insight-Example (regenerate, never edit)
```

Regenerate: `python3 delivery/ui/insight-job-view-data.py ../../../insight/Insight-Example > delivery/ui/insight-job-view-data.js`.


Decided
-------

s11-D01 · the real 💼 Jobs section groups an insight Board's Jobs by `release:` and its Tasks by DIKW letter; a closed Job reads faded (`page/job_task_views/focus_jobs.py`, test `test_an_insight_board_groups_jobs_by_question_version_and_tasks_by_level`) (JL 261126: "do it as you planned")

s11-D02 · one topic per kind of Job: s11 the Board Job, s12 the Question Book Job, s13 the DataPrep Job, each previewed from its own example under `insight/`; the real page has one renderer for all three (`focus_jobs.py`), and a Board Job that pins a prep version reads `j03 · data-v2 · prep-v1` (JL 261126: "should we have s12, s13 as well?")

s11-D03 · a question × a segment is one Run, never a Task: the Task view lists its segment Runs in the question version's segment order (its `partitions.md`, then cross), a refused Run with its reason; the Job's Main gains a 🧩 Segments grid, questions × segments, previewed in Effect as Segment grid. The quick views Topic rows and Job Main (`insight-job-view.html`) are in the code now and shown under Page (removed 261126) (JL 261126: "please go ahead and do it")

Still owed: the Job's Main on the real page is the insight theme's own Job Report (Sign and close, Overall Report); the Overview, 📊 Tasks by level and 🔎 Findings of this preview are not built yet.


Open
----

1. Row 1 has one button today (question-v1 only): keep it shown so a second version has its place, or hide it until there are two?
2. Row 3 names the levels by word and letter; would the letter alone (D I K W X) be enough once the reader knows them?
3. Findings shows held or changed per question; should a changed row also open the two answers side by side?

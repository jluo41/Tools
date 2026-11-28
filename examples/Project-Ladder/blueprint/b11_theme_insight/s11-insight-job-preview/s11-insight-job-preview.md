s11 · Block Job UI Preview: Insight Board
====================================================
view: ui-job

**Tags:** `Job UI`

**Stage:** shaping

**For:** an Insight Board Job and its Tasks inside their owning Block.

**Delivery type:** ui

**UI preview:** Job · Insight Board

**Why:** What must this kind of Job and its selected Task make understandable?

**Topic:** A fixed question version × data version, with a pinned prep version when used.

**Feeds:** Q01

Main
----

Brief holds the research goal, evidence, version pins and limits. Plan + Results relates each question to its segment Runs, output and obstacles. Findings holds the resulting understanding and comparisons, linked to the same source records.

Selected Task
-------------

A question Task shows the ask, method, evidence, segment Runs, answer, review and cross-Job comparison. The prep Task instead shows the execution of the whole preparation chain.

Views
-----

Page-Job embeds the real Insight-Example Block with j03 selected: job-rows, job-overview, job-tasks and job-findings. Page-Task selects its actual t02 in the same Block. Job types and Task types read the owning contracts; they do not create schema fields. QuickHtml holds Segment grid. Draw preserves the native MindMap and editable Canvas. Outputs stay in their original files and the shared Files pane.

Sources
-------

- [Shared Studio Type: Block Job UI Preview](../../b17_theme_work/s72-studio-type-block-job-ui-preview/s72-studio-type-block-job-ui-preview.md)
- [Actual example](../../../insight/Insight-Example/board.md)
- [Binding generator](../delivery/structure/build_job_previews.py)
- [Current bindings](studio-views.json)
- [Segment grid proposal](delivery/ui/segment-grid.html)

Checklist
---------

- [x] Open j03 and t02 inside Insight-Example; keep the Block title and route.
- [ ] Compare Brief, Plan + Results and Findings with their owning sources.
- [ ] Check Segment grid against the implementation; retain the proposal until its case passes.
- [ ] Open source files and Canvas without copying content into this Studio.

Decided
-------

s11-D01 · the real 💼 Jobs section groups an insight Board's Jobs by `release:` and its Tasks by DIKW letter; a closed Job reads faded (`page/job_task_views/focus_jobs.py`, test `test_an_insight_board_groups_jobs_by_question_version_and_tasks_by_level`) (JL 261126: "do it as you planned")

s11-D02 · one topic per kind of Job: s11 the Board Job, s12 the Question Book Job, s13 the DataPrep Job, each previewed from its own example under `insight/`; the real page has one renderer for all three (`focus_jobs.py`), and a Board Job that pins a prep version reads `j03 · data-v2 · prep-v1` (JL 261126: "should we have s12, s13 as well?")

s11-D03 · a question × a segment is one Run, never a Task: the Task view lists its segment Runs in the question version's segment order (its `partitions.md`, then cross), a refused Run with its reason; the Job's Main gains a 🧩 Segments grid, questions × segments, previewed in Effect as Segment grid. The quick views Topic rows and Job Main (`insight-job-view.html`) are in the code now and shown under Page (removed 261126) (JL 261126: "please go ahead and do it")

Still owed: the Job's Main on the real page is the insight theme's own Job Report (Sign and close, Overall Report); the Overview, 📊 Tasks by level and 🔎 Findings of this preview are not built yet.

Open
----

- Preparation still needs its semantic group in the shared reader.
- The Segment grid is a proposal; it is not a claim that Main already implements that grid.
- Automatic type-to-instance comparison belongs in the shared Checklist interface.

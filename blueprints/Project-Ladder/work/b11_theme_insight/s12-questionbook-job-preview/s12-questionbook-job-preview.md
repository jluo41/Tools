s12 · Question Book Job UI preview: a question version worked on inside its Book
================================================================================
view: ui-job

**Tags:** `Job UI`

**Stage:** shaping

**For:** a Question Book's 💼 Jobs section, where a Job (one question version) is worked on without leaving the Book page, as a screen preview in `delivery/ui/`, for JL to agree and for the workbench code (`servers/workbench/page/job_task_views/focus_jobs.py` and the insight theme's renderer)

**Delivery type:** ui

**UI preview:** Job · insight-questionbook

**Covers:** the four rows on a Question Book (question version, its Job, Main and the DIKW levels, the questions at a level); the Job's Main (Overview with the version and its segments, 📊 Questions by level, 🔎 Changes against the version before and the open proposals); a question's view (Ask, Method, Needs, Segments, Across versions)

**Excluded:** the Board Job (s11-insight-job-preview); the DataPrep Job (s13-dataprep-job-preview); the shared frame (b17 `s11-work-job-preview`)

**Why:** what do the four rows and the Main become when a Job is a question version and a Task is one question as that version asks it?

**Topic:** A Question Book Job is one release (`jNN_question-vN_<slug>`), so row 1 is its `release:` and row 2 its one Job. Its questions are the version's `release.yaml`: each kept from an earlier version (its Task stays in that version's folder) or new in this one, marked 🆕 when the version has a `from:`. Row 3 is Main and the DIKW levels its questions use; row 4 the questions at a level. Main's Overview shows the version (signed or not, and the version it came from) and its segments (`partitions.md`); 📊 Questions folds by level, each question opening on its ask and its needs; 🔎 Changes lists the new questions against the version before, and, while the version is open, the Book's proposals waiting for the next one. A question's view reads its `question.md`: ❓ Ask, 🧭 Method (ask, answer, read), 📐 Needs, 🧩 Segments asked, ↔ Across versions.

**Feeds:** Q01


Files
-----

```text
s12-questionbook-job-preview/
├── s12-questionbook-job-preview.md        this face
├── s12-questionbook-job-preview.html      the views: Page (job-rows, job-overview, job-tasks, job-findings: one page, four marks), Effect (Version changes)
└── delivery/ui/
    ├── version-changes.html           Effect: what a version changed from the one before, and the proposals waiting
    ├── book-job-view-data.py          reads the Book's versions, questions, segments and proposals
    └── book-job-view-data.js          its output for InsightQuestionBook-Example (regenerate, never edit)
```

Regenerate: `python3 delivery/ui/book-job-view-data.py ../../../insight/InsightQuestionBook-Example > delivery/ui/book-job-view-data.js` (needs PyYAML).


Decided
-------

s12-D01 · Page shows the example Book's real Jobs view (Topic rows and Job Main, one address, two marks) and a question's page; Effect keeps only Version changes, which the real page cannot draw yet (JL 261126: "please go ahead and do it")



Open
----

1. Row 1 and row 2 hold the same thing (a version is its one Job): keep both rows, as the real page draws them, or show only row 2 on a Question Book?
2. A kept question's Task lives in an earlier version's folder: should its button say which version it comes from?

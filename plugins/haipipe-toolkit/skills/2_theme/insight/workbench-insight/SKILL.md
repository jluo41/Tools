---
name: workbench-insight
description: >-
  The insight theme of the shared workbench frame: an insight Board, each Job
  (one release × one data version) and each Task (one question) open on the
  frame's tabs Guide · Block · Job ▾ · Task ▾, each with the six Spaces
  (Description · Idea Studio · Audience Report | Work Details | Runs ·
  Delivery) as b11's s11 · s12 · s13 draw them, and a Runs panel whose buttons
  are the insight run cards by level and Space. Read-only: it shows the Board's
  and the Prototype's files and copies prompts; every write stays with the
  insight skills. Use to see or explain what an insight screen shows, which file
  each view reads, and which card a button copies. Trigger: insight workbench,
  insight tab, insight Board tab, insight Job tab, insight Task tab, insight
  spaces on screen, /workbench-insight.
metadata:
  version: "1.0.0"
  last_updated: "2026-10-08"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /workbench-insight · the insight theme on the shared frame

**LOAD `workbench` FIRST.** It defines the common Workbench law (STORAGE, SURFACE, WRITER, BOUNDARY) and the frame
every theme shares (`servers/workbench/`). This skill is insight's delta: which views each level's Spaces show,
where they read, and which run cards their Runs panels list.

The design is drawn in `Tools/blueprints/b01_haipipe-toolkit/j11_theme_insight/studio/`: s11 (the Board), s12 (a Job), s13 (a Task), s21
(the Runs and skills), s31 (the Guide by level). The folders are `haipipe-insight/ref/insight-ladder.md`. The page
that came before (`/_board/insight-board`) is retired and redirects here; what it showed is kept in
[`ref/old-page.md`](ref/old-page.md) and [`ref/insight-board.md`](ref/insight-board.md).

```text
the link       /_board/workbench?path=<Project>/insights/Insight-<name>[/<Job>[/<Task>]]
the server     servers/workbench-insight/insight_theme.py (the Theme) · insight_views.py (the three levels) ·
               insight_plan_c.py (reads the Board and its Prototype) · guide/guide.yaml (the Guide's words)
the cards      haipipe-insight-workflow/ref/run-cards.md (one per button; scripts/run_cards.py --check)
the table      ref/workbench-table.md, generated from the cards by scripts/cards_table.py; never edited by hand
```


The three levels
----------------

```text
          Description                  Idea Studio        Audience Report                 Work Details        Runs · Delivery
Block     Map (releases × data         question map ·     Partition × Reading: Coverage · the Jobs: All ·     soft · from below ·
(Board)   versions) · Prototype ·      topics             Tracks · Consistency · Findings p1 · p2 …           Handoff
          Dataset · Partitions
Job       the Job's line (pN × vM ·    topics             Partition × Period: Current ·   Job → Task → Run    All · hard · soft ·
          state · moved) atop                             vs previous                     tree                launch · power ·
          Prototype · Dataset                                                                                 compare · propose · close
Task      Question · Records           topics             Table · Reading                 Partitions          All · hard · soft
```

Each Space reads files only: the Board's `board.md` (dataset, versions, prototype), the Prototype's releases
(`release.yaml`, `partitions.md`, each question's `question.md`), a Job's face and `reports/vs-<prev>.md`, a Task's
page and its Runs' `run.yaml` and `result/report.md`. A "… ↗" opens a file in the pop-out. The Prototype in `tasks/`
opens in the work theme until a Prototype level is drawn (s21 lists its run types).


The Runs panel
--------------

Each Space's buttons are the run cards whose `<Level> › <Space>` matches, shown in the views the card names. A button
shows its Run's name (`run-add-j<NN>`, `rNN_<partition>`) with its words in small under it, and copies the card's
prompt with `{folder}` filled in. A button the shared frame also has keeps the frame's Run name (Add a topic:
`run-draw-<sNN>`). The Guide's Runs (Add a method, Add a paper) are on every tab.

Change a button by changing its card, then rerun `scripts/cards_table.py` and
`haipipe-insight-workflow/scripts/run_cards.py --check`; the table and the check follow.


Boundary
--------

Nothing here writes. Adding a data version, a Job, a Run, a page or a signature is the skill the card names, run
by the agent it names; a person signs where it says. The workbench never shows a row of data: counts, rates and
the Runs' generated reports only.

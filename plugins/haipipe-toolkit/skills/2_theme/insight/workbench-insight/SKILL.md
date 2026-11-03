---
name: workbench-insight
description: >-
  The insight theme of the shared workbench frame: an insight Board, each Job
  (one release × one data version) and each Task (one question) open on the
  frame's tabs Guide · Block · Job ▾ · Task ▾, each with the six Spaces
  (Description · Idea Studio · Audience Report | Work Details | Runs ·
  Delivery) as b11's s11 · s12 · s13 draw them, and a Runs panel whose buttons
  are the insight run cards by level and Space. It shows the Board's and the
  Prototype's files and copies prompts; the one thing it writes is a person's
  own CHECK of a page and sign of a Job's close (POST /_board/insight-act),
  every other write staying with the insight skills. Use to see or explain what an insight screen shows, which file
  each view reads, and which card a button copies. Trigger: insight workbench,
  insight tab, insight Board tab, insight Job tab, insight Task tab, insight
  spaces on screen, /workbench-insight.
metadata:
  version: "1.4.0"
  last_updated: "2026-11-01"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /workbench-insight · the insight theme on the shared frame

**LOAD `workbench` FIRST.** It defines the common Workbench law (STORAGE, SURFACE, WRITER, BOUNDARY) and the frame
every theme shares (`servers/workbench/`). This skill is insight's delta: which views each level's Spaces show,
where they read, and which run cards their Runs panels list.

The design is drawn in `Tools/blueprints/Project-Ladder/work/b11_theme_insight/studio/`: s11 (the Board), s12 (a Job), s13 (a Task), s21
(the Runs and skills), s31 (the Guide by level). The folders are `haipipe-insight/ref/insight-ladder.md`. The page
that came before (`/_board/insight-board`) is retired and redirects here; what it showed is kept in
[`ref/old-page.md`](ref/old-page.md) and [`ref/insight-board.md`](ref/insight-board.md).

```text
the link       /_board/workbench?path=<Project>/insight/Insight-<name>[/<Job>[/<Task>]]
the server     servers/workbench-insight/insight_theme.py (the Theme) · insight_views.py (the three levels) ·
               insight_plan_c.py (reads the Board and its Prototype) · guide/guide.yaml (the Guide's words)
the cards      haipipe-insight-workflow/ref/run-cards.md (one per button; scripts/run_cards.py --check)
the table      ref/workbench-table.md, generated from the cards by scripts/cards_table.py; never edited by hand
```


The three levels
----------------

```text
          Description                  Idea Studio        Audience Report                 Work Details        Runs · Delivery
Block     Map (releases × data         question map ·     Overall Report · then           the Jobs: All ·     soft · from below ·
(Board)   versions) · Prototype ·      topics             Partition × Reading: Coverage · p1 · p2 …           Handoff
          Dataset · Partitions                            Tracks · Consistency · Findings
Job       the Job's line (pN × vM ·    topics             Overall Report · then           its steps:          All · hard · soft ·
          state · moved) atop                             Partition × Period: Current ·   1 Launch · 2 Run ·  launch · power ·
          Prototype · Dataset                             vs previous                     3 Write · 4 Check · compare · propose · close
                                                                                          5 Compare · 6 Close
Task      Question · Records           topics             Table · Reading                 Partitions          All · hard · soft
```

The words (JL 261011): the Map's corner reads `analysis plan \ data freeze`, a row `AP1 · first ladder`, a column `F1 · first 5 days`; the Job ▾ menu shows the Job's folder name as it is, `j01_prototype-p1-basic-questions_data-SMSR2v1` (JL 261012).

The Overall Report (JL 261012: "before the Full, we should have a Overall Report ... we can click and read it"): when a
release asks Executive questions (X), the Audience Report's first button, before Full, reads them as one document: a
section per question from its Task page, its one-line answer and how sure, its figure, its points, each `(K01 · t30)`
a link to the Task it rests on, and the print (`delivery/<job>/overall-report.pdf`). It opens with **At a glance**
(JL 261013: "figures to show it to quickly get the outcome"): a card per question, its outcome in bold over its
figure, a click to its section. The figures are the X pages' `figures:`, drawn by haipipe-insight
`ref/overall_figures.py` into `delivery/<job>/figures/`; one not drawn yet says so. At the Board it is the latest
Job's. No cut's table lists the X questions (`insight_views._overall`, `_figure`, `_board_overall`). Each Space reads files only: the Board's `board.md` (dataset, versions, prototype), the Prototype's releases
(`release.yaml`, `partitions.md`, each question's `question.md`), a Job's face and `reports/vs-<prev>.md`, a Task's
page and its Runs' `run.yaml` and `result/report.md`. A "… ↗" opens a file in the pop-out. The Prototype in `work/`
opens in the work theme until a Prototype level is drawn (s21 lists its run types).


A Job's Work: its steps (b11 s12, 261022)
-----------------------------------------

JL 261022: "how to make it that when the user want, they can open this work panel and work on it". A Job's Work is its
steps in the order a Job runs, one tab each: 1 · Launch · 2 · Run · 3 · Write · 4 · Check · 5 · Compare · 6 · Close
(`insight_views._work_view`). A tab is Operation over Result, as the draft and labeling Tasks' steps are:

```text
Operation  🚀 1 · Launch  ✓ done           folded until opened; its chip read from disk on every open
           Input          what the step has: pins, Runs on disk, pages written and checked, what is still to do
           Running now    a Run whose card says running (a soft Run: open)
           Prompt         the step's run card, the Job filled in, "Still to …" the Tasks named; your notes go with it
                          (user feedback:), then "Run this in the Claude session <Board>: <job>"
           🙋 sign        6 · Close only: a person signs the close
Result     a card per DIKW level (2 · Run: Task × cut marks; 3 · Write: each page's answer; 4 · Check: CHECK and
           alignment), the pins and cuts (1 · Launch), the comparison (5 · Compare), what the close freezes (6 · Close)
```

The chips: a step is done from its files (Launch: a closed run-launch, or the Runs ran; Run: every Data, Information and
Knowledge question answered or refused; Write: every page `written`; Check: every written page's `check:` starts ✅;
Compare: the comparison, or the proposals on a first Job, where it is optional; Close: the Job closed). The first step
not done is next (the close reads sign) and a bare link opens it; the old tree's links (`All`, `hard`, `soft`) open
2 · Run, whose last card is that tree. A page whose question has not run waits on 2 · Run. Each tab's buttons are the
Job › Work Details run cards whose `views` name its step. The screen still writes nothing.
In a real browser: `servers/workbench-insight/checks/job_work_browser.mjs` (its head says how to run it).

A Job on the focus page: Work by letter (b11 j01 s55, 261101)
-------------------------------------------------------------

The focus page (`layout=focus`, what `/wb` opens) shows an insight Job's Work in the Report's three letters, the same parts
the paper's version Work and the labeling Task's steps use (`servers/workbench/ui_parts.py`): each view ⚙️ Process
then 📊 Results, numbered sections, to-do rows that end in a state word, Copy prompt on a row, the one Prompt box for a
single next act. `servers/workbench-insight/insight_focus.py` draws them; `focus_page.py` asks it through one hook
(`insight_job_work`), as it asks the paper theme's.

```text
A Overall       Process  🙋 your signs · Write the Overall Report (its state: done, ready, waits on <questions>) ·
                         what the close freezes, once the close is yours to sign
                Results  the Overall Report · this Job: plan, freeze, state, what moved, the Job before
B Grid          Process  🙋 your signs · Launch all · Write all · Check all (Copy prompt each) · the grid, each
                         cell its next verb: launch on a planned Run, write on a page ready, check it on a written page
                Results  the question × cut grid, rows by DIKW level, marks only (Report B)
C vs previous   Process  🙋 your signs · "<n> changed answers to turn into proposals" · Compare, then Propose
                Results  the comparison against the Job before
```

Three letters, not four (s54 round 2): The pair's facts sit under the Overall Report.

🙋 your signs, first on every view, in their order: sign the plan (in the Prototype, `signed: ✅` on its release;
until then the Job is a preview), then close the Job (greyed with what it waits on; once every step is done, Sign the
close posts to `/_board/insight-act`). The steps' facts and states stay `insight_views` (`_work_facts`,
`_work_states`), so the focus page and the six-Space page agree. Tests: `tests/test_insight_focus.py`.


Every level on the focus page (b11 j01 s51 to s58, 261102)
-----------------------------------------------------------

The rest of the 3 × 3 is live in the same file, each view as its cell in b11 j01 (`insight_ui_cells.py`). A Report view
is its numbered sections only, no ⚙️ Process or 📊 Results band (s51-D02); a Work view is ⚙️ Process then 📊 Results,
its Results the Report view's own sections. Each opens on its first letter; MindMap stays last in Report.

```text
Board  Report  A Answers (question × Job) · B Questions (each, its DIKW level, where answered; the Board's own) ·
               C Jobs (analysis plan × data freeze, what each Job moved) · D Data (freezes, cuts) · E Handoff
       Work    the same letters; Process: 🙋 sign the newest plan, triage the proposals, then the letter's acts
               (write the Overall Report · propose questions · open the newest Job, add a Job · add a freeze, propose
               a cut · write the counsel, draft the handoff), each with its run card's Copy prompt
Job    Report  Overall · Grid (marks only) · vs previous          (Work: above)
Task   Report  Answer (the answer, how sure, what it rests on) · By cut (cut × step, the full result) ·
               Across Jobs · Plan (needs, may say, agreed)
       Work    the same letters; Process: the chain plan → agree → Runs → page → check → alignment, one verb live on
               the next link · the next act per cut, propose a cut · track across Jobs · the plan's steps. No 🙋
```

Hooks in `focus_page.py`: `insight_board_report` and `insight_views_for` (Board Work, Job Report, Task Report and Work),
beside `insight_job_work`. Tests: `tests/test_insight_focus.py` (`InsightLettersTest`).

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

Adding a data version, a Job, a Run or a page is the skill the card names, run by the agent it names. Two things a
person does on the screen itself (JL 261023: "design the work in a way that we human can operate this system as
well"), through one narrow route, `POST /_board/insight-act` (`servers/workbench-insight/insight_act.py`):

```text
CHECK a page     4 · Check, the page's row ▸ "check it": tick "I read the page and its Runs' results", then
                 ✅ Pass, or ↩ Return with the reason. Writes the page's check: line (✅ <YYMMDD> · a person, or
                 ↩ <YYMMDD> · a person · <why>) and a pass of run-check-tNN (by: a person). A returned page counts
                 as not written: 3 · Write lists it under "Returned by CHECK" and its prompt asks for a rewrite.
Sign the close   6 · Close, once every step before it is done: tick "I read what the close freezes", then Sign.
                 Writes the Job face's state: closed and signed: ✅ <YYMMDD>, and a pass of run-close-jNN.
```

Each re-reads the files and checks its gate before it writes (an unwritten page, a closed Job, a page a person wrote,
a step still open: refused, nothing written). The route answers only a page of this host (its Origin) and never a
read-only host. Board files carry no names: "a person". Everything else on the screen copies a prompt. The
workbench never shows a row of data: counts, rates and the Runs' generated reports only.
In a real browser: `servers/_host/checks/person_actions_browser.mjs`, on `person_actions_fixture.py`'s throwaway
Projects.

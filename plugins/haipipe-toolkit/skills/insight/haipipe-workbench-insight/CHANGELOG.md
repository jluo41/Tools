## 0.10.0 · 2026-10-02 · Carried questions and their runs (JL 261002)

- A Prototype and Instance board shows its carried short question and name in the Logic cell, and the ask, Why now, What would answer it and any other carried field under More; the Dataset view reads `0-Meta/meta.md`; a register page reads `<rung>/rung.md`. Layout unchanged.
- Workbench Table: Scope › Questions gains Carry a board over and Review the questions (a person signs a change); Insight › Work's Bind the work and Run a ticket become Write the question's script, Review the script and Run a partition; Settle the cell is gone (status is computed).

## 0.9.0 · 2026-10-02 · Methods move to Scope, with a Methods studio (JL 261002)

- Methods is a Scope tab (Dataset · Partitions · Methods · Questions); Insight keeps Questions. Its views: Discovery methods · Design methods · Methods studio · Papers. Methods studio embeds `ref/insight-methods.excalidraw` in the Excalidraw canvas, as the Design board's Theory › Methods studio does. The Workbench Table's Add a method and Add a paper rows move to Scope; the design drawing's Part 2 follows. Card and index wording names Scope › Methods.

## 0.8.0 · 2026-10-02 · Insight › Methods (JL 261002)

- New sub-space Insight › Methods beside Questions, with three views: Discovery methods, Design methods, Papers. Cards and paper cards use the Design workbench's renderers. New files: `ref/insight-discovery-methods.md`, `ref/insight-design-methods.md`, `ref/methods/discovery/`, `ref/methods/design/`, `ref/insight-papers.md`.
- Runs panel (Insight Space): Add a method, Add a paper.

## 0.5.0 · 2026-10-01 · Partition names, not letters (JL 261001)

- Register example uses the partition-name page id (`I<NN>-full`) and generic task/run names.

## 0.7.0 · 2026-10-01 · Work column by need (JL 261001)

- Server: the Work column lists each evidence need with what the page's `answers.yaml` binds to it, a red `not bound` for a gap, and only the runs those needs use; pages without bindings keep the ticket view. Part 1 of the studio drawing is read from `ref/workbench-table.md` with table-workbench's reader; Part 4 shows page folders, not the retired store.

## 0.6.0 · 2026-10-01 · Workbench Table and evidence needs (JL 261001)

- `ref/workbench-table.md`: the Insight Workbench Table (16 rows, `table-workbench --check` passes; planned: the two Insight agents and `haipipe-insight-partition`). "Plan the evidence", "Bind the work" and "Check alignment" are the rows that keep question and work aligned.
- `ref/insight-board.md`: the three columns meet at the evidence need; the served board does not read `answers.yaml` yet (next server change).
- Server: a Page Face page (`folder-kind:` declared) shows its Opening's answer and its `strength:` line in the Report column; the Logic panel lists the question's evidence needs and whether they are agreed.

## 0.3.0 · 2026-10-01 · Logic · Work · Report (JL 261001)

- Insight › Questions has three columns. Work shows only the task and its runs (the old
  "Answer" page link left it); Report shows what the answer says: a report file when one
  exists, else the old answer page's headline and Opening, marked as such.
- The Runs panel's Knowledge answer and Wisdom answer types became one Report type.
- A report opens as a document: `/_board/insight?board=&report=<partition>:<QID>`.

## 0.4.0 · 2026-10-01 · The answering page is the report (JL 261001)

- Work reads the answering page's `runs/` tickets first and falls back to config `answers:`;
  Report shows the answering page, labelled "page <id>". No `reports/` folder, no board store.
- The run view shows a ticket's result from the page's `results/<ticket>/`, figures above tables.

## 0.2.0 · 2026-10-01 · One dataset, logic left and work right (JL 261001)

- The board follows `servers/workbench-insight/studio/insight-workbench-design.excalidraw`:
  four Spaces (Scope · Insight · Check · Delivery), a dataset banner on every Space, a Runs
  panel beside each. Run Space and Evidence Space are gone: runs sit in the panels and on
  the Work side; the workflow runtime index moved to Check › Runtime.
- Insight › Questions: one High/Low table per partition. Logic is the MT01–MT04 questions by
  level and number (no QK codes on screen); Work is the task calls that answer them, joined by
  each config's `answers:` line and its MT00 partition. Cross lists only its own questions.
- A run opens its results in a pop-out (`/_board/insight-run`); a page opens as a document
  (`/_board/insight`). The page-level workbench (This page · Cites · Cited by · Gates · Log)
  and the question × partition grid are retired.
- `_task_calls` counts one call per task and name: tickets symlinked to one `_run.sh` had
  collapsed into a single call.

## 0.1.1 · 2026-09-28 · No content hashes (JL 260928)

- `servers/workbench-insight`: a question registration writes no `definition_hash` or
  evidence `sha256`; the Run Spec reader and request text no longer check or show one.
- Handoff eligibility checks that the recorded files and anchored receipts exist; the
  handoff reads stale when the signed Page or a whole-file dependency is newer than the
  GI5 receipt (file time). Hash fields left in older records are ignored.

## 0.1.0 · 2026-09-22

- New skill: the served face of the Insight family, paired with
  `servers/workbench-insight`. Until now the two 🔎 routes were named only in
  the Board skill's route table; the page grain was described inside
  `haipipe-page-insight` and the board grain inside `haipipe-insight`. This
  skill states the read-only contract of both grains in one place and leaves
  the domain with its owners.

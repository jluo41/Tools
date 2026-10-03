## 0.14.0 · 2026-10-03 · Partitions are the Insight Views; RoadMap Draw moves to the Prototype (JL 261003)

- The Insight Space's Views are its partitions, Full to Cross, in the View-tab look; the Questions and Studio tabs are gone.
- The working drawings move to Prototype › RoadMap Draw, in the Prototype's `studio/`, so every board of this kind sees the same ones.
- Workbench Table, design drawing and Guide text follow.
- A question's needs read as numbered steps in words, 🧮 Compute · 📎 Reuse · ⚖️ Answer, in the Insight Space's Work column and More ("How it is answered"); the E id stays in the files and shows only as a tooltip. The Prototype rung rows show no steps: a question there reads as its ask, why now and what would answer it.
- The board header is the title alone: the `all boards · board index` line is gone, on the board and on the board list.

## 0.13.0 · 2026-10-03 · A Prototype Space (JL 261003)

- New Space after Scope: Prototype, with Views Meta · Data · Information · Knowledge · Wisdom. Meta is the former Scope › Prototype view plus the partitions in words and the shared settings; each rung View lists its questions as folding rows (chips: partitions, needs, script, agreed) with retired ones folded. Scope keeps Dataset · Partitions · Questions.
- Space order Guide · Scope · Prototype · Insight · Check · Delivery: data, then what is asked and by which code, then the answers. Written as a shared rule in `workbench-shared/README.md` § Space order.
- Workbench Table: every View is a live tab (Prototype's design runs, Insight's runs under Questions, Check's Runtime, Delivery's Handoff); the design drawing's Part 1 has one column per Space and Part 2 gains the Prototype panel.

## 0.12.1 · 2026-10-02 · Workbench Table in the Guide, with folders (JL 261002)

- The Workbench Table gains the Folder column: where each run writes, in the Prototype, the Instance or Tools. The two Guide rows, which sat after the Notes and so were never read, are back in the table.
- Guide › RoadMap Draw shows the table (Space · View · Run type · Agent · Skill · Folder) in place of the Skills, Workbench and Folders lists; Agent and Skill share one column; the family entry names it with `table`.
- The table starts with Guide, as the workbench does, with all four Guide Views; Description and RoadMap Draw have no run.
- The RoadMap card is clean (its name only), its drawn table has the Folder column, and under it a Workflow drawn from the entry's `flow`: Question (Logic) → Work → Report over Input → Processing → Output, and the loop over partitions, questions and rungs. The design drawing above it folds ("Workbench design").
- A Guide opened alone forwards to its Insight board with the Guide open (`board_route`), or lists the Instance boards (`boards`); the board page keeps its Space tabs in view while Guide's canvases load.
- A trackpad pinch or ctrl-scroll no longer zooms the tab on the board, Guide or methods page (it zoomed every 127.0.0.1 port at once); keyboard zoom and the canvases' own zoom stay.
- Check › Gates labels a gate Gate-I0 … Gate-I6 (its id, GI0 …, stays in records and is the card's tooltip); Insight's Space tabs and View tabs follow the shared Guide's tab style (16px, a light-blue fill when selected), so the Guide and Insight rows look the same.
- The Guide's Views and content sit in one box (`wg-shell`), the same box a Space's content sits in.
- Scope › Prototype is laid out for the reader: a card with the Prototype and four numbers, one table by rung (questions, needs, scripts, this board's copies, retired), only the copies that need action as chips grouped by state, and the design files last with the shared code folded.
- The design drawing's frames stand apart: one 240px gap between frames, 40px inside each.

## 0.12.0 · 2026-10-02 · Guide holds the method, Scope holds the data (JL 261002)

- The shared Guide has four Views: Description · Method · RoadMap Draw · Related Paper. Insight's Method View shows the Prototype → Instance steps and then the discovery and design method cards with the Methods studio; RoadMap Draw is the whole design drawing, view only; Related Paper is the papers file. Both card pages come from `render_methods_embed`.
- Scope is the board's own data: Dataset · Partitions · Prototype · Questions. The Methods tab is gone, and Scope's Runs panel drops Add a method and Add a paper, which are Guide rows in the Workbench Table.
- Test: the methods test now checks that Scope has Prototype and no Methods, and that the embed page serves the cards and papers.

## 0.11.0 · 2026-10-02 · Insight › Studio and the Guide (JL 261002)

- Insight › Studio: a view beside Questions with the board's own working drawings, `studio/<name>.excalidraw` beside `board.md`, as folding rows (view only until Edit drawing; Open full screen; Add drawing). Scenes are minted and saved by the shared Studio routes, following the shared Workbench design's Task alignment. A space in a new name is saved as `_`, since the shared route takes the path as written.
- The shared Guide's Insight entry describes the Prototype and Instance boards: its skills, the five-step method, the Spaces and a folder map that resolves from an Instance board.
- Guide Views lead with the design drawing (JL 261002: the generated UI map is replaced by the workbench UI design we want): the generator wraps Parts 1, 2-3 and 4-5 in named frames, and each Guide View opens its frame view only, its generated drawing folded beneath. The drawing gains Insight › Studio and Check › Runtime tabs; nothing else in it moves.

## 0.10.0 · 2026-10-02 · Carried questions and their runs (JL 261002)

- A Prototype and Instance board shows its carried short question and name in the Logic cell, and the ask, Why now, What would answer it and any other carried field under More; the Dataset view reads `0-Meta/meta.md`; a register page reads `<rung>/rung.md`. Layout unchanged.
- Workbench Table: Scope › Questions gains Carry a board over and Review the questions (a person signs a change); Insight › Work's Bind the work and Run a ticket become Write the script, Review the script and Run a partition; Settle the cell is gone (status is computed).

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

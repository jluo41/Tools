Task Workbench in the Insight style: plan (261003)
==================================================

The Task Block Workbench (`servers/workbench-work/`) follows the Insight Workbench's style:
a bare header, the shared Space order with Delivery last, every View opened by a heading
and one lead sentence, the work Space as one Logic / Work / Report table, the drawings in
the setup Space, and Guide › Method served by the shared method page. Questions use the
skills in `skills/1_base/question/`. This file is the plan; the work is done in the phases below,
each verified before the next starts.

The reference is the Haipipe-Insight-v5 session and what it built: read its decisions
first, then the live Insight board and `servers/workbench-insight/insightboard.py`. Where
this plan and Insight-v5 differ, follow Insight-v5 and note the difference in the report.


Target
------

```text
📋 <Block title>                                     header: the title only
<block> · N Jobs · N Tasks · N Runs · N Questions    band (unchanged)
Guide · Scope · Task · Check · Delivery              Space order: Guide, setup, work, Delivery

Scope    Block · Questions · Resources · RoadMap Draw     setup: the Block, its asks, its data, its drawings
Task     <group> · <group> …   (one View per register group; "Questions" when none)
           Logic · the question │ Work · the Tasks and Runs │ Report · what it says
Check    Runs · Tasks · Reports                            judgments, unchanged
Delivery Reports                                           answered reports only
```


Phase 0 · Before editing
------------------------

1. Baseline: the host suite passes (`servers/_host/tests`, 37 tests); save the served page
   and `format=json` snapshot of one live Block to the scratchpad for before/after.
2. Shared files (`workbench/README.md` "Task / Task / Task" row,
   `guide_families.py` task entry, the conformance test) belong to the Workbench-Shared
   session: message it with the planned changes before editing them; edit only the task
   entry and the Task row.
3. Not touched: `code/haifn/`, any `results/**`, `board/**.html`; the board builder is not run.


Phase 1 · Shell and View openings
---------------------------------

1. Header: `<header><h1>📋 title</h1></header>` only, as Insight's (the `board.md` link
   stays in Scope › Block).
2. Every View starts with `<h2>` and `<p class="lead">`: one sentence saying what it reads.
   The `tw-explain` lines are replaced, not kept beside them.

| View | Lead |
|---|---|
| Scope › Block | The spine, the close condition and the Jobs, from board.md. |
| Scope › Questions | Each Question is one main topic; its Logic is a person's to sign. |
| Scope › Resources | The _WorkSpace folders the Jobs read, then the papers and links the Questions use. |
| Scope › RoadMap Draw | The question map, drawn from the register, then any drawing in studio/. |
| Task › <group> | One row per Question: what it asks, the Tasks and Runs that answer it, and its report. |
| Check › Runs | Every Run and its receipt status; a running receipt is not a heartbeat. |
| Check › Tasks | Each Task Folder's Runs and what its audit found. |
| Check › Reports | Each report's answer status, evidence warnings and next action. |
| Delivery › Reports | The answered reports, word for word, with the Results they cite. |

Files: `task_views.py` (render, bodies), `assets/css/90-task-workbench.css` (`h2`, `.lead`
with Insight's sizes: h2 17px, lead 14px muted).


Phase 2 · The Task Space as one table
-------------------------------------

1. Register: an optional `group:` on each Question (free text, for example the series a
   Question belongs to). `task_questions.extend_snapshot` carries it; `block-questions.md`
   and `haipipe-question` document it; the helper writes it through unchanged.
2. Views: one per group, in the order the register first names it; a register with no
   groups gets one View, "Questions". View keys are `q-<slug>`; the old key `task` opens
   the first one.
3. Each View: `<h2><group> · N Questions</h2>`, the lead, then Insight's head row
   (`.hl-head`): "Logic · the question", "Work · the Tasks and Runs", "Report · what it says".
4. One `.hl-row` per Question, three cells, no status anywhere:
   - Logic: a `kind` pill with the id (Q01), the title in bold, the question; a folded
     **More** (`details.q-more`): "What we expect" (hypothesis), "What would answer it"
     (acceptance), and register findings when there are any.
   - Work: `details.wk` open, summary "Task Work · N Tasks · N Runs", then today's
     Block → Job → Task → Run tree, unchanged.
   - Report: a `Report` pill, the title as a pop-out link, the Opening's first paragraph,
     the report's drawings, and a tag "report qNN". "No report yet" when absent.
5. Tasks under no Question: a closing `details.lvl` "Not under a Question · N Tasks" in
   the last group View, only when there are any.
6. Selecting a row (click outside its links) marks it and sends `space-target` with the
   Question id, so the Task Runs panel's prompts name it; if the shared panel's target
   cannot filter by Question, the selection only marks the row and the gap is noted.
7. Removed: the stacked cards (`question_html`, `.tw-question`, `.tw-columns`). Kept:
   `#question-<id>` anchors, now on the rows, so Scope › Questions and Check › Reports
   still link to them.

CSS: Insight's rules for `.hl-head`, `.hl-row`, `.hl-l/.hl-r/.hl-p`, `.kind`, `.q-more`,
`.rp-title`, `.rp-text`, `.rp-tags`, `details.wk`, `details.lvl`, copied with the same values
into `90-task-workbench.css`. Proposed to Workbench-Shared afterwards: move these rules
into one shared stylesheet both families read.


Phase 3 · RoadMap Draw moves to Scope
-------------------------------------

1. The Studio View leaves Task and becomes Scope › RoadMap Draw (key `studio` kept, so old
   links open it). Its rows, Edit drawing, Open full screen and Add drawing are unchanged.
2. A generated question map comes first: `servers/workbench-work/studio/question_map.py
   <block-dir>` reads the register and writes `<block>/studio/question-map.excalidraw`:
   one column of Questions by group, the Jobs and Tasks each one uses, and its report.
   The row is view only (no Edit drawing) and says "rerun question_map.py" when
   board.md is newer than the drawing. Only the script writes that file (rule 0).
3. Workbench Table: the Draw row moves to Scope › RoadMap Draw; a new row "Draw the
   question map" names the script's run.


Phase 4 · Delivery
------------------

1. A new last Space, Delivery, one View, Reports: each report whose `answer-status` is
   `answered`, with its title (pop-out), its whole Opening and Answer, its evidence links
   and drawings.
2. Empty state: "No Question is answered yet. A report moves here when its
   answer-status is answered."
3. Check › Reports stays: it keeps status, warnings and next actions for every report.
4. Guide's `spaces` list for the task family gains Delivery (the Space-order test checks
   it is last); the Workbench Table gains a Delivery › Reports row with run type none.


Phase 5 · Guide › Method through the shared method page
-------------------------------------------------------

The shared page (`workbench_guide.method_page_html`) is how Paper, Page and Labeling
already serve Method: a method file with fold cards and a methods drawing. Task joins it.

1. `skills/2_theme/work/workbench-work/ref/task-method.md`, in the shape of
   `page-method.md`:
   - 1 · The steps: `| step | what happens | methods | where in the workbench | who signs |`
     for Ask the question · Plan the Task · Build it · Review the code · Run the Ticket ·
     Report the Run · Write the report · Check, each naming its Space › View and runs.
   - 2 · Step 1 in depth: question-asking. Points to `haipipe-question-asking` (its eight
     cards) and `haipipe-question-review` (Q1 to Q7); no copies here.
   - 3 · Steps 2 to 6 in depth: building and running, with Task's own cards.
   - 4 · Steps 7 and 8 in depth: reporting from exact Results, and the independent check.
   - 5 · Checking: `| test | asks | when | source |`: code review before the Ticket
     (gate 1), the result gate, the complete receipt, generated files only from their
     generator (rule 0), evidence newer than the report, the Page CHECK.
   - 6 · Why it works; Reference (terms: Block, Job, Task, Run, Ticket, Result, receipt).
     One made-up example runs through the page; no project data.
2. Cards: `ref/methods/{run,report}/NN-by-*.md`, the card shape of Page's (family, move,
   comes from, reads, returns, test now, test in use; what the literature says).
   Planned: by contract first, by independent code review, by ticket and receipt, by light
   Result and heavy store; by report from exact Results, by independent check.
3. `ref/task-papers.md`: each `group` becomes a card name, so every card lists its papers;
   `table-papers --online` passes.
4. `guide_families.py` task entry: `method_doc`, `method_drawing`, and
   `explain["method"] = ("/_board/guide", {"family": "task", "mode": "method"}, "", "only")`;
   the `method` list keeps the same eight steps (the conformance test needs it).
5. `ref/task-methods.excalidraw`: first version from `designs/b02_workbench/studio/s02-guide-drawings/method-canvas.py
   task-method.md task-methods.excalidraw`; after that the canvas is the source.


Phase 6 · Skills in the Workbench Table
---------------------------------------

1. Ask a Question: skill `haipipe-question-asking`; it records through `haipipe-question`.
2. Review the questions: skill `haipipe-question-review`, a different agent from the asker.
3. `haipipe-task-question (new)` leaves the planned list for those two rows.
4. `table-workbench --check` passes; `task-workbench-design.py` is rerun so Guide ›
   RoadMap Draw shows the new table.


Phase 7 · Docs and checks
-------------------------

1. Docs: `workbench-work/SKILL.md` (0.5.0) and `CHANGELOG.md`; this server's
   `README.md`; `block-questions.md` (`group:`); the shared README's Task row (through
   Workbench-Shared).
2. Checks after a host restart: the host suite and the conformance test pass; the served
   page has the title-only header, five Spaces with Delivery last, an `h2` and a lead in
   every View, one row per Question in the Task Views, Method served by the shared page;
   `format=json` matches the baseline apart from the new fields; no tracebacks in the log.
3. A headless-browser pass over every Space and View when one is available; otherwise the
   served HTML is checked and the visual check is left to the person.


Defaults, unless the person says otherwise
------------------------------------------

1. `group:` is optional; with no groups the Task Space has one View, Questions.
2. Delivery shows answered reports only.
3. Add drawing stays in RoadMap Draw (Task's drawings are freeform, unlike Insight's).
4. Status stays out of the Task table; Check › Reports keeps it.
5. Nothing is committed until the person asks.

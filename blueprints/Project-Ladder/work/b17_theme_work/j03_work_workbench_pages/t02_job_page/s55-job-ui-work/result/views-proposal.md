# s55 · Job UI: Work · the views, proposed

for: b17.j03.t02-s55:theme_work.work_workbench_pages.job_page @ job_ui_work
written: 2026-10-31, by an agent for JL; nothing here is decided until JL answers the form
the page: `/_board/workbench?path=<block>/<jNN_job>&layout=focus&section=work` (a work Job's Work section, verb do)
JL's choices: `../../runs/r02_collect_job_work_views/` (four questions, each option with its preview, written by
`../../scripts/build_r02_previews.py`)
sample: b17's own `j03_work_workbench_pages` (public, read from disk); the private 5599 Job was read for its view and
section names only

Words used below, each defined once:

- **Job**: a folder `jNN_<job>/` with its face `jNN_<job>.md`; the face's `## Tasks` lists its Tasks in order,
  one line each, `N. tNN_<task> · <title>` (haipipe-job `ref/job-contract.md`).
- **Task**: `tNN_<task>/` with its face `tNN_<task>.md` (`goal:`, `close:`, `state:`, `task-type:`) and its `runs/`.
- **hard Run**: `runs/rNN_<slug>/`; its output lands only in its own `result/` (a compute Run; a form is hard too).
- **soft Run**: `runs/run-<type>-<target>/`; agent work, each round a pass in `passes/pNN-<MMDD>/pass.md`.
- **form** (a collection Run): `runs/rNN_collect_<slug>/`; questions in `question_collection.md`, the form
  `rNN_collect_<slug>.html`, the answers in `result/answer_collection.md` (haipipe-interaction).
- **sNN**: a Studio topic, `sNN-<slug>/`, beside the Jobs and Tasks; its `delivery/render.yaml` names, for each piece
  of its delivery, the Run that makes it (`by:`, b35 s01-D14).
- **word**: the one state word a row carries: 🙋 waits for you, ⏳ running, ❗ failed, ⬜ not run yet, ✅ done (JL
  261029: no 🔶; "partly done" is written in words).


## (a) The view list

Work's view-button-list, in order, with my picks (Q1 A, Q2 A):

1. **Tasks** (opens first; with my picks the only button): the Job's Tasks in its face's `## Tasks` order; first
   what waits for you; each Task with its word, what it makes and its Runs.

Two buttons join only on another answer:

2. **Runs** (only if JL picks Q1 B): every Run of the Job and its Tasks, Task by Task.
3. **Deliverables** (only if JL picks Q2 B, and only when the face has a `## Deliverables` block): the Job's to-do
   list, ticked from disk.

The Job page opens on Work (haipipe-ui: every level below the Block is judged by its Work), and Work opens on Tasks. A
section with one view keeps its one button (haipipe-ui rule 2), so the goal-line never moves.

The Tasks view with my picks, on j03:

```text
j03_work_workbench_pages  Work
[Tasks]
Goal  the work theme's three pages on the focus page, ...
Its Tasks in its face's order: where each stands and what waits.
🙋 Interactions ........................................... [Answer all]
   Block Report views   t01_block_page                        [Answer]
   ... one line per form, sign or Run waiting on you (nine forms on j03)
t01_block_page  The work Block page                     🙋 waits for you
   the work Block's page on the focus page, its Report, Work and Studio
   makes b17-s04 · block-page  ui  by run-design-block-page · ⬜ queued
   r01_collect_report_and_delivery  hard · collect  ✅ answered  [Interaction]
   r02_collect_block_report_views   hard · collect  🙋 waiting  [🙋 Interaction]
   run-design-block-page            soft · design   ⬜ queued   [Ticket]
   [🙋 Interaction]
t02_job_page ... t03_task_page ...      (the same rows)
Its own Runs                            (only when j03/runs/ exists; it does not)
```


## (b) Each view, its subsections in order

### View 1 · Tasks

Caption (the view-caption line): "Its Tasks in its face's order: where each stands and what waits."

**1. Interactions** (first; an orange box; Q3 A; named as b16's version Work and s52's pick name the same box)

- Shows: one line per thing that waits for the person at the Job or below: a waiting form (its title, the Task it
  sits in, Answer); a soft Run's pass that waits for a sign (its Run, its Task, Pass); a hard Run that is built and
  waits for its person to press Run (its Run, its Task, Ticket). The head says "🙋 Interactions" and, when two or more
  forms wait, carries Answer all.
- Reads: `focus_page.interactions(<job>, root)` rows whose state is `waiting` (each form's `run.yaml` `status:`, its
  `question_collection.md` `# title`, its `rNN_collect_<slug>.html`); every `runs/*/run.yaml` at the Job and its
  Tasks whose `signs:` names a person while its newest `passes/pNN-<MMDD>/pass.md` has no sign line; every hard
  `run.yaml` with `status: planned`, an `agent:` that names a person, and its ticket (`rNN_<slug>.sh` or `.ps1`) on
  disk. Answer all opens `<job>/runs/answer_all.html`, which `collect.py bundle <job>` writes (generated; rerun it).
- Empty: the box does not show (haipipe-ui: a section with nothing in it does not show).
- Tags: none on the head, and never a count (JL 261029); each line carries the form's own title and the Task's
  folder name.
- Actions: Answer (the form), Answer all (the combined page), Pass (the pass to sign), Ticket (the Run to press).

**2. The Task rows**, one per Task, in the face's `## Tasks` order; each a full-width row with a 1 px border:

- **2.1 Head**: the folder name `tNN_<task>` (opens the Task's page on Work), its title from the `## Tasks` line, its
  word on the right (Q4 A).
  - Reads: `jNN_<job>.md` `## Tasks`; the word from every `runs/*/run.yaml` under the Task and each hard Run's
    `result/runtime.yaml`. The most urgent wins: 🙋 waits for you, then ❗ failed, ⏳ running, ⬜ not run yet,
    ✅ done. A face `state:` that says closed overrides it as ✅ closed, since only a person closes a Task.
  - Empty: a Task with no `runs/` says ⬜ no Runs yet.
- **2.2 Goal line**: the Task face's `goal:`, its first clause (as `focus_page.one_line` cuts it).
  - Empty: the line is left out.
- **2.3 Makes line** (Q2 A): "makes `<sNN address>` · `<piece>`", the sNN's delivery type as a tag, then "by
  `<Run>` · `<that Run's word>`"; one line per piece.
  - Reads: every `delivery/render.yaml` in the Block (its own sNN and its Jobs' and Tasks' sNN), each piece whose
    `by:` is `jNN_<job>/tNN_<task>/runs/<run>`; the piece's name is the text before ":" in its value; the tag is
    that sNN face's `**Delivery type:**`. A Job that keeps a `## Deliverables` block adds each item whose `task:` is
    this Task: its `what:` and its tick from disk (haipipe-job rule 3, its partial written "partly", no 🔶).
  - Empty: "makes: not named yet" (muted), which is itself a finding: a Task no piece needs is a question for the
    Job (haipipe-task `ref/lifecycle.md`).
  - On j03 today: t01_block_page makes b17-s04's block-page, t02_job_page its job-page, t03_task_page its task-page,
    each by the Task's `run-design-<level>-page` (s04's `delivery/render.yaml`).
- **2.4 Run lines** (Q1 A): one per Run in the Task's `runs/`, by name: the name (monospace), kind · type, its word,
  one verb.
  - Reads: `frame.runs_of(<task>)` and each card. A form: ✅ answered when `result/answer_collection.md` exists, 🙋
    waiting when its form is built, ⬜ not sent yet before. A soft Run: ⬜ queued (no pass), ⏳ pass pNN (open), ✅
    done, from `status:` and `passes/`. A hard compute Run: `result/runtime.yaml` `status:` running ⏳, complete ✅,
    partial "partly done", failed ❗; none yet ⬜ planned.
  - Verbs, one each: a form, Interaction (🙋 Interaction in orange while it waits; the same button everywhere, b16
    t01 r04 Q6); a soft Run, Pass (its newest `pass.md`) or Ticket (`run-<type>-<target>.md`); a hard Run, Result
    (its `result/`, in the pop-out) or Ticket.
  - Empty: "no Runs yet" (muted).
- **2.5 Newest result in place** (kept from today's `focus_page.output_of`): the newest Run's `result/figure.png` or
  `result/preview.png`, with `result/display.yaml` `question:` and `result/headline.txt`.
  - Empty: nothing shows. If JL's answer on s54 puts each Task's result in the Report, this shrinks to the headline.
- **2.6 Row verb**: Interaction, 🙋 and orange while a form under the Task waits (it pops the list of the Task's
  forms, waiting first). The name itself opens the Task.
- Left off the row on purpose: "open points wait on you" from open sNN (Studio's, s56) and a picture (Studio's and
  Report's).

**3. Not in ## Tasks** (last; only when a `tNN_` folder is missing from the face's list, or a list line names no
folder)

- Shows: the same rows, each marked "not in ## Tasks" or "⬜ no folder yet".
- Reads: the same comparison `new_job.py check <job>` makes.
- Empty: does not show.

**4. Its own Runs** (last; only when `<job>/runs/` exists; named as s52's pick names the Block's)

- Shows: the Job's soft Runs (`run-face-jNN`, `run-add-tNN`, `run-delivery-<target>`), one line each as in 2.4. Its
  own forms sit in Interactions while they wait, and here once answered.
- Reads: `frame.runs_of(<job>)`.
- Empty: does not show (j03 has no `runs/`).

### View 2 · Runs (only if JL picks Q1 B)

Caption: "Every Run of its Tasks, Task by Task."

1. **Its own Runs** (first, only when `<job>/runs/` exists): as View 1, part 4.
2. **One group per Task**, in the `## Tasks` order: its heading is the Task's folder name (it opens the Task; the
   group folds by its heading and opens by default, haipipe-ui rule 4), then its Run lines exactly as 2.4.

- Reads: `frame.runs_of` for the Job and each Task, and each Run's card and receipt.
- Empty: "No Runs yet."
- With B, the Task rows in Tasks drop 2.4 and keep their word and their Interaction button.

### View 3 · Deliverables (only if JL picks Q2 B)

Caption: "What it must hand over, ticked from the disk." (today's `VIEW_WORDS["deliverables"]`)

1. **One group per Task that has items**, in the `## Tasks` order, its heading the Task's folder name.
2. **The Job itself** (last): items with no `task:`.

- Each item: its tick (✅ its files on disk and its Run finished; ⏳ its Run is running; ❗ a failed Run with nothing
  on disk; "partly" when some files are there or an `open:` line remains; ☐ nothing yet), its `what:`, its `kind:`
  as a tag, its `means:` bullets, its `files:` (each opens in the pop-out), its `open:` lines.
- Reads: the face's `## Deliverables` yaml block (`what · kind · task · means · files · count · run`), today drawn by
  `focus_page.deliverables_html`.
- Empty: the button does not show when the face has no `## Deliverables` (j03 has none; Q2 B's preview drafts three
  items from j03's `close:` line and each sNN's `delivery/ui/` path, and says so).
- With B, the Task rows drop 2.3.


## (c) What it leaves to the other cells

- **s54 · Job UI: Report** (`t02_job_page/s54-job-ui-report/`): the MindMap (the Job's Tasks with their Runs, as a
  map), the delivery the Job makes, by type, with one word, its current version; and whether each Task's result shows
  there too (s54's open question). If JL picks Q2 C, the pieces show only there.
- **s56 · Job UI: Studio** (`t02_job_page/s56-job-ui-studio/`): the sNN at the Job and its Tasks, their groups and
  tags, and their open points; that is why "open points wait on you" leaves the Work rows.
- **s52 · Block UI: Work** (`t01_block_page/s52-block-ui-work/`): the Job rows one level up, and what a Job row shows
  of its Tasks; its view name (Progress or Jobs) is its own call. Its form (`t01_block_page/runs/r03_collect_block_work_views/`)
  picks the same shapes one level up: an Interactions box first, every Task one line each under its Job, the sNN a
  Job makes on its row, a last section "Its own Runs". This cell uses the same names, so the two pages read alike.
- **s58 · Task UI: Work** (`t03_task_page/s58-task-ui-work/`): a Task's Runs in full (each card, its passes, Ask the
  agent); a Run line here opens that Run there.
- **s57 · Task UI: Report**: reading a Task's newest result in full.
- **b17-s04** (`s04-workbench-page-structure/`): the page parts every work page shares (path, title-&-section,
  view-button-list, goal-line, view-caption, both rails) and the right rail's sections: Interactions (the inbox),
  Delivery, Timeline, Files.
- **haipipe-interaction**: the forms themselves, `collect.py bundle` (Answer all) and the applied flags.
- **design_b02_workbench**, the code's owner: the change in `servers/workbench/focus_page.py`, never made here:
  1. `render()`: at a Job, Work's first view becomes `("tasks", "Tasks", ...)` in place of `("progress", "Progress",
     ...)`; add `"runs"` only on Q1 B; keep `"deliverables"` only on Q2 B; `VIEW_WORDS["tasks"]` holds the caption.
  2. `status_html(folder, root, "Job", ...)`: order the rows by the face's `## Tasks` (a helper reading the lines
     `new_job.py check` reads; `frame.children` sorts by folder name); the word from the Run cards (a new
     `task_word`, beside `state_kind`); the makes line (a new `pieces_made`, reading each `delivery/render.yaml`
     `by:`); the Run lines (a new `run_line` over `frame.runs_of`); drop `open_topics` from the Job's rows; keep
     `interaction_button` and `output_of`.
  3. The Interactions box: `interactions(<job>, root)` filtered to `waiting`, plus the sign and press-Run rows read
     from the cards, with the bundle link when two or more forms wait.
  4. The two "last" sections (Not in ## Tasks; Its own Runs) under the rows.


## (d) Compared with b16's matching cell and today's pages

**b16's s36 · Version UI: Work** (`b16_theme_paper/j01_paper_workbench_pages/t02_version_page/s36-version-ui-work/`;
its Decided s36-D01 and s36-D02; its live code `servers/workbench/workbench-task-draft/focus_draft.py`
`version_work_views` and `section_row`):

- **The same**: one row per Task, its name opening the Task's page; the row says where the Task stands in words that
  each open the thing they name (s36-D01: five step words; here, one line per Run with its verb); the page's forms
  show in Work.
- **Views differ**: b16 has Draft-Main · Draft-Appendix · Display-Main · Display-Appendix (more to come, such as
  Citations), one view per band of Task numbers (t00 to t19, t20 to t39, t41 to t49, t51 to t59). A work Job has no
  bands: its Tasks are one ordered list, `## Tasks`, read top to bottom as their dependency order, so one view, Tasks.
- **The row differs**: a paper Section has five fixed steps (Plan · Write · Evidence · Display · Revise); a work Task
  has no fixed steps but has Runs of three kinds, so its row shows its Runs (Q1 A) and one word (Q4 A). Q4 C offers a
  work Task's own five words (plan · build · run · read · close, haipipe-task `ref/lifecycle.md`) for the b16 look.
- **What waits differs**: b16 puts the version's own forms in an Interactions section after the Sections
  (`ix_waiting`, at the end of Draft-Main); b17 puts every waiting form first, in orange (JL 261031).
- **What the row hands over differs**: a paper Section is itself part of the paper; a work Task makes one piece of an
  sNN's delivery, named in that sNN's `delivery/render.yaml` `by:`, so the row names it (Q2 A).

**Today's pages** (read 2026-10-31):

- 5623, `b17_theme_work/j01_work_ladder_contract`, Work: view-button-list [Progress]; caption "Its parts."; three Task
  rows, each its name, its goal and the face's raw state "🔴 OPEN"; no Run, no piece, nothing waiting. The code's Job
  branch of `status_html` would also put the Job's own forms first and the newest figure in place.
- 5623, `b17_theme_work/j03_work_workbench_pages`, Work: the same rows plus "3 open topics waiting on you" and an
  Interaction button. That count is the running server's: the code on disk already says "open points wait on you",
  never a count, so the server has not been restarted since. The rows follow the folders' order (`frame.children`
  sorts by name), not the face's.
- 5599, a private work Job (its view and section names only): [Progress · Deliverables]; one row per Task with its
  name, goal line and state line; the Deliverables view draws the face's `## Deliverables`; no Run on any row; the
  right rail Report · Work · Interactions · Timeline · Files.

**What changes, and why**: the view is named for what it holds (Tasks); the rows follow the face's order; the word
comes from disk; each row shows its Runs and the piece it makes. These answer the three reasons s55's drawing gives
(Tasks sat as cards with many tabs; the order was the folders', not the plan's; a Run hid two clicks deep). What waits
sits first because JL asked for it there (261031).


## (e) The alternatives weighed, my pick and why

1. **The view list**: Tasks alone (my pick) · Tasks · Runs · Tasks · Deliverables (today, renamed) · Progress
   (today's name) · one view per `task-type:`, as the Report has one per delivery type. Pick: Tasks alone, since one
   place per Task reads fastest; most Jobs hold one task-type, and a split by type breaks the `## Tasks` order.
   Asked as Q1 and Q2.
2. **The view's name**: Tasks (my pick) or Progress. Tasks names what it holds, and the right rail already says "its
   Tasks". Decided here, not asked.
3. **Where Runs show** (s55's open question): in the row (my pick, Q1 A) · a Runs view (Q1 B) · only the Task's page
   (Q1 C) · folded under each Task (the cell's first drawing; out, by haipipe-ui rule 4, no fold arrows) · only the
   Run that waits (out: it hides the done Runs that hold the results).
4. **What a Task hands over**: on the row (my pick, Q2 A) · a Deliverables view (Q2 B) · only in the Report (Q2 C) ·
   on the row and in a view (out: it says the same thing twice).
5. **What waits**: one box first (my pick, Q3 A) · nothing extra (Q3 B, which is today on j03) · one line (Q3 C) ·
   only the right rail's Interactions (out: JL asked for it first, in Work).
6. **The Task's word**: from its Runs (my pick, Q4 A) · the face's `state:` (Q4 B) · five life words (Q4 C) · the
   Block's tally of kinds (out: a Task is one thing, so one word).
7. **The order**: the face's `## Tasks` (decided) over the folders' (today), since the haipipe-job contract makes the
   list the reading and dependency order.
8. **Open sNN on a row** ("open points wait on you"): dropped (decided). JL named what waits as a form or a sign;
   topics are Studio's (s56), and their own cards carry their Interaction.
9. **A picture on a row**, as the Block's Job rows carry: none (decided); the newest result's figure shows when there
   is one.
10. **The newest result in place**: kept (decided); cut to its headline if JL's s54 answer puts Task results in the
    Report.
11. **Ask the agent on the Job's Work**: no (decided). JL called it clutter outside a draft's Plan, Write and Revise
    (261031); the Task page (s58) keeps it.
12. **Add a Task** (haipipe-job's button, `run-add-tNN`): later, with the operations that write back (s04's Phase B);
    this page is read only.
13. **The Job's own soft Runs**: a last section (decided) over the Runs view or hiding them (today). They are the
    Job's own work (`run-face-jNN`, `run-delivery-<target>`), and no view shows them today.
14. **The Job's README "Run it" commands, `src/`, `sbatch/`**: Files, not Work (haipipe-ui rule 4: no instruction
    paragraphs on a page).

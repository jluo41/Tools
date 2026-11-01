# s58 · Task UI: Work · views proposal

for: b17.j03.t03-s58:theme_work.work_workbench_pages.task_page @ task_ui_work
written: 2026-10-31 18:54, by the agent drafting s58 (claude)
JL's choices: `../../runs/r02_collect_task_work_views/` (the form, my pick ticked; six questions)
previews: `../../scripts/build_r02_previews.py` writes them; never edit a preview by hand

A work Task's Work section, verb do: what the Task did and is doing, one row per Run, what waits for you first.
This file is the whole proposal under my picks; the form asks the six choices that are JL's. When an answer comes
back, the Run that applies it is `../../runs/run-design-task-page/` (the form's `feeds:`).

Terms, once:

1. **work Task**: a `tNN_<task>/` folder in a work Job; its face `tNN_<task>.md` holds `state:`, `goal:`, `close:` and `task-type:` (haipipe-task).
2. **Run**: one folder in the Task's `runs/`, one commission (haipipe-run). Its **card** is `run.yaml` (run, kind, type, role, scope, target, ticket, skill, agent, signs, status, passes, writes, feeds).
3. **hard Run**: `runs/rNN_<slug>/`, its **ticket** `rNN_<slug>.sh` (`.ps1` for Stata on Windows, `.cmd`), its `config.yaml`, its `result/` (the **receipt** `runtime.yaml`, `headline.txt`, `metrics.json`, figures, `heavy.yaml`).
4. **soft Run**: `runs/run-<type>-<target>/`, its ticket `run-<type>-<target>.md` (target, ask, close); agent work, no `result/`.
5. **collection Run**, or **form**: `runs/rNN_collect_<slug>/`, its `question_collection.md`, its form `rNN_collect_<slug>.html`, its answers `result/answer_collection.md` (haipipe-interaction).
6. **pass**: one execution or round of one Run, `passes/pNN-<MMDD>/` (a retry of a ticket, or one more round of agent work).
7. **role**: the card's `role:`, the one job a Run does in its Task, in haipipe-run's order: trial · make · fix · check · describe · figures · evidence · publish (JL 261020: each Run its own job).
8. **you**: the person reading the page, JL.


(a) The view list
-----------------

1. **Runs** · opens first · every Run in `runs/`: what waits for you first, then each Run under its role, then Ask the agent.
2. **Deliverables** · only when the Task's face has a `## Deliverables` section, as today; a work Task's face normally has none (the Job's face holds the list, haipipe-job), so a work Task shows Runs alone.

One button names the one view, so the goal-line never moves (haipipe-ui rule 2). The right-rail item stays "its Runs".
The view-caption: "Every Run in runs/, one row each; what waits for you first."


(b) Each view, section by section
---------------------------------

### Runs

Its sections, in this order. Each is a heading bar with its content below it, folding by its heading, open by
default, the reader's choice kept in the browser (haipipe-ui rule 4; b32 s42-D08, D09). A section with nothing in it
does not show, except Ask the agent.

#### 1. Waits for you

1. **Shows**: one row per thing only you can do, orange edge, the heading orange; the row moves here, it is not repeated below.
2. **A form to answer**: its name, its form's title as its line, "🙋 waits for you", and the 🙋 Interaction button (orange edge).
3. **A built ticket you press**: its name, its line, "🙋 ready: you press Run", then Copy command and Open.
4. **A sign**: a card with `signs:` and `status: waiting`, with Open; signing stays the owning skill's.
5. **Order**: by Run number, as the folder lists them.

Reads from disk:

- a form: `runs/rNN_collect_<slug>/run.yaml` `status: waiting` and no `result/answer_collection.md`; its title is the first `# ` line of `question_collection.md` (as `focus_page.interactions()` reads it today); the button is `interaction_button()`, which pops out `view=focus-part&part=interactions&path=<the Run folder>`.
- a built ticket: `runs/rNN_<slug>/run.yaml` with `status: planned` and `agent:` naming you, the file its `ticket:` names present in the Run folder, and no receipt saying `running` or `complete`. A planned Run whose `agent:` is claude or codex stays in Runs as "⬜ planned": the agent presses it.
- Copy command copies the one line that starts the ticket from the SPACE root: `bash <path>/rNN_<slug>.sh`; `pwsh -File <path>/rNN_<slug>.ps1` for a `.ps1`; a `.cmd` as it is. The line shows when you rest on the button.

Empty: the section does not show; Runs heads the view.
Tags and actions: no tags, no counts; at most three verbs a row (Copy command, Open; or 🙋 Interaction).

#### 2. Runs

1. **Shows**: every other Run, one row each, under its role's heading in haipipe-run's order: trial · make · fix · check · describe · figures · evidence · publish.
2. **Forms not waiting**: answered or not sent yet, last, under the heading forms, each with its Interaction button.
3. **Inside a heading**: by Run number, then the soft Runs, as `frame.runs_of()` sorts the folder.
4. **A row**: its name, one line of what it is for, its state word, its newest pass (`p02 · 10-29`).
5. **A done hard Run**: its picture small at the row's right; a click opens it large in the pop-out (haipipe-ui Rows rule 3).

Reads from disk:

- the Runs: `frame.runs_of(<task>)`, every folder in `runs/` but names starting `.` or `_` and `README.md`.
- the heading: the card's `role:` (written by haipipe-run `scripts/run_roles.py`); a card with none takes `run_roles.propose(<name>)`, as the classic page's `role_of()` does.
- the one line: a hard Run's `config.yaml` `_meta.purpose` ("why does this run exist?", haipipe-task `ref/config-meta-template.yaml`), else its card's `target:`; a soft Run's ticket `ask:` line; a form's `# ` title.
- the state word: a hard Run's receipt `result/runtime.yaml` `status:`, else its card's `status:` (the receipt wins when they disagree, haipipe-run `ref/receipts-and-inventory.md`); a soft Run's or a form's card `status:`, a form answered once `result/answer_collection.md` exists. The words are in the table below.
- the newest pass: the last `passes/pNN-<MMDD>/` folder, shown `pNN · MM-DD`; nothing when it has none.
- the picture: `result/figure.png`, else `result/preview.png` (as `output_of()` reads today).

Empty: "No Runs yet."
Tags and actions: Open (every Run: the Run pop-out, below), Result (a hard Run whose `result/` holds files: the pop-out at
its Result), Interaction (a form: its list, Answer or See answers). No Copy prompt on a row (JL 260927 removed those
chips), no type word (the name says it: `rNN_` hard, `run-` soft, `_collect_` a form), no agent or skill (in Open).

#### 3. Ask the agent

1. **Shows**: one notes box, "your notes, copied with the prompt", kept in this browser per Task.
2. **Copy prompt: plan** copies a prompt for `run-plan-<tNN>`: the face's goal and close, each Run to make as a planned card.
3. **Copy prompt: build** copies one for `run-build-<tNN>`: worker, config and tickets, then the code review (`run-review-code-<tNN>`, `CODE_REVIEW.md`).
4. **Copy prompt: check** copies one for `run-check-<tNN>`: the close line against every receipt and Result gate.
5. **Place**: the foot of the view, after every Run.

Reads from disk: the Task folder's name and its tag (`t01`), filled into the work theme's own Run names
(haipipe-run `ref/run-types-by-space.md`, "work": Plan a Task `run-plan-<tNN>` · Build the Task `run-build-<tNN>` ·
Check a Task `run-check-<tNN>`); each prompt shows when you rest on its button, as the draft page's do
(`focus_draft._run_rows`).
Empty: always shows; it is an action, not content.
Tags and actions: the three Copy prompt buttons (rule 5: at most three).

#### What Open shows: the Run pop-out

A Run opens over the page and closes back to the same place (haipipe-ui rule 4; b17-s32-D04), never as a page of its
own. Its sections, in order:

1. **Card**: `run.yaml` in words, one line per field it has: kind, type, role, status, agent, skill, target, writes, feeds.
2. **Ticket**: the file its card's `ticket:` names, read in place; a hard Run's start line with Copy command.
3. **Config**: `config.yaml` (`config.do` for Stata), its `_meta.purpose` first; none for a soft Run or a form.
4. **Result**: `result/`: the receipt's status, `started_at`, `finished_at`, `failure`; `headline.txt`; figures; `metrics.json`; small tables; `heavy.yaml` (each big file's path and size); a form's `result/answer_collection.md`.
5. **Passes**: one line per `passes/pNN-<MMDD>/`, newest first: its id, its date, its `pass.md` title or its files; each opens to read.

Empty: Result says "No result yet."; Passes says "No pass yet."
Opens with `view=focus-part&part=run&path=<the Run folder>`, a new part beside `map`, `work`, `delivery` and
`interactions` in `part_document()`.

#### State words

Every mark is a word (haipipe-ui rule 5), its emoji one of ⏳ ✅ ⬜ 🙋 ❗ (JL 261029: no 🔶).

```text
kind        on disk                                          the word
hard        status planned, ticket built, agent: you         🙋 ready: you press Run
hard        receipt or card planned                          ⬜ planned
hard, soft  running                                          ⏳ running
hard        receipt complete, or card done                   ✅ done
hard        receipt partial                                  partly done
hard, soft  failed (the receipt's failure: in Open)          ❗ failed
hard        receipt blocked                                  ❗ blocked
hard, soft  superseded                                       superseded
soft        card queued or planned                           ⬜ queued
soft        card waiting (a sign)                            🙋 waits for you
soft        card done                                        ✅ done
soft        card held                                        held
form        card planned, no form built                      ⬜ not sent yet
form        card waiting                                     🙋 waits for you
form        result/answer_collection.md exists               ✅ answered
```

### Deliverables

Unchanged from today, and only when the face has `## Deliverables`: "What it must hand over, ticked from the disk"
(`deliverables_html()`). Empty: the button does not show.


(c) What it leaves to the other cells
-------------------------------------

- s57 · Task UI: Report (check): the MindMap, the newest result shown large (its figures, headline, metrics), the close line, the face's reading. A row's picture and Result open the same files; Work never redraws Report's view.
- s59 · Task UI: Studio (think): the Task's own sNN topics, and the Studio's Ask the agent (Copy prompt: talk and sketch).
- s55 · Job UI: Work: this Task's row on its Job's page, its state and what waits, by the same Waits for you rule.
- s52 · Block UI: Work: the Jobs' rows.
- b17-s04 (what every work page shares): the path, the title-&-section, where the view-button-list sits, the goal-line (Aim for a Task), both rails, the Interactions section (the inbox), Delivery, Timeline (every pass and receipt by date), Files (the folder tree: `scripts/`, configs, `notebooks/`); and s04's open point 6, a Run's own row or a pop-out, which stays s04's.
- haipipe-interaction: the form, the Interaction button and its pop-out list (decided in b16 t01 r04 Q3 to Q6 and r07).
- haipipe-run: the card's fields, roles (`run_roles.py`), soft Run passes (`soft_run.py`), pruning.


(d) Compared with b16's matching cell and today's pages
-------------------------------------------------------

b16's s39 · Section UI: Work is the draft Task page (b32 s42, agreed): Work's views are its steps, 1 · Plan · 2 · Write
· 3 · Evidence · 4 · Display · 5 · Revise · Runs, each step's state a word on its button.

1. **Same**: what waits for you is first, its verb beside it.
2. **Same**: Ask the agent is one notes box and Copy prompt buttons (s42-D10 keeps it on three steps).
3. **Same**: a view holds sections, each a heading bar, folding by its heading, open by default (s42-D08, D09).
4. **Differs**: one view, Runs, not five steps; a work Task's work is its Runs.
5. **Differs**: a built ticket waits for you to press Run, with Copy command; a draft Task has no hard Run.

Why they differ: JL asked for the work theme, not the paper (r01 Q1). Most work Tasks have no plan or build Run of
their own (each b17 Task has one soft Run), so step buttons would stand mostly empty, and each Run's state word would
repeat on a step button. A draft step shows its text; a work Run shows its picture, small, on its row.

Today's pages:

1. **Tools `t01_block_page`** (5623, Work): one view, Progress, caption "Its parts.": five rows, r01 done, r02 to r04 planned, `run-design-block-page` queued.
2. **Its gaps**: no line says what a Run is for; a planned form looks like a done one; nothing says what waits; no Ask the agent; no pass.
3. **The private OpioidRx Task** (5599, structure only): Progress, three hard Runs, each "planned"; nothing says a ticket is built and waits for you.
4. **The classic page** (5623 without `layout=focus`): Work Details › Code · Review · Notebooks · Evidence · Value; Runs › All · collect · design · Page Runs.
5. **Its Runs panel**: Run-type buttons (`rNN_<slug>` Run a Task, `run-plan-t01`, `run-build-t01`, `run-review-code-t01`, `run-check-t01`), + New Run, a Prompt box with Copy.

Kept from today: one row per Run, its real name, a state word, the Interaction button, a done Run's figure. Changed:
the view is Runs (it was Progress, "Its parts."); Waits for you comes first; each row says what its Run is for, sits
under its role, and carries its newest pass; a built ticket gets Copy command; Ask the agent carries the classic
Prompt box over; Code, Review and Notebooks move to Files and the Run pop-out.


(e) The alternatives weighed
----------------------------

The six on the form, my pick first:

```text
Q   choice            A (my pick)                         B                              C
Q1  Work's views      Runs, one view                      Runs · Code                    Plan · Build · Run · Check
Q2  Runs or passes    a row per Run, newest pass a word   a row per pass                 a row per Run, pass buttons
Q3  one Run row       name, line, state, pass             also agent · skill             name and state, as today
Q4  what waits        forms, built tickets                forms only                     also failed Runs
Q5  its result        picture small at the right          full width under, as today     one headline line
Q6  Ask the agent     at the foot                         second, under Waits for you    nowhere in Work
```

1. **Q1 A**: one screen to do the work; code is in Files, results in Report.
2. **Q2 A**: you act on a Run; each pass is in Open and in Timeline.
3. **Q3 A**: enough to choose a row; who runs it and how are in Open.
4. **Q4 A**: only you press Run; fixing a failed Run starts with the agent.
5. **Q5 A**: each result shows where its Run is, and rows stay short.
6. **Q6 A**: the Runs come first; you ask for the next one after reading them.

If JL picks Q1 B, the Code view's sections are: the worker (`scripts/*.py`, `.do` or `.R`, each with its docstring's
first line), shared settings (`scripts/config/`: `_defaults.yaml`, `prompts/`), each Run's config
(`runs/<run>/config.yaml`), the Job's code a ticket calls (`WORKER_PATH`, the Job's `src/`), the review
(`CODE_REVIEW.md`: its verdict and date), notebooks (`notebooks/`); empty: "No code: this Task's Runs are agent work."

If JL picks Q1 C, each step is one view with its state word: Plan (goal, close, the Job's `## Deliverables` item it
feeds, the planned Runs, `workflow/plan.yaml` when there is one; `run-plan-<tNN>`), Build (the worker, the configs,
each Run's ticket present or missing, `CODE_REVIEW.md`; `run-build-<tNN>`, `run-review-code-<tNN>`), Run (Waits for
you, the hard Runs with their receipts and passes), Check (the close line against each receipt;
`run-check-<tNN>`); a bare link opens the step that waits; a step with nothing in it does not show.

Decided here, not asked (each follows a rule or a decision already made):

1. **Role headings**: haipipe-run's card contract says "role: groups a Task's Runs in the workbench, in that order" (JL 261020).
2. **Forms last**: forms not waiting sit under a last heading, forms; the role list has no word for asking.
3. **Pop-out**: a Run opens over the page (b17-s32-D04, haipipe-ui rule 4); s04's open point 6 stays s04's.
4. **No row prompts**: no Copy prompt on a Run row (JL 260927 removed those chips as clutter).
5. **No counts**: no count in a heading or a button (JL 261031: labels carry no counts).
6. **No close line**: the close line is a check, Report's (s57); the Aim already says what the Task delivers.
7. **Deliverables**: shown only when the face has the section, as today.
8. **Words**: ⏳ ✅ ⬜ 🙋 ❗ only (JL 261029).


The code change, for its owner
------------------------------

The owner is design_b02_workbench; the file is `servers/workbench/focus_page.py`, never edited from this Task.

1. `status_html()`, its Task branch: the three sections (Waits for you, Runs by role, Ask the agent) in place of today's flat rows; the view key `progress` is named Runs at Task level, with its caption in `VIEW_WORDS`.
2. `part_document()`: a new part, `run`, the Run pop-out (Card, Ticket, Config, Result, Passes).
3. A Run's one line: `config.yaml` `_meta.purpose`, a soft ticket's `ask:`, a form's title.
4. The ready rule: card `status: planned`, `agent:` the person, its ticket file present, no receipt running or complete.
5. Ask the agent: `focus_draft._run_rows()` reused (one notes box, Copy prompt buttons) with the work theme's Run names.


Found on the way
----------------

1. `run_roles.py` (owner haipipe-run): its check pattern is `audit|contract|compare`, so `run-check-tNN` and `run-review-code-tNN` get role make; adding `check` and `review` fixes it.
2. Today a Task row shows the card's `status:`, never the receipt's, though the contract says the receipt wins.
3. Today a planned form and a planned hard Run read the same word, "planned"; only the button tells them apart.

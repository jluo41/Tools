# Runs of a draft Task · names, the two ends, a new family

The focus page has no Runs view; a step's Runs show inside Display, and every Run stays reachable from the
Task's folder. These rules hold wherever a Run is shown: its name, how it opens and closes, and what a new Run
family must register. The panel itself is the classic route's.

## The Runs panel (classic route)

1. **Place**: a column on the right at every page width; `▸` folds it to a
   strip, `◂` opens it; the choice is remembered per Space in this browser.
   The folded strip turns green when a run awaits the person.
2. **Run types**: the `🔘 BUTTON` lines of
   `../../../draft/hai-draft-workflow/ref/run-cards.md`, as `label · Space · ticket
   pattern · views <names>`. A view or tab shows only the buttons that name it,
   each with its run count for the current target, then `+ New Run`.
3. **Target**: the selected paragraph or item narrows every list; nothing
   selected means the whole Page.
4. **Run card**: an id strip when there are two or more runs, the name, a state
   badge (Closed · Held · Awaiting you · Running), Rerun, the skill it uses
   (`Skill hai-draft-writing · hai-draft`: a `skills:` line in its ticket
   or runtime, else its card's `🧩 SKILL` line), a folded `▸ Prompt`
   with Copy, the running process, and the Results folder with its files.
5. **Starts nothing**: Rerun, `+ New Run` and Copy copy a prompt (the
   `💬 PROMPT` line with `{page} {plan} {target} {button} {run}` filled in).
   The person runs it in a Claude or Codex session, which records who started it.

The panel opens on a type with a run awaiting the person, else the view's
first type with runs. The Evidence Supporting Runs tab adds `Task runs` and
`Discovery runs`; a run no button claims shows under `Other`.

**Which runs, where, in what order, with which skill** is the studio drawing's
section "The runs of a Page": 1 Context, 2 Structure revise, 5 Evidence embed
(Draft › Table) · 3 Task and Discovery runs (Evidence › Supporting Runs) · 4 one
run per Evidence item (Citations · Displays · Values) · 6 Auto write (Draft ›
Reading) · 7 Section revise, 8 Paragraph revise (Draft › Revise) · adopt (code) ·
9 Build (Delivery) · 10 Check (Delivery › Checks); Scratch and Revise edits any
time. Every card in `run-cards.md` carries the same Space, view and skill.

**Run names** (`src/run_names.py`): `run-<kind>-<slug>`, the
name on disk and on screen alike (`run-section-0927-readability-cleanup`,
`run-paragraph-0928-c1-p2`, `run-value-0928-score-validation`); a taken name gets
`-2`. The three Delivery runs have one fixed name each, `run-delivery-webpage`,
`-latex`, `-word`, rebuilt in place. An older name (`rp-sec-07`, `re-value-07_x`,
`pj06t11r01_x`) still reads and is shown by `display_name` / `_name_by_item` until
`page.py run-names <page>` renames the Page once (flat `runs/`, `results/`, every
mention inside the Page; then `page.py export`).

**Records at the two ends**: `page.py open-run <page>
--kind <kind> --slug <words> [--target C1.P2] [--goal …]` writes the one ticket
(`status: open`); while open only the Page's text changes and the panel shows the
run as Running with no result; `page.py close-run <page> <run>` writes
`results/<name>/`, marks the ticket closed and adds one log line. The workbench's
own writers follow it: the first Revise Save on a paragraph opens
`run-revise-<c1-p2>` (its ticket keeps the text before), and Finish Scratch
is the close of a Scratch run.

**To add a run type** for runs that already exist (a known ticket prefix), edit
`run-cards.md` only; the page rereads it on every load:

1. **Own prompt, own card**: every button in a card shares that card's first
   `💬 PROMPT` (`runs_panel.py::run_types`); a button that needs its own prompt
   gets its own `## \`…\`` card.
2. **Patterns never overlap**: a run joins the FIRST button, in card order, whose
   pattern matches its ticket name, so `re-value-check-` would fall under `^re-value-`.
3. **No runs yet**: a button with no runs shows `No runs yet.`; its prompt is
   copied from `+ New Run`, where `{run}` is not filled, so a new-run prompt never uses it.
4. **Selection**: a selected paragraph or row finds a run through the run's
   `target:` (a Bullet `C1.P2.B3` also counts for `C1.P2`) and its Evidence item
   (an `item: E<NN>-…` line near the top of its `.md` ticket), never its name
   (`runs_panel.py::_targets`).

**A new ticket prefix is a new Run family.** Prefer a Step inside an existing
Run when the work belongs to it. A new family needs all of:

1. **Owner skill or ref page** under `../../../draft/` (run-cards.md leaves Run authority
   to it) and its card in `run-cards.md`.
2. **`../../../../../servers/workbench/workbench-task-draft/run_views/runs.py`**: `_TICKET_NAME` (else the run
   never appears); for a Page writing run also `_valid_page_run_id` (else it shows
   Held) and the label helpers `_page_run_label`, `_page_writing_subspace`,
   `_run_name`, `_run_action`.
3. **`runs_panel.py::_DISPLAY`**: its full-word name (`run-…-NN`); a family
   already named in full words (`run-delivery-latex`) needs none.
4. **`../../../draft/hai-draft/src/run_folders.py::_KINDS`**: its `runs/<space>-run/` folder.
5. **Docs**: `../../../draft/hai-draft/ref/page-run-families.md`, `../../../draft/hai-draft-workflow/`
   (SKILL.md, `ref/interactive-writing-run.md`), `../../../project/hai-run/ref/run-catalog.md`,
   and a case in `servers/workbench/workbench-task-draft/reader/tests/test_runs_panel.py`.

Cross-check by mirroring the newest family: `grep -rnE "rp-revise|_REVISE_RUN|revise\)"`
over `servers/workbench/workbench-task-draft`, `skills/page` and `skills/run` lists every place it is registered.

A new tab or view needs `space_views.py`.

The All-runs view (`lens=run`, reached by a `?run=` link, no button) is the
older full Run presenter: `ref/run-space.md`.

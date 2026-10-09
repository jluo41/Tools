Labeling Workbench · shared workbench rules
===========================================

How the Labeling Workbench was brought up to the rules every workbench shares
(`haipipe-toolkit/servers/README.md` § "Adding a workbench", rules 1-6), the same way
the Paper and Page workbenches were. This file is the progress log and the record of
the choices made on the way.


Progress
--------

| step | rule | what | state |
|---|---|---|---|
| 1 | 1 · same shell | title, an `all labeling jobs` link (no `all boards · board index`), a band (phase · round · guideline · HOLD), plain Space names, View tabs and content in one box, Insight's tokens and tab sizes | done |
| 2 | 6 · Runs on the right | the shared Runs panel (`live.runs_panel.panel_markup`), folded at first; `labeling` off `RUNS_GAPS` | done |
| 3 | 3 · no window heights | the map, conversation and prompt boxes sized in px | done |
| 4a | 2 · Guide | `description`, Method steps and Space lines in the `labeling` entry | done |
| 4b | 2 · Guide | Workbench Table generated from `ref-space-mapping.md` (`ref/make_workbench_table.py`); `--check` passes | done |
| 4c | 2 · Guide | "Workbench design" drawing from `studio/labeling-workbench-ui.py`; the old run-table drawing retired | done |
| 4d | 2 · Guide | `ref/labeling-papers.md`, checked by table-papers (`--online`); now `servers/workbench-labeling/related/papers.md` (261007) | done |
| 5 | 4 · short address | `/w/<board>` and `/w/<board>/<page>/labeling` redirect; the skill and ref give that form | done |
| 6 | docs | `labeling.py` docstring, SKILL.md 0.24.0 + CHANGELOG, `servers/README.md`, `ref-space-mapping.md` | done |


Decisions
---------

1. **One link under the title: `all labeling jobs`.** The old `←` before the title
   becomes that link. The shared `all boards · board index` line is left out (asked on
   2026-10-03: not needed); a Page opened without a Board, and the Board level itself,
   have no link line.
2. **The band states where the job stands, never what an item says.** Phase, the open
   round and how many of its items are labeled, the current guideline version, and HOLD.
   The next step stays the title's tooltip, as before.
3. **No box inside a box.** Inside a Space's box a `.card` loses its border and becomes a
   section with a rule above it, as the Paper Spine cards did. A round stays a folding
   box, the way Insight keeps its folding rows.
4. **Labeling keeps its own Run cards inside the shared panel.** `panel_markup` gained an
   optional `card=` (default unchanged for Paper, Page, Task and Design), so a Labeling card
   still decides Resume or Rerun from HOLD, G0 and the round's state, and a review-only Run
   shows its Record instead of a prompt. The shared script reads only the card's
   `data-type`, `data-targets` and `data-views` hooks.
5. **A gated run type offers no "+ New Run".** The shared script hides "+ New Run" when the
   view has no run type or the chosen type's prompt is empty. Labeling leaves a prompt empty
   while a step is not next, a gate is not passed, or the job is on HOLD; every other family
   always fills its prompts, so nothing changes for them.
6. **Run types keep their id.** A kind may carry `op`, shown as `data-op` on its button, so
   the Labeling tests and the round ↔ Run link keep finding a type by its id.
7. **A human Run waiting on the person counts as waiting.** A `running` Run whose worker is
   the human enters the shared panel as `waiting`, so the panel opens on it, as the old one did.
8. **Rounds and Runs still find each other.** Opening a round picks its Run in the panel, and
   picking a Run opens its round, through a small adapter over the shared panel's buttons.
9. **The map stops at 1000 px wide.** Its old `calc(72vh …)` width followed the window
   height; at 1000 px the 1000 × 600 map is about 600 px tall. The conversation box stops at
   420 px. The panel's own `100vh` cap is shared CSS (`SPLIT_CSS`) and this page is never
   shown inside Guide, so it stays.
10. **The board-level page wears the shell too.** `/w/<board>` lands on it: the title, a
    band (jobs, waiting, the next step), then Guide and one Space, Jobs, in one box. It lists jobs and starts no Run, so it has no Runs panel.
11. **Engine tests load the shared host.** `engine/test_preparation_workbench.py` puts the
    shared host on `sys.path` when it is checked out beside, since the page now mounts the
    shared Guide and Runs panel; before this, four of its tests failed on `No module named 'live'`.

12. **Agents and sign-offs live in `ref-space-mapping.md`.** A new `## Run Type agents`
    table sits beside `## Run Type skills`; the Workbench Table is generated from that one
    file, so it cannot drift from the Run types the page shows. There is no run-cards file
    for Labeling, so `--cards` does not apply: the table agrees with the map by construction.
13. **A row's Skill is the View's own.** Each Run type declares four Skills; the row names
    the last, the one for its View, since a `-workflow` skill routes and is never a row's Skill.
14. **Checks are done by agents that make nothing.** `unit-check` and `scan-preflight` go to
    one planned checker (`labeling-checker-agent (new)`), and `risk-route` to
    `classifier-agent`, which scores uncertainty and does nothing else on this page.
    `corpus-preparer-agent (new)` and `haipipe-studio-agent (new)` are planned too.
15. **`human-review` is the person labeling.** Its words become `You label one production
    risk queue`, next to `You label one round`; the old `Review ...` read as an agent judging
    another's output.
16. **The old run-table drawing is retired.** `labeling-workbench-run-table.md/.py` and
    `labeling-workbench-design.excalidraw` restated the Run types by hand, had no review tick
    set, and held real item text; the generated Workbench Table and
    `labeling-workbench-ui.excalidraw` replace them as the one source.


Tests outside this change
-------------------------

On 2026-10-03 the wider sweep (`haipipe-board/tests`, `haipipe-page/tests`) had 17 failures
that this change did not cause and does not touch: Insight and Design workbench tests and the
folder-contract checks (other sessions' work in progress on the Insight skills), and five
standalone Page-server tests, one of which renders `engine/page_plugin.py` (a separate
Labeling page) and expects a `Workflow Space` it no longer has.

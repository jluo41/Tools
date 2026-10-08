s21 · Run and skill
===================

**Topic:** every design Run and the skills behind them, and the plan to make the skills carry the new ladder
(JL 261007: "s21 should be s21-run-skill. It should include both runs and skills"; then "the current skill is not
that powerful enough … make a plan to update the skills"; "a before after plan of the skill folders and what to
change and why"). Drawn in b16's `s21-paper-run-skill` shape (JL 261007: "this one is much better, follow it"):
lines-only tables, black, red for what is open, green for what changed (the studio's three colours, 261007).

**Source:** read from disk on every build:

- the Runs each Space shows in s11 · s12 · s13 (their builders' `SCREENS` and `BANDS`, imported, never run)
- the run cards: `haipipe-design-workflow/references/run-cards.md`
- the live design workbench (`servers/workbench-design/design_theme.py`)
- the skills in `skills/2_theme/design/` (version, size, callers, how often each still writes an old name)
- the base skills a design borrows, found by name
- the Runs in the Project design folders (`examples-*/*/designs/`), counted by run type and layout; names only,
  never content, and no Board or design is named

Typed, since they are the proposal: one name per Run, each Run's owner after the plan, each skill's job and its
change on the ladder, the folder moves, and the plan.

**Feeds:** `../../reports/q01_design_ladder/` (the Runs per level) and `../../reports/q02_design_workbench/`
(the Runs panel); a proposed Q04, "Which skill owns each part of the design ladder?".


Files
-----

```text
s21-run-skill/
├── s21-run-skill.md            this notes file
├── build_s21_run_skill.py      the builder
├── s21-run-skill.excalidraw    the drawing; marks are kept on rebuild
├── s21-run-skill.png           preview
└── history/                    the first cut of the builder (Runs typed by hand)
```

Rebuild: `python build_s21_run_skill.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s21-run-skill.excalidraw s21-run-skill.png 0.4`.


What the drawing holds
----------------------

```text
Runs by level        every Run the screens of s11 · s12 · s13 show, Block · Job · Task: Run · as drawn · kind ·
                     shows in · today · today's button · who does it · who checks · skill · on disk; then the
                     old cards no new Run takes over
one Job, in order    set up the Block → launch a Job → set up ×3 → t00 reason → tNN generate · verify → t99 rank →
                     release → the Exp scored, and back to a new method version; the skill under each step
the skills           the 6 design skills and the 2 proposed (owns · Runs that use it · old names · on the new
                     ladder), the borrowed base skills, and what sits in 2_theme/design but is no skill
skill folders        before → after: today's tree (read from disk) beside the proposed one, then one row per
                     changed file: before · after · change · what · why · plan phase
skill x Run          which skill each Run loads after the plan; x ? = a skill that does not exist yet
Runs on disk         Runs in the Project design boards by type and layout; the name forms
skill update plan    six phases: each skill, what it learns, the Runs it gains, done when
```

Every Run is named `run-<type>-<target>` (JL 261007: "unify the name to be run-xxx-xxx"): hard or soft is its
`kind:` and whether it has `result/`; a repeat names what it reads (`run-verify-d<NN>-v<k>`), never a counter.
"as drawn" shows a level drawing's own spelling where it still differs (s12 · s13 write `rNN_<type>_<target>`).

"today" says where a Run stands: **card** (a run card names a button for it, though it is the old Space's),
**screen** (the live workbench has the button, no card), **drawn** (only in the drawing).


Finding (261007)
----------------

Of 22 Runs, 8 have an old card, 1 is on the live screen and 13 are drawn only (Block 3 · 1 · 6, Job 3 · 0 · 4,
Task 2 · 0 · 3). Even a carded Run's card is an old Space's button (Commission's Generate and Verify, Add design
tasks), so no level of the new ladder runs on its own cards yet. The skills still write old names often:
workbench-design 125 times, haipipe-design 78, haipipe-design-workflow 74, haipipe-design-unit 28. On disk, the
2 design boards hold only old-layout Runs (commission · generate · verify); none uses the ladder yet.


Skill folders, before → after (proposed 261007)
-----------------------------------------------

Shaped like b16's paper plan: one ladder contract in `ref/`, one scaffold script for every level.

```text
haipipe-design/ref/design-ladder.md      rewrite      the three levels as s11 – s13 draw them
haipipe-design/scripts/design_ladder.py  edit         jNN_<goal>_<design-method>/ · inputs/ · t00 · tNN · t99
haipipe-design-brief/                    retire       the Block's goal list replaced it (s11)
haipipe-design-unit/references/modes.md  retire       a method version says how ③ works
old refs (method-folders, space-mapping …) → legacy/  read only until the old boards carry over
rename_runs.py                           → haipipe-design/scripts/carry_over/
new: haipipe-design-method/ ?  haipipe-design-delivery/ ?  reviewer agent · inputs.md · make_inputs.py ·
     reason.md · rank.md · score_exp.py · carry_over.py · tests/test_design_ladder.py
```

The drawing's table gives every row its what and its why; 6 files stay as they are.


Skill update plan (proposed 261007)
-----------------------------------

1. **Contract** (haipipe-design): design-ladder.md as s11 – s13 draw it; scaffold Block · Job · t00 · tNN · t99,
   every Run `run-<type>-<target>`. Gains run-add-job, run-open-designs, run-close.
2. **Inputs and methods** (haipipe-design-goal, haipipe-design-method): the goal list with the Brief merged in,
   rules, inputs versions, a Job's `inputs/` + `manifest.yaml`; the 13 cards moved in from the Guide, versions
   with ① – ⑤ and T0 – T3, the scorecard.
3. **Worker** (haipipe-design-unit, agents): reason ② and rank ⑤ beside generate and verify; the Ticket pins
   method + inputs; a reviewer agent verifies and ranks.
4. **Runs and release** (haipipe-design-workflow, haipipe-design-delivery): run cards by level × six Spaces;
   routes; a design's state; the release, frozen predictions, `designs.json`.
5. **Screens** (workbench-design): the six Spaces × three levels, run types read from the cards; the old page
   stays for old boards.
6. **Old words out** (all): carry the old boards over, the Brief retires, old refs into `legacy/`, versions.


Applied (261007)
----------------

JL 261007: "go ahead and then apply them to update the skills". Phases 1 – 4 are in the skills; the drawing's "done"
column checks each file against disk, and frame 1 now reads the ladder run cards (21 of 22 Runs carded; the 22nd,
run-plan-test, stays outside the theme).

1. **Contract** (haipipe-design): door rewritten; `ref/design-ladder.md` as s11 – s13 draw it; `design_ladder.py`
   writes `jNN_g<NN>_m<NN>/`, `t00` · `tNN_d<NN>_<slug>` · `t99` and `run-<type>-<target>/` with `kind:`; the older
   Design Folder contract in `ref/legacy/`.
2. **Inputs and methods**: haipipe-design-goal rewritten (`make_inputs.py`: freeze iN, build a Job's fence from the
   method's `sees:`); new haipipe-design-method (M01 – M05, versions, `pin_method.py`, `score_exp.py`); the Brief kept
   as legacy for older boards.
3. **Worker**: haipipe-design-unit as one method step (reason · generate · verify · rank), `check_unit.py
   --ladder-result`; a new haipipe-design-reviewer-agent.
4. **Runs and release**: haipipe-design-workflow rewritten, 30 ladder cards (the older board's 13 kept below them,
   still parsed by the old page), `project_predictions.py`; new haipipe-design-delivery (`release.py`).

Checked: 95 tests pass (4 browser renders skipped); one Job runs end to end through every script and the
workbench's reader reads it; the release refuses a ranked Job whose ranking was not projected.

Not done: phase 5 (design_views.py reading its buttons from the cards, the Guide and design_reader.py reading the
method registry; another session owns those files) and phase 6 (the carry-over of the older boards; the version).
design_reader.py now reads `kind:` from a Run's run.yaml (one line), so a hard `run-<type>-<target>` reads as hard.


Reviewed and fixed (261007, second round)
-----------------------------------------

JL 261007: "go ahead and continue, could you review them again?". Two fresh-context reviews: a cold read of every
design skill (26 must-fix, 14 nice-to-have) and a hands-on run of the skills on a placeholder Job. Fixed:

1. **Projection has an owner**: `haipipe-design-workflow/scripts/project_draft.py` (draft → the face's ## Design and
   elements.yaml; verdict → state passed | revise). Hard Runs write only result/; the workflow writes the Task.
2. **Verify names the draft it read** (`-v<k>`, k = 1 + revise passes), never a counter; a verify of an older draft
   is refused.
3. **Gates in the scripts**: run-add-job needs a signed goal, signed shared rules, a registered method version and the
   inputs version; N is the goal's; the fence is not built before the method is pinned; a run type must fit its
   folder.
4. **The fence (T1) is strict**: a `from` names a fence file (or `rule r2.1`, `W-03 row 2`) or is exactly
   `own knowledge`; a step may cite its own source; ideas carry a `name`; a verify needs a `by:`.
5. **Release** refuses the scaffold's unfilled words and a ranked Job whose ranking was not projected, checks every
   design before writing anything, and puts screens where both delivery folders can find them.
6. **One answer per contradiction**: T2 when the method lists it, T3 in t99's rank; `arms.csv` column `observed`;
   run-report is haipipe-report's; a person signs the goal, the rules, the freeze with the release, and the close;
   the fence check is a reviewer-written pass of run-open-designs; run.yaml carries haipipe-run's card fields.
7. **Server and drawings**: the workbench reads the method registry and the run cards (phase 5); s11 · s12 · s13 use
   the unified Run names; the Workbench Table is generated from the ladder cards (`workbench-design/scripts/
   cards_table.py`); the venue packs speak the ladder's words.

Checked: every design test suite passes, the server's design tests pass, and one Job runs end to end through every
gate (each refusal fires in turn; a failed draft is revised, verified as v2, released with its revised words).

Left on purpose: haipipe-project's audit does not check `designs/` (its own choice: "design keeps its family
layout"); the older board pages and legacy refs keep the older words.


Open
----

1. Decided 261007: the method registry is `haipipe-design-method/methods/`; s12's note and design_reader.py's comment
   still say `haipipe-design-unit/methods/`.
2. The design family is pinned at 0.4.0 and only a person may change it: 0.5.0 for this rewrite?
3. s12 and s13 still spell the hard Runs `rNN_<type>_<target>`: rename them in their builders.
4. Plan the test (`run-plan-test-<app>`): a design Run, or outside the theme with the Exp?

(write here, or mark the drawing in red)

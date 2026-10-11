s21 · paper Run and skill
=========================

**Topic:** every paper Run type and the skills behind them, and the plan to make the skills carry the new
ladder (JL 261007: "focus on show what are the skills and runs we have in the paper set"; then "the current
skill is not that powerful enough … make a plan to update the skills"). Drawn in b12's `s21-run-skill` style:
lines-only tables in the studio palette: black, red for what is open, green for what changed. Named `s21-paper-run-skill`, not `s21-run-skill`, because
b12 has a drawing of that name.

**Source:** read from disk on every build:

- the run types each Space shows in s11 · s12 · s13 (their builders' `SCREENS` and `ROWS`, imported, never run)
- the run cards: `haipipe-paper-workflow/ref/run-cards.md` and the Page's `haipipe-page-workflow/ref/run-cards.md`
- the live paper workbench (`servers/workbench-paper/paper_theme.py`) and the base frame (`servers/workbench/`)
- the skills in `skills/2_theme/paper/` (version, size, callers, how often each still writes an old name)
- the base skills a paper borrows, found by name
- the Runs in the Project paper folders (`examples-*/*/paper*/Paper-*`), counted by run type and shelf; names
  only, never content, and no Board or Section name is drawn

Typed, since they are the proposal: each skill's job and its change on the ladder, the owner and folder of a run
type with no card yet, and the plan.

**Feeds:** `../../reports/q05_skills_and_runs/` (Q05, "Which skills and Runs make the paper theme?") and
`../../reports/q01_paper_ladder/` (run types per level). The plan is run by `../../goals/g04-paper-skills.md`.


Files
-----

```text
s21-paper-run-skill/
├── s21-paper-run-skill.md            this notes file
├── build_s21_paper_run_skill.py      the builder
├── s21-paper-run-skill.excalidraw    the drawing; marks are kept on rebuild
├── s21-paper-run-skill.png           preview
├── haipipe-paper-comments-draft.md   the comments skill's draft (was s22)
└── history/                          the first cut of the builder (run types from run-cards.md only)
```

Rebuild: `python build_s21_paper_run_skill.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s21-paper-run-skill.excalidraw s21-paper-run-skill.png`.


What the drawing holds
----------------------

```text
Runs by level          every Run the buttons of s11 · s12 · s13 make, Block · Job · Task: Run · button ·
                       Space › view · today · who does it · who checks · skill · on disk; then the cards no screen shows
one version, in order  set up the Board → Story → open a version → write the Sections → release → build · check
                       → send → comments, and back to a new version; the skill under each step
the skills             the 9 paper skills (owns · Runs that use it · old names · on the new ladder), the borrowed
                       base skills, and what sits in 2_theme/paper but is no skill
skill folders          before → after: today's tree (read from disk) beside the proposed one, then one row per
                       changed file: before · after · change · what · why · plan phase
skill x Run            which skill each run type loads; x ? = proposed, no card yet
Runs on disk           Runs in the Project paper folders by type and shelf; the Run names
skill update plan      six phases: each skill, what it learns, the run types it gains, done when
```

Every Run is named `run-<type>-<target>` (JL 261007: "unify the run to be run-xxx-xxx"): a card's own ticket
pattern where it has one, else the name in the builder's `RUN_NAME`; the button that makes it stands beside it, and
two buttons that make one Run share a row. The only other form is a supporting Run of another theme, whose hard
`rNN_` keeps its own name (run-naming.md: never renamed for the paper).

"today" says where a run type stands: **card** (a run card names its skill, agent and sign), **base** (the shared
frame runs it), **screen** (the paper workbench shows the button, but no card says who runs it), **drawn** (only
in the drawing).


Finding (261007, before g04; after it, every Job and Task button has its card and the Block lacks only s11's two
"?" buttons; Q05 § 4)
------------------------------------------------------------------------------------------------------------

Counted as Runs (two buttons for one Run count once). The Task runs: all 19 of its Runs are the Page workflow's
cards or the frame's. The Block and the Job are where the paper skills fall short: of the Block's 23 Runs 11 have
no card (4 on screen, 7 drawn only), and of the Job's 21, 10 (4 on screen, 6 drawn only). Seven old cards (Idea
review, Select idea, Claim review, Redraw, Evidence runs, Delivery runs, Page check) sit on no designed screen:
place each or retire it. Two skills, haipipe-paper-story and haipipe-paper-ideation, still write the Pages that Q04 retired.


Skill folders, before → after (proposed 261007)
-----------------------------------------------

Shaped like the design theme's skill: one ladder contract in `ref/` and one scaffold script for every level.

```text
haipipe-paper/ref/paper-structure.md     → ref/paper-ladder.md          one contract, named like design-ladder.md
haipipe-paper/scripts/version_paper.py   → scripts/paper_ladder.py      board · version · task · run, not versions only
haipipe-paper/scripts/{migrate,rename_tasks,topics}_paper.py → scripts/carry_over/   one-time moves, retire later
workbench-paper/ref/space-mapping.md     → retired                      it maps the four old Spaces
haipipe-paper-venue/template.md          → ref/call-template.md         templates sit in ref/
new: comments scripts/review_items.py · story ref/narrative.md · section ref/requirement.md · tests/test_paper_ladder.py
rewritten: the SKILL.md of -paper, -workflow, workbench-paper, -story, -ideation, -venue, -section; run-cards.md
open: venue/ out of skills/ ? · assemble profiles/ into venues/<venue>/kit/ ? (Q02)
```

The drawing's table gives every row its what and its why; 16 files stay as they are.


Skill update plan (proposed 261007)
-----------------------------------

The contract and the cards come first, so each later skill has a folder to write and a card to answer; the Task
comes last, being mostly the Page's.

1. **Contract** (haipipe-paper): one folder law for B J T R; scaffold new board · version · task · run with
   runs/README.md. Gains Update the Board, Open a version, Update the version, Add a resource, Board status.
2. **Cards** (haipipe-paper-workflow, workbench-paper): run-cards.md re-cut by level × the six Spaces, one card per
   run type, gates G0-G5 at their level; the workbench reads its run types from the cards; the old page retires.
3. **Block** (haipipe-paper-story, -ideation, -venue): the Story as `studio/sNN-story-<telling>/` with RQs as Board
   Questions and reports, Narrative N1-N4 and Review for an audience; the Ideation as `studio/s01-ideation/`;
   venues as `venues/<venue>/` (Q02).
4. **Job** (haipipe-paper-comments, -assemble, -workflow): Add a review, Route an item, Reply to an item over
   `## Review Items`; build, check and Send from the version folder, the cover letter from `t31_`; the version
   face's `## Narrative` and J1-J5; Release a Section (G3).
5. **Task** (haipipe-paper-section): `t0N_` · `t2N_` · `t3N_`, the reader contract, Requirement with the rubric,
   a Section's own studio/ and reports/; Add a Section.
6. **Old words out** (all nine): no Story Page, `B[abc]-`, `RD<NN>`, `S-<desk>`, `-<MMDD>-`; versions and CHANGELOGs.


haipipe-paper-comments (261007)
-------------------------------

`haipipe-paper-round` is gone: it is `haipipe-paper-comments` (JL 261007: "we do not need to keep the round
anymore"). Designed here first (moved from s22), in `haipipe-paper-comments-draft.md`. A batch is a report of type
comments, `reports/qNN_<kind>-<MMDD>/` in the version that answers it (1.1.0); its points keep ids by source (R1.1 ·
E1.2 · A1.1 · M2.3 · V1.1); Review Items (`Review-<slug>`) are what gets routed and answered.


Open
----

- `venue/` is its own git repo inside the skills tree the installer scans; `.gitmodules` names it, but
  Tools does not register it. Mount it outside `skills/`, and register it?
- `haipipe-paper-venue` (a Venue Page) and b03's `venues/<venue>/` (call.md, kit/): one home (Q02).
- An older paper-edit family is installed at user level from clones outside this SPACE: retire it, or
  bring it into `2_theme/paper/`?
- Hard `rNN_` Runs sit on Story Pages, and compile is a hard ticket in `delivery/runs/`; Q01 proposes a
  paper holds soft Runs only.
- The four judgment run types (`run-paper-*`) have cards but no Run on disk yet.

(write here, or mark the drawing in red)

# b15 · Theme: labeling

board-kind: task-block
package: plugins/haipipe-toolkit
theme: labeling
ui-block: http://100.121.165.84:5599/_board/workbench?layout=focus&path=examples-6-labeling/Project-Labeling-SocialMediaWithLabels/labeling/b01_dices350
ui-job: http://100.121.165.84:5599/_board/workbench?layout=focus&path=examples-6-labeling/Project-Labeling-SocialMediaWithLabels/labeling/b01_dices350/j01_dices350_response_safety
ui-task: http://100.121.165.84:5599/_board/workbench?layout=focus&path=examples-6-labeling/Project-Labeling-SocialMediaWithLabels/labeling/b01_dices350/j01_dices350_response_safety/t01_dices350_items
shared-blueprint: b01_haipipe-toolkit
spine: Design questions about the labeling Theme as one ladder: what a labeling Block, a dataset × label Job, a step Task and an operation Run each hold and show, how the Building and Scanning sides and their human gates map onto the six Spaces, and where the schema and the frozen handoff live.
close: Each recorded question has a report Page with an answer status, and every answered question names the skill, workbench or builder change that settled it.
session: Ladder-b15-Labeling-v1031

## Topic

The labeling Theme teaches and freezes what one identified person means by a vague label
(Building: contract, definition, calibration rounds, guideline, the signed Label Handoff), then
qualifies executors on a sealed test, scans the corpus and audits the labels (Scanning). Its
Block holds one Job per dataset × label (`jNN_<dataset>_<label>/`, its `schema.yaml`); its Tasks
come in six types, named by each face's `task-type:` line: 📦 items · 📏 ground truth · 🧭 meaning ·
🛠 expression · 🔍 scanning · 📊 score (s13, JL 261014; building split into the two loops, meaning and
expression, JL 261101); its Runs are one per operation.

Today the labeling theme sits on the shared frame (`servers/workbench-labeling/labeling_theme.py`):
Job › Work shows each Task's type and state and a dashed card for each type still to make; the items
Task's Report opens on Itemization · Embedding; a building or scanning Task links each step to the
engine's own Labeling workbench (`labeling.py`: Data · Labeling · Quality · Delivery), still the one
place a person labels. The skills came from the subjective-label plugin (b04 q03).

The shared ladder (b10) gives every level one frame: Guide · Studio | Block · Job · Task | Delivery on
top, Description | Report | Work | Runs at each level. This Block asks how labeling fits that ladder
level by level, and what it needs that no other Theme has.

Most answers here are a change to the labeling skills (`2_theme/labeling/haipipe-labeling` and its view skills, `haipipe-labeling-building`, `haipipe-labeling-scanning`), the Labeling workbench
server, or b10's shared builder, not a Task Run. A Question may have no work entries; its report
links the changed files and the drawings.

Excluded: the ladder itself and what every Theme shares (b10_project_workbench); moving the plugin's files
(b04_skill_folder).

## Pipeline

```text
chat section -> Related question -> haipipe-report -> skill, workbench or builder change -> report Page
                                                     -> studio/ drawings (shared by the questions)
```

## Pages

`j01_labeling_workbench_pages/` (261031) designs the labeling pages as a 3 × 3, copied from the paper theme's
(b16 j01): Block, Job and Task × Report, Work and Studio, one sNN each (s51 to s59), every view drawn as the same
full screen, lettered, settled one letter per round. All nine are drawn by its `labeling_ui_cells.py`. The Task
page letters the six Task types (A items to F score; 🧭 meaning and 🛠 expression are the two loops) and numbers each type's steps. The earlier sketches s04
(job-centered content) and s05 (old layout refinement) now sit in s54 and s58.

```text
                 Report · check    Work · do    Studio · think
t01 Block        s51               s52          s53
t02 Job          s54               s55          s56
t03 Task         s57               s58          s59
```

The shared drawing is `s01-labeling-ladder/s01-labeling-ladder.excalidraw`:
every labeling row, Block to Run, proposed and today. It is drawn from b10's shared definitions
(`b10_project_workbench/s01-overall-tree-structure/`) by `b10_project_workbench/studio/_build/theme_ladder.py`
and rebuilt by b10's `studio/_build/make.sh`.

`s13-labeling-task/` is a labeling Job's six Task types (261014; six since 261101), as b12's s13 is a design
Job's three: the slides' steps mapped on the types, the two loops and the round report between them, and the first
drawing (the dices350 Job and its items Task on screen).

`s02-labeling-workbench/` is the Labeling workbench as built today (moved from the
server, 261007): the "before" the s01 proposal replaces, shown in its Guide › RoadMap Draw.

## Implementation plan

[Studio s03 implementation plan](s03-agent-role/implementation-plan/PLAN.md) specifies the proposed two-loop system, Workbench decision reports, data custody, executor evaluation and scale-up. It contains 21 work packages, explicit agent ownership and coordinator acceptance gates. Three specialists reviewed the plan and rechecked the corrections; this is a reviewed specification, not a claim that the new system is implemented. On 2026-11-01 it became version 2, reconciled to the slide deck's version 12 (Train and Test, the Execution & Audit Agent, the round report); its first milestone (M1) is now served in the meaning Task's Preferences view, as s13 maps the steps. The reconciliation itself has not been re-reviewed.

## Slides

The Subjective Labeling deck is Studio s03's delivery: `s03-agent-role/delivery/deck/` (since 261031; it was `slides/`).

- [Current 23-slide deck](s03-agent-role/delivery/deck/deliverables/agent-mediated-labeling-workflows-and-evaluation-v12-preference-return.pptx): the round report returns to the whole Meaning Loop Agent for investigation, renewed preference collection, versioned updates and rerunning Step 5. [Full PDF](s03-agent-role/delivery/deck/deliverables/agent-mediated-labeling-workflows-and-evaluation-v12-preference-return.pdf) · [Five-page discussion PDF](s03-agent-role/delivery/deck/deliverables/subjective-labeling-preference-return-v12-discussion.pdf).
- [Deck sources and prompts](s03-agent-role/delivery/deck/README.md); versions 1 to 11 in `_archive/20261031/slides-v1-v11/`.
- Concept owner: [Studio s03](s03-agent-role/s03-agent-role.md).

## Questions

```yaml
questions:
- id: Q01
  title: How does a labeling job climb the ladder?
  question: What do the labeling Block, a dataset × label Job, a step Task and an operation Run each
    hold and show on screen, and which of today's four Spaces (Data · Labeling · Quality · Delivery)
    moves to which level?
  hypothesis: 'The Job is today''s page-level workbench: Description = contract and schema, Work Details
    = its step Tasks grouped Building · Scanning, Runs = operations, Delivery = Handoff and final
    labels.'
  acceptance: Answered when every level names its folder and its six Spaces' content, drawn in studio/.
  work: []
  report: reports/q01_labeling_ladder/q01_labeling_ladder.md
- id: Q02
  title: Where do the two sides and the human gates show?
  question: How do Building and Scanning, and the human gates between them (Confirm meaning, freeze,
    test lock, audit), appear in the six Spaces?
  hypothesis: The two sides are the third row of Work Details; each gate is a chip on its step's row
    and a Run the person signs; the Label Handoff is the one crossing, shown in Delivery.
  acceptance: Answered when each gate has one place on screen and the handoff's place is agreed.
  work: []
  report: reports/q02_building_scanning_gates/q02_building_scanning_gates.md
- id: Q03
  title: Where do the schema and the handoff live?
  question: Is `schema.yaml` the Block's or each Job's, and where on disk do the frozen guideline,
    gold and Label Handoff sit?
  hypothesis: The schema is per Job (one label each); the handoff and its frozen parts sit in the
    Job's delivery/, read by Scanning by exact identity.
  acceptance: Answered when the disk layout is written and the workbench reads it.
  work: []
  report: reports/q03_schema_and_handoff/q03_schema_and_handoff.md
```

## Related resources

```yaml
resources:
- title: haipipe-labeling skill (the labeling door; subjective-label until 261007)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/2_theme/labeling/haipipe-labeling
  questions:
  - Q01
  - Q02
  - Q03
- title: haipipe-labeling-building and -scanning (the two sides' law; label-building and label-scanning until 261007)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/2_theme/labeling/haipipe-labeling-building
  questions:
  - Q01
  - Q02
  - Q03
```

## Blueprint home

This Theme is an independent blueprint Block under `blueprints/Project-Ladder/work/b15_theme_labeling/`
since 261010. Its studio topics, questions, reports and Runs keep their existing
identities. Shared toolkit foundations remain in [b01](../../../Project-Packages/work/b01_haipipe-toolkit/board.md).

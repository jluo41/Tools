# b15 · Theme: labeling

board-kind: task-block
package: plugins/haipipe-toolkit
theme: labeling
shared-blueprint: b01_haipipe-toolkit
spine: Design questions about the labeling Theme as one ladder: what a labeling Block, a dataset × label Job, a step Task and an operation Run each hold and show, how the Building and Scanning sides and their human gates map onto the six Spaces, and where the schema and the frozen handoff live.
close: Each recorded question has a report Page with an answer status, and every answered question names the skill, workbench or builder change that settled it.

## Topic

The labeling Theme teaches and freezes what one identified person means by a vague label
(Building: contract, definition, calibration rounds, guideline, the signed Label Handoff), then
qualifies executors on a sealed test, scans the corpus and audits the labels (Scanning). Its
Block holds one Job per dataset × label (`jNN_<dataset>_<label>/`, its `schema.yaml`); its Tasks
are the steps (prepare · keys · label · score); its Runs are one per operation.

Today the Labeling workbench shows a job at page level in four Spaces (Data · Labeling ·
Quality · Delivery), and a board level lists the jobs. The skills came from the
subjective-label plugin (b04 q03).

The shared ladder (b03) gives every level the same six Spaces: Description · Idea Studio ·
Audience Report | Work Details | Runs · Delivery. This Block asks how labeling fits that ladder level
by level, and what it needs that no other Theme has.

Most answers here are a change to the labeling skills (`2_theme/labeling/haipipe-labeling` and its view skills, `haipipe-labeling-building`, `haipipe-labeling-scanning`), the Labeling workbench
server, or b03's shared builder, not a Task Run. A Question may have no work entries; its report
links the changed files and the drawings.

Excluded: the ladder itself and what every Theme shares (b03_project_workbench); moving the plugin's files
(b04_skill_folder).

## Pipeline

```text
chat section -> Related question -> haipipe-question -> skill, workbench or builder change -> report Page
                                                     -> studio/ drawings (shared by the questions)
```

## Pages

No Jobs yet. The shared drawing is `studio/s01-labeling-ladder/s01-labeling-ladder.excalidraw`:
every labeling row, Block to Run, proposed and today. It is drawn from b03's shared definitions
(`b03_project_workbench/studio/s01-overall-tree-structure/`) by `b03_project_workbench/studio/_build/theme_ladder.py`
and rebuilt by b03's `studio/_build/make.sh`.

`studio/s02-labeling-workbench/` is the Labeling workbench as built today (moved from the
server, 261007): the "before" the s01 proposal replaces, shown in its Guide › RoadMap Draw.

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

This Theme is an independent blueprint Block under `blueprints/b15_theme_labeling/`
since 261010. Its studio topics, questions, reports and Runs keep their existing
identities. Shared toolkit foundations remain in [b01](../b01_haipipe-toolkit/board.md).

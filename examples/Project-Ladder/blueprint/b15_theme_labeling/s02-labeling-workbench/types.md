# Types of Guideline Generation

example: examples/Project-Ladder/labeling/b04_guideline_generation
example-kind: design-preview

This Block contains a UI design, with no Job or Task records. It is not an executed example of these types.
The combined b02 walkthrough supplies Items, Meaning and Expression record evidence only; it is not an
independent Guideline Generation Block. Task names below refer to contract identifiers, not operation names.

## Job group type

absence: No fixed Job group type is registered for this independent Block.
for: Group related Job instances when the Block declares a grouping.
holds: Jobs; a group does not change their types.
field: `bands:` on `board.md` names numbered Job groups.
owner: plugins/haipipe-toolkit/skills/3_theme/labeling/hai-labeling/SKILL.md
source: examples/Project-Ladder/labeling/b04_guideline_generation/board.md
proposal: 〈Construct〉 is grouping intent, not a registered type or band.

## Job type

absence: The independent Job Type identifier is not registered.
for: One Items snapshot, construct and human authority. Expression methods and rounds remain inside the Expression Task under the same signed meaning.
holds: `labeling-meaning`, `labeling-expression` Tasks under that binding.
field: `job-type:` on the Job face; no such independent Job face exists in this preview.
owner: plugins/haipipe-toolkit/skills/3_theme/labeling/hai-labeling/SKILL.md
source: plugins/haipipe-toolkit/skills/3_theme/labeling/hai-labeling/SKILL.md
name: 〈Construct and scope〉; Name the Job for the construct and scope agreed with its human authority.

## Task group type

absence: No separate Task group is defined; the Job holds its Tasks directly.
for: A declared group would organize Task instances without changing their types.
holds: No additional grouping layer in this Block design.
field: `bands:` on the Job face would name Task groups; none is declared here.
owner: plugins/haipipe-toolkit/skills/1_base/project/hai-job/SKILL.md
source: examples/Project-Ladder/labeling/b04_guideline_generation/board.md

## Task type

field: `task-type:` on each Task face.
source: plugins/haipipe-toolkit/servers/workbench-labeling/labeling_theme.py `TYPES`.

### labeling-meaning
for: Resolve the construct and reference labels under an identified human authority.
holds: Frame decisions; interaction reports, human preferences and update Runs; versioned meaning and its human approval.
field: `task-type: labeling-meaning` on the Task face.
owner: plugins/haipipe-toolkit/skills/3_theme/labeling/2_labeling/hai-labeling-interaction/SKILL.md
source: plugins/haipipe-toolkit/skills/3_theme/labeling/2_labeling/hai-labeling-interaction/SKILL.md
name: 〈Meaning goal〉; Name the Meaning Task for the semantic question it resolves.
evidence: examples/Project-Ladder/labeling/b02_labeling_walkthrough/j01_example_response_safety/t03_example_meaning/t03_example_meaning.md — `task-type: labeling-meaning`

### labeling-expression
for: Develop executable wording under one signed meaning.
holds: The bound meaning version; Rewrite, Run and Evaluate receipts per expression round; release criteria and a human-signed release.
field: `task-type: labeling-expression` on the Task face.
owner: plugins/haipipe-toolkit/skills/3_theme/labeling/2_labeling/hai-labeling-expression/SKILL.md
source: plugins/haipipe-toolkit/skills/3_theme/labeling/2_labeling/hai-labeling-expression/SKILL.md
name: 〈Expression goal〉; Name the Expression Task for the guidance it develops; alternatives remain inside it.
evidence: examples/Project-Ladder/labeling/b02_labeling_walkthrough/j01_example_response_safety/t04_example_expression/t04_example_expression.md — `task-type: labeling-expression`

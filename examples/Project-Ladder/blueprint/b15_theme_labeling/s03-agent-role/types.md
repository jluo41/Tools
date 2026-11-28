# Types of Labeling at Scale

example: examples/Project-Ladder/labeling/b05_labeling_at_scale
example-kind: design-preview

This Block contains a UI design, with no Job or Task records. It is not an executed example of these types.
The combined b02 walkthrough supplies Items, Meaning and Expression record evidence only; it is not an
independent Labeling at Scale Block. Task names below refer to contract identifiers, not operation names.

## Job group type

absence: No fixed Job group type is registered for this independent Block.
for: Group related Job instances when the Block declares a grouping.
holds: Jobs; a group does not change their types.
field: `bands:` on `board.md` names numbered Job groups.
owner: plugins/haipipe-toolkit/skills/3_theme/labeling/hai-labeling/SKILL.md
source: examples/Project-Ladder/labeling/b05_labeling_at_scale/board.md
proposal: 〈Guideline release〉 is grouping intent, not a registered type or band.

## Job type

absence: The independent Job Type identifier is not registered.
for: One Items snapshot, signed Guideline release and executor configuration. Batches, qualification and audit stay within this binding.
holds: `labeling-scanning`, `eval` Tasks under that binding.
field: `job-type:` on the Job face; no such independent Job face exists in this preview.
owner: plugins/haipipe-toolkit/skills/3_theme/labeling/hai-labeling/SKILL.md
source: plugins/haipipe-toolkit/skills/3_theme/labeling/hai-labeling/SKILL.md
name: 〈Release and population〉; Name the Job for the Guideline release and target population.

## Task group type

absence: No separate Task group is defined; the Job holds its Tasks directly.
for: A declared group would organize Task instances without changing their types.
holds: No additional grouping layer in this Block design.
field: `bands:` on the Job face would name Task groups; none is declared here.
owner: plugins/haipipe-toolkit/skills/1_base/project/hai-job/SKILL.md
source: examples/Project-Ladder/labeling/b05_labeling_at_scale/board.md

## Task type

field: `task-type:` on each Task face.
source: plugins/haipipe-toolkit/servers/workbench-labeling/labeling_theme.py `TYPES`.

### labeling-scanning
for: Execute and audit a frozen guideline without changing its meaning.
holds: The immutable handoff, corpus and executor binding; Test, Scan and Audit operation Runs; terminal item dispositions and the final audit receipt.
field: `task-type: labeling-scanning` on the Task face.
owner: plugins/haipipe-toolkit/skills/3_theme/labeling/hai-labeling-scanning/SKILL.md
source: plugins/haipipe-toolkit/skills/3_theme/labeling/hai-labeling-scanning/SKILL.md
name: 〈Execution goal〉; Name the Scanning Task for the frozen binding it applies and audits.
evidence: plugins/haipipe-toolkit/servers/workbench-labeling/labeling_theme.py — `("labeling-scanning", "labeling")`
evidence: plugins/haipipe-toolkit/skills/3_theme/labeling/hai-labeling-scanning/SKILL.md — `P3 Test`

### eval
for: Optionally compare final labels with separately authorized external gold; this is the Labeling adapter role.
holds: Pinned inputs, an evaluation worker, Run tickets and metrics. The owning scaffold currently requires ModelInstance and AIData inputs; its adapter to final labels and external gold remains to be specified.
field: `task-type: eval` on the Task face.
owner: plugins/haipipe-toolkit/skills/1_base/task/6_eval/hai-task-for-eval/SKILL.md
source: plugins/haipipe-toolkit/skills/1_base/task/6_eval/hai-task-for-eval/SKILL.md
name: 〈Evaluation question〉; Name the optional Evaluation Task for the independent comparison it answers.
evidence: plugins/haipipe-toolkit/servers/workbench-labeling/labeling_theme.py — `("eval",)`
optional: Requires separately authorized external ground truth and a resolved input adapter.

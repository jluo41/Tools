# Types of DataPrep

example: examples/Project-Ladder/insight/InsightDataPrep-Example

These names describe existing responsibilities. Source fields below identify them; they are not new job-type/task-type schema fields.

## Job group type

absent: The Job is already the version; do not repeat it in a version group.

## Job type

### Prep-code version
for: prepare one independently reviewable version of the data preparation chain.
holds: Ordered step definitions and scripts, shared code, step review and version signature/hash; execution stays on the Board.
source: board-kind: insight-dataprep; Job prep, from, signed and hash fields. No job-type field exists.
owner: plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight/SKILL.md

## Task group type

absent: Steps are ordered directly under the prep version; no Task group is needed.

## Task type

### Prep step
for: define one ordered operation in the preparation chain.
holds: step.md interfaces and checks and a script exposing run(ctx); no dataset config, local execution Run or output.
source: step.md step, script, reads, writes, checks, cut and params; order from tNN. No task-type field exists.
owner: plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight/SKILL.md; plugins/haipipe-toolkit/skills/1_base/task/1_data/hai-task-for-data/SKILL.md

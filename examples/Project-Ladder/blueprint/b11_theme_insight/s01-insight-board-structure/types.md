# Types of Insight Board

example: examples/Project-Ladder/insight/Insight-Example

These names describe existing responsibilities. Source fields below identify them; they are not new job-type/task-type schema fields.

## Job group type

### Question version
for: compare analyses that pin the same question release.
holds: Jobs sharing the same release; data and preparation versions remain visible per Job.
source: Job face release; no group directory or bands field required.
owner: plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight/SKILL.md; plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/SKILL.md

## Job type

### Analysis
for: answer a fixed question release on a frozen data version, with signed preparation when used.
holds: The version pins and goal, question-answer Tasks, optional preparation execution, comparisons and review evidence.
source: board-kind: insight-board; Job release, prototype, hash, data and optional prep/dataprep/prep-hash. No job-type field exists.
owner: plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight/SKILL.md; plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight-workflow/SKILL.md

## Task group type

### Preparation
for: keep the preparation execution visible before dependent questions.
holds: The prep Task when the Job pins a prep version; omitted when no preparation is used.
source: Job prep field and its t01_prep-vK Task.
owner: plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight/SKILL.md

### Question level
for: read answers at the Data, Information, Knowledge, Wisdom and Executive levels.
holds: The Tasks whose referenced questions have the matching level; no extra directory.
source: Pinned release.yaml → question.md level and stable question id.
owner: plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight/SKILL.md; plugins/haipipe-toolkit/skills/3_theme/insight/folder-kinds/hai-insight-question/SKILL.md; plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight-evidence-plan/SKILL.md

## Task type

### Preparation execution
for: execute the signed preparation chain for this Job.
holds: The pinned prep version, one whole-chain Run, runtime checks and a ready-output reference.
source: t01_prep-vK face and runs; Job prep and ready fields. No task-type field exists.
owner: plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight/SKILL.md

### Question answer
for: answer one release question using this Job’s pinned evidence.
holds: Question id/source, required segment Runs or cited inputs, answer, findings and independent review.
source: Task question field and the pinned release member; DIKWX is its group, not another Task type.
owner: plugins/haipipe-toolkit/skills/3_theme/insight/folder-kinds/hai-insight-data/SKILL.md; plugins/haipipe-toolkit/skills/3_theme/insight/folder-kinds/hai-insight-information/SKILL.md; plugins/haipipe-toolkit/skills/3_theme/insight/folder-kinds/hai-insight-knowledge/SKILL.md; plugins/haipipe-toolkit/skills/3_theme/insight/folder-kinds/hai-insight-wisdom/SKILL.md; plugins/haipipe-toolkit/skills/3_theme/insight/hai-page-insight/SKILL.md

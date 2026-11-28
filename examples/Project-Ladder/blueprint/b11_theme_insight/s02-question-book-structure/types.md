# Types of Question Book

example: examples/Project-Ladder/insight/InsightQuestionBook-Example

These names describe existing responsibilities. Source fields below identify them; they are not new job-type/task-type schema fields.

## Job group type

absent: The Job is already the version; do not repeat it in a version group.

## Job type

### Question-set version
for: prepare one release of the question set.
holds: Motivation, planned changes and results, release.yaml with all retained and changed members, segments and review/signature evidence.
source: board-kind: prototype; Job release and release.yaml. No job-type field exists.
owner: plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight/SKILL.md; plugins/haipipe-toolkit/skills/3_theme/insight/folder-kinds/hai-insight-question/SKILL.md

## Task group type

### Question level
for: organize definitions by Data, Information, Knowledge, Wisdom and Executive.
holds: Every release member of that level, including members retained by reference from another version.
source: release.yaml member paths → question.md level. No group directory.
owner: plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight/SKILL.md; plugins/haipipe-toolkit/skills/3_theme/insight/folder-kinds/hai-insight-question/SKILL.md; plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight-evidence-plan/SKILL.md

## Task type

### Question definition
for: define a neutral question and how it could be answered.
holds: Stable id, ask, motivation, dependencies, evidence needs, method, script where needed and independent reviews.
source: question.md id, level, ask, needs and agreement; membership from release.yaml. No task-type field exists.
owner: plugins/haipipe-toolkit/skills/3_theme/insight/folder-kinds/hai-insight-question/SKILL.md; plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight-evidence-plan/SKILL.md

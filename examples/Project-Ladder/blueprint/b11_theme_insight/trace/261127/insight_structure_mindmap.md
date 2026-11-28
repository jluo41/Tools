---
title: Insight organization as a horizontal mind map
date: '2026-11-27'
aim: Job Type → Job Name → Task Type → Task Name as connected branches with each parent
  once.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/insight_structure_mindmap.md
  what: request, file plan and acceptance
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_structure.py
  what: horizontal map from existing type model
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure.js
  what: map fit and actual size interaction
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure.css
  what: connected map layout
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/check_structure.py
  what: parent and child mapping guards
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/insight-board.html
  what: generated Board map
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/question-book.html
  what: generated Book map
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/data-prep.html
  what: generated Prep map
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/s01-insight-board-structure.mindmap.md
  what: group each parent once
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/s02-question-book-structure.mindmap.md
  what: group each parent once
- do: edit
  path: examples/Project-Ladder/blueprint/b11_theme_insight/s03-dataprep-structure/s03-dataprep-structure.mindmap.md
  what: group each parent once
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/block-structure.md
  what: horizontal map rule
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/topics.md
  what: record correction and guard
changed:
- examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/insight_structure_mindmap.md
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_structure.py
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure.js
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure.css
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/check_structure.py
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/insight-board.html
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/question-book.html
- examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/data-prep.html
- examples/Project-Ladder/blueprint/b11_theme_insight/s01-insight-board-structure/s01-insight-board-structure.mindmap.md
- examples/Project-Ladder/blueprint/b11_theme_insight/s02-question-book-structure/s02-question-book-structure.mindmap.md
- plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/block-structure.md
- plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/topics.md
---

# Insight organization mind map

## Prompts

User, verified in Work theme design: block skill, thread
01a21d6c-cdee-7580-aeda-b1852ffb4a14, message 01a21dc6-b587-73e3-b35a-f84402b7989b:

> 不是，我意思是做一个mind map一样的炊，你懂吗。

The preceding user message asks for Job Type, Job Name, Task Type, Task Name in four
columns and explicitly rejects a table. Work relayed the correction to this owning session.
The previously verified instruction to update the plan and execute remains in force;
all files above were listed in this chat before editing. No source folder is moved.

## Design

Use Work's left-to-right branching pattern. Group Jobs under their one semantic type;
each named Job branches to its own Task types and concrete Tasks. A Job without Tasks
ends at Job Name. Structure and Draw use one map. Fit and actual-size controls allow
both overview and readable phone inspection. Folder and Studio views keep their content.

## Check

- `python3 -B delivery/structure/check_structure.py`: passed for all three Blocks, including
  one parent per branch, left-to-right connected levels, no-Task termination, no table/select
  output, source links, retained members and existing semantic guards.
- `node --check delivery/structure/structure.js`: passed. Generated output is current.
- Fresh-context validator loaded the current skills and reviewed the implementation; passed
  with no concrete defects. It correctly left visual acceptance to the parent session.
- Actual b11 shared Studio: Structure and Draw both show the horizontal connected map.
  Board has one Job Type node and three named Jobs; DOM geometry found no node overlap.
- Actual Question Book map: both named versions and all retained source references appear.
- Actual DataPrep map: one code-version Job and one step type branch to the three real steps.
- 390 × 844 browser viewport: fit shows the whole pattern; 1:1 shows readable names and
  horizontal scrolling reaches the later levels. Reset viewport and retained deliverable tabs.
- Scoped diff whitespace check passed; all planned readable files remain below 700 lines.
- All source Jobs/Tasks, Folder content, Studio manifests and shared servers are unchanged.

## Summary

Completed the three horizontal organization mind maps. T35 is fixed with a guard. The
DataPrep Markdown tree was already a single-parent tree and required no content change.
The separate live Jobs integration gaps remain T34. This is the same presentation format
subsequently relayed by Design; no additional rewrite or shared server restart is needed.

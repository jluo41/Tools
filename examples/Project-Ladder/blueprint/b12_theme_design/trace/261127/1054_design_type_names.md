---
title: Design Block type and name organization
date: 2026-11-27 10:54
topic: s01-design
aim: Replace generic placeholder hierarchy with verified Job Type, Job Name, Task Type and Task Name relationships for both Design Block types.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1054_design_type_names.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/build_structure_studios.py
  what: Draw and check actual type/name relationships
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/s01-design.md
  what: Record superseding type/name design
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.md
  what: Map Job Type Job Name Task Type Task Name with evidence
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.excalidraw
  what: Synchronize type/name relationship drawing
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.png
  what: Render synchronized preview
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/s02-workbench-ui.md
  what: Record superseding type/name design
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.md
  what: Map Job Type Job Name Task Type Task Name with evidence
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.excalidraw
  what: Synchronize type/name relationship drawing
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.png
  what: Render synchronized preview
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
  what: Record correction and acceptance guard
changed:
- examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1054_design_type_names.md
- examples/Project-Ladder/blueprint/b12_theme_design/delivery/build_structure_studios.py
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/s01-design.md
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.md
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.excalidraw
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.png
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/s02-workbench-ui.md
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.md
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.excalidraw
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/delivery/structure.png
- plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
---

# Design Block type and name organization

## Prompts

- **10:54** Relayed by Work owner: 每一个 block，之所以跟其他 block 不一样，那就是它们的 job name、job type、task name，它们应该有自己的名字……先放在 block structure，它里面 job 种类是什么、job name 是什么、task 种类是什么、task name 是什么，这个一定要弄出来……给每一个 session 发 message，让他们重新更新 plan，然后执行。

## Check

- Type/name structure guard passes: four explicit fields in docs and diagrams, actual names and versions, separate Design Task nodes, no placeholder names, no fabricated Book Tasks, valid source paths and editor routes.
- Ten existing Design Job regression tests pass. git diff --check passes; new builder remains under 700 lines.
- Chrome on the Tailscale 5623 service verified both four-column Structure tables and both Excalidraw Draw views. Actual screenshots: /tmp/design-type-board.jpg and /tmp/design-type-book.jpg. Four top views and live example manifests remain unchanged.

## Summary

Completed the superseding type/name requirement across both Design structure Studios. Updated 11 planned files including this Trace. Folder and shared server code were untouched. No separate persisted type enum was invented; future enum and method-development Tasks require an owning-contract decision.

## Authorization

The Work owner relayed the user’s explicit correction and instruction to update this session’s plan and execute (source thread 01a21d6c-cdee-7580-aeda-b1852ffb4a14). This supersedes the prior generic-placeholder design. The plan was listed in chat before implementation. The quoted message’s exact original timestamp is unavailable; the Trace uses its receipt time. No shared server, skill implementation or example Folder is changed.

## Evidence and boundaries

Board: Design execution → Confirm by reply, by Overall performance (M02 m1, inputs-v2) → Reason ideas / Design / Review whole → reason ideas / reply-first-short and reminder-one-ask / review whole. Book: Method type (registered M01/M02) → M01 · goal only / M02 · overall performance → no Task Type or Task Name. Sources: design-ladder.md The tree and Method Book; design-method SKILL Three layers; design-unit operations; actual Design-Example j03 and four Task faces; MethodBook j01/j02 faces and m2/m1 files. Type labels name contract roles, not newly invented persisted enum fields. The older s05 five-Task proposal remains historical. Actual Folder paths, manifests, shared code and skill implementations are unchanged.

## Drawing preservation

Before replacement, compared both existing diagrams against the prior builder output ignoring only volatile seed/version/update fields. No added or edited human elements were detected. Migration retained any differing or extra elements and replaced only generated content. The regular builder still leaves existing canvases untouched. Both diagrams now show four explicit fields; the Design Task type branches to two separate concrete Task nodes.

---
title: Labeling Job and Task type-name mapping
date: 2026-11-27 10:57
topic: s01-labeling-ladder
aim: Each Labeling structure shows evidence-backed Job and Task types and names, with correct ownership, grouping and explicit unresolved contracts.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/trace/261127/1057_labeling_type_name_mapping.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/model.json
  what: Record named mappings, sources and unresolved contracts
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/build.py
  what: Render type-name relationships and validate evidence
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/structure.css
  what: Lay out the mapping table and named diagrams
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/itemization.html
  what: Regenerate the named Structure and Draw
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/guideline.html
  what: Regenerate the named Structure and Draw
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/scale.html
  what: Regenerate the named Structure and Draw
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/s01-labeling-ladder.md
  what: Document the named mapping and contract gaps
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/studio-views.json
  what: Name the Job and Task organization view
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/s02-labeling-workbench.md
  what: Document the named mapping and contract gaps
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/studio-views.json
  what: Name the Job and Task organization view
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/s03-agent-role.md
  what: Document the named mapping and contract gaps
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/studio-views.json
  what: Name the Job and Task organization view
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/labeling/workbench-labeling/ref/topics.md
  what: Record the correction, evidence and remaining contract gaps
changed:
- examples/Project-Ladder/blueprint/b15_theme_labeling/trace/261127/1057_labeling_type_name_mapping.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/model.json
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/build.py
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/structure.css
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/itemization.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/guideline.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/scale.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/s01-labeling-ladder.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/studio-views.json
- examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/s02-labeling-workbench.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/studio-views.json
- examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/s03-agent-role.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/studio-views.json
- plugins/haipipe-toolkit/skills/3_theme/labeling/workbench-labeling/ref/topics.md
---

# Labeling Job and Task type-name mapping

## Prompts

- **10:57** Work session 01a21d6c-cdee-7580-aeda-b1852ffb4a14 relayed the user correction and instruction to update the plan and execute. Exact user quote: 『每一个 block，之所以跟其他 block 不一样，那就是它们的 job name、job type、task name，它们应该有自己的名字……先放在 block structure，它里面 job 种类是什么、job name 是什么、task 种类是什么、task name 是什么，这个一定要弄出来……给每一个 session 发 message，让他们重新更新 plan，然后执行。』 Requirements: explicitly show Job Type / Job Name / Task Type / Task Name and their relationships; Job topic and Task topic are groupings, not types; verify owning skills, contracts and real files; do not invent types from use cases or hide absent/conflicting contracts; synchronize Structure and Draw; preserve actual folders and Skills view; do not change other themes or shared servers. Earlier generic placeholders are superseded.

## Check

- The new plan named 13 content files, all within the user-approved earlier file list, plus this Trace. Applied only those paths; no other theme, shared server, Job/Task folder or archive was modified.
- Rechecked source contracts and actual files: Items contract and Task face; legacy b02 Job and Meaning/Expression Task faces; labeling_theme.py Task aliases; Scanning contract; b03/b05 synthetic preview model names. No independent Job Type registration was found in these Block contracts; the page explicitly leaves it to define.
- delivery/structure/build.py --check passed: 3 topics, 12 shared views, all declared file/Block targets, fragment anchors, source excerpts, canonical Task types, Guideline Task ownership and no generic Job/Task placeholders.
- Shared Studio component tests: 9 passed. Generated scripts: 9 passed node --check. git diff --check passed; all authored changed files stay below 700 lines (model.json: 299).
- Browser: checked all three named Structure tables and their Draw views on the actual Tailscale workbench. Four fields are visible: Job Type, Job Name, Task Type, Task Name. Existing Task names, preview-model Job names and proposed names are distinguished.
- Browser: compact Draw shows a connected named tree; hiding the shared left list gives a 750px diagram with 3 Itemization, 5 Guideline and 5 Scale relationship edges. Verified named Studio ownership in Scale. Restored the shared left list after checking.
- Three original face archives and all 167 pre-existing protected topic files still match their original hashes. Old canvas marks, deliveries, builders and relative references are preserved.
- Open contract work: define three independent Job Type contracts and materialize/migrate their Job/Task records. The b04 prototype's expression-method Jobs and phase Tasks conflict with the current Meaning/Expression contracts; the b03/b05 previews also still split operations into Tasks. Those examples remain explicitly synthetic and their shared-frame migration stays with T03.

## Summary

Replaced generic placeholders with explicit type/name mappings shared by Structure and Draw. Itemization maps Assistant replies to the existing items type with a proposed consolidated Task name. Guideline uses the actual legacy Response safety Job and its Meaning and Expression Tasks, keeping expression methods and rounds inside the same human meaning ownership. Scale maps Support replies to labeling-scanning and optional eval, with proposed Task names. Job Type gaps are visible rather than invented; Job topic is a grouping and no unsupported Task topic layer is added. Studio ownership names are meaningful and existing folders remain. T05's mapping/presentation correction is fixed with a repeatable guard; missing contracts and example migration remain open under T01/T03. The browser deliverable stays open for review.


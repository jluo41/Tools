---
title: Branching Idea, Grant and Paper organization maps
date: 2026-11-27 11:11
topic: s03-paper-block-structure
aim: Show Job Type → Job Name → Task Type → Task Name as one connected tree, with each parent once and verified semantic names, using the shared Work design renderer.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/trace/261127/1111_branching_block_maps.md
  what: this trace's own record, written first
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/structure/organization.json
  what: Named four-level tree; source links and unresolved contracts stay explicit.
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/structure/jobs.html
  what: Generated connected mind map using the Work renderer; same content in Structure and Draw.
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/studio-views.json
  what: Bind Structure and Draw to the same organization map; retain the existing overview drawing.
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/s01-idea-block-structure.mindmap.md
  what: Align the Job branch to Job Type → Job Name → Task Type → Task Name; preserve other notes.
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/s01-idea-block-structure.md
  what: Record the four-level branching design and links; retain prior decisions.
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/structure/jobs.md
  what: Keep contract evidence as reference documentation; lead with the interactive map link.
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/structure/organization.json
  what: Named four-level tree; source links and unresolved contracts stay explicit.
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/structure/jobs.html
  what: Generated connected mind map using the Work renderer; same content in Structure and Draw.
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/studio-views.json
  what: Bind Structure and Draw to the same organization map; retain the existing overview drawing.
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/s02-grant-block-structure.mindmap.md
  what: Align the Job branch to Job Type → Job Name → Task Type → Task Name; preserve other notes.
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/s02-grant-block-structure.md
  what: Record the four-level branching design and links; retain prior decisions.
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/structure/jobs.md
  what: Keep contract evidence as reference documentation; lead with the interactive map link.
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/structure/organization.json
  what: Named four-level tree; source links and unresolved contracts stay explicit.
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/structure/jobs.html
  what: Generated connected mind map using the Work renderer; same content in Structure and Draw.
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/studio-views.json
  what: Bind Structure and Draw to the same organization map; retain the existing overview drawing.
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/s03-paper-block-structure.mindmap.md
  what: Align the Job branch to Job Type → Job Name → Task Type → Task Name; preserve other notes.
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/s03-paper-block-structure.md
  what: Record the four-level branching design and links; retain prior decisions.
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/structure/jobs.md
  what: Keep contract evidence as reference documentation; lead with the interactive map link.
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/delivery/page-spec/build_organization_maps.py
  what: Render the three domain trees through the Work design renderer without a private UI framework.
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/delivery/page-spec/check_block_structures.py
  what: Check explicit hierarchy, unique siblings, named branches and shared Structure/Draw bindings.
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper/CONSTITUTION.md
  what: Record the required connected mind-map presentation.
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper/ref/topics.md
  what: Record original user wording, verification and remaining runtime boundaries.
changed:
- examples/Project-Ladder/blueprint/b16_theme_paper/trace/261127/1111_branching_block_maps.md
- examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/structure/organization.json
- examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/structure/jobs.html
- examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/studio-views.json
- examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/s01-idea-block-structure.mindmap.md
- examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/s01-idea-block-structure.md
- examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/structure/jobs.md
- examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/structure/organization.json
- examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/structure/jobs.html
- examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/studio-views.json
- examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/s02-grant-block-structure.mindmap.md
- examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/s02-grant-block-structure.md
- examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/structure/jobs.md
- examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/structure/organization.json
- examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/structure/jobs.html
- examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/studio-views.json
- examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/s03-paper-block-structure.mindmap.md
- examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/s03-paper-block-structure.md
- examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/structure/jobs.md
- examples/Project-Ladder/blueprint/b16_theme_paper/delivery/page-spec/build_organization_maps.py
- examples/Project-Ladder/blueprint/b16_theme_paper/delivery/page-spec/check_block_structures.py
- plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper/ref/topics.md
---

# Branching Idea, Grant and Paper organization maps

## Prompts

- **11:11** Verified human message in Work thread 01a21d6c-cdee-7580-aeda-b1852ffb4a14: “不是，我意思是做一个mind map一样的炊，你懂吗。” Relayed to Paper under the earlier verified authorization to update each session plan and execute.
- **11:32** Design owner relayed the same four-level connected-map format, keeping the shared Structure / Draw / Examples / Skills frame and original editable canvas. This was already within the listed plan; no new storage migration was added.

## Check

- Connected-map guard passed for all three Studios, including four-level hierarchy, unique siblings, parent-child edge counts, named content, linked sources and identical primary Structure/Draw bindings.
- All three structured mind-map files passed their grammar checker; builder and guard compile; scoped git diff --check passed.
- Fresh-context workbench-paper invocation passed the semantic and source review. Its generated-output drift finding was resolved by rebuilding after the shared renderer finished; an independent rerun passed.
- Browser acceptance: all three Structure/Draw pairs displayed the same branching map. Paper fit/actual-size controls worked, direct Paper map opened, and the final shared-renderer output was reloaded and visually checked. Paper Studio remains open.
- Existing Excalidraw canvases and seeds were left intact as Overview. No research record, actual folder hierarchy, other theme file or shared server was modified by this plan.

## Summary

Delivered connected Job Type → Job Name → Task Type → Task Name maps for Idea, Grant and Paper using Work's organization_document renderer. Named semantic tree data is separate from runtime schemas; Job-only branches terminate without invented Tasks. Structure and Draw share the same generated content and sources. T08 is fixed with a guard and real-page acceptance; T07 remains open for missing/conflicting type contracts, real Idea/Grant examples and actual-record migration.


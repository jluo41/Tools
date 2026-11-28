---
title: Reuse the shared structure mind map
date: 2026-11-27 11:57
topic: s01-work-structure
aim: Render structure through hai-mindmap inside the owning Block and preserve the existing naming rules and examples.
closed: false
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1157_shared_structure_mindmap.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
  what: Adapt verified data to existing mmmap renderer
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
  what: Verify shared renderer and Block-scoped source links
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/work-organization.html
  what: Embed existing folded mind map
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/blueprint-organization.html
  what: Embed existing folded mind map
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/cowork-organization.html
  what: Embed existing folded mind map
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/discovery-organization.html
  what: Embed existing folded mind map
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_views.py
  what: Route mindmap files to existing focus-map
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_structure_views.py
  what: Guard native mindmap routing and containment
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
  what: Record renderer reuse and user clarification
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1157_shared_structure_mindmap.md
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/work-organization.html
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/blueprint-organization.html
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/cowork-organization.html
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/discovery-organization.html
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_views.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_structure_views.py
- plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
---

# Reuse the shared structure mind map

## Prompts

- **11:57** 协调要求：复用 hai-mindmap 的 mapview/mmmap；结构和例子保留内容，从所属 Block 验收，不再另造 SVG 布局。

## Check

- PASS: check_organization.py validates the four models, naming rules, real sources, original Folder hashes and reproducible outputs.
- PASS: eleven shared Studio tests, including native mindmap routing and containment.
- PASS: 96 embedded scripts pass node --check; scoped git diff --check passes.
- LIVE: Tailscale b17 Block → S01 → Structure / Examples; default collapse, expand all, First command line → First docs switch, readable horizontal scrolling.
- LIVE: source Read CSV opens b01_example_work with group=j01 and task=t01; full directory group parameter was found wrong and corrected before acceptance.
- LIVE: Files pane discovers this registered Trace and planned changes.
- OPEN: consuming theme native .mindmap.md binding needs actual Block acceptance after its manifest switches; Design currently uses its fragment-based HTML adapter. No server restart made by this chat.

## Summary

b17 shared-renderer replacement is implemented and live-checked. Naming rules, examples, actual Folder sections and historic drawings are preserved. Native manifest support is implemented and unit-tested; consuming-theme browser acceptance remains open. Schedule was a misunderstanding and is outside scope.

## Scope

Use existing data models through mmmap.draw; preserve real Folder sections, historic drawings and hand-edited maps. Shared Studio adds only .mindmap.md → focus-map route selection. The existing focus-map route already calls frame.mindmap_module().fragment. Do not restart shared services without coordination. Schedule: current scans find no verified match to the referenced screenshot; clarification requested, no replacement component invented.

## Clarification

用户回复：我不知道你啥意思。慢慢慢普，我不知道啥schedule。

This means mind map; schedule was an interpretation error and is outside this change. No schedule component is required.

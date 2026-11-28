---
title: Labeling shared structure Studios
date: 2026-11-27 10:25
topic: s01-labeling-ladder
aim: Use the shared Studio manifest for Itemization, Guideline Generation and Labeling at Scale while retaining historical decisions, references and canvases.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/trace/261127/1025_shared_structure_studio_integration.md
  what: this trace's own record, written first
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/model.json
  what: Generic structures and real Task boundaries
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/structure.css
  what: Styles for structure content and drawings only
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/build.py
  what: Build content files through shared page components
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/prior-structure-261127.md
  what: Preserve the previous face verbatim
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/s01-labeling-ladder.md
  what: Describe the type and retain historical decisions
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/studio-views.json
  what: Use the shared four-view Studio manifest
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/prior-structure-261127.md
  what: Preserve the previous face verbatim
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/s02-labeling-workbench.md
  what: Describe the type and retain historical decisions
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/studio-views.json
  what: Use the shared four-view Studio manifest
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/prior-structure-261127.md
  what: Preserve the previous face verbatim
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/s03-agent-role.md
  what: Describe the type and retain historical decisions
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/studio-views.json
  what: Use the shared four-view Studio manifest
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/board.md
  what: Register structure topics and keep historical Question answers
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/itemization.html
  what: Generated structure and Draw content
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/guideline.html
  what: Generated structure and Draw content
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/scale.html
  what: Generated structure and Draw content
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/labeling/workbench-labeling/ref/topics.md
  what: Record the shared structure integration and remaining limits
changed:
- examples/Project-Ladder/blueprint/b15_theme_labeling/trace/261127/1025_shared_structure_studio_integration.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/model.json
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/structure.css
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/build.py
- examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/prior-structure-261127.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/s01-labeling-ladder.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/studio-views.json
- examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/prior-structure-261127.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/s02-labeling-workbench.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/studio-views.json
- examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/prior-structure-261127.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/s03-agent-role.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/studio-views.json
- examples/Project-Ladder/blueprint/b15_theme_labeling/board.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/itemization.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/guideline.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/scale.html
- plugins/haipipe-toolkit/skills/3_theme/labeling/workbench-labeling/ref/topics.md
---

# Labeling shared structure Studios

## Prompts

- **10:25** Work session 01a21d6c-cdee-7580-aeda-b1852ffb4a14 relayed: b17 s01–s04 已上线并验证统一格式 Structure / Draw / Examples / Skills。可复用共享 studio-views.json：{"views":[{"name":"Structure","items":[{"name":"Jobs &amp; Tasks","path":"SPACE-relative/file.html"}]},{"name":"Draw","items":[{"name":"Jobs &amp; Tasks","path":"SPACE-relative/file.html","fragment":"draw"}]},{"name":"Examples","items":[{"name":"Example 1","block":"SPACE-relative/block-folder"}]},{"name":"Skills","items":[{"name":"skill-name","path":"plugins/.../SKILL.md"}]}]}。block 必须是实际含 board.md 的目录；不支持外部 URL 或 Job/Task 独立路由。多条目自动复用共享左tab右内容。11项测试通过，17个实际源URL返回200。通用名称放 Structure/Draw，实际案例放 Examples，Skills不另建s5x。共享模块 studio/tabs/studio_views.py 已可使用。预览 http://100.121.165.84:5623/_board/workbench?path=examples%2FProject-Ladder%2Fblueprint%2Fb17_theme_work&amp;layout=focus&amp;section=studio&amp;group=Structure#s01-work-ladder
- **10:46** Go ahead to implement them

## Check

- Applied exactly the 17 approved content files; the only additional repository change is this planned Trace. No shared renderer or existing example Block was changed.
- Real shared Studio reader and renderer: 3 topics, 12 top views; all manifest targets and fragments validated. The new repeatable guard is delivery/structure/build.py --check.
- Shared component unit tests: 9 passed. Nine generated JavaScript blocks passed node --check. git diff --check passed; all authored changed files stay under 700 lines.
- Chrome on the Tailscale workbench: opened Structure, Draw, Examples and Skills for Itemization, Guideline Generation and Labeling at Scale. All three example Block frames loaded with their own Block title.
- Fixed the embedded Draw breakpoint: the shared 700px rule hid SVG wires inside a 629px pane. The structure-specific CSS restores wires while retaining the compact tree below 600px. Rechecked visible SVG dimensions and 3/5/5 Jobs-and-Tasks connections, plus 4 Studio-ownership connections. Clicking a Task highlights it and shows its canonical responsibility.
- Three archived faces are byte-identical to the reviewed originals; sibling archives preserve original relative-link bases. All 167 protected topic files, including original canvases, annotations, builders and deliveries, retain their original SHA-256 values. Historical Questions now reference the archived answers; s03 decision IDs remain.
- The browser deliverable is open at the actual b15 Studio route. No server restart was required for these data/content changes.
- Remaining limits belong to T03: b03/b04/b05 example Blocks still use custom synthetic preview shells. This Trace does not claim shared Block-frame migration, persisted execution or production readiness.

## Summary

Implemented the approved structure Studio integration: s01 Itemization, s02 Guideline Generation and s03 Labeling at Scale use the shared studio-views.json reader, with Structure / Draw / Examples / Skills and existing top-view/left-tab/right-content navigation. Historical content and drawings are preserved. Added a repeatable integration check to the approved builder, verified the actual browser interactions and corrected the embedded diagram wire breakpoint. T04 is fixed with its guard; T03 remains open for the separate example Block-frame migration. User confirmation was recorded before applying files.


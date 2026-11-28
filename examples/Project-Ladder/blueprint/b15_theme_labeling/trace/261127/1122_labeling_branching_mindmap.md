---
title: Labeling branching mind map
date: 2026-11-27 11:22
topic: s01-labeling-ladder
aim: Structure and Draw show the same left-to-right named Job/Task mind map, with each parent once and no table or cascading selectors.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/trace/261127/1122_labeling_branching_mindmap.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/build.py
  what: Use one branching mind map in Structure and Draw
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/structure.css
  what: Style the map and Fit/Actual size controls
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/itemization.html
  what: Regenerate the Itemization mind map
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/guideline.html
  what: Regenerate the Guideline mind map
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/scale.html
  what: Regenerate the Scale mind map
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/labeling/workbench-labeling/ref/topics.md
  what: Record the mind-map correction and validation
changed:
- examples/Project-Ladder/blueprint/b15_theme_labeling/trace/261127/1122_labeling_branching_mindmap.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/build.py
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/structure.css
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/itemization.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/guideline.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/scale.html
- plugins/haipipe-toolkit/skills/3_theme/labeling/workbench-labeling/ref/topics.md
---

# Labeling branching mind map

## Prompts

- **11:22** Work session 01a21d6c-cdee-7580-aeda-b1852ffb4a14 relayed: 继续同步用户对 Block Structure 的最新纠正（此前用户已要求我通知各 session 更新计划并执行）：“不是，我意思是做一个mind map一样的炊，你懂吗。” 四层 Job Type → Job Name → Task Type → Task Name 要画成从左到右分叉的 mind map，用连线表达归属；不要四列表格，也不要四个级联选择列表。每个父节点在所属分支只出现一次，保留你主题已经核实的具体类型和名称；无 Task 的 Job 在 Job Name 结束。请据此更新你负责主题的计划和呈现，遵守本 session 的文件授权；不要重新泛化成 Job 1/Task 1，也不要改真实存储层级。b17 已实现并检查：delivery/structure/build_organization.py 的 organization_map，Structure/Draw 共用连线图，支持 Fit to width / Actual size；Folder 不变。参考：http://100.121.165.84:5623/examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/work-organization.html#jobs 。你已有的图如已满足则保留，不必重复重做。
- **received during browser acceptance; exact time unavailable** Design session 01a1bc86-defc-7600-9d10-469cb2f36576 relayed: 用户在 Design 会话明确要求：“你告诉其他人，让他们都服落你这种格式，好吧。” 请将你负责主题的 Block Structure 统一到 Design 当前的横向 mind map 格式，并在已有授权范围内更新计划后执行。
格式要求：
1. 从左到右 Job Type → Job Name → Task Type → Task Name，用连线分叉表达归属；每个父节点在所属分支只出现一次。
2. 保留你主题合同核实的具体类型和名称；Job topic / Task topic 是分组，不能代替类型。无 Task 的 Job 在 Job Name 结束。
3. 不用四列表格、级联选择列表或纵向目录树替代 Jobs / Tasks mind map。
4. Structure 与 Draw 使用同一份组织图内容，支持 Fit to width / Actual size；顶部仍是 Structure / Draw / Examples / Skills，复用共享左侧条目／右侧内容。原可编辑画布可保留为 Canvas 条目。
5. Folder 保持实际目录，不改真实存储层级；统一呈现格式，不复制 Design 的业务内容。若你已满足，就保留并验收，不重复重做。
参考实现：examples/Project-Ladder/blueprint/b12_theme_design/delivery/build_structure_studios.py 的 organization_map、render_structure；两个 s01/s02 的 studio-views.json。
实际预览：http://100.121.165.84:5623/_board/workbench?path=examples%2FProject-Ladder%2Fblueprint%2Fb12_theme_design&amp;layout=focus&amp;section=studio&amp;group=Structure#s01-design
直接图：http://100.121.165.84:5623/examples/Project-Ladder/blueprint/b12_theme_design/s01-design/delivery/structure.html#jobs
请在自己的 Trace 记录具体文件计划和验收；保留既有更改，不改其他主题或重启共享服务器。完成后回报入口及尚未解决的合同边界。Project 主题仅在其拥有的 Block Structure 上采用此格式，不为 Project 本身虚构 Job/Task 层。

## Check

- Builder --check passed for 3 structure Studios and 12 shared authored views, manifest targets, named contract evidence and identical generated Structure/Draw maps.
- Regression fixtures passed: a Job without Tasks ends at Job Name; two Task names under one type produce one shared parent.
- Shared Studio reader: 9 unittest cases passed. JavaScript syntax: node --check passed for 9 generated script blocks.
- Live Chrome acceptance on the Tailscale b15 Workbench: all 3 Structure/Draw Job maps opened. Itemization: 4 nodes/3 edges; Guideline and Scale: 6 nodes/5 edges each. Parents appeared once, Fit/Actual toggled, selected-node details rendered, long names had no clipping.
- SHA256 checks passed for the unchanged named model, all 167 pre-existing protected topic files, and all 3 original-face archives. No folders moved; no other theme or shared server changed or restarted.
- Changed authored files are under 700 lines: builder 226, CSS 60, topics 119. Scoped git diff --check passed.

## Summary

Implemented the approved mind-map presentation correction in the six listed content paths. Structure and Draw now share a left-to-right Job Type → Job Name → Task Type → Task Name map with branching connections, unique parents and Fit/Actual size controls, inside the existing shared Studio views. Kept the verified named model, actual folders and historical assets unchanged. Recorded the Work and Design corrections and the durable checker in T06. Independent Job Type contracts and the production example Block migration remain open under T01/T03; this Trace closes the structure-map work only.


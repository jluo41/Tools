---
title: Labeling uses the existing mind map
date: 2026-11-27 11:57
topic: s01-labeling-ladder
aim: The three structure Studios use the shared folding mind map inside their Block, with naming rules, evidenced examples and preserved historical content.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/trace/261127/1157_labeling_existing_mindmap.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/build.py
  what: Adapt model data through the existing mindmap_module renderer
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/structure.css
  what: Remove private map layout and scaling
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/model.json
  what: Separate naming rules from evidenced example names
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/itemization.html
  what: Regenerate embedded content with shared folding maps
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/guideline.html
  what: Regenerate embedded content with shared folding maps
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/scale.html
  what: Regenerate embedded content with shared folding maps
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/studio-views.json
  what: Bind naming structures and verified examples
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/s01-labeling-ladder.md
  what: Describe shared renderer and example boundaries
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/studio-views.json
  what: Bind naming structures and verified examples
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/s02-labeling-workbench.md
  what: Describe shared renderer and example boundaries
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/studio-views.json
  what: Bind naming structures and verified examples
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/s03-agent-role.md
  what: Describe shared renderer and example boundaries
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/labeling/workbench-labeling/ref/topics.md
  what: Record renderer correction and unresolved schedule component
changed:
- examples/Project-Ladder/blueprint/b15_theme_labeling/trace/261127/1157_labeling_existing_mindmap.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/build.py
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/structure.css
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/model.json
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/itemization.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/guideline.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/scale.html
- examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/studio-views.json
- examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/s01-labeling-ladder.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/studio-views.json
- examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/s02-labeling-workbench.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/studio-views.json
- examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/s03-agent-role.md
- plugins/haipipe-toolkit/skills/3_theme/labeling/workbench-labeling/ref/topics.md
---

# Labeling uses the existing mind map

## Prompts

- **11:57** Work session 01a21d6c-cdee-7580-aeda-b1852ffb4a14 relayed: 用户在本协调会话明确要求：“你检查一下这个，然后让所有的 session都用这一套规则来重新去做。然后你不要再接收别人的信息了，你是来负责发送信息的，OK？” 已核对其截图和现有 hai-mindmap skill，现在统一执行下面的纠正，更新本主题计划并在已有授权范围内实际重做，不能只回复收到。
1. 默认打开本主题对应的 Work Block，在该 Block 的 Studio 内看 Structure/Draw/Examples。向用户交付已验证的 Tailscale Block 入口；内部 HTML、SVG、mindmap 静态文件只作为嵌入内容，不能再作为默认入口或默认打开的独立页面。Job/Task 选择始终留在其 Block。
2. 必须先读 plugins/haipipe-toolkit/skills/1_base/project/hai-mindmap/SKILL.md、ref/grammar.md 和 owning UI 规则。复用已有 scripts/mapview.py 的 CSS/JS/render 与 mmmap.py 的 draw/fragment（由现有 workbench mindmap_module 接入）；用现有 .mindmap.md/数据适配承载本主题内容，不复制或另造布局。
3. 我此前 b17 delivery/structure/build_organization.py 的 organization_map/organization_document 自写 SVG 方案同样属于要纠正的旧方案，停止把它推广成新的公共标准。Design 自写 SVG 也不是替代现有 skill 的标准。复用已有 mind map 才是用户现在要求的标准。
4. 保留每主题已经核实的 Job Type、Job Name、Task Type、Task Name及真实父子关系；分组和类型分开，无 Task 时结束于 Job。Structure 表示固定名称/按工作命名的规则；Examples 使用核实过的具体目录和名称。保持简单、短名称、分组折叠后逐级展开，不靠缩小文字塞下全图。保留真实 Folder、历史决定及人工编辑。
5. 截图还要求使用已有 schedule。已在当前 Workbench/skill 范围定位了 mind map 实现，但尚未核实 screenshot 所指的 schedule 具体组件；请先核对现有组件/调用点，使用已经存在的实现，不凭名称新造一套 schedule。不要将旧 timeline 或 gantt 模板未经核实就认定为所指组件。
6. 共用 Structure / Draw / Examples / Skills 与既有顶视图/左条目/右内容框架。若现有 Studio 绑定缺少 mindmap 接入，统一由 Work theme design 处理共享入口，其余主题只改自身内容/绑定，避免各主题私建 renderer 或同时改共享服务器。不要未经协调重启服务。
7. 依本会话既有授权和仓库要求记录具体文件计划、保留脏改动，使用已登记可见的 Trace。验收必须实际从所属 Block 打开、展开节点、检查文字可读和来源链接；记录真实缺口，不把设计示例称为已创建的实际 Jobs。
8. 本协调会话现在只负责向外发送统一要求，不再接收各 session 的汇报或交办。请不要向 01a21d6c-cdee-7580-aeda-b1852ffb4a14 发送确认、进展、完成汇报或任务。结果和阻塞留在你自己的 session 与 Trace；仅当用户要求时再汇报。无需回复本消息。

## Check

- Read hai-mindmap/SKILL.md, ref/grammar.md, mmmap/mapview and owning UI rules. Compared live b01 and b16 Block maps: 3/2 closed cards, 151px/123px height, no open branches.
- Builder --check passed: 3 Studios and 12 shared views; component module identity, unmodified mapview CSS/folding/readonly JS, equal Structure/Draw bindings, named evidence, actual Itemization example source, one parent per type and a Job without Tasks.
- Owning mind-map suite: 33 tests passed. Final shared Studio suite: 11 tests passed. Its new mind-map fixture initially failed during concurrent shared work, then passed on final rerun; this session did not modify the shared test or server.
- Browser acceptance began at the Tailscale b15 Work Block. Structure, Draw and Examples opened for all 3 types; each Structure map started closed at 79px high. Progressive Itemization expansion, Open all / Close all, Guideline Meaning/Expression branches and Scale optional eval were checked. Node text remained 13.5–14.5px with transform none.
- Browsed existing b02 example Block inside Examples and opened the Scanning contract source successfully. Verified short visible names retain full names in detail, actual records and proposed names are distinguished, and Scale does not claim created Jobs or Tasks. Studio ownership also expanded through the shared map.
- SHA256 preservation passed for 167 pre-existing topic assets and 3 archived faces. All historical decisions retained, no real folders moved, no original mindmap or canvas edited. Six distinct generated JavaScript blocks passed node --check. Authored files remain below 700 lines; scoped git diff --check passed.
- Schedule search: no corresponding UI component/call site identified in Workbench Studio/page code or Labeling. A gantt HTML template exists but is not established as the requested schedule. T08 remains open; no schedule replacement or binding is claimed.

## Summary

Replaced the private SVG and scaling implementation in the 13 approved content files with a data adapter to frame.mindmap_module().draw and the existing mapview component. Structure/Draw share one binding and show proposed naming rules with verified types; Examples keep actual and proposed names separate, with source links and a real legacy Items case. The default entry remains b15 Studio, using shared four-view navigation; generated HTML is embedded content only. The shared-renderer correction is complete and guarded (T07). Schedule identification (T08), independent Job Type contracts and production example Block migration (T01/T03) remain open. No messages were sent to the coordinating session.


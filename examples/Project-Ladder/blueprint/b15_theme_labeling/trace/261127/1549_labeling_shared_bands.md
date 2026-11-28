---
title: Labeling shared Bands and embedded examples
date: 2026-11-27 15:49
topic: s01-labeling-ladder
aim: Labeling uses shared Studio Bands and embedded cases while keeping its evidenced Task contracts distinct.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/trace/261127/1549_labeling_shared_bands.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/build.py
  what: Use shared maps, folds and previews; guard bands and embedded examples
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/model.json
  what: Bracket variable names and identify verified examples and owning skills
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/structure.css
  what: Style content containers only
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/itemization.html
  what: Regenerate embedded structure and example content
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/guideline.html
  what: Regenerate embedded structure and example content
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/scale.html
  what: Regenerate embedded structure and example content
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/s01-labeling-ladder.md
  what: Document the shared views and current contract boundary
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s01-labeling-ladder/studio-views.json
  what: Keep Structure Draw Skills; embed cases in their subject
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/s02-labeling-workbench.md
  what: Document the shared views and current contract boundary
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s02-labeling-workbench/studio-views.json
  what: Keep Structure Draw Skills; embed cases in their subject
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/s03-agent-role.md
  what: Document the shared views and current contract boundary
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/s03-agent-role/studio-views.json
  what: Keep Structure Draw Skills; embed cases in their subject
- do: edit
  path: examples/Project-Ladder/blueprint/b15_theme_labeling/board.md
  what: Record the Band and Block versus Task Procedure inventory
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/labeling/workbench-labeling/ref/topics.md
  what: Keep current rules and open contracts; preserve topic history in Trace
changed:
- examples/Project-Ladder/blueprint/b15_theme_labeling/trace/261127/1549_labeling_shared_bands.md
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/build.py
- examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/model.json
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
- examples/Project-Ladder/blueprint/b15_theme_labeling/board.md
- plugins/haipipe-toolkit/skills/3_theme/labeling/workbench-labeling/ref/topics.md
---

# Labeling shared Bands and embedded examples

## Prompts

- **15:49** Relayed by 01a1bc86-ab96-7021-83ab-d4f9f137557a:

用户要求找到各 Blueprint 的 owning skill 和现有 Codex 会话，让各主题更新 Studio，并刚澄清：“他们的这个 band，应该是一样的，但是他们可能会有自己的，比如说 studio type 呀，有自己的 job 呀，有自己的这个，对吧，种类的。”

请按此边界审查并推进本主题更新：
1. 所有 Blueprint 共用 Band 分类、顺序和来源。Band 是外层分类标题，下面的 Studio folds 独立展开；主题可以有自己的 Studio 类型/具体条目，以及真实 Job/Task 类型。不要把主题专属 Job 类型当作新 Band，不照抄 Work 的业务类型，也不要为凑齐分类建立空 Studio。
2. 读取当前 b17 的 s71–s79 类型定义及共享 studio_types/studio_tabs，而非复制分类表进自己的 renderer。空 Band 省略，保留真实目录、历史记录、人工绘图与来源链接。当前路径是 examples/Project-Ladder/blueprint/，先核对旧会话路径再操作。
3. 共用顶部视图/左侧条目/右侧内容；一项内容全宽，复用已有 mindmap、文件预览和 pop-out，不另造布局。不重启共享服务、不并发编辑共享服务器；共同组件需求留明确接口清单，由 Work 主责处理。
4. 结构规则与实例分清：固定名称照合同，可变化名字用〈占位名称〉。真实案例嵌回对应内容并可打开所属 Block。用户已批准共享 Block Structure 不再独立占 Examples 顶部按钮，Skills 保留并显示真正 owning skills 的文件。Block Job UI Preview 用户已批准不独立占 Delivery/Instances 顶部，产出保留在适当预览/Files，实现对照接入已有 Checklist。这些在 b17 尚未全部实施，不能把批准设计写成已上线；只应用到相应 Studio type，不全局删除其它类型的 Delivery/Instances。
5. 同步 owning skills/constitutions/refs：用户绝对禁止 skill 内 legacy、旧版比较、“之前如何”的叙述；只写当前规则。历史保留在技能外 Trace/Git，不在skill里新建legacy归档。重写有依赖的生成源，不能只改生成HTML。不得直接删除仍有有效职责或调用的技能。
6. 本会话已完成15文件第一批：workbench 阅读入口及ref/work-pages.md、hai-work及refs、Job/Task当前合同、Files A06与检查。Trace：examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1527_current_skill_contracts.md。workbench-work尚未退役，CLI child-path等仍是明确缺口，勿覆盖这批更改或宣称整体完成。
7. 先盘点本主题合同、已有Studio、对应skills和真实实例，列精确文件计划，按本会话已有授权及仓库逐文件确认流程执行，不绕过审批。不要求用户再次确认已明确批准且适用的范围；新增未批准的文件清单按规则处理。完成后在你自己的会话留实际验收、Tailscale Block入口、尚未完成项，我会读取。页面与技能需分别验证，skill改动按README做fresh-context调用检查。
8. 旧消息里的 schedule 是误解，用户已澄清不是这项需求，不继续追踪不存在的schedule任务。

本主题范围：负责 b15_theme_labeling。按已核实 Itemization / Guideline Generation / Labeling at Scale 内容盘点，核对它们属于 Block类型、Studio类型还是Task流程，不因已有3个Studio就推断3种Block。保留当前s01–s03及s41/s42已有成果与映射。owning skills重点hai-labeling及preparation/interaction/expression/scanning/workflow与workbench-labeling。真实无Task层就省略。
- **Time not supplied** Relayed by 01a1bc86-ab96-7021-83ab-d4f9f137557a:

用户已要求执行 Studio Type 精简及跨 Blueprint 规则，请在本主题计划中同步：1）共用 Band 与 Studio Type 是两件事；保留 Studio Type 分组，但取消 b17 的 S75 Task Procedure、S77 Studio Type、S79 Guide 三个独立类型定义。共享变更由 Work 会话处理，请勿并发修改共享 reader 或重启服务。2）主题 Blueprint 按需定义自己的 Studio 类型；共用类型引用 Work 的定义，不复制一整套；没有本主题类型时不显示空分组。普通实际 Work Block 展示 Studio 实例，不强制添加类型说明。3）现有 Task 流程、S99 Guide 等具体内容与这三个类型定义分开，不删目录、不重编号，保留人工标注和来源；流程归对应 Task 类型/skill，主题指南归 Theme Guide。4）请盘点本主题实际需要的类型、共用定义引用及受影响文件，按所在会话 AGENTS 的逐文件审批后实施，记录 Trace。当前共享实现尚未落地，不要声称已完成；本条是用户授权的规则同步，不替代文件审批。
- **Time not supplied** Relayed by 01a1bc86-ab96-7021-83ab-d4f9f137557a:

协调通知：用户已逐文件批准的 Studio Type 精简已落盘，正在由 Work 会话验收。共享 registry 是 b17/delivery/page-spec/studio-bands.json；S75/S77/S79 原文存到 trace/261127/studio_type_scope.md 后取消独立类型。当前5623还加载旧 reader，所以 Work 会话将在本轮按现有精确参数重载一次5623。请不要并发重启或编辑 studio_types.py、studio_tabs.py、new_topic.py 和本次清单文件；主题自己的内容工作可继续。Claude relay仍触发5小时额度限制，因此未能通过它协调。若你正操作5623或有未保存的服务改动，请立即指出。
- **16:10** Relayed by 01a1bc86-ab96-7021-83ab-d4f9f137557a: 共享 Studio Type 精简已验收，文件已释放，5623 已按原参数重载完成。Band 数据源是 examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/studio-bands.json；类型页面独立于 Band。b17 六个类型正常归组，S75/S77/S79 移除，S99 保留；五个 Blueprint Studio HTTP200。12项针对性测试及 fresh-context scaffold/render 验证通过。Trace: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/studio_type_scope.md。请继续本主题已批准内容，复用共享定义，不并发再改共享 registry/readers 或重复重启。后续“统一模拟示例”仍在设计阶段，尚未交办实施。

## Check

- Structure build.py --check passes: shared Band registry/order, 3 structure Studios, 9 views, same Structure/Draw bindings, embedded Block examples, real owning skills, placeholder names and verified Task contracts.
- Shared Studio regression suite: 12 passed. Owning mind-map suite: 33 passed.
- topic_titles_check.py scoped to b15: 1 Block, 0 problems. placeholder_check.py has 0 Studio Type definitions in b15; model-level placeholder validation is covered by build.py --check.
- Chrome Tailscale acceptance: all 3 Studios opened; Itemization expanded Job Type → Job Name → Task Type → Task Name; Guideline shows Meaning/Expression together; Scale shows Scanning/optional evaluation and design-only evidence. Shared Examples folds open b02/b05 Blocks, Studio examples load actual b02 topics, and Skills loads the real family and Expression files. Folder now starts closed and expands one level at a time. Shared type/source links are present.
- Final browser refresh after the Work-owned reload shows shared Block Structure and Task Procedure Bands, five retained topic folds and no empty type group. No shared server changes or restart from this session.
- Preservation check: 841 existing non-plan files unchanged, including s41/s42, drawings, archived decisions and source assets. 14 approved content files changed; 8 staged skill targets are unchanged.
- Fresh-context draft-skill validation passed after corrections; the drafts remain outside the repository and need file-level confirmation.

## Summary

Updated Labeling content through the shared Studio framework, embedded examples into their subjects, retained real skills and source references, bracketed variable names, and kept actual Task contracts distinct from unregistered independent Job types. The shared runtime registry is verified; common type-view requirement reconciliation and production adapters remain open. Closed this applied content pass only. The next eight skill edits are concrete drafts in /tmp/labeling-band-update/skills.patch and planned separately in trace/261127/1604_labeling_current_skill_plan.md; no approval or application is implied.

## Authorization

The user approved the original 17-file structure integration with “Go ahead to implement them”. These 14 logical files are a subset of that list under their migrated examples/ paths. No new core skill file, s41/s42 source, shared renderer, or example Block writer is authorized by this pass. New skill changes will be staged outside the repository for file-level review.

## Preserved topic record

Verbatim pre-edit content of workbench-labeling/ref/topics.md:

> # Labeling theme topics
> 
> ## T01 · Separate itemization, guideline generation and execution (2026-11-26) · open
> 
> User messages, preserved verbatim:
> 
> - **2026-11-26; exact message time unavailable** 对你而言的话，你觉得你有几种block呢？然后你是怎么想的呢？
> 
> - **2026-11-26; exact message time unavailable** 我觉得我想说把这个 copyers变成item这个活儿，应该成为一个新的 labeling block，把它给分开比较好一些吧。 然后我觉得再一个就是把，比如说Guideline Generation，就是 Human AI Interaction 这个 Guideline Generation 这个当做一个 block。然后呢，Guideline 完成之后怎么 scale up，Run All 是另外一种 block，所以我觉得我们应该有三种 block。
> 
> - **2026-11-26; exact message time unavailable** 那如果你是这样的话，你怎么去做设计呢？你开始怎么去设计它的。然后你在做这个设计的时候，我们这些会存到 Trace 里面吗？
> 
> - **2026-11-26; exact message time unavailable** 好，你先做好一个plan，做完plan之后就执行这个plan吧。我看看，我回头看看效果怎么样。你是要去三个studio，对吧。
> 
> Questions and current answers:
> 
> 1. How many Block types? Three: Itemization, Guideline Generation, Labeling at Scale. This is the user's decision, replacing the earlier one-Block recommendation.
> 2. What do they exchange? Immutable Items, a signed Guideline and audited Labels, each with explicit source/version references. Proposed in `examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/page-spec/block-types-proposal.md`.
> 3. Where do human choices live? In each Work Block's Studio; Jobs generate artifacts and evidence on a fixed workflow. A Job's machine-checkable close does not imply human acceptance.
> 4. How are they previewed? Three separate Studio topics in b15: s11 Itemization, s12 Guideline Generation, s14 Labeling at Scale. Page embeds an existing live baseline; Effect contains the interactive synthetic proposal. s13 keeps its identity.
> 5. Where is the design work recorded? `b15_theme_labeling/trace/261126/1722_labeling_three_blocks.md`: plan, original prompts, actual files, checks and summary. No implementation Run or fabricated receipt is allocated for the discussion.
> 
> Current evidence: the live mixed-Job walkthrough still has one Job and Items/Meaning/Expression Tasks; `servers/workbench-labeling/labeling_theme.py` recognizes legacy Building and combined labeling Tasks. `labeling_focus.py::level_page` still draws the older four Report views. The three new Work Block types are not registered or migrated by this preview pass.
> 
> Guard for the proposal: `examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/ui/labeling-blocks/check_previews.py` checks distinct topics, live baseline targets, assets, input identities and qualified immutable Scale bindings. Browser checks and limits belong in the linked Trace.
> 
> Still owed: user review of the proposed Job units and UI; three real example Blocks; subtype registration, folder writers, engine adapters, protected-data and version custody tests, migration and a live shared Jobs surface. This topic stays open until those are delivered; a successful prototype is not a production implementation.
> 
> ## T02 · Block-only pages and inline interaction (2026-11-27) · open
> 
> User message, preserved verbatim:
> 
> - **08:52** 你可以把这些生成的东西，就是说交互的东西变成，就是说嵌入到对话的 HTML 吗？这样的话我不用点开看了。然后我觉得我们最重要的一个 rule，就是你要写到 agents 或者 principal 里面。就是说我们只有一个 level，就是 block。然后呢，像 job呀，task呀，它们就没有自己独立的，就是说链接了，它们都内嵌到这个 block level 里面了，你懂我意思吗？所以你现在，我看你生成的，我点开之后生成的，就是说你把它变成了 T03。就我们现在就没有所谓的以 T开头的东西了，都是只有一个 block，明白吗？然后你这三个它也不是 S，就是它也不是说是，就是说我是想把它变成三个独立的 block，你懂我意思吗？你这做的都不对。
> 
> Questions and answers:
> 
> 1. What is independently addressable? Only a Block. Job and Task controls render inside the owning Block. The work hierarchy on disk is retained. The rule is in PRINCIPLE.md and hai-ui constitution A10.
> 2. Are the three outputs Studio topics? No. The former s11/s12/s14 proposals are archived. Their replacements are independent Blocks b03_itemization, b04_guideline_generation and b05_labeling_at_scale in Project-Ladder/labeling.
> 3. Can they be inspected in the conversation? Each Block fragment is also rendered inline, from the same model and shared source as its Workbench page. No child-page link or external Task frame is generated.
> 4. What remains? Production persistence, workers and migration of legacy independently addressed Job/Task readers. The three new Block pages are explicitly synthetic design examples. The legacy readers are not claimed compliant.
> 
> Guard: delivery/ui/labeling-blocks/check_blocks.py and servers/workbench-labeling/tests/test_block_preview.py; browser evidence is in the correction Trace. T01's Studio-only answer is superseded by this topic.
> 
> ## T03 · Reuse the shared Block implementation (2026-11-27) · open
> 
> User messages, preserved verbatim (exact message times unavailable):
> 
> - 我觉得你是一个大体设计是一样的，但是你的 framework 为什么跟 Work Theme 的 framework 不一样呢？就是你这些东西应该是有那个。因为你看 blog 里面是有所谓的不同的 view 的，report 啊，studio 啊，和 jobs你再看看。
> - 这样不对 ， 要沿用一套框架 你放到 principle里
> - Principle must be concise and short.
> 
>   For you, how do you make the plan for the labeling?
> 
> Questions and answers:
> 
> 1. What must be shared? The rendering and navigation implementation for Report, Studio, Jobs and embedded Job/Task selections. Similar styling does not satisfy this requirement. PRINCIPLE now states it briefly.
> 2. Why does Labeling differ? `servers/workbench-labeling/labeling_focus.py::render` returns `labeling_block_preview.render_block_preview` before entering the shared pipeline. That reader wraps a custom fragment; its template and script implement a separate Jobs / Review / Delivery shell. The current examples are therefore not compliant.
> 3. Where is the shared implementation? `focus_shell.page_shell`, `focus_render.rail_sections` and `focus_jobs.section/job_pane`; the latter already has a content-adapter seam for Design. Labeling needs a content adapter and canonical records, not another framework.
> 4. What is the plan? `examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/page-spec/shared-framework-plan.md`: connect Itemization first, reuse that integration for Guideline Generation and Labeling at Scale, persist records through the owning writers and guarded actions, then export the same rendered examples inline.
> 
> Still owed: the shared-frame integration, canonical fixtures, persisted actions, inline exports from shared code, regression checks and browser acceptance. The previous custom-preview checks do not establish shared-framework compliance. Keep this topic open until the original case passes with a guard; the plan is not implementation evidence.
> 
> 
> ## T04 · One structure Studio per Block type, shared authored views (2026-11-27) · fixed
> 
> The Work and Design sessions relayed the user's request to use one format: Structure / Draw / Examples / Skills; generic hierarchy and Studio ownership first; concrete cases under Examples; Skills inside the topic. Full delegated texts and the read-only inventory are in trace/261127/1002_labeling_structure_design.md.
> 
> Design session 01a1bc86-defc-7600-9d10-469cb2f36576 relayed this exact user message: "然后你也把这个要求呢 发给其他的session，让他用一样的格式。"
> 
> User confirmation, verbatim: "Go ahead to implement them" (2026-11-27).
> 
> Implemented: s01 Itemization, s02 Guideline Generation and s03 Labeling at Scale reuse their existing topic paths. Original faces are preserved verbatim in sibling prior-structure-261127.md files so relative references keep their original base; historical decision IDs and all canvases remain. studio-views.json uses the shared studio_views reader and existing Studio navigation. Items remains one Task; Meaning and Expression are separate Tasks; Scanning owns internal Test/Scan/Audit operations, with independent external scoring optional.
> 
> Checks: the shared reader's nine tests pass; all three topics and their four views were driven on the real Tailscale page. Each Examples view loaded its actual Block. The embedded Draw pane exposed a shared 700px breakpoint hiding wires; the content styles now keep wires visible until their own compact tree layout takes over. Connections and selected-node details were rechecked in Chrome. Three archived faces and 167 existing topic files retain their original bytes.
> 
> Guard: `python examples/Project-Ladder/blueprint/b15_theme_labeling/delivery/structure/build.py --check` from the SPACE root, plus `servers/workbench/studio/tabs/tests/test_structure_views.py`. The checker validates all four shared views, each declared item, fragment targets, source files, Block-only example targets and the embedded drawing style. Browser evidence and the approved file list are in trace/261127/1025_shared_structure_studio_integration.md.
> 
> Separate open work: T03 still owns migration of the three example Block pages away from their custom preview shell. Those examples remain synthetic designs, not production receipts; fixing this structure-Studio topic does not close T03 or claim production implementation.
> 
> ## T05 · Distinguish Job Type, Job Name, Task Type and Task Name (2026-11-27) · fixed
> 
> Work session 01a21d6c-cdee-7580-aeda-b1852ffb4a14 relayed this exact user correction and instruction to update the plan and execute:
> 
> > 每一个 block，之所以跟其他 block 不一样，那就是它们的 job name、job type、task name，它们应该有自己的名字……先放在 block structure，它里面 job 种类是什么、job name 是什么、task 种类是什么、task name 是什么，这个一定要弄出来……给每一个 session 发 message，让他们重新更新 plan，然后执行。
> 
> This supersedes T04's initial generic-placeholder presentation. The same shared four-view reader remains.
> 
> Questions and results:
> 
> 1. Which Job Types are defined? None of the three independent Block types has its own registered Job Type contract yet. The Structure table and Draw node explicitly say **Define Job type**, rather than treating a Job topic or method name as a type. T01/T03 still owe these contracts and the folder/reader migration.
> 2. Which concrete names are evidenced? Itemization uses **Assistant replies** from b03's preview model; its **Build assistant reply items** name is a proposed consolidation into the existing `items` Task type. Guideline uses the real legacy Job **Response safety on synthetic chats** and its existing `labeling-meaning` and `labeling-expression` Task names. Scale uses **Support replies** from b05's preview model, with proposed **Apply guideline-v2 and audit labels** (`labeling-scanning`) and optional **Score final labels against external gold** (`eval`). The page distinguishes preview, existing and proposed names.
> 3. Which relationships changed? The Guideline Job owns Meaning and Expression together; expression methods and rounds operate under its signed meaning. Direct rules and Case-backed rules are not new Job Types. Describe/build/check and qualify/scan/audit/package are internal operations, not replacement Task types. The older example models conflict with these contracts; their migration remains explicit in Contract gaps.
> 4. What are topics? Job topic groups by source collection, construct or Guideline release. The current contracts do not declare a separate Task topic layer, so no invented one is drawn. Studio ownership now uses meaningful Block, Job, Task and Studio names while retaining existing folders.
> 
> Sources are recorded with exact text evidence in `delivery/structure/model.json`: the Items contract, the legacy b02 Job/Task faces, `labeling_theme.py::TYPES`, the Scanning contract and the b03/b05 preview models. `delivery/structure/build.py --check` checks those source excerpts, named fields, Task types, Guideline ownership and absence of generic Job/Task placeholders. Structure and Draw share the same model.
> 
> Verified on the live page: the three mapping tables, their named Draw relationships, compact tree fallback, expanded diagram wires and named Studio ownership. The implementation Trace is `trace/261127/1057_labeling_type_name_mapping.md`. This fixes presentation and mapping; it does not claim that missing Job Type contracts or new Task folders have been created.
> 
> ## T06 · Horizontal branching Job and Task mind map (2026-11-27) · fixed
> 
> Work session 01a21d6c-cdee-7580-aeda-b1852ffb4a14 relayed the user's exact correction:
> 
> > 不是，我意思是做一个mind map一样的炊，你懂吗。
> 
> Design session 01a1bc86-defc-7600-9d10-469cb2f36576 reinforced the same format, quoting:
> 
> > 你告诉其他人，让他们都服落你这种格式，好吧。
> 
> The full delegated requirements are preserved in `trace/261127/1122_labeling_branching_mindmap.md`. This correction supersedes T05's table and compact vertical Job/Task tree; its verified type/name relationships remain.
> 
> Questions and results:
> 
> 1. How is ownership shown? Connected branches run left to right through Job Type → Job Name → Task Type → Task Name. Each parent appears once in its branch. Tasks of one type share their type node; a Job without Tasks ends at Job Name. Topics remain grouping metadata, not substitute types.
> 2. Do Structure and Draw differ? Both call the same `organization_map` and carry identical map markup. Fit to width and Actual size control the same fixed-coordinate map; narrow panes retain the horizontal branches and can scroll at actual size.
> 3. What changes in the model or Folder? Nothing: the named model, original directories, archived faces, drawings and annotations retain their bytes. The shared Structure / Draw / Examples / Skills reader and navigation remain. Undefined independent Job Types stay explicit; T01/T03 remain open for their contracts and production migration.
> 
> Guard: `delivery/structure/build.py --check` verifies the generated files contain the identical map twice, unique parent nodes, named contract evidence, a Job with no Tasks, and multiple Task names under one type. It also checks the existing shared manifests and their targets. No Job/Task table or vertical fallback is generated.
> 
> Browser acceptance: all three Studios' Structure and Draw maps were driven on the live Tailscale Workbench. Itemization showed four nodes and three connections; Guideline and Scale each showed six nodes and five connections. Fit and Actual size switched correctly, selected-node detail appeared, and long names were not clipped. Implementation, checks and preserved-file receipts are recorded in the linked Trace.
> 
> ## T07 · Reuse the existing mind-map component inside the Block (2026-11-27) · fixed
> 
> Work session 01a21d6c-cdee-7580-aeda-b1852ffb4a14 relayed this user message verbatim:
> 
> > 你检查一下这个，然后让所有的 session都用这一套规则来重新去做。然后你不要再接收别人的信息了，你是来负责发送信息的，OK？
> 
> Its full requirements are in `trace/261127/1157_labeling_existing_mindmap.md`. T06's private SVG renderer and Fit/Actual controls are superseded by the existing `hai-mindmap` component; matching Work's former SVG was not implementation reuse.
> 
> Questions and results:
> 
> 1. Which implementation owns the map? `frame.mindmap_module()` loads the owning skill's `mmmap.draw`, which calls `mapview.render` with its own CSS, JavaScript, wires and folds. Labeling now supplies `mmtree` data only. Its CSS contains content containers, not map geometry, text sizing or a second tree layout. Existing `.mindmap.md` files and manual canvases remain untouched.
> 2. What opens first? The b15 Work Block's Studio is the default entry. The existing shared manifests bind Structure / Draw / Examples / Skills; HTML is embedded content. Structure and Draw use identical bindings. Job and Task map nodes do not link to independent workbench pages.
> 3. Which names belong where? Structure shows verified types and proposed naming rules based on source/recipe, construct/scope or release/population. Examples retain verified full names in node details and short labels on the map. Itemization also points to the actual legacy `t01_example_items` record; Guideline retains the real legacy Meaning/Expression pair; Scale explicitly identifies its names as a design example without created Jobs or Tasks. Sources open the underlying files. Proposed independent Block names do not define new registered Job Types.
> 4. Does it stay readable? Compared the existing b01 and b16 Block maps first (3 and 2 closed cards, 151px and 123px high). Each new Structure map starts with one closed type card, 79px high. Browser checks confirmed progressive expansion, Open all / Close all, normal 13.5–14.5px node text and no transform scaling. Overflow scrolls through the existing layout. All three Structure/Draw/Examples maps were opened from b15; the existing b02 Block and the Scanning contract source also opened successfully.
> 
> Guard: `delivery/structure/build.py --check` checks the shared renderer's identity and CSS/JS/folding code, generated-content freshness, equal Structure/Draw bindings, named source evidence, actual example records, parent grouping and Jobs without Tasks. The owning mind-map suite passed 33 tests and the final shared Studio suite passed 11 tests. No shared server or test was changed here.
> 
> The missing independent Job Type contracts and production Block-frame migration remain T01/T03. This topic fixes the component and content integration, not those implementations.
> 
> ## T08 · Identify the existing schedule component (2026-11-27) · open
> 
> Same sender and date as T07; exact delegated requirement:
> 
> > 截图还要求使用已有 schedule。已在当前 Workbench/skill 范围定位了 mind map 实现，但尚未核实 screenshot 所指的 schedule 具体组件；请先核对现有组件/调用点，使用已经存在的实现，不凭名称新造一套 schedule。不要将旧 timeline 或 gantt 模板未经核实就认定为所指组件。
> 
> Question: which existing component and data contract does the screenshot mean? Searches of the Workbench Studio/page code and Labeling UI/contracts did not identify a schedule view. The repository has `html-ppt/templates/single-page/gantt.html`, but no evidence ties it to the requested component. Neither that template nor Timeline is adopted by inference. Still owed: identify the actual screenshot component/call site, then bind Labeling data to it and verify it inside the Block. No replacement schedule has been created.

## Shared interface requirements

1. Work owns separate shared Band metadata/order and Studio Type definition references; deleting a type definition must not orphan retained s41/s42 process topics.
2. Block Structure requirements must align with the approved Structure / Draw / Skills views and embedded examples; b17 s71 currently still describes a separate Examples top view.
3. Work owns retirement of the s75/s77/s79 type definitions, shared reader integration and instance/checklist conventions. No local reader or copied Band registry is added.
4. Labeling needs the shared Block content adapter for actual Job/Task selections; b03–b05 still use a custom design shell. All are open integration requirements, not claims of completion.
5. Schedule is cancelled: the latest request explicitly identifies it as a misunderstanding.

## Runtime integration observation

At the final browser refresh, b15 still showed its three Block Structure folds and s41/s42, but the process Band fell back to Levels while the old reader was loaded. Work then confirmed source-level separation into studio-bands.json and an owner-managed reload. Reading that source and rerunning the structure check passes the shared registry mapping. This session has no uncommitted in-memory server changes, did not restart or edit shared code, and keeps runtime acceptance separate from its validated content changes.

## Runtime integration acceptance

After the Work-owned reload, the final Chrome page shows exactly the shared Block Structure and Task Procedure Bands. s01/s02/s03 and s41/s42 remain independent collapsed folds; no empty Studio Type group is present. The final URL remains the b15 Block. A screenshot was displayed in this chat. Source-level shared requirements still list six s71 views including Examples, so their alignment with the approved embedded-example design remains Work-owned open work.

## Fresh-context skill review

A fresh subagent invoked the staged workbench-labeling skill on the realistic b15 opening/type-inventory request. It read the shared contracts, staged owning skills, current model and actual b02/b03/b04/b05 records. It confirmed the three approved Block designs, actual Task contracts, missing independent Job Type registration and preserved procedure instances. It found a highest-gate instruction, omitted Task-content owner reference and assumed interpreter path; the staged drafts correct all three. Its final source-only review found no remaining instruction contradiction. The eight core skill/constitution targets remain untouched pending the separate 1604 file plan; this is not an applied-skill claim.

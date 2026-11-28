---
title: Knowledge topics s05 s15 s55
date: 2026-11-27 22:50
aim: Knowledge is Block type 5 in every band; s05 drops Examples, s15 previews the example Block, s63 becomes s55.
closed: true
plan:
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/board.md
  what: "s05 标题去掉 〈〉；s63 链接改为 s55；Renumbered 加一行。"
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s05-knowledge-structure/s05-knowledge-structure.md
  what: "标题改为 Block Structure: Knowledge；删除 Examples 视图说明。"
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s05-knowledge-structure/studio-views.json
  what: "删除 Examples 视图。"
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/s71-studio-type-block-structure.md
  what: "Examples 视图可选；s05 不设。"
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s15-knowledge-job-preview/
  what: "新增 Knowledge 的 Block Job UI Preview：face、html、studio-views.json，显示 b18 的 Block 页。"
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/s63-skills-knowledge/
  what: "改名为 s55-skills-knowledge/，标题与文件行同步。"
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/s72-studio-type-block-job-ui-preview.md
  what: "Examples 加 s15。"
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-skills/
  what: "s76 face 与 elements.md 中 s63 改为 s55。"
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
  what: "案例 s63 Knowledge 改为 s55。"
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/block-job-ui-preview/TYPE.md
  what: "Job UI Preview 表加 s15 knowledge 行。"
---

## Prompts

1. "why we have the knolwedge with < >, we should drop it."
2. "why the name is not: BlockS Structure: Knoweldge????"
3. "and you will also have a s15 for it."
4. "and the skill s64 sould be the s55."
5. "I think we don't need the Examples. here."
6. "okay"

## Result

- 5623 Studio：s05 视图为 Structure · Job types · Task types · Draw · Skills；s15 显示 block-page、block-studio；s55 出现在 s54 之后，s63 不再出现。
- `build_structure.py --check`（Python 3.13 + pyyaml）通过；s05 的 delivery/structure.html 因共享样式更新而过期，已用 --content-only 重建，未动绘图。
- ui-preview-topic.md 的 Job UI Preview 表按当前编号修正（s12 blueprint、s13 cowork、s14 discovery），并加 s15 knowledge。

## s15 follows its type (s72)

Prompts: "for the s15, you know what is the studio type it is, why you didn't follow that type requirement?" · "yes, I chagned that, please go ahead."

- knowledge/b18_a2ui_learning：用 new_job.py 新建练习 Job j01_interactive_card（job-type: code，bands t0N）与 Task t01_fixed_input_messages（task-type: code）；board.md bands 加 j0N 🃏 Interactive card。
- s05 build_structure.py：b18 的 bands 断言更新；“不得有 Job”改为“只有 j01_interactive_card”。
- s72 build_type_pages.py：s15 的 INSTANCES 指向 j01 / t01，重建；s15 的 Checklist 除 QuickHtml、Draw 外全为 ✅（与 s12-s14 同）。
- 5623：s15 的 Page-Job、Page-Task 实页显示 j01 与 t01。

## Section emojis and b18 as a work page (hai-ui A12)

Prompts: "for there, why no emojis? who will check this? Do you think?" · "even it is the normal block folder, it should have the emojis, what are the check files for it?" · "the layout of the studio, is not the same as … so we should have the band + folds. who will take care of this? I think the servers/workbench-work." · "ok"

- servers/workbench/page/parts_and_map/section_icons.py（新）：一张表 SECTION_ICONS 与 section_label。
- work_frame.SHARED、focus_render 的 Jobs 项、focus_shell.side_launcher 改为读这张表；标题 h1 与 aria-label 保持原样。
- servers/workbench-work/work_theme.claims：face 写 theme: work 或 workbench: work 的 Block 由 work 主题认领；b18 因此是 work 页。
- 新测试 workbench-work/tests/test_knowledge_claim.py 3 passed；workbench/page、studio、labeling、paper 共 424 passed，剩 1 个 paper 失败与本改动无关。
- hai-ui：CONSTITUTION.md 加 A12，constitution/A12-section-icons.md，scripts/section_icons_check.py（--url 检查 25 个示例 Block 全通过；去掉一个表项时会报错）。
- 5623 已重启：b18 菜单与 b17 相同，Studio 为 band + fold。

## b18 s01: Resource names, official images, Page as left tabs

Prompts: R → Resource 1..6 · "add more detailed information about the each resrouces, and describe them in the Draw" · mind map details · "have you read these sources? … select and put their images to the draw" · "too word … top left right format" · "okay, please go ahead and do it"

- 六个来源读原文（a2ui 仓库 docs/site 的 mdx 与 README，Apache-2.0）；五张图为 a2ui.org 渲染页上的单个图形截图，第六张为 README 的 a2ui_gallery_examples.png；均缩小后存 s01-official-sources/assets/，来源写在 assets/SOURCES.md。
- build_studios.py：s01 Draw 为六张卡片（名称、页面、官方图、一句画面说明、Supports）；Page 由 learning.md 按 ## 拆成 delivery/page/NN-*.md，s01 的 Source records 每个 Resource 一个左侧 tab；b18 检查允许 j01。
- learning.md：R1–R6 → Resource 1–6（s01/s11/s21/s31、mind map、旧 trace），s01 每个 Resource 加图与“In the picture”一句；Resource 5/6 标题统一为 Quickstart/Repository。
- 检查：build_studios.py 通过；无头浏览器看 5623：Draw 六图显示，Page 左侧 tab + 右侧内容，图正常显示。

## Knowledge Block type, topic emojis, Questions band

Prompts: "so the JSON is return by our Agent, or … post processing turn the text to the JSON? please markdown my questions … we should have the Band of Questions" · "I wnat a better emojis for this." · "❓ <--- I want to replace this." · "this should be Block Type Knowledge Block, usage: learn new concepts" · "these fives are five types of the work" · "ok"

- focus_identity.py：WORK_BLOCK_TYPES（五种 work Block，按所在文件夹）与 BLOCK_USE_CASE（Blueprint 🎨 Theme development，Knowledge 🎓 Learn new concepts）；test_knowledge_claim.py 加一项，4 passed。
- b18：s01 📑、s11 🧩、s21 👆、s31 🚧；新 band s4N 🤔 Questions；s41 🔧、s42 🔄 两个问题 topic（原话、分 tab 回答、配官方图的 Draw、Map、Slides）。
- s05：Studio 结构加 Questions（face、drawing、check）；--check 通过。
- 未改（不在确认清单）：b17 delivery/page-spec/block-views.md（无 Knowledge 行）、studio-bands-by-block-type.md、s05 mindmap 的 Studio 分支。

## s11 redrawn in the official three parts

Prompt: "ok, go ahead with s11"

- build_studios.py：s11 Draw 改为官方 Overview 的三段（Server · your agent / Transport 三条消息 / Client · your app），action 虚线回到服务端；下方“One surface, two halves”：组件结构与数据模型，用订机票例子（/outbound/pax 1 → 2）；配 Resource 1、Resource 3 官方图。
- s11 learning.md：在 “Three things to distinguish” 后加 Resource 3 图。
- 检查：build_studios.py 通过；PNG 目视无重叠；Page 内图片路径存在。

## s41 made clear: who writes JSON, where the skill goes

Prompts: "previous, agent only return text, now you wwant agent to return json, right? … and we need to add the skill of A2UI to our chatbot?" · "okay, update this, I am not clean about it."

- build_studios.py：s41 Draw 改为 Before（提示 → Model → 文字）与 After（绿色为新增：提示里加 A2UI 技能；模型输出 = 文字 + <a2ui> 块；SDK 编译器把块变成 JSON；文字照旧发给 App）。
- s41 learning.md：加 “Follow-up: does the agent now return JSON?”（原话、三段回答、Before/After 表），成为 Page 的一个 tab。
- 检查：build_studios.py 通过；PNG 目视箭头与文字无重叠。

## s41 follow-up: streaming and broken output

Prompt: "so ideal, I need to chnage my chatbot a bit … streaming out like the next token prediction … what is the json is corrupted. also add this questions to s41."

- s41 learning.md：加 “Follow-up: streaming, and broken output”（原话、回答、四行表），依据官方 inference-formats.mdx（open_stream、Direct JSON 修复、校验后交回模型自改）与 overview.mdx（流式编译）。

## s42 redrawn; blurry JSON image fixed

Prompts: "for the s42, you might want to update it e tter." · "The images here are not clear, how to fix it?"

- build_studios.py：s42 Draw 改为四段：① 模型流式写出聊天文字 + 完整的 <a2ui> Express（官方订机票例子）② Agent SDK 四步（拆分、逐句解析、对照 catalog 校验、给 ID 并拆成消息），错误虚线回到模型 ③ 三条 JSON 消息写出关键字段 ④ App 显示；底部绿框追踪 $/return/pax = 2 → updateDataModel → UA 901 显示 2 人。不再嵌入看不清的 Resource 2 图。
- s42 learning.md：去掉 Resource 2 图，改为 “The three JSON messages, in full”，用文字贴出官方 v1.0 三条消息（Apache-2.0）。
- s01 assets/resource-2.png：以 2 倍分辨率重截，不再缩小（1364×4230，约 470 KB），代码清晰。

## s22 added; s21 drawn as two timelines

Prompts: "please add the s 22." · "for s21, how do you make the timeline? … with the A2UI, what is workflow, how data is flowing … wihtout A2UI, what it looks like, please make the draw."

- s22-chatbot-to-a2ui/（新，Methods）：face（原话）、learning.md（起点 + 六步：Catalog、Skill、Compile、Send、Render、Actions；每步“改什么 / 用哪个官方工具 / Travel A2UI 里在哪”，加三类 SDK 包表）、mind map、slides、views；Draw：今天的 chatbot 一行 + 服务器与 App 两个区域内的六步（新增为绿色），配 Resource 5 图。board.md 加链接；s05 check 的 topic 清单加 s22。
- s21 Draw：两条时序图并排（User / App / Your server / Model 四列，时间向下）。无 A2UI：改乘客数要再走一轮模型（红）。有 A2UI：模型写 text + <a2ui>，SDK 编译，App 画卡片；点 + 只改本地数据（绿虚线）；点 Confirm 才发 action。
- 检查：build_studios.py、s05 --check 通过；PNG 目视无重叠。

## s21 icons; server vs model

Prompt: "so what is the different from the Your Server and Model … Your server will be the endpoint? … my endpoint will also call the LLM API, which is the Model … try to make this vivid, adding some icon"

- build_studios.py：s21 每列上方加图标（person、phone、server、写着 LLM 的云），列名改为 App (renderer)、Your server (endpoint)、Model (LLM API)；底部加一句：Your server 即 endpoint，放 Agent 代码与 A2UI SDK，通过 LLM API 调用模型。
- 检查：build_studios.py 通过；PNG 目视四个图标居中。

## Block type by folder first

Prompt: "ok" (fix the wrong Block type, then list the Knowledge rules)

- focus_identity.py：page_type 先按 Block 所在的 Project 文件夹查 WORK_BLOCK_TYPES（work、blueprint、cowork、discovery、knowledge），不论哪个主题画页面；只有文件夹不在表里时才用 theme:/UI 配置判 Blueprint。
- 结果（5623 实页）：work/b01_example_work 由 (Blueprint) 改为 Work Block (Work)；cowork、discovery 示例页出现类型行；b17 与 b18 不变。
- test_knowledge_claim.py 加五种类型一项；servers 测试 233 passed, 1 skipped。

## Shorter titles; hai-knowledge A08 to A10

Prompts: "I feel these stutdio name are a bit long, is that okay? … How to make this to be things like: Application" · "ok"

- b18：七个标题缩短（Resources: Official Docs · Methods: Messages and Data · Methods: Trace a Tap · Methods: Chatbot to A2UI · Applications: When to Use · Questions: What Must Change? · Questions: Who Writes the JSON?），face、board 链接、build_studios.py、views、mind map、learning.md 标题同步；文件夹名不动。band 改名与 Concepts 并入 Methods 已由 s7N 会话完成（A07）。
- hai-knowledge：A04、A06 已由 s7N 会话更新；本会话新增 A08（来源配官方图 + SOURCES.md，Resource 全名）、A09（代码用文字）、A10（Draw 生动、一例追到底）；SKILL.md 加一段指向 A08–A10。
- 已发给 s7N：把 A08–A10 写成 s77–s80 的 must: 条目。
- 检查：b18 type_follow 7 ✅，topic_titles_check 0 problems，build_studios.py --check 通过；assets 全部登记在 SOURCES.md，无 R〈n〉。skill_text_check 报两条不在本次新增行（SKILL.md:149 的 Type 名单、ref/types.md 不存在），已告知 s7N。

## Long titles back; Pages as lists with emojis (A11)

Prompts: "I think I prefer the previous title for the sNN, especailly for the questions." · "for the page part, how to add more bullet points and emojis to make it more vivid to read?" · "ok"

- b18：标题冒号后恢复完整写法，band 名保持 s7N 的单数（Resource、Method、Application、Question）；face、board、build_studios.py、views、mind map 同步。
- b18：七个 learning.md 改写：每个 tab 一句加粗结论，下面每项一行、emoji 开头（含义全 Block 一致），方法步骤与来源以 🔍 Look for 和 ✅ You know it when 结尾；表头加 emoji；代码块与官方图保留。s31 去掉已并入 Method 的 Concepts 说法。
- hai-knowledge：CONSTITUTION 加 A11（含 emoji 含义表），SKILL.md 加一句；已请 s7N 写入 learning 基础 Type 的 Page。
- 检查：build_studios.py 通过；type_follow 7 ✅；topic_titles_check 0 problems；无头浏览器看 s11 第 1 个 tab 正常。
- 补：s77 现在要求每个 Resource 以 🔍 Look for 和 ✅ You know it when 结尾；s01 六个 Resource 已补上；build_studios.py 通过。

## Drawings brought to the learning base type's Draw rules

Prompt: "check the draws, I think you might need to update them again like /hai-studio to update them again"

- 先查：learning 基础 Type 的 Draw 要求 + hai-draw check.py。s22、s41、s42 文字框过多（75–83%，上限 50%），s22、s42 有超过 30 词的文字块；s31 仍是旧草图（无例子、无绿色、无追踪）；s01 没有贯穿的例子。
- build_studios.py：加通用 actor()（person、phone、server、写 LLM 的云、doc）。s01 每张 Resource 1–4 卡片加一行绿色“乘客数”追踪并用箭头串起；s22 六步改为图标、包名拆成三行；s41 前后对比改为图标，绿色追踪“LH 454 从句子移进卡片”；s42 Express 逐行写、$/return/pax 一路绿色追到 UA 901 卡片；s31 重画为决策图（旅行助手 vs 注册表单）加两条边界（盾牌、锁）。
- 检查：七张图 check.py 0 ❌；hai-studio checks/run.py exit 0；build_studios.py --check 通过；PNG 目视无重叠。读者评审代理已启动，结果待回。
- 读者评审：s42 通过；s01、s22、s31、s41 有缺口。已修：s01 加版本规则与新问题；s22 每步加绿色 UA 901·2 人追踪和 Travel A2UI 路径，User 标签，action 线避开数字；s31 在用户与手机之间加 Agent (LLM API)，问题改为“注册表单还是旅行助手用 A2UI”；s41 App 端绿色“renderer 画出 LH 454 卡片”，问题改为本 topic 的“哪些绿色部分”。

## s01 redrawn from scratch as a reading trail

Prompt: "I just don't wnat this rigid display, redraw it from scatch"

- build_studios.py：s01 不再是网格卡片：一条虚线小路（箭头）从学习者出发，依阅读顺序经过六个站点，每站一张官方图（Excalidraw 中略倾斜）、红色图钉、名称、一句画面说明；Resource 1–4 下绿色追踪乘客数；终点是版本牌（v1.0，文档也有 v0.9.1）和绿色“📌 一起固定代码与包版本”。小路先画，图片盖在上面；绕开 Resource 4 的说明文字。
- s05 build_structure.py：hai-studio 的 types/ 改名为 gallery/ 后，block_types_check、block_types_pages 移到 gallery/block-structure/scripts，补一行 import 路径；s05 --check 通过。
- 检查：五张图 check.py 0 ❌；checks/run.py exit 0；build_studios.py --check 通过。

## check_type by name; sharp official pictures

Prompts: "ok" (name the types; s05 names block-structure) · "I feel the content here is not clear enoiugh"

- build_studios.py：check_type 写类型名（resources、methods、applications、questions），不再写 s77–s80 的路径；check 不再依赖 instances: 行。s05 build_structure.py：manifest() 写 "check_type": "block-structure"。type_follow：b18 7 ✅、s05 ✅；checks/run.py exit 0。
- s01 assets：resource-1、3、4、5 按 2 倍重截且不缩小（约 1320 px 宽），resource-6 用 1300 px；SOURCES.md 说明更新。原先缩到 900 px，违反 A09。

## Application merged into Method

Prompts: "application and methods, what are the differences?" · "maybe they are the same, right? How do yoiu think we can merge the two studio type?" · "okay, I think this is want we want, go ahead for it."

- b18：bands 改为 s3N 🧭 Method；_studio_groups.txt 只剩 Resource、Method、Question；s31 改为 Method（face、Tags、board 链接、views、mind map），learning.md 改写为 Method 步骤：Where you start、1. Ask the question、2. Choose、3. Check the boundaries、4. Plan a practice、Try explaining；build_studios.py 的类型表去掉 Application。
- s05：face、mind map（Method · s1N, s2N, s3N）、build_structure.py（三个 band；band 表断言在 s79 退役前兼容）。
- hai-knowledge：A04、A06、A07 与 SKILL.md 改为三个 Type，A07 记下原话。
- 已请 s7N：退役 s79 与 gallery/applications，s78 加“做决定的步骤写两面与边界、练习只是计划”，更新 studio-bands-by-block-type.md。
- 检查：5623 页面 band：Resource [s01] · Method [s11 s21 s22 s31] · Question [s41 s42]；type_follow 7 ✅；标题检查 0；checks/run.py exit 0；s05 --check 通过。

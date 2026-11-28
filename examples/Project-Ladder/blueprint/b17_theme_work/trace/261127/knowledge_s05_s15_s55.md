---
title: Knowledge topics s05 s15 s55
date: 2026-11-27
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
  path: examples/Project-Ladder/blueprint/b17_theme_work/s76-studio-type-skills/
  what: "s76 face 与 elements.md 中 s63 改为 s55。"
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
  what: "案例 s63 Knowledge 改为 s55。"
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/ui-preview-topic.md
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

---
title: Studio types and shared bands
date: 2026-11-27
aim: Separate shared bands from type topics and remove three unnecessary type entries.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/studio_type_scope.md
  what: "新增：写入批准清单、用户原话、三个移除页面的完整原文、实施和验收记录；保留历史在 Trace。"
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/studio-bands.json
  what: "新增：集中定义共享 Band 名称与顺序；Band 不再依赖同名 Studio Type 页面存在。"
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
  what: "修改 Band reader，读取共享定义；保持类型要求和元素说明的读取独立。"
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  what: "共享 Blueprint Band 不由各主题覆盖；非 Blueprint 保持自身分组；修正文档说明。"
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_studio_bands.py
  what: "验证删除三个类型不影响已有分组、主题共用 Band、空分组省略、普通 Block 不被强制注入类型。"
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/new_topic.py
  what: "标题与编号读取同一份 Band 定义，不从类型页面推导。"
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/topic_titles_check.py
  what: "同步检查说明和缺失 Band 的报错来源。"
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_studio_bands.py
  what: "新增：验证创建脚本与页面读取同一 Band，且类型数量不决定分组数量。"
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
  what: "同步 Band、Studio Type、实际 Studio 的区别和 Blueprint 按需引用规则。"
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-numbering.md
  what: "更新编号与分组来源，明确 S75/S77/S79 不再是独立类型；正文只写当前规则。"
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
  what: "校正 A06 的 Band 与 Type 一对一假设和类型范围，规定共用类型引用、主题特有类型按需定义。"
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
  what: "记录本次类型精简与跨 Blueprint 归属问题，按实际验收结果标记。"
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
  what: "结构图读取共享 Band 定义，取消从 S71–S79 页面推导分组。"
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/blueprint-organization.html
  what: "只重建受影响的 Blueprint 结构内容，保留其他三份生成页。"
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
  what: "Studio 组织的来源和验收改为共享 Band 定义，区分类型与实例。"
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/structure--studio.html
  what: "只重建该条要求页面。"
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/s71-studio-type-block-structure.md
  what: "保留类型；把“此页定义所有 Blueprint 的 Band”改为引用共享 Band 定义；保留历史决定。"
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/s72-studio-type-block-job-ui-preview.md
  what: "保留类型；把“此页定义所有 Blueprint 的 Band”改为引用共享 Band 定义；保留历史决定。"
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s73-studio-type-report/s73-studio-type-report.md
  what: "保留类型；把“此页定义所有 Blueprint 的 Band”改为引用共享 Band 定义；保留历史决定。"
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s74-studio-type-ui-plugin/s74-studio-type-ui-plugin.md
  what: "保留类型；把“此页定义所有 Blueprint 的 Band”改为引用共享 Band 定义；保留历史决定。"
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s76-studio-type-skills/s76-studio-type-skills.md
  what: "保留类型；把“此页定义所有 Blueprint 的 Band”改为引用共享 Band 定义；保留历史决定。"
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s78-studio-type-theme-guide/s78-studio-type-theme-guide.md
  what: "保留类型；把“此页定义所有 Blueprint 的 Band”改为引用共享 Band 定义；保留历史决定。"
- do: remove
  path: examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-task-procedure/s75-studio-type-task-procedure.md
  what: "原文完整保存至本次 Trace 后移除独立类型页面；不删除实际 Task 流程、S99 或其他主题内容。"
- do: remove
  path: examples/Project-Ladder/blueprint/b17_theme_work/s77-studio-type-studio-type/s77-studio-type-studio-type.md
  what: "原文完整保存至本次 Trace 后移除独立类型页面；不删除实际 Task 流程、S99 或其他主题内容。"
- do: remove
  path: examples/Project-Ladder/blueprint/b17_theme_work/s79-studio-type-guide/s79-studio-type-guide.md
  what: "原文完整保存至本次 Trace 后移除独立类型页面；不删除实际 Task 流程、S99 或其他主题内容。"
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/studio_type_scope.md
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/studio-bands.json
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_types.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_studio_bands.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/new_topic.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/topic_titles_check.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_studio_bands.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/SKILL.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-numbering.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/blueprint-organization.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/delivery/requirements/structure--studio.html
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/s71-studio-type-block-structure.md
- examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/s72-studio-type-block-job-ui-preview.md
- examples/Project-Ladder/blueprint/b17_theme_work/s73-studio-type-report/s73-studio-type-report.md
- examples/Project-Ladder/blueprint/b17_theme_work/s74-studio-type-ui-plugin/s74-studio-type-ui-plugin.md
- examples/Project-Ladder/blueprint/b17_theme_work/s76-studio-type-skills/s76-studio-type-skills.md
- examples/Project-Ladder/blueprint/b17_theme_work/s78-studio-type-theme-guide/s78-studio-type-theme-guide.md
- examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-task-procedure/s75-studio-type-task-procedure.md
- examples/Project-Ladder/blueprint/b17_theme_work/s77-studio-type-studio-type/s77-studio-type-studio-type.md
- examples/Project-Ladder/blueprint/b17_theme_work/s79-studio-type-guide/s79-studio-type-guide.md
---

# Studio types and shared bands

## Request and approval

> s75 s77 s79 我觉得这三个studio type没必要存在了吧。你觉得呢？

> 然后还有一个点就是说，我们其他的几个block，The Studio页面也要有这个Studio Type。 他们需要有吗？还是没有呢？我这里我也不是很清楚啊。

> 好，我确认了，你现在开始执行吧。

The exact 25-file list was shown before this approval. Learning Block is a separate design discussion. Other theme chats were notified; their content changes are not part of this file list.

## Preserved type records

### examples/Project-Ladder/blueprint/b17_theme_work/s75-studio-type-task-procedure/s75-studio-type-task-procedure.md

```markdown
s75 · Studio Type: Task Procedure
=================================
view: overview
emoji: 🪜
band: s4N
name: Task Procedure

**Stage:** shaping

**Holds:** One per Task type of a theme: its steps, Runs, files, tabs and prompts.

**Title:** `sNN · Task Procedure: <Task type>`

**Examples:** none in b17 yet

**Topic:** the Studio type of the s4N band. Its band, emoji and name above are read by the Studio page (band headings of every blueprint Block), the Studio tab of s02 and hai-studio (new_topic.py titles, topic_titles_check.py). Change them here, nowhere else.

**Feeds:** none


Decided
-------

- s75-D01 · Each Studio type is its own topic in the s7N Studio Type band (JL 261127: "I want each type of the studio should be a sperate markdown. and I want to put them as a group of studio in studio as well.")
```

### examples/Project-Ladder/blueprint/b17_theme_work/s77-studio-type-studio-type/s77-studio-type-studio-type.md

```markdown
s77 · Studio Type: Studio Type
==============================
view: overview
emoji: 🏷️
band: s7N
name: Studio Type

**Stage:** shaping

**Holds:** One topic per Studio type: its band, emoji, name, what it holds and how its topics are titled. The Studio page, the Studio tab of s02 and hai-studio read the band names from these topics.

**Title:** `sNN · Studio Type: <type>`

**Examples:** s71 … s79

**Topic:** the Studio type of the s7N band. Its band, emoji and name above are read by the Studio page (band headings of every blueprint Block), the Studio tab of s02 and hai-studio (new_topic.py titles, topic_titles_check.py). Change them here, nowhere else.

**Feeds:** none


Decided
-------

- s77-D01 · Each Studio type is its own topic in the s7N Studio Type band (JL 261127: "I want each type of the studio should be a sperate markdown. and I want to put them as a group of studio in studio as well.")
```

### examples/Project-Ladder/blueprint/b17_theme_work/s79-studio-type-guide/s79-studio-type-guide.md

```markdown
s79 · Studio Type: Guide
========================
view: overview
emoji: 🧭
band: s9N
name: Guide

**Stage:** shaping

**Holds:** How to use this Block's page; one per Block, always s99.

**Title:** `sNN · Guide: <page>`

**Examples:** s99

**Topic:** the Studio type of the s9N band. Its band, emoji and name above are read by the Studio page (band headings of every blueprint Block), the Studio tab of s02 and hai-studio (new_topic.py titles, topic_titles_check.py). Change them here, nowhere else.

**Feeds:** none


Decided
-------

- s79-D01 · Each Studio type is its own topic in the s7N Studio Type band (JL 261127: "I want each type of the studio should be a sperate markdown. and I want to put them as a group of studio in studio as well.")
```

## Validation

- Approved 25 files changed against their saved baseline, not against unrelated dirty Git changes.
- Shared page suites: 9 tests passed; writer/registry suite: 3 passed.
- b17 title checker: 0 problems.
- Fresh-context skill invocation: actual temporary Blueprint type creation and ordinary Work topic creation; rendered groups and titles verified; no repository edits by reviewer.
- Broader Studio suite: 34 tests, 32 passed under system Python; two builder/preview failures also reproduced with the saved pre-change new_topic.py. Host venv additionally lacks Pillow. These pre-existing drawing checks were not changed.
- Shared server reload coordinated with four theme chats, with exact existing command/options preserved. Claude relay was unavailable due to its 5-hour quota; no Go delivery is claimed.
- Browser at the Tailscale b17 Block: six retained types under Studio Type; three removed types absent; S71 Structure → Studio displayed current registry requirements; S99 Guide opened while S71 stayed expanded.
- Read-only HTTP checks of b11, b12, b15, b16 and b17 completed successfully after reload. No other theme content edited.
- Whitespace, file-length checks and reverse application of the baseline diff passed.

## Boundaries

- Shared type reference examples and theme-specific type content remain with their owning sessions; no copied type sets were created.
- Existing drawing-test failures and pre-existing S99 content are outside this change.
- User's subsequent request for simulated type examples is pending design; no unapproved examples or new Learning Block were added.
- Claude Code availability check returned: "You've hit your 5-hour limit · resets 5pm (America/New_York)". The resume attempt sent no worker instructions.


## Preserved A06 provenance

```markdown
## A06 · A Studio type is the class of its topics: same top and left, the requirement on its right

> "Do you now the relation ship between studio type and studio instance? Just like the class and instance." (JL 261127)
> "for the studio class vs instance, I think we will have the same top, left ... in the class, for the right content, it will be the describption, like what we want to show here, it is more like the requirements, and in the studio instance, it will just be the real things" (JL 261127)

**Rule:** A Studio Type topic shows the same top buttons and left tabs as the topics of its band; its right side states what an instance must show there and why (What, Why, Must show, From, Check), an instance's right side is the real thing.
**Why:** s71 first showed a flat Elements list, then a copy of the Work instance: neither told a reader what a Block Structure topic has to contain.
**Class:** a type that does not read as the specification of its instances; every Studio Type topic (b17 s71-s79), every instance band, every blueprint Block.
**Cases:** ✅ s71 Block Structure (11 requirement pages, right-click words in s71 and s01-s04) · ⬜ s72 Block Job UI Preview (laid out as its instances; requirements not written) · ✅ s76 Skills (6 requirement pages; top 〈skill〉, left SKILL.md, CONSTITUTION.md, ref/, scripts/, 〈folder〉/, 〈file〉) · ⬜ s73-s75, s77-s79 · ⬜ a check that an instance has its type's buttons and tabs
**Check:** each type's requirement pages and views are built from its `elements.md` and are not stale.
**Run:** `PYTHONPATH=plugins/haipipe-toolkit/servers/_host ~/.cache/haipipe/host-venv/bin/python plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_requirements.py examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure --check`
**Status:** open
**Solved by:** `scripts/type_requirements.py`: pages and views from elements.md; `servers/workbench/studio/tabs/studio_types.py`: right-click words

```

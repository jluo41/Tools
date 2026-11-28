---
title: Studio bands by Block type
date: 2026-11-27 17:05
aim: Define the Work theme Block types Studio bands and embed native organization maps.
closed: false
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1705_studio_bands_by_block_type.md
  what: 新增：保存用户要求、获批逐文件计划、执行和验收结果。
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/studio-bands-by-block-type.md
  what: 新增：记录五种Block的Band内容规则、固定名与实例名的区别；Blueprint引用现有registry，Knowledge引用S05与Sources责任边界。
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/studio-organization.mindmap.md
  what: 新增：Work 的 Band → 〈Studio主题〉组织图；短名称、默认折叠，示例不声明为已创建的实例。
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/studio-views.json
  what: 修改：Structure → Studio 指向原生mindmap；Draw中增加同图入口，保留现有人工画布和其他视图。
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/s01-work-structure.md
  what: 修改：补充Studio组织定义和新图链接，保留既有内容、历史决定与人工标注。
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s02-blueprint-structure/studio-organization.mindmap.md
  what: 新增：Blueprint 的 Band → 〈Studio主题〉组织图；短名称、默认折叠，示例不声明为已创建的实例。
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s02-blueprint-structure/studio-views.json
  what: 修改：Structure → Studio 指向原生mindmap；Draw中增加同图入口，保留现有人工画布和其他视图。
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s02-blueprint-structure/s02-blueprint-structure.md
  what: 修改：补充Studio组织定义和新图链接，保留既有内容、历史决定与人工标注。
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s03-cowork-structure/studio-organization.mindmap.md
  what: 新增：CoWork 的 Band → 〈Studio主题〉组织图；短名称、默认折叠，示例不声明为已创建的实例。
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s03-cowork-structure/studio-views.json
  what: 修改：Structure → Studio 指向原生mindmap；Draw中增加同图入口，保留现有人工画布和其他视图。
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s03-cowork-structure/s03-cowork-structure.md
  what: 修改：补充Studio组织定义和新图链接，保留既有内容、历史决定与人工标注。
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s04-discovery-structure/studio-organization.mindmap.md
  what: 新增：Discovery 的 Band → 〈Studio主题〉组织图；短名称、默认折叠，示例不声明为已创建的实例。
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s04-discovery-structure/studio-views.json
  what: 修改：Structure → Studio 指向原生mindmap；Draw中增加同图入口，保留现有人工画布和其他视图。
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s04-discovery-structure/s04-discovery-structure.md
  what: 修改：补充Studio组织定义和新图链接，保留既有内容、历史决定与人工标注。
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_studio_bands.py
  what: 新增只读检查：固定Band与定义一致、占位名明确、manifest目标存在且Structure/Draw同源、Blueprint与registry一致。
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
  what: 追加：记录Studio Band定义这个主题、验证证据和真实剩余工作，不改其他条目。
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1705_studio_bands_by_block_type.md
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/studio-bands-by-block-type.md
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/studio-organization.mindmap.md
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/s01-work-structure.md
- examples/Project-Ladder/blueprint/b17_theme_work/s02-blueprint-structure/studio-organization.mindmap.md
- examples/Project-Ladder/blueprint/b17_theme_work/s02-blueprint-structure/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s02-blueprint-structure/s02-blueprint-structure.md
- examples/Project-Ladder/blueprint/b17_theme_work/s03-cowork-structure/studio-organization.mindmap.md
- examples/Project-Ladder/blueprint/b17_theme_work/s03-cowork-structure/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s03-cowork-structure/s03-cowork-structure.md
- examples/Project-Ladder/blueprint/b17_theme_work/s04-discovery-structure/studio-organization.mindmap.md
- examples/Project-Ladder/blueprint/b17_theme_work/s04-discovery-structure/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/s04-discovery-structure/s04-discovery-structure.md
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_studio_bands.py
- plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
---

# Studio bands by Block type

## Prompts

> 现在我们就 focus 在沃克主题。在沃克主题下面不是这个 block 不是多了一个 Knowledge 吗？你怎么没有把它加进来呢？然后这里面，就是我们就 focus 在沃克主题，沃克主题里面 block 有五个，对吧？然后这五个里边他们的 Studio，那个页面的那个 banner 定好了吗？还是没有定好。

> OK，好的，那你就去这样去执行吧，做plan，看看怎么执行比较好啊。

Approval of the displayed 16-file plan:

> 好，那现在开始是执行吧，好吧。

## Scope

This batch defines S01–S04. Knowledge and Knowledge Sources belong to the separate Knowledge Block design chat; its S05 files are not edited here. Actual work Blocks are not migrated and example topics are not created as work records. Shared server and renderers are unchanged.

## Verification

S01–S04 content and bindings implemented; checks below. The overall topic remains open for the identified gaps.

## Check

- check_studio_bands.py passed: four maps match the content contract/Blueprint registry and both manifest bindings.
- Native mindmap grammar check passed for all four maps. Negative probes reject a wrong Band name and an unbracketed example.
- Browser opened the actual Tailscale Block Studio. S01, S02, S03 and S04 each rendered their native Studio map; Work, CoWork and Discovery nodes expanded. S01 Draw → Studio used the same source and the original canvas entry remained.
- At 390 × 844, expanded CoWork/Discovery branches extended beyond the embedded visible area. Mobile usability is not accepted; no shared renderer or CSS was modified in this batch.
- Baseline comparison confirmed non-Studio Structure items, original Draw entries and other views preserved in all four manifests. All 16 paths exist and are below 700 lines; scoped whitespace checks passed.
- Trace schema is valid, but this approved filename lacks the numeric prefix required by files_tree/trace_view.py:traces. It is not registered in the Files-pane Trace selector. A correctly named registration remains owed; do not claim visible Trace acceptance.
- Knowledge chat is still active; S05/Sources implementation has not been accepted by this chat.

## Summary

The approved content and bindings are implemented in S01–S04. Fixed Band labels and bracketed illustrative topic names are distinct; existing folders and drawings are preserved. Knowledge source ownership is documented and handed to its owning chat. The overall topic stays open for Knowledge acceptance, narrow-screen map usability and Trace selector registration.

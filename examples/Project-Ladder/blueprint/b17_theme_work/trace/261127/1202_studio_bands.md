---
title: Studio Bands group topic folds
date: 2026-11-27 12:02
topic: s31-files-pane
aim: Studio shows named Bands containing the existing independently expandable topic folds.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1202_studio_bands.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  what: Group existing topic folds under visible Band headings
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/tests/test_focus_studio.py
  what: Check group membership, ordering and independent folds
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  what: Record Studio Band grouping rule
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
  what: Record request and verification
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1202_studio_bands.md
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/tests/test_focus_studio.py
- plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
---

# Studio Bands group topic folds

## Prompts

- **12:02** 啊，你还等啥呢？
- Earlier in this session: 我们可不可以在这个这里也加上 B A N D 的呢？就是按照不同的组来分它们。你懂我意思吗？
- Clarification: 你懂我的意思吗？我的意思是说你这个办的当作一个group，你把这些 fold给组织起来。

## Check

- 14 focus Studio tests and 15 Studio tab tests passed; scoped git diff --check passed.
- Chrome on the running Tailscale service: b17 displayed grouped Bands; s01 and s02 remained open independently. b12 displayed Workflow, Structure, Levels, Run and Skill, and Guide containing the existing topic folds.

## Summary

Implemented shared Studio Band headings around existing folds, using authored Tags and group order. Empty groups are omitted and multi-tag topics appear once in the full list. Existing service was relaunched with its original arguments. UI rule A11 and Work topic record now include the regression guard and browser verification.


---
title: 's71: scrolling left tabs, phone layout, examples in place, real Skills, open types, checks'
date: 2026-11-27 19:50
topic: s71-studio-type-block-structure
aim: 's71 and its instances s01-s04: left tabs keep a fixed width and scroll; requirement pages read on a phone; the Examples button goes and each rule links its real example; Skills opens real skill files; types not agreed read 〈 〉 with b01''s names as one example''s values; every requirement names a runnable check or says by eye.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1950_s71_round_two.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  what: 'Studio left tabs: one line, sideways scroll (test_studio_bands.py)'
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_requirements.py
  what: 'page style: narrow label column, label above text on a phone; example links; a view of real skill files'
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
  what: 'Examples view removed, example: lines, skills:, checks named; pages and views rebuilt'
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/records
  what: JL's comment on the label column, as an item card
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/types.md
  what: open types in 〈 〉, b01's names as example values (block_types_pages.py, block_types_check.py follow)
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/studio-views.json
  what: Examples view merged into Structure (s02, s03, s04 the same)
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
  what: expects the new view list
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1950_s71_round_two.md
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_requirements.py
- examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure/elements.md
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/types.md
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/studio-views.json
- examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/check_organization.py
---

# s71: scrolling left tabs, phone layout, examples in place, real Skills, open types, checks

## Prompts

- **19:50** go

## Check

- left tabs: rendered with a long name in headless Chrome, column stays 170px, one line, list scrolls; requirement page at 340px stacks label over text and at 430px keeps a 64-72px label column, no overflow; s71 as served: Structure, Job types, Task types, Draw, Skills (hai-block, -job, -task, -studio), Check; s01 types show 〈Version〉 … 〈display〉; type_requirements --check, block_types_check, placeholder_check pass; studio 62 and hai-studio 70 tests pass; check_organization stops only at the old work folder hash; comment saved as Comment 2 · el.studio.s71-requirements.label-column in b17 records/board-comments.md; not done: merging s01-s04's Examples view into Structure

## Summary

s71 round two: scrolling fixed-width left tabs, phone layout of requirement pages, real Skills, Work's types open in 〈 〉, a script or by eye on every check.


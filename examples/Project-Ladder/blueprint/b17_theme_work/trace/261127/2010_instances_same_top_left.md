---
title: instances same top and left
date: 2026-11-27 20:10
work: [s72, s11, s12, s13, s14, s15]
aim: "Every instance of s72 · Studio Type: Block Job UI Preview (s11 Work, s12 Blueprint, s13 CoWork, s14 Discovery, s15 Knowledge) shows the type's seven top views in the type's order and the type's left tabs under Page-Job and Page-Task. Where the instance has the real thing the right side is the real thing; where it is not built the right side is the type's requirement for that part, its left tab faded; where the Block type has no such level the right side says why."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2010_instances_same_top_left.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/build_type_pages.py
    what: "an instance always gets the seven views and all Page tabs: real, else the type's requirement page (faded), else a one-line reason page; s15 joins the instances; each instance gets the Check view from the type"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/ (s11, s12, s13, s14, s15: studio-views.json)
    what: rebuilt
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/ (s11, s12, s13, s14, s15: delivery/check.html, delivery/types/)
    what: the Check page inherited from s72; a reason page where a level does not exist
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/ (s11, s12, s13, s14, s15 faces)
    what: the Checklist section rebuilt (new on s15)
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/ (studio_tabs.py, tests/test_structure_views.py)
    what: "added after JL's 'yes, it should': a view whose items are all faded draws its top button faded; a test for it"
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2010_instances_same_top_left.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/build_type_pages.py
  - examples/Project-Ladder/blueprint/b17_theme_work/ (s11, s12, s13, s14, s15: studio-views.json, delivery/check.html; s13 delivery/types/no-task-level.html)
  - examples/Project-Ladder/blueprint/b17_theme_work/ (s11, s12, s13, s14, s15 faces: Checklist section)
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  - plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_structure_views.py
---

# instances same top and left

## Prompts

- **20:05** [Image #60] they are the same studio type, right? why they are not the same to [Image #61]
- **20:10** go
- **21:30** yes, 补成 4 个 do this. (s13's Page-Task left tabs)
- **20:25** yes, it should. (the top button of a view that is not built reads faded)

## Check

- 5623's b17 Studio, read from the served page (the Chrome extension is disconnected; not looked at in a browser): s11, s12, s13, s14, s15 and s72 each show Page-Job, Page-Task, Job types, Task types, QuickHtml, Draw, Check, in that order.
- Page-Job has its four left tabs on all five; Page-Task four on s11, s12, s14, s15 and one on s13 (the reason page, which answers 200). s15's and s12's Check pages answer 200.
- s15's earlier Page-Block view (the live Knowledge Block page and its Studio) is replaced: its example Block has no Job, so every part reads the type's requirement and its Checklist marks each ❗.
- A whole view that is not built (QuickHtml on s12) has one item, so it shows full width and nothing fades: only a left tab fades. Fading the top button needs studio_tabs.py, not in this plan.
- build_type_pages.py --check: files current; the parts missing are s12 QuickHtml and Draw, s13 and s14 QuickHtml, and all of s15. check_views.py --check passes on s72, s11, s15; placeholder_check.py passes.
- Later, the top button: 5623 serves QuickHtml faded on s12, s13, s14; Draw on s12; Page-Task and Task types on s13; all six content views on s15; none on s11 or s72. Tests: workbench page, side_pane, studio, home 267 passed, 1 skipped. 5623 and 5602 restarted, both 200.
- Later, s13 (JL: "yes, 补成 4 个 do this"): its Page-Task has the type's four left tabs, each the reason page, in place of one tab; the type-follow check (hai-studio type_follow.py) passes on s11 to s15.

## Summary

The five instances show the type's seven views and Page tabs; a part an instance lacks shows the type's requirement instead of vanishing.

---
title: preview rules skills
date: 2026-11-26 11:20
work: [s11, j13t01]
aim: "The skills that hold the UI preview say what s11 settled today: views of one page share one address and differ only by their mark, a mark names a class or a data attribute, Page and Effect keep left tabs even for one view, a quick view is named for what it shows and is deleted once settled; the check catches two live views with the same address."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1120_preview_rules_skills.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
    what: A08's Rule, Class, Cases and Solved by gain the mark, one address per page, left tabs, naming and deleting a quick view
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A08-preview-on-example-block.md
    what: today's cases (Job Main on the wrong page, Effect without left tabs, Task states) and their fixes
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/ui_preview_check.py
    what: two live views of one topic with the same address (no mark between them) is a problem
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/ref/top-view-left-tab-right-content.md
    what: the one exception to "one thing, full width", a UI preview's Page and Effect
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/README.md
    what: the mark parameter, one line
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1120_preview_rules_skills.md
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/CONSTITUTION.md
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/constitution/A08-preview-on-example-block.md
  - plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/ui_preview_check.py
  - plugins/haipipe-toolkit/servers/workbench/ref/top-view-left-tab-right-content.md
  - plugins/haipipe-toolkit/servers/workbench/README.md
---

# preview rules skills

## Prompts

- **11:19** yes, this is what I want, please also update the skills related to this.

## Check

- ui_preview_check.py on a made-up topic with Topic rows and Job Main at one address: "views 'Topic rows' and 'Job Main' open the same address; give each its mark="; with mark=jsub=main on Job Main: 0 problems.
- On b17: s11, s12, s13 pass; the problems left are older topics with no page and s99-guide-view.
- ui-preview-topic.md already carried the mark, one address per page, left tabs and naming rules (trace 1117).

## Summary

hai-ui A08, its case file and its check, the layout ref and the workbench README now say what s11 settled: one page, different marks; left tabs for Page and Effect; a quick view named for what it shows and deleted once settled.

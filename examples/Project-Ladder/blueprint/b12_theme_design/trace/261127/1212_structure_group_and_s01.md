---
title: "b12 Studio as b17's: Block Structure and Job previews"
date: 2026-11-27 12:12
topic: s01-design
aim: b12 is a blueprint Block for the design theme; its Studio reads as b17's, two bands, Block Structure (s01 Design Board, s02 Design Method Book) and Job previews (s11 Design Board Job, s12 Method Book Job, live over the design examples); j01 stays as Earlier design; every other topic moves to _archive/20261127/.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1212_structure_group_and_s01.md
  what: this trace's own record, written first
- do: move
  path: examples/Project-Ladder/blueprint/b12_theme_design/s03-design-methods/ s04-design-structure/ s05-design-method-ladder/ s06-design-workflow/ s11-design-block/ s12-design-job/ s13-design-task/ s21-run-skill/ s31-design-guide/ s32-design-element-ui/ s33-ui-issue/ s61-design-slides/
  what: to _archive/20261127/, as b16 did today
- do: move
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/
  what: the 261007 overview files (s01-design.excalidraw, .png, .slides.*, .ideas.md, .mindmap.*, .seed.json, result/) to _archive/20261127/s01-design-overview/
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/s11-design-job-preview/s11-design-job-preview.md
  what: face, UI preview Job · design, over design/Design-Example j03
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/s11-design-job-preview/s11-design-job-preview.html
  what: live views job-rows, job-overview, job-tasks, job-findings
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/s12-methodbook-job-preview/s12-methodbook-job-preview.md
  what: face, UI preview Job · design-methodbook, over design/DesignMethodBook-Example j02
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/s12-methodbook-job-preview/s12-methodbook-job-preview.html
  what: live views job-rows, job-overview, job-tasks, job-findings
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/s01-design.md
  what: one lean face like b11 s01; the 261007 stacked face dropped
- do: move
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/
  what: the 261030 face files (s02-workbench-ui.excalidraw, .png, .slides.*, .ideas.md, .mindmap.*, result/) to _archive/20261127/s02-workbench-ui-overview/; design-workbench-ui.* stays (the Guide reads it)
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/s02-workbench-ui.md
  what: one lean face; its old stacked face said Delivery type ui, so the preview check flagged it
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/board.md
  what: bands and examples lines; Topic tree of the new topics; Questions' report paths
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/_studio_groups.txt
  what: Structure, Job UI
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/0921_design_job_main_bands.md
  what: its s12-design-job files retargeted to s11-design-job-preview
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench-design/tests/test_design_jobs.py
  what: live preview test reads s11-design-job-preview and s12-methodbook-job-preview
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench-design/designboard_theory.py
  what: methods drawing also found in _archive/20261127/s03-design-methods
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/legacy/older-page.md
  what: s03 drawing path to its archive home
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/ui-preview-topic.md
  what: design's two Job UI Previews in the table, as insight's
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
  what: T13 b12 Studio is Block Structure and Job previews, with its guard
changed:
- examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/1212_structure_group_and_s01.md
---

# b12 Studio as b17's: Block Structure and Job previews

## Prompts

- **12:0x** yes, go ahead and update s01, how do you think you should update s01.
- **12:1x** [screenshot of the Structure group: s03 Design methods, s04 Design structure, s05 Design method ladder] I want to remove this out of the structure.
- **12:2x** [screenshot of b17's Studio: 🧱 Block Structure s01 to s04, 👀 Job previews s11 to s14] I want you to update the studio strucutre basd on this.
- **12:2x** you know b12 is actaully the blueprint block, right?

## Plan details

- b12 is a blueprint Block: its own Jobs follow b17 s02 (Blueprint Block Structure) and s14 (Blueprint
  Job UI preview). Its Studio describes the Blocks it plans, the design examples under
  `Project-Ladder/design/`: two Block types, so two structure topics and two Job previews.
- Bands by board.md's `bands:` line, as b17: `j0N 🗄️ Earlier design · s0N 🧱 Block Structure · s1N 👀 Job previews`.
  j01_design_workbench_pages stays under Earlier design (b17 keeps its j01 to j03 the same way).
- Job previews follow hai-studio ref/ui-preview-topic.md: Page holds live views of the example Block's
  Jobs section, one per part (job-rows, job-overview, job-tasks, job-findings); no quick views yet.
- s01's live page reads only `studio-views.json` and `delivery/`; the root overview files are the 261007
  first drawing and its deck, linked from nothing outside s01.
- Not in this change: `s01-design/delivery/structure.md` § Main and a selected Task waits on the Job Main
  trace (0921).

- **12:3x** did you updated the band? [screenshot of b17's bands] what is the emoji, please have the same name.

## Check

- Served on 5623, b12 Studio: 🧱 Block Structure with s01 Design Board Structure and s02 Design Method Book
  Structure, then 👀 Job previews with s11 Design Job UI preview and s12 Method Book Job UI preview.
- Both previews' live addresses render the example Block's Jobs section (Design-Example j03, DesignMethodBook-Example j02).
- `ui_preview_check.py examples/Project-Ladder`: no b12 topic flagged outside j01 (Earlier design, as b17's j03).
- The archived s03 drawing still resolves for designboard_theory.py (`_archive/20261127/s03-design-methods/parts/`).
- Tests: workbench-design suite and hai-draft test_design_board_workbench.py, 88 passed and 1 failed (the live preview test still read s12/s13); after repointing it, test_design_jobs.py 10 passed.
- Chrome was not connected; the page was read from its served HTML.

## Summary

b12's Studio now reads as b17's: two bands with b17's names and emojis, two structure topics with one face each,
two live Job previews. Twelve older topics and the first faces and drawings of s01 and s02 are in `_archive/20261127/`.
The paths moved under the session's feet (blueprints/ is now examples/, work/ is now blueprint/); this trace uses the new paths.

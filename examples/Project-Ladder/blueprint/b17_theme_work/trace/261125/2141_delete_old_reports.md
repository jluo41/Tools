---
title: delete every _old in b17
date: 2026-11-25 21:41
topic: s31-files-pane
aim: 'b17 has no _old/ folder anywhere: the Block''s, j01''s, j02''s and j03''s (17 files, all in git) are gone, and the lines that said a thing went to _old/ say it was removed 261125.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2141_delete_old_reports.md
  what: this trace's own record, written first
- do: delete
  path: examples/Project-Ladder/blueprint/b17_theme_work/_old
  what: two unanswered report placeholders (q02, q03) and two empty folders (q01, q04 moved to s03 and s05)
- do: delete
  path: examples/Project-Ladder/blueprint/b17_theme_work/j01_work_ladder_contract/_old
  what: retired Tasks and a sketch, nothing reads them
- do: delete
  path: examples/Project-Ladder/blueprint/b17_theme_work/j02_workbench_work_skill/_old
  what: retired Tasks and a sketch, nothing reads them
- do: delete
  path: examples/Project-Ladder/blueprint/b17_theme_work/j03_work_workbench_pages/_old
  what: retired Tasks and a sketch, nothing reads them
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/j03_work_workbench_pages/j03_work_workbench_pages.md
  what: '''went to _old/'' becomes ''removed 261125'''
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/j03_work_workbench_pages/t03_task_page/t03_task_page.md
  what: '''went to _old/'' becomes ''removed 261125'''
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/s01-work-structure.ideas.md
  what: '''went to _old/'' becomes ''removed 261125'''
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/s01-work-structure.slides.json
  what: '''went to _old/'' becomes ''removed 261125'''
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/2141_delete_old_reports.md
- examples/Project-Ladder/blueprint/b17_theme_work/j03_work_workbench_pages/j03_work_workbench_pages.md
- examples/Project-Ladder/blueprint/b17_theme_work/j03_work_workbench_pages/t03_task_page/t03_task_page.md
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/s01-work-structure.ideas.md
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/s01-work-structure.slides.json
- examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure/s01-work-structure.slides.html
---

# delete b17 _old

## Prompts

- **21:41** could we remove this as well?
- **21:42** plesae delete the _old, all of them

## Check

- git rm: b17/_old (4), j01/_old (3), j02/_old (6), j03/_old (4); no _old folder left in b17
- j03 face, t03_task_page, s01 ideas and slides say removed 261125; the slides page re-rendered
- the Files page answers 200

## Summary

Every _old folder in b17 is gone: the Block's two unanswered report placeholders and two empty folders, j01's retired scaffold Task, j02's two retired Tasks and j03's retired element-picks Task and sketch, 17 files in all, removed with git rm so history keeps them. The four live lines that said a thing went to _old/ now say it was removed 261125.


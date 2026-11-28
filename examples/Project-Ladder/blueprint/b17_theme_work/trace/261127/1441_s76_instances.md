---
title: 's76 Instances: the six Skills topics against the type'
date: 2026-11-27 14:41
topic: s76-studio-type-skills
aim: 's76 has an Instances view: one row per Skills topic, one column per left tab of the type, each cell a mark with the requirement on its hover, built and checked by a script; a fold''s file loads only when the fold is opened.'
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1441_s76_instances.md
  what: this trace's own record, written first
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/skills_instances.py
  what: writes s76's delivery/instances.html from elements.md and the six topics; --check when stale or an instance lacks a part
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_skills_instances.py
  what: has, lacks, not applicable
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_requirements.py
  what: keeps an Instances view when the topic has delivery/instances.html
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
  what: 'A06 and A08: the instance check and its command'
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s76-studio-type-skills/ (delivery/instances.html, studio-views.json)
  what: built
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/folder_folds.py
  what: a fold's frame gets its address on open, not when the tab shows
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_folder_folds.py
  what: the frame carries no address until opened
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1441_s76_instances.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/type_requirements.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/CONSTITUTION.md
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/folder_folds.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_folder_folds.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/skills_checklist.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/tests/test_skills_checklist.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/skills-topic.md
- 'examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work, s52-skills-blueprint, s53-skills-cowork, s54-skills-discovery, s60-skill-studio, s61-skill-trace, s62-skills-ladder, s63-skills-knowledge (face: Checklist lines)'
- examples/Project-Ladder/blueprint/b17_theme_work/s76-studio-type-skills/delivery (requirement pages and check.html rebuilt), examples/Project-Ladder/blueprint/b17_theme_work/s51-skills-work (views and check.html rebuilt)
---

# s76 Instances: the six Skills topics against the type

## Prompts

- **14:41** (relayed by the session tools-space-88 as approved by JL in the Codex coordination session) keep the real file and folder names; next add S76's Instances comparison; check the six Skills topics' top, left and right against S76, and really verify folder folds, file preview and long names; machine checks and browser interaction recorded apart; no new layout this round.
- **14:53** (relayed by the session tools-space-ac, not typed here: JL cannot type remotely and asked the Codex coordination session to enter Go for them) go: continue on the listed file plan, scope not widened
- **19:49** go

## Check

- machine: 8 Skills topics against s76's 7 parts, all ✅ or — (skills_checklist.py --check); skills_views.py --check 8 fresh; type_requirements.py --check s76 7 pages; topic titles and placeholders 0 problems
- tests: hai-studio 70 passed (6 new, skills_checklist); studio tabs 30 passed
- browser (headless Chromium, real clicks, before the fold fix): 7 topics, 19 top buttons, 101 left tabs, 0 page errors; 50 file tabs showed text; 200 folds closed at first, 91 opened and showed their file; no clipped tab or fold name at 1440, 900, 390
- browser after the fold fix (5623 restarted): hai-studio ref/ shown: 23 folds, 0 frames with an address, 0 requests; one fold opened: 1 request, 2230 characters; reopened: still shown
- served Block Checklist section: 8 topics' lines shown, no marker text
- changed from the plan: the comparison sits in each topic's Checklist, not in an Instances top view (JL's s72 decision, relayed, and go typed here); so no skills_instances.py, no instances.html, no edit to type_requirements.py. Marker comments were dropped because the page shows a comment line as text; an edit to work_frame.py to hide them was refused by the session's auto review and not made
- not done: nothing checked in JL's own Chrome (extension not connected); top-button wrapping on a phone-wide window not measured

## Summary

Each Skills topic is held against s76 part by part and the result shows in the Block's Checklist; a fold fetches its file only when opened.


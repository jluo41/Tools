---
title: types left tabs
date: 2026-11-27 15:00
work: [s72, s11, s12, s13, s14]
aim: "Under Job types the left tabs are the Block's Job groups, then its Job types, one tab each (an instance: Group · First version, Type · code; the type: 〈Job group〉, 〈Job type〉); the right side lists the Jobs of the picked one. Task types the same, with the example Job's Task groups and the Block's Task types."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1500_types_left_tabs.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/ (elements.md, build_type_pages.py, studio-views.json, delivery/)
    what: "〈Job group〉, 〈Job type〉, 〈Task group〉, 〈Task type〉 as elements and left tabs; the builder writes one page per group and per type of each instance"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/ (s11, s12, s13, s14: studio-views.json, delivery/types/)
    what: rebuilt by s72's builder; the two whole-list pages go
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1500_types_left_tabs.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/ (elements.md, build_type_pages.py, studio-views.json, delivery/: job-group, job-type, task-group, task-type pages; job-types, task-types deleted)
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/ (studio-views.json, delivery/types/)
  - examples/Project-Ladder/blueprint/b17_theme_work/s12-blueprint-job-preview/ (studio-views.json, delivery/types/)
  - examples/Project-Ladder/blueprint/b17_theme_work/s13-cowork-job-preview/ (studio-views.json, delivery/types/)
  - examples/Project-Ladder/blueprint/b17_theme_work/s14-discovery-job-preview/ (studio-views.json, delivery/types/)
---

# types left tabs

## Prompts

- **14:55** [Image #57] for this in the left, it should be something like job group type 1, job gorup type 2, ... job type 1, job type 2, etc. Do you get it>
- **15:00** go

## Check

- 5623's b17 Studio, read from the served page (the Chrome extension is disconnected; not looked at in a browser): s72's Job types has left tabs 〈Job group〉, 〈Job type〉, its Task types 〈Task group〉, 〈Task type〉. s11's Job types: Group · Ideas, Group · Second version, Group · First version, Type · check, Type · code, Type · doc; its Task types: Group · Task Group 1, Group · Task Group 2, Type · code, Type · display.
- A tab's page, s11: Type · code lists its seven Jobs with each one's group; Group · Second version lists j11 to j18 with each one's type. Served 200.
- s12: Group · 🧰 Workbench, Group · 🗄️ Earlier design, Type · no type (its Jobs name none). s13: Group · j0N (its board names no band), Type · cowork-job; no Task types.
- build_type_pages.py --check: files current; the same seven instance gaps as trace 1440 (none in Job types or Task types).
- No server code changed.

## Summary

Job types and Task types have a left tab per group and per type; the type shows the requirement for a group and for a type, an instance its real groups and types with their Jobs or Tasks.

---
title: types from pinned list
date: 2026-11-27 15:45
work: [s72, s11]
aim: "The Job types and Task types views read a Block type's pinned lists (its Block Structure topic's types.md: Job group type, Job type, Task group type, Task type). The type s72's left tabs are numbered slots, 〈Job group type 1〉, 〈Job group type 2〉, 〈Job type 1〉, 〈Job type 2〉 (as s71's); an instance whose Block type has a types.md shows the real names (s11: Version, Ideas, code, check, doc), each with its for:, its holds: and the Jobs or Tasks that have it."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1545_types_from_pinned_list.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/ (elements.md, build_type_pages.py, studio-views.json, delivery/)
    what: "numbered slot tabs; the four parts named 〈Job group type〉, 〈Job type〉, 〈Task group type〉, 〈Task type〉; the builder reads types.md for an instance's tabs when its Block type has one"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/ (studio-views.json, delivery/types/)
    what: rebuilt from s01-work-ladder/types.md
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1545_types_from_pinned_list.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/ (elements.md, build_type_pages.py, studio-views.json, delivery/: job-group-type, task-group-type pages; job-group, task-group deleted)
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/ (studio-views.json, delivery/types/: nine pages, one per pinned type)
---

# types from pinned list

## Prompts

- **15:40** go

## Check

- 5623's b17 Studio, read from the served page (Chrome extension disconnected): s72's Job types tabs 〈Job group type 1〉, 〈Job group type 2〉, 〈Job type 1〉, 〈Job type 2〉, its Task types the same with Task; s11's Job types Version, Ideas, code, check, doc, its Task types Make, Show, code, display, read from s01-work-ladder/types.md.
- A tab's page, s11: check reads its for: and holds:, then j11 and j14 with their group; Version reads its for: and holds:, then the Jobs of First version and Second version (a group belongs to a group type when its name holds the type's word).
- Gap found, not fixed: Make and Show list no Task, because j11's Task groups are named "Task Group 1" and "Task Group 2", which hold neither word. The list or the Job's bands: line has to say which group is which.
- s12, s13, s14 keep their tabs read from the faces: their Block types pin no types.md yet.
- placeholder_check.py: 0 bare slot names. build_type_pages.py --check: files current; the seven instance gaps of before. First try of the check mixed up its two cases (every view read "lacks a group and a type"); fixed.

## Summary

Job types and Task types read the pinned lists: numbered 〈 〉 slots on the type, the real type names on s11, each with what it is for, what it holds and its Jobs or Tasks.

---
title: s72 checklist, no guessing
date: 2026-11-27 19:55
work: [s72, s11, s12, s13, s14]
aim: "s72 · Studio Type: Block Job UI Preview keeps six top views (Page-Job, Page-Task, Job types, Task types, QuickHtml, Draw; Check stays as the Studio check pilot made it): Delivery and Instances go. What Instances compared moves into each instance's own face as a Checklist section, read by the side pane's existing Checklist: ✅ shown, ❗ applies and is missing, — does not apply, 🙋 waits on a decision. A group type lists no Job or Task by a guessed name. Every Page-Task tab opens inside the Block."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1955_s72_checklist_no_guessing.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/build_type_pages.py
    what: "no Delivery or Instances view; checks() gives each instance's lines and the builder writes them into its face's Checklist section as one section it owns whole; group-type pages carry for and holds only; Task tabs use the Block's address; --check fails when Delivery or Instances is back"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/ (elements.md, examples.json)
    what: the Delivery element and its example binding go; the group-type requirement no longer promises a Job or Task list
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/ (studio-views.json, delivery/)
    what: rebuilt; delivery.html and instances.html deleted (built pages)
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/ (s11, s12, s13, s14 faces)
    what: a Checklist section each, written by the s72 builder
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/ (s11, s12, s13, s14: studio-views.json, delivery/types/)
    what: rebuilt; no Delivery view, Task tabs inside the Block, group-type pages without guessed lists
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1955_s72_checklist_no_guessing.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/ (build_type_pages.py, elements.md, examples.json, studio-views.json, delivery/ rebuilt; delivery.html, instances.html deleted)
  - examples/Project-Ladder/blueprint/b17_theme_work/ (s11, s12, s13, s14 faces: a Checklist section)
  - examples/Project-Ladder/blueprint/b17_theme_work/ (s11, s12, s13, s14: studio-views.json, delivery/types/ rebuilt)
---

# s72 checklist, no guessing

## Prompts

- Relayed through other sessions before 19:50 (held until a go typed here): stop matching a group to a group type by its name; separate "applies but not built" from "not decided"; open the Task tabs inside the Block; remove s72's Delivery and Instances top buttons and move the comparison into the existing Checklist.
- **19:50** go

## Check

- 5623, read from the served pages (the Chrome extension is disconnected; not looked at in a browser): b17's 📝 Checklist shows a tab per instance with its lines, e.g. s13: ✅ Page-Job · job-rows, 🙋 job-overview, job-tasks, job-findings, — Page-Task, — Task types, ❗ QuickHtml, ✅ Draw.
- First try put the lines between two HTML comment lines; the side pane showed the comments as text, so the builder owns the whole Checklist section instead.
- s72's views read Page-Job, Page-Task, Job types, Task types, QuickHtml, Draw, Check; s11's the first six. s72's delivery.html no longer answers 200. A group-type page (s11 Version) answers 200 and lists no Job.
- s11's four Page-Task addresses all carry the Block's path with group=j11 and task=t02; the findings one answers 200.
- build_type_pages.py --check: files current, nothing taken out is back; four parts missing, left for JL: s12 QuickHtml and Draw, s13 and s14 QuickHtml.
- check_views.py --check on s72 passes; placeholder_check.py passes; hai-studio tests 70 passed.
- checks/run.py --target s72 fails its generated check: it expects delivery/requirements/ pages from type_requirements.py, which s72 never had (s72 is built by build_type_pages.py). The folder was absent before this trace; not changed here.
- No server code changed; no restart.

## Summary

s72 has no Delivery or Instances view; each instance's face carries its Checklist against the type, shown in the side pane's Checklist. Group types list nothing by a guessed name; Task tabs stay inside the Block.

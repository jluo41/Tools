---
title: quickhtml view
date: 2026-11-27 15:20
work: [s72, s11]
aim: "A Block Job UI Preview's Effect view is named QuickHtml, on the type (s72) and on its instances; on the type its left tabs read 〈quick page 1〉, 〈quick page 2〉, one such tab per proposal on an instance."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1520_quickhtml_view.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/ (elements.md, build_type_pages.py, studio-views.json, delivery/)
    what: "Effect becomes QuickHtml; its left tabs on the type read 〈quick page 1〉, 〈quick page 2〉 (one tab alone is drawn full width, with no tab); delivery/effect.html becomes quickhtml.html"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/studio-views.json
    what: rebuilt, its Effect view named QuickHtml
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1520_quickhtml_view.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/ (elements.md, build_type_pages.py, studio-views.json, delivery/quickhtml.html; effect.html deleted)
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/studio-views.json
---

# quickhtml view

## Prompts

- **15:15** [Image #58] for effect in the left, we will have <effect> as well, How about we change it to the be QuickHtml, in the Top view list?

## Check

- 5623's b17 Studio, read from the served page (Chrome extension disconnected): s72 and s11 both read Page-Job, Page-Task, Job types, Task types, QuickHtml, Draw, Delivery (s72 then Instances). s72's QuickHtml left tabs: 〈quick page 1〉, 〈quick page 2〉; s11's: Overview · interactive, Task states, Overview · top views.
- Only this type and its instances are renamed; a Studio topic without a studio-views.json still gets the shared renderer's "Effect" name.
- build_type_pages.py --check: files current; the instance gaps now read QuickHtml (s12, s13, s14 have none).

## Summary

The Effect view is QuickHtml on s72 and its instances; the type's left tabs are 〈quick page〉 placeholders.

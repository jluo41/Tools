---
title: s72 type by name
date: 2026-11-27 23:16
work: [s72, s11, s12, s13, s14, s15]
aim: "s72 and its instances s11 to s15 name their Studio Type by name (check_type: block-job-ui-preview), and their built pages are rebuilt after tonight's shared changes (Example fold open, the Pattern tree's style)."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2316_s72_type_by_name.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/build_type_pages.py
    what: "the two places that write check_type write the name block-job-ui-preview"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/ (studio-views.json, delivery/*.html)
    what: rebuilt by the builder
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/ (s11 to s15: studio-views.json, delivery/check.html, delivery/types/)
    what: rebuilt by the builder
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2316_s72_type_by_name.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s72-studio-type-block-job-ui-preview/ (build_type_pages.py, studio-views.json, delivery/*.html)
  - examples/Project-Ladder/blueprint/b17_theme_work/ (s11 to s15: studio-views.json, delivery/check.html, delivery/types/)
---

# s72 type by name

## Prompts

- **23:16** go
- **23:34** go

## Check

- build_type_pages.py: Built 66 files; --check: no stale file, the six known gaps only (s12 QuickHtml, Draw; s13, s14 QuickHtml; s15 QuickHtml, Draw).
- hai-studio/scripts/checks/run.py --target b17: every line for s11 to s15 and s72 is PASS (19 lines).
- All six studio-views.json read "check_type": "block-job-ui-preview"; the kept copy hai-studio/gallery/block-job-ui-preview/elements.md equals s72/elements.md.
- Read from 5623's served pages, not looked at in a browser (the Chrome extension is disconnected). No server code changed.
- 23:34: the comment beside TYPE in build_type_pages.py says hai-studio/gallery (the types folder was renamed); --check PASS, checks/run.py exit 0.

## Summary

s72 and s11 to s15 name their type by name, and their built pages are current again.

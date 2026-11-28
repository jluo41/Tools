---
title: preview mark
date: 2026-11-26 11:10
work: [s11, j11t01]
aim: "A live view in a UI preview outlines the part it is about: the page reads a mark parameter (class names) and draws those elements in a red outline, scrolled into view; s11's Topic rows marks the Job rows."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1110_preview_mark.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.js
    what: a mark=<class>[,<class>] parameter outlines those elements in red and scrolls the first into view
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
    what: Topic rows opens with mark=jobs-rows
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/block-job-ui-preview/TYPE.md
    what: a live view names the part it is about with mark=
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1110_preview_mark.md
  - plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.js
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.html
  - plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/block-job-ui-preview/TYPE.md
---

# preview mark

## Prompts

- **11:08** [Image #16] when we see this, for the topic rows, could you right highlight the related elements? o you get it?

## Check

- 5623, b01_example_work's Jobs with mark=jobs-rows: one element marked (.jobs-rows, the Job topic row and the Job buttons), outline rgb(224, 49, 49), seen in Chrome; without mark nothing changes.
- focus.js parses; workbench tests as before (the reader's known 6 fail).
- No restart: focus.js is read when a page is built, and the page cache rebuilds a page whose files changed.

## Summary

A live view can name the part it is about: mark=<class> outlines it in red in the browser; s11's Topic rows now opens with the Job rows outlined.

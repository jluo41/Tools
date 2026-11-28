---
title: 'Studio page: closed topics no longer load their frames, so the page stops jumping back'
date: 2026-11-27 22:02
aim: A frame loads only when every fold around it is open. Closed topics load nothing, so no hidden frame pulls the Studio page back while the reader scrolls.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2202_studio_page_scroll_jumps.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
  what: load a frame only inside open folds (test_studio_bands.py)
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2202_studio_page_scroll_jumps.md
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/studio_tabs.py
- plugins/haipipe-toolkit/servers/workbench/studio/tabs/tests/test_studio_bands.py
---

# Studio page: closed topics no longer load their frames, so the page stops jumping back

## Prompts

- **22:02** I cannot scroll down?

## Check

- headless Chrome on the served Studio page: 0 frames loaded with all topics closed (423 before the reader opens anything), scroll set to 900 stays for 8 s; s71 opened loads 1 frame and scroll stays; Studio tests 36 pass

## Summary

A Studio frame loads only when every fold around it is open; the page no longer jumps back.


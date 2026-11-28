---
title: metro full width
date: 2026-11-25 17:45
topic: s31-files-pane
aim: "The metro map keeps its full width (all 40 traces) and scrolls left and right; the page's max-width on images no longer squeezes it to the strip's width."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1745_metro_full_width.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
    what: the map's svg keeps its own width (max-width none)
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1745_metro_full_width.md
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
---

# metro full width

## Prompts

- **17:45** do we just have these? I cannot scroll to the right.
- **17:49** yes, gplease go ahead and do it. How can you scroll to right? and how could I scroll in and out, to have different level of the details

## Check

- 5623 b17 Files: the map is 962 px wide in a 152 px strip; it opens at the newest end (scrollLeft 810 of 810);
  › is off there, ‹ moves it back (to 722).

## Summary

The page's max-width on svg squeezed the map to the strip; the map keeps its own width now and scrolls.

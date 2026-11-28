---
title: metro zoom
date: 2026-11-25 17:49
topic: s31-files-pane
aim: "The metro map zooms between three levels of detail: by day (one column a day), by trace (one column a trace, as now) and close (wider columns with each trace's name); minus and plus buttons, or Ctrl or Cmd with the wheel or a pinch over the map."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1749_metro_zoom.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
    what: three zoom levels; minus and plus in the top row; Ctrl or Cmd with the wheel, or a pinch, over the map
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
    what: the zoom buttons are there
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1749_metro_zoom.md
  - plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  - plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
---

# metro zoom

## Prompts

- **17:49** How can you scroll to right? and how could I scroll in and out, to have different level of the details, do you understand what I mean?
- **17:52** yes, please do it. I think we should have a skill named /haitrace for this, what is your thoughts? ANd go ahead

## Check

- 5623 b17 Files: − gives one column for 11-25 (by day) and turns itself off; + twice gives close up, 1930 px
  wide, each column 'HH:MM name'; − back gives 44 columns at 984 px. workbench tests: 240 passed.

## Summary

The metro zooms by day, by trace and close up, with − and + or Ctrl/Cmd and the wheel; a day column zooms into that day.

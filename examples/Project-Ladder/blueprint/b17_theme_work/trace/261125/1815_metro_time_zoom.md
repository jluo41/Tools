---
title: metro time zoom
date: 2026-11-25 18:15
topic: s31-files-pane
aim: The metro zooms through five levels, by day, by hour, by half hour, by trace and close up; a bucket merges the traces that fall in it, and a click on it zooms one level in, centred on it.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1815_metro_time_zoom.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  what: five zoom levels; hour and half-hour buckets; a bucket click zooms in on it
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
  what: the zoom data carries each trace's day and time for the buckets
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1815_metro_time_zoom.md
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
- plugins/haipipe-toolkit/servers/workbench/tests/test_trace_view.py
---

# metro time zoom

## Prompts

- **18:15** okay, how do you think we can also zoom by hours, half hours, if we want.
- **18:19** yes, yes, pleasego ahead and do it

## Check

- 5623 b17 Files: − to the end gives by day (1 column, 11-25); + gives by hour (7: 10:00 … 18:00), by half hour (11: 10:30 … 18:00), by trace (55), close up (time and name); a click on 17:00 zooms into half hours around it.
- workbench tests: 242 passed.

## Summary

The metro zooms through five levels: by day, by hour, by half hour, by trace and close up; a bucket merges its traces' stations (strongest state) and a click on it zooms one level in around it.


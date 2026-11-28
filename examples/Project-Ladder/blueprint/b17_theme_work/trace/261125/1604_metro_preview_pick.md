---
title: metro preview pick
date: 2026-11-25 16:04
topic: s31-files-pane
aim: s31's Metro map preview carries the row effects (+ to create, sweep, strike, dashed), picks a trace by a click (no dropdown) and has a button to show or hide the metro.
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1604_metro_preview_pick.md
    what: this trace's own record
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/delivery/ui/files-metro-lr.html
    what: effects merged; click to pick, no dropdown; metro toggle
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261125/1604_metro_preview_pick.md
  - examples/Project-Ladder/blueprint/b17_theme_work/s31-files-pane/delivery/ui/files-metro-lr.html
---

# metro preview pick

## Prompts

- **16:16** how could we merge the effects of this to [the Metro map] as well? for example, there is a new trace in the plan mode, then we can see the related files will be changed
- **16:20** I don't thinks we need this, we can just clikc and select, we can drop [the dropdown] and keep [the aim]; we might also have an icon to hide or show the metro map
- **16:04** you can update this direclty.
- **16:24** maybe a btter icon? this is too complicated. (the metro toggle is now one line with one station)

## Check

- s31 Studio › Page › Metro map: no dropdown; a click on 1418_trace_timeline.md lights its four files; the metro icon hides
  and shows the map; the sample plan (15:58) shows + rows, a struck row and dashed underlines.

## Summary

The Metro map preview now carries the row effects and picks a trace by a click; the 15:58 plan and its files are samples.

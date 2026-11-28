---
title: Fix round one's speed problems
date: 2026-11-26 10:21
aim: The Block UI left-tab freeze is gone and the first Files panel no longer re-asks git or parses traces slowly.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1021_pane_speed_round_two.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/focus_ui.py
  what: tab sync installs once, skips Elements
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
  what: libyaml, git without submodules, 10 s git cache
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t03_pane_speed/scripts/bench_pane.py
  what: wait past the 10 s cache
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t03_pane_speed/runs/run-check-pane-speed/passes/p02-1126/pass.md
  what: round two
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1021_pane_speed_round_two.md
- plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/focus_ui.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
- examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t03_pane_speed/scripts/bench_pane.py
- examples/Project-Ladder/blueprint/b17_theme_work/j12_side_pane/t03_pane_speed/runs/run-check-pane-speed/passes/p02-1126/pass.md
---

# Fix round one's speed problems

## Prompts

- **10:21** go

## Check

- Chrome: Block UI › Work Block › Findings tab click 39 ms, longest stall 0.38 s, one preview loads (was a freeze of minutes)
- workbench tests 310 passed, the 6 old draft-reader failures
- bench under load 35-54: dirty() gone from the slowest five; numbers not comparable, rerun when quiet

## Summary

The freeze is fixed; the panel's git and YAML costs are cut; a quiet rerun is owed.


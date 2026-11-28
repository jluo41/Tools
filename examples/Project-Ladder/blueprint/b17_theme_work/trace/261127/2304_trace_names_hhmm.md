---
title: trace names hhmm
date: 2026-11-27 23:04
topic: s32-trace-section
aim: Every trace file is named HHMM_slug.md, so the Files pane and the checks see it; a name without the time is reported by trace.py check.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2304_trace_names_hhmm.md
  what: this trace's own record, written first
- do: move
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/ (folder_existing_only, knowledge_s05_s15_s55, organization_by_block_type, structure_folder_organization, structure_studios, studio_bands_by_block_type, studio_type_scope)
  what: each gets its HHMM_ prefix
- do: move
  path: examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/ (5 files)
  what: each gets its HHMM_ prefix
- do: move
  path: examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/ (2 files)
  what: each gets its HHMM_ prefix
- do: edit
  path: plugins/haipipe-toolkit/skills/0_utils/hai-trace/scripts/trace.py
  what: check reports a trace file with no HHMM_ prefix
- do: edit
  path: plugins/haipipe-toolkit/skills/ (workbench-work, workbench-design, workbench-insight ref/topics.md)
  what: links to the renamed traces
changed:
- examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/2304_trace_names_hhmm.md
- plugins/haipipe-toolkit/skills/0_utils/hai-trace/scripts/trace.py
---

# trace names hhmm

## Prompts

- **23:04** in the trace, why we have these with HHMM? remove them or fix them.

## Check

- 14 trace files had no HHMM_ prefix (7 in b17, 5 in b11, 2 in b12); each is renamed HHMM_slug.md and its date line carries the time; none had a time written inside, so the time is the file's creation time, and two b17 files (knowledge_s05_s15_s55, studio_type_scope) got 22:50, the time a later sweep rewrote them
- Links to them updated in 23 files; find shows 0 trace files without the prefix
- trace.py check now reports such a file: a probe file zz_probe.md was reported, then removed; hai-trace tests pass

## Summary

The seven traces shown without a time were written by hand, not by trace.py, so they had no HHMM_ prefix and neither the Files pane nor the checks saw them. All 14 such files across b17, b11 and b12 now carry the prefix, and trace.py check reports any new one.


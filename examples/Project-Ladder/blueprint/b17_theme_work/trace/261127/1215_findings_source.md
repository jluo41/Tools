---
title: findings source
date: 2026-11-27 12:15
work: [s11, j11t02]
aim: "A finding names the raw file(s) it was made from (run.yaml finds: from:) and, if it wants, how it was made (how:); Findings shows each raw file under the finding with its open dot and a mark (✅ the finding is newer than its raw file, ❗ the raw file changed after it or is gone), and the steps in a 'How this table is made' fold, as the paper theme does. A fold with one finding shows it full width, no left tab."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1215_findings_source.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/run_finds.py
    what: "finds: reads from: and how:; each finding draws its raw files with marks and its steps; one finding takes the full width"
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_findings_by_type.py
    what: "from: draws the raw file with ✅, ❗ when the raw file is newer or gone; how: draws the steps; one finding has no left tab"
  - do: edit
    path: plugins/haipipe-toolkit/skills/1_base/project/hai-run/ref/receipts-and-inventory.md
    what: "the finds: section names from: and how:"
  - do: add
    path: examples/Project-Ladder/work/b01_example_work/j11_core_checks/t01_schema_check/runs/run-check-02-name/result/example.csv
    what: the example raw file the schema check passed
  - do: edit
    path: examples/Project-Ladder/work/b01_example_work/j11_core_checks/t02_value_ranges/runs/run-build-01-name/run.yaml
    what: "its finding names from: the example raw file and how: three steps"
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
    what: its Decision notes say a finding links back to its raw file
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1215_findings_source.md
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/run_finds.py
  - plugins/haipipe-toolkit/servers/workbench/page/job_task_views/tests/test_findings_by_type.py
  - plugins/haipipe-toolkit/skills/1_base/project/hai-run/ref/receipts-and-inventory.md
  - examples/Project-Ladder/work/b01_example_work/j11_core_checks/t01_schema_check/runs/run-check-02-name/result/example.csv
  - examples/Project-Ladder/work/b01_example_work/j11_core_checks/t02_value_ranges/runs/run-build-01-name/run.yaml
  - examples/Project-Ladder/blueprint/b17_theme_work/s11-work-job-preview/s11-work-job-preview.md
---

# findings source

## Prompts

- **12:08** go ahead and do them.

## Check

- 5623's j11 page (200, no traceback): under t02's Values table, example.csv with ✅ (hover: ranges.csv was made after example.csv last changed), its open dot opens the raw file (200), and "How this table is made" holds three steps.
- Values and Displays (one finding each) are full width, no left tab; Reports (two) keeps its left tabs.
- Tests: the findings tests cover ✅, ❗ when the raw file is newer, ❗ when it is gone, the steps, and full width; workbench page, side_pane, studio, home 240 passed, 1 skipped.
- folder_icons_check.py: only the 3 known problems from the b10 merge traces.
- 5623 and 5602 restarted, both 200. Chrome would not load the page for this check, so it was read from the served HTML.

## Summary

A finding names its raw files (from:) and its steps (how:); Findings shows each raw file with its open dot and ✅ or ❗, and the steps in a fold. One finding takes the full width.

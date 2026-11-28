---
title: run placeholder names
date: 2026-11-26 12:10
work: [s11, j11t02]
aim: "The example Block's Runs and rounds carry placeholder names as its Task groups and Tasks do: a Run is run-<type>-NN-name (its number inside its Task, oldest first), a round's heading is Round NN name; what a round asked and found stays, since Findings shows it."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1210_run_placeholder_names.md
    what: this trace's own record, written first
  - do: edit
    path: examples/Project-Ladder/work/b01_example_work/ (every Task's runs/)
    what: the 13 Run folders renamed to run-<type>-NN-name, their run.yaml run, target and ticket, their ticket file and heading; the 14 pass headings to Round NN name
  - do: edit
    path: examples/Project-Ladder/work/b01_example_work/j11_core_checks/t01_schema_check/t01_schema_check.md
    what: its close line names the new Run
  - do: edit
    path: examples/Project-Ladder/work/b01_example_work/trace/ (3 traces)
    what: the Run names they mention
  - do: edit
    path: examples/Project-Ladder/blueprint/b17_theme_work/ (traces 1135, 1142, 1145, 1153; s99-guide-view/delivery/ui/guide.html)
    what: the Run names they mention
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/1210_run_placeholder_names.md
  - examples/Project-Ladder/work/b01_example_work/ (13 Run folders, their run.yaml and tickets, 14 pass headings)
  - examples/Project-Ladder/work/b01_example_work/j11_core_checks/t01_schema_check/t01_schema_check.md
  - examples/Project-Ladder/work/b01_example_work/trace/ (1015_html_report_first_page, 1430_schema_second_round, 1600_value_ranges_start)
  - examples/Project-Ladder/blueprint/b17_theme_work/ (traces 1135, 1142, 1145, 1153; s99-guide-view/delivery/ui/guide.html)
---

# run placeholder names

## Prompts

- **12:08** yes, please go ahead and do it.

## Check

- Runs numbered inside their Task by their first round, oldest first: t01_schema_check holds run-check-01-name (was the earlier check) and run-check-02-name; every other Task one run-<type>-01-name.
- A round keeps its Ask and Summary (Findings shows them); only its heading is Round NN name.
- 5623's j11 page: the Run bars read run-check-02-name and so on, the rounds Round 01 name and Round 02 name; no old Run name left on it; the Run page opens (200, no traceback).
- No old example Run name left under examples/ or servers/ (rg); the matches left are b17's own Runs and a test fixture.
- Tests: workbench page, side_pane, studio, home 210 passed, 1 skipped.
- folder_icons_check.py: only the 3 known problems from the b10 merge traces.

## Summary

The example Block's Runs read run-<type>-NN-name and its rounds Round NN name, as its Tasks read Task NN name.

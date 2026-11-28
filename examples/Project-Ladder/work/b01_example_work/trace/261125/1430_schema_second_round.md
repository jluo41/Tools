---
title: schema second round
date: 2026-11-25 14:30
work: [j11, j11t01]
aim: "The column check's second round: one column reads as text in two rows."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/work/b01_example_work/j11_core_checks/t01_schema_check/runs/run-check-02-name/passes/p02-1125/
    what: the second round's pass
changed:
  - examples/Project-Ladder/work/b01_example_work/j11_core_checks/t01_schema_check/runs/run-check-02-name/passes/p02-1125/
---

# schema second round

## Check

- The check ran on the example file; one column failed in two rows.

## Summary

The date column reads as text in two rows; whether to keep it as text or fix the file waits on the reader.

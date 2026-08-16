# Q — Across the ten page-type contracts under `board/page-types/`, how many times does each one name a path that a page of that type actually owns on disk? Report one row per contract with the count and the contract's own line count, so a length explanation can be ruled in or out.
- state:   answered
- started: 2026-08-07T18:11
- by:      A01_measure_paths/measure_artifact_paths.py

## Answer

```text
  contract    paths  lines
  ----------  -----  -----
  design          5    100
  display        10    105
  literature      5     96
  meeting         0     74
  section         4     99
  skill           0    307
  slide           1    119
  stage           2    368
  value           1     91
  venue           2    381

```

10 contracts · 30 artifact-path mentions total · 2 name none at all

Counted terms: `float.tex`, `preview.`, `assets/`, `candidates/`, `QA-probe/`, `sections/`, `.bib`, `.cls`, `.bst`.

RE-MEASURED 260807 after the contracts changed. The first run the same morning returned 6 mentions with 7 contracts naming none, which is what `QB6` §7 was opened on. Every contract then gained a block stating its own input and output, and re-running this instrument is what shows the change was real rather than asserted.

The two still at zero are `meeting` and `skill`, correctly rather than owed: neither produces a paper artifact, so neither has one of the counted paths to name.

The `lines` column kills the obvious rival explanation. When the count was low, `venue` was the longest contract at 363 lines and named zero while `design` was among the shortest at 85 and named three, so length never predicted it. What predicted it was whether the contract's author had a folder open.

One limit travels with this: it counts MENTIONS, not correctness. A contract naming a path wrongly still counts as naming one.

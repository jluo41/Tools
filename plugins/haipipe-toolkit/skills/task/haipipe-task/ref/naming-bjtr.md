# Naming rules for block · job · task · run

Every rule below came from a break this repo actually hit, and every one is
checked mechanically by `ref/check_task_tree.py` (this skill's copy; a project may mirror it under `tasks/_tools/`).

## The pattern

```
<letter><NN>_<STAGE>_<kind>_<subject>[_<what varies>]

b03  CD  visit_pain                                   the study
j01  C   data_table   visit_pain                      the stage's job
t01  C   data         VisitLBP_1stPair                the cohort
r01  C   data         VisitLBP_1stPair   2015_2020    the run
```

## N1 · Every name must stand alone

A name is not read only in its folder. A job name goes into a scheduler queue, a
task name into `results/<task>/<run>/` and every log line, a run name into error
text and `runtime.yaml`. So each must be readable with no path around it.

⛔ `j01_C_data_table` — data table of what?
✅ `j01_C_data_table_visit_pain`

**Repetition with the parent is the PRICE of standing alone, and it is worth
paying.** The old tree already knew this: `C01_data_pipeline_opioid`, not
`C01_data_pipeline`.

## N2 · Carry the stage letter at every level

`b03_CD` · `j01_C` · `t01_C` · `r01_C`. A reader who sees only the run name still
knows which stage produced it.

## N3 · Use the project's own vocabulary, never a nicer synonym

✅ `lbp` `musc` `osteo` `ami` `VisitLBP_1stPair`
⛔ `lowbackpain` `musculoskeletal` `heartattack`

Every config, ticket, store asset and board page already says `VisitLBP`.
Renaming it to something more readable only adds a translation layer. Where a
task publishes a store asset, the task IS named for that asset.

## N4 · Order is numeric, never alphabetical

`1_ols 2_iv 3_did 4_ols_windows`, taken from the project's own sequence. Sorted
by name, `did` would come first, which is meaningless.

## N5 · A shape word alone is not a name

`data`, `table`, `pipeline`, `analysis`, `pool`, `rank` may FOLLOW a noun; they
may never replace one.

## N6 · Siblings must be unique across the whole block

`t01_VisitLBP_1stPair` existed in both the C job and the D job. One rename map
then hit both, and 175 regression configs were silently repointed at the data
table task. Two tasks in one block never share a name.

## N7 · A ticket and its config share one stem

`r01_D_reg_VisitLBP_1stPair_agre_af7d_ols.ps1` ↔ `...same....do`. Anything else
makes the pair impossible to check.

## N8 · A name a script must know is FOUND, not spelled

Deriving `asset` from a folder name broke twice, the moment the folder gained a
prefix. The runner now globs `config/` for the one non-`rNN` file instead. A
script must never rebuild a name it can look up.

## N9 · Never restate the tree in a file

A file that lists every ticket only repeats what `t*/runs/` already says, and then
must be kept in step with it. The guard such a file needs is the proof it should
not exist: the tree IS the list.

⛔ `sbatch/all.ps1` listing 175 `Invoke-Run` lines, plus a count check to catch drift
✅ `run_slice.ps1` with no filter runs everything; `-WhatIf` prints the plan from disk

The same test applies anywhere: if keeping a file honest means re-deriving what is
already on disk, delete the file and derive it at the moment of use.

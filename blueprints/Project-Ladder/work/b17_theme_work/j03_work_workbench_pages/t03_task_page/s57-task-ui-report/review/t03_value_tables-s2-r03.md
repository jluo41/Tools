# Task page, value-tables kind (t03_value_tables) · stage 2 · round 3 · 261106

```text
page     http://127.0.0.1:5623/_board/workbench?layout=focus&path=blueprints/Project-Ladder/work/b90_example_paper_results/j02_example_estimates/t03_value_tables (Report and Work: MindMap, Status; Run pop-outs)
answers  what: t03_value_tables, Aim "Copy the returned values unchanged, then arrange them into the Values tabs the Block's Findings shows." · where: full path ✅ · here: Status, bar 1 "2 tabs, 2 tables, 52 raw cells" with "done", bar 2 · 🔢 Values "all current" ✅ · do: open Values; nothing waits ✅
rules    1 ✅ · 2 ✅ · 3 ✅ · 4 ✅ the Block's Values part on its own page · 5 ✅ Number column now as returned (2.3461, 0.0021, 41.27) · table ✅ Report and Work Status drawn by one function
tasks    see the two Values tabs: 1 click (2 for the subgroup) · check the values were copied unchanged: 1 click, full precision matches the source; "current" still not "unchanged" · where the values came from: 2 clicks (Values, How this table is made), 3 to the source Run's pop-out ✅
walk     25 steps (20 builder, 5 mine) · 22 ✅ · 0 ❌ · 3 ⚠️ (at 390 with Values open every cell repeats its column label under a header row that already names it, Status sits off-screen, and the whole panel scrolls sideways, cutting the Source Runs link; in the r02 pop-out the Values table's "As printed" column is cut at the box edge at 1440); console clean
bar      the Values part matches the paper value Job and the Block's Findings, provenance linked, pop-out drawn as Values tabs; short of it: the phone table regressed (r02 fit 390 cleanly)
rubrics  Glance 9 · Place 9 · Lean 8 · Words 8 · One job 8 · Same look 9 · Phone 6 · Salience 8 · Works 8 · Modern 8 · Plain 8 · Complete 8
score    mean 8.1/10 · not yet: Phone 6 (r02 7.9)
landed   r02 fix 1 ✅ numbers as returned, ❌ "current" kept · fix 2 ✅ Source Runs and pop-out reads link to the Run · fix 3 ✅ pop-out tables.json drawn as Values tabs, ✅ pop-out file tabs are side tabs
fixes    1. Remove the vt-rows cell labels (td::before) and the visible-overflow rule inside a side-tab panel at 600 px or less, so the Values table keeps one header and scrolls in its own box like t01_example_main's.
         2. Move the pop-out's Values table into its own scroll box so "As printed" is never cut.
         3. Rename "current" to "unchanged" if it means the cell equals its source.
complete goal, headline, both tabs (title, line, table, status per value), Run states, Source Runs (linked): shown · tables.json (drawn), copied values.csv, SOURCE.txt: one click (pop-outs) · face state, task-type: one click (Markdown only) · scripts/tables.yaml: missing
questions Does "current" mean the cell equals its source? If so "unchanged" matches the Aim. Does the phone regression also hit the Block's Findings 🔢 Values (same part)?
```

# Task page, value-tables kind (t03_value_tables) · stage 2 · round 2 · 261106

```text
page     http://127.0.0.1:5623/_board/workbench?layout=focus&path=blueprints/Project-Ladder/work/b90_example_paper_results/j02_example_estimates/t03_value_tables (Report and Work: MindMap, Status; Run pop-outs)
answers  what: t03_value_tables, Aim "Copy the returned values unchanged, then arrange them into the Values tabs the Block's Findings shows." · where: full path ✅ · here: Status, bar 1 "2 tabs, 2 tables, 52 raw cells" with "done", bar 2 · 🔢 Values "all current" ✅ · do: open Values; nothing waits ✅
rules    1 ✅ · 2 ✅ · 3 ✅ · 4 ✅ the Values tabs this Task builds show on its own page, the Block's part · 5 ❌ the caption says "as it returned them" over a Number column that rounds (0.0021 shows 0.002, 41.27 shows 41.3) · table ✅ Report and Work Status drawn by one function
tasks    see the two Values tabs: 1 click (2 for the subgroup) · check the values were copied unchanged: 1 click to "current" on every row, but the rounded Number column hides it and the copied files sit in r01's pop-out · where the values came from: 2 clicks (Values, How this table is made), then dead end (Source Runs is plain text)
walk     25 steps (20 builder, 5 mine) · 22 ✅ · 0 ❌ · 3 ⚠️ (opened MindMap leaves clipped at the box edge; pop-out tables.json still a raw JSON wall; Source Runs and pop-out reads not links); phone with all open fits 390, no sideways scroll; console clean
bar      the 🔢 Values part now matches the paper value Job and the Block's Findings (side tabs, line, table, a status word per value); short of it: rounded numbers under an "as returned" caption, provenance in plain text, the pop-out still raw
rubrics  Glance 9 · Place 9 · Lean 8 · Words 7 · One job 8 · Same look 9 · Phone 8 · Salience 8 · Works 6 · Modern 8 · Plain 8 · Complete 7
score    mean 7.9/10 · not yet (r01 6.4)
landed   r01 fix 1 ✅ Values side tabs under the headline, one function · fix 2 ❌ pop-out tables.json still raw JSON, ❌ pop-out file tabs still on top · fix 3 ❌ reads and Source Runs still plain text, ✅ Values bar has a state word ("all current")
fixes    1. Rename the Values Number cells to the value as returned (2.3461, 0.0021, 41.27), or name the rounding in the column head; rename "current" to "unchanged" if it means the cell equals its source.
         2. Make Source Runs under "How this table is made" and the pop-out's reads links to that Run's pop-out.
         3. Rename the pop-out's tables.json tab to draw the Values side tabs instead of raw JSON, and make the pop-out's file tabs side tabs.
complete goal: shown · headline, both tabs (title, line, story, table, status per value), Run states: shown · full-precision numbers: one click (pop-out CSV), rounded on the page · tables.json: one click, raw · copied values.csv, SOURCE.txt: one click (r01 pop-out) · Source Runs: shown, not a link · face state, task-type, Content sentence: one click (Markdown only) · scripts/tables.yaml: missing
questions Does a value's "current" mean it equals its source cell? If so, "unchanged" matches the Aim. The build worker still writes 12480.0 in main.csv (the copy holds 12480): the placeholder breaks its own "unchanged" goal, a worker fix, not a page fix.
```

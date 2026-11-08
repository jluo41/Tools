# Task page, value-tables kind (t03_value_tables) · stage 2 · round 1 · 261106

```text
page     http://127.0.0.1:5623/_board/workbench?layout=focus&path=blueprints/Project-Ladder/work/b90_example_paper_results/j02_example_estimates/t03_value_tables (Report and Work: MindMap, Status; Run pop-outs)
answers  what: t03_value_tables, Aim "Copy the returned values unchanged, then arrange them into the Values tabs the Block's Findings shows." · where: full path ✅ · here: opens on Work · Status, two Run cards "done", no values (partly) · do: open a Run (partly)
rules    1 ✅ · 2 ✅ · 3 ✅ · 4 ❌ the Values tabs this Task exists to build show nowhere on its page; tables.json opens as a raw JSON wall · 5 ✅ · table ❌ Report Status (rows with headlines) and Work Results (cards without) are drawn by different code
tasks    see the two Values tabs it built: could not; 3 clicks reach raw JSON (Status, r02, tables.json) · check the values were copied unchanged: 5 clicks across two pop-outs, nothing side by side; main.csv prints sample.n_units as 12480.0 where the copied file holds 12480 · where the values came from: 2 clicks, then dead end (two reads paths in plain text)
walk     18 steps (12 builder, 6 mine) · 14 ✅ · 0 ❌ · 4 ⚠️ (opened map: the r02 leaf runs past the box at 1440, clipped at 390; tables.json raw; reads not links; 12480.0 against 12480)
bar      paper's value Job and this Block's own Findings draw the same tables.json as 🔢 Values side tabs (tab title, line, table, a status word per value); here it is monospace text
rubrics  Glance 8 · Place 9 · Lean 8 · Words 8 · One job 7 · Same look 6 · Phone 7 · Salience 3 · Works 4 · Modern 5 · Plain 8 · Complete 4
score    mean 6.4/10 · not yet
fixes    1. Move the newest Run's tables.json into Status as 2 · 🔢 Values, drawn with the Block Findings' Values side tabs, under 1 · 📌 headline large; one function for Report and Work.
         2. Rename the pop-out's tables.json tab to draw those side tabs instead of raw JSON, and make the pop-out's file tabs side tabs.
         3. Make each reads path a link to its Run's pop-out, and give the Values section a state word read from the copied and built cells ("unchanged" or what differs).
complete goal: shown · face state, task-type, Content sentence: missing · Run status: shown · says: one click (Open all) · headlines: shown in Report, one click in Work · tables.json tabs (title, line, story, tables): one click, raw JSON only · main.csv, subgroup.csv, copied values.csv, SOURCE.txt: one click · reads, writes, skill, ticket: one click · scripts/tables.yaml: missing
questions Should a value Task draw its Values on its own page (fix 1), or only on the Block's Findings it feeds? The 12480.0 comes from the build worker's output, not the page: the placeholder breaks its own "unchanged" goal.
```

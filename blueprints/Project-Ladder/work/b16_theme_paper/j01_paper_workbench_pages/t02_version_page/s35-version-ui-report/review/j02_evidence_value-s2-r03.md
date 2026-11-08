# Value Job page (Report and Work) · stage 2 · round 3 · 261106

A fresh reviewer looked at the live placeholder value Job (Paper-Example's j02_evidence_value) and followed the haipipe-ui Review steps as written. This is the last round, after the round 2 fixes and a new walk.

```text
page     http://127.0.0.1:5623/_board/workbench?layout=focus&path=blueprints/Project-Ladder/paper/Paper-Example/j02_evidence_value (Report: mindmap, value-list, value-check · Work: work-value-list, work-value-check)
answers  what: j02_evidence_value, goal "values: one Task per group of printed numbers, each read from a returned Result" (structure, partial) · where: path ✅ · here: Report, bars "1 differs" ✅ · do: waiting line "1 printed number to fix: t03_results C2.P1.B2 prints 4.10, its Run returned 4.12" ✅
rules    1 ✅ · 2 ✅ · 3 ✅ · 4 ⚠️ ids stand in for names: "C2.P1.B2", "Never printed: RQ1-t01-009", "from b90 j02 t01 r01 · values.csv · main.b" · 5 ⚠️ Check has two Open buttons, top and bottom
tasks    which printed number differs: 0 clicks (waiting line) · which printed number has no binding: 2 clicks, then a scroll past 10 cards · what to do about the two found values: Work › Check, "Bind the proposed values" → Copy prompt, 2 clicks. Its closed bar says "waits for your tick" but shows no waiting line
walk     21 steps · 21 ✅ · 0 ❌ · my rerun of both pop-outs: 0 console errors · the check pop-out now uses the page's words ✅
bar      Values (side tab plus a table of named rows) reads like the Board's Evidence. Check is still ten five-line cards, a column 1,700 px tall, where the Board uses short rows.
rubrics  Glance 9 · Place 9 · Lean 8 · Words 7 · One job 8 · Same look 8 · Phone 7 · Salience 8 · Works 8 · Modern 6 · Plain 7 · Complete 8
score    mean 7.8/10 · not yet (Modern 6)
fixes    1. Move Check's cards into short rows (value name · printed · its Run · state word), problems first. Put printed in, bound by and note behind a click. Keep one Open.
         2. Add the waiting line under Work › Check's closed "Bind the proposed values" bar ("2 found values wait for your tick: mean <outcome> before and after <the policy>").
         3. Rename "RQ1-t01-009" to its value's name and "C2.P1.B2" to a place in words, with the id in hover. Remove the "b90 j02 t01 r01 · … · main.b" line. At 390 px let the Values panel grow.
landed   r02 1 mostly: rows and cards named ✅, command moved to a Work Copy prompt ✅, two ids still on the page ❌ · r02 2 half: 390 px labels ✅, panel still scrolls inside ❌ · r02 3 yes ✅ (check line gone from Values, tally once, the subgroup row "differs from its Run")
complete value table (value, number, unit, as printed, status) ✅ · how it is made ✅ · numbers to quote ✅ · check cards (state, printed in, printed, its Run, bound by, note) ✅ · no binding and never printed ✅ · face state and close ❌
questions none that would undo a settled decision
```

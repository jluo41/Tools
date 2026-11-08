# Value Job page (Report and Work) · stage 2 · round 2 · 261106

A fresh reviewer on the live placeholder value Job (Paper-Example's j02_evidence_value), following the haipipe-ui Review steps as written, after the round 1 fixes and a new walk.

```text
page     http://127.0.0.1:5623/_board/workbench?layout=focus&path=blueprints/Project-Ladder/paper/Paper-Example/j02_evidence_value (Report: mindmap, value-list, value-check · Work: work-value-list, work-value-check)
answers  what: j02_evidence_value, goal "values: one Task per group of printed numbers, each read from a returned Result" (structure, partial) · where: path ✅ · here: Report, bars "1 differs" ✅ · do: waiting line "1 printed number to fix: t03_results C2.P1.B2 prints 4.10, its Run returned 4.12" ✅
rules    1 ✅ · 2 ✅ · 3 ✅ · 4 ⚠️ raw keys and ids stand for names (sub.b, main.ci_lo, RQ1-t01-009, "V_main_b · b90 j02 t01 r01"); a Note holds a command ("tick, then bind --adopt") · 5 ⚠️ the Values view carries the whole-paper check line too, and its table marks sub.b "✅ current" while the waiting line says it differs
tasks    which printed number differs: 0 clicks (waiting line) · which printed number has no binding: 2 clicks, then scroll past 10 cards · what to do about it: Work › Values, waiting row "RQ1 … 1 differs" → Open, 2 clicks (Interaction still "nothing yet")
walk     20 steps · 20 ✅ · 0 ❌ (my rerun: no console error) · ⚠️ the check pop-out page keeps "1 owed", "2 found", "1 value Tasks", "1 printed numbers" · ⚠️ in Work "Open the check" jumps to Report's Check, "Open j02_evidence_value" reloads itself
bar      Side tab plus table follows the Board's Evidence. Check is now ten six-line cards in a column, longer than the Board's short rows.
rubrics  Glance 9 · Place 9 · Lean 7 · Words 6 · One job 7 · Same look 7 · Phone 6 · Salience 8 · Works 8 · Modern 7 · Plain 6 · Complete 8
score    mean 7.3/10 · not yet (Words, Phone, Plain at 6)
fixes    1. Rename each check card and table row to the value's name ("<outcome> in the <subgroup>: difference"), key in hover; move the command note to a Work Copy prompt.
         2. At 390 px, keep column labels on the stacked Values cells and let the panel grow instead of scrolling inside.
         3. Remove the whole-paper check line from Values (Check owns it), print the tally once in Work · Check, and mark sub.b "printed 4.10, differs" in the table.
landed   r01 1 mostly: plain words and grammar fixed on the page ✅, still printed on both views and in the pop-out's old words ❌ · r01 2 yes ✅ · r01 3 half: no-binding row inline ✅, 390 px labels ❌
complete value table (value, number, unit, as printed, status) ✅ · how it is made ✅ · numbers the text can quote ✅ · check cards (state, printed in, printed, its Run, value, bound by, note) ✅ · no-binding and never-printed ✅ · face state, close ❌ (Markdown only)
questions r01's open: should "1 differs" also show under 🙋 Interaction, or only under Values and Check?
```

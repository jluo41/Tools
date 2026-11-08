# Value Job page (Report and Work) · stage 2 · round 1 · 261106

A fresh reviewer on the live placeholder value Job (Paper-Example's j02_evidence_value), following the haipipe-ui Review steps as written.

```text
page     http://127.0.0.1:5623/_board/workbench?layout=focus&path=blueprints/Project-Ladder/paper/Paper-Example/j02_evidence_value (Report: mindmap, value-list, value-check · Work: work-value-list, work-value-check)
answers  what: j02_evidence_value, goal "values: one Task per group of printed numbers, each read from a returned Result" (partial: it describes structure) · where: path ✅ · here: Report, bars "Values all current" and "Check 6 of 9 match" ✅ · do: no verb until a bar opens; nothing flags the number that differs (partial)
rules    1 ✅ · 2 ✅ · 3 ✅ · 4 ❌ the instruction line "One row per source row. Click a cell for its source."; raw keys (main.ci_lo) and ids (RQ1-t01-006, "V_main_b · b90 j02 t01 r01") stand in for names · 5 ⚠️ "owed", "found" and "binding" are unexplained, and "all current" sits beside "1 differs"
tasks    which printed number differs from its Run: 2 clicks (red "differs", 4.10 vs 4.12) · is the main estimate current, and where is it printed: 2 clicks in Values, plus 2 in Check · which number has no binding: 3 clicks (the row is cut off below the frame, so Pop out is needed) · what to do about the difference: dead end (no waiting line, Interaction says "nothing yet", the Work step says "done")
walk     20 steps · 20 ✅ · 0 ❌ · ⚠️ the Check frame cuts off its last table · ⚠️ at 390 px the Values table stacks its cells without column labels ("12480", "units", "current")
bar      The side tab plus table follows the Board's Evidence shape. The Board's panels are short rows; here the panel is a fixed-height frame with its own scroll. The summary line is printed twice (Work row, table heading) and has grammar slips ("1 value Tasks", "1 numbers").
rubrics  Glance 7 · Place 9 · Lean 6 · Words 6 · One job 7 · Same look 7 · Phone 6 · Salience 7 · Works 7 · Modern 6 · Plain 5 · Complete 8
score    mean 6.8/10 · not yet
fixes    1. Rename the count line to plain words: "1 differs from its Run · 1 waits for its Run · 6 match". Print it once, and fix "1 value Tasks" and "1 numbers".
         2. Move the differing number to a waiting line under the closed Check bar, and stop the Values state saying "all current" while a printed number differs.
         3. Render the check table inline, or size its frame to fit, so the "no binding" row shows; at 390 px, keep each stacked cell's column label.
complete value table (name, number, unit, as printed, status) ✅ · how it is made (fold) ✅ · numbers the text can quote ✅ · check table (where, printed, value, status, source) ✅ · no-binding row one click away (Pop out) · face state and close ❌
questions The Check and Interaction bars start closed (settled 2). Should the "1 differs" also show under Interaction, or only under Check?
```

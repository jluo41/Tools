# Expression Task page · stage 2 · round 2 · 261106

```text
page     http://127.0.0.1:5623/_board/workbench?layout=focus&path=blueprints/Project-Ladder/labeling/b02_labeling_walkthrough/j01_example_response_safety/t04_example_expression (Report: rewrite, run, evaluate, release · Work: the same four · Interactions · Skills)
answers  what: t04_example_expression and its Aim ✅ · where: the full path from Tools ✅ · here: Work › Release, e01 → e02 "released", a green "e02 released" line and closed bars ✅ · do: "4 · 🙋 Interaction 3 wait for you", with "Release Use Choices: Q1 · Serving executor" under it ✅
rules    1 ✅ · 2 ✅ · 3 ✅ · 4 ⚠️ a prompt card sits open under every closed Process bar, even on done steps (Rewrite "done" still offers "rewrite the whole round e02") · 5 ⚠️ the Release button says only "released" while 3 questions wait; the runs table reads "24 · 6" with no unit; the "card" column shows "r08 Q5"
tasks    is the release done: 0 clicks · why the models erred: 2 clicks, "4 errors, all executor limit" over 0 · 0 · 0 · 4 ✅ · what waits on me: 1 click from the default page (open 🙋 Interaction), and the side tabs work · read e01's round report: 1 click (the e01 box)
walk     32 steps · 32 ✅ · 0 ❌ · 0 ⚠️. The frame cap stopped it after Work › Run. My screenshots show Evaluate and Release render, the form returns 200, and there is no console error
bar      Same banded shape as paper, with tiles, criteria rows marked "met" and a labels table. Paper's Process is closed bars only, but here every step adds an open prompt card. At 390 the fold mark sits alone above a long bar title
rubrics  Glance 9 · Place 9 · Lean 7 · Words 8 · One job 8 · Same look 9 · Phone 8 · Salience 8 · Works 9 · Modern 8 · Plain 7 · Complete 9
score    mean 8.3/10 · pass
fixes    1. Move each Process step's prompt card inside its closed step bar.
         2. Make the Release button's state word "released · 3 wait".
         3. Make each "card" cell (r08 Q5) open its question, and add "items" to the runs table's Train and Test.
r01      1 form served ✅ (200, shown inline); 🙋 Interaction is Release's last section, with its waiting line ✅ · 2 state words match ✅ ("4 errors, all executor limit"; e02 "released"; "no fresh check yet") · 3 the e01 box opens e01's round report ✅; "Run this in the Claude session…" ✅ gone from the screen; "signed by Example Person" ✅ now "signed 2026-11-04 21:43"
complete wording changes ✅ · executor runs ✅ · round reports e01 and e02 (1 click) ✅ · errors, performance ✅ · final labels (6 shown, all 1 click) ✅ · criteria ✅ · fresh check ✅ · release choices ✅
questions r01's question is still open: is "released" right while three release-use choices wait, or should Release say "released · 3 wait"? Fix 2 assumes the second.
```

The walk: [task-t04_example_expression.html](../walks/task-t04_example_expression.html)

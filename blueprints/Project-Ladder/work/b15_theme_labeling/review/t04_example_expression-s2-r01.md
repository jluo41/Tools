# Expression Task page · stage 2 · round 1 · 261106

```text
page     http://127.0.0.1:5623/_board/workbench?layout=focus&path=blueprints/Project-Ladder/labeling/b02_labeling_walkthrough/j01_example_response_safety/t04_example_expression (Report: rewrite, run, evaluate, release · Work: the same four · Interactions · Skills)
answers  what: t04_example_expression and its Aim ✅ · where: the full path from Tools ✅ · here: Report › Release, a lock line, the e01 → e02 chain and three closed bars ("30 labels, signed", "all met") ✅ · do: could not; 3 questions wait for the person, and the only sign is a pale rail mark
rules    1 ✅ · 2 ✅ · 3 ✅ · 4 ⚠️ "Run this in the Claude session…"; the lock line repeats on all 4 views · 5 ❌ "4 errors in 4 kinds" over tiles that read 0 · 0 · 0 · 4; the chain says e02 "report sent" while Release says "released"; "Interaction3 wait for you" (glued)
tasks    is the release done: 0 clicks · why the models erred: 2 clicks, but the counts contradict each other · what waits on me: dead end (no view shows it; the Interactions rail opens a 404)
walk     33 steps · 33 ✅ · 0 ❌. Not walked: Interactions and Work › Release's pop-out (frame cap). ❌ (mine): Interactions › Release Use Choices opens "Error response 404"
bar      Same banded shape as the paper Board, with tiles and tables where paper shows them. Paper shows a waiting form as each view's last 🙋 Interaction, with its waiting line under the closed bar. Release shows neither, though 3 questions wait
rubrics  Glance 7 · Place 9 · Lean 7 · Words 6 · One job 7 · Same look 9 · Phone 9 · Salience 8 · Works 4 · Modern 8 · Plain 7 · Complete 6
score    mean 7.3/10 · not yet
fixes    1. Serve this Task's form: labeling_form_view (workbench-task-labeling/labeling.py, about line 4501) returns a 404 for any Task that is not "meaning". Add 🙋 Interaction as Release's last section, with "🙋 Release Use Choices: Q1 · Serving executor" under its closed bar.
         2. Make each state word match its content. "4 errors in 4 kinds" becomes "4 errors, all executor limit". e02 in the chain becomes "released". "a reminder" gets a real state word.
         3. Make the e01 chain box open e01's round report. Remove "Run this in the Claude session…" and "signed by Example Person".
complete wording changes ✅ · executor runs ✅ · round report (1 click) ✅ · errors, performance ✅ · final labels (6 shown, all one click away) ✅ · criteria ✅ · e01 round ❌ · waiting release choices ❌ (missing from the views, 404 on the rail)
questions Release reads "released" while 3 release-use questions wait. Is the release done, or should it say "waiting for you" until they are answered?
```

The walk: [task-t04_example_expression.html](../walks/task-t04_example_expression.html)

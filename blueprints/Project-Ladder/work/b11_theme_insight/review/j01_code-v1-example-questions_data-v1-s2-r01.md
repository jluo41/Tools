# Stage 2 review r01 · j01_code-v1-example-questions_data-v1 (closed first Job)

```text
page     http://127.0.0.1:5623/_board/workbench?layout=focus&path=blueprints/Project-Ladder/insight/Insight-Example/j01_code-v1-example-questions_data-v1 (Report, Work · Overall, Grid, MindMap)
answers  what: folder name, "Overall Report · analysis plan 1 × data freeze 1"; no goal-line (partly) · where: path ✅ · here: Report · Overall, three closed bars with state words ✅ · do: open a bar, switch view; Work's Process rows ✅
rules    1 ❌ no goal-line (the work Job shows "GOAL …") · 2 ✅ · 3 ✅ · 4 ✅ · 5 ⚠️ This Job's keys (plan, freeze) are blue, not links
tasks    what it found in one line: 2 clicks · D02 answered at every cut and checked: 2 clicks; its name opens "No such run." (dead end) · plan, freeze, close date: 3 clicks, the date only in Work
walk     29 steps · 27 ✅ · 2 ❌ (Report and Work Grid pop-out "D01 extract-shape": "No such run.", noted ✅) · 0 ⚠️ · no console errors
bar      thinner than the work Job: no goal-line; Overall's headline is a label, not the finding; its side tabs and figure match paper's
rubrics  Glance 8 · Place 8 · Lean 8 (grey meta line; "moved" twice) · Words 8 · One job 9 · Same look 9 · Phone 7 (opened grid cut at "Fi…") · Salience 7 · Works 4 · Modern 8 · Plain 8 · Complete 8 (missing: question text in the Grid)
score    mean 7.7/10 · not yet
fixes    1. rename the Grid's question link (insight_focus.py:416, run_url on a Task folder) to the answer pop-out (insight-run?answer=) 2. move the Job's goal to a goal-line under the view buttons 3. move X01's one line into the Overall headline
questions bars start closed (decision 2): may the Overall headline carry X01's one line?
```

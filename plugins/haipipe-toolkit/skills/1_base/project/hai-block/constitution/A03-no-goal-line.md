# A03 · No goal-line under the title

> "... <---- we can delete this as well." (JL 261124, on the "Purpose" line of b16_theme_paper)

## 1. Need
The page head is the path, the name and the views; the goal is read in the 🎯 Goal fold, not twice.

## 2. Now
`focus_render.crumbs_goal_source` built `<div class="focus-goal"><span class="goal-word">Purpose</span>…` from the
face's goal for every page; `labeling_focus_frame.task_shell` did the same with "Aim".

## 3. Gap
The goal-line was a named page part (hai-ui "Page parts": goal-line), so every writer filled it.

## 4. Methods
1. Hide by CSS: rejected, the text stays in markup.
2. Remove everywhere: rejected for a draft Task, whose Aim (the reader question) shows nowhere else.
3. Chosen: empty unless the page is a draft Task with an aim.

## 5. Update
- `focus_render.py`: goal_html only for a draft aim
- `labeling_focus_frame.py`: goal_html empty
- tests: `test_focus_faces.py`, `test_focus_runs.py`, labeling `test_decision_view.py`
Suites: workbench 223, paper 111, design 58, labeling 85. Live b16: no `focus-goal`.

## 6. Never again
`test_focus_faces.py` asserts no `focus-goal` on Block and paper Board pages; the Run line reruns it.

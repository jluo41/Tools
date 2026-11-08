# Items Task page · stage 2 · round 1 · 261106

```text
page     http://127.0.0.1:5623/_board/workbench?layout=focus&path=blueprints/Project-Ladder/labeling/b02_labeling_walkthrough/j01_example_response_safety/t01_example_items (older layout, rail sections: goal, runs, data, items, embedding, reports, outputs, studio, timeline, folders)
answers  what: "t01 · Example chats as items" and its goal ✅ · where: only the Job's title "Response safety on synthetic chats", no path from the SPACE (partial) · here: "Goal" with a Next action box ✅ · do: "Continue labeling" ✅
rules    1 ❌ no path, no goal-line, a Runs chip row and "T01 · Items · Your input needed" badges sit up top · 2 ❌ the steps (Data, Items, Embedding) are rail sections, not views; no Skills, Interactions or Delivery on the rail · 3 ✅ · 4 ❌ instruction lines ("Answer Items recipe choices first, then read the recipe below and press Sign", "Confirm the proposal shown above…"); Data is one 3050 px open column · 5 ⚠️ "1 columns", "Studio-All", "Files: not found" beside the file it reads
tasks    do the waiting step: 2 clicks, then a dead end (Answer opens a 404) · see a raw sample: 1 click; Draw again says "Nothing to draw yet." for 600 rows · open r01's record: dead end (a 404)
walk     4 steps · 2 ✅ · 2 ❌ (both pop-outs are logged ✅, but frames 01 and 03 show a 404); Report and Work are not sections here, so both opened Goal. I also found that the Answer button and all 3 Run records return a 404
bar      Nothing of the paper UI's shape is here: no view buttons, no numbered closed bars, no side tabs. Data is a long stack of open tables where paper would show closed bars with side tabs
rubrics  Glance 8 · Place 4 · Lean 4 · Words 6 · One job 5 · Same look 4 · Phone 4 · Salience 6 · Works 3 · Modern 4 · Plain 4 · Complete 5
score    mean 4.8/10 · not yet
fixes    1. Move the Task to the shared layout used by meaning and expression (path, Aim line, Data · Items · Embedding as views with numbered closed bars and state words, Skills/Interactions/Delivery on the rail, section-line on phone). Do not count this twice.
         2. Serve this Task's form and records. labeling_form_view (workbench-task-labeling/labeling.py, about line 4501) returns a 404 for any Task whose kind is not "meaning". The Run chips link to static run.yaml paths, which also return a 404.
         3. Fix the Data step's file lookup ("Files: not found", empty Draw again). Remove the instruction lines and the "Your name" field.
complete Data cards ✅ · recipe ✅ · embedding step ✅ · Studio topic one click away · waiting form ❌ (404) · Run records ❌ (404) · raw samples ❌ · interactions, skills, delivery ❌ (no section)
questions Should Data · Items · Embedding become this Task's view buttons, as Frame · Report · Preferences · Update are on meaning, with Runs, Studio, Timeline and Folders kept on the rail?
```

The walk: [task-t01_example_items.html](../walks/task-t01_example_items.html)

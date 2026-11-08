# Job page, the source Job (Report and Work) · stage 2 · round 2 · 261106

```text
page     http://127.0.0.1:5623/_board/workbench?layout=focus&path=blueprints/Project-Ladder/work/b90_example_paper_results/j01_example_source (Report and Work · MindMap, Status, Findings)
answers  what: j01_example_source and its goal line · where: the path down to j01 · here: MindMap with two Task cards; Status and Findings as numbered closed bars with state words ("1 of 2 done", "1 of 2 returned", "built 2026-11-05", "nothing yet") · do: partly, Open all · Close all and the folds; no verb on a Task row
rules    1 ✅ · 2 ✅ · 3 ✅ · 4 ❌ each empty Delivery tab carries an instruction ("When there is a model it hands over, its clean version goes in delivery/model/, and shows here.") · 5 ❌ the map-card fold mark has no word; "Next steps 1 to do" over a row marked "planned", with no verb. Section table ✅ MindMap · Status · Findings on Report and Work
tasks    how many units came back: 2 clicks (Findings › Headlines, or Status › Tasks) · are the checks run: 2 clicks (Status › Tasks: t02 not started, its Run planned) · see the source map: 2 clicks (Findings › Maps); Enlarge map opens it in the pop-out (r01: could not)
walk     33 steps · 33 ✅ · 0 ❌ · 0 ⚠️; my checks add 0 console errors and 0 failed requests on all six views · ⚠️ the Maps frame is blank in the walk (the map draws about 2 s after the fold opens) and leaves about 300 px blank under the map · ⚠️ after Open all at 390 px the "finds out" leaves sit off the map box's right edge and the box grows tall and empty
bar      Findings now has the paper Evidence shape (numbered bars, side tabs, a map drawn in place); short of it: three empty Delivery tabs of instructions where paper shows nothing it lacks, Status's Task list is rows with ids, the MindMap's Interaction bar has no number
rubrics  Glance 9 · Place 9 · Lean 6 · Words 7 · One job 7 · Same look 8 · Phone 6 · Salience 7 · Works 8 · Modern 7 · Plain 6 · Complete 8
score    mean 7.3/10 · not yet
fixes    1. rename each empty Delivery tab's text to "Nothing handed over yet." (remove the delivery/model/, data/, web/ instructions)
         2. move each "finds out" leaf under its Task card when the leaves do not fit (always at 600 px or less), and fit the map box to the map's height, so Open all hides nothing
         3. move the face's state line ("⏳ IN PROGRESS · the source tables are returned; their checks are planned") onto Status as its main point, and fit the Maps box to its map, drawn as the fold opens
landed   r01 fix 1 ✅ Findings at the Job: each Task's headline as a side tab, 🧠 Maps from t01's result/maps, tables.csv and all_tables.csv as links · fix 2 ✅ t01's headline on its Status row, Status as "1 · 🧱 Tasks 1 of 2 done" and "2 · 🙋 Interaction" · fix 3 ✅ no console 404 (an icon is served), the rail's empty line reads "Nothing asked yet."; r01's ⚠️ also fixed: the map root no longer breaks mid-word, t01's pop-out shows its headline
complete title phrase missing · state line missing · goal shown · Task names shown · Task goals one click (Open all) · Task state shown · Run state and headline one click · tables.csv and all_tables.csv one click · source map one click (Maps) · t02's planned Run one click
questions While nothing is handed over, should Findings drop 📦 Delivery (a section with nothing in it does not show), or keep it as a closed bar reading "nothing yet"? Findings › Headlines repeats Status's Task rows on a Job with no Questions: keep both?
```

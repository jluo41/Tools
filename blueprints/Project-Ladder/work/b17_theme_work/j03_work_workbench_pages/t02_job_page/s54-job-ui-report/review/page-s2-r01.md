# Job page (Report and Work) · stage 2 · round 1 · 261105

A fresh reviewer, the live placeholder work Job (j02_example_estimates); haipipe-ui Review, verbatim.

```text
page     http://127.0.0.1:5602/_board/workbench?layout=focus&path=Tools/blueprints/Project-Ladder/work/b90_example_paper_results/j02_example_estimates (Report and Work · MindMap, Status)
answers  what: j02_example_estimates, "Return the estimates the paper prints…" · where: path from DrFirst-SPACE down to j02 · here: partly answered, Report/Work · Status shows three Task names marked "done" but none of the estimates · do: partly answered, only Open all and Close all, no verbs on the rows
rules    1 ✅ · 2 ✅ · 3 ✅ · 4 ❌ 🙋 Interaction holds an instruction paragraph ("…as a collection Run: runs/rNN_collect_<slug>/ (haipipe-interaction)"); Status caption reads "Where its Jobs, Tasks and sNN stand" · 5 ❌ every Run shows a bare grey ⬜ with no word; the map cards' corner dots have no label; Task goals show only on hover. Section table ❌: the Job has no Findings view, though its Block has one.
tasks    what estimates came back: 3 clicks (fold, Run, pop-out) · is it done: 0 clicks, but the Run marks contradict it · what each Task does: 0 · what needs me: 1 · where the Values tables are: 3, and Job level has no Values
walk     16 steps · 12 ✅ · 1 ❌ · 3 ⚠️ (❌ completed Runs drawn ⬜, "not started", while the pop-out says completed; ⚠️ at 390 px the map is clipped and scrolls inside its box; ⚠️ console 404 "no icon"; ⚠️ the map root breaks mid-word, "j02_example_esti/mates")
bar      below paper's Evidence side tabs: no values and no result lines, only a bare list of names in monospace. Status is a plain "TASKS" list, not the Block's numbered bars
rubrics  Glance 8 · Place 9 · Lean 6 · Words 5 · One job 7 · Same look 6 · Phone 8 · Salience 4 · Works 4 · Modern 5 · Plain 6 · Complete 5
score    mean 6.1/10 · not yet
fixes    1. rename each Run's bare ⬜ to its receipt's state word ("✅ done", from result/runtime.yaml) in Status and MindMap
         2. move each Task's result line (its face's Content or Run headline) onto its Status row, and add the Job's Findings view (🔢 Values from t03's tables.json, then the answers)
         3. remove the Interaction instruction paragraph (keep "Nothing for you here yet"), rename the caption to "Where its Tasks and Runs stand", and show the Job's state line
complete face title phrase missing · state line missing · goal shown · Tasks with one-line names shown · Task state shown · Task state detail missing · Task goal on hover only · Task Content missing · Run headline and values.csv one click away (pop-out) · Run status shown wrong · tables.json missing at Job level
questions On a Job, MindMap (after Open all) and Status draw the same Task-to-Run tree. Dropping either would undo decision 7. Keep both, or should the Job's MindMap show what each Task must find out instead of its Runs?
```

The walk, recorded after this round's fixes (261105), as a short video to pause and step: [job.html](../../../../walks/job.html)
(also under the Block's Report › Job UI › 🎬 The walk).

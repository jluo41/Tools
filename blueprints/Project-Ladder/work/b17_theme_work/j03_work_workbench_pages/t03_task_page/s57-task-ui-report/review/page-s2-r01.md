# Task page (Report and Work) · stage 2 · round 1 · 261105

A fresh reviewer, the live placeholder work Task (t01_example_main); haipipe-ui Review, verbatim. The five step views
are not built yet (they wait for the person's look), so their absence was not scored.

```text
page     http://127.0.0.1:5602/_board/workbench?layout=focus&path=Tools/blueprints/Project-Ladder/work/b90_example_paper_results/j02_example_estimates/t01_example_main (Report and Work: MindMap, Status; Run pop-out r01_example_main)
answers  what: t01_example_main, Aim "Return every value Paper-Example prints" · where: the full path ✅ · here: Report or Work, MindMap or Status, but the content is thin · do: unclear beyond Open all, Close all and folds
rules    1 ✅ · 2 ✅ (left rail has no Runs listed under the page) · 3 ✅ · 4 ❌ the result is not on the page; Interaction shows an instruction with `runs/rNN_collect_<slug>/ (haipipe-interaction)` · 5 ❌ the map leaf is an empty ⬜ with no word, and it says not started while Status says done · table ❌ no Findings view; Report Status is drawn by different code than Work's Results
tasks    main number: 2 clicks from Work, a dead end from Report Status · is it done: 1 click, but the map contradicts it · its values: 3 clicks, one row breaks · what it reads: dead end (a path in plain text, not a link) · needs me: 1 click
walk     16 steps · 8 ✅ · 2 ❌ · 6 ⚠️ (❌ the Run row in Report Status is not a link; ❌ in values.csv a quoted comma splits the main.b row) (⚠️ the ⬜ leaf; the root wraps as "t01_example_mai n"; the caption "Where its Jobs, Tasks and sNN stand."; the Interaction instruction; a favicon 404 in the console; the map cut off at 390 px)
bar      emptier than paper's side tabs: no headline, no values, no picture; the pop-out's file tabs sit on top instead of the side
rubrics  Glance 7 · Place 9 · Lean 6 · Words 6 · One job 6 · Same look 6 · Phone 8 · Salience 3 · Works 4 · Modern 5 · Plain 7 · Complete 5
score    mean 6.0/10 · not yet
fixes    1. Move the Run's headline ("9 values; the main association is 2.35 points…") and the page's state line into Status as section 1, shown large.
         2. Draw Report Status with Work's status-row code, so the Run row opens its pop-out in Report too. Fix the values.csv parsing of quoted commas.
         3. Replace the map leaf's ⬜ with the Run's state word. Change the caption to "Where its Runs stand." Cut the empty Interaction text to one line and number it as the last section.
complete face state, task type, Content sentence: missing · Run status: shown · headline, values, reads, ticket: one click away (Work only) · worker, scripts/: missing
questions At Task level MindMap and Status both show only the one Run. Should the Task's MindMap go (it is settled), or should Findings carry the values?
```

The walk, recorded after this round's fixes (261105), as a short video to pause and step: [task.html](../../../../walks/task.html)
(also under the Block's Report › Task UI › 🎬 The walk).

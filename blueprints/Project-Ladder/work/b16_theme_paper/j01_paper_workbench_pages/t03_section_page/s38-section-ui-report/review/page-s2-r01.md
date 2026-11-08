# Section page (Report, Work, Studio) · stage 2 · round 1 · 261105

A fresh reviewer, the live placeholder Section (Paper-Example's Introduction); haipipe-ui Review, verbatim.

```text
page     http://127.0.0.1:5602/_board/workbench?layout=focus&path=Tools/blueprints/Project-Ladder/paper/Paper-Example/j11_writing_v1130_desk/t01_introduction (Report: MindMap · Text · Status; Work: Plan · Write · Evidence · Revise · Runs; Studio)
answers  what: only partly. The title is t01_introduction and the Aim is a placeholder. · where: the path, yes · here: Report · Text with two paragraphs, yes · do: only partly. Report has just "Go" rows, and in Work the actions sit behind closed "Ask the agent" bars.
rules    1 ✅ · 2 ✅ · 3 ✅ · 4 ❌ the 🙋 Interaction instruction sentence (with "runs/rNN_collect_<slug>/") on every view; Studio's "Run this in the Claude session…" line and two empty-state lines that say the same thing · 5 ✅ · section table ❌ Work has no "4 · Display"
tasks    read the text: 0 clicks · get the next step's prompt: 4 clicks · see the Section's contract: 2 clicks · go to the Display step: dead end at Status "4 · Display · Go" (it opens Plan) · find the Aim's done-when and the cited sources: could not
walk     23 steps · 17 ✅ · 2 ❌ · 4 ⚠️. ❌ the Display Go opens Plan; ❌ on Runs the view buttons run their words together ("1 · Plannext"). ⚠️ 🙋 Interaction is numbered only on Plan and Write; ⚠️ Write and Revise say "No text yet" while Report Text shows text; ⚠️ MindMap is empty; ⚠️ the Revise prompt says "the desk desk". Headless screenshots and HTML only; the console was not read.
bar      The Board numbers 🙋 Interaction and boxes every section. Here, Text uses grey capital-letter labels, Status is a plain table showing each state twice, and no view has a picture.
rubrics  Glance 8 · Place 9 · Lean 6 · Words 7 · One job 6 · Same look 6 · Phone 9 · Salience 5 · Works 4 · Modern 6 · Plain 6 · Complete 5 (shown: Content and the reader question; one click away: the contract fields and the rubric; missing: Aims, state, Opening, sentence ids, the draft/evidence/bibex .bib file)
score    mean 6.4/10 · not yet
fixes    1. Add "4 · Display" to Work's view-button-list (or remove its row from Status), and load the view-button state CSS on the Runs view.
         2. Move the face's Content into MindMap and into the Write and Revise Results, and move Aims (Target · Done when · Now) and the state into Status.
         3. Remove the 🙋 Interaction instruction sentence, Studio's session line and its duplicate empty-state line; number 🙋 Interaction last on every view; drop the second state word on each Status row.
questions Text shows its sections open as headings (the draft rule of 261031), but settled decision 3 starts every section closed. Which rule applies on a Section's Text view?
```

The walk, recorded after this round's fixes (261105), as a short video to pause and step: [task.html](../../../../walks/task.html)
(also under the Block's Report › Task UI › 🎬 The walk).

# Display Job page (Report and Work) · stage 2 · round 2 · 261106

A fresh reviewer on the live placeholder display Job (Paper-Example's j01_evidence_display), following the haipipe-ui Review steps as written, after the round 1 fixes and a new walk.

```text
page     http://127.0.0.1:5623/_board/workbench?layout=focus&path=blueprints/Project-Ladder/paper/Paper-Example/j01_evidence_display (Report: mindmap, display-plan, display-list, display-examples · Work: work-display-plan, work-display-list, work-display-examples)
answers  what: j01_evidence_display, goal "displays: one Task per figure or table, t01-t19 main, t51-t59 appendix" (a rule, not a purpose: partial) · where: path ✅ · here: Report, closed bars with state words ("4 of 4 drawn", "shaping") ✅ · do: no waiting line on any bar, and the open point in Examples ("which example Display C should follow") is not flagged (partial)
rules    1 ✅ · 2 ✅ · 3 ✅ · 4 ⚠️ MindMap cards are folder slugs ("figure1-example"), the run id "r01_draw_figure1" heads the panel · 5 ⚠️ "Open j01_evidence_display" on its own page only reopens it in Work
tasks    is Table 1 drawn: 3 clicks, Displays says done, the Plan picture still says "not drawn yet" · which example should Display C follow: 2 clicks, shown only in red inside the drawing, Interaction "nothing yet" · does the plan follow the venue rules: Plan text unreadable at 1440, Draw pop-out needed (3 clicks)
walk     33 steps · 33 ✅ in the notes · ❌ every Draw pop-out (Report Plan, Report Examples, Work Plan) logs "A bad HTTP response code (404) was received when fetching the script" (/sw.js); errors.txt misses it because it reads the main frame only · ⚠️ Plan picture lists 3 displays (no D) with stale states
bar      Displays (side tabs, PDF in place, Open above it) matches the Board's Evidence tabs. Plan is a small picture where the Board shows rows. The MindMap column is narrower than the other views.
rubrics  Glance 8 · Place 9 · Lean 7 · Words 7 · One job 7 · Same look 8 · Phone 8 · Salience 8 · Works 4 · Modern 7 · Plain 7 · Complete 7
score    mean 7.3/10 · not yet (Works 4: a console error on every Draw)
fixes    1. Remove the /sw.js service-worker registration from the Excalidraw pop-out page (or serve the file), so Draw logs no 404.
         2. Rename the Plan's per-display states to each Task's status: (drawn date) and add Display D, or move the plan to rows (type, section, made by, state) with Draw as the button.
         3. Rename the MindMap cards to each Task's "number · name" with its caption as the finds-out leaf, and widen the map column to the page width.
landed   r01 1 half: "action is not defined" gone, the 404 stays · r01 2 no: Plan still says B and C "not drawn yet" · r01 3 half: "Open t01_figure1-example" now above the PDF ✅, map cards still slugs ❌
complete displays (label, number, type, name, PDF, caption, Run, built date) ✅ · plan rows only as a stale picture ❌ · examples drawing ✅ · Task names in the map ❌ · face state, close one click (Markdown)
questions r01's open: may a view with a single Results section open it (settled 2 keeps it closed)?
```

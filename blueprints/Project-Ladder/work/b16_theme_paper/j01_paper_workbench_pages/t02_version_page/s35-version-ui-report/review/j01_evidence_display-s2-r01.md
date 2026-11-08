# Display Job page (Report and Work) · stage 2 · round 1 · 261106

A fresh reviewer on the live placeholder display Job (Paper-Example's j01_evidence_display), following the haipipe-ui Review steps as written.

```text
page     http://127.0.0.1:5623/_board/workbench?layout=focus&path=blueprints/Project-Ladder/paper/Paper-Example/j01_evidence_display (Report: mindmap, display-plan, display-list, display-examples · Work: work-display-plan, work-display-list, work-display-examples)
answers  what: j01_evidence_display, goal "displays: one Task per figure or table, t01-t19 main, t51-t59 appendix" (a rule, not a purpose: partial) · where: path Tools / … / Paper-Example / j01_evidence_display ✅ · here: Report, the open view's bars with state words ("4 of 4 drawn") ✅ · do: Report shows no verb until a bar opens (partial)
rules    1 ✅ · 2 ✅ · 3 ✅ · 4 ⚠️ the MindMap shows folder slugs ("figure1-example"), and the run id "r01_draw_figure1" heads each panel · 5 ⚠️ "no session named" is a state word nobody can read
tasks    is Table 1 drawn, and what is in it: 3 clicks, but Plan says Display B is "not started" and Displays says "4 of 4 drawn" · venue examples beside ours: 2 clicks · all displays as one PDF: 3 clicks · start planning: Work › Plan, then 2 clicks to Copy prompt
walk     33 steps · 33 ✅ in the notes · ❌ every Draw pop-out (Plan, Examples) throws "action is not defined" plus a 404 on a script fetch (reproduced) · ⚠️ Plan's state for B and C contradicts Displays · ⚠️ "Open t01_figure1-example" is cut off at the bottom of the side-tab panel
bar      The Displays side tabs with the PDF embedded match the Board's Story tabs and are the best part. Plan is a picture whose text is too small to read, while the Board shows rows. The MindMap column is narrower than the other views, so the page jumps when you switch.
rubrics  Glance 8 · Place 9 · Lean 7 · Words 7 · One job 7 · Same look 8 · Phone 8 · Salience 8 · Works 4 · Modern 7 · Plain 7 · Complete 7
score    mean 7.3/10 · not yet (Works 4: a console error on every Draw)
fixes    1. Fix the Draw pop-out's "action is not defined" error and its 404 script fetch.
         2. Have Plan read each display's state from its Task (drawn date), the same source Displays uses, so B and C stop showing "not started".
         3. Rename the MindMap cards to each Task's name (e.g., "<Outcome> by <group>, before and after"), and move "Open t0N_…" above the PDF in the side-tab panel.
complete displays (label, number, type, name, PDF, caption, answers, Run, built date) ✅ · plan table (type, section, where, made by, state) one click away (Work › Open), and only as a picture in Report · examples drawing ✅ · face state, close, reads ❌ (only through "Open this page's Markdown") · Task goals in the map ❌
questions With every section closed (settled 2), the view's one result sits behind a click. May a view with a single Results section open it? Report has MindMap but Work does not (settled 7 lists Plan·Displays·Examples). Is that intended?
```

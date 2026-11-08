# Display Job page (Report and Work) · stage 2 · round 3 · 261106

A fresh reviewer looked at the live placeholder display Job (Paper-Example's j01_evidence_display) and followed the haipipe-ui Review steps as written. This is the last round, after the round 2 fixes and a new walk.

```text
page     http://127.0.0.1:5623/_board/workbench?layout=focus&path=blueprints/Project-Ladder/paper/Paper-Example/j01_evidence_display (Report: mindmap, display-plan, display-list, display-examples · Work: work-display-plan, work-display-list, work-display-examples)
answers  what: j01_evidence_display, goal "displays: one Task per figure or table, t01-t19 main, t51-t59 appendix" (a rule, not a purpose: partial) · where: path ✅ · here: Report, closed bars with state words ("4 of 4 drawn", "shaping") ✅ · do: no waiting line on any bar. The plan's two venue misses and Examples' open question show only in red inside pictures (partial)
rules    1 ✅ · 2 ✅ · 3 ✅ · 4 ⚠️ Plan is a small picture whose text is unreadable at 1440; the Displays panel head is the Run id "r01_draw_table1" · 5 ⚠️ Table 1 has three names: "Example" (tab), "<Patients> at baseline" (Plan), "Display B" (map)
tasks    is Table 1 drawn: 2 clicks, now the same in Plan and Displays ✅ · does the plan follow the venue rules: 3 clicks (open, Draw, zoom). Figure 1 at 900 px and eFigure 1 at 1280 px miss the 2100 the venue needs, yet the bar says "shaping" · which example Display C should follow: 2 clicks, red box in the drawing, Interaction "nothing yet"
walk     33 steps · 33 ✅ · 0 ❌ · my rerun of Draw (Report Plan, Examples, Work Plan) and of the PDF pop-out: 0 console errors, 0 HTTP 4xx · ⚠️ at 390 px the PDF panel scrolls inside and cuts the caption
bar      Displays (side tabs, PDF in place) matches the Board's Evidence. Plan is still a picture where the Board shows rows. MindMap's page is narrower than the other three views.
rubrics  Glance 8 · Place 9 · Lean 8 · Words 7 · One job 8 · Same look 7 · Phone 8 · Salience 7 · Works 8 · Modern 7 · Plain 7 · Complete 8
score    mean 7.7/10 · not yet (mean under 8)
fixes    1. Move the Plan's red venue misses into the bar, as the state word "2 break a venue rule" and a waiting line naming Figure 1 and eFigure 1. Move Examples' open question into its waiting line.
         2. Move the plan out of the picture into rows (display, type, section, made by, venue check), with Draw as the row's button.
         3. Rename Table 1 everywhere to its Task's one name with its drawn date. Rename the panel head "r01_draw_table1 · …" to the display's name. Give MindMap the page width of the other views.
landed   r02 1 yes ✅ (no /sw.js 404) · r02 2 yes ✅ (four displays, each ticked; still a picture) · r02 3 half: three of four map cards named and dated ✅, "Table 1 · Display B · drawn" and the narrow map column ❌
complete displays (label, type, name, PDF, caption, Run, built date) ✅ · plan rows and venue check ✅ (picture only) · examples ✅ · map finds-out leaves ✅ · face state and close ❌
questions none that would undo a settled decision
```

# Submission Job page (Report and Work) · stage 2 · round 3 · 261106

A fresh reviewer looked at the live placeholder submission Job (Paper-Example's j21_submission_v1130_desk) and followed the haipipe-ui Review steps as written. This is the last round, after the round 2 fixes and a new walk.

```text
page     http://127.0.0.1:5623/_board/workbench?layout=focus&path=blueprints/Project-Ladder/paper/Paper-Example/j21_submission_v1130_desk (Report: mindmap, letter, portal · Work: work-letter, work-portal)
answers  what: j21_submission_v1130_desk, goal "everything the portal asks beside the manuscript, ready to review and paste" ✅ · where: path ✅ · here: Report, bars "waits for you" ✅ · do: waiting line "Corresponding author: the portal and the manuscript disagree (…); 7 more for you to decide" ✅
rules    1 ✅ · 2 ✅ · 3 ✅ · 4 ⚠️ the Files tab has "no [[portal.upload]] names this file yet: add it to paper-build.toml, then build" (an instruction with markup in Report), and its word "1 to fix" leaves out its 2 "you decide" · 5 ✅
tasks    which field disagrees: 0 clicks (waiting line names it), 1 click to its row, first tab ✅ · read the cover letter: 2 clicks · is the fill page built: MindMap says "Portal fill · not started", Work says "done" and Delivery lists portal-fill.html. Two answers
walk     26 steps · 26 ✅ · 0 ❌ · my rerun of "Pop out the fill page": 0 console errors · ⚠️ MindMap marks all three Tasks "not started", against Work's "done" and "waits for your sign"
bar      Portal is now side tabs in the workbench look, the disagreeing field first, like the Board's Evidence. The old framed page lives only in the pop-out. MindMap's page is narrower than the other views.
rubrics  Glance 9 · Place 9 · Lean 8 · Words 7 · One job 8 · Same look 8 · Phone 9 · Salience 8 · Works 7 · Modern 8 · Plain 7 · Complete 8
score    mean 8.0/10 · pass
fixes    1. Rename MindMap's "not started" on each card to its Task's real state (Cover letter waits for your sign, Portal walk starter, Portal fill done), read from the source Work reads.
         2. Rename the Files tab's "no [[portal.upload]] … then build" to "no file named yet" and move the how-to into Work's prompt. Rename the tab word to "1 to fix, 2 to decide".
         3. Move the face's state "open · nothing submitted" and its close line onto the page (the MindMap root or Portal's first line). Give MindMap the page width of the other views.
landed   r02 1 yes ✅ (fields in side tabs by group, Authors first, fill page as a pop-out) · r02 2 yes ✅ (waiting line names Corresponding author; the tally appears once per view) · r02 3 mostly: map leaves fold and show whole at 1440 and 390 ✅, portal-fill.html under Delivery ✅, map column still narrow ❌
complete letter text ✅ · portal fields, states, files ✅ · walk and fill states ✅ (Work) · for: j11 ✅ · venue ✅ · Delivery ✅ · face state and close ❌
questions none that would undo a settled decision
```

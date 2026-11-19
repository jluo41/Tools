# Work theme topics

One entry per topic: its name, the words that raised it, the questions it raises, its state.

## T01 · Three linked views: Folder, Element, Session (2026-11-17) · open

From tools-space-bc, relaying JL: "For the theme design, we should have three views. Folder Structure: how things are
stored in the file system. Element Structure: how the UI presents the Folder Structure on the website. Session
Structure: a view that records the important session history; the session keeps recording chat progress to the
history, and shows how each session episode relates to each Folder and Element."

Questions:
1. Which folder kinds does a work Block hold at Block, Job, Task and Run level?
2. Which view and section shows each kind today?
3. Where do work sessions already leave a trace, and in which folder?
4. What in the proposed shape (one shared Session view, episode = one goal, join key = folder path from the Block)
   does not fit the work theme?

Answered to tools-space-bc on 2026-11-17 (map below). No code change yet: the shared part is built once in
`servers/workbench/page` by its owner; the work theme fills its hook after.

```text
level  folder kind                         element today (view · section)
Block  board.md, records/, delivery/,      Overview (Goal, Requirements, MindMap, Work map);
       related/, sNN-<topic>/, runs/,      Delivery; Around the Work: Studio, Interactions,
       src/                                 Timeline, Files; records/ = cards (💬 📝 ✓)
Job    jNN_<job>/ + jNN_<job>.md, runs/,   Plan + Results: a Job row (marks, cards, 🙋 N)
       sNN-<topic>/
Task   tNN_<task>/ + face, scripts/,       Plan + Results: a Task row; Findings tabs
       runs/, draft/ (draft Task)          (Values tables.json, Maps runs/*/result/maps/)
Run    runs/rNN_<slug>/ run.yaml, result/, Plan + Results: a Run row; its pop-out (result,
       passes/pNN-<MMDD>/, ticket .html    card, ticket, passes); collect Run = 🙋 card
```

Session traces today: `passes/pNN-<MMDD>/pass.md` in a Run (`run.yaml` `passes:` and `source: chat`) or a Studio
topic; `Session:` chips on face cards (`## Plan + Results` items); `records/<stem>-comments.md` cards; git commits
(Timeline). None names the session that wrote it, and a Block or Job face keeps no episode list.

Contract merged by tools-space-bc: `servers/workbench/ref/three-views.md` (card addresses, several folders per
episode, collect Run passes read as episodes, page words). Still owed: a guard (test) once the shared Session view lands and the work hook fills it.

## T02 · A Run receipt said ok on 1% of the data (2026-11-18) · fixed

Report from Proj-PD2D: "PD2D b03 r06 (CaseSet v2) died after 1 of 100 partitions and left no result, but the queued
b10 r08 r09 and b11 r06 r07 ran next, each wrote status ok, so their Deliverables would tick ✅ with test AUROC 0.7735
trained on 913 cases instead of about 90,000." Cause there: b10 t01 scripts/4_aidata_reachpd2d.py:56 globbed whatever
partitions existed (fixed in PD2D 0c931d7), and the chain kept going after a failed ticket.

Questions:
1. Can a work Deliverable tick ✅ when a Run its maker read never finished? It could: `item_state` checked only the
   maker's own receipt.
2. How does a Run say what it read? Only in words (`goal: ... (r06_prediabvisit_v261116)`); now also `reads:`.

Fix: `servers/workbench-work/work_progress_deliverables.py` `unfinished_upstream` follows `reads:` and rNN_ names in a
goal across the Project, through ok Runs to the one that never finished; such an item shows 🔶. On the real PD2D tree it
flags exactly b10 r08 r09 and b11 r06 r07. Rule: haipipe-run 0.37.0 (Result, evidence, and closure). Guard:
`servers/workbench-work/tests/test_deliverable_upstream.py` (3 tests).

## T03 · Elements as designs in b17 (2026-11-18) · fixed

JL: "should we change the Block UI to Block UI + element, so we have a Element Section at the first, right, and we can
understand what we will need. Because, otherwise, in the Element UI, we still need to group them into the block, Job,
and tasks."

Fix: each UI view of b17 opens with 🧩 Elements, from `ui/<level>-elements.md` (12 Block parts, 6 Job, 6 Task, 5 Run).
Walked on 5694: every Block tab outlines its part on the live b90 page. Guard: `workbench/tests/test_ui_elements.py`.

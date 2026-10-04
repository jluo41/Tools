# How should a Page's logic and structure be drawn?
state: 🟡 DRAFT · written from the 2026-10-03 workbench changes; CHECK pending
content: draft v0.1 · adopted 261003 2204
answers: Q02
answer-status: answered
results-read: 2026-10-03T22:05:20-04:00

## Opening

A Section is drawn twice, left to right: a logic tree the person edits and a Section map generated from the plan, each Bullet a row with room to write and its evidence cards beside it; only the logic tree is editable on the page.

**Where this Page sits:** [Q02 · How should a Section's argument and its place in the paper be drawn, so a person can read, write beside and check each point and its evidence?](../../board.md).

**Why it matters:** A drawing that cannot be written beside, or that silently saves another drawing into its file, stops being the place where the Section's argument is worked out.

## Content

### 1 · Answer

A Section is drawn twice, both read left to right: its logic tree shows why the claim holds and is the person's to edit; its Section map shows where each part sits in the paper and is generated. <!-- realizes: C1.P1.B1 -->
In both, each Bullet is its own row in one column; a Bullet that supports another sits just under it, stepped in, so nothing is drawn to the right of the column. <!-- realizes: C1.P1.B2 -->
Right of the Bullets come a Text column left empty for writing each point's content, and an Evidence column with one card per Evidence Item on its Bullet's row, green once verified, dashed orange while waiting. <!-- realizes: C1.P1.B3 -->
Only one canvas on a page is editable, the logic tree in Draft › RoadMap Draw; the Section map, Guide's methods canvas and the paper map open view only, because two editable canvases share the browser's drawing storage and one can save the other's drawing. <!-- realizes: C1.P1.B4 -->

### 2 · Evidence

The rules and checks are in [draw-logic-tree](../../../../../plugins/haipipe-toolkit/skills/0_utils/draw-logic-tree/SKILL.md) and [excalidraw-section](../../../../../plugins/haipipe-toolkit/skills/display/excalidraw-section/SKILL.md). <!-- realizes: C2.P2.B1 -->
On S-ManSci-Main-Abstract both drawings pass their checks: ten Bullets, nine evidence cards, and the claim's own card under the claim. <!-- realizes: C2.P2.B2 -->
On 2026-10-03 at 20:50 the Abstract's logic drawing was overwritten by Paper's methods canvas, open for editing in Guide at the same time; it was restored from a copy, and Guide's methods canvas now opens view only. <!-- realizes: C2.P2.B3 -->

### 3 · Limits

Only the Abstract has a Draft plan, so the paper map shows the other eighteen Sections as no plan yet. <!-- realizes: C3.P3.B1 -->
A logic drawing edited by hand can drift from its plan; the check finds a missing Bullet or card, but not a reason that no longer fits. <!-- realizes: C3.P3.B2 -->

### 4 · Next

Draw the logic and the Section map for each Section as its plan is written. <!-- realizes: C4.P4.B1 -->
Refresh the evidence cards with `--cards` as items are verified, so the drawings show what still waits. <!-- realizes: C4.P4.B2 -->

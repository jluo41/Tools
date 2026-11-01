s42 · A draft Task on the focus page
====================================

**Stage:** agreed

**For:** a deck, and the focus page (`layout=focus`) of a draft Task (`task-type: draft`), for JL and whoever writes a Section on it

**Delivery type:** ui

**Covers:** where the seven draft steps live on the focus page; how one step shows what you do (its verbs) and what it
made (its result) natively, with no iframe, no fold, no card in a card; where Studio, Delivery and the Runs go; what
Report shows for a draft Task.

**Excluded:** the seven steps themselves and what each writes (s41-task-draft-procedure; haipipe-draft); the base
focus page every level shares (`servers/workbench/focus_page.py`, built by the session "Basic-Design-BJTR-v2"); the
page parts' names (haipipe-ui 0.1.8, "Page parts: one name each").

**Topic:** JL 261031, on `t00_summary`'s focus page: "why I cannot see what we have prepared for the /haipipe-draft?
... we are working on the draft here ourself"; "I should see the outcome as well"; "the studio should be in the right
rail right?"; "could you think about how to desing the UI more carefully by reading all the details?". A first
stopgap (session "Opioid-PDMP-DID") put the old step pages in iframes; this topic designs the page itself.

**Feeds:** s41-task-draft-procedure


Files
-----

```text
s42-draft-task-focus-page/
├── s42-draft-task-focus-page.md        this face
├── result/mock/ui-draft-v1.html        the first mock: four screens, red notes, old to new map
├── result/mock/ui-draft-v2.html        Report and Work: their view-button-lists, every old piece's new view
└── (code) servers/workbench/workbench-task-draft/focus_draft.py, tests/test_focus_draft.py
```


Proposal (v1, 2026-10-31)
-------------------------

Names follow haipipe-ui 0.1.8: path, title-&-section, view-button-list, goal-line, view-caption, content, left-rail,
right-rail.

1. **right-rail:** Report · Work · Studio · Delivery · Timeline · Files. Studio and Delivery leave Work's
   view-button-list; they are sections. Studio reads the Block topics whose face names this Task (draft_steps
   `_studio_topics`) and then the paper's own (s02 story, s04 paper flow); Delivery reads the Board's
   `delivery/<job>/<task>/` lanes (draft_steps `_built`, `delivery_cards`), so neither is empty for a Section.
2. **Work's view-button-list:** 1 · Plan · 2 · Write · 3 · Evidence · 4 · Display · 5 · Revise · Runs, each with its state
   as a word (sign, done, next, pass 2, none called). A bare link opens the step that waits (draft_steps `current`).
3. **goal-line:** Aim, from the face's `reader-question:`.
4. **Every step, one shape:** a waiting row (what waits for you, with its verb: Sign, Accept all, Mark sent), a verbs
   row (your notes, then the step's verb, which copies the prompt with them), the result drawn natively, then the
   step's Runs as rows. The old Operation and Result folds, Input tables and "Copy prompt" boxes go.
5. **1 · Plan:** the plan as paragraphs and points, each paragraph's Scratch note under it; Requirement, Context,
   Examples, Contract and Rubric one line each with Open (a popup). Sign is a new action that writes only the
   `approved:` line; until now JL typed ✅ by hand (🙋 JL's call).
6. **Runs:** at the foot of each step, and all of them in Work › Runs; the old vertical "Disk · Runs" tab goes.
7. **Report:** MindMap (keeps the stopgap's Text, Steps, Delivered branches) · Text (the adopted text, natively, in
   place of the iframe) · Status.
8. **Code home:** a focus hook in `servers/workbench/workbench-task-draft/` (like `task_card` calls `work_card`), with
   only a small marked hook in `focus_page.py`; it replaces `is_draft`, `draft_frame`, `draft_steps_work`,
   `draft_text_html` there. The step results reuse draft_steps' own HTML (`_plan_map`, `_text_and_evidence`,
   `_text_and_cards`), unwrapped from `_fold` and `_step_box`.


Proposal (v2, 2026-10-31): Report and Work
------------------------------------------

JL 261031: "for each page, we have the report, work, and studio, they serve differnet aims ... studio UI we are fixed,
the next one is how to immigrate the previous version to the report and work, where the view-button-list is the most
important ones."

1. **Report (check): MindMap · Text · Review · Status · Questions.** Text, the adopted text as a reader gets it, opens
   first; Review is the latest Revise Review Report (a judgment, so a check); Status lists each step's state word with
   Go; Questions only when the Section has some.
2. **Work (do): 1 · Plan · 2 · Write · 3 · Evidence · 4 · Display · 5 · Revise · Runs.** Each step's result shows once,
   here; the old Audience Report's copy of every step's Result goes. The old Table moves into 1 · Plan.
3. **Studio stays the base Studio, unchanged; Delivery stays on the right-rail;** the face (old Description) is Files.


Decided
-------

s42-D01 · Build v2 on the live page now: Report and Work drawn in place, Studio and Delivery on the right-rail (JL 261031: "I asked you to fix it"; "Just go ahead to update this").
s42-D02 · Under each view, sections; never folds (JL 261031: "under each view, we will have the sections").
s42-D03 · A draft page fills the screen, its rails at the edges (JL 261031: "the margins outside the left and right rails are too large").
s42-D05 · Report › MindMap is the paper content: paragraphs, points, sentences (JL 261031: "the mindmap here should be the paper content").
s42-D06 · Report › Text is sentence by sentence, its evidence, changes and notes on the right, read only (JL 261031: "sentence level, and the tracking, and the evidence etc. left and right panel").
s42-D07 · The review report stays in Work › 5 · Revise; Report is MindMap · Text · Status (JL 261031: "the revise should be in the Work Section").
s42-D08 · Each section of a view folds by its heading, open by default, remembered in the browser (JL 261031: "could they be like collapse as well").
s42-D04 · Built in `workbench-task-draft/focus_draft.py`; `focus_page.py` holds one marked HOOK (`draft_parts`, `draft_branches`).
s42-D09 · Each section's box is its heading bar only; the content follows below, unboxed (JL 261031, relayed: "could we put the box just in the section? and the content below it we should be outside of the box").
s42-D10 · Ask the agent stays only on 1 · Plan, 2 · Write and 5 · Revise; 4 · Display hides when the text calls no Table or Figure (JL 261031, relayed: "I don't think we need this").
s42-D11 · The plan mind map stays inside its own bounded frame and scrolls there (JL 261031, relayed: "why the mindmap here is not embeded? as before"). Recorded: runs/r02_collect_draft_page_chat_decisions.


Open
----

1. Does the Sign button go in (a click writes ✅ on `approved:`), or stays Sign a typed ✅?
2. Studio for a Section: its own topics first, then the paper's (s02, s04), as two groups?

(write here, or mark the drawing in red)

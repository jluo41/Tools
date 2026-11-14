s39 · Section UI: Work
======================

**Tags:** `Task UI`

**Stage:** explore

**For:** a deck, and a Section (a draft Task)'s Work screen on the focus page (`delivery/ui/section-work`), for the people who build the workbench

**Delivery type:** ui

**Covers:** a Section page's Draft view. Work is retired on paper pages (261113), so this cell now records Draft.

**Excluded:** the other eight cells of the 3 × 3 (j01's other sNN); the draft Task page itself (b32-s42:draft @ draft_task_focus_page).

**Topic:** A Section's Work, retired: the Section page is Report alone, and this cell records its Draft view; one cell of the paper's 3 × 3, a Section (a draft Task) × Work (do) (JL 261031: "we have the board, then job of the
paper version, and task of the section draft, I think it should be 3 x 3"). Its drawing is haipipe-studio's five parts,
drawn by `build_s39_section_ui_work.py` through j01's `paper_ui_cells.py`; its Design A is the Draft view as it is live. Names are placeholders: the papers are unpublished, and Tools is public.

**Feeds:** Q01


Files
-----

```text
s39-section-ui-work/
├── s39-section-ui-work.md            this face
├── build_s39_section_ui_work.py      the builder (../../paper_ui_cells.py draws it)
├── s39-section-ui-work.excalidraw    the five parts: Idea · Now · Design · Process · Delivery
├── s39-section-ui-work.png           its card
└── delivery/ui/                     the agreed screen, once agreed
```


Decided
-------

s39-D01 · Superseded 261113: Draft shows no state words on its bars, no 📥 Input and no "Where this step stands" (s39-D03, D11).
The 261101 proposal to regroup each step (Process, then Results) · Superseded 261113: Work and its steps are retired.
s39-D02 · Work is retired on paper pages: a Section page has Report only, views 1 · Draft (opens first), 2 · Plan, 3 · Evidence, 4 · Display; an old Work, Write or Revise link opens Draft (261113). Live: focus_draft_steps.work_views.
s39-D03 · Draft holds five numbered sections, no state word on any bar: 1 · ✍️ Draft Lab, 2 · 📋 Review Report, 3 · 📚 Examples, 4 · 📏 Writing Rubric, 5 · ⚖️ Decisions (261113). Live: focus_draft_steps.step_html.
s39-D04 · Draft Lab is one row per sentence: its reading-position number, its fixed id (S3b) small, its marks after the last word (📊 📚 🖼️ 🕘 📝 ★ 💬 ✓) (261113). Live: draft_step_revise._text_and_cards.
s39-D05 · Section and paragraph headings are rows with their own cards; the text is justified and cards line up with the sentence edges (261113). Live: draft_step_revise._text_and_cards.
s39-D06 · Edit cards list the current one first; a decided card is faded, collapsed and hides its A/B choices; "% same" shows on Edit cards only (261113). Live: draft_step_revise_cards._revise_card.
s39-D07 · A ✓ checked sentence is never changed by a Revise pass or a rescoring (261113). Live: draft_step_revise_notes.checked.
s39-D08 · Review Report holds the score and the rubric table only (261113). Live: draft_step_revise._review_report.
s39-D09 · Writing Rubric holds writing rules only, tabs on the left: This Section (W rules, R rulings), Coauthors, Venue, Plain English and Anti-AI read-only; an add-a-rule row POSTs /_board/draft-rule (261113). Live: draft_rubric.tabs.
s39-D10 · Decisions has tabs This Section (D-threads, then <stem>-decisions.md), Contract, Paper, Venue; you can add on This Section, Paper and Venue (261113). Live: draft_rubric.decision_tabs.
s39-D11 · Not on Draft: Where this step stands, Ask the agent, Input, Runs (261113). Live: focus_draft_steps.step_html.
s39-D12 · Below the content, 📋 Review Content then 🧭 Around the Work; an empty section is hidden, and the band's heading too when all are empty (261113). Live: focus_render.around_work.
s39-D13 · The first section is named "✍️ Draft Lab", not "Sentences" (JL 261113). Live: focus_draft_steps.step_html.
s39-D14 · A view button carries its number and name alone, no state word such as "pass 1" or "done" (261113, § Page words). Live: focus_draft_delivery.parts (words is empty).
s39-D15 · Each Revise card and each 🕘 earlier-wording line carries "by" badges (JL, RA, GG, AI) from its `By:` line, else the people its Why names, and "✓JL" for who decided it (261113). Live: draft_step_revise_cards._by_badges.
s39-D16 · Paragraph headings keep the old index, "C2.P2 · <title>"; the reading-order number is not used on headings (261113). Live: draft_step_revise._text_and_cards (porder is not called).


Open
----

Nothing open.

(write here, or mark the drawing in red)

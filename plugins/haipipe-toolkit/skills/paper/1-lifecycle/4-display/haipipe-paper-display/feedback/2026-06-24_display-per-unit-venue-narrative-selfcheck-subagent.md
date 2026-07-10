---
status: fixed
created: 2026-06-24
context: display stage; want a per-display self-check before the gallery is called done
updated: 2026-06-24
occurrences: 2
fixed_in: "haipipe-paper-display v3.0.0"
---
Going through the displays one by one, the display stage should run a SELF-CHECK on each figure/table, not just inline them. For every display, judge: (a) venue fit, are these figures good for the venue we want to submit to (e.g. JAMA Internal Medicine actually wants a STROBE flow, a Table 1, a main results table, a forest, and is cool on concept/method schematics)?; (b) narrative + minimap fit, does it map to a claim/beat and sit in the right place in the arc?; (c) quality, caption/labels/rendering, no broken assets, no overclaim. Per display the verdict is keep-main | keep-supplement | fix | demote | cut + one sharp reason.

This is the same 拷打-every-unit discipline already used for narrative beats ([[feedback_narrative_points_subagent_review_smallfont]]), now applied to DISPLAY. Do NOT self-grade the figures (the author marking their own homework comes out limp); CALL an independent subagent to judge each display (builder != judge), then apply the fixes it surfaces and reflect the verdicts in the gallery order/grouping (also consistent with the minimap/narrative, see the sibling feedback on display order).

How to apply (display-stage skill revision, haipipe-paper-display): add a Step that, after building/realigning the display units, dispatches one reviewer subagent over ALL units (so it can also judge flow/redundancy), returns per-unit verdict + sharp comment, and gates stage-close on it. Render the per-unit comments somewhere visible (small font in 4-display.tex, like the narrative beat comments).

## Recurrences
- 2026-06-24 (digest, Display-for-Opioid-JAMA): "should we go through the displays one by one, i think you should have the self check yourself, like whether this figures are good for the venue we want to put? Whether it fit the narrative etc, please add this to the /haipipe-paper feedabck and call a subagent to fix it." + "what is the venue requirement for jama original paper?"

Fix: v3.0.0 — CHECK dispatches ONE independent render-review subagent over the whole
compiled set (venue fit + narrative fit + render quality + five-second test), verdict
keep-main | keep-supplement | fix | demote | cut + one sharp reason per display;
verdicts land in the 4-display.md blocks and sync renders them small-font in the
gallery; the stage gate walks on it.

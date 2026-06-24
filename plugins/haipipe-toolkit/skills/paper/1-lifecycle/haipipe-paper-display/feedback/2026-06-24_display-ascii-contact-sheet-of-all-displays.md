---
status: open
created: 2026-06-24
context: display stage, ProjB Paper-Personality2Opioid-MISQ2026
fixed_in: ""
---
"how about you should have /diagram-ascii to preview the figure and tables and ask
the user to add the comments?" + "should this be a preview of all the displays in
the paper?" + "add the ascii diagram to .../0-lifecycle/4-display by using /diagram-ascii"

Standing practice for the display stage: produce an ASCII CONTACT SHEET that
previews EVERY display in the set (not just the ones being built), saved as
`0-lifecycle/4-display/4-display-preview.txt`, generated via /diagram-ascii.

Why: the compiled gallery (4-display.pdf) shows only what is already rendered, and
prose descriptions are hard to react to. A single ASCII contact sheet — one block
per display, narrative order, each with a compact sketch + claim + status + a
`👉 {JL}:` comment slot — lets the user interrogate the WHOLE set at once and add
per-unit comments BEFORE/while units are built. It is the planning/comment surface;
4-display.pdf stays the compiled visual gallery.

How to apply:
- One block per display, in narrative order, numbered `[N/total]`.
- Each block: Fig/Tab N + name + section + claim, a compact ASCII sketch (real
  numbers when available), status (rendered/building/to-build), and a `👉 {JL}:`
  slot.
- Include a to-build (🔴) preview for displays that do not exist yet, so the user
  shapes them before they are rendered.
- Collected `👉 {JL}:` notes are persisted VERBATIM into 4-display.tex as
  `%% {JL}: ...` (the canonical comment home) and then the unit is built to match.
- Re-generate the contact sheet as the set evolves.

FIX (proposed): haipipe-paper-display should, at the display stage, generate and
maintain `0-lifecycle/4-display/4-display-preview.txt` (the all-displays ASCII
contact sheet) as the comment-collection surface, alongside the compiled
4-display.pdf. Add it to the display CHECKLIST.md done-gate. Pairs with the
existing rule that JL comments live in 4-display.tex.

Fix:

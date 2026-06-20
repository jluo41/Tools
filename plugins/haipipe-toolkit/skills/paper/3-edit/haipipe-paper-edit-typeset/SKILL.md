---
name: haipipe-paper-edit-typeset
description: "Fix typesetting defects in a compiled LaTeX draft: widows, orphans, overfull boxes, bad breaks. Topic ⑥ of the 4-edit cycle. Self-contained typeset checks driven by the compiled PDF. STUB — scope defined, checklist to be filled. Trigger: widow orphan, overfull box, fix line breaks, typeset pass, page breaks."
metadata:
  version: "0.0.1"
  status: stub
  stage: 4-edit
  topic: "⑥ typeset"
---

# haipipe-paper-edit-typeset  (stub)

Topic ⑥ of the `4-edit` cycle — the **last** pass, because every earlier edit
moves the type. Self-contained: carries its own check logic, driven by the
compiled PDF and the LaTeX log.

Read `../_shared/` first — especially `comment-protocol.md`. Like every 4-edit
sub-skill it is **comment-first**: Round 1 inserts `%% {CC-typeset-vMMDD}: finding
| suggestion ========>` and changes no text; apply waits for the human
`========> {XX}:` reply.

## Scope

The compiled document reads cleanly: no widows or orphans, no overfull/underfull
boxes, no awkward page or column breaks, figures/tables near their references.

## Intended checks (to be written)

- [ ] No widow line (a paragraph's last line alone atop a page/column).
- [ ] No orphan line (a paragraph's first line alone at the foot).
- [ ] LaTeX log clean of `Overfull \hbox` / `Underfull` warnings past threshold.
- [ ] Figures/tables float near their first `\ref`, not pages away.
- [ ] No bad hyphenation or stretched interword spacing.
- [ ] Section/equation breaks don't strand a heading at a page foot.

## Approach (intended)

Compile with `4-write/paper-compile` and read the PDF + log (`Overfull` /
`Underfull` warnings, widow/orphan) — fix at the **prose** level first (tighten a
sentence to pull a widow back) before reaching for manual break commands. A diff
of before/after PDFs (`haipipe-paper-edit-diffpdf`) confirms nothing else moved.

## Done means

- [ ] No widows/orphans/overfull boxes in the section's pages; ⑥ cell → `done`.

> **Status:** stub. Fill the checklist into `ref/` when topic ⑥ is activated.

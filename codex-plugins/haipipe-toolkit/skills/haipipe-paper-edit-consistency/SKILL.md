---
name: haipipe-paper-edit-consistency
description: "Keep terminology, notation, and \\label/\\ref cross-references consistent across an existing LaTeX draft. Topic ④ of the 4-edit cycle. Self-contained consistency checks. STUB — scope defined, checklist to be filled. Trigger: consistency pass, terminology check, fix cross-references, label integrity."
metadata:
  version: "0.0.1"
  status: stub
  stage: 4-edit
  topic: "④ consistency"
---

# haipipe-paper-edit-consistency  (stub)

Topic ④ of the `4-edit` cycle. Runs **after** content/values/citations, because
it is cross-section by nature. Self-contained: carries its own checks.

Read `../_shared/` first — especially `comment-protocol.md`. Like every 4-edit
sub-skill it is **comment-first**: Round 1 inserts `%% {CC-consist-vMMDD}: finding
| suggestion ========>` and changes no text; apply waits for the human
`========> {XX}:` reply.

## Scope

The paper says one thing one way everywhere: one name per concept, one notation
per symbol, and every `\ref` points at a live `\label`.

## Intended checks (to be written)

- [ ] One term per concept — variants noted during content edits are reconciled.
- [ ] Notation/symbols introduced in Methods are used identically in Results.
- [ ] Every `\ref` / `\eqref` / `\cref` resolves to an existing `\label`.
- [ ] No duplicate `\label` keys; keys follow the `fig:`/`tab:`/`sec:` convention.
- [ ] Abstract and Introduction claims match what Results actually show.
- [ ] Contribution list (Intro/Conclusion) stays aligned across sections.

## Done means

- [ ] No undefined refs / duplicate labels; terminology and notation uniform.
- [ ] The section's ④ cell → `done`.

> **Status:** stub. Fill the checklist into `ref/` when topic ④ is activated.

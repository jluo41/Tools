---
name: haipipe-paper-edit-consistency
description: "Keep terminology, notation, and \\label/\\ref cross-references consistent across an existing LaTeX draft. CHECK-phase whole-paper consistency pass in build-submit. Self-contained consistency checks. STUB — scope defined, checklist to be filled. Trigger: consistency pass, terminology check, fix cross-references, label integrity."
metadata:
  version: "0.0.1"
  status: stub
  stage: build-submit
  topic: consistency
---

# haipipe-paper-edit-consistency  (stub)

CHECK-phase whole-paper consistency pass in the build-submit layer. Runs **after** per-section editing (DRAFT/GATHER/POLISH/CHECK) is complete, because it is cross-section by nature. Self-contained: carries its own checks.

Like every build-submit sub-skill it is **comment-first**: Round 1 inserts `%% {CC-consist-vMMDD}: finding | suggestion ========>` and changes no text; apply waits for the human `========> {XX}:` reply.

## Scope

The paper says one thing one way everywhere: one name per concept, one notation per symbol, and every `\ref` points at a live `\label`.

## Intended checks (to be written)

- [ ] One term per concept — variants noted during content edits are reconciled.
- [ ] Notation/symbols introduced in Methods are used identically in Results.
- [ ] Every `\ref` / `\eqref` / `\cref` resolves to an existing `\label`.
- [ ] No duplicate `\label` keys; keys follow the `fig:`/`tab:`/`sec:` convention.
- [ ] Abstract and Introduction claims match what Results actually show.
- [ ] Contribution list (Intro/Conclusion) stays aligned across sections.

## Done means

- [ ] No undefined refs / duplicate labels; terminology and notation uniform.

> **Status:** stub. Fill the checklist into `ref/` when the consistency pass is activated.

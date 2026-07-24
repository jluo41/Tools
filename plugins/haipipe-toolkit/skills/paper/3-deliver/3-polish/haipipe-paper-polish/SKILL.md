---
name: haipipe-paper-polish
description: "Whole-paper polish pass over a finished LaTeX draft — three passes in order: consistency (terminology, notation, \\label/\\ref integrity), format (venue style: abbreviations, units, headings, reference style), then typeset (widows, orphans, overfull boxes, bad breaks). Runs after per-section editing is complete because each pass is cross-section by nature. Comment-first. Trigger: polish, consistency pass, terminology check, fix cross-references, format pass, venue style, typeset, widow orphan, overfull box, fix line breaks."
metadata:
  version: "0.1.0"
  last_updated: "2026-07-17"
  stage: deliver
  summary: "3-polish worker. One skill, three ordered whole-paper passes (consistency -> format -> typeset). Comment-first like every deliver sub-skill. History: ./CHANGELOG.md."
---

# haipipe-paper-polish

The whole-paper polish pass in the deliver layer. Runs **after** per-section editing (DRAFT/PROBE/REVISE/CHECK) is complete, because every pass here is cross-section by nature. Self-contained: carries its own checks.

**Comment-first** (like every deliver sub-skill): Round 1 inserts `%% {CC-polish-vMMDD}: finding | suggestion ========>` and changes no text; apply waits for the human `========> {XX}:` reply.

Run the three passes **in this order** — later passes assume earlier ones are settled, and typeset must be last because every earlier edit moves the type.

## Pass 1 — Consistency

The paper says one thing one way everywhere: one name per concept, one notation per symbol, every `\ref` points at a live `\label`.

- [ ] One term per concept — variants noted during content edits are reconciled.
- [ ] Notation/symbols introduced in Methods are used identically in Results.
- [ ] Every `\ref` / `\eqref` / `\cref` resolves to an existing `\label`.
- [ ] No duplicate `\label` keys; keys follow the `fig:`/`tab:`/`sec:` convention.
- [ ] Abstract and Introduction claims match what Results actually show.
- [ ] Contribution list (Intro/Conclusion) stays aligned across sections.

Done: no undefined refs / duplicate labels; terminology and notation uniform.

## Pass 2 — Format

Surface conventions follow the target venue: headings, abbreviations, units, numbers, capitalization, reference format.

- [ ] Abbreviations/acronyms spelled out on first use, used consistently after.
- [ ] Number and unit style per venue (e.g. `5\%` vs `5 percent`; SI spacing).
- [ ] Heading case and depth match the venue template.
- [ ] Figure/table caption style and placement per venue.
- [ ] Math formatting conventions (operators, vectors, function names).
- [ ] Reference list style matches the `.bst` / venue requirement.

Done: paper conforms to venue style.

## Pass 3 — Typeset

The compiled document reads cleanly, driven by the compiled PDF and the LaTeX log. Compile with `haipipe-paper-compile` (sibling in `4-ship/`), read the PDF + log, and fix at the **prose** level first (tighten a sentence to pull a widow back) before reaching for manual break commands. Confirm nothing else moved with `haipipe-paper-diffpdf`.

- [ ] No widow line (a paragraph's last line alone atop a page/column).
- [ ] No orphan line (a paragraph's first line alone at the foot).
- [ ] LaTeX log clean of `Overfull \hbox` / `Underfull` warnings past threshold.
- [ ] Figures/tables float near their first `\ref`, not pages away.
- [ ] No bad hyphenation or stretched interword spacing.
- [ ] Section/equation breaks don't strand a heading at a page foot.

Done: no widows/orphans/overfull boxes in the paper's pages.

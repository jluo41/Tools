haipipe-paper-build-scaffold — Changelog
========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [0.2.0] — 2026-07-26 — reframed as THE MANUSCRIPT UPGRADE, and everything it writes is unnumbered

Rewritten against the layout ruled on the design board (face QA6).

- **Reframed.** It used to claim "build a new paper folder", which collided with `haipipe-paper-folder`. It does not create papers; it gives a paper that has reached the Display or section frontier its LaTeX toolchain. A paper that never reaches Display never grows one.
- **Everything it writes is UNNUMBERED** except `2-src/`: `<paper>.tex`, `<paper>.bib`, `sections/`, `appendices/`, `displays/`, `<venue>.cls`/`.bst`.
- **Templates rewritten**, not just the prose: `driver.tex.tpl` (`0-{{PAPER_SLUG}}.tex` to `{{PAPER_SLUG}}.tex`, `\input{0-sections/…}` to `\input{sections/…}`, `\bibliography`), `supplementary.tex.tpl`, `sections-README.md.tpl`, and `compile.sh.tpl` (self-location and clean paths moved to `2-src/compile.sh`, `displays/`, `sections/`, `appendices/`).
- **Step 3 now gates on the delete test**: `conform` block J must pass, and an upgrade that leaves it failing is not done.


## [0.1.1] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.1.0; older entries below keep their original numbers).

## [1.1.0] — 2026-06-05

- renamed from paper-scaffold to haipipe-paper-build-scaffold (haipipe-paper-* name unification).

## [1.0.0] — 2026-06-04

- initial version, grounded in Paper-MapPhyTrait-npjDM2025.

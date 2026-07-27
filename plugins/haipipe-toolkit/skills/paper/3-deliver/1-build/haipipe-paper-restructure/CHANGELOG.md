haipipe-paper-build-restructure — Changelog
===========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [0.2.0] — 2026-07-26 — migrates INTO the ruled layout; the delete test is a third gate

Rewritten against the layout ruled on the design board (face QA6). This skill was migrating papers into the shape the rule now forbids, which made it the most harmful of the four build skills to leave stale.

- **Target inverted.** Was: split into `0-sections/`, relocate assets to `0-displays/`, install `1-compile.sh`. Now: un-number the deliverable, `sections/` + `appendices/`, unitize assets into `displays/<unit>/assets/`, move the build script to `2-src/`.
- **A third non-negotiable gate: the delete test.** Prose parity and compile parity said the migration did no harm; nothing said it achieved anything. Block J of `conform` is now the gate that says the migration actually happened, and its line must be quoted in the report.
- **The mapping table rewritten** with the real starting shape, including the two cases the old table had no row for: renaming a numbered deliverable, and unitizing a flat `Figure/`/`Table/` bucket.
- **Two new execute rules**: leave `0-lifecycle/` alone (it is the board, and `/haipipe-board` owns it), and never create a `STATUS.md`; retiring an existing one is a separate ruling, not a side effect of a folder migration.
- **Repair mode** gains the delete-test remedy and loses the row that told it to move assets into `Figures/`/`Tables/` buckets.
- Preserved the invocation hint under `metadata.argument_hint`, which conforms to
  the current Skill frontmatter schema.


## [0.1.1] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.1.0; older entries below keep their original numbers).

## [1.1.0] — 2026-06-05

- renamed from paper-restructure to haipipe-paper-build-restructure (haipipe-paper-* name unification).

## [1.0.0] — 2026-06-04

- initial version.

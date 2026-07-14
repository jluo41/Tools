haipipe-application-enter — Changelog
=====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [2.1.0] — 2026-07-14

Changed (PROBE LAYER REDESIGN — Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14)
- Probe state on the console is DERIVED from `1-probes/PP*.md` on disk: per question SECTION, its `state:` (`planned | commissioned | answered | read | answered-local | failed`), resolved by `ls`-ing its `target:`. Never a stored status. An OVERDUE `commissioned` section (eta passed, no QA file) surfaces as an open need — and a loud one.
- GET-OR-CREATE scaffolds `1-probes/` instead of the retired `1-probe-plans/README.md` index.

## [1.0.0] — 2026-06-22

- initial version modeled on paper-enter.

## [2.0.0] — 2026-07-06

- rewritten on the paper-enter model: get-or-create, Gate Ledger awareness, paper-aligned maturity ladder (pre-v4 rationale/design/variants/delivery-plan ladder retired), closing-block inheritance (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

haipipe-discovery-review — Changelog
====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [0.4.1] — 2026-09-03

- Route the Review citation aggregate through Outline's Evidence Workspace at
  `outline/evidence/bibex/`.

## [0.4.0] — 2026-09-02

- Own SYNTHESIZE for review article types, route missing evidence back to
  ACQUIRE, and use Evidence for the citation aggregate.

## [0.3.0] — 2026-09-01

- Serve topic-summary, verdict, and landscape article types through the Review
  route; every type writes the root Page.
- Treat summary/verdict/landscape files as optional Task-side synthesis
  records and keep all evidence authority in per-Subject Results.

## [0.2.0] — 2026-09-01

- Review now synthesizes completed Paper Results. Missing evidence is added as
  new one-Subject Runs, and every terminal claim links to a Result Card plus
  exact cite key.


## [0.1.0] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.0.0; older entries below keep their original numbers).

## [1.0.0] — 2026-07-03

### Added
- Created (JL: each type gets its own specialist, now that buckets = types 1:1). Owns the Review type's Execute: judge (prior_art_check / counterevidence -> `verdict.md`) or synthesize (landscape_review / benchmark_landscape -> `landscape.md`); dispatches research-lit / comm-lit-review / academic-researcher.
- Canonical home of the five-rule Review Output Contract (moved from the orchestrator, which keeps a pointer).
- Post-validation patch: return contract to the caller (terminal path + verdict status or cluster/gap counts + NEEDS-VERIFICATION count); one-off mode returns inline, writes no files.

novelty-check — Changelog
=========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [0.2.1] — 2026-09-04

- Move the invocation hint under supported metadata so the skill passes the
  current skill schema validator.

## 0.2.0 — 2026-08-23

- Ported from the updated ARIS reference (a431e28 → 9cbb6aa), localized: the
  anti-hallucination rule for prior-work entries (resolve via 1_search
  arXiv/Semantic-Scholar workers; unresolved → `[UNVERIFIED]`; never fabricate
  ids) and the dossier-file pattern for long reviewer prompts.
- Replaced the stale ARIS trace plumbing (`.aris/traces/`, `save_trace.sh`)
  with the family's own record rule (terminal file + QA digest).
- Preserved the two local improvements ARIS lacks: the `— venues:` filter and
  the per-paper subsection report format.
- The paper family's new Explore page (haipipe-page-for-explore 0.1.0) binds
  this skill's QA output for its ledger novelty cells.

## [0.1.0] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.0.0; older entries below keep their original numbers).

## [1.0.0] — 2026-05-31

- baseline metadata added.

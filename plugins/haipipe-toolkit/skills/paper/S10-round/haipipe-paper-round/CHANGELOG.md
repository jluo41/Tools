haipipe-paper-round — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.

## [0.2.0] — 2026-07-26 — one round, one Board page

- Replaced the retired `1-rounds/` five-file bundle and `latest.md` pointer
  with `0-lifecycle/7-round/S-Round-<n>-<vYYMMDD>.md`.
- Moved discussion, queue, decisions, applied history, and close receipt onto
  the owning S page; routes now use the grouped Board families and stage PROBE.
- Removed the unsupported `argument-hint` frontmatter key.

## [0.1.0] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.0.1; older entries below keep their original numbers).

## 1.0.1 — 2026-07-19

- WIKI RETIREMENT — the retired wiki folder's `07-paper-rounds.md` (5 referrers) absorbed here as the **Rounds contract** section; this skill is now its ONE home, and every referrer points at the section instead of the file.
  - Merged into the existing folder-contract block rather than added beside it: the no-nested-branch-level rule (`good: 1-rounds/v260621/` vs `bad: 1-rounds/<branch>/v260621/`), the file-semantics table, the round lifecycle (open → collect → extract → triage → route → record → close), the triage-targets table, and the dashboard rule (`/haipipe-paper enter` MUST surface open round items; round todos are first-class open needs).
  - The `triage` subcommand no longer restates the target list — it points at the contract's Triage targets table. Its stale `0-lifecycle/2-claims` target is corrected to `0-lifecycle/1b-claims`.
  - `Read first:` drops the wiki entry (the contract is in this file now).
- First CHANGELOG for this skill.

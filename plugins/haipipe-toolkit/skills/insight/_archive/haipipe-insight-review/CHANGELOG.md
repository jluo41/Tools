haipipe-insight-review — Changelog
==================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [2.0.0] — 2026-07-05

- Canonical-ref paths fixed: bare `ref/` → `../ref/` (9 sites; the bare form resolved to a nonexistent haipipe-insight-review/ref/).
- Narrative scope REMOVED (JL: narrative layer retired, "直接都删掉"); a discovery scope added in its place (discoveries/<X>/discovery.yaml + terminal files), closing the description's unimplemented "discover" promise.
- DoD action enum gains `merge` (first-class per review-contract; was missing while the same DoD used it two lines later).
- Audit artifacts corrected to `insights/_reviews/` (INDEX_AUDIT.md was listed at insights/ root; per-layer CARD_REVIEW files now listed too).
- ask-session scope REMOVED (JL: "delete it."): application_ask dropped from commands, Step 1 mapping, Step 3 scan blocks, and the project-scope sweep; scopes are now project | probe | task | discovery.
- Backfill note: the 3.1.0 PRE-ASSIGN IDS block and recut candidate rules landed 2026-06-22 without a version bump.

## [1.1.0] — 2026-06-20

- renamed user-facing flow to review/apply.

## [1.0.0] — 2026-06-20

- initial review/apply contract.

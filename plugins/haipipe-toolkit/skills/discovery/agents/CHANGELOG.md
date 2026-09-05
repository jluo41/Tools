discovery agents — Changelog
============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match the skill frontmatter `version:`. Newest first.

## 2026-09-04 · Page workflow unification

- Preserve `1_search`, `2_review`, and `3_idea` as numbered skill-family
  groups parallel to `haipipe-task`; agents dispatch into them but do not treat
  them as phases.
- Separate D1 SCOPE/PREPARE/ACQUIRE/SYNTHESIZE/CLOSE ownership from the shared
  Page 00–04 workflow and make their handoff explicit.
- Keep one-Subject Discovery Runs under D1 ACQUIRE; Page phases alone own
  Page-family Runs and Page mutations.
- Make ENRICH explicitly enter D1 ACQUIRE, constrain reviewer Bib comparison
  to read-only recomputation, and replace the obsolete lifecycle review with a
  current authority audit.
- Reviewer 1.9.1 drops Write/Edit capabilities so the read-only contract is
  enforced by the agent definition, not only by prose.
- Reviewer 1.9.2 also drops unrestricted Bash; deterministic commands run by
  the owning creator/checker and the reviewer inspects their receipts.

## 2026-09-02 — D1 five-cycle workflow

- Orchestrator 2.5.0, creator 1.14.0, and reviewer 1.8.0 now distinguish
  SCOPE, optional PREPARE, one-Subject ACQUIRE Runs, L3 SYNTHESIZE, and CLOSE.
- Citation/Bib aggregation routes through the Outline Evidence Workspace;
  `haipipe-plugin-evidence` is compatibility-only.

## 2026-09-01 — Explicit BJTR addresses

- Orchestrator 2.4.0, creator 1.13.0, and reviewer 1.7.0 now resolve and audit
  explicit `bNN_` Block, `jNN_` Job, `tNN_` Task Page, and `rNN_` Run segments.
- Manifests and runtime receipts carry both readable and compact global
  addresses; missing letters, missing levels, and bare `01_` names fail review.

## 2026-09-01 — Typed Discovery Page agents

- Orchestrator 2.3.0, creator 1.12.0, and reviewer 1.6.0 now plan and return a
  canonical `discovery_type`, universal root Page, and optional typed record.
- Agent gates enforce the published Phase × Run Map and require runtime
  `family: discovery` plus a Subject-matched analysis operation.

## 2026-09-01 — Topic Page + Paper Run agents

- Orchestrator 2.2.0, creator 1.11.0, reviewer 1.5.0, and search worker 1.2.0
  now enforce Trigger -> canonical Subject -> one numbered Run -> same-stem
  Result, per-Result Bib authority, and derived Topic Evidence Bib.
- ENRICH adds Paper Runs instead of anonymous `sources.md`/`notes.md`
  deltas.


## [1.10.0] — 2026-07-19

- ⑨ TOMBSTONES erased. Owner ruling (JL): "不需要留退役告示,直接抹除任何痕迹" — a doc states the CURRENT contract and never names the dead thing.
  Four 💀 blocks erased across `README.md`, the creator, the reviewer, and the orchestrator; each restated
  positively as "this layer is probe-unaware / nothing under `discoveries/` carries a trace of who asked".
  The reviewer's bank-purity CHECK is kept (executable detection); only its "is DELETED, not optional" gloss went.


## [1.9.0] — 2026-07-19

- Owner ruling, 2026-07-19 (JL): "宪法 don't use this name, just use `probe`." The nickname
  "THE CONSTITUTION" / "the constitution" for `probe/haipipe-probe/SKILL.md` is dropped everywhere;
  each site now names either `probe` or the actual path.
  Touched: `haipipe-discovery-creator-agent.md` QA-file contract pointer and `README.md`.

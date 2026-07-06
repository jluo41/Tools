haipipe-insight-explore — Changelog
===================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [2.0.0] — 2026-07-05

- FULL REWRITE to the recut model (JL skill-set review: "重新写吧"). The 1.0.0 body predated the 3.0.0 recut and scanned fields/shapes that do not exist: `result.status` (real probe.yaml has a top-level `status:`, e.g. `deposited`), a two-level `probes/<GROUP>_<slug>/<NN>_<slug>/` glob (real shape is flat `probes/<MMDD>_<slug>/`), `source_experiment`, "P cards", and confirmed-probe gating (the admission gate 3.0.0 removed); as written it matched zero probes and reported an always-empty KB.
- New model: chain-per-dataset coverage (D profile → I pattern → K with confidence + claim_type → W), unreviewed-settled-material detection, and no admission gates (negative / low-confidence K are first-class).
- `--out` formalized in the argument-hint (the old tail referenced a flag that was never declared).

## [1.0.0] — 2026-05-31

- baseline metadata added.

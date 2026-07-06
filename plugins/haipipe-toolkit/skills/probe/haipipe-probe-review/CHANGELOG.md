haipipe-probe-review — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `probe/CHANGELOG.md`.


## [1.0.0] — 2026-07-06

Added (JL ruling: the reviewer agent may be called by the gateway, but the PROCESS must be governed by a skill — "haipipe-probe-review可以被新的agent call，但是我们还是需要一个skill来规范流程")
- New skill: the G1/G2/G3 judgment rulebook, extracted verbatim-in-substance from haipipe-probe-reviewer-agent 2.1.0 (which becomes a thin shell that invokes this headless and returns the output).
- Instruments migrated here from `../agents/`: `g2_integrity_check.py` (deterministic G2) + `probe-caveats-checklist.txt` (G1 confound checklist) — the skill owns its own docs.
- Direct invocation allowed only with a complete spec (claim + on-disk refs); the normal path is gateway full mode. Light mode never judges.

haipipe-paper-check — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [1.4.0] — 2026-07-03

- Gate Modes section added (JL: copilot 人给 comments / autopilot 派 subagent 给 comments，必须有 approval 动作): mode spec owned by wiki/08-stage-gate.md; autopilot dispatches ONE fresh-context reviewer subagent that leaves > REVIEWER: comments + returns proceed|restart|accept; HUMAN-ONLY items (Scholar bibtex verification) are marked DEFERRED into a human queue, never silently passed; humans can reopen agent-approved gates.
- Stage Exit Invariant added under What Each Decision Does (JL: only check can jump out the current stage): restart re-opens a phase WITHIN the same stage; proceed/accept is the only cross-stage move; cross-stage loopback is a lifecycle re-entry, not a CHECK outcome.

## [1.3.0] — 2026-07-03

- renamed haipipe-paper-checker -> haipipe-paper-check. Phase workers are named by the phase verb (draft/probe/revise/check); agent nouns are reserved for sub-tools (proof-checker stays).

## [1.2.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE); sibling worker names updated; seed check row aligned with the 3-section seed.

## [1.1.0] — 2026-07-03

- reframed as internal worker. Users invoke stage skills (seed, claims, pitch...), not this skill directly. Stage skills call this during their CHECK phase.

## [1.0.0] — 2026-07-02

- created as the general auto-gate. The former checker was actually a proof-checker (mathematical proofs only); renamed to haipipe-paper-proof-checker and kept as one sub-checker.

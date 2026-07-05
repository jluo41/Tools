haipipe-paper-check — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [1.5.2] — 2026-07-05

Changed (JL: 为啥不叫comments — one mechanic, one name)
- "pin" vocabulary dropped throughout: the feature is plain `> CHECK:` comments (comment family: > USER: / > CC: / > REVIEWER: / %% {CC-worker}: / > CHECK:). Report line renamed PINS SEEDED -> CHECK COMMENTS SEEDED. Mechanics unchanged.

## [1.5.1] — 2026-07-05

Fixed (audit of 1.5.0: pin contract landed in the front half, back half still spoke pre-pin language — the sections a fresh session reads as the operational contract)
- On-restart reads pins + replies (unanswered pin = surfaced back, never silently skipped); done criteria gain pin-seeded + pin-replied gates; anti-patterns gain clean-file handover + pin-ignoring; Human Actions entry point = walk the pins (not self-service flag hunting); pin targets include _DISPLAY_; report Summary carries a PINS SEEDED line (count + files).

## [1.5.0] — 2026-07-05

Added (test-123333333: JL entered 0-seed.md for the CHECK pass and found a clean file — flags lived only in the chat report; JL: "check的时候我需要进去仔细看，然后你加comments 之类的，这些你有做吗")
- SEED THE PINS (step 2.5, mode-independent): every flagged/🔍/⚠️ report item is planted as ONE `> CHECK:` comment at its exact spot in the working doc (issue + judgment needed, concrete values). Chat report = map, in-file pins = what the human walks; clean-file handover is DEFECTIVE. Human replies `> USER:` per pin; restart reads pins + replies; resolved pins archive to _LOG per wiki/02. Autopilot reviewer reads the pins too.

## [1.4.1] — 2026-07-04

Fixed
- Seed row PROBE check updated: `_DISCOVERY_ takeaways linked` -> `_PROBE/ plan takeaways backfilled + _CITATION_ candidates eyeballable` (naming unification).

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

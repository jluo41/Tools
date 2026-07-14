haipipe-application-iterate — Changelog
=======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.
## [1.2.2] — 2026-07-14 — probe-redesign residue sweep

Fixed
- **Self-contradiction inside one section.** "Feeding deployment evidence back" opened: "they enter the project through the **evidence gateway**, never through a side door" — while line 89 of the same section says "there is NO probe gateway agent any more (retired 2026-07-14)". The earlier residue sweep fixed the mechanism block and left the topic sentence on the dead noun, so a reader who stopped at the first sentence went looking for a gateway that does not exist and cannot be dispatched. Now: "they enter the project through the PROBE phase — the ONE door".

## [1.2.1] — 2026-07-14

Fixed (LIVE-INSTRUCTION SWEEP — probe redesign, Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3)
- v1.2.0 migrated the frontmatter and the triage table but MISSED the body: "the gateway does the work, the PP card carries the verdict" survived. That single sentence named THREE dead things — the RETIRED probe gateway agent, the RETIRED probe card, and the DELETED `verdict` (R7) — and an agent obeying it would have dispatched an agent that no longer exists.
- Deployment evidence now: the NEED is a question SECTION in `1-probes/PPNN_<topic>.md`; the PROBE phase hands its `commission:` block VERBATIM to `Agent(haipipe-task-orchestrator-agent)` / `Agent(haipipe-discovery-orchestrator-agent)` (their clean context IS the wall); the answer returns as the QA file the section's `target:` points at; the `reading:` says what it means; the claim's STATUS lands in `1-claims.md`.

## [1.2.0] — 2026-07-14

Changed (PROBE LAYER REDESIGN — Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14)
- A/B results bearing on a claim raise a question SECTION in `1-probes/` (`serves: 1-claims`); `probe run` MATCHes the bank first, then commissions. The settled judgment is the CLAIM's status in `1-claims.md` — the probe `## Verdict` and the `verdicted` state are DELETED (R7).

## [1.0.0] — 2026-06-22

- initial version.

## [1.1.0] — 2026-07-06

- re-homed 5-iterate/ -> 4-iterate/; triage targets on the new spine; ask-kind reference removed (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

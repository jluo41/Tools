haipipe-application-review — Changelog
======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [1.1.1] — 2026-07-14

Fixed (LIVE-INSTRUCTION SWEEP — probe redesign, Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3)
- The claim-traceability checklist item required each factual claim to trace to "the PP card that settled it". Probe CARDS are RETIRED (the probe is now a FILE of question SECTIONS), so a reviewer obeying this item was looking for an artifact that no longer gets written.
- It now traces to a supported ledger claim (C##) in `1-claims.md` — the only home of a claim's status — plus the probe SECTION (`PP<NN> § Q<n>`) whose `target:` names the answering QA file in the bank.
- Also fixed this file's ordering: `[1.0.0]` was sitting ABOVE `[1.1.0]`, contradicting the "Newest first" rule in the header.

## [1.1.0] — 2026-07-06

- old-spine paths replaced (3-design/4-variants/2-claims.md); retired verdict word removed (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

## [1.0.0] — 2026-06-22

- initial version.

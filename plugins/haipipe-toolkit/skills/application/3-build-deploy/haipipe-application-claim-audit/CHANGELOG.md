haipipe-application-claim-audit — Changelog
===========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [1.2.1] — 2026-07-14

Fixed (LIVE-INSTRUCTION SWEEP — probe redesign, Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3)
- v1.2.0 migrated the frontmatter but left the AUDIT CHECKLIST — the part an agent actually executes — on the retired model: it asked for "The PP card backing the claim" and scoped statements against "the verdict's scope". Probe cards and `verdict`/`verdicted` are both DELETED (R7), so the audit's two central checks tested for absent artifacts.
- The checklist now verifies: the probe SECTION exists (`PP<NN> § Q<n>`), its `target:` still resolves to a live QA file, the claim's status in `1-claims.md` is current, and the statement stays inside the scope the QA file's `## Caveats` + the 1-claims.md status line support.

## [1.2.0] — 2026-07-14

Changed (PROBE LAYER REDESIGN — Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14)
- The audit now reads `1-probes/PP*.md` — each section's `target:` names the QA file its claim cites — and reads the claim's STATUS from `1-claims.md`, its only home. R7 deleted the probe `## Verdict` block and the `verdicted` state, so there is no verdict in a probe to audit against.

## [1.0.0] — 2026-06-22

- initial version modeled on paper-edit-claim-audit.

## [1.1.0] — 2026-07-06

- ledger path updated to the 1-claims stage folder (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

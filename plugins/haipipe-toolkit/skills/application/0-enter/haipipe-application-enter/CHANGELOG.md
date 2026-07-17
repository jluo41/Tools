haipipe-application-enter — Changelog
=====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [2.3.0] — 2026-07-17

- Insight-KB retired as an evidence layer: dropped `insight` from the delivery-need type enumerations, the `filing insight memory` ask-first item, and `and insights` from the shared-evidence location.

## [1.0.0] — 2026-06-22

- initial version modeled on paper-enter.

## [2.0.0] — 2026-07-06

- rewritten on the paper-enter model: get-or-create, Gate Ledger awareness, paper-aligned maturity ladder (pre-v4 rationale/design/variants/delivery-plan ladder retired), closing-block inheritance (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

## [2.1.0] — 2026-07-09

- BENCH RULINGS (Test-Haipipe-Application, 01_sms_young_male): get-or-create now scaffolds the venue-FREE spine EAGERLY (0-seed + 1a-1d rung folders, each with empty _PROBE/; folders only, no stub .md — progress is judged by doc content). Venue-ALIGNED stages stay absent-until-written.
- New section: legacy pre-ladder layouts (0-lifecycle/1-claims/, no rungs) are flagged as LAYOUT DRIFT and get a confirm-gated one-shot migration offer (rename to 1c-claims/, scaffold missing rungs, re-file probes by shape, fix index rows, consume FORWARD pointers; worked example logged in 01_sms_young_male).

## [2.2.0] — 2026-07-09

- FEEDBACK INBOX item (2026-07-09_surface-releasable-probes, filed by the Testing-Haipipe-App bench: "you should let me know what probes to release"): dashboard gains a dedicated **Releasable Probes** block between Open Needs and Loopback Diagnosis — one row per `status: planned` + deps-met PPNN card (stage, mode, need, deps, exact `probe run PPNN` command) plus a one-line roster summary for dispatched/read/verdicted. Complements the draft worker's end-of-DRAFT release menu (6.3.0): the menu fires at drafting time, this block fires at every console open.

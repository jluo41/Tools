# Application Skill Wiki

Single source of truth for application skill conventions, architecture, and protocols. Numbered to MIRROR the paper wiki (`../../paper/wiki/`) — same number = same concept, application flavor; gaps are concepts that live paper-side only (consult paper's copy) or in the umbrella SKILL.md.

## Index

**Foundations**
0. Evidence Principles — SHARED root doctrine, lives paper-side: `../../paper/wiki/00-evidence-principles.md` (land-at-home, review-on-write, layered orders, trim-ceremony-not-principle)

**System architecture**
3. [Intervention Lifecycle](03-intervention-lifecycle.md) — stage spine, venue gating, maturity ladder, loopback, evidence flow
5. [Intervention Dashboard](05-intervention-dashboard.md) — how to derive the dashboard from disk
6. [Application Skill Structure](06-application-skill-structure.md) — skill folder layout, stage-to-procedure map, router rule

**Operational protocols**
8. [Stage Gate](08-stage-gate.md) — Gate Ledger protocol + venue-scaled gate depth
11. [Delivery Need](11-delivery-need.md) — need record schema + probe interface + backfill

Focus strip + closing block: `../haipipe-application/SKILL.md` Closing Block section (the single source of truth), rendered by `../haipipe-application/stage-strip.sh`. Probe files (`1-probes/PPNN_<topic>.md`) convention: `../haipipe-application/fn/probes.md` (twin of `paper/haipipe-paper/fn/probes.md`). Rounds contract: `../0-enter/haipipe-application-round/SKILL.md`.

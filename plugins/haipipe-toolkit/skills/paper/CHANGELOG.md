paper -- Changelog
====================

Layer-scoped changelog for the paper (DELIVERY) layer. Newest first.
Rollup lives in the plugin-level CHANGELOG.md.


[2.0.0] -- 2026-06-22
-----------------------

Cross-cutting protocol overhaul addressing 22 feedback items from the initial
Paper-Personality-Opioid-MedJournal walkthrough. Four implementation waves.

### Added (new ref docs)

- **ref/stage-gate.md** -- Stage Gate protocol. Every stage transition requires
  explicit user confirmation. Per-stage exit criteria table. Gate Ledger in
  STATUS.md tracks confirmed/date per stage. Strip checkmark means
  user-confirmed, not artifact-exists. Autonomy policy: boundary = PAUSE.
- **ref/stage-illuminate.md** -- Illuminate + Elicit protocol. Socratic
  teach-then-elicit-then-draft loop before every stage draft. Per-stage
  taste-bearing decision examples. Re-walks diff-and-ask, not overwrite.
- **ref/tex-quality.md** -- Lifecycle TeX Quality Standard. Three rules:
  SELF-CONTAINED (standalone compilable), REAL PROSE (not comment blocks),
  SENTENCE-INDEXED (Pn.Sm tags from birth). Compile rule: pdflatex after every
  edit, clean aux, stale PDF is a defect.
- **ref/evidence-routing.md** -- Evidence Routing Protocol. Paper/evidence
  boundary: paper owns story, probe owns evidence. The \\needprobe{} LaTeX
  macro marks claims lacking evidence with a red flag in the compiled PDF.
  Handoff protocol (stop, mark, record, route, backfill). Heavy probes
  dispatch to background subagents. Construction as a first-class Methods beat.

### Changed (stage skills)

- **haipipe-paper-seed v1.1.0** -- added Step 0 Illuminate + Elicit, Compile +
  Exit Gate step, shared protocol cross-references, stage strip in handoff.
- **haipipe-paper-pitch v1.5.0** -- added Title section (first in template),
  multi-hook candidates (>=2, all kept visible, never collapsed), Template
  Enforcement lint, Quality Gate (Step 3b rubric), illuminate+gate+compile
  protocols. Fixed pitch-readability.md: removed "collapse" instruction,
  reworded principle 6.
- **haipipe-paper-claims v1.2.0** -- added Step 0 Illuminate + Elicit with
  venue-coupling taste questions, compile step, stage-gate confirm, stage strip.
  Venue coupling was already in principles/stage-gate from v1.1.0.
- **haipipe-paper-narrative v1.3.0** -- added per-beat subagent interrogation
  protocol (independent reviewer: keep/move/demote/cut + venue-aware comment
  in \\footnotesize). Illuminate + gate + compile protocols.
- **haipipe-paper-display v1.4.0** -- added per-unit subagent interrogation
  in scaffold and audit modes. Illuminate note in plan mode. Gate/compile/confirm
  in handoff. Already routed to production skills (display-figure, -table,
  -diagram, -illustration, task-for-display).
- **haipipe-paper-minimap v1.2.0** -- added illuminate + gate + compile
  protocols, stage strip in handoff.

### Changed (orchestrator + enter)

- **haipipe-paper v2.0.0** -- version bump, cross-reference to
  ref/evidence-routing.md in Delivery Need Routing section. Probe/discover/task
  verbs already existed from v1.4.0-1.5.0.
- **haipipe-paper-enter v2.1.0** -- restructured dashboard output: pitch summary
  first (what the paper is about), then stage strip, then compact operational
  state, then open needs. Stale-deliverable flagging. Structured tail enforced.

### Changed (bootstrap)

- **init_paper_layout.py** -- lifecycle_stage_tex() preamble now includes
  parskip, xcolor, and \\needprobe{} macro. STATUS.md template now includes
  Gate Ledger table and venue field. current_layer uses bare stage name (seed)
  not 0-seed.

### Changed (infrastructure)

- **ref/stage-strip.sh** -- reads Gate Ledger from STATUS.md when present.
  Checkmark = ledger-confirmed (preferred) or before-current (fallback).

### Feedback items resolved (22)

All 22 open feedback items from 2026-06-22 marked fixed:
- Wave 1A (tex quality): lifecycle-tex-self-contained-not-fragments,
  lifecycle-tex-must-use-edit-content-format,
  lifecycle-bootstrap-produced-comment-only-tex
- Wave 1B (session infra): orchestrator-must-enforce-status-tail,
  console-too-dense-want-stage-progress, enter-should-show-what-paper-is-about
- Wave 2 (stage gate): stage-advance-needs-user-confirm,
  stage-strip-in-every-response
- Wave 3 (per-stage quality): every-stage-must-illuminate-and-elicit-taste,
  every-stage-must-compile-readable-pdf
- Wave 4A (pitch): pitch-not-following-hook-surprise-template,
  pitch-skill-no-structure-gate, pitch-template-missing-title-section,
  pitch-hook-needs-multiple-candidate-versions
- Wave 4B (claims+venue): claims-must-couple-to-venue,
  venue-pack-lifecycle-wiring (open design questions parked)
- Wave 4C (evidence routing): paper-evidence-gap-route-to-probe,
  probe-invocation-path-from-paper,
  construction-is-first-class-beat-probe-via-subagent
- Wave 4D (per-unit review): narrative-points-need-subagent-reviewed-inclusion-comments,
  interrogate-every-unit-narrative-beats-and-display-figures,
  figures-tables-must-route-to-production-skills

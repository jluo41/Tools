paper -- Changelog
====================

Layer-scoped changelog for the paper (DELIVERY) layer. Newest first.
Rollup lives in the plugin-level CHANGELOG.md.


[2.3.0] -- 2026-07-21
-----------------------

BINDING: **the display SPLIT**. A display unit has TWO halves with DIFFERENT owners, and the
consumer-side unit is GENERATED from the bank's `source_data.csv`. Hand-typing numbers into a
unit's `.tex` is now a declared DEFECT, not a shortcut.

### Why -- the failure it exists to prevent

Observed on `Paper-Personality2Opioid-MISQ2026` the same day. A ruling flipped §6's primary
exposure from the continuous score to the binary indicator. The prose was updated;
`0-displays/Table/table3-main-results.tex` was NOT, because its numbers were hand-authored and
nothing linked them back to the bank. The table silently contradicted the text it supported, and
only a manual display-lane sweep caught it. A GENERATED unit makes that drift mechanically
detectable; a hand-typed one cannot.

### Changed

- `1-lifecycle/haipipe-paper-stage/stages/4-display/stage.md` -- new BINDING block +
  `display_split: binding`. BANK side (task-folder, stake-free, LAW 1: the executor holds the pen)
  owns `source_data.csv` / `metrics.json` / provenance, produced by the task layer
  (`haipipe-task-for-display`), never by a paper stage. CONSUMER side (`0-displays/<unit>/`,
  stake-aware, venue-bound) owns which rows/columns the argument needs, venue formatting, and
  `\label`/`\ref` wiring.
- `1-lifecycle/haipipe-paper-stage/stages/5-section-edit/stage.md` -- new `display_split:` pointer
  beside `displays: file-only`: a DR row filed from a section names BOTH `bank deliverable:` and
  `consumer deliverable:`; a DR naming only one half is incomplete.
- Router `1-lifecycle/haipipe-paper-stage/SKILL.md` -- Status bumped v0.3.0 -> v0.4.0.

### Note

Structurally a DR row IS the display-flavoured q-executor: the same consumer-to-executor crossing,
the same LAW-1 ownership rule, a different artifact shape. Recorded here so the symmetry is not
rediscovered a third time.


[2.2.0] -- 2026-07-19
-----------------------

The `wiki` folder is RETIRED. The shared-reference folder is gone; each doc moved into the ONE
skill that owns its subject, and every inbound reference now points at that
section. Nothing was duplicated -- a doc with 18 referrers got ONE home and 18
pointers, never 18 copies.

### Moved (doc -> new home, as a titled section)

| Retired doc | New home | Section |
|---|---|---|
| `02-comment-lifecycle.md` (18 refs) | `haipipe-paper/SKILL.md` | Comment lifecycle |
| `11-delivery-need.md` (11 refs) | `haipipe-paper/SKILL.md` | Delivery Need Routing (merged into the existing section) |
| `12-evidence-routing.md` (4 refs) | `haipipe-paper/SKILL.md` | Evidence Routing Protocol |
| `13-tex-quality.md` (8 refs) | `3-deliver/haipipe-paper-deliver/SKILL.md` | Lifecycle TeX Quality Standard |
| `07-paper-rounds.md` (5 refs) | `0-enter/haipipe-paper-round/SKILL.md` | Rounds contract |
| `06-paper-skill-structure.md` (4 refs) | `README.md` | Skill-tree layout · Stage to Procedure · Router Rule · Maturity Rule |
| `05-paper-dashboard.md` (1 ref) | `0-enter/haipipe-paper-enter/SKILL.md` | Dashboard Spec |
| `00-evidence-principles.md` (1 ref) | `1-lifecycle/ref/08-stage-gate.md` | Evidence Principles (总纲) |
| `README.md` (wiki index) | -- | dropped; its one referrer (`ref/03-paper-lifecycle.md`) now describes `1-probes/` directly |

Placement follows ownership, not convenience: the three family-wide conventions
land in the umbrella (which already owned the Closing Block), the tex standard
lands in the group that produces compiled artifacts, the rounds contract and the
dashboard spec land in the skills that ARE those things, and the evidence
principles land in the stage-gate rule that cited them as its general statement.

### Changed

- Binding protocol preserved verbatim where it matters: the `> USER:` / `> CC:`
  comment lifecycle (including the loaded-context rule that every skill still
  INLINES its binding subset) and the dashboard's derive-from-disk behavior spec.
- De-duplicated on absorption rather than pasted twice: delivery-need merged into
  the umbrella's existing Delivery Need Routing section; the dashboard's maturity
  ladder merged into enter's existing evidence→maturity table; the resource
  exemption keeps its single statement in enter's Diagnosis Rules.
- Historical `wiki`-folder paths in CHANGELOG prose reduced to bare doc names so
  no dangling path survives the folder deletion; the reasoning is untouched.
- Citation cruft stripped from every touched passage (`JL ruling C8-i`, `R7`,
  `run-3`, bare ruling dates) while keeping the REASON each rule exists.

### Fixed

- `haipipe-paper/stage-strip.sh` cited the stage-gate doc as a wiki page; the file has lived
  at `1-lifecycle/ref/08-stage-gate.md` for some time. Repointed.
- `ref/03-paper-lifecycle.md` described `1-probes/` as holding the wiki README.
- `haipipe-paper-round` corrected a stale triage target (`0-lifecycle/2-claims`
  -> `0-lifecycle/1b-claims`).
- `README.md` flags `venue/` as a TARGET layout: the folder does not exist on
  disk, so every `venue/playbook-<venue>` citation in the stage skills currently
  resolves to nothing. Pre-existing; recorded, not silently asserted as real.

### Added

- First CHANGELOGs for `haipipe-paper-round` and `haipipe-paper-deliver`.


[2.1.0] -- 2026-07-14
-----------------------

components/ retired (was already half-migrated: figure/ had moved to
1-lifecycle display, edit-diffpdf to 3-build-submit).

### Moved

- **paper-compile** (+ its feedback inbox) -> 3-build-submit/paper-compile.
  Feedback-router bucket renamed components/compile -> paper-compile.

### Removed

- **citation-audit**, **citation-verifier**, **reference-audit-guide** --
  superseded by the citation probe lane (haipipe-paper-probe-citation:
  AUDIT / PLACE / REVIEW verbs; acquisition via the discovery orchestrator).
  All dispatch references rewired (probe-citation, diffpdf, to-overleaf,
  narrative, section-related-work, build-check, 6 _venue playbooks,
  feedback router).
- **paper-diff-folder** -- orphan; no inbound references
  (haipipe-paper-edit-diffpdf covers the diff need).
- **components/README.md** and the components/ container itself; structure
  docs updated (paper README, 04-lifecycle-map.md, 06-paper-skill-structure.md).


[2.0.0] -- 2026-06-22
-----------------------

Cross-cutting protocol overhaul addressing 22 feedback items from the initial
Paper-Personality-Opioid-MedJournal walkthrough. Four implementation waves.

### Added (new ref docs)

- **1-lifecycle/ref/08-stage-gate.md** -- Stage Gate protocol. Every stage transition requires
  explicit user confirmation. Per-stage exit criteria table. Gate Ledger in
  STATUS.md tracks confirmed/date per stage. Strip checkmark means
  user-confirmed, not artifact-exists. Autonomy policy: boundary = PAUSE.
- **1-lifecycle/ref/09-stage-illuminate.md** -- Illuminate + Elicit protocol. Socratic
  teach-then-elicit-then-draft loop before every stage draft. Per-stage
  taste-bearing decision examples. Re-walks diff-and-ask, not overwrite.
- **13-tex-quality.md** -- Lifecycle TeX Quality Standard. Three rules:
  SELF-CONTAINED (standalone compilable), REAL PROSE (not comment blocks),
  SENTENCE-INDEXED (Pn.Sm tags from birth). Compile rule: pdflatex after every
  edit, clean aux, stale PDF is a defect.
- **12-evidence-routing.md** -- Evidence Routing Protocol. Paper/evidence
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
  12-evidence-routing.md in Delivery Need Routing section. Probe/discover/task
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

- **10-stage-strip.sh** -- reads Gate Ledger from STATUS.md when present.
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

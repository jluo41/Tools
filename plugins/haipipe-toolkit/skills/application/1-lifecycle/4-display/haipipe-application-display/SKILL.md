---
name: haipipe-application-display
description: "Stage 4 of the intervention lifecycle (venue-GATED: required for dashboard/ui-card/report, optional for email, skipped for sms/push/reminder/checklist — per STATUS.md stages_skipped). Answers 'what content element carries each claim, and what job does each unit do?' Maps claims to display units (panels, widgets, charts, sections) with per-unit jobs and evidence anchors — the retired minimap stage's concern lives here. Output: 0-lifecycle/4-display/4-display.md + _LOG + _PROBE/. Trigger: display, content elements, panels, widgets, unit jobs, /haipipe-application display."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "4.0.0"
  last_updated: "2026-07-06"
  summary: "Paper-aligned: absorbs minimap (per-unit Job field is now required on every display unit); stage FOLDER paths; gating via STATUS.md stages_skipped; materialization routes through the PROBE worker to /haipipe-task; DPRC phases."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-display
=====================================

Stage 4 of the intervention lifecycle (venue-GATED, venue-ALIGNED). What specific content element carries each claim, and what JOB each unit does for the reader. Same role as paper's display; the retired `minimap` stage's job-assignment concern is folded in per-unit.

Question answered
==================

"What content element carries each claim, and what job does each unit do?"

When this stage fires
======================

Read `STATUS.md | stages_skipped |`: if `display` is listed, this stage is skipped (the venue template already fixes the elements). `optional` venues (email) pull it in on user request.

Input
======

- `0-lifecycle/3-narrative/3-narrative.md` (required if narrative fired)
- `0-lifecycle/1d-principles/1d-principles.md` (always -- elements carry principles)
- `0-lifecycle/1c-claims/1c-claims.md` (always -- the evidence anchor behind each element)
- Venue profile (available display element types)

Output
=======

```
<intervention-root>/0-lifecycle/4-display/4-display.md
<intervention-root>/0-lifecycle/4-display/_LOG_4-display.md
<intervention-root>/0-lifecycle/4-display/_PROBE/       (materialization needs)
```

Display artifact schema (venue-dependent)
==========================================

Canonical template (source of truth for section order + placeholders): `ref/display-template.md`.

> CC: 🆔 id collision needs your ruling — the illustration below names display units `D01/D02`, but `D<n>` now belongs to 1a description ids (ladder restage).
>
>     🆔 id namespaces after the restage
>       1a-descriptions        1b       1c       1d        4-display
>     +-----------------+   +------+ +------+ +------+  +----------------+
>     | 📊 DS<n> dataset |   | 🧩 T |▶| 🧾 C |▶| 🎯 P |  | 🖼️ units:      |
>     | 📈 D<n>  entry   |──▶+------+ +------+ +------+  |  SKILL: D01 ⚡ |
>     +-----------------+                                |  ref/:  U01 ✅ |
>             ▲                                          +----------------+
>             └──────── ⚡ two meanings of "D" ──────────────────┘
>
>     A ✅ rename display units to U<nn> (template already does; 1 schema block to fix; no filled display docs exist yet)
>     B    rename 1a entries instead (e.g. A<n>; re-edits 5 fresh files + SOP; loses the D-rung DIKW echo)
>     C    keep both namespaces (zero cost now, but claim-audit greps D<n> cross-rung and will misfire)
>
> CC: my rec = A. Reply `> USER:` below.

> CC: 🎨 heading-style: the schema blocks below use `#`/`##` while the formatting note + template are ascii — ONE ruling covers seed/pitch/narrative/display; the full options thread lives in `1-lifecycle/0-seed/haipipe-application-seed/SKILL.md` (reply there).

Every unit carries FOUR required fields -- type, claim, JOB, data source. The Job field is the minimap absorption: one sentence on what this unit must make the reader see/do.

**venue-dashboard:**
```markdown
# Display Map: <intervention name>

## Display units

### D01: KPI Card — Refill Rate
- **Type:** metric-card
- **Claim:** C01
- **Job:** show current vs target at a glance; alert color when below
- **Content:** current rate, trend arrow, target
- **Data source:** task T01

### D02: Panel — Timing Analysis
- **Type:** line-chart
- **Claim:** C03
- **Job:** make the timing window visible (rate by hours-before-expiry)
- **Data source:** task T02
```

**venue-report:**
```markdown
### D01: Table 1 — Summary Statistics
- **Claim:** C01, C02
- **Job:** establish the cohort so later effects are credible
- **Content:** cohort descriptives
- **Data source:** task T03

## Probes
<materialization needs, INLINE and visible: one line per PP with status
(unit → task route); cards in _PROBE/>
```

Artifact formatting: `=====` title / `-----` sections (no `#` headings); one sentence per line. Display reads the venue stage doc's Artifact Principles (2-venue.md) for available element types.

Materialization
================

A unit whose data source does not exist yet is an evidence need: buffer a `_PROBE/` card (kind: artifact, route: task) and dispatch via the PROBE worker -- display never runs `/haipipe-task` or computes inline. Rendered outputs land task-side; the unit's Data source field points at them.

Phases
=======

```
DRAFT   map claims to unit types + jobs per venue rules (haipipe-application-draft)
PROBE   materialization needs → _PROBE/ cards → task routing (haipipe-application-probe)
REVISE  unit set coherence: one job per unit, no orphan units (haipipe-application-revise)
CHECK   exit criteria below → Gate Ledger row (haipipe-application-check)
```

Definition of done
===================

```
[ ] 0-lifecycle/4-display/4-display.md exists (when the venue requires it)
[ ] Every primary claim has at least one display unit
[ ] Every unit has all four fields — type, claim, JOB, data source
[ ] Unmaterialized data sources have _PROBE/ cards (task-routed)
[ ] Display types match the venue's available element types
```

Handoff: `promote -> /haipipe-application section-edit` (sectioned venues) or `-> /haipipe-application draft`. End the reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).

Risk profile
=============

WRITES the 4-display/ stage folder only. Never computes or renders inline.

---
name: haipipe-application-display
description: "Stage 4 of the intervention lifecycle (venue-GATED: required for dashboard/ui-card/report, optional for email, skipped for sms/push/reminder/checklist — per STATUS.md stages_skipped). Answers 'what content element carries each claim, and what job does each unit do?' Maps claims to display units (panels, widgets, charts, sections) with per-unit jobs and evidence anchors — the retired minimap stage's concern lives here. Output: 0-lifecycle/4-display/4-display.md + _LOG + 1-probes/. Trigger: display, content elements, panels, widgets, unit jobs, /haipipe-application display."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.4.8"
  last_updated: "2026-07-19"
  summary: "Display stage (stage 4, venue-GATED + venue-ALIGNED) — maps each claim to a display UNIT with a required per-unit Job (minimap absorbed); materialization raised as a section in the flat probe pool 1-probes/, uniquely commissioned by this stage. History: ./CHANGELOG.md."
---

Skill: haipipe-application-display
===================================

Stage **4** of the intervention lifecycle — venue-ALIGNED and venue-GATED.
It answers: what content element carries each claim, and what job does each unit do for the reader?

```text
2-pitch         what this intervention sells
3-narrative     how claims compose into the output's arc
4-display       what element carries each claim + its job   <- THIS STAGE
5-section-edit  does each section's prose do its job
```

Read first: `../../../PHILOSOPHY.md`, the probe layer's `../../../2-phase/1-evidence/haipipe-application-evidence/ref/per-stage-dispatch.md` (the 4-display lane wording).


## What's special: three things make a display a display

**1. Claims become UNITS, each carrying a required Job — the minimap absorption.**
Every display unit carries FOUR fields: Type, Claim, Job, Data source.
The Job is one sentence on what this unit must make the reader see or do — the retired `minimap` stage's job-assignment concern, folded in per-unit.
Same role as paper's display; here a unit is a panel, widget, chart, or section rather than a figure or table.

**2. Venue-GATED and venue-ALIGNED.**
Read `STATUS.md | stages_skipped |`: `display` is skipped for sms/push/reminder/checklist (the venue template already fixes the elements), required for dashboard/ui-card/report, and `optional` venues (email) pull it in on user request.
The available element types come from the venue stage doc's Artifact Principles (`0-lifecycle/2-venue/2-venue.md`); a venue change re-runs the display set.

**3. Display is the ONE stage that commissions its own units.**
A missing unit raised from narrative or a section is NOT commissioned there — it becomes a request row this stage later fulfills, and that section closes `answered-local`.
Only THIS stage commissions render/materialization work for its own accepted units; every other stage's display lane merely LINKs what landed.
A unit whose data source does not exist yet is an evidence need: it is raised as a question SECTION in the flat probe pool `1-probes/PPNN_<topic>/` and dispatched through EVIDENCE — display never runs `/haipipe-task` or renders inline (LAW 1).
The rendered output lands task-side; the unit's Data source field points at it.


## The four phases, in display

```text
DRAFT   read 3-narrative.md (the arc, if it fired), 1d-advice.md (what each element carries), 1c-claims.md
        (the evidence anchor behind each element), and the venue profile's element types; map every
        primary claim to >=1 display UNIT, each with Type / Claim / Job / Content / Data source
EVIDENCE   one worker call; an unmaterialized data source is raised as a SECTION in 1-probes/ and, uniquely,
        commissioned by this stage; the display lane LINKs landed units. Routing is the probe layer's:
        ../../../2-phase/1-evidence/haipipe-application-evidence/SKILL.md (4-display lane in ref/per-stage-dispatch.md)
REVISE  unit-set coherence: one job per unit, no orphan units, types match the venue's element set
CHECK   the done list below vs the unit set -> Gate Ledger row in STATUS.md
```

Display PLANS and LINKs units; it never computes, renders, or hand-authors an asset (LAW 1) — materialization is task work reached through the EVIDENCE phase, which binds each question to a QA file in the task/discovery bank.


## The artifact

`0-lifecycle/4-display/4-display.md` — full skeleton in `ref/display-template.md` (the per-venue dashboard/report unit templates live there, not inline):

```text
Display units      one U<nn>: Type + Claim (via A<n> where an advice entry drives it) + Job + Content
                   + Data source · Status: planned | commissioned (PP<nn>) | landed
Unit -> section    (sectioned venues) which unit goes in which section, and why
  mapping
Q-consumer         materialization questions, one `## Q-Disp-<n>` block each (Ask / Why / Answer); the display lane LINKs what landed
```

Sidecar: `_LOG_4-display.md` (phase journal).
Evidence questions live in the flat probe pool `1-probes/PPNN_<topic>/` (one file per TOPIC; each ENTRY is one `## QX<n>` q-executor carrying `### q-executor` / `### q-consumer` / `### bank binding` / `### a-executor`), states `planned | commissioned | answered | read | answered-local | failed`; the stake stays in this doc's Q-consumer.
Formatting: `=====` title / `-----` sections; content uses no `#`, Q-consumer questions use `## Q-Disp-<n>`; one sentence per line; the doc reads `2-venue.md`'s Artifact Principles for the available element types.


## Definition of done (read at CHECK)

```text
[ ] 4-display.md exists (when the venue requires it)
[ ] every primary claim has at least one display unit
[ ] every unit has all four fields — Type, Claim, Job, Data source
[ ] unmaterialized data sources have 1-probes/ sections (task-routed, commissioned by this stage)
[ ] display types match the venue's available element types
```


## Questions this stage typically raises

DRAFT's RAISE+PLAN step raises what the draft cannot answer. These are the kinds this stage is prone to — read this list, then walk the draft against it.

```
📤 evidence exists   Does a task-produced result exist that this element would show?
                     An element with no producing task cannot be refreshed.
🎨 element form      Panel, chart, table, or plain sentence — which does this claim
                     need? Ask when the venue's budget makes it a real trade.
📐 venue budget      How many elements does this modality allow, and what is cut?
🖥️ render context   On what screen / in what client will this be seen? An element
                     that breaks on a phone is not done.
```

## Exits

```text
promote -> /haipipe-application section-edit   (sectioned venues)
       or -> /haipipe-application draft         (compose the artifact)
```

End every reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).

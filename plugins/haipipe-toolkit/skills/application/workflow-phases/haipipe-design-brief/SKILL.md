---
name: haipipe-design-brief
description: >-
  DesignBoard workflow phase D0 and Folder contract for the one Brief: why the
  Application exists, for whom, the behavior/outcome and venue boundary, the
  insight needs it raises, and the Design roster it authorizes. Trigger:
  design brief, application brief, D0, folder-kind brief, /haipipe-design-brief.
metadata:
  version: "1.0.1"
  last_updated: "2026-08-31"
  workflow: haipipe-design-workflow
  phase: D0
  folder_kind: brief
  primary_face: page
  page_ruling: none
  legacy_page_type: brief
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Opportunity → Audience Set and Behavior → Outcome and Kill Criteria → Venue Scope → Promise → Insight Needs Raised → Core PageX Inputs → Design Roster and Handoff"
---

# /haipipe-design-brief · frame the Application

Load `haipipe-folder`, `haipipe-page`, `haipipe-design`, and the Design
workflow. Existing Briefs may retain `page-type: brief`; new ones use
`folder-kind: brief`.

## Position

D0 frames one DesignBoard and enters through GD0. The Brief lives at
`0-BR-brief/BR00-brief/` and is the board's only authority for scope, promise,
needs raised, and Design roster.

## Folder Kind

Brief says what the Application is building and for whom. It does not inventory
data, perform DIKW, decide a design direction, write content, or field an
experiment.

## Input

Two births are legal: `born-of: mandate` records a person's program decision;
`born-of: <W id list>` resolves signed Wisdom handoffs on boards named by
`reads:`. Evidence-first text is drafted from the handoffs and remains subject
to a person's edit.

## Page Face

Use the eight fixed divisions declared in metadata. Every insight need has a
stable QD/QI/QK/QW id, neutral wording, affected audience/job, target rung, and
blocked Aim. The Design roster is one row per audience × behavior job × primary
venue.

## Task Face

Resolve `born-of:` and `reads:`; reconcile opportunity, audience, behavior,
outcome/kill, venue, and promise; raise unanswered needs; bind already accepted
core inputs; and release a Design roster. Do not answer a need locally.

## Plugins

- `pagex` required for evidence-first birth or accepted core inputs;
- `outline` required;
- `probe` forbidden: missing insight is raised to the InsightBoard;
- `code` forbidden: the Brief frames work.

## Gate and Closure

GD0 passes when birth resolves, scope and kill criteria are explicit, every
load-bearing premise is a bound input or neutral need, and every roster row has
one audience/job/venue. No source inventory or preferred answer remains.

## Handoff

Hand D1 the GD0-closed Brief version, board `reads:`, Design roster, venue packs,
and current need/register state.

## Files

- Page: `0-BR-brief/BR00-brief/BR00-brief.md`
- Cross-board inputs: `0-BR-brief/BR00-brief/evidence/pagex/`

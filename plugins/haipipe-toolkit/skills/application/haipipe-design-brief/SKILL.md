---
name: haipipe-design-brief
description: >-
  Canonical owner of the DesignBoard's one Brief Folder: why the Application
  exists, for whom, the behavior/outcome and venue boundary, the insight needs
  it raises, and the Design roster it authorizes. Trigger: design brief,
  application brief, folder-kind brief, /haipipe-design-brief.
metadata:
  version: "0.4.0"
  last_updated: "2026-09-13"
  folder_owner: canonical
  folder_kind: brief
  primary_face: page
  page_ruling: none
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Opportunity → Audience Set and Behavior → Outcome and Kill Criteria → Venue Scope → Promise → Insight Needs Raised → Frozen Signed-W Inputs → Design Roster and Handoff"
---

# /haipipe-design-brief · frame the Application

## Version governance

This Design family remains pre-1.0. Only explicit user approval may authorize
`1.0.0` or any higher major version. Architecture size, clean breaks, and
field-test repairs do not independently authorize a major-version jump.

Load `haipipe-folder`, `haipipe-page`, and `haipipe-design`. A current Brief
uses `folder-kind: brief` and its own Page workflow.

## Position

The Brief lives at `0-BR-brief/BR00-brief/` and is the board's only authority
for scope, promise, needs raised, and Design roster. It is a precondition for
Design Commissions, not a Design workflow phase.

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
stable QD/QI/QK/QW id, neutral wording, affected partition/audience, target
rung, derived Question Group, and blocked Aim. The Design roster is one row per
audience × behavior job × primary venue.

## Task Face

Resolve `born-of:` and `reads:`; reconcile opportunity, audience, behavior,
outcome/kill, venue, and promise; raise unanswered needs; bind already accepted
core inputs; and release a Design roster. Do not answer a need locally.

## Plugins

- exact signed-W path/Page-version/content-hash/signature/GI6 receipt required
  for evidence-first birth or accepted core inputs; PageX is invalid;
- `outline` required;
- upstream execution forbidden: missing insight is raised to the InsightBoard;
- `code` forbidden: the Brief frames work.

## Gate and Closure

The Brief is releasable when birth resolves, scope and kill criteria are
explicit, every load-bearing premise is a bound input or neutral need, and
every roster row has one audience/job/venue. The Page workflow releases that
exact version. No source inventory or preferred answer remains.

## Handoff

Each Commission pins the released Brief version, board `reads:`, Design roster,
venue packs, and current need/register state.

## Clean break

Do not resolve `page-type: brief`, D0/GD0 records, PageX, or D1 handoffs. They
are unsupported and cannot authorize a current Commission.

## Files

- Page: `0-BR-brief/BR00-brief/BR00-brief.md`
- Cross-board inputs: frozen records in the Brief's current Context/Evidence workspace

---
name: haipipe-application-artifact
description: "Artifact composer for the intervention lifecycle (the `draft` verb). Reads the pinned venue profile (template, constraints, style-profile, exemplars), the audience profile, and the lifecycle stages the venue required (claims always; narrative/display/sections when present), then composes 0-artifacts/<slug>-v{N}.md through a DPRC pass. One skill, all venues — the venue profile IS the instruction set; no format-specific sub-skills. Renamed from haipipe-application-draft (paper-alignment 2026-07-06: 'draft' is a PHASE name; the phase worker in 2-phase/0-draft now owns it). Trigger: draft, write, create, generate, make the SMS, compose the email, /haipipe-application draft."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "3.1.0"
  last_updated: "2026-07-17"
  summary: "Composes 0-artifacts/<slug>-v{N}.md through a DPRC pass — one skill for every venue, because the pinned venue profile IS the instruction set. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-artifact (the `draft` verb)
=======================================================

One skill, all venues. The venue profile carries the composing instructions -- template, constraints, style guide, exemplars. No venue-specific sub-skills needed. Users reach this via `/haipipe-application draft`.

How it works
=============

```
1. Read STATUS.md → pinned venue + audience + stages_skipped + Gate Ledger.
   If no venue pinned → BLOCK ("run /haipipe-application venue first").
   If the venue's required lifecycle stages are not gate-approved → WARN and
   ask (compose-anyway is allowed but recorded in the artifact's Review notes).
2. Load venue profile:
     venue/venue-<name>/README.md          constraints + template
     venue/venue-<name>/style-profile.md   voice + drafting rules + self-review checklist
     venue/venue-<name>/exemplars/         real artifacts to imitate (when present)
3. Tone-by-audience: the venue style-profile (step 2) carries the per-audience tone + citation rules.
4. Load lifecycle inputs:
     0-lifecycle/2-venue/2-venue.md         Artifact Principles (template/slots, limits, tone, element types, section structure, gate depth) — the venue contract, not re-derived from the pack
     0-lifecycle/1d-advice/1d-advice.md  design advice (always -- content-WHAT; each move traces A<-C)
     0-lifecycle/1c-claims/1c-claims.md     the ledger (always -- the evidence backstop)
     0-lifecycle/3-narrative/3-narrative.md arc (if venue required it)
     0-lifecycle/4-display/4-display.md     content elements + jobs (if required)
     0-sections/*.md|.tex                   section prose (sectioned venues)
5. Compose through a DPRC pass (below) → 0-artifacts/<slug>-v{N}.md
```

Simple venues (sms, push, reminder)
=====================================

For venues that skip narrative/display/section-edit, compose directly from the ledger + venue template:

```
Input:   1d-advice adopted entries (1c ledger as backstop) + venue template + audience profile
Output:  one artifact following the template slots

Example (venue-sms):
  Slot 1 (greeting):  "Hi [Name], your [Medication]..."  ← personalization
  Slot 2 (benefit):   "Refilling on time helps..."       ← A1
  Slot 3 (CTA):       "Reply REFILL to start"            ← A2
  Slot 4 (close):     "Reply STOP to opt out"            ← standard
```

The advice-to-slot mapping happens HERE (venue-ALIGNED), not in the ladder: the advice says what the content should do, the template says where it goes. Record every adopted A id -- and each declined one, with a one-line why -- in the artifact frontmatter; declined entries persist for the next venue/round. An adopted EXPLORE entry keeps its tag in the list (e.g. `A3 (explore)`) -- the artifact knowingly ships a bet, and iterate reads the tag to route the A/B result back to the claim it settles.

Sectioned venues (dashboard, report)
=====================================

Compose the deliverable from the approved lifecycle artifacts: structure from the venue template, arc from narrative, content elements + jobs from display, prose from 0-sections/. The artifact is an assembly with connective text -- new claims never appear here.

DPRC composition pass
======================

```
COMPOSE (draft)   fill the template/assembly from lifecycle inputs
PROBE             trace every number to its task-result/card anchor; flag what does not
REVISE            style-profile + audience pass (length limits, tone, reading level)
                  via the shared revise worker's rules
CHECK             run the venue self-review checklist; then hand to
                  Skill("haipipe-application-check", args="draft") for the human
                  gate -- approve writes the `draft` Gate Ledger row
```

Artifact output
================

```
<intervention-root>/0-artifacts/<slug>-v{N}.md
```

Version N increments on re-draft (after round feedback). Previous versions kept for diff.

```yaml
---
kind: intervention
venue: <pinned venue>
audience: <audience>
intent: "<from pitch>"
created: YYYY-MM-DD
adopted_A: [A1, A2]
declined_A: [A3]   # one-line why per declined id
status: draft | reviewed | deployed
---
```

Definition of done
===================

```
[ ] 0-artifacts/<slug>-v{N}.md exists, frontmatter complete (venue, audience, adopted_A/declined_A)
[ ] Content follows the venue template/structure; tone matches the audience profile
[ ] Every number and adopted A traces through its C to a resolvable anchor (no unflagged inventions)
[ ] Venue self-review checklist run (failures noted in ## Review notes)
[ ] CHECK presented; on approve, Gate Ledger `draft` row written
```

Risk profile
=============

WRITES one artifact to `0-artifacts/` (+ the CHECK worker's ledger row on approve). READ-ONLY on everything else. Never edits lifecycle stage docs -- a composition problem that traces upstream is a loopback suggestion, not an inline fix.

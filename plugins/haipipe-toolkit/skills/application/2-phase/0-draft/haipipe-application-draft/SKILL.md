---
name: haipipe-application-draft
description: "DRAFT phase worker (internal). Called first by every application stage skill to settle the stage doc's structure and sentences with the user: illuminate what exists, elicit taste-bearing choices, write the stage artifact per the calling stage's artifact spec. Content decisions happen here (agent + user together); evidence collection is PROBE's job, prose quality is REVISE's. Users invoke stage skills, not this skill directly."
argument-hint: "[stage <stage-name>] [intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
metadata:
  version: "1.1.0"
  last_updated: "2026-07-07"
  summary: "NEW thin DRAFT worker (paper parity). Settles stage-doc structure + sentences; the calling stage supplies the artifact spec. The old artifact-generator of this name moved to 3-build-deploy/haipipe-application-artifact. v1.1: DRAFT MAY use inline WebSearch for orientation -- but its output is drafting fuel (stage-doc prose + buffered planned PPNN skeletons) only, NEVER durable evidence (no refs/findings into PP cards). Real evidence is the PROBE phase's job."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-draft (internal phase worker)
=========================================================

DRAFT phase worker. Every stage skill calls this first. The calling stage passes its artifact spec (files, content structure, done-criteria); this worker turns intent into a settled stage doc.

## What DRAFT means

```
1. ILLUMINATE   read what already exists (stage doc, upstream stage docs,
                STATUS.md venue/audience when the stage is venue-ALIGNED);
                surface the taste-bearing choices instead of guessing
2. ELICIT       ask the user the few choices that shape the doc (framing,
                emphasis, scope); mechanical structure is autonomous
3. WRITE        the stage artifact per the calling stage's spec:
                0-lifecycle/<N-stage>/<N-stage>.md + a [DRAFT] entry in _LOG
4. FLAG         every spot where the draft needs evidence it does not have
                ("NEED: ...") -- these become PROBE's work list
```

DRAFT settles WHAT the doc says. It does NOT collect evidence (PROBE), polish prose (REVISE), or approve anything (CHECK).

## Boundaries

- Venue-FREE stages (seed, claims): do not read venue packs; the doc must survive retargeting.
- Venue-ALIGNED stages (pitch, narrative, display, section-edit): read `_venue/venue-<name>` + `_audience/profile-<name>` for structure and tone expectations.
- Never invent evidence: an unbacked statement is written as a flagged NEED, not asserted.
- Stage docs are markdown, one physical line per paragraph/bullet.

## DRAFT may search; PROBE must dispatch

Inline WebSearch/WebFetch is ALLOWED in DRAFT -- as drafting fuel, NOT as evidence.

DRAFT may search the web to orient (is this intervention space crowded? what response rates do comparable programs report? what are the channel's framing norms?) and to sharpen the stage doc. What that search produces has exactly two legal destinations:

1. **PROSE** in the stage doc (Opportunity, Mechanism hypothesis, beat text, ...) -- phrased as orientation, never as settled fact; anything load-bearing stays a flagged NEED.
2. **BUFFERED probe skeletons** -- when the search reveals something the intervention must later verify, write it as a PPNN card SKELETON (Need / Why / Route, `status: planned`, EMPTY `refs:`) in the calling stage's `_PROBE/` + an index row in `1-probe-plans/README.md`, per the buffer convention `../../../haipipe-application/fn/probe-plans.md`. This HANDS the gap to the PROBE phase; it does not answer it.

FORBIDDEN in DRAFT: writing findings, `refs:`, or takeaways INTO a PP card, or treating an inline result as a landed probe. Real evidence lands ONLY via the PROBE phase dispatching `haipipe-application-probe` (the single door to the /haipipe-probe gateway); inline search results have no project-side ledger -- per the probe contract, evidence gathered any other way means "the PROBE phase did not happen."

The line is CARD STATE: DRAFT leaves `status: planned` skeletons; only PROBE flips them to `read` with resolving `discoveries/` / `tasks/` refs. `check-probe-cards.sh` enforces this mechanically at the probe worker's VERIFY step and again at the CHECK gate -- planned/empty-ref cards block green, so DRAFT search can never masquerade as evidence.

## Return contract

```
status:    ok | blocked
stage:     <stage-name>
artifact:  <path written>
needs:     <count of flagged NEEDs for PROBE>
next:      PROBE
```

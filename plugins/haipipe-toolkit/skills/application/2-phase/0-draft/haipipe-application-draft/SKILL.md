---
name: haipipe-application-draft
description: "DRAFT phase worker (internal). Called first by every application stage skill to settle the stage doc's structure and sentences with the user: illuminate what exists, elicit taste-bearing choices, write the stage artifact per the calling stage's artifact spec. Content decisions happen here (agent + user together); evidence collection is PROBE's job, prose quality is REVISE's. Users invoke stage skills, not this skill directly."
argument-hint: "[stage <stage-name>] [intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.0.0"
  last_updated: "2026-07-06"
  summary: "NEW thin DRAFT worker (paper parity). Settles stage-doc structure + sentences; the calling stage supplies the artifact spec. The old artifact-generator of this name moved to 3-build-deploy/haipipe-application-artifact."
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

## Return contract

```
status:    ok | blocked
stage:     <stage-name>
artifact:  <path written>
needs:     <count of flagged NEEDs for PROBE>
next:      PROBE
```

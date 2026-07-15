---
name: haipipe-application-draft
description: "DRAFT phase worker (internal). Called first by every application stage skill to settle the stage doc's structure and sentences with the user: illuminate what exists, elicit taste-bearing choices, write the stage artifact per the calling stage's artifact spec. DRAFT IS WHERE THE QUESTIONS ARE BORN -- what it cannot answer, it RAISES as a `state: planned` SECTION in the right topic's probe file under 1-probes/, for the PROBE phase to bind. Content decisions happen here (agent + user together); evidence collection is PROBE's job, prose quality is REVISE's. Users invoke stage skills, not this skill directly."
argument-hint: "[stage <stage-name>] [intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
metadata:
  version: "1.2.1"
  last_updated: "2026-07-14"
  summary: "NEW thin DRAFT worker (paper parity). Settles stage-doc structure + sentences; the calling stage supplies the artifact spec. The old artifact-generator of this name moved to 3-build-deploy/haipipe-application-artifact. v1.1: DRAFT MAY use inline WebSearch for orientation -- but its output is drafting fuel only, NEVER durable evidence. v1.2 (probe redesign, Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3 approved JL 2026-07-14): DRAFT is the birthplace of the QUESTIONS. What it cannot answer it RAISES as a question SECTION (state: planned, empty target:) in 1-probes/PPNN_<topic>.md -- not a PPNN card skeleton in a per-stage _PROBE/ folder (retired), not an index row in 1-probe-plans/ (retired). It may write the `q-executor` (the question in general language) but NEVER the `## Why` into it: the stake never leaves the probe file. The line is SECTION STATE: DRAFT leaves `planned`; only PROBE reaches `read` with a target: that resolves to a QA file in the bank. Convention pointer repointed: `haipipe-application/fn/probe-plans.md` was RENAMED to `fn/probes.md` (matching the paper twin; 'plans' is retired vocabulary per skills/STRUCTURE.md)."
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
2. **RAISED QUESTIONS** -- when the search reveals something the intervention must later verify, RAISE IT AS A QUESTION. **DRAFT is where the questions are born.** Write each one as a SECTION (`state: planned`, EMPTY `target:`) in the right topic's probe file under `1-probes/PPNN_<topic>.md`, per `../../../haipipe-application/fn/probes.md`. This HANDS the gap to the PROBE phase; it does not answer it.

FORBIDDEN in DRAFT: writing a `a-consumer`, writing a `target:`, or treating an inline result as a landed answer. Real evidence lands ONLY through the PROBE phase (`haipipe-application-probe`), which MATCHes the bank's QA corpus and commissions what is missing to the task/discovery orchestrators. Inline search results have no project-side home -- per the probe contract, evidence gathered any other way means "the PROBE phase did not happen."

The line is SECTION STATE: DRAFT leaves `state: planned` sections with an empty `target:`; only PROBE moves them to `read` with a `target:` that RESOLVES to a QA file in the bank. `check-probe-cards.sh` enforces this mechanically at the probe worker's VERIFY step and again at the CHECK gate -- a `planned` section blocks green, so DRAFT search can never masquerade as evidence.

DRAFT may write the `q-executor` (the question in general language) when the question is already clear. It must NEVER write the `## Why` into a q-executor: the stake stays in the probe file, always.

## Return contract

```
status:    ok | blocked
stage:     <stage-name>
artifact:  <path written>
needs:     <count of flagged NEEDs for PROBE>
next:      PROBE
```

---
name: haipipe-application-draft
description: "DRAFT phase worker (internal). Called first by every application stage skill to settle the stage doc's structure and sentences with the user: illuminate what exists, elicit taste-bearing choices, write the stage artifact per the calling stage's artifact spec. Content decisions happen here (agent + user together); evidence collection is PROBE's job, prose quality is REVISE's. Users invoke stage skills, not this skill directly."
argument-hint: "[stage <stage-name>] [intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
metadata:
  version: "1.3.0"
  last_updated: "2026-07-09"
  summary: "DRAFT phase worker (internal): settle the stage doc's structure + sentences with the user (illuminate → elicit → write per the stage's template), and RAISE what the draft cannot answer as `state: planned` question SECTIONS in 1-probes/ — never an answer or a target. Inline WebSearch is drafting fuel only, never durable evidence. The calling stage supplies the artifact spec + template; this worker carries neither. History: ./CHANGELOG.md."
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
4. RAISE        every spot where the draft needs evidence it does not have
                becomes a QUESTION -- a `state: planned` SECTION in the right
                topic's probe file (1-probes/PPNN_<topic>.md), per
                ../../../haipipe-application/fn/probes.md; write its q-executor
                (general language, the stake stripped out), never an answer or
                a target
5. PRESENT      end the phase reply with the raised questions, one line each --
                PP id -- question -- mode -- what it fills/settles -- then STOP
                and ask which to pursue. APPROVE is the user's gate; the probe
                worker's ORGANIZE only advances approved questions. No open
                questions -> say "questions raised: none".
```

DRAFT settles WHAT the doc says. It does NOT collect evidence (PROBE), polish prose (REVISE), or approve anything (CHECK).

## Template registry (WRITE reads the stage's canonical template)

At WRITE, read TWO things from `1-lifecycle/`: the calling stage's SKILL.md artifact spec (WHAT to produce, done-criteria) and its canonical template (section order, placeholders, formatting). This worker carries NO templates of its own -- the stage owns its format.

| Stage | Artifact spec | Template |
|---|---|---|
| seed | `1-lifecycle/0-seed/haipipe-application-seed/SKILL.md` | `ref/seed-template.md` |
| descriptions | `1-lifecycle/1a-descriptions/haipipe-application-descriptions/SKILL.md` | `ref/descriptions-template.md` |
| themes | `1-lifecycle/1b-themes/haipipe-application-themes/SKILL.md` | `ref/themes-template.md` |
| claims | `1-lifecycle/1c-claims/haipipe-application-claims/SKILL.md` | `ref/claims-template.md` |
| advice | `1-lifecycle/1d-advice/haipipe-application-advice/SKILL.md` | `ref/advice-template.md` |
| venue | `1-lifecycle/haipipe-application-venue/SKILL.md` | `ref/venue-template.md` |
| pitch | `1-lifecycle/2-pitch/haipipe-application-pitch/SKILL.md` | `ref/pitch-template.md` |
| narrative | `1-lifecycle/3-narrative/haipipe-application-narrative/SKILL.md` | `ref/narrative-template.md` |
| display | `1-lifecycle/4-display/haipipe-application-display/SKILL.md` | `ref/display-template.md` |
| section name | `1-lifecycle/5-section-edit/haipipe-application-section-edit/SKILL.md` | per-section scaffolds in that skill |

(Template paths are relative to each stage skill's OWN folder, e.g. `1-lifecycle/1a-descriptions/haipipe-application-descriptions/ref/descriptions-template.md`. Artifact formatting is uniform: `=====` title / `-----` sections / `**bold**` sub-items, one sentence per line, no `#` headings.)

## Boundaries

- Venue-FREE stages (seed + the 1a-1d ladder: descriptions, themes, claims, advice): do not read venue packs; the doc must survive retargeting.
- Venue-ALIGNED stages (pitch, narrative, display, section-edit): read `_venue/venue-<name>` + `_audience/profile-<name>` for structure and tone expectations.
- Never invent evidence: an unbacked statement is written as a raised question, not asserted.
- Stage docs are markdown, one physical line per paragraph/bullet.

## DRAFT may search; PROBE must dispatch

Inline WebSearch/WebFetch is ALLOWED in DRAFT -- as drafting fuel, NOT as evidence.

DRAFT may search the web to orient (is this intervention space crowded? what response rates do comparable programs report? what are the channel's framing norms?) and to sharpen the stage doc. What that search produces has exactly two legal destinations:

1. **PROSE** in the stage doc (Opportunity, Mechanism hypothesis, beat text, ...) -- phrased as orientation, never as settled fact; anything load-bearing stays a raised question.
2. **RAISED QUESTIONS** -- when the search reveals something the intervention must later verify, RAISE IT AS A QUESTION: a SECTION (`state: planned`, EMPTY `target:`) in the right topic's probe file at `1-probes/PPNN_<topic>.md`, per `../../../haipipe-application/fn/probes.md`. Write the `q-executor:` (general language — no claim ids, no stake, no hint of which answer is wanted); the `## Why` (the stake) stays in the file and never crosses. This HANDS the gap to the PROBE phase; it does not answer it.

FORBIDDEN in DRAFT: writing an `a-consumer:`, a `target:`, or any finding INTO a probe section, or treating an inline result as landed evidence. Real evidence lands ONLY via the PROBE phase dispatching `haipipe-application-probe` (the single door); inline search results bind to nothing -- evidence gathered any other way means "the PROBE phase did not happen."

The line is the SECTION STATE: DRAFT leaves sections at `state: planned` with an empty `target:`; only PROBE reaches `read`, with a `target:` that RESOLVES to a QA file on disk. `check-probe-cards.sh` enforces this mechanically at the probe worker's VERIFY step and again at the CHECK gate -- a `planned` section blocks green, so DRAFT search can never masquerade as evidence.

## Return contract

```
status:    ok | blocked
stage:     <stage-name>
artifact:  <path written>
needs:     <count of questions raised for PROBE>
probes:    <each raised question: PPNN -- question -- mode -- fills/settles; or "none">
next:      PROBE (ORGANIZE advances only the approved questions)
```

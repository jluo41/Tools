---
name: haipipe-application-draft
description: "Application-specific DRAFT phase worker (internal). Called whenever a stage enters DRAFT to define or reopen its purpose, Aims, and artifact shape, then raise stake-bearing Q-consumers for what it cannot answer. It writes no Probe record or executor-side field. Content decisions happen here; evidence collection is PROBE's job, realization under fixed Aims is REVISE's. Users invoke stage skills, not this skill directly."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent
metadata:
  argument_hint: "[stage <stage-name>] [intervention-path]"
  version: "0.1.6"
  last_updated: "2026-08-04"
  summary: "Application-specific DRAFT worker layered on haipipe-board-page-draft: settle the stage promise and artifact, raise stake-bearing Q-consumers, and stop before every PROBE-side field."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-draft (internal phase worker)
=========================================================

DRAFT phase worker. A stage calls it whenever the Page router enters DRAFT. The calling stage passes its artifact spec (files, content structure, done-criteria); this worker turns intent into a settled stage doc.

**LOAD THE PAGE LAYERS FIRST:** `../../../../board/page-types/haipipe-board-page-for-stage/SKILL.md`, then `../../../../board/page-phases/haipipe-board-page-draft/SKILL.md`.
Those contracts own the Stage Page shape and DRAFT authority.
This file adds only application artifact knowledge.

## Rules

The DRAFT authority lives in `haipipe-board-page-draft`.
`../../../../probe/haipipe-probe/SKILL.md` supplies the Q-consumer vocabulary and evidence-wall boundary only.
On a phase conflict, the Page Phase contract wins; application-specific additions are the steps below.

## What DRAFT means

```
1. ILLUMINATE   read what already exists (stage doc, upstream stage docs,
                STATUS.md venue/audience when the stage is venue-ALIGNED);
                surface the taste-bearing choices instead of guessing
2. ELICIT       ask the user the few choices that shape the doc (framing,
                emphasis, scope); mechanical structure is autonomous
3. WRITE        the stage artifact per the calling stage's spec:
                0-lifecycle/<N-stage>/<N-stage>.md + a [DRAFT] entry in _LOG
4. RAISE        FIND the questions first: read the calling stage's
                **Questions this stage typically raises** and walk the draft
                against it. Every spot where the draft needs evidence it does
                not have becomes a stake-bearing `Q-<Stage>-<n>` in the stage
                doc's Q-consumer. DRAFT writes no Probe file, Q-executor, route,
                bank, target, or A-executor. PROBE owns the whole five-step loop.
4b. SELF-REVIEW a fresh-context sub-agent checks the draft + Q-consumer shape
                before handoff (creator/reviewer split — the drafter
                does not grade its own work). Report-only; the drafter fixes.
                Bounded at 2 rounds; a 3rd-round residual is SURFACED at the gate,
                never hidden. See **Step 4b** below.
5. HAND OFF     record the draft, raised Q-consumers, and self-review verdict.
                If the local stage contract declares a DRAFT gate, present them
                and wait there. Otherwise route immediately: consequential
                questions go to PROBE; a version ready for judgment may go to
                CHECK; more promise work remains in DRAFT.
```

## Step 4b. 🤖 SELF-REVIEW — check the draft + Q-consumers before handoff

```text
Agent(general-purpose, prompt="
  Review this DRAFT phase output against the checklist. Report PASS or a numbered issue list
  (file + line + what's wrong + the fix). Do NOT edit anything — only report.

  READ:
    - the stage draft (the stage doc this run wrote/updated)
    - the calling stage's artifact spec, and probe's 'The DRAFT self-review checklist' at
      Tools/plugins/haipipe-toolkit/skills/probe/haipipe-probe/SKILL.md (repo-root-relative —
      you resolve from the repo root, not from the calling skill's folder)

  Surface A — the draft, vs the stage's artifact spec:
    - every section filled with REAL content (no unmarked placeholders)
    - one physical line per paragraph/bullet
    - every Q-<Stage>-<n> is cited inline [Q-<Stage>-<n>] on the sentence it hangs on
    - COMPLETENESS, the reverse direction: every unbacked statement is either owned by a
      Q-<Stage>-<n> or explicitly declined in _LOG. An unowned hole is a defect — nobody
      owns it, so nobody will ever fill it.

  Surface B — the Page-facing question register:
    every open need has one specific Q-consumer carrying its stake and a matching State row;
    no Probe file, q-executor, route, bank, target, or a-executor was authored during DRAFT
")
```

Issues → FIX them, then re-run (bounded: at most 2 rounds). The self-review PRECEDES the human gate; it never replaces it.

DRAFT settles WHAT the doc says. It does NOT collect evidence (PROBE), polish prose (REVISE), or approve anything (CHECK).

## Template registry (WRITE reads the stage's canonical template)

At WRITE, read TWO things from `../../../1-lifecycle/`: the calling stage's SKILL.md artifact spec (WHAT to produce, done-criteria) and its canonical template (section order, placeholders, formatting). This worker carries NO templates of its own -- the stage owns its format.

| Stage | Artifact spec | Template |
|---|---|---|
| seed | `../../../1-lifecycle/0-seed/haipipe-application-seed/SKILL.md` | `ref/seed-template.md` |
| descriptions | `../../../1-lifecycle/1a-descriptions/haipipe-application-descriptions/SKILL.md` | `ref/descriptions-template.md` |
| themes | `../../../1-lifecycle/1b-themes/haipipe-application-themes/SKILL.md` | `ref/themes-template.md` |
| claims | `../../../1-lifecycle/1c-claims/haipipe-application-claims/SKILL.md` | `ref/claims-template.md` |
| advice | `../../../1-lifecycle/1d-advice/haipipe-application-advice/SKILL.md` | `ref/advice-template.md` |
| venue | `../../../1-lifecycle/haipipe-application-venue/SKILL.md` | `ref/venue-template.md` |
| pitch | `../../../1-lifecycle/2-pitch/haipipe-application-pitch/SKILL.md` | `ref/pitch-template.md` |
| narrative | `../../../1-lifecycle/3-narrative/haipipe-application-narrative/SKILL.md` | `ref/narrative-template.md` |
| display | `../../../1-lifecycle/4-display/haipipe-application-display/SKILL.md` | `ref/display-template.md` |
| section name | `../../../1-lifecycle/5-section-edit/haipipe-application-section-edit/SKILL.md` | per-section scaffolds in that skill |

(Template paths are relative to each stage skill's OWN folder, e.g. `../../../1-lifecycle/1a-descriptions/haipipe-application-descriptions/ref/descriptions-template.md`. Artifact formatting is uniform: `=====` title / `-----` sections / `**bold**` sub-items, one sentence per line, no `#` headings.)

## Boundaries

- Venue-FREE stages (seed + the 1a-1d ladder: descriptions, themes, claims, advice): do not read venue packs; the doc must survive retargeting.
- Venue-ALIGNED stages (pitch, narrative, display, section-edit): read `venue/venue-<name>` for structure and tone expectations (the pack carries tone-by-audience).
- Never invent evidence: an unbacked statement is written as a raised question, not asserted.
- Stage docs are markdown, one physical line per paragraph/bullet.

## DRAFT may search; PROBE must dispatch

Inline WebSearch/WebFetch is ALLOWED in DRAFT -- as drafting fuel, NOT as evidence.

DRAFT may search the web to orient (is this intervention space crowded? what response rates do comparable programs report? what are the channel's framing norms?) and to sharpen the stage doc. What that search produces has exactly two legal destinations:

1. **PROSE** in the stage doc (Opportunity, Mechanism hypothesis, beat text, ...) -- phrased as orientation, never as settled fact; anything load-bearing stays a raised question.
2. **A RAISED QUESTION** -- a gap the search reveals goes through step 4 RAISE+PLAN like any other question, with no special status. The entry contract lives there, not here.

FORBIDDEN in DRAFT: writing an `### a-executor` (the ANSWER -- that is PROBE's ⑤ harvest), or treating an inline result as landed evidence. Real evidence lands ONLY via the PROBE phase dispatching `haipipe-application-probe` (the single door); inline search results bind to nothing -- evidence gathered any other way means "the PROBE phase did not happen."

DRAFT writes no `target:` or Probe state at all.
Only PROBE may create the persisted Probe record, write `### a-executor`, and advance its derived state.

## Return contract

```
status:    ok | blocked
stage:     <stage-name>
artifact:  <path written>
needs:     <count of Q-consumers raised for PROBE>
questions:<each raised Q-consumer id + question; or "none">
next:      <PROBE | REVISE | CHECK | DRAFT, chosen by the Page router>
```

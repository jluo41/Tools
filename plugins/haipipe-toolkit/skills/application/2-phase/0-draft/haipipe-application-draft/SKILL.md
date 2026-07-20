---
name: haipipe-application-draft
description: "DRAFT phase worker (internal). Called first by every application stage skill to settle the stage doc's structure and sentences with the user: illuminate what exists, elicit taste-bearing choices, write the stage artifact per the calling stage's artifact spec. Content decisions happen here (agent + user together); evidence collection is PROBE's job, prose quality is REVISE's. Users invoke stage skills, not this skill directly."
argument-hint: "[stage <stage-name>] [intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent
metadata:
  version: "1.5.0"
  last_updated: "2026-07-19"
  summary: "DRAFT phase worker (internal): settle the stage doc's structure + sentences with the user (illuminate → elicit → write per the stage's template), and RAISE what the draft cannot answer as `## QX<n>` question ENTRIES in 1-probes/ AND author their probe plan (`### q-executor` + route + bank + target — PROBE runs the loop's ①ORGANIZE + ②MATCH); never writes an answer (`### a-executor`). Inline WebSearch is drafting fuel only, never durable evidence. The calling stage supplies the artifact spec + template; this worker carries neither. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-draft (internal phase worker)
=========================================================

DRAFT phase worker. Every stage skill calls this first. The calling stage passes its artifact spec (files, content structure, done-criteria); this worker turns intent into a settled stage doc.

## Rules (follow these — the model is haipipe-probe's)

The DRAFT-phase rules live in `../../../../probe/haipipe-probe/SKILL.md` → **Phase rules · DRAFT phase** + **The DRAFT self-review checklist**. Follow those; on conflict, that file wins. Application-specific additions are the steps below.

## What DRAFT means

```
1. ILLUMINATE   read what already exists (stage doc, upstream stage docs,
                STATUS.md venue/audience when the stage is venue-ALIGNED);
                surface the taste-bearing choices instead of guessing
2. ELICIT       ask the user the few choices that shape the doc (framing,
                emphasis, scope); mechanical structure is autonomous
3. WRITE        the stage artifact per the calling stage's spec:
                0-lifecycle/<N-stage>/<N-stage>.md + a [DRAFT] entry in _LOG
4. RAISE+PLAN   FIND the questions first: read the calling stage's
                **Questions this stage typically raises** and walk the draft
                against it. Then every spot where the draft needs evidence it
                does not have becomes a QUESTION -- a `Q-<Stage>-<n>` in the stage doc's
                Q-consumer AND a `## QX<n>` ENTRY in the right topic's probe file
                (1-probes/PPNN_<topic>.md) -- then write the
                `→ 1-probes/PP<NN> · QX<n>` pointer BACK into that
                `Q-<Stage>-<n>`, so the stage doc says where its answer will
                come from. Per
                ../../../haipipe-application/fn/probes.md. DRAFT runs the loop's
                ①ORGANIZE + ②MATCH: write `### q-executor` (general language,
                stake stripped, + Deliverable/Accepted) + a `### q-consumer`
                bullet + `### bank binding` (route · bank · target — an existing
                path or `NEW <path>`). NEVER write `### a-executor` (the answer).
4b. SELF-REVIEW a fresh-context sub-agent checks the draft + the probe plan
                before the human sees either (creator/reviewer split — the drafter
                does not grade its own work). Report-only; the drafter fixes.
                Bounded at 2 rounds; a 3rd-round residual is SURFACED at the gate,
                never hidden. See **Step 4b** below.
5. PRESENT      ⛔ STOP and end the turn, presenting all THREE things the one
                merged gate exists to review:
                  (a) the DRAFT -- structure + where the placeholders are;
                  (b) the PROBE PLAN -- one line per question:
                      PP id -- question -- route -- bank -- what it fills/settles;
                  (c) the SELF-REVIEW VERDICT, incl. any residual.
                No open questions -> say "questions raised: none".
                The user reviews structure AND plan and adds `> USER:` comments;
                reply `> CC:` underneath each, never deleting or rewording one.
                Iterate until the user advances -- their verb/"go" is the gate.
6. CONFIRM      on approval: move resolved threads to `_LOG`, write the phase
                summary + a `[GATE] draft-review: approved` line quoting the user,
                mark draft ✅, hand off to PROBE.
```

## Step 4b. 🤖 SELF-REVIEW — check the draft + probe plan before the gate

```text
Agent(general-purpose, prompt="
  Review this DRAFT phase output against the checklist. Report PASS or a numbered issue list
  (file + line + what's wrong + the fix). Do NOT edit anything — only report.

  READ:
    - the stage draft (the stage doc this run wrote/updated)
    - the probe plan (the 1-probes/PPNN_*.md files touched this run)
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

  Surface B — the probe plan (run probe's 'DRAFT self-review checklist' verbatim):
    LAW-2-clean q-executor · answerable+specific · route set · bank ROOTED to a specific folder
    (candidate READ + judged on the answer) · target agrees with bank · each ### q-consumer bullet
    copies a real stage-doc Q-consumer id · no stake leaked into a q-executor
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

The line is no longer an empty `target:` (DRAFT now writes the `target:` plan) -- it is `### a-executor` / `state`: DRAFT leaves an entry at `planned` (a `NEW` target awaiting dispatch) or `answered` (an existing target already answered, awaiting harvest), never `read`; only PROBE's harvest writes `### a-executor` and reaches `read`. `check-probe-cards.sh` enforces this at the probe worker's VERIFY step and again at the CHECK gate -- a `planned` entry blocks green, so DRAFT search can never masquerade as evidence.

## Return contract

```
status:    ok | blocked
stage:     <stage-name>
artifact:  <path written>
needs:     <count of questions raised for PROBE>
probes:    <each raised question: PPNN -- question -- route -- bank -- fills/settles; or "none">
next:      PROBE (runs the approved entries forward: ③DISPATCH → ④POINT → ⑤INTERPRET)
```

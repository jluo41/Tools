---
name: haipipe-paper-seed
description: "Create or update the paper folder's 0-lifecycle/0-seed/0-seed.md + _LOG_0-seed.md: the venue-FREE earliest stage contract that keeps a paper possibility alive before evidence is mature. States why the paper might exist and what it may argue. Venue-free: does not change when retargeting to a different journal. Markdown only. Use for paper seed, why this paper, project seed, 0-seed."
argument-hint: "[paper-dir] [--source <path-or-note>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "3.2.0"
  last_updated: "2026-07-03"
  summary: "Seed stage orchestrator. Defines WHAT (3 sections) and drives phases (draft -> probe -> revise -> check) internally. User invokes seed, not phases."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-seed
===================================

Stage orchestrator for the **seed** stage (stage 0, venue-FREE). The user invokes this skill; it drives the phases internally.

It answers one question:

```text
Why might this paper exist?
```

The seed is not a pitch, claim ledger, or outline. It keeps a paper-shaped possibility alive while the evidence is still forming.

Read first: `../../PHILOSOPHY.md`, `../../wiki/04-lifecycle-map.md`.

## Artifact Spec

**Files produced:**
- `0-lifecycle/0-seed/0-seed.md` -- the seed contract
- `0-lifecycle/0-seed/_LOG_0-seed.md` -- phase progress journal (per `../../wiki/02-comment-lifecycle.md`)
- `0-lifecycle/0-seed/_PROBE/PPNN_<slug>.md` -- probe plans spawned by this stage (need -> probe_ref -> takeaways, one file per need; indexed in `1-probe-plans/README.md`)
- `0-lifecycle/0-seed/_CITATION_0-seed.md` -- citation candidates HARVESTed from what the probe brought back (only when the probe returns literature; candidates 🔍, no bibtex)

**Content structure (0-seed.md):**
- Seed Question -- the one paper-shaped question this seed exists to answer
- Motivations -- why this is interesting, what makes the angle novel, to whom
- Tentative Claim Shape -- what the paper may eventually argue, phrased as a hypothesis

**Done-criteria:**
- [ ] All three sections filled with real content (not placeholders)
- [ ] _LOG entry records the current state

## Phase Orchestration

When the user invokes `/haipipe-paper seed`, this skill drives the phases in order. The user does not call phase skills directly.

```
seed invoked
  │
  ▼
DRAFT ──→ illuminate existing content, elicit taste,
          write/iterate the 3 sections with > JL: / > CC: comments
          (internally calls /haipipe-paper-draft with this artifact spec)
  │
  ▼
PROBE ──→ DEFAULT RUN for a new seed: landscape / related work / novelty (mode light) --
          it answers the CHECK questions "who cares?" and "is this new?" before the gate
          (internally calls /haipipe-paper-probe → Agent(haipipe-probe-orchestrator-agent)
           → /haipipe-probe → discovery; takeaways backfill the PP plan file in _PROBE/,
           sources harvest into _CITATION_0-seed.md, full evidence stays project-side;
           NEVER dispatch discovery/task agents or /haipipe-probe directly from here)
  │
  ▼
REVISE ─→ refine prose clarity of the 3 sections, weave probe takeaways into Motivations
          (internally calls /haipipe-paper-revise)
  │
  ▼
CHECK ──→ present exit gate per ../../wiki/08-stage-gate.md
          user confirms → advance to claims
          (internally calls /haipipe-paper-check)
```

Phase visibility per the Phase Transition Contract in `../../wiki/08-stage-gate.md`: announce every phase boundary (reply line + `[PHASE]` entry in `_LOG` + phase-line 🔥 moves); PROBE/REVISE may be skipped only on re-entry or minor edits, and only by an explicit logged verdict (`[PROBE] skipped -- <reason>`, phase line shows `--`); CHECK is never implicit -- it opens by presenting the exit-criteria report and the approval ask.

Comment lifecycle per `../../wiki/02-comment-lifecycle.md`: comments live in 0-seed.md while active, move to _LOG on resolve, each phase starts clean.

## Location

```text
<paper>/0-lifecycle/0-seed/0-seed.md              seed contract
<paper>/0-lifecycle/0-seed/_LOG_0-seed.md          phase progress journal
<paper>/0-lifecycle/0-seed/_PROBE/PPNN_<slug>.md   probe plans + backfilled takeaways
<paper>/0-lifecycle/0-seed/_CITATION_0-seed.md     harvested citation candidates (when probe returns lit)
```

Markdown only (argument documents don't need compilation).

## Template

The canonical template is the source of truth for section order: `ref/seed-template.md`

```markdown
## Seed Question
The one paper-shaped question this seed exists to answer.

## Motivations
Why this is interesting (puzzle / gap / surprise), what makes the angle novel or feasible now, and to whom it is interesting (name the audiences and why each cares).

## Tentative Claim Shape
What the paper may eventually argue, phrased as a hypothesis, not a finding.
```

## Principles

1. A seed may be intuition. It does not require evidence yet.
2. Do not create `0-sections/`, displays, or compile obligations from the seed. Those start later.
3. **Seed is venue-FREE.** Venue selection happens after claims (seed -> claims -> [venue] -> pitch). Do not reference a target venue here.
4. Evidence inventory, routing, and gap analysis belong in the claims stage, not here.

## Handoff

On CHECK confirm, update `STATUS.md` (`current_layer`, `maturity: seed`) and advance:

```text
promote     -> /haipipe-paper claims <paper-dir>
```

End the reply with the stage strip (run `../../../haipipe-paper/stage-strip.sh`).

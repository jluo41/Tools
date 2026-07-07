---
name: haipipe-paper-seed
description: "Create or update the paper folder's 0-lifecycle/0-seed/0-seed.md + _LOG_0-seed.md: the venue-FREE earliest stage contract that keeps a paper possibility alive before evidence is mature. States why the paper might exist and what it may argue. Venue-free: does not change when retargeting to a different journal. Markdown only. Use for paper seed, why this paper, project seed, 0-seed."
argument-hint: "[paper-dir] [--source <path-or-note>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "3.4.0"
  last_updated: "2026-07-06"
  summary: "Seed stage orchestrator. Defines WHAT (4 sections: question, motivations, claim shape, probes) and drives phases (draft -> probe -> revise -> check) internally. User invokes seed, not phases. v3.4: PROBE phase is exactly one worker call (Skill haipipe-paper-probe); NEVER-do-evidence-itself rule; gate confirms PP cards have refs (outcome, not mechanics)."
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
- Probes -- landscape/novelty probes that answer "is this new?" and "who cares?", with takeaways inline

**Formatting:**
- Heading style: `=====` for the document title, `-----` for sections. No `#`/`##`/`###`.
- One sentence per line (semantic line breaks). No dense multi-sentence paragraphs.

**Done-criteria:**
- [ ] All four sections filled with real content (not placeholders)
- [ ] Probes section carries at least the novelty/landscape probe result
- [ ] _LOG entry records the current state
- [ ] Probe cards verify clean: locate the checker layout-agnostically (installed skills flatten the tree, so the `../../../2-phase/...` relative path is NOT reliable) -- `CHK=$(find ~/.claude/skills "$CLAUDE_PLUGIN_ROOT" -name check-probe-cards.sh 2>/dev/null | head -1)` then `sh "$CHK" <paper_root>` exits 0 (refs resolve project-side, no tables, no fat cards -- the gate RUNS the checker and shows its output; it never eyeballs cards)

## Phase Orchestration

When the user invokes `/haipipe-paper seed`, this skill drives the phases in order. The user does not call phase skills directly.

```
seed invoked
  │
  ▼
DRAFT ──→ illuminate existing content, elicit taste,
          write/iterate the 4 sections with > JL: / > CC: comments
          (internally calls /haipipe-paper-draft with this artifact spec)
  │
  ▼
PROBE ──→ DEFAULT RUN for a new seed: landscape / related work / novelty (mode light) --
          it answers the CHECK questions "who cares?" and "is this new?" before the gate.
          This stage does EXACTLY ONE thing here:
              Skill("haipipe-paper-probe", args="from-buffer <paper_root>")
          The worker owns everything downstream: PP card creation/format, index
          bookkeeping, project-root resolution, agent dispatch, refs backfill.
          THIS STAGE NEVER does evidence work itself -- never searches, never
          launches search/discovery/task agents, never writes findings into PP
          cards. Evidence produced any other way than the worker call above has
          no project-side ledger and is void: the PROBE phase did not happen.
          After the worker returns: takeaways appear in the PP plan files in
          _PROBE/ (with refs: pointing at discoveries/ or tasks/) AND get woven
          into the Probes section in 0-seed.md; sources harvest into
          _CITATION_0-seed.md; full evidence stays project-side.
  │
  ▼
REVISE ─→ refine prose clarity of the 4 sections, weave probe takeaways into Motivations
          AND into the Probes section
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
0-seed: <working title>
========================

Date: YYYY-MM-DD
Status: DRAFT

Seed Question
-------------
The one paper-shaped question this seed exists to answer.

Motivations
-----------
Why this is interesting (puzzle / gap / surprise).
What makes the angle novel or feasible now.
To whom it is interesting (name the audiences and why each cares).

Tentative Claim Shape
---------------------
What the paper may eventually argue, phrased as a hypothesis, not a finding.

Probes
------
Landscape/novelty probes that answer "is this new?" and "who cares?"
Each probe as a **bold** sub-item with type, status, and takeaways inline.
```

## Principles

1. A seed may be intuition. It does not require evidence yet.
2. Do not create `0-sections/`, displays, or compile obligations from the seed. Those start later.
3. **Seed is venue-FREE.** Venue selection happens after claims (seed -> claims -> [venue] -> pitch). Do not reference a target venue here.
4. Evidence inventory, routing, and gap analysis belong in the claims stage, not here.
5. **Probes are explicit.** The Probes section makes the landscape/novelty check visible in the seed document itself, not buried in a satellite file. The `_PROBE/` files carry the execution detail.
6. **One sentence per line.** Semantic line breaks for readability. No dense multi-sentence paragraphs.
7. **Heading style.** `=====` for the document title, `-----` for sections. No `#`/`##`/`###`.

## Handoff

On CHECK confirm, update `STATUS.md` (`current_layer`, `maturity: seed`) and advance:

```text
promote     -> /haipipe-paper claims <paper-dir>
```

End the reply with the stage strip (run `../../../haipipe-paper/stage-strip.sh`).

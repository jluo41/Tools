---
name: haipipe-paper-seed
description: "Create or update the paper folder's 0-lifecycle/0-seed/0-seed.md + _LOG_0-seed.md: the venue-FREE earliest stage contract that keeps a paper possibility alive before evidence is mature. States why the paper might exist and what it may argue. Venue-free: does not change when retargeting to a different journal. Markdown only. Use for paper seed, why this paper, project seed, 0-seed."
argument-hint: "[paper-dir] [--source <path-or-note>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "3.6.1"
  last_updated: "2026-07-10"
  summary: "Seed stage orchestrator. Defines WHAT (4 sections: question, motivations, claim shape, probes) and drives phases (draft -> probe -> revise -> check) internally. User invokes seed, not phases. v3.4: PROBE is exactly one worker call; NEVER-do-evidence-itself; gate confirms refs. v3.5: DRAFT may WebSearch to orient (fuel -> prose + buffered planned skeletons), PROBE must ALWAYS run the real orchestrator; seed probes are FEASIBILITY only (novelty + external-data-obtainable), internal-data profiling forward-points to CLAIMS via a _LOG pointer."
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

When the user invokes `/haipipe-paper seed`, this skill drives the phases in order. The user does not call phase skills directly — but steers them with VERBS on this stage:

```
/haipipe-paper seed <paper-dir>            -> open: status + frontier; advance ONLY on the user's verb
/haipipe-paper seed <paper-dir> draft      -> run/redo DRAFT  -> STOP for user review
/haipipe-paper seed <paper-dir> probe      -> run/redo PROBE  (agent-only)
/haipipe-paper seed <paper-dir> revise     -> dispatch REVISE workers (agent-only, proof-carrying)
/haipipe-paper seed <paper-dir> check      -> open the CHECK gate
```

**Hard gates (binding).** After DRAFT: ⛔ STOP — present the draft for review and end the turn; the user's verb/"go" advances, logged as `[GATE] draft-review: approved` quoting the user. Each phase runs via its `Skill()` dispatch — a phase executed inline did not happen; the `[REVISE]` _LOG entry carries its `workers:` proof line. Never commit or conclude the stage before CHECK opens with its report. The agent never self-advances past a gate.

**Comment rules (binding).** The agent NEVER deletes, rewords, or relocates a `> USER:` comment; it replies `> CC:` underneath; only the user resolves a thread; resolved threads MOVE to `_LOG` verbatim. Working files are edited surgically — no full-file rewrite of a file carrying `> USER:` comments. Background: `../../wiki/02-comment-lifecycle.md`.

```
seed invoked
  │
  ▼
DRAFT ──→ illuminate existing content, elicit taste,
          write/iterate the 4 sections with > USER: / > CC: comments.
          Ends at ⛔ STOP: user reviews, iterates, approves ([GATE] logged).
          MAY WebSearch inline to ORIENT the angle (crowded field? dataset
          exist? anchor names?) -- the result is drafting fuel: weave it into
          the prose (as orientation, `\cite{TOADD}` slots — never invented keys) AND buffer
          the feasibility probes as `status: planned` PP skeletons (empty
          refs). NEVER write findings/refs into a PP card here -- that is the
          PROBE phase's job (the seed is allowed to be intuition; probe makes
          it evidence). The line is card state: DRAFT leaves planned skeletons.
          (internally calls /haipipe-paper-draft with this artifact spec)
  │
  ▼
PROBE ──→ DEFAULT RUN for a new seed: FEASIBILITY probes (mode light) --
          they answer "can this paper exist at all?": is it NOVEL (landscape /
          related work / 查新) and does the EXTERNAL labeled data EXIST. That is
          the seed's whole probe scope. Profiling OUR OWN data belongs in
          claims (task work on our AIData) -- if the draft surfaced such a need,
          it was registered as a `[FORWARD -> CLAIMS] PPNN` pointer in _LOG at
          DRAFT, NOT dispatched here.
          ALWAYS run the real probes -- this stage does EXACTLY ONE thing here:
              Skill("haipipe-paper-probe", args="from-buffer <paper_root>")
          The worker owns everything downstream: PP card creation/format, index
          bookkeeping, project-root resolution, agent dispatch, refs backfill.
          THIS STAGE NEVER does evidence work itself -- never searches, never
          launches search/discovery/task agents, never writes findings into PP
          cards. (Inline WebSearch was fine in DRAFT as orientation fuel; here
          in PROBE it is forbidden -- durability is the whole point.) Evidence
          produced any other way than the worker call above has no project-side
          ledger and is void: the PROBE phase did not happen.
          After the worker returns: takeaways appear in the PP plan files in
          _PROBE/ (with refs: pointing at discoveries/ or tasks/) AND get woven
          into the Probes section in 0-seed.md; sources harvest into
          _CITATION_0-seed.md; full evidence stays project-side.
  │
  ▼
REVISE ─→ refine prose clarity of the 4 sections, weave probe takeaways into Motivations
          AND into the Probes section
          (internally calls /haipipe-paper-revise; [REVISE] _LOG entry carries workers: proof)
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
5a. **Seed probes are FEASIBILITY only.** A seed probe answers "can this paper exist at all?" -- novelty (is the angle new?) and external-data-obtainability (does the labeled data the paper needs exist and is it accessible?). Both are `discover` (lit/repo) work. Profiling OUR OWN data (cohort size, field coverage, label availability in our AIData) is `task` work that belongs in the CLAIMS stage. When DRAFT surfaces an internal-data question, DO NOT open a seed probe for it -- record a `[FORWARD -> CLAIMS] PPNN_<slug>` pointer line in `_LOG_0-seed.md` (need + why, no dispatch); it fires when claims opens. This keeps the seed's cost bounded to the feasibility question and stops the seed from doing claims-stage evidence work early.
5b. **DRAFT may search; PROBE must dispatch.** Inline WebSearch is legitimate DRAFT fuel (orientation -> prose + buffered `status: planned` PP skeletons), but it is NEVER evidence. The PROBE phase must ALWAYS run the real orchestrator (`Skill(haipipe-paper-probe, from-buffer ...)`); inline results with no project-side ledger mean the PROBE phase did not happen. The invariant that separates the two is card state: planned skeleton (DRAFT) vs `read` + resolving `discoveries/` refs (PROBE), mechanically enforced by `check-probe-cards.sh` at the CHECK gate.
6. **One sentence per line.** Semantic line breaks for readability. No dense multi-sentence paragraphs.
7. **Heading style.** `=====` for the document title, `-----` for sections. No `#`/`##`/`###`.

## Handoff

On CHECK confirm, update `STATUS.md` (`current_layer`, `maturity: seed`) and advance:

```text
promote     -> /haipipe-paper claims <paper-dir>
```

End the reply with the stage strip (run `../../../haipipe-paper/stage-strip.sh`).

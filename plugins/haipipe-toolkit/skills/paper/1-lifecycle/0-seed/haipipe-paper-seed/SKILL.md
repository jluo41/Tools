---
name: haipipe-paper-seed
description: "Create or update the paper folder's 0-lifecycle/0-seed/0-seed.md + _LOG_0-seed.md: the venue-FREE earliest stage contract that keeps a paper possibility alive before evidence is mature. States why the paper might exist and what it may argue. Venue-free: does not change when retargeting to a different journal. Markdown only. Use for paper seed, why this paper, project seed, 0-seed."
argument-hint: "[paper-dir] [--source <path-or-note>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "4.1.1"
  last_updated: "2026-07-14"
  summary: "Seed stage orchestrator. Defines WHAT (4 sections: question, motivations, claim shape, probes) and drives phases (draft -> probe -> revise -> check) internally. User invokes seed, not phases. v3.4: PROBE is exactly one worker call; NEVER-do-evidence-itself; gate confirms refs. v3.5: DRAFT may WebSearch to orient (fuel -> prose + buffered planned skeletons), PROBE must ALWAYS run the real orchestrator; seed probes are FEASIBILITY only (novelty + external-data-obtainable). v3.7: seed hands to RESOURCE (which hands to claims); internal-data profiling / prerequisite work forward-points to RESOURCE via a _LOG pointer. v4.1 (probe-redesign residue sweep): DRAFT raises `state: planned` question SECTIONS (not `status: planned` PP card skeletons); the DRAFT/PROBE line is SECTION STATE, not card state. v4.1.1: every shared-convention pointer was off by one `../` — `../../PHILOSOPHY.md` / `../../wiki/<page>.md` resolved to 1-lifecycle/, which holds neither. The stage skills sit TWO levels under skills/paper/ (1-lifecycle/<N>-<stage>/<skill>/), so the correct depth is `../../../`. Every required-read at the top of this skill silently failed. Repointed."
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

Read first: `../../../PHILOSOPHY.md`, `../../../wiki/04-lifecycle-map.md`.

## Artifact Spec

**Files produced:**
- `0-lifecycle/0-seed/0-seed.md` -- the seed contract
- `0-lifecycle/0-seed/_LOG_0-seed.md` -- phase progress journal (per `../../../wiki/02-comment-lifecycle.md`)
- `1-probes/PPNN_<topic>.md` -- the probe files this stage's questions land in (one file per TOPIC, one SECTION per question: serves/target/state/q-executor/a-consumer, plus ONE `## Why` per file; flat cross-stage pool at the paper root, the SECTION's `serves:` carries the stage; Status board in `1-probes/README.md`)
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
- [ ] Probe files verify clean: locate the checker layout-agnostically (installed skills flatten the tree, so the `../../../2-phase/...` relative path is NOT reliable) AND filter on the FAMILY -- TWO files named `check-probe-cards.sh` exist on disk (paper + application), and a bare `-name` find resolves to whichever the filesystem hands back first, silently asserting a paper against application invariants:
      ```sh
      CHK=$(find ~/.claude/skills "$CLAUDE_PLUGIN_ROOT" -path '*haipipe-paper-probe/check-probe-cards.sh' 2>/dev/null | head -1)
      [ -n "$CHK" ] || { echo 'FAIL: paper probe checker not found'; exit 1; }
      sh "$CHK" <paper_root>
      ```
      exits 0 (every section's `target:` resolves on disk, no `planned` survivors, no markdown tables, LAW 2 clean on both surfaces -- the gate RUNS the checker and shows its output; it never eyeballs probe files)

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

**Comment rules (binding).** The agent NEVER deletes, rewords, or relocates a `> USER:` comment; it replies `> CC:` underneath; only the user resolves a thread; resolved threads MOVE to `_LOG` verbatim. Working files are edited surgically — no full-file rewrite of a file carrying `> USER:` comments. Background: `../../../wiki/02-comment-lifecycle.md`.

```
seed invoked
  │
  ▼
DRAFT ──→ illuminate existing content, elicit taste,
          write/iterate the 4 sections with > USER: / > CC: comments.
          Ends at ⛔ STOP: user reviews, iterates, approves ([GATE] logged).
          MAY WebSearch inline to ORIENT the angle (crowded field? dataset
          exist? anchor names?) -- the result is drafting fuel: weave it into
          the prose (as orientation, `\cite{TOADD}` slots — never invented keys) AND raise
          the feasibility questions as `state: planned` SECTIONS in 1-probes/
          (empty `target:`). NEVER write a `a-consumer:` or a `target:` into a section
          here -- that is the PROBE phase's job (the seed is allowed to be intuition;
          PROBE makes it evidence). The line is SECTION STATE: DRAFT leaves `planned`.
          (internally calls /haipipe-paper-draft with this artifact spec)
  │
  ▼
PROBE ──→ DEFAULT RUN for a new seed: FEASIBILITY probes (mode light) --
          they answer "can this paper exist at all?": is it NOVEL (landscape /
          related work / 查新) and does the EXTERNAL labeled data EXIST. That is
          the seed's whole probe scope. Profiling OUR OWN data belongs in
          RESOURCE (task work on our AIData) -- if the draft surfaced such a need,
          it was registered as a `[FORWARD -> RESOURCE] PPNN` pointer in _LOG at
          DRAFT, NOT dispatched here.
          ALWAYS run the real probes -- this stage does EXACTLY ONE thing here:
              Skill("haipipe-paper-probe", args="from-buffer <paper_root>")
          The worker owns everything downstream: the probe file + its sections,
          project-root resolution, MATCH against the bank, dispatch, and the
          `target:`/`a-consumer:` backfill.
          THIS STAGE NEVER does evidence work itself -- never searches, never
          launches search/discovery/task agents, never writes findings into PP
          cards. (Inline WebSearch was fine in DRAFT as orientation fuel; here
          in PROBE it is forbidden -- durability is the whole point.) Evidence
          produced any other way than the worker call above has no project-side
          ledger and is void: the PROBE phase did not happen.
          After the worker returns: takeaways appear in the PP plan files in
          1-probes/ (with target: resolving to a QA file in discoveries/ or tasks/) AND get woven
          into the Probes section in 0-seed.md; sources harvest into
          _CITATION_0-seed.md; full evidence stays project-side.
  │
  ▼
REVISE ─→ refine prose clarity of the 4 sections, weave probe takeaways into Motivations
          AND into the Probes section
          (internally calls /haipipe-paper-revise; [REVISE] _LOG entry carries workers: proof)
  │
  ▼
CHECK ──→ present exit gate per ../../../wiki/08-stage-gate.md
          user confirms → advance to resource
          (internally calls /haipipe-paper-check)
```

Phase visibility per the Phase Transition Contract in `../../../wiki/08-stage-gate.md`: announce every phase boundary (reply line + `[PHASE]` entry in `_LOG` + phase-line 🔥 moves); PROBE/REVISE may be skipped only on re-entry or minor edits, and only by an explicit logged verdict (`[PROBE] skipped -- <reason>`, phase line shows `--`); CHECK is never implicit -- it opens by presenting the exit-criteria report and the approval ask.

Comment lifecycle per `../../../wiki/02-comment-lifecycle.md`: comments live in 0-seed.md while active, move to _LOG on resolve, each phase starts clean.

## Location

```text
<paper>/0-lifecycle/0-seed/0-seed.md              seed contract
<paper>/0-lifecycle/0-seed/_LOG_0-seed.md          phase progress journal
<paper>/1-probes/PPNN_<topic>.md              probe files; one SECTION per question, `a-consumer:` written at harvest
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
3. **Seed is venue-FREE.** Venue selection happens after claims (seed -> resource -> claims -> [venue] -> pitch). Do not reference a target venue here.
4. Evidence inventory, routing, and gap analysis belong in the claims stage, not here.
5. **Probes are explicit.** The Probes section makes the landscape/novelty check visible in the seed document itself, not buried in a satellite file. The `1-probes/` probe files carry the question SECTIONS and their bindings.
5a. **Seed probes are FEASIBILITY only.** A seed probe answers "can this paper exist at all?" -- novelty (is the angle new?) and external-data-obtainability (does the labeled data the paper needs exist and is it accessible?). Both are `discover` (lit/repo) work. Profiling OUR OWN data (cohort size, field coverage, label availability in our AIData) is `task` work that belongs in the RESOURCE stage, which asks "what EXACTLY must exist, does it, and can it CARRY the claim?". When DRAFT surfaces an internal-data or other prerequisite question, DO NOT open a seed probe for it -- record a forward pointer line in `_LOG_0-seed.md` (need + why, no dispatch); it fires when resource opens. This keeps the seed's cost bounded to the feasibility question and stops the seed from doing resource-stage evidence work early.
5b. **DRAFT may search; PROBE must bind.** Inline WebSearch is legitimate DRAFT fuel (orientation -> prose + `state: planned` question SECTIONS), but it is NEVER evidence. The PROBE phase must ALWAYS run the real worker (`Skill(haipipe-paper-probe, from-buffer ...)`); an inline result binds to nothing, so the PROBE phase did not happen. The invariant that separates the two is SECTION STATE: `planned` with an empty `target:` (DRAFT) vs `read` with a `target:` that RESOLVES to a QA file on disk (PROBE), mechanically enforced by `check-probe-cards.sh` at the CHECK gate.
5c. **The forward pointer has ONE emitted form.** Seed emits, in `_LOG_0-seed.md`, ASCII arrow, destination RESOURCE:

    ```text
    **[FORWARD -> RESOURCE] PPNN_<slug>**
    <the need, and why it is not a seed question>
    ```

    Resource's DRAFT consumes it with a grep that is GLYPH- and LEGACY-TOLERANT -- `grep -E "\[FORWARD (->|→) (RESOURCE|CLAIMS)\]"` -- because 7 pointers written before the resource stage existed say `CLAIMS`, and one of them uses a unicode arrow (→). Emit the ASCII/RESOURCE form above for anything new; never rewrite a legacy pointer to match, the consume-grep already takes it.
6. **One sentence per line.** Semantic line breaks for readability. No dense multi-sentence paragraphs.
7. **Heading style.** `=====` for the document title, `-----` for sections. No `#`/`##`/`###`.

## Handoff

On CHECK confirm, update `STATUS.md` (`current_layer`, `maturity: seed`) and advance:

```text
promote     -> /haipipe-paper resource <paper-dir>
```

Seed hands to **RESOURCE**, which hands to claims (`seed -> resource -> claims -> [venue] -> pitch`). The boundary between the two venue-free front stages:

```text
SEED      is this paper WORTH doing, and is the data even OBTAINABLE in principle?
RESOURCE  what EXACTLY must exist, does it, and can it CARRY the claim?
```

Seed KEEPS its own probe policy (novelty + external-data-obtainable feasibility); novelty probes do NOT move to resource. Every `[FORWARD -> RESOURCE]` pointer left in `_LOG_0-seed.md` (principle 5c) is picked up by resource's DRAFT.

End the reply with the stage strip (run `../../../haipipe-paper/stage-strip.sh`).

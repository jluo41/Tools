---
name: haipipe-paper-seed
description: "Create or update the paper folder's 0-lifecycle/0-seed/0-seed.md + _LOG_0-seed.md: the venue-FREE earliest stage contract that keeps a paper possibility alive before evidence is mature. States why the paper might exist and what it may argue. Venue-free: does not change when retargeting to a different journal. Markdown only. Use for paper seed, why this paper, project seed, 0-seed."
argument-hint: "[paper-dir] [--source <path-or-note>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "4.5.0"
  last_updated: "2026-07-19"
  summary: "Seed stage orchestrator (stage 0, venue-FREE): 5 sections -- Seed Question, Motivations, Landscape, Tentative Claim Shape, Q-consumer -- driving DRAFT -> PROBE -> REVISE -> CHECK internally (the user invokes seed, not the phases). RAISE freely, DISPATCH narrowly: the seed may raise ANY question its draft hangs on (asking is cheap, the Q-consumer is generous), while what it DISPATCHES at seed stays feasibility-shaped (novelty + is external data obtainable) -- the DRAFT gate decides the split. DRAFT may WebSearch as orientation fuel, but PROBE is exactly one real worker call and never does evidence itself. Seed hands forward to RESOURCE (which hands to claims); prerequisite/internal-data work forward-points to RESOURCE via a _LOG pointer. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-seed
===================================

Stage orchestrator for the **seed** stage (stage 0, venue-FREE).
The user invokes this skill; it drives the phases internally.

It answers one question:

```text
Why might this paper exist?
```

The seed is not a pitch, claim ledger, or outline.
It keeps a paper-shaped possibility alive while the evidence is still forming.

Read first: `../../../PHILOSOPHY.md`, `../../ref/04-lifecycle-map.md`.

## Artifact Spec

**Files produced:**
- `0-lifecycle/0-seed/0-seed.md` -- the seed contract
- `0-lifecycle/0-seed/_LOG_0-seed.md` -- phase progress journal (per the Comment lifecycle section in `../../../haipipe-paper/SKILL.md`)
- `1-probes/PPNN_<topic>.md` -- the probe files this stage's questions land in (one file per TOPIC, one ENTRY per q-executor: `## QX<n>` with `### q-executor` / `### q-consumer` / `### bank binding` (route/bank/target/state) / `### a-executor`; no `## Why` -- the stake lives in each stage-doc Q-consumer; flat cross-stage pool at the paper root, the `### q-consumer` bullets carry the stage via their `Q-Seed-<n>` ids; Status board in `1-probes/README.md`)
`1-probes/` is the only consumer-side source of truth; `_LOG_0-seed.md` is the only sidecar. An owed citation is written `\cite{TOADD} [Q-Seed-<n>]` — the citation command and the anchor bracket sit side by side, never fused — where the bracket names the question that will produce the key. A bare `\cite{TOADD}` with no bracket is a defect: it is a hole no question will ever fill.

**Content structure (0-seed.md).**
The FILL rules for every section live INLINE in `ref/seed-template.md` as `<!-- RULE: … -->` comments -- follow them, then delete them (a RULE comment never ships in the seed). The template is the single source of truth; do NOT restate the fill rules here.
Sections, in order: Seed Question, Motivations, Landscape, Tentative Claim Shape, Q-consumer.
The DPRC loop that binds Q-consumer to the content is phase behavior (see Phase Orchestration): DRAFT raises a `Q-Seed-<n>` and cites it inline as `[Q-Seed-<n>]` in the sentence(s) it hangs on; PROBE fills its `Answer`; REVISE weaves the answer back into every citing sentence and discharges the bracket.

**Formatting:**
- Heading style: `=====` for the document title, `-----` for sections.
  No `#`/`##`/`###` — EXCEPT the Q-consumer question blocks, which `ref/seed-template.md` defines as `## Q-Seed-<n> · <title>`. That is the one sanctioned `##` in the file; the template is the source of truth and wins here.
- One sentence per line (semantic line breaks).
  No dense multi-sentence paragraphs.

**Done-criteria:**
- [ ] All five sections filled with real content (not placeholders); every `<!-- RULE -->` comment deleted from 0-seed.md
- [ ] Q-consumer carries every question the draft hangs on, each ANCHORED to a draft assertion; the gate marked each DISPATCHED (feasibility-shaped -> an entry in `1-probes/`) or DEFERRED (`Answer: deferred -> RESOURCE` + a `[FORWARD -> RESOURCE]` pointer, no entry); answers land at PROBE, not DRAFT
- [ ] _LOG entry records the current state
- [ ] Probe files verify clean: locate the checker layout-agnostically (installed skills flatten the tree, so the `../../../2-phase/...` relative path is NOT reliable) AND filter on the FAMILY -- TWO files named `check-probe-cards.sh` exist on disk (paper + application), and a bare `-name` find resolves to whichever the filesystem hands back first, silently asserting a paper against application invariants:
      ```sh
      CHK=$(find ~/.claude/skills "$CLAUDE_PLUGIN_ROOT" -path '*haipipe-paper-probe/check-probe-cards.sh' 2>/dev/null | head -1)
      [ -n "$CHK" ] || { echo 'FAIL: paper probe checker not found'; exit 1; }
      sh "$CHK" <paper_root>
      ```
      exits 0 (every entry's `target` resolves on disk, no `planned` survivors, no markdown tables, LAW 2 clean on both surfaces -- the gate RUNS the checker and shows its output; it never eyeballs probe files)

## Phase Orchestration

When the user invokes `/haipipe-paper seed`, this skill drives the phases in order.
The user does not call phase skills directly — but steers them with VERBS on this stage:

```
/haipipe-paper seed <paper-dir>            -> open: status + frontier; advance ONLY on the user's verb
/haipipe-paper seed <paper-dir> draft      -> run/redo DRAFT  -> STOP for user review
/haipipe-paper seed <paper-dir> probe      -> run/redo PROBE  (agent-only)
/haipipe-paper seed <paper-dir> revise     -> dispatch REVISE workers (agent-only, proof-carrying)
/haipipe-paper seed <paper-dir> check      -> open the CHECK gate
```

**Hard gates (binding).**
After DRAFT: ⛔ STOP — present the draft for review and end the turn; the user's verb/"go" advances, logged as `[GATE] draft-review: approved` quoting the user.
Each phase runs via its `Skill()` dispatch — a phase executed inline did not happen; the `[REVISE]` _LOG entry carries its `workers:` proof line.
Never commit or conclude the stage before CHECK opens with its report.
The agent never self-advances past a gate.

**Comment rules (binding).**
The agent NEVER deletes, rewords, or relocates a `> USER:` comment; it replies `> CC:` underneath; only the user resolves a thread; resolved threads MOVE to `_LOG` verbatim.
Working files are edited surgically — no full-file rewrite of a file carrying `> USER:` comments.
Background: `../../../haipipe-paper/SKILL.md`, Comment lifecycle.

```
seed invoked
  │
  ▼
DRAFT ──→ illuminate existing content, elicit taste,
          write/iterate the 5 sections with > USER: / > CC: comments.
          Ends at ⛔ STOP: user reviews, iterates, approves ([GATE] logged).
          MAY WebSearch inline to ORIENT the angle (crowded field? dataset
          exist? anchor names?) -- the result is drafting fuel: weave it into
          the prose (as orientation, `\cite{TOADD} [Q-Seed-<n>]` slots — never invented keys) AND raise
          EVERY question the draft hangs on, each as a `## Q-Seed-<n>` block in Q-consumer,
          CITING its id inline -- `[Q-Seed-<n>]` in the sentence(s) it hangs on (the forward
          link). Raising is generous; propose a new question rather than leave a sentence
          unanchored. The GATE rules which go out NOW (principle 5a): a DISPATCHED question
          (feasibility-shaped) also gets an ENTRY in 1-probes/; a DEFERRED one keeps its
          Q-consumer block, gets NO entry, and takes a `[FORWARD -> RESOURCE]` pointer.
          Then PLAN each dispatched entry (DRAFT runs
          the loop's ①ORGANIZE + ②MATCH): write its `### q-executor`, `### q-consumer` (the
          Q-Seed-<n> id + original question), and `### bank binding` -- `route` (task |
          discovery), `bank` (root to a SPECIFIC bank folder — a read-only grep, LAW 1:
          reuse | run | code | new), and `target` (an existing QA path or `NEW <path>`). NEVER
          write a `### a-executor` here — the ANSWER is PROBE's ⑤ harvest (the seed may be
          intuition; PROBE makes it evidence). ENTRY STATE after DRAFT: `planned` (a NEW target)
          or `answered` (an existing target already answered), never `read`.
          (internally calls /haipipe-paper-draft with this artifact spec)
  │
  ▼
PROBE ──→ DEFAULT RUN for a new seed: FEASIBILITY probes --
          they answer "can this paper exist at all?": is it NOVEL (landscape /
          related work / 查新) and does the EXTERNAL labeled data EXIST. That is
          the seed's whole DISPATCH scope; this phase runs exactly the entries the
          DRAFT gate approved, no more. Profiling OUR OWN data belongs in
          RESOURCE (task work on our AIData) -- such a question may well have been
          RAISED in Q-consumer, but it was deferred at the gate with a
          `[FORWARD -> RESOURCE] PPNN` pointer in _LOG, and is NOT dispatched here.
          ALWAYS run the real probes -- this stage does EXACTLY ONE thing here:
              Skill("haipipe-paper-probe", args="from-buffer <paper_root>")
          The worker RUNS THE DRAFT-AUTHORED PLAN FORWARD (①ORGANIZE + ②MATCH already
          happened at DRAFT): project-root resolution, ③ DISPATCH the `NEW` entries,
          ④ POINT each `target`, ⑤ harvest the `### a-executor`.
          THIS STAGE NEVER does evidence work itself -- never searches, never
          launches search/discovery/task agents, never writes findings into PP
          cards. (Inline WebSearch was fine in DRAFT as orientation fuel; here
          in PROBE it is forbidden -- durability is the whole point.) Evidence
          produced any other way than the worker call above has no project-side
          ledger and is void: the PROBE phase did not happen.
          After the worker returns: takeaways appear in the PP plan files in
          1-probes/ (with `target` resolving to a QA file in discoveries/ or tasks/) AND land in the
          matching Q-consumer question's `Answer` field in 0-seed.md; sources harvest into
          the ENTRY's own `**sources**:` lane; full evidence stays project-side.
          PROBE STOPS at the `Answer` field -- it is EVIDENCE, not prose. Weaving that
          answer back into the main content (Motivations, Claim Shape, the anchored
          sentence) is REVISE's job, not PROBE's.
  │
  ▼
REVISE ─→ refine prose clarity of the 5 sections, and CLOSE THE LOOP: weave each answered
          question's takeaway FROM its `Answer` field back INTO every sentence that cites its
          `[Q-Seed-<n>]` (Motivations, Landscape, Claim Shape) AND DISCHARGE the bracket
          -- content -> question -> answer -> content
          (internally calls /haipipe-paper-revise; [REVISE] _LOG entry carries workers: proof)
  │
  ▼
CHECK ──→ present exit gate per ../../ref/08-stage-gate.md
          user confirms → advance to resource
          (internally calls /haipipe-paper-check)
```

Phase visibility per the Phase Transition Contract in `../../ref/08-stage-gate.md`: announce every phase boundary (reply line + `[PHASE]` entry in `_LOG` + phase-line 🔥 moves); PROBE/REVISE may be skipped only on re-entry or minor edits, and only by an explicit logged verdict (`[PROBE] skipped -- <reason>`, phase line shows `--`); CHECK is never implicit -- it opens by presenting the exit-criteria report and the approval ask.

Comment lifecycle per `../../../haipipe-paper/SKILL.md` (Comment lifecycle section): comments live in 0-seed.md while active, move to _LOG on resolve, each phase starts clean.

## Location

```text
<paper>/0-lifecycle/0-seed/0-seed.md              seed contract
<paper>/0-lifecycle/0-seed/_LOG_0-seed.md          phase progress journal
<paper>/1-probes/PPNN_<topic>.md              probe files; one ENTRY per q-executor, `### a-executor` written at harvest,
                                              citation candidates on the ENTRY's `**sources**:` lane (no stage sidecar)
```

Markdown only (argument documents don't need compilation).

## Template

`ref/seed-template.md` is the single source of truth -- BOTH the skeleton and the fill rules.
Open that file. It carries `<placeholders>` you replace and `<!-- RULE: … -->` comments you follow then delete; the finished seed keeps neither.
Do NOT restate its rules here or anywhere else (one home; duplication is how things drift, e.g. the old `Probes` -> `Q-consumer` rename).

## Principles

1. A seed may be intuition.
   It does not require evidence yet.
2. Do not create `0-sections/`, displays, or compile obligations from the seed.
   Those start later.
3. **Seed is venue-FREE.**
   Venue selection happens after claims (seed -> resource -> claims -> [venue] -> pitch).
   Do not reference a target venue here.
4. Evidence inventory, routing, and gap analysis belong in the claims stage, not here.
5. **Q-consumer is explicit, and generous.**
   The Q-consumer section makes every QUESTION the draft hangs on visible in the seed document itself -- as many as the draft needs; their ANSWERS arrive at PROBE, not DRAFT.
   The `1-probes/` probe files carry the question SECTIONS and their bindings, for the questions this stage dispatches (principle 5a).
5a. **RAISE freely; DISPATCH narrowly.**
    Asking is cheap, so the Q-consumer is as generous as the draft needs: raise ANY question the seed's prose actually hangs on, however far from feasibility it sits, and when a sentence rests on something no existing question tests, PROPOSE A NEW ONE rather than leave it unanchored.
    Nothing about a question's shape disqualifies it from being asked here.
    The narrow part is DISPATCH: what goes out at seed stays feasibility-shaped -- novelty (is the angle new?) and external-data-obtainability (does the labeled data the paper needs exist and is it accessible?), both `discover` (lit/repo) work.
    A raised question of any other shape -- profiling OUR OWN data (cohort size, field coverage, label availability in our AIData), or any other prerequisite -- KEEPS its `## Q-Seed-<n>` block, gets NO entry in `1-probes/`, records `Answer: deferred -> RESOURCE` and carries a `[FORWARD -> RESOURCE]` pointer in `_LOG_0-seed.md` (principle 5c); it fires when resource opens.
    **The DRAFT gate is where the split is decided**: the user rules, per question, what goes out now and what waits.
    This bounds the seed's SPEND without narrowing what the seed is allowed to notice.
5b. **DRAFT may search; PROBE must bind.**
    Inline WebSearch is legitimate DRAFT fuel (orientation -> prose + `state: planned` q-executor ENTRIES), but it is NEVER evidence.
    The PROBE phase must ALWAYS run the real worker (`Skill(haipipe-paper-probe, from-buffer ...)`); an inline result binds to nothing, so the PROBE phase did not happen.
    The invariant that separates the two is ENTRY STATE: DRAFT leaves an entry `planned` (a `NEW` target) or `answered` (an existing target), with NO `### a-executor` yet; only PROBE's ⑤ harvest writes the `### a-executor` and reaches `read` (its `target` resolving to a QA file on disk), mechanically enforced by `check-probe-cards.sh` at the CHECK gate.
5c. **The forward pointer has ONE emitted form.**
    Seed emits, in `_LOG_0-seed.md`, ASCII arrow, destination RESOURCE:

    ```text
    **[FORWARD -> RESOURCE] PPNN_<slug>**
    <the need, and why it is not a seed question>
    ```

    Resource's DRAFT consumes it with a grep that is GLYPH- and LEGACY-TOLERANT -- `grep -E "\[FORWARD (->|→) (RESOURCE|CLAIMS)\]"` -- because 7 pointers written before the resource stage existed say `CLAIMS`, and one of them uses a unicode arrow (→).
    Emit the ASCII/RESOURCE form above for anything new; never rewrite a legacy pointer to match, the consume-grep already takes it.
6. **One sentence per line.**
   Semantic line breaks for readability.
   No dense multi-sentence paragraphs.
7. **Heading style.**
   `=====` for the document title, `-----` for sections.
   No `#`/`##`/`###` — EXCEPT the Q-consumer question blocks (`## Q-Seed-<n> · <title>`), per the Formatting clause above and `ref/seed-template.md`.
   Do not strip those: the `[Q-Seed-<n>]` anchor loop hangs on them.

## Questions this stage typically raises

DRAFT's Step 4b raises what the draft cannot answer. These are the kinds seed raises — feasibility only, because seed's whole job is "can this paper exist at all?"

```
👣 occupied ground   Has anyone already taken this angle? Name the closest prior art on
                     each half of the pairing, or name the ground as unoccupied.
📦 obtainability     Does the external data this paper needs EXIST, and can we get it?
                     In principle only — size and coverage are RESOURCE's.
```

NOT here: profiling OUR OWN data. That is RESOURCE-stage work — register it as a `[FORWARD -> RESOURCE]` pointer in `_LOG` and do not raise it in seed.

Two questions is the usual shape. A seed raising eight has not decided what it is about.

## Handoff

On CHECK confirm, update `STATUS.md` (`current_layer`, `maturity: seed`) and advance:

```text
promote     -> /haipipe-paper resource <paper-dir>
```

Seed hands to **RESOURCE**, which hands to claims (`seed -> resource -> claims -> [venue] -> pitch`).
The boundary between the two venue-free front stages:

```text
SEED      is this paper WORTH doing, and is the data even OBTAINABLE in principle?
RESOURCE  what EXACTLY must exist, does it, and can it CARRY the claim?
```

Seed KEEPS its own DISPATCH policy (novelty + external-data-obtainable feasibility goes out at seed); novelty questions do NOT move to resource.
Every `[FORWARD -> RESOURCE]` pointer left in `_LOG_0-seed.md` (principle 5c) is picked up by resource's DRAFT.

End the reply with the stage strip (run `../../../haipipe-paper/stage-strip.sh`).

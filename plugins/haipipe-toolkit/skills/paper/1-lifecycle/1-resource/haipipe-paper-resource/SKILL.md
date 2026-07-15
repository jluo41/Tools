---
name: haipipe-paper-resource
description: "Stage orchestrator for the venue-FREE prerequisite stage (0-lifecycle/1-resource/): what must EXIST for this paper to be testable, does it exist, and can it CARRY the claim? Two sections only -- Demand (one N<n> per hypothesis) and Questions (one Q<n> + its A). Covers data, model checkpoints, and producing-code alike. Use for resource, prerequisite, do we have the data, does the checkpoint exist, can this corpus carry the claim, 1-resource."
argument-hint: "[paper-dir] [draft|probe|revise|check]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.1.1"
  last_updated: "2026-07-14"
  summary: "Resource stage orchestrator (stage 1, venue-FREE, shares its number with claims): what must EXIST for this paper to be testable, does it exist, can it CARRY the claim? Two sections only -- Demand (N<n>, keyed on H<n>) and Questions (Q<n> + A). The stage ASKS; the probe layer ROUTES (no PP ids minted here). Two lanes -- SCAN (blocking, minutes) and BUILD (non-blocking, days-to-months, cross-project: mandatory) -- with the SPEND gate (GATE 1b) between them. History: ./CHANGELOG.md. Design of record: ../../../../diagram/260714-resource-stage/."
---

Skill: haipipe-paper-resource
=======================================

Stage orchestrator for the **resource** stage (stage 1, venue-FREE). The user invokes this skill; it drives the phases internally.

It answers one question:

```text
What must EXIST for this paper to be testable, does it exist, and can it CARRY the claim?
```

Resource sits between seed and claims: `seed (0) -> RESOURCE -> claims (1) -> [venue] -> pitch -> narrative -> display -> section-edit`.
It shares the number **1** with claims, deliberately, exactly as `2-venue/` and `2-pitch/` already share the number 2 on disk.
The number is decoration -- `stage-strip.sh` strips the leading digit before matching, and the spine key is the bare name `resource`.
No other stage renumbers.

**Venue-FREE.** Like seed and claims, this stage does not change when you retarget the journal. What a paper NEEDS to exist does not depend on where you send it.

**Scope: DATA + MODELS + PRODUCING-CODE.** Any prerequisite.
Datasets (AIData / corpora), model checkpoints and backbones, and producing-code ("does code that emits metric X exist?") are the SAME KIND of question.
Data is the bulk of it; data is NOT the boundary.
A checkpoint that does not yet exist is a resource question; a metric claim with no code that emits it is a resource question.

**Why this stage exists.** It owns the ruling "this resource cannot carry this claim" and is the gate that stops a dispatch before it burns a full training pass re-deriving what an earlier probe already knew.
The live case is recorded in `../../../../diagram/260714-resource-stage/02-worked-example.txt`.

Read first: `../../../PHILOSOPHY.md`, `../../../wiki/04-lifecycle-map.md`, `../../../wiki/08-stage-gate.md`, `../../../wiki/02-comment-lifecycle.md`.

## Artifact Spec

**Files produced:**
- `0-lifecycle/1-resource/1-resource.md` -- the resource contract (two sections, below)
- `0-lifecycle/1-resource/_LOG_1-resource.md` -- phase progress journal (per `../../../wiki/02-comment-lifecycle.md`)

**No sidecars. None.** No `_VALUES_1-resource.md`, no `_CITATION_1-resource.md`, no `_RESOURCE_` satellite, no new probe lane worker.
The question SECTIONS this stage's Q's become live where every other stage's sections live: the flat cross-stage pool at `1-probes/` (one file per TOPIC, one SECTION per question), OPENED by the PROBE WORKER's ORGANIZE stage intake from the approved Q's -- never by this stage.

**Content structure (1-resource.md) -- EXACTLY TWO SECTIONS:**

```text
Demand       what we MIGHT NEED    one N<n> per hypothesis, derived from the seed
Questions    what we need to KNOW  one Q<n>, and its A when the answer lands
```

That is the whole artifact.

**Do not reintroduce, in any form, under any name:** Kill Conditions, Setup Contract, Resource Ledger, Resource Binding table, any sidecar file.

**Why two sections suffice.** "Do we have it?" AND "does it WORK?" are BOTH the ANSWER.
So there is no separate existence axis, no separate fitness axis, and no binding table -- the **A** says it.
A resource that exists but cannot carry the claim is a Q whose A says so, in one sentence, with what it KILLS.

**Keyed on H\<n\>, not C\<n\>.** Every N row names the hypothesis it serves: `N1 (H1)`.
C-ids do not exist at resource time -- the seed emits H1/H2/H3 as prose in its Tentative Claim Shape, and C-ids are minted downstream in claims.
Writing this stage in C-space is only possible by retro-fitting a claims ledger that was already written, which is the exact ordering failure this stage exists to prevent.

**Formatting:**
- Heading style: `=====` for the document title, `-----` for the two sections. No `#`/`##`/`###`.
  (The design ruling writes the sections as `## Demand` / `## Questions`; the `##` there denotes the SECTION, not the glyph. On disk they are `Demand` / `Questions` with `-----` underlines, per the ASCII style law and both sibling venue-free stages.)
- Sub-items within sections: `**bold**` (e.g. `**N1 (H1)**`, `**Q3 (N1)**`).
- One sentence per line (semantic line breaks). No dense multi-sentence paragraphs.
- No tables. Prose and bullets only.

**Done-criteria:**
- [ ] Demand section: one `**N<n> (H<n>)**` per hypothesis in the seed's Tentative Claim Shape
- [ ] Every N is either answered by a Q, or is a SCOPE CUT the human said out loud (logged in `_LOG`)
- [ ] Every Q carries an **A**, or a `-> PP<NN>` backlink to a probe file that EXISTS (asked, answer pending), or a DECLINED line in `_LOG`. A Q with none of the three is an UNASKED QUESTION and the gate FAILs it by name. The probe worker writes the backlink and the A; this stage writes neither.
- [ ] Every Q that has landed carries its **A**; a woolly A ("probably fine") is a DEFECT, not an answer
- [ ] Every BUILD question carries `cross-project:` -- a sibling-project path ② MATCH NAMED, or `none-found`. Empty is a FAIL.
- [ ] No unconsumed `[FORWARD -> RESOURCE]` / `[FORWARD -> CLAIMS]` pointer in seed's `_LOG_0-seed.md` that belongs here -- each is an N row, a Q, or explicitly DECLINED in `_LOG`
- [ ] `[GATE] draft-review: approved` exists in `_LOG`, quoting the user, BEFORE any Q was routed
- [ ] If any BUILD-lane question exists: `[GATE] spend-authorized` exists in `_LOG`, quoting the user, and its timestamp is AFTER the SCAN answers landed. No BUILD section may be dispatched before it.
- [ ] Probe cards verify clean, SCOPED TO THIS STAGE -- locate the checker layout-agnostically AND unambiguously (see GATE 2 for the full locator; a bare `-name check-probe-cards.sh` can resolve to the APPLICATION family's checker), then `sh "$CHK" <paper_root> --stage resource` exits 0.
      The `--stage resource` flag is what keeps another stage's un-run sections from redding THIS gate, and this stage's in-flight builds from redding theirs.

## The Cleavage Rule (resource vs claims)

This stage's constitution, in two lines:

```text
a question that CHANGES what exists on disk            -> RESOURCE
a question that READS what exists and MOVES A CLAIM'S  -> CLAIMS
  STATUS
```

The toolkit already wrote the pipeline-stage / task-type mapping and filed it under the wrong stage (`haipipe-paper-claims/SKILL.md`, its evidence-plan section).
These rows MOVE here:

```text
input      task-for-data   -> RESOURCE   builds an AIData
method     task-for-algo   -> RESOURCE   builds a capability
fit        task-for-fit    -> RESOURCE   builds a checkpoint
evaluate   task-for-eval   -> CLAIMS     produces the VERDICT      <- STAYS IN CLAIMS
```

**HARD BOUNDARY 1: resource may NOT commission `task-for-eval`.**
That one rule is what stops this stage swallowing the paper.
A bundled fit+eval makes its own null uninterpretable: you cannot tell whether it came from the MODEL or from the CORPUS.
Fit makes the model. Eval makes the evidence. Resource stops at the model.

**HARD BOUNDARY 2: resource NEVER EXECUTES.**
It never invokes `/haipipe-data`, `/haipipe-nn`, or `/haipipe-task`.
It never scaffolds a task folder.
It never scans a store inline, greps a checkpoint directory inline, or web-searches for a corpus inline during PROBE.
It writes QUESTIONS; the PROBE WORKER MATCHes them against the bank and DISPATCHES what MATCH cannot close.
Always run real probes -- never substitute an inline scan: an inline scan leaves `1-probes/` empty and the phase did not happen.

## The Stage ASKS. The Probe Layer ROUTES.

The division of labour is absolute:

```text
THIS STAGE writes   Q1, Q2, Q3 ...        a question, in paper-space, keyed to an N
           NEVER    mints a PP id
           NEVER    picks a probe type (task | discovery) or a probe topic
           NEVER    knows what the project already holds -- that is ② MATCH's job

THE HUMAN  at GATE 1, picks which Q's are worth ASKING.
           A declined Q is LOGGED in _LOG (with the reason), never deleted.
           at GATE 1b, AFTER the SCAN answers have landed, authorizes the SPEND.

THE PROBE  picks the approved Q's UP and OPENS one SECTION per Q under 1-probes/
WORKER     (serves: resource · blocks: N<n> · target: NEW ? · state: planned ·
           commission: the Q re-posed as a self-contained evidence question),
           then writes the `-> PP<NN>` backlink into 1-resource.md. It does NOT
           decide the type, the topic, or the DEPTH -- ② MATCH may close the
           section for free, and an unmatched one is dispatched to the task /
           discovery orchestrator, which picks the shape in its own clean context.

THE       is what ② MATCH could not close: the section's `commission:` block goes,
EXECUTOR   VERBATIM, to Agent(haipipe-task-orchestrator-agent) or
           Agent(haipipe-discovery-orchestrator-agent). IT picks the shape and the
           DEPTH in its own clean context, and answers in <task-folder>/QA/<n>-<slug>.md.
           The answer lands back as the Q's A -- ⑤ INTERPRET writes it there.
           Dispatch goes DIRECT; the executor's clean context IS the wall.
```

**The ownership chain, end to end.** Read it once; it is the whole wire:

```text
DRAFT asks (Q<n>) -> GATE 1 approves -> the PROBE WORKER opens the SECTION + writes
the `-> PP<NN>` backlink -> ② MATCH resolves it, or ③ DISPATCH commissions it to the
executor -> the answer lands as a QA file -> ⑤ INTERPRET writes the A back into the Q.
```

The SECTION is opened by the probe WORKER, and that is not a detail -- it is the only place it can happen.
This stage is forbidden to mint a PP id, and the executor never learns that one exists.
If the worker does not open the section, NOBODY does: PROBE runs over an empty pool and CHECK greens over a stage that asked nothing.
The wire is in `2-phase/1-probe/haipipe-paper-probe/SKILL.md` ① ORGANIZE (RESOURCE STAGE INTAKE) and ⑤ INTERPRET (RESOURCE WRITE-BACK), and `check-probe-cards.sh --stage resource` FAILs any Q that has neither an `A:` nor a backlink.

Asking is cheap -- every SCAN is minutes -- so GATE 1 approves the QUESTIONS, not the SPEND.
The SPEND decision cannot be made at GATE 1: it needs ② MATCH, and MATCH does not run until PROBE.
That is what GATE 1b is for. See Phase Orchestration.

**Side effect worth stating out loud:** because this stage mints no PP ids, it CANNOT collide with a sibling paper's ids. The probe layer owns that namespace, and it is the only thing that does.

## Two Lanes

Every Q, once approved, routes into exactly one of two lanes. The PROBE worker assigns the lane; the stage's job is to write a question that is honestly one or the other.

```text
SCAN    minutes.  GATE-BLOCKING.  This is what makes the stage DECIDABLE.
        store scan / capability grep / access-rung determination
        (PUBLIC | REGISTER | DUA | APPLICATION).
        HARD RULE: a SCAN question whose route exceeds ~1 HOUR is MISFILED.
        Re-route it to BUILD, or shrink the question until it fits the hour.

BUILD   days to weeks.  NON-BLOCKING, ALWAYS.
        task-for-data / task-for-algo / task-for-fit, and LONG ACQUISITIONS
        (a DUA or IRB application -- an ETA in MONTHS, a CALENDAR cost, not a
        compute cost).
        Its SECTION carries (BUILD-lane fields, only at state: commissioned):
            state: commissioned
            owner: <name>
            eta: YYYY-MM-DD
            blocks: N<n>
            cross-project: <path or none-found>
```

`cross-project:` is **MANDATORY on every BUILD question** (JL ruling C4). Empty -> FAIL at CHECK.
Its value is either a sibling-project path ② MATCH NAMED as a reuse candidate, or the literal `none-found`.
MATCH may NAME a sibling-project source; it may NOT consume it (JL 2026-07-05: cross-project reuse is a USER decision).

The field is only NAMED by ② MATCH, and MATCH runs in PROBE.
So the human gate that authorizes SPEND must sit AFTER the sweep, not before it -- otherwise it authorizes spend BLIND, which is the exact failure this field was invented to prevent.
That gate is **GATE 1b**, and the two lanes are what make it possible: SCAN is blocking and cheap, BUILD is not, so the SPEND decision belongs BETWEEN them.

## Phase Orchestration

When the user invokes `/haipipe-paper resource`, this skill drives the phases in order. The user does not call phase skills directly — but steers them with VERBS on this stage:

```
/haipipe-paper resource <paper-dir>            -> open: status + frontier; advance ONLY on the user's verb
/haipipe-paper resource <paper-dir> draft      -> run/redo DRAFT  -> STOP for user review (GATE 1)
/haipipe-paper resource <paper-dir> probe      -> run PROBE       (agent-only)
                                                  first invocation  -> SCAN pass, then STOP at GATE 1b
                                                                       (only if BUILD questions exist)
                                                  after spend-auth  -> BUILD pass
/haipipe-paper resource <paper-dir> revise     -> dispatch REVISE workers (agent-only, proof-carrying)
/haipipe-paper resource <paper-dir> check      -> open the CHECK gate (GATE 2)
```

**Hard gates (binding).** TWO human stops, not one.
After DRAFT: ⛔ STOP at **GATE 1** — the human approves WHICH QUESTIONS to ask; logged as `[GATE] draft-review: approved` quoting the user.
After the SCAN pass, if any BUILD question exists: ⛔ STOP at **GATE 1b** — the human authorizes the SPEND, informed; logged as `[GATE] spend-authorized` quoting the user.
Each phase runs via its `Skill()` dispatch — a phase executed inline did not happen; the `[REVISE]` _LOG entry carries its `workers:` proof line. Never commit or conclude the stage before CHECK opens with its report. The agent never self-advances past a gate.

**THE SPEND-GATE RULE, plainly:**

```text
NO BUILD-LANE SECTION MAY BE DISPATCHED BEFORE `[GATE] spend-authorized` EXISTS
IN _LOG_1-resource.md.
```

A scope cut at GATE 1b is FREE. The same cut after claims costs a CLAIM; after display it costs a FIGURE.

**Comment rules (binding).** The agent NEVER deletes, rewords, or relocates a `> USER:` comment; it replies `> CC:` underneath; only the user resolves a thread; resolved threads MOVE to `_LOG` verbatim. Working files are edited surgically — no full-file rewrite of a file carrying `> USER:` comments. Background: `../../../wiki/02-comment-lifecycle.md`.

```
resource invoked
  │
  ▼
DRAFT ──→ FIRST: consume the seed's forward pointers out of _LOG_0-seed.md.
          The grep MUST be GLYPH- AND LEGACY-TOLERANT. There are 7 live pointers
          on disk; ALL of them say "CLAIMS" (this stage did not exist when they
          were written), and at least one uses a UNICODE arrow (→) rather than
          ASCII (->). A strict ASCII/RESOURCE-only grep silently orphans all
          seven. Match roughly:
              grep -E "\[FORWARD (->|→) (RESOURCE|CLAIMS)\]" _LOG_0-seed.md
          Each pointer becomes an N demand row, or a Q question, or is
          explicitly DECLINED in _LOG (with its reason). A pointer that is a
          CLAIM-STATUS question, not a prerequisite question, is NOT ours --
          leave it for claims and say so in _LOG. Cleavage rule decides.
          THEN: read 0-seed.md's Tentative Claim Shape -> derive one N<n> per H.
          THEN: draft the Q<n> questions -- paper-space questions only, no PP
          ids, no probe types.
          DRAFT may glob / WebSearch to ORIENT (is there obviously a corpus? is
          the checkpoint obviously absent?) -- that is FUEL, never EVIDENCE, and
          it never lands in an A.
          (internally calls /haipipe-paper-draft with this artifact spec)
          Ends at ⛔ STOP -> GATE 1.
  │
  ▼
GATE 1 ─→ HARD STOP FOR THE HUMAN. The human approves WHICH QUESTIONS TO ASK --
          NOT the spend. Asking is CHEAP: every SCAN is minutes, and nothing
          expensive can be reached from here without passing GATE 1b first.
          The human approves THREE things:
            (a) the DEMAND      -- is this really what the claims will need?
            (b) the QUESTIONS   -- which Q's are worth asking at all? A declined
                                   Q is LOGGED in _LOG with its reason, never
                                   deleted (JL: "In the draft, I will determine
                                   whether we want to ask these questions.")
            (c) the SCOPE CUTS  -- a demand nobody intends to resource is a scope
                                   cut, said out loud, here, for free
          NO Q IS ROUTED BEFORE `[GATE] draft-review: approved` EXISTS IN _LOG,
          QUOTING THE USER.
  │
  ▼
PROBE ──→ EXACTLY ONE worker call per pass. Never do evidence inline.
/SCAN         Skill("haipipe-paper-probe", args="from-buffer <paper_root>")
          The worker owns everything downstream. Its STAGE INTAKE (① ORGANIZE)
          READS 1-resource.md, PICKS UP every GATE-1-approved Q, and OPENS one
          SECTION per Q -- then writes the `-> PP<NN>` backlink back into
          1-resource.md, which is the mechanical proof the question was asked.
          ② MATCH then closes what the bank already answers; each surviving
          section gets a lane (SCAN | BUILD), and ③ DISPATCH commissions the SCAN
          lane to the task/discovery orchestrator. This stage never searches, never
          scans a store, never launches an agent, never writes a finding into a
          section -- and never opens the section either.
          (Inline WebSearch was fine in DRAFT as orientation fuel; here in PROBE
          it is forbidden -- durability is the whole point.)
          BLOCKING. The SCAN A's land -- INCLUDING, for every BUILD row, the
          `cross-project:` candidate that ② MATCH just NAMED. The BUILD sections
          now exist as PROPOSALS; NOTHING IN THE BUILD LANE HAS DISPATCHED.
          Ends at ⛔ STOP -> GATE 1b, IF there is at least one BUILD question.
          If there are none, there is nothing to authorize: skip straight to
          REVISE and log `[GATE] spend-authorized: n/a -- no BUILD questions`.
  │
  ▼
GATE 1b ─→ THE SPEND GATE. A SECOND, NARROW human stop. Fires ONLY when BUILD
/SPEND     questions exist. This is the gate the `cross-project:` field was
           invented to feed, and it can only sit HERE: ② MATCH is what NAMES the
           reuse candidate, and MATCH does not run until PROBE.
           At GATE 1 the human would have been authorizing GPU-WEEKS BLIND.
           NOW, INFORMED, the human decides PER BUILD ROW:
             build it  ·  cut it  ·  AUTHORIZE cross-project reuse
           (JL ruling C4; JL 2026-07-05: MATCH may NAME a sibling-project
            source, only the USER may CONSUME it.)
           Present, per row: what it BLOCKS (N<n>), its COST (pipeline-days,
           GPU-weeks, or a DUA whose cost is CALENDAR-MONTHS, not compute), and
           its `cross-project:` candidate or `none-found`.
           Logged as `[GATE] spend-authorized: ...` in _LOG, QUOTING THE USER.
           RULE: NO BUILD-LANE SECTION MAY BE DISPATCHED BEFORE THAT LINE EXISTS.
           A scope cut HERE is FREE. The same cut after claims costs a CLAIM;
           after display, a FIGURE.
  │
  ▼
PROBE ──→ The authorized BUILD sections dispatch, through the same one worker call.
/BUILD    NON-BLOCKING, ALWAYS. They land as `state: commissioned` with owner +
          eta + blocks + cross-project, and the stage does NOT wait for them.
          A row the human CUT is logged as a scope cut, not commissioned.
          A row the human sent to REUSE carries the authorized sibling path.
  │
  ▼
REVISE ─→ DEFAULT: `[REVISE] skipped -- ledger doc, no venue-quality prose`
          (same default as seed and claims).
          NOT skipped when a fitness ruling is woolly: "probably fine" is a
          DEFECT, not an answer. Sharpen the A until it says what it KILLS.
          Either way the [REVISE] _LOG entry carries its `workers:` proof line.
  │
  ▼
CHECK ──→ GATE 2. Present the exit gate per ../../../wiki/08-stage-gate.md,
          around the load-bearing sentence below.
          (internally calls /haipipe-paper-check)
```

Phase visibility per the Phase Transition Contract in `../../../wiki/08-stage-gate.md`: announce every phase boundary (reply line + `[PHASE]` entry in `_LOG` + phase-line 🔥 moves); skip a phase only by an explicit logged verdict (`[PROBE] skipped -- <reason>`, phase line shows `--`); CHECK is never implicit -- it opens by presenting the exit-criteria report and the approval ask.

Comment lifecycle per `../../../wiki/02-comment-lifecycle.md`: comments live in 1-resource.md while active, move to _LOG on resolve, each phase starts clean.

## GATE 2 (CHECK)

The load-bearing sentence of the whole stage. CHECK asks exactly this, verbatim:

```text
Does every hypothesis have a resource that is HAVE+FIT,
or a COMMISSIONED build with an owner and a DATE,
or a SCOPE CUT the human said out loud?
```

It does NOT ask "are the resources BUILT?".
That is unanswerable in a turn when a build takes three weeks, and a stage that waits on it is a stage that never closes.
The sentence above is answerable in MINUTES even when the work takes WEEKS.

Rulings that follow directly:

- `commissioned` + owner + eta-in-the-future -> **PASS**.
- `commissioned` with no owner -> **FAIL**. An unowned build is a wish.
- `commissioned` whose `eta:` has PASSED with no receipt -> **HARD FAIL at the next gate** (JL ruling C6). Without the date test, `commissioned` becomes the status every un-run probe wears, and the whole mechanism ships as a LAUNDERING TOKEN. Already implemented in `check-probe-cards.sh`.
- A fitness ruling that does not say what it KILLS -> **FAIL**.
- A demand with NO resource is **NOT a failure**. It is a SCOPE CUT, said out loud, logged in `_LOG`. The paper gets smaller; the paper does not get wrong.
- Every BUILD section missing `cross-project:` -> **FAIL**.
- A `commissioned` BUILD section with no `[GATE] spend-authorized` line in `_LOG` -> **FAIL**. It was dispatched behind the human's back, and a gate that can be walked around is not a gate.

CHECK RUNS the checker and SHOWS its output; it never eyeballs sections:

```sh
# Locate layout-agnostically -- installed skills flatten the tree, so a hard-coded
# relative path is fragile. Glob for it -- but glob UNAMBIGUOUSLY: TWO files named
# check-probe-cards.sh exist on disk (paper's, and the APPLICATION family's), so a
# bare `-name check-probe-cards.sh | head -1` can resolve to the WRONG FAMILY and
# silently check this paper against application invariants. Filter on the path.
CHK=$(find ~/.claude/skills "$CLAUDE_PLUGIN_ROOT" "$CLAUDE_SKILL_DIR/../../../.." \
        -path "*haipipe-paper-probe*" -name check-probe-cards.sh 2>/dev/null | head -1)
[ -n "$CHK" ] || { echo "FAIL: paper checker not found"; exit 1; }

sh "$CHK" <paper_root> --stage resource
```

Fail LOUDLY when the checker is not found. A gate that cannot run its checker has not checked anything, and a silent skip is exactly how a green gate ships over an un-run probe.

`--stage resource` is not optional. Without it, one in-flight BUILD reds the gate of EVERY downstream stage for as long as the build runs, and every other stage's un-run sections red THIS one.

## Location

```text
<paper>/0-lifecycle/1-resource/1-resource.md          the resource contract (2 sections)
<paper>/0-lifecycle/1-resource/_LOG_1-resource.md      phase progress journal
<paper>/1-probes/PPNN_<topic>.md                   probe files; one SECTION per approved Q,
                                                       OPENED by the PROBE WORKER's ORGANIZE
                                                       stage intake. The executor picks the type
                                                       and topic. This stage never writes one.
```

The SECTION and the Q point at each other, and both receipts are required:
the worker writes `-> PP<NN>` into the Q (proof it was ASKED) and, when the answer lands, writes the `A:` back under the Q (proof it was ANSWERED).

Markdown only (argument documents don't need compilation).

## Template

The canonical template is the source of truth for section order: `ref/resource-template.md`

```markdown
1-resource: <paper title> (what must EXIST for this paper to be testable)
=========================================================================

Date: YYYY-MM-DD
Status: DRAFT


Demand
------

What we MIGHT NEED. One N<n> per hypothesis, derived from the seed's Tentative Claim Shape.

**N1 (H1)** <the resource, and the property that makes it usable>
**N2 (H1)** ...
**N3 (H2)** ...


Questions
---------

What we need to KNOW. One Q<n>, keyed to the N it serves; its A lands when the answer does.
YOU write no PP ids and no probe topics. The PROBE WORKER opens the SECTION and writes
the `-> PP<NN>` backlink in; the EXECUTOR it dispatches to picks the shape of the work.

**Q1 (N1)** <question -- as YOU write it at DRAFT: no backlink yet>

**Q2 (N1) -> PP07** <question -- ASKED: the worker opened the section in PP07 and wrote the backlink>

**Q3 (N2) -> PP08** <question -- ANSWERED: the worker wrote the A back>

A: <the answer -- existence AND fitness, and what it KILLS>
```

**The `-> PP<NN>` backlink is not decoration -- it is the receipt the CHECK gate tests.**
At CHECK, every Q must carry an `A:` (answered), or a `-> PP<NN>` backlink to a probe file that EXISTS (asked), or a DECLINED line in `_LOG` (the human said no at GATE 1).
A Q with none of the three is an UNASKED QUESTION and `check-probe-cards.sh --stage resource` FAILs it by name (`unasked-question(Q3)`).
Neither the backlink nor the A is written BY THIS STAGE: the probe worker writes both. This stage writes only the Q.

A full worked instance of this artifact (real, the SPEC OF RECORD) lives in `../../../../diagram/260714-resource-stage/02-worked-example.txt` — read it to see a Q whose `A:` blocks a fit before it burns a training pass.

## Principles

1. **The stage ASKS; the probe layer ROUTES.** Write Q ids. Never mint a PP id, never pick a probe topic. The chain is: DRAFT asks (Q) -> GATE 1 approves -> the PROBE WORKER opens the SECTION and writes the `-> PP<NN>` backlink -> ② MATCH resolves it or ③ DISPATCH commissions it -> the answer lands as a QA file -> ⑤ INTERPRET writes the A back into the Q. The section lives in the paper's OWN `1-probes/` pool and PP numbers are paper-local footnote numbers, which is also why this stage can never collide with a sibling paper's ids.
2. **Exactly two sections.** Demand (N<n>) and Questions (Q<n> + A). Kill Conditions, Setup Contract, a Resource Ledger, a Binding table, and every sidecar were CUT BY JL on 2026-07-14. Do not reintroduce them under any name. "Do we have it?" and "does it WORK?" are BOTH the A.
3. **Keyed on H<n>, not C<n>.** C-ids do not exist yet at resource time. Demanding them forces a retro-fitted claims ledger -- the exact ordering failure this stage prevents.
4. **The cleavage rule is the constitution.** A question that CHANGES what exists on disk is RESOURCE. A question that READS what exists and MOVES A CLAIM'S STATUS is CLAIMS. `task-for-data` / `task-for-algo` / `task-for-fit` live here; `task-for-eval` does NOT.
5. **Resource may NOT commission `task-for-eval`.** The one rule that stops the stage swallowing the paper. Fit makes the model; eval makes the evidence; a bundled fit+eval entangles the judgment (PP04's null was uninterpretable precisely because of this).
6. **Resource NEVER EXECUTES.** No `/haipipe-data`, no `/haipipe-nn`, no `/haipipe-task`, no task scaffolding, no inline store scan. It writes questions; the PROBE worker dispatches them (LAW 1).
7. **DRAFT may orient; PROBE must dispatch.** Inline glob/WebSearch is legitimate DRAFT fuel. It is NEVER evidence and never lands in an A. PROBE is exactly one worker call.
8. **`cross-project:` is MANDATORY on every BUILD question.** A named sibling-project path or `none-found`. Empty is a FAIL. This is how JL's 2026-07-05 ruling (cross-project reuse is a USER decision; MATCH may NAME a source but not CONSUME it) reaches the gate that authorizes spend -- GATE 1b, which is the only gate that can SEE it, because the MATCH that NAMES it does not run until PROBE.
9. **SCAN blocks; BUILD does not -- so the SPEND decision goes BETWEEN them.** A SCAN question whose route exceeds ~1 HOUR is MISFILED -- re-route to BUILD or shrink the question. A BUILD is non-blocking, ALWAYS. PROBE therefore runs in TWO passes: the SCAN pass lands the answers (including every BUILD row's `cross-project:` candidate), then **GATE 1b** takes the human's INFORMED per-row decision (build it · cut it · authorize reuse), then the BUILD pass dispatches. **NO BUILD-LANE SECTION MAY BE DISPATCHED BEFORE `[GATE] spend-authorized` EXISTS IN `_LOG_1-resource.md`.** GATE 1 approves the QUESTIONS; GATE 1b approves the SPEND. Authorizing spend at GATE 1 would be authorizing it BLIND.
10. **A woolly fitness ruling is a defect.** "Probably fine" is not an answer. An A must say what it KILLS.
11. **A demand with no resource is a SCOPE CUT, not a failure.** Said out loud, at the gate, logged. Free here; costs a CLAIM after claims; costs a FIGURE after display.
12. **`commissioned` is not a laundering token.** Owner + eta + blocks, and the eta must still be in the FUTURE. Overdue with no receipt is a HARD FAIL at the next gate (C6).
13. **Venue-FREE.** What a paper needs to exist does not depend on where you send it. Do not reference a target venue here.
14. **One sentence per line.** Semantic line breaks. No dense multi-sentence paragraphs.
15. **Heading style.** `=====` for the document title, `-----` for the two sections. Sub-items as `**bold**`. No `#`/`##`/`###`. No tables.

## Handoff

On CHECK confirm, update `STATUS.md` (`current_layer`, `maturity`) and take ONE of three exits.

```text
proceed  -> /haipipe-paper claims <paper-dir>       the normal forward gate
                                                    maturity: resource

reseed   -> [LOOPBACK -> SEED] /haipipe-paper seed <paper-dir>
                                                    EVERY demand row is UNOBTAINABLE.
                                                    The paper cannot be written as seeded.
                                                    🔥 moves back to seed; 🚀 stays at the frontier.

park     -> maturity: resource-blocked              the demand is real, the resource is in
                                                    flight or behind a DUA, and there is
                                                    nothing to do but wait.
```

These three exits AMEND the Stage Exit Invariant in `../../../wiki/08-stage-gate.md`, which otherwise admits only "backward within the stage" and "forward across the gate" (JL ruling C7).
A stage whose PURPOSE is discovering that the paper CANNOT BE WRITTEN must be able to SAY SO.
Without `reseed` and `park` it could only `promote -> claims`, mechanically handing a DEAD PAPER FORWARD -- which is the failure this stage was built to end.

End the reply with the stage strip (run `../../../haipipe-paper/stage-strip.sh`).

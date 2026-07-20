---
name: haipipe-probe
description: "The probe layer: a consumer-level Q/A map (papers/<P>/ or applications/<A>/1-probes/PPNN_<topic>.md) that binds each question a paper or application cannot answer itself, by PATH, to a QA file in the probe-unaware task/discovery bank. Owns the probe-file anatomy, the five-step loop, the cost ladder, the QA state-line contract, the two LAWS, and the checker's FAIL conditions. Trigger: probe, probe file, PPNN, q-executor, a-consumer, QA file, qa verb, state, working, answered, superseded, evidence, /haipipe-probe."
argument-hint: "[contract | anatomy | status | \"<question>\"]"
allowed-tools: Bash, Read, Grep, Glob, Agent, Skill
metadata:
  version: "9.6.0"
  last_updated: "2026-07-19"
  summary: "The probe layer, operational form. A probe maps a question to a QA file in the probe-unaware bank — communication, not judgment. Spec + rationale: ../../../diagram/260714-probe-qa/. History: ./CHANGELOG.md."
---

Skill: haipipe-probe — the probe layer
======================================

A probe maps a question your paper or application cannot answer itself to an answer in the bank.
It lives in the consumer, one file per topic, and binds each question by PATH to a QA file that the executor wrote.
A probe is COMMUNICATION between a consumer and an executor — it carries a question out and an answer back, and nothing else.

Spec and rationale (why it is built this way): `../../../diagram/260714-probe-qa/`.
This file is the operational form and the vocabulary source; where another skill disagrees, this file wins.

⚠️ ONE SOURCE FOR THE VOCABULARY.
The task/discovery twins, the `qa` verbs, the probe workers, and `check-probe-cards.sh` COPY the canonical strings from here.
Change a `state:` value, a field name (`state:` / `started:` / `by:`), the TTL constant `QA_WORKING_TTL_HOURS`, the timestamp format `YYYY-MM-DDTHH:MM`, or the `set -C` idiom HERE, then propagate.


What a probe is
===============

```text
   YOUR PAPER / APPLICATION                THE BANK  (task = discovery, probe-UNAWARE)
   ────────────────────────                ──────────────────────────────────────────
   1-probes/PP03_welldoc.md                tasks/A03_welldoc_cycle_check/01_column_scan/
     ## QX1  "cycle indicator?"              ├── workflow/plan.yaml · results/   (code)
     ### q-executor ────────────┐            └── QA/1-cycle-indicator.md         (readable)
     ### bank binding · target ─┼───────────────▶ "none — 40 tables scanned"
     ### a-executor: "…"  ◀────────┘   the answer comes back as a FILE the executor wrote
```

The question crosses as a STRING in an agent's prompt (the `q-executor`), never as a file on the bank side.
The bank never learns probes exist: no mailbox, no back-reference, no probe id under `tasks/` or `discoveries/`.
The answer comes back as a QA file the executor wrote for its own reasons — readable, general, with no consumer in it.
That asymmetry is the whole design: the same answer is reusable, because two consumers read the same file differently.

YOUR QUESTION AND THE EXECUTOR'S QUESTION ARE NOT THE SAME QUESTION.
Yours carries the STAKE — "does WellDoc have a cycle column? (my claim C6 dies if it does)".
The executor must never see that stake, or it shapes the answer around your hypothesis.
So the probe writes a Q-EXECUTOR: the SAME question in plain, general language — "scan the WellDoc tables for a cycle column; report present or absent" — with the stake stripped out.
The q-executor is the executor-facing question, and the ONLY thing that crosses to the bank.
Writing it — your question → the q-executor — is the probe's core act.

The probe does NOT judge.
It carries the answer (`### a-executor`, a copy of the QA answer) back to the consumer, which interprets it into its own a-consumer in the stage doc; whether that settles a claim is the consumer's own business, in its own `1-claims.md`, and never the probe's.

THE FOUR FORMS — a question and its answer, on each side of the wall:

```text
                 CONSUMER (holds the stake)          EXECUTOR (never sees it)
                 ──────────────────────────          ────────────────────────
   QUESTION      Q-consumer            ──T1 strip──────▶  Q-executor = `### q-executor`
                 (stage doc, per consumer)                 the ONLY thing sent to the bank
   ANSWER        A-consumer            ◀──T2 interpret──  A-executor = `### a-executor`
                 (stage doc, per consumer)                 (a copy of the QA file's ## Answer)
```

The probe file holds the EXECUTOR side of both — `### q-executor` (the question OUT) and `### a-executor` (the answer BACK, copied in as the consumer-side single source of truth).
The CONSUMER side of both lives in the stage doc: the Q-consumer (the question, with its stake) and the A-consumer (the per-consumer interpretation, station ②).
One q-executor may serve SEVERAL Q-consumers — many consumer questions reduce to the same executor question — so the probe entry lists them and copies each in.
The two arrows are the two loop steps: T1 = ① ORGANIZE (write `### q-executor`), T2 = ⑤ INTERPRET (write `### a-executor`, a copy of the QA answer; each consumer then writes its own a-consumer in its stage doc).
Q-consumer is where a stage RAISES its questions: literally the `Q-consumer` section in a stage doc (was "Probes"), the same in paper and application.

The `Q-consumer` section lives at the END of every stage doc — the DRAFT-time list of the questions the stage raises, one `##` subsection each, with an id, a title, and what the question wants (the `Answer:` lands later, at PROBE — see **The answer's three stations** below):

```text
   ## Q-<Stage>-<n> · <question title>
   <what this question wants to know — plain words, one sentence per line>
```

The Q-consumer id is CONSUMER-LOCAL — `Q-Seed-1`, `Q-Claim-6` (paper); each family owns its own scheme and the ids never collide across consumers, because a Q-consumer id (like a PP number) never crosses the wall. Only the `q-executor` is shared vocabulary. (The `resource` stage already numbers this way.)

DRAFT WRITES THE WHOLE PLAN — the draft prose, the Q-consumer questions, AND their probe plan — so ONE human gate reviews draft + probe plan together (the plan-review gate is MERGED into the DRAFT gate, never a second gate). For each question DRAFT runs the loop's first two steps:
- ① ORGANIZE — turn the Q-consumer into a probe ENTRY (below): find-or-open its `## QX<n>`, write its `### q-executor` (the stake stripped out, plus the Deliverable / Accepted lines), copy the Q-consumer's original wording under `### q-consumer`, and choose its `route` (`task | discovery`). If an existing q-executor already asks it, just add a `### q-consumer` bullet — no new entry.
- ② MATCH — root the question to a SPECIFIC bank folder (a read-only grep of `QA/*.md` is legal — LAW 1 bans the pen and the run, not the eye): `bank` records the verdict (`reuse | run | code | new`), and `target` is set to the existing QA path or `NEW <path>`.

`route` and the `bank` verdict are AUTHORITATIVE — at plan time the consumer already knows which bank/partition holds the answer, so the executor EXECUTES that plan rather than re-deciding it.
Before the gate, DRAFT SELF-REVIEWS its output: a review sub-agent in a FRESH context (a creator/reviewer split — the drafter does not grade its own work) checks the draft against the stage's artifact spec and the probe plan against **The DRAFT self-review checklist** below, and returns PASS or an issue list; the drafter fixes and re-reviews (bounded) so what reaches the human is already clean of mechanical defects. The self-review PRECEDES the human gate; it never replaces it.
APPROVE is the HUMAN gate at the DRAFT│PROBE boundary: the consumer (a person) reviews the draft AND the probe plan and approves which questions to pursue — the agent never self-advances. Only APPROVED sections go on.
PROBE then RUNS FORWARD (no re-planning, no second gate; it stays a milestone): ③ DISPATCH the `new`/`run`/`code` entries (`target: NEW`), ④ POINT their `target`, ⑤ INTERPRET (copy the QA answer into `### a-executor`).
Ids: three LOCAL layers, none crossing the wall — `Q-<Stage>-<n>` in the stage doc (consumer-local), `QX<n>` in the probe file (topic-local), `QA/<n>-<slug>.md` in the bank (task-folder-local). They bind by PATH (`target`), never by a shared id. Each stage-doc `Q-<Stage>-<n>` gains a `→ 1-probes/PPnn · QX<n>` pointer, and its `state` is DERIVED — that state, not an empty `target`, marks a planned-but-unrun entry, because DRAFT now writes `target`.

The DRAFT self-review checklist
-------------------------------

The pre-gate self-review reads and judges what `check-probe-cards.sh` cannot; the checker still runs at CHECK as the mechanical backstop, and the two are complementary. A review sub-agent (fresh context) runs it per question SECTION, plus per file:

Per SECTION:
- `q-executor:` is CLEAN (LAW 2) — no claim ids, no "our / this paper", no stake, no hint of the wanted answer; a stranger could answer it.
- the question is ANSWERABLE + SPECIFIC — a concrete check with a definite result, not broad or ambiguous.
- `route` is set (`task | discovery`).
- `bank` is judged by READING a SPECIFIC candidate folder ON THE ANSWER (topic-similarity is not a hit): `reuse`/`run`/`code` names the folder; `new` says nothing exists.
- `target` agrees with `bank` (an existing QA path for reuse/run/code, or `NEW <path>` for new).
- each `### q-consumer` bullet copies in a real stage-doc Q-consumer (id + its original question); the strip lost nothing and leaked no stake.
Per FILE:
- no stake anywhere — it stays in the stage-doc Q-consumers; only `### q-executor` text is dispatch-bound.

The stage's DRAFT worker adds the draft-PROSE checks (its own artifact spec). Issues → the drafter fixes → re-review (bounded); the verdict rides to the human gate.

The answer's three stations
---------------------------

An answer returns from the bank and lands in THREE places — each a more integrated FORM of the same fact, each ANCHORED to the one before, so a copy can never drift or be fabricated:

```text
  🏦 QA file  ─▶  ① PROBE FILE           ─▶  ② Q-consumer Answer      ─▶  ③ STAGE CONTENT
  (bank)          ### a-executor: "12.9…"    Q-Claim-6 Answer: 12.9…      "…prescribe 12.9 more
                  [→ target QA file]         [source: PPnn]               MME (N=766k)…"
  form:           the copy = single truth     the per-consumer Q&A         the reader-facing prose
  written at:     ⑤ INTERPRET (PROBE)         PROBE/REVISE (beside ①)      REVISE (weave + discharge)
```

- **① probe file** — `### a-executor`, a COPY of the QA answer, anchored to the `target` QA file: the consumer-side single source of truth, reusable by every Q-consumer this q-executor serves.
- **② Q-consumer `Answer:`** in the stage doc, PER CONSUMER, carrying a `[source: PPnn]` anchor to ①: the answer recorded NEXT TO its question, so the stage doc is a self-contained Q&A. A copy, but ANCHORED — the anchor points at ①, which points at the QA file, so nothing drifts or is fabricated.
- **③ stage content** — the answer WOVEN into the sentence(s) that cite `[Q<n>]`, citation discharged.

Each hop is a copy anchored to the last, so the whole chain is self-contained AND traceable — you can walk content → a-consumer → a-executor → QA to see where any error entered. The STAKE never enters this chain; it stays in the stage-doc Q-consumer. Same three stations in paper and application.


The probe file
==============

`papers/<P>/1-probes/PPNN_<topic>.md`, or identically `applications/<A>/1-probes/PPNN_<topic>.md`.
One file per TOPIC; each ENTRY is one Q-EXECUTOR (the file is Q-executor-oriented — the consumers hang off it).
PP numbers are consumer-local footnote numbers — two consumers may both carry a PP04, and nothing collides because no PP id ever crosses to the bank.
The stake lives in each Q-consumer, in the stage doc, not here.

Fillable form + rules: `ref/probe-template.md`. An entry is `## QX<n>` + four `###` subsections; no markdown tables.

```text
   # PP03 — WellDoc data feasibility

   ## QX1 — cycle indicator          ← topic-local q-executor id (QX1, QX2 … within this file)

   ### q-executor                    ← the question in general language, FROZEN — the dispatch payload
   Scan all 40 WellDoc CSV tables for menstrual/cycle/hormone columns. Report which exist, or none.
   Deliverable: QA digest + machine artifact. Accepted: present | absent.

   ### q-consumer                    ← who needs it; each bullet copies in that consumer's ORIGINAL question
   * Q-Claim-6 — does WellDoc have a cycle column? (C6 dies if it does)
   * Q-Seed-1 — is menstrual-cycle-labelled external data obtainable?

   ### bank binding
   **route**: task                   ← the dispatch door (AUTHORITATIVE), chosen at DRAFT
   **bank**: reuse                   ← reuse | run | code | new — what the bank needs (the DRAFT verdict)
   **target**: tasks/A03_welldoc_cycle_check/01_column_scan/QA/1-cycle-indicator.md
   **state**: read                   ← DERIVED from disk, never asserted

   ### a-executor                    ← a COPY of the QA file's answer, written at harvest
   No cycle column in 40 tables.
```

An entry's parts (`## QX<n>` + four `###` subsections), all but `### a-executor` authored at DRAFT:
- `### q-executor` — the executor-facing question (plain, general, no stake), frozen once written; the ONLY thing dispatched, and the ONLY shared (cross-consumer) form. Carries its own `Deliverable:` and `Accepted: a | b` lines.
- `### q-consumer` — one bullet per Q-consumer this q-executor serves: the stage-doc id + that consumer's ORIGINAL question, copied in (review-only, never dispatched). One q-executor may serve several — that is reuse, structurally. A stage gate greps these ids for its stage token (Q-Seed-1 → seed).
- `### bank binding` — four `**field**:` lines:
  - `route` — the dispatch door, `task | discovery`, chosen at DRAFT; AUTHORITATIVE (the executor executes it, not re-decides).
  - `bank` — the DRAFT verdict, read-only-grep judged: `reuse` (a results folder already answers it), `run` (folder + code exist, needs a run), `code` (folder exists, code needs a change first), `new` (nothing exists, create a folder). The plan; `state` is where it is now.
  - `target` — a PATH to the answering QA FILE; `NEW <path>` while it does not exist yet, `NEW ?` while even the folder is undecided. Point at the FILE, never the folder.
  - `state` — `planned | commissioned | answered | read | answered-local | failed`; derived from disk, never asserted. This — not an empty `target` — marks a planned-but-unrun entry.
- `### a-executor` — a COPY of the answering QA file's answer, written at harvest (PROBE); empty until answered. The consumer-side single source of truth. Each Q-consumer then writes its own a-consumer in its stage doc (station ②), anchored `[source: PP<NN>]` back to this copy.

The STAKE never appears in a probe file — it lives in each Q-consumer, in the stage doc.

(An entry may also carry optional `**values**:` / `**sources**:` / `**displays**:` pointers under `### bank binding`. Those are HARVEST-LANE fields — how the consumer later pulls a number, a citation, or a figure out of the answer — and they belong to the probe WORKERS, not to this model. See the workers.)


BUILD-LANE FIELDS.
A section whose answer legitimately takes DAYS-TO-WEEKS additionally carries, and ONLY at `state: commissioned`:

```text
   **owner**: <who> · **eta**: YYYY-MM-DD · **blocks**: <the claim/demand ids it gates>
   **cross-project**: <sibling-project path NAMED as a reuse candidate, or `none-found`>
```

A section still `commissioned` when a gate runs is build-lane by definition, so these four fields are unconditional there.
`cross-project:` is how a named sibling-source candidate reaches the one human gate that authorizes SPEND — the MATCH may NAME it but never CONSUME it.


The five-step loop
==================

```text
   ① ORGANIZE   collect the DRAFT's questions into probe files (grouped by TOPIC), and
                write each one's `### q-executor` — translate your question into the executor-
                facing form, stripping the stake out; copy the Q-consumer under `### q-consumer`.
   ② MATCH      SCAN the bank's existing QA files FIRST (grep + READ each state line), and set
                `bank` (reuse | run | code | new). If one already answers it, REUSE (point, skip ③).
                Only a `new`/`run`/`code` entry goes on.
   ③ DISPATCH   only for `new`/`run`/`code`: hand the `### q-executor` VERBATIM to the executor
                orchestrator → it returns a QA-file PATH (a new answer, written by the executor).
   ④ POINT      set the entry's `target` at the answering QA file
   ⑤ INTERPRET  copy the QA answer into `### a-executor` (each consumer then writes its own
                a-consumer in its stage doc)
```

The order is the point: ② always precedes ③, so an existing answer is REUSED and only a genuinely new question ever creates new bank work.
PHASE MAP: ①② run at DRAFT (the consumer organizes + roots each of its own questions — a read-only bank grep, LAW 1), so ONE human gate reviews draft + probe plan together; ③④⑤ run at PROBE, which RUNS FORWARD with no second gate.

THE COST LADDER — cheap doors first; only T3/T4 summon an agent.

```text
   T0 JOIN    another q-executor already asks this        → add a q-consumer bullet   ~0
   T1 LOCAL   my own registries answer it                 → answered-local      ~0
   T2 REUSE   an existing QA file answers it              → point the section   1 grep + 1 read
   T3 ENRICH  the task-folder exists, never asked this    → new section → ③     agent
   T4 FRESH   no task-folder                              → new section → ③     agent
```

MOST sections should land on T2: in a healthy project the bank fills on its own, so most answers already exist before anyone asks.
MATCH ON THE ANSWER, NEVER ON THE TOPIC: a HIT counts only if the QA file LITERALLY ANSWERS the question — read it; topic similarity is not evidence.

THE DISPATCH PAYLOAD — copy this block; do not invent variants:

```text
Agent(haipipe-task-orchestrator-agent, prompt="
  action: qa
  project: <project_root>
  question: |
    <the section's q-executor block, VERBATIM. Nothing else.>
  task-folder: <the section's target: — an existing path, `NEW <path>`, or omit if unknown>
")
```

…and identically for `Agent(haipipe-discovery-orchestrator-agent, ...)`.
The executor picks the shape and depth in its own clean context and returns a PATH to the answering QA file.


Phase rules — the followable checklists
=======================================

The sections above are the MODEL; these are the DO-THIS rules a phase worker follows. A stage's DRAFT / PROBE worker POINTS here and adds only its FAMILY-specific rules (paper registries, harvest lanes, …). On any conflict, the model sections above win.

DRAFT phase — author the plan, self-review, stop:
1. Write the stage artifact per the STAGE's own spec (real content; the spec is the stage skill's, not this file's).
2. For each open question: raise a `## Q-<Stage>-<n>` in the stage doc's Q-consumer AND author its probe ENTRY — ① find-or-open `## QX<n>`, write `### q-executor` (stake stripped) + copy the Q-consumer under `### q-consumer` + choose `route`; ② judge `bank` against a SPECIFIC folder (read the candidate, ON THE ANSWER) + set `target` (an existing path, or `NEW <path>`).
3. NEVER write `### a-executor` — that is PROBE's ⑤ harvest. An entry is left `planned` (a `NEW` target) or `answered` (an existing target), never `read`.
4. Before the gate, SELF-REVIEW the draft + plan (fresh-context sub-agent; see **The DRAFT self-review checklist**); fix + re-review, bounded.
5. STOP at the human gate; never self-advance.

PROBE phase — run the plan forward, harvest, verify:
1. READ the DRAFT-authored entries; do NOT re-author or re-match them (`route` / `bank` are AUTHORITATIVE).
2. ③ DISPATCH only the `target: NEW` entries — hand the `### q-executor` VERBATIM to the collector agent (LAW 1: never run bank work inline). An already-`answered` target skips to ④/⑤.
3. ④ POINT `target` at the answering QA file, then OPEN it and read its `state:` line (an `ls` is not enough).
4. ⑤ INTERPRET — copy the QA answer into `### a-executor` (ONLY against an `answered`, non-superseded target); each consumer then writes its own a-consumer (station ②), then the family harvest.
5. LAW 2 holds on both surfaces: the `### q-executor` carries no stake; the QA file carries no consumer vocabulary.
6. VERIFY with `check-probe-cards.sh` before the stage's CHECK gate.


The QA file — the bank's answer
===============================

Every executor task-folder MAY carry a `QA/` folder (task and discovery, same shape); not every one does.
`QA/<n>-<slug>.md`, where `n` is creation order — `ls QA/` IS the index. Slug only, never a PP id.

A QA file is a TICKET that becomes a RECEIPT: exactly ONE mutable field, the `state:` line.

```markdown
# Q — <the question, restated by the EXECUTOR in its own words>
- state:   working | answered | superseded-by: QA/<m>-<slug>.md
- started: 2026-07-14T09:12          ← MANDATORY while state: working
- by:      <run id | agent | human>  ← optional

## Answer     empty while working; filled at the executor's Report. plain words + [→ results/<file>] anchors
## Caveats    what this does NOT establish
## Not-done   what was asked but not resolved, and why
```

ONE WRITER — the EXECUTOR, for the whole life of the file.
It writes twice: the CLAIM (`state: working` + `started:`) when it starts, and the COMPLETION (`state: answered` + the body) at its Report.
⛔ A CONSUMER never creates, claims, edits, completes, or supersedes a QA file — a probe that finds a stale target re-points its OWN section, never the file.

THE CLAIM MUST EXPIRE.
`QA_WORKING_TTL_HOURS = 24` — a `working` file whose `started:` is older is STALE and restartable.

THE RACE GUARD — `set -C` (noclobber), and nothing more.
Two runs may both pick `QA/3-`; the claim is created under noclobber, and the loser re-scans and defers.

SUPERSESSION.
A later run whose answer CHANGES writes a NEW file and appends `superseded-by: QA/<m>-<slug>.md` to the OLD file's state line; the body is never rewritten.

The executor-side flow that WRITES these files (the qa verb: scan → digest → run) lives in `../../task/haipipe-task/fn/qa.md` and its discovery twin.


The two LAWS
============

LAW 1 — A CONSUMER SESSION NEVER RUNS BANK WORK INLINE.
Dispatch means hand the `### q-executor` VERBATIM, and nothing else — never the `### q-consumer` copies, never the probe file, never the paper.
It is broken the moment a consumer session runs bank work or writes a bank file (including a QA digest it thinks it is being helpful by authoring).
A read-only grep of `{tasks,discoveries}/**/QA/*.md` is LEGAL and REQUIRED — that IS step ② MATCH. The wall bans the PEN and the RUN, not the EYE.

LAW 2 — BACKSTOP LINT, ON TWO SURFACES.
Q-executor blocks carry no claim ids and no stake words ("rescue", "we want", "the hoped-for").
The bank's `QA/*.md` carry no consumer vocabulary (claim ids, "the paper" meaning *our* paper).


Section state, derived from disk
================================

State is never a claim about an agent; it is checkable on disk, and the reader OPENS the file — an `ls` is not enough.

```text
   planned         the section exists; the target task-folder is missing (or `NEW …`)
   commissioned    the task-folder exists with no answered QA file yet, OR the target QA file is `working`
   answered        the target QA file exists AND is `state: answered`
   read            the entry's `### a-executor` is non-empty — LEGAL ONLY against an `answered`, non-superseded target
   answered-local  target points into the consumer's own registries; no dispatch
   failed          a dead target · the task-folder was deleted · the executor REFUSED
```

THE CHECKER — `check-probe-cards.sh` enforces these (each FAILs, exit 1):
`read-target-working` · `read-target-superseded` · `qa-working-no-started` · `qa-working-expired` · `qa-answered-empty` · `qa-no-state` · `commissioned-target-answered`, plus the build-lane `commissioned-no-owner` / `-no-eta` / `-no-blocks` / `-no-cross-project`.


Verbs
=====

```text
   /haipipe-probe                    → this file, the operational contract
   /haipipe-probe contract|anatomy   → the probe-file anatomy + the QA contract
   /haipipe-probe status             → derive states from disk: ls the 1-probes/ files, resolve each
                                       target:, ls the QA files. Never a stored state.
   /haipipe-probe "<question>"       → ROUTE, do not execute. A question with no consumer behind it is not
                                       a probe — hand it to the executor's own door: task-shaped →
                                       /haipipe-task qa, discovery-shaped → /haipipe-discovery qa.
```


Pointers
========

```text
   spec + rationale (why it is built this way)  → ../../../diagram/260714-probe-qa/
   the PROBE-phase workers that run the loop     → ../../paper/2-phase/1-probe/haipipe-paper-probe/
                                                   ../../application/2-phase/1-probe/haipipe-application-probe/
   the question-level collector agent (②③④,       → ../agents/haipipe-probe-q-executor-agent.md
     stake-free, shared, isolated context)
   the executor-side qa verb (writes QA files)   → ../../task/haipipe-task/fn/qa.md  ·  the discovery twin
```

---
name: haipipe-probe
description: "The probe layer: a consumer-level Q/A map (papers/<P>/ or applications/<A>/1-probes/PPNN_<topic>.md) that binds each question a paper or application cannot answer itself, by PATH, to a QA file in the probe-unaware task/discovery bank. Owns the probe-file anatomy, the five-step loop, the cost ladder, the QA state-line contract, the two LAWS, and the checker's FAIL conditions. Trigger: probe, probe file, PPNN, commission, reading, QA file, qa verb, state, working, answered, superseded, evidence, /haipipe-probe."
argument-hint: "[contract | anatomy | status | \"<question>\"]"
allowed-tools: Bash, Read, Grep, Glob, Agent, Skill
metadata:
  version: "9.0.0"
  last_updated: "2026-07-15"
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
     ## Q1  "cycle indicator?"               ├── workflow/plan.yaml · results/   (code)
     - commission ──────────────┐            └── QA/1-cycle-indicator.md         (readable)
     - target: ─────────────────┼───────────────▶ "none — 40 tables scanned"
     - reading: "…"  ◀──────────┘   the answer comes back as a FILE the executor wrote
```

The question crosses as a STRING in an agent's prompt (the `commission`), never as a file on the bank side.
The bank never learns probes exist: no mailbox, no back-reference, no probe id under `tasks/` or `discoveries/`.
The answer comes back as a QA file the executor wrote for its own reasons — readable, general, with no consumer in it.
That asymmetry is the whole design: the same answer is reusable, because two consumers read the same file differently.

The probe does NOT judge.
It carries the answer's interpretation (`reading`) back to the consumer; whether that settles a claim is the consumer's own business, in its own `1-claims.md`, and never the probe's.


The probe file
==============

`papers/<P>/1-probes/PPNN_<topic>.md`, or identically `applications/<A>/1-probes/PPNN_<topic>.md`.
One file per TOPIC; each question is one SECTION.
PP numbers are consumer-local footnote numbers — two consumers may both carry a PP04, and nothing collides because no PP id ever crosses to the bank.

⛔ The words "card", "row", and "table" are BANNED here; it is a probe file holding question SECTIONS, and no markdown tables live inside one.

```text
   # PP03 — WellDoc data feasibility
   - mode: light | full

   ## Why   🔒 the STAKE, in consumer vocabulary. NEVER handed to an executor, NEVER copied anywhere.

   ## Q1 — cycle indicator
   - serves: 1-claims (C6)          ← which stage/claim this question is FOR
   - target: tasks/A03_welldoc_cycle_check/01_column_scan/QA/1-cycle-indicator.md
   - state:  read                   ← DERIVED from disk, never asserted
   - commission: |                  ← the question in general language, FROZEN — the dispatch payload
       Scan all 40 WellDoc CSV tables for menstrual/cycle/hormone columns. Report which exist, or none.
       Deliverable: QA digest + machine artifact. Do-not: no new data pulls. Accepted: present | absent.
   - reading: |                     ← the answer in the consumer's own words, written at harvest
       No cycle column in 40 tables.
```

The section fields:
- `serves:` — which stage or claim of the consumer this question is for; the affinity a stage gate greps.
- `target:` — a PATH to the answering FILE; `NEW <task-folder-path>` while the task-folder does not exist yet. Point at the FILE, never the folder.
- `state:` — `planned | commissioned | answered | read | answered-local | failed`; derived from disk, never asserted.
- `commission:` — the question in general language, frozen once written; this is the dispatch payload and nothing else.
- `reading:` — the answer in the consumer's own words, written at harvest; empty until answered.

`## Why` is the stake, in consumer vocabulary; it NEVER leaves the file and is NEVER handed to an executor.

HARVEST LANES.
`values:` / `sources:` / `displays:` carry pointers that feed the consumer's own `_VALUES_` map, `.bib`/`_CITATION_` docs, and `0-displays/` units.
They are paid by the citation/values/display harvesters, and omitted when a return carries nothing for them.

BUILD-LANE FIELDS.
A section whose answer legitimately takes DAYS-TO-WEEKS additionally carries, and ONLY at `state: commissioned`:

```text
   - owner: <who> · eta: YYYY-MM-DD · blocks: <the claim/demand ids it gates>
   - cross-project: <sibling-project path NAMED as a reuse candidate, or `none-found`>
```

A section still `commissioned` when a gate runs is build-lane by definition, so these four fields are unconditional there.
`cross-project:` is how a named sibling-source candidate reaches the one human gate that authorizes SPEND — the MATCH may NAME it but never CONSUME it.


The five-step loop
==================

```text
   ① ORGANIZE   collect the DRAFT's questions into probe files, grouped by TOPIC
   ② MATCH      grep the bank's QA files; READ each state line; a HIT literally answers THIS question
   ③ DISPATCH   hand the commission VERBATIM to the executor orchestrator → it returns a QA-file PATH
   ④ POINT      set the section's target: at the answering QA file
   ⑤ INTERPRET  write the reading (the answer in the consumer's own words)
```

THE COST LADDER — cheap doors first; only T3/T4 summon an agent.

```text
   T0 JOIN    another section already asks this question  → add my serves:      ~0
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
    <the section's commission block, VERBATIM. Nothing else.>
  task-folder: <the section's target: — an existing path, `NEW <path>`, or omit if unknown>
")
```

…and identically for `Agent(haipipe-discovery-orchestrator-agent, ...)`.
The executor picks the shape and depth in its own clean context and returns a PATH to the answering QA file.


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
Dispatch means hand the `commission` block VERBATIM, and nothing else — never `## Why`, never the probe file, never the paper.
It is broken the moment a consumer session runs bank work or writes a bank file (including a QA digest it thinks it is being helpful by authoring).
A read-only grep of `{tasks,discoveries}/**/QA/*.md` is LEGAL and REQUIRED — that IS step ② MATCH. The wall bans the PEN and the RUN, not the EYE.

LAW 2 — BACKSTOP LINT, ON TWO SURFACES.
Commission blocks carry no claim ids and no stake words ("rescue", "we want", "the hoped-for").
The bank's `QA/*.md` carry no consumer vocabulary (claim ids, "the paper" meaning *our* paper).


Section state, derived from disk
================================

State is never a claim about an agent; it is checkable on disk, and the reader OPENS the file — an `ls` is not enough.

```text
   planned         the section exists; the target task-folder is missing (or `NEW …`)
   commissioned    the task-folder exists with no answered QA file yet, OR the target QA file is `working`
   answered        the target QA file exists AND is `state: answered`
   read            the section's reading: is non-empty — LEGAL ONLY against an `answered`, non-superseded target
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
   the executor-side qa verb (writes QA files)   → ../../task/haipipe-task/fn/qa.md  ·  the discovery twin
```

<!-- TEMPLATE (follow, then delete). Everything above "The filled section" is GUIDANCE — read it,
     then ship only a copy of the filled section. One file per TOPIC; one entry per Q-EXECUTOR.
     Shared by paper + application. The machine anatomy this must satisfy lives in ../SKILL.md
     ("The probe file"); every finished file must pass check-probe-cards.sh. Delete this line. -->

What this file is
=================

A probe file is one TOPIC's list of Q-EXECUTORS.
A Q-executor is a question in its executor-facing form — stripped of stake, ready to send to the bank.
The file collects the q-executors that share a topic, and for each one records who needs it, where it goes in the bank, and the answer that came back.
PP<NN> is a consumer-local number; `ls 1-probes/` is the authority, and no PP number ever crosses to the bank.
There is no `Why` section here — the stake lives in each Q-consumer, in the stage doc, not in this file.

Each q-executor is one `## QX<n>` entry, and its fields are grouped under four `###` subsections:
q-executor (the question), q-consumer (who needs it), bank binding (how it reaches the bank), a-executor (the answer).


Executor side here, consumer side in the stage doc
==================================================

A question has two forms, and so does an answer; this file holds the EXECUTOR side of both.
Q-consumer (stage doc, one per consumer, carries the stake) — strip → Q-executor (here, shared).
A-executor (here, the bank's answer, shared) — interpret → A-consumer (stage doc, one per consumer).
One q-executor may serve SEVERAL Q-consumers, because many consumer questions reduce to the same executor question.
So each entry copies in the Q-consumers it serves — id and original wording — and each of those consumers writes its OWN a-consumer back in its stage doc.


Three homes for the answer, each a copy anchored to the last
============================================================

The answer is copied at each step, and each copy anchors to the one before, so the chain is self-contained and traceable.
QA file answer → a-executor (here, the single source of truth) → a-consumer (stage doc, anchored `[source: PP<NN>]`) → stage content.
`target` is the anchor from the a-executor copy back to the QA file it came from.


The filled section
==================

Copy this shape. One `## QX<n>` entry per q-executor, four `###` subsections each.

# PP<NN> — <topic>
**mode**: light | full

## QX<n> — <short q-executor title>

### q-executor
<the question, stake-free, general language>
Deliverable: <what comes back>
Accepted: <a> | <b>

### q-consumer
* Q-<Stage>-<n> — <that consumer's ORIGINAL question, copied so you see what it asks>
* Q-<Stage>-<n> — <another consumer's original question, if this q-executor serves several>

### bank binding
**route**: task | discovery
**bank**: reuse | run | code | new
**target**: <bank>/<group>/<folder>/QA/<n>-<slug>.md | NEW ?
**state**: planned | commissioned | answered | read | answered-local | failed

### a-executor
<empty until harvest; then a copy of the QA file's answer>


Field guide
===========

QX<n>  (the entry heading)
--------------------------
A topic-local id for this q-executor — QX1, QX2, … within this file.
It is not a Q-consumer id and not a bank id.
Each layer keeps its own local id (Q-Seed-1 in the stage doc, QX1 here, QA/<n> in the bank), and nothing shares an id across the wall.

### q-executor
----------------
The question with the stake stripped out — the only thing dispatched, and the only text shared with the bank.
No claim ids, no "our / this paper", no stake, no hint of the wanted answer; a stranger could answer it.
It carries a `Deliverable:` line and an `Accepted: a | b` line.
Freeze it once written.

### q-consumer
----------------
One bullet per Q-consumer this q-executor serves: the stage-doc id, then that consumer's ORIGINAL question, copied in.
The copy is here so the entry is self-contained — you see what each consumer asked, and you can see how the q-executor was stripped from it.
It is review-only and never crosses the wall (only `q-executor` is dispatched).
One q-executor may list several — that is how reuse shows up structurally.
The checker's --stage gate greps these ids for the stage word (Q-Seed-1 → seed).

### bank binding
-----------------
Four fields that say how this q-executor reaches the bank; all authored at DRAFT.
`route` — which bank: `task` for internal work (data, a run, a regression), `discovery` for outside evidence (prior-art, landscape). Authoritative — the executor runs it, it does not re-decide.
`bank` — what the bank needs, judged by reading it (a read-only grep is allowed): `reuse` (a results folder already answers it), `run` (folder + code exist, needs a run), `code` (folder exists, code needs a change first), `new` (nothing exists, create a folder). This is the plan; `state` is where it actually is now.
`target` — the path to the answering QA FILE, never the folder. `NEW ?` while the folder is undecided; `NEW <path>` once chosen but the QA digest is unwritten. Binding is by path.
`state` — the live lifecycle, derived from disk, never asserted: `planned`, `commissioned`, `answered`, `read`, `answered-local`, `failed`.

### a-executor
---------------
Written at harvest: a COPY of the answering QA file's answer.
This is the consumer-side single source of truth — the paper references it, through the anchor chain, when it writes content.
Empty until the target is `answered`.
Each Q-consumer then writes its own a-consumer in its stage doc, anchored `[source: PP<NN>]` back to this copy.


For the creator (what DRAFT writes, and what PROBE runs)
=======================================================

DRAFT authors the whole plan, so one human gate reviews the draft and its probe plan together.
For each question the draft raised:
  1. Find or open the q-executor entry (`## QX<n>`) — if an existing q-executor already asks it, add a bullet under its `### q-consumer` instead of opening a new entry.
  2. Write `### q-executor` — strip the stake, add the Deliverable and Accepted lines.
  3. Under `### q-consumer`, copy in each consumer's id and original question.
  4. Under `### bank binding`, write `route` and `bank` (read the bank read-only, judge reuse / run / code / new), set `target`, and leave `state: planned`.
  5. Leave `### a-executor` empty.
PROBE then runs the plan forward: it dispatches the `run` / `code` / `new` entries, points each target, and copies the QA answer into `### a-executor`.

Optional fields (add only when they apply)
------------------------------------------
Build-lane, only at `state: commissioned`, for days-to-weeks work: add `**owner**:`, `**eta**:`, `**blocks**:`, `**cross-project**:` under `### bank binding`.
Harvest lanes, when the answer yields reusable artifacts: `**values**:` / `**sources**:` / `**displays**:`, each `harvest: OWED` until its sub-worker accepts it.

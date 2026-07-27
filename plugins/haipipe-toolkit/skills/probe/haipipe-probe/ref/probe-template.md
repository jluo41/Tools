<!-- TEMPLATE (follow, then delete). Everything above "The filled section" is GUIDANCE — read it,
     then ship only a copy of the filled section. One FOLDER per TOPIC; one FILE per Q-EXECUTOR.
     Shared by paper + application. The machine anatomy this must satisfy lives in ../SKILL.md
     ("The probe file"); every finished file must pass check-probe-cards.sh. Delete this line. -->

🧭 What this file is
====================

A probe TOPIC is a FOLDER `1-probes/PPNN_<topic>/`, holding one FILE per Q-EXECUTOR.
A Q-executor is a question in its executor-facing form — stripped of stake, ready to send to the bank.
Each q-executor file records who needs it, its bank binding and returned answer, or the explicit terminal `concern` ruling when no bank can close it; the folder groups the q-executors that share a topic.
PP<NN> is a consumer-local number naming the folder — pick the next free NN (`ls 1-probes/` is the authority; the first topic is `PP01`), and no PP number ever crosses to the bank.
There is no `Why` section here — the authoritative stake lives in each stage-doc Q-consumer.
The original question is copied under `### q-consumer` for review and may retain that stake, but only `### q-executor` is dispatchable.

Each q-executor is one FILE `QXn_<slug>.md`, holding a single `## QX<n>` entry whose fields are grouped under four `###` subsections:
📤 q-executor (the question) · 🙋 q-consumer (who needs it) · 🔗 bank binding (how it reaches the bank) · 📥 a-executor (the answer).
Those four emojis are the map — they mark the same four subsections again in the Field guide below.

ON-DISK LAYOUT — a topic is a FOLDER, one q-executor per file:
  1-probes/PPNN_<topic>/QXn_<slug>.md   ← each file is one `## QX<n>` entry, path-addressable.
`check-probe-cards.sh` globs `PP*/*.md`, and every file carries one `## QX<n>` heading.


🔀 Executor side here, consumer side in the stage doc
====================================================

A question has two forms, and so does an answer; this file holds the EXECUTOR side of both.
Q-consumer (stage doc, one per consumer, carries the stake) — strip → Q-executor (here, shared).
A-executor (here, the bank's answer, shared) — interpret → A-consumer (stage doc, one per consumer).
One q-executor may serve SEVERAL Q-consumers, because many consumer questions reduce to the same executor question.
So each entry copies in the Q-consumers it serves — id and original wording — and each of those consumers writes its OWN a-consumer back in its stage doc.


🪜 Three homes for the answer, each a copy anchored to the last
==============================================================

The answer is copied at each step, and each copy anchors to the one before, so the chain is self-contained and traceable.
QA file answer → a-executor (here, the single source of truth) → a-consumer (stage doc, anchored `[source: PPNN_<topic>/QXn_<slug>.md]`) → stage content.
`target` is the anchor from the a-executor copy back to the QA file it came from.


📋 The filled section
=====================

Create the folder `1-probes/PPNN_<topic>/`, then one file `QXn_<slug>.md` per q-executor. Copy this shape into each file — one `## QX<n>` entry, four `###` subsections.

FORMATTING — every free-text BODY is written one sentence per line (semantic line breaks), never a dense paragraph: the `### q-executor` question, the `### q-consumer` originals, and the `### a-executor` answer. When a body lists sources, one source per bullet.
The `### q-consumer` id is BOLD — `**Q-<Stage>-<n>**` — so it stands out at a glance.
This is checker-safe by construction: the rule touches BODIES only. The machine tokens `check-probe-cards.sh` parses — `## QX<n>`, the four `###` names, and the `**field**:` lines (`**state**:`, `**bank**:`, `**target**:`, …) — are never wrapped or split, and the bold `**…**` is decoration around unchanged id text (the --stage grep is a substring match), so every awk/grep match is unchanged.

--- 1-probes/PP<NN>_<topic>/QXn_<slug>.md  (one file per q-executor; the folder name carries the topic) ---

## QX<n> — <short q-executor title>

### q-executor
<the question, stake-free, general language>
Deliverable: <what comes back>
Accepted: <a> | <b>

### q-consumer
* **Q-<Stage>-<n>** — <that consumer's ORIGINAL question, copied so you see what it asks>
* **Q-<Stage>-<n>** — <another consumer's original question, if this q-executor serves several>

### bank binding
**route**: task | discovery | none (concern only)
**bank**: reuse | run | code | new
**target**: <bank>/<group>/<folder>/QA/<n>-<slug>.md | NEW ?
**state**: planned | commissioned | answered | read | answered-local | deferred | failed | concern

### a-executor
<empty until harvest; then a copy of the QA file's answer — one sentence per line, one source per bullet>


📖 Field guide
==============

🔖 QX<n>  (the entry heading)
-----------------------------
A topic-local id for this q-executor — QX1, QX2, … within its topic folder.
It is not a Q-consumer id and not a bank id.
Each layer keeps its own local id (Q-Seed-1 in the stage doc, QX1 here, QA/<n> in the bank), and nothing shares an id across the wall.

📤 q-executor  (the question OUT)
---------------------------------
The question with the stake stripped out — the only thing dispatched, and the only text shared with the bank.
No claim ids, no "our / this paper", no stake, no hint of the wanted answer; a stranger could answer it.
It carries a `Deliverable:` line and an `Accepted: a | b` line.
Freeze it once written.

🙋 q-consumer  (who needs it)
-----------------------------
One bullet per Q-consumer this q-executor serves: the stage-doc id in BOLD — `**Q-<Stage>-<n>**`, so it stands out — then that consumer's ORIGINAL question, copied in.
The copy is here so the entry is self-contained — you see what each consumer asked, and you can see how the q-executor was stripped from it.
It is review-only and never crosses the wall (only `q-executor` is dispatched).
One q-executor may list several — that is how reuse shows up structurally.
The checker's --stage gate greps these ids for the stage word (Q-Seed-1 → seed); the bold `**…**` around the id does not affect that substring match.

🔗 bank binding  (how it reaches the bank)
------------------------------------------
Normal entries use four fields that say how this q-executor reaches the bank; all are authored at PROBE (①②).
A terminal `concern` uses only `route: none` plus `state: concern` because no bank or target exists.
`route` — which bank: `task` for internal work (data, a run, a regression), `discovery` for outside evidence (prior-art, landscape). Authoritative — the executor runs it, it does not re-decide. Use `none` only for terminal `concern`.
`bank` — what the bank needs, judged by reading it (a read-only grep is allowed): `reuse` (a specific existing QA file answers it), `run` (folder + code exist, needs a run), `code` (folder exists, code needs a change first), `new` (nothing exists, create a folder). This is the plan; `state` is where it actually is now.
`target` — the path to the answering QA FILE, never the folder. `NEW ?` while the folder is undecided; `NEW <path>` once chosen but the QA digest is unwritten. Binding is by path.
`state` — the live lifecycle: `planned`, `commissioned`, `answered`, `read`, `answered-local`, `deferred`, `failed`, `concern`.
All bank-facing values are derived from disk, never asserted.
`concern` is the consumer-side terminal exception for a doubt no task or discovery can close.
It keeps all four subsections and a real stake-free `q-executor`, uses `route: none`, omits `bank` and `target`, and leaves `a-executor` empty.
At final delivery add `**discussed**: <where the manuscript bears the limitation>`.

`deferred` — the PROBE CEILING landed here. The entry's `bank` verdict maps to a depth ABOVE the
stage's `probe_depth`, so answering it would cost money nobody has authorized. This is a CORRECT
outcome. It must be DECLARED, with a fifth field, or it is indistinguishable from a PROBE that was
simply skipped:

```text
**state**: deferred
**deferred**: depth-<n> · <what it would actually take, one line> · raise with `probe --depth <n>`
```

A `deferred` entry with no `**deferred**:` line FAILs the checker as `deferred-undeclared`.
The depth ladder: `reuse`=0 (free) · `run`=1 · `code`=2 · `new`=3.

📥 a-executor  (the answer BACK)
--------------------------------
Written at harvest: a COPY of the answering QA file's answer.
This is the consumer-side single source of truth — the paper references it, through the anchor chain, when it writes content.
Empty until the target is `answered`.
Each Q-consumer then writes its own a-consumer in its stage doc, anchored `[source: PP<NN>]` back to this copy.
It is the LONGEST body in the file and the one a human actually reads, so its readability matters most: one sentence per line, and one source per bullet — never a wall of prose.


✍️ For the phase workers
========================

DRAFT writes the stage content and raises each Q-consumer on the owning S page.
It writes no probe entry and never opens `1-probes/`.

PROBE authors the plan. For each question DRAFT raised:
  1. Find or open the q-executor entry (`## QX<n>`) — if an existing q-executor already asks it, add a bullet under its `### q-consumer` instead of opening a new entry.
  2. Write `### q-executor` — strip the stake, add the Deliverable and Accepted lines.
  3. Under `### q-consumer`, copy in each consumer's id and original question.
  4. Under `### bank binding`, write `route` and `bank` (read the bank read-only, judge reuse / run / code / new), set `target`, and leave `state: planned`.
  5. Leave `### a-executor` empty.
PROBE then runs the plan forward: it hands authorized `run` / `code` / `new` entries as a set to `haipipe-probe-q-executor-agent`, points each target, and copies the QA answer into `### a-executor`.
For a true terminal `concern`, PROBE writes the neutral q-executor plus the review-only q-consumer copy, sets `route: none` and `state: concern`, and does not dispatch.

➕ Optional fields (add only when they apply)
--------------------------------------------
Build-lane, only at `state: commissioned`, for days-to-weeks work: add `**owner**:`, `**eta**:`, `**blocks**:`, `**cross-project**:` under `### bank binding`.
Harvest lanes, when the answer yields reusable artifacts: `**values**:` / `**sources**:` / `**displays**:`, each `harvest: OWED` until its sub-worker accepts it.
Terminal concern, at final delivery: add `**discussed**: <section/paragraph carrying the limitation>`.

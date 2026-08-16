---
name: haipipe-page-probe
description: >-
  The PROBE phase contract for any Board Page. PROBE's plain job: send one question the Page cannot answer out to a real source, and bring the answer back without letting the source learn what is at stake. In the layer's terms, PROBE owns a consequential unknown from the Page's stake-bearing Q-consumer through a neutral Q-executor and returned A-executor to a per-consumer A-consumer; it changes the Page's knowledge boundary without authoring its argument. Load haipipe-page, the matching Page Type, this contract, and the shared haipipe-probe crossing protocol before the family door's probe tooling. Use when a Page has an unresolved question, when stake must be stripped before dispatch, when one Q-executor can serve several Q-consumers, when evidence must be matched or collected, or when an answer needs to return without being silently woven into prose. Trigger: page probe, PROBE phase, Q-consumer, Q-executor, A-executor, A-consumer, stake stripping, probe page, evidence return, /haipipe-page-probe.
metadata:
  version: "0.4.0"
  last_updated: "2026-08-06"
  summary: "On an evidence page the lifecycle runs COLLECT-first (JL 260806): a new Q-consumer lands in E0, PROBE translates it into an E<n> division + its QA-probe, the A-executor copies back, and each A-consumer is written under the division's #### consumers rows."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-probe · move one Page question across the evidence wall

Load the contracts in this order:

```text
haipipe-page
  → matching page-types/ variant, when one exists
  → haipipe-page-probe
  → haipipe-probe
  → the family DOOR's probe tooling, when the Page belongs to paper or application
```

`haipipe-probe` owns the shared crossing protocol, bank independence, and evidence boundary.
This file owns how that protocol participates in a Board Page lifecycle.

## 🧭 One phase, one lowercase unit, one persisted surface

Use three names and introduce no fourth lifecycle concept:

```text
PROBE       the uppercase Page phase
probe       one question and answer exchange
QA-probe    the persisted surface for one neutral Q-executor: a hidden
            source record below the evidence page's probes/ folder, named
            <n>-<slug>.md, never a board page
```

The QA-probe ("entry" survives only as an informal alias) is a source file the evidence page points at, like a PDF; the board renders the evidence page, never the record (JL ruling B, 260806).
One conversation, two QAs: the QA-bank is the original, the QA-probe is the consumer's stub that points at it; consumer and executor name SLOTS inside them, never files, and the four slot words are capitals: Q-consumer, A-consumer, Q-executor, A-executor.
On the evidence page one `### E<n> ·` Content division owns one QA-probe (1:1), and many QA-probes may point at one QA-bank; that sharing lives at the bank (JL 260806).

## 🧱 The four forms and the wall

The consumer and executor do not receive the same question:

```text
                 CONSUMER SIDE                    EXECUTOR SIDE
QUESTION         Q-consumer      ── strip stake ─▶ Q-executor
ANSWER           A-consumer      ◀─ interpret ─── A-executor
```

- Q-consumer is authoritative on the target Page and carries what the Page needs, why it matters, and what breaks.
- Q-executor is neutral, answerable by a stranger, and is the only question sent across the wall.
- A-executor is the returned answer anchored to its evidence source.
- A-consumer is the interpretation written for one Q-consumer.

One Q-executor may serve several Q-consumers.
That is reuse, not duplication.
The stake may appear in the Q-consumer and its audit trace, but never in the Q-executor, A-executor, dispatch payload, or bank artifact.

## 🔎 What PROBE owns

On an evidence page the lifecycle runs COLLECT-first (JL 260806): a Q-consumer born on any page is COLLECTED into the owning topic's `### E0 · incoming` queue; PROBE then TRANSLATES it, opening a new `### E<n>` division and its QA-probe, and the shared loop carries the rest:

```text
COLLECT      land the newly raised Q-consumer in the owning topic's E0 queue
① ORGANIZE   translate: strip the stake, write or reuse the Q-executor,
             promote E0's row into its E<n> division + QA-probe
② MATCH      read existing evidence before requesting new work
③ DISPATCH   send only the neutral Q-executor when new work is authorized
④ POINT      bind the returned answer by path (the QA-probe's target)
⑤ INTERPRET  copy the A-executor back into the QA-probe, then write one
             A-consumer per Q-consumer under the division's #### consumers
```

The family contract chooses the physical QA-probe, route vocabulary, cost ceiling, and evidence bank.
Those details do not change the phase boundary.

## ✍️ The write surfaces

PROBE writes beside the target prose and writes back only the Page-facing answer records:

```text
QA-probe        Q-executor · audit trace · route/binding · A-executor copy
target Page     E0 queue · E<n> division: QA-probe pointer, #### consumers
                rows (A-consumer per Q-consumer), #### answer digest ·
                evidence-based State update
target prose    never
purpose/Aims    never
```

PROBE does not decide how an answer should be argued or silently replace a hole in target prose.
That landing edit belongs to REVISE while the promise stays fixed, or DRAFT if the answer changes the Page's purpose or Aims.

## 🔀 Trigger, exit, and routing

PROBE starts when DRAFT, REVISE, or CHECK identifies a consequential unknown.
It may repeat, branch, reuse an existing answer, defer work above an authorized ceiling, or report that no route can answer the question.

Route after the probe:

```text
answer changes target prose under fixed Aims → REVISE
answer changes purpose or Aims               → DRAFT, new round
answer needs no prose change                 → CHECK or continue current work
question remains authorized but unresolved   → PROBE again or explicit defer
```

PROBE is optional when the Page has no consequential unknown.

## 🧾 RUN receipt

When called by RUN, read `../haipipe-page-workflow/ref/page-run-contract.md` and
return its common phase receipt. PROBE's receipt must additionally identify:

```text
reason             the consequential unknown being resolved
artifacts          Q-executor / A-executor surface and Page-facing A-consumer
evidence           source bindings and the returned answer's limits
route              PROBE | REVISE | DRAFT | CHECK | HOLD
reopens_promise    true only when the answer changes purpose or an Aim
```

The target Page's source hash may remain unchanged when PROBE only writes its
declared side surface. That is not a missing version: the probe artifacts and
evidence must still appear in the receipt. PROBE never routes to CLOSE.

## 📂 Files

```text
page-workflows/haipipe-page-probe/
├── SKILL.md            this Page-phase adapter
└── CHANGELOG.md        version history
```

Owns no scripts.
The shared crossing model is `probe/haipipe-probe`; Page Type variants live under `page-types/`; the family DOOR owns the persisted QA-probe shape and checker.
The Board engine owns execution and audit; this phase owns only its authority and receipt.

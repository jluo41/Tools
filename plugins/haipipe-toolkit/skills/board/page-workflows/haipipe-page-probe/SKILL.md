---
name: haipipe-page-probe
description: >-
  The PROBE phase contract for a Board Page. It turns each approved Task- or
  Discovery-backed outline obligation into one Page-local probe card, preserves
  the stake behind the wall, MATCHES the selected QA bank before DISPATCH, and
  stops when every such obligation is served. This is the QA branch of the
  Probe family; PageX is its existing-Page branch and runs in OUTLINE. Trigger: page probe, PROBE phase,
  raise a probe card, Task evidence, Discovery evidence, Q-consumer,
  Q-executor, match before dispatch, /haipipe-page-probe.
metadata:
  version: "0.9.0"
  last_updated: "2026-08-20"
  summary: "The PROBE phase runs the QA branch; PageX is the Probe family's OUTLINE branch."
---

# /haipipe-page-probe · run Probe's Task/Discovery QA branch

Load `haipipe-page`, the matching Page Type, this phase,
`../../page-plugins/haipipe-plugin-probe`, and `haipipe-probe`.

```text
Probe family
├─ accepted Page obligation ── PageX in OUTLINE
└─ Task/Discovery obligation ── QA Probe here
```

PageX is grouped under Probe for discovery and configuration, but it is already
resolved before this phase begins. The two lanes do not fall through into one
another. If an OUTLINE mislabeled
the source, return to OUTLINE and correct the obligation before creating a card.

## ⚡ Phase card

```text
READS    target Page · person-LOOKED outline · existing local probe cards
WRITES   <page>/probe/PP<NN>-<slug>/ card, consumer, executor, empty proof manifest
NEVER    Page prose · accepted outline · PageX ranking · returned answer · display intake
EXITS    EVIDENCE when every Task/Discovery mark is served and dispatched or matched
HUMAN    a person's LOOK releases this phase; no human read/accept gate is ticked here
```

PROBE owns the outbound half of the shared crossing:

```text
① ORGANIZE   Q-consumer → stripped Q-executor
② MATCH      current local cards, then the selected Task/Discovery QA bank
③ DISPATCH   only when no literal QA answer or live matching question exists
```

EVIDENCE owns `④ POINT` and `⑤ INTERPRET` after the answer returns.

## 🎯 Authority

PROBE may:

- create or reuse a local card;
- merge several outline obligations into one answerable executor question;
- serve one obligation with several cards when sources differ;
- choose `task`, `discovery`, or `none` from the approved source obligation;
- defer or hold an authorized question with a named reason;
- dispatch the stripped question.

PROBE may not:

- search or rank existing Pages through PageX;
- turn a topic-similar Page into evidence;
- add an obligation absent from the approved outline;
- edit the outline, purpose, Aims, States, or Content;
- land the returned answer, allocate values, or freeze a display.

## 🕐 Card creation

The outline carries a source-typed mark but no card id. A rejected outline must
leave no evidence-card litter, so the card is created only after a person's LOOK
releases PROBE.

```text
OUTLINE   C4.P1.B4 · subgroup estimate · source: task · 📮
PROBE     probe/PP03-subgroup-estimate/ · serves: C4.P1.B4
```

Allocate the next unused two-digit `PP<NN>` on this Page. Follow the plugin's
noun-based slug rule. The card points backward with `serves:` because its id did
not exist when the outline was authored.

Many-to-many joins are valid:

```text
many bullets → one card    one bank question answers several planned sentences
one bullet   → many cards  separate sources are jointly necessary
```

A bullet is served only when every card it needs lands. A duplicate card for an
already-asked unknown is a defect.

## 🧱 Organize and strip

Write the stake-bearing need to `consumer/q-consumer.md`. Write an independently
answerable, neutral question to `executor/q-executor.md`.

The executor side contains no Page/claim id, venue pressure, desired answer, or
phrases such as “our paper” and “we need to show.” The neutral question should
still name the population, variable, comparison, method, and requested output
needed for an exact answer.

Route by source:

```text
task        computed, measured, run-bound, or repository-local fact
discovery   literature, prior art, external fact, or novelty question
none        neither bank can answer; record concern and HOLD
```

## 🔎 MATCH before DISPATCH

Match in this order:

```text
1. existing probe cards on this Page
2. selected Task or Discovery bank with its QA verb in --check-only mode
3. only then create/dispatch new work
```

Do not insert PageX into this list. Existing Page evidence should already be a
PageX-bound OUTLINE input; reopening that selection is an OUTLINE decision.

Use the bank's own side door:

```text
/haipipe-task qa "<Q-executor>" [<task-folder>] --check-only
/haipipe-discovery qa "<Q-executor>" [<discovery-folder>] --check-only
```

Read state before answer:

```text
answered          reuse exact QA path; EVIDENCE will bind it
working, live      dispatch nothing; record the active QA path
superseded-by      follow to the live QA file
near miss/no hit   DISPATCH
```

Topic overlap is navigation only. A match passes only when the QA file literally
answers Q-executor.

## 📮 DISPATCH

Dispatch only `executor/q-executor.md` through the shared probe executor. The
payload may name card id, route, bank verdict, and return address, but never the
consumer stake.

The Task or Discovery layer decides whether to digest existing terminal files,
run code, enrich a topic, or create a correctly scoped folder. PROBE does not
direct those internals. Its return is an exact QA path or an explicit refusal.

The card may end this phase as:

```text
planned         neutral question exists; no dispatch required or authorized yet
commissioned    matching QA work is active or newly dispatched
concern         route none or bank refusal prevents an answer
```

`answered` and `read` belong to the landing/human half and are not synthesized
here.

## 🧭 Which marks create cards

```text
📮 probe      always, when source is Task or Discovery
📚 citation   only when an unknown source requires a Discovery question
🧮 value      no new card when it already names PP<NN>.v<n>
🖼 display    no card; EVIDENCE owns the display unit and intake
🎯 aim        no card; it is an outline target
🔗 PageX      no card; OUTLINE owns accepted Page selection and scope
```

A Page with no Task/Discovery obligation skips PROBE cleanly.

## 🔀 Exit and routing

```text
every Task/Discovery obligation served and matched/dispatched → EVIDENCE
wrong source type or wrong obligation                          → OUTLINE vNext
authorized question still needs outbound work                 → PROBE again
no allowed bank can answer                                    → HOLD
```

PROBE never routes directly to DRAFT or REVISE. The returned evidence must land
and flow back through OUTLINE before prose begins.

## 🧾 RUN receipt

Follow `../haipipe-page-workflow/ref/page-run-contract.md` and add:

```text
phase:       PROBE
outline:     approved path/version and human LOOK
marks:       number of Task and Discovery obligations
cards:       PP id · route · serves · state · dispatch target
matches:     local reuse or exact bank QA path; never a PageX candidate
coverage:    served obligations / total obligations
limits:      refused, deferred, or source-misclassified work
next:        EVIDENCE | PROBE | OUTLINE | HOLD
```

A coverage gap is a HOLD, not a successful receipt. The next phase is
`haipipe-page-evidence`, which binds what this phase matched or dispatched.

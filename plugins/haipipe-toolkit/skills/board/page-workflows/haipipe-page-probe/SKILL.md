---
name: haipipe-page-probe
description: >-
  The PROBE phase contract for a Board Page: turn each approved Task- or
  Discovery-backed outline obligation into one page-local probe card, keep the
  stake behind the wall, and MATCH the QA bank before DISPATCH. PageX is the
  sibling lane and runs in OUTLINE. Trigger: page probe, PROBE phase, raise a
  probe card, Task evidence, match before dispatch, /haipipe-page-probe.
metadata:
  version: "0.12.0"
  last_updated: "2026-08-31"
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

## 🧱 The crossing itself is `haipipe-probe`'s · this is the page-local delta

Steps ① ORGANIZE, ② MATCH and ③ DISPATCH are stated ONCE, in
`probe/haipipe-probe` §🔁: what goes in `consumer/` versus `executor/`, what
counts as stake, the `task | discovery | none` route table, the `--check-only`
side door, and how to read a candidate's `state:` line before its answer. Read
them there.

⚠️ **Until 260821 this file restated all three**, which is the §🪞 mirror its own
family forbids — and it had already drifted: a sixth bullet mark, `🔗 PageX`,
appeared in §🧭 below that `haipipe-plugin-outline` §📐 (the mark authority) has
never carried. What follows is only what the shared contract does NOT say.

**① the local pass comes first.** `haipipe-probe` §② starts at the bank; on a
Board Page there is a step in front of it:

```text
1. existing probe/PP<NN>-<slug>/ cards ON THIS PAGE      ← page-local, step 0
2. the page's collection job's QA/ and values.yaml       ← haipipe-task-for-page
3. the selected Task or Discovery bank, --check-only     ← haipipe-probe §②
4. only then dispatch new work                           ← haipipe-probe §③
```

Do not insert PageX into that list. Existing Page evidence should already be a
PageX-bound OUTLINE input; reopening that selection is an OUTLINE decision, and
a topic-similar Page is never a bank answer.

**② one door out, and it is an agent.** Dispatch `executor/q-executor.md` — and
nothing else — by handing the batch to `haipipe-probe-q-executor-agent`. A phase
producer never calls `haipipe-task-orchestrator-agent` or
`haipipe-discovery-orchestrator-agent` itself (JL 260820: 永远只有
haipipe-probe-q-executor-agent 才能够做这件事). The payload may name card id,
route, bank verdict and return address; it may never name the consumer stake. Since 260831 a page's TASK-route batch has a home: the page's
collection job (task-type `page`, `task/haipipe-task-for-page`, linked first in
the `task/` lane). The executor agent runs each stripped question as
`/haipipe-task qa "<question>" <collection-job>`; the job computes, digests or
proposes, and the door stays the one above.

**③ the three states this phase may leave behind.** The full ladder is
`haipipe-plugin-probe` §✍️; these are the only ones PROBE writes:

```text
planned         neutral question exists; no dispatch required or authorized yet
commissioned    matching QA work is active or newly dispatched
concern         route none or bank refusal prevents an answer
```

`answered`, `answered-local` and `read` belong to the landing and human halves
and are never synthesized here.

## 🧭 Which marks create cards

```text
📮 probe      always, when source is Task or Discovery
📚 citation   only when an unknown source requires a Discovery question
🧮 value      no new card when it already names PP<NN>.v<n>
🖼 display    no card; EVIDENCE owns the display unit and intake
🎯 aim        no card; it is an outline target
```

These are the FIVE marks `haipipe-plugin-outline` §📐 defines, and there is no
sixth. A `🔗 PageX` row stood here until 260821; PageX is a LANE resolved in
OUTLINE, never a bullet mark, and inventing one is what restating another
file's table costs.

A Page with no Task/Discovery obligation skips PROBE cleanly.

## 🔀 Exit and routing

```text
every Task/Discovery obligation served and matched/dispatched → EVIDENCE
wrong source type or wrong obligation                          → OUTLINE vNext
authorized question still needs outbound work                 → PROBE again
no bank can answer IN PRINCIPLE (route: none)                 → HOLD
```

⚠️ **A missing task folder is NOT that HOLD.** It is `T4 FRESH` and dispatches
normally; the executor opens the leaf at depth 3 (`haipipe-probe` §💰 · §③).
Only a question no executor could ever close — a value judgment, a fact nobody
holds — reaches `route: none`. Turning "no folder yet" into a HOLD converts a
missing ANSWER into a refused QUESTION, and only the second one is terminal.

PROBE never routes directly to DRAFT or REVISE. The returned evidence must land
and flow back through OUTLINE before prose begins.

## 🧾 RUN receipt

Follow `../haipipe-page-workflow/ref/page-run-contract.md` and add:

```text
phase:       PROBE
outline:     approved path/version and human LOOK
marks:       number of Task and Discovery obligations
cards:       PP id · route · tier · serves · state · dispatch target
tiers:       how many cards landed on each of T0-T4 (`haipipe-probe` §💰).
             Every card at T3/T4 is a smell worth one line: lazy MATCH, or a
             starving bank (CC-7).
matches:     local reuse or exact bank QA path; never a PageX candidate
coverage:    served obligations / total obligations
limits:      refused, deferred, or source-misclassified work
next:        EVIDENCE | PROBE | OUTLINE | HOLD
```

A coverage gap is a HOLD, not a successful receipt. The next phase is
`haipipe-page-evidence`, which binds what this phase matched or dispatched.

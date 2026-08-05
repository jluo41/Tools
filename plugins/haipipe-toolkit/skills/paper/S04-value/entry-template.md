<!-- TEMPLATE (follow, don't ship). Copy this skeleton to <paper>/0-lifecycle/S04-value/probes/V<nn>-<topic>/S-Value-<n>-<slug>.md: replace every <...>, and each `<!-- RULE: ... -->` comment is guidance to FOLLOW then DELETE. A RULE comment must never appear in the finished entry. Delete this top line too. -->
# S Value <n> · <the neutral computation, in a few words>
state: 🔴 OPEN · q-executor written, not dispatched
owner: <who; usually JL>
method: one q-executor, bound by PATH to a task bank answer
requires: <topic-page-id, e.g. S-Value-1>
provides: the answer this row owes on the task route

<!-- RULE: requires: names the ONE direct topic page whose register raised this entry. The checker fails any entry beneath probes/ whose requires: is not a topic page owning a ### Q-consumer register. -->

## Opening
What does the paper still need from outside itself here, and has it come back?
This page is ONE probe entry: one computation the paper cannot do on its own, bound to one answer in the task bank.

## Stage Contract

<!-- RULE: machine-managed span. Leave this section heading in place and run stage.py sync to fill it from the requires: metadata above; never hand-edit between the haipipe:contract markers once they appear. -->

## Content

<!-- RULE: the four #### parts below are the entry anatomy from board/haipipe-board/ref/topic-entry-contract.md: exactly one of each, at exactly this heading level, in this order. -->

#### q-executor
<!-- RULE: the computation with the stake STRIPPED: no claim ids, no "our paper", no target value, no hint of which result would rescue what. The stake stays on the topic page's register; this asks for the computation in neutral terms. State the deliverable and what counts as an accepted answer, including the honest refusal shape. -->
<From <the existing task's outputs or the data it may touch>, emit <the exact statistics or estimates wanted>.>
Deliverable: <the numbers with their source paths, in a QA digest>.
Accepted: <all emitted with provenance | not producible from this source; name which and why>.

#### consumer trace
<!-- RULE: audit copy only, never a second register. One line per consumer question id, with the stake as the register states it; every id written here must appear in the parent topic page's register, and the checker verifies that. -->
* **Q-<Stage>-<n>**: <the stake this id carries, copied from the register for audit>

#### bank binding
<!-- RULE: route and bank say where the computation went; target is the QA file the bank answers at, written as a path from the project root. The **state**: line is the queue, one lowercase value on its own line: planned | commissioned | deferred are queued; read | answered-local are resolved. If the wanted aggregate cannot come from the bound export, say so here and DEFER rather than fabricating. -->
**route**: task
**bank**: <run | code | reuse | new> · tasks/<task-group-or-folder>/
**target**: tasks/<task-folder>/QA/<n>-<slug>.md
**state**: planned

#### a-executor
<!-- RULE: what came back, harvested from the QA file at target, still in neutral language: each figure with its uncertainty and its source path, plus every caveat the run recorded. Empty until the bank answers. A figure the export cannot produce is written NOT ANSWERABLE with the reason, never estimated. -->
<empty until the answer lands>

## Aims

### A1 · 🔗 The entry, as PROBE wrote it
- A1.1 · The computation is answered and the answer is bound to a real bank path.
  **Done when:** the a-executor is present and its target resolves to a file that exists.

## States

### A1 · 🔗 The entry, as PROBE wrote it
- ⬜ A1.1 · <the honest present, e.g. state `planned`, no target yet>

## Log

- <date> · [PROBE-CC] entry opened from `<topic-page-id>`'s register row `Q-<Stage>-<n>`
<!-- RULE: the entry's own Log carries the dispatch pair when it happens: [PROBE-CC] dispatched, working since <date>, then [PROBE-CC] answered → <QA path>. Grammar: `- <date> [<time>] · [<PHASE>-<actor>] <what moved> [→ <pointer>]`. -->

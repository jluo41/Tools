<!-- TEMPLATE (follow, don't ship). Copy this skeleton to <paper>/0-lifecycle/S03-literature/probes/L<nn>-<topic>/S-Literature-<n>-<slug>.md: replace every <...>, and each `<!-- RULE: ... -->` comment is guidance to FOLLOW then DELETE. A RULE comment must never appear in the finished entry. Delete this top line too. -->
# S Literature <n> · <the neutral question, in a few words>
state: 🔴 OPEN · q-executor written, not dispatched
owner: <who; usually JL>
method: one q-executor, bound by PATH to a discovery bank answer
requires: <topic-page-id, e.g. S-Literature-2>
provides: the answer this row owes on the discovery route

<!-- RULE: requires: names the ONE direct topic page whose register raised this entry. The checker fails any entry beneath probes/ whose requires: is not a topic page owning a ### Q-consumer register. -->

## Opening
What does the paper still need from outside itself here, and has it come back?
This page is ONE probe entry: one neutral question the paper cannot answer on its own, bound to one answer in the discovery bank.

## Stage Contract

<!-- RULE: machine-managed span. Leave this section heading in place and run stage.py sync to fill it from the requires: metadata above; never hand-edit between the haipipe:contract markers once they appear. -->

## Content

<!-- RULE: the four #### parts below are the entry anatomy from board/haipipe-board/ref/topic-entry-contract.md: exactly one of each, at exactly this heading level, in this order. -->

#### q-executor
<!-- RULE: the question with the stake STRIPPED: no claim ids, no "our paper", no hint of which verdict would rescue what. The stake stays on the topic page's register; this is the neutral question another system can answer. State the deliverable and what counts as an accepted answer. -->
<The neutral question a discovery bank can answer without knowing why it matters.>
Deliverable: <what must come back, e.g. a prior-art digest naming the closest study on each half>.
Accepted: <the answer shapes that count, e.g. occupied (name the study) | unoccupied (name the nearest neighbors)>.

#### consumer trace
<!-- RULE: audit copy only, never a second register. One line per consumer question id, with the stake as the register states it; every id written here must appear in the parent topic page's register, and the checker verifies that. -->
* **Q-<Stage>-<n>**: <the stake this id carries, copied from the register for audit>

#### bank binding
<!-- RULE: route and bank say where the question went; target is the QA file the bank answers at, written as a path from the project root. The **state**: line is the queue, one lowercase value on its own line: planned | commissioned | deferred are queued; read | answered-local are resolved. -->
**route**: discovery
**bank**: <run | reuse | new> · discoveries/<discovery-group>/<discovery-folder>/
**target**: discoveries/<discovery-group>/<discovery-folder>/QA/<n>-<slug>.md
**state**: planned

#### a-executor
<!-- RULE: what came back, harvested from the QA file at target, still in neutral language: findings, sources, caveats, scope. Empty until the bank answers. This entry IS the record; the topic page's register row interprets it, never replaces it. -->
<empty until the answer lands>

## Aims

### A1 · 🔗 The entry, as PROBE wrote it
- A1.1 · The question is answered and the answer is bound to a real bank path.
  **Done when:** the a-executor is present and its target resolves to a file that exists.

## States

### A1 · 🔗 The entry, as PROBE wrote it
- ⬜ A1.1 · <the honest present, e.g. state `planned`, no target yet>

## Log

- <date> · [PROBE-CC] entry opened from `<topic-page-id>`'s register row `Q-<Stage>-<n>`
<!-- RULE: the entry's own Log carries the dispatch pair when it happens: [PROBE-CC] dispatched, working since <date>, then [PROBE-CC] answered → <QA path>. Grammar: `- <date> [<time>] · [<PHASE>-<actor>] <what moved> [→ <pointer>]`. -->

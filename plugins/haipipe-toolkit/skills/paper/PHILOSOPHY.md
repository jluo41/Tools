# Paper design philosophy

A paper is a delivery contract, not a writing folder. It selects evidence,
expresses the argument, and produces reader-facing artifacts. Tasks run project
work. Discoveries inspect outside evidence. Both return a general-language QA
file that the Paper may read but never author.

## Delivery, engine, execution

```text
Paper delivery       why an answer matters to this manuscript
  ↓
Nested probe entry   neutral question and bank binding
  ↓
Task or discovery    executes and authors the QA evidence
  ↓
Paper interpretation what the answer means for this paper
```

The Paper owns the first and last line. The executor owns the middle evidence.
That boundary keeps a desired conclusion out of the evidence request.

## Evidence routing

```text
S03 Literature topic page
  └── nested discovery entry

S04 Value topic page
  └── nested task entry
```

Each direct topic page owns the canonical Q-consumer register and paper stake.
Each nested entry owns one stake-free q-executor, consumer trace, bank binding,
and returned answer. The five-step PROBE loop is ORGANIZE → MATCH → DISPATCH →
POINT → INTERPRET. The paper matches before it dispatches and never executes
bank work inline.

## Lifecycle

The Paper family uses one delivery grammar:

```text
S01 Opening → S02 Work → S03 Literature → S04 Value → S05 Display
→ S06 Main → S07 Appendix → S08 Present → S09 Build → S10 Round
```

Venue is part of Opening. Literature and Value are shared runtime evidence
stores that enable the user-facing stages, rather than extra public stages.
The Board reads this order as delivery orientation; execution follows explicit
stage contracts and their dependencies.

## Non-negotiable boundaries

- Paper does not run code, inspect raw data, or author bank evidence.
- Task and discovery do not learn which paper claim an answer would settle.
- A claim status lives on the Paper claim ledger, not in a probe entry.
- A queue is derived from nested-entry state. It is not a separate folder or
  a hand-maintained list.
- The only live evidence-entry homes are `S03-literature/probes/` and
  `S04-value/probes/`.

---
name: haipipe-board-page-for-value
description: >-
  The VARIANT contract for a VALUE topic Page: a topic page owning a `### Q-consumer register` whose questions face INWARD, toward results this project must produce, with one probe entry page nested below probes/ per neutral executor question. It loads haipipe-board-page for the base frame and the shared topic-entry core for the anatomy, then adds only the inward route's translation layer: what a legal register row carries here, what a returned answer must become (a value binding: the number, its run provenance, the claim it serves), and when the topic may close. Use when writing or fixing a Value topic page, when a register row names no claim dependency, when a number appears in prose with no run behind it, or when a claim ledger row cannot say which specification produced its estimate. Trigger: value topic, value page, S-Value, task route, value binding, run provenance, claim ledger, number evidence, /haipipe-board-page-for-value.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-05"
  summary: "First cut, on JL's D ruling: separate types over ONE loaded topic core; this file is the inward route's dictionary and nothing else."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-page-for-value · the inward route: what this project must produce

**LOAD TWO THINGS FIRST.** `haipipe-board-page` owns the base frame. `haipipe-board/ref/topic-entry-contract.md` owns the shared anatomy: the `### Q-consumer register` on the direct topic page, entry pages below `probes/`, the four fixed entry headings, and the state-derived queue. This file restates NEITHER; it adds only what the inward route means, because the anatomy is stated once or the two topic types drift apart (`QB6 §4`, JL 260805).

**The kind this variant covers**: a topic page whose questions face INWARD.

```
kind     resolved by                          closes when
─────────────────────────────────────────────────────────────────────
Value    the page declares a Q-consumer       every register row's claim is
topic    register AND its route is the        bound to an accepted run, deferred
         inward, task-bank direction          with a reason, or withdrawn
```

"Value" names a DIRECTION, not a paper section: any family may ask for a number its own work must produce. The paper family's projection files these pages as `S-Value-<n>-<topic>` with `V<n>` entry folders; those letters are family vocabulary and stay in the paper projection.

## 🗣 What a legal register row carries HERE

A Value Q-consumer carries a CLAIM DEPENDENCY: which claim rests on the number, and what specification would count as producing it.

```
✅  "H2 states high-dose prescribing rises with the trait score.
     It needs the LBP-cohort estimate, its CI, and the spec that made it."
🚫  "Get the regression results."                    no claim named · a chore
🚫  "Produce an estimate near 0.3."                  the answer ordered in advance
```

The stake stays on this page. The nested entry's q-executor asks for the computation in neutral terms, and the bank that runs it never learns which claim would be rescued (`page-phases/haipipe-board-page-probe` owns that wall).

## 📥 What a returned answer must BECOME: the value binding

An answer that stays in the entry's `#### a-executor` is not yet a number the page may print. The register's write-back is a typed record with three parts:

```
1  the value           with its uncertainty, exactly as the run reported it
2  the run provenance  which run, which specification, which QA file · BY PATH
3  the claim update    which claim consumed it, and what its status became:
                       supported · weakened · unresolved
```

🚫 A number whose provenance line is missing is a HOLE, not a result. It reads exactly like a real one, which is why the record, not the prose, is what CHECK audits.

## 🚪 When the topic closes

Every register row reaches one of three states: its claim is BOUND to an accepted run by path, DEFERRED with the reason written on the row, or WITHDRAWN because the claim changed. A row that is none of these holds the topic open, and the topic's human gate reads the register, not the entries.

## 📂 Files

```
haipipe-board-page-for-value/
├── SKILL.md            this route dictionary
└── CHANGELOG.md        version history
```

Owns no scripts and no anatomy. The core is `haipipe-board/ref/topic-entry-contract.md`; the checker is `haipipe-board/src/topic_entry_contract.py`; the crossing is `page-phases/haipipe-board-page-probe`; the outward sibling is `haipipe-board-page-for-literature`; the paper projection is `paper/workers/haipipe-paper-probe/ref/topic-entry-contract.md`.

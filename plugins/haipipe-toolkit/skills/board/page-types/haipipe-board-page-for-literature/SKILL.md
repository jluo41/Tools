---
name: haipipe-board-page-for-literature
description: >-
  The VARIANT contract for a LITERATURE topic Page: a topic page owning a `### Q-consumer register` whose questions face OUTWARD, toward published knowledge, with one probe entry page nested below probes/ per neutral executor question. It loads haipipe-board-page for the base frame and the shared topic-entry core for the anatomy, then adds only the outward route's translation layer: what a legal register row carries here, what a returned answer must become (a citation binding: a real key, a positioning sentence, a novelty verdict), and when the topic may close. Use when writing or fixing a Literature topic page, when a register row carries no positioning stake, when an answer landed but never became a citation record, or when a novelty claim rests on nothing traceable. Trigger: literature topic, literature page, S-Literature, discovery route, positioning, novelty, citation binding, related work evidence, /haipipe-board-page-for-literature.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-05"
  summary: "First cut, on JL's D ruling: separate types over ONE loaded topic core; this file is the outward route's dictionary and nothing else."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-page-for-literature · the outward route: what is already known

**LOAD TWO THINGS FIRST.** `haipipe-board-page` owns the base frame. `haipipe-board/ref/topic-entry-contract.md` owns the shared anatomy: the `### Q-consumer register` on the direct topic page, entry pages below `probes/`, the four fixed entry headings, and the state-derived queue. This file restates NEITHER; it adds only what the outward route means, because the anatomy is stated once or the two topic types drift apart (`QB6 §4`, JL 260805).

**The kind this variant covers**: a topic page whose questions face OUTWARD.

```
kind        resolved by                          closes when
────────────────────────────────────────────────────────────────────────
Literature  the page declares a Q-consumer       every register row's positioning
topic       register AND its route is the        is supported, deferred with a
            outward, discovery-bank direction    reason, or withdrawn
```

"Literature" names a DIRECTION, not a paper section: any family may ask what is already known. The paper family's projection files these pages as `S-Literature-<n>-<topic>` under its discovery group with `L<n>` entry folders; those letters are family vocabulary and stay in the paper projection.

## 🗣 What a legal register row carries HERE

A Literature Q-consumer carries a POSITIONING STAKE: what the work claims to add, and what published result would strengthen or break that claim.

```
✅  "Is our review-text trait measure novel, or did <field> already do it?
     H1's contribution claim dies if a published precedent exists."
🚫  "Find papers about physician reviews."          no stake · a reading list
🚫  "Confirm nobody has done this."                 a verdict ordered in advance
```

The stake stays on this page. The nested entry's q-executor carries the neutral question only, and the wall between them is PROBE's (`page-phases/haipipe-board-page-probe`).

## 📥 What a returned answer must BECOME: the citation binding

An answer that stays in the entry's `#### a-executor` is not yet evidence the page can use. The register's write-back is a typed record with three parts:

```
1  a real key          resolvable in the bibliography, never a title from memory
2  a positioning       one sentence stating how this work stands NEXT TO the
   sentence            found result: extends, contradicts, first-in-setting
3  a novelty verdict   supported · threatened · broken, with the source named
```

🚫 Never write "novelty confirmed" from an ABSENCE of findings alone. Absence after a bounded search is written as "no precedent found within <the search's own scope>", because the search's limits are part of the fact.

## 🚪 When the topic closes

Every register row reaches one of three states: its positioning is SUPPORTED by named sources, DEFERRED with the reason written on the row, or WITHDRAWN because the claim it served changed. A row that is none of these holds the topic open, and the topic's human gate reads the register, not the entries.

## 📂 Files

```
haipipe-board-page-for-literature/
├── SKILL.md            this route dictionary
└── CHANGELOG.md        version history
```

Owns no scripts and no anatomy. The core is `haipipe-board/ref/topic-entry-contract.md`; the checker is `haipipe-board/src/topic_entry_contract.py`; the crossing is `page-phases/haipipe-board-page-probe`; the inward sibling is `haipipe-board-page-for-value`; the paper projection is `paper/workers/haipipe-paper-probe/ref/topic-entry-contract.md`.

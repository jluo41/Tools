---
name: haipipe-board-page-for-literature
description: >-
  The VARIANT contract for a LITERATURE topic Page: a topic page owning a `### Q-consumer register` whose questions face OUTWARD, toward published knowledge, with one probe QA (the entry record) nested below probes/ per neutral executor question. It loads haipipe-board-page for the base frame and the shared topic-entry core for the anatomy, then adds only the outward route's translation layer: what a legal register row carries here, what a returned answer must become (a citation binding: a real key, a positioning sentence, a novelty verdict), and when the topic may close. Use when writing or fixing a Literature topic page, when a register row carries no positioning stake, when an answer landed but never became a citation record, or when a novelty claim rests on nothing traceable. Trigger: literature topic, literature page, S-Literature, discovery route, positioning, novelty, citation binding, related work evidence, /haipipe-board-page-for-literature.
metadata:
  version: "0.3.0"
  last_updated: "2026-08-06"
  summary: "Entries are hidden source records, not board pages (JL ruling B, 260806): one probe QA per neutral executor question, named <n>-<slug>.md below probes/, pointing at its bank QA, with the anatomy in the core contract."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-page-for-literature · the outward route: what is already known

**LOAD TWO THINGS FIRST.** The base frame is `haipipe-board-page`, and the register and entry-record anatomy is `haipipe-board/ref/topic-entry-contract.md`, stated once for both topic routes so they cannot drift apart (`QB6 §4`, JL 260805). A probe QA is a hidden source record named `<n>-<slug>.md`, never a board page (JL ruling B, 260806); it is the paper's copy that points at the bank QA, the original. This file is the outward route's dictionary and nothing more: what a question aimed at the published record carries, and what a found result must become before this page may lean on it. Any sentence here that seems to describe the register's shape belongs to the core, not to this file.

**The kind this variant covers**: a topic page whose questions face OUTWARD.

```
kind        resolved by                          closes when
────────────────────────────────────────────────────────────────────────
Literature  the `### Q-consumer register`        every register row is SUPPORTED,
topic       marker plus its REQUIRED             DEFERRED, or WITHDRAWN, per the
            `route: outward` line                core's Register-row states
```

"Literature" names a DIRECTION, not a paper section: any family may ask what is already known. The paper family's projection files these pages as `S-Literature-<n>-<topic>` under its discovery group with `L<n>` entry folders; those letters are family vocabulary and stay in the paper projection. The register opens with its REQUIRED key, `route: outward`: the filename looks like a stage page's, so only this line routes the page here (base, type resolution step ②).

## 🗣 What a legal register row carries HERE

A Literature Q-consumer carries a POSITIONING STAKE: what the work claims to add, and what published result would strengthen or break that claim.

```
✅  "Is our review-text trait measure novel, or did <field> already do it?
     H1's contribution claim dies if a published precedent exists."
🚫  "Find papers about physician reviews."          no stake · a reading list
🚫  "Confirm nobody has done this."                 a verdict ordered in advance
```

The stake stays on this page. The nested probe QA's q-executor carries the neutral question only, and the wall between them is PROBE's (`page-phases/haipipe-board-page-probe`).

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

The three terminal row states, and the rule that the gate reads the register rather than the entries, live in the core (`topic-entry-contract.md`, Register-row states). This route only says what SUPPORTED takes here: named, real sources standing behind the positioning, which is the citation binding above, written onto the row. A search that came back empty supports nothing by itself; the row either carries the bounded no-precedent finding, scope and all, or it stays open.

## 📂 Files

```
haipipe-board-page-for-literature/
├── SKILL.md            this route dictionary
└── CHANGELOG.md        version history
```

This folder holds prose only. The anatomy lives in `haipipe-board/ref/topic-entry-contract.md` and its checker in `haipipe-board/src/topic_entry_contract.py`; a literature question crosses to the discovery bank through `page-phases/haipipe-board-page-probe`. A question about what this project must PRODUCE, rather than what the field already holds, belongs on a `haipipe-board-page-for-value` page instead. The paper family's projection of the shape is `paper/haipipe-paper/probe/topic-entry-contract.md`.

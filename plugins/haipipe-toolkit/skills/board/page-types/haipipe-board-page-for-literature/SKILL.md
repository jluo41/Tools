---
name: haipipe-board-page-for-literature
description: >-
  The VARIANT contract for a LITERATURE evidence Page: an evidence page declaring `route: outward` in its metadata head, whose questions face OUTWARD, toward published knowledge. Its Content is organized BY EXECUTOR: one `### E<n> · <question>` division per Q-executor conversation, each owning one QA-probe record below probes/, its collected consumers, and an answer digest, plus the standing `### E0 · incoming` queue. It loads haipipe-board-page for the base frame and the shared topic-entry core for the anatomy, then adds only the outward route's translation layer: what a legal consumer row carries here, what a returned answer must become (a citation binding: a real key, a positioning sentence, a novelty verdict), and when the page may close. Use when writing or fixing a Literature evidence page, when a consumer row carries no positioning stake, when an answer landed but never became a citation record, or when a novelty claim rests on nothing traceable. Trigger: literature evidence, evidence page, literature topic, S-Literature, discovery route, positioning, novelty, citation binding, related work evidence, /haipipe-board-page-for-literature.
metadata:
  version: "0.4.0"
  last_updated: "2026-08-06"
  summary: "Evidence pages organize BY EXECUTOR (JL 260806): the head route: line is the type key, one E<n> Content division per Q-executor conversation with its QA-probe pointer, #### consumers, and #### answer digest, plus the E0 incoming queue; the flat Q-consumer register is retired."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-page-for-literature · the outward route: what is already known

**LOAD TWO THINGS FIRST.** The base frame is `haipipe-board-page`, and the E-division and QA-probe anatomy is `haipipe-board/ref/topic-entry-contract.md`, stated once for both evidence routes so they cannot drift apart (`QB6 §4`, JL 260805). A QA-probe is a hidden source record named `<n>-<slug>.md`, never a board page (JL ruling B, 260806); it is the paper's stub that points at the QA-bank, the original. This file is the outward route's dictionary and nothing more: what a question aimed at the published record carries, and what a found result must become before this page may lean on it. Any sentence here that seems to describe the page's shape belongs to the core, not to this file.

**The kind this variant covers**: an evidence page whose questions face OUTWARD.

```
kind        resolved by                          closes when
────────────────────────────────────────────────────────────────────────
Literature  the REQUIRED `route: outward`        every E<n> division's consumers
evidence    line in the metadata head            are SUPPORTED, DEFERRED, or
            (base, type resolution step ②)       WITHDRAWN, AND E0 is empty
```

"Literature" names a DIRECTION, not a paper section: any family may ask what is already known. The paper family's projection files these pages as `S-Literature-<n>-<topic>` under its discovery group with `L<n>` probe folders; those letters are family vocabulary and stay in the paper projection. The filename looks like a stage page's, so only the head `route: outward` line routes the page here.

## 🧬 The page organizes BY EXECUTOR

One `### E<n> · <the executor question>` Content division per Q-executor conversation; one division owns exactly one QA-probe. `### E0 · incoming` is the collect queue: a Q-consumer born on ANY page is COLLECTED into the owning topic's E0 first, and PROBE later promotes it into a new E<n> and opens its QA-probe. The division's `#### consumers` block is where the collected Q-consumers live, one row each: source page id, the stake in one line, then the A-consumer interpretation and the row state. Its `#### answer digest` is 2-3 lines from the A-executor; the full text stays in the QA-probe record. The anatomy is the core's; this route only says what its rows mean.

## 🗣 What a legal consumer row carries HERE

A Literature Q-consumer carries a POSITIONING STAKE: what the work claims to add, and what published result would strengthen or break that claim.

```
✅  "Is our review-text trait measure novel, or did <field> already do it?
     H1's contribution claim dies if a published precedent exists."
🚫  "Find papers about physician reviews."          no stake · a reading list
🚫  "Confirm nobody has done this."                 a verdict ordered in advance
```

The stake stays on this page. The QA-probe's Q-executor carries the neutral question only, and the wall between them is PROBE's (`page-phases/haipipe-board-page-probe`).

## 📥 What a returned answer must BECOME: the citation binding

An answer that stays in the QA-probe's `#### A-executor` is not yet evidence the page can use. The consumer row's write-back is a typed record with three parts:

```
1  a real key          resolvable in the bibliography, never a title from memory
2  a positioning       one sentence stating how this work stands NEXT TO the
   sentence            found result: extends, contradicts, first-in-setting
3  a novelty verdict   supported · threatened · broken, with the source named
```

🚫 Never write "novelty confirmed" from an ABSENCE of findings alone. Absence after a bounded search is written as "no precedent found within <the search's own scope>", because the search's limits are part of the fact.

## 🚪 When the page closes

The terminal row states, and the rule that the gate reads the E divisions rather than the QA-probes, live in the core (`topic-entry-contract.md`). The close rule on this route: every E<n> division's consumers are terminal AND `E0 · incoming` is empty. This file only says what SUPPORTED takes here: named, real sources standing behind the positioning, which is the citation binding above, written onto the consumer row. A search that came back empty supports nothing by itself; the row either carries the bounded no-precedent finding, scope and all, or it stays open.

## 📂 Files

```
haipipe-board-page-for-literature/
├── SKILL.md            this route dictionary
└── CHANGELOG.md        version history
```

This folder holds prose only. The anatomy lives in `haipipe-board/ref/topic-entry-contract.md` and its checker in `haipipe-board/src/topic_entry_contract.py`; a literature question crosses to the discovery bank through `page-phases/haipipe-board-page-probe`. A question about what this project must PRODUCE, rather than what the field already holds, belongs on a `haipipe-board-page-for-value` page instead. The paper family's projection of the shape is `paper/haipipe-paper/probe/topic-entry-contract.md`.

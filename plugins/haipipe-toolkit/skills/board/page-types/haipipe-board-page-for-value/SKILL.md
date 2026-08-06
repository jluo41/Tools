---
name: haipipe-board-page-for-value
description: >-
  The VARIANT contract for a VALUE evidence Page: an evidence page declaring `route: inward` in its metadata head, whose questions face INWARD, toward results this project must produce. Its Content is organized BY EXECUTOR: one `### E<n> · <question>` division per Q-executor conversation, each owning one QA-probe record below probes/, its collected consumers, and an answer digest, plus the standing `### E0 · incoming` queue. It loads haipipe-board-page for the base frame and the shared topic-entry core for the anatomy, then adds only the inward route's translation layer: what a legal consumer row carries here, what a returned answer must become (a value binding: the number, its run provenance, the claim it serves), and when the page may close. Use when writing or fixing a Value evidence page, when a consumer row names no claim dependency, when a number appears in prose with no run behind it, or when a claim ledger row cannot say which specification produced its estimate. Trigger: value evidence, evidence page, value topic, S-Value, task route, value binding, run provenance, claim ledger, number evidence, /haipipe-board-page-for-value.
metadata:
  version: "0.4.0"
  last_updated: "2026-08-06"
  summary: "Evidence pages organize BY EXECUTOR (JL 260806): the head route: line is the type key, one E<n> Content division per Q-executor conversation with its QA-probe pointer, #### consumers, and #### answer digest, plus the E0 incoming queue; the flat Q-consumer register is retired."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-page-for-value · the inward route: what this project must produce

**LOAD TWO THINGS FIRST.** `haipipe-board-page` gives the frame; `haipipe-board/ref/topic-entry-contract.md` gives the E-division and QA-probe anatomy, which both evidence routes share and neither restates (`QB6 §4`, JL 260805). A QA-probe is a hidden source record named `<n>-<slug>.md`, never a board page (JL ruling B, 260806); it is the paper's stub that points at the QA-bank, the original. What this file adds is the inward route alone. Inward means the answer does not exist yet: the project must RUN something to make it, so every rule here is about chaining a produced number to the run that made it and to the claim that needs it.

**The kind this variant covers**: an evidence page whose questions face INWARD.

```
kind     resolved by                          closes when
─────────────────────────────────────────────────────────────────────
Value    the REQUIRED `route: inward`         every E<n> division's consumers
evidence line in the metadata head            are BOUND, DEFERRED, or
         (base, type resolution step ②)       WITHDRAWN, AND E0 is empty
```

"Value" names a DIRECTION, not a paper section: any family may ask for a number its own work must produce. The paper family's projection files these pages as `S-Value-<n>-<topic>` with `V<n>` probe folders; those letters are family vocabulary and stay in the paper projection. `route: inward` is the REQUIRED head key; it is what separates a page that must produce numbers from one that searches for papers.

## 🧬 The page organizes BY EXECUTOR

One `### E<n> · <the executor question>` Content division per Q-executor conversation; one division owns exactly one QA-probe. `### E0 · incoming` is the collect queue: a Q-consumer born on ANY page is COLLECTED into the owning topic's E0 first, and PROBE later promotes it into a new E<n> and opens its QA-probe. The division's `#### consumers` block holds the collected Q-consumers, one row each: source page id, the stake in one line, then the A-consumer interpretation and the row state. Its `#### answer digest` is 2-3 lines from the A-executor; the full text stays in the QA-probe record. The anatomy is the core's; this route only says what its rows mean.

## 🗣 What a legal consumer row carries HERE

A Value Q-consumer carries a CLAIM DEPENDENCY: which claim rests on the number, and what specification would count as producing it.

```
✅  "H2 states high-dose prescribing rises with the trait score.
     It needs the LBP-cohort estimate, its CI, and the spec that made it."
🚫  "Get the regression results."                    no claim named · a chore
🚫  "Produce an estimate near 0.3."                  the answer ordered in advance
```

The stake stays on this page. The QA-probe's Q-executor asks for the computation in neutral terms, and the bank that runs it never learns which claim would be rescued (`page-phases/haipipe-board-page-probe` owns that wall).

## 📥 What a returned answer must BECOME: the value binding

An answer that stays in the QA-probe's `#### A-executor` is not yet a number the page may print. The consumer row's write-back is a typed record with three parts:

```
1  the value           with its uncertainty, exactly as the run reported it
2  the run provenance  which run, which specification, which QA file · BY PATH
3  the claim update    which claim consumed it, and what its status became:
                       supported · weakened · unresolved
```

🚫 A number whose provenance line is missing is a HOLE, not a result. It reads exactly like a real one, which is why the record, not the prose, is what CHECK audits.

## 🚪 When the page closes

The core owns the terminal row states and the rule that the human gate reads the E divisions, not the QA-probes. The close rule on this route: every E<n> division's consumers are terminal AND `E0 · incoming` is empty. What BOUND takes here is a run you can walk to: the consumer row carries the number together with its run, specification, and QA file, each named by path. A number typed from memory binds nothing. Until the provenance paths exist the row stays open, however right the number looks in the prose.

## 📂 Files

```
haipipe-board-page-for-value/
├── SKILL.md            this route dictionary
├── template.md         the page skeleton to copy, plus the QA-probe record shape
└── CHANGELOG.md        version history
```

Nothing executable ships here. The E-division and QA-probe shape belongs to `haipipe-board/ref/topic-entry-contract.md`, enforced by `haipipe-board/src/topic_entry_contract.py`; the wall a computation request crosses is owned by `page-phases/haipipe-board-page-probe`. A question about what is already published goes to `haipipe-board-page-for-literature`. The paper family projects this shape at `paper/haipipe-paper/probe/topic-entry-contract.md`.

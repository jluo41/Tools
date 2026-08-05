---
name: haipipe-board-page-for-value
description: >-
  The VARIANT contract for a VALUE topic Page: a topic page owning a `### Q-consumer register` whose questions face INWARD, toward results this project must produce, with one probe QA (the entry record) nested below probes/ per neutral executor question. It loads haipipe-board-page for the base frame and the shared topic-entry core for the anatomy, then adds only the inward route's translation layer: what a legal register row carries here, what a returned answer must become (a value binding: the number, its run provenance, the claim it serves), and when the topic may close. Use when writing or fixing a Value topic page, when a register row names no claim dependency, when a number appears in prose with no run behind it, or when a claim ledger row cannot say which specification produced its estimate. Trigger: value topic, value page, S-Value, task route, value binding, run provenance, claim ledger, number evidence, /haipipe-board-page-for-value.
metadata:
  version: "0.3.0"
  last_updated: "2026-08-06"
  summary: "Entries are hidden source records, not board pages (JL ruling B, 260806): one probe QA per neutral executor question, named <n>-<slug>.md below probes/, pointing at its bank QA, with the anatomy in the core contract."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-page-for-value · the inward route: what this project must produce

**LOAD TWO THINGS FIRST.** `haipipe-board-page` gives the frame; `haipipe-board/ref/topic-entry-contract.md` gives the register and entry-record anatomy, which both topic routes share and neither restates (`QB6 §4`, JL 260805). A probe QA is a hidden source record named `<n>-<slug>.md`, never a board page (JL ruling B, 260806); it is the paper's copy that points at the bank QA, the original. What this file adds is the inward route alone. Inward means the answer does not exist yet: the project must RUN something to make it, so every rule here is about chaining a produced number to the run that made it and to the claim that needs it.

**The kind this variant covers**: a topic page whose questions face INWARD.

```
kind     resolved by                          closes when
─────────────────────────────────────────────────────────────────────
Value    the `### Q-consumer register`        every register row is BOUND,
topic    marker plus its REQUIRED             DEFERRED, or WITHDRAWN, per the
         `route: inward` line                 core's Register-row states
```

"Value" names a DIRECTION, not a paper section: any family may ask for a number its own work must produce. The paper family's projection files these pages as `S-Value-<n>-<topic>` with `V<n>` entry folders; those letters are family vocabulary and stay in the paper projection. `route: inward` is the REQUIRED key on the register's first line; it is what separates a page that must produce numbers from one that searches for papers (base, type resolution step ②).

## 🗣 What a legal register row carries HERE

A Value Q-consumer carries a CLAIM DEPENDENCY: which claim rests on the number, and what specification would count as producing it.

```
✅  "H2 states high-dose prescribing rises with the trait score.
     It needs the LBP-cohort estimate, its CI, and the spec that made it."
🚫  "Get the regression results."                    no claim named · a chore
🚫  "Produce an estimate near 0.3."                  the answer ordered in advance
```

The stake stays on this page. The nested probe QA's q-executor asks for the computation in neutral terms, and the bank that runs it never learns which claim would be rescued (`page-phases/haipipe-board-page-probe` owns that wall).

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

The core's Register-row states section owns the three terminal states and the rule that the human gate reads the register, not the entries. What BOUND takes on this route is a run you can walk to: the row carries the number together with its run, specification, and QA file, each named by path. A number typed from memory binds nothing. Until the provenance paths exist the row stays open, however right the number looks in the prose.

## 📂 Files

```
haipipe-board-page-for-value/
├── SKILL.md            this route dictionary
└── CHANGELOG.md        version history
```

Nothing executable ships here. The register and entry shape belongs to `haipipe-board/ref/topic-entry-contract.md`, enforced by `haipipe-board/src/topic_entry_contract.py`; the wall a computation request crosses is owned by `page-phases/haipipe-board-page-probe`. A question about what is already published goes to `haipipe-board-page-for-literature`. The paper family projects this shape at `paper/haipipe-paper/probe/topic-entry-contract.md`.

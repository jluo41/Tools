---
name: haipipe-page-for-literature
description: >-
  The VARIANT contract for a LITERATURE DISPLAY Page: an outward evidence page declaring `route: outward` and `display: companion`, whose questions face published knowledge. Each E division owns a QA-probe and a same-numbered Literature Display companion, so a citation binding becomes a managed matrix, map, or positioning table before Narrative decides whether it belongs in the paper. It adds the outward route's binding rule: real key, positioning sentence, novelty verdict, and candidate-display disposition. Trigger: literature display, literature matrix, theory map, literature topic, discovery route, positioning, novelty, citation binding, related work evidence, /haipipe-page-for-literature.
metadata:
  version: "0.5.0"
  last_updated: "2026-08-10"
  summary: "Literature Display update (JL 260810): each probe has a same-numbered display companion, turning every positioning result into a candidate matrix or map with an explicit disposition before Narrative selects paper material."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-for-literature · Literature Display: what is already known and can be shown

**LOAD TWO THINGS FIRST.** The base frame is `haipipe-page`, and the E-division and QA-probe anatomy is `haipipe-board/ref/topic-entry-contract.md`, stated once for both evidence routes so they cannot drift apart (`QB6 §4`, JL 260805). A QA-probe is a hidden source record named `<n>-<slug>.md`, never a board page (JL ruling B, 260806); it is the paper's stub that points at the QA-bank, the original. This file is the outward route's dictionary and nothing more: what a question aimed at the published record carries, and what a found result must become before this page may lean on it. Any sentence here that seems to describe the page's shape belongs to the core, not to this file.

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

One `### E<n> · <the executor question>` Content division per Q-executor conversation; one division owns exactly one QA-probe. `### E0 · incoming` is the collect queue: a Q-consumer born on ANY page is COLLECTED into the owning topic's E0 first, and EVIDENCE later promotes it into a new E<n> and opens its QA-probe. The division's `#### consumers` block is where the collected Q-consumers live, one row each: source page id, the stake in one line, then the A-consumer interpretation and the row state. Its `#### answer digest` is 2-3 lines from the A-executor; the full text stays in the QA-probe record. The anatomy is the core's; this route only says what its rows mean.

## 🗣 What a legal consumer row carries HERE

A Literature Q-consumer carries a POSITIONING STAKE: what the work claims to add, and what published result would strengthen or break that claim.

```
✅  "Is our review-text trait measure novel, or did <field> already do it?
     H1's contribution claim dies if a published precedent exists."
🚫  "Find papers about physician reviews."          no stake · a reading list
🚫  "Confirm nobody has done this."                 a verdict ordered in advance
```

The stake stays on this page. The QA-probe's Q-executor carries the neutral question only, and the wall between them is EVIDENCE's (`page-workflows/haipipe-page-evidence`).

## 📥 What a returned answer must BECOME: the citation binding

An answer that stays in the QA-probe's `#### A-executor` is not yet evidence the page can use. The consumer row's write-back is a typed record with three parts:

```
1  a real key          resolvable in the bibliography, never a title from memory
2  a positioning       one sentence stating how this work stands NEXT TO the
   sentence            found result: extends, contradicts, first-in-setting
3  a novelty verdict   supported · threatened · broken, with the source named
```

🚫 Never write "novelty confirmed" from an ABSENCE of findings alone. Absence after a bounded search is written as "no precedent found within <the search's own scope>", because the search's limits are part of the fact.

## 🖼 Every probe gets a Literature Display companion

After EVIDENCE returns, the finding has two distinct products: a citation binding that protects the paper's positioning, and a candidate display that makes the positioning visible.
The page declares `display: companion` in its metadata head.
Every nonzero E division therefore carries one `🖼 Display:` pointer to `display/<topic page>/<n>-<slug>.md`, sharing its QA-probe's number and stem.

```text
QA-probe             the neutral question, source search, and answer
Literature Display   the possible matrix, concept map, or positioning table,
                     its five-second takeaway, narrative role, and disposition
```

`not-displayable` is valid when the finding belongs only in prose.
A candidate becomes a formal Paper Display unit only when Narrative selects it and files a Display request.
The companion never owns final caption, render acceptance, or manuscript placement; those remain `haipipe-page-for-display`'s job.
Use `haipipe-board/ref/topic-display-card.md` for its exact shape.

## 🚪 When the page closes

The terminal row states, and the rule that the gate reads the E divisions rather than the QA-probes, live in the core (`topic-entry-contract.md`). The close rule on this route: every E<n> division's consumers are terminal AND `E0 · incoming` is empty. This file only says what SUPPORTED takes here: named, real sources standing behind the positioning, which is the citation binding above, written onto the consumer row. A search that came back empty supports nothing by itself; the row either carries the bounded no-precedent finding, scope and all, or it stays open.

**The template.** `template.md`, beside this file. ONE template serves every page of this type: two pages of it differ in what they say, never in what shape they are, so nothing has to be resolved before writing one. Copy it, fill every `<slot>`, and delete each RULE comment as you satisfy it.

## 📥📤 What this page reads, and what it hands on

**A page is a unit of work** (`QB6` §7). A literature page reads a SHARED bank that lives outside every paper, and hands on a generated bibliography.

```text
 🏦 BANK    paper/venue/literature/bank.bib          shared, hand-maintained,
                                                     one entry per key across all papers
 📥 INPUT   <stage>/QA-probe/<page name>/            one record per question sent out
            + this page's `### Sources already named` claim lines, one per key:
                  - \citep{key} · what job this source does
 📤 OUTPUT  <paper root>/<paper>.bib                 🤖 GENERATED
              ▶ only the keys this paper CLAIMS or CITES; stock stays in the bank
              ▶ printed through the venue's .bst
            <stage>/display/<page name>/<n>-<slug>.md
                                                     candidate Literature Display companion
```

The claim line's second half is the point: claiming a key means saying what job it does, which a bare list cannot carry. A key is added to the bank ONCE and never copied into a paper by hand.

```bash
python3 <skill>/cli/bib-from-bank.py <stage>            # write the .bib
python3 <skill>/cli/bib-from-bank.py <stage> --check    # non-zero if a key is broken
```

Three findings, and only the first is an error: **broken** (used and absent from the bank, so the citation will not resolve), **unclaimed** (cited and no page answers for it), **unused** (claimed and not cited yet, which is normal while drafting).

## 📂 Files

```
haipipe-page-for-literature/
├── SKILL.md            this route dictionary
└── CHANGELOG.md        version history
```

This folder holds prose only. The E-division, QA-probe, and Display companion anatomy lives in `haipipe-board/ref/topic-entry-contract.md` and its checker in `haipipe-board/src/topic_entry_contract.py`; a literature question crosses to the discovery bank through `page-workflows/haipipe-page-evidence`. A question about what this project must PRODUCE, rather than what the field already holds, belongs on a `haipipe-page-for-value` page instead. The paper family's projection of the shape is `paper/haipipe-paper/probe/topic-entry-contract.md`.

---
name: haipipe-board-page
description: >-
  The PAGE contract of a board, as a loadable spec: the base every page kind varies from (Q decision, S stage, Skill mirror), the seven on-stage sections in their fixed order (Opening, Diagram, Content, Items to Finish, Where we are, Files, folds), what each section owes a reader, and where a machine may write into one. Load this when an agent must read or write ONE page without operating the whole board: routing an input to a section, priming a per-page chat session, or authoring a page-kind variant in another family. Trigger: page contract, page grammar, page sections, which section, base page, page kind, /haipipe-board-page.
metadata:
  version: "0.1.0"
  last_updated: "2026-07-31"
  summary: "First cut, contract-first (QC6 §8: a SPEC the routing and digest verbs LOAD): the base/variant model, the seven sections, and the write anchors. No code moved."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-page · the page, as a contract you can load

`haipipe-board` is the door you walk through to RUN a board.
This skill is a SPEC: what a page IS, loadable by an agent that has no board open.
QC6 §7 on the design board states the test it passes: a consumer needs these rules with no board open, and the consumers exist: the routing verb deciding "which page, which section", the chat drawer priming a per-page session, and the variant authors in other families.

**The boundary, and it is a hard one:**

```
haipipe-board-page               haipipe-board
─────────────────────            ──────────────────────────────
what a page IS                   rendering it (src/page_question.py)
the section contract             serving and write-back (serve.py)
where a write may land           the checker (check.py)
the base/variant model           the template file itself (ref/q-template.md)
```

This skill NEVER renders, serves, or checks.
The authoritative template stays `haipipe-board/ref/q-template.md`; this contract cites it and must never fork it.

## 🧬 Three page kinds, one base

A page's KIND comes from its filename, and the kind decides only how the page closes and what its Content holds.
Everything else is the shared base (the model on the design board's QB4, JL 260729).

```
kind          filename                     closes when
─────────────────────────────────────────────────────────────────
Q  decision   Q<group><n>[<face>]-<slug>   its Items boxes all close
S  stage      S-<Family>-<unit>-<slug>     its human gate passes
Skill mirror  Skill-<unit>-<slug>          the unit ships · NEVER counted
```

A page kind used by one consumer family is a VARIANT of the base: it redefines Content only, and it ships under its consumer (`haipipe-paper-stage` is the first), never here.
This skill owns the BASE those variants extend.

## 📑 The seven sections, in their fixed on-stage order

```
#   section            owes the reader                      a machine may write
──────────────────────────────────────────────────────────────────────────────────
1   Opening            the lead question + the drawer       nothing
                       (Structure · Boundary · Why)         (render-derived)
2   Diagram            the figure; ids in it are links      nothing without the human
3   Content            the substance, ### divisions         nothing without the human
4   Items to Finish    the testable gap, - [ ] boxes        PROPOSE a tick, never tick
5   Where we are       the state mirror, dated entries      append a dated entry
6   Files              engine · inputs · outputs            append a row
7   folds              Discussion · Law · Lesson · Log      append a Log or > lane line
```

Subsection names inside Items, Where we are, and Files are CONTEXTUAL (JL 260729): they come from the page's subject, and any names a spec shows are examples, not a taxonomy.

**The write anchor rule (QC6 §9, from a real casualty).**
A machine write lands at a SECTION BOUNDARY, never at a byte offset: on 260730 a concurrent session spliced a `###` block into the middle of another page's `## Opening` sentence.
Appending under a named `## ` heading is safe; inserting by offset is how that damage reproduces at scale.

**The tick rule (QC6 §10).**
A verb reading a transcript can report what the transcript CLAIMS, not verify it.
So a machine may write Log lines and Where-we-are prose and may PROPOSE a tick; it may not close a checkbox or flip `state:`.

## 🏷 Addressing

```
page        QB4            #QB4
face        QB4a           a page whose id carries its parent's number
group       #group-QB      scrolls the index, opens nothing
sentence    QB5's grammar  haipipe-board-sentence owns everything below the section
```

Every id inside a fenced figure renders as a link (haipipe-board 0.53.0), so a contract that names pages is itself a map.

## 📂 Files

```
haipipe-board-page/
├── SKILL.md            this contract
└── CHANGELOG.md        version history
```

Reads `haipipe-board/ref/q-template.md` and `ref/board-form.md` §8 as the authority; owns no scripts at 0.1.0.
The named next step (QC6 §7): `serve.py`'s hand-rolled `CHAT_RULES` string becomes this contract's consumer instead of restating it, which kills the copy that has already rotted once.

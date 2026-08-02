---
name: haipipe-board-sentence
description: >-
  The SENTENCE contract of a board, as a loadable spec: the sentence as the board's atomic unit, its dotted address, the > comment lanes and who may write one, the evidence card, editing, per-location chat focus, and the lifecycle of attached records (archive, never delete). Load this when an agent must write ONE line that reads like the board without operating the whole board: a routed log line, a comment into a lane, a chat focus packet, or the paper family's evidence card. Trigger: sentence contract, comment lane, > lane, evidence card, sentence address, apparatus, /haipipe-board-sentence.
metadata:
  version: "0.1.2"
  last_updated: "2026-08-02"
  summary: "The lane figure and the lane rules teach `> Comment WHO`, the only comment form to write since 260802, and mark ## Discussion's thread grammar as unaffected."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-sentence · the sentence, as a contract you can load

Below the section sits the board's atomic unit: one sentence, one row on the rendered page, one anchor.
This skill is the SPEC for everything that attaches to it, loadable by an agent with no board open.
Its consumers are the routing and digest verbs (a routed write must READ LIKE THE BOARD), the chat drawer teaching an agent what a lane is, and the paper family's evidence card.

**The boundary, and it is a hard one:**

```
haipipe-board-sentence           haipipe-board
─────────────────────            ──────────────────────────────
what a sentence IS               rendering it (src/body.py)
the lane grammar                 the comment write path (serve.py)
the evidence card's contract     the card's popover HTML
the record lifecycle             the details panel's controls
```

This skill NEVER renders or serves.
The grammar's authority is `haipipe-board/ref/board-form.md` §5; this contract cites it and must never fork it.

## ✍️ The unit and its address

One prose line in the source is one sentence on the page: that is why prose is written ONE SENTENCE PER LINE (`check.py` warns on a hard wrap, because a wrapped sentence renders as a broken row).

```
QB5.C1.P1.S1        Content division 1 · paragraph 1 · sentence 1
                    UPPERCASE+digit tokens, so a section slug can
                    never collide with a coordinate
```

The address is how chat focuses one location, how a comment pins, and how an edit names what it replaces.

## 💬 The lanes

A `>` line under a sentence is a LANE: a signed, dated remark that belongs to the sentence above it.

```
> Comment JL …   the human's lane · decisions and corrections live here
> ✎ ~old~ *new* · WHO · YYMMDD HHMM   the change record
> Citation: · > Value: · > Display: …  the typed lanes, named by what they attach
>> CC{MMDD}: the worker's dated reply lane, nested under what it answers
```

Lane rules a machine must hold:

```
· a lane is APPENDED, never edited in place; the record is the point
· a person's remark is `> Comment WHO …`, the only form to write (JL 260802);
  the older `> JL:` still renders and check.py warns on it inside Content
· `## Discussion` is NOT affected: it keeps `> JL:` + `>> CC0726:`, a THREAD
· never delete a signed comment or `> ✎` line (ref/writing-rules.md: they are the durable review trail)
· a reply nests one level under what it answers, dated
· a lane without a signature is not a lane, it is unclaimed prose
```

## 🃏 The evidence card

A marker in a sentence (a citation, a value, a display unit) renders as a chip whose card shows the THING, not a description of it: the reference as the paper's own .bst prints it, the figure itself, the rows themselves.
The card is a strict superset of a bare link, which is why a display unit's name in prose ALWAYS renders as the card (JL 260727).
This contract owns what a card must show; the paper dialect that resolves markers stays deletable (`haipipe-board/src/dialect_paper.py`).

## ♻️ The record lifecycle

The canonical sentence normally REMAINS; what ages is what attaches to it.

```
comment lanes · evidence · edit records     archive on resolution, restorable
the sentence itself                         edited through the page, logged
nothing                                     is ever silently deleted
```

Resolved threads leave the stage for the archive the same way a retired page leaves for `_archive/`: recoverable, out of the read.

## 📂 Files

```
haipipe-board-sentence/
├── SKILL.md            this contract
└── CHANGELOG.md        version history
```

Reads `haipipe-board/ref/board-form.md` §5 as the authority; owns no scripts at 0.1.0.
The named next step (QC1b §1): the drawer's lane instructions in `live/chat.py` become this contract's consumer instead of a second prose copy.

---
name: haipipe-board-sentence
description: >-
  The SENTENCE contract of a board, as a loadable spec: the sentence as the board's atomic unit, its dotted address, the > comment lanes and who may write one, the evidence card on a span of words, editing, per-location chat focus, and the lifecycle of attached records (archive, never delete). Load this when an agent must write ONE line that reads like the board without operating the whole board: a routed log line, a comment into a lane, a chat focus packet, or the paper family's evidence card. TWO USES, and this skill is the door for both: RUN a verb on one sentence (comment on it, edit it, put a card on its words) or LOAD it as a pure contract with no board open. Trigger: comment on this sentence, edit this sentence, card on these words, sentence contract, comment lane, > lane, evidence card, sentence address, apparatus, /haipipe-board-sentence.
metadata:
  version: "0.3.0"
  last_updated: "2026-08-02"
  summary: "Became the DOOR for one sentence, not only its spec: comment, edit and card are its three verbs, migrated out of haipipe-board's SKILL.md on the haipipe-board-page precedent."
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

**The boundary, and it is the same hard one `haipipe-board-page` keeps:**

**Who owns what**: this skill holds the contract, `haipipe-board` holds the machinery.

```
haipipe-board-sentence           haipipe-board
─────────────────────            ──────────────────────────────
what a sentence IS               rendering it (src/body.py)
what may attach, and how         the write routes (live/write.py, serve.py)
which gesture reaches which      the controls (assets/js/40-sentence/)
where a write may land           the checker (cli/check.py)
the two anchors                  the recorded drive (tests/drive_sentence.py)
```

This skill never CONTAINS the renderer, the server or the controls. It CALLS them, because someone asking to comment on one line should not have to know which file does what.

## 🚪 Three verbs, and this skill is the door for all of them

Say any of these and this skill runs it. You never call the engine yourself.

```
💬 COMMENT    /haipipe-board-sentence comment on "<the sentence>"
✎ EDIT       /haipipe-board-sentence edit "<the sentence>"
🪪 CARD       /haipipe-board-sentence card on "<the words>"
```

### 💬 comment · a person's remark under one line

Hover the sentence and click the `＋` in its rail, or select text inside it and click 💬 Comment, then Save. The live layer writes `> Comment WHO … · YYMMDD HHMM` directly beneath that sentence and rebuilds.

There is no comment box at the bottom of the page and never will be: a queue down there makes the reader rebuild the context the writer already had. `## Discussion` is a different grammar and holds only discussion pinned to no sentence.

### ✎ edit · replace one line, leave one record

Double-click the sentence, change the words, Save. The source line is replaced and one word-level record is written beside it:

```
The coefficient is 0.42 in the clustered pooled model.
> ✎ The coefficient is 0.42 in the *clustered* pooled model. · JL · 260729 1502
```

The old wording is never stored a second time and no History section is built. A duplicate sentence and a sentence carrying markdown decoration are both REFUSED rather than guessed at. Locks and concurrent writers are not this skill's: they belong to the board's `QE4`.

### 🪪 card · attach a panel to a few words

Select the words and click 🪪 Card, or type the line yourself. See `## 🃏 The evidence card` below for both sources and what the render refuses.

### What every verb must hold

```
· the anchor is an EXACT match on the source line; a miss FAILS VISIBLY
· a form CLOSES before it asks for the repaint, or the swap refuses it:
  the swap will not run while a textarea inside div.wrap holds text, which
  is the rule that stops a rebuild from eating a half-written comment
· a write needs serve.py; with it down the page keeps a pending line or a
  copyable patch and never grows a comment area at the foot of the page
· the badge names WHICH KIND is underneath: 💬 waiting ▸ ✎ change ▸ ⚑ lane
```

## 🏷 The reader's controls

```
🖱 hover      the address, ＋ Comment, 💬 Chat fade in on the right
🖱 dblclick   edit this sentence
📱 touch      one quiet ⋯ expands to the address plus Comment · Chat · Edit
🔒 default    every attached record starts SHUT; one click opens
```

A single click on the body is unclaimed on purpose, so selecting and copying still work normally.


## 💬 The lanes

A `>` line under a sentence is a LANE: a signed, dated remark that belongs to the sentence above it.

```
> Comment JL …   the human's lane · decisions and corrections live here
> ✎ ~old~ *new* · WHO · YYMMDD HHMM   the change record
> Citation: · > Value: · > Display: …  the typed lanes, named by what they attach
> Card the words: what to show   the ONE lane that renders INSIDE the sentence
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

TWO SURFACES, TWO ANCHORS (JL 260802). A LANE anchors to the whole line and opens in a drawer beneath it. A CARD anchors to a few WORDS inside the line and opens over the prose when those words are clicked. A machine writing one must know which it is producing.

```
anchor       ① the marked words          ② the whole sentence
opens        over the prose              a drawer below it
holds        one thing                   any number, any kind
answers      "what is this?"             "what do we know about this line?"
```

A card has two sources and the same render:

```
✍️ a record       > Card the words: what to show
   the span is QUOTED in the record, so the prose gains no marker and no id;
   the renderer finds those words in the sentence above by exact text, the
   same match `serve.py` uses one level up to find a sentence.
   Words it cannot find render as a LOUD row in the drawer, never as silence.

📐 a paper marker  \citep{} · {VAL:? …} · [Q-X-n] · displayNN · \ref{}
   the marker names itself, and the build resolves it against .bib,
   1-probes/ and displays/. The paper dialect stays deletable.
```

The words KEEP THE PROSE'S OWN FONT, COLOUR AND WEIGHT and take one dotted underline. A box around them turns a paragraph into a row of buttons, which costs more attention than the card is worth.

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

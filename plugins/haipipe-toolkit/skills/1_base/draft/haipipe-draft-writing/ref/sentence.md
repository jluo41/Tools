# The sentence contract

Part of `haipipe-draft-writing` (was the skill `haipipe-sentence`, folded in 2026-10-16, JL 261016; its history is `history/haipipe-sentence-CHANGELOG.md`). The old triggers (comment on this sentence, edit this sentence, sentence address, `/haipipe-sentence`) now reach `haipipe-draft-writing`.

## The sentence, as a contract you can load

Below the section sits the board's atomic unit: one sentence, one row on the rendered page, one anchor.
This skill is the SPEC for everything that attaches to it, loadable by an agent with no board open.
Its consumers are the routing and digest verbs (a routed write must READ LIKE THE BOARD), the chat drawer teaching an agent what a lane is, and the paper family's evidence card.

**The boundary, and it is a hard one:**

```
sentence contract           haipipe-draft
─────────────────────            ──────────────────────────────
what a sentence IS               rendering it (src/body.py)
the lane grammar                 the read-only Page controls
evidence cards: haipipe-evidence    the card popover HTML
the record lifecycle             the details panel's controls
```

This skill NEVER renders or serves.
The grammar's authority is `haipipe-draft/ref/board-form.md` → Body grammar; this contract cites it and must never fork it.

## ✍️ The unit and its address

One prose line in the source is one sentence on the page: that is why prose is written ONE SENTENCE PER LINE (`check.py` warns on a hard wrap, because a wrapped sentence renders as a broken row).

```
QB8.C1.P1.S1        Content division 1 · paragraph 1 · sentence 1
                    UPPERCASE+digit tokens, so a section slug can
                    never collide with a coordinate
```

The rendered address locates the passage in a copied prompt. It is recomputed on rebuild, so the agent must also use the source path and quoted wording when finding a sentence.

**The boundary, and it is the same hard one `haipipe-draft` keeps:**

**Who owns what**: this skill holds the contract, `haipipe-draft` holds the machinery.

```
sentence contract           haipipe-draft
─────────────────────            ──────────────────────────────
what a sentence IS               rendering it (src/body.py)
what may attach, and how         the source helpers (servers/space-home/write.py)
which gesture reaches which      the controls (assets/js/40-sentence/)
where a write may land           the checker (cli/check.py)
the two anchors                  the recorded drive (tests/drive_sentence.py)
```

This skill never CONTAINS the renderer, the server or the controls. It CALLS them, because someone asking to comment on one line should not have to know which file does what.

## 🚪 Three verbs, and this skill is the door for all of them

Request these actions in an agent conversation, with a copied passage and an explicit instruction. The browser Page itself is read-only. Resolve the owning Page workflow before
writing: a bounded sentence/paragraph feedback request resumes or selects its
Page Run as described in `../../haipipe-draft/SKILL.md`. During a Writing Step,
save the candidate and feedback in that Run; adopted Page Content and delivery
are updated at Page release. For a direct source maintenance change outside a
Run, apply the authorized change to the matched source and rebuild the Page.

```
💬 COMMENT    /haipipe-draft-writing comment on "<the sentence>"
✎ EDIT       /haipipe-draft-writing edit "<the sentence>"
🪪 CARD       /haipipe-draft-writing card on "<the words>"
```

### 💬 comment · a person's remark under one line

Click `⧉ Copy prompt` beside the sentence, or select a passage and copy its prompt. Paste into your agent conversation and request a comment. For an authorized source change, the comment is `> Comment WHO … · YYMMDD HHMM` directly beneath the matched sentence. Active Run feedback follows the workflow boundary above.

There is no comment box at the bottom of the page and never will be: a queue down there makes the reader rebuild the context the writer already had. `## Discussion` is a different grammar and holds only discussion pinned to no sentence.

Candidate sentences in the Outline Draft Space do not use this published
sentence address grammar or a paragraph Comments composer. Copy the saved
`C.P.B` sentence into chat and give feedback through the active Page Run;
`workbench-task-draft/ref/content-preview.md` owns that rehearsal boundary.
Historical signed review lanes remain embedded in the Outline Markdown but are
not rendered.

### ✎ edit · replace one line, leave one record

Copy the sentence prompt and tell the agent the replacement you want. When the owning workflow allows the source change, match the source line, replace it, and record the change beside it:

```
The coefficient is 0.42 in the clustered pooled model.
> ✎ The coefficient is 0.42 in the *clustered* pooled model. · JL · 260729 1502
```

Keep the old/new wording in the sentence-local change record; do not create a separate History section. A duplicate sentence and a sentence carrying markdown decoration are both REFUSED rather than guessed at. Locks and concurrent writers are not this skill's: they belong to the board's `QE4`.

An Opening-wide or partial-selection prompt is context, not an exact replacement
anchor. Resolve it to the unique source line using the path, quotation, and any
full-sentence context. If multiple lines could match, ask which line or scope
the user means before changing source.

### 🪪 card · attach a panel to a few words

Select the words, copy the prompt, and ask the agent to attach a Card to that exact span. See `## 🃏 Evidence on a span of words` below.

### What every verb must hold

```
· the anchor is an EXACT match on the source line; a miss FAILS VISIBLY
· source changes require a user's request; copying context never submits one
· the generated Page is read-only; do not call the retired /_board/comment,
  /edit-sentence, /sentence, /card, /discuss, or /resolve browser endpoints
· keep existing signed comments, evidence lanes, and edit records readable
· follow the Page workflow boundary above for adoption and rebuilding
```

## 🏷 The reader's controls

```
🖱 hover/focus   a location label and one ⧉ Copy prompt button
🖱 selection     normal text selection; ⧉ Copy prompt includes the selected passage
🖱 dblclick      normal word selection; never an inline editor
📱 touch         the same copy button, directly available
🔒 default       attached records start shut; one click opens them for reading
```

Sentence, Opening, and heading prompts include the Page id, Board/source
paths, location, quoted text, and available attached context, followed by a
blank `My request:` field. Paste that into an agent conversation and add the
requested action. Copying does not open chat or write to Markdown. The Page
has no Comment, Chat, Card creation, or Edit control. Evidence-card viewing,
folding, and navigation remain available. Explicit workbench workspaces have
their own controls.


## 💬 The lanes

A `>` line under a sentence is a LANE: a signed, dated remark that belongs to the sentence above it.

```
> Comment JL …   the human's lane · decisions and corrections live here
> ✎ ~old~ *new* · WHO · YYMMDD HHMM   the change record
> Citation: · > Value: · > Display: · > Supporting Run: …  the typed lanes, named by what they attach
> Card the words: what to show   the ONE lane that renders INSIDE the sentence
>> CC{MMDD}: the worker's dated reply lane, nested under what it answers
```

Lane rules a machine must hold:

```
· a lane is APPENDED, never edited in place; the record is the point
· a person's remark is `> Comment WHO …`, the only form to write (JL 260802);
  the older `> JL:` still renders and check.py warns on it inside Content
· `## Discussion` is NOT affected: it keeps `> JL:` + `>> CC0726:`, a THREAD
· never delete a signed comment or `> ✎` line (haipipe-draft/ref/writing-rules.md: they are the durable review trail)
· a reply nests one level under what it answers, dated
· a lane without a signature is not a lane, it is unclaimed prose
```

## 🃏 Evidence on a span of words

The evidence card, and the exact words it backs (its `anchor`), are `haipipe-evidence`'s: see `../../../evidence/haipipe-evidence/SKILL.md` (`anchor`, `for`, `cards.yaml`). This contract does not define a second card format.
What stays here is only the sentence side: a `> Card the words: what to show` lane under a sentence quotes the span, the renderer finds those words in the sentence above by exact text, and words it cannot find render as a loud row, never as silence. Markers in a sentence (`\citep{}`, `{VAL:? ...}`, `[Q-X-n]`, `displayNN`, `\ref{}`) are resolved by the paper dialect (`haipipe-draft/src/dialect_paper.py`), which stays deletable.

## ♻️ The record lifecycle

The canonical sentence normally REMAINS; what ages is what attaches to it.

```
comment lanes · evidence · edit records     archive on resolution, restorable
the sentence itself                         edited in source by request, logged
nothing                                     is ever silently deleted
```

Resolved threads leave the stage for the archive the same way a retired question leaves for a BOARD's own `_archive/`: recoverable, out of the read. (That board-level archive is live machinery and is not the skill-tree `_archive/` deleted on 260822.)

## 📂 Where it lives

This file is `haipipe-draft-writing/ref/sentence.md`; history is `ref/history/haipipe-sentence-CHANGELOG.md`. It owns no scripts.
Reads `haipipe-draft/ref/board-form.md` → Body grammar as the authority.

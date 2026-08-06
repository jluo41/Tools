# haipipe-board-sentence · v0.3.1
state: 🟡 in flux · became a door 260802; four releases that day, all now in the changelog
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
`haipipe-board-sentence` is the contract for one source line, the board's smallest addressable thing, and since 260802 it is also the door that runs three verbs on one.
A line renders as one row a reader can click.
Two things attach to that line and they are not the same: a card takes a few marked WORDS and renders inside the sentence, and a `>` lane takes the whole line and renders under it.

**Since when it is a door**: say `comment on "<the sentence>"`, `edit "<the sentence>"` or `card on "<the words>"` and this skill runs that verb.
`haipipe-board-page` is what you reach for when the question is which SECTION a write belongs in rather than which line.

**What the words mean**: an address like `QB8.C1.P1.S1` points at one sentence, reading page `QB8`, Content division 1, paragraph 1, sentence 1.
A lane is a signed `>` line written beneath that sentence, such as `> Comment JL …` for a person's remark or `> ✎ the sentence with ~removed~ *added* words · CC · 260802 1720` for a change record.
A card is different: `> Card the words: what to show` quotes a span from the line above, and the reader sees those very words carry a panel, keeping the prose's own font, colour and weight.

**What changed on 260802**: `QB8` closed with all 16 of its Aims met and JL moved the line on what this unit is.
It stopped being only a thing an agent LOADS and became a thing a person RUNS, with three verbs that write to one line: comment, edit, card.
The rules the verbs share are the interesting part, because each is a scar: the anchor is an exact match on the source line and a miss fails visibly, a form must close before it asks for the repaint so a rebuild cannot eat a half-written comment, and a duplicate sentence is REFUSED rather than guessed at.

**Covered elsewhere**: which section a write lands in, and what a whole page owes its reader, belong to `haipipe-board-page`.
Rendering the line (`src/body.py`), the write path (`live/write.py`) and the popover a card opens in are `haipipe-board`'s, and locks and concurrent writers are `QE4`'s.
The grammar's authority is `haipipe-board/ref/board-form.md` §5, which this spec cites and is forbidden to fork.

**Where it stands**: 0.1.0 to 0.3.0 in two days, and the door half, shipped 260802, still has nothing measured against it.
Its three named consumers are still only named: `live/chat.py`, whose duplicated lane rules justified cutting this spec out in the first place, still teaches the grammar from its own Python prose.
The release that made it a door shipped with no changelog entry and `cli/agree.py` caught it; the entry was reconstructed from the shipped file on 260802 and the tool now reports clean.

## Diagram
<!-- haipipe:skill:tree:start f458d05475e3651a board/haipipe-board-sentence -->

**What `haipipe-board-sentence` ships**: every file in the folder, with the one-line purpose each one states for itself.

```
haipipe-board-sentence/
  CHANGELOG.md          80 ln  haipipe-board-sentence · Changelog
  SKILL.md             191 ln  /haipipe-board-sentence · the sentence, as a contract you can load
```

<!-- haipipe:skill:tree:end -->

**Two anchors, three verbs**: what attaches to a few WORDS renders inside the line; what attaches to the LINE renders under it.

```text
WORKFLOW  one line, two anchors, and the three verbs that write to it

  ONE source line  =  ONE row on the page  =  ONE anchor
  prose is one sentence per line; check.py warns on a hard wrap,
  because a wrapped sentence renders as a broken row
        │
        ▼
  QB8.C1.P1.S1     page · Content division · paragraph · sentence
                   UPPERCASE and digit tokens only, so a section
                   slug can never collide with a coordinate
        │
   ┌────┴─────────────────────────┐
   ▼                              ▼
 🪪 ON THE WORDS                 📎 ON THE LINE
   > Card the words: …             > Comment WHO …      a person's remark
   quotes a span above             > ✎ ~old~ *new* …    the change record
   renders INSIDE the             > Citation: · Value:  the typed lanes
   sentence, keeping the           renders UNDER the line
   prose's own font and            badge says which kind is below:
   colour                          💬 waiting ▸ ✎ change ▸ ⚑ lane

  ── the three verbs it now RUNS (0.3.0, JL moved the line 260802) ──
  💬 comment on "<the sentence>"   ✎ edit "<the sentence>"
  🪪 card on "<the words>"
     · the anchor is an EXACT match; a miss FAILS VISIBLY
     · a form CLOSES before the repaint, or the swap refuses it, so a
       rebuild cannot eat a half-written comment
     · a duplicate sentence is REFUSED, never guessed at
     · a write needs serve.py; with it down the page keeps a pending
       line and never grows a comment area at its foot

  ── the boundary ──────────────────────────────────────────────────
  this says what a sentence IS and runs the three verbs on one.
  haipipe-board RENDERS it (src/body.py), WRITES it (live/write.py)
  and serves the popover. haipipe-board-page owns which SECTION.
  QE4 owns locks. board-form.md §5 is the authority this must not fork.
```

## Content
<!-- haipipe:skill:body:start f458d05475e3651a board/haipipe-board-sentence -->

**haipipe-board-sentence** · `0.3.1` · last shipped 2026-08-03

- folder   `board/haipipe-board-sentence/`
- tools    not declared
- summary  Became the DOOR for one sentence, not only its spec: comment, edit and card are its three verbs, migrated out of haipipe-board's SKILL.md on the haipipe-board-page precedent.

### SKILL.md




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


- 1 · ✍️ The unit and its address
      One prose line in the source is one sentence on the page: that is why prose is written ONE SENTENCE PER LINE (`check.py` warns on a hard wrap, because a wrapped sentence renders as a broken row).
      ```
      QB8.C1.P1.S1        Content division 1 · paragraph 1 · sentence 1
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

- 2 · 🚪 Three verbs, and this skill is the door for all of them
      Say any of these and this skill runs it. You never call the engine yourself.
      ```
      💬 COMMENT    /haipipe-board-sentence comment on "<the sentence>"
      ✎ EDIT       /haipipe-board-sentence edit "<the sentence>"
      🪪 CARD       /haipipe-board-sentence card on "<the words>"
      ```

- 2.1 · 💬 comment · a person's remark under one line
      Hover the sentence and click the `＋` in its rail, or select text inside it and click 💬 Comment, then Save. The live layer writes `> Comment WHO … · YYMMDD HHMM` directly beneath that sentence and rebuilds.
      There is no comment box at the bottom of the page and never will be: a queue down there makes the reader rebuild the context the writer already had. `## Discussion` is a different grammar and holds only discussion pinned to no sentence.

- 2.2 · ✎ edit · replace one line, leave one record
      Double-click the sentence, change the words, Save. The source line is replaced and one word-level record is written beside it:
      ```
      The coefficient is 0.42 in the clustered pooled model.
      > ✎ The coefficient is 0.42 in the *clustered* pooled model. · JL · 260729 1502
      ```
      The old wording is never stored a second time and no History section is built. A duplicate sentence and a sentence carrying markdown decoration are both REFUSED rather than guessed at. Locks and concurrent writers are not this skill's: they belong to the board's `QE4`.

- 2.3 · 🪪 card · attach a panel to a few words
      Select the words and click 🪪 Card, or type the line yourself. See `## 🃏 The evidence card` below for both sources and what the render refuses.

- 2.4 · What every verb must hold
      ```
      · the anchor is an EXACT match on the source line; a miss FAILS VISIBLY
      · a form CLOSES before it asks for the repaint, or the swap refuses it:
        the swap will not run while a textarea inside div.wrap holds text, which
        is the rule that stops a rebuild from eating a half-written comment
      · a write needs serve.py; with it down the page keeps a pending line or a
        copyable patch and never grows a comment area at the foot of the page
      · the badge names WHICH KIND is underneath: 💬 waiting ▸ ✎ change ▸ ⚑ lane
      ```

- 3 · 🏷 The reader's controls
      ```
      🖱 hover      the address, ＋ Comment, 💬 Chat fade in on the right
      🖱 dblclick   edit this sentence
      📱 touch      one quiet ⋯ expands to the address plus Comment · Chat · Edit
      🔒 default    every attached record starts SHUT; one click opens
      ```
      A single click on the body is unclaimed on purpose, so selecting and copying still work normally.

- 4 · 💬 The lanes
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

- 5 · 🃏 The evidence card
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

- 6 · ♻️ The record lifecycle
      The canonical sentence normally REMAINS; what ages is what attaches to it.
      ```
      comment lanes · evidence · edit records     archive on resolution, restorable
      the sentence itself                         edited through the page, logged
      nothing                                     is ever silently deleted
      ```
      Resolved threads leave the stage for the archive the same way a retired page leaves for `_archive/`: recoverable, out of the read.

- 7 · 📂 Files
      ```
      haipipe-board-sentence/
      ├── SKILL.md            this contract
      └── CHANGELOG.md        version history
      ```
      Reads `haipipe-board/ref/board-form.md` §5 as the authority; owns no scripts.
      The named next step (QC1b §1): the drawer's lane instructions in `live/chat.py` become this contract's consumer instead of a second prose copy.
<!-- haipipe:skill:body:end -->

## Aims
- [x] 📓 The release that made it a door is written down
      `cli/agree.py` reported `SKILL.md says 0.3.0 · CHANGELOG.md shipped 0.2.0`, so the three verbs shipped with no changelog entry at all.
      Reconstructed from the shipped file on 260802 and marked as reconstructed, since it was written after the fact rather than at release time; the tool now reports clean.
      The finding came from `Skill-7`'s own tool pointed at this family, which is the first time one skill page checked another.
- [ ] 🧪 Something is measured against the door half
      It gained three verbs on 260802 and nothing has exercised them from this contract: no run, no fresh agent choosing this door, no check that the exact-match anchor fails visibly the way the page says it does.
      Its two shared rules read as scars from real incidents, which is a good sign about their origin and no evidence at all about their current state.
- [ ] 🧹 `live/chat.py` loads this spec instead of restating it
      Two of its four rule strings teach the lane grammar in Python prose, and `QB8d` caught one describing a page shape that no longer existed.
      This is `A6.1` on `QC1b`, it is the consumer whose duplication justified cutting this spec out, and it still has not become a consumer.
- [ ] 🔗 The no-fork promise is checked, not just written
      This contract cites `haipipe-board/ref/board-form.md` §5 as the authority and promises never to fork it, and it doubled in size to 191 lines while nothing verified that promise.
      A spec that quietly restates its authority is the exact failure it was cut out to prevent.

## States
The ground moved under this page on 260802: `QB8` closed with all 16 Aims met, and this unit went from a 94-line contract an agent loads to a 191-line door a person runs, across three releases in two days.
Its health is `🟡 in flux` for one reason now: the door half, shipped 260802, still has nothing measured against it.

- 260802 JL · 🚪 It stopped being only a SPEC
  `QB8` settled the sentence as the board's atomic unit and handed each attachment its own page, and the skill followed by taking three verbs: comment, edit, card.
  The roster on `QC1b` had it filed as a pure SPEC beside `haipipe-board-page`, which is now half true, and the same misfiling is what hid `haipipe-board-index`'s duplication for two days.
- 260802 CC · 📓 A tool built one page over found the drift on this one
  `Skill-7`'s `cli/agree.py` compares two statements of one fact and reported this unit's `SKILL.md` at 0.3.0 against a changelog shipping 0.2.0.
  That is the first time a skill page was checked by another skill page's engine rather than by a person reading it, which is worth more than the defect it found.
- 260802 CC · ⚠️ This page contradicted itself for several hours
  The derived Content span carried `Three verbs, and this skill is the door for all of them` while the authored fence directly above it still read `loaded, never run`.
  A sync updates the derived half and cannot touch the authored one, so a page can be green on `skillpage.py check` and self-contradictory on screen, which is the sharpest example yet of why that check covers frontmatter only.

## Log
- 260806 2115 · [REVISE-CC] swept to the 260806 architecture; head state line's release count corrected from three to four (CHANGELOG dates 0.1.1, 0.1.2, 0.2.0 and 0.3.0 all to 260802), every cited path and pointer verified live
- 260806 0140 · [REVISE-CC] card synced to disk truth after 260805 (ten types · thin-paper phase 2 · first live RUN); the "one day old" age clauses on the door half now date it 260802 instead, and no 260805 change touched this unit.
260802 2030 · Rewritten after `QB8` closed and this unit reached 0.3.0: the Opening and the `WORKFLOW` fence had said `loaded, never run` while the page's own derived Content announced three verbs. Four Aims replace the earlier set, including the missing 0.3.0 changelog entry that `agree.py` found, and `state:` now names the two live problems rather than the one it had
260802 1720 · Authored half written: the `WORKFLOW` fence replaced the template placeholder with the address, the three consumers and the boundary, four real Aims replaced the single health placeholder, and `state:` moved from 🔴 to 🟡 in flux. Recorded plainly that this unit's consumers are declared rather than measured, and that `live/chat.py`, the consumer that justified cutting it out, still carries its own copy
260731 1116 · page generated from `board/haipipe-board-sentence/` by `skillpage.py new`

<!-- haipipe:skill:log:start f458d05475e3651a board/haipipe-board-sentence -->

Converted from the skill's own `CHANGELOG.md`: 7 releases.

260803 · `0.3.1`
      **Board bucket review, 260803** (JL: "go ahead to solve yourself, dont ask me"). Ledger: `skills/_console/260803-board-bucket-review.md`.
      - The Files block said "owns no scripts at 0.1.0", a version string frozen three releases back.
260802 · `0.3.0`
      **🚪 Became the DOOR for one sentence, not only its spec** (JL 260802: "if we want to put sentence things, we migrate that part from haipipe-board to haipipe-board-sentence, just like haipipe-board-page, right?").
      The `haipipe-board-page` precedent is precise about what migrates: that skill owns the page contract and its two verbs, owns no scripts, and CALLS the engine. This unit had it the other way round, with the operating detail living in `haipipe-board`'s SKILL.md while this file was 94 lines of spec carrying no verbs at all.
      - **Three verbs**, migrated out of `haipipe-board` 0.111.0: `comment` (a person's remark under one line), `edit` (one line replaced, one word-level record), `card` (a panel on a few words inside the line).
      - **The boundary block**, mirroring the page skill's: this holds what a sentence IS, what may attach, which gesture reaches which, and the two anchors. `haipipe-board` keeps the renderer, the write routes, the controls, the checker and the recorded drive.
      - **The reader's controls**: hover rail, double-click to edit, one `⋯` on touch, every record shut by default.
      - **What every verb must hold**: the anchor is an exact match and a miss fails visibly; a form CLOSES before it asks for the repaint, because the live swap will not run while a textarea inside `div.wrap` holds text.
      192 lines, against the page skill's 299.
260802 · `0.3.0`
      ⚠️ **Entry reconstructed on 260802 from the shipped file, not written at release time.**
      `cli/agree.py` reported `SKILL.md says 0.3.0 · CHANGELOG.md shipped 0.2.0`, so the release that changed what this unit IS went unrecorded. What follows is read off the committed `SKILL.md`; if the author of 0.3.0 meant more by it, this entry is the floor and not the ceiling.
      **This skill stopped being only a contract and became a DOOR.** Its `description` now opens "TWO USES, and this skill is the door for both: RUN a verb on one sentence or LOAD it as a pure contract."
      - `## 🚪 Three verbs, and this skill is the door for all of them` is new: `comment` on a sentence, `edit` one line and leave one record, and `card` on a few words. Say any of them and this skill runs it; the caller never touches the engine.
      - `### What every verb must hold` is new, and every line of it is a scar: the anchor is an EXACT match on the source line and a miss FAILS VISIBLY; a form CLOSES before it asks for the repaint, or the swap refuses it, which is what stops a rebuild eating a half-written comment; a write needs `serve.py` and with it down the page keeps a pending line rather than growing a comment area at its foot; and the badge names WHICH KIND is underneath.
      - `## 🏷 The reader's controls` is new: hover for the address plus Comment and Chat, double-click to edit, one quiet `⋯` on touch, every attached record SHUT by default, and a single click on the body left unclaimed so selecting and copying still work.
      **Two consequences nobody recorded either.** The roster on the design board's `QC1b` filed this unit as a pure SPEC beside `haipipe-board-page`, which stopped being true here; and `### What every verb must hold` restates the addressing law that `QC4a` owns, which is a second copy of a rule rather than a citation of it.
260802 · `0.2.0`
      **Two surfaces, two anchors.** The spec knew about lanes under the line and about markers, but not that a card can be attached to a few WORDS by a record that quotes them. An agent loading this to write one line could not have produced `> Card the words: what to show`, and would not have known that a card and a lane anchor differently.
      - `## 💬 The lanes` — `> Card the words: what to show` joins the lane figure, marked as the one lane that renders INSIDE the sentence rather than under it.
      - `## 🃏 The evidence card` — opens with the two-anchor table, then the card's two sources: a record that quotes its span, and a paper marker that names itself. Adds the rule that the words keep the prose's own font, colour and weight.
      Engine and board-page work shipped in `haipipe-board` 0.108.0-0.110.0; this is the loadable contract catching up.
260802 · `0.1.2`
      - Repointed the door test from `QC6 §7` to `QC1b §1` after that page's 260802 Content rebuild,
        and corrected the named next step: the drawer's lane instructions live in `live/chat.py`, not
        in `cli/serve.py`, since the `QC2c` live-layer split.
260802 · `0.1.1`
      - The lane figure taught `> JL: the human's lane`, which QB4 §3.3.3 retired on
        260802: a person's remark is `> Comment WHO …`, the older form still renders,
        and `check.py` warns on it inside Content. The figure now shows the three
        kinds that hang under a sentence (comment, `✎` change record, typed lane).
      - The never-delete rule said `> WHO:`; it names the comment form instead.
      - `## Discussion` is called out as NOT affected: it keeps `> JL:` with nested
        `>>` replies, which is a thread and a different grammar in a different
        section.
260731 · `0.1.0`
      - First cut, created on JL's order alongside `haipipe-board-page` and
        `haipipe-board-routing`, from QC6 §8's settled shape: one door, two SPECS, two
        VERBS. This is the sentence SPEC, the one a routed write loads so its output
        reads like the board.
      - Contract-first: no code moved. It owns the atomic unit and its dotted address,
        the `>` lane grammar with its standing rules (append only, never delete a user's
        lane, signed and dated, one nesting level), the evidence card's show-the-thing
        contract, and the archive-never-delete record lifecycle.
      - The authority stays `haipipe-board/ref/board-form.md` §5; this contract cites it
        and must never fork it, which is the same no-second-copy rule that motivated the
        whole extraction (serve.py's prose copies rotted once already).

<!-- haipipe:skill:log:end -->

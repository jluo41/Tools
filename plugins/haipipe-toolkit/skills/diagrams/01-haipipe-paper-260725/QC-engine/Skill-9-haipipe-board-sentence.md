# haipipe-board-sentence · v0.1.0
state: 🔴 OPEN
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
`haipipe-board-sentence` defines the reusable sentence unit: one addressable source line, lanes, evidence-card surface, and an archive-never-delete record lifecycle. It is the mechanism that makes a Paper sentence inspectable without inventing a separate annotation file.

It does not decide whether a sentence makes a valid scientific claim, how a paragraph advances an argument, or what counts as adequate evidence. Those are Paper requirements on `QC5`. This card is therefore the substrate half of the seam, and `QC5` is the Paper dialect half.

## Diagram
<!-- haipipe:skill:tree:start f5e312722743a0b5 board/haipipe-board-sentence -->

```
haipipe-board-sentence/
  CHANGELOG.md          22 ln  haipipe-board-sentence · Changelog
  SKILL.md              89 ln  /haipipe-board-sentence · the sentence, as a contract you can load
```

<!-- haipipe:skill:tree:end -->

```
WORKFLOW  (authored: a folder can be read off disk, an intent cannot)
Draw how this skill is actually used: the entry point, what it reads,
what it writes, and where it hands off. Delete this fence if the tree
above is the whole story.
```

## Content
<!-- haipipe:skill:body:start f5e312722743a0b5 board/haipipe-board-sentence -->

**haipipe-board-sentence** · `0.1.0` · last shipped 2026-07-31

- folder   `board/haipipe-board-sentence/`
- tools    not declared
- summary  First cut, contract-first (QC6 §8: the second SPEC the routing and digest verbs LOAD): the atomic unit, the lanes, the card, and the record lifecycle. No code moved.

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
      QB5.C1.P1.S1        Content division 1 · paragraph 1 · sentence 1
                          UPPERCASE+digit tokens, so a section slug can
                          never collide with a coordinate
      ```
      The address is how chat focuses one location, how a comment pins, and how an edit names what it replaces.

- 2 · 💬 The lanes
      A `>` line under a sentence is a LANE: a signed, dated remark that belongs to the sentence above it.
      ```
      > JL: the human's lane · decisions and corrections live here
      >> CC{MMDD}: the worker's dated reply lane, nested under what it answers
      ```
      Lane rules a machine must hold:
      ```
      · a lane is APPENDED, never edited in place; the record is the point
      · never delete a signed `> WHO:` or `> ✎` line (ref/writing-rules.md: they are the durable review trail)
      · a reply nests one level under what it answers, dated
      · a lane without a signature is not a lane, it is unclaimed prose
      ```

- 3 · 🃏 The evidence card
      A marker in a sentence (a citation, a value, a display unit) renders as a chip whose card shows the THING, not a description of it: the reference as the paper's own .bst prints it, the figure itself, the rows themselves.
      The card is a strict superset of a bare link, which is why a display unit's name in prose ALWAYS renders as the card (JL 260727).
      This contract owns what a card must show; the paper dialect that resolves markers stays deletable (`haipipe-board/src/dialect_paper.py`).

- 4 · ♻️ The record lifecycle
      The canonical sentence normally REMAINS; what ages is what attaches to it.
      ```
      comment lanes · evidence · edit records     archive on resolution, restorable
      the sentence itself                         edited through the page, logged
      nothing                                     is ever silently deleted
      ```
      Resolved threads leave the stage for the archive the same way a retired page leaves for `_archive/`: recoverable, out of the read.

- 5 · 📂 Files
      ```
      haipipe-board-sentence/
      ├── SKILL.md            this contract
      └── CHANGELOG.md        version history
      ```
      Reads `haipipe-board/ref/board-form.md` §5 as the authority; owns no scripts at 0.1.0.
      The named next step (QC6 §7): the drawer's lane instructions in `serve.py` become this contract's consumer instead of a second prose copy.
<!-- haipipe:skill:body:end -->

## Aims
- [ ] 🧠 Rule this skill's health
      `state:` is a judgment, not a version number: stable, in flux, needs work, or parked.

## States
Mirrored into the Engine roster to make the generic sentence contract discoverable from the Paper Board. The Paper-specific section, paragraph, sentence, and evidence requirements remain exclusively on `QC5`.

## Log
260801 0000 · page generated from `board/haipipe-board-sentence/` by `skillpage.py new`

<!-- haipipe:skill:log:start f5e312722743a0b5 board/haipipe-board-sentence -->

Converted from the skill's own `CHANGELOG.md`: 1 releases.

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

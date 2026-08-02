haipipe-board-sentence · Changelog
==================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.3.0 - 2026-08-02

**🚪 Became the DOOR for one sentence, not only its spec** (JL 260802: "if we want to put sentence things, we migrate that part from haipipe-board to haipipe-board-sentence, just like haipipe-board-page, right?").

The `haipipe-board-page` precedent is precise about what migrates: that skill owns the page contract and its two verbs, owns no scripts, and CALLS the engine. This unit had it the other way round, with the operating detail living in `haipipe-board`'s SKILL.md while this file was 94 lines of spec carrying no verbs at all.

- **Three verbs**, migrated out of `haipipe-board` 0.111.0: `comment` (a person's remark under one line), `edit` (one line replaced, one word-level record), `card` (a panel on a few words inside the line).
- **The boundary block**, mirroring the page skill's: this holds what a sentence IS, what may attach, which gesture reaches which, and the two anchors. `haipipe-board` keeps the renderer, the write routes, the controls, the checker and the recorded drive.
- **The reader's controls**: hover rail, double-click to edit, one `⋯` on touch, every record shut by default.
- **What every verb must hold**: the anchor is an exact match and a miss fails visibly; a form CLOSES before it asks for the repaint, because the live swap will not run while a textarea inside `div.wrap` holds text.

192 lines, against the page skill's 299.

## 0.2.0 - 2026-08-02

**Two surfaces, two anchors.** The spec knew about lanes under the line and about markers, but not that a card can be attached to a few WORDS by a record that quotes them. An agent loading this to write one line could not have produced `> Card the words: what to show`, and would not have known that a card and a lane anchor differently.

- `## 💬 The lanes` — `> Card the words: what to show` joins the lane figure, marked as the one lane that renders INSIDE the sentence rather than under it.
- `## 🃏 The evidence card` — opens with the two-anchor table, then the card's two sources: a record that quotes its span, and a paper marker that names itself. Adds the rule that the words keep the prose's own font, colour and weight.

Engine and board-page work shipped in `haipipe-board` 0.108.0-0.110.0; this is the loadable contract catching up.

## 0.1.2 - 2026-08-02

- Repointed the door test from `QC6 §7` to `QC1b §1` after that page's 260802 Content rebuild,
  and corrected the named next step: the drawer's lane instructions live in `live/chat.py`, not
  in `cli/serve.py`, since the `QC2c` live-layer split.

## 0.1.1 - 2026-08-02

- The lane figure taught `> JL: the human's lane`, which QB4 §3.3.3 retired on
  260802: a person's remark is `> Comment WHO …`, the older form still renders,
  and `check.py` warns on it inside Content. The figure now shows the three
  kinds that hang under a sentence (comment, `✎` change record, typed lane).
- The never-delete rule said `> WHO:`; it names the comment form instead.
- `## Discussion` is called out as NOT affected: it keeps `> JL:` with nested
  `>>` replies, which is a thread and a different grammar in a different
  section.

## 0.1.0 - 2026-07-31

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

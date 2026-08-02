haipipe-board-sentence · Changelog
==================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

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

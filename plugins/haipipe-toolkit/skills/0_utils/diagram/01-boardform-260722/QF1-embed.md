# Embeds: a Q shows another file's content
state: ✅ SETTLED
owner: JL
method: embed remains available; lifecycle stages now use canonical S faces, so no paper-side anchors handshake is needed

## Question
How does a Q file show content that lives in another file, without copying it and without the
board learning that file's format?

The first board laid directly over a paper's lifecycle tree (the MISQ paper's `0-lifecycle/`,
260724) exposed the gap: the stage docs there carry their own formats (setext headings, a
`Status:` line, five different question-ID families), and a Q face can relate to them in only
three ways today. Copying their open items into the face drifts the moment the source moves,
which is JL's core objection. Teaching build.py to parse each dialect couples this skill to
haipipe-paper's still-evolving contracts, and a parser that misses a new marker silently drops
a question from the deck, which is worse than visible staleness. Doing neither leaves faces as
bare pointers, and the deck loses Items to Finish counting, one of the two founding rules.
JL also asked the companion question: what should change in haipipe-paper-stage so the two
sides align instead of colliding.

## Boundary
- ✅ Covered here
  The embed mechanism (syntax, resolution scope, rendering, comments pinned on embedded text)
  and the minimal anchors the paper side would guarantee in its stage contracts.
- ↪ Covered elsewhere
  Discovering Q files inside subfolders (folder-as-Q) is recorded in the QC group; the comment
  write-back protocol itself is QA6.

## Diagram
```
route 1 · copy into the face      route 2 · parse the source        route 3 · embed by reference
┌───────────────────┐             ┌───────────────────┐             ┌────────────────────────┐
│ face restates the │             │ build.py learns   │             │ face = Q shell         │
│ source's items    │             │ every doc dialect │             │ + ![[path#Section]]    │
└───────────────────┘             └───────────────────┘             │   read fresh at build  │
  ▼ drifts as the source moves      ▼ couples to evolving formats   └────────────────────────┘
  🟡 but a human SEES stale text    🔴 a missed marker silently        ✅ zero drift, zero dialect
     and fixes it                      DROPS a question                 ❓ open: comment anchors
```

## Items to Finish
- [x] 🧭 Route ruled
      JL ruled 260724: the embed route plus the generic renderer; the deck stays Q-only (a
      stage doc renders INSIDE a face, it does not become a stateless slide of its own).
- [x] ✍️ Syntax pinned
      `![[path]]` and `![[path#Section]]` on its own line; path board-relative with an upward
      ladder (≤8 levels); `.md`/`.txt` only; rendered as a "live from source" block; every
      failure mode is a visible red box; no recursive expansion.
- [x] 💬 Comment-anchor rule for embedded text
      Resolved by design, no new protocol: the comment lives in the FACE's `## Comments`
      (serve.py target is the face), and at rebuild the anchor is re-found inside the
      re-rendered embed because mark_span scans the card html, which includes embeds. It shows
      unanchored only when the SOURCE actually drops the sentence, which is the honest signal.
- [x] 📐 Setext extraction rule
      `#Section` matches atx `##` headings AND setext underlined titles; verified against a
      stage-doc-shaped fixture and the live paper board.
- [x] 🧷 Paper-side handshake resolved
      The shared S-face contract removed the handshake rather than adding another adapter:
      stage state, Content, finish items, and status now live in the same canonical S file
      the board renders. Embeds remain available for genuinely external supporting material.
- [x] 🧪 First consumer proves the transition
      The MISQ paper first proved live embeds, then exposed their unnecessary indirection for
      lifecycle stages. Its current board runs 14 Q faces plus 8 canonical S faces; no stage
      depends on an embed or a separate lifecycle log.
- [x] 📖 Graduation
      Shipped 260724: the embed row in `ref/board-form.md` §5, the folder-tree + embed lines
      in `SKILL.md`'s 🗂 section, CHANGELOG 0.11.0.

## Where we are
Settled. Generic embeds still render through `src/page_stage.py`, but the lifecycle use case
no longer needs them: Q and S share one face grammar, and the MISQ paper board runs 14 Q faces
plus 8 S faces. That keeps supporting-file transclusion available without making stage state
depend on a cross-file anchors contract.

- 260725 JL · 🧩 Lifecycle route simplified
      JL chose one Q/S template with Question above Content and Q-consumers under Items to
      Finish. The paper-side anchors handshake was therefore closed by removal: S is the
      canonical stage file, not a face around another stage document.

- 260724 JL · 💡 Problem named
      The stage formats and the Q format must work together; asked whether a markdown file can
      incorporate another file, and how haipipe-paper-stage should be updated so the sides align.
- 260724 CC · 🔍 Design space mapped
      The three routes above, with the embed route's two open risks: comment anchors on
      embedded text, and setext section extraction.
- 260724 JL · 🧭 Route ruled: go
      Embed route plus the generic renderer, with the src/ split (QB5) landing first so the
      feature had a clean seat in `src/page_stage.py`.
- 260724 CC · 🚢 Shipped and proven on the first consumer
      Byte-identical split gate first, then the embed feature, then 22 faces; both risks closed
      (comment anchors by design, setext by the extraction rule).

## Files
- `build.py`
  Where an embed directive would resolve and inline; `split_sections` already exists for
  heading-scoped extraction.
- `ref/board-form.md`
  §5 syntax table gains the embed row at graduation.
- `haipipe-paper-stage/`
  The lifecycle owner whose stages now map directly to canonical S faces.
- `0-lifecycle/`
  First consumer: the board laid directly over a paper's lifecycle tree.

## Law
- One embed per line, on its own line: `![[path]]` or `![[path#Section]]`; path board-relative, then an upward ladder of at most 8 levels; `.md` and `.txt` only.
- The board never parses a source's dialect: embedded content is rendered generically (atx AND setext headings, fences, lists, quotes, record lines), unfolded, under a "live from source" header.
- Every embed failure is visible on the page (missing file, wrong extension, heading not found); an embed never silently renders empty.
- `![[…]]` inside embedded content is NOT expanded; no recursion, no cycles.
- Comments pinned on embedded text are written to the FACE's `## Comments` and re-anchor against the re-rendered embed; unanchored appears only when the source drops the sentence.

## Glossary
- transclusion: showing another file's content in place, by reference, without copying it.
- face: the thin Q file that fronts a folder question; the detail stays in the folder's own docs.

## Discussion
> JL 260724: the problem is how the different stage formats and the Q format work together. Can a markdown file incorporate another file? And haipipe-paper-stage should be updated so things align.
>> CC0724: embed-by-reference keeps both pens where they are: the board never parses stage dialects, and the paper side only promises a `Status:` line and one stable section name.
> JL 260725: maybe we can combine Q and S as one template.
>> CC0725: resolved by making S the canonical stage face; embeds stay generic but are no longer the lifecycle adapter.

## Log
260725 · settled: the shared S-face contract superseded the paper-side anchors handshake; embeds remain available for external supporting content
260724 · shipped: route ruled, syntax + renderer landed in src/page_stage.py, graduated to ref/board-form.md §5 + SKILL.md; paper-side handshake stays open
260724 · question opened (new QF group) while laying the first board over a paper's 0-lifecycle

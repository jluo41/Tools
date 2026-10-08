haipipe-studio · Changelog
==========================

## [0.4.1] · 2026-10-08 · Change notes on a slide draft

- A slide draft's change note about one slide sits only under that slide, not repeated in the title
  frame (JL 261008: "why this is not under each slide?"); the rule is excalidraw-slide's.

## [0.4.0] · 2026-10-07 · Slide drafts drawn by excalidraw-slide

- How a slide draft is drawn moved to the new `excalidraw-slide` skill (JL 261007: "go"), words kept:
  SKILL.md § Slide drafts and `ref/topic-contract.md` § A slide draft are now pointers. This skill keeps
  the s61-s69 band, the folder, the face, the sessions and the palette exemption. `canvas.ACCENT ·
  ACCENT_FILL · MUTED` stay, the same values as `slide_kit`'s, for the builders that read them here.
- `canvas.assign_ids` gives ids by position: two elements a builder gave one id stay two (b11). `write`
  warns when a canvas has no snapshot and no seed ids, so another writer's drawing is not doubled.

## [0.3.1] · 2026-10-07 · A slide draft keeps its deck

- The deck lives with its draft (JL 261007: "we can have the delivery in the s61 as well"):
  `studio/s6N-<deck>/build_deck.py` writes `studio/s6N-<deck>/delivery/<deck>.pptx · .pdf`; the
  level's `delivery/` holds a pointer, never a copy.

## [0.3.0] · 2026-10-07 · Slide drafts

- New kind of topic, s61-s69 (JL 261007: "one type is about propose the slide draft"): a proposed
  deck drawn before it is built, from one `slides.py` the deck writer also reads. Frames left to
  right: logic flow · the slides (half size, one skeleton) · on disk and open. `new_topic.py --band
  slides`; SKILL.md § Slide drafts; `ref/topic-contract.md` § A slide draft.
- The one colour exception (JL 261007: "make the slide to be a bit colorful by highlight the
  important things"): inside a slide, one accent marks its key thing. `canvas.ACCENT · ACCENT_FILL ·
  MUTED`, and `canvas.off_palette(els, slides=True)` allows them.

## [0.2.0] · 2026-10-07 · Change notes; the old copies retired

- `canvas.write` enforces the look (JL 261007, "Recolour all"): `apply_palette` maps any other stroke
  to black and drops fills in the builder's elements; images, transparent strokes and the person's
  marks untouched; slide drafts (s61-s69) exempt (JL: "but for the slide draft, maybe not").
- The look (JL 261007: "just the color of black, with red for uncertainty questions, and green for
  our previous changes"): trees, lines and boxes in black; red for an uncertain question; green for
  a change. `canvas.INK · RED · GREEN` and `canvas.off_palette(els)`.
- Every change to a drawing gets a short green note where it changed, `✎ <YYMMDD> <what changed>`,
  and the same line in the title frame (JL 261007: "when I change the draw, you can leave the short
  green comments to where we changed"). `canvas.change_note(x, y, what, date, frame)` makes the
  note; the builder skeleton keeps a `CHANGES` list and draws it in the title frame.
- b03 s21 phase 5: every builder imports `canvas` from `scripts/` here; the copies in b03's
  `studio/_build/` are retired. `canvas.LEGACY_DIRS` stays for a Block that still keeps older
  snapshots in a folder of its own.

## [0.1.0] · 2026-10-07 · New: the Idea Studio at any level (b03 s21)

- New skill (JL 261007: "what skill we should have for the studio and for the report").
- `ref/topic-contract.md`: `studio/sNN-<topic>/` at any level, its face (Topic · Feeds · Files ·
  Decided · Open, the marks the Idea Studio reads), the numbering (s0x concepts · s1x levels ·
  s2x runs and skills · s3x Guide · s5x server), builders that keep a person's marks, previews,
  sessions as passes of `run-draw-<sNN>`, the buttons.
- `scripts/canvas.py` and `scripts/render_png.py` moved in from b03's design `studio/_build/`,
  which keeps shims so every Block's builders still import them. `canvas.legacy_seed` now looks
  only in `canvas.LEGACY_DIRS`, which a shim fills with its own folder.
- `scripts/new_topic.py`: new, `topic` (the scaffold, `--builder` writes and runs a builder) and
  `session` (a pass of `run-draw-<sNN>`, through haipipe-run's `soft_run.py`).

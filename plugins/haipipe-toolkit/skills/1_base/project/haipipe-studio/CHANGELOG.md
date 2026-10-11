haipipe-studio · Changelog
==========================

## [0.8.0] · 2026-10-10 · A proposal topic

- b03_event_cgm's s03 (SHIFT Task 2.1) is the worked example of a topic that works on one section of a
  proposal or a paper (JL 261010, on its drawing: "I think this one is very very great!"). Five frames in
  two rows: ① the idea workflow, ② why and the plan, ③ the proposal figure, each one screen; ④ the draft
  today marked up and ⑤ the section written out, each one frame read down. The rules of each frame, the
  section-written-out layout (tight text rows, evidence cards free in two columns joined by lines that go
  around cards, a one-line card instead of a line longer than a screen, the figure as a DISPLAY item), where
  the words live (the face's yaml; a draft passage found by its anchors), what went wrong on the way, and
  the builders to copy from: `ref/topic-contract.md` § A proposal topic; a short section in SKILL.md.
- `canvas.numbered_frames(els)` finds one piece cut into numbered frames ("X · 1", "X · 2"), and
  `canvas.write` warns about it (JL asked twice on 261010 for one frame instead of many: b02_aid_ai's s03 and b03_event_cgm's s03). Tested.

## [0.7.1] · 2026-10-10 · One long piece, one frame

- A piece read top to bottom (a section written out, a draft's pages marked up) stays ONE frame that grows
  down; only its width must fit the screen (JL 261010, after b03_event_cgm's s03 had cut Task 2.1 written out
  into 9 frames and the marked-up draft into 4: "the draft take should be one single frame, and the Written
  out should be one large frame"). `canvas.reads_down(frame)` marks such a frame (`customData.reads`), and
  `canvas.oversized` then checks its width only. 0.7.0's "longer material takes more frames in rows" is
  withdrawn. SKILL.md (The look), `ref/topic-contract.md`, tested in `tests/test_haipipe_studio.py`.

## [0.7.0] · 2026-10-10 · Each frame fits the screen

- A frame is sized to read on one screen: the whole frame at 50% zoom, most of it at 100% (JL 261010, on
  the 9,200 x 5,650 px idea frame of b03_event_cgm's s03: "This is too huge, what I want is: when I zoom in
  50% I can read the whole workflow, when I read 100%, I can see most part of the frame"). About
  2560 x 1440 px, the workbench's 1280 x 720 pane at 50% zoom, at most 2800 x 1600 (`canvas.FRAME_MAX`);
  body words 20 px or more (`canvas.TEXT_MIN`); room comes from fewer words and boxes sized to them, never
  from scaling the drawing down (that shrinks the words), and longer material takes more frames in rows.
  `canvas.oversized(els)` lists the frames over the size, `canvas.small_text(els)` the frames whose words
  are mostly under 20 px (green notes not counted), and `canvas.write` warns about each. "One idea, one large frame" now reads "one
  dense frame": large means much information, not a large canvas. SKILL.md (The look),
  `ref/topic-contract.md`, tested in `tests/test_haipipe_studio.py`.
- `render_png.py` stacks a text's lines at the canvas's own line height (1.25 x the font size), so a
  preview no longer draws lines over the next box's words.

## [0.6.1] · 2026-10-10 · One idea, one large frame

- A topic's idea is one big connected frame, dense with facts, its key part largest; extra frames only for
  separate material such as a marked-up source (JL 261010 to a Codex session that split s03 of
  b02_aid_ai into 12 frames: "你这么多 frame，其实只相当于我的一个 frame"). In SKILL.md (The look) and
  `ref/topic-contract.md`.

## [0.6.0] · 2026-10-09 · Frames in rows

- `canvas.grid(els, rows, gap)` places a drawing's frames in rows, read left to right and then down;
  each frame moves with what is drawn in it (JL 261009, on a studio topic of 8 frames stacked 11,600 px
  tall: "don't put all the things in one column, I told you"). `canvas.one_column(els)` finds the old
  layout and `canvas.write` warns about it. The rule is in SKILL.md (The look) and
  `ref/topic-contract.md`; tested in `tests/test_haipipe_studio.py`.

## [0.5.0] · 2026-10-09 · One readable font

- Every word a builder writes is Nunito, Excalidraw's "Normal" font (`canvas.FONT` = 6), and code
  stays Cascadia (`canvas.CODE_FONT` = 3) (JL 261009, on a drawing in Comic Shanns with notes in
  Virgil: "I think the font should be more readable, change it"). `canvas.write` applies it with
  the palette (`apply_font`); `change_note` and the `new_topic.py` builder template write it. A
  person's own marks and a slide draft keep their fonts. Every studio drawing takes the font on its
  next rebuild.

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

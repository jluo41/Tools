excalidraw-slide · Changelog
============================

## [0.2.0] · 2026-10-12 · The ask first, and j51 the job to copy

- Asked 261012: "could you update the skills of the excalidraw-slide?", after b31 s03 was redrawn on j51
  ("I think you should use the examples from .../Paper-TestToLearn-MS2026, there is a slide job").
- The ask comes first (b31 s03 Open 1): a topic before the draft (j51's `s01-what-they-want`) holds who,
  how long, when it is shown, what is due when, and each pain with the slide that answers it, every line
  with where it was said. SKILL.md step 0; `ref/slide-draft.md` § The ask, before the draft; the folder now
  shows the Job's studio/.
- j51 is the slide job to copy (b31 s03 Open 2): SKILL.md § The slide job to copy, its folder and what each
  file shows; the deck writer starts from j51's `build_deck.py`.
- Screens and figures: a `screen` or `figure` visual names its `file`; a screen is retaken by a script,
  never pasted (step 7, ref § Screens and figures). `slide_kit.check` fails a visual whose `file` is not on
  disk and warns on a screen or figure that names none (a new test; 10 pass). the eleven visual kinds
  j51's builders render are listed.
- Sizes and words (b31 s03 Open 5): a slide draft keeps its own; `canvas.is_slide_draft` skips those
  checks and excalidraw-studio's `check.py` names a slide draft without judging them.
- Still open: one deck writer in the skill (b31 s03 Open 3), one drawing kit (Open 4).

## [0.1.3] · 2026-10-08 · Exporting a deck's PDF

- The deck writer exports the PDF from a temporary copy of the .pptx, never the file itself: PowerPoint
  hands back the person's open window (possibly an older version), and closing it closes theirs.
- A slide's `ask` shown in a corner box of the deck is one deck's choice (j51), not the contract (JL
  261008: "this is special case, the in the current version is good enough").

## [0.1.2] · 2026-10-08 · Change notes under their slide

- A change note sits under the slide it changed, after that slide's red `ask` lines (JL 261008: "why
  this is not under each slide?"). `CHANGES` is `(where, date, what)`, `where` = a slide's n · "disk"
  (frame 3) · "all" (the title). Not repeated in the title: haipipe-studio 0.4.1 names the exception.

## [0.1.1] · 2026-10-08 · A slide's own questions

- Optional per-slide `ask`: our open questions about one slide, drawn in red right under it on the
  canvas, never written into the deck (JL 261008: "you can use the red color to ask question"). The
  top-level `OPEN` keeps the deck-wide ones. `slide_kit.check` accepts it as a list of strings.

## [0.1.0] · 2026-10-07 · New: slide drafts, moved out of haipipe-studio

- New skill (JL 261007: "should we have the new skill of excalidraw-slide" · "go"). How a slide draft
  is drawn moved here from haipipe-studio 0.3.1 (SKILL.md § Slide drafts, `ref/topic-contract.md`
  § A slide draft), words kept; haipipe-studio keeps the s61-s69 band, the folder, the face, the
  sessions and the palette exemption.
- `ref/slide-draft.md`: the folder, the three frames left to right, the half-size slide skeleton, the
  colour exception, the deck in the topic's own delivery/, and the field contract of `slides.py`
  (AUDIENCE · LENGTH · SHOWN · GROUPS · SLIDES · OPEN; per slide n · slug · group · title · headline ·
  visual{kind, …, hl} · caption · source · next · notes), taken from the first slide draft.
- `scripts/slide_kit.py`: the colours, `off_palette`, `load` and `check` of a `slides.py`.
- No deck writer yet: `build_deck.py` lives in its topic until its generic part is separable.

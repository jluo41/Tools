# Changelog

## 2.2.0 · 2026-10-19 · Section canvas sync: the canvas back into the files (b32 s41-D28)

- `section_canvas.py sync <face>`: a sentence typed over goes into §3 by its address (logged before → after), a
  person's note, box, arrow or line into `draft/records/<stem>-feedback.md` at the sentence it sits beside; then the
  canvas is rebuilt, so the step tabs and the canvas show the same files (JL 2026-10-19: "去做 sync 吧").

## 2.1.0 · 2026-10-19 · Section mode: one Section on one canvas (b32 s41)

- `ref/section_canvas.py` and `ref/section.md`: b21 s06's builder made shared. A face's `canvas:` yaml names the
  draft folder and, as they exist, the Section, the rendered pages (newest `-v<N>`, haipipe-delivery `word_round.py`),
  evidence/cards.yaml (haipipe-evidence) and a revise plan; s06 now calls it and draws the same 187 elements (JL
  2026-10-19: "I want to make it ready to use").

## 2.0.0 · 2026-10-16 · excalidraw-section and excalidraw-revise merged (JL 261016, b32 s41-D16)

- One skill, `excalidraw-draft`, two modes: Map (`ref/map.md`, was excalidraw-section) and Revise (`ref/revise.md`,
  was excalidraw-revise). Scripts moved into `ref/`: `excalidraw_section.py`, `read_revise.py`, `track_changes.py`,
  `revise-spec.md`. The old names stay as triggers. Every live mention in the SPACEs follows.

# Before the merge: excalidraw-revise
## 1.2.0 · 2026-10-14 · A writing review's proposals as notes (b21 s04)

- The plan's `review` key, off unless named (`ref/revise-spec.md`): a haipipe-writing review's proposals, each a red
  note at the sentence it names (`at: C<k>.P<m>.S<n>`), with a red L from the sentence, drawn after the changes'
  notes under one red label; open until a person picks (JL 261014: "could you add these comments to that frame?").
  Sentence mode only; the build stops when an `at` names no sentence of the draft.

## 1.1.0 · 2026-10-14 · Layout options for a long file (b21 s04)

- The plan's `notes`, `content`, `section_stairs` and `replies` keys, each off unless named, so b31 and b32 draw as
  before (`ref/revise-spec.md`): fewer, wider notes as stairs, each joined to its sentence by an L; a wider, larger
  draft column; each section a step right of the one before; a co-author's comment as a blue note.
- `section_stairs.frames`: each section its own frame, named for it with a 44 px title, the key in a small frame
  above, the frames as stairs (JL 261014: "I would like to have each subsection to be a single frame"); then, from
  JL's sketch ("I want things like this"), the plan and the key in one row, the frames `step` right and `gap` below
  each other, and an L arrow from each frame's foot into the next one's title.

## 1.0.0 · 2026-10-13 · Its own skill, out of excalidraw-read

- JL 261013, on b01_irb's CIR 2 topic: "I think we want to have the /excalidraw-revise, a new skill for this type
  of tasks"; then "please go ahead and continue and do it". excalidraw-read's revise mode (its 0.3.0 to
  0.4.0; that CHANGELOG keeps the history) moves here: `ref/read_revise.py`, `ref/track_changes.py`, `ref/revise-spec.md`.
  `read_revise.py` still draws with excalidraw-read's `ref/read_paper.py`, found through the sibling folder.
- A file without Heading 1: the plan's `sections` lists its headings in order (`head`, `name`, `find`), for the
  page cuts, the draft's divisions and the delivery (b01_irb s03, JHM IRB eForm A, 261012).
- `seed` writes the tracked Word file from the plan's changes when it does not exist yet, so a file of our own
  needs no hand-made tracked copy first (b01_irb s03).
- `deliver` asks for no paragraph break where a draft paragraph already starts a file paragraph: a form's
  one-word paragraph ("recommendations.") repeats and cannot be found once (b01_irb s03).
- The copy is read from `related/files/` (haipipe-related's name) as well as `related/materials/`.
- The drawing's writer source is `excalidraw-revise/ref/read_revise.py`; every builder and delivery script that
  called the old path was moved to the new one (SHIFT b02, b03, b04; Samsung b01_irb; b31 s04 and s21).

# Before the merge: excalidraw-section
## 0.1.0 · 2026-10-03 · Paper and Section maps (JL 261003)

- New skill (JL 261003: "for drawing the sections only, I mean the paper and paragraph",
  "in the right part add the evidence card as well", "Maybe call it as this": excalidraw-section).
- `ref/excalidraw_section.py`: a Section map (Section → paragraphs → Bullets, each a row,
  then a Text column and an Evidence column of cards) and a paper map (paper → Main ·
  Appendix · Round → Sections in board order → paragraphs, deeper with `--depth`). Left to
  right, labels wrapped to their box; generated (`source` names the script), never replaced
  after a canvas edit without `--force`. Cards come from `draw-logic-tree`.
- First maps: S-ManSci-Main-Abstract (12 boxes, 9 cards) and Paper-MessageTradeOffEgm (19
  Sections in three groups; only the Abstract has a plan yet).

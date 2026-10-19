# Section mode · one Section on one canvas, for editing it

**LOAD `../SKILL.md` (`excalidraw-draft`) FIRST.** The canvas a draft Task's Studio opens on (b32 s41): one Section
in one frame, read down. Left, the file today (its page pictures) and how the paragraphs read; middle, the text, one
sentence a row, words black, a pale box under the words a card is about; right, the evidence cards, the comments
with our replies, and the change cards, each joined to its sentence. First built as b21 s06 (C5) on 2026-10-15,
shared here on 2026-10-19 (JL: "I want to make it ready to use").

```text
draft/*-draft-v*.md ─┐
render/<file>-vN/    ├─▶ section_canvas.py <face.md> ─▶ <topic>.excalidraw · .png
evidence/cards.yaml  ┤        (a rebuild keeps a person's marks)
a revise plan        ┘
```

## Start one

1. **A topic**: one Studio topic per Section, `studio/sNN-<what>/` (haipipe-studio `new_topic.py topic`). A new
   round stays in the same topic; the last round's drawing moves to `history/round-<n>-<yymmdd>/` (s41-D23).
2. **The face**: a `canvas:` yaml block; only `draft_folder` is needed, the rest is added as it exists:

```yaml
canvas:
  draft_folder: ../s04-task21-updated-draft/draft          # one current *-draft-v*.md
  section: C2                                              # or paragraphs: [C2.P3, C2.P4]
  pages: {render: ../../delivery/render, name: "Task 2.1 - Gordon Gao-draft-JL", pick: [2]}
  evidence: ../s04-task21-updated-draft/evidence/cards.yaml
  title: "Task 2.1 · Section C2 · Challenge and Significance"
```

3. **The builder**: a three-line `build_sNN_<what>.py` beside the face that imports `build` from
   `ref/section_canvas.py` (b21 s06's is the example), or run it straight:
   `.venv/bin/python <this skill>/ref/section_canvas.py <face.md>`.

## Where each part comes from

| On the canvas | Read from | Owner |
|---|---|---|
| sentences, paragraphs, their plan | `draft_folder`: `## 3 · Draft` and `## 1 · Structure` | haipipe-draft-writing, haipipe-draft-logic |
| the file today | `pages`: the newest `render/<name>-v<N>/p-<k>.png` | haipipe-delivery `word_round.py render` |
| evidence cards | `evidence`: cards.yaml; blue CITE, violet WORK, red needed | haipipe-evidence |
| comments and replies, change cards, asks | a revise plan: `plan_face`, `plan_key`, `part` | Revise mode (`ref/revise-spec.md`) |

A card is drawn only when it backs a sentence of this Section; a comment or ask whose words left the text is shown
in red, never dropped. Keys for the words on the canvas (`title`, `subtitle`, `key`, the column titles, `footer`) have
defaults in `section_canvas.py`.

## Work on the canvas, then sync

The canvas and the step tabs show the same files (s41-D28). What you do on the canvas goes back into them with one
command, which then rebuilds the canvas:

```text
.venv/bin/python <this skill>/ref/section_canvas.py sync <face.md> [--dry]
a sentence typed over          → §3 of the Draft, by its address; logged before → after
a note, box, arrow or line     → draft/records/<stem>-feedback.md as "- [ ] a red arrow from S7 (C2.P4.B1) to S11 …"
```

A mark is recorded once (it keeps `recorded:` on the canvas) and stays where you drew it. An edit whose sentence
changed in the Draft since the canvas was built stops the sync: rebuild, then type it again. The feedback lines are
for an agent: haipipe-draft-writing turns them into Revise cards, haipipe-draft-logic into a §1 change.

## After a round comes back

`word_round.py pull` saves the returned file as the next version and renders it; rebuild the canvas and its left side
shows that version (the newest `-v<N>` folder wins).

## Not yet

- Comments read from the returned Word file itself, with the words they are anchored to (today: a revise plan's
  `replies`).
- Revise cards from `draft/records/<stem>-revise.md` (s41 Open 1; today: a revise plan's `edits`), and a ✓ on a card
  that sync reads as accepted.
- Rebuilding a canvas on open when its files are newer (today: run the builder or sync).

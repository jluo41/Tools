# The topic contract · sNN-<topic>/ beside the Jobs or Tasks

Read before adding, redrawing or saving a Studio topic, or writing a builder.

There is no `studio/` folder for topics: each `sNN-<topic>/` sits beside the Jobs or Tasks of the level it serves,
one topic per folder, each a drawing to think on together and a short face that says what it settles. This contract
is the folder, its face, its builder and its rounds. How a topic's drawing should look is `hai-draw`'s (a
report picture or a scratch: `hai-draw report`'s). A Page's own `studio/` (its chat and draw lanes) is a different
folder and stays.

## Count and ownership

One sNN numbering per Block. A topic sits at the level that uses its delivery. A level holds at most 9 topics at a
Block, 5 at a Job and 3 at a Task, counting folders, not the highest number; `new_topic.py` refuses one past the
limit unless `--over-limit`. Before adding one past the limit, reuse a related topic, put it on the Job or Task that
uses its delivery, or split the level. The limit never deletes or renumbers an existing topic.

## The files

One file per part of the contract; read the one you need.

| Read | For |
|---|---|
| `ref/topic-folder.md` | what sits in `sNN-<topic>/` |
| `ref/topic-face.md` | the face: its lines, Decided, Open |
| `ref/topic-numbering.md` | sNN numbers and the Studio bands |
| `ref/topic-delivery.md` | one topic, one delivery; delivery types; the render out |
| `ref/topic-builder.md` | drawing with a builder; the reader review |
| `ref/topic-look.md` | what `canvas.py` enforces; change notes |
| `ref/topic-rounds.md` | a round: a session or a meeting |
| `ref/studio-section.md` | what the page's Studio section shows and reads |
| `ref/topic-transcripts.md` | transcript originals inside a Task topic |

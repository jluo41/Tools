Topic count and ownership
=========================

One sNN numbering per Block; a topic sits at the level that uses its delivery. A level holds at most 9 topics at a Block, 5 at a
Job and 3 at a Task, counting folders rather than the highest sNN number; `new_topic.py` refuses one past the
limit unless `--over-limit`. Reuse a related topic or split an independent area into a peer Block first. The
limit never deletes or renumbers existing topics. Older local topics and their sessions stay
readable until explicitly moved.

# The topic contract · sNN-<topic>/ beside the Jobs or Tasks

Read before adding, redrawing or saving a studio topic, or writing a builder. There is no
`studio/` folder for topics (JL 261031): each `sNN-<topic>/` sits beside the Jobs or Tasks of the
level it serves, one topic per folder,
each a drawing to think on together and a short face that says what it settles. How a
topic's drawing should look is `excalidraw-studio`'s (a report picture or a scratch:
`excalidraw-report`'s); this contract is the folder, its face, its builder and its sessions.
A Page's own `studio/` (its chat and draw lanes, workbench `ref/roster.md`) is a different folder and stays.

## The files

One file per topic of the contract; read the one you need.

- `ref/topic-folder.md`: the folder: what sits in sNN-<topic>/
- `ref/topic-transcripts.md`: transcript originals inside a Task Studio
- `ref/topic-numbering.md`: sNN numbers: the bands, s99, never reused
- `ref/topic-face.md`: the face: its marks, view:, Why, Decided, Open
- `ref/topic-look.md`: how a topic looks on the page
- `ref/proposal-topic.md`: a proposal topic: one section, drawn so it can be written
- `ref/slide-draft-topic.md`: a slide draft (s61-s69)
- `ref/ui-preview-topic.md`: a UI preview topic (`**Delivery type:** ui`): live views under Page, quick views under Effect, s99
- `ref/topic-builder.md`: drawing with a builder
- `ref/topic-rounds.md`: rounds
- `ref/topic-buttons.md`: the buttons
- `ref/topic-scripts.md`: the scripts

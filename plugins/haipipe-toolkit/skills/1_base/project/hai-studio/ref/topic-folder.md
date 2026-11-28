# The folder

Part of hai-studio's topic contract (`ref/topic-contract.md`).


```text
<Block, Job or Task>/               (an older Block: <block>/studio/, still read until studio_move.py moves it)
├── sNN-<topic>/
│   ├── sNN-<topic>.md              the face: Topic · Feeds · Files · Decided · Open
│   ├── sNN-<topic>.excalidraw      its drawing (the first one the Idea Studio shows)
│   ├── sNN-<topic>.png             its preview (render_png.py)
│   ├── .sNN-<topic>.seed.json      the builder's last drawing: what canvas.write compares with
│   ├── build_sNN_<topic>.py        the builder, when a script draws it
│   ├── sNN-<topic>.mindmap.md      its structured side, the mind map: the source (hai-mindmap)
│   ├── sNN-<topic>.mindmap.html    the mind map as a static page (git ignores it: rebuilt on every change)
│   ├── history/                    older builders or drawings kept on a redesign
│   ├── passes/pNN-<MMDD>/          one round each: a working session or a meeting
│   └── result/                     its own working output, messy is fine (b35 s01-D10); never a copy of a Run's
└── studio/_build/                  loose items only: the level's shared builder helpers and make.sh
```

1. **One topic, one folder**: a topic is a question being thought through, not a picture.
2. **Where it sits**: at the level that uses its delivery, a Block's beside its `jNN_` folders, a
   Job's beside its `tNN_` folders, a Task's beside `runs/`; a page shows its own topics and its
   children's. An older `studio/sNN-<topic>/` stays readable until moved.
3. **Its drawings**: the first `.excalidraw` is the one the Idea Studio opens across the row;
   more are links beside it. A topic with a builder opens view only; one drawn by hand edits
   in place.
4. **Its structured side, its mind map**: every topic has `sNN-<topic>.mindmap.md` with the topic's own name (s01-work-ladder → s01-work-ladder.mindmap.md), its mind map, written with the face by `new_topic.py` from the face's labelled lines and
   sections (hai-mindmap `from-topic`). It is not a canvas: the card's `Free | Structured` switch
   shows it as the draft's §1 Structure map, in HTML, edited in place (click and type, Enter for the
   next node, ＋ for a child, empty to take out, drag to move), each change written into the file. Edit
   (the free canvas) shows on Free only; the ↗ opens the side showing; the choice is remembered.

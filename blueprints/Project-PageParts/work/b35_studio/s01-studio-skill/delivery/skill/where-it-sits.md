There is no `studio/` folder: each topic is an `sNN-<topic>/` folder that sits directly beside the Jobs or Tasks of
the level it serves, a Block's beside its `jNN_` folders, a Job's beside its `tNN_` folders, a Task's beside `runs/`
(b35 s01-D12, JL 261030: "we just have sNN, along side with jNN, to make it visible directly"). Which level: the one
that uses its delivery. The count is capped per level (JL 261030: "we might have many sNN, but we need to control the
numbers"): at most **9 at a Block, 5 at a Job, 3 at a Task**; more means the level is really two. A page shows its own
topics and its children's. An older Block's `sNN-<topic>/` still reads, until it is moved. A topic's address is `bNN.jNN-sNN` (dots for the ladder, a hyphen before the topic:
`b17.j01-s07`, s01-D02), always followed by its names, `b17-s04:theme_work @ workbench_page_structure`,
`b17.j01.t03-s09:theme_work.tables.cut @ which_cut_first` (s01-D03, `frame.topic_label`): never an address alone. `new_topic.py topic <Block, Job or Task>` puts the topic in that folder and refuses one past its level's limit (`--over-limit` to add it anyway). Each topic has a drawing to think on
together and a short face that says what it settles and which Questions it feeds. This skill owns the folder, the face, the numbering, the builders that
keep a person's marks, and the sessions. How a topic's drawing looks and reads is `excalidraw-studio`'s: load
`/excalidraw studio` before drawing or redrawing a topic (its principles, `scripts/draw.py` to draw with,
`scripts/check.py` to check); a report's drawing is `excalidraw-report`'s.

```text
<Block, Job or Task>/sNN-<topic>/
├── sNN-<topic>.md            Topic · Feeds · Files · Decided · Open
├── sNN-<topic>.excalidraw    the drawing (a builder's, with the person's marks kept)
├── sNN-<topic>.png           its preview
├── build_sNN_<topic>.py      the builder, when a script draws it
├── sNN-<topic>.mindmap.md    its structured side, the mind map: Markdown, drawn as the §1 map (haipipe-mindmap)
├── sNN-<topic>.ideas.md      its open ideas: a question, its options, the leaning, what is unknown
├── slides/idea-NN-<slug>.png  one picture per idea (haipipe-display _parts/slide, its deck's style; source)
├── sNN-<topic>.slides.json   the record: "style" (default sketch-notes), then per idea: content, image, notes
├── sNN-<topic>.slides.html   the deck to look at, one picture a slide (generated, git-ignored)
├── sNN-<topic>.slides.pptx   the same as PowerPoint, notes as speaker notes (generated, git-ignored)
├── passes/pNN-<MMDD>/        one round each: a working session or a meeting (pass.md)
├── result/                   its own working output: mock pages, trial pictures, extra drawings and builders (b17
                              s01-D06); messy is fine. A Task Run's output stays in that Run's result/, shown here
└── delivery/                 the agreed version: deck/ (its slides, they stay here) and the thing it hands over;
                              render.yaml says where each piece goes, render_delivery.py writes it there
```

An sNN hands over through its own `delivery/` (JL 261030: "studio/sNN/delivery, this is the delivery, and then we do
the render, to render the delivery out, to that area, like the haipipe-studio"). Two steps: the agreed, clean version
goes into `delivery/` (never `result/`, which is messy by design), then a render writes it out to where it is used. A
text piece (a skill's section, a Section's draft) lands between `<!-- render <address> <block> -->` markers in its
target, a region nobody edits by hand; a code piece is built by the Task that `render.yaml` names; the deck stays in
`delivery/deck/`. `python $S/render_delivery.py <sNN>` checks every piece, `--apply` writes the ones that differ.

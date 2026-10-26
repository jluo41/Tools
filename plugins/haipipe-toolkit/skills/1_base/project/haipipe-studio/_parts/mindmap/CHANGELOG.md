mindmap (haipipe-studio part) · Changelog
=========================================

## [0.3.0] · 2026-10-26 · the mind map is the §1 map, not a canvas; a part of haipipe-studio

- JL 261026: "the mindmap is not the excalidraw … I want that type of the mindmap" (the draft's §1 Structure map),
  and "the mindmap will also be in the haipipe-studio, they are linked to each other". The skill haipipe-mindmap
  becomes haipipe-studio's part `_parts/mindmap/`; a topic's two sides, its drawing (sNN) and its mind map (mNN), are
  linked by number, and `new_topic.py topic` makes both.
- `scripts/mmmap.py`: the map drawn as `draft_steps.py` `_plan_map` draws §1 (the root left in the key colour, each
  node's children a column to its right, curved wires, a note on hover) and edited in place (type, Enter, ＋, empty,
  drag); `act` writes each change into the `.mindmap.md` (POST `/_board/mindmap`, servers/_host/serve.py), refusing
  words that changed on disk since the page showed them, and rebuilds the static page.
- Removed: the Excalidraw canvas and its preview (`mmcanvas.py`, `render` to `.excalidraw` and `.png`), `sync` and its
  conflicts (an edit now goes straight into the file), and the 200-word folding made for the canvas (every Run and
  leaf is shown; a leaf keeps up to fourteen words). `render` writes the static page; `check` reads grammar and ids.
- Tests: 21 (the map, read only and editable, each kind of edit, a stale edit refused, the builders, refresh).


## [0.2.0] · 2026-10-25 · editable both ways; built from disk

- `sync`: a canvas edit comes back into the file: changed words, added boxes joined by an arrow, rewiring (an arrow
  from another node, or a line's start dragged onto another box), reordering (boxes read top to bottom), deletions
  (children move up). Everything else drawn on the canvas is kept through every render; a box taken into the file
  is drawn again as the map's own. The frame `mm:frame` keeps the base, the tree as last drawn, so the canvas's
  edits and the file's are told apart.
- An edit made on both sides stops `sync` (exit 2, nothing written) until the person picks a side: `--take canvas`,
  `--take file`, or per node `--take <id>=canvas`. `render` refuses to draw over unsynced canvas edits (`--force`).
- Builders: `from-work` (a world, a Block or a Job: Block → Job → Task → Run, with run counts and each Run's state)
  and `from-topic` (a Studio topic's structured side, `mNN-<topic>.mindmap.md`, from its face's labelled lines and
  sections). `refresh` rebuilds from disk after a `sync`; a built node carries `#hash` of its builder's words, so a
  person's nodes and words are kept and only unchanged words update.
- Principle ⑦ and ①: a builder folds its longest lists into `+N more` until the map, its title included, holds at
  most 200 words and one screen of leaves (`--all` keeps everything); the layout narrows or widens its columns and
  closes its gaps to fit 2800 x 1600.
- `check`: the grammar, ids, the canvas and preview there, nothing unsynced either way.
- Docs: ref/grammar.md (the file, the canvas's ids, how sync reads, the conflict table, refresh), agents/openai.yaml.
- Tests: 22, from the grammar to a refresh that keeps a person's words.

## [0.1.0] · 2026-10-25 · one source, three views

- A `.mindmap.md` file (front matter, `# root`, a nested bullet list with `<!-- id -->` marks, free notes after) is
  the source; `render` draws it left to right on an Excalidraw canvas with excalidraw-studio's `draw.py` (the root in
  the key colour, a column per depth, the ⑥ ⑦ badge), previews it with haipipe-studio's `render_png.py`, and writes
  the web page `.mindmap.html` with its Markdown rendered and the tree folding. `new` and `html`.

haipipe-mindmap · Changelog
===========================

## [0.6.1] · 2026-10-26 · written maps: a kind per branch, a question between, a role per point

- The grey line over a branch's name is its kind (`[question] …`), or nothing; no bare number. b17's five maps are
  written as §1 is: each branch a step of the topic's argument, the question it hands to the next, short points with
  roles, the long text and the links (reports, faces, builders) in each detail.
- A map with `written:` in its header keeps its branches on refresh; only its Files branch follows the disk. A node
  with no builder hash (the root of a written map) is a person's, never rewritten. Renaming a branch keeps its kind.
- Tests: 27.

## [0.6.0] · 2026-10-26 · one structure map, shared with the draft's §1; a skill again

- JL 261026: "你把他们那个 map 也放到我们这个新的 skill 里面去 /haipipe-mindmap，这样的话他们就共享了，不用搞那么多代码了"
  and "就不能够做出来一模一样的东西吗". The §1 Structure map's markup, CSS and script move from
  `servers/workbench/workbench-task-draft/draft_steps.py` into `scripts/mapview.py`; `_plan_map` and the paper theme
  draw through it (three real JAMA drafts render byte for byte as before, but for the one line that posts to the
  map's endpoint), and so does every topic's mind map (`mmmap.draw`).
- A mind map now looks and edits as §1: root card with its note as the arc, a card per first-level node, the question
  between two (`→ <question>`), a plain line per point with its number and role pill, grey curves. `act` answers §1's
  payload (words, role, para, ask, arc, add, addpara, drop, move; and note). Removed: the card-per-node layout, the
  three styles and the branch colours.
- The part `haipipe-studio/_parts/mindmap/` is the skill `haipipe-mindmap` again, so `/haipipe-mindmap` opens it.
- Tests: 25 (the shared CSS and script, §1's markup, the question and role, five levels down, chips and pictures,
  read only, each edit of §1's payload).

## [0.5.2] · 2026-10-26 · no side bars

- JL 261026, of the thick coloured bar down a leaf's and a detail's left side: "我其实不是很想要左边这个东西，感觉它太 AI
  了". Leaves are edged in a thin line of their branch's colour; a detail is a soft rounded box washed in it.

## [0.5.1] · 2026-10-26 · curved wires again, met at the card's words

- JL 261026: "你这也太直了 … 做得跟那个 haipipe-draft paper 一样 … 还是那种曲线型的", and of the opened card's wire,
  "它那个比较奇怪". Wires are §1's curves again (draft_steps.py PLAN_JS), in the branch's colour; each end meets its card
  at the first line (at most 18 px down), so a card opened to its detail is joined at its words, not halfway down.

## [0.5.0] · 2026-10-26 · straight wires, a colour per branch, three styles

- JL 261026: "为什么这个不是笔直的呀" and "这个颜色它们是非常一样的 … 能不能做一下 visualization 之类的，做一下不同风格的变化".
  Wires are straight: a stub from the parent, one trunk halfway to its children, a straight run into each.
- Each first-level branch takes a hue of the dataviz reference categorical palette in its fixed order (run through its
  validator: light and dark pass; the light contrast warning is met by each branch's name on its card); a ninth
  branch on is grey. Wires, card edges and the detail panel follow the branch.
- A style switch above each map: Branches (default), Filled, Ink; remembered in the browser (applied to every map on
  the page, after each reload of a map). An opened detail is its own panel, washed in its branch's colour.
- Tests: 26 (the branch order, the three styles, no curved wire).

## [0.4.0] · 2026-10-26 · a short card, its detail behind ▸

- JL 261026: "把这个 leaf 写得比较 concise 一些，点开之后就可以把它展开，有详细的介绍" and "它既有可以点开的泡泡链接，点开之后也
  可以看到 detail information". A card keeps its bubble (🖼 or ↗, the file it names) and gains ▸, which opens its
  detail (the lines under its bullet) below its words, as Markdown: links open in the pop-out, a picture shows as
  itself. ✎ edits the detail (`act` what=note; a detail line never becomes a bullet); open details stay open when the
  map reloads after an edit; ▸ works on the static page too.
- from-topic: a leaf is at most seven words, its whole sentence the detail; a file is a link, a picture also shown in
  its detail. from-work: a Task's detail is its face's `goal:` and `close:`.
- A built node's hash covers its words and its detail. Fixed: a refresh that updated a node's words kept its old hash,
  so the next refresh took the node for a person's edit and froze it; the hash now follows the update. b17's maps were
  rebuilt clean.
- Tests: 26.

## [0.3.1] · 2026-10-26 · a card opens its file; any depth

- JL 261026: "点击这个卡的时候，我能不能点出来一些内容？比如能把图片点出来". A node whose words link a file shows a button
  beside them (🖼 a picture, ↗ else) that opens the file in the workbench's pop-out (`url_of`, passed by frame.py: a
  drawing in its editor, a page in its reader, else the file); a link to a file not on disk gets no button; the static
  page links the file beside it. `from-topic`'s Files branch writes each file as `[name](name)`.
- "这个它可以是几层的吗": any depth, already; a test now holds a node five levels below the root. Tests: 23.

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

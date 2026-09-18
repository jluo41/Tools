# CHANGELOG · haipipe-plugin-paper

## 0.2.1 · 2026-09-18

- Workflow map × Folder tree (JL): `ref/space-mapping.md` gains a second table,
  `Folder tree × Run-Type`, one row per folder slot of the paper (board ·
  story00 · story · main · appendix · round · delivery · tasks · discoveries)
  with what it holds and the Run-Types acting there. Run Space › Workflow map
  now adds a `folder on this board` column to the map and, under it, draws the
  REAL folder tree of the paper as a nested collapsible explorer in two boxes
  (the paper folder; the project homes: claimed Task-home blocks and Discovery
  inquiries), each box two aligned columns: the bare tree on the left, the
  works on the right as one edged cell per row (counts on every folder; each
  slot's Run-Type chips on its first folder) and nothing else. The tree is
  complete: every folder opens down to its files (three levels below a page
  folder, two below a Task or Discovery task; 40 files per folder, the rest a
  count) (JL: a tree, not a table; concise and clean, the works to the right,
  readable at 1360px, the project homes in another box; the `holds` text and
  an explanation table were both tried on the tree and dropped: less is
  more); slots with no folder yet are named under the boxes. The card states
  its backend Markdown. Nothing is created from the view.
- Every Space ends with a `backend Markdown` card listing the files it read
  (JL: every word on the web must come from some Markdown): Markdown pages and
  outline files, the engine receipts (runtime.yaml, discovery.yaml,
  build-manifest.json, paper-build.toml), the task and discovery homes, and the
  space map. The plugin's own labels and hints remain in `live/paper.py`.

## 0.2.0 · 2026-09-16

- The route is live: `board/haipipe-board/live/paper.py` renders Setup,
  Ideation, Story, and Run from the Board's Markdown on every open, on any
  board.md with `dialect: paper`. No per-paper file, no Links key.
- Retire the 0.1.0 `console/` prototype (static `data.js`, one paper only)
  and its `paper-plugin` Links key; `board-console` alias stays readable.
- Codex sessions are per Section Page (JL): one row per Main/Appendix page,
  none for Ideation, Story, or Supporting; a row is a plan until a pair
  manifest with exactly that name exists.
- Ideation reads the Ideas (ranked) table, else the plan's `Idea <n>:`
  divisions, so a P0 board with no Content still lists its ideas. Each idea
  is one collapsed Idea Card shaped like Outline's Evidence cards (JL: open
  and hide it); the detail holds Bullets, Notes, Evidence lines, bound
  Evidence Items, table fields, and the division link.
- Gates G0–G5 read named files; the Workflow map is projected from
  `ref/space-mapping.md`. Type scale and chips follow `live/outline.py`.
- Story Space is five card lists (JL: judge, not write): Claims & Hypothesis
  (C5 joined to C3), Task Roadmap, Sections (C8), and hero Evidence Items
  (Main-page DISPLAY + Abstract VALUE), beside Spine. Spine shows the Story's
  C1 Identity, C2 Pitch and C4 Stakes content, not a division list (JL).
- Task Roadmap opens with the project's Task home, examples/<Project>/tasks/
  or task/ (JL: check the existing folder): one collapsed card per bNN block,
  its jobs and a task table (addr · task · develops · runs · state) read off
  the folder on every load, in both Task shapes (a task folder under the job
  with its own runs/ results/ scripts/, or the flat runs/<task>/ layout). C7
  rows follow; a row joins the tree only through a bNN[.jNN[.tNN]] address in
  one of its cells and otherwise reads `no address yet`. It also shows on a
  board with no Story yet.
- A paper claims its part of the Task home (JL: b05, b06 are another study's):
  board.md `blocks: b00.j04 b02.j01 b02.j02 b03 b04` plus every C7 address.
  Claimed blocks expand; a claim at job level hides the block's other jobs;
  unclaimed blocks are named once in a muted tail; no claim shows the whole
  home and says so. `task-home:` may name the folder outright.
- Discovery needs link to the Discovery home (JL): examples/<Project>/
  discoveries/ (or `discovery-home:`) is scanned bNN board → jNN inquiry →
  tNN Discovery Task Page; each D-row's address (b01.j04) becomes an Outline
  link into that Discovery Board, one card per inquiry lists its Task Pages
  with question · runs · status · outcome · confidence from discovery.yaml,
  and each card's feeds row names the D-rows that claim it. Claim with
  `discoveries:` + C6 addresses; MISQ StoryA C6 rows D1–D6 now carry
  `Discovery: b01.j01` … `b01.j06`.
- Setup's Board and Folder & Page views are one table (folder · role · state ·
  pages) with the desk named, and no generated `delivery/` row.
- Delivery Space (JL: the whole paper's delivery was missing): Manuscript ·
  Sections · Displays · Checks · Rounds & Venue, read from delivery/
  (paper-build.toml, build-manifest.json, display-register.md, the outputs and
  word-feedback/), the compile order with every page's fragment and lanes, and
  the Bc-<desk>-Round pages. Chip order was Setup · Ideation · Story · Delivery ·
  Run (superseded below); a board with no delivery/ shows `G4 open` and the finish rule.
- Run Space rebuilt by run type (JL: like the Outline Run workspace, Supporting
  Runs as a BJTR tree): Page Runs (RP · RD · judgment), Evidence Runs (each
  Evidence Item joined to its Local Run), Supporting Runs (the addresses on
  `Supporting Runs:` lines drawn Block › Job › Task › Run per owner, Execution
  and Discovery, each Run resolved to its ticket and receipt with its users).
  Chip order is now Setup · Ideation · Story · Run · Delivery. Run ids keep
  their dotted targets (`rp-scratch-01_C1.P1`).
- `⧉ copy to chat` (JL: it was only readable): every card, Spine row and text
  selection copies a chat-ready snippet that cites its Markdown `source:` and
  row ref; cards carry `data-src` / `data-ref`. It writes nothing and the page
  makes no request. Storage now states the law: Markdown is the only truth
  source; JSON/TOML/YAML read are engine receipts, shown and never edited.
- Evidence Items: a `#### E…` heading is a retired item; an item ends at any
  heading, so a retired block no longer overwrites the live item above it.
- Reading pass (JL: larger, and cell edges instead of text nested in text):
  label/value rows are one `_kv()` table with borders and a shaded label cell;
  a row with no label, or whose value is a table or a tree, spans the full
  width; every grid table has cell edges and a shaded header; base type is
  16px; long Story prose is set one sentence per line (`prose()`, display
  only); an open card shows its whole title. Every card's
  Discussion row joins the judgment Run whose ticket `target:` names the row
  (ridea · rclaim · rtask · rnarra; run-naming.md §8).
- Tooth: `board/haipipe-board/tests/test_paper_plugin.py`.

## 0.1.0 · 2026-09-16

- First contract: four Spaces over a static per-paper `console/` behind
  `/_board/paper`.

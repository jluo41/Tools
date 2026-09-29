# CHANGELOG · haipipe-workbench-paper

## 0.9.1 · 2026-09-29 · Each Appendix page shows its own pair

- `servers/workbench-paper/paper.py`: Sections › Narrative finds a page's call-peer pair by its `session:` and `codex-session:` ids together first. The Appendix pages share one Claude session and each keeps its own Codex thread, so the Claude id alone gave every Appendix page the last pair registered (Paper-CGMtoHbA1c showed `CGM2HbA1c-Appendix-C` three times). Tests: `test_paper_workbench.py`, 12 pass.

## 0.9.0 · 2026-09-29 · The cover letter in Delivery; the Roadmap tree

- An opened T or D question shows its BJTR folders first, already open (JL 260929: "I want to make the bjtr be the most important things"); the row's own text (design, contrast, result form, branches, depends on, feeds) folds under a closed Details line; the Task home rows that repeated the folders are gone.
- Delivery gains a fourth tab, Cover letter (JL 260929: the cover letter is one more delivery item). It
  reads `build-manifest.json` `cover_letter`, which haipipe-paper-assemble 0.9.0's run-delivery-coverletter
  writes from the submission Round page's Cover letter division: Preview shows the letter PDF, Artifacts
  its files, Checks each letter check and whether it is ready, with Open ↗ to the Round page. The fixed
  run run-delivery-coverletter shows under the `paper.coverletter` card (views cover). The letter no
  longer repeats in the LaTeX and Word tabs.
- Story › Roadmap is a tree when the Story has a C6 `Q` table: general question → its T and D rows (by
  their `Q` column) → their folders; a row with no Q comes last; a range address such as
  `b03.j02.t01–t03` names each task; selecting a Q filters the Runs panel to its runs.
- New buttons with skills: Select idea (Ideation, haipipe-ideation-select), Page check (Sections,
  haipipe-page-check).

## 0.8.0 · 2026-09-28 · Question first; every run names its skill

- Story › Roadmap is question first: a C7 T row or C6 D row card holds the folder that answers it;
  folders no question names are listed last, down to the task. The separate Task home and Discovery
  home lists are gone. `no address yet` reads `no folder yet`.
- The Story's C6 and C7 rows lead with a short plain question and a folder column; B1–B4 became
  T1–T4 (the header always said T; B was the old Block Board id).
- Runs panel: every Paper run card has a `🧩 SKILL` line (`paper_run_types` reads it); Supporting
  runs split into Task runs (haipipe-task) and Discovery runs (haipipe-discovery).
- Sections › Evidence cards show the item's real state (`Result ready` when its Local Run Result
  is on disk, instead of `contract only` on every card), type-first names (Evalue03) and its
  Supporting Runs.
- `studio/paper-workbench-design.py` now generates `studio/paper-workbench-design.excalidraw`
  (AGENTS.md rule 6). Part 1 answers the main question: each Space, its sub-spaces, their runs in
  order, and the skill of each run; it also draws the next step, Q1–Q5 general questions above T
  and D, and a Delivery › Cover letter sub-space.

## 0.7.1 · 2026-09-28

- `ref/space-mapping.md`: `deliver.<page>.<format>` reruns the lane's one fixed Delivery Run (`run_delivery_<lane>`); no receipt (JL 260928).
- The Narrative card's Session row reads the Section Page's own `session:` and
  `codex-session:` lines (written by `/haipipe-paper sessions`) and joins a call-peer pair by
  that exact Claude session id, before the old exact-name lookup. It shows the pair name,
  `claude <id>` and `codex <id> · <date>`; a page with no session still reads `no session · plan`.

## 0.7.0 · 2026-09-27

- The Paper Workbench follows the Page workbench (JL 260927: "make it aligned"; the drawing is
  `servers/workbench-paper/studio/paper-workbench-design.excalidraw`). Four Spaces: Ideation ·
  Story (Spine, Questions, Roadmap) · Sections (Main, Appendix × Table, Narrative, Evidence) ·
  Delivery (LaTeX, Word × Preview, Artifacts, Checks; Rounds). Each Space has its content on the
  left and its own Runs panel on the right, the Page's `runs_panel.py` markup; buttons come from
  `haipipe-paper-workflow/ref/run-cards.md`. Opening a card or clicking a row selects it for the panel.
- Gone: the Setup Space (a C8 row with no Page reads `not set up`; the Codex session sits on the
  Section's Narrative card), the Run Space (its runs are in the Runs panels; gates show where they
  happen), the Workflow map and folder tree (docs only), the backend Markdown cards, `⧉ chat` and
  `⧉ Copy Run request`, tallies, briefs and hint lines. Old `#setup/…`, `#run/…` and view routes
  still land on the view that holds their content.
- Sections Space is new: the compile order joined to each Section Page (draft version, state,
  Open ↗ to its workbench), the C8 narrative cards, and the hero Displays and Values; a selected
  Section shows its Narrative review and its own Draft, Evidence and Delivery runs.
- Shared with the Page workbench (`servers/workbench-page/runs_panel.py`): a type's count follows
  the selected target and view, and the panel opens on a type that has runs there; `panel_markup`
  is the reusable half of `panel_html`; judgment runs show as `run-idea`, `run-claim`, `run-task`,
  `run-narrative`.
- `tests/audit_paper_views.py` walks the seventeen new routes and flags a view with no Runs panel.
- Rosters and Stories in other shapes now read: a `### Label · folder · what it holds` heading, or one
  with no folder (the page is found by its own folder name), and C8 rows written as records
  (`**S-<id> (N) · job**` + `- **Field**: value` lines) beside the table form. A desk name may carry
  a hyphen (`S-JAMA-IM-Main-1-Introduction`). Paper-AgreeableOpioid-Jama showed no Story before.

## 0.6.0 · 2026-09-22

- Story Space reads legacy numbered Story pages (`Story01-seed`, `Story02-roadmap`,
  `Story03-narrative-MISQ`) as Stories beside canonical `Story<Letter>`; before, a board
  with only numbered Stories showed "no Story yet" and none of their cards or Runs (JL 260925).
- Story Space: the `Claims & Hypothesis` view is now `Research Questions`
  (`#story/questions`; `#story/claims` still lands there). The card grain is
  the C3 research question; its C5 propositions (the claims) sit inside as
  nested cards, each keeping its `claim-En` id, `C5 · En` source stamp and
  rclaim Discussion row. Before, one card per claim repeated the same question
  in every card that shared it (JL 260922: combine them, do not rename claims
  to research questions). E-rows whose RQ cell names no C3 row are kept in one
  last card. `servers/workbench-paper/paper.py`: `_rq_cards` + `_claim_card`
  replace `_claim_cards`; E/RQ columns are found by header name when the table
  has a header row, else by the positional convention.

- Ideation Space: an Idea Card leads with the Idea's **Research Question** (its title
  drops to the subline); without one the title leads and the subline says `no Research
  Question written yet`, with a row naming the empty field. The plan's Bullets are a
  collapsed `writing plan` at the end of the card, never the lead (JL 260922: "the
  ideation should be the research question, which can trigger the reader to think").
- Ideation Space: the line above the Idea pool cards (`Story00-ideation · state … · plan
  … · approved: …`) is gone (JL 260922: "I don't want this"). The page and its plan
  remain named in the Space's backend Markdown footer.

## 0.5.0 · 2026-09-22

- Renamed with the vocabulary: `plugin` now means only a Claude Code plugin
  (`plugins/haipipe-toolkit`), a **lane** is a folder on disk, a **workbench** is
  a served tab and its contract. This skill was `haipipe-plugin-paper`; it pairs by name with
  `servers/workbench-paper`.

## 0.4.1 · 2026-09-21

- Add separate `⧉ Copy Run request` clipboard controls to bound Paper judgment
  entries for admitted Ideas, C5 claims, C7 obligations, and C8 narratives.
  Prompts carry the exact Page/target, instantiated Spec, Run Type, owner,
  prerequisites, family-filtered matching Ticket/Result/status, expected
  receipt, and next permitted owner action.
- Keep `⧉ chat` as source-grounded discussion context. Run-request controls
  only copy text; they never send, start, allocate, or write. Leave unsupported
  Page, Evidence, Support, Delivery, Compile, and Response entries prompt-free.

## 0.4.0 · 2026-09-21

- Expand the Run map with reader-facing names, canonical Types/Specs, bounded
  work, owner/worker Skills, actors, prerequisites, and per-Space role/entry.
- Keep controls distinct from Specs and actual native Runs. Preserve source-
  grounded copy-to-chat as discussion context; identify the separate Run-
  request prompt control as not built.
- Cite the map's Markdown when copying selected map text and avoid repeating
  folder chips across the normalized Spec × Space entries.

## 0.3.0 · 2026-09-20

- Align the Space/folder map with the canonical Run Specs and explicit controls. Present all five Spaces and owner-native receipts without allocating wrapper Runs.

## 0.2.2 · 2026-09-18

- Reading polish from a full audit (all twenty Space views of both papers,
  driven in real Chrome over CDP at 1360px and 2000px: no page overflow, no
  leaking view, nothing past the right edge): no type under 12px (the `⧉ chat`
  control, kind pills, sub labels, gate ids and bullet ids were 10 to 11px); a
  closed card shows its whole headline instead of clipping a claim or an idea
  with an ellipsis; a card subline that repeats the `where` label (the RQ on a
  claim card) is dropped; a long name clipped deep in the folder tree carries
  its full name as a tooltip. The audit is kept as a tool:
  `board/haipipe-board/tests/audit_paper_views.py --base … --paper …`.
- Cold-read fixes (a fresh agent was handed a pasted `⧉ copy to chat` snippet
  and asked to act on it, dry run; its friction log): the C7 card resolved
  only the FIRST address on a row while the claim counted them all, so
  `task_home()` now resolves every address and the card shows each; SKILL.md
  gains the address grammar and the `Task: bNN.jNN.` suffix convention, the
  two words CLAIMED and ADDRESSED, the writer rule (a traceability edit is
  made directly in the `source:` file; an edit that changes what the paper
  says routes to its owning skill), the `#<space>/<view>` route table, where
  the reader-facing origin comes from, and what to take from `haipipe-workbench`;
  stale `four Spaces` wording swept from SKILL.md, `servers/workbench-paper/paper.py` and the
  test; the Task-home brief no longer says nothing is typed (the claim is).

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
  space map. The workbench's own labels and hints remain in `servers/workbench-paper/paper.py`.

## 0.2.0 · 2026-09-16

- The route is live: `servers/workbench-paper/paper.py` renders Setup,
  Ideation, Story, and Run from the Board's Markdown on every open, on any
  board.md with `dialect: paper`. No per-paper file, no Links key.
- Retire the 0.1.0 `console/` prototype (static `data.js`, one paper only)
  and its `paper-workbench` Links key; `board-console` alias stays readable.
- Codex sessions are per Section Page (JL): one row per Main/Appendix page,
  none for Ideation, Story, or Supporting; a row is a plan until a pair
  manifest with exactly that name exists.
- Ideation reads the Ideas (ranked) table, else the plan's `Idea <n>:`
  divisions, so a P0 board with no Content still lists its ideas. Each idea
  is one collapsed Idea Card shaped like Outline's Evidence cards (JL: open
  and hide it); the detail holds Bullets, Notes, Evidence lines, bound
  Evidence Items, table fields, and the division link.
- Gates G0–G5 read named files; the Workflow map is projected from
  `ref/space-mapping.md`. Type scale and chips follow `servers/workbench-page/outline.py`.
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
- Tooth: `board/haipipe-board/tests/test_paper_workbench.py`.

## 0.1.0 · 2026-09-16

- First contract: four Spaces over a static per-paper `console/` behind
  `/_board/paper`.

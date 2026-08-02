# The round trip: md to html, and html back to md
state: 🟡 PARTIAL · the canonical board/ tree, per-page rebuild, rerooting, and checks ship; SSE remains open
owner: JL
method: draw the whole loop in both directions first, then rule the unit of change, the output layout, and what refreshes when

## Opening
How does a change travel from Markdown to the open page and safely return from the browser to Markdown?

The forward build, browser delivery, and write-back path live in different parts of the engine.
Without one contract, each feature can choose a different unit of change or treat generated HTML as a second source.
The loop determines what rebuilds, what the browser replaces, and how an edit becomes durable.
It succeeds when a returned edit updates one Markdown source, rebuilds its page, group, and Index, and swaps only the requested page.


## Diagram

```text
   ── the loop, as it runs today ───────────────────────────────────

   ✍️ SOURCE                  ⚙️ RENDER                🌐 DELIVERY
   board.md                   build.py                 board/index.html
   QA1-….md                     src/parse.py             board/<GROUP>.html
   QB4-….md                     src/page_board.py        board/<GROUP>/<page>.html
   …                            src/page_question.py     board/_assets/{css,js}
        │                       src/body.py                    │
        │                            ▲                         │
        │  a human edits             │  one page + group       │  HEAD poll
        │  a file directly           │  + Index under --only   │  every 4 s
        ▼                            │                         ▼
   ┌─────────────────────────────────┴──────────────────────────────┐
   │                                                                 │
   │   live/write.py            ◀── the RETURN direction             │
   │   add_comment · edit_sentence · add_sentence · add_discuss      │
   │   anchor by exact sentence match (QC4a), insert at a section     │
   │   boundary, rewrite the whole .md, then call build.py           │
   │                                                                 │
   └─────────────────────────────────────────────────────────────────┘
        ▲
        │  a person selects a sentence in the browser and types
        │  a comment, an edit, a lane, a discussion line
        └── or the chat drawer writes the same way, through the same endpoints

   markdown is the ONLY source; html is derived and never edited
```

```text
   ── the same loop, with the unit marked at each hop ──────────────

                        today                         still open
   source write         one Markdown file            —
   rebuild scope        page + group + Index         —
   output shape         board/ tree                  —
                        one file per page + assets
   notification         poll, up to 4 s              SSE, under 100 ms
   what the tab swaps   one page's div.wrap          —

   every row is independent: each can be adopted without the others
```

## Content
### 1 · The forward path, as it is
`build.py` takes a Board source folder and writes the canonical `board/` site.
It discovers every page by path (`page_files()` in `src/common.py`), parses each into sections (`src/parse.py`), renders one file per page and group plus the Index, and assembles the CSS and JavaScript once under `board/_assets/`.
`watch.py` passes one changed filename through `--only`, so that page, its group page, and the Index move while unrelated page files stay byte-identical.

### 2 · The return path, as it is
Every write endpoint in `live/write.py` follows the same four steps, and `QC4a` owns the first two.
It normalizes the sentence the browser sent, finds the one source line whose normalized form matches exactly, refuses when there are zero matches or several, walks to a structural insert point rather than a byte offset, rewrites the whole markdown file, and then calls `build.py`.
The chat drawer is not a separate path: it writes through the same endpoints, so a machine and a person leave the same kind of line in the same place.

That symmetry is the reason the loop is safe, and it is worth protecting: there is exactly one implementation of "how a change is written into markdown", and everything that writes goes through it.

### 3 · The unit at every hop
The source write is one Markdown file, anchored by an exact sentence or a named section boundary.
The incremental rebuild is that page, its group page, and the Index.
The generated unit is one page file; CSS and JavaScript are shared.
The browser swaps the requested page's `div.wrap`, leaving the drawer and terminal outside the replaced region.
Only notification remains larger and slower than it needs to be: the open tab polls every four seconds instead of receiving the changed page id through SSE.

### 4 · The shape that ships
`board/index.html` is the front door, `board/<GROUP>.html` explains one group, `board/<GROUP>/<page>.html` holds one focused page, and `board/_assets/` is shared.
Internal links are intercepted, the target page is fetched and swapped, and the URL is pushed; with scripts off the same links navigate normally, so the strip-scripts invariant holds.
Board-root-relative `href`, `src`, and `data` attributes are rerooted for each generated depth, including the evidence-card panels outside the page body.
A push instead of a poll is the only proposed structural change left on this page.

### 5 · What happened to `board.html`
JL ruled it out on 260731, and a Board-folder build now removes a leftover monolith after generating `board/`.
The no-script property moved with the canonical output: every page remains complete and navigable with JavaScript removed, and `build.py` plus `check.py` assert that property on the split files.
A single Markdown target may still render one HTML file for compatibility; that is not a Board-folder output and is not a second front door.

## Items to Finish
### The loop as one description
- [x] 🔁 Write the loop into the skill, once
      `SKILL.md` now states the complete source → render → delivery → write-back loop in one place; the implementation files remain its executable parts.
- [x] 📏 State the unit at every hop
      The contract now names source-write, rebuild, generated-file, notification, and browser-swap units separately.

### Building the proposed shape
- [x] 🗂 Emit the `board/` tree
      The canonical output: one file per page, one per group, one Index, shared assets, and rerooted local resources.
- [x] ⚡ Rebuild one page
      `build.py --only` rewrites the changed page, its group page, and the Index while leaving unrelated page files byte-identical.
- [ ] 📡 Push instead of poll
      An SSE endpoint that names the page that changed, and a client that fetches and swaps only that section.
- [x] 🔗 Intercept internal links
      So navigation inside the tree never destroys the drawer or the terminal, and so the no-JS path still navigates.

## Where we are

- 260801 JL · 🐢 Navigation was re-downloading a rail it throws away
  JL: "why I feel it will have a long time to navigate to different pages?"
  Measured rather than guessed, and the answer was not the renderer: the server answers in 8ms, wiring a swapped page costs 4ms, and the fetch itself was the whole cost.
  Every page file carries the complete rail, 112 KB of it, and the router swaps only `div.wrap`, so on a median 136 KB page 82% of the bytes are discarded on arrival; across the tree that is 7.10 MB of 9.40 MB spent on 65 copies of one rail.
  The fetch also asked for `cache: 'no-store'` and the server sent `Cache-Control: no-store`, so those bytes were re-downloaded on every single visit.
  `no-store` was the wrong instrument for the guarantee it was written to protect (JL 260726, "why now I cannot open them"): the requirement is never serve a page from before the last build, and that is `no-cache`, which means REVALIDATE BEFORE USE rather than may-be-stale.
  Both sides now say `no-cache`, and a revisit costs 0.3 KB instead of 119 KB, with the body still arriving from cache.
  The staleness guarantee was tested directly rather than assumed: warm fetch 0.3 KB, then the file was edited on disk, and the very next fetch was a full 119 KB carrying the new bytes.

- 260801 CC · 🧭 The contract and the canonical output agree
  `SKILL.md`, `ref/board-form.md`, `haipipe-board-index`, `build.py`, `watch.py`, `check.py`, and the design and Paper boards now describe the same Board-Folder to Board-Webpage tree.
  The Paper Board exposed the remaining runtime defect: evidence-card panels were outside the body reroot pass, so 749 source links plus their images and PDF objects broke on split pages.
  One shared `tree_reroot()` now moves `href`, `src`, and `data`; the checker covers all three.

- 260731 CC · 🔌 The split broke both halves of the live layer, and both are fixed
  Splitting one document into 61 files moved two assumptions the drawer and the server had each baked in.
  The drawer identified its page by `location.hash`, which no split page has, so every page opened the board session; it now reads the document itself (`QD1`).
  The server derived a board folder as the URL's parent directory, so any POST from `board/<GROUP>/<page>.html` was refused with "no board.md here"; `target()` now walks up until it finds `board.md`, bounded by `--root`, which leaves the one-file path matching on its first try.
  Both were invisible from the source: only driving the real split pages in Chrome surfaced them.


- 260731 JL · 🗂 The `board/` tree is BUILT and serving
  JL: "just go ahead and work until I can check the board", so this shipped rather than becoming another row to tick.
  `build.py` emits one file per page, one per group, and an index, sharing a single copy of the CSS and JavaScript: 61 files for this board, and one page is 27 KB against the former single file's 2.06 MB.
  The MISQ lifecycle board is the sharper case, 132 KB against 3.23 MB.
  Verified rather than assumed: every one of the 61 links crawled from the index resolves and renders, `page_files()` still discovers 54 pages with none from `board/`, and all five sibling boards plus the MISQ board split cleanly.
  Two things had to change with it, and both were predictable from the design: the CSS router hid a lone page because it waits for a `:target` that a one-page document never has, so `body.site` opts out, and a link click in the tree would have been a real navigation, which destroys the drawer, so internal links are intercepted and swapped exactly as the live update does.
  `board/` is gitignored because it is derived; the later JL ruling retired `board.html` as a Board-folder output.

- 260731 JL · 🧪 Driven in a real browser, which is where the real bugs were
  JL asked twice whether CC tests its own work, so the tree was driven over CDP with real clicks instead of checked with curl.
  Three defects only a real submit could expose, all of them silent.
  Every write in the tree failed without an error: a write posts `location.pathname` and the server takes its PARENT as the board folder, so from `board/QC/page.html` it looked for `board.md` inside `board/QC/` and found nothing; seven writers now share one `boardPath()` that collapses the tree tail back to the board root.
  `serve.py`'s rebuild did not pass `--split`, so a comment written from the page updated the then-current monolith and left the tree stale; a Board-folder build now always targets the tree.
  And deleting a page's `.md` left its `.html` in the tree forever, still linkable and still looking real, so the tree now prunes anything outside the expected set, computed from every page rather than from what one run happened to write.
  What the first render pass got wrong belongs here too, because it was this family's own law broken by its author: the index rows were REIMPLEMENTED with invented class names instead of reused, so not one CSS rule matched and the index rendered as a wall of inline links.
  The rows now come from one shared builder.

- 260731 JL · ⚡ One page changes, three files move, and nobody else is disturbed
  `watch.py` passes the changed filenames to `build.py --only`, which rewrites just those pages plus the groups containing them plus the index: 3 files out of 61.
  Measured in a real browser: sitting on `QB4` while `QC4` was rewritten left `QB4`'s DOM untouched, its open sections open, and its scroll unmoved.
  End to end with nothing but a file save, the page updated itself in about 4 seconds with no reload.

Both directions of the loop work and are now written once in the operating skill.
The return path still has one implementation and one anchoring rule; the forward path has one parser and renderer, one canonical tree, and one explicit unit at each hop.
SSE remains open because the four-second notification poll is the only hop still larger than the changed page.

### Decision Now
- [ ] 🪞 Rule what to do about the rail in every page file
      112 KB of every page is the rail, the router discards it on arrival, and it is 76% of the whole tree on disk; revalidation now hides that cost on revisits but a FIRST visit still pays it.
      A · leave it, now that a revisit costs 0.3 KB: the waste is only paid once per page per build, and the rail is what makes the tree navigable with scripts off.
      B · serve a fragment when a server is present: the router asks for `div.wrap` only, the file on disk keeps its rail, and a static host is unaffected.
      C · stop emitting the rail in page files and let the Index carry navigation: smallest files, but a page opened with scripts off can then only go back to the Index.
      → CC recommends B, because it is the only one that makes a FIRST visit cheap without taking anything away from the no-JS reader; A is a fair answer if the tree is only ever read over localhost.
These are the calls only JL can make; CC ticks nothing here.

- [x] 🧭 Rule what the tree's index still owes
      Before this ruling, the split tree's Index was only a roster and did not carry the Board-level orientation found in the retired monolith.
      A · port all four onto the tree index, so the tree becomes the only front door.
      B · port only the progress bar and the Section Matrix, and leave the Board Map and Activity to the single file, keeping the tree lean.
      C · leave the tree index as a plain roster, and treat the single file as the place you go to see board-level state.
      → JL chose the canonical tree front door. It carries the Board Map, Related Folders when declared, Section Matrix, page roster, and Activity; progress lives on group pages.
- [x] 🔍 Rule whether `check.py` looks at the tree at all
      Before this ruling, no checker verified missing pages, orphan files, scripts-off content, or resource links in the generated tree.
      A · teach `check.py` the tree: every page has exactly one file, no orphans, and the two packagings list the same pages.
      B · leave it, on the grounds that the tree is derived and a rebuild fixes everything.
      → JL chose A. `check.py` now verifies the split site directly, including no orphan, no missing page, scripts-off content, local links, media, and balanced structure.

- [x] 📄 Rule whether `board.html` is dropped now that `board/` ships
      JL 260731: "then we will not use this anymore, right? we will drop this."
      A Board-folder build has one live output today: the generated `board/` tree.
      A · drop `board.html`, leaving one output and nothing to keep in step.
      B · keep emitting it until `board/` has carried real work for a while, then drop it against a stated criterion.
      C · keep it permanently as the shareable artifact, which is what `QE3`'s Law says today.
      → JL chose A. `build.py` removes a leftover monolith after generating the tree, and every new deep link points into `board/`.

- [x] 🗂 The generated tree lives in `board/`
      BUILT 260731, named by JL, who rejected both `_site` and `_board`: "I just want board".
      Verified rather than assumed: `page_files()` discovers 54 pages and none come from `board/`, because that folder holds no `.md` at all, so the discovery rule never needed the `_` prefix here.
      The `.gitignore` entry is ANCHORED on purpose: a bare `**/board/` would also match `skills/board/`, the skill family itself, and silently untrack all 52 of its files.
      A `board/` folder inside a board folder does not collide with the `/_board/` API either, because every route check is anchored at the server root; both were tested.
- [ ] 📡 Rule push versus poll
      A · SSE, so the page is told which page changed the moment the write lands, under 100 ms instead of up to 4 s.
      B · keep the 4 second poll, which needs no new endpoint and no long-lived connection.
      → CC recommends A; `QD4`'s Law already names SSE as the upgrade path, and this is the case it was reserved for.

## Files
- `../../board/haipipe-board/build.py`
  The forward path's entry point; it decides the output shape, so the `board/` tree is a change here and nowhere else.
- `../../board/haipipe-board/live/write.py`
  The return path: four endpoints, one anchoring rule, one implementation.
- `../../board/haipipe-board/assets/js/70-router.js`
  The delivery half: the 4 second poll, the swap, and the link behaviour that a split tree would change.
- `../../board/haipipe-board/src/common.py`
  `page_files()`, the discovery rule whose `_` prefix exclusion is what makes `board/` free.
- `QC4a-writepath.md`
  The return direction's addressing contract, which this face uses and does not restate.
- `QD4-liveupdate.md`
  How the browser learns and what it replaces, including the three symptoms this face's unit argument explains.

## Log
260801 · Navigation cost measured and halved at the wire: `no-store` became `no-cache` on both the router's fetch and the server's header, so a revisited page costs 0.3 KB instead of 119 KB; staleness re-tested by editing a page on disk. The 112 KB rail duplicated into every page file is recorded as an open decision
260801 0920 · Canonicalized the board/ tree across contract, engine, checker, and both design/Paper Board structure blocks; fixed href/src/data rerooting exposed by 749 Paper Board failures
260801 0140 · Full renumber QC7 -> QC4 (JL forced 260801); write-path face QC7a -> QC4a
260801 0130 · Reindexed QC9 -> QC7: the round trip becomes the parent, with the write path (old QC7) as its face QC7a (JL 260801)
260731 · `board/` tree BUILT and verified across 6 boards: build.py --split, body.site router opt-out, link interception so the drawer survives navigation, gitignored as derived (haipipe-board 0.80.0)
260731 · Opened on JL's ask for one Q describing how md renders into html and how page changes go back into md, after the file-layout and Flask discussions kept landing on faces that owned only one hop of the loop

# The round trip: md to html, and html back to md
state: 🟡 PARTIAL · the board/ tree is built and serving; per-page rebuild and SSE are next
owner: JL
method: draw the whole loop in both directions first, then rule the unit of change, the output layout, and what refreshes when

## Opening
How does one change travel from a markdown file to the page a person is looking at, and how does a change made on that page travel back into the markdown?
Both halves exist and work today, and neither is described in one place: the forward path lives in `build.py`, the return path in `live/write.py`, and the delivery in `board.js`, so the loop can only be understood by reading three files and inferring the join.
Nothing owns the loop itself, which is why questions about it keep landing on whichever face is nearest.

The loop has one property worth stating before anything else: markdown is the only source.
Every other artifact is derived and disposable, so the html is never edited and never merged; it is rewritten.
That single rule is what makes a round trip safe, because the return direction only ever has to produce markdown, never reconcile two versions of the truth.


## Diagram

```text
   ── the loop, as it runs today ───────────────────────────────────

   ✍️ SOURCE                  ⚙️ RENDER                🌐 DELIVERY
   board.md                   build.py                 board.html
   QA1-….md                     src/parse.py             ONE file, 2.02 MB
   QB4-….md                     src/page_board.py        all 53 pages inside
   …                            src/page_question.py     CSS + JS inlined
        │                       src/body.py                    │
        │                            ▲                         │
        │  a human edits             │  0.38 s, whole board    │  HEAD poll
        │  a file directly           │  on ANY change          │  every 4 s
        ▼                            │                         ▼
   ┌─────────────────────────────────┴──────────────────────────────┐
   │                                                                 │
   │   live/write.py            ◀── the RETURN direction             │
   │   add_comment · edit_sentence · add_sentence · add_discuss      │
   │   anchor by exact sentence match (QC7), insert at a section     │
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

                        today            proposed
   rebuild scope        whole board      the ONE page that changed
   output shape         1 file           board/ tree, one file per page
                        2.02 MB          34 KB per page + shared assets
   notification         poll, up to 4 s  push, under 100 ms  (SSE)
   what the tab swaps   all 53 pages     the one section that changed

   every row is independent: each can be adopted without the others
```

## Content
### 1 · The forward path, as it is
`build.py` takes a board folder and writes one file.
It discovers every page by path (`page_files()` in `src/common.py`), parses each into sections (`src/parse.py`), renders them (`src/page_board.py`, `src/page_question.py`, `src/body.py`), and inlines `assets/board.css` and `assets/board.js` so the result is self-contained.
The whole board is rebuilt on every invocation, and it takes 0.38 seconds on this board's 53 pages, so the rebuild has never been the slow part.

### 2 · The return path, as it is
Every write endpoint in `live/write.py` follows the same four steps, and `QC7` owns the first two.
It normalizes the sentence the browser sent, finds the one source line whose normalized form matches exactly, refuses when there are zero matches or several, walks to a structural insert point rather than a byte offset, rewrites the whole markdown file, and then calls `build.py`.
The chat drawer is not a separate path: it writes through the same endpoints, so a machine and a person leave the same kind of line in the same place.

That symmetry is the reason the loop is safe, and it is worth protecting: there is exactly one implementation of "how a change is written into markdown", and everything that writes goes through it.

### 3 · What the loop is missing, stated as one word
The unit.
Every hop in the loop operates on the whole board when it could operate on one page: the rebuild regenerates 53 pages because one changed, the output is one 2.02 MB file when a reader needs 34 KB, the browser is told only that "something changed" rather than what, and it therefore replaces every page in the document.

The cost is not theoretical and JL named all three symptoms on 260731.
A reader on page B has their page replaced when page C is written, because the swap's unit is the document.
The chat drawer and the terminal survive that swap only because they were deliberately parked outside the swapped region, which is a workaround for a unit that is too large.
And the visible flash through the Index on every update is a consequence of replacing the element the URL fragment pointed at.

### 4 · The proposed shape
Three changes, each independent of the others, each addressing one row of the second figure.

A `board/` tree, emitted by the same renderer as a second output mode.
One file per page plus one per group, sharing a single copy of the CSS and JS, so a page costs 34 KB rather than 2 MB and has a real URL that can be linked, bookmarked, and shared.
The `_` prefix already means "not a page" in this board's discovery rule, so no new rule is needed to keep the generated tree out of the page roster.

A per-page rebuild, so a write to one page rewrites one file.

A push instead of a poll, so the browser learns which page changed the moment the write lands rather than up to four seconds later.
`QD4`'s Law already names SSE as the upgrade path, and this is the case it was reserved for.

Navigation inside the tree must not be a real page load, or the drawer and terminal die on every click, which is the exact problem the parked-outside-the-region design was invented to avoid.
Internal links are intercepted, the target page is fetched and swapped, and the URL is pushed; with scripts off the same links still navigate normally, so the strip-scripts invariant holds.

### 5 · What happens to `board.html`
It is the one-file artifact: hand a colleague one file, open it with no server, project it in a meeting, attach it to a mail, keep it as an archive of what the board said on a date.
`QE3`'s Law makes it an invariant, and that Law is settled rather than incidental.

The case for dropping it once `board/` exists is that two outputs are two things to keep correct.
The case against is that they cannot drift in content, because both come from one parser and one renderer and differ only in packaging, so the maintenance argument is weaker here than it usually is.
What dropping it actually costs is the single-file properties, and a `board/` tree recovers most of them: relative links work over `file://` and a folder can be zipped, but a folder is not one attachment and the strip-scripts assertion is written against the single file.

## Items to Finish
### The loop as one description
- [ ] 🔁 Write the loop into the skill, once
      Today an agent has to read `build.py`, `live/write.py`, and `board.js` to learn what this face draws in one figure; the loop belongs in `SKILL.md` or in the routing spec as a stated contract.
- [ ] 📏 State the unit at every hop
      Rebuild scope, output shape, notification granularity, and swap granularity are four separate decisions that have always been made together by accident.

### Building the proposed shape
- [ ] 🗂 Emit the `board/` tree
      A second output mode on the same renderer: one file per page, one per group, shared assets, relative links.
- [ ] ⚡ Rebuild one page
      `build.py` needs a page-scoped mode before a per-page rebuild means anything.
- [ ] 📡 Push instead of poll
      An SSE endpoint that names the page that changed, and a client that fetches and swaps only that section.
- [ ] 🔗 Intercept internal links
      So navigation inside the tree never destroys the drawer or the terminal, and so the no-JS path still navigates.

## Where we are

- 260731 CC · 🔌 The split broke both halves of the live layer, and both are fixed
  Splitting one document into 61 files moved two assumptions the drawer and the server had each baked in.
  The drawer identified its page by `location.hash`, which no split page has, so every page opened the board session; it now reads the document itself (`QD1`).
  The server derived a board folder as the URL's parent directory, so any POST from `board/<GROUP>/<page>.html` was refused with "no board.md here"; `target()` now walks up until it finds `board.md`, bounded by `--root`, which leaves the one-file path matching on its first try.
  Both were invisible from the source: only driving the real split pages in Chrome surfaced them.


- 260731 JL · 🗂 The `board/` tree is BUILT and serving
  JL: "just go ahead and work until I can check the board", so this shipped rather than becoming another row to tick.
  `build.py --split` emits one file per page, one per group, and an index, sharing a single copy of the css and js: 61 files for this board, and one page is 27 KB against the single file's 2.06 MB.
  The MISQ lifecycle board is the sharper case, 132 KB against 3.23 MB.
  Verified rather than assumed: every one of the 61 links crawled from the index resolves and renders, `page_files()` still discovers 54 pages with none from `board/`, and all five sibling boards plus the MISQ board split cleanly.
  Two things had to change with it, and both were predictable from the design: the CSS router hid a lone page because it waits for a `:target` that a one-page document never has, so `body.site` opts out, and a link click in the tree would have been a real navigation, which destroys the drawer, so internal links are intercepted and swapped exactly as the live update does.
  `board.html` still ships, so nothing that pointed at it broke, and `board/` is gitignored because it is derived.

- 260731 JL · 🧪 Driven in a real browser, which is where the real bugs were
  JL asked twice whether CC tests its own work, so the tree was driven over CDP with real clicks instead of checked with curl.
  Three defects only a real submit could expose, all of them silent.
  Every write in the tree failed without an error: a write posts `location.pathname` and the server takes its PARENT as the board folder, so from `board/QC/page.html` it looked for `board.md` inside `board/QC/` and found nothing; seven writers now share one `boardPath()` that collapses the tree tail back to the board root.
  `serve.py`'s rebuild did not pass `--split`, so a comment written from the page updated `board.html` and left the tree stale, which is the one way the two packagings can disagree.
  And deleting a page's `.md` left its `.html` in the tree forever, still linkable and still looking real, so the tree now prunes anything outside the expected set, computed from every page rather than from what one run happened to write.
  What the first render pass got wrong belongs here too, because it was this family's own law broken by its author: the index rows were REIMPLEMENTED with invented class names instead of reused, so not one CSS rule matched and the index rendered as a wall of inline links.
  The rows now come from one shared builder.

- 260731 JL · ⚡ One page changes, three files move, and nobody else is disturbed
  `watch.py` passes the changed filenames to `build.py --only`, which rewrites just those pages plus the groups containing them plus the index: 3 files out of 61.
  Measured in a real browser: sitting on `QB4` while `QC9` was rewritten left `QB4`'s DOM untouched, its open sections open, and its scroll unmoved.
  End to end with nothing but a file save, the page updated itself in about 4 seconds with no reload.

Both directions of the loop work today and neither is written down in one place, which is why this face exists.
The forward path rebuilds the whole board in 0.38 seconds, the return path has exactly one implementation and one anchoring rule, and the join between them has never been described as a single contract.
Everything proposed above is about the UNIT, not about correctness: nothing in the loop is wrong, and every hop is simply larger than it needs to be.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [ ] 🧭 Rule what the tree's index still owes
      The single file's index carries a Board Map, the Section Matrix, the progress bar, and the Activity panel; the tree's index has none of them, so the tree is currently a worse front door than the file it is replacing.
      A · port all four onto the tree index, so the tree becomes the only front door and `board.html` is purely an export.
      B · port only the progress bar and the Section Matrix, and leave the Board Map and Activity to the single file, keeping the tree lean.
      C · leave the tree index as a plain roster, and treat the single file as the place you go to see board-level state.
      → CC recommends A, because the whole point of the tree is that it is what you actually work in, and a front door that shows less than the artifact will send you back to the 2 MB file.
- [ ] 🔍 Rule whether `check.py` looks at the tree at all
      Nothing verifies that the tree and the single file agree, that every page has a file, or that no orphan survived; the orphan bug was found by hand and would not have been caught by any checker.
      A · teach `check.py` the tree: every page has exactly one file, no orphans, and the two packagings list the same pages.
      B · leave it, on the grounds that the tree is derived and a rebuild fixes everything.
      → CC recommends A, because "derived" is exactly why nobody looks at it, and the orphan bug proves a stale file can outlive its page and still look real.

- [ ] 📄 Rule whether `board.html` is dropped now that `board/` ships
      JL 260731: "then we will not use this anymore, right? we will drop this."
      Both outputs are live today and come from one parser and one renderer, so they cannot disagree on content; only the packaging differs.
      A · drop `board.html`, leaving one output and nothing to keep in step.
      B · keep emitting it until `board/` has carried real work for a while, then drop it against a stated criterion.
      C · keep it permanently as the shareable artifact, which is what `QE3`'s Law says today.
      → CC recommends B: it costs 0.4 seconds a build, and dropping it also overturns a settled Law, which deserves a deliberate reversal on `QE3` rather than a side effect here.

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
- `QC7-writepath.md`
  The return direction's addressing contract, which this face uses and does not restate.
- `QD4-liveupdate.md`
  How the browser learns and what it replaces, including the three symptoms this face's unit argument explains.

## Log
260731 · `board/` tree BUILT and verified across 6 boards: build.py --split, body.site router opt-out, link interception so the drawer survives navigation, gitignored as derived (haipipe-board 0.80.0)
260731 · Opened on JL's ask for one Q describing how md renders into html and how page changes go back into md, after the file-layout and Flask discussions kept landing on faces that owned only one hop of the loop

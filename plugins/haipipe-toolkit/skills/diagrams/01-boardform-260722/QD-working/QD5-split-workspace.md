# Operating the board: index, page, and chat, each refreshing on its own

state: 🟡 PARTIAL · built 260801-02 and driven end to end in a real browser; 12 of 15 Aims ✅, A2.2 the real gap
owner: CC
method: three same-origin iframes inside one shell page, so a refresh is a frame re-fetch and no pane's reload can reach another
session: 232f5bbd-3a8c-4887-964a-778765a44c6c
## Opening
Should the board be operated as three side-by-side panes, index and page and chat, that each refresh on their own?
A board is a folder of Markdown pages you read in a browser, with a chat beside them that edits those same files for you.
Today the three are one web page, so one edit rebuilds all of it, chat included.
This page rules three panes, each its own document, so an edit refreshes the page while the terminal beside it keeps running.

**What a pane is**: One of the three regions of the shell, each loading its own document at a URL that still works on its own.
The page pane is this page's html, the index pane is the board's rail, and the chat pane is whatever you talk to Claude through, today a terminal running the CLI.
Because they are three documents rather than three parts of one, a reload of any of them cannot reach the other two.

**Where this page sits**: The QD group covers how work actually happens beside the board.
`QD3` owns the engine behind the terminal and `QD4` its form on a small screen, `QD2` owns the SDK chat drawer, and `QB2a` owns what the index shows.
This page owns the pane LAYOUT and nothing else, and it is the successor to the archived `QD4-liveupdate`, which chased the same automatic refresh by swapping the page in place.

**What three panes buy**: An edit reaches the page in under a second instead of up to four, and the index is parsed once per session instead of once per page.
The terminal is safe by construction rather than by guard code, because a reload cannot cross a frame boundary.

**What one document costs**: Four cooperating files exist only to make one page behave like three: a router that swaps the content column on a click, a poll that swaps it again on an edit, restoration code that puts back scroll and open drawers, and PTY parking so the terminal survives a hard reload.
Every one of them is repair for a problem three panes do not have.

**One constraint that is not negotiable here**: Every page a pane loads must still read with all scripts stripped, which is `QB2`'s rule.
The split is therefore an operate-time shell and never the shipped artifact.

## Diagram

**The two doors**: one address, and what a request gets depending on how it asks.

```
  …/QB4-overall.html            a browser tab   ▶  the SPLIT      three frames
                                ?plain          ▶  the old board  one document
                                ?pane=index     ▶  the page file  a frame
                                curl, fetch     ▶  the page file  Accept: */*
  ────────────────────────────────────────────────────────────────────────────
  the query says HOW to show a page, never WHICH page          QB2 still holds:
  the file a reader can strip of scripts is one GET away
```

**What the split is**: three documents in one shell, and which of them a given event can reach.

```
  ┌─ the shell · 10 KB, the only new document ─────────────────────────┐
  │  🏠  ☰ Index   >_ TUI   💬 GUI   ·  board · page  ·  ↗ plain       │
  ├──────────────┬──────────────────────────┬──────────────────────────┤
  │ index frame  │ page frame               │ chat frame               │
  │              │                          │                          │
  │ state        lazy · 0 KB   the page itself   lazy · 0 KB           │
  │ on show      34 KB          157 KB            228 KB               │
  │ refresh      itself, 800ms  itself, 800ms     never                │
  │ hidden       column 0       always shown      column 0, still LOADED│
  └──────────────┴──────────────────────────┴──────────────────────────┘
     an edit reaches ONE frame · a reload cannot cross a frame boundary
```

**Working a page into shape**: the loop the split exists for, with what each step costs.

```
  ① open it            a bare board url          157 KB · 167 ms
                       index and chat unloaded

  ② ☰ Index            the rail, to find the      34 KB ·  30 ms
                       page that RULES the shape  e.g. QB4

  ③ >_ TUI or 💬 GUI   ask for the work          228 KB ·  31 ms
                       the chat is attached to
                       the .md behind the page

  ④ it repaints        the md changes, build.py runs, the page frame
                       reloads ITSELF, ~1.5 s, and nothing else moves

  ⑤ repeat ③④         the rail keeps its scroll, the chat keeps its
                       history, you keep your place
  ────────────────────────────────────────────────────────────────────
  a NEW page starts at ③ from an empty template instead of an old page
```

**What is still one document's problem**: the guard code three frames were meant to retire.

```
  70-router.js       returns at line 1 in a pane      ✅ unreachable
  20-live-refresh    returns at line 1 in a pane      ✅ unreachable
  80-restore.js      LOAD-BEARING in a pane           ❌ A2.3 predicted
                     a real reload loses scroll          it would go
  PTY parking        still there, now dead weight     ❌ A3.2 half
  the rail's bytes   83% of every page, three copies  ❌ A2.2 open
                     when all three panes are shown
```

## Content

### C1 · What operating the board is today

```
  one request  ──▶  QD5-split-workspace.html   125,805 bytes
                      │
                      ├─ 94,942 B  nav sidebar   53 sb-out blocks, one per page
                      └─ 30,863 B  div.wrap      the page you actually came for
                                     ▲
      70-router.js ──── replaces ────┤ on every internal link click
  20-live-refresh.js ── replaces ────┘ on every change to the md
```

Every page ships `<body class="single split">`, all 53 of them, so a form of split already runs today.
It is not a split of frames.
`70-router.js` intercepts internal links, fetches the target, replaces `div.wrap`, and calls `pushState`, so navigation never becomes a real page load.
`20-live-refresh.js` does the same replacement on a different trigger, polling the page's own `Last-Modified` and swapping `div.wrap` when the Markdown moves.
The chat drawer and the terminal are appended to `<body>`, deliberately outside `div.wrap`, which is the only reason either survives a swap.
`80-restore.js` then puts back what a real reload destroys: which sections were open, keyed by summary text, plus scroll position, caret, and the drawer's own state.
That is four cooperating files whose entire job is to make one document behave like several, and it is the architecture this page proposes to replace.

This page owns the pane LAYOUT and nothing else.
The engine behind the terminal is `QD3` and its form on a small screen is `QD4`, the SDK chat drawer is `QD2`, and what the sidebar shows is `QB2a`.
One constraint arrives from `QB2` and is not negotiable here: every page a pane loads must still read with all scripts stripped.
The split is therefore an operate-time shell and never the shipped artifact.
This page is also the successor to the archived `QD4-liveupdate`, which chased the same auto-refresh behavior by swapping the page in place.

### C2 · Why a refresh is not smooth

```
  cause 1   poll 4000 ms      ──▶  you wait, and only then does it move
  cause 2   sidebar is 75%    ──▶  53 blocks re-parsed on every navigation
  cause 3   replaceWith       ──▶  the column tears out, then is patched back
  cause 4   JS stamp moved    ──▶  location.reload(), terminal open or not
                                        │
                                        ▼
                            one coupling, seen four ways

  cause 5   nothing gzipped   ──▶  every one of those bytes crosses the
            (found 260802)         forward at full price · 5 to 7 times
                                   more than it needed to be
                                   · measured and closed in C5 P3
```

#### P1. The update is a poll, so the wait is built in
(why an edit takes seconds to land, and why no amount of tuning inside the browser fixes it)
`20-live-refresh.js:184` sets `setInterval(tick, 4000)`.
Each tick sends a `HEAD` request, compares `Last-Modified`, and only then fetches the page, so a saved edit waits up to four seconds plus a round trip before anything moves.
The server already holds a live connection for the terminal, so the information is available immediately and is simply not being pushed.

#### P2. Three quarters of every page is a copy of the index
(the cost that makes each navigation heavy, measured on this page and on the largest one)
This page's built html is 125,805 bytes, of which 94,942 are the sidebar, one `sb-out` block per page on the board.
That is 75 percent of the download and the parse, and it is the same 53 blocks on all 53 pages.
On `Skill-0-haipipe-board.html` the same duplication reaches 448,347 bytes.
A persistent index pane loads that once per session instead of once per page.

#### P3. The swap is a replacement, not a diff
(why the content column visibly flickers even when only one sentence changed)
The refresh path ends in `old.replaceWith(nw)`, which throws away the entire content column and inserts a freshly parsed one.
Everything after that line is repair: open drawers restored by position, with a fallback to summary text when the drawer count changed, then scroll, then caret, then selection, then unsaved textarea drafts.
The flicker is not a rendering artifact, it is the page genuinely being rebuilt, and the restoration is what a reader perceives as the page resetting under them.

#### P4. New JavaScript is still a hard reload
(the roughest jump of the four, and the one that fires on every asset rebuild)
A CSS change hot-swaps the `<link>` and nobody notices, which is already the right behavior.
A JS change cannot be hot-swapped safely, so the code calls `location.reload()` even with a terminal open, and survives it only because the PTY is parked rather than killed and the drawer reattaches afterwards.
That machinery works, and it is still a full reload of everything in order to update one file.

#### P5. Nothing on the wire was compressed
(the cause the page did not have, added the day JL asked why opening a page takes so long)
The server answers in two to six milliseconds, so the wait is not the machine thinking; it is bytes crossing a VS Code or ssh forward at full price.
Measured 260802: a page is 172,525 bytes and gzips to 30,741, the index is 243,979 and gzips to 33,709, the largest page is 450,824 and gzips to 125,564; `board.js` and `board.css` are another 349,503 that gzip to 109,762.
Opening one page cold cost 521 KB and now costs 140 KB, and the split's first open cost 937 KB across its three documents and now costs 206 KB.
`serve.py` sends `Content-Encoding: gzip` for GET on text above 1 KB, and nothing else changed: revalidation still answers a 0-byte 304, `HEAD` is left alone because the panes poll with it and read only `Last-Modified`, and a `.md` link still opens as text rather than downloading.
This is orthogonal to `cause 2`: compression makes the repeated rail cheap to send, and `A2.2` is what stops sending it at all.

### C3 · Three frames, and why iframes won

```
  A · three iframes in one shell    same origin, so the shell can drive a pane
      RULED 260801                  serve.py gains one route, no dependency
                                    each pane's page stays byte-identical
  B · a split-pane library          smoother drag, one vendored dependency,
                                    and the panes are still one document
  C · separate browser windows      fullest isolation, loses the single
                                    surface, and QD4's phone form breaks
```

Three same-origin iframes inside one shell page is the mechanism, ruled by CC on 260801 after JL declined to arbitrate it.
It is the only option that buys the isolation this page exists for without buying anything else as well.
Same origin matters because the shell has to tell the page frame to re-fetch itself, and a cross-origin frame cannot be driven that way.
`serve.py` needs one new route for the shell and nothing more, since every pane loads a page that already exists at its own URL.
The strip-scripts invariant from `QB2` survives untouched, because a pane's page is the same static file it is today and the shell is the only new document.
Option B was rejected because a resize handle is not worth a vendored dependency, and because a split-pane layout still leaves all three panes inside one document, which is the problem rather than the fix.
Option C was rejected because separate windows break the single working surface, and `QD4` has already established that the terminal needs a form that works on a phone, where arranging a second window is not something a reader can do.

This page also supersedes the archived `QD4-liveupdate`, ruled the same day.
That page stays archived as the record of the in-place-swap approach, and the live layer belongs here, so that one page owns how the board is operated rather than two that will disagree.

### C4 · How the shell works, step by step

```
  shell.html   the only new document, served by serve.py
  ┌────────────────────────────────────────────────────────────────┐
  │  <iframe name="index"  src="board/index.html">                 │
  │  <iframe name="page"   src="board/QD/QD5-split-workspace.html">│
  │  <iframe name="chat"   src="_term/">                           │
  └────────────────────────────────────────────────────────────────┘
        │                      ▲                        │
        │ ① a plain anchor     │ ② the frame asks      │ ③ never asks,
        │   target="page"      │   about ITSELF        │   never reloads
        ▼                      │   every 800 ms        ▼
   no JavaScript at all   HEAD on its own URL        a terminal mid-command
                          changed → location.reload()  is never interrupted
```

#### P1. Navigation is a plain HTML anchor, and needs no JavaScript at all
(the step that lets the index become a pane without any router code)
Name the middle iframe `page`, then give every link in the index frame `target="page"`.
A click then loads the target into the sibling frame, which is ordinary HTML that browsers have done since before JavaScript existed.
The index frame is not reloaded, because nothing navigated it.
This is why `70-router.js` can be deleted rather than ported: it exists to fake, in JavaScript, exactly what `target` does for free.
It also satisfies `QB2`'s rule by accident rather than by effort, since a link with a `target` still works with every script stripped.

#### P2. A refresh becomes one frame reloading itself
(the step that replaces the `div.wrap` swap and everything written to repair it)
When a page's Markdown changes, that frame calls `location.reload()` on itself and nothing else does anything.
That is a real document reload, so the page is rebuilt correctly by the browser rather than surgically patched by us, and there is no `replaceWith`, no drawer-key matching, and no caret bookkeeping across panes.
The index frame and the chat frame are separate documents, so a reload of the page frame cannot reach either of them.
Scroll position inside the page frame is the one thing still worth restoring, and it is now the only thing, instead of the six-item list `80-restore.js` carries today.

#### P3. Each frame asks about itself, and the shell is not involved
(the step that turns cause 1 from a four second wait into under one, and the step this page got wrong twice)
A pane sends a `HEAD` for its OWN url every 800 ms, compares the `Last-Modified` against `document.lastModified`, and reloads itself when they differ.
The chat pane never asks, because it is the one frame whose whole value is not being interrupted.
The design ruled a server push instead, and that was built first: `serve.py` streamed the path of every rewritten page and the shell reloaded the matching frame.
It worked, and it cost more than it bought, for the reason `P6` records; a shell-side poll was tried next and failed differently, because anything that remembers what it has already told a frame to do will sooner or later remember a reload that never happened.
A frame asking about itself has neither problem: the question is one `HEAD`, the answer is its own reload, and being still stale on the next tick IS the retry.
Two things make it exact rather than nearly right: the baseline is `document.lastModified`, which is the response the frame is actually showing rather than the first answer it happens to receive, and `serve_pane` sends `Last-Modified`, which the static handler gave for free and a served pane does not.

#### P4. The chat frame is never in the blast radius
(the step that makes the terminal safe by construction, which is what A3.2 asks for)
The chat frame is its own document, and no other pane's reload can reach across a frame boundary to touch it.
The guard machinery that exists today, deferred swaps, asset-stamp reload deferral, PTY parking, and ring replay at the new width, was all written to survive a reload of the one document everything shared.
Once the panes are separate, a page refresh is not a chat event at all, so most of that machinery has nothing left to guard and can go.
PTY parking stays useful for the case it was really for, which is the reader closing the tab and coming back.

#### P5. The one real cost, named honestly
(what option A gives up, so nobody discovers it later and calls it a surprise)
An iframe's URL does not appear in the address bar, so without help the shell would always read as one address and no page could be linked or bookmarked.
It costs twice, and the second half was missed until JL opened the split and asked how he was supposed to know which board he was in: mirroring the path fixes SHARING the address, and it does nothing for READING it, because what the address bar now shows is `/_shell?p=…%2F…%2F…`, which is a path a person does not parse at a glance.
So the shell carries a 30-pixel strip of its own: 🏠 back to `/boards`, ☰ and 💬 to put the rail and the chat away, the board folder's name, the current page's title, and `↗ plain` to leave the split for that page on its own.
And the address it mirrors is the PAGE's own, plus `?split`, so the same page has one url however it is shown.
Mirroring is also refused for anything that is not a real page, because a frame that has not loaded reports `about:blank` and `/_shell?p=blank` names no board, cannot be shared, and 404s on reload.
The fix is for the shell to mirror the page frame's current path into its own query string with `history.replaceState`, and to read that query string on load so a shared link opens the shell already showing the right page.
That is roughly twenty lines and it is the only piece of JavaScript the shell genuinely needs.
Every pane still works without it, since each pane's page remains a real URL that can be opened on its own, which is exactly the fallback `QB2` requires.

#### P6. Why the push was built and then removed
(the cost the design did not predict, written down at the price it was paid)
A browser allows six connections to one origin, and a stream HOLDS one for as long as the document that opened it lives.
That budget is fine until a stream outlives its document, which is exactly what a reload does: the browser neither closes such a connection nor makes it readable to the server holding the other end, so the server cannot tell it is talking to a corpse.
Opening the split twice inside a few seconds therefore wanted seven connections in six slots, and the failure is silent by nature: the second shell's panes never loaded, its frames' `location.reload()` did nothing at all, and a queued request is indistinguishable from a slow one, so nothing anywhere reported an error.
Bounding the stream (an id per tab so a reload retires its own orphan, a 55 second life, a 3 second heartbeat) reduced it and did not remove it, because the terminal's WebSocket spends a second connection the same way.
So the push was removed and each pane now asks about itself, which holds nothing: the whole class of failure is gone rather than bounded, and the panes only ever ask about one url each.
The residue is honest and small: open a second split within a few seconds of the first and its page frame takes about ten seconds to catch its first refresh, until the previous tab's terminal socket is collected.

### C5 · Performance comparison

```
  what a reader pays, both doors, one server, one cold cache
  ────────────────────────────────────────────────────────────
  read a page      old 204 ms / 150 KB      split 137 ms / 158 KB   ▲ split
  open the chat    old +106 ms / +148 KB    split +296 ms / +199 KB ▲ old
  a pane you       nothing at all           0 KB until you show it
  cannot see
  toggle it back   nothing at all           1-3 ms, 0 requests
```

#### P1. Reading a page, which is where the time goes
The same page opened two ways is the only fair test, and `?plain` is what makes it possible, since the old board and the split are now the same file behind the same address.

```
  READING A PAGE                     time     bytes   requests
  ────────────────────────────────────────────────────────────
  old board   ?plain                204 ms   150 KB      3
  split       bare url              137 ms   158 KB      4
                                    ▲ a third faster, for 8 KB

  THEN OPENING THE CHAT ON IT
  old board   drawer + terminal    +106 ms  +148 KB     12
  split       >_ TUI               +296 ms  +199 KB     21
                                    ▲ +190 ms and +51 KB
```

Reading is where the time actually goes, and the split is the faster door by about a third: the shell paints in ten kilobytes while the page frame loads beside it, and nothing else is fetched at all, because the index and chat frames are not loaded until they are asked for.
Opening the chat is where the split pays, and it pays for exactly the property this page exists to buy: the chat pane is its OWN document, so it fetches a second copy of the page that the one-document board already had in hand.
So the trade, stated plainly, is about 190 ms and 50 KB once per page, in exchange for a chat that a page refresh cannot touch.
The old board's price for that same isolation is not zero either; it is the four cooperating files in `C1` and most of the bugs this page's Log records.

#### P2. What each pane costs the first time you show it
(the number JL asked to have recorded, because a pane is now loaded lazily and the cost moved)
Both side frames ship as `data-src` and are given a real `src` the first time they are shown, so opening a page loads ONE document.

```
  opening a page  (index and chat hidden)   167 ms   157 KB    4 requests
  ☰  first open of the index                 30 ms    34 KB    3 requests
  >_ first open of the chat                  31 ms   228 KB   27 requests
     its xterm mounted                      +69 ms
  toggling anything, once loaded            1-3 ms     0 KB    0 requests
```

Against the eager version measured the same morning, 310 ms and 563 KB for a cold split, that is 3.6 times fewer bytes to read a page.
The two costs that used to dominate every open are now paid only by someone who opens the chat: 118 KB of `xterm.min.js`, and a `claude` process that takes about 1.4 seconds to boot.
Once a frame is loaded it stays loaded, so hiding it is still only a zero-width column and a terminal mid-command survives being put away.

#### P3. Where the wire time went, before any of this was true
(the finding that made every number above worth measuring)
The server answers in two to six milliseconds, so none of the wait was ever the machine thinking; it was bytes crossing a VS Code or ssh forward, and nothing was compressed.
`xterm.min.js` alone is 477 KB and `/_board/asset/` bypassed the compression path, because that route serves VENDORED files which do not live under `--root`: the single largest thing this server hands out was the one thing going uncompressed, on every cold chat.
Compressing the static text and that route took a cold split from 1,312 KB to 563 KB and the old single page from 631 KB to 260 KB, and only then was it honest to compare the two doors at all.

#### P4. Three frames spend the connection budget three times as fast
(what the split changes about a cost that is not bytes, found the hard way on 260802)
A browser opens at most SIX connections per origin and shares them across every tab, and a request that has not finished is still holding one.
One document asking for things spends that budget once; three panes in one tab spend it three ways, and two tabs of the split can reach the ceiling on their own.

```
  per TAB, at rest              old board        split
  ────────────────────────────────────────────────────────────
  documents polling                    1             2   index + page
  a chat holding a socket              1             1   only when shown
  a page's own load requests           3             4
  ────────────────────────────────────────────────────────────
  a leak that is survivable in one document is not survivable in three
```

This is not hypothetical: `POST /_board/activity` never returned, one per pane, and the ceiling was reached with a few tabs open, which is `QD8`'s `2.3` and the reason a click sat unanswered for two minutes.
The split's two defences are both already here and both were built for other reasons: a pane you cannot see is never loaded at all, so a hidden index and a hidden chat cost no lanes, and the refresh poll backs off from 800 ms to 5 s while nothing changes, so an idle tab is not spending a lane every second.
What the split must never do is add a long-lived connection per pane; the design rule is at most one per TAB, which is why the shell's update channel is a poll on each frame rather than a stream each.

## Aims

### C1 · What operating the board is today
- A1.1 · The in-place swap stops being the board's operating model.
  **Done when:** `70-router.js` no longer replaces `div.wrap`, because navigation happens inside the page frame.

### C2 · Why a refresh is not smooth
- A2.1 · A saved edit reaches the page in well under a second.
  **Done when:** `serve.py` pushes the change over a connection it already holds and the 4000 ms interval is deleted.
- A2.2 · The index is loaded once per session, not once per page.
  **Done when:** the sidebar is its own frame and no page's html carries `sb-out` blocks for the other 52 pages.
- A2.3 · A page update repaints the page and nothing else.
  **Done when:** the restoration code in `80-restore.js` can be deleted and no reader loses scroll, caret, or an open drawer.
- A2.4 · Shipping new JavaScript no longer throws the reader out of the board.
  **Done when:** a changed JS stamp reloads only the frame that owns that file.
- A2.5 · Opening a page costs what the text costs, not what the markup costs.
  **Done when:** `serve.py` sends text compressed, and revalidation, `HEAD` and the `.md` links all still behave exactly as before.

### C3 · Three frames, and why iframes won
- A3.1 · A terminal edit to a page's Markdown refreshes the page frame on its own.
  **Done when:** the terminal writes this page's md and the page frame repaints with no pane reloaded by hand.
- A3.2 · The terminal survives a page refresh by construction, not by guard code.
  **Done when:** deferred swaps, asset-stamp deferral, and PTY parking are removed and the terminal still survives.
- A3.3 · Each pane's underlying page still reads with every script stripped.
  **Done when:** the strip-scripts assertion in `build.py` passes on the page a pane loads.

### C4 · How the shell works, step by step
- A4.1 · The shell exists and serves the three frames.
  **Done when:** `serve.py` answers one shell route and it loads the index, page, and chat frames from URLs that already work on their own.
  **Plan:** Write it as static html plus the twenty lines of address-bar mirroring, and nothing else.
- A4.2 · Navigation costs no JavaScript.
  **Done when:** the index frame's links carry `target="page"` and a click loads the page frame without any script running.
- A4.3 · A page is linkable even though it lives in a frame.
  **Done when:** the shell mirrors the page frame's path into its own query string, and opening that address opens the shell already showing that page.

### C5 · Performance comparison
- A5.1 · The split is not slower to READ than the board it replaces.
  **Done when:** the same page is measured through both doors on one server with one cold cache, and the split reaches a readable page at least as fast.
- A5.2 · A pane you cannot see costs nothing.
  **Done when:** opening a page loads one document, and the index and chat frames are fetched only the first time each is shown.

### P · Page-level
- P1 · The split is proven on one real job.
  **Done when:** the shell opens, a terminal runs inside it, that terminal edits a page, the page frame refreshes, and the terminal keeps running untouched.

## States

### C1 · What operating the board is today
- ✅ A1.1 · Inside a pane the router returns at its first line, so navigation is a real frame load and no `div.wrap` swap runs; `70-router.js` still owns navigation for a page opened on its own, which is the packaging `QB2` requires to keep working.

### C2 · Why a refresh is not smooth
- ✅ A2.1 · Each pane asks about its own url every 800 ms and reloads itself; the 4000 ms poll and its swap are unreachable in a pane. Measured under a second from this page's own bytes landing, on a fresh open. The push the Aim named was built first and then removed, for the reason C4 P6 records.
- ⬜ A2.2 · Half by behaviour, none by bytes: the index is now loaded once per session because it is its own frame, but every page still SHIPS the 53 `sb-out` blocks and the pane only stops drawing them. Deleting them is a `build.py` change that would take the rail off a page opened on its own, so it needs its own decision.
- ✅ A2.3 · Proven, and the Aim's own reasoning turned out to be half wrong. The outcome holds: `checks/splitgaps.py` G2 opens a drawer, scrolls the frame, rebuilds, and finds both back afterwards. But the Aim expected `80-restore.js` to become deletable, and a real reload genuinely loses scroll where a `div.wrap` swap did not, so that file is now LOAD-BEARING in a pane rather than removable. What went away is the drawer-key matching and the caret bookkeeping across panes, not the restore.
- 🔨 A2.4 · Unchanged: the CSS half hot-swaps, the JS half still reloads. It is no longer a reader-visible cost in the shell, because the reload it triggers is one frame's.

### C3 · Three frames, and why iframes won
- ✅ A3.1 · Verified through the write path the terminal and the drawer both use: `checks/splitgaps.py` G4 posts a comment to `/_board/comment`, and the page pane repaints with that comment visible while the chat pane's window marker survives. Finding it took fixing a real bug first, recorded in the Log: `rebuild()` pointed at a `build.py` that the 0.99.0 move had taken into `cli/`, so every write updated the Markdown and silently never rebuilt the html.
- 🔨 A3.2 · Half, and the half that is left is the one the Aim actually names. The behaviour is there: the chat frame survives every page-frame reload in the suite, and it survives because a reload cannot cross a frame boundary rather than because anything guarded it. But the Aim says done when deferred swaps, asset-stamp deferral and PTY parking are REMOVED, and all three are still in the tree. They are now dead weight in a pane rather than load-bearing, which is a different claim from gone.
- ✅ A3.3 · Asserted on the SERVED pane rather than inferred from the built file: `checks/splitgaps.py` G3 fetches all three pane kinds, strips every `<script>`, and finds ~12,000 chars of body text left in each.

### C4 · How the shell works, step by step
- ✅ A4.1 · `/_shell?p=…` serves the three frames from URLs that each work on their own, and accepts a board FOLDER as well as a page. The `⇱ Split` link on `/boards` opens it, so nobody types the route.
- ✅ A4.2 · The index frame is served with `<base target="page">` and its links carry `?pane=page`; a click loads the sibling frame with no script running in that frame at all.
- ✅ A4.3 · The shell mirrors the page frame's path into its own query string on every frame load, and `?p=` opens the shell already showing that page.

### C5 · Performance comparison
- ✅ A5.1 · Measured 260802: 204 ms and 150 KB the old way, 137 ms and 158 KB in the split. Faster by about a third, for the 8 KB the shell document costs.
- ✅ A5.2 · Both side frames ship as `data-src`; opening a page is 157 KB and 4 requests, the rail costs 34 KB when first shown, the chat 228 KB, and toggling either afterwards is 1 to 3 ms and no request at all.
- ✅ A5.3 · Lazy panes and the 800 ms to 5 s backoff hold the per-tab cost down, and `checks/pending.mjs` now fails if any pane leaves a request pending. Verified after the `/_board/activity` fix: 8 requests on a page pane, none pending, one ESTABLISHED connection from the laptop where there had been six.

### P · Page-level
- ✅ P1 · Run end to end in headless Chrome: the shell opens, a real `claude` runs in the chat pane, an edit to the md repaints the page frame, and that terminal keeps running untouched. 23 assertions in `checks/splitshell.mjs`, 21 in `checks/splitgaps.py`, and 12 unit tests in `tests/test_shell.py`.

- 260801 CC · 🔀 What is built so far, and what is not ⚠️ SUPERSEDED the same day
      Kept as the record of where the page stood that morning; every count in it is now wrong, and the States rows above are the current truth. `live/shell.py` exists, `cli/serve.py:168-174` routes `/_shell`, `/_events` and `?pane=` ahead of the static handler, and `checks/splitshell.mjs` + `tests/test_shell.py` are both on disk. Nine of twelve Aims are ✅ and P1 ran end to end.
      The decisions and the page are done; not one line of the split itself is written.
      Done today: both open decisions ruled (mechanism and supersession), the page rewritten onto the canonical shape with Content carrying the measured anatomy of the current architecture, and the four causes of the unsmooth refresh measured rather than guessed. Already existing before today and counting toward the Aims: the drawer and terminal parked outside `div.wrap`, the CSS hot-swap, `80-restore.js` making a reload lossless, the terminal surviving a reload through PTY parking, and `build.py`'s strip-scripts assertion. Not started: the shell route, the three frames, the push channel, and the removal of the router swap. Zero of twelve Aims are met, A2.4 being the only one half delivered.

- 260801 CC · 🔀 The pane mechanism is three same-origin iframes in one shell page
      Option A over B and C, recorded in C3 with the reason each loser was dropped.
      The page had carried the fork as an open decision since it opened that morning, and JL declined to arbitrate it, so CC ruled it rather than leave the page blocked. It costs one new route in `serve.py` and no dependency.

- 260801 CC · 🔀 This page supersedes the archived QD4-liveupdate
      QD4-liveupdate stays archived as the record of the in-place-swap approach, and this page owns the live layer.
      Two pages describing how the board is operated would disagree the first time either of them changed, and the archived one is the approach being replaced, so it is the one that stops being authoritative.

## Files

### Engines
- `live/base.py`
  The request floor every mixin sits on; `rebuild()` and `try_gzip()` both live here.
- `live/shell.py`
  The whole split: the `/_shell` document, the `?pane=` injection, the link carry-over, and the `/_events` stream. New on 260801.
- `cli/serve.py`
  Serves the pages, the terminal proxy at `/_term/`, and the chat endpoints; routes `/_shell`, `/_events` and `?pane=` before the static handler, because two of the three are ordinary board URLs wearing a query.
- `live/home.py`
  The `/boards` home; its cards carry the `⇱ Split` link, which is how the shell is opened without typing a route.
- `assets/js/20-live-refresh.js`
  The 4000 ms poll and the `div.wrap` swap; causes 1, 3 and 4 in C2 all live in this file.
- `assets/js/70-router.js`
  Intercepts internal links and swaps `div.wrap` instead of navigating; the split removes its reason to exist.
- `cli/build.py`
  Generates the per-page static html a pane loads, and asserts the strip-scripts invariant A3.3 depends on.

### Checks
- `checks/splitshell.mjs`
  The split driven in a real browser against the family's own board: three frames, a click that moves one, the address bar, a rebuild that repaints one frame, and the chat frame surviving it. 23 assertions.
- `checks/splitgaps.py` · `checks/splitgaps.mjs`
  What that suite leaves untested, on a throwaway fixture because these WRITE: the ordinary page's regression, scroll and section survival, strip-scripts on the served pane, and a real comment repainting the pane. 21 assertions, own server, own Chrome.
- `tests/test_shell.py`
  Pane recognition, index resolution, link carry-over, and the served shell document. 11 tests, no browser.

### Output files
- `board/QD/QD5-split-workspace.html`
  Generated, do not hand-edit; the 125,805 bytes measured in C1 and C2 are this file.

## Glossary
chat: the third pane, meaning whatever you talk to Claude through. It is the SDK chat box of `QD2` or the CLI running inside the terminal of `QD3`, and this page treats them as one pane because a reader does not care which is behind it (JL 260801: the terminal is just our chat).
pane: one of the three regions of the operating shell, each loading its own document, so refreshing one cannot disturb another.

## Log
260802 CC · Recorded `C5 P4`: three panes spend the browser's six-connection budget three times as fast, and `POST /_board/activity` never returning is what proved it. Two tabs of the split reached the ceiling and a click then had no lane to travel on, which is `QD8`'s `2.3`. The split's two defences already existed for other reasons, lazy panes and the 800 ms to 5 s poll backoff, and the design rule they imply is now written down: at most ONE long-lived connection per tab, never one per pane
260802 · Ran `/haipipe-board-page` on this page and worked the checker's list before touching prose: 24 findings to 0. The one ERROR was the `state:` line, which opened with a bare 🟢 where the grammar wants one of ✅ SETTLED · 🟡 PARTIAL · 🔴 OPEN · ⏸ ON HOLD, so it now reads 🟡 PARTIAL. The other 23 were em-dashes, every one of them in Log lines I wrote today, and each was repaired on its own terms rather than swept: a colon where the clause explains, parentheses where it is an aside, a full stop where it was really two sentences
260802 · REBUILT THE DIAGRAM SECTION to the page contract and to what actually exists. It carried two figures, neither captioned, and the first was still labelled PROPOSED and still claimed the guard code was deleted, which is not true and is exactly what A3.2 says. Four captioned figures now: the two doors (one address, four ways to ask), what the split IS with each frame's real state and byte cost, the working loop with what every step costs, and a fourth that names what three frames have NOT retired. `80-restore.js` turned out to be load-bearing rather than deletable, PTY parking is still there, and the rail's 83% is still shipped three times over, so the page says so in a figure instead of leaving it to a State row
260802 · Gave the numbers their own division, `C5 · Performance comparison`, with the Aims and States rows the shape requires (JL: "update the Content with the division of Performance Comparison"). It carries three things that had been scattered: P1 the two doors measured against each other, P2 what each pane costs the first time it is shown, P3 where the wire time went before any of it was worth measuring. `A5.1` asks that the split not be slower to READ than the board it replaces and `A5.2` that a pane you cannot see cost nothing; both are ✅ with the measurement beside them
260802 · Measured the split AGAINST the old board, which is the comparison JL actually asked for and which `?plain` finally makes possible: the same file, the same server, one cold cache, one criterion. Reading a page is 204 ms / 150 KB the old way and 137 ms / 158 KB in the split: a third faster for 8 KB, because the shell paints in ten kilobytes while the page frame loads beside it and nothing else is fetched. Opening the chat is 106 ms / 148 KB the old way and 296 ms / 199 KB in the split, and that is the split paying for the thing it exists for: the chat pane is its own document, so it fetches a second copy of the page the old board already had. Recorded as C2 P4b
260802 · ⚠️ REPAIRED MY OWN DAMAGE: the `#### P5` block had been pasted THREE times, once correctly in Content and twice into the middle of Aims and States, because the replacement I anchored it on, the `### C3` heading, occurs in all three sections. Two copies removed. A section heading is not a unique anchor on a page whose Aims and States repeat the Content headings by design, which is the shape `QB4` rules
260802 · A PANE YOU CANNOT SEE IS NO LONGER PAID FOR (JL: "could you by default to hide the index and chat? and could you record the timing of opening them as well?"). Both side frames now ship as `data-src` and are given a real `src` the first time they are shown, so opening a page loads ONE document. Measured cold, gzip on, on the family's own board:

      opening a page (index and chat hidden)   167 ms   157 KB    4 requests
      ☰ first open of the index                 30 ms    34 KB    3 requests
      >_ first open of the chat                 31 ms   228 KB   27 requests
         its xterm mounted                     +69 ms
      toggling anything, once loaded           1-3 ms     0 KB    0 requests

  Against the eager version measured earlier the same day, 310 ms and 563 KB for a cold split, that is 3.6× fewer bytes to read a page, and the two costs that dominated (118 KB of xterm, and a `claude` process that takes ~1.4 s to boot) are now paid only by someone who opens the chat. Once a frame is loaded it STAYS loaded, so hiding remains a zero-width column and a terminal mid-command still survives being put away
260802 · Added the second `## Diagram`: how a page is actually worked into shape in the split: open it, ☰ the rail to see the page that RULES the shape, ask the chat to conform this one, watch the middle frame repaint, repeat. A new page starts the same way from an empty template. The first diagram says what the split IS; this one says what it is FOR, which is the question JL asked and the page could not answer
260802 · THE SPLIT IS THE DEFAULT (JL: "could you make the ?split to be default and make ?plain to be the old version?"). Opening any board page in a browser now gives the three panes; `?plain` gives the one document it always was, and `↗ plain` in the strip is that link. The test is what the request ASKS FOR: `?pane=` or `?plain` are answered with the file, `Accept: text/html` means a tab is navigating and gets the shell, and everything programmatic (`70-router.js`, `20-live-refresh.js`, curl, a scraper) sends `*/*` and still receives the page. QB2 survives on that last line: the page a reader can open and read with scripts stripped is still one GET away, and is what every non-browser gets by default
260802 · `Sec-Fetch-Dest: document` was the obvious test and it is useless here, which cost a round of "the change did nothing": browsers send the `Sec-Fetch-*` headers only to a TRUSTWORTHY origin, https or localhost, and this board is plain http on a tailnet address, so they never arrive. Chrome's own request headers over that origin are `Upgrade-Insecure-Requests` and `User-Agent`, nothing else. The header is still believed when it IS present, so an iframe that announces itself is never mistaken for a tab
260802 · The narrow layout was broken and JL hit it by making the window smaller: one pane filling the top and white below. `#split.hi` and `#split.hc` are id+class, so they outranked the bare `#split` inside the media query and the column layout survived into a phone-width screen. Below 820px the same five children are now rows (index, gutter, page, gutter, chat) with every hidden-state selector repeated at the same specificity, and the drag handles follow the axis the grid is actually on
260802 · THE PANE REFRESH IS NANOSECONDS NOW, not whole seconds. `Last-Modified` has one-second resolution, so a rebuild landing in the SAME second as a pane was served left the two timestamps identical and that frame sat stale believing it was current. Narrow, and this board is rebuilt in bursts, so it was hit. `serve_pane` sends an `ETag` of the file's `st_mtime_ns` and injects the same string as `window.__paneStamp`; the poll compares tags and falls back to the timestamp. `do_HEAD` gained a pane route that answers from a `stat` alone, because three panes ask every 800 ms and none of them wants the page built
260802 · Measured what a refresh actually costs, since the number matters more than the mechanism: a pane on its own repaints 250 ms after a rebuild; a pane in the FIRST shell of a tab, 1,562 ms from the build starting, which is ~200 ms after it finishes. A pane in a LATER shell of the same tab takes 14 to 28 seconds, and that is C4 P6's residue rather than the refresh: the shell it replaced still holds a terminal socket out of the browser's six per origin. `checks/splitshell.mjs` T5 is the later case by construction, so it now asserts the ISOLATION (chat frame untouched, same page still shown) and PRINTS the time instead of bounding it; the latency claim lives in `checks/splitgaps.py` G2, which runs one shell on a fixture with no terminal. Widening a bound until it passed would have turned a real named cost into a number nobody trusts
260802 · SWITCHING TUI/GUI IS SMOOTH ONE WAY AND HONEST THE OTHER, filmed frame by frame after JL said the clicking is not smooth and asked me to open Chrome and look. To the GUI the click used to `await` the session hand-back before flipping the panel, so the pane showed the OLD view for a round trip of 284 ms with nothing happening, which is exactly what reads as sticky. The view flips first now and the release runs behind it: 9 ms. To the TUI it stays ~309 ms and should: nothing can be drawn until the server names the PTY and the ring replays, and the terminal arrives fully painted rather than as an empty black box
260802 · Two things that fix broke, both found by filming rather than reasoning. Revealing the terminal panel BEFORE the open (to make that direction feel instant too) left a black empty pane whenever the open then failed, which is worse than the wait it saved, reverted the same minute. And a release nobody awaits is a release the next open can overtake: switch away and straight back, and the park landed on the terminal that had just been attached, so the pane stayed empty. `termOpen` now waits for any hand-back in flight, bounded to one second, because a hang there must never be able to stop a terminal from opening
260802 · An hour of "the terminal will not open" was my own test profile, not the code: clicking to the GUI persists `board-tui-default=0`, so every later load in that Chrome opened in the chat box and my film's wait for `xterm-rows` never came. A fresh profile opened the terminal first try. Worth writing down because the same thing will read as a bug to anyone whose browser remembers the GUI
260802 · The rejoin probe went quiet (JL: "why it is always indicating the rejoining? what is it about?"). The sync heartbeat asks the server whether a turn is running with nobody watching, which is a real case, since the transcript is only written when a turn ENDS. It painted "Rejoining" before it had an answer, and the watchdog then escalated a probe that found nothing into "no reply for 60s, ⏹ to stop" and a diagnostics button. The label now waits for the first real event and a silent probe gives up in 6 s instead of 7 minutes; a rejoin that finds a live turn is unchanged
260802 · MEASURED THE SPLIT IN A REAL BROWSER, cold cache, because JL asked twice why it takes a while and I had been answering from arithmetic. On the server the split is not slow: shell 67 ms, index pane 49, page pane 25 (you can read from here), chat document 2, drawer 1, TUI terminal painted 166: about 310 ms end to end against 227 ms for the old single page. Switching is 82 ms to the GUI box and 84 ms back to a painted terminal; hiding either pane is 1 ms because it is a column, not a load. What JL feels is the WIRE, and the measurement found the reason: `xterm.min.js` is 477 KB and `/_board/asset/` bypasses `try_gzip`, because that route serves VENDORED files which do not live under `--root`, so the single largest thing this server hands out was the one thing crossing the forward uncompressed, on every cold chat. Compressing it there took the cold split from 1,312 KB to 563 KB and the old single page from 631 KB to 260 KB. The split is still about twice the page because three documents each carry the rail, which is A2.2 and still open
260802 · The chat's footer reads Sessions · Quick actions · Settings (JL). Widest scope first: which conversation, then what to say in it, then how it is configured, with Settings last because it is touched least. This is the shared drawer, so the one-document board gets the same order
260802 · THE CHAT IS TWO BUTTONS, and it is JL's design (having tried mine twice): "how about that when we just have two button, like TUI-Chat or GUI-Chat? when either of them is not toggled, we hide the chat channel". `>_ TUI` and `💬 GUI` are one radio with an off position: the lit one is the mode you are in, the other switches, the lit one puts the pane away, neither lit means no chat on screen. It is better than what it replaced for a reason worth keeping: which chat you want and whether you want one are the SAME question, so they are the same control, and the state is readable without clicking anything. My two attempts both put a door in front of it: a `<select>` inside the pane header (so you had to open the chat to change the chat), then a popup at a `💬 Chat ▾` button (so the state was invisible until you clicked, and there was something to dismiss)
260802 · The shell wore its own dark chrome and read as three windows in a black frame (JL: "I don't want the black boundary for the three split... make it the same style like the old version"). It now declares the board's own palette variables, values and dark query copied, and the gutter is a 1px `--line` hairline with a 5px grab area rather than a dark bar; the rail and the drawer draw their own edges again, which is exactly how the one-document board separates the same three regions. A shell is a separate document and cannot inherit the board's CSS, so matching it means copying the six variables that matter
260802 · ⚠️ RE-ADDED. The six entries below this one were written during the session and were gone an hour later: another session rewrote this page and its copy did not have them. Nothing was merged and nothing warned, and the later write simply won. QD1's one-window Law covers a SESSION per page; this is the same hazard one level up, a page with two writers, and the QD2 handover on 260801 had already said so ("which is its own argument for one writer per page")
260802 · The chat pane's mode is a NAMED CHOICE, not a flipping glyph (JL: "could we have drop list, to choose the TUI-chat or GUI-Chat", then "what is a good symbol for the GUI? ← is not good. >_ is good for TUI"). `←` named the ACTION and never the destination, so the control could only say what it would do next, never where you were. The list shows both and marks the current one: `>_ TUI` and `💬 GUI`. The drawer's own `.term` button still performs the switch and the list clicks it, because handing a session back and forth is QD1's Law and should keep one implementation. Scoped to `body.pane-chat`, so the one-document board is untouched
260802 · A Python string is not a JS string, twice in five minutes. The chat pane answered 000, nothing at all, and the frame came back as an opaque cross-origin error page, because the list's 💬 was written as a surrogate-pair escape in `live/shell.py`: Python resolved it before any browser saw it, leaving two lone surrogates that utf-8 refuses to encode. Then the fix's own comment, quoting that escape, broke the module at import. One lesson, now a comment in the file: write the literal character, and the html block is an `r"""` string so the regexes inside it stay regexes
260802 · `/boards` TOOK 95 SECONDS, which is why JL could not open it, and I first read his report as a network problem. `render_home()` used `rglob("board.md")` and applied its skip list to the RESULTS, so it walked 366,951 entries (`.venv`, `node_modules`, `.git`, `_WorkSpace`, every generated `board/` tree) to find ten files. Warm 2.7 s, cold 95 s. Pruning the directories in place during the walk leaves 11,670 entries and 0.12 s, measured three times running
260802 · ONE URL PER PAGE (JL: "why they don't share the same URL? It is very weird"). It was weird: the split lived at `/_shell?p=<escaped path>` while the page lived at its own address, so one page had two names. The path is now the page and the QUERY says how to show it: nothing, `?split`, or `?pane=…` for a frame inside the split. `/_shell?p=` still answers
260802 · The split carries the old board's two gestures (JL: "with chat icon and index icon, when we open it, it will show, we close it, it will hide"): `☰ Index` and `💬 Chat` in the strip, each remembered per machine. Hiding is a zero-width COLUMN and never an unloaded frame, so a terminal mid-command survives being put away. Labelled rather than bare glyphs, and a floating pill was considered and dropped: a toggle can never hide itself the way the old fab did once the drawer opened, so it would have covered the prose permanently
260802 · Two defects JL found in a minute of use, both inside what C4 P5 called the shell's one real cost. `/_shell?p=blank`: `mirror()` wrote whatever the page frame reported, and an unloaded frame reports `about:blank`, whose pathname is the word `blank`, an address naming no board, unshareable, 404 on reload. And the better question, "how do we know which board it is???": the address bar shows the SHELL, so three frames had nothing on screen naming the board. Hence the 30-pixel strip
260802 · The URL to hand over is the TAILNET one (JL: "It is not 127, it should be our tailscale IP"). Claude runs on the Studio and JL reads from a laptop, so `127.0.0.1` is Claude's own view and opens nothing on his side
260802 · Rewrote the Opening to `QB4` §1 (JL). Two defects, both of them the ones QB4 names by example: the blank line sat directly under the question, so a reader on stage saw ONLY the question while the four sentences explaining it were hidden in `More details` (QB4 §1.1.2, "a single bare question while the five sentences that explained it sat unread below"), and that drawer was one block of prose with no labels to scan (QB4 §1.3.1). The visible paragraph is now question + words + why it is hard + what the page rules, 4 sentences and 435 characters against the ~450 ceiling, and the drawer is five bold-labelled parts carrying the bearing `QB4` §1.2.2 asks for, which the page had never had. 24 of the board's 45 pages share the blank-line defect and are untouched here
260802 · Closed the testing gaps JL asked for, and the first thing they found was not in the split at all: `live/base.py`'s `rebuild()` still pointed at `HERE / "build.py"`, which the 0.99.0 move had taken into `cli/`, so EVERY write through the server (comment, sentence edit, resolve, chat, terminal) updated the Markdown and then silently failed to rebuild the html, returning 200 with the error text in a field nobody reads. `checks/run.py` carried the same two stale paths. Both fixed; G4 goes green only because of it
260802 · Added `checks/splitgaps.py` + `splitgaps.mjs`, 21 assertions on a throwaway fixture board with its own server and Chrome, because they WRITE: G1 an ordinary page is unchanged (the router still swaps, live-refresh still lands in place, neither reloads): that is the regression surface of this whole session and it was untested; G2 scroll and open sections survive a pane refresh; G3 all three pane kinds still read with every script stripped; G4 a comment posted to `/_board/comment` repaints the page pane, shows up in it, and leaves the chat pane alone. 21/21
260802 · Recorded against A2.3 that the Aim's reasoning was half wrong: a real reload DOES lose scroll where the swap did not, so `80-restore.js` is load-bearing in a pane rather than deletable. The outcome the Aim wanted still holds and is now proven; the route to it is not the one the Aim predicted
260802 · Corrected A3.2 from ✅ down to 🟡 on rereading its own done-when: the Aim says the guard code is REMOVED, and deferred swaps, asset-stamp deferral and PTY parking are all still in the tree. The behaviour it describes is real and the removal is not, and those are two different claims
260802 · Answered the QD2 handover below by rewriting what it flagged, and the answer moved again while it was being written: the shell-side poll it describes is gone too. THE REFRESH NOW BELONGS TO EACH PANE: a `HEAD` on its own url every 800 ms against `document.lastModified`, the chat pane never asking, so the shell holds no connection and remembers nothing. Three mechanisms in one day, each removed by the cost of the last: a held stream (spends one of six connections, wedges the second open), a shell-side poll (remembers what it told a frame, so a dropped reload is never retried), and this. C4 P3 and P6 now tell that story, and `live/shell.py` is 4 routes with no stream in it
260802 · Two engine fixes the split needed and nothing else would have found: `serve_pane` now sends `Last-Modified` (the static handler gave it for free, a served pane did not, so a pane's `HEAD` had nothing to compare and never refreshed), and the refresh baseline is `document.lastModified` rather than the first answer received (an edit landing between a frame's load and its first tick was otherwise adopted as current, leaving that frame stale forever while believing it was fresh)
260802 · Built the split and drove it: `live/shell.py` (4 routes), the `⇱ Split` link on `/boards`, `?pane=` injection with link carry-over, `checks/splitshell.mjs` (23 assertions, green twice from a fresh browser) and `tests/test_shell.py` (11). Verified in headless Chrome with a real `claude` running in the chat pane: a rail click moves only the page frame, a rebuild repaints only the page frame, and the terminal keeps running. A1.1, A2.1, A2.3, A3.1-3.3, A4.1-4.3 and P1 are met; A2.2 is met by behaviour and not by bytes, since a page still SHIPS the 53 `sb-out` blocks and the pane only stops drawing them
260801 · HANDOVER from `QD2`, left as a Log line rather than as edits to Content, because this page has an owner and had a live session while the reading was done. Three places describe an architecture that `live/shell.py` says was built, measured and REMOVED. C4 P3 says "/_events streams server-sent events"; the route is `GET /_events?poll=1&p=…`, it answers a JSON map of every `.html` mtime under `board/`, and the shell diffs it on `setInterval(poll, 400)`. C4 P6 says the six-connection cost was BOUNDED by a per-tab stream id, a 55s self-termination and a 3s heartbeat; none of those three exists, and the module's docstring says the cost is what "ruled it back out": the stream was deleted, not bounded. A2.1's State inherits the same wording. `grep -rn "EventSource|event-stream" live/ cli/` finds nothing but one stale comment at `assets/js/20-live-refresh.js:185`. Worth saying plainly: the real story is better than the documented one, since a design that got built, cost something measurable, and was reversed is the most useful thing on this page and is currently the part that is mis-told. Also read and NOT filed as a defect: `PANE_BOOT` was keyed `_bisect`, so the chat pane's drawer-reopen never injected; another session fixed it to `chat` at 23:52 while this was being written, which is its own argument for one writer per page
260801 · Header corrected from "nothing built yet" to built, because the page had been contradicting itself since the split landed: the `state:` line and the morning's 🔀 record both said zero of twelve, while the States rows directly above them carried nine ✅ with named evidence. Checked on disk rather than trusted: `live/shell.py` exists, `cli/serve.py:168-174` routes `/_shell`, `/_events` and `?pane=` ahead of the static handler, and both `checks/splitshell.mjs` and `tests/test_shell.py` are there. The morning's record is kept and marked SUPERSEDED rather than deleted, since it is the honest record of where the page stood when it was written. Noticed while reading this page for `QD2`, which is the case for reading a sibling end to end instead of its header
260801 · Repointed `## Files` at the paths that exist: haipipe-board 0.99.0 moved the runnable scripts into `cli/` the same day, so `serve.py` and `build.py` became `cli/serve.py` and `cli/build.py`; the two `assets/js` entries were already right
260801 · Corrected the count in the 🔀 States record from nine Aims to twelve, because C4 added A4.1 to A4.3 after that record was written; still zero met, with A2.4 the one half
260801 · Re-verified the four measured claims in C2 against the live files rather than the page: `20-live-refresh.js:184` still `setInterval(tick, 4000)`, `70-router.js:40` still `old.replaceWith(nw)`, `cli/serve.py` has no shell route and no `/_events`, and every URL a pane would load already answers on its own
260801 · Added C4, the step-by-step mechanism JL asked for: how `target="page"` replaces the router with no JavaScript, how a refresh becomes one frame reloading itself, how an SSE endpoint on `serve.py` replaces the 4000 ms poll, why the chat frame is out of the blast radius by construction, and the one real cost, which is that an iframe has no address bar and the shell must mirror the path itself; three new Aims A4.1 to A4.3 carry it
260801 · Recorded what is built so far in States: corrected A3.1 from ✅ to ⬜ because ruling the mechanism is not the same as meeting the Aim, marked A2.4 🟡 since the CSS half of it already ships, and gave every other row the fact that already counts toward it rather than a bare "not started"
260801 · Added `--no-url` to `status.py` so a chat reply carries the board and page label without a raw address (JL); the closing block itself is `QD6`, so the rule belongs there and only the flag was written here
260801 · Renamed the third pane from terminal to chat, in the title, the Opening and the Diagram, after JL pointed out that the terminal IS the chat from a reader's side; the word terminal stays only where the text means the actual PTY, and the Glossary now records the difference
260801 · Retitled again after JL read the title cold and could not follow it: "Three panes, not one document" was a slogan naming no subject, so it became "Operating the board: index, page, and terminal, each refreshing on its own", which is the house shape every sibling uses, a thing followed by its payoff
260801 · Rewrote the Opening after JL read it and could not tell what the page was about: the lead said "frames" without saying what one is, the paragraph then counted four things where the question had said three, and it never said what a board is or what operating one means
260801 · Rewrote the page onto the canonical shape: retitled from "Operate the board as a split, not drawers on one page", deleted the Boundary section per JL 260731, converted Items to Finish and Where we are into Aims and States, and added Content carrying the measured anatomy of the current architecture
260801 · Repaired the ASCII that the QD13 to QD5 renumber broke, where substituting QD4-liveupdate for QD4 inside the code block pushed three lines out of alignment and left an em-dash behind
260801 · Ruled the two open decisions rather than holding them: mechanism A (three iframes in one shell), and supersession A (this page owns the live layer)
260801 · Opened from JL: make terminal edits to a page's md refresh the webpage automatically, by making QD a SPLIT (index · page · terminal panes) rather than widgets bolted to one html; named as the successor to the archived QD4-liveupdate page's in-place-swap approach

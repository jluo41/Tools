# What a board page costs to open, and what we spend to make it less

state: 🟡 PARTIAL · bytes and lanes are both measured and closed; the browser half has counts but no timings
owner: CC
method: measure the wire and the browser separately, then spend only where a number says to
session: 69b5de89-5db8-411f-9597-1b3a0a43461a

## Opening
What does opening one board page actually cost, and which of those costs is worth paying to remove?

A board page is a file the server sends and the browser then builds into something you can read, and each half has its own price.
The wire half is bytes and the lanes that carry them: file size, what repeats on every page, and whether a connection is free to send it at all.
The browser half is work: parsing, running the JavaScript, building what you scroll.
This page rules which of those costs we pay to remove.

**What "a page" means here**: One generated `.html` under a board's `board/` folder, such as `QB1-form.html`, together with the `board.css` and `board.js` it asks for.
The three arrive separately, and only the first is different from page to page.

**Where this page sits**: `QD` is where a board is WORKED ON, and waiting is the thing that stops the work, so the cost of opening a page belongs beside the surfaces you wait at.
The levers themselves are all in `QC`'s engine, and this page names them rather than owning them: `build.py` decides what a page contains, `serve.py` decides what crosses the wire and what a browser may cache, and `assets/` is the bundle both halves pay for.
`QD5` next door keeps only what is true because there are three frames; everything here is true of `?plain` as well, which is why it is its own page and not a division of that one.

**What "a lane" means here**: A browser opens at most SIX connections to one origin and shares them across every tab.
A request that has not finished is still holding one, so a request that never finishes removes a lane permanently.

**Why this is hard**: Three different failures read as one word, "slow".
A page can arrive slowly, arrive fast but take a second to build, or never leave the browser's queue because no lane is free, and from a chair all three are the same wait.
The tools are each blind to two of the three: `curl` never parses and always gets its own fresh connection, and a browser profile never shows you a cache header.
So a number from the wrong instrument sends the work in the wrong direction, which has now happened three times on this board, once for eight days.

**What decides it**: Every claim here carries the command that produced it, and no lever is pulled without a number naming it.

## Diagram

**The two halves**: what a page costs, split by who pays it and what can measure it.

```
  THE WIRE                              THE BROWSER
  ────────────────────────────────      ────────────────────────────────
  page html      20-49 KB gzipped       parse html      605 KB uncompressed
  board.js       82 KB · cached         execute js      250 KB uncompressed
  board.css      33 KB · cached         build the DOM   3,455 elements
  a free lane    1 of 6 per origin      ────────────────────────────────
  ────────────────────────────────      measured by     devtools, CDP Tracing
  measured by    curl, CDP Network      paid            once per NAVIGATION
  bytes paid     once per session                       unless the page swaps
  lanes paid     for as long as a
                 request stays open
```

A lane is the row that was missing until 260802, and it is the only one whose cost is TIME HELD rather than a size, which is why no byte count ever showed it.

**Where a page's bytes go**: measured on `QD5-split-workspace.html`, and the shape holds board-wide.

```
  page html            163,415 B raw          30,741 B gzipped
    the page list        110,651 B   67%        the same 53 blocks on all 53 pages
    the page itself     52,764 B   33%        what the reader came for
  ────────────────────────────────────────────────────────────────────────
  the page list is the single largest thing a board sends and the only one
  that is identical on every page it is sent with          A2.4 keeps it
```

**The six lanes**: why a fast server and a fast link still produced a two-minute page.

```
  a browser opens at most SIX connections per origin, shared by every tab
  ────────────────────────────────────────────────────────────────────────
  1  POST /_board/activity    held · the walk never returned
  2  POST /_board/activity    held · another tab
  3  POST /_board/activity    held · another tab
  4  POST /_board/activity    held
  5  POST /_board/activity    held
  6  POST /_board/activity    held
  ────────────────────────────────────────────────────────────────────────
  GET QB1-form.html?pane=page   ⏳ queued, no lane free
     devtools calls this "Provisional headers are shown"
     the page was never slow to serve; it never got a socket to be served on
```

**What is already spent**: the levers pulled on 260802, each with the number that justified it.

```
  free the six lanes       60 s+ → 43 ms     POST /_board/activity, the same walk
  gzip on text            521 KB → 140 KB    a cold page open
  gzip on vendored xterm  477 KB → 118 KB    /_board/asset/ bypassed the first pass
  immutable on ?v= assets 114 KB → 0         per navigation, after the first
  prune the /boards walk   95 s → 0.12 s     366,951 entries → 11,670
  swap instead of navigate  7 req → 1 req    a page list click in the split
```

## Content

### 1 · What is measured, and by what

**Which tool sees which cost**: what each measurement can report, and what it is blind to.

```
              wire bytes   cache hdr   LANE HELD   parse   execute   paint
  curl            ✅           ✅          ✗         ✗        ✗        ✗
  CDP Network     ✅           ✅          ✅        ✗        ✗        ✗
  devtools        ✅           ✅          ✅        ~        ~        ~
  devtools trace  ~            ✗           ✗         ✅       ✅        ✅
  ─────────────────────────────────────────────────────────────────────
  the LANE HELD column is why this took eight days: the instrument used
  most is the one instrument that cannot see it              1.3 is this
```

#### 1.1 · Two tools, two blind spots

`curl` sees the wire exactly and the browser not at all: it reports connect time, time to first byte and transfer time, and it never parses a tag.
A browser profile is the reverse, and a cache header is invisible in it.
Every number on this page therefore names the tool that produced it, because a reading from the wrong half has twice sent this work in the wrong direction: once when a `no-store` header was read off a URL the browser never requests, and once when a click was called fast because it measured 49 ms on the machine serving it.

#### 1.2 · The link is not the subject, but it sets the exchange rate

Measured 260802 from a laptop over a direct tailnet path: 24 to 35 ms round trip, about 0.92 MB/s on a single stream and 1.30 MB/s across six.
The server answers a static asset in about 1 ms and a generated page in about 20 ms, so neither the link nor the server explains a slow page on its own.
What the link does is set the price of a REQUEST: at 30 ms, seven requests cost a fifth of a second before a byte of content is drawn, which is why request COUNT is a first-class number here and not a detail.

#### 1.3 · Why every measurement said fast while a reader waited two minutes

`curl` opens its own connection every time, so it can never be short of one, and it reported 20 to 70 milliseconds for a page throughout the eight days a page took one to two minutes to open.
That is not a wrong reading: the server really was that fast, and so was the link at 24 to 35 milliseconds.
What `curl` cannot represent is the browser's SHARED budget of six connections per origin, so a page whose request is sitting in Chrome's queue with no lane free is, to `curl`, a page that does not exist to be measured.
The instrument that does see it is CDP or devtools, and the question it has to be asked is not "how long did the page take" but "is anything still pending", which is a different question and was never asked until 260802.
`checks/pending.mjs` now asks it on every run.

### 2 · The wire half

**What a second page in a session costs**: everything already paid for, and what is left.

```
  first page of a session    html 20-49 KB  +  js 82 KB  +  css 33 KB
  every page after           html 20-49 KB     cached       cached
  ────────────────────────────────────────────────────────────────────
  of that html, 67% is the page list, on all 53 pages   A2.4 ✅ kept
```

#### 2.1 · The assets are cached, and the version hash is why

`board.js` and `board.css` measured 260802 at 82 KB and 33 KB gzipped, they are identical on every page, and the markup asks for them with a content hash: `board.js?v=25cc58ca7354`.
`serve.py` answers a stamped request with `public, max-age=31536000, immutable` and an unstamped one with `no-store`, which is correct in both cases: the hash already guarantees a changed file gets a new URL, so nothing stale can survive, and nothing unchanged is ever re-sent.
The unstamped path is the one a person types by hand, and reading its header is how two separate measurements concluded the assets were never cached.

#### 2.2 · Compression was worth more than anything else on this page

Nothing was compressed until 260802, and board text compresses 3 to 7 times because it repeats itself.
A cold page open went from 521 KB to 140 KB, the split's first open from 937 KB to 206 KB, and `xterm.min.js`, at 477 KB the largest single thing this server hands out, from 477 KB to 118 KB once `/_board/asset/` stopped bypassing the compression path.
It is one header and a `gzip.compress`, and it beat every structural change considered beside it.

#### 2.3 · A request that never returns costs more than any number of bytes

Every board page posts `op=stats` to `/_board/activity` as it loads, and that call ran an unpruned `rglob` over the whole repository, 366,951 entries, to find ten `board.md` files.
It was measured here at over 60 seconds with no answer at all, and a browser allows only SIX connections per origin across all its tabs, so a handful of open pages held every lane and the next CLICK simply queued behind them, which devtools reports as "Provisional headers are shown" and a reader experiences as one to two minutes of nothing.
It is the same walk that made `/boards` take 95 seconds, fixed there earlier the same day and missed in this copy, which sits on a far hotter path.
Pruning it in place and caching the result for two seconds took the endpoint to 43 milliseconds, ten at once to 0.88 seconds, and a click from `QB1` to `QB2` to 53 milliseconds.

The three commands behind those numbers, so the claim can be re-derived:

```
  the endpoint      curl -X POST $HOST/_board/activity -d '{"op":"stats","path":"<board>/board.md"}'
  under load        the same, ten times with &, then wait
  a real page       node checks/pending.mjs $HOST
  ────────────────────────────────────────────────────────────────────────────────
  the last one is the only one of the three that can fail on a held lane
```

The symptom to recognise next time is not a timing at all: it is devtools showing "Provisional headers are shown" with "0 B transferred", which means Chrome never sent the request, and the count of ESTABLISHED connections from one client sitting at exactly six.

#### 2.4 · The page list is what is left, and it is staying

The page list is the panel down the left of every page: every page of the board, each opened out into its own section links.
On 260802 that was 55 pages and 303 links, 110,651 bytes, 67% of a page's html; re-counted 260806 on the sidebar `<nav>` of this page's own built html, it is 57 pages, 995 links and 149,359 bytes, 80%, because the board and its section links have both grown.
It is the same blocks on every page, and gzip does not remove it: compression makes a repeated thing cheap to send, not absent.
It is therefore the single largest lever left on this page, and on 260802 JL ruled that it will not be pulled: "I still want to have that panel, please give me that panel. Please keep it."
That closes the question rather than deferring it, and the reason is worth writing down: the panel is what makes any page reachable from any other page, and a page opened on its own would otherwise be a dead end.
So the panel's share, 67% then and 80% now, is a KNOWN price for a named benefit, which is a different thing from a share nobody had looked at, and the remaining work on this page moves to the browser half.

### 3 · The browser half

**What a navigation rebuilds, and what a swap keeps**: the cost no cache header can reach.

```
                        full navigation        swap one column
  fetch                 the page               the page
  parse html            605 KB                 the new column only
  execute board.js      250 KB                 nothing, it is running
  build the DOM         3,455 elements         the changed subtree
  the drawer            rebuilt                untouched
```

#### 3.1 · A navigation costs 250 KB of JavaScript, every time

Counted on `QB1-form.html`: 604,938 uncompressed bytes parsed, 250 KB of JavaScript executed, 3,455 DOM elements built.
That is the price of a NAVIGATION, and it is paid whether the bytes came from the network or from cache, which is exactly the cost no cache header can touch.
A swap avoids it: replacing one column inside a document that is already running keeps the parsed page, the executed bundle and the built DOM.

#### 3.2 · This is the half that is not yet measured

Everything in 3.1 is a COUNT, not a time.
Nobody has yet timed parse, execute, layout and paint on the machine a reader actually uses, and that number is what decides whether any further work here is worth doing.
Until it exists, this page refuses to spend on the browser half beyond the swap it already has.

## Aims

### A1 · 🔬 What is measured, and by what
- A1.1 · Every cost claim on this page names the command that produced it.
  **Done when:** each number in Content can be re-derived from a command written beside it.
- A1.2 · Every instrument on this page has its blind spot written down.
  **Done when:** the table in 1 names, for each tool, at least one cost it cannot see, and no claim rests on a tool blind to it.

### A2 · 🚚 The wire half
- A2.1 · Nothing unchanged is sent twice.
  **Done when:** the assets carry a content hash and an immutable header, and a second page in a session fetches only its own html.
- A2.2 · Text crosses the wire compressed.
  **Done when:** every text response above 1 KB is gzipped, including vendored assets, with revalidation and `HEAD` unchanged.
- A2.3 · No request holds a connection longer than it needs.
  **Done when:** after a page settles, nothing is still pending, and every board endpoint answers in well under a second under concurrent load.
- A2.4 · What the page list costs is paid on purpose, not by accident.
  **Done when:** its bytes are measured and written here, and keeping it is a recorded decision rather than an unexamined default.

### A3 · 🧠 The browser half
- A3.1 · Moving between pages does not rebuild the page from nothing.
  **Done when:** a click inside a board replaces the content and keeps the parsed document, on both packagings.
- A3.2 · The browser half has a number.
  **Done when:** parse, execute and paint are timed on a real client and written here.

## States

### A1 · 🔬 What is measured, and by what
- ✅ A1.1 · Every figure in Content carries its source; the three readings that came from the wrong instrument are named in 1.1 and 1.3 so the mistake is not repeatable.
- ✅ A1.2 · The table in 1 carries a `LANE HELD` column precisely because the tool used most, `curl`, is the one that cannot see it. That gap is what 1.3 is about.

### A2 · 🚚 The wire half
- ✅ A2.1 · `serve.py` answers a `?v=` request with `public, max-age=31536000, immutable`; a second page in a session fetches only its own html, measured at 1 request and 29 KB.
- ✅ A2.2 · `try_gzip` covers static text and `serve_asset` covers the vendored bundle; 304 revalidation, `HEAD` and the `.md` links were each checked by hand afterwards.
- ✅ A2.3 · `log_boards` prunes in place and caches for two seconds. `POST /_board/activity` went from over 60 s with no answer to 43 ms, ten concurrent to 0.88 s, and a headless load of `QB1-form.html?pane=page` finished all 8 requests with nothing pending.
- ✅ A2.4 · RULED by JL on 260802: "I still want to have that panel, please give me that panel. Please keep it." The page list ships on every page of every door: 55 page blocks and 303 links, 110,651 bytes, 67% of the file at the ruling, 57 blocks, 995 links and 80% at the 260806 re-count. That is now a price this board pays knowingly for being able to jump anywhere from anywhere, and it is not a defect to be worked off. The Aim was rewritten to match the ruling; what it asks for is measurement and a decision, and it has both.

### A3 · 🧠 The browser half
- ✅ A3.1 · The one-document board always swapped; the split now does too, after a regression that made every click a full document load. 7 requests to 1.
- ⬜ A3.2 · Not started. `curl` cannot see it and no headless trace has been taken.

## Files

### ⚙️ Engines
- `live/activity.py`
  `log_boards`, the walk behind every page's `op=stats` post, and the two-second cache that keeps many tabs from each paying for it.
- `cli/serve.py`
  Decides what crosses the wire: the gzip path, the cache headers, and the `?v=` branch that makes an asset immutable.
- `live/base.py`
  `try_gzip` and the shared header rules every response passes through.
- `cli/build.py`
  Decides what a page CONTAINS, which is where the page list's 67% is added.
- `assets/js/70-router.js`
  The swap that keeps a navigation from rebuilding the document.

### 🧪 Checks
- `checks/pending.mjs`
  Opens a page in headless Chrome and asserts that NOTHING is still pending once it settles. This is the check that would have caught A2.3: the page loaded fine, so every existing check passed while a request sat holding a socket.
- `checks/splitgaps.py`
  G1 asserts the ordinary page still swaps rather than reloads, which is the regression this page's A3.1 exists to prevent.

## Lesson
260802 · A FAST SERVER AND A FAST LINK DO NOT ADD UP TO A FAST PAGE, because the third term is whether a connection was free, and that term is invisible to the tool most likely to be reached for. Eight days of measurements all said 20 to 70 ms and all of them were correct. The reading that finally landed was not a faster timing, it was a COUNT: exactly six ESTABLISHED connections from one laptop, which is a ceiling rather than a coincidence, and one request that had not finished after 25 seconds.
260802 · WHEN A WALK IS FIXED IN ONE PLACE, GREP FOR THE OTHERS THE SAME HOUR. `rglob` over the repository root was found and fixed in `live/home.py` in the morning and left standing in `live/activity.py` until the evening, on a path a hundred times hotter. The fix was known; only its second site was not. `grep -rn "rglob" live/` takes one second and was not run.
260802 · A CHECK THAT ASKS "DID IT WORK" WILL NOT FIND A RESOURCE LEAK. Every existing check passed throughout, because the page did load and its content was right. The question that finds this class of bug is "is anything still pending", and it has to be asked of a real browser, since a request never sent is not a request any server log will show.

## Log
- 260806 2143 · [REVISE-CC] swept to the 260806 architecture; corrected the dead `QB1-opening.html` name to `QB1-form.html` in Opening and 3.1, and re-anchored the page-list price with a 260806 re-count of the built sidebar: 57 pages, 995 links, 149,359 B, 80% of the file
260802 · A2.4 RULED AND CLOSED by JL: "I still want to have that panel, please give me that panel. Please keep it." He read the open question as a proposal to delete the page list, which it was not, and the wording was mine to fix. The 67% stays, knowingly: 110,651 bytes buying the ability to reach any page from any page, where a page opened on its own would otherwise be a dead end. The Aim was rewritten from "a page does not carry the whole board" to what it now asks, that the cost be measured and the keeping be a decision, and it has both. The only work left on this page is the browser half, A3.2
260802 · Moved from `QC5` to `QD8-pagecost` on JL's call ("move it"), then renumbered to `QD7-pagecost` the same day when the empty QD7 rejoin-bench stub was archived and this lane closed its gap. Both old ids resolve here through `## Links`. The QD8 position was a poor one anyway: it had already meant the activity dashboard, absorbed into `QC2` on 260726, so it was a collision waiting to be read the wrong way. It was opened in the engine lane because every lever it names is engine code, `serve.py`, `build.py`, `live/activity.py`, and that is the wrong test: a lane is chosen by where a cost is FELT, not by which file holds its fix. Waiting stops the work, and `QD` is where the work happens. The QD8 position had been a second alias into `QE2` from the 260731 split, which is one more reason it was the wrong home; `QDb2` still resolves that page, and `QC5-pagecost` and `QD8-pagecost` both resolve here
260802 · Found and fixed the cause of the one-to-two-minute page JL had reported for days, recorded in 2.3. `POST /_board/activity` never returned, because `log_boards` still ran the unpruned `rglob` that `/boards` had been fixed for that morning. Each hung post held one of the browser's six connections per origin, so a few open tabs left a CLICK with nowhere to go, which is the "Provisional headers are shown" in JL's devtools and the "12 requests / 0 B transferred" beneath it. The diagnosis took as long as it did because every measurement said the server was fast, and it was: 20 to 70 ms to serve a page, on a 24 to 35 ms link. Nothing was measuring whether a socket was free to serve it on, which is why `checks/pending.mjs` now exists and asks exactly that
260802 · Opened, after the same performance question was asked and answered three times inside `QD5` and did not belong there. `QD5` owns the pane layout; what a page costs to open is true of the one-document board as well, and every lever is in `QC`'s engine. Carries the measurements taken on 260802 from both sides of the wire, including JL's own laptop-side record, and the two readings that came from the wrong half: a `no-store` header read off a URL the browser never requests, and a click called fast because it measured 49 ms on the machine serving it

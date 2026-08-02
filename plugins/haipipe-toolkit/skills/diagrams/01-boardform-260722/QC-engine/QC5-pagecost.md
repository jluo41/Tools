# What a board page costs to open, and what we spend to make it less

state: 🟡 PARTIAL · the wire half is measured and closed; the browser half has counts but no timings
owner: CC
method: measure the wire and the browser separately, then spend only where a number says to

## Opening
What does opening one board page actually cost, and which of those costs is worth paying to remove?

A board page is a file the server sends and the browser then builds into something readable, and each half has its own price.
The wire half is bytes: how big the file is, how much of it repeats on every other page, and whether the browser is allowed to keep a copy.
The browser half is work: parsing the html, running the board's JavaScript, and building the elements you scroll through.
This page rules what those costs are and which ones we spend engineering time to reduce.

**What "a page" means here**: One generated `.html` under a board's `board/` folder, such as `QB1-opening.html`, together with the `board.css` and `board.js` it asks for.
The three arrive separately, and only the first is different from page to page.

**Where this page sits**: `QC` owns the engine, and every lever named here is in it: `build.py` decides what a page contains, `serve.py` decides what crosses the wire and what a browser may cache, and `assets/` is the bundle both halves pay for.
`QD5` owns the pane layout and keeps only what is true because there are three frames; the costs on this page would exist if the split had never been built.

**Why this is hard**: The two halves fail in ways that look identical from a chair.
A page that arrives slowly and a page that arrives fast but takes a second to build both read as "it is slow", and the tools that measure one are blind to the other: `curl` never parses, and a browser profile never shows you a cache header.
So a number from the wrong half sends the work in the wrong direction, which has already happened twice on this board.

**What decides it**: Every claim here carries the command that produced it, and no lever is pulled without a number naming it.

## Diagram

**The two halves**: what a page costs, split by who pays it and what can measure it.

```
  THE WIRE                              THE BROWSER
  ────────────────────────────────      ────────────────────────────────
  page html      20-49 KB gzipped       parse html      605 KB uncompressed
  board.js       82 KB · cached         execute js      250 KB uncompressed
  board.css      33 KB · cached         build the DOM   3,455 elements
  ────────────────────────────────      ────────────────────────────────
  measured by    curl, CDP Network      measured by     devtools, CDP Tracing
  paid           once per session       paid            once per NAVIGATION
                 for the assets                         unless the page swaps
```

**Where a page's bytes go**: measured on `QD5-split-workspace.html`, and the shape holds board-wide.

```
  page html            163,415 B raw          30,741 B gzipped
    the rail           110,651 B   67%        the same 53 blocks on all 53 pages
    the page itself     52,764 B   33%        what the reader came for
  ────────────────────────────────────────────────────────────────────────
  the rail is the single largest thing a board sends and the only one
  that is identical on every page it is sent with          A2.2 is this row
```

**What is already spent**: the levers pulled on 260802, each with the number that justified it.

```
  gzip on text            521 KB → 140 KB    a cold page open
  gzip on vendored xterm  477 KB → 118 KB    /_board/asset/ bypassed the first pass
  immutable on ?v= assets 114 KB → 0         per navigation, after the first
  prune the /boards walk   95 s → 0.12 s     366,951 entries → 11,670
  swap instead of navigate  7 req → 1 req    a rail click in the split
```

## Content

### 1 · What is measured, and by what

**Which tool sees which half**: what each measurement can report, and what it is blind to.

```
              wire bytes   requests   cache hdr   parse   execute   paint
  curl            ✅          ✅          ✅        ✗        ✗        ✗
  CDP Network     ✅          ✅          ✅        ✗        ✗        ✗
  devtools trace  ~           ~           ✗        ✅       ✅        ✅
  ─────────────────────────────────────────────────────────────────────
  a reading from the wrong half has sent this work the wrong way twice
```

#### 1.1 · Two tools, two blind spots

`curl` sees the wire exactly and the browser not at all: it reports connect time, time to first byte and transfer time, and it never parses a tag.
A browser profile is the reverse, and a cache header is invisible in it.
Every number on this page therefore names the tool that produced it, because a reading from the wrong half has twice sent this work in the wrong direction: once when a `no-store` header was read off a URL the browser never requests, and once when a click was called fast because it measured 49 ms on the machine serving it.

#### 1.2 · The link is not the subject, but it sets the exchange rate

Measured 260802 from a laptop over a direct tailnet path: 24 to 35 ms round trip, about 0.92 MB/s on a single stream and 1.30 MB/s across six.
The server answers a static asset in about 1 ms and a generated page in about 20 ms, so neither the link nor the server explains a slow page on its own.
What the link does is set the price of a REQUEST: at 30 ms, seven requests cost a fifth of a second before a byte of content is drawn, which is why request COUNT is a first-class number here and not a detail.

### 2 · The wire half

**What a second page in a session costs**: everything already paid for, and what is left.

```
  first page of a session    html 20-49 KB  +  js 82 KB  +  css 33 KB
  every page after           html 20-49 KB     cached       cached
  ────────────────────────────────────────────────────────────────────
  of that html, 67% is the rail, identical on all 53 pages     A2.3
```

#### 2.1 · The assets are cached, and the version hash is why

`board.js` and `board.css` are 82 KB and 33 KB gzipped, they are identical on every page, and the markup asks for them with a content hash: `board.js?v=25cc58ca7354`.
`serve.py` answers a stamped request with `public, max-age=31536000, immutable` and an unstamped one with `no-store`, which is correct in both cases: the hash already guarantees a changed file gets a new URL, so nothing stale can survive, and nothing unchanged is ever re-sent.
The unstamped path is the one a person types by hand, and reading its header is how two separate measurements concluded the assets were never cached.

#### 2.2 · Compression was worth more than anything else on this page

Nothing was compressed until 260802, and board text compresses 3 to 7 times because it repeats itself.
A cold page open went from 521 KB to 140 KB, the split's first open from 937 KB to 206 KB, and `xterm.min.js`, at 477 KB the largest single thing this server hands out, from 477 KB to 118 KB once `/_board/asset/` stopped bypassing the compression path.
It is one header and a `gzip.compress`, and it beat every structural change considered beside it.

#### 2.3 · The rail is what is left

67% of a page's bytes are the navigation rail, the same 53 blocks on all 53 pages, and gzip does not remove it: it makes a repeated thing cheap to send, not absent.
Deleting it from the shipped page is `A2.2` on `QD5`, and it is the only remaining lever of that size.
It is not free: a page opened on its own would lose its navigation, so what replaces it has to be decided before it is taken away.

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

Counted on `QB1-opening.html`: 604,938 uncompressed bytes parsed, 250 KB of JavaScript executed, 3,455 DOM elements built.
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

### A2 · 🚚 The wire half
- A2.1 · Nothing unchanged is sent twice.
  **Done when:** the assets carry a content hash and an immutable header, and a second page in a session fetches only its own html.
- A2.2 · Text crosses the wire compressed.
  **Done when:** every text response above 1 KB is gzipped, including vendored assets, with revalidation and `HEAD` unchanged.
- A2.3 · A page does not carry the whole board.
  **Done when:** a page's own bytes are the majority of what it ships.

### A3 · 🧠 The browser half
- A3.1 · Moving between pages does not rebuild the page from nothing.
  **Done when:** a click inside a board replaces the content and keeps the parsed document, on both packagings.
- A3.2 · The browser half has a number.
  **Done when:** parse, execute and paint are timed on a real client and written here.

## States

### A1 · 🔬 What is measured, and by what
- ✅ A1.1 · Every figure in Content carries its source; the two readings that came from the wrong half are named in 1.1 so the mistake is not repeatable.

### A2 · 🚚 The wire half
- ✅ A2.1 · `serve.py` answers a `?v=` request with `public, max-age=31536000, immutable`; a second page in a session fetches only its own html, measured at 1 request and 29 KB.
- ✅ A2.2 · `try_gzip` covers static text and `serve_asset` covers the vendored bundle; 304 revalidation, `HEAD` and the `.md` links were each checked by hand afterwards.
- 🧠 A2.3 · The rail is still 67% of every page. This is `QD5`'s A2.2 and it waits on a person: taking it out changes what a standalone page can do.

### A3 · 🧠 The browser half
- ✅ A3.1 · The one-document board always swapped; the split now does too, after a regression that made every click a full document load. 7 requests to 1.
- ⬜ A3.2 · Not started. `curl` cannot see it and no headless trace has been taken.

## Files

### ⚙️ Engines
- `cli/serve.py`
  Decides what crosses the wire: the gzip path, the cache headers, and the `?v=` branch that makes an asset immutable.
- `live/base.py`
  `try_gzip` and the shared header rules every response passes through.
- `cli/build.py`
  Decides what a page CONTAINS, which is where the rail's 67% is added.
- `assets/js/70-router.js`
  The swap that keeps a navigation from rebuilding the document.

### 🧪 Checks
- `checks/splitgaps.py`
  G1 asserts the ordinary page still swaps rather than reloads, which is the regression this page's A3.1 exists to prevent.

## Log
260802 · Opened, after the same performance question was asked and answered three times inside `QD5` and did not belong there. `QD5` owns the pane layout; what a page costs to open is true of the one-document board as well, and every lever is in `QC`'s engine. Carries the measurements taken on 260802 from both sides of the wire, including JL's own laptop-side record, and the two readings that came from the wrong half: a `no-store` header read off a URL the browser never requests, and a click called fast because it measured 49 ms on the machine serving it

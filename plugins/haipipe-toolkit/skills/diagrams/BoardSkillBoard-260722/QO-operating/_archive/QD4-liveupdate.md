# Live pages: update without losing your place
state: 🗄️ ARCHIVED · 260801, JL: "drop QD4 to the _archive" — v1 live-updates shipped and works (auto in-place swap, chat/terminal/comment-dock survive); the open swap-vs-morph, dirty-editor guard, and per-page-swap decisions are retired with it. File stays readable in _archive, never deleted.
owner: JL
method: never reload: poll our own Last-Modified and swap div.wrap in place; the drawer survives because it was never inside the content
session: 8ffce751-3dec-429b-8e05-57cc3c91402f
## Question
A board page is a static file (`board/QD/QD4.html` since QC9 retired the one-file `board.html`).
Someone (or serve.py) edits the md and regenerates that file, but **my open tab does not update itself**, so I have to refresh to see it.
Should this become live?
Does that require a Node.js version?

A static page has no built-in channel for "the server notifies me", so going live means the page carries a script that polls or listens; but the board's iron rule is "strip every script and the body remains", so it can only be an **enhancement**, never a JS-required page.
With several parties (you + colleagues + the drawer AI) viewing/editing one board, nobody sees what others just wrote, and everyone edits their own copy and overwrites; even alone, after saving a comment you still refresh by hand to see it rendered.
This is the threshold for "can the board serve as a collaboration dashboard": only after the mechanism lands can "open it and it stays fresh" be discussed.


## Boundary
- ✅ Covered here
  **How the page learns the content changed, and how it updates**: polling / SSE / WebSocket / manual refresh, pick one; full-page reload vs. a "new changes" banner.
  Plus the one-line answer: Node or not.
- ↪ Covered elsewhere
  How comments get into the md (`QA6`, solved) or how drawer/terminal work (`QD2`/`QD3`).
  Only "after a change, how do other browsers learn of it first".

## Diagram

```
  five routes, from zero infrastructure to a rewrite, side by side:

  ① manual refresh (today)   press F5 yourself             infra 0 · downside: must remember
  ② polling                  page asks every N seconds     serve.py adds an mtime endpoint
                             "did this page's file change?" pure enhancement, cheapest live
  ③ SSE (server push)        serve.py holds a long conn    ★ my lean
                             pushes "reload" after build   one-way push, native to Python, fits best
  ④ WebSocket                full duplex                   heavy; the terminal already uses WS,
                                                           but for "refresh" it is overkill
  ⑤ Node.js version          rewrite the server (vite-HMR-style)  ✗ a rewrite, splits the Python
                                                           stack (chat/comments/terminal) in two

  the key judgment: ② and ③ both fit inside **today's serve.py (Python)** — no Node.
           Node pays off only for vite-style hot module replacement, and all we need is
           "md changed → tell the browser" — a much smaller ask.
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/BoardSkillBoard-260722/board.excalidraw&frame=QD4

## Items to Finish
- [x] Pick a mechanism (manual / poll / SSE / WS)
      Decided by JL's requirement (260724: "when the chat changed something, it can be refreshed automatically, and after the refresh my chat interface is still there") → **HEAD-poll every 4s on the page's own URL** (both servers send Last-Modified; zero new endpoints).
      SSE stays the upgrade path if 4s ever feels slow.
- [x] Answer the Node question
      **No**, and the survive-the-refresh requirement is the strongest reason yet: the drawer survives because it hangs off `<body>` and we swap only `div.wrap`.
      A framework re-render buys nothing here.
- [x] Settle "what an update looks like"
      Better than the banner I leaned to: **in-place swap, automatic**: content updates under you, scroll restored, a small "↻ board updated" toast; held while you have text selected (mid-comment).
      No reload ever, so nothing to lose.
- [x] Keep the script-free readability invariant
      The watcher lives inside the page's single script block; build.py's strip-scripts assertion still passes (223k chars of body without JS).
- [x] Seen working in a real browser
      JL operated the loop live through the afternoon of 260724 (drawer edits landing under an open tab) and closed it with "It is better now.", the tick this line was waiting for.

## Where we are
**v1 shipped 260724: automatic in-place refresh; the drawer, terminal, and comment dock all survive updates.**

- 260731 JL · 🗑 The swap destroys in-flight typing, on every page at once
  JL: "when I add discussion, and add that, along the way the board is updated, and the things are gone."
  Confirmed in the code rather than inferred: the only guard before `old.replaceWith(nw)` is a text-SELECTION test, so a focused textarea carrying unsaved words is not protected at all, and `board.js` has no reference to `document.activeElement` anywhere.
- 260731 CC · 🛟 An interim silent hold SHIPPED (0.71.0) while the rows below stay open
  The tick now defers the whole swap when the focused element is a textarea or input inside `div.wrap`, or when ANY `.wrap` textarea holds a non-empty draft; the 4-second poll simply tries again after the save.
  This is the 🛟 row's option A shipped as a data-loss tourniquet, not a ruling: B's banner and the 🧬 morph remain JL's calls, and either supersedes this guard cleanly.
  The same round also stopped the OTHER killer this page owns: an asset-stamp `location.reload()` while the ⌨ terminal is open now defers with a badge ("will reload when the terminal closes"), and the pagehide beacon parks the PTY (grace 600s, same-pid reattach) instead of killing it, so even a real reload no longer costs the terminal (`QD3` ⑤, verified live).
  The Law above is not wrong, it is incomplete: it protects widgets anchored to `<body>`, and every in-page editor is inside the swapped region instead.
  This board renders 52 `.dadd` boxes, all of them inside `div.wrap`, so the blast radius is the second half of JL's complaint: because all 52 pages live in one document, a write to ANY page destroys unsaved typing on EVERY page.
  Two fixes are separable, and the cheap one is not the interesting one.
  Deferring the swap while an editor holds unsaved text ends the data loss completely and needs no library.
  Replacing the wholesale swap with a DOM morph is the modern answer to the smoothness half, since a morph mutates only what actually differs and leaves focus, scroll, and untouched inputs alive; it is what Turbo 8 and htmx 2 both adopted for exactly this complaint.

- 260731 JL · 🧟 The swap's blind spot found and closed: a stale tab's dead buttons
  JL's "add to discussion" on QB4c wrote nothing and no POST ever reached the server, because the swap keeps a tab's SCRIPTS alive forever while three sessions shipped 0.57→0.62 under it, and old JS rewiring new markup died silently, leaving every ➕ button dead.
  Two guards now close it: the build stamps `<meta name="board-assets">` (md5 of the inlined JS+CSS) and `tick()` does the one full reload when the fetched stamp differs, and every wire function runs guarded so one throw cannot kill the buttons after it (`safewire`, console-visible).
  A tab opened before this ship needs one manual hard reload to pick the guards up; every later JS ship reloads it automatically.
  Shipped in haipipe-board 0.63.0.

- How it works
  Every 4s the page HEADs its own URL and compares Last-Modified.
  On change: fetch the new page, DOMParser it, `replaceWith` ONLY `div.wrap` (all content), re-run the wiring (`window.__boardRewire`: marks/paint/resolve/discuss/chat buttons; the expand-all listener is delegated and survives by itself), restore scroll, toast "↻ board updated".
  Everything the scripts appended to `<body>` (comment dock, chat drawer mid-stream, terminal, fab) is untouched.
- The console needed one line
  FastAPI registers GET only, so `boards_api.py`'s page route gained `methods=["GET","HEAD"]`; serve.py had HEAD via SimpleHTTPRequestHandler all along.
- Held during selection
  If you have text selected (probably mid-comment), the swap waits for the next tick.

- The file is always fresh, only the browser does not know
  You write a comment on the page → serve.py writes the md and regenerates that page's html on the spot.
  So **the html on disk is already current**; the only gap is "make the open tab know to re-read".
  Which makes live updates genuinely light, not content sync, just a "go refresh" signal.
- Why I lean SSE (③) over Node (⑤)
  · The moment serve.py finishes regenerating the html it knows "changed"; pushing a word down an SSE long connection is incidental; Python's http server holds long connections natively (the terminal's WS reverse proxy already proves this connection handling runs). · A Node version would tear today's stack (comment write-back / drawer chat / terminal proxy, all in one serve.py) apart and rewrite it, for the sole gain of "smoother refresh", not worth it. · Polling (②) is simpler and sufficient, just a few seconds of lag + idle requests; SSE has neither.
  So SSE first, poll second.
- One detail that must be settled together
  "Full reload on every change" is obnoxious: mid-read or mid-comment, the page jumps and everything is gone.
  The update behavior must be settled with the mechanism; I lean "banner + reload on click".

- 260731 JL · 🪶 The two smoothness complaints are fixed, and both were measured
  JL: "even when a section is open, the change should be smooth", and separately that submitting a comment felt like the whole page refreshing.
  The swap now carries every drawer's open state across, keyed by position, because position IS identity when only text changed; the first attempt keyed on summary text and only 1 of 3 open sections survived, which the browser test caught.
  Submitting a discussion line no longer calls `__boardRefresh` at all: the row is inserted next to the box that wrote it, in exactly the markup the next build emits, with a brief tint so the eye finds it.
  Measured live: 3 sections open before and 3 after, scroll unchanged at 700, and on submit the page did not move (2321 to 2314, the difference being the empty-state line making way for a real row).
  The scenario JL asked about specifically also holds: with the chat drawer open and a half-typed question in it, an update to the page left the drawer open, the draft intact, and the terminal alive.

### Decision Now
- [ ] 🎯 Kill the index flash by routing on a class, not only on `:target`
      JL 260731: "Page A is updated, and reload it, we first go to index, and then go to Page A."
      That is not a perception, it is literally the code: `board.js` line 2110 runs `location.hash = ''; location.hash = h;` after every swap, and the empty hash makes `:target` match nothing, so `.q{display:none}` shows the Index for one frame before the page comes back.
      It exists because `:target` binds to an ELEMENT, and the swap destroys the element the fragment pointed at, so the browser never re-resolves it.
      A · keep `:target` as the no-JS fallback and add a JS-maintained class, so the CSS reads `.q:target, .q.is-open`, and the swap sets the class directly with no hash round trip and therefore no blank frame.
      B · keep the hash round trip and hide the flash with a CSS transition, which conceals the symptom and leaves the cause.
      → CC recommends A, and it is small: one CSS selector pair plus one line in the swap, and the strip-scripts invariant survives because `:target` still routes with scripts off.
- [ ] 📦 Swap only the page that changed, not all 53
      JL 260731: "I am working on page B, and page C updated, page B need to be reload."
      Written when one `board.html` held all 53 pages, so any write anywhere moved its Last-Modified and every open tab replaced the whole of `div.wrap`.
      QC9 retired that monolith on 260731: each page is now its own file under `board/`, and `watch.py` passes `--only` so a write rebuilds just the pages whose md changed, which means a reader sitting on page B is no longer disturbed by a write to page C.
      What the row still decides is the granularity WITHIN a page: the swap replaces that page's whole `div.wrap` even when one sentence changed.
      A · the update ships and replaces ONLY the changed `<section class="slide q">`, so a change to page C leaves a reader on page B with an untouched DOM.
      B · keep the whole-wrap swap and accept that any write anywhere disturbs every reader.
      → CC recommends A; it is the same work as the unit-of-change page proposed as `QC9`, and it also removes the 2 MB re-parse that makes the swap feel heavy.
- [ ] 💬 Make the chat survive a real reload, rather than trying to never reload
      JL 260731: "how could we detach the chat drawer and chat TUI from html, so when the html is updated the chat interface is not."
      Half of this is already true and worth stating: the drawer and the terminal hang off `<body>`, OUTSIDE the swapped region, so an ordinary update does not touch them, which is this face's Law.
      What still kills them is the FULL reload the assets stamp fires when the inlined JS changes, and today that reload defers only while the terminal is open or a turn is actively streaming (`termon` / `chatbusy`, with a 90 second cap), so an open but idle drawer is destroyed without warning.
      That guard is CC's own 0.63.0 change, and this is its cost.
      A · widen the deferral so an OPEN drawer holds the reload the same way an open terminal does, which is a one-line change and buys time but does not survive a hard refresh.
      B · make the drawer restorable: persist which session, which sentence focus, scroll position, and open state, then rehydrate on load, so even a hard reload continues the conversation. The transcript is already persisted per question in localStorage; only the open state and focus are lost.
      C · truly detach the TUI into its own browser window, which survives the opener reloading entirely, at the cost of the inline-context feel.
      → CC recommends B, with A shipped first as the cheap stopgap: immortal DOM is not achievable across a real refresh, and restorable state is, so aiming at restoration is the only version that always holds.

These are the calls only JL can make; CC ticks nothing here.

- [ ] 🔁 Reopen this page, or rule the finding out of scope
      The state line still says ✅ SETTLED, which was true for v1 and is not true now that three decisions are open, and `check.py` reports the contradiction as `settled-with-open-items`.
      CC does not flip a state line, so this row exists to make that flip yours rather than silent.
      → CC's proposal: reopen to 🟡 PARTIAL; v1 genuinely shipped and genuinely works, and what was found is a gap in its Law rather than a failure of the mechanism.
- [ ] 🛟 Rule the dirty-editor guard, which is the fix for losing typing
      Hold the swap while any editor inside `div.wrap` holds unsaved text, and show the pending update as a banner instead of applying it.
      A · hold and queue the update silently, applying it on blur or save, so nothing interrupts the typing but the reader never learns an update arrived.
      B · hold and show "updates ready, click to apply", which costs one click and makes the staleness visible.
      C · keep today's behaviour, which means unsaved typing keeps being destroyed.
      → CC's proposal: B; the 260724 note directly above this row already leaned "banner + reload on click" for exactly this reason, and a silent queue leaves a reader looking at stale content with no way to know.
- [ ] 🧬 Rule whether the wholesale swap becomes a DOM morph
      A morph mutates only the nodes that actually differ, so focus, scroll position, open drawers, and untouched textareas survive by construction rather than by being anchored outside the region.
      A · adopt a morph library, inlined like every other asset, which buys the behaviour Turbo 8 and htmx 2 ship at the cost of one vendored dependency.
      B · hand-roll a narrower patch that replaces only the one page section that changed, which keeps the code ours but reimplements the hard part.
      C · keep replacing `div.wrap` whole, which leaves every open drawer and scroll position dying on each update.
      → CC's proposal: A; idiomorph is the library Turbo 8 adopted for this exact complaint, it is dependency-free and small enough to inline, and B is the same work done worse unless `QC9` lands a fragment protocol first.
- [ ] 📦 Rule whether the Law gains a third clause
      Today it protects widgets anchored to `<body>` and says nothing about editors inside the swapped region, which is the gap this round found.
      → CC's proposal: yes; state that an in-flight editor is preserved across an update, so a future widget author cannot reintroduce this by placing a form inside the page.

## Law
- Never reload; swap `div.wrap` in place
  Every widget the scripts build (comment dock, chat drawer, terminal, fab) hangs off `<body>`, OUTSIDE the swapped region; that placement is the whole trick and must be preserved by future widgets.
- The page watches its own URL
  HEAD-poll every 4s, compare Last-Modified; zero server endpoints invented.
  SSE is the upgrade path if 4s ever feels slow.
- `location.reload()` is banned in the page's own controls
  Any "refresh" affordance calls `window.__boardRefresh` (the immediate in-place swap).
  A hard reload tears down the drawer; that is a bug, not a refresh (0.9.1's lesson).
- Swaps hold while text is selected
  A selection is probably a comment being written; the update waits for the next tick.
- Still an enhancement
  The watcher lives inside the page's single script block; strip every script and the full body remains (build.py asserts it).

## Files
- `serve.py`
  The live mechanism lands here (an mtime endpoint, or one SSE long connection).
  The spot where html gets generated is exactly the "changed" trigger.
- `build.py`
  It generates the `board/` tree, one file per page; live updates are only "notify the browser afterward", so its generation logic is untouched.
  The strip-scripts assertion stays its job, now asserted on the split pages.
- `watch.py`
  Rebuilds on an md change and passes `--only` the changed pages, which is what keeps one page's write off every other page's file.

## Discussion
> JL: this page does not update in real time, what should we do? Do we need to build a nodejs version? Open a Q to discuss.
>> CC0724: opened. My initial verdict: no Node; "md changed → tell the browser" is one SSE (or polling) endpoint inside today's Python serve.py; Node-style HMR is a much bigger ask. Five routes laid out, yours to call.
> JL: if we have the haichat-board, could the content be updated in realtime, or do I reload manually? What I want: in QD2, when the chat changed something, it refreshes automatically, and after the refresh my chat interface is still there, should we use node js for it?
>> CC0724: shipped exactly that, without Node: the page watches its own Last-Modified and swaps div.wrap in place; your chat drawer (even mid-stream), the terminal, and the comment dock are appended to <body>, so they never notice. When the drawer's edit lands, the content under it updates itself within ~4s with a "↻ board updated" toast.
> JL: I still have this problem? Do you think I should have a server on? with the npm as the front end? How do you think?
>> CC0731: the server was already on; what failed was this face's own blind spot, a stale tab whose swapped-in markup outran its never-refreshed JS, and an npm frontend would not have saved an open tab either: its cure for this is hot-module-reload, which is exactly the assets-stamp reload 0.63.0 just shipped, minus the toolchain. So the verdict stays no Node for the live layer; the mature-stack direction has its own home on `QE3` (the haichat-board sibling, `feat/haichat-board`), where it is a hosting decision rather than a bug fix.

## Log
260801 · Renamed to "Live pages: update without losing your place" and every live-facing `board.html` reference dropped (QC9 retired the monolith): the Question, the ② route, "the file is always fresh", the 📦 row's premise and ## Files now name the split `board/` tree and `watch.py --only`; Log history left verbatim
260731 · Open drawers now survive the swap (position-keyed) and a discussion line lands in place instead of triggering a whole-page refresh; verified over CDP with the chat drawer open and a draft in it (haipipe-board 0.81.0)
260731 · JL named three symptoms and each had a distinct cause in the code: the index flash is the hash round trip at board.js:2110, page B reloading on page C's write is whole-wrap swap granularity, and the lost chat is the 0.63.0 assets-stamp reload deferring only for termon/chatbusy; three Decision Now rows opened
260731 · liveswap probe
260731 · Interim guards shipped (0.71.0): mid-typing silent hold, terminal-open reload deferral + badge, beacon parks the PTY; the guard/morph/Law rows stay open for JL
260731 · JL reported losing typing to an incoming update; confirmed the only guard is a selection test, so a focused textarea is unprotected and one page's write clears every page's in-flight work; three Decision Now rows opened (dirty guard, morph, a third Law clause)
260731 · The stale-tab blind spot closed: assets stamp + full reload on JS change, safewire guards each wire step; JL's second Node ask answered on this face's Discussion (haipipe-board 0.63.0)
260724 1550 · JL: "It is better now.", the seen-in-a-real-browser tick lands; all items done → ✅ SETTLED, ## Law written (swap-not-reload · body-anchored widgets · reload ban · selection hold · enhancement-only)
260724 1525 · JL hit the drawer's old "↻ Reload" button and it closed the chatbot; all four location.reload() sites now call the in-place swap (window.__boardRefresh) instead; labels renamed "Refresh in place"; the drawer survives its own post-write refresh
260724 1510 · v1 shipped per JL's requirement (auto-refresh, chat survives): HEAD-poll 4s + in-place div.wrap swap + rewire + scroll restore + toast; held during text selection; console page route gained HEAD; Node answered NO, 🔴 → 🟡, only the seen-in-browser tick remains
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260724 · JL raised "the page is not live, Node or not"; QD4 opened; five routes laid out (manual/poll/SSE/WS/Node), I lean SSE and no Node, JL to decide

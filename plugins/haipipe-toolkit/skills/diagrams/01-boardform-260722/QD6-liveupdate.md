# Live page updates
state: ✅ SETTLED
owner: JL
method: never reload: poll our own Last-Modified and swap div.wrap in place; the drawer survives because it was never inside the content
session: 8ffce751-3dec-429b-8e05-57cc3c91402f
## Question
`board.html` is a static file.
Someone (or serve.py) edits the md and regenerates the html, but **my open tab does not update itself**, so I have to refresh to see it.
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
                             "did board.html change?"      pure enhancement, cheapest live
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

- How it works
  Every 4s the page HEADs its own URL and compares Last-Modified.
  On change: fetch the new page, DOMParser it, `replaceWith` ONLY `div.wrap` (all content), re-run the wiring (`window.__boardRewire`: marks/paint/resolve/discuss/chat buttons; the expand-all listener is delegated and survives by itself), restore scroll, toast "↻ board updated".
  Everything the scripts appended to `<body>` (comment dock, chat drawer mid-stream, terminal, fab) is untouched.
- The console needed one line
  FastAPI registers GET only, so `boards_api.py`'s page route gained `methods=["GET","HEAD"]`; serve.py had HEAD via SimpleHTTPRequestHandler all along.
- Held during selection
  If you have text selected (probably mid-comment), the swap waits for the next tick.

- The file is always fresh, only the browser does not know
  You write a comment on the page → serve.py writes the md and regenerates board.html on the spot.
  So **the html on disk is already current**; the only gap is "make the open tab know to re-read".
  Which makes live updates genuinely light, not content sync, just a "go refresh" signal.
- Why I lean SSE (③) over Node (⑤)
  · The moment serve.py finishes regenerating the html it knows "changed"; pushing a word down an SSE long connection is incidental; Python's http server holds long connections natively (the terminal's WS reverse proxy already proves this connection handling runs). · A Node version would tear today's stack (comment write-back / drawer chat / terminal proxy, all in one serve.py) apart and rewrite it, for the sole gain of "smoother refresh", not worth it. · Polling (②) is simpler and sufficient, just a few seconds of lag + idle requests; SSE has neither.
  So SSE first, poll second.
- One detail that must be settled together
  "Full reload on every change" is obnoxious: mid-read or mid-comment, the page jumps and everything is gone.
  The update behavior must be settled with the mechanism; I lean "banner + reload on click".

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
  It generates the html; live updates are only "notify the browser afterward"; its generation logic is untouched.
  The strip-scripts assertion stays its job.

## Discussion
> JL: this page does not update in real time, what should we do? Do we need to build a nodejs version? Open a Q to discuss.
>> CC0724: opened. My initial verdict: no Node; "md changed → tell the browser" is one SSE (or polling) endpoint inside today's Python serve.py; Node-style HMR is a much bigger ask. Five routes laid out, yours to call.
> JL: if we have the haichat-board, could the content be updated in realtime, or do I reload manually? What I want: in QD2, when the chat changed something, it refreshes automatically, and after the refresh my chat interface is still there, should we use node js for it?
>> CC0724: shipped exactly that, without Node: the page watches its own Last-Modified and swaps div.wrap in place; your chat drawer (even mid-stream), the terminal, and the comment dock are appended to <body>, so they never notice. When the drawer's edit lands, the content under it updates itself within ~4s with a "↻ board updated" toast.

## Log
260724 1550 · JL: "It is better now.", the seen-in-a-real-browser tick lands; all items done → ✅ SETTLED, ## Law written (swap-not-reload · body-anchored widgets · reload ban · selection hold · enhancement-only)
260724 1525 · JL hit the drawer's old "↻ Reload" button and it closed the chatbot; all four location.reload() sites now call the in-place swap (window.__boardRefresh) instead; labels renamed "Refresh in place"; the drawer survives its own post-write refresh
260724 1510 · v1 shipped per JL's requirement (auto-refresh, chat survives): HEAD-poll 4s + in-place div.wrap swap + rewire + scroll restore + toast; held during text selection; console page route gained HEAD; Node answered NO, 🔴 → 🟡, only the seen-in-browser tick remains
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260724 · JL raised "the page is not live, Node or not"; QD6 opened; five routes laid out (manual/poll/SSE/WS/Node), I lean SSE and no Node, JL to decide

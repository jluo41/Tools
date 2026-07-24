# Live page updates
state: 🔴 OPEN
owner: JL
method: decide whether live updates are wanted and via which mechanism; answer the Node question along the way — I lean no

## Question
`board.html` is a static file. Someone (or serve.py) edits the md and regenerates the html, but **my open tab does not update itself** — I have to refresh to see it. Should this become live? Does that require a Node.js version?

- Why it is hard
  A static page has no built-in channel for "the server notifies me". Going live means the page carries a script that polls or listens — but the board's iron rule is "strip every script and the body remains", so it can only be an **enhancement**, never a JS-required page.
- What breaks if we leave it
  With several parties (you + an RA + the drawer AI) viewing/editing one board, nobody sees what others just wrote — everyone edits their own copy and overwrites. Even alone: after saving a comment you still refresh by hand to see it rendered.
- What it affects downstream
  This is the threshold for "can the board serve as a collaboration dashboard". Only after the mechanism lands can "open it and it stays fresh" be discussed.

## Boundary
- ✅ This question owns
  **How the page learns the content changed, and how it updates**: polling / SSE / WebSocket / manual refresh — pick one; full-page reload vs. a "new changes" banner. Plus the one-line answer: Node or not.
- ❌ This question does not own
  How comments get into the md (`QA6`, solved) or how drawer/terminal work (`QD2`/`QD3`). Only "after a change, how do other browsers learn of it first".

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
- [ ] Pick a mechanism (manual / poll / SSE / WS)
      My reasoning is in Where we are; the final call is yours.
- [ ] Answer the Node question
      My initial verdict: no. Overturning it requires naming something Python's serve.py cannot do.
- [ ] Settle "what an update looks like"
      A hard full-page reload wipes your scroll position and half-written comments. Lean: a banner "↻ new changes, click to refresh" — reload only on click.
- [ ] Keep the script-free readability invariant
      Whatever the pick, it is pure enhancement: delete the script and the page still reads. build.py's assertion keeps standing guard.

## Where we are
None of it is built; today is ① manual refresh.

- The file is always fresh — only the browser does not know
  You write a comment on the page → serve.py writes the md and regenerates board.html on the spot. So **the html on disk is already current**;
  the only gap is "make the open tab know to re-read". Which makes live updates genuinely light — not content sync, just a "go refresh" signal.
- Why I lean SSE (③) over Node (⑤)
  · The moment serve.py finishes regenerating the html it knows "changed" — pushing a word down an SSE long connection is incidental; Python's http server holds long connections natively (the terminal's WS reverse proxy already proves this connection handling runs).
  · A Node version would tear today's stack (comment write-back / drawer chat / terminal proxy, all in one serve.py) apart and rewrite it, for the sole gain of "smoother refresh" — not worth it.
  · Polling (②) is simpler and sufficient, just a few seconds of lag + idle requests; SSE has neither. So SSE first, poll second.
- One detail that must be settled together
  "Full reload on every change" is obnoxious — mid-read or mid-comment, the page jumps and everything is gone. The update behavior must be settled with the mechanism; I lean "banner + reload on click".

## Files
- `serve.py`
  The live mechanism lands here (an mtime endpoint, or one SSE long connection). The spot where html gets generated is exactly the "changed" trigger.
- `build.py`
  It generates the html; live updates are only "notify the browser afterward" — its generation logic is untouched. The strip-scripts assertion stays its job.

## Discussion
> JL: this page does not update in real time — what should we do? Do we need to build a nodejs version? Open a Q to discuss.
>> CC0724: opened. My initial verdict: no Node — "md changed → tell the browser" is one SSE (or polling) endpoint inside today's Python serve.py; Node-style HMR is a much bigger ask. Five routes laid out, yours to call.

## Log
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260724 · JL raised "the page is not live — Node or not"; QD6 opened; five routes laid out (manual/poll/SSE/WS/Node), I lean SSE and no Node, JL to decide

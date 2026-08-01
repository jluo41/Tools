# TUI chat version: the real CLI
state: 🟡 PARTIAL
owner: JL
method: ttyd spawns the process + serve.py reverse-proxies through 5599; claude opens at the SPACE root, one session per question
session: d650c47e-0d7d-464d-8405-a98a545fe552

## Opening
The TUI chat version is the real Claude Code, verbatim, inside the page rather than imitated by it.
What does the board still owe a process it does not render and cannot restyle?

The original question was whether this could exist at all, and it does: one PTY per page, running where the files are, reaching the browser through the single port already forwarded.
What is open now is everything the board wraps around that process rather than inside it.
It shares one session per page with `QD2`, which is `QD1`'s Law, and 260731 showed the seam is where this breaks: a TUI chat that died left a hold that refused the SDK chat, and the refusal reached the reader as an empty answer.
The split with `QD2` is not safe versus unsafe, since the SDK chat version can open up fully too; it is a difference of FORM, and the SDK chat is a rebuilt chat box while the TUI chat is the CLI itself.


## Boundary
- ✅ Covered here
  **The real-terminal form**: how it starts, how it passes through one port, how multiple boards and questions avoid collisions, how processes get reaped.
  Since 260801 also **the smooth pane**: rendering this same session as web chat beside the raw TTY (absorbed from `QD3m`, whose full myrlin analysis is archived at `_archive/QD3m-smooth-terminal.md`).
- ↪ Covered elsewhere
  The rules themselves: that is `QD1`; nor the web drawer: that is `QD2` — and the session host the smooth pane rides on is `QD2` M1.

## Diagram

```
   browser (JL's laptop)                        server (the files live here)
   ┌──────────────────┐                         ┌──────────────────────────────┐
   │ boardA/QD3 tab   │ /_term/cc6638…/ (WS)    │ ttyd -i haiboard/cc6638.sock  │
   │ boardA/QA6 tab   │ ─────────────────────►  │   claude --resume a0c6698a    │
   │ boardB/QD3 tab   │     everything rides    │ ttyd -i haiboard/3d798.sock   │
   │  …N tabs…       │   the forwarded 5599    │   claude --session-id <uuid>  │
   └──────────────────┘ ◄─────────────────────  │ …one unix socket per Q, no ports│
      each tab = one question                   └───────────┬──────────────────┘
      = one key = one session        cwd = SPACE root ▼
                                    ~/.claude/projects/-Users-…-Physician-SPACE/<uuid>.jsonl
   key = sha1(absolute Q-file path)[:12]  ← unique across all boards; boardA/QD3 and boardB/QD3 never collide
   cwd = the whole repo (not the board folder)  ← the session reads the code it discusses; archives under the repo root's project dir

   why 5599 reverse proxy + unix sockets: only 5599 is forwarded to the laptop; no port pool —
   one socket file per question (no "which port / will they run out"). ttyd -b mounts a subpath; serve.py forwards verbatim (WS included).
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QD3

## Items to Finish
### ⌨ The entry and its session
- [x] A ⌨ entry on every Q card
      A ⌨ in the drawer header; switching turns the whole drawer into this question's real terminal.
- [x] Clicking it enters **this question's own** session
      With a session: `--resume`; without: serve.py generates a uuid, writes it back to the header, `--session-id` uses it.
      Never an empty terminal, never a second stray session.

### 🧭 The route, proven live
- [x] Route chosen
      **Neither myrlin nor hand-rolled node-pty: ttyd + serve.py reverse proxy.** Reasons in Where we are.
- [x] End-to-end verified it actually works
      WebSocket connected through the 5599 proxy; on screen was this question's real session (a0c6698a, prior history intact); sent "reply only BOARDLIVE" and got the reply on the spot.
      Not "should work", tested.

### 🔌 Many terminals through one port
- [x] Multiple questions open simultaneously
      Open more board tabs (one question per tab); no separate "pop out" button needed.
      Two ttyds verified coexisting.
- [x] Ports → unix sockets; boards never collide
      No more TCP port racing: one unix socket per question, key = path hash, globally unique.
      Verified: same-named QD3 on two boards gets different keys (cc6638… vs 3d798…), zero interference.
- [x] Processes reap themselves, no orphans
      Startup sweeps TERM_DIR and kills last round's leftovers (not relying on exit signals, most reliable); exit reaps best-effort again; `/_board/killall` closes everything; closing the board page sends a `pagehide` beacon to release.
      Verified: planted a stale ttyd → started serve.py → it was killed and its socket removed.
- [x] The terminal works through the console too (260724)
      `boards_api.py` relays `POST /_board/term|release` and, the real pipe, `WS /_term/{key}/ws` (message-level, 'tty' subprotocol preserved) plus `GET /_board/asset/*` for the vendored xterm.js.
      Verified end to end through port 8093: term started (reused QD3's own session id), ttyd's stream arrived (the first frames carried the title op and the `claude --append-system-prompt` orientation line), release cleaned up.
      Chain: browser xterm ⇄ console ⇄ serve.py ⇄ ttyd ⇄ claude.

### 🪄 The smooth pane (absorbed from QD3m, 260801)
- [ ] Render the session as web chat beside the raw pane
      Plan of record (QD3m's Decision Now proposals adopted under JL's 260731 no-decisions rule; say the word to reverse any): route **D** — serve.py holds the stream-json process (`QD2` M1's session host) and this pane renders its events, no file to tail, no boot cost per message; the raw TTY stays permanently one toggle away (standing **A**), because permission dialogs and pickers exist only on the PTY screen.
      The two location rulings were decided by shipping (sidecar registry · fig/); the picker's whole-repo expander is parked until asked for.
      Blocked on `QD2` M1 landing in `live/chat.py`; the full route analysis is in the archive.
- [ ] The fallback seam
      Detect the waiting-on-TUI moment, surface the ⌨ toggle, take the screen back after — the seam, not the rendering, is the real work.

### 🚧 Smoothness and the security line
- [ ] Make it smooth (JL 260724): ①–④ built, ⑤⑥ open, live drop-test still owed
      ① auto-reconnect with backoff, BUILT: the WS rebuilds on drops (1s→2s→…→15s, 6 tries), the terminal object survives so scrollback stays; the post-auth resize makes claude repaint.
      Not yet exercised against a real mid-session drop. ② keepalive, BUILT: a same-size resize op every 30s keeps idle relays/proxies from reaping the pipe. ③ fit on drawer resize, BUILT: ResizeObserver on the terminal host, debounced 150ms → fit → resize op. ④ pre-warm on hover, BUILT (assets only): pointer on ⌨ pulls the 480KB xterm.js early, so the click is instant.
      Deliberately NOT pre-starting ttyd: POST /_board/term takes HOLD, and a hover that never becomes a click would lock the question (see the HOLD Lesson). ⑤ grace-period release: closing the tab keeps ttyd alive ~10 min before reaping (pagehide kills it instantly today; --resume makes reopening lossless, this would make it fast).
      Open. ⑥ optional: vendored xterm WebGL addon for big-scrollback rendering.
      Open.
- [ ] The security boundary written down in black and white
      "Written down" means: who may connect, what they may touch, how auth works, all explicit and fixed, nothing vague in someone's head.
      The guardrails got stronger: ttyd listens only on unix socket files (no TCP port at all), reachable only through the 5599 proxy, keys must be registered 12-hex values.
      Still unsettled: ttyd itself does no auth; whoever reaches 5599 can use it; before any outside exposure, auth must come first.
      The console relay widens the audience the day inlab is exposed (`QE1`): auth lands there first.

## Where we are
Built, and it lives in the page. ⌨ in the drawer header enters the terminal; clicking again (💬) hands the session back.

- 260801 JL · ⌨ The same fix, done properly, after JL reported it still broken
  The first attempt above was verified on ONE path and shipped as if it were general, which it was not.
  Two defects survived it, and both were the client guessing at state the server owns.
  The save hook watched `#chat`'s class list, but opening the terminal toggles `termon` on `<body>` and touches nothing on `#chat`, so opening the TUI never recorded itself and the flag existed only when `pagehide` happened to run.
  The alive check matched basenames from `/_board/terms`, but a group or board terminal registers under a FOLDER such as `QD-working` while the drawer's `cq.file` is `board.md`, so at those two levels it always concluded no terminal existed.
  Both are now answered by the server: `POST /_board/term-probe` resolves the target with the same `term_key` the registry uses, and a parked terminal counts as present because parking is precisely what a reload does.
  Verified on all four paths this time: page, group, board, and a real browser refresh rather than a scripted `location.reload()`.

- 260801 JL · ⌨ The view now survives a reload, because the process always did
  JL: "when I use TUI and when I come back it became the GUI again, in truth the TUI is running, why it is not kept?"
  The PTY was never the problem: a reload beacons `park:true`, which keeps the process and its pump alive and only drops the WebSocket, so the terminal was still there every time.
  What was lost was the drawer's VIEW, which is rebuilt on every load and always rebuilt as the chat box, so the page asserted the SDK chat version while the TUI chat version was the one holding the session.
  The drawer now records which half it was showing and, on reload, reattaches to a terminal that is genuinely still listed by `/_board/terms`; it never spawns one, so a reload cannot start a process nobody asked for.
  Reproduced first and then verified: before the fix a reload came back with `termOn:false` and no xterm while the PTY was alive, after it the same reload comes back with the terminal mounted.
  One trap worth recording: `/_board/terms` is a POST, and calling it as a GET returned 404 into a swallowed catch, which made the reattach silently decide no terminal existed.

- 260801 JL · 🏷 Renamed and re-cut around what is still open
  JL: "We can call it SDK chat version, and TUI chat version" and "could you rethink about the Q in QD?"
  The Opening asked whether a real terminal per page could exist at all, which it does; it now asks what the board owes a process it wraps but does not render, which is the seam that failed on 260731.
  Nothing in `QF4` tests this version yet, and that gap is the reason its state stays 🟡.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [ ] 🧭 Rule where board-level work lives, now that a chat can attach at three levels
      `QD1` settled that a chat attaches to a board, a group, or a page, and board chat and group chat both ship.
      `QD7` was opened when chat was pinned to one question and asks for a board-level agent, so part of its premise is now answered by `QD1`.
      → CC's proposal: `QD1` keeps ATTACHMENT (what a chat is bound to and how many sessions it may hold) and `QD7` narrows to a DISPATCHED agent that runs without a reader watching, which no level of chat covers.

- 260801 JL+CC · 📦 QD3m folded back into this page; one terminal page again
  JL: "the QD3 and QD3m, should we just keep one of them?" — yes, this one. QD3m's engine half (§8 own-PTY) had already shipped INTO this page as 0.64.0, its picker and paste items were built and ticked, and its still-open smooth view rides `QD2` M1's session host, so a separate page held only a decision list. The open work moved up into the 🪄 smooth-pane items with CC's proposals adopted as plan of record (route D · toggle standing A), the file is archived at `_archive/QD3m-smooth-terminal.md` with the full myrlin analysis intact, and `checks/pty_e2e.py`'s default target repointed here.
- 260731 JL · 🔩 The engine under this page changed: serve.py now owns the PTY, ttyd is the fallback
  JL approved `QD3m` §8 and 0.64.0 shipped it: `spawn_pty` + a reader thread + a ring buffer replace the ttyd process; `/_term/<key>/ws` is terminated by serve.py itself, still speaking ttyd's wire protocol, so everything this page verified (5599-only, keys, HOLD, reaping, self-heal respawn) carries over unchanged.
  What this page gains for free: reconnects replay the last 256KB instantly instead of waiting for a repaint, the UTF-8 tail guard removes one smear cause at the source, and pasting a screenshot over the ⌨ pane now works.
  ttyd remains reachable via `serve.py --ttyd` until JL's click-through; after that the brew dependency can go.
- 260731 JL · 🪄 The smoothness question moved up a level, to its own face
  JL steered back here asking how to make the terminal as smooth as myrlin, and the honest answer is that a TUI can only be polished, not made smooth: myrlin's smoothness comes from rendering the session's jsonl instead of a screen.
  That form question is now `QD3m`; this page keeps the PTY plumbing and its own raw-TTY polish items ⑤⑥.

- The terminal is drawn inside the drawer with xterm.js, no more iframe (JL: closer to myrlin / A)
      xterm.js runs directly in the drawer (vendored, served by serve.py from /_board/asset/); it connects to ttyd's WebSocket itself, speaking ttyd's subprotocol (one auth message, one resize, input '0'+data, output frames lead with '0').
      Dropping the iframe layer: no webview CSP, faster load, own control of fit/reconnect. ttyd stays in the back as the PTY; the front end is our own xterm, not ttyd's page.
      Verified: the proxied WS handshake is browser-legal (101 + exact Sec-WebSocket-Accept); claude's output streams through this WS into xterm; pitfalls in Lesson.
- The route is ttyd + reverse proxy, not myrlin, not hand-rolled node-pty
      · myrlin is a whole application (AGPL, its own service), too heavy for "a terminal inside a board". · hand-rolled node-pty + xterm means managing processes, scrollback, reconnects yourself, ~150 lines to start. · ttyd is a one-job tool (`brew install ttyd`): one command turns `claude` into a web terminal.
        serve.py already serves this page, so it moonlights as the proxy, cheapest.
- Knows its question the moment it opens (JL 260723)
      The terminal starts `claude` with an `--append-system-prompt` block: which board, which question, what it asks, how many comments are open, where the file is.
      A system prompt, costs no turn, triggers nothing on its own; the moment you open it, claude already knows where it is, waiting for you to speak.
      The ttyd tab title also becomes "QD3 · title".
      Verified: a fresh terminal, zero context given, asked "which board and question am I on", answered "QC4: Migrate the two old boards".
- claude opens at the SPACE root, not the board folder (JL 260723)
      When ttyd starts `claude`, cwd = the whole repo.
      Why: a question's session keeps touching the code it discusses (e.g. "migrate the old boards" edits things outside the board folder); the board folder alone is too narrow.
      Two things follow the cwd change: ① the system prompt hands out repo-root-relative paths, not bare names; ② sessions archive under the repo root's project dir (`~/.claude/projects/-Users-…-Physician-SPACE/`).
      The cost is in Lesson: changing cwd strands the old board-folder sessions; every question restarted under root.
- One session per question is enforced (see ⚖️ Law)
      First terminal open: serve.py generates the uuid, writes it into the question's `session:` header, then `claude --session-id <uuid>`.
      So even a terminal-first open leaves no unrecorded session.
      Verified: opening a terminal on a session-less question immediately adds `session:` to its header; reopening reuses the same id.
- N questions, N terminals, via more board tabs
      To watch several questions' terminals at once, open more board tabs; each drawer is independent.
      Cleaner than a "pop out" button, and closing a tab lets pagehide reap that terminal.
      The LAW blocks only "drawer + terminal on the SAME question" (same `.jsonl`), never different questions.
- Everything rides 5599; underneath are unix sockets, not ports
      One unix socket per question (`haiboard-terms/<key>.sock`), no port pool, nothing to run out of.
      The URL is `/_term/<key>/`, key = `sha1(absolute Q-file path)[:12]`: **each board's QD3 is naturally distinct**. serve.py forwards `/_term/<key>/…` to the matching socket: plain HTTP passes straight through, WebSocket rides a raw `Upgrade` relay.
- Process lifecycle is closed
      · startup sweeps last round's leftovers first (scans the socket dir, kills stragglers), the main line of defense, no reliance on catching exit signals · atexit / SIGTERM reap best-effort on the way out · `/_board/killall` closes everything; `/_board/terms` lists what runs (across boards) · closing a board page sends a pagehide beacon to release the drawer's terminal
- Character widths agree end to end: Unicode 11 tables + a CJK-aware font (260724)
      The smear cause left standing after the 0.9.2 metrics fix: the vendored xterm.min.js only carries Unicode 6 width tables, so 🟡 ✅ 💬 count 1 cell while claude's TUI counts 2 (modern wcwidth): every emoji shifts the row, a full-screen repaint lands off-cell, and the old frame shows through as interleaved double text.
      Fixed by vendoring @xterm/addon-unicode11 (served at `/_board/asset/addon-unicode11.js`, loaded right after xterm.min.js, `unicode.activeVersion = '11'`); verified offline that the v11 provider returns width 2 for 🟡✅💬 and CJK where the built-in V6 tables said 1.
      Stacked cause fixed with it: Menlo has no CJK, so those glyphs fell back to a taller system font that bled into neighboring rows; fontFamily now carries PingFang SC / Hiragino / YaHei and lineHeight 1.2 adds the headroom.
      The addon load is soft-fail (console warning, terminal still opens), so an older serve.py cannot brick the drawer.
      Visual re-check in the drawer owed to JL.

**Still unsettled:**

- Of the security boundary, only "auth" remains unwritten
      The guardrails are no longer weak: unix sockets (no scannable TCP port), entry only through the 5599 proxy, keys must be registered.
      The single gap: ttyd itself does no auth; whoever reaches 5599 can use it.
      Pure-local + SSH forwarding today, good enough; the day it pages the outside, auth comes first.
      Parked until exposure is real.
- Auto-release on tab close: the drawer's own terminal is reaped, the rest rely on the fallback
      Closing a whole board page reaps the drawer's open terminal via the pagehide beacon.
      To sweep everything at once: `/_board/killall` (or restart serve.py, startup clears leftovers).

## Files
- `serve.py`
  `terminal()` / `proxy_term()` / `reap_stale_terms()`: ttyd + unix sockets + reverse proxy + process reaping.
- `build.py`
  The page-side entry that switches into the terminal.

## Lesson
#### An exception after `termView(true)` IS a black pane, and the wire being perfect proves nothing about the front end.
JL's 260731 black screen survived four wire-level ALL-PASS batteries because the defect lived entirely in the browser: `loadAddon(Unicode11Addon)` throws `You must set the allowProposedApi option to true` in the vendored xterm, `termOpen`'s catch turns the throw into a 3-second toast, and the pane the user stares at stays black with no banner and no console error.
It took clicking the real gesture in a real Chrome over CDP to reproduce it, and three instruments to corner it: netlog proved the script downloaded fully, tag listeners proved both assets fired `load`, and only a MutationObserver on the toast caught the swallowed message.
Two rules follow: `allowProposedApi: true` stays in the Terminal constructor as long as the unicode11 addon is loaded, and a terminal-path failure must never end in a toast alone: the pane itself must show the error, because the toast dies in 3 seconds and the pane is where the eyes are.

#### A released terminal looks like a network failure to the page.
CC released QD3's ttyd from the CLI while JL had that very terminal open in the drawer; the page saw only a dead WebSocket and knocked six times; reconnect cannot revive a terminal that no longer exists.
JL's screenshot caught it, banners interleaved with claude's half-repainted screen:

![reconnect banners over a mangled TUI after the terminal was released](fig/qd3-reconnect-after-release-260724.png)

Since 0.9.2 the third knock stops knocking and re-asks serve.py for a FRESH terminal (`--resume` restores the session), so a release under your feet costs a two-second restart, not a dead pane.
The mangled columns had a second cause: fitTerm used guessed glyph metrics (8.4px/17px); it now reads xterm's real rendered cell size and refits 350ms after connect, so the pty and the pane agree on the width claude repaints into.

#### Wiring the pipe is not the whole terminal: both ends must agree on how wide a character is.
Three width opinions meet in one pane: the app's (claude counts 🟡✅💬 as 2 cells, modern wcwidth), the terminal's (the vendored xterm shipped only Unicode 6 tables, which say 1), and the font's (Menlo has no CJK glyphs, and the fallback glyph is wider and taller than the measured ASCII cell).
Any disagreement drifts the cursor or bleeds the rows, and a TUI that repaints in place turns the drift into interleaved double-frames, the QD3 smear (fig/image.png).
Emoji-dense content (state pills, 💬 markers) guarantees the trigger on this very board.
All three are now pinned explicitly: addon-unicode11 (`activeVersion '11'`), a CJK-aware font stack, and lineHeight 1.2. None of them is left assumed.

#### A hollow session (id recorded, never chatted) makes --resume exit instantly; the terminal dies on open.
`claude --session-id <uuid>` starts a session, but if only the UI booted and no message was ever sent, no jsonl lands on disk.
Next open reads that id from the header → `claude --resume <id>` → "No conversation found" → claude exits at once → ttyd drops the connection → the terminal blacks out right after ttyd's handshake bytes.
Presented as "365 bytes then disconnect".
Fix: before opening, check **whether that conversation's jsonl exists on disk**: resume only if it does; otherwise (hollow or brand-new) use `--session-id`.
Same rule on the drawer side: check the jsonl before resuming.

#### A stuck HOLD makes "won't open" look like a bug when it is an unreleased lock.
A drawer or terminal that never finished holds the question's HOLD, and every later open gets blocked with "session is held by …".
While debugging xterm, one stale drawer-HOLD blocked every terminal open, so the browser's mountTerm never received a key; looked like xterm was broken; it was an uncleared HOLD.
Fallback: `/_board/killall` clears all HOLDs + terminals; the real fix is a reliable release in every path's finally.

#### Sessions follow the cwd; changing cwd swaps the session set; migrating jsonl does not work.
Directory names under `~/.claude/projects/` are the cwd with slashes turned to dashes: one cwd, one project.
After moving cwd from the board folder to the SPACE root:
  · old board-folder sessions stayed in their old project dir, and `claude --resume <old sid>` from root cannot find them.
  · copying the 6 jsonl files into root's project dir was tried: **resume still refused** (file did not grow after a command), because a session is bound to its original cwd; moving files does not fool it.
So this time: cleared each question's old `session:` line and restarted each under root (`--session-id`).
The old sessions are not deleted, still in the board folder's project dir; to view one, `cd` into that folder and `claude --resume`. **Lesson**: cwd is a session's home, not a tweakable parameter; changing it = this question starts over.

#### Set the id yourself on first open; never let it self-generate.
A bare `claude` invents its own new session id, which we cannot capture → one question accumulates several sessions.
With `--session-id <uuid>`: we generate first, write it back to the header first, then let the terminal use it.
That is how one-question-one-session holds.

#### Only 5599 is forwarded, so the terminal must be proxied, WebSocket included.
Forwarding one more port per question is unrealistic. ttyd's `-b <base>` makes it live under a subpath, and serve.py must handle `Upgrade: websocket` besides plain HTTP (all terminal I/O rides the WS); only a correctly forwarded handshake yields a character stream.

#### Look for an existing wheel first, but "existing" is not "the one to use".
The myrlin-workbook discovery path matched our storage location byte for byte; for a moment it looked plug-in ready.
But it is a whole application; we needed "a terminal embedded in a board".
The smaller ttyd + our own proxy won.
Searching for wheels is right; choosing one is about how big "the piece you need" is, not how much the wheel can do.

## Glossary
ttyd: a small tool that turns a command-line program into a usable web terminal.
`-i` binds the address, `-b` mounts a subpath, `-W` allows input. reverse proxy: serve.py forwards `/_term/<key>/…` requests verbatim to the local ttyd; the browser talks only to 5599 and never needs to know where ttyd is.
WebSocket / Upgrade: one always-open, two-way character connection.
All terminal keystrokes and output ride it.
AGPL-3.0: myrlin's license.
Fine to use as a standalone tool; constraints bite when you copy it into something you redistribute.

## Discussion
> JL: I wonder if we could add this too, a terminal icon?
> JL: and I want each question page to have a terminal that is its own.
> JL: I don't know whether the myrlin package could help you, github.com/therealarthur/myrlin-workbook
>> CC0723: read its source: the discovery path matches ours exactly. But it is a whole application, too heavy; ended with ttyd + serve.py's own proxy embedded instead.

## Log
260801 0020 · QD3m merged in on JL's ask: smooth-pane items absorbed (route D adopted per the no-decisions rule), the file archived under `_archive/`, board.md's lane and map updated, pty_e2e default target repointed (0.91.1)
260731 1934 · ⌨'s hard items became STANDING checks (`checks/run.py --full`, 0.89.0, home on `QC8`): the own-PTY engine and ⑤ park/reattach are re-proven on every run — a real CLI turn through the PTY (pty_e2e ①–⑦), park-not-held on tree navigation (termnav T9c/T9d `reused:true`), paste on a tree URL — all on a throwaway fixture, never a real page
260731 1905 · ⌨ follows the tree router (0.86.0): `follow()`'s split-page/group branches had no terminal hand-over, so tree navigation switched the drawer label while the OLD page's claude kept the screen and its PTY stayed unparked; both branches now park-rebind-reopen like the hash branch, and all three `termRelease` sites pass the group (a group PTY was parking the wrong scope). Found by reading SDK-Talk's navtest coverage on JL's ask — their suite never opens ⌨ — and proven with `termnav.mjs` (same CDP harness): 12/12, parked-not-held shown by `reused:true` reopens, paste re-proven on a tree URL
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · Shift+Enter fixed (0.73.1): xterm sends backslash+CR (claude's continuation); ESC+CR tested first and it SUBMITS, so the pick is empirical, bytes through the WS
260731 · Item ⑤ grace release BUILT (0.71.0): park on beacon/toggle, 600s grace, same-pid reattach with ring replay, drawer evicts parked (one-jsonl law); verified live
260731 · Env-marker lesson: serve.py restarted from a Claude session passed CLAUDE_CODE_CHILD_SESSION down, and every board terminal silently stopped saving its transcript; serve.py and spawn_pty now scrub the session markers
260731 · The black screen's real root cause found by clicking a real Chrome (0.69.0): allowProposedApi missing → loadAddon throw → toast-swallowed; one line fixes it; Lesson written
260731 · The PTY engine swapped under this page (QD3m §8, 0.64.0): serve.py owns it, ttyd → --ttyd fallback; ring replay + tail guard + ⌨ image paste arrive free
260731 · The myrlin-smoothness question split out as QD3m (render the jsonl, not the screen); this page keeps the PTY plumbing and items ⑤⑥
260726 · opening lead widened to three lines (JL: the openings are too short; say the question, how it is answered, and what turns on it)
260725 1105 · The terminal also opens on the index's chatbot (JL's ask on QC2, details on QD2): ⌨ in the board drawer posts /_board/term with file=board.md; verified live: ttyd up at /_term/117a3466ca18/, HTTP 200 through the proxy, SAME session id as the drawer (two front ends, one session holds), released clean
260724 1925 · Width accounting aligned (JL's fig/image.png smear): vendored addon-unicode11 (emoji 1→2 cells, matches claude's wcwidth; offline-verified provider v11) + CJK font fallbacks + lineHeight 1.2 in the drawer's xterm; serve.py asset whitelist + soft-fail load; Lesson added
260724 1550 · JL confirms in the browser: "It is better now."; the self-healing respawn + real cell metrics hold up live; ⑤ grace release, ⑥ WebGL, and the auth line keep this 🟡
260724 1540 · JL's screenshot (fig/qd3-reconnect-after-release-260724.png) → two fixes in assets/board.js: reconnect self-heals (2 dead knocks → respawn via /_board/term, --resume restores the session) and fitTerm uses xterm's real cell metrics + a post-connect refit. Lesson written
260724 1410 · Smoothness ①–④ built into build.py's page JS (reconnect-with-backoff keeping scrollback · 30s keepalive resize op · ResizeObserver fit · hover pre-warms assets only, never HOLD); emitted JS node-checked; ⑤ grace release and ⑥ WebGL stay open
260724 1350 · Console relay shipped and verified (boards_api.py: term/release POSTs, the /_term WS pipe, xterm assets, bytes flowed through 8093, session reused, released clean); JL asked "make it very smooth" → the six-point smoothness list added to Items to Finish
260724 1242 · Translated to English (JL 260724: everything on the board in English); closed the two open comments: the 2038 "change this to English" one (this round IS that change) and the stray 1511 copy of the already-resolved trade-offs comment
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 1810 · Closed 4 comments: QD2 now has the three tiers (default full), the framing rewritten from "restricted vs. unrestricted" to
              "a difference of form" (gated SDK chat box vs. gateless real CLI); "security boundary written down" reworded with an explanation
260723 1745 · JL asked for "an opening prompt so it knows its question". Added prime_context(): terminal via --append-system-prompt,
              drawer via system_prompt: board/question id/title/open comment count/file path. Verified both answer correctly with zero context
260723 1730 · JL ruled: claude opens at the SPACE root, not the board folder. Changed both serve.py cwds (terminal + drawer) +
              system prompts now use repo-root-relative paths; verified terminal pwd = SPACE root, all skills load.
              Migration of the 6 old sessions failed (resume rejects cross-cwd jsonl); cleared each question's session: line, restarted under root; see Lesson
260723 1650 · Removed the ↗ "pop out to a new tab" button (JL: not needed): multi-question terminals = more board tabs; cleaner, and pagehide reaps them
260723 1645 · Ports → unix sockets + global keys (no cross-board collisions) + lifecycle closed (startup sweep/killall/beacon); all verified
260723 1630 · End-to-end verified the QD3 terminal: WebSocket driven through the 5599 proxy, resumed a0c6698a, sent a command, got the reply, confirmed real
260723 1610 · Terminal built: ttyd + serve.py proxy through 5599 (WebSocket included), drawer ⌨ enters / ↗ popped a tab
260723 1600 · One-session-per-question tightened: first terminal open uses --session-id and writes it back to the header; no more unrecorded sessions
260723 1550 · Fixed refused-to-connect: everything rides the 5599 proxy, WS Upgrade forwarded along
260723 1315 · Verified route ① on the spot: this very conversation IS the real Claude Code CLI in the board folder (session a0c6698a-…)
260723 1445 · Split out of QD1 as its own question (JL: chat / terminal / sdk, one each)
260723 1440 · Read myrlin-workbook's source: the discovery path matches ours, but not used in the end, too heavy
260723 1355 · Confirmed a question-level session is a real Claude Code session; terminal and drawer are two front ends of one session

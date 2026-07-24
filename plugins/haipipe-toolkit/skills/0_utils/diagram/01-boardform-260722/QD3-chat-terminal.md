# Terminal version: the real CLI
state: 🟡 PARTIAL
owner: JL
method: ttyd spawns the process + serve.py reverse-proxies through 5599; claude opens at the SPACE root, one session per question
session: d650c47e-0d7d-464d-8405-a98a545fe552

## Question
Besides the restricted drawer, can every Q also have **its own real terminal** — the full Claude Code, nothing missing?

- Why it is hard
  The terminal must run on the machine the files are on, and squeeze through Remote-SSH's single forwarded port; several boards and questions open at once must not fight over ports.
- What breaks if we leave it
  The drawer is ultimately a re-built chat box; any job needing commands or skills gets stuck — without a real terminal the board can only do "edit some text" work.
- What it affects downstream
  The split with `QD2` stops being "safe vs. unsafe" (QD2 can now open up fully too) and becomes a **difference of form**: the drawer is a rebuilt chat box, the terminal is the CLI verbatim.

## Boundary
- ✅ Covered here
  **The real-terminal form**: how it starts, how it passes through one port, how multiple boards and questions avoid collisions, how processes get reaped.
- ↪ Covered elsewhere
  The rules themselves — that is `QD1`; nor the web drawer — that is `QD2`.

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

## Items to Finish
- [x] A ⌨ entry on every Q card
      A ⌨ in the drawer header; switching turns the whole drawer into this question's real terminal.
- [x] Clicking it enters **this question's own** session
      With a session: `--resume`; without: serve.py generates a uuid, writes it back to the header, `--session-id` uses it.
      Never an empty terminal, never a second stray session.
- [x] Route chosen
      **Neither myrlin nor hand-rolled node-pty — ttyd + serve.py reverse proxy.** Reasons in Where we are.
- [x] End-to-end verified it actually works
      WebSocket connected through the 5599 proxy; on screen was this question's real session (a0c6698a, prior history intact);
      sent "reply only BOARDLIVE" and got the reply on the spot. Not "should work" — tested.
- [x] Multiple questions open simultaneously
      Open more board tabs (one question per tab); no separate "pop out" button needed. Two ttyds verified coexisting.
- [x] Ports → unix sockets; boards never collide
      No more TCP port racing: one unix socket per question, key = path hash, globally unique.
      Verified: same-named QD3 on two boards gets different keys (cc6638… vs 3d798…), zero interference.
- [x] Processes reap themselves, no orphans
      Startup sweeps TERM_DIR and kills last round's leftovers (not relying on exit signals — most reliable); exit reaps best-effort again;
      `/_board/killall` closes everything; closing the board page sends a `pagehide` beacon to release.
      Verified: planted a stale ttyd → started serve.py → it was killed and its socket removed.
- [x] The terminal works through the console too (260724)
      `boards_api.py` relays `POST /_board/term|release` and — the real pipe — `WS /_term/{key}/ws` (message-level, 'tty' subprotocol preserved) plus `GET /_board/asset/*` for the vendored xterm.js. Verified end to end through port 8093: term started (reused QD3's own session id), ttyd's stream arrived (the first frames carried the title op and the `claude --append-system-prompt` orientation line), release cleaned up. Chain: browser xterm ⇄ console ⇄ serve.py ⇄ ttyd ⇄ claude.
- [ ] Make it smooth (JL 260724) — ①–④ built, ⑤⑥ open, live drop-test still owed
      ① auto-reconnect with backoff — BUILT: the WS rebuilds on drops (1s→2s→…→15s, 6 tries), the terminal object survives so scrollback stays; the post-auth resize makes claude repaint. Not yet exercised against a real mid-session drop.
      ② keepalive — BUILT: a same-size resize op every 30s keeps idle relays/proxies from reaping the pipe.
      ③ fit on drawer resize — BUILT: ResizeObserver on the terminal host, debounced 150ms → fit → resize op.
      ④ pre-warm on hover — BUILT (assets only): pointer on ⌨ pulls the 480KB xterm.js early, so the click is instant. Deliberately NOT pre-starting ttyd — POST /_board/term takes HOLD, and a hover that never becomes a click would lock the question (see the HOLD Lesson).
      ⑤ grace-period release: closing the tab keeps ttyd alive ~10 min before reaping (pagehide kills it instantly today — --resume makes reopening lossless, this would make it fast). Open.
      ⑥ optional: vendored xterm WebGL addon for big-scrollback rendering. Open.
- [ ] The security boundary written down in black and white
      "Written down" means: who may connect, what they may touch, how auth works — all explicit and fixed, nothing vague in someone's head.
      The guardrails got stronger: ttyd listens only on unix socket files (no TCP port at all), reachable only through the 5599 proxy,
      keys must be registered 12-hex values. Still unsettled: ttyd itself does no auth — whoever reaches 5599 can use it;
      before any outside exposure, auth must come first. The console relay widens the audience the day inlab is exposed (`QE1`) — auth lands there first.

## Where we are
Built, and it lives in the page. ⌨ in the drawer header enters the terminal; clicking again (💬) hands the session back.

- The terminal is drawn inside the drawer with xterm.js — no more iframe (JL: closer to myrlin / A)
      xterm.js runs directly in the drawer (vendored, served by serve.py from /_board/asset/); it connects to ttyd's
      WebSocket itself, speaking ttyd's subprotocol (one auth message, one resize, input '0'+data, output frames lead with '0').
      Dropping the iframe layer: no webview CSP, faster load, own control of fit/reconnect.
      ttyd stays in the back as the PTY; the front end is our own xterm, not ttyd's page.
      Verified: the proxied WS handshake is browser-legal (101 + exact Sec-WebSocket-Accept);
      claude's output streams through this WS into xterm; pitfalls in Lesson.
- The route is ttyd + reverse proxy — not myrlin, not hand-rolled node-pty
      · myrlin is a whole application (AGPL, its own service) — too heavy for "a terminal inside a board".
      · hand-rolled node-pty + xterm means managing processes, scrollback, reconnects yourself — ~150 lines to start.
      · ttyd is a one-job tool (`brew install ttyd`): one command turns `claude` into a web terminal.
        serve.py already serves this page, so it moonlights as the proxy — cheapest.
- Knows its question the moment it opens (JL 260723)
      The terminal starts `claude` with an `--append-system-prompt` block: which board, which question, what it asks,
      how many comments are open, where the file is. A system prompt — costs no turn, triggers nothing on its own —
      the moment you open it, claude already knows where it is, waiting for you to speak. The ttyd tab title also becomes "QD3 · title".
      Verified: a fresh terminal, zero context given, asked "which board and question am I on" — answered "QB3 — Migrate the two old boards".
- claude opens at the SPACE root, not the board folder (JL 260723)
      When ttyd starts `claude`, cwd = the whole repo. Why: a question's session keeps touching the code it discusses
      (e.g. "migrate the old boards" edits things outside the board folder); the board folder alone is too narrow.
      Two things follow the cwd change: ① the system prompt hands out repo-root-relative paths, not bare names;
      ② sessions archive under the repo root's project dir (`~/.claude/projects/-Users-…-Physician-SPACE/`).
      The cost is in Lesson: changing cwd strands the old board-folder sessions; every question restarted under root.
- One session per question is enforced (see ⚖️ Law)
      First terminal open: serve.py generates the uuid, writes it into the question's `session:` header, then `claude --session-id <uuid>`.
      So even a terminal-first open leaves no unrecorded session. Verified: opening a terminal on a session-less question
      immediately adds `session:` to its header; reopening reuses the same id.
- N questions, N terminals — via more board tabs
      To watch several questions' terminals at once, open more board tabs; each drawer is independent.
      Cleaner than a "pop out" button, and closing a tab lets pagehide reap that terminal.
      The LAW blocks only "drawer + terminal on the SAME question" (same `.jsonl`), never different questions.
- Everything rides 5599; underneath are unix sockets, not ports
      One unix socket per question (`haiboard-terms/<key>.sock`) — no port pool, nothing to run out of.
      The URL is `/_term/<key>/`, key = `sha1(absolute Q-file path)[:12]` — **each board's QD3 is naturally distinct**.
      serve.py forwards `/_term/<key>/…` to the matching socket: plain HTTP passes straight through, WebSocket rides a raw `Upgrade` relay.
- Process lifecycle is closed
      · startup sweeps last round's leftovers first (scans the socket dir, kills stragglers) — the main line of defense, no reliance on catching exit signals
      · atexit / SIGTERM reap best-effort on the way out
      · `/_board/killall` closes everything; `/_board/terms` lists what runs (across boards)
      · closing a board page sends a pagehide beacon to release the drawer's terminal

**Still unsettled:**

- Of the security boundary, only "auth" remains unwritten
      The guardrails are no longer weak: unix sockets (no scannable TCP port), entry only through the 5599 proxy, keys must be registered.
      The single gap: ttyd itself does no auth — whoever reaches 5599 can use it. Pure-local + SSH forwarding today, good enough;
      the day it faces the outside, auth comes first. Parked until exposure is real.
- Auto-release on tab close: the drawer's own terminal is reaped, the rest rely on the fallback
      Closing a whole board page reaps the drawer's open terminal via the pagehide beacon.
      To sweep everything at once: `/_board/killall` (or restart serve.py — startup clears leftovers).

## Files
- `serve.py`
  `terminal()` / `proxy_term()` / `reap_stale_terms()` — ttyd + unix sockets + reverse proxy + process reaping.
- `build.py`
  The page-side entry that switches into the terminal.

## Lesson
**A hollow session (id recorded, never chatted) makes --resume exit instantly — the terminal dies on open.**
`claude --session-id <uuid>` starts a session, but if only the UI booted and no message was ever sent, no jsonl lands on disk.
Next open reads that id from the header → `claude --resume <id>` → "No conversation found" → claude exits at once →
ttyd drops the connection → the terminal blacks out right after ttyd's handshake bytes. Presented as "365 bytes then disconnect".
Fix: before opening, check **whether that conversation's jsonl exists on disk** — resume only if it does; otherwise (hollow or brand-new) use `--session-id`.
Same rule on the drawer side: check the jsonl before resuming.

**A stuck HOLD makes "won't open" look like a bug when it is an unreleased lock.**
A drawer or terminal that never finished holds the question's HOLD, and every later open gets blocked with
"session is held by …". While debugging xterm, one stale drawer-HOLD blocked every terminal open,
so the browser's mountTerm never received a key — looked like xterm was broken; it was an uncleared HOLD.
Fallback: `/_board/killall` clears all HOLDs + terminals; the real fix is a reliable release in every path's finally.

**Sessions follow the cwd; changing cwd swaps the session set; migrating jsonl does not work.**
Directory names under `~/.claude/projects/` are the cwd with slashes turned to dashes — one cwd, one project.
After moving cwd from the board folder to the SPACE root:
  · old board-folder sessions stayed in their old project dir, and `claude --resume <old sid>` from root cannot find them.
  · copying the 6 jsonl files into root's project dir was tried — **resume still refused** (file did not grow after a command),
    because a session is bound to its original cwd; moving files does not fool it.
So this time: cleared each question's old `session:` line and restarted each under root (`--session-id`).
The old sessions are not deleted — still in the board folder's project dir; to view one, `cd` into that folder and `claude --resume`.
**Lesson**: cwd is a session's home, not a tweakable parameter — changing it = this question starts over.

**Set the id yourself on first open; never let it self-generate.**
A bare `claude` invents its own new session id, which we cannot capture → one question accumulates several sessions.
With `--session-id <uuid>`: we generate first, write it back to the header first, then let the terminal use it. That is how one-question-one-session holds.

**Only 5599 is forwarded, so the terminal must be proxied — WebSocket included.**
Forwarding one more port per question is unrealistic. ttyd's `-b <base>` makes it live under a subpath,
and serve.py must handle `Upgrade: websocket` besides plain HTTP (all terminal I/O rides the WS) —
only a correctly forwarded handshake yields a character stream.

**Look for an existing wheel first — but "existing" is not "the one to use".**
myrlin-workbook's discovery path matched our storage location byte for byte; for a moment it looked plug-in ready.
But it is a whole application; we needed "a terminal embedded in a board". The smaller ttyd + our own proxy won.
Searching for wheels is right; choosing one is about how big "the piece you need" is, not how much the wheel can do.

## Glossary
ttyd: a small tool that turns a command-line program into a usable web terminal. `-i` binds the address, `-b` mounts a subpath, `-W` allows input.
reverse proxy: serve.py forwards `/_term/<key>/…` requests verbatim to the local ttyd; the browser talks only to 5599 and never needs to know where ttyd is.
WebSocket / Upgrade: one always-open, two-way character connection. All terminal keystrokes and output ride it.
AGPL-3.0: myrlin's license. Fine to use as a standalone tool; constraints bite when you copy it into something you redistribute.

## Discussion
> JL: I wonder if we could add this too — a terminal icon?
> JL: and I want each question page to have a terminal that is its own.
> JL: I don't know whether the myrlin package could help you — github.com/therealarthur/myrlin-workbook
>> CC0723: read its source — the discovery path matches ours exactly. But it is a whole application, too heavy; ended with ttyd + serve.py's own proxy embedded instead.

## Comments
- [x] JL “❓ Question — besides the restricted drawer, can every Q also have its own real terminal — the full Claude Code, nothing missing?” · 260723 2038
      We need to change this to English as well, must to make this can be well written and easier to follow, and also list several bullets.
      >> CC0724: done in this round — the whole board (this file included) is now English, and the Question section carries the standard three bullets (why hard / what breaks / what it affects).
- [x] JL “two implementations of the same need as QD2, with exactly opposite trade-offs:” · 260723 1511
      we already changed that — look at QD2, it now matches QD3.
      >> CC0724: right — same resolution as the 1420/1358/1354 copies of this comment: the old "opposite trade-offs / QD2 restricted" wording was rewritten (see the Question's third bullet — the split is a difference of form, not of safety). This stray open copy is closed with them.
- [x] JL “when we open the terminal/chatbot, give some prompt so they know which question and board they're working on” · 260723 1500
      >> CC0723: done. Opening injects an orientation block via `--append-system-prompt` (the drawer builds it into system_prompt):
      board + question id + title + what it asks + open comment count + file path. Costs no turn, runs nothing.
      Verified: fresh terminal/drawer, no context, asked "which question am I on" — answered QB3 / QB2.
- [x] JL “I want to make the chat or claude opened in the SPACE dir, not in the board” · 260723 1430
      >> CC0723: changed. `ttyd` and the drawer's `claude` both open at the SPACE root (`cwd = whole repo`);
      verified `pwd` in the terminal = SPACE root and all skills visible. Cost: old board-folder sessions stayed put,
      every question restarted under root (jsonl migration tried, resume refused — see Lesson). QD1/QD2 updated together.
- [x] JL “two implementations of the same need as QD2, with exactly opposite trade-offs:” · 260723 1420
      we already changed that — look at QD2, it now matches QD3.
      >> CC0723: yes — read QD2; it now has the three permission tiers, default "full·ask" = can do anything like the CLI,
      no longer "restricted only". Rewrote the framing: the two questions differ in form, not in safety —
      QD2 is an SDK chat box with an adjustable gate, QD3 is the gateless real CLI.
- [x] JL “two implementations of the same need as QD2, with exactly opposite trade-offs:” · 260723 1358
      we already changed that — look at QD2, it now matches QD3.
      >> CC0723: same as above; the framing is rewritten. The stale "opposite trade-offs / QD2 restricted" wording is gone, replaced by the difference-of-form framing.
- [x] JL “the security boundary written down” · 260723 1355
      what does that mean?
      >> CC0723: "written down" = who may connect, what they may touch, how auth works — fixed in black and white, not left vague in anyone's head.
      That Done-when line is now titled "the security boundary written down in black and white" with an explanation line.
      Only "auth" remains: ttyd itself does no auth; whoever reaches 5599 can use it; exposure requires auth first.
- [x] JL “two implementations of the same need as QD2, with exactly opposite trade-offs: QD2 restricted, safe, one editable file; this one unrestricted, can do anything, no guardrails.” · 260723 1354
      we already changed that — look at QD2, it now matches QD3.
      >> CC0723: same as above. QD2's default "full·ask" edits any relevant file too, no longer one-file-only;
      the framing is rewritten to the new facts (a difference of form, not of restriction).
- [x] JL “Wait, here each terminal is one port? for the QD3? will that be too hard to manage?” · 260723 1640
      >> CC0723: port count was never the problem (a board runs a handful of concurrent terminals); lifecycle was.
      Switched to unix sockets (no port pool) + global keys (no cross-board collisions) + startup sweeps + killall. All verified.
- [x] JL “suppose in the future we have several boards open at the same time, how do we handle that?” · 260723 1640
      >> CC0723: at the server layer one serve.py has always served the whole repo (3 boards verified coexisting).
      Terminal identity became the hash of the Q file's absolute path — globally unique; each board's QD3 is naturally distinct.
- [x] JL “127.0.0.1 refused to connect. I have this.” · 260723 1550
      >> CC0723: an unforwarded port (same family as the earlier 3000 case). Everything now rides the forwarded 5599 proxy,
      ttyd mounts a subpath via -b, WebSocket forwarded too. Verified GET 200, WS 101.
- [x] JL “in the questions, I cannot open two claude terminal version at the same time?” · 260723 1600
      >> CC0723: you can — the UI blocked it, not the LAW. Different questions are different sessions; open more board tabs. (The ↗ pop-out button was later removed per JL.)

## Log
260724 1410 · Smoothness ①–④ built into build.py's page JS (reconnect-with-backoff keeping scrollback · 30s keepalive resize op · ResizeObserver fit · hover pre-warms assets only, never HOLD); emitted JS node-checked; ⑤ grace release and ⑥ WebGL stay open
260724 1350 · Console relay shipped and verified (boards_api.py: term/release POSTs, the /_term WS pipe, xterm assets — bytes flowed through 8093, session reused, released clean); JL asked "make it very smooth" → the six-point smoothness list added to Items to Finish
260724 1242 · Translated to English (JL 260724: everything on the board in English); closed the two open comments — the 2038 "change this to English" one (this round IS that change) and the stray 1511 copy of the already-resolved trade-offs comment
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 1810 · Closed 4 comments: QD2 now has the three tiers (default full), the framing rewritten from "restricted vs. unrestricted" to
              "a difference of form" (gated SDK chat box vs. gateless real CLI); "security boundary written down" reworded with an explanation
260723 1745 · JL asked for "an opening prompt so it knows its question". Added prime_context(): terminal via --append-system-prompt,
              drawer via system_prompt — board/question id/title/open comment count/file path. Verified both answer correctly with zero context
260723 1730 · JL ruled: claude opens at the SPACE root, not the board folder. Changed both serve.py cwds (terminal + drawer) +
              system prompts now use repo-root-relative paths; verified terminal pwd = SPACE root, all skills load.
              Migration of the 6 old sessions failed (resume rejects cross-cwd jsonl); cleared each question's session: line, restarted under root; see Lesson
260723 1650 · Removed the ↗ "pop out to a new tab" button (JL: not needed) — multi-question terminals = more board tabs; cleaner, and pagehide reaps them
260723 1645 · Ports → unix sockets + global keys (no cross-board collisions) + lifecycle closed (startup sweep/killall/beacon); all verified
260723 1630 · End-to-end verified the QD3 terminal: WebSocket driven through the 5599 proxy, resumed a0c6698a, sent a command, got the reply — confirmed real
260723 1610 · Terminal built: ttyd + serve.py proxy through 5599 (WebSocket included), drawer ⌨ enters / ↗ popped a tab
260723 1600 · One-session-per-question tightened: first terminal open uses --session-id and writes it back to the header; no more unrecorded sessions
260723 1550 · Fixed refused-to-connect: everything rides the 5599 proxy, WS Upgrade forwarded along
260723 1315 · Verified route ① on the spot: this very conversation IS the real Claude Code CLI in the board folder (session a0c6698a-…)
260723 1445 · Split out of QD1 as its own question (JL: chat / terminal / sdk, one each)
260723 1440 · Read myrlin-workbook's source: the discovery path matches ours — but not used in the end, too heavy
260723 1355 · Confirmed a question-level session is a real Claude Code session; terminal and drawer are two front ends of one session

# Chat · the TUI version, the real CLI
state: 🗂 FOLDED · into QPf4-chat §5 the TUI form (JL 260815) · the full record stays here
owner: JL
method: serve.py owns the PTY and terminates /_term/<key>/ws itself through 5599 (ttyd is the --ttyd fallback); claude opens at the SPACE root, one session per question
session: d650c47e-0d7d-464d-8405-a98a545fe552
## Opening
What must the board give a real Claude Code terminal, so the session stays usable, safe, and easy to get back?

The TUI is the whole command line, shown inside the page, and the board does not rebuild its screen.
That also means the board cannot restyle it, and cannot tell what is going on inside the process.
The trouble sits at the joins: handing the session over, reconnecting, starting and ending the process, and giving out a real shell.
This page is done when the process can be opened, picked up again, let go, and handed back to the SDK chat with no surprise.

**Covered elsewhere**: The rules are `QD1`.
The web chat panel is `QD2`, and the session host that the smooth pane rides on is `QD2` M1.
Since 260801 the FORM is `QD4`: where typing happens, what the pane shows when 80 columns will not fit, and what the page owes a reader who leaves and comes back.
A fault in the process belongs on this page, and a fault in the form belongs on that one.


## Diagram

```
   browser (JL's laptop)                        server (the files live here)
   ┌──────────────────┐                         ┌──────────────────────────────┐
   │ boardA/QD3 tab   │ /_term/cc6638…/ws (WS)  │ serve.py PTY cc6638…          │
   │ boardA/QA6 tab   │ ─────────────────────►  │   claude --resume a0c6698a    │
   │ boardB/QD3 tab   │     everything rides    │ serve.py PTY 3d798…           │
   │  …N tabs…       │   the forwarded 5599    │   claude --session-id <uuid>  │
   └──────────────────┘ ◄─────────────────────  │ …one PTY per key, no ports    │
      each tab = one question                   └───────────┬──────────────────┘
      = one key = one session        cwd = SPACE root ▼
                                    ~/.claude/projects/-Users-…-Physician-SPACE/<uuid>.jsonl
   key = sha1(page path [+ session])[:12]  ← unique across all boards; boardA/QD3 and boardB/QD3 never collide
   cwd = the whole repo (not the board folder)  ← the session reads the code it discusses; archives under the repo root's project dir

   why one port, no port pool: only 5599 is forwarded to the laptop. Since 260731 (0.64.0) serve.py spawns the
   PTY itself and terminates the WS at /_term/<key>/ws, still speaking ttyd's wire protocol; the ttyd road
   (haiboard-terms/<key>.sock unix sockets, reverse-proxied verbatim) survives as the --ttyd fallback.
```


## Content

### 1 · Which chat to open, and what stays when you switch
**The two chats, side by side**: when to pick the terminal, how the two buttons hand one question back and forth, and what stays alive.

```
  ⌨️ WHEN TO PICK THIS ONE, and not the GUI chat of `QD2`
     long jobs · skills · anything shaped like a command · watching a command run
     the GUI chat is for checked edits in the page, diffs, and tool cards

  🔁 ONE QUESTION, TWO WINDOWS, NEVER BOTH        QD1's Law
     >_ TUI Chat  ▶ hands this question to a real terminal
     💬 GUI Chat  ▶ takes it back, with the past messages still there
     the two buttons are one switch: the lit one shows where you are,
     clicking it again closes the whole chat pane

  🧷 WHAT SURVIVES WHAT
     moving around the page   ▶ the terminal is untouched, it lives elsewhere
     a full browser reload    ▶ the PTY is PARKED, not killed, and it comes back
     closing the tab          ▶ parked, then cleaned up on its own timer
```
📌 One question is handed between two chats, never open in both, and switching or reloading does not kill the terminal.

The terminal is the real command line, running on the machine that holds the files.
It can do anything a terminal can do, and that is why you pick it over the drawn chat of `QD2`.
Reach for it when the job is long, when it needs skills, or when you want to watch a command run instead of reading a summary.

Handing the question over is the part worth learning, and it takes one click.
`>_ TUI Chat` gives this question to the terminal.
`💬 GUI Chat` takes it back, and the past messages are still there.
The two buttons work as one switch, not two, and the lit one shows where you are.
Click the other one and you move over.
Click the lit one and the chat pane closes, while nothing stops running.
`checks/guichat.mjs` T17 clicks both and checks the result, so a broken hand-over shows up as a failed check.

Never both at once, because `QD1`'s Law allows one live window per question.
Two front ends writing one `.jsonl` file split the history in two.
So the switch hands the question over instead of opening a second window, and the chat panel's own `>_` control underneath still does the work.

## Aims
### Decision Now
Only JL can make these calls, and CC ticks nothing here.

- [x] 🧭 Ruled 260801: board-level work lives in `QD1`'s attachment levels, and `QDa7` is archived
      JL: "你把那个 Q board 的 agent 给删掉，我们不再需要了."
      CC had proposed cutting `QDa7` down to a sent-off agent that runs with no reader watching. JL took the simpler road and retired the page instead.
      `QD1` settled that a chat attaches to a board, a group, or a page, and both board chat and group chat now ship.
      That covers the need `QDa7` was opened for, back when chat was pinned to one question.
      The page can be read at `../_archive/QD7-boardagent.md`, and `QDa7` points there through `## Links`.
      The bare `QD7` short name was deleted on 260802, because a LIVE `QD7` now exists and was quietly winning every one of these links.

- 260801 JL+CC · 📦 QD3m folded back into this page, so there is one terminal page again
  JL: "the QD3 and QD3m, should we just keep one of them?" The answer was yes, this one.
  QD3m's engine half, §8 own-PTY, had already shipped INTO this page as 0.64.0, and its picker and paste items were built and ticked.
  Its still-open smooth view rides `QD2` M1's session host, so a separate page held only a list of decisions.
  The open work moved up into the 🪄 smooth-pane items, with CC's proposals taken as the plan on record: route D, and the toggle as standing choice A.
  The file is archived at `../_archive/QD3m-smooth-terminal.md` with the full myrlin study intact, and `checks/pty_e2e.py` now points here by default.
- 260731 JL · 🔩 The engine under this page changed: serve.py now owns the PTY, and ttyd is the fallback
  JL approved `QD3m` §8 and 0.64.0 shipped it.
  `spawn_pty`, a reader thread, and a saved-text buffer replace the ttyd process, and serve.py now ends `/_term/<key>/ws` itself while still speaking ttyd's wire format.
  So everything this page had already proven carries over unchanged: 5599 only, the keys, the HOLD, the clean-up, and the self-healing restart.
  Three things arrive for free with it.
  A reconnect draws the last 256KB at once instead of waiting for a repaint.
  The UTF-8 tail guard removes one cause of a smeared screen at the source.
  And pasting a screenshot into the ⌨ pane now works.
  ttyd is still reachable with `serve.py --ttyd` until JL has clicked through it, and after that the brew dependency can go.
- 260731 JL · 🪄 The smoothness question moved up a level, onto a page of its own
  JL came back here asking how to make the terminal as smooth as myrlin.
  The honest answer is that a TUI can be polished but not made smooth, because myrlin's smoothness comes from drawing the session's jsonl file instead of a screen.
  That form question is now `QD3m`, and this page keeps the PTY plumbing and its own raw-TTY polish items ⑤ and ⑥.

- The terminal is drawn inside the chat panel with xterm.js, and the iframe is gone (JL: closer to myrlin / A)
      xterm.js runs straight in the panel. We ship our own copy, and serve.py serves it from /_board/asset/.
      It connects to ttyd's WebSocket itself, speaking ttyd's subprotocol: one auth message, one resize, input as '0' plus the data, and output frames that start with '0'.
      Dropping the iframe layer buys three things: no webview CSP, a faster load, and our own control of fit and reconnect.
      ttyd stays behind as the PTY, and the front end is our own xterm, not ttyd's page.
      Checked: the proxied WS handshake is legal for a browser (101 plus the exact Sec-WebSocket-Accept), and claude's output streams through this WS into xterm. The traps are in Lesson.
- The route is ttyd plus a reverse proxy, not myrlin, and not a hand-built node-pty
      · myrlin is a whole application, AGPL, with its own service, and far too heavy for "a terminal inside a board".
      · a hand-built node-pty plus xterm means running the processes, the scrollback, and the reconnects yourself, about 150 lines before anything works.
      · ttyd does one job (`brew install ttyd`): one command turns `claude` into a web terminal.
        serve.py already serves this page, so it can be the proxy as well, which is the cheapest road.
- It knows its question the moment it opens (JL 260723)
      The terminal starts `claude` with an `--append-system-prompt` block: which board, which question, what that question asks, how many comments are open, and where the file is.
      It is a system prompt, so it costs no turn and starts nothing by itself.
      The moment you open the terminal, claude already knows where it is, and waits for you to speak.
      The ttyd tab title also becomes "QD3 · title".
      Checked: a fresh terminal with nothing told to it was asked "which board and question am I on", and it answered "QC4: Migrate the two old boards".
- claude opens at the SPACE root, not the board folder (JL 260723)
      When ttyd starts `claude`, the working folder is the whole repo.
      The reason: a question's session keeps touching the code it talks about, and "migrate the old boards" edits things outside the board folder, so the board folder alone is too narrow.
      Two things follow from that change. ① the system prompt gives out paths from the repo root, not bare file names.
      ② sessions are stored under the repo root's project folder (`~/.claude/projects/-Users-…-Physician-SPACE/`).
      The price is in Lesson: changing the working folder strands the old board-folder sessions, so every question was restarted under the root.
- One session per question is enforced (see ⚖️ Law)
      On the first terminal open, serve.py makes the uuid, writes it into the question's `session:` header, and then runs `claude --session-id <uuid>`.
      So even opening the terminal first leaves no session unrecorded.
      Checked: opening a terminal on a question with no session adds `session:` to its header at once, and opening it again reuses the same id.
- N questions, N terminals, by opening more board tabs
      To watch several questions' terminals at once, open more board tabs, since each chat panel stands on its own.
      That is tidier than a "pop out" button, and closing a tab lets `pagehide` clean that terminal up.
      The LAW blocks only a chat panel and a terminal on the SAME question, which share one `.jsonl` file. Different questions are fine.
- Everything rides on 5599, and underneath are unix sockets, not ports
      One unix socket per question (`haiboard-terms/<key>.sock`), no pool of ports, and nothing to run out of.
      The URL is `/_term/<key>/`, where the key is `sha1(absolute Q-file path)[:12]`, so **each board's QD3 is different by itself**.
      serve.py forwards `/_term/<key>/…` to the matching socket: plain HTTP passes straight through, and the WebSocket rides a raw `Upgrade` relay.
- Nothing is left running by accident
      · startup first sweeps what the last round left behind, scanning the socket folder and killing stragglers. This is the main defence, and it waits for no exit signal.
      · atexit and SIGTERM try to clean up on the way out, as best they can.
      · `/_board/killall` closes everything, and `/_board/terms` lists what is running across all boards.
      · closing a board page sends a `pagehide` beacon that releases the chat panel's terminal.
- Both ends now agree how wide a character is: Unicode 11 tables plus a font that knows CJK (260724)
      One cause of the smeared screen was still standing after the 0.9.2 metrics fix.
      Our copy of xterm.min.js carries only Unicode 6 width tables, so 🟡 ✅ 💬 count as 1 cell while claude's TUI counts them as 2, following modern wcwidth.
      Every emoji then shifts the row, a full-screen repaint lands off the cell, and the old screen shows through as doubled text.
      Fixed by shipping @xterm/addon-unicode11, served at `/_board/asset/addon-unicode11.js`, loaded right after xterm.min.js, with `unicode.activeVersion = '11'`.
      Checked offline that the v11 provider returns width 2 for 🟡✅💬 and for CJK, where the built-in V6 tables said 1.
      A second cause was fixed with it: Menlo has no CJK glyphs, so those characters fell back to a taller system font that bled into the rows next door.
      fontFamily now carries PingFang SC, Hiragino, and YaHei, and lineHeight 1.2 adds the headroom.
      If the addon fails to load, the terminal still opens with a console warning, so an older serve.py cannot break the panel.
      A look at it in the panel is still owed to JL.

**Still unsettled:**

- On the security line, only login is still unwritten
      The guards are no longer weak: unix sockets with no TCP port to scan, entry only through the 5599 proxy, and keys that must be registered.
      The one gap: ttyd itself asks for no login, so whoever reaches 5599 can use it.
      Today it is local only, over an SSH forward, and that is good enough. The day it faces the outside, login comes first.
      Parked until that day is real.
- Auto-release when a tab closes: the chat panel's own terminal is cleaned up, and the rest fall back
      Closing a whole board page cleans up the chat panel's open terminal, through the `pagehide` beacon.
      To sweep everything at once, call `/_board/killall`, or restart serve.py, since startup clears leftovers.


### 🔁 Coming back to a parked terminal
- ✅ A4.1 · A reader who reloads the page gets the SAME terminal back, with what was on it.
  **Done when:** after a full reload the pane shows the parked session with its saved text drawn again, not an empty terminal.
  **Now:** CLOSED 260802, and it was never broken.
  The terminal comes back after a full browser reload with the SAME key and its saved text drawn again.
  That held four runs out of four (`1c87f5ece80e` → `1c87f5ece80e`, about 1,240 characters).
  Two false alarms had to be cleared first, and both were mine.
  I said it came back EMPTY. It does not.
  The `echo` typed before the reload is missing because the CLI paints its screen again when it reconnects.
  That is what a full-screen app does.
  Then I said it was random, about half the runs. It is not.
  The coin flip was `checks/tuichat.mjs` clicking `>_ TUI` every time without looking first.
  The strip's two buttons are one switch with an OFF position, so clicking the lit one PUTS THE CHAT AWAY.
  Whether it was already lit depended on what the previous run left in `board-split-chat`, so the suite was closing the pane it meant to open.
  Now it is checked, not just reported.

- A4.2 · The terminal always fits the pane it sits in, at any width.
  **Done when:** dragging the split handle changes how many columns the terminal has, and no width leaves a sideways scrollbar.

### ⌨ The way in, and the session it opens
- [x] A ⌨ button on every Q card
      The ⌨ sits in the chat panel header, and clicking it turns the whole panel into this question's real terminal.
- [x] Clicking it opens **this question's own** session
      If the question already has a session, serve.py runs `--resume`. If it has none, serve.py makes a uuid, writes it into the header, and passes it to `--session-id`.
      Never an empty terminal, and never a second stray session.

### 🧭 The route, proven live
- [x] Route chosen
      **Not myrlin, and not a hand-built node-pty: ttyd plus a serve.py reverse proxy.** The reasons are further down this page.
- [x] Tested end to end, and it works
      The WebSocket connected through the 5599 proxy, and the screen showed this question's real session, a0c6698a, with its earlier history intact.
      Sent "reply only BOARDLIVE" and the reply came back at once.
      Not "should work", tested.

### 🔌 Many terminals through one port
- [x] Several questions open at the same time
      Open more board tabs, one question per tab. No "pop out" button is needed.
      Two ttyds were seen running side by side.
- [x] Ports became unix sockets, so boards never collide
      No more racing for a TCP port. Each question gets one unix socket, and its key is a hash of the path, so it is unique everywhere.
      Checked: a QD3 on two different boards gets two different keys (cc6638… and 3d798…), with no interference.
- [x] Processes clean themselves up, and leave no orphans
      At startup serve.py sweeps TERM_DIR and kills what the last round left behind, which is safer than waiting for exit signals.
      On exit it tries again, `/_board/killall` closes everything, and closing the board page sends a `pagehide` beacon that releases the terminal.
      Checked: planted a stale ttyd → started serve.py → the stale one was killed and its socket removed.
- [ ] 🔑 Finish the (page, session) re-key: four lookups still use the page-only key
      On 260801 terminals were re-keyed by (page, session), so that opening one stops killing another.
      `terminal()` now files a terminal under `term_key(f, sid)` at `live/term.py:581`.
      Four lookups were never moved. They still ask for `term_key(f)`, and that can never match an entry whose key holds a session.
      They are `hold()` at 398 and 408, `park()` at 503, and `kill_term()` at 789. The line numbers were re-checked against live/term.py on 260806, and all four are still page-only.
      `term_probe()` is fine, because it looks up by FILE through `terms_for(f)`. That gap is the tell: the page can SEE the terminal but cannot ACT on it.
      What goes wrong, worst first. `hold()` finds no terminal, treats the terminal's claim as void, and drops the HOLD.
      The chat panel then opens an SDK session on the SAME `.jsonl` file a live PTY is writing, which breaks QD1's Law and loses the past messages.
      `park()` returns `parked:false` and quietly does neither. `kill_term()` can never close a terminal.
      The numbers prove it, so no argument is needed.
      The live QB4 terminal is filed as `47d8ca068ee1`, while `sha1(path)[:12]` for that same page is `f891ba932470`, so the lookups miss every time.
      Seen directly too: `/_board/release` returned `{"closed": false}` for a terminal that `/_board/terms` was listing as alive.
      The fix is to look up by file (`terms_for(f)`) instead of by page key.
      `park` and `kill_term` also need a ruling on WHICH terminal they mean, now that one page can hold several.
- [x] The terminal works through the console too (260724)
      `boards_api.py` passes on `POST /_board/term|release`, and the real pipe, `WS /_term/{key}/ws`, message by message with the 'tty' subprotocol kept.
      It also passes on `GET /_board/asset/*` for the copy of xterm.js we ship.
      Tested end to end through port 8093. The terminal started and reused QD3's own session id, ttyd's stream arrived, and release cleaned up.
      The first frames carried the title op and the `claude --append-system-prompt` opening line.
      The chain is: browser xterm ⇄ console ⇄ serve.py ⇄ ttyd ⇄ claude.

### 🪄 The smooth pane (moved in from QD3m, 260801)
- [ ] Draw the session as web chat next to the raw pane
      The plan on record, taken from QD3m's Decision Now proposals under JL's 260731 no-decisions rule. Say the word and any of it can be reversed.
      Route **D**: serve.py holds the stream-json process, which is `QD2` M1's session host, and this pane draws its events.
      There is no file to tail, and no start-up cost per message.
      The raw TTY stays one click away for good, which is standing choice **A**, because permission dialogs and pickers only appear on the PTY screen.
      The two questions about where things live were settled by shipping them, as a sidecar list and a fig/ folder.
      The picker's whole-repo expander waits until someone asks for it.
      `QD2` M1 landed on 260731 as the session host in `live/chat.py`, so nothing blocks this now.
      Drawing the pane is the work that is left, and the full study of the routes is in the archive.
- [ ] The fallback seam
      Spot the moment the session is waiting on the TUI, show the ⌨ toggle, and take the screen back after.
      The seam is the real work, not the drawing.

### 🚧 Smoothness and the security line
- [ ] Make it smooth (JL 260724): ① to ⑤ built, ⑥ still open, and a live drop test still owed
      ① reconnect on its own, waiting longer each time. BUILT: the WebSocket rebuilds after a drop, waiting 1s, 2s, and so on up to 15s, six tries.
      The terminal object stays alive, so the scrollback stays too, and the resize after login makes claude paint the screen again.
      It has not yet been tried against a real drop in the middle of a session.
      ② keepalive. BUILT: a resize message of the same size every 30s stops idle relays and proxies from closing the pipe.
      ③ fit when the chat panel is resized. BUILT: a size watcher on the terminal host waits 150ms, fits, then sends a resize message.
      ④ warm up on hover. BUILT, for the files only: pointing at ⌨ pulls the 480KB xterm.js early, so the click feels instant.
      The PTY is on purpose NOT started early, because `POST /_board/term` takes the HOLD, and a hover that never becomes a click would lock the question. See the HOLD lesson below.
      ⑤ release after a grace period. BUILT in 0.71.0: closing the tab PARKS the PTY for 600s instead of killing it.
      Reattaching to the same pid draws the saved text again, and this is re-proven on every `checks/run.py --full`.
      ⑥ optional: ship the xterm WebGL addon, for drawing a big scrollback.
      Open.
- [ ] 📱 Moved to `QD4` on 260801: the phone is a FORM question, not an engine one
      This item looked like one focus bug. JL's 260801 phone session showed four separate failures with the same shape.
      Keystrokes doubled, frames came out shredded, the keyboard would not open, and the chat panel froze after switching away.
      None of them is fixed by adjusting the grid.
      `QD4` now owns it, along with the first focus finding: `focus()` runs only after the terminal has finished starting, and iPhone Safari need not count that as the user's tap.
- [ ] The security line written down in plain words
      "Written down" means: who may connect, what they may touch, and how login works, all stated and fixed, with nothing left vague in someone's head.
      The guards did get stronger. ttyd listens only on unix socket files, with no TCP port at all, it is reachable only through the 5599 proxy, and keys must be registered 12-hex values.
      One thing is still open: ttyd itself checks no login, so whoever reaches 5599 can use it.
      Login must come first, before this is opened to the outside.
      The console relay widens the audience the day inlab is opened up (`QE1`), so login lands there first.

## Files
- `live/term.py`
  `terminal()`, `proxy_term()`, `reap_stale_terms()`, and `spawn_pty`: the PTY engine, the WebSocket end, and the clean-up of processes.
  ttyd and unix sockets are used only on the `--ttyd` fallback. It moved here from `cli/serve.py` in the 260731 live/ split.
- `cli/serve.py`
  The HTTP way in. It routes `/_term/<key>/…` and `/_board/term*` into `live/term.py`, and `--ttyd` turns on the fallback.
- `assets/js/10-drawer/30-terminal.js`
  The page-side code that switches into the terminal. It was part of `cli/build.py`'s page JS before the assets split.

## Lesson
#### An error after `termView(true)` IS a black pane, and a perfect wire proves nothing about the browser side.
JL's 260731 black screen passed four ALL-PASS test rounds on the wire, because the fault lived entirely in the browser.
In our copy of xterm, `loadAddon(Unicode11Addon)` throws `You must set the allowProposedApi option to true`.
`termOpen`'s catch turns that throw into a 3-second toast.
The pane the user stares at stays black, with no banner and no console error.
Reproducing it took clicking the real button in a real Chrome over CDP, and three tools to corner it.
netlog proved the script downloaded in full, tag listeners proved both files fired `load`, and only a MutationObserver on the toast caught the swallowed message.
Two rules follow. `allowProposedApi: true` stays in the Terminal constructor for as long as the unicode11 addon is loaded.
And a failure on the terminal path must never end in a toast alone.
The pane itself must show the error, because a toast dies in 3 seconds and the pane is where the eyes are.

#### A released terminal looks like a network failure to the page.
CC released QD3's ttyd from the command line while JL had that very terminal open in the chat panel.
The page saw only a dead WebSocket and knocked six times, and a reconnect cannot revive a terminal that no longer exists.
JL's screenshot caught it, with banners mixed into claude's half-painted screen:

![reconnect banners over a mangled TUI after the terminal was released](fig/qd3-reconnect-after-release-260724.png)

Since 0.9.2 the third knock stops knocking and asks serve.py for a FRESH terminal instead, and `--resume` brings the session back.
So a release under your feet costs a two-second restart, not a dead pane.
The mangled columns had a second cause. fitTerm used guessed glyph sizes, 8.4px by 17px.
It now reads xterm's real drawn cell size and fits again 350ms after connecting, so the PTY and the pane agree on the width claude paints into.

#### Wiring the pipe is not the whole terminal: both ends must agree how wide a character is.
Three opinions about width meet in one pane.
The app's: claude counts 🟡✅💬 as 2 cells, following modern wcwidth.
The terminal's: our copy of xterm shipped only Unicode 6 tables, which say 1.
The font's: Menlo has no CJK glyphs, and the fallback glyph is wider and taller than the measured ASCII cell.
Any disagreement drifts the cursor or bleeds the rows, and a TUI that paints in place turns that drift into doubled screens, the QD3 smear (fig/image.png).
Content full of emoji, such as state pills and 💬 marks, makes it happen for certain on this very board.
All three are now pinned down: addon-unicode11 set to `'11'`, a font list that knows CJK, and lineHeight 1.2.
None of them is left to chance.

#### An empty session, with an id written down but never used, makes --resume quit at once, and the terminal dies on open.
`claude --session-id <uuid>` starts a session, but if only the UI came up and no message was ever sent, no jsonl file lands on disk.
The next open reads that id from the header → `claude --resume <id>` → "No conversation found" → claude quits at once → ttyd drops the connection → the terminal goes black right after ttyd's handshake bytes.
It showed up as "365 bytes then disconnect".
The fix: before opening, check **whether that conversation's jsonl file is on disk**. Resume only if it is, and otherwise use `--session-id`.
The same rule holds on the chat panel side: check the jsonl file before resuming.

#### A stuck HOLD makes "it will not open" look like a bug, when it is a lock nobody let go of.
A chat panel or terminal that never finished still holds the question's HOLD, and every later open is blocked with "session is held by …".
While debugging xterm, one stale panel HOLD blocked every terminal open, so the browser's mountTerm never got a key.
It looked like xterm was broken. It was a HOLD nobody cleared.
The way out: `/_board/killall` clears all HOLDs and terminals. The real fix is a release that always runs, in every path's finally.

#### Sessions follow the working folder. Change it and you get a different set of sessions, and copying the jsonl files does not work.
Folder names under `~/.claude/projects/` are the working folder with the slashes turned into dashes, so one working folder means one project.
After moving the working folder from the board folder to the SPACE root:
  · the old board-folder sessions stayed in their old project folder, and `claude --resume <old sid>` from the root cannot find them.
  · copying the 6 jsonl files into the root's project folder was tried, and **resume still refused**.
    The file did not grow after a command, because a session is tied to the folder it was born in, and moving files does not fool it.
So this time each question's old `session:` line was cleared and each was restarted under the root with `--session-id`.
The old sessions are not deleted. They are still in the board folder's project folder, and to read one you `cd` into that folder and run `claude --resume`.
**Lesson**: the working folder is a session's home, not a setting you can change. Change it and this question starts over.

#### Set the id yourself on the first open, and never let it make its own.
A bare `claude` invents a new session id that we cannot catch, so one question ends up with several sessions.
With `--session-id <uuid>` we make the id first, write it into the header first, and only then let the terminal use it.
That is how one question, one session holds.

#### Only 5599 is forwarded, so the terminal has to go through the proxy, WebSocket and all.
Forwarding one more port per question is not realistic.
ttyd's `-b <base>` puts it under a subpath, and serve.py has to handle `Upgrade: websocket` as well as plain HTTP, because all terminal input and output rides the WebSocket.
Only a correctly forwarded handshake gives you a stream of characters.

#### Look for an existing wheel first, but "it exists" is not "use it".
The myrlin-workbook discovery path matched where we store things, byte for byte, and for a moment it looked ready to plug in.
But it is a whole application, and what we needed was a terminal sitting inside a board.
The smaller ttyd plus our own proxy won.
Looking for a wheel is right. Picking one is about how big the piece you need is, not how much the wheel can do.

## Glossary
TUI: the text screen you type into, the real command line, shown inside the page.
PTY: the real terminal process on the server, the thing your typing and its output run through.
ttyd: a small tool that turns a command-line program into a web terminal you can use.
`-i` sets the address, `-b` puts it under a subpath, and `-W` lets you type. Since 260731 ttyd is used only on the `--ttyd` fallback.
reverse proxy: on that fallback serve.py passes `/_term/<key>/…` requests through to the local ttyd, word for word.
Either way the browser talks only to 5599, because the normal engine ends the WebSocket in serve.py itself.
WebSocket / Upgrade: one connection that stays open and carries characters both ways.
Every keystroke and every line of output rides it.
AGPL-3.0: myrlin's licence.
It is fine to use as a tool on its own. The rules bite when you copy it into something you give out.

## Discussion
> JL: I wonder if we could add this too, a terminal icon?
> JL: and I want each question page to have a terminal that is its own.
> JL: I don't know whether the myrlin package could help you, github.com/therealarthur/myrlin-workbook
>> CC0723: read its source: the discovery path matches ours exactly. But it is a whole application, too heavy; ended with ttyd + serve.py's own proxy embedded instead.


### From the retired States section (merged 260831)
### 🔁 Coming back to a parked terminal
Built, and it lives in the page.
The ⌨ in the chat panel header opens the terminal, and clicking again (💬) hands the session back.
- 260801 JL · 🩹 The mangled screen was the saved text, drawn at the last viewer's width
  JL: "整个页面都是乱的，我不知道为什么会非常非常乱."
  A new client is sent the whole saved buffer the moment it attaches, and only AFTER that does it say how wide it is.
  So bytes drawn for the last viewer's size land in this viewer's grid, and every cursor move to a fixed spot is off.
  Setting the right size does not repair it.
  A full-screen app only paints again on a CHANGE, and the size it is handed is usually the size it already has, so the mess stays until something else forces a redraw.
  On attach the width is now nudged by one column and back on the first size message, and that is a real change either way.
  So the app paints its whole screen at the size this browser really has.
  Checked the hard way: attach at 54 columns, shrink the window, reload so the replay is certainly at the wrong width, then read the screen back.
  It came back an 87x29 grid against an 87x29 PTY, with no escape leftovers, no over-wide lines, and a clean screenshot.
  Two earlier fixes belong to the same symptom and do not explain it on their own.
  The tab strip took rows above the pane after the fit had run, and a size watcher now refits on any pane change.

- 260801 JL · 🧭 One place to pick a session, not two
  JL: "你为什么不把这个 session 放到那个 session 的选择那里去?"
  The tab strip added a second place to pick a session when the picker already did that job, and it was also what took rows from the pane, so it is gone.
  The session picker now owns the job.
  A session with a live terminal is marked `⌨` and reads `terminal running` or `terminal parked`.
  Clicking one attaches that terminal at once instead of promising to next time, and `＋ New session` starts another right away.
  Since this round the server keys terminals by (page, session), so attaching one no longer kills the other.
  The old key was per page, and that is why switching used to end the terminal you were in.

- 260801 JL · 🎨 The TUI was black and white because it took `NO_COLOR` from its parent
  JL: "why the TUI is black and white? not colored?"
  The spawn already forced `TERM=xterm-256color` and `COLORTERM=truecolor`, so the terminal claimed full colour while drawing none.
  That made it look like an xterm theme problem rather than an environment one.
  `serve.py` is usually restarted from a tmux or agent shell that sets `NO_COLOR=1`.
  `NO_COLOR` is the standard way to turn colour off, and every colour library obeys it, Claude Code included.
  It beats `TERM`, and it was passed straight down into the PTY.
  The spawn now drops `NO_COLOR` and sets `FORCE_COLOR=3`, in the same block that already strips the `CLAUDE_CODE_*` child-session marks, and for the same reason.
  The parent's choice is about the parent's own output, and this PTY is a browser window.
  Checked by tapping the terminal WebSocket and scanning the incoming bytes for colour SGR codes, with the server started under `NO_COLOR=1` on purpose so only the code fix was on trial.
  It found 43 colour codes, including Claude's own `38;2;255;153;0` orange.

- 260801 JL · ⌨⌨ One keystroke typed two letters, because input was tied to the SOCKET
  JL: "why for the CLI, I enter the one letter, it will type two letters?" with `what happened?` arriving as `wwhhaatt hhaappppeenneedd??`.
  `connectWS()` added `termT.onData(...)` every time it ran, and it runs again on every reconnect while the xterm object stays alive.
  So one dropped connection left two live listeners on one terminal, and every keystroke was sent twice.
  A second drop would have made it three, so the doubling showed up only after the terminal had been open a while.
  The listeners can be thrown away, so the old pair is now dropped before the next pair is added.
  They send through the CURRENT socket instead of the one they were born with, and closing the terminal drops them too.
  Checked by tapping `WebSocket` before the page scripts ran, forcing one reconnect, and counting sends per keypress: sockets went from 1 to 2, and sends stayed at 1.

- 260801 JL · ⌨ The same fix, done properly, after JL reported it still broken
  The first try above was checked on ONE path and shipped as if it worked everywhere, which it did not.
  Two faults survived it, and both were the browser guessing at something only the server knows.
  The save hook watched the classes on `#chat`, but opening the terminal sets `termon` on `<body>` and touches nothing on `#chat`.
  So opening the TUI never recorded itself, and the flag was only there when `pagehide` happened to run.
  The alive check compared file names from `/_board/terms`, but a group or board terminal is filed under a FOLDER such as `QD-working`, while the chat panel's `cq.file` is `board.md`.
  At those two levels it always decided no terminal existed.
  The server now answers both. `POST /_board/term-probe` finds the target with the same `term_key` the list uses.
  A parked terminal counts as present, because parking is exactly what a reload does.
  Checked on all four paths this time: page, group, board, and a real browser refresh instead of a scripted `location.reload()`.

- 260801 JL · ⌨ The view now survives a reload, because the process always did
  JL: "when I use TUI and when I come back it became the GUI again, in truth the TUI is running, why it is not kept?"
  The PTY was never the problem.
  A reload sends `park:true`, which keeps the process and its pump alive and only drops the WebSocket, so the terminal was still there every time.
  What was lost was the chat panel's VIEW.
  It is rebuilt on every load, and it was always rebuilt as the chat box, so the page showed the SDK chat while the TUI chat was the one holding the session.
  The panel now records which half it was showing, and on reload it reattaches to a terminal that `/_board/terms` still lists.
  It never starts one, so a reload cannot start a process nobody asked for.
  Reproduced first, then checked.
  Before the fix a reload came back with `termOn:false` and no xterm while the PTY was alive, and after it the same reload comes back with the terminal in place.
  One trap worth writing down: `/_board/terms` is a POST, and calling it as a GET returned 404 into a swallowed catch, which quietly made the reattach decide no terminal existed.

- 260801 JL · 🏷 Renamed and re-cut around what is still open
  JL: "We can call it SDK chat version, and TUI chat version" and "could you rethink about the Q in QD?"
  The Opening used to ask whether a real terminal per page could exist at all. It can.
  It now asks what the board owes a process that it wraps but does not draw, which is the join that failed on 260731.
  Nothing in `QF4` tests this version yet, and that gap is why its state stays 🟡.

- 260801 CC · 📱 Phone input looked at and written down, with nothing changed yet
  Chat gets a real textarea and its own phone layout. The raw TUI gets neither.
  `termOpen()` waits for `POST /_board/term` and for xterm to load before `termT.focus()` runs, so focus lands after the touch that started it.
  That is a known iOS keyboard rule, not proof that the PTY or the WebSocket lost the typed bytes.
  The next change should ask the reader for one clear tap on the live terminal to take focus, and should tie xterm's fit to the visible part of the screen.
  It needs a check on a real phone before anyone calls it fixed.

## Log
- 📖 260816 · [REVISE-CC, JL ruled] the page was rewritten in plain words, for a reader with ADHD whose English is a second language (JL: "我真的读不下去"). The 🧭 Outline tab had been showing this page's own sentences back, and they were unreadable, so the tab was right and the prose was not. Every division title now names its consequence instead of a mechanism, each one gained a `📌` line saying in one sentence what the part settles, and every aim, `Done when:` and State row was replaced with a short plain-word version. House words went with them, `division` to part, `store` to list, `render` to read or draw, `seed` to suggest, `mint` to build. Measured with `haipipe-writing`'s `cli/score.py`: 81 sentences flagged before, 20 after, every one that remains inside this Log, which is history and was not touched. No fact, id, `§` mark or section changed; only the words.
- 260806 2143 · [REVISE-CC] swept to the 260806 architecture; head method, Diagram, Files and Glossary now name serve.py's own-PTY engine (ttyd = --ttyd fallback), ⑤ grace release marked BUILT (0.71.0), the QD2-M1 blocker on the smooth pane cleared (M1 landed 260731), and the 🔑 re-key line numbers refreshed against live/term.py (581/503/789; all four lookups verified still page-only)
260802 · A4.1 closed, and the lesson is worth more than the row. The terminal reattach after a reload was reported by me twice as broken, first as coming back empty and then as non-deterministic, and it was correct both times. The empty screen is the CLI repainting on reconnect. The coin-flip was the CHECK clicking `>_ TUI` unconditionally: the strip's buttons are a radio with an off position, clicking the lit one puts the chat away, and whether it was lit depended on what the previous run left in `board-split-chat`, so the suite was closing the pane it meant to open, about half the time. Click-only-if-not-lit, and it is four for four. The rule this leaves: when a UI control is a TOGGLE, a test that clicks it without reading its state is measuring its own history, not the product
260802 · A4.1 corrected, and the correction is the finding. The terminal does NOT come back empty after a reload: same key either side, 1,300 characters replayed from the ring, parking working as designed. The missing `echo` is the CLI repainting on reconnect, which is what a full-screen app does. What is real is that the reattach is not DEPENDABLE, three outcomes from identical code in one sitting, including one where no terminal returned inside sixty seconds. Also learned, and worth keeping: the shell mirrors the page frame's path into its own address, so a test that moves the page frame and then reloads is asking for a DIFFERENT page's terminal, and asserting sameness across that is the test lying rather than the terminal failing
260802 · The messy terminal layout was found, measured and fixed. Inside the chat pane xterm held a 501px screen in a 16px box at a fixed 64 columns, because `fitTerm` measures `.tm` and the pane's fixed positioning left that element reporting only its padding, so the small-box guard returned on every call. It now falls back to the frame's viewport and watches its own box with a `ResizeObserver`, since dragging the split handle resizes a frame without firing `resize` in it. Columns now track the pane: 64 at 520px, 102 at 820px, 36 at 300px, 47 by 11 on a phone, no sideways scrollbar anywhere. Recorded as A4.2 and asserted in `checks/switchback.mjs` S3
260802 · `checks/tuichat.mjs` written, the first check this page has ever had, and it found the one rough edge on the terminal side. U1 the terminal opens on this question · U2 what you type runs and its output comes back, using `echo` so it costs nothing · U3 moving the page pane leaves it and its scrollback alone · U4 a full shell reload. U4 is the finding: the terminal comes back and it comes back EMPTY, and across runs it is not dependable about returning inside sixty seconds. Parking exists and `term.py` replays a 256KB ring on reconnect, so the machinery is there and the reattach is not reaching it. Recorded as A4.1 rather than asserted, because a flaky red teaches nothing
260802 · Added `## Content` with the usage half a reader actually needs, on JL's ask that QD2 and QD3 both say how to use the two chats smoothly. It states when to reach for the terminal rather than the drawn chat, that the strip's `>_ TUI Chat` and `💬 GUI Chat` are ONE radio handing the same question back and forth under `QD1`'s Law rather than two windows, and what survives what: a page-pane navigation leaves the terminal untouched because it is a different frame, and a shell reload parks the PTY rather than killing it. The handover is driven and asserted in `checks/guichat.mjs` T17, so a broken one is a failing check instead of a surprise
260801 · JL: "他已经在跑了，为什么我看不到？我切完之后，他那个状态全都没了" Root cause found and it is an ENGINE defect, not a form one: the 260801 (page, session) re-key changed where terminals are REGISTERED (`term_key(f, sid)`, term.py:538) and left four lookups on the old page-only key (`hold` 398/408, `park` 460, `kill_term` 734), so they cannot match by construction. `hold()` therefore rules a live terminal's claim void and lets the drawer open a second writer on the same `.jsonl`, which is how switching loses the state. Proven by key arithmetic (live `47d8ca068ee1` vs page-only `f891ba932470` for the same page) and by `/_board/release` returning `closed:false` on a terminal `/_board/terms` listed as alive. Fix drafted, not applied: it needs a serve.py restart, which ends every running terminal, so JL picks the moment
260801 · JL retired `QD7` (the board-level agent): its premise expired when `QD1` settled three attachment levels, so the page is archived rather than narrowed as CC had proposed. Closes this page's 🧭 Decision Now item
260801 · Design half split out as `QD4` after JL's phone session: this page keeps the engine, QD4 takes the form. The 📱 item handed over, Boundary now names the seam. Three diagnoses recorded there, all read from code and none yet confirmed on a device: the doubled keystroke on a phone is a THIRD cause (the IME's composition path, not the twice-fixed listener duplication), a correct repaint at ~46 columns is still unreadable, and the freeze after switching away is `pagehide` registered in three files with `pageshow` in none
260801 0020 · QD3m merged in on JL's ask: smooth-pane items absorbed (route D adopted per the no-decisions rule), the file archived under `_archive/`, board.md's lane and map updated, pty_e2e default target repointed (0.91.1)
260731 1934 · ⌨'s hard items became STANDING checks (`checks/run.py --full`, 0.89.0, home on `QC8`): the own-PTY engine and ⑤ park/reattach are re-proven on every run, a real CLI turn through the PTY (pty_e2e ①–⑦), park-not-held on tree navigation (termnav T9c/T9d `reused:true`), paste on a tree URL, all on a throwaway fixture, never a real page
260731 1905 · ⌨ follows the tree router (0.86.0): `follow()`'s split-page/group branches had no terminal hand-over, so tree navigation switched the drawer label while the OLD page's claude kept the screen and its PTY stayed unparked; both branches now park-rebind-reopen like the hash branch, and all three `termRelease` sites pass the group (a group PTY was parking the wrong scope). Found by reading SDK-Talk's navtest coverage on JL's ask, their suite never opens ⌨, and proven with `termnav.mjs` (same CDP harness): 12/12, parked-not-held shown by `reused:true` reopens, paste re-proven on a tree URL
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

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0
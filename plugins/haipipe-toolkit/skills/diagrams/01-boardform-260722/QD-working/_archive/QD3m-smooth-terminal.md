# Smooth like myrlin: render the session, not the screen
state: 📦 MERGED into QD3 · 260801, JL: "should we just keep one of them?" — the engine half (§8) had already shipped into QD3, the picker/paste items were built, and the open smooth-view work moved to QD3's 🪄 smooth-pane items; this file is the archive of the myrlin analysis (routes A–D, §5–§8, the P0 run-beside trial) and stays readable, never deleted
owner: JL
method: tail the question's jsonl into a rendered transcript; keep the PTY as the engine and the fallback; pick the route before building
session: b7573f60-7c0f-4fb1-a75d-e5b1a1384485
## Opening
Can the question's real CLI feel as smooth as myrlin, without giving up that it IS the real CLI?
The working answer is a third front end: render the session's own `.jsonl` as web chat (markdown bubbles, collapsible tool cards, diffs as diffs) while the CLI engine underneath stays verbatim, with the raw TTY one toggle away.
What turns on it is the route decision below: `QD3`'s remaining polish items only manage the TUI's repaint defects, while this form would remove the whole class, because there is no screen to repaint.


## Diagram
```
   ╔═══════════════════════════════════════════════════════════════════════════╗
   ║  ⚖️  LAW  ·  one scope  ·  one CURRENT session  ·  one live window          ║
   ║        (QD1's Law, rewritten 260731)                                       ║
   ╚═══════════════════════════════════════════════════════════════════════════╝
        📁 scope = a page · a group folder · or the board
        🗂 older sessions wait in the picker — only ONE window is live at a time
                                   │
                                   ▼
   ┌───────────────────────────────────────────────────────────────────────────┐
   │ 📄 ~/.claude/projects/-Users-…-Physician-SPACE/<uuid>.jsonl                │
   │    the CURRENT id, read from the page header · 🔁 picker swaps which THIS   │
   └───────────────────────────────────────────────────────────────────────────┘
                                   ▲
                 every front end below is just a VIEW of THIS one file
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
   ┌─────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
   │ 💬 QD2 DRAWER   │  │ 🪄 QD3m SMOOTH VIEW  │  │ ⌨  QD3 RAW TERMINAL  │
   ├─────────────────┤  ├──────────────────────┤  ├──────────────────────┤
   │ 🔧 rebuilt chat │  │ ✨ jsonl rendered as │  │ 🖥️ the TUI verbatim  │
   │    box          │  │    web chat          │  │                      │
   │ 🧠 SDK engine   │  │ 🧩 CLI engine below, │  │ 📟 xterm + ttyd +    │
   │ 🔒 gated verbs  │  │    untouched         │  │    proxy             │
   │                 │  │ 🫧 bubbles · cards · │  │ 🧷 nothing missing   │
   │                 │  │    diffs-as-diffs    │  │                      │
   ├─────────────────┤  ├──────────────────────┤  ├──────────────────────┤
   │ 🟡 smooth,      │  │ 🟢 smooth AND full   │  │ 🔵 full, not smooth  │
   │    not full     │  │                      │  │                      │
   └─────────────────┘  └──────────────────────┘  └──────────────────────┘

   ⌨️  input     🪄 types text into the SAME session (ttyd WS already built)
   🚪 fallback   any TUI-only moment (permission dialog · picker)
                 ─ ─ ─▶  one toggle hands the screen to ⌨
```

## Content
### 1 · What myrlin's smoothness actually is
Myrlin never draws a terminal: it reads the session transcript from disk and renders it as structured web chat.
That single move buys everything that felt smooth: no PTY repaint, so the whole `QD3` smear class (unicode widths, font metrics, interleaved frames) cannot occur by construction.
Markdown, code, and diffs become web objects instead of character grids; tool calls become collapsible cards; input is a real text box that handles IME, paste, and multiline for free.
The proof it fits us is already on `QD3`: myrlin's session discovery path matched our storage location byte for byte (260723), meaning the jsonl alone is enough to reconstruct the conversation.

### 2 · What this board already owns that the form needs
`QD1` gives the scope its CURRENT session, its uuid in the page header and the rest of its history in the sidecar, so the jsonl to render is always known and the 🗂 picker can point the view at an older one.
`QD3` gives the input pipe: the ttyd WebSocket through 5599 already delivers text into the live session, and `--resume` restores it after any drop.
`QD2` gives the drawer chrome the view would live in.
Nothing about the engine changes; this page is only about the screen.

### 3 · The three routes
- A · keep polishing the raw TTY
  `QD3` ⑤ grace release and ⑥ WebGL plus whatever comes next; the ceiling is that a TUI repaint can be managed but never removed.
- B · render the jsonl, keep the CLI engine
  A transcript pane tails the question's jsonl and renders it; typed input rides the existing ttyd WS into the same session; the raw TTY stays one toggle away.
- C · adopt myrlin-workbook itself
  Rejected 260723 on `QD3` (whole application, AGPL, its own service) and the reasons have not changed; it stands rejected.
- D · hold the process and read its stream, added 260731 from the VS Code extension teardown (`QD2`)
  serve.py keeps `claude --input-format stream-json --output-format stream-json` open per question and writes into its stdin, which is exactly how the extension drives its bundled CLI.
  It reaches route B's destination without the tail: live structured events instead of a file to watch, no boot cost per message, and the permission channel intact.
  The jsonl tail exists in myrlin because myrlin does not own the process; we do.
  D and the §8 PTY plan are not rivals, they are the two halves of the same drawer: §8 owns the RAW pane (a real screen, for the TUI-only moments this page's §4 says cannot go away), and D owns the SMOOTH pane (structured events, no screen to repaint).
  Two processes per question would break `QD1`'s one-window rule, so whichever pane is open holds the question's process and the toggle hands it over.

### 4 · The hard edge: TUI-only moments
Permission dialogs, option pickers, and interactive command screens exist only on the PTY screen, never in the jsonl.
So the smooth view cannot be the ONLY front end: it must either detect the waiting-on-TUI state and surface the ⌨ toggle, or accept that those moments happen in the raw pane.
Designing that seam, not the rendering, is the real work of route B.

### 5 · Read from the code, 260731
Cloned and read the real source (AGPL-3.0: the design is learned from, the code never copied).
The mirror is our route B, production-hardened: a byte-offset jsonl tailer that never re-reads the file (their corpus holds a 1.86GB transcript), `fs.watch` on the parent directory with a debounce plus an fstat poll fallback, a capped tail-window on first open, and SSE batches carrying offset/prevOffset so a client detects gaps and re-opens idempotently.
Liveness is mtime-based ("recently wrote the transcript", not "process running"), which is exactly the signal a drawer's 🟢 live dot wants.
The session picker is `discover()`: walk `~/.claude/projects/<encoded-cwd>/*.jsonl`, title from a custom-title entry or the first message, sorted by mtime, size shown.
Paste is text-only into the PTY and drag-drop moves sessions between workspaces, so the image ask below goes beyond myrlin.

### 6 · The two asks of 260731, designed
- The history picker (JL: "when I open the chat, I think I can choose the chat history, and then talk with it")
  Opening 💬/⌨ on a question that has history offers: continue the current session · resume an older one · start fresh.
  Candidates come from a serve.py sidecar map written at mint time (serve.py already generates every id it hands out, so it can record question → ids as they are born); title, last-active, and size are read from each jsonl, myrlin's `discover()` shape.
  The page header keeps only the CURRENT id, honoring `QD1`'s "the board's md records outcomes only"; every resume passes the hollow-session check first (`QD3` Lesson).
- Image paste (JL: "the ability to paste the images")
  The browser paste event carries the blob in `clipboardData.items`; `/_board/paste-image` writes it server-side and returns the repo-root-relative path (sessions sit at the SPACE root per `QD1`'s Law, so the path resolves).
  The terminal front end then types the path into the PTY for the Read tool; the SDK drawer can attach a real image block instead.
  Landing pasted images under the board's `fig/` keeps a pasted sketch attachable to a page later (`QD5`).

### 7 · Reusing myrlin: three modes, one ruled out
Myrlin is AGPL-3.0 and `Tools` is a distributed GitHub repo, so copying any myrlin file into `haipipe-board` would relicense the family; that mode is ruled out.
The two live modes: 📦 RUN BESIDE, the whole app unmodified as its own service (exactly how ttyd is used today), and ✍️ BY DESIGN, rewriting a small piece from its contracts.
Mapped onto the pieces: the picker (`discover()`, 124 lines), the jsonl parse, and the byte-offset tailer are each an afternoon of our own Python by design; the transcript UI and the PTY are already ours (drawer bubbles, ttyd); the only thing worth running as real myrlin code is ALL of myrlin, beside serve.py, for whole-corpus session browsing.
Phases: P1 picker + Law + resizable drawer (no myrlin code at all) → P2 the mirror read-half (`/_board/mirror`, offset/prevOffset contract, mtime liveness) → P3 input through the existing ttyd WS plus the TUI-only seam; P0 optional at any time, `npx myrlin-workbook` linked from the board.

### 8 · The replacement plan: serve.py owns the PTY, myrlin's method in our code (JL 260731: "how could we replace current CLI version to use the method of myrlin")
What myrlin's terminal actually is, once read: node-pty inside its own server, spawning `claude --resume` itself, streaming raw bytes over its own WebSocket to xterm, with a server-side ring buffer replayed on reconnect.
No ttyd anywhere; the server IS the terminal backend.
The same shape in Python is the standard library: `pty.openpty()` + `subprocess` + `fcntl TIOCSWINSZ`, terminated at the WS endpoint serve.py already routes.

The one trick that makes this cheap: KEEP ttyd's wire protocol as our own contract.
`board.js` already speaks it (auth JSON, size JSON, input `'0'+data`, resize `'1'+json`, output frames leading `'0'`), so the front end needs near-zero changes; only the party at the other end of `/_term/<key>/ws` changes from a proxied ttyd to serve.py itself.

- M1 · PTY core in serve.py
  `spawn_pty(f)`: openpty → `claude --append-system-prompt … --resume|--session-id` on the slave side, cwd = SPACE root; per-question registry replaces TERM_DIR sockets; resize = TIOCSWINSZ + SIGWINCH.
  A ring buffer (last ~200KB of output) per terminal, myrlin's reconnect trick: a rejoining client gets the recent screen instantly instead of a blank pane waiting for repaint.
- M2 · The WS endpoint flips from relay to terminus
  `/_term/<key>/ws` keeps its URL and its wire protocol; `proxy_term`/`pump` retire; the reader thread pumps master-fd → all attached WS clients, input pumps back.
  ttyd stays installed as a fallback behind `--ttyd` until M3 verifies, then the dependency (brew install, socket files, `-b` subpath quirks) is deleted.
- M3 · Lifecycle unchanged, then verified
  HOLD, the session picker's `session:` parameter, pagehide beacon, killall, startup sweep: all keep their routes; reaping simplifies to killing our own child.
  The QD3 verification bar applies verbatim: end-to-end through 5599, two questions at once, release-under-feet self-heal, and the emoji-dense repaint fixture.
- M4 · What owning the PTY newly unlocks
  Image paste into the raw terminal (serve.py types the saved path into the master fd itself, the missing half of the 🖼 item); server-side idle keepalive; and the P2 mirror can later read the SAME process's output without a second attach.

Cost estimate: M1+M2 ≈ 150-200 lines in serve.py, minus ~90 lines of retired proxy/socket code; board.js diff ≈ a dozen lines.
Risk: PTY edge cases ttyd already solved (flow control, orphan reaping on crash, TERM env); the `--ttyd` fallback flag is the insurance until the fixture passes.

## Items to Finish
### ✨ The smooth view itself
- [ ] 🪄 Route decided by JL
      The A · B · C call sits in Decision Now below.
- [ ] 📜 Prototype the read half
      Tail one question's jsonl and render bubbles, tool cards, and diffs in the drawer; no input yet.
      The emoji-dense content that smeared `QD3` (state pills, 💬 markers) is the fixture: it must render clean by construction.
- [ ] ⌨ Settle the input path
      Candidate: text through the existing ttyd WS (arrives as if typed); alternative: one `claude --resume -p` turn per message.
      The WS path keeps one live process and is the lean; the -p path forks a process per turn and loses TUI state.
- [ ] 🚪 Settle the fallback seam
      Define how the view detects a TUI-only moment and hands over to ⌨, and how it takes the screen back.

### 🗂 The session picker and image paste
- [x] 📜 Build the session picker on open
      BUILT 260731 as haipipe-board 0.62.0, the same round JL amended `QD1`'s Law.
      `POST /_board/sessions` lists current + sidecar history with jsonl metadata; the drawer's 🗂 Session strip picks; `/_board/chat` and `/_board/term` take `session:"<uuid>"|"new"`, so the picked session reaches the ⌨ terminal too; hollow-session check on every resume.
- [x] 🖼 Build image paste
      Drawer half BUILT 260731: paste into the chat textarea rides the existing `/_board/image` into this board's `fig/`, and the message gets a repo-root-relative path claude can Read from the SPACE root.
      Terminal half BUILT with the own-PTY switch (0.64.0): paste over the ⌨ pane saves through the same `/_board/image` and types the path into the PTY; press Enter to send it to claude.

## Where we are
Opened 260731 from JL steering back to `QD3` with "how could I make it as smooth as myrlin"; nothing is built, and the route is the first call.
The id's `m` is mnemonic for myrlin, JL's pick, a deliberate deviation from the `a`-ladder used on `QB4`/`QB5`.

- 260731 JL+CC · ⚖️ The Law line on this page's Diagram was retired; the rewrite lives on `QD1`
  JL quoted this page's Diagram line, "one question · one session · one jsonl (QD1's law)", and ruled on it: "this law should be updated. It is actually very old."
  All three terms had moved under it: group and board sessions made SCOPE the unit, JL's own picker amendment made it the CURRENT session, and the history of jsonls followed from that; the surviving invariant is the window.
  `QD1` now reads **one scope · one CURRENT session · one live window**, and this page's Diagram quotes that, with the picker and the one-window clause drawn in.
  Nothing on this page's route argument changes: the smooth view renders whichever jsonl is current, and §4's TUI-only seam is untouched.

- 260731 JL+CC · 🔩 The §8 replacement SHIPPED: serve.py owns the PTY, ttyd is now the fallback
  JL approved route A and haipipe-board 0.64.0 delivered it: `spawn_pty` (stdlib `pty` + `os.login_tty`), a per-terminal reader thread with a 256KB ring buffer and a UTF-8 tail guard (half an emoji is never split across frames, the QD3 smear's cousin), and `/_term/<key>/ws` terminated by serve.py itself, RFC6455 handshake and all, still speaking ttyd's wire protocol so `board.js` needed zero changes on the wire.
  The seven-step live test passed in 24s: spawn, handshake, TUI boot, a REAL turn (PTYOK round-trip through this very page's session), resize, a second client receiving the full ring replay instantly, and a clean release; two questions then ran side by side and `killall` reaped both with no orphan process or pidfile.
  ttyd survives only behind `serve.py --ttyd`, the insurance fuse until JL's own click-through; the brew dependency is deletable after that.
  Terminal image paste landed with it: the ⌨ pane now accepts a pasted screenshot, saves it to the board's `fig/`, and types the repo-root-relative path into the PTY.
- 260731 JL+CC · 📦 P0 trialed live: myrlin's terminal CAN drive board sessions
  JL asked to use myrlin's terminal itself; CC ran the cloned source beside serve.py (its own service, unmodified, AGPL untouched) and proved the chain: it discovered all 149 SPACE-root sessions with real titles, and its node-pty pane spawned `claude --resume` on QD1's session in the right cwd, then stopped clean.
  One data-side fix was needed, no myrlin code touched: its path decoder trusts the first jsonl carrying a `cwd`, and the failed 260723 migration copies in our project dir made it guess wrong; writing `sessions-index.json` (`originalPath`) into `~/.claude/projects/-Users-…-Physician-SPACE/` pins resolution #1 and fixed discovery.
  Now running for JL at the tailnet on :3457 with the saved `~/.myrlin` password.
  The standing caveat: myrlin cannot see the board's HOLD, so one window per session across BOTH apps stays JL's discipline; the board only guards its own front ends.
- 260731 CC · 🛠 P1 landed as haipipe-board 0.62.0, under the Law JL amended the same day
  serve.py records every minted id in the gitignored sidecar (`.haipipe-board/sessions.json`), `POST /_board/sessions` lists current + history with jsonl metadata, and chat and terminal both take `session:"<uuid>"|"new"`; picking resumes that session and the header follows it.
  The drawer grew the 🗂 Session strip (current · history · ＋ new, self-opening when there is a real choice), a drag-resize handle on its left edge (`--chatw`, persisted per machine), and image paste in the chat textarea.
  Verified live on 5599: QD1's session listed with its title, an explicit resume left its header untouched, and "new" minted the `session:` line this very page now carries.
  Left open: the route and reuse-mode rulings below, the mirror (P2), the input seam (P3), and JL's browser click-through after a reload.
- 260731 JL · 📜🖼 Two asks joined the page, grounded in myrlin's actual source
  JL asked for a chat-history picker on open ("choose the chat history, and then talk with it") and for image paste; CC cloned myrlin-workbook and read it the same round.
  The code confirmed route B's shape at production grade (Content §5), gave the picker its `discover()` pattern, and showed image paste is beyond myrlin (its paste is text-only); both designs are in Content §6.
  The picker touches `QD1`'s Law ("One Q ⇄ one session"), so the amendment ruling sits in QD1's Decision Now, not here.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [ ] 🪄 Pick the route to myrlin-smoothness
      A · the raw TTY is polished further; the ceiling is that repaint defects can be managed but never removed.
      B · the jsonl is rendered as web chat and the CLI engine is kept; a transcript pane tails the jsonl while typed input rides ttyd into the same session.
      C · myrlin-workbook is adopted wholesale; it is an AGPL application with its own service, rejected 260723 and reasons unchanged.
      D · the process is held open and its stream is read directly; this reaches B's smoothness without tailing a file, with no boot cost per message, and the permission channel intact.
      → CC's proposal changed to D on 260731, after reading the VS Code extension: it reaches B's destination with no file to tail, no boot cost per message, and the permission channel intact, and it is the same architecture `QD2` is now being asked to adopt.
      The prior lean was B; it stands as the fallback if the held process proves hard to keep alive.
- [ ] ⌨ Rule the raw TTY's standing under B
      A · the TTY stays permanently accessible via toggle; permission dialogs and pickers are handled in the raw pane and the smooth view detects these moments and surfaces the toggle.
      B · the TTY is retired once the smooth view can handle TUI-only moments; permission dialogs and pickers would need to be rendered in the web interface.
      → CC's proposal: A; permission dialogs and pickers live only on the PTY screen, so the toggle is the seam that keeps "nothing missing" true.
- [ ] 📜 Pick the session picker's scope
      A · the picker shows only this question's own session history; you can resume older sessions for this one question but cannot attach sessions from other questions.
      B · the picker shows the whole repo's sessions myrlin-style; the list is large and floods the default view with sessions from other questions.
      C · the picker defaults to this question's history with an expander to the whole repo; the question's own history answers "continue where I was" while still allowing you to attach any session.
      → CC's proposal: C; the question's own history answers "continue where I was" and the expander still allows attaching any session, without flooding the default view.
- [ ] 🗃 Pick where the history is recorded
      A · serve.py writes a sidecar map (.haipipe-board/sessions.json) when each id is minted; the page header stays clean and only keeps the CURRENT id, honoring "the board's md records outcomes only".
      B · history lines accumulate in the page header; every session id is recorded there, making the header grow with every new session.
      → CC's proposal: A; `QD1` already ruled the board's md records outcomes only, and plumbing ids are not outcomes.
- [ ] 🖼 Pick where a pasted image lands
      A · pasted images land in `fig/` (or `fig/chat/`) inside the board folder, visible in the file tree and reusable as page attachments later.
      B · pasted images land in an invisible scratch dir and are swept periodically; they disappear after use and are never reused.
      → CC's proposal: A; a pasted sketch often becomes a page figure (`QD5`), and visible files match how this board keeps its records.
- [ ] 📦 Pick the myrlin reuse mode (Content §7)
      A · the whole myrlin app runs unmodified beside serve.py as its own service (like ttyd today); one integrated application handles session browsing.
      B · the drawer pieces are rewritten from myrlin's design without copying code; no myrlin code enters haipipe-board, and the phased build (P1/P2/P3) proceeds with only our Python.
      C · both modes coexist; B for the drawer (our own code following myrlin's contracts) and A as an optional corpus browser (the full myrlin app running separately for whole-repo session browsing).
      → CC's proposal: C; copying files is ruled out by AGPL either way, and P1 proceeds under any answer because it needs no myrlin code at all.
- [x] 🔩 Approve the ttyd → own-PTY replacement plan (Content §8)
      APPROVED 260731 by JL ("ok, go ahead and implement it"), option A; BUILT and verified the same round as haipipe-board 0.64.0, details in Where we are.
      serve.py owns the PTY itself, myrlin's method rewritten in stdlib Python, ttyd's wire protocol kept so board.js barely changes; M1-M4 with a `--ttyd` fallback flag until the QD3 fixture passes.
      A · M1+M2 are built now; the PTY is owned by serve.py immediately, an external dependency is deleted, and terminal image paste is unblocked, with --ttyd as a fallback.
      B · M1+M2 are approved but postponed until P2 ships; the work waits for the mirror feature to be built first.
      C · ttyd stays as the PTY backend; the external dependency remains and terminal image paste waits.
      → CC's proposal: A; it deletes an external dependency, adds reconnect replay, and unblocks terminal-side image paste, while the fallback flag caps the risk.

## Files
- `../../board/haipipe-board/serve.py`
  Owns the ttyd WS pipe the view would reuse for input, and would grow the jsonl tail endpoint.
- `../../board/haipipe-board/assets/js/10-drawer/30-terminal.js`
  Owns the drawer the view would render into; the xterm mount it would sit beside.
- `QD3-chat-terminal.md`
  The engine this page puts a face on; its Lessons are the defect class route B retires.

## Discussion
> JL: one question · one session · one jsonl (QD1's law) <--- this no longer work.
>> CC0731: right on all three terms, and the rewrite landed in `QD1` (its Law, Diagram, Boundary, and a Where-we-are entry), because the Law's home is there and this page only quotes it.
>> **question** → **scope**: group and board sessions ship, so the unit is a path, not a Q. **one session** → **one CURRENT session**: your own 260731 picker amendment. **one jsonl** → **one live window**: a scope now has a history of jsonls, and the part that actually still holds is HOLD.
>> This page's Diagram now carries the new wording; §2 and §4's reasoning are unaffected, since the smooth view renders whichever jsonl is current.

## Log
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · JL asked "could we make image paste doable?" and it already ships (0.62.0 drawer, 0.64.0 terminal); this round CLICK-verified both in a real Chrome (CDP + synthetic ClipboardEvent carrying a real File): drawer paste inserted `![image](fig/…)` into the input, ⌨ paste uploaded to fig/ and typed the repo-root-relative path into claude's prompt; the comment-box surface shares the same handler; no code changed, no version cut
260731 1642 · Diagram redrawn fancier via diagram-ascii (⚖️ Law banner, boxed jsonl node, three emoji-headed front-end panels with 🟡🟢🔵 status footers, dashed fallback arrow); wording unchanged
260731 · JL: the quoted Law "is actually very old"; Diagram, Boundary, and §2 updated to **one scope · one CURRENT session · one live window**; the rewrite itself was made on QD1, whose Law owns it
260731 · JL asked "did you clicked it yourself?": no was the honest answer, so CC clicked it in a real Chrome over CDP, reproduced the black pane, and traced it to the swallowed allowProposedApi throw (0.69.0); the clicked terminal now paints the full TUI, screenshot-verified
260731 · §8 SHIPPED as haipipe-board 0.64.0: serve.py owns the PTY (ring replay, UTF-8 tail guard, RFC6455 terminus, ttyd wire kept), 7-step live test + coexistence + killall all pass; ttyd demoted to --ttyd fallback; terminal image paste landed
260731 · Route D opened from the VS Code extension teardown on QD2 (hold the stream-JSON process rather than tail the jsonl); route lean moved B → D, and D was reconciled with the §8 PTY plan as the smooth half beside the raw half
260731 · Replacement plan drawn (Content §8): serve.py to own the PTY in stdlib Python, ttyd wire protocol kept, M1-M4 + fallback flag; approval row opened in Decision Now
260731 · P0 trialed live: myrlin run-beside on :3457 drove a real board-session resume; path decode pinned via sessions-index.json, no AGPL code touched
260731 · P1 shipped as haipipe-board 0.62.0 (picker + Law wiring + drag-resize + drawer image paste), verified against the live 5599; state → 🟡
260731 · Reuse plan landed (Content §7): copy ruled out by AGPL, run-beside or by-design remain, P0-P3 phases set; P1 execution started the same round
260731 · Cloned and read myrlin-workbook's source; picker + image-paste designs added (Content §5 §6); three Decision Now rows opened; QD1 asked to amend its Law
260731 · Opened as QD3m on JL's ask ("how could I make it as smooth as myrlin"), split from QD3's smoothness item; the m is mnemonic, JL's pick

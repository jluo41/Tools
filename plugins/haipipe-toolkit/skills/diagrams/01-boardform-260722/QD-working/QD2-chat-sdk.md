# The SDK chat version: a chat box drawn in the page, given what a terminal inherits
state: 🟡 PARTIAL
owner: CC
method: claude_agent_sdk + serve.py's /_board/chat; three selectable permission tiers (restricted / full·ask / full·auto)
session: 8c9903ba-dadb-4f00-bdd1-823986cac937
## Opening
What makes a chat interface that lives inside a page actually good to use?

This board has one, on the right of every page: it reads the page and edits it while you watch.
Because the Agent SDK gives it events instead of a terminal screen, every part of it is ours to design.
A terminal inherits its behaviour; a drawn interface has to be given all of it, and the parts nobody designed are the ones that break.
The test: you can work in it all day without wishing you were in the terminal instead.

**Why this matters**: Permission was the original question here and it is closed, with three selectable tiers shipped.
What is left is not a safety problem but a design one, and it does not show up in a design document, only in daily use.
The drawer scrolled the page instead of itself, opened at the top of the transcript, lost a reply when you looked away, and had nowhere to pick a session from.
None of those is exotic; each is one piece of behaviour a terminal never had to be given, and this page is the list of what still has to be.


## Writing Style
How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules all come from `QB4-overall.md` and are not restated here.
Read `QB4 § Writing Style` first; everything below is what this page adds on top of it.

**The axis is GUI against TUI (JL 260801)**: this page is about a chat box DRAWN in a browser, and `QD3` is the terminal.
Never argue from the CLI as if this were an imitation of it ("我们强调的不是 SDK 吗？…应该是 Graph UI 吧").
The terminal appears here only as the contrast, never as the definition.

**Every defect is written as a fact about where state lives**: a complaint arrives as a feeling about the interface, and this page's job is to say which code owns it.
"The drawer feels janky" is not a record; "`chatOpen` rebuilt every bubble from storage when the scope had not changed" is.

**Quote JL in the language he used**: a report keeps its original words, Chinese or English, because the wording is evidence of what was actually experienced.
Translating it into the page's own vocabulary loses the thing that made it a report.

## Diagram

```
  🌐 browser right-side drawer            🖥️ serve.py (on the machine the files are on)
  ┌────────────────────┐   📮 POST      ┌──────────────────────────────────────┐
  │ 💬 QD2  title       │ /_board/chat   │ 🤖 claude_agent_sdk                   │
  │ ┌ 💭 bubbles ─────┐ │ ═════════════► │  📂 cwd = SPACE root (whole repo)     │
  │ │ ⚡ streams live │ │                │  📖 reads the code it discusses,      │
  │ └────────────────┘ │ ◄───────────── │     not just the board folder         │
  │ 🔧 handle N cmts    │  📄 one JSON   │  🚦 can_use_tool ─ the gate (3 tiers) │
  │ 🧠 Opus4.8 / high   │  per line      │    🔒 restricted: this Q's files only │
  │ ⌨️ [input]  [⏹]    │                │    🙋 full·ask: prompts for the rest  │
  └────────────────────┘                │    🚀 full·auto: bypass, no prompts   │
                                        └───────────────┬──────────────────────┘
                                                        │ 🏗️ build.py after edits
                                                        ▼  ↻ reload the page to see it
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QD2

## Content
### 1 · What the extension's backend actually is (read from v2.1.220, 260731)
```
🧩 the extension is a HOST, not an agent
   ┌──────────────┐  📦 bundles   ┌──────────────┐  🚀 spawns  ┌──────────────┐
   │ 🖼️ webview UI │ ────────────▶ │ 🤖 Agent SDK │ ──────────▶ │ ⌨️ claude CLI │
   └──────────────┘               └──────────────┘             └──────────────┘
   ❌ no new agent   ❌ no new protocol   ✅ only a shell around an engine we run
```
The extension does not implement an agent, and it does not implement a protocol either.
It BUNDLES the TypeScript Agent SDK and drives it, which `extension.js` gives away verbatim in its option names: `pathToClaudeCodeExecutable`, `canUseTool`, `includePartialMessages`, `settingSources`, `permissionPromptToolName`, `forkSession`, `sessionMirror`.
Those are the same option names our Python `claude_agent_sdk` exposes, because it is the same SDK in two languages.

```
   webview/index.js    5MB    the chat UI: bubbles, diffs, tool cards. web chat, never a terminal
   extension.js      2.5MB    the host: bundled Agent SDK + VS Code glue + the IDE bridge server
   resources/native-binary/claude   245MB   a bundled copy of the ORDINARY CLI, spawned as a subprocess
   ~/.claude/ide/<pid>.lock          the bridge handshake: the EXTENSION listens on a WebSocket
                                     and the CLI dials OUT to it (transport: "ws" + authToken)
```

That 245MB file is not a special build and not a second product (JL asked, 260731).
It is the Claude Code CLI compiled to one Mach-O executable with the Node runtime and every dependency baked in, which is the whole reason for the size.
Verified on this machine: `shasum -a256` matches `~/.local/share/claude/versions/2.1.220` byte for byte, which is exactly what `claude` on the PATH symlinks to.
The extension carries a copy so it still works for someone who never installed the CLI; that is the only thing the copy buys, and we need no copy because serve.py already spawns the one on the PATH.

The spawn line is fixed and short, then one flag per set option:
`claude --output-format stream-json --verbose --input-format stream-json`.
Everything else is mechanical translation, the same table our options would produce: `--model`, `--effort`, `--thinking adaptive|disabled`, `--max-turns`, `--max-budget-usd`, `--setting-sources=…`, `--allowedTools`, `--disallowedTools`, `--permission-mode`, `--mcp-config`, `--resume=<sid>`, `--session-id=<sid>`, `--fork-session`, `--include-partial-messages`.

This page owns the DRAWER and nothing else: the three permission tiers, streaming, rendering, cost, its session handling, and every part of it a reader touches.
The rules it obeys about who may hold a session are `QD1`'s, the real terminal is `QD3` and its form on a small screen is `QD4`, and the shell that puts the drawer in its own frame is `QD5`.
Whether a reader can TRUST what the drawer shows, along BINDING · TURN · CONTINUITY · HANDOVER · INTERRUPTION, is tested by `QF4`, which is also where "were these fixes ever clicked in a browser" belongs.
How well this page is WRITTEN is `QB4`'s grammar and `QF1`'s checker, recorded here 260801 only because JL asked it on this page ("为什么你不 follow 我们现在的 guideline 呢… 这是哪个 Q 要管的事儿啊") and the answer is that it is not this page's to own.

### 2 · The protocol on that pipe
```
📡 ONE pipe, four kinds of newline JSON
   🗨️ assistant + deltas      ──▶  ✅ the half the drawer already renders
   🚦 control_request         ◄──  the CLI ASKING: a permission prompt
   ✔️ control_response        ──▶  our allow/deny, matched by request_id
   🛑 control_cancel_request  ◄──  plus 💓 keep_alive · 🪞 transcript_mirror
   🔑 setting can_use_tool is what switches the control half ON
```
One pipe carries four kinds of traffic, all newline JSON.
Assistant output and partial deltas come up as ordinary messages; that is the half our drawer already renders.
The other three are the half we do not use yet: `control_request` (the CLI asking, which is how a permission prompt arrives), `control_response` (our answer, matched by `request_id`), and `control_cancel_request`.
`keep_alive` and `transcript_mirror` frames ride the same channel.
Setting `canUseTool` is what turns the channel on: the SDK appends `--permission-prompt-tool stdio`, and every gate decision then travels as a control message rather than a side channel.

### 3 · The one difference that matters, named exactly
```
🧩 extension   ▶ ONE process, MANY turns   ⚡ instant follow-up
   turn1 ─┐
   turn2 ─┼──▶ 🤖 one live claude ──▶ 💬
   turn3 ─┘

🖥️ serve.py    ▶ one process PER TURN     🐢 8.1s first token · 💸 ~$0.9
   turn1 ──▶ 🤖 boot 🔥 ~150 skills ──▶ 💬 ──▶ 💀 dropped
   turn2 ──▶ 🤖 boot 🔥 ~150 skills ──▶ 💬 ──▶ 💀 dropped
                    ⬆ the WHOLE gap: we drop the client every POST
```
The extension's read loop runs ONCE for the life of a session and pushes each new user turn into the live process with `inputStream.enqueue(...)`.
That is what `--input-format stream-json` buys: stdin is a STREAM of turns, not a single prompt, so one process serves the whole conversation.
Our `ClaudeSDKClient` has the identical capability, and its own docstring names our exact use case ("Building chat interfaces or conversational UIs", "Multi-turn conversations with context").
serve.py throws it away: `chat()` opens `async with ClaudeSDKClient(...)` inside a per-POST `anyio.run(run)`, so every message connects, runs one turn, and disconnects.
That single line is the whole "not that good": the 8.1s first token and the near-$0.9 full-tier message are both the cost of reconnecting and reloading the ~150-skill registry per message.

The blocker is equally specific, and it is not the protocol.
The SDK forbids using one client across async runtime contexts ("you must complete all operations with the client within the same async context"), while serve.py runs a fresh `anyio.run()` per request inside `ThreadingHTTPServer`.
So holding the client means one long-lived event-loop thread owning every live client, with queues in and out; the HTTP handler stops owning the loop and becomes a producer and consumer of it.

### 4 · What "exactly the same as the extension" costs, in milestones
```
🔌 M1 the session host  ── unlocks everything below ──┐
   one daemon thread · one loop · SESSIONS[question]  │
                                                      ├─▶ 🎛 M2 streaming verbs
                                                      │      interrupt · set_model
                                                      │      set_permission_mode
                                                      │      get_context_usage
                                                      ├─▶ ⏪ M3 rewind_files()
                                                      └─▶ 🖱 M4 @-mentions · plan mode
   ⚠️ M4 is OURS to build; M2 and M3 are option flips once M1 lands
```
- M1 · the session host
  A daemon thread runs one asyncio loop for the process's life; `SESSIONS[question] -> {client, inbox, outbox}`.
  `chat()` stops calling `anyio.run`; it submits the message to the loop, then drains that session's outbox into the existing NDJSON stream, so the browser side changes not at all.
  Idle reaping and the `QD1` HOLD keep their current rules.
- M2 · the streaming-mode verbs, free once M1 lands
  Four `ClaudeSDKClient` methods work ONLY in streaming mode and are unreachable today: `interrupt()` replaces our flag that waits for the next message boundary, `set_model()` and `set_permission_mode()` switch mid-conversation with no reboot, and `get_context_usage()` gives the drawer a real context meter.
- M3 · rewind, the feature we had parked
  `rewind_files(user_message_id)` is checkpoints and rewind, listed on this page as "parked, it fights the LAW".
  It stops fighting: the amended `QD1` Law already allows many sessions per question, and rewind operates inside one session rather than forking a second history.
  It needs `enable_file_checkpointing=True` plus `replay-user-messages`, both option flips.
- M4 · the two UI affordances that are ours to build
  `@`-file mentions need a picker over the repo and a path injected into the message.
  Plan mode is `--permission-mode plan`, which M2's `set_permission_mode()` already reaches.

### 5 · Could we just use `extension.js`, and should we go JS? (JL asked 260731)
```
🐍 "the JS version" is THREE things, with three answers
   ❌ extension.js    require("vscode") throughout · cannot even LOAD outside the IDE
   🟰 the npm SDK     the SAME SDK in another language · 0 capability gained
   ✅ stay Python     47 options already cover every flag the extension emits
   🎯 the slowness is the DROPPED CLIENT, not the language
```
Three different things get called "the JS version", and they have three different answers.

- `extension.js` itself: NO, and not for taste reasons.
  It is a VS Code extension-host module that calls `require("vscode")` throughout, exports no public API, and ships as one 2.5MB minified bundle.
  Outside VS Code the `vscode` module does not exist, so the file cannot even load.
- The SDK it bundles: yes, reusable, and it is on npm as `@anthropic-ai/claude-agent-sdk`.
  But that is the SAME SDK as our Python one, so adopting it is a language change, not a capability change.
- Parity, checked rather than assumed: `ClaudeAgentOptions` in Python carries 47 options covering every flag the extension's arg builder emits, including `thinking`, `effort`, `task_budget`, `can_use_tool`, `include_partial_messages`, `fork_session`, `skills`, `sandbox`, `plugins`, and `enable_file_checkpointing`, plus `extra_args` as the escape hatch for any flag it has not mapped.
  There is no capability we would gain by switching.

So the recommendation is to stay in Python, and the decisive evidence is what else serve.py is (JL asked 260731, "what does serve.py do besides the claude code?").
It is 2938 lines across 20 HTTP routes plus the terminal WebSocket, and the chat is one job of seven.
Counting lines of method body per area:

```
   443  excalidraw     proxy the app · per-page frames · save scenes · hydrate and
                       stash embedded images · attach a drawing to a page   (QB4b, QD5)
   414  chat           the Claude Code bridge                                (QD2)
   390  activity       a SQLite focus-time database: spans per board, group,
                       page and actor, day-part aggregation, cross-board stats (QD6)
   334  write-back     every comment, lane, edit, discussion and resolve landed as a
                       typed line under its exact anchor sentence             (QB5)
   322  terminal       the PTY serve.py now owns, its WS terminus, ring buffer,
                       resize and reaping                                     (QD3)
   291  http           routing, headers, target resolution, and calling build.py
                       to regenerate board.html after every write
    48  image paste · HOLD locking · structure edits (add Q, add group, archive)
   ~670 module level   the four rules texts, prime_context, tool_brief, _slugify,
                       structure_op, the PTY helpers
```

Going JS therefore means porting an Excalidraw round-trip, a SQLite database, a sentence-anchor engine, and a PTY, none of which touch Claude Code, in order to change the language of the one part that already has full parity.
`build.py` `check.py` `xcal.py` `lanes.py` `skillpage.py` are Python as well.
The decisive point: the slowness is not Python against JS, it is that we drop the client every POST, so a language switch alone would fix nothing while holding the client fixes everything.

### 6 · The goal, stated properly: migrate the plugin ONTO the board (JL 260731)
```
   🧩 VS Code plugin                       🗒️ this board                      state
   ───────────────────────────────────     ─────────────────────────────────  ─────
   🖼️ webview/index.js   the chat UI  ─▶   board.html's drawer                  ✅
   🖥️ extension.js       the host     ─▶   serve.py                             ✅
   🔌 vscode.postMessage the wire     ─▶   POST /_board/chat + NDJSON           ✅
   🤖 bundled Agent SDK  the engine   ─▶   claude_agent_sdk  (same SDK)         ✅
   ⌨️ the claude binary               ─▶   the same binary, from PATH           ✅
   🏛️ the workbench      one long-    ─▶   QD5's shell: the chat frame is its   ✅
                         lived UI          own document, and it docks              260802
   🔁 the RETAINED       a hidden     ─▶   the ring: a turn survives its         🟡
      webview            panel keeps       reader, and a returning reader           A9.1
                         its state         re-attaches at a cursor
   🌉 IDE bridge (WebSocket)          ─▶   ❓ nothing yet, and this is the interesting one
```
The frame is not "make the drawer more like the plugin".
It is that the board becomes the plugin, and the mapping is one to one at every layer.

The IDE bridge exists so the session can reach EDITOR surfaces: a diff in a real tab, the current selection, the language server's diagnostics.
On this board the editor IS the board page, so the equivalent already half exists and has different names: the sentence address is the selection, `QB5`'s lanes are the annotations, and `check.py`'s output is the diagnostics.
That is the one place where migrating means translating rather than copying, and it is where the board can end up better than the plugin rather than merely equal to it.

### 7 · What stays VS Code only, and does not matter
```
🌉 the IDE bridge is the ONE piece we cannot copy
   it exists to reach EDITOR surfaces:  📑 a diff in a real tab
                                        🖱️ the current selection
                                        🩺 the language server's diagnostics
   ✅ EXACT at the engine + protocol layer
   ✳️ deliberately DIFFERENT at the surface layer  ← the alignment line we hold
```
The IDE bridge is the one piece we cannot copy, because it exists to put things in EDITOR surfaces: a diff in a real editor tab, the current text selection, the language server's diagnostics.
The drawer answers the same need in its own surface and already ships the important half, the diff preview at the permission gate.
So "exactly the same" is exact at the engine and protocol layer, and deliberately different at the surface layer, which is the alignment line this page already holds.

### 8 · What a drawn interface has to be given
```
🎛 FOUR things nobody gave the drawer          22 defects · ✅12 🟡2 ❌8
   🪟 THE VIEWPORT IS BORROWED      it is fixed OVER a page it does not control
   🔁 THE VIEW IS REGENERATED       build.py bakes it into every page, so it dies with each
   ✍️ THE RECORD IS WRITTEN ONCE    at `done`, the last thing the stream ever sends
   🎛 THE CONTROLS WERE NEVER GIVEN a terminal has them for free; a drawn surface does not
   ⚠️ not four UI complaints: state a reader can see has to be PUT somewhere, and
      three of these four rows are one mechanism away from each other (§9)
```
JL asked twice on 260801 whether the day's problems should become a division named for the surface, something like Mobile Usage or UI Experience, and the first answer here was no, on the grounds that filing them under UI would file architecture under taste.
That answer was half right: the grouping by OWNER stands, because every defect arrived as a feeling about the interface and turned out to be a fact about where state lives, but the NAME was a metaphor that told a cold reader nothing.
The subject is the interface, and the Opening already names why it needs one: a terminal inherits its behaviour, a drawn interface has to be given all of it, and this section is the list of what nobody gave it.
The fourth row is new and is what the rename makes room for: rows one to three are state a reader can lose, row four is an affordance a reader never had, and both are things a drawn surface has to be handed.

Scope, corrected on JL's ask 260801 ("focus on the SDK GUI version… the problems for QD2 only"): everything below is the DRAWER's own behaviour.
Two classes that were briefly filed here have gone back to their owners, and the Boundary now names both: how well this page is WRITTEN is `QB4`'s grammar and `QF1`'s checker, and whether the drawer's fixes were ever clicked in a browser is `QF4`, which already exists as "Driving the talk layer: the SDK chat version and the TUI chat version".

Every row below is a thing JL hit, read off both session transcripts rather than from memory (`ccda0c28-ef7e-47e0-a7e1-c13abc4f4cea` + `8c9903ba-dadb-4f00-bdd1-823986cac937`, 98 user messages, 260723 14:36 → 260801 20:43).

```
🪟 THE VIEWPORT IS BORROWED                                    4 · ✅3 🟡1
   ✅ a wheel over the drawer scrolled the PAGE behind it
   ✅ opening landed at the oldest message, not the newest
   ✅ scrolling up during a live turn snapped the reader back down
   🟡 below 820px it overlays instead of docking; ⇤ Page shipped, R3 owed
      └ the phone is the usage mode, not the edge case (JL 20:16)

🔁 THE VIEW IS REGENERATED PER PAGE                            7 · ✅3 🟡1 ❌3
   ✅ close → reopen rebuilt every bubble; the flash read as janky
   ✅ reopening mid-turn did nothing: the guard returned above `.on`
   ✅ a reload rebuilt the chat box while the terminal held the session
   🟡 a replayed session does not paint like a live one
      └ markdown · tool cards · timestamps landed; gate diffs + 💭 thinking owed
   ❌ starting a new session leaves the page unchanged, with no switch
   ❌ history has no selectable turn boundary, so two turns cannot be compared
   ❌ the drawer is generated into every page at all              → §9 R2

✍️ THE RECORD IS WRITTEN AT EXACTLY ONE MOMENT                 6 · ✅4 ❌2
   ✅ the reply appeared only after sending the NEXT message
   ✅ the drawer never re-asked the server: syncFromServer had one caller
   ✅ a cut-short turn dropped the text that had already arrived
   ✅ a group's history was written under `<id>` and read under `G:<id>`
   ❌ an in-flight turn dies with the HTTP response that carries it → §9 R1
      └ navigate away · switch a setting · let it run long
   ❌ a ten-minute turn hits the HTTP timeout                     → §9 R1

🎛 THE CONTROLS WERE NEVER GIVEN                               5 · ✅2 ❌3
   ✅ 🗂 Sessions, as a composer tab rather than a fold
   ✅ the context-usage meter: ctx 38% (62k/200k)
   ❌ typing `@` does not pull a repo file into the message
   ❌ no plan-mode toggle for a read-only planning turn
   ❌ two named sessions on one page cannot be live at once
      └ blocked on a `QD1` ruling: HOLD keys on the SCOPE
```
Read down the ❌ column and the shape is not eight separate builds.
Five of the eight are `QD1`-blocked or closed by §9's R1 and R2, one is R3, and only two are genuinely their own work: `@`-mentions and plan mode, which are the two the page has always called chrome.

#### The viewport is borrowed
The drawer is `position:fixed` over a page it does not control, so anything it declines to handle, the page handles instead.
A wheel it cannot use scrolls the page behind it, and `overscroll-behavior` cannot fix that half alone, because the property governs a scroller that has REACHED its edge and not one that never overflowed.
Below 820px the drawer stops docking and covers the page outright, so "go back to the page" stops existing as an action and only "close the chat" remains.
The VS Code panel docks at every width, and that one difference is what makes it read as part of the editor rather than as a thing on top of it.
Read from the transcript 260801 and correcting how this was filed: below-820px is not an edge case to rule on later, it is the machine JL was holding when he hit the last five defects of the day ("我他妈我现在在手机上操作，我咋按这个键啊", 20:16).
The phone is a usage mode, so docking at every width is a requirement rather than a fork.

#### The view is regenerated per page
`build.py` embeds the chat into every self-contained board page, so the view is re-instantiated on each one and dies with it.
That is the shared root of three separate-looking bugs: the drawer opened at the top because the replay ran while it was still `display:none`, a reload rebuilt it as the chat box while the terminal held the session, and navigating away aborted the turn.
It is also why a fix does not reach the reader until the page is reloaded, which is the same coupling seen from the maintenance side.
The VS Code split is the target and half of it is already ours: the extension host is a separate process that never touches the DOM, and M1's SessionHost is exactly that.

#### The record is written at exactly one moment
The transcript is saved when a turn reaches `done`, and `done` is the last thing the stream ever sends, so it is precisely what a cut connection loses.
A turn that ends any other way leaves the question saved and the reply gone, which is why an answer seemed to arrive only after the next message was sent.
The same fragility appears in the small: the send path wrote the log under a bare id while the load path read a group under `G:<id>`, so a group's history was written to one key and looked for under another.
Both carry one lesson, which is that a record with a single writing moment has a single moment in which to be lost.
Corrected 260801 from the transcript: this page dates the defect to 260801 and to having been found "by USING it", and it is a day older than that.
On 260731 between 14:34 and 15:45 the same four probes were sent fourteen times, seven of them the identical "Narrate one short sentence before each step" and three the identical "Reply with exactly: HELLO", with no complaint attached to any of them.
The re-sends WERE the symptom and nobody read them as one, which is the strongest argument on this page for the repeatable check: a defect that only shows up as a person quietly retrying is invisible to every method except driving it.

#### The controls were never given
The first three rows are state a reader can LOSE; this one is a control a reader never HAD, and it is the row that most directly answers why a terminal felt better.
A terminal hands you scrollback, a session list and a status line for free because the emulator has always had them, while every one of those is a thing the drawer must be handed one at a time.
The evidence is that each arrived only when JL asked for it by name: the session picker on 260801 17:35 ("我怎么能加一个新的 button，叫 Sessions"), the context meter at 17:46 ("我怎么看到我现在这个 context 的 usage，就是用了百分之几"), and both took an afternoon each.
What is still missing is `@`-mentions and plan mode, and they stay last on purpose, because they are affordances on top of a harness whose state problems are the thing actually felt.

### 9 · The one build that closes them, and it already exists next door
```
🖥️ QD3 terminal — already right              💬 QD2 chat — the gap
   PTY master fd                                claude_agent_sdk
        │ one reader thread  term.py:195             │ one HTTP handler
        ▼                                            ▼
   🔁 ring bytearray  ≤256KB                     ✂️ self.wfile.write()  chat.py:637
      RING_CAP  base.py:65                          the response socket ITSELF
        ├──▶ 🧑 client A                            ❌ no ring
        ├──▶ 🧑 client B                            ❌ no client list
        └──▶ 🧑 client C                            ❌ no replay
   🔌 reconnect → ws_send(b"0"+ring)  term.py:679   🚪 reader leaves → emit() fails
   ⏳ grace deadline → 秒接, 进程根本没死过            → stop.set() → the turn DIES
```
The target is not a new architecture, it is the one QD3 shipped: a terminal survives a reload because its bytes go to a RING that clients attach to, and chat's bytes go straight down the socket of whoever happened to ask.
That single asymmetry is the mechanism under three of the five rows above, and it is why the VS Code panel feels different rather than merely nicer.

- R1 · the ring, ported from `term.py` — 🟡 BUILT 260801, server half proven, one client defect open
  `live/turnring.py` is the module: one `Turn` per question key, events carrying a monotonic `n`, a 1MB/20k cap that trims from the front and reports a `gap` rather than a silently short stream, and a 600s grace window. `emit()` now pushes into it and `chat()` spawns a runner thread, so the request is no longer the turn's owner but its FIRST READER; `POST /_board/attach {file, cursor}` is how the second one joins.
  Proven by `checks/ring_e2e.py`, which is shaped like the complaint rather than like the code: start a turn, hang up the socket the way navigating does, re-attach at the cursor, and demand the rest. It gets it — 117 events and an 11k-character answer that the original reader never saw.
  Two defects the wire test could not see and a real browser did, which is the rule working: a FINISHED ring was re-attached on every 25s heartbeat and repainted its answer each time (fixed: attach declines a finished turn, because once it ends the transcript is the right source), and the cursor was keyed on `logKey()`, which folds in a session id that CHANGES mid-turn (fixed).
  STILL OPEN, and it is why this row is 🟡 rather than ✅: after a real reload the drawer does attach — `REJOIN at cursor 2` appears in its own diagnostics — but at a cursor near zero rather than where the reader left off, so it replays instead of resuming. The mechanism is live; carrying the reader's place across the reload is not.
  `emit()` writes into a per-session outbox with a monotonic cursor and fans out to every attached client, instead of writing to one `wfile`.
  A departed reader stops being an event: no `stop.set()` at chat.py:628, no `fut.cancel()` + `host().evict()` in the `finally`, and `gate()` keeps answering permission requests for the life of the TURN rather than the life of the request.
  Closes: the turn dying on navigate, reload, config switch or timeout; the ten-minute turn; and `这一题当前没有在跑的对话`.
- R2 · the retained view — ↪ RETIRED 260801 to `QD5`, which had already built it
  The plan was to stop the drawer being rebuilt per page by making it a retained view attached to the ring by cursor, VS Code's webview answer to "打开、关了、又打开，它就没有那么丝滑了".
  Reading `QD5`'s shell rather than its summary closed the row: the chat frame's src IS `<page>.html?pane=chat`, so the drawer is ALREADY its own document and no page navigation can reach it.
  That is the same outcome one layer up, and a better one, because it removes the rebuild instead of recovering from it.
  What survives here is only the half `QD5` does not touch, which is that a replayed session still paints in a poorer format than a live one; that stays in §8's second row as its own item.
- R3 · dock at every width — ↪ RETIRED 260801 to `QD5`, same reading
  `shell.py`'s own stylesheet already does it: `@media(max-width:820px)` switches the grid to `grid-template-rows:1fr 5px 1fr` and hides only the page list, so page and chat are both visible on a phone.
  The fork this page carried, overlay-with-a-way-back against collapse-to-a-tab, is answered by neither: the shell simply stacks them.

So §9 is ONE build, not three, and the two that left were not descoped but already delivered next door.
R1 stands alone because the turn dying with its HTTP response is a SERVER fact, three sites in `live/chat.py`, and no arrangement of frames reaches it.
The blocker is named and is not technical: `QD1`'s HOLD keys on the SCOPE path while the Law's stated reason is the shared jsonl, and a resumable channel redefines "one live window", so two named sessions on one page cannot be live together until that Law is re-ruled.

CORRECTION, 260801, mine to make: this page briefly warned that R1's held `/_board/attach` would compete with `QD5`'s `/_events` for the browser's six connections per origin.
That was written from `QD5`'s prose and is wrong. `/_events` holds nothing: it is one small JSON ask every 400 ms on a pooled connection, and `shell.py`'s own docstring explains that a held stream was built FIRST and removed precisely because it cost a connection.
The budget question is still real but smaller and differently shaped: the held connections are the terminal's WebSocket and R1's own two, the turn stream and an attach.

## Aims

### C4 · What "exactly the same as the extension" costs, in milestones
- A4.1 · One `claude` process serves every turn of a session, instead of one booted per POST.
  **Done when:** a follow-up message reaches its first token without reloading the skill registry, and costs a fraction of the first.
- A4.2 · The streaming-mode verbs are reachable from a live session.
  **Done when:** `interrupt()`, `set_model()`, `set_permission_mode()` and `get_context_usage()` all work mid-conversation with no reconnect.
- A4.3 · A turn can be rewound to an earlier checkpoint.
  **Done when:** `rewind_files(user_message_id)` restores the files a turn changed.
- A4.4 · Typing `@` pulls a repo file into the message.
  **Done when:** a picker over the repo inserts a path the model then reads without being told where to look.
- A4.5 · A plan-mode toggle runs a read-only planning turn before any edit.
  **Done when:** the drawer enters `--permission-mode plan` mid-conversation and leaves it again.

### C8 · What a drawn interface has to be given
- A8.1 · The drawer never moves the page behind it.
  **Done when:** a wheel anywhere over the drawer scrolls the drawer or nothing, at every transcript length.
- A8.2 · A reader can see the page and the chat at once, at any width.
  **Done when:** a phone-width reader reads the page and the chat without closing either.
- A8.3 · Reopening the drawer costs a repaint, not a rebuild.
  **Done when:** closing and reopening the same scope produces no flash and no re-parse, however often it is done.
- A8.4 · A replayed session paints exactly like the live turn it is a recording of.
  **Done when:** a session picked from 🗂 carries the same markdown, tool cards, gate diffs and 💭 thinking a live turn carries.
- A8.5 · Two named sessions on one page are live at the same time.
  **Done when:** `QD2-type-1` and `QD2-type-2` both run, and neither takes the other's HOLD.
- A8.6 · One history turn can be compared against another.
  **Done when:** a reader selects two turns and sees them diffed with the same − / + renderer the permission gate already uses.
- A8.7 · Whatever a turn produced survives every way a reader can leave.
  **Done when:** navigating away, reloading, switching a setting, locking a phone and waiting ten minutes each leave the answer readable afterwards.
- A8.8 · The drawer has the controls a terminal gets for free.
  **Done when:** a session list and a context meter are reachable from the composer without leaving the page.
- A8.9 · A reader chooses which chat they are opening, and sees what is already running before they commit.
  **Done when:** the bottom-right button offers GUI-Chat and TUI-Chat as a list, each row reporting whether a turn is live or a terminal is parked, with the last choice marked.

### C9 · The one build that closes them
- A9.1 · A turn outlives the request that started it, and a returning reader rejoins it where it stopped.
  **Done when:** hanging up mid-turn and re-attaching delivers the rest of that turn from the reader's own cursor.
  **Plan:** R1, the ring ported from `term.py`. R2 and R3 are retired into `QD5`, which had already built both.

### P · Page-level
- P1 · The drawer runs, resumes, and pays its way.
  **Done when:** a session starts, answers, resumes by id, and a follow-up message costs cents.
- P2 · Each permission tier restrains exactly what it says it restrains.
  **Done when:** the restricted tier's blocked tools are refused at the tool layer, and the ask tier prompts for everything else.
- P3 · The drawer's own behaviour is covered by a repeatable check.
  **Done when:** a browser-driven suite asserts the scroll, dock, replay and session-list behaviours, and is run before any fix here is claimed.

## States

### C4 · What "exactly the same as the extension" costs, in milestones
- ✅ A4.1 · Built 260731 as M1: a daemon thread owns one asyncio loop for the process's life and `SESSIONS[question] -> {client, inbox, outbox}`, so the browser protocol did not change at all. The blocker it had to clear was that the SDK forbids a client crossing async runtime contexts while `serve.py` ran a fresh `anyio.run()` per request.
- 🔨 A4.2 · One of four landed. `get_context_usage()` ships and is read once per turn on the existing `done` event, so it costs no extra call and degrades to absent rather than wrong; it is shown as `ctx 38% (62k/200k)`. `interrupt`, `set_model` and `set_permission_mode` are reachable now that the client is held and are not wired.
- ⬜ A4.3 · Unparked 260731 when JL amended `QD1` to one question, many sessions, so rewind no longer forks a second history. It needs `enable_file_checkpointing=True` plus `replay-user-messages`, both option flips.
- ⬜ A4.4 · Ours to build rather than the SDK's: a picker over the repo plus the chosen path injected into the outgoing message.
- ⬜ A4.5 · Free once A4.2 lands, since it is `--permission-mode plan` reached through `set_permission_mode()`.

### C8 · What a drawn interface has to be given
- ✅ A8.1 · Fixed 260801 in two parts, because `overscroll-behavior` governs a scroller that has REACHED its edge and not one that never overflowed: `contain` on every inner scroller, plus a `wheel` handler that walks up from the pointer and keeps the event when nothing inside can take the delta. A nearly empty transcript was the case with nothing to scroll, which is why it seemed to heal after the first message (JL: "感觉还是背后的那个 page 页面在滑动").
- 🔨 A8.2 · A labelled `⇤ Page` button ships and appears exactly at the width where the drawer stops docking. ↪ Answered inside `QD5`'s shell, whose `@media(max-width:820px)` stacks page over chat and hides only the page list; this row stays open only for a drawer on a page opened alone, which is the packaging `QB2` requires.
- ✅ A8.3 · Fixed 260801: when the same scope is already painted and no turn is running, the drawer is shown again rather than torn down and rebuilt from storage. `chatOpen` had re-parsed markdown for every bubble and then sometimes rebuilt a second time when the server answered, and the flash between the two is what read as janky (JL: "打开、关了、又打开，它就没有那么丝滑了").
- 🔨 A8.4 · Half. `session_log` now carries each message's `timestamp` and every `tool_use`, one `replayRow()` draws bubbles, tool cards and dated turn separators, and the tail cap rose from 120 to 300. Still owed for parity: the gate diffs, the 💭 thinking block, and a load-earlier control instead of a hard cap.
- 🧠 A8.5 · Blocked on a `QD1` ruling, not on this page. HOLD keys on the SCOPE path while the Law's stated reason is that "two front ends on the same jsonl still fork histories"; two named sessions are two different jsonls, so the key is stricter than the rule that justifies it.
- ⬜ A8.6 · Not started. The replay is one flat text list with no turn boundary a reader can select, so there is nothing to compare yet.
- 🔨 A8.7 · Most ways closed, one open. Closed 260801: `emit()` no longer calls `stop.set()` when a write to a departed browser fails, so leaving the page loses the view and not the work; a cut-short turn saves what streamed, marked `partial`, and the sync adopts whenever anything provisional is present; `syncFromServer` retries at 1.5s, 4s, 9s and 20s, re-asks on tab and window focus, and keeps a 25s heartbeat, after having had exactly one caller; and one `logKey()` helper owns both halves of the group-chat store, which used to write under `<id>` and read under `G:<id>`. Open: the live trace of a running turn, and the ten-minute turn against the HTTP timeout, both of which are A9.1.
- 🔨 A8.9 · Shipped 260802 and OVERTAKEN the same day, so the Aim is met by someone else's control. `QD5`'s split now answers a plain board url with the SHELL, whose header already carries `>_ TUI` and `💬 GUI`, and a page inside it hides `#chatfab` by design. The choice a reader makes is therefore real and the picker that made it is unreachable; the honest close is to retire this one into `QD5`'s header rather than keep two choosers. What shipped, for the record: The board had two chats and one button, so which one you got was decided by a `board-tui-default` preference you could not see, and the only way to switch was the `>_` in the drawer header, which is hard to find on a phone. `#chatpick` is two rows on the FAB only: the per-card `🤖 Chat` still goes straight to the last-used view, because its reader has already decided what they want and twelve choosers would be noise. Each row reports what no surface reported before, which is whether something is already running: `POST /_board/attach {probe:1}` answers for a turn without joining its queue, and `term-probe` answers for a parked PTY. Verified by clicking it: the menu drew both rows, the TUI row read `🟢 a session is parked here` and carried the last-used dot, the drawer stayed shut until a row was chosen, and choosing GUI opened the drawer with `termon` off and the preference flipped to `0`; zero JS exceptions.
- ✅ A8.8 · Both shipped 260801 on JL's ask, each after he named it. `🗂 Sessions` became the middle composer tab between `✨ Quick actions` and `⚙ Settings`, with the picker element moved unchanged so its loader needed no edit; the context meter rides the turn's own `done` event.

### C9 · The one build that closes them
- ✅ A9.1 · Proven in a real browser 260802, which is the claim this row owed all day. `live/turnring.py` holds one `Turn` per question key with events carrying a monotonic `n`, a 1MB/20k cap that trims from the front and reports a `gap` rather than a short stream, and a 600s grace; `emit()` pushes into it and the request became the turn's FIRST READER rather than its owner, with `POST /_board/attach {file, cursor}` for the next reader and `{probe:1}` for asking without joining the queue.
      Three defects were found on the way and not one of them by reading. `drain()` treated a notify that did not satisfy its condition as a reason to leave the wait, so it wrote a keepalive per loop and spun to 13,149 threads at 292% CPU; `tests/test_turnring.py` now pins that at 200 events producing exactly 200 writes. A FINISHED ring was re-attached on every 25s heartbeat and repainted its answer. And the cursor was keyed on `logKey()`, which folds in a session id that changes mid-turn.
      The proof is `checks/guichat.mjs` T6: it sends a turn long enough to still be running after a reload PLUS reopening the shell, reloads mid-turn, and asserts the drawer REJOINED rather than merely ending up with an answer. `REJOIN attached at cursor 137` against a pre-reload cursor of 99, 22,899 characters landed, zero apology bubbles. The first version of that assertion passed on the transcript sync without touching the ring at all, and catching that soft pass is what makes the row worth anything.

### P · Page-level
- ✅ P1 · `claude-agent-sdk 0.2.126` starts a session, reads board files and answers; auth needs no work of its own because the SDK drives the machine's `claude` CLI and inherits the logged-in OAuth. `session:` sits in the page header beside `state:` and `owner:`. Cost went from a $0.92 default to $0.24 by narrowing, and a follow-up message is $0.012.
- ✅ P2 · Three tiers ship, default full·ask (JL ruled 260723). The restricted tier hard-disables Bash, Task, Skill and Web through `disallowed_tools`, because `can_use_tool` is not reliably invoked for Bash and a blacklist is the solid way; verified by forcing Bash and getting "Bash exists but is not enabled in this context". The gate has genuinely fired: a forced `Edit` against `board.md` was blocked at the tool layer with `denied: ['Edit -> …/board.md']` and the file was untouched, comparing resolved absolute paths rather than name strings.
- ✅ P3 · `checks/guichat.mjs`, 22 assertions, green on four runs. It drives the REAL split shell rather than a page in isolation: it opens a board url, checks the header offers both chats, clicks `💬 GUI`, then reaches into the chat frame for everything else. T1 the split · T1b what you CLICK is what OPENS, from a cleared storage · T2 a usable composer · T3 an answer whose markdown is RENDERED, asserted on `<strong>`/`<code>`/`<li>` rather than on text · T4 no apology bubbles and no JS exceptions · T5 a reader who scrolls up during a live turn is still there nine seconds later · T6 the ring, above · T7 close and reopen neither loses nor duplicates a transcript · T8 🗂 Sessions populates · T9 the meter reads `ctx N%`.
      Every turn is scoped, haiku and low effort, so a full run costs cents. This is what nine unclicked fixes on 260801 should have had, and it exists because JL made the point a third time ("please go ahead to make sure the GUI Chat is good, no, very very good to use"). ↪ The axis this belongs to is `QF4`.

### Decision Now
The calls only JL can make. CC ticks nothing here, and every row names the Aim it unblocks.

- [ ] ❄️ A4.1 · Rule how a held session is reaped
      A held client is a live `claude` process per question, so something must end it. Today it is a partial C: `SessionHost._reaper(idle_s=1800, every=120)` evicts after thirty idle minutes and nothing frees a client when the page closes, which is what JL was looking at on 260802 when two held clients sat there four minutes after a restart.
      A · idle timeout plus the existing pagehide beacon; reaping mirrors how `QD3` already reaps terminals and needs no new gesture from you.
      B · explicit release only; you close a session by hand and no timer runs.
      C · timeout only; a closed page does not free the process, which is today's behaviour.
      → CC's proposal: A. It matches `QD3` and needs nothing new from you. One hole in C is worth naming whichever way you rule: `reap()` skips a session whose turn lock is held, so a turn that HANGS pins its client past any timeout.
- [ ] 🔒 A8.5 · Ask `QD1` to re-rule one-window-per-scope
      Not this page's Law to change, and it blocks the only 🟠 Aim here. HOLD keys on the SCOPE path while the Law's stated reason is that two front ends on one jsonl fork histories; two named sessions are two different jsonls, so the key is stricter than its own justification.
      → CC's proposal: carry it to `QD1` rather than work around it here.

## Files
### The host
- `cli/serve.py`
  `chat()`: `ClaudeSDKClient` + the `can_use_tool` permission callback + NDJSON streaming, all here.

### The drawer surface
- `cli/build.py`
  The generator embeds the drawer assets into each self-contained board page.
- `assets/js/00-header.js`
  Drawer markup and behavior, including title binding and terminal/chat mode switching.
- `assets/css/10-focus.css`
  Drawer layout and visual hierarchy, including the compact neutral header.

## Lesson
#### `query()` closes the input stream once the prompt generator is exhausted, then `can_use_tool` has nowhere to reply.
The symptom was bizarre: reads fine, writes hang, `Tool permission request failed: AbortError: Stream closed`.
The permission callback's allow/deny answer travels back to the CLI over the stdin control channel.
`query(prompt=<one-shot async generator>)` closes that stream right after the message is sent: reads usually ask before the close and pass; writes ask later, the channel is gone, the CLI times out.
Switching to `ClaudeSDKClient` (connection held for the whole turn) fixed it immediately. **`haichat-inlab` always used `ClaudeSDKClient`, never `query()`**; the port missed exactly this.
Lesson: when copying someone's code, copy **why this API and not that one** along with it.


#### One port, one server.
Chasing "page unresponsive / chat gives no response" ended at two stacked causes: ① reverse DNS: `SimpleHTTPRequestHandler.address_string()` runs `getfqdn()` on the client IP by default, costing 7.8 seconds per request on this machine.
   Overridden to return the raw IP.
② two `serve.py` processes fighting over 5599; connections landed on either at random.
   Now `--daemon` double-forks away from the terminal, and startup verifies the port is clean first.
After both fixes the 150KB page returns in 0.001s.

## Glossary
can_use_tool: the SDK's tool gate callback.
Every tool use asks it for allow/deny first. effort: how much thinking the model spends on one answer, five tiers low→max.

## Discussion
> JL: I lean toward claude_agent_sdk, we can add it. OAuth is fine for auth.
> JL: why not use the best model? claude 4.8 opus, or let us pick model and effort and so on.
>> CC0723: added both dropdowns, default opus 4.8 + high.
> JL: how do I stop this chat? any smooth way?
>> CC0723: the send key turns into ⏹ while running; clicking it raises the server-side flag and aborts browser-side.
> JL: how do you think the claude code plugin in the vscode work? we want to align it with QD2?
>> CC0724: it is the same engine underneath (local claude runtime, same credentials, same session jsonls), so alignment is UX, not architecture. What it has that the drawer lacks: diff preview at the permission prompt, @-file mentions, plan mode, checkpoints. Adopt in that order; skip checkpoints (fights the one-session LAW). Full comparison in Where we are; new Items-to-Finish line added.
> JL: I think it is also related to QD5, right? maybe we can just remove it. as it is very related to QD2 and QD3, how do you think? (260725)
>> CC0725: agreed and archived (moved to _archive/QD5-boardagent.md, recoverable). QD5 asked for a board-level agent; what shipped is smaller and lives here: the same drawer and terminal, opened on board.md from the index. Its entry-point/stack/permission questions are answered by this question's machinery; its one real leftover, the "two agents, one file" rule, was already QD1's open item and stays there.
> JL: will this make it better to use the claude sdk or terminal? I want to know what is the back end of the vscode claude plugin? and I want to duplicate it.
>> CC0724: the console split changes nothing about which to use, both still run on the workstation serve.py; the console only pipes. Choose by job: drawer (SDK) for gated, comment-driven edits in the page; terminal for long tasks, skills, anything CLI-shaped. The plugin's backend is the claude binary itself over the stream-JSON protocol, which is what the drawer already drives, so "duplicating it" = the shell: diff-at-the-gate (shipped today, ①) and one persistent process per session (④, next). Anatomy written into Where we are.
> JL: for QD2, the chat interface is not clean. The header shows a heavy blue bar, muted id pill, oversized title, and uneven terminal/close controls. (260725)
>> CC0725: simplified it into a neutral utility bar. The id is quiet metadata, the full title uses available width with ellipsis, and `>_` plus `×` are matching compact controls with accessible labels.

## Log
260802 · A replayed transcript showed eighteen bare lines where the tool cards should be (JL, screenshot: "the thinking process become lines"). Measured in a clean browser on the same page and the cards render correctly, `.tn` reading `Read` at 12px and `.tb` the grey path, so the most likely cause on JL's screen is a tab holding an older bundle. The row was still wrong to be POSSIBLE: `replayRow` built a bordered row for any saved entry, including one carrying neither text nor a tool name, and an empty entry can arrive from an older log or from a message that held only thinking. It now draws nothing at all, because an absent row reads as absent while a blank one reads as a fault. `checks/guichat.mjs` gained the assertion that no child of the transcript is empty, which is the only way this stays fixed
260802 · Clicking `💬 GUI` opened the TUI, and the cause was a race nobody could have read off the page (JL: "when I click the GUI, but it is the TUI selected and opened, why?"). The shell asks the pane for a mode by calling `frames.chat.__paneMode(mode)`, but on the FIRST click that frame has not loaded yet, because the shell loads it lazily inside its own `paint()` which runs AFTER the call. So the request went to a window with no such function, the `try` swallowed it, and the pane then booted with the DRAWER's own preference, which defaults to the TUI; the shell's repaint 1.4s later read the live mode and lit `>_ TUI`, which is why the wrong button also looked deliberate. Reproduced from a cleared localStorage: `board-split-mode` read `gui`, `board-tui-default` was null, the pane came up `termon`. FIXED in `live/shell.py`'s chat `PANE_BOOT`: the shell's radio is now the source of truth and the drawer's own key is DERIVED from it at pane boot, before the drawer is told to open, with a 300ms belt-and-braces switch for the race the other way. Verified both directions and all four gestures — open, switch, click-the-lit-one-to-hide, bring it back — and folded into `checks/guichat.mjs` as T1b, which clears storage first because a FIRST-TIME reader is the only one who ever saw this
260802 · The GUI chat was DRIVEN rather than argued about, and `checks/guichat.mjs` is what that leaves behind: 17 assertions through the real split shell, green on two consecutive runs. A9.1 is finally ticked on evidence a reader would accept — T6 sends a turn long enough to outlive a reload plus reopening the shell, reloads mid-turn, and demands the drawer REJOINED rather than merely ended up with an answer; `REJOIN attached at cursor 137` against a pre-reload cursor of 99, 22,899 characters, zero apology bubbles. The first version of that same assertion PASSED on the transcript sync without touching the ring, and catching that soft pass is the whole reason the row is worth anything. P3 ticks with it, closing the 260801 admission that nine drawer fixes shipped unclicked. A8.9 moved the other way, ✅ to 🔨: the picker works and is now unreachable, because a plain board url opens the shell and the shell hides the fab, so the choice it offered already lives in `QD5`'s header. One correction of mine: I reported the `?pane=page` redirect as a bug earlier today and it is the intended split — I was looking for the old door
260802 · The bottom-right button became a CHOICE on JL's ask, and the tap pays for itself. Two rows, `#chatpick`, GUI-Chat against TUI-Chat, on the FAB only: a per-card `🤖 Chat` means talk about THIS card and its reader has already decided, so twelve choosers would be noise. What the board had before was two chats behind one button, arbitrated by a `board-tui-default` key nobody can see, with the `>_` header toggle as the only way to switch and no way at all to find it on a phone. Each row also answers the question nothing on the board answered: is something already running here. `POST /_board/attach {probe:1}` is new and deliberately narrow, because a plain attach would answer by PARKING on the ring until the turn ended, which is the opposite of a question; `term-probe` already answered the terminal half. Clicked it rather than claimed it: both rows drew, the TUI row read `🟢 a session is parked here` with the last-used dot, the drawer stayed shut until a row was picked, choosing GUI opened it with `termon` off and the preference flipped, and the narrow window proved the `@media(max-width:820px)` rule by going full width. Recorded as A8.9
260802 · Migrated onto `QB4`'s page grammar, which this page had recorded as a finding on 260801 and DEFERRED on JL's call. Four changes and one of them is the whole job: `## Boundary` is gone, because the protocol has no such section, and its routing became the placing paragraph that now closes Content §1, the way `QD5`'s C1 does it; `## Items to Finish` became `## Aims`, forty checkboxes rewritten as seventeen durable targets grouped by the Content division they serve, each with a testable `Done when` and no checkbox anywhere, per QB4 §4.5 which says Aims are not a work history; `## Where we are` became `## States`, one row per Aim in the five statuses, carrying the evidence the checkboxes used to hold; and `## Writing Style` was added, which QB4 §8.6 requires and which only QB4 itself had. The title also changed, since §8.3 asks a title to say what a page is FOR: "SDK chat version: the chat box" named a subject only. Three Decision Now rows were overtaken by events and moved here rather than left standing beside live ones (below); the `### Decisions taken` subsection went the same way, because §5.3 makes Decision Now the ONE reserved subsection of States and §5.4 puts history in Log. Worth recording for whoever migrates the next page: 51 of 53 pages still carry Items to Finish and Where we are, and 36 still carry a Boundary, so this is the third page on the board to obey its own contract
260802 · Three Decision Now rows retired as overtaken by events, kept here so the reasoning survives. 🐍 the language ruling (Python against the npm TypeScript SDK) is settled by what was built: M1 landed in Python inside serve.py, which was option A, and Content §5 had already checked parity at 47 options rather than assuming it. 🔀 whether QD2 and QD3m are one build or two is moot, since `QD3m-smooth-terminal.md` is archived. 🧲 which extension affordance comes next was answered the same way as 🐍, by the effort going to the engine rather than to `@`-mentions or plan mode, which was option C. What is left standing is ❄️ the reaping rule and a pointer at `QD1` for the one 🟠 Aim
260731 JL · 🔌 The session host, M1, approved and built. JL: "make the chatbot sdk version exactly the same to the vscode claude code plugin version". The teardown said exactly-the-same is reachable because the extension runs the SAME SDK we already run, and the only engine-layer gap was that it holds the client while we dropped it every POST. Chosen A: one daemon thread owning a long-lived event loop plus a per-question client registry, with the browser protocol unchanged. B, warming a pool and caching the registry, was rejected because it treats the symptom and still cannot reach `interrupt`, `set_model`, `set_permission_mode`, `get_context_usage` or `rewind_files`, all of which are streaming-mode only; C was to leave it. Moved out of a `### Decisions taken` subsection on 260802, because QB4 §5.4 puts history in Log
260801 · §9 collapsed from three builds to one after reading `QD5`'s `live/shell.py` instead of its page. R2 and R3 are RETIRED into `QD5` rather than descoped: the split shell's chat frame is `<page>.html?pane=chat`, so the drawer is already its own document and no navigation rebuilds it, and `shell.py`'s own `@media(max-width:820px)` already stacks page over chat on a phone, which answers the docking fork by making it moot. Both Items rows keep their place but now say ↪ ANSWERED BY QD5, scoped to the one case the shell does not cover, a drawer on a page opened alone, which is the packaging `QB2` requires. R1 survives alone because a turn dying with its HTTP response is a server fact that no arrangement of frames reaches. One correction of my own recorded in §9: the warning that R1's attach would compete with `/_events` for the six connections per origin was written from QD5's prose and is wrong, since `/_events` holds nothing and is one 400 ms ask on a pooled connection. Three writers were live in this area tonight (this session, QD2's own drawer, and a Codex companion inside `shell.py`); nothing collided, and the near-miss is why the QD5 findings went over as an append-only Log line instead of edits to its Content
260801 · R1 built and left HONESTLY half-ticked. `live/turnring.py` gives chat what `term.py` has had all along: one ring per question key, events carrying a monotonic `n`, a front-trimming cap that reports a `gap` instead of a short stream, and a grace window; `emit()` pushes into it, `chat()` spawns a runner thread, and the request becomes the turn's FIRST READER rather than its owner, with `POST /_board/attach {file, cursor}` for the second. `checks/ring_e2e.py` proves the server half by doing what JL does — start a turn, hang up the socket, come back — and gets 117 events and an 11k answer the first reader never saw. The rule about clicking it yourself then earned its keep twice: a real browser showed a FINISHED ring being re-attached on every 25s heartbeat and repainting its answer each time (fixed by declining a finished turn, since the transcript is the right source once it ends), and showed the cursor keyed on `logKey()`, which folds in a session id that changes mid-turn (fixed). What is still broken and why the row is 🟡: after a reload the drawer DOES attach, its own diagnostics say `REJOIN at cursor 2`, but the cursor is near zero rather than where the reader stopped, so it replays instead of resuming. Server restart owed before any of this reaches the live board, since it is in `live/chat.py`
260801 · §8 re-scoped to QD2 ONLY on JL's ask ("if we focus on the SDK GUI version… could you specific the problems for the QD2 only?"), and the correction was mine to make: the same-day expansion to five rows had put two classes here that belong to other faces. The page's own writing went back to `QB4` (page grammar) and `QF1` (the checker), and whether a fix was ever clicked in a browser went to `QF4`, which already exists as "Driving the talk layer: the SDK chat version and the TUI chat version"; both are now ↪ lines in Boundary rather than divisions here. In their place a fourth row that IS the drawer's own, 🎛 the controls were never given, which is what the rename made room for: rows one to three are state a reader can lose, row four is an affordance a reader never had, and its evidence is that the session picker and the context meter each arrived only when JL named them and each cost an afternoon. §8 now carries the full enumerated list instead of three sample symptoms: 22 defects, ✅12 🟡2 ❌8, each one a thing JL actually hit, and the ❌ column collapses rather than fanning out, since five of the eight are `QD1`-blocked or closed by §9's R1/R2, one is R3, and only `@`-mentions and plan mode are their own work
260801 · Both session transcripts read off disk on JL's ask ("read the content there and understand what are the problems I encountered along the time"), 98 user messages from 260723 14:36 to 260801 20:43, and §8 rewritten against them. Renamed from "The bill the CLI never sends you" to "What a drawn interface has to be given", which is the Opening's own sentence, so the section stops being a metaphor and becomes the Opening's evidence; JL had proposed a surface name (UI/UX experience) and the earlier refusal was half right, since the grouping by OWNER stands but the NAME and the COUNT did not. Three corrections the transcript forced: the lost-reply defect is a day older than this page says, evidenced by fourteen sends of four identical probes on 260731 14:34-15:45 with no complaint attached, so the re-sends were the symptom nobody read; the below-820px overlay stops being a fork because JL was on a PHONE for the last five defects of 260801; and two owners were missing entirely, the page's own prose (four Opening rejections, and "which Q owns quality check" still unassigned) and the fixes themselves (nine claimed unclicked, then one unclosed comment took the bundle down). Added Content §9, which names the build: QD3's terminal already survives a reload because its bytes go to a RING that clients attach to (`term.py:195`, `RING_CAP` at `base.py:65`, replay at `term.py:679`) while chat writes straight to `self.wfile` at `chat.py:637`, and that one asymmetry is the mechanism under three of the five rows. R1 the ring, R2 the retained view attached by cursor (which is what 丝滑 names, and it closes replay fidelity for free), R3 dock at every width; order forced because R2 has nothing to re-attach to without R1, and blocked on a `QD1` re-ruling since HOLD keys on the SCOPE
260801 · A replayed session now reads like the turn it is a recording of, which it did not: the server kept assistant TEXT only, so a turn that ran ten tools replayed as one bare paragraph, and there were no times and no turn boundaries in a flat wall of bubbles. Three changes, one idea, which is that the live view and the replay should not disagree about what happened: `session_log` carries each message's `timestamp` and every `tool_use` call, the drawer draws replayed rows through one `replayRow()` that knows all three shapes (bubble, tool card, dated turn separator), and the tail cap rose from 120 to 300 because tool rows eat the budget. Still owed for full parity: the gate diffs and the 💭 thinking block, plus a load-earlier control instead of a hard cap
260801 · Reopening the drawer stopped rebuilding it, which is the answer to why it felt worse every time it was closed and opened. `chatOpen` tore down the transcript and re-created every bubble from storage even when the scope had not changed, and the discarded transcript was identical to the one it built; the flash between them is what read as janky. VS Code retains its webview so showing a hidden panel costs one repaint, and the drawer now does the same when the scope matches and nothing is running. Same root as Content §8's second row, now visible in the one place a reader feels it
260801 · JL threw out the framing, not the wording: "这跟 Trust 有个蛋的关系？我们这不是在说怎么设计这个 GUI 的界面的吗". He is right, and the frame was inherited rather than examined. Trust arrived at the 260801 rename and every later pass, mine included, polished it instead of questioning it, while the actual work on this page all day was interface design: scrolling, docking, tabs, a session list, a context meter, diff cards, and whether the drawer should stop being generated into each page. The Opening now asks what makes a chat interface inside a page good to USE, and its one idea is that a terminal inherits its behaviour while a drawn interface has to be given every part of it, so the parts nobody designed are the ones that break. The lost-reply failure keeps its place as one of those parts rather than as the page's thesis
260801 · The root of "I only see your reply after sending a new one" removed at the server: `emit()` called `stop.set()` when a write to a departed browser failed, so leaving the page did not lose the view, it ENDED the work, and the answer never reached the `.jsonl` for any later sync to find. A failed write now marks the turn detached and lets it finish; ⏹ still stops a turn, because that is a person deciding rather than a socket closing. Caught while doing it: my own two 260801 fixes were fighting, because the abort-save left a cut-short reply that made the local log the same LENGTH as the server's, and the sync adopts only when the server knows MORE, so a fragment could never be upgraded; cut-short entries are now marked `partial` and the sync asks whether the server knows BETTER. Server half needs a restart, client half needs a hard reload
260801 · JL diagnosed the one that had beaten me twice, and he was right: the drawer never checks for session updates on its own. `syncFromServer` had exactly one caller, `chatOpen`, so it asked the server the instant the drawer opened and never again, and coming back mid-turn is precisely when the answer has not reached the `.jsonl` yet. That also explains the tell, that sending a new message seemed to reveal the previous reply: reopening the drawer was silently firing the one retry. A second guard made it stick, since the sync refused to adopt while `body.chatbusy` was set and an aborted turn leaves that class behind. It now retries with backoff after opening, re-asks on tab and window focus, and keeps a 25s idle heartbeat, all gated on a genuinely live turn rather than on a class that can go stale
260801 · The Opening re-aimed at THIS page's identity after JL caught it borrowing the sibling's: it argued from the CLI ("rebuilt rather than borrowed"), which makes the SDK version read as an imitation of the TUI version and hands `QD3` the framing. The axis is GUI against TUI, and the reason a GUI is possible at all is that the SDK yields structured events rather than a painted screen; that trade is now the pitch's ONE idea, with what it buys (a diff at the gate, tool cards, the session picker, the context meter) set against what it costs (a terminal shows its own state for free, a drawn surface has to be told and can look right while being wrong). The terminal now appears only as the contrast, never as the definition
260801 · The lead question rewritten once more on JL's ask: the previous one asked what "a chat box" must earn, which is true of any chat box anywhere and told a cold reader nothing about THIS one. It now names the thing before it asks about it (a chat box on every page that reads the page and rewrites it, rebuilt in a browser rather than borrowed from the CLI), so the question arrives with its subject already standing, and the second line says why the stake is high, which is that the lightest door is the one people actually use
260801 · Opening rewritten AGAIN, this time against QB4 §1 read line by line after JL rejected the first attempt: one real question on stage, a three-line pitch carrying ONE idea (a rebuilt chat box pays for what the CLI gives away) and closing on a test that is checkable (if you cannot tell a finished answer from a killed one, nothing else here counts), then Why this matters as a single drawer row. The first attempt failed three of the seven rules: four ideas instead of one, implementation detail in the pitch (reload, ten-minute turn), and three `**Item**:` rows where the contract lists one. Two structural findings recorded and DEFERRED on JL's call (option B, this page's Opening only): q-template says there is NO `## Boundary` section, and 46 pages including this one still carry one, and the canonical section names are now `## Aims` and `## State` where this page still says Items to Finish and Where we are. Both are board-wide migrations and belong to their own Q, not to today's debugging
260801 · Opening rewritten to QB4's contract after JL called it badly written, and it was: QB4 asks for a PITCH (one question, then three or four lines that promise an outcome and close on a test) and what stood there was a summary with the lead split across two sentences. It now opens on what a chat box owes a reader, and the rationale moved into three `**Item**: prose` rows the way QB4's own Opening does. Also added Content §8, which is JL's ask to organize the day's problems: he proposed a surface-shaped division such as Mobile Usage or UI Experience, and the answer is no, because every defect arrived as a feeling about the interface and turned out to be a fact about where state lives, so the division groups them by OWNER instead (the viewport is borrowed · the view is regenerated per page · the record is written at exactly one moment) under one property, the durability of shown state
260801 · The context meter shipped on JL's ask ("用了百分之几"): `get_context_usage()` is read once per turn and rides the existing `done` event, so it costs no extra call, and it degrades to absent rather than wrong. It is the FIRST M2 verb to land, which makes the M1 decision concrete: this is streaming-mode only and was unreachable while the client was dropped every POST. Needs a serve.py restart, since the change is in `live/chat.py` and not in the page bundle. Recorded honestly alongside it: none of the day's nine drawer fixes has been clicked in a real browser, so `checks/chatui.mjs` is now an open item, shaped after `checks/termnav.mjs`
260801 · Wheel containment fixed: the drawer sits fixed OVER the page, so a wheel it could not use chained to the document and scrolled the page behind, which an almost-empty transcript guarantees and which is why it appeared to heal after the first message. Two parts, because `overscroll-behavior` only governs a scroller that has reached its edge and not one that never overflowed: `contain` on every inner scroller, plus a `wheel` handler that walks up from the pointer and keeps the event when nothing inside can take the delta
260801 · Four more drawer defects fixed from JL's live use, three of them one root: the transcript is only as durable as the moment it happens to be written. A cut-short turn dropped its reply because the save lived at `done` alone (now the abort path keeps what streamed, marked); a GROUP chat wrote its log under the bare id and read it under `G:<id>`, so its history never returned (now one `logKey()` helper owns both halves); reopening mid-turn did nothing because `chatOpen`'s same-target guard returned above the line that adds `.on` (now it shows the drawer first). Separately, `🗂 Sessions` became the middle utility tab on JL's ask, with the picker element moved unchanged so its loader needed no edit, and the two-way tab logic generalized to a table
260801 · Autoscroll separated into FOLLOW and JUMP after JL corrected the diagnosis (the complaint was never "it does not reach the bottom", it was "it will not let me leave it"): a scroll listener on `.bd` remembers when the reader has scrolled up, `bdAuto()` declines to chase them, and `bdJump()` is kept for opening, replaying and sending; the permission gate keeps its jump because it is waiting for an answer. Six raw `scrollTop = 1e9` sites across four files converted, all node-checked and rebuilt
260801 · A labelled `⇤ Page` button shipped in the drawer header, shown at exactly the width where the drawer stops docking and starts covering the page; the docking question itself stays open as a fork. Same round, the in-flight-turn item stopped being a symptom and became a spec: the three sites in `live/chat.py` that deliberately kill a detached turn are named (`emit()` 628 sets stop on a failed write, the `finally` 928-937 also cancels the future and EVICTS the held client, and `gate()` 804-808 denies every tool with "这一题当前没有在跑的对话" once TURN_GATE is empty, which is the string this page's own session hit twice). Not built: swapping the turn engine while JL is talking through it would take away the only channel he has to tell me it broke
260801 · Seven problems JL hit in one sitting were inventoried and two were fixed at the root. FIXED: the drawer opened at the top because `chatOpen` replayed the log while `#chat` was still `display:none`, so every `scrollTop` was clamped to 0 and the one rescue path early-returns when the local log is current (now a `requestAnimationFrame` scroll after `add('on')`); replayed history showed no markdown and no bubble styling because `session_log` emits `k:"ai"` while the renderer and the CSS only know `cc` (now normalized in `bubble()`). Both node-checked, rebuilt, and confirmed present in `board/_assets/board.js`. OPENED as items: history has no selectable turn boundary so it cannot be compared; the drawer overlays instead of docking below 820px, leaving only a 32px `×` as the way back; two named sessions of one page cannot be live together because HOLD keys on the SCOPE while the Law's reason is the shared jsonl; an in-flight turn dies with the HTTP response that carries it; and the drawer is generated into every page instead of living beside a long-lived host, which is the shared root of most of the above
260801 · Face diagrams added on JL's ask, closing the QB4c §1 gap the quality check named: all 7 Content divisions now open with a fenced ascii figure as their FIRST line (verified 7/7); §1-§5 and §7 are new high-level figures drawn with /diagram-ascii, and §6's existing plugin→board mapping was MOVED up to the heading and given emoji rather than duplicated; no prose changed
260801 · Quality-check fixes applied: the ticked 🔌 M1 row left Decision Now for a new `### Decisions taken` record (QB4e §2 says a made decision moves out, and the section's own "CC ticks nothing here" line contradicted it); the ①-⑤ mega-checkbox split into five judgeable rows plus a new `### 🔭 Owed beyond the extension` group (QB4d §1: a box must be judgeable true or false); Boundary now redirects the trust axes to `QF4`. STILL OPEN for JL: Content §1-§7 answers the retired permission/engine question, not the trust question the 260801 Opening now asks, and no Content division opens with its face diagram (QB4c §1)
260731 1934 · "💬 answers a turn" became a STANDING check (`checks/run.py`, 0.89.0, home on `QC8`): smoke asks the live server's own interpreter for the SDK through `GET /_board/health` (the 3.9 restart trap: pages 200 while every chat turn dies), and the full tier runs one real scoped SDK turn (CHATOK) on a throwaway fixture
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 1705 · Regrouped ## Items to Finish into four context-named ### subsections per QB4d-items.md's deliver requirement (renderer auto-counts each group): 🚀 runs·resumes·cost · 🚦 permission gate · 💬 usable surface · 🧩 match the extension; every checkbox and its detail lines kept verbatim, only reordered under headings (asked as "QB4c", but QB4c is the Content face; QB4d owns Items)
260731 1650 · Redrew the ## Diagram block emoji-rich via /diagram-ascii: same flow (drawer → serve.py → claude_agent_sdk, 3 tiers), added box/label/status emoji; no content change
260731 · Goal restated by JL as "migrate the Claude Code VS Code plugin to our board": the layer-by-layer mapping is Content §6, the JS question answered in §5 (stay Python, parity checked at 47 options), and the 245MB binary identified as a byte-identical copy of the PATH CLI
260731 · Backend teardown landed as Content §1-§5 (JL: "make it exactly the same"): the extension bundles the same Agent SDK we run, the only engine gap is the held client, M1-M4 written, ⑤ rewind unparked, two Decision Now rows opened
260731 · Read the VS Code extension from disk (v2.1.220): bundled CLI, stream-JSON over stdio, WebSocket IDE bridge; the per-POST boot named as the root of "not that good", and a held-process architecture opened as a Decision Now
260730 · Added the open integration item for section/subsection heading focus; QAb3 owns the path and this drawer owns displaying and sending its focus packet
260725 · Chat header cleaned: neutral utility bar, quiet page id, full CSS-ellipsized title, consistent 32px controls, and stable `>_` terminal mark replacing the tiny keyboard emoji
260725 1115 · QD5 archived on JL's call (redundant with QD2/QD3: the index chatbot IS this drawer + the QD3 terminal on board.md); references cleaned in QD1 and board.md's QD intro; the "two agents, one file" rule stays open on QD1
260725 1050 · A chatbot on the index (JL's ask on QC2): the drawer accepts file=board.md (board-flavored rules + orientation in serve.py, chatOpen('board') + index fab in board.js, session: in board.md's header rendered as data-bsession). Verified: orientation answer, session resume, in-board Write allowed, /tmp Write denied. This question's own machinery untouched
260724 1510 · The wait line tells the truth now: serve.py emits stage events ("booting claude, the full tier loads the whole skill registry…" / "session up") so the drawer shows real progress instead of a static "…thinking"; the collapsed 💭 block is labeled "Thinking (N chars, click to reopen)". Also verified: RESUMED sessions stream thinking now (probe on QD4: 3 think events), yesterday's loose end ② is gone, cured by the explicit thinking={enabled} flag
260724 1455 · Diff preview at the gate BUILT (serve.py ask events carry `detail`, drawer renders −/+ blocks; node-checked; live pop owed: the E2E's full-tier boot outran the window, turn stopped clean, board.md untouched). The extension's backend anatomized in Where we are per JL's "duplicate it"; item ④ persistent-process named as the real remaining delta
260724 1350 · Console relay verified (boards_api.py pipes /_board/chat NDJSON through 8093, "RELAY OK" streamed); VS Code extension alignment analyzed per JL's question: same engine, adopt diff-preview → @-mentions → plan mode, skip checkpoints
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 1745 · Opening orientation: system_prompt carries prime_context (board/question/what it asks/comments/file); verified it answers QF2
260723 1730 · JL ruled: the drawer's claude also opens at the SPACE root (cwd = whole repo), matching QD3:
              sessions read the code they discuss; the system prompt switched to repo-root-relative paths. Restricted tier still edits only this question's files
260723 1720 · JL said "shut them down": all serve.py / ttyd / terminal sockets cleaned; nothing listens on 5599 or terminal ports.
              Files and code intact, restartable anytime. ⚠️ During the sweep, found other sessions/agents concurrently editing serve.py (scope widened to the whole repo) and QA2/QA5; before restarting the server, confirm exactly one session manages it.
260723 1710 · Added the collapsible thinking block (JL's ask): the server emits thinking_delta as `{"t":"think"}`; the drawer renders a collapsible 💭 Thinking
              (expands while thinking, folds when the answer arrives, click to reopen). Client done and pushed.
              Two known loose ends: ① seeing thinking requires a server running current code (now shut down per JL);
              ② resumed sessions do not stream thinking (QD2/QA4/QA6/QD3): only brand-new sessions do; that is Claude Code resume behavior, not a bug.
              An isolated probe confirmed the code path (EXACT server config → thinking_delta=3).
260723 1640 · Fixed two bugs (JL-reported): ① every reply falsely claimed "changes written" + Reload; the server now sets a `wrote` flag;
              only real Edit/Write reports a write and regenerates html; read-only replies no longer trigger it.
              ② the empty-reply fallback and several prompts were still Chinese; all English now ("(no text reply…)" etc.)
260723 1620 · System language defaults to English (CHAT_RULES/FULL_RULES + drawer UI); closed the 1305 comment
260723 1615 · Restricted tier switched to disallowed_tools hard-off for Bash/Task/Skill/Web: can_use_tool is not reliably called for Bash; verified blocked
260723 1610 · Permissions became three tiers (restricted/full·ask/full·auto), default full·ask; full tier loads skills, ~150 visible
260723 1345 · Chat opener icon 💬 → 🤖, distinguished from the comment dock's 💬 (talk to AI vs. humans commenting)
260723 1340 · Correction: the drawer stays a full right panel (haichat-inlab); the "💬 Chat" opener became a floating bottom-right button,
              shown in focus mode; JL wanted the opener in the corner, not the drawer moved there
260723 1330 · (briefly mis-built as a floating bottom-right box; reverted)
260723 1535 · Markdown rendering inside the drawer (small built-in renderer, escape-then-render, rendered during streaming too)
260723 1530 · The gate first genuinely fired: forced Edit on board.md, blocked at the tool layer, board.md unchanged
260723 1525 · Fixed hanging writes: query() closes the input stream → switched to ClaudeSDKClient
260723 1520 · The drawer renamed to a chat box
260723 1420 · Character streaming through, first text at 8.1s measured
260723 1415 · Model/effort selection, default claude-opus-4-8 + effort=high
260723 1410 · Stop key: ⏹ → /_board/stop + AbortController
260723 1405 · Drawer became a full right-side panel (after haichat-inlab's drawer)
260723 1400 · Fixed the two service-killing issues: reverse DNS 7.8s per request; two instances racing one port
260723 1335 · Three-step usage: sync first → one-click handle comments → reload
260723 1310 · Chat window done: a 💬 Chat per card, history per question
260723 1305 · Switched to the can_use_tool hard gate, after haichat-inlab
260723 1250 · /_board/chat through; cost $0.92 → $0.24
260723 1445 · Split out of QD1 as its own question (JL: chat / terminal / sdk, one question each)

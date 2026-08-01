# SDK version: the chat box
state: 🟡 PARTIAL
owner: CC
method: claude_agent_sdk + serve.py's /_board/chat; three selectable permission tiers (restricted / full·ask / full·auto)
session: ccda0c28-ef7e-47e0-a7e1-c13abc4f4cea
## Question
Open a conversation right inside the page: it reads this question's content and open comments, and edits this question's md.
How much permission should it get?

Too little permission and it cannot work; too much and a browser tab can edit the whole repo at will.
JL's direction is "same as the CLI": ask when asking is due, instead of a hard-coded whitelist.
The drawer is the most-used entry, lighter than opening a terminal, so without settled tiers either you dare not use it or you dare not hand it to anyone.
It and `QD3` are two forms of one need with entirely different trade-offs, so each must be settled on its own, neither bent to fit the other.


## Boundary
- ✅ Covered here
  **The web-drawer implementation**: the three permission tiers, streaming, markdown rendering, cost, and how it obeys `QD1`'s LAW.
- ↪ Covered elsewhere
  The rules themselves (levels, boundaries): that is `QD1`.
  Nor the real terminal: that is `QD3`.

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

### 2 · The protocol on that pipe
One pipe carries four kinds of traffic, all newline JSON.
Assistant output and partial deltas come up as ordinary messages; that is the half our drawer already renders.
The other three are the half we do not use yet: `control_request` (the CLI asking, which is how a permission prompt arrives), `control_response` (our answer, matched by `request_id`), and `control_cancel_request`.
`keep_alive` and `transcript_mirror` frames ride the same channel.
Setting `canUseTool` is what turns the channel on: the SDK appends `--permission-prompt-tool stdio`, and every gate decision then travels as a control message rather than a side channel.

### 3 · The one difference that matters, named exactly
The extension's read loop runs ONCE for the life of a session and pushes each new user turn into the live process with `inputStream.enqueue(...)`.
That is what `--input-format stream-json` buys: stdin is a STREAM of turns, not a single prompt, so one process serves the whole conversation.
Our `ClaudeSDKClient` has the identical capability, and its own docstring names our exact use case ("Building chat interfaces or conversational UIs", "Multi-turn conversations with context").
serve.py throws it away: `chat()` opens `async with ClaudeSDKClient(...)` inside a per-POST `anyio.run(run)`, so every message connects, runs one turn, and disconnects.
That single line is the whole "not that good": the 8.1s first token and the near-$0.9 full-tier message are both the cost of reconnecting and reloading the ~150-skill registry per message.

The blocker is equally specific, and it is not the protocol.
The SDK forbids using one client across async runtime contexts ("you must complete all operations with the client within the same async context"), while serve.py runs a fresh `anyio.run()` per request inside `ThreadingHTTPServer`.
So holding the client means one long-lived event-loop thread owning every live client, with queues in and out; the HTTP handler stops owning the loop and becomes a producer and consumer of it.

### 4 · What "exactly the same as the extension" costs, in milestones
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
The frame is not "make the drawer more like the plugin".
It is that the board becomes the plugin, and the mapping is one to one at every layer.

```
   VS Code plugin                          this board
   ───────────────────────────────────     ───────────────────────────────────
   webview/index.js      the chat UI  ─▶   board.html's drawer
   extension.js          the host     ─▶   serve.py
   vscode.postMessage    the wire     ─▶   POST /_board/chat + NDJSON
   bundled Agent SDK     the engine   ─▶   claude_agent_sdk  (same SDK)
   the claude binary                  ─▶   the same binary, from PATH
   IDE bridge (WebSocket)             ─▶   nothing yet, and this is the interesting one
```

The IDE bridge exists so the session can reach EDITOR surfaces: a diff in a real tab, the current selection, the language server's diagnostics.
On this board the editor IS the board page, so the equivalent already half exists and has different names: the sentence address is the selection, `QB5`'s lanes are the annotations, and `check.py`'s output is the diagnostics.
That is the one place where migrating means translating rather than copying, and it is where the board can end up better than the plugin rather than merely equal to it.

### 7 · What stays VS Code only, and does not matter
The IDE bridge is the one piece we cannot copy, because it exists to put things in EDITOR surfaces: a diff in a real editor tab, the current text selection, the language server's diagnostics.
The drawer answers the same need in its own surface and already ships the important half, the diff preview at the permission gate.
So "exactly the same" is exact at the engine and protocol layer, and deliberately different at the surface layer, which is the alignment line this page already holds.

## Items to Finish
### 🚀 It runs, resumes, and pays its way
- [x] Starts a session, reads board files, answers correctly
      `claude-agent-sdk 0.2.126`, verified.
- [x] No separate auth work
      The SDK drives the machine's `claude` CLI and inherits the logged-in OAuth (`~/.claude/.credentials.json`).
      Same as `haichat-inlab`; read its source: zero special OAuth handling.
- [x] Sessions resume, and visibly so
      `session:` sits in the Q file header, beside `state:` / `owner:`.
- [x] Cost squeezed to acceptable
      Default $0.92 → **$0.24** after narrowing; a follow-up message **$0.012**.

### 🚦 The permission gate is real
- [x] Three permission tiers, default "full·ask" (JL 260723)
      A dropdown at the drawer's bottom: restricted-to-this-Q / full·ask / full·auto.
      Full tiers use setting_sources=["user","project","local"] → **the Skill tool is available; ~150 skills visible in practice**.
      "full·ask" prompts per tool call (= CLI default behavior), "full·auto" = bypassPermissions, zero prompts.
- [x] The restricted tier actually restrains
      can_use_tool is not reliably invoked for Bash in default mode (verified: Bash slipped through), so the restricted tier hard-disables Bash/Task/Skill/Web via `disallowed_tools`, an SDK-level blacklist, no callback involved.
      Verified: forcing Bash in restricted mode reports "Bash exists but is not enabled in this context".
- [x] The hard gate has been genuinely triggered
      Forced a real `Edit` against `board.md`; the tool layer blocked it: `denied: ['Edit -> …/board.md']`, `board.md` untouched.
      The check compares **resolved absolute paths**, not name strings.

### 💬 The drawer is a usable surface
- [x] Compact shortcut and settings menus (260731)
      The drawer now starts with only two small buttons: `✨ Quick actions` and `⚙ Settings`.
      The first reveals one-click, read-only prompts — Quality Check, Where are we?, What next?, Clarify aim, and the page/board-specific missing-item prompt. The second reveals model, effort, permission tier, session controls, and cost. Only one panel opens at a time, and starting a turn closes it again.
- [x] An entry on the page
      A `💬 Chat` per card; a full right-side drawer (modeled on haichat-inlab's drawer).
- [x] Character-level streaming
      `include_partial_messages` → `content_block_delta`, NDJSON as-it-comes.
      Measured: first text at 8.1s.
- [x] Model and effort selectable
      Opus 4.8 / Sonnet 5 / Haiku 4.5 × low→max, default **opus + high**.
- [x] Stoppable mid-run
      ⏹ → `/_board/stop` raises a flag (wraps up at the next message boundary) + browser `AbortController`.
- [x] Acts on comments
      Opening the drawer first syncs unsaved comments, then one button "🔧 handle N open comments" sends a ready-made prompt.
- [x] Markdown renders inside replies
      The drawer carries a small renderer (headings / lists / code blocks / inline code / bold-italic), escape-then-render, no third-party library.
      Rendered even while streaming.
- [x] System language defaults to English
      CHAT_RULES / FULL_RULES both say "Answer in English by default"; the drawer UI is fully English.
- [x] The drawer works through the console too (260724)
      `haichat-inlab`'s `boards_api.py` relays `/_board/chat` (NDJSON stream), `/_board/answer`, `/_board/stop` to the workstation serve.py; verified end to end: a "Reply with exactly: RELAY OK" turn streamed `delta`/`done` lines through port 8093.
      One implementation; the console is only a pipe (`QE3`'s Law).
- [x] The drawer header is a clean utility bar (JL 260725)
      The heavy blue banner became a neutral 56px header with a small mono page id, a single-line title that ellipsizes only when space runs out, and two compact square controls.
      The terminal control uses stable `>_` text instead of a tiny platform-dependent keyboard emoji; both controls have hover, keyboard-focus, tooltip, and accessible labels.

### 🧩 Match the VS Code extension
- [ ] Align the drawer with the Claude Code VS Code extension (JL 260724: "I want to duplicate it")
      Same engine underneath already (see Where we are, the extension's backend IS the local claude runtime this drawer drives).
      Progress: ① diff preview inside the permission prompt, BUILT 260724: the ask event now carries `detail` (Edit: old/new; Write: current-file vs proposed; MultiEdit: per-edit pairs; Bash: the command), and the drawer renders − red / + green blocks above Allow/Deny.
      Emitted JS node-checked; a live gate-pop is still owed (the full-tier E2E boots ~150 skills and outran the test window; the turn was stopped cleanly and board.md verified untouched). ② @-file mentions (type `@` to pull a repo file into context): open, and ours to build (Content §4 M4); ③ plan mode toggle (read-only planning turn before edits): open, and it is `--permission-mode plan` reached through M2's `set_permission_mode()`; ④ persistent process per session: open, and now specified as Content §4 M1, the session-host thread; the 260731 teardown proved this is the ONLY engine-layer gap and named its blocker (a client cannot cross async runtime contexts, and serve.py runs a fresh `anyio.run` per POST); ⑤ checkpoints/rewind: UNPARKED 260731, it is `rewind_files()` (M3), and it stopped fighting the LAW when JL amended `QD1` to many sessions per question.
- [ ] Long tasks
      Today one HTTP request waits start to finish.
      A ten-minute job will hit the timeout.
      (Note: NOT the same root as the old "writes hang" issue; that one was diagnosed and fixed, see Lesson.)
- [ ] Section and subsection focus packets
      Accept the generated heading path from `QAb3`, display it in the existing Focus card, and send page id, section/subsection names, source file, and visible block with the next user message.

## Where we are
Usable.
The `🤖 Chat` you click on the page is this.

- The control surface is compact by default (JL 260731)
      Configuration no longer occupies permanent vertical space in the drawer. A user chooses either Quick actions or Settings when needed; action chips are hidden again as soon as a message starts. Quality Check remains server-enforced read-only even if Settings previously selected full auto.

- Reading the extension named the real gap, and a fourth architecture with it (JL 260731)
      JL: "I feel the current SDK chatbot is somehow not that good?"
      The engine is not the gap.
      `claude_agent_sdk` spawns the same binary over the same stream-JSON protocol the extension drives, so SDK and CLI are one engine wearing two harnesses, and no capability is missing by construction.
      The gap is that serve.py boots a `claude` per POST while the extension holds one per session, and that single fact is the root of both symptoms: first text at 8.1s and a full-tier message near $0.9, because every message reloads the ~150-skill registry.
      The code already says so out loud, in the stage line it emits while you wait ("booting claude, the full tier loads the whole skill registry, the first message is the slow one").
      The consequence is larger than item ④ was written to be.
      If serve.py holds `claude --input-format stream-json --output-format stream-json` open per question and writes into its stdin, it gets a live structured event stream with no boot cost, no screen to repaint, and the permission channel intact.
      That is `QD3m` route B without the jsonl tail: myrlin reads the transcript off disk because it does not own the process, and we do own it.
      So this page and `QD3m` may be converging on one build instead of two.

- Section/subsection focus is designed, not implemented (JL 260730)
      `QAb3` now defines one generated breadcrumb per visible heading plus Copy and Chat actions.
      This drawer remains the one engine and one page session; it only needs to accept the new heading-focus packet alongside the existing sentence-focus packet.

- The chat header is now quiet and scannable (JL 260725)
      The screenshot showed four competing shapes in one bright strip: a muted pill, oversized title, tiny keyboard glyph inside a large button, and a circular close button.
      The revised header uses one neutral surface and one control shape; id is metadata, title owns the remaining width, and terminal/close sit as a consistent pair.

- The drawer also opens from the index page (JL 260725: "just add a chatbot in the index page")
      The bottom-right 🤖 button on the index opens this same drawer with `file=board.md`: the orientation block carries the index's view (spine, close, every page's state and open comments), the restricted tier's "own files" widens to any `.md` inside the board folder (verified 260725: an in-board Write passed, a /tmp Write was denied), and the session id sits in `board.md`'s header (`session:` under `close:`), resuming like any question's.
      Everything else is unchanged: three tiers, streaming, the gate, ⌨ to the `QD3` terminal.
      No second engine.

- Three permission tiers, dropdown at the drawer bottom (JL ruled 260723, default "full·ask")
      · restricted-to-this-Q: setting_sources=[], read + edit this question's files only, Bash/Task/Skill/Web hard-off, cheap ($0.24, no skills) · full·ask: all tools + all skills; touching anything else prompts allow-once / always / deny (= CLI default) · full·auto: permission_mode=bypassPermissions, zero prompts (= --dangerously-skip-permissions) Switching to "full" loads the skill registry; a message climbs back to ~$0.9; the restricted tier skips that bill.
- Skills are callable now
      Full tiers with setting_sources=["user","project","local"] → the Skill tool appears; it counted ~150 skills, can invoke diagram-ascii, haipipe-paper and the like by name.
      Exactly the "open like the CLI" goal.
- The three tiers restrain differently
      Restricted: `disallowed_tools` hard-off for dangerous tools (can_use_tool is not reliably called for Bash; the blacklist is the solid way). full·ask: permission_mode=default + can_use_tool, per-call prompts (writing allowed_tools or switching mode bypasses the callback, the inlab pitfall). full·auto: permission_mode=bypassPermissions, no callback at all.
- Knows its question the moment it opens (JL 260723)
      The system_prompt carries a `prime_context` block: board + question id + title + what it asks + open comment count + file path.
      So the first thing you type, it already has the background.
      Verified: restricted tier, no context given, asked "which question are you on", answered QF2 · Fresh-agent acceptance test.
- Sessions open at the SPACE root, not the board folder (JL 260723)
      `ClaudeAgentOptions(cwd=...)` now points at the whole repo, matching the QD3 terminal: a session must read the code it discusses; the board folder alone is too narrow.
      The system prompt hands out repo-root-relative paths, not bare file names.
      The restricted tier still edits only this question's files (can_use_tool compares absolute paths); full tiers open up.
      Same Lesson as QD3: changing cwd strands old sessions; every question restarted under root.
- Python comes from the repo's own venv
      The SDK needs 3.10+; system `python3` is 3.9.6.
      The repo `.venv` is 3.13.14, fine; it has no pip because **uv manages it**: `uv pip install --python .venv/bin/python claude-agent-sdk`.
- The three-step usage (JL's)
      ① open the drawer, unsaved comments sync first → ② click "🔧 handle N open comments" → ③ "↻ reload the page to see the result".
      The server regenerates the html after editing the md, so a reload suffices.

**🧩 How the Claude Code VS Code extension relates (JL asked 260724; "duplicate it" is the goal)**

- Its backend, anatomically (inferred 260724, read from disk 260731 at v2.1.220)
      The extension does NOT implement an agent.
      `resources/native-binary/claude` is a 245MB copy of the CLI that the extension SHIPS and spawns itself, so it never depends on the `claude` on your PATH.
      `extension.js` talks to that subprocess in stream-JSON over stdin and stdout, the exact protocol `claude_agent_sdk` wraps; the bundle's flag surface includes `--input-format`, `--output-format`, `--include-partial-messages`, `--fork-session`, `--no-session-persistence`, `--max-turns`, `--max-budget-usd`, `--effort`, and `--model`.
      Permissions come back as control messages on that channel (what our `can_use_tool` receives); one process stays alive across the turns of a session; sessions land in the same `~/.claude/projects/<cwd>/<sid>.jsonl`; auth is the CLI's own login.
      `webview/index.js` is a 5MB chat UI: web chat, never a terminal.
      The IDE bridge runs the opposite way from how it reads: the EXTENSION listens on a WebSocket and the CLI dials OUT to it, discovering it through `~/.claude/ide/<pid>.lock` (`{"pid":…,"workspaceFolders":[…],"ideName":"Visual Studio Code","transport":"ws","authToken":…}`, two live on this machine right now).
      That bridge is what carries the editor-native affordances: the diff view, selection context, diagnostics.
- So the drawer already IS the duplicate, at the engine layer
      serve.py's `chat()` = ClaudeSDKClient = the same subprocess + protocol + session store + permission channel.
      What differs is the shell around it: the extension holds ONE live process per session (instant follow-ups), and its gate shows the proposed edit.
      The first is item ④ above; the second shipped today (①).
- What the drawer already matches
      allow-once / always / deny prompts (= the extension's permission dialog) · character streaming with a collapsible thinking block · model + effort pickers · per-turn cost · resumable sessions.
- What the extension has that the drawer lacks
      @-file mentions · plan mode · checkpoints/rewind (parked: it fights the one-window rule) · ONE live process per session (item ④, the real architectural delta).
      Two former gaps have closed since this list was written: the diff preview at the permission prompt (① BUILT 260724), and the session picker, which flipped from "deliberately NOT wanted" to SHIPPED on 260731 when JL amended `QD1`'s Law to one Q, many sessions (the drawer's 🗂 Session strip).
- The alignment line to hold
      adopt affordances, never a second engine: everything stays `serve.py` + `claude_agent_sdk`; the drawer copies the extension's UX where it makes the gate more informed (diff preview first).
      Holding the process ourselves does not cross that line: it is the same binary and the same protocol the SDK already drives, with the subprocess kept instead of dropped.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [x] 🔌 Approve the session host, M1 (JL 260731: "make the chatbot sdk version exactly the same to the vscode claude code plugin version")
      BUILT and measured 260731 on JL's go-ahead; the numbers and the correction they force are in Where we are.
      The teardown says exactly-the-same is reachable, because the extension runs the SAME SDK we already run; the only engine-layer gap is that it holds the client and we drop it every POST (Content §3).
      M1 is one daemon thread owning a long-lived event loop plus a per-question client registry, with the browser protocol unchanged.
      A · M1 is built now, one daemon thread owning a long-lived event loop; streaming-mode verbs (`interrupt`, `set_model`, `set_permission_mode`, `get_context_usage`, `rewind_files`) become reachable immediately.
      B · the boot is shrunk by warming a pool and caching the registry; streaming-mode verbs still cannot be reached because the client continues to be dropped after each turn.
      C · the current per-POST architecture stays; it continues to suffer from slow first token and high full-tier cost.
      → CC's proposal: A; B treats the symptom and still cannot reach `interrupt`, `set_model`, `set_permission_mode`, `get_context_usage`, or `rewind_files`, which are streaming-mode only.
- [ ] 🐍 Rule the language, before M1 is written (JL 260731: "can I change it to the js version, using the extension.js?")
      `extension.js` itself cannot be reused at all (it loads `require("vscode")`), so the real question is Python SDK against the npm TypeScript SDK, and Content §5 checked parity rather than assuming it: 47 Python options cover every flag the extension emits, plus `extra_args`.
      A · stay Python inside serve.py; the slowness root (dropped client, not language) gets fixed by M1 in the same codebase.
      B · a second Node service sits beside serve.py and is proxied; the server splits across two runtimes and manages two dependency chains for the same SDK.
      C · serve.py is rewritten in Node; the entire ~2600-line server moves to a different runtime, affecting all twenty other endpoints, not just chat.
      → CC's proposal: A; the two SDKs are the same SDK, the slowness is the dropped client and not the language, and B or C splits a ~2600-line server that owns twenty other endpoints across two runtimes for zero capability gained.
- [ ] 🧊 Rule how a held session is reaped
      A held client is a live `claude` process per question, so something must end it: idle timeout, page close, or explicit release.
      A · a held client dies on idle timeout plus the existing pagehide beacon; reaping mirrors QD3's terminal reaping and requires no new user gesture.
      B · a held client requires explicit release only; the user must manually close the session and timeout is not checked.
      C · a held client dies on timeout only; pagehide beacon is not used, so a closed page does not free the process.
      → CC's proposal: A; it matches how `QD3`'s terminals already die and needs no new gesture from you.
- [ ] 🔀 Rule whether QD2 and QD3m are one build or two
      A held stream-JSON process would serve both this drawer and `QD3m`'s smooth view, which were designed as separate front ends.
      A · QD2 and QD3m merge into one held-process view with the raw ⌨ pane beside it, unified by one child process; the merge becomes coherent once the process is held per the row above.
      B · QD2 (SDK drawer) and QD3m (smooth view) stay as distinct faces, each potentially with its own process management, because merging them conflicts with the current architecture.
      → CC's proposal: A, but only after the row above is ticked; the merge is only coherent if the process is held.
- [ ] 🧲 Pick which remaining extension affordance comes next
      A · @-file mentions are built next; they add a UI feature on top of the slow boot, leaving the cost untouched.
      B · plan mode is built next; it adds another UI feature but does not fix the boot cost that is the real pain point.
      C · neither @-mentions nor plan mode are built this round; the effort goes to fixing the engine (M1) because the boot cost is what you actually feel.
      → CC's proposal: C; both are chrome on a harness whose boot cost is the thing you actually feel.

## Files
### The host
- `serve.py`
  `chat()`: `ClaudeSDKClient` + the `can_use_tool` permission callback + NDJSON streaming, all here.

### The drawer surface
- `build.py`
  The generator embeds the drawer assets into each self-contained board page.
- `assets/board.js`
  Drawer markup and behavior, including title binding and terminal/chat mode switching.
- `assets/board.css`
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

# QPf4b-chat-sdk · outline v1
outline-version: v1
supersedes: —
date: 260817
approved: ⬜            🚧 a person ticks this. No machine may.

Generated 260817 from this page's own divisions, face-figure captions and
sentences, so no bullet claims anything the page does not already say.
UNAPPROVED, so it is a working document: rewrite it, delete what is wrong.

## C1 · The plugin runs the same engine we already run (read from v2.1.220, 260731)

### C1.P1 · its three layers, and which one really talks to Claude
- B1 · The plugin does not build an agent of its own.
- B2 · It does not build its own message format either.
- B3 · It packs in the TypeScript Agent SDK and drives it, and `extension.js` gives that away in its own option names.
- B4 · Our Python `claude_agent_sdk` offers those same option names, because it is the same SDK in two languages.
- B5 · That 245MB file is not a special build, and it is not a second product (JL asked, 260731).
- B6 · It is the Claude Code CLI compiled into one Mach-O program, with the Node runtime and every dependency baked in, and that is the whole reason it is so big.
- B7 · Checked on this machine: `shasum -a256` matches `~/.local/share/claude/versions/2.1.220` byte for byte, and that is exactly what `claude` on the PATH points to.
- B8 · ⚠️ 13 more sentences in this division are not planned here yet

## C2 · One pipe carries the answers and the permission asks

### C2.P1 · what travels each way between us and the CLI, on one pipe
- B1 · One pipe carries four kinds of traffic, and all of them are JSON, one object per line.
- B2 · The answer text and its partial pieces arrive as ordinary messages, and that is the half our chat box already draws.
- B3 · The other three are the half we do not use yet.
- B4 · `keep_alive` and `transcript_mirror` messages ride the same channel.
- B5 · Setting `canUseTool` is what turns that channel on.
- B6 · The SDK then adds `--permission-prompt-tool stdio`, and every allow or deny travels as a control message instead of on a side channel.

## C3 · We started a new claude for every message, and that was the whole cost

### C3.P1 · how the plugin serves a conversation, and how serve.py used to
- B1 · The plugin's read loop runs ONCE for the life of a session, and it pushes each new user turn into the live process with `inputStream.enqueue(...)`.
- B2 · That is what `--input-format stream-json` buys: stdin is a STREAM of turns, not a single prompt, so one process serves the whole conversation.
- B3 · Our `ClaudeSDKClient` can do exactly the same.
- B4 · Its own docstring even names our use case ("Building chat interfaces or conversational UIs", "Multi-turn conversations with context").
- B5 · serve.py threw that away.
- B6 · `chat()` opened `async with ClaudeSDKClient(...)` inside a per-POST `anyio.run(run)`, so every message connected, ran one turn, and disconnected.
- B7 · That single line was the whole "not that good".
- B8 · ⚠️ 7 more sentences in this division are not planned here yet

## C4 · What it takes to match the plugin, in four steps

### C4.P1 · what M1 unlocks, and what falls out of it for free
- B1 · A daemon thread runs one asyncio loop for the life of the process, and `SESSIONS[question] -> {client, inbox, outbox}` holds the clients.
- B2 · `chat()` stops calling `anyio.run`.
- B3 · It hands the message to the loop, then drains that session's outbox into the NDJSON stream we already have, so the browser side does not change at all.
- B4 · Idle reaping and the `QD1` HOLD keep their current rules.
- B5 · Four `ClaudeSDKClient` methods work ONLY in streaming mode, and none of them can be reached today.
- B6 · `interrupt()` replaces our flag that waits for the next message boundary.
- B7 · `set_model()` and `set_permission_mode()` switch mid-conversation with no reboot.
- B8 · ⚠️ 6 more sentences in this division are not planned here yet

## C5 · Moving to JavaScript would buy us nothing (JL asked 260731)

### C5.P1 · which of them we could use, and what each one would gain
- B1 · Three different things get called "the JS version", and they have three different answers.
- B2 · It is a VS Code plugin-host module that calls `require("vscode")` all through, exports no public API, and ships as one 2.5MB minified bundle.
- B3 · Outside VS Code the `vscode` module does not exist, so the file cannot even load.
- B4 · But it is the SAME SDK as our Python one, so taking it is a change of language, not a change of what we can do.
- B5 · There is nothing we would gain by switching.
- B6 · So the advice is to stay in Python, and the strongest evidence is what else serve.py is (JL asked 260731, "what does serve.py do besides the claude code?").
- B7 · Measured on 260731 it was 2938 lines across 20 HTTP routes plus the terminal WebSocket, with chat one job out of seven.
- B8 · ⚠️ 10 more sentences in this division are not planned here yet

## C6 · The board becomes the plugin, layer by layer (JL 260731)

### C6.P1 · which piece of the VS Code plugin each piece of this board already is
- B1 · The goal is not "make the chat box more like the plugin".
- B2 · It is that the board becomes the plugin, and the map is one to one at every layer.
- B3 · The IDE bridge exists so a session can reach things inside the EDITOR: a diff in a real tab, the current selection, the language server's warnings.
- B4 · On this board the editor IS the board page, so the same thing already half exists under different names.
- B5 · The sentence address is the selection, `QB8`'s `>` lines are the notes, and `check.py`'s output is the warnings.
- B6 · That is the one place where copying means translating instead, and it is where the board can end up better than the plugin rather than only equal to it.

## C7 · The one piece we cannot copy, and why it does not hurt

### C7.P1 · what it reaches, and where we choose to be different
- B1 · The IDE bridge is the one piece we cannot copy.
- B2 · It exists to put things inside the EDITOR: a diff in a real editor tab, the current text selection, the language server's warnings.
- B3 · The chat box answers the same need in its own view, and it already ships the important half, the diff preview at the permission check.
- B4 · So "exactly the same" is exact at the engine and at the message format, and different on purpose in what the reader sees.
- B5 · That is the line this page already holds.

## C8 · Four things a terminal has for free, and the chat box did not

### C8.P1 · what nobody gave the chat box, and how many defects each one caused
- B1 · JL asked twice on 260801 whether the day's problems should become a part named for what the reader sees, something like Mobile Usage or UI Experience.
- B2 · The first answer here was no, because filing them under UI would file architecture under taste.
- B3 · That answer was half right.
- B4 · The grouping by OWNER stands, because every defect arrived as a feeling about the interface and turned out to be a fact about where state lives.
- B5 · The NAME was a picture that told a cold reader nothing.
- B6 · The subject is the interface, and the Opening already says why it needs one.
- B7 · A terminal carries its own behaviour, a chat box we draw has to be given all of it, and this part is the list of what nobody gave it.
- B8 · ⚠️ 48 more sentences in this division are not planned here yet

## C9 · One build closes most of them, and the terminal already had it

### C9.P1 · the ring the terminal keeps, and the socket chat wrote to instead
- B1 · The target was not a new architecture.
- B2 · It was the one QD3 already shipped.
- B3 · A terminal survives a reload because its bytes go to a RING that clients attach to.
- B4 · Chat's bytes went straight down the socket of whoever happened to ask.
- B5 · That single difference was the mechanism under three of the five rows above, and it is why the VS Code panel felt different rather than only nicer.
- B6 · `live/turnring.py` is the module.
- B7 · It holds one `Turn` per question key, and every event carries a counter `n` that only goes up.
- B8 · ⚠️ 40 more sentences in this division are not planned here yet

## C10 · The ten things a reader does, and the check that holds each one

### C10.P1 · how to open the chat, and what a reader does once inside
- B1 · Every row above is a gesture, not a feature, and each one is held by an assertion in `checks/guichat.mjs`.
- B2 · Read this part as the manual and the test list at once.
- B3 · If a row here is wrong, the check that names it is the thing to run.
- B4 · A plain board url gives the original one-page board, where the chat is the 💬 button at the bottom right, and that button asks which of the two you want.
- B5 · Being in the split is remembered, so a plain url after using the split gives you the split back.
- B6 · `?plain` is how you ask for the single page on purpose.
- B7 · Scrolling up during a turn is respected, and the next token will not drag you back down.
- B8 · ⚠️ 8 more sentences in this division are not planned here yet


# SDK version: the chat box
state: 🟡 PARTIAL
owner: CC
method: claude_agent_sdk + serve.py's /_board/chat; three selectable permission tiers (restricted / full·ask / full·auto)
session: ccda0c28-ef7e-47e0-a7e1-c13abc4f4cea
## Question
Open a conversation right inside the page: it reads this question's content and open comments, and edits this question's md. How much permission should it get?

- Why it is hard
  Too little and it cannot work; too much and a browser tab can edit the whole repo at will. JL's direction: "same as the CLI" — ask when asking is due, instead of a hard-coded whitelist.
- What breaks if we leave it
  The drawer is the most-used entry (lighter than opening a terminal). Without settled tiers, either you dare not use it or you dare not hand it to anyone.
- What it affects downstream
  It and `QD3` are two forms of one need with entirely different trade-offs — each must be settled on its own, neither bent to fit the other.

## Boundary
- ✅ Covered here
  **The web-drawer implementation**: the three permission tiers, streaming, markdown rendering, cost, and how it obeys `QD1`'s LAW.
- ↪ Covered elsewhere
  The rules themselves (levels, boundaries) — that is `QD1`. Nor the real terminal — that is `QD3`.

## Diagram
```
  browser right-side drawer            serve.py (on the machine the files are on)
  ┌──────────────────┐   POST         ┌────────────────────────────────┐
  │ QD2  title       │ /_board/chat   │ claude_agent_sdk               │
  │ ┌ bubbles ─────┐ │ ─────────────► │  cwd = SPACE root (whole repo) │
  │ │ streams live │ │                │  reads the code it discusses,  │
  │ └──────────────┘ │ ◄───────────── │  not just the board folder     │
  │ 🔧 handle N cmts │  one JSON      │  can_use_tool ─ the gate (3 tiers)│
  │ Opus4.8 / high   │  per line      │    restricted: this Q's files only│
  │ [input] [⏹]     │                │    full·ask: prompts for the rest │
  └──────────────────┘                │    full·auto: bypass, no prompts  │
                                      └───────────┬────────────────────┘
                                                  │ build.py after edits
                                                  ▼  reload the page to see it
```

## Items to Finish
- [x] Starts a session, reads board files, answers correctly
      `claude-agent-sdk 0.2.126`, verified.
- [x] No separate auth work
      The SDK drives the machine's `claude` CLI and inherits the logged-in OAuth (`~/.claude/.credentials.json`).
      Same as `haichat-inlab` — read its source: zero special OAuth handling.
- [x] Cost squeezed to acceptable
      Default $0.92 → **$0.24** after narrowing; a follow-up message **$0.012**.
- [x] Sessions resume, and visibly so
      `session:` sits in the Q file header, beside `state:` / `owner:`.
- [x] An entry on the page
      A `💬 Chat` per card; a full right-side drawer (modeled on haichat-inlab's drawer).
- [x] Character-level streaming
      `include_partial_messages` → `content_block_delta`, NDJSON as-it-comes. Measured: first text at 8.1s.
- [x] Model and effort selectable
      Opus 4.8 / Sonnet 5 / Haiku 4.5 × low→max, default **opus + high**.
- [x] Stoppable mid-run
      ⏹ → `/_board/stop` raises a flag (wraps up at the next message boundary) + browser `AbortController`.
- [x] Acts on comments
      Opening the drawer first syncs unsaved comments, then one button "🔧 handle N open comments" sends a ready-made prompt.
- [x] The hard gate has been genuinely triggered
      Forced a real `Edit` against `board.md`; the tool layer blocked it:
      `denied: ['Edit -> …/board.md']`, `board.md` untouched.
      The check compares **resolved absolute paths**, not name strings.
- [x] Markdown renders inside replies
      The drawer carries a small renderer (headings / lists / code blocks / inline code / bold-italic),
      escape-then-render, no third-party library. Rendered even while streaming.
- [x] Three permission tiers, default "full·ask" (JL 260723)
      A dropdown at the drawer's bottom: restricted-to-this-Q / full·ask / full·auto.
      Full tiers use setting_sources=["user","project","local"] → **the Skill tool is available; ~150 skills visible in practice**.
      "full·ask" prompts per tool call (= CLI default behavior), "full·auto" = bypassPermissions, zero prompts.
- [x] The restricted tier actually restrains
      can_use_tool is not reliably invoked for Bash in default mode (verified: Bash slipped through),
      so the restricted tier hard-disables Bash/Task/Skill/Web via `disallowed_tools` — an SDK-level blacklist, no callback involved.
      Verified: forcing Bash in restricted mode reports "Bash exists but is not enabled in this context".
- [x] System language defaults to English
      CHAT_RULES / FULL_RULES both say "Answer in English by default"; the drawer UI is fully English.
- [x] The drawer works through the console too (260724)
      `haichat-inlab`'s `boards_api.py` relays `/_board/chat` (NDJSON stream), `/_board/answer`, `/_board/stop` to the workstation serve.py — verified end to end: a "Reply with exactly: RELAY OK" turn streamed `delta`/`done` lines through port 8093. One implementation; the console is only a pipe (`QE3`'s Law).
- [ ] Align the drawer with the Claude Code VS Code extension (JL 260724: "I want to duplicate it")
      Same engine underneath already (see Where we are — the extension's backend IS the local claude runtime this drawer drives). Progress:
      ① diff preview inside the permission prompt — BUILT 260724: the ask event now carries `detail` (Edit: old/new; Write: current-file vs proposed; MultiEdit: per-edit pairs; Bash: the command), and the drawer renders − red / + green blocks above Allow/Deny. Emitted JS node-checked; a live gate-pop is still owed (the full-tier E2E boots ~150 skills and outran the test window; the turn was stopped cleanly and board.md verified untouched).
      ② @-file mentions (type `@` to pull a repo file into context) — open;
      ③ plan mode toggle (read-only planning turn before edits) — open;
      ④ persistent process per session (the extension keeps one claude process alive across turns; the drawer boots one per POST — the real architectural delta, and the fix for slow full-tier boots) — open;
      ⑤ checkpoints/rewind — parked; it fights the one-session-per-question LAW.
- [ ] Long tasks
      Today one HTTP request waits start to finish. A ten-minute job will hit the timeout.
      (Note: NOT the same root as the old "writes hang" issue — that one was diagnosed and fixed, see Lesson.)

## Where we are
Usable. The `💬 Chat` you click on the page is this.

- Three permission tiers, dropdown at the drawer bottom (JL ruled 260723, default "full·ask")
      · restricted-to-this-Q — setting_sources=[], read + edit this question's files only, Bash/Task/Skill/Web hard-off, cheap ($0.24, no skills)
      · full·ask — all tools + all skills; touching anything else prompts allow-once / always / deny (= CLI default)
      · full·auto — permission_mode=bypassPermissions, zero prompts (= --dangerously-skip-permissions)
      Switching to "full" loads the skill registry; a message climbs back to ~$0.9; the restricted tier skips that bill.
- Skills are callable now
      Full tiers with setting_sources=["user","project","local"] → the Skill tool appears; it counted ~150 skills,
      can invoke diagram-ascii, haipipe-paper and the like by name. Exactly the "open like the CLI" goal.
- The three tiers restrain differently
      Restricted: `disallowed_tools` hard-off for dangerous tools (can_use_tool is not reliably called for Bash; the blacklist is the solid way).
      full·ask: permission_mode=default + can_use_tool, per-call prompts (writing allowed_tools or switching mode bypasses the callback — the inlab pitfall).
      full·auto: permission_mode=bypassPermissions — no callback at all.
- Knows its question the moment it opens (JL 260723)
      The system_prompt carries a `prime_context` block: board + question id + title + what it asks +
      open comment count + file path. So the first thing you type, it already has the background.
      Verified: restricted tier, no context given, asked "which question are you on" — answered QB2 · Fresh-agent acceptance test.
- Sessions open at the SPACE root, not the board folder (JL 260723)
      `ClaudeAgentOptions(cwd=...)` now points at the whole repo, matching the QD3 terminal — a session must read the code it discusses;
      the board folder alone is too narrow. The system prompt hands out repo-root-relative paths, not bare file names.
      The restricted tier still edits only this question's files (can_use_tool compares absolute paths); full tiers open up.
      Same Lesson as QD3: changing cwd strands old sessions; every question restarted under root.
- Python comes from the repo's own venv
      The SDK needs 3.10+; system `python3` is 3.9.6. The repo `.venv` is 3.13.14 — fine;
      it has no pip because **uv manages it**: `uv pip install --python .venv/bin/python claude-agent-sdk`.
- The three-step usage (JL's)
      ① open the drawer, unsaved comments sync first → ② click "🔧 handle N open comments" → ③ "↻ reload the page to see the result".
      The server regenerates the html after editing the md, so a reload suffices.

**🧩 How the Claude Code VS Code extension relates (JL asked 260724; "duplicate it" is the goal)**

- Its backend, anatomically
      The extension does NOT implement an agent. It spawns the machine's own `claude` binary as a subprocess and speaks the stream-JSON agent protocol over stdin/stdout — the exact protocol `claude_agent_sdk` wraps. Permissions come back as control messages on that channel (what our `can_use_tool` receives); one process stays alive across the turns of a session; sessions land in the same `~/.claude/projects/<cwd>/<sid>.jsonl`; auth is the CLI's own login. On top sits a webview UI plus an IDE bridge (a small local service the CLI discovers via `~/.claude/ide/` lockfiles) for editor-native affordances: the diff view, selection context, diagnostics.
- So the drawer already IS the duplicate, at the engine layer
      serve.py's `chat()` = ClaudeSDKClient = the same subprocess + protocol + session store + permission channel. What differs is the shell around it: the extension holds ONE live process per session (instant follow-ups), and its gate shows the proposed edit. The first is item ④ above; the second shipped today (①).
- What the drawer already matches
      allow-once / always / deny prompts (= the extension's permission dialog) · character streaming with a collapsible thinking block · model + effort pickers · per-turn cost · resumable sessions.
- What the extension has that the drawer lacks
      diff preview at the permission prompt · @-file mentions · plan mode · checkpoints/rewind · a session picker (deliberately NOT wanted here — one session per question is the LAW).
- The alignment line to hold
      adopt affordances, never a second engine: everything stays `serve.py` + `claude_agent_sdk`; the drawer copies the extension's UX where it makes the gate more informed (diff preview first).

## Files
- `serve.py`
  `chat()` — `ClaudeSDKClient` + the `can_use_tool` permission callback + NDJSON streaming, all here.
- `build.py`
  The drawer UI (`#chat` / `#chatfab`) and markdown rendering live in the page script.

## Lesson
**`query()` closes the input stream once the prompt generator is exhausted — then `can_use_tool` has nowhere to reply.**
The symptom was bizarre: reads fine, writes hang, `Tool permission request failed: AbortError: Stream closed`.
The permission callback's allow/deny answer travels back to the CLI over the stdin control channel.
`query(prompt=<one-shot async generator>)` closes that stream right after the message is sent —
reads usually ask before the close and pass; writes ask later, the channel is gone, the CLI times out.
Switching to `ClaudeSDKClient` (connection held for the whole turn) fixed it immediately.
**`haichat-inlab` always used `ClaudeSDKClient`, never `query()`** — the port missed exactly this.
Lesson: when copying someone's code, copy **why this API and not that one** along with it.


**One port, one server.**
Chasing "page unresponsive / chat gives no response" ended at two stacked causes:
① reverse DNS — `SimpleHTTPRequestHandler.address_string()` runs `getfqdn()` on the client IP by default,
   costing 7.8 seconds per request on this machine. Overridden to return the raw IP.
② two `serve.py` processes fighting over 5599; connections landed on either at random.
   Now `--daemon` double-forks away from the terminal, and startup verifies the port is clean first.
After both fixes the 150KB page returns in 0.001s.

## Glossary
can_use_tool: the SDK's tool gate callback. Every tool use asks it for allow/deny first.
effort: how much thinking the model spends on one answer, five tiers low→max.

## Discussion
> JL: I lean toward claude_agent_sdk, we can add it. OAuth is fine for auth.
> JL: why not use the best model? claude 4.8 opus — or let us pick model and effort and so on.
>> CC0723: added both dropdowns, default opus 4.8 + high.
> JL: how do I stop this chat? any smooth way?
>> CC0723: the send key turns into ⏹ while running; clicking it raises the server-side flag and aborts browser-side.
> JL: how do you think the claude code plugin in the vscode work? we want to align it with QD2?
>> CC0724: it is the same engine underneath (local claude runtime, same credentials, same session jsonls) — so alignment is UX, not architecture. What it has that the drawer lacks: diff preview at the permission prompt, @-file mentions, plan mode, checkpoints. Adopt in that order; skip checkpoints (fights the one-session LAW). Full comparison in Where we are; new Items-to-Finish line added.
> JL: will this make it better to use the claude sdk or terminal? I want to know what is the back end of the vscode claude plugin? and I want to duplicate it.
>> CC0724: the console split changes nothing about which to use — both still run on the workstation serve.py; the console only pipes. Choose by job: drawer (SDK) for gated, comment-driven edits in the page; terminal for long tasks, skills, anything CLI-shaped. The plugin's backend is the claude binary itself over the stream-JSON protocol — which is what the drawer already drives, so "duplicating it" = the shell: diff-at-the-gate (shipped today, ①) and one persistent process per session (④, next). Anatomy written into Where we are.

## Comments
- [x] JL “open the terminal/chatbot with a prompt so they know which question and board” · 260723 1500
      >> CC0723: the drawer's system_prompt now carries `prime_context` (board/question id/title/open comments/file).
      Verified: asked with no context, it answers QB2. The terminal side uses --append-system-prompt with the same block, see QD3.
- [x] JL “I want to make the chat opened in the SPACE dir, not in the board (same to QD1/QD2)” · 260723 1430
      >> CC0723: the drawer's `cwd` moved from the board folder to the SPACE root, matching QD3 — sessions read the whole repo now.
      The restricted tier still edits only this question's files; full tiers open up. Old sessions stayed in the old folder; every question restarted under root (see QD3's Lesson).
- [x] JL “maybe we have the robot icon for the chatbox?” · 260723 1345
      >> CC0723: switched to 🤖. Also untangled a confusion: the corner used to show two 💬 (💬 Chat before the 🤖, plus 💬 Comment above),
      indistinguishable. Now 🤖 = talk to the AI, 💬 = humans writing comments.
- [x] JL “could you put it in the right bottom conner?” · 260723 1330
      >> CC0723: first misread — moved the whole drawer to the corner. JL clarified: the drawer stays a full right-side panel like haichat-inlab;
      what goes to the bottom-right is **the "💬 Chat" opener icon** (previously buried in each card's header row).
      Fixed: drawer restored to the full right side; a floating bottom-right 💬 Chat appears in focus mode and opens that question's drawer.
- [x] JL “may only edit this question's md. How, and at what cost?” · 260723 1305
      it should not be only the md — other closely related files should be editable too.
      keep it consistent with claude code cli as much as possible.
      >> CC0723: done. Permissions became three tiers, default "full·ask" = same as the CLI: all tools + all skills,
      can edit any relevant file, prompts you before touching anything else (no longer locked to one file). "Restricted" stays as the cheap option,
      "full·auto" = bypassPermissions. Verified the full tier calls skills (~150 visible).
- [x] JL “Starts a session, reads board files, answers correctly” · 260723 1240
      but one question: is this output actually streaming out? It doesn't feel like it.

## Log
260724 1510 · The wait line tells the truth now: serve.py emits stage events ("booting claude — the full tier loads the whole skill registry…" / "session up") so the drawer shows real progress instead of a static "…thinking"; the collapsed 💭 block is labeled "Thinking (N chars — click to reopen)". Also verified: RESUMED sessions stream thinking now (probe on QD6: 3 think events) — yesterday's loose end ② is gone, cured by the explicit thinking={enabled} flag
260724 1455 · Diff preview at the gate BUILT (serve.py ask events carry `detail`, drawer renders −/+ blocks; node-checked; live pop owed — the E2E's full-tier boot outran the window, turn stopped clean, board.md untouched). The extension's backend anatomized in Where we are per JL's "duplicate it"; item ④ persistent-process named as the real remaining delta
260724 1350 · Console relay verified (boards_api.py pipes /_board/chat NDJSON through 8093 — "RELAY OK" streamed); VS Code extension alignment analyzed per JL's question: same engine, adopt diff-preview → @-mentions → plan mode, skip checkpoints
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 1745 · Opening orientation: system_prompt carries prime_context (board/question/what it asks/comments/file); verified it answers QB2
260723 1730 · JL ruled: the drawer's claude also opens at the SPACE root (cwd = whole repo), matching QD3 —
              sessions read the code they discuss; the system prompt switched to repo-root-relative paths. Restricted tier still edits only this question's files
260723 1720 · JL said "shut them down": all serve.py / ttyd / terminal sockets cleaned; nothing listens on 5599 or terminal ports.
              Files and code intact, restartable anytime. ⚠️ During the sweep, found other sessions/agents concurrently editing serve.py (scope widened to the whole repo) and QA2/QA5 — before restarting the server, confirm exactly one session manages it.
260723 1710 · Added the collapsible thinking block (JL's ask): the server emits thinking_delta as `{"t":"think"}`; the drawer renders a collapsible 💭 Thinking
              (expands while thinking, folds when the answer arrives, click to reopen). Client done and pushed.
              Two known loose ends: ① seeing thinking requires a server running current code (now shut down per JL);
              ② resumed sessions do not stream thinking (QD2/QA4/QA6/QD3) — only brand-new sessions do; that is Claude Code resume behavior, not a bug.
              An isolated probe confirmed the code path (EXACT server config → thinking_delta=3).
260723 1640 · Fixed two bugs (JL-reported): ① every reply falsely claimed "changes written" + Reload — the server now sets a `wrote` flag;
              only real Edit/Write reports a write and regenerates html; read-only replies no longer trigger it.
              ② the empty-reply fallback and several prompts were still Chinese — all English now ("(no text reply…)" etc.)
260723 1620 · System language defaults to English (CHAT_RULES/FULL_RULES + drawer UI); closed the 1305 comment
260723 1615 · Restricted tier switched to disallowed_tools hard-off for Bash/Task/Skill/Web — can_use_tool is not reliably called for Bash; verified blocked
260723 1610 · Permissions became three tiers (restricted/full·ask/full·auto), default full·ask; full tier loads skills, ~150 visible
260723 1345 · Chat opener icon 💬 → 🤖, distinguished from the comment dock's 💬 (talk to AI vs. humans commenting)
260723 1340 · Correction: the drawer stays a full right panel (haichat-inlab); the "💬 Chat" opener became a floating bottom-right button,
              shown in focus mode — JL wanted the opener in the corner, not the drawer moved there
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

Chat code · where it lives and how it is wired
==============================================

The in-page chat and terminal, kept and still served (JL 261009: "don't delete it, could you save it
somewhere"). Moving it out of the server is Q01's decision, not done: the labeling workbench's terminal
hold and about twenty tests use it. This page is the map, as of Tools commit `44a69c37`.

What it was for: a drawer beside a Page or Board with a Claude chat (Agent SDK) and a terminal (a PTY in
the browser) bound to one question, with a session list per question. No live page loads the drawer
today: the shared workbench frame's right panel is Disk and Runs, and Home does not load it either.


Files
-----

```text
plugins/haipipe-toolkit/servers/
├── workbench/chat.py                    1869 lines  ChatMixin: /_board/chat, sessions, names, hold, release;
│                                                    prime_context, board_prime_context, chat_guard
├── workbench/term.py                     919 lines  TermMixin: /_board/term, PTY spawn and pump, ttyd
│                                                    fallback, labeling_tui_hold
├── workbench/assets/js/10-drawer/
│   ├── 20-chat/00-open … 50-prefs-paste.js          the chat drawer (sessions, focus, render,
│   │                                                permissions, prefs and paste)
│   └── 30-terminal.js                               the terminal pane
├── haipipe-page/assets/css/20-drawer.css            the drawer's look
└── _host/serve.py                                   mounts both: Handler(… ChatMixin, TermMixin …),
                                                     the routes below, --no-terminal, --no-hold
```

The drawer scripts are pieces of one shared script block: `10-drawer/00-open.js` opens it and
`10-drawer/50-structure.js` (space-home) closes it, and `host_assets.verify()` checks the reassembled
script on every load. Taking the chat or terminal pieces out must keep that block balanced.


Routes
------

```text
POST /_board/chat · chat-keep · stop · release        the chat itself, and handing a session back
POST /_board/sessions · session-name · session-log    a question's sessions: list, name, transcript
POST /_board/term · term-type · term-probe · local-cmd · killall · terms     the terminal
GET  /_term/<key>/ws                                   the terminal's websocket
```

A host started with `--no-terminal` (as the shared hosts here are) already answers 404 on the terminal
routes. Chat sessions are listed in `~/.claude/projects/<proj>/haipipe-sessions.json` since 261009 (no
`.haipipe-board/` folder in the SPACE).


What depends on it
------------------

1. `_host/serve.py` imports `labeling_tui_hold` from `term.py`: the labeling workbench's TUI hold.
2. Tests: `_host/tests/` (test_auth, test_workbench_short, gate_live), `_host/checks/` (chatui, guichat,
   tuichat, scopechat, switchback, termnav, pty_e2e), `servers/haipipe-page/tests/test_standalone_server.py`,
   and twelve tests in `skills/1_base/page/haipipe-page/tests/` (test_hold, test_chatlog,
   test_sentence_chat, test_labeling, test_paper_workbench, test_quality_check, …).
3. Skill docs: `skills/1_base/page/workbench-studio/ref/chat.md`, `skills/1_base/page/workbench/ref/roster.md`.


To retire it (Q01, if decided)
------------------------------

Move the two modules, the chat and terminal scripts and the drawer CSS into `j05_chat/legacy/`; keep
`labeling_tui_hold` (or move it into the labeling server); drop ChatMixin and TermMixin from `serve.py`
with their routes and flags; retire or rewrite the tests above; check `host_assets.verify()` still
passes; update the two skill refs. One commit, tested.

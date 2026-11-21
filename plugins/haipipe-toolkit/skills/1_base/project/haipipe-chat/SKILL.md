---
name: haipipe-chat
description: "Owns a Block's chat sessions: cNN_<slug>/ folders beside its Jobs (jNN) and Studio topics (sNN), one per kept session, numbered in time order, each naming the folders it changed. Use to save a session, list a Block's chats or check them. Trigger: save this chat, keep this session, chat folder, cNN, /haipipe-chat."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "0.1.0"
  last_updated: "2026-11-21"
  # version history: ./CHANGELOG.md
---

# /haipipe-chat · a Block's chat sessions, cNN

A Block holds three kinds of numbered folders side by side (`PRINCIPLE.md`):

```text
bNN_<block>/
├── board.md
├── jNN_<job>/      the work            (haipipe-job)
├── sNN-<topic>/    a topic, drawn      (haipipe-studio)
└── cNN_<slug>/     one chat session    (haipipe-chat, this skill)
    ├── cNN_<slug>.md     the face: front matter, # cNN · <title>, Ask, Summary, Changed
    └── transcript.md     optional: the raw words; a page never links it
```

A chat is worth keeping when it decided something or changed files. Its number is its place in time:
`c01` is the Block's first kept session, the next one is the next free number, and a number never
moves. The face names every folder and file the session changed (`paths:`, SPACE-relative), so the
Session view joins the chat to those folders and puts 🧵 on them.

Read `ref/chat-contract.md` before saving a chat or changing the face.


Save, list, check
-----------------

```bash
S=Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-chat/scripts
python $S/new_chat.py new <block> --slug <slug> --title '<title>' --ask '…' --summary '…' \
       --changed <file> <file> --session <name> [--cards C3.P5.s14] [--transcript <session.jsonl>]
python $S/new_chat.py list  <block>
python $S/new_chat.py check <block>
```

1. **One writer**: `new_chat.py new` is the only tool that makes a `cNN_<slug>/`; nobody types one.
2. **Paths**: list the files the session itself wrote (its Edit and Write calls), not `git diff`.
3. **Transcript**: `--transcript` renders the Claude Code session file; tool output is left out.
4. **Check**: `check` exits 1 on a missing face, date or goal, or a path not on disk.


Where a chat is not a cNN
-------------------------

- A Run's own round of work is a pass of that Run (`runs/<run>/passes/pNN-<MMDD>/`, `haipipe-run`).
- A Studio topic's working round or meeting is a pass of that topic (`haipipe-studio`).
- A Page's chat pane (the 💬 half of the 🎨 Studio tab) and its kept `studio/chat/<YYMMDD-HHMM>/` are
  `haipipe-studio/ref/chat.md`'s.

All of them, and every `cNN`, are episodes of the same Session view
(`servers/workbench/ref/three-views.md` § 4).


Boundary
--------

| Owner | Owns |
|---|---|
| `haipipe-block` | the Block and which folders it may hold |
| `haipipe-chat` | `cNN_<slug>/`: its face, its number, its writer and check |
| `haipipe-studio` | `sNN-<topic>/`, the chat pane and its Page lane |
| `haipipe-run` | a Run's passes |


Files
-----

```text
haipipe-chat/
├── SKILL.md
├── CHANGELOG.md
├── agents/openai.yaml
├── ref/chat-contract.md     the folder, the face, what a chat may and may not hold
├── scripts/new_chat.py      new · list · check
└── tests/test_new_chat.py
```

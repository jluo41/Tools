---
name: haipipe-chat
description: "Owns a Block's chat sessions: cNN_<slug>/ folders beside its Jobs (jNN) and Studio topics (sNN), one per kept session, numbered in time order, kept as QAs (question, answer, outputs). Use to save a session, list a Block's chats or check them. Trigger: save this chat, keep this session, chat folder, cNN, /haipipe-chat."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "0.3.0"
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
    └── cNN_<slug>.md     the face: front matter, # cNN · <title>, a summary, ## QA
```

A chat is kept as **QAs**, as short as possible. One QA is one turn, three lines at most:

```markdown
- **q07** 01:01 · please add all the changes and then push it to the remote.
  → 提交并推送好了：远端 `main` 现在是 `ad54ab904`。
  ⇢ `PRINCIPLE.md`, `AGENTS.md`
```

The question (with anything sent while the turn ran), `→` the answer (the reply's line 1), `⇢` the files
the turn wrote. Tool calls, tool output, reasoning and the rest of the reply are left out.

A chat is worth keeping when it decided something or changed files. Its number is its place in time:
`c01` is the Block's first kept session, the next one is the next free number, and a number never
moves. The face names every folder and file the session changed (`paths:`, SPACE-relative), so the
Session view joins the chat to those folders and puts 🧵 on them.

Read `ref/chat-contract.md` before saving a chat or changing the face.


Save, list, check
-----------------

```bash
S=Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-chat/scripts
python $S/new_chat.py new <block> --slug <slug> --title '<title>' --summary '…' \
       --from ~/.claude/projects/<slug>/<session>.jsonl --session <name> [--changed <file> …]
python $S/new_chat.py refresh <block>/cNN_<slug> --from <session.jsonl>     # the session went on
python $S/new_chat.py list  <block>
python $S/new_chat.py check <block>
```

1. **One writer**: `new_chat.py new` is the only tool that makes a `cNN_<slug>/`; nobody types one.
2. **QAs**: `--from` reads them from the session file (`scripts/qa.py`); without it, `--ask` and `--answer` give one.
3. **Outputs**: a QA's outputs are its Edit and Write calls; add files a shell command wrote with `--changed`.
4. **When**: once, when an answer ends: the `Stop` hook `scripts/chat_hook.py` refreshes a chat saved with
   `--from`, never mid-turn. Register it once in `~/.claude/settings.json`:
   `"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "<a python with PyYAML> <this skill>/scripts/chat_hook.py"}]}]}`.
5. **Check**: `check` exits 1 on a missing face, date or goal, or a path not on disk.


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
├── scripts/new_chat.py      new · refresh · list · check
├── scripts/qa.py            a session file read as QAs
├── scripts/chat_hook.py     the Stop hook: refresh a kept chat when an answer ends
└── tests/test_new_chat.py
```

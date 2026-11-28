# The chat contract · cNN_<slug>/

## Where it sits

```text
<Project>/<theme folder>/bNN_<block>/
├── jNN_<job>/        Jobs
├── sNN-<topic>/      Studio topics
└── cNN_<slug>/       chat sessions, numbered in time order
```

Only a Block holds `cNN` folders. A session that worked inside one Job or Task still lands at its
Block; its `paths:` say where it acted. The folder name is `c`, two or more digits, `_`, then a slug of
lower-case words joined by `_` (`c03_add_chat_skill`).

## The face: cNN_<slug>.md

```markdown
---
session: <the session's saved name>     # who did it; kept in the record, never a page label
provider: claude | codex
date: 2026-11-21
goal: Add the hai-chat skill        # one line; the row's title on the Session view
paths:                                  # SPACE-relative, every file or folder it wrote
  - Tools/PRINCIPLE.md
cards:                                  # card addresses it changed, below a file
  - t02.C3.P5.s14
---

# c03 · Add the hai-chat skill

A Block's chats are cNN folders, kept as QAs.

## QA

- **q01** 01:02 · we might have a skill named hai-chat, right?
  → Yes, a Block's cNN folders should have their own owner.
- **q02** 01:04 · yes, please go ahead and do it.
  → hai-chat is built and works.
  ⇢ `SKILL.md`, `new_chat.py`
```

## The QA: the basic element

A chat is a list of QAs, and a QA is all that is kept of a turn:

| Part | What | From the session file |
| --- | --- | --- |
| question | the person's words on one line, cut at 200 characters | their message, plus any message sent while the turn ran |
| answer | one line, cut at 160 | the first line of the turn's last reply |
| outputs | the file names; full paths are `paths:` | its Edit, Write and NotebookEdit calls |

Left out: tool calls and their output, reasoning, injected context, the rest of the reply. The reply's
detail lives in the files it wrote; the QA points at them. A QA's address is `cNN.qNN` (`c03.q02`), so a
page can mark the element a QA changed. A file a shell command wrote is not seen by the reader; the saver
adds it with `--changed`.

These are the same fields as a pass's front matter (`servers/workbench/ref/three-views.md` § 4.2), so
the Session view reads both the same way.

## Rules

1. **Kept, not logged.** A session is saved when it decided something or changed files; most sessions
   never become a `cNN`.
2. **Time order.** The next free number; a number never moves and is never reused.
3. **Paths at the time.** `paths:` is written when the chat is saved, from the files the session itself
   wrote. `refresh` rewrites the QAs when the session went on; the number, title, date and summary stay.
   It runs once when an answer ends (the Stop hook, `scripts/chat_hook.py`), never mid-turn, and only for
   a session saved with `--from` (its id is in `~/.claude/hai-chat/kept.json`).
4. **No transcript.** Only the QAs are kept; the session file stays where Claude Code keeps it.
5. **No work output.** A drawing belongs in an `sNN`, a result in a Run's `result/`. A `cNN` holds the
   conversation and points at what it made.
6. **Signed and frozen files are never written** by the saver (three-views § 5).

## Where it shows

- **Session view**: each `cNN` is one episode, grouped under its Block, newest first; the row opens the face.
- **Folder view**: 🧵 on every folder and file its `paths:` name, and on the folders above them.
- **Job and Task pages**: the Sessions part, filtered to the chats that touched that Job or Task.

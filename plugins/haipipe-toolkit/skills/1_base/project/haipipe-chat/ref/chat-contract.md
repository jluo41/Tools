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
goal: Add the haipipe-chat skill        # one line; the row's title on the Session view
paths:                                  # SPACE-relative, every file or folder it wrote
  - Tools/PRINCIPLE.md
cards:                                  # card addresses it changed, below a file
  - t02.C3.P5.s14
---

# c03 · Add the haipipe-chat skill

## Ask
What the person asked, in their words or close to them.

## Summary
What happened and what was decided.

## Changed
- `Tools/PRINCIPLE.md`
```

These are the same fields as a pass's front matter (`servers/workbench/ref/three-views.md` § 4.2), so
the Session view reads both the same way.

## Rules

1. **Kept, not logged.** A session is saved when it decided something or changed files; most sessions
   never become a `cNN`.
2. **Time order.** The next free number; a number never moves and is never reused.
3. **Paths at the time.** `paths:` is written when the chat is saved, from the files the session itself
   wrote; it cannot be recovered later.
4. **No transcript on a page.** `transcript.md` is for reference. The Session view links the face only,
   since a transcript may hold printed rows a page must never show.
5. **No work output.** A drawing belongs in an `sNN`, a result in a Run's `result/`. A `cNN` holds the
   conversation and points at what it made.
6. **Signed and frozen files are never written** by the saver (three-views § 5).

## Where it shows

- **Session view**: each `cNN` is one episode, grouped under its Block, newest first; the row opens the face.
- **Folder view**: 🧵 on every folder and file its `paths:` name, and on the folders above them.
- **Job and Task pages**: the Sessions part, filtered to the chats that touched that Job or Task.

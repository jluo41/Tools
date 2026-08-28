---
name: haipipe-plugin-chat
description: >-
  The chat/ plugin of a Board page: one 💬 Chat tab, with
  <page>/chat/<YYMMDD-HHMM>/ as the home for sessions worth keeping. Trigger:
  chat plugin, chat tab, keep this session, kept conversation, chat record,
  /haipipe-plugin-chat.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-15"
---
# /haipipe-plugin-chat · one Chat, its record in the folder, its form chosen inside

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only chat's delta: one tab over two forms, and the shape a kept session takes.

## 🗂 Storage · a kept session, not a live one

```text
<page>/chat/
└── <YYMMDD-HHMM>/       one KEPT session
    ├── digest.md        what it decided · the reading path
    └── transcript.md    the raw exchange · reference only
```

PRIMARY material: a person chose to keep it, so it is committed and never regenerated.
The live session is not this plugin: it runs through the server, pointed at by the page's `session:` line, and most sessions are noise that never lands here.
The grammar is the meeting record's (digest is the path, raw is reference, decisions route onward as sentences), because a kept chat is typed testimony the way a meeting note is spoken testimony.

## 📡 Surface · ONE tab, the form inside it

One 💬 Chat tab (JL 260815: "just have one Chat in the plugin, not more ChatGUI or Chat TUI").
The GUI/TUI choice is a FORM segment inside the tab, subordinate to it, never a second tab: the strip stopped selling the form.
GUI is the SDK chat box (`live/chat.py`); TUI is the real CLI in the terminal (`live/term.py`); one question, one session, one window.

## ⚠️ Writer · the one OPEN row, kept open on purpose

What writes a kept session into `chat/` — the closing "keep this" step, its trigger, and who owns the digest — is **unruled**, and `QPf4`'s Decision row owns it.
Until it lands, this plugin's folders are written by hand or not at all, and this file records the boundary instead of inventing the rule.
The roster marks the row 🟡 for exactly this reason.

## 📂 Files

- `../../haipipe-board/live/chat.py`
  The GUI form: sessions, the SDK turn, the drawer.
- `../../haipipe-board/live/term.py`
  The TUI form: the PTY, parking, reattachment.
- `../../haipipe-plugin/ref/roster.md`
  The row this skill expands, 🟡 until QPf4 rules the landing.

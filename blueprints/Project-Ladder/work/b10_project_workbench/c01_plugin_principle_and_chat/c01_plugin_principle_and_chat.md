---
session: Tools-PRINCIPLE-cNN
provider: claude
date: '2026-11-21'
goal: PRINCIPLE.md and the cNN chat folder
paths:
- ../../../../PRINCIPLE.md
- ../../../../AGENTS.md
- ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-chat
- ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-block/ref/board-contract.md
- ../../../../plugins/haipipe-toolkit/servers/workbench/page/frame_sessions.py
- ../../../../plugins/haipipe-toolkit/servers/workbench/ref/three-views.md
cards: []
---

# c01 · PRINCIPLE.md and the cNN chat folder

## Ask

A principle for how a plugin is designed: File System (skill, Block, chat folders), UI System, and the map. Chat sits under the Block as cNN beside jNN and sNN, owned by a haipipe-chat skill.

## Summary

PRINCIPLE.md says a plugin is a File System, a UI System and the map between them, and a Block holds jNN, sNN and cNN. haipipe-chat owns cNN_<slug>/ with new_chat.py as its one writer; the Session view reads cNN; the ladder, audit, Job and report checkers accept it.

## Changed

- `../../../../PRINCIPLE.md`
- `../../../../AGENTS.md`
- `../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-chat`
- `../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-block/ref/board-contract.md`
- `../../../../plugins/haipipe-toolkit/servers/workbench/page/frame_sessions.py`
- `../../../../plugins/haipipe-toolkit/servers/workbench/ref/three-views.md`

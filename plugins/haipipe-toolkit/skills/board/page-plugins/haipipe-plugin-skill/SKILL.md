---
name: haipipe-plugin-skill
description: >-
  The skill/ plugin of a Board page: the page's skill LIST at <page>/skill/<stem>.md (PRIMARY) — one `- <name>` row per related skill OR AGENT, where the ORDER of the rows IS the person's rank (top = most related) — worked through a derived 🛠 index of cards the person drags to rank. Owns the three-route contract (scan-seed, drag-order, entry) and its one law: the scan seeds names at the bottom and the person ranks them; a `removed` row is the person's ✕ and is never re-seeded. Loads haipipe-plugin for the four-facet contract and never restates it. Trigger: skill plugin, skill list, skill map, page dependencies, which skills does this page depend on, which agents does this page dispatch, drag to rank, add a skill, add an agent, remove a skill, skill tab, /haipipe-plugin-skill.
metadata:
  version: "0.2.1"
  last_updated: "2026-08-16"
  summary: "Agents joined the list (JL 260816): an agents/<name>-agent.md is a first-class 🤖 row, same rank, same ✕; its open door is the live markdown view."
---
# /haipipe-plugin-skill · which skills stand behind this page

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only skill's delta: the list's row grammar, the seed's modesty, and whose gesture the rank is.

## 🗂 Storage · MIXED, one ranked list worked through an index

```text
<page>/skill/
├── <stem>.md            PRIMARY · the list: one row per skill or
│                        agent, ORDER = rank
└── <stem>-skill.html    DERIVED · the 🛠 index of cards, regenerated
```

The row grammar is one line: `- <name>` with an optional ` · note: free text`, where the name is a skill (a folder with a SKILL.md) or an AGENT (an `agents/<name>-agent.md` definition, JL 260816: a page's working relations include the agents it dispatches).
An agent card wears 🤖 and the meta word `agent`, and opens through the live markdown view, because no SKILL.md folder stands behind it.
The order of the rows is the person's rank: top = most related, and nothing else in the file encodes a judgment.
A row ending ` · removed` is the person's ✕: it stays in the store as a tombstone so a refresh can never re-seed the name, and ↩ restores it.

## ⚖️ The one law · the scan seeds, the person ranks

The scan-seed never invents: it lists only names the page's text actually writes, matched against real SKILL.md folders and agent definitions, and a page that names none seeds empty.
A scanned name lands at the BOTTOM of the list, because everything above it is the person's order; a refresh never edits, reorders, or removes a row.
The earlier vocabulary — uses/designs relations, the aligned ✓, drift dates — was removed on JL's ruling (260816: "we just need to show these skills and the user can drag and rank them themselves"); the drag is the one judgment, and it is always a person's.

## ⚙️ Writer · three routes, the bibex shape

```text
POST /_board/skill          scan-seed: append newly scanned names at the
                            bottom · rebuild the index view
POST /_board/skill-order    the drag: the store keeps exactly the sent order
POST /_board/skill-entry    the pen: add a name (typo-guarded, lands at the
                            TOP) · ✕ remove (tombstone) · ↩ restore · note
```

## 📡 Surface · the index and the reader

The 🛠 tab opens on the index: one card per skill with a ⠿ drag handle, the skill's version, last_updated, and description, `open the skill`, and ✕.
Clicking a card's name shows that skill in the SAME frame (`/_board/skillview`), whose bar walks the page's skills in the ranked order with ← and → plus ☰ back to the index; an agent card opens its definition through `/_board/mdview`, outside the walk.
Removed names sit in a quiet fold with ↩ restore; ＋ adds a name by hand, which lands at the top because adding by hand says "this matters".

## 📂 Files

- `../../haipipe-board/live/skillmap.py`
  The three routes, the store writer, the index view, and the skill reader.
- `../../haipipe-plugin/ref/roster.md`
  The row this skill expands.

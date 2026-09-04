---
name: haipipe-plugin-skill
description: >-
  The ranked Skills record of a Board Page, stored at the Page's
  outline/skill/STEM.md path and displayed inside Outline → Page Records → Skills.
  One row names one related skill or agent; row order is the person's rank. A
  scan seeds names and the person ranks them. It is not a standalone top-level
  plugin. Trigger: page records skills, skill list, which skills does this page
  depend on, drag to rank, add a skill, /haipipe-plugin-skill.
metadata:
  version: "0.4.2"
  last_updated: "2026-09-03"
---
# /haipipe-plugin-skill · the ranked Skills Page Record

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only skill's delta: the list's row grammar, the seed's modesty, and whose gesture the rank is.

## 🗂 Storage · MIXED, one ranked list worked through an index

```text
<page>/outline/skill/
├── <stem>.md            PRIMARY · the list: one row per skill or
│                        agent, ORDER = rank
└── <stem>-skill.html    DERIVED · the 🛠 index of cards, regenerated
```

The row grammar is one line: `- <name>` with an optional ` · note: free text`, where the name is a skill (a folder with a SKILL.md) or an AGENT (an `agents/<name>-agent.md` definition, JL 260816: a page's working relations include the agents it dispatches).
An agent card wears 🤖 and the meta word `agent`, and opens through the live markdown view, because no SKILL.md folder stands behind it.
Once a person ranks the rows, their order is the person's rank: top = most
related, and nothing else in the file encodes a judgment. A freshly scanned
sequence is only a rankable seed; the surface must not present that mechanical
order as a completed human judgment.
A row ending ` · removed` is the person's ✕: it stays in the store as a tombstone so a refresh can never re-seed the name, and ↩ restores it.

## ⚖️ The one law · the scan seeds, the person ranks

The scan-seed never invents: it lists only names the page's text actually writes, matched against real SKILL.md folders and agent definitions across every installed `Tools/plugins/*/skills` tree, and a page that names none seeds empty.
A plugin-level `agents/` directory participates in the same index, so a Board hosted by `haipipe-toolkit` can cite the skills and agents of a sibling plugin such as `subjective-label`; the hosting plugin is not an index boundary.
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

## 📡 Surface · Page Records → Skills

The Outline plugin embeds the generated index at **Page Records → Skills**:
one card per skill with a ⠿ drag handle, the skill's version, last_updated, and
description, `open the skill`, and ✕. The primary store remains
`outline/skill/<stem>.md`; Outline reads it in place and never copies it. A
pre-migration sibling `skill/<stem>.md` is a read-only compatibility input;
the next write lands canonically under `outline/skill/`. The compatibility
routes remain active, but the Plugin picker has no standalone 🛠 Skill row. Its
header says `drag to rank · refresh appends`; it does not infer that a seed has
already been human-ranked or manufacture a rank-movement date.
Clicking a card's name shows that skill in the SAME frame (`/_board/skillview`), whose bar walks the page's skills in the ranked order with ← and → plus ☰ back to the index; an agent card opens its definition through `/_board/mdview`, outside the walk.
Removed names sit in a quiet fold with ↩ restore; ＋ adds a name by hand, which lands at the top because adding by hand says "this matters".

## 📂 Files

- `../../haipipe-board/live/skillmap.py`
  The three routes, the store writer, the index view, and the skill reader.
- `../../haipipe-plugin/ref/roster.md`
  The row this skill expands.

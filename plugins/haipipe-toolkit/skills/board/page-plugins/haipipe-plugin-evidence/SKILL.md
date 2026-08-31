---
name: haipipe-plugin-evidence
description: >-
  The ONE presentation plugin for a page's evidence: a single 🧾 Evidence tab
  that shows the bibex, probe, value, display and pagex lanes together,
  joined per plan bullet. Presentation only — the storage folders, their writers,
  their walls and their human gates stay with their own contracts. Trigger:
  evidence plugin, evidence tab, show the evidence, citations cards values
  displays together, evidence bundle tab, /haipipe-plugin-evidence.
metadata:
  version: "0.2.0"
  last_updated: "2026-08-31"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-evidence · one tab presents what five lanes hold

**LOAD `haipipe-plugin` FIRST.** This plugin owns no storage and no writer:
it is the SURFACE over five lanes that keep their own contracts (JL 260831:
"we still have the subfolder for bibex, etc, but we just need one evidence
plugin, to present bibex, display, etc"). The precedent is Probe, "a logical
family over two rows", and value, "a surface with no folder" — this file
takes the same shape one level up.

```text
this file     the 🧾 Evidence tab: segments, the per-bullet join, the counts
the lanes     bibex/ (haipipe-plugin-bibex) · probe/ + pagex/ (haipipe-plugin-probe)
              · ## Values blocks (haipipe-plugin-value) · display/
              (haipipe-plugin-display) — storage, writers, walls, gates UNCHANGED
the phase     ③ EVIDENCE (haipipe-page-evidence) lands what this tab shows
the fields    the page type's evidence: record names what is OWED
              (haipipe-page/ref/type-registry.md)
```

## 🗂 Since the v3 folder, the tab has a disk twin

JL 260831 ("the evidence should include the display, the bibex, the pagex"):
the lanes this tab presents now LIVE under `<page>/evidence/` (bibex · probe ·
display · pagex · code · materials), one category folder a stranger opens for
"what backs this page". Flat lane names are migration stubs for the unpatched
engine paths. The tab is the category folder's surface; nothing else changed.

## 📡 Surface · one tab, six segments, one join

One 🧾 Evidence tab on the page, replacing the separate 📚, 🚪 and 🖼 tabs in
the strip (each remains reachable as a SEGMENT inside it, the way GUI and TUI
are form segments inside one 💬 Chat tab). It ranks after 🧭 Outline and
💬 Chat.

```text
🧾 Evidence
├── ⧉ By bullet      the JOIN, first and default: one row per owing plan
│                    bullet — its marks, then what each mark has on disk
│                    (key state · card state · value rows · unit state)
├── 📚 Citations     the bibex workbench, as haipipe-plugin-bibex §surface
├── 🚪 Cards         the probe card list, as haipipe-plugin-probe §surface
├── 🧮 Values        every PP<NN>.v<n> row with its source path
├── 🖼 Displays      the unit strip, as haipipe-plugin-display §surface
└── 🔗 Pagex         the borrow view, as haipipe-plugin-pagex §surface — its
                     pens ride inside the saved view, so the standalone 🔗
                     strip row folded in here (260831); the task lane's read
                     arrives here when a pagex card learns a task unit's status
```

- **By bullet is the default** because the reader's question is "what does
  this page still owe", not "what does this folder hold"; the segment order
  is the mark order 📚 📮 🧮 🖼.
- **Counts stay separate**: the tab header prints `owed n · landed n ·
  accepted n` computed as `cli/evidence-status.py` computes them, never
  collapsed into one number.
- **Both failure modes render as named rows**: 🕳 owed-and-absent · 🎈
  present-and-uncited (the outline tab's law, kept identical here).
- **The tab writes nothing and calls no model.** Every pen stays with its
  lane: the bibex entry pen, the probe crossing, the display `accepted:` row,
  the value allocation at ③ EVIDENCE.

## 🔒 What merging the surface must never merge

```text
lane        writer                       human gate      the wall
────────────────────────────────────────────────────────────────────────────
bibex/      person-supplied, transcribed  verified:       never composed from memory
probe/      ② raises · ③ binds            read:           stake behind consumer/
values      ③ allocates PP<NN>.v<n>       (rides read:)   aggregate only, never rows
display/    the display family renders    accepted:       intake frozen before render
```

A surface that offered one "approve all" control would collapse three gates
into one tick; this tab shows each gate beside its own thing and offers none.

## 🗺 Status · 🟢 built 260831, driven in a real browser

`live/evidence.py` serves GET `/_board/evidence` (the segmented surface) and
its POST twin; `84-plugin-evidence.js` registers the ONE row; the 📚 BibEx,
🧮 Values, 🖼 Display and 🚪 Probe strip rows are folded (their builder routes
stay, pressed by the segments on demand); 260831 evening the 🔗 Pagex strip
row folded in too (85-plugin-pagex.js removed, the saved view's inline pens
ride along). Verified end to end on SM05-results:
menu entry → tab → segments → the Values segment loading the live view.

## 📂 Files

- `../haipipe-plugin-bibex/SKILL.md` · `../haipipe-plugin-probe/SKILL.md` ·
  `../haipipe-plugin-value/SKILL.md` · `../haipipe-plugin-display/SKILL.md` ·
  `../haipipe-plugin-pagex/SKILL.md` · the lane contracts this surface presents
- `../haipipe-plugin-outline/ref/evidence-bundle.md` · the per-bullet join
  and its six status words, reused verbatim by ⧉ By bullet
- `../../haipipe-board/cli/evidence-status.py` · the counts and the
  `<stem>-evidence.md` snapshot
- `../../haipipe-board/live/evidence.py` · the segmented surface and its twin
- `../../haipipe-board/assets/js/10-drawer/84-plugin-evidence.js` · the one registry row
- `../../page-workflows/haipipe-page-evidence/SKILL.md` · phase ③, which
  lands what this tab shows

---
name: haipipe-plugin-bibex
description: >-
  The bibex/ plugin of a Board page: the page's own bib at
  <page>/bibex/<stem>.bib, worked through a citation workbench with status
  chips, DOI links, and a human ✓ verified tick. Law: bibtex is never
  generated, only subset or landed verbatim. Trigger: bibex plugin, page bib,
  citation workbench, verify a citation, add a bib entry,
  /haipipe-plugin-bibex.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-15"
---
# /haipipe-plugin-bibex · the page's own bib, never composed by a machine

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only bibex's delta: a MIXED plugin, one primary file worked through three routes under one law.

## 🗂 Storage · MIXED, and the split is the contract

```text
<page>/bibex/
├── <stem>.bib           PRIMARY · the page's own bib (JL 260815)
└── <stem>-bib.html      DERIVED · the workbench, regenerated
```

The `.bib` is a person's material: committed, never overwritten by a refresh, growing only through the two human doors below.
The workbench html is a projection of it and regenerates freely.

## ⚖️ The one law · subset and transcribe, never compose

citation-craft forbids generating bibtex: a machine may SUBSET a `.bib` a person already wrote, and it may land a person-supplied entry VERBATIM, and that is the whole list.
A composed reference is a hallucination wearing a key, and one of those costs more than the workbench saves.

## ⚙️ Writer · three routes, each one verb wide

```text
POST /_board/bibex          refresh: seed-import keys this page cites
                            from the paper's own 0-*.bib · reads it,
                            NEVER writes it · rebuilds the workbench
POST /_board/bibex-verify   the human ✓: lands as a `verified` field
                            on the entry · a tick is a person's word
POST /_board/bibex-entry    the pen: a person-supplied entry lands
                            verbatim, typo-guarded, never composed
```

Outside any paper the page's bib simply starts empty; the refresh has nothing to seed from and says so rather than inventing.

## 📡 Surface · the workbench

The 📚 tab renders one row per entry: status chip, Scholar/DOI/URL links for checking, ✓ to verify, ✎ to edit, ＋ to add.
The ✓ ticks are all a person's: a seeded entry arrives unverified, and stays so until an eye has been on it.

## 📂 Files

- `../../haipipe-board/live/export.py`
  The three routes and the workbench builder.
- `../../../paper/haipipe-paper/` (citation-craft)
  The law this plugin obeys and did not write.
- `../../haipipe-plugin/ref/roster.md`
  The row this skill expands.

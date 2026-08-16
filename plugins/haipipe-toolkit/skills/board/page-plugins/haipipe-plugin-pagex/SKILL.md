---
name: haipipe-plugin-pagex
description: >-
  The pagex/ plugin of a Board page: the page's borrow LIST at <page>/pagex/<stem>.md (PRIMARY) — one row per FILE taken from another page anywhere in the repo, where the ORDER of the rows IS the person's rank — materialized as relative symlinks so the borrowed material is read live and never copied. Owns the three-route contract (seed-and-re-mint, drag-order, pen), the vet a target must pass, and its two laws: pagex links files and never a page's home folder, and the scan seeds while the person ranks. Loads haipipe-plugin for the four-facet contract and never restates it. Trigger: pagex plugin, seed borrows from the prose, borrow a file from another page, reference other pages, reuse a component from another page, symlink plugin, page citations into pages, dangling borrow, pagex tab, /haipipe-plugin-pagex.
metadata:
  version: "0.2.1"
  last_updated: "2026-08-16"
  summary: "A borrow opens as the rendered BOARD PAGE, not raw markdown (JL 260816), and the repo path moved off stage into a `where` fold."
---
# /haipipe-plugin-pagex · which files this page borrows from other pages

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only pagex's delta: the borrow row, the minted link, the vet, and how a borrow is seeded.

The family is three now: bibex holds a page's references into the literature, skill into the skill tree, and pagex into the repo's own page tree.
The design page is `QPf11` on the board skill's board.

## 🗂 Storage · MIXED, one ranked list and the links minted from it

```text
<page>/pagex/
├── <stem>.md                    PRIMARY · the borrow list, ORDER = rank
├── <src-page>/<inner path>      DERIVED · relative symlinks, re-minted
└── <stem>-view.html             DERIVED · the 🔗 card view
```

The row grammar is one line: `- <repo-relative path>` with an optional ` · note: free text`, and a row ending ` · removed` is the person's ✕ tombstone with ↩ to restore.
A minted link keeps the SOURCE page's inner path, so `QPs1-overall/skill/QPs1-overall.md` rather than a flat basename: a page's own md and its skill list often share a stem, and the inner path both prevents that collision and says which layer was borrowed.

## ⚖️ The two laws

**Files only, never a page's home folder.**
Discovery already ignores a plugin folder's contents, so a symlinked `Q*.md` cannot surface as a ghost page.
A DIRECTORY link named like a page would satisfy the folded-page test and discovery would walk into it, so the pen and the minter both refuse a folder outright.

**The scan seeds, the person ranks** — `haipipe-plugin-skill`'s law, adopted whole (JL 260816: "it should not be manually added").
A page already declares what it leans on, in its Opening's "Covered elsewhere" line and in every sentence citing an id, so a refresh borrows those pages instead of asking someone to name them again.
A seeded row lands at the BOTTOM, because everything above it is the person's rank; a refresh never edits, reorders, or removes a row, and a ` · removed` tombstone is never re-seeded.

## 🌱 Seeding · what one refresh does

```text
the page's prose ──▶ the page ids it writes, counted
                     QPs1 16× · QPf10 9× · QPf1 7× · QPf3 4×
                     ▼
the store        ──▶ each named page's OWN md, appended at the bottom,
                     noted `scan-seeded — this page names <id> N×`
                     ▼
the links        ──▶ re-minted, and every card shows its source page's
                     live `state:` — ✅ lends a ruling, 🟡 lends an argument
```

A seed stops at the named page's `.md`, because the prose named a PAGE and not a file inside it.
The ＋-by-path pen, folded shut under the cards, is how a deeper file or another board's file is reached.

## ⚙️ Writer · three routes

```text
POST /_board/pagex          seed from the prose · re-mint every live row's
                            symlink · rebuild the view
POST /_board/pagex-order    the drag: the store keeps exactly the sent order
POST /_board/pagex-entry    the pen: `borrow` a file (note optional, lands at
                            the TOP) · ✕ remove (tombstone) · ↩ restore
```

The pen's field is `borrow`, not `path`: every view merges the board context `{path, file}` into its POST body, so a borrowed file sent as `path` is overwritten by the board's own path.

**The minter's one safety rule**: it only ever unlinks a SYMLINK inside `pagex/`.
A real file that lands there is never touched, so a re-mint can be run at any moment without eating anything it did not make.
A target that resolves outside the repo root, is a folder, or already has a real file in its slot is refused with the reason shown on its card.

## 📡 Surface · the 🔗 tab

One card per borrow, in the person's order. On stage: the SOURCE PAGE's name as the title, its live `state:`, which file was borrowed, the note, ⠿ and ✕. Folded under `where`: the repo-relative path and a link to the raw file.

**The title opens the BOARD PAGE, not the file** (JL 260816: "when I open them, why not the page in the board, but the raw markdown????").
A borrow is taken to be read, and reading happens on the rendered page with its prose, comments, and rail; a served `.md` is raw text. A borrowed page md resolves to `board/<group>/<stem>.html` by walking up for board.md, and anything that is not a page keeps the served file as its door.
A borrow whose source has moved shows ⚠ dangling with what it pointed at, which is the whole reason this is a link and not a copy.
Under the cards sits one folded ＋, the by-path pen; nothing on stage asks a person to choose before the scan has run.

The 📂 folder tab marks a symlink row with a bare 🔗, full target on hover, because it reports the RESOLVED file and a borrowed page md would otherwise read as duplicated bytes (JL 260816: "are they copied or are they the symlink?").
The mark stays bare: pagex mints links whose place mirrors the source, so spelling the target out repeats the row's own name and was the first fix's own defect.

## 📂 Files

- `../../haipipe-board/live/pagex.py`
  The three routes, the store writer, the minter and its vet, the prose scan behind the seeder, and the card view.
- `../../haipipe-board/assets/js/10-drawer/85-plugin-pagex.js`
  The registry entry whose `tab` spec the shell builds the 🔗 tab from.
- `../../haipipe-plugin/ref/roster.md`
  The row this skill expands.

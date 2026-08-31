---
name: haipipe-plugin-pagex
description: >-
  The pagex/ plugin of a Board page: the page-local borrow list, one row per
  file taken from another Page anywhere in the repo, row order expressing the
  person's rank, made live by relative symlinks. Links files, never Page home
  folders. Trigger: pagex plugin, borrow a file from another page, reference
  other pages, symlink plugin, /haipipe-plugin-pagex.
metadata:
  version: "0.6.2"
  last_updated: "2026-08-31"
---
# /haipipe-plugin-pagex · which files this page borrows from other pages

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only pagex's delta: the borrow row, the minted link, the vet, and how a borrow is seeded.

The family is three now: bibex holds a page's references into the literature, skill into the skill tree, and pagex into the repo's own page tree.
The design page is `QPf11` on the board skill's board.

> 🧾 Since 260831 this view is the 🔗 Pagex SEGMENT inside the one 🧾 Evidence tab (`haipipe-plugin-evidence`); the standalone strip row folded away, and every pen below rides inside the saved view unchanged.

## 🔎 Probe family · the existing-Page lane

PageX is the cross-page lookup surface used while OUTLINE decides which already
accepted Page evidence the consumer will rely on. It is the `source: page` lane
inside the Probe family. It is not a bank and it does not dispatch:

```text
Probe source router
  ├─ page             ── PageX ───── exact file/scope binding in OUTLINE
  └─ task/discovery   ── QA Probe ── QA-bank crossing in PROBE/EVIDENCE
```

The PageX selection is valid only when the borrowed file and scope literally
support the outline obligation or name the exact accepted Display being reused.
A Page that merely shares a topic is a candidate, not evidence. The OUTLINE
records the selected source path/scope; the ranked borrow list remains the
person's durable choice.

The board exposes `POST /_board/pagex-match` as a read-only candidate
shortlist. It reports transparent token overlap and a short excerpt, but its
result is deliberately `inspect exact source before use`: the endpoint never
binds evidence, edits the borrow list, or claims that similarity is evidence.

When a source Page already owns an accepted probe answer, PageX borrows the
exact accepted Page material and keeps that Page as the durable authority; it
does not open a new local Probe card merely to mirror the source. When a Display
is reused, cite its fully qualified unit id or borrow its specific file; never
link an entire page home folder.

## 🗂 Storage · MIXED, one ranked list and the links minted from it

```text
<page>/evidence/pagex/
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
POST /_board/pagex-entry    the pen: `borrow` one path OR a list (note
                            optional, lands at the TOP) · ✕ remove
                            (tombstone) · ↩ restore
POST /_board/pagex-match    OUTLINE's read-only candidate shortlist; no write
GET  /_board/pagexview      one borrow, framed under ← ☰ → over the list
```

`borrow` takes a list so one gesture can move a batch: a card's ✕ drops every row of that source page, and a folder's ＋ use takes every file in it.

The pen's field is `borrow`, not `path`: every view merges the board context `{path, file}` into its POST body, so a borrowed file sent as `path` is overwritten by the board's own path.

**The minter's one safety rule**: it only ever unlinks a SYMLINK inside `pagex/`.
A real file that lands there is never touched, so a re-mint can be run at any moment without eating anything it did not make.
A target that resolves outside the repo root, is a folder, or already has a real file in its slot is refused with the reason shown on its card.

## 📡 Surface · the 🔗 tab

ONE CARD PER SOURCE PAGE, in the person's rank, not one per borrowed file (JL 260816: "每一个 page folder 我们用了它的哪些 information … 这个 sub-folder 用了，那个 sub-folder 没有用").
On stage: the page's name as the title, its live `state:`, then its WHOLE folder as an inventory — `using N of M`, ✅ on each part in use, ⬜ on each part not, every ⬜ carrying ＋ use, which takes that folder's files in one click. Under it, the files actually borrowed, each with its own ✕; the card's ✕ drops the page entirely.
A borrow list alone cannot tell a deliberate one-file borrow from a page nobody opened, which is the question the inventory answers.

**The title opens the BOARD PAGE, framed with a way back** (JL 260816: "why not the page in the board, but the raw markdown????" and "我点进去之后，怎么退回来呢？").
A borrow is taken to be read, and reading happens on the rendered page with its prose, comments, and rail; a served `.md` is raw text. A borrowed page md resolves to `board/<group>/<stem>.html` by walking up for board.md, and `GET /_board/pagexview` frames it under ← ☰ →: ☰ returns to the cards, the arrows walk the borrows in ranked order, and `open on its own` escapes the frame. The page is served untouched inside it, never rewritten.
A borrow whose source has moved shows ⚠ dangling with what it pointed at, which is the whole reason this is a link and not a copy.
Under the cards sits one folded ＋, the by-path pen; nothing on stage asks a person to choose before the scan has run.

The 📂 folder tab marks a symlink row with a bare 🔗, full target on hover, because it reports the RESOLVED file and a borrowed page md would otherwise read as duplicated bytes (JL 260816: "are they copied or are they the symlink?").
The mark stays bare: pagex mints links whose place mirrors the source, so spelling the target out repeats the row's own name and was the first fix's own defect.


> Since 260831 this lane lives under the page's category folder (`evidence/` or `delivery/`, haipipe-page 0.47.0 §📁); a flat lane name on an unmigrated page, or a flat SYMLINK STUB on a migrated one, is the same lane during the migration.

## 📂 Files

- `../../haipipe-board/live/pagex.py`
  The three routes, the store writer, the minter and its vet, the prose scan behind the seeder, and the card view.
- `../../haipipe-board/assets/js/10-drawer/85-plugin-pagex.js`
  The registry entry whose `tab` spec the shell builds the 🔗 tab from.
- `../../haipipe-plugin/ref/roster.md`
  The row this skill expands.

# PageX lane · how one Folder points into another Folder

Read this reference from `haipipe-plugin-outline` when SURVEY considers an
accepted cross-Folder source or the 🧭 Outline plugin's Evidence Workspace presents that relationship.
PageX is an internal Evidence lane and source-binding mechanism—not a Plugin,
Run family, action, or typed Result. This reference owns its link scope, ranked
row, minted link, safety vet, live Folder-face read, and prose seeding.

The Evidence Citations lane points into literature, Skill points into the
skill tree, and PageX
points into the repo's Folder graph. There is no separate Task plugin:
execution belongs to a Folder's Task Face; a cross-Folder task relationship is
still a PageX link.
The design page is `QPf11` on the board skill's board.

> 🧾 This view is the 🔗 PageX segment inside the 🧭 Outline plugin's Evidence Workspace
> (`haipipe-plugin-outline`). There is no standalone PageX Plugin or Result.

## 🔎 SURVEY binding · select an exact authority, not a topic

For evidence reuse, PageX is the cross-Page lookup surface used while SURVEY
decides which already accepted material a typed Evidence Item will rely on. It
is not a bank and it does not dispatch:

```text
SURVEY · one Evidence Item
  ├─ Supporting Runs   0..N Execution/Discovery plans
  ├─ PageX Bindings    0..N exact accepted cross-Folder sources
  ├─ Local Input       exactly one future frozen envelope
  └─ Local Run         exactly one Page · Evidence Item plan
```

The PageX selection is valid only when the borrowed exact file or Result and
its named authority literally support the Evidence Item's obligation. A Page
that merely shares a topic is a candidate, not evidence. SURVEY records the
selected exact path and authority in the item's `PageX Bindings`; the ranked
borrow list remains the person's durable navigation choice.

An Evidence Item binding uses:

```text
<repo-relative exact file-or-Result path> · authority <Run id, accepted artifact id, or accepted Page version>
```

`PageX Bindings: []` means the item uses no cross-Folder Page source. A path
ending `/` is a whole-Folder relationship and may be useful navigation, but it
cannot satisfy an evidence binding until SURVEY resolves an exact accepted
file or Result within it.

The board exposes `POST /_board/pagex-match` as a read-only candidate
shortlist. It reports transparent token overlap and a short excerpt, but its
result is deliberately `inspect exact source before use`: the endpoint never
binds evidence, edits the borrow list, or claims that similarity is evidence.

When a source Page already owns an accepted probe answer, PageX borrows the
exact accepted Page material and keeps that Page as the durable authority; it
does not open a new local Probe card merely to mirror the source. When a Display
is reused as evidence, cite its fully qualified unit id or borrow its specific
file. Link the whole Folder only when the relationship is to that work object
and its lifecycle, not as a shortcut for naming an evidentiary scope.

## 🛬 LAND validation · link, supports, input, then local Result

For every `☑ make` item, LAND validates every PageX binding before freezing the
Local Input. It confirms that the exact target exists, its authority is
accepted, and the bytes, version, or hash still match what SURVEY selected. A
dangling, superseded, whole-Folder-only, or merely similar source keeps the item
in LAND or routes it back to SURVEY.

PageX never replaces either Run layer. LAND closes only when all declared
Supporting Results are valid, all PageX bindings are valid, one Local Input
freezes both sets of sources, and exactly one local Page Evidence Item Run has
an accepted `VALUE`, `CITE`, or `DISPLAY` Result. The PageX segment shows this
whole lineage without counting the link as another Run or Result.

## 🗂 Storage · MIXED, one ranked list and the links minted from it

```text
<page>/outline/evidence/pagex/
├── <stem>.md                         PRIMARY · link list, ORDER = rank
├── <src-page>/<inner path>           DERIVED · exact-file symlinks
├── _folders/<repo-relative Folder>/  DERIVED · whole-Folder symlinks
└── <stem>-view.html             DERIVED · the 🔗 card view
```

The row grammar is one line: `- <repo-relative path>` with an optional
` · note: free text`. A whole Folder ends in `/`, preserving its kind even
when the target later moves. A row ending ` · removed` is the person's ✕
tombstone with ↩ to restore.
A minted link keeps the SOURCE page's inner path, so `QPs1-overall/skill/QPs1-overall.md` rather than a flat basename: a page's own md and its skill list often share a stem, and the inner path both prevents that collision and says which layer was borrowed.

## ⚖️ The two laws

**Choose the relationship's scope.**
Use an exact file for an evidence claim. Use a whole Folder when the consumer
depends on the work object, needs its two faces, or tracks its lifecycle.
PageX accepts a directory only when it is recognizably a Folder: it has a named
Page Face, Task plan/report/QA evidence, explicit `folder.yaml`, or belongs to
a compatibility `tasks/` tree. It refuses arbitrary directories, the repo
root, the consumer's own home, anything inside its PageX lane, and any path
resolving outside the repo.

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

## ⚙️ Writer · four routes

```text
POST /_board/pagex          seed from the prose · re-mint every live row's
                            symlink · rebuild the view
POST /_board/pagex-order    the drag: the store keeps exactly the sent order
POST /_board/pagex-entry    the pen: `borrow` one file or Folder path OR a
                            list (note optional, lands at the TOP) · ✕ remove
                            (tombstone) · ↩ restore
POST /_board/pagex-match    OUTLINE's read-only candidate shortlist; no write
GET  /_board/pagexview      one borrow, framed under ← ☰ → over the list
```

`borrow` takes a list so one gesture can move a batch: a Page card's ✕ drops
every exact-file row for that source, while a whole-Folder row is one ranked
relationship.

The pen's field is `borrow`, not `path`: every view merges the board context `{path, file}` into its POST body, so a borrowed file sent as `path` is overwritten by the board's own path.

**The minter's one safety rule**: it only ever unlinks a SYMLINK inside
`outline/evidence/pagex/` (or an explicitly detected flat compatibility stub).
A real file that lands there is never touched, so a re-mint can be run at any moment without eating anything it did not make.
A target that resolves outside the repo root, is not an addressable Folder, is
self-referential, or already has a real file in its slot is refused with the
reason shown on its card.

## 📡 Evidence segment · the 🔗 view

Exact files retain ONE CARD PER SOURCE PAGE, in the person's rank, not one per
borrowed file (JL 260816: "每一个 page folder 我们用了它的哪些 information …
这个 sub-folder 用了，那个 sub-folder 没有用").
On stage: the page's name as the title, its live `state:`, then its WHOLE folder as an inventory — `using N of M`, ✅ on each part in use, ⬜ on each part not, every ⬜ carrying ＋ use, which takes that folder's files in one click. Under it, the files actually borrowed, each with its own ✕; the card's ✕ drops the page entirely.
A borrow list alone cannot tell a deliberate one-file borrow from a page nobody opened, which is the question the inventory answers.

A whole-Folder row gets one Folder card in the same rank. It shows:

- Page Face present or absent, plus the source `state:` when present;
- Task plan and report present or absent;
- `QA/*.md` receipt count;
- live lifecycle badge: reported, planned, Page-only, or unknown.

These are source-file reads on every refresh, never status copied into PageX.

**The title opens the BOARD PAGE, framed with a way back** (JL 260816: "why not the page in the board, but the raw markdown????" and "我点进去之后，怎么退回来呢？").
A borrow is taken to be read, and reading happens on the rendered page with its prose, comments, and rail; a served `.md` is raw text. A borrowed page md resolves to `board/<group>/<stem>.html` by walking up for board.md, and `GET /_board/pagexview` frames it under ← ☰ →: ☰ returns to the cards, the arrows walk the borrows in ranked order, and `open on its own` escapes the frame. The page is served untouched inside it, never rewritten.
A borrow whose source has moved shows ⚠ dangling with what it pointed at, which is the whole reason this is a link and not a copy.
Under the cards sits one folded ＋, the by-path pen; nothing on stage asks a person to choose before the scan has run.

The 📂 folder tab marks a symlink row with a bare 🔗, full target on hover, because it reports the RESOLVED file and a borrowed page md would otherwise read as duplicated bytes (JL 260816: "are they copied or are they the symlink?").
The mark stays bare: pagex mints links whose place mirrors the source, so spelling the target out repeats the row's own name and was the first fix's own defect.


> The canonical lane is `outline/evidence/pagex/`. A former root `evidence/`
> or flat PageX path is read-only migration input and must not be recreated.

## 📂 Files and ownership

- `../../haipipe-board/live/pagex.py`
  The three routes, the store writer, the minter and its vet, the prose scan behind the seeder, and the card view.
- `../../haipipe-board/assets/js/10-drawer/07-plugin-outline.js`
  The single 🧭 Outline registration whose Evidence Workspace includes PageX.
- `../../haipipe-plugin/ref/roster.md`
  The internal `pagex/` storage row owned by `haipipe-plugin-outline`.

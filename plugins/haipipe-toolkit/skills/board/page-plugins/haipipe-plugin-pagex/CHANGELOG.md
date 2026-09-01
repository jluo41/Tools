# CHANGELOG · haipipe-plugin-pagex

## 0.6.3 — 2026-08-31
- Lives nested at evidence/pagex (JL); minter computes relpath from the
  REAL dir so stub-era re-mints keep the right depth.

## 0.6.2 — 2026-08-31
- Surface rehomed: the borrow view is the 🔗 Pagex segment inside the one 🧾
  Evidence tab; the standalone strip row folded away, every pen rides inside
  the saved view unchanged.

## 0.6.1 · 2026-08-31

Category-folder sweep: lane paths read `<page>/evidence/<lane>` or
`<page>/delivery/<lane>` (haipipe-page 0.47.0 §📁); flat names are the same
lane during migration (stubs).


## 0.6.0 — 2026-08-20

- **0.5.0 and 0.6.0 shipped in SKILL.md with no entry here**, both in the 260819
  phase-agent split (`3aaeba4f`) and its 260820 follow-up. Reconstructed from the
  frontmatter each version left behind rather than re-authored: PageX became
  Probe's ACCEPTED-PAGE lane, selected and bound during OUTLINE, beside the QA
  lane that runs at PROBE/EVIDENCE. Recorded 260822 while closing a
  version-vs-changelog sweep; the per-change detail is in the git log, not here.

## 0.4.0 · 2026-08-17

Documents PageX as PROBE's cross-page MATCH surface: it is a ranked live reuse
list, not a second QA bank, and exact reuse leaves an audit trace without copy.
Adds the read-only `pagex-match` candidate endpoint; overlap is navigation and
never an automatic reuse decision.

## 0.3.0 · 2026-08-16

A card stopped being a borrowed file and became a source PAGE with its inventory.

- JL: "每一个 page folder 我们用了它的哪些 information … 这个 sub-folder 用了，那个 sub-folder 没有用之类的？" One card per source page now, carrying that page's whole folder as `using N of M` with ✅ on each part in use and ⬜ on each part not. A list of what was taken could not distinguish a deliberate one-file borrow from a page nobody opened.
- Every ⬜ row carries ＋ use, which takes that folder's files in one click; the picker ruling of 0.2.0 binds here, so there is no dropdown and nothing to type.
- `GET /_board/pagexview` frames a borrowed page under ← ☰ →. JL: "我点进去之后，怎么退回来呢？我进去之后好像没法退回来了" — the bare link had replaced the tab with a full board page and left no exit.
- `pagex-entry` accepts a list, so a card's ✕ drops a whole page and a folder's ＋ takes a whole folder in one POST.

## 0.2.1 · 2026-08-16

Two surface defects, both about landing where a person came for.

- A borrow opened as RAW MARKDOWN. JL: "when I open them, why not the page in the board, but the raw markdown????" A card's title now resolves a borrowed page md to its rendered `board/<group>/<stem>.html`; the raw file dropped into the `where` fold.
- The 📂 row was unreadable. JL: "very ugly." The 0.2.0 link mark printed the whole repo path inline, and in a flex row that crushed the filename to nothing while the path wrapped over three lines. The mark is now a bare 🔗 with the target on hover, spelled out only when the link's place differs from its target.
- The repo path left the card's stage for the same fold, leaving the source page's name, its live state, and the borrowed file.

## 0.2.0 · 2026-08-16

The picker came out the day it shipped.

JL saw the first 🔗 tab and rejected its centre: "I don't think the filter should be there, it should not be manually added."
The build had asked a person to choose a page, open a dropdown of its files, type a reason, and press ＋ borrow — three manual gates, where the skill plugin already rules one law for exactly this shape: the scan seeds, the person ranks.

- A refresh now SEEDS: it reads the page ids this page's prose already writes and borrows each named page's own `.md`, appended at the bottom with `note: scan-seeded — this page names <id> N×`.
- The note-required gate is gone; it had been invented in this plugin and belonged to no other.
- `POST /_board/pagex-find` and the repo-wide shape query retired with the surface they lived in; the ＋-by-path pen, folded shut, keeps the cross-board reach.
- `folderstat.py` prints `🔗 link → <target>` on a symlink row, answering the question the 📂 tab could not: "are they copied or are they the symlink?" It had reported each borrowed file's RESOLVED size, so a link read as duplicated bytes.

## 0.1.0 · 2026-08-16

Born, whole, in the session that asked for it.

JL asked for a way to build a new page out of material that already lives in other pages, by reference and not by copy: "不是 all-in-one，按需引用 … 可以用软链接的方法把那些内容给弄出来".
The plugin ships as the third citation twin, after bibex (into the literature) and skill (into the skill tree).

- The store, the minter and its vet, the pen, the drag, and both finding routes: `live/pagex.py`.
- The 🔗 tab: `assets/js/10-drawer/85-plugin-pagex.js`.
- The design page: `QPf11` on the board skill's own board.

Two rules were forced by the first real borrow rather than designed in the abstract.
A minted link keeps the source page's inner path, because QPs1's page md and its skill list share the basename `QPs1-overall.md` and a flat layout collides on the second borrow.
The pen's field is `borrow` and not `path`, because every view merges the board context `{path, file}` into its POST body and a borrow sent as `path` is silently overwritten.

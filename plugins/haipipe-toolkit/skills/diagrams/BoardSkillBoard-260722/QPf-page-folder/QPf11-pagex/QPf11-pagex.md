# Pagex · the page's citations into the repo's other pages
state: ✅ SETTLED · shipped and lived in 260816; every aim met against a live borrow on this page
owner: JL
method: give a page a ranked borrow list of FILES from other pages, and materialize each row as a symlink so the borrowed material is read in place, live, never copied

## Opening
How does a page borrow a file from another page and read it live, without copying it?
A borrow here is one file, not a whole page folder: one deck from a slide page, one float from a display unit.
Copying ages the moment the source moves, and a person browsing cannot see which borrowings still point at something real.
This page rules the pagex plugin: a ranked list of borrowed files a person writes, plus symlinks re-minted from that list into the page's own folder.

**The family shape**: bibex holds the page's references into the literature, skill into the skill tree, and pagex into the repo's page tree: the third twin, same grammar.

**Covered elsewhere**: the roster row is `../../board/haipipe-plugin/ref/roster.md`; the twin whose store grammar this adopts is `QPf10` (skill); the folder tab that will show pagex/ like any other plugin is `QPf1`.

## Diagram
**The pagex store and its shadows**: the ranked list a person writes, and the two things a refresh re-mints from it.
```text
  🗂 QPf3-slide/slide/deck.html    🗂 …/OtherBoard/QX2/display/float.tex
        │   pick FILES, never a page's home folder   │
        ▼                                            ▼
  🗃 pagex/<stem>.md         PRIMARY · one row per borrowed file
        🏷 row       <repo-relative path> · note: why it is wanted
        🥇 order     the person's rank, top first
        ✕ removed    a tombstone the refresh never re-seeds
        │
        ▼ refresh re-mints, from the store ONLY
  ⚙️ pagex/<source-page-stem>/<inner path>   DERIVED · relative symlinks
  ⚙️ pagex/<stem>-view.html                  DERIVED · the 🔗 card view
```
The list is the truth; the symlinks and the view are shadows re-minted from it.

## Content
### 1 · The contract
**The two halves of pagex/**: what a person writes and keeps, and what a refresh may overwrite.
```text
  🗃 PRIMARY   pagex/<stem>.md            rows · order · tombstones · committed
  ⚙️ DERIVED   pagex/<src>/<inner path>   relative symlinks · re-minted
  ⚙️ DERIVED   pagex/<stem>-view.html     the 🔗 card view · re-minted
  ⚖️ the rule  a refresh writes the derived half and never the store
```
**A MIXED plugin, like bibex and skill**: one primary file a person rules, everything else regenerable.
The store is `<page>/pagex/<stem>.md`, one row per borrowed file, repo-relative path, order = rank, tombstone = ` · removed`.
The symlinks are DERIVED: the refresh deletes only links it minted and re-creates them from the store, one folder per source page keeping the source's inner path, so a builder sees `pagex/QPs1-overall/skill/QPs1-overall.md` and reads the live original.
A copy would age silently; a symlink stays current while the source keeps moving, and when the source is renamed or archived the link breaks VISIBLY and the view flags it ⚠ dangling instead of showing yesterday's content.

### 2 · The reach and its vet
**The vet a refresh must run**: which targets a row may reach, and what a refusal has to show.
```text
  ✅ allowed   any file under the repo root · other boards, other projects
  🚫 refused   a target resolving outside the repo root
  🚫 refused   a page's HOME folder · file rows only
  🔗 written   relative links, so a clone or a move stays portable
  📣 shown     a refused row keeps its reason on its card
```
**Scope is the whole repo**: a row may point into another board or another project's pages, not only this board's tree.
The refresh must be the only symlink minter, and it must vet every target: a path resolving outside the repo root is refused, with its reason shown on the card.
Links must be written relative, so the repo stays portable across machines and clones.

### 3 · The boundary
**Where discovery stops**: the rule that already hides plugin folders, and the one link shape it cannot survive.
```text
  🧱 _in_plugin   a non-page subfolder of a folded page is a plugin
  🙈 the effect   discovery never enters it, so a linked Q*.md is no ghost page
  ⚠ the trap     a DIRECTORY link named like a page satisfies _page_home
  ⛔ the rule     pagex links files only, never a page's home folder
```
Discovery never sees a borrowed page twice.
`_in_plugin` in `src/common.py` already blinds discovery to every non-page subfolder of a folded page, so a symlinked `Q*.md` inside pagex/ cannot surface as a ghost page.
The one trap is a DIRECTORY symlink named like a page's home: it would satisfy `_page_home` and discovery would walk in, so the contract forbids linking a page's home folder outright.
Pagex links files, which is the point of the plugin anyway.

### 4 · The seeding
**The scan borrows; the person ranks**: the skill map's law, adopted whole.
```text
  📄 <page>.md  ── the page ids its own prose already writes ──▶ the SCAN
        │            QPs1 16× · QPf10 9× · QPf1 7× · QPf3 4×
        ▼
  🗃 the store   each named page's OWN md, appended at the BOTTOM,
                 with `note: scan-seeded — this page names <id> N×`
        │        a ` · removed` row is the person's ✕, never re-seeded
        ▼
  ⠿ the person   drags to rank · ✕ to drop · ＋ by path for depth
```
A page cannot lean on another page silently: it says so in its prose, in the Opening's "Covered elsewhere" line and in every sentence that cites an id.
So the borrow is already declared, and asking someone to re-enter it by hand is asking them to say the same thing twice.
The first build got this backwards and shipped a picker (choose a page, open a dropdown of its files, type a reason, press ＋ borrow), which JL threw out the hour it appeared: "I don't think the filter should be there, it should not be manually added."
What the machine may not decide is RANK, so a seeded row lands at the bottom and everything above it is the person's order, exactly as `QPf10` rules for skills.

**What a seed borrows is the named page's own `.md`**, because that is what the prose named; a deeper file, a component or a display unit inside that page, is reached with the ＋-by-path pen and is the one thing still worth arguing (see the Decision Now row in States).

### 5 · The first worked borrow
**The QPs1 borrow, on disk**: the row, the link minted from it, and what minting it buys.
```text
  the row     - …/QPs-page-structure/QPs1-overall/skill/QPs1-overall.md
                  · note: borrow its skill ordering to start QPf11's own list
  the link    pagex/QPs1-overall/skill/QPs1-overall.md
                  ──▶ ../../../../../QPs-page-structure/QPs1-overall/skill/…
  the point   QPs1 re-ranks tomorrow ▶ QPf11 reads the NEW order, not a snapshot
```
This ran: the row sits in `pagex/QPf11-pagex.md` and the link beside it resolves to QPs1's live list, at exactly the five-`../` depth the figure was drawn with while it was still a design.
Designing it before building it is what refined §1's layout, and the specimen forced the inner-path rule: QPs1's page md and its skill list SHARE the basename `QPs1-overall.md`, so a flat per-page folder would collide; keeping the source's inner path makes collision structurally impossible, and the path itself says which layer was borrowed.
It also drew the line to the skill twin: pagex borrows a list to READ, while seeding QPf11's OWN skill list from those names is the skill plugin's pen, copied once and then the person's; pagex never fakes that door.

## Aims
### A1 · 📐 The contract
- A1.1 · The row grammar parses and survives a refresh untouched: order kept, tombstones kept, nothing re-seeded.
  **Done when:** A refresh over a hand-written store leaves every row byte-identical.
- A1.2 · The pen ships: add a row by picking a page then a file, note, ✕ remove, ↩ restore, ⠿ drag-to-rank.
  **Done when:** Each of those five actions writes the store from the tab, and nothing else writes it.

### A2 · 🌍 The reach and its vet
- A2.1 · Refresh re-mints relative symlinks from the store only, one folder per source page, and deletes nothing it did not mint.
  **Done when:** A refresh creates a link for every live row and touches no other file under pagex/.
- A2.2 · The repo-root vet holds: a target outside the repo is refused visibly; a page HOME folder is refused outright.
  **Done when:** Both refusals are reproduced on a test row, each showing its reason on the card.

### A3 · 🚧 The boundary
- A3.1 · A board holding live pagex/ folders builds clean: no ghost pages, no duplicate-basename warnings from borrowed files.
  **Done when:** A build and check over a board with minted links report neither finding.

### A4 · 🔍 The seeding
- A4.1 · The prose scan lists the page ids this page's own md names, ranked by how often it names them, each with the source page's state.
  **Done when:** The scan runs from the tab and returns that ranked list without a person reading the md.
- A4.2 · The shape query answers "which pages anywhere carry a `<plugin>/`" across every board in the repo, one row per candidate file.
  **Done when:** One query returns candidates from more than one board in a single list.
- A4.3 · A candidate row shows the source page's live `state:`, so borrowing an unsettled page is a visible choice rather than an accident.
  **Done when:** A candidate's badge changes after its source page's head line changes.

### P · 🔗 The surface
- P0 · Opening a borrow lands where a person READS: the board page it renders as, never the raw markdown.
  **Done when:** A card's title opens the rendered page, and the raw file is a second, smaller door.
- P1 · The tab shows borrow cards grouped by source page; each file opens as the served file; a dead link shows ⚠ dangling with what it pointed at.
  **Done when:** All three behaviours are seen on one page holding a live borrow and a broken one.
- P2 · The 📂 folder tab treats pagex/ as source material with an age, never STALE, because a symlink cannot go stale.
  **Done when:** A page with minted links shows an age and no STALE marker in the 📂 tab.
- P3 · A borrowed file is legible as a LINK wherever the folder is shown, never as a copy.
  **Done when:** The 📂 tab names the link's target on the row, so nobody has to ask which it is.

## States
### 🗣 Decision Now
🗣 Does a seed ever go DEEPER than the named page's own `.md`?
📍 Part: §4, the seeding · 🔔 Why now: the ask that opened this page was about borrowing "其他 pages 里面的 component … 或者用它们的 props、display", and a seed that stops at the page md never reaches one.
- ⭐ **Stay shallow.** A seed borrows the named page's md, and a deeper file is the ＋-by-path pen's job. Zero invention: the prose named a PAGE, not a file inside it.
- **Seed a page's PRIMARY plugin files too** (its `skill/` list, its `draw/` scene), so a named page arrives with the parts a builder actually reuses. Richer, but the machine starts choosing what you meant.
- **Seed shallow, then offer a one-click "go deeper" on the card**: no dropdown and no note, just the named page's files listed under it once you ask.

🛑 Blocks: nothing; the pen already reaches any file.
🤖 If nobody answers: stays shallow, which is what shipped.

The plugin shipped 260816 and this page is its first consumer: `QPf11-pagex/pagex/` holds a real store and two live symlinks, so every state below was read off a working borrow rather than a test rig.

### A1 · 📐 The contract
- ✅ A1.1 · A re-mint over the two-row store left it byte-identical (md5 before and after), so the derived half is the only half a refresh writes.
- ✅ A1.2 · All five actions round-tripped through the routes: ＋ borrow with a note, the note-less refusal, ✕ (tombstone written, link withdrawn), ↩ (link re-minted), and the drag, which moved QPs1 above QPf10 in the store.

### A2 · 🌍 The reach and its vet
- ✅ A2.1 · Both rows minted as relative links, and a hand-written `HANDWRITTEN.txt` dropped into `pagex/` survived a re-mint untouched: the minter only ever unlinks a symlink.
- ✅ A2.2 · Both refusals reproduced with their reasons: `../../../etc/hosts` refused as not under the repo root, and `QPs1-overall/` refused as a folder, naming the ghost-page reason.

### A3 · 🚧 The boundary
- ✅ A3.1 · The board rebuilt with two live links, one of them a borrowed page's OWN md (the riskiest shape): 16 QPf pages as before, no ghost page, no duplicate-basename warning, no `QPs1` leaking into `board/QPf/`.

### A4 · 🔍 The seeding
- ✅ A4.1 · Superseded upward and met: the scan no longer offers a ranked list to pick from, it BORROWS. One refresh against an empty store seeded four rows (QPs1 16× · QPf10 9× · QPf1 7× · QPf3 4×) and minted four links, with no typing at all.
- ⏸️ A4.2 · Retired on JL's 260816 ruling with the picker it belonged to. The repo-wide shape query worked (one `draw/` run returned 81 pages across `BoardSkillBoard-260722` and `SubjectiveLabel-260722`) and was removed anyway, because its only surface was the filter; the ＋-by-path pen keeps the cross-board reach, and a finder can return if a real borrow ever needs one.
- ✅ A4.3 · The cards read the head line live: QPs1 shows `🟡 REOPENED 260816` beside QPf10's `✅ SETTLED`, which is the disclosure this aim asked for.

### P · 🔗 The surface
- ✅ P1 · The 🔗 tab is registered and renders the cards; a borrowed file opens as the served original, and a deleted source turned its card `⚠ dangling · the target no longer exists` before the probe row was cleared.
- ✅ P2 · Met by construction: `folderstat.py`'s `DERIVED` set does not name pagex, so the 📂 tab reports the folder as source material with no STALE marker.
- ✅ P0 · A card's title opens the board page: QPs1's card lands on `board/QPs/QPs1-overall.html`, the rendered page with its prose, comments, and rail. The raw file moved into the `where` fold, which is also where the repo path went.
- ✅ P3 · A borrowed file no longer reads as a copy in the 📂 tab. JL asked the plain question the surface could not answer, "are they copied or are they the symlink?", and it could not, because the row reported the RESOLVED file, so a linked 13KB page md looked like 13KB of duplicated bytes. Each symlink row now carries `🔗 link → <target>`.

## Files
### ⚙️ Engines
- `../../board/haipipe-board/live/pagex.py`
  The whole plugin: the store reader and writer, the minter and its vet, both finding routes, the four POST doors, and the card view.
- `../../board/haipipe-board/assets/js/10-drawer/85-plugin-pagex.js`
  The registry entry whose `tab` spec the shell builds the 🔗 tab from.
- `../../board/haipipe-board/live/skillmap.py`
  The skill twin, whose store grammar, drag route, and view shape pagex adopts rather than reinvents.

### 📋 Contracts
- `../../board/haipipe-plugin/ref/roster.md`
  The one list of plugin names; the `pagex/` row there is what this page rules.
- `../../board/page-plugins/haipipe-plugin-pagex/SKILL.md`
  The plugin's own delta-only skill, shipped with the row when it went 🟢.

### 🧪 Evidence
- `pagex/QPf11-pagex.md`
  This page's own borrow list, the plugin's first consumer: QPs1's skill list and QPf10's page md, ranked.

### 🧪 Checks
- `../../board/haipipe-board/src/common.py`
  `_page_home` and `_in_plugin`: the discovery walk that would surface a borrowed page as a ghost, and where §3's boundary is tested.

## Law
- 🏷 The name is `pagex/`, bibex's twin (JL 260816).
- 🌍 The reach is the whole repo, not one board (JL 260816); the refresh vets every target under the repo root.
- 📄 Pagex links FILES, never a page's home folder: a directory link named like a page would become a ghost page home.
- ✂️ The scan SEEDS, the person RANKS (JL 260816: "I don't think the filter should be there, it should not be manually added"): `QPf10`'s law adopted whole: a refresh borrows every page this page's prose names, appends it at the bottom, and never edits, reorders, or re-seeds a row; the ＋-by-path pen is for depth, not for the common case, and its note is optional.
      This overturns CC's own note-required gate of the same day, which had made a person type by hand what the page already said.
- 🧭 A minted link keeps the source page's INNER path (`pagex/<source-stem>/<inner path>`): QPs1 proved a flat layout collides, because a page md and its skill list share a basename.
- 🗃 The store is the only truth: symlinks and the view are re-minted from it, and a refresh never edits, reorders, or removes a row a person wrote.

## Log
- 260816 · [RULE-JL] two surface defects, both mine, both about respecting what a person came for. First, a borrow opened as RAW MARKDOWN (JL: "when I open them, why not the page in the board, but the raw markdown????"): the card linked the served file, but a page is taken to be READ, and reading happens on the rendered board page with its prose, its comments, and its rail. A borrow that is a page md now resolves to `board/<group>/<stem>.html` by walking up for board.md, and the raw file dropped to a small link inside the `where` fold. Second, the 📂 row was unreadable (JL: "very ugly"): my link mark had printed the whole repo path inline, and since the row is a flex line the filename was crushed to nothing while the path wrapped over three lines. The mark is now a bare 🔗 with the full target on hover, shown only when the link's place differs from its target, which for pagex is almost never. On the card the same path went into a fold, leaving the source page's name, its live state, and the borrowed file on stage.
- 260816 · [RULE-JL] the filter came out and the scan took over (JL, on the first screenshot of the 🔗 tab: "I don't think the filter should be there, it should not be manually added"). The shipped surface had made a person choose a page, open a dropdown of its files, type a reason, and press ＋ borrow, three manual gates where `QPf10` already rules ONE, namely that the scan seeds and the person ranks. A refresh now borrows every page this page's prose names, appending at the bottom with a `scan-seeded` note carrying that id and its count; the note-required gate CC had invented the same morning is gone, and the ＋-by-path pen folded shut as the depth door. Proven against an emptied store: one click seeded QPs1 16× · QPf10 9× · QPf1 7× · QPf3 4× and minted four links with nothing typed. The shape query retired with the filter it lived in (A4.2), leaving the pen as the cross-board reach. Same round, JL's second question exposed a surface that was quietly contradicting the plugin's whole claim: "are they copied or are they the symlink?" The 📂 tab reported each borrowed file's RESOLVED size, so a link read as 13KB of duplicated bytes, and `folderstat.py` now prints `🔗 link → <target>` on a symlink row (P3).
- 260816 · [BUILD-CC] the plugin shipped whole on JL's word ("那你就给我 work 到一直能 work 为止"), and this page became its first consumer: `live/pagex.py` with four doors, `85-plugin-pagex.js` for the 🔗 tab, the roster row 📋 → 🟢, and `haipipe-plugin-pagex` beside it, since a row going live brings its skill with it. Every aim was met against a real borrow rather than a rig; the specimen §5 designed on paper is now two symlinks on disk, and the five-`../` depth it predicted is what the minter wrote. Three things the build corrected in the design: the pen's field had to become `borrow`, because every view merges the board context `{path, file}` into its POST body and a borrow sent as `path` is silently overwritten by the board's own path (caught before the first click); the shape query had to group by BOARD and disclose its cap, because one `draw/` run returned 81 candidates across two boards and a bare page stem cannot say which one it came from; and the minter's safety rule was written as "only ever unlink a SYMLINK", then proven by leaving a hand-written file in `pagex/` through a re-mint. The riskiest boundary case was tested rather than reasoned about: borrowing a page's OWN md, then rebuilding, gave no ghost page and no duplicate-basename warning.
- 260816 · [REVISE-CC] structure and truth pass under the same purpose and Aims: the `state:` line took a legal 🔴 token, `## States` was rebuilt to mirror all ten Aim ids at ⬜, `## Files` moved above `## Law`, the Aims groups took their divisions' numbers, names, and emoji in order (the boundary aim became A3.1 and the two surface aims became P1 and P2), the checkboxes gave way to plain ids with a `Done when` line each, and the four board-skill citations lost one `../` and now resolve to files that exist. Two claims failed verification and were corrected: the `skill/` folder count is 16 and not 21, all 16 on this board, and QPs1 was not alone at 🟡, since QPf3 is PARTIAL while QPf10 and QPf1 are SETTLED. §2's minting rule became a contract instead of a running fact, §5 was captioned as the designed specimen because no pagex/ folder or symlink is on disk, each division gained a captioned face figure, and the Opening question, five em-dashes, two whole-line bold sentences, and the Chinese note row were rewritten.
- 260816 · [DRAFT-CC] the finding got its contract (JL: "我们怎么知道，比如说我们是需要这一个配置还是那一个配置？它会通过什么方法去做这个搜寻呢？"): the first two drafts specified the ROW and never how a row is found, and with 16 `skill/` folders on this board browsing is no method at all. §4 now carries two routes for two starting points: the prose scan, ranked by mention count, which reaches inside this board only, and the shape query, folderstat widened to the tree, which is the only one that crosses boards, plus the source page's live state on every candidate. That last one was not designed but observed: scanning QPf11 put QPs1 far ahead of QPf10, QPf3, and QPf1, and reading their heads showed QPs1 reopened that same day, so the most-wanted borrow was the least settled. A4 opened with three aims and the Law took the note-required line; CC decided it, because nothing stopped on it.
- 260816 · [DRAFT-CC] the first worked borrow (JL: "我们可能会引用这个 skill 配置来帮我们给现在这个 QPf11，你觉得该怎么引用呢?"): QPs1-overall's skill list became the specimen row in §5, and it refined the contract twice: the minted link now keeps the source's inner path (QPs1's page md and skill list share a basename, so the flat layout of the first draft collides), and the pagex-vs-skill-pen line was drawn, since pagex borrows to READ while seeding QPf11's own list is the skill plugin's door.
- 260816 · [DRAFT-CC] page born from JL's ask ("我想有这样一个 plugin，能把需要引用的这些 pages 给组织起来… 按需引用… 可以用软链接"): the third citation twin, file-level borrowing materialized as symlinks. JL ruled the name `pagex/` over `use/` and `pages/`, and the reach repo-wide over same-board, in the same session; CC's boundary read of `_in_plugin` (src/common.py:207) grounded the never-link-a-page-home law. Roster row added as 📋 declared.

# Pagex · the page's citations into the repo's other pages
state: 🟡 PARTIAL · shipped, seeded, ranked, linked · open: seed depth, the raw-file door, A4.2 on ice
owner: JL
method: give a page a ranked borrow list of FILES from other pages, and materialize each row as a symlink so the borrowed material is read in place, live, never copied

## Opening
How does a page use a file that lives on another page, and always see the newest version?
It borrows one file, not a whole page: one deck from a slide page, one figure from a display page.
Copying is the easy answer and the wrong one, because a copy stops changing the moment the original moves on.
This page decides the answer: the page keeps a short list of the files it borrows, and shortcuts to those files are built from that list.

**Its two cousins**: `bibex` lists the papers a page cites, `skill` lists the skills it leans on, and this one lists the files it borrows. Same shape, three different things pointed at.

**Covered elsewhere**: the list of plugin names is `../../board/haipipe-plugin/ref/roster.md`. `QPf10` is the cousin whose list format this copies. `QPf1` is the 📂 tab that shows this folder like any other.

## Diagram
**The pagex store and its shadows**: the ranked list a person keeps, and the two things a refresh re-mints from it.
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
### 1 · What you keep, and what gets rebuilt
**The two halves of the folder**: one file is yours, everything else is rebuilt from it.
```text
  🗃 PRIMARY   pagex/<stem>.md            rows · order · tombstones · committed
  ⚙️ DERIVED   pagex/<src>/<inner path>   relative symlinks · re-minted
  ⚙️ DERIVED   pagex/<stem>-view.html     the 🔗 card view · re-minted
  ⚖️ the rule  a refresh writes the derived half and never the store
```
📌 One file in this folder is yours to write; everything beside it is rebuilt from that file and may be overwritten.

The list lives at `<page>/pagex/<stem>.md`.
It holds one line per borrowed file: where the file is, why you wanted it, and where it sits in your order.
A line ending ` · removed` is one you dropped, and a rebuild never brings it back.

The shortcuts are rebuilt, not written by you.
A rebuild deletes only shortcuts it made itself, then makes them again from the list.
Each source page gets its own folder, keeping the file's path inside that page, so you open `pagex/QPs1-overall/QPs1-overall.md` and read the real thing.
If the original is renamed or filed away, the shortcut breaks where you can SEE it and the card says `⚠ dangling`.
A copy would have quietly shown you last week's text instead.

### 2 · Which files a line may point at
**The check every rebuild runs**: what a line may reach, and what a refusal has to show you.
```text
  ✅ allowed   any file under the repo root · other boards, other projects
  🚫 refused   a target resolving outside the repo root
  🚫 refused   a page's HOME folder · file rows only
  🚫 refused   a target inside this page's own pagex/ · a borrow of the borrow
  🚫 refused   a slot already holding a real file the minter did not mint
  🔗 written   relative links, so a clone or a move stays portable
  📣 shown     a refused row keeps its reason on its card
```
📌 A line may point at any file in this repo, on any board; anything outside is refused, and the refusal says why.

A line may reach into another board, or another project, not just this board.
Only the rebuild makes shortcuts, and it checks every target first.
A target outside the repo is refused, and the reason shows on the card instead of failing quietly.
Shortcuts are written as relative paths, so the repo still works after it is copied or moved.

### 3 · Why a borrowed page never becomes a second page
**Where the page hunt stops**: the rule that skips plugin folders, and the shape this never makes anyway.
```text
  🧱 _in_plugin   a non-page subfolder of a folded page is a plugin
  🙈 the effect   discovery stops at pagex/, so a linked Q*.md is no ghost page
  ⛔ the rule     pagex links files only, never a page's home folder
  📣 the refusal  the minter and the pen both refuse a folder, reason on the card
```
📌 The board's page hunt stops at this folder, so a borrowed page never shows up twice in the board.

The board finds its pages by walking the folders.
`_in_plugin` in `src/common.py` tells it to stop as soon as it reaches `pagex`, and to skip everything under it.
So a borrowed `Q*.md` never appears as a second, ghost page, and neither does the list file itself.
The hardest case would be a shortcut to a whole page FOLDER.
That shape is never made: this plugin borrows files only, and both the rebuild and the ＋ button refuse a folder.

### 4 · The list fills itself; you put it in order
**The machine suggests, you rank**: the same rule the skill list already follows.
```text
  📄 <page>.md  ── the page ids its own prose already writes ──▶ the SCAN
        │            at the seed · QPs1 16× · QPf10 9× · QPf1 7× · QPf3 4×
        ▼
  🗃 the store   each named page's OWN md, appended at the BOTTOM,
                 with `note: scan-seeded — this page names <id> N×`
        │        a ` · removed` row is the person's ✕, never re-seeded
        ▼
  ⠿ the person   drags to rank · ✕ to drop · ＋ by path for depth
```
📌 The page already names the pages it leans on, so the machine reads those names and fills the list; you only put them in order.

A page cannot lean on another page in secret.
It says so in its own words, in the "Covered elsewhere" line and in every sentence that names another page.
The borrow is therefore already written down, and asking someone to type it again is asking them to say the same thing twice.
The first build got this backwards.
It shipped a picker: choose a page, open a list of its files, type a reason, press ＋.
JL threw it out the hour it appeared ("I don't think the filter should be there, it should not be manually added").

What the machine must NOT decide is your order.
A suggested line lands at the bottom, and everything above it is where you put it, the same rule `QPf10` follows for skills.
The count in a line is the count on the day that line was added, and later rebuilds leave it alone.

**A suggested line takes the named page's own `.md`**, because a page is what the writing named.
A file deeper inside that page is added with the ＋ button, and whether that should happen by itself is the open question in States.

### 5 · What of a page you use, and what you do not
**One card per page you borrow from**: its whole folder, with the parts you use ticked.
```text
  📄 QPs1-overall   🟡 REOPENED 260816          using 1 of 3
     ✅ 📄 QPs1-overall.md   1 file
     ⬜ 📁 draw/             1 file    ＋ use
     ⬜ 📁 skill/            3 files   ＋ use
```
📌 A card shows the whole source page, so you can see what you took and what you left.

A plain list says nothing about what it did NOT take.
That silence is what trips a reader up: taking one file on purpose and never opening a page at all look exactly the same.
So the list could not answer the plain question JL asked of it, which was which parts of that page are we actually using.
Now each card shows that page's whole folder with `using 1 of 7` on top, and the parts you left carry ＋ use, which takes a folder in one click with nothing to type.

### 6 · Opening a borrow, and getting back
**Going in must not trap you**: the borrowed page opens inside a frame with ← ☰ → on top.
```text
  ← QPf1-folder   ☰ the borrows   → QPs1-overall     open on its own
  ─────────────────────────────────────────────────────────────────
  the borrowed board page, framed whole and untouched
```
📌 A borrowed page opens framed, with a way back to the cards and arrows to the next borrow.

The first build linked the page bare, so the frame filled with a whole board page and no way out (JL 260816: "我点进去之后，怎么退回来呢？").
Now the arrows walk your list in your own order, ☰ goes back to the cards, and the page inside is exactly what the board built, never rewritten.

### 7 · The four borrows this page actually has
**Read off the disk, not the design**: the lines the machine suggested, the order a person gave them, and the shortcuts built from both.
```text
  the rows    1 QPf10-skill   2 QPs1-overall   3 QPf1-folder   4 QPf3-slide
              each row the source page's OWN md, its scan-seeded note kept
  the rank    the person's, not the scan's: QPs1 was seeded 16× and sits second
  a link      pagex/QPs1-overall/QPs1-overall.md
                  ──▶ ../../../../QPs-page-structure/QPs1-overall/QPs1-overall.md
  the depth   four `../`, since every source sits one group folder off the board root
  the point   QPs1 is edited tomorrow ▶ QPf11 reads the NEW text, not a snapshot
```
📌 This page borrows four files, and one click built every shortcut with nothing typed.

The list holds four lines and the folder holds four shortcuts, one folder per source page.
One rebuild wrote all of them, with nothing typed by hand.
The order is no longer the machine's: QPs1 was suggested first on 16 mentions and now sits second, because a person moved it there, and a rebuild never touches that.
Every shortcut is relative, so a borrow still works after the repo is copied or moved.
Opening one proves the point: `pagex/QPs1-overall/QPs1-overall.md` shows QPs1's text as it is today, where a copy would show the day it was copied.
Each shortcut keeps the file's path inside its source page, so two files taken from one page can never collide on the same name.
These four take one file each from four different pages, so that collision has not been forced here yet.

### 8 · What the card and the folder row must admit
**Two places, two admissions**: what a card must say about the page it borrowed from, and what the folder row must not hide.
```text
  🔗 the card    the store's order, top = most wanted
                 · the source page's live state: · 🔗 linked
                 · ⚠ dangling when the target is gone · ⛔ refused, with the reason
  📂 the row     pagex/ as source material with an age, never STALE
                 · a symlink marked 🔗, full target on hover
```
📌 A card must show whether its source page is still moving, and the folder row must show that a shortcut is a shortcut.

The cards stand in your order, so the top card is the borrow you said matters most.
Each card also shows how settled its source page is, so leaning on an argument that is still changing is a choice you can see rather than an accident.
If the target is gone the card says `⚠ dangling` and gives the reason, and a refused line keeps its own reason too.
Being able to see that is the whole reason a borrow is a shortcut and not a copy.

The 📂 folder tab is owned by the folder view, but two of its rules come from here.
This folder is never marked out of date, because a shortcut cannot fall behind the file it points at.
And every shortcut row carries a 🔗 with its full target on hover, so a borrowed file is never counted as bytes this page owns.

## Aims
### A1 · 📐 What you keep, and what gets rebuilt
- A1.1 · A rebuild never touches the list you wrote.
  **Done when:** Running a rebuild over a hand-written list leaves it exactly as it was.
- A1.2 · You can edit the list from the tab: add, remove, put back, and reorder.
  **Done when:** All four actions work from the tab, and nothing outside the tab writes the list.

### A2 · 🌍 Which files a line may point at
- A2.1 · A rebuild makes shortcuts from the list only, and deletes nothing it did not make.
  **Done when:** It creates one shortcut per live line and leaves every other file alone.
- A2.2 · A file outside the repo is refused, and so is a whole page folder.
  **Done when:** Both refusals happen on a test line, each showing its reason on the card.

### A3 · 🚧 Why a borrowed page never becomes a second page
- A3.1 · A board with borrowed pages still builds clean.
  **Done when:** A build and check show no ghost page and no duplicate-name warning.

### A4 · 🔍 The list fills itself; you put it in order
- A4.1 · The machine reads which pages this page names, and how often, and suggests them.
  **Done when:** One click fills the list, in that order, with nobody reading the page by hand.
- A4.2 · You can ask which pages anywhere have a given kind of folder.
  **Done when:** One search returns files from more than one board in a single list.
- A4.3 · A suggested page shows how settled it is.
  **Done when:** Its badge changes after that page's own status line changes.

### A5 · 🗂 What of a page you use, and what you do not
- A5.1 · A card shows which parts of a page you use, and takes an unused part in one click.
  **Done when:** Each card reads `using N of M` over that page's folder, with ＋ use on every part you left.

### A6 · 🚪 Opening a borrow, and getting back
- A6.1 · Going into a borrow is never a one-way door.
  **Done when:** The framed page has ☰ back to the cards and ← → across your list, in your order.

### A8 · 🔗 What the card and the folder row must admit
- A8.1 · Opening a borrow lands on the readable page, not the raw file.
  **Done when:** A card's title opens the rendered page, and the raw file is a second, smaller door.
- A8.2 · The tab groups borrows by source page, each file opens, and a dead one says so.
  **Done when:** All three are seen on one page holding a live borrow and a broken one.
- A8.3 · This folder is never marked out of date, because a shortcut cannot fall behind.
  **Done when:** A page with shortcuts shows an age and no stale mark in the 📂 tab.
- A8.4 · A borrowed file always reads as a shortcut, never as a copy.
  **Done when:** The 📂 tab names the shortcut's target on the row, so nobody has to ask.

## States
This page is the plugin's first user.
Its own folder holds a four-line list and four live shortcuts, so everything below is read off real borrows and not a test.

### 🗣 Decision Now
- [ ] 🗣 Does a seed ever go DEEPER than the named page's own `.md`?
      📍 `Part` §4, the seeding
      🔔 `Why now` the ask that opened this page was about reusing a component or a display from inside another page, and a seed that stops at the page md never reaches one
      ⭐ `A ·` stay shallow. A suggestion takes the named page's own file, and anything deeper is added with the ＋ button. The writing named a PAGE, not a file inside it, so nothing is guessed.
      `B ·` also suggest a page's own working files, its skill list and its drawing. A named page then arrives with the parts a builder reuses, but the machine is choosing what you meant.
      `C ·` seed shallow, then offer a one-click "go deeper" on the card: no dropdown and no note, just the named page's files listed under it once you ask
      🛑 `Blocks` nothing; the pen already reaches any file, and §5's ＋ use reaches a whole folder
      🤖 `If nobody answers` A. That is what shipped.

### A1 · 📐 What you keep, and what gets rebuilt
- ✅ A1.1 · Done. A rebuild over the four-line list left it byte for byte the same.
- ✅ A1.2 · Done. All four actions work, and the list proves it: the lines stand QPf10 · QPs1 · QPf1 · QPf3 while their notes still read 9× · 16× · 7× · 4×, an order only a person could have made.

### A2 · 🌍 Which files a line may point at
- ✅ A2.1 · Done. Four lines, four shortcuts, and nothing else in the folder moved: the rebuild removes only shortcuts it made.
- ✅ A2.2 · Done. Both refusals reach the card. A file outside the repo and a whole folder each end as a refused line with its reason.

### A3 · 🚧 Why a borrowed page never becomes a second page
- ✅ A3.1 · Done. The four borrowed pages stay invisible to the page hunt, and the built board holds 16 QPf pages with no `QPs1` among them.

### A4 · 🔍 The list fills itself; you put it in order
- ✅ A4.1 · Done. One click wrote all four lines and built all four shortcuts, with nothing typed. Each line still carries the count from that day.
- ❄️ A4.2 · On ice, not done. The repo-wide search went out with the picker it lived in, and the ＋ button covers reaching other boards for now. Killing the goal outright is a change of purpose and needs its own round.
- ✅ A4.3 · Done. Each card reads its source page's status when the shortcut is built, so QPs1 shows `🟡 REOPENED` beside two `✅ SETTLED` and one `🟡 PARTIAL`.

### A5 · 🗂 What of a page you use, and what you do not
- ✅ A5.1 · Done on all four borrows. QPf3-slide reads `using 1 of 7`, and every part left carries ＋ use, which takes that folder in one click.

### A6 · 🚪 Opening a borrow, and getting back
- ✅ A6.1 · Done. The borrowed page opens framed, with ☰ back to the cards, ← → across your list, and a way to open it on its own.

### A8 · 🔗 What the card and the folder row must admit
- 🔨 A8.1 · Half done. The title opens the readable page, but the raw file lost its door when the inventory replaced the old fold.
- 🔨 A8.2 · Half done. Cards are grouped by page and a dead one says `⚠ dangling`, but a file row under a card opens nothing today.
- ✅ A8.3 · Done. The 📂 tab shows this folder with an age and no stale mark.
- ✅ A8.4 · Done. Every shortcut row carries a 🔗 with its target on hover, so a borrowed file is never counted as this page's own bytes.

## Files
### ⚙️ Engines
- `../../board/haipipe-board/live/pagex.py`
  The whole plugin: the store reader and writer, the minter and its vet, the prose scan, the three POST doors, the framed viewer, and the card view with its inventory.
- `../../board/haipipe-board/assets/js/10-drawer/85-plugin-pagex.js`
  The registry entry whose `tab` spec the shell builds the 🔗 tab from.
- `../../board/haipipe-board/live/folderstat.py`
  The 📂 tab: where pagex/ is kept out of the DERIVED set, and where a symlink row gets its 🔗 mark.
- `../../board/haipipe-board/live/skillmap.py`
  The skill twin, whose store grammar, drag route, and view shape pagex adopts rather than reinvents.

### 📋 Contracts
- `../../board/haipipe-plugin/ref/roster.md`
  The one list of plugin names; the `pagex/` row there is what this page rules.
- `../../board/page-plugins/haipipe-plugin-pagex/SKILL.md`
  The plugin's own delta-only skill, shipped with the row when it went 🟢.

### 🧪 Evidence
- `pagex/QPf11-pagex.md`
  This page's own borrow list: four scan-seeded rows, each naming a source page's own md, in the rank a person dragged them into.

### 🧪 Checks
- `../../board/haipipe-board/src/common.py`
  `_page_home` and `_in_plugin`: the discovery walk that would surface a borrowed page as a ghost, and where §3's boundary is tested.

## Law
- 🏷 The name is `pagex/`, bibex's twin (JL 260816).
- 🌍 The reach is the whole repo, not one board (JL 260816); the refresh vets every target under the repo root.
- 📄 Pagex links FILES, never a page's home folder: the minter and the pen each refuse a folder, so the one shape that could hand discovery a page home never gets made.
- ✂️ The scan SEEDS, the person RANKS (JL 260816: "I don't think the filter should be there, it should not be manually added"): `QPf10`'s law adopted whole: a refresh borrows every page this page's prose names, appends it at the bottom, and never edits, reorders, or re-seeds a row; the ＋-by-path pen is for depth, not for the common case, and its note is optional.
      This overturns CC's own rule from the same day, which had asked a person to type by hand what the page already said.
- 🧭 A minted link keeps the source page's INNER path (`pagex/<source-stem>/<inner path>`): a flat layout collides the moment two files come from one page, since QPs1's page md and its skill list both sit under the basename `QPs1-overall.md`.
- 🗃 The store is the only truth: symlinks and the view are re-minted from it, and a refresh never edits, reorders, or removes a row a person wrote.

## Log
- 260816 · [REVISE-CC] the page was a build round behind its own folder, so this pass read the shipped engine and the store on disk before touching a line, and then brought every affected claim to what is actually there. The store holds FOUR rows, all four a source page's own md, and `pagex/` holds four links at four `../`; there is no `skill/` segment and no skill-list borrow anywhere on disk, so the old §7 "first worked borrow" was still describing the paper specimen at five `../`, and §1's example path carried the same phantom `skill/` segment. §7 is rewritten from the four real rows, and it now says the thing the store actually proves: the rank reads QPf10 · QPs1 · QPf1 · QPf3 while the seed notes read 9× · 16× · 7× · 4×, so a person's drag is sitting on top of the machine's count. Every A1 to A3 state said "two rows" or "two links" against A4.1's four, and all of them are restated against the four-row store. §8 was added for the surface the cards and the 📂 row actually show, since four Aims ruled behaviours no division established once §5 and §6 took the inventory and the door; P0 to P3 became A8.1 to A8.4, P4 became A5.1, and P5 became A6.1, with no promise changed. A1.2 still promised the picker JL threw out and its state cited a note-less refusal that `live/pagex.py` calls OPTIONAL in the pen's own docstring, so the aim now names the ＋-by-path pen and the state names the routes that write the store. A4.2 is ❄️ on ice on JL's ruling, not retired: an aim dies in DRAFT, not here. The head state dropped from ✅ SETTLED to 🟡, because a page is not settled while an unanswered Decision Now sits in its States and an aim is held. Two aims came off ✅ on inspection rather than on request: the card lost its raw-file door when the `where` fold gave way to the inventory (A8.1), and a per-file row under a card is now plain code beside a ✕ and opens nothing (A8.2), so both promises are half on the surface. Three smaller corrections: `live/pagex.py` has THREE POST doors and one finding route, not the four and two Files claimed; §3 now says what `_in_plugin` does, which is to stop at the `pagex` segment before anything below it is read, instead of claiming a directory link would walk discovery in; and the `skill/` recount was written the wrong way round twice, since the number that matters is that 16 pages carry a `skill/` list, and the larger count of folders merely NAMED `skill/` sits on this board too, so `repo-wide` was never the right qualifier for it.
- 260816 · [RULE-JL] the card became a page's INVENTORY, and the door got a way back. JL asked for both in one breath: "我点进去之后，怎么退回来呢？我进去之后好像没法退回来了" and "每一个 page folder 我们用了它的哪些 information … 这个 sub-folder 用了，那个 sub-folder 没有用之类的？". The first was mine to answer plainly: the title had been a bare link, so the frame filled with a full board page and offered no exit; `/_board/pagexview` now frames it under ← ☰ →, walking the borrows in ranked order, which is the two-depth shape the skill map already ships. The second changed what a card IS. One card per SOURCE PAGE now, not per borrowed file, carrying that page's whole folder with the used part ticked and `using N of M` on the summary; QPf3-slide reads `using 1 of 7`. A list of what was taken cannot distinguish a deliberate one-file borrow from a page nobody opened, and the unticked rows turn that reading into an action: ＋ use takes a folder's files in one click, no dropdown and no typing, since §4's picker ruling binds here too. The pen learned to take a batch so one ✕ drops a whole page and one ＋ takes a whole folder.
- 260816 · [RULE-JL] two surface defects, both mine, both about respecting what a person came for. First, a borrow opened as RAW MARKDOWN (JL: "when I open them, why not the page in the board, but the raw markdown????"): the card linked the served file, but a page is taken to be READ, and reading happens on the rendered board page with its prose, its comments, and its rail. A borrow that is a page md now resolves to `board/<group>/<stem>.html` by walking up for board.md, and the raw file dropped to a small link inside the `where` fold. Second, the 📂 row was unreadable (JL: "very ugly"): my link mark had printed the whole repo path inline, and since the row is a flex line the filename was crushed to nothing while the path wrapped over three lines. The mark is now a bare 🔗 with the full target on hover, shown only when the link's place differs from its target, which for pagex is almost never. On the card the same path went into a fold, leaving the source page's name, its live state, and the borrowed file on stage.
- 260816 · [RULE-JL] the filter came out and the scan took over (JL, on the first screenshot of the 🔗 tab: "I don't think the filter should be there, it should not be manually added"). The shipped surface had made a person choose a page, open a dropdown of its files, type a reason, and press ＋ borrow, three manual gates where `QPf10` already rules ONE, namely that the scan seeds and the person ranks. A refresh now borrows every page this page's prose names, appending at the bottom with a `scan-seeded` note carrying that id and its count; the note-required gate CC had invented the same morning is gone, and the ＋-by-path pen folded shut as the depth door. Proven against an emptied store: one click seeded QPs1 16× · QPf10 9× · QPf1 7× · QPf3 4× and minted four links with nothing typed. The shape query retired with the filter it lived in (A4.2), leaving the pen as the cross-board reach. Same round, JL's second question exposed a surface that was quietly contradicting the plugin's whole claim: "are they copied or are they the symlink?" The 📂 tab reported each borrowed file's RESOLVED size, so a link read as 13KB of duplicated bytes, and `folderstat.py` now prints a link mark on a symlink row (then P3, now A8.4).
- 260816 · [BUILD-CC] the plugin shipped whole on JL's word ("那你就给我 work 到一直能 work 为止"), and this page became its first consumer: `live/pagex.py` with four doors, `85-plugin-pagex.js` for the 🔗 tab, the roster row 📋 → 🟢, and `haipipe-plugin-pagex` beside it, since a row going live brings its skill with it. The specimen designed on paper became links on disk, but not the ones it drew: the seeder borrows each named page's own md, so the skill-list row the design used as its worked example was never written, and the minter's depth came out at four `../` rather than the five the design predicted. Three things the build corrected in the design: the pen's field had to become `borrow`, because every view merges the board context `{path, file}` into its POST body and a borrow sent as `path` is silently overwritten by the board's own path (caught before the first click); the shape query had to group by BOARD and disclose its cap, because one `draw/` run returned 81 candidates across two boards and a bare page stem cannot say which one it came from; and the minter's safety rule was written as "only ever unlink a SYMLINK", then proven by leaving a hand-written file in `pagex/` through a re-mint. The riskiest boundary case was tested rather than reasoned about: borrowing a page's OWN md, then rebuilding, gave no ghost page and no duplicate-basename warning.
- 260816 · [REVISE-CC] structure and truth pass under the same purpose and Aims: the `state:` line took a legal 🔴 token, `## States` was rebuilt to mirror all ten Aim ids at ⬜, `## Files` moved above `## Law`, the Aims groups took their divisions' numbers, names, and emoji in order (the boundary aim became A3.1 and the two surface aims became P1 and P2), the checkboxes gave way to plain ids with a `Done when` line each, and the four board-skill citations lost one `../` and now resolve to files that exist. Two claims failed verification and were corrected: 16 pages on this board carry a `skill/` list, which is the count §4 needed, and QPs1 was not alone at 🟡, since QPf3 is PARTIAL while QPf10 and QPf1 are SETTLED. §2's minting rule became a contract instead of a running fact, the specimen division was captioned as designed rather than built because no pagex/ folder or symlink was on disk yet, each division gained a captioned face figure, and the Opening question, five em-dashes, two whole-line bold sentences, and the Chinese note row were rewritten.
- 260816 · [DRAFT-CC] the finding got its contract (JL: "我们怎么知道，比如说我们是需要这一个配置还是那一个配置？它会通过什么方法去做这个搜寻呢？"): the first two drafts specified the ROW and never how a row is found, and with 16 pages on this board carrying a `skill/` list browsing is no method at all. §4 now carries two routes for two starting points: the prose scan, ranked by mention count, which reaches inside this board only, and the shape query, folderstat widened to the tree, which is the only one that crosses boards, plus the source page's live state on every candidate. That last one was not designed but observed: scanning QPf11 put QPs1 far ahead of QPf10, QPf3, and QPf1, and reading their heads showed QPs1 reopened that same day, so the most-wanted borrow was the least settled. A4 opened with three aims and the Law took the note-required line; CC decided it, because nothing stopped on it.
- 260816 · [DRAFT-CC] the first worked borrow (JL: "我们可能会引用这个 skill 配置来帮我们给现在这个 QPf11，你觉得该怎么引用呢?"): QPs1-overall's skill list became the specimen row in the worked-borrow division, and it refined the contract twice: the minted link now keeps the source's inner path (QPs1's page md and skill list share a basename, so the flat layout of the first draft collides), and the pagex-vs-skill-pen line was drawn, since pagex borrows to READ while seeding QPf11's own list is the skill plugin's door.
- 260816 · [DRAFT-CC] page born from JL's ask ("我想有这样一个 plugin，能把需要引用的这些 pages 给组织起来… 按需引用… 可以用软链接"): the third citation twin, file-level borrowing materialized as symlinks. JL ruled the name `pagex/` over `use/` and `pages/`, and the reach repo-wide over same-board, in the same session; CC's boundary read of `_in_plugin` (src/common.py:207) grounded the never-link-a-page-home law. Roster row added as 📋 declared.

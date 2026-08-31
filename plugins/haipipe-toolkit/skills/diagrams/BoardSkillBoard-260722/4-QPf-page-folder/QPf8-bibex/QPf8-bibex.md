# Bibex · the page's own bib, worked through a citation workbench
state: 🟡 PARTIAL · store, workbench, three doors shipped · open: real ✓, browser click, paper bib, checker
owner: JL
method: give each page its own .bib, filled by copying from the paper's 0-*.bib, and worked through cards that show status and links and take a person's ✓ or pasted entry
session: da839d44-de6a-4874-a8d1-11e93495056c

## Opening
Where does a page keep its references, and how does a person work on them?
They live in the page's own `bibex/<stem>.bib`, copied in from the paper's `0-*.bib`, which is never written back to.
The 📚 tab is a workbench over that file, and every entry shows as a card.
A card carries its Scholar, DOI, and URL links, beside a mark only a person may tick.
The machine never writes a reference itself; it only copies whole entries and lands what a person pastes.

**What a person gets on one card**: the title, authors, and year, read out of the entry.
🔎 a Google Scholar search built from the title, and 🔗 DOI and 📄 URL when the entry carries them.
✅ checked, with who and when, or ⬜ unchecked, with the ✓ button beside it.
The raw bibtex sits behind an ✎ edit fold, which is where an entry is fixed or a new one pasted in.

**Covered elsewhere**: `QPf1` rules the folder, and the roster row is `../../board/haipipe-plugin/ref/roster.md`.
The siblings are `QPf6` (latex) and `QPf7` (word).
`QPf6`'s Decision row rules what git does with the rebuilt files, while the page bib itself is always committed.
The live law comes from `../../board/page-plugins/haipipe-plugin-bibex/SKILL.md`.

## Diagram
**The page bib is the truth, and three doors work it**: ↻ copies cited entries in, ✓ writes a person's check into the entry, and ✎ lands a person's pasted bibtex.
```text
  📄 <page>/<stem>.md ── cite keys (code fences stripped) ──▶ the KEYS
        ▼
  🗃 bibex/<stem>.bib      PRIMARY · the page's OWN store
        ▲ seeded           entries copied whole from the paper's 0-*.bib
        ▲ refresh          appends only, never overwrites, never deletes
        │
  three doors, one truth
    ↻ /_board/bibex          re-scan keys · seed-import · re-render the view
    ✓ /_board/bibex-verify   writes verified = {WHO YYMMDD} INTO the entry
    ✎ /_board/bibex-entry    lands a PERSON's pasted bibtex, verbatim
        │
        ▼
  🖼 bibex/<stem>-bib.html   DERIVED · the card view the 📚 tab frames
```

## Content
### 1 · One file is yours, the rest is rebuilt
**A MIXED plugin, like display/**: one file a person rules, and files a rebuild may replace.
```text
  <page>/bibex/
    <stem>.bib         🧑 PRIMARY · the page's citation store · committed
                          header says: edits welcome, refresh only APPENDS
    <stem>-bib.html    ⚙️ DERIVED · the workbench view, regenerated freely
    .board-refs.bbl    ⚙️ DERIVED · the formatted references, for the word export
  flat page fallback: <board>/bibex/
```
📌 The page's `.bib` is yours to write and is never overwritten, while the card view and the formatted references are rebuilt for you at any time.
The `.board-refs.bbl` comes from no door at all: the word export runs `cli/refs.py` over this bib whenever the bib is newer, so the .docx prints the in-text labels and the References list.
Filling looks a cited key up in the paper's `0-*.bib`, searching upward, and copies the whole entry into the page bib.
The paper file is read and never written.
A refresh scans the page's keys again, brings in what can now be found, and draws the view again.
An entry already in the page bib is never overwritten and never deleted, because a person may have edited it.
An entry no longer cited on the page stays, marked `not cited on this page`, so cutting a sentence never quietly drops its source.
A cite inside a code fence or backticks is stripped before the scan, because a figure showing the syntax is a picture, not a citation.

### 2 · What a person can do to an entry, and what the machine may not
**What a person does on a card**: check, mark, fix, add.
```text
  ✅ checked · JL 260815  [undo]     the tick writes verified = {JL 260815}
  ⬜ unchecked  [✓ I checked this]    INTO the entry · travels with it,
                                      no sidecar to drift
  🔎 Scholar · 🔗 DOI · 📄 URL        the links the checking happens through
  ▸ raw bibtex · ✎ edit → [save]     fix a field, replace in place
  🔴 missing key → 🔎 Scholar →       find it, paste its bibtex, it lands
     [📋 paste] → done                 verbatim in the page bib
  ＋ add a citation                    same pen, for uncited sources
```
📌 A person ticks, fixes, and pastes, and the machine only copies text whole and never writes a reference itself.
The ✓ answers one question: did I check this link myself?
Nobody but a person clicks it, the field records who and when, and undo takes it away.
The edit buttons check the shape only, one balanced entry with a key.
They refuse a repeated key unless the save says outright that it replaces the old one.
They never write, finish, or fix the text itself, and that is the line between a pen and an author.
The ＋ box also takes a LINK: a DOI, an arXiv link, Scholar's Cite to BibTeX link, or a paper URL.
The bibtex is then fetched WHOLE from that source into the box.
Fetching is copying, so the fetched text sits in the box for review, and landing it stays the person's second click.
A fetched key you cannot use, such as doi.org's URL-as-key, is renamed to surname plus year by rule, because a key is a local handle and not information about the paper.
The whole raw `.bib` opens right below the cards, with its path printed.
The file is the person's, and editing it by hand is allowed.
This page's own file holds one entry, JL's KDD paper \citep{luo2026eventglucose}.
It is cited here so the page draws the inline link and the References block that the binding makes.

### 3 · How the tab gets on screen
**The 📚 tab**: framed the way the slide tab is, from a registry entry, a HEAD probe, and an iframe, with the view carrying its own buttons.
```text
  82-plugin-exports.js ──POST──▶ /_board/bibex ──▶ refresh + view
  tab.url()  names bibex/<stem>-bib.html · HEAD hit ▶ frame it
  the view's own buttons POST bibex-verify / bibex-entry, then reload
  clicking the 📚 tab while it is open ▶ the refresh door again
```
📌 The 📚 tab frames a page the server wrote, and the buttons inside that page talk to the server on their own.
Clicking a tab that is already open rebuilds what that tab shows, so the second click on 📚 is the refresh: it draws the view again and appends any import the paper bib can now resolve, and it touches no entry already there.

## Aims
### A1 · 🗃 One file is yours, the rest is rebuilt
- ✅ A1.1 · The page owns its file, copying fills it, and a refresh is safe.
  **Done when:** a page has its own `bibex/<stem>.bib`, a cited key the paper's `0-*.bib` can find arrives in it by copy, and a repeat refresh changes no entry already there.
  **Now:** Shipped as haipipe-board 0.129.0 and tested end to end 260815 on a made-up paper: the copy brought an upstream entry in whole, a second refresh brought in nothing, and a person's added entry came through untouched.
- ⬜ A1.2 · One page inside a real paper lives on its filled bib.
  **Done when:** a page that cites sources has copied entries beside at least one a person pasted, and the upstream `0-*.bib` comes out of the whole round byte for byte the same.
  **Now:** No page in a real paper has lived on its filled bib yet.

### A2 · 🧑 What a person can do to an entry, and what the machine may not
- ✅ A2.1 · A card shows the entry, and the routes carry a person's four actions to the file.
  **Done when:** a card shows its read-out fields beside its links and its status, and the routes carry four actions through to the file: a tick, an undo, a word-for-word paste, and a refused repeat key.
  **Now:** Shipped 260815 and run through the routes: read-out fields, Scholar/DOI/URL links, the verified field written and undone, word-for-word landing, and replace-only overwrite.
- 🧠 A2.2 · The first REAL checked entry is JL's.
  **Done when:** an entry carries `verified = {JL …}` because JL opened its link and clicked ✓, and not because a machine or a demo wrote it.
  **Now:** Held until the record can be traced: `../QPf4-chat/bibex/QPf4-chat.bib:12` carries `verified = {JL 260815}`, but a field cannot show whose click wrote it, and this page's Log records a machine writing that same field once, so only JL's own dated note of the tick closes this.
- ✅ A2.3 · The ＋ box turns links into bibtex, and the raw file is one fold away.
  **Done when:** each of the four accepted link shapes returns bibtex into the box for review, a link outside them is refused with those four shapes named rather than guessed at, and the whole `.bib` can be read from the view with its path on disk.
  **Now:** Shipped 260815 and tested over the network against all four shapes, each fetch landing in the box and not in the file: `_resolve_bib_link` refuses anything else by naming them, and the view's last fold prints the whole `.bib` with its path.

### A3 · 🖼 How the tab gets on screen
- ✅ A3.1 · The 📚 tab frames the view, and the view draws everything a person needs.
  **Done when:** the 📚 tab frames `bibex/<stem>-bib.html`, and that page shows a card, its status chip, its links, its edit fold, the add box, and the refresh button.
  **Now:** Shipped 260815 and checked against a screenshot: a real entry's card, its status chip, its links, its edit fold, the add box, and the refresh button.
- 🧠 A3.2 · One workbench action is clicked in a real browser.
  **Done when:** a person clicks add and ✓ on the view's own buttons in a live browser, and the POSTs and the reload carry the change through to the file.
  **Now:** Held on the same write A2.2 is held on: `../QPf4-chat/bibex/QPf4-chat.bib:12` carries `verified = {JL 260815}`, and a field cannot show that a person's browser click wrote it, so a browser-side artifact closes this, a screenshot of the click or a server access log for the two POSTs, the way a screenshot closed A3.1.

### P · 🚧 The boundary
- ⬜ P1 · `bibex/` joins the checker's list of known plugin folders.
  **Done when:** `check.py` knows `bibex/` as a plugin folder by name and warns on nothing inside it.
  **Now:** `check.py` does not yet know `bibex/` by name.


## Discussion

### From the retired States section (merged 260831)
The file and the workbench are built, and every route is tested.
What is left is a ✓ that can be traced to a person, a click that can be traced to a real browser, a real paper page living on its filled bib, and the checker boundary.

## Law
- 🗃 The page owns its bib; the paper's is read-only here (JL 260815: "the bib for this page only")
      Filling copies whole entries out of the paper's `0-*.bib`, and nothing this plugin does ever writes that file.
- ✂️ The pen, never the author, inherited from the Bibex plugin contract
      The machine lands a person's pasted text word for word, or copies an upstream entry whole.
      It writes, finishes, and fixes no entry, and a missing key is reported rather than guessed at.
- 🧑 The ✓ is a person's
      `verified` records that a person opened the link and checked it.
      No machine may write it, and the one demo tick that did was taken back the same hour.

## Files
### ⚙️ Engines
- `../../board/haipipe-board/live/export.py`
  All three doors and the view: `_bibex_state`, `export_bibex`, `bibex_verify`, `bibex_entry`, `_bibex_view`.
- `../../board/haipipe-board/assets/js/10-drawer/82-plugin-exports.js`
  The registry entry whose `tab` spec the shell builds the 📚 tab from.
- `../../board/haipipe-board/live/shell.py`
  The tab strip that frames the view: `d.tab.url(page)`, the HEAD probe, then `landFrame`, and the rebuild a second click on an open tab runs.
- `../../board/haipipe-board/cli/refs.py`
  What the word export runs to compile `.board-refs.bbl` in `bibex/`; it is the only writer of the third file §1 lists.

### 📋 Contracts
- `../../board/page-plugins/haipipe-plugin-bibex/SKILL.md`
  The live Bibex law; if the two disagree, that contract wins and this design Page is the defect.

### 🧑 What a person rules
- `bibex/QPf8-bibex.bib`
  This page's own file, holding the one entry §2 cites, `luo2026eventglucose`; it carries no `verified` field, so the ✓ here is still JL's to click.

## Log
- 🚢 260831 · [HAIPIPE-PAGE-SKILL, JL ruled] the 📚 strip row folded into the 🧾 Evidence tab as the Citations segment (QPf15); the workbench, its pens and the verified: gate unchanged. Also agreed direction: bibex may carry its own SIMPLE code (dedup/format) under the coming code-lane law.
- 260816 · [REVISE-CC] JL's second hold lands, and four factual findings are worked; the plain wording stays as it was rewritten.
      A3.2 goes to 🧠, held, because it and A2.2 close on the SAME write, `../QPf4-chat/bibex/QPf4-chat.bib:12`'s `verified = {JL 260815}`.
      This page already rules that write inadmissible for A2.2, a field cannot show whose click wrote it and the Log records a machine writing that field once, so reading it as conclusive for A3.2 made one write mean two things.
      Under-claiming beats over-claiming, so the row names what closes it, a browser-side artifact such as a screenshot or a server access log, which is how A3.1 closed.
      The `open:` list and the States intro carry four items now instead of three, and the `state:` line stays under 110 characters.
      §1 listed two files where `bibex/` holds three on disk: `.board-refs.bbl` sits beside them, and no door writes it.
      `live/export.py`'s `export_word` compiles it through `cli/refs.py` whenever the bib is newer, and haipipe-board 0.132.0 records why; the row is marked DERIVED and one sentence names the export as its writer.
      A1.1, A2.1, A2.3 and A3.1 each ended in a dated shipped sentence, so history and current fact both sat in Aims while States said the same thing in other words; the shipped sentence moved into each State row and the Aim keeps its target and its `Done when`.
      A1.1, A2.1 and A3.1 were also TITLED as accomplishments, "… shipped", where an Aim states a target the way A1.2, A2.2 and A3.2 do; each is re-titled in the present tense its own `Done when` already tests.
      The Diagram caption promised three doors and listed two of them merged plus the view, which the same figure marks DERIVED, so it now names ↻, ✓ and ✎, the three the figure draws.
      §3 used `lit-click`, a word no Glossary on this page defines: clicking a tab that is already open rebuilds what the tab shows, so the second click on 📚 is the refresh, and the sentence says that plainly.
      The refresh is not view-only, which the old fence row implied: `export.py`'s `export_bibex` appends a newly resolvable import and touches no entry already there, and the 📌 line now says both halves.
      The Opening lost one sentence to come back under the 520-character ceiling; the editor it named is now in the drawer's card list, where the ✎ fold is already described.
- 📖 260816 · [REVISE-CC, JL ruled] the page was rewritten in plain words, for a reader with ADHD whose English is a second language (JL: "我真的读不下去"). The 🧭 Outline tab had been showing this page's own sentences back, and they were unreadable, so the tab was right and the prose was not. Every division title now names its consequence instead of a mechanism, each one gained a `📌` line saying in one sentence what the part settles, and every aim, `Done when:` and State row was replaced with a short plain-word version. House words went with them, `division` to part, `store` to list, `render` to read or draw, `seed` to suggest, `mint` to build. Measured with `haipipe-writing`'s `cli/score.py`: 15 sentences flagged before, 8 after, every one that remains inside this Log, which is history and was not touched. No fact, id, `§` mark or section changed; only the words.
- 260816 · [REVISE-CC] JL's ruling lands: A2.2 goes back to 🧠, held, and the second-round findings are worked.
      A2.2's ✅ stood on scope and not on provenance, so the Aim is held rather than met.
      Its `Done when` decides on who wrote the field, "because JL opened its link and clicked ✓, not because a machine or a demo wrote it", and `../QPf4-chat/bibex/QPf4-chat.bib:12` shows the field and not the hand.
      That is the one thing the Aim exists to exclude, and this page's own Law and Log already record a machine writing that exact field once.
      The State row now waits on a citable human record and names it, JL's own dated note of the tick, and the page-level `open:` list carries it again.
      Under-claiming beats over-claiming, so the record below, which read that same field as satisfying the `Done when` as written, is superseded here.
      The §1 fence attributed the flat page fallback to `deck.py`, which no longer exists: `skills/board/CHANGELOG.md:26` retires `live/deck.py` with the slide variant, and the folder holds `autodeck.py` instead.
      Re-attributing the row to `autodeck.py` would have been a second false claim, because `autodeck.py` refuses a flat page outright rather than falling back to a board-level folder; the fork this row means lives in `export.py`'s own `_export_target`.
      The attribution is dropped and the row is a label and its value again.
      §2 no longer dates its own store: the sentence states what is there now, one entry, JL's KDD paper, cited so the render produces the inline link and the References block.
      The claim that it "landed through the pen on 260815" is not relocated into this Log either, because nothing on disk shows how it arrived; the file carries no `%% seeded` line, which proves only that no seed-import wrote it.
      The same unprovable clause sat in the Files row and went with it.
      The rest is shape.
      The Aims dropped their checkboxes, which the engine reads as the legacy form that exempts a page from Aim-to-State mirroring, so the ids now drive the count and each Aim row takes its emoji from States.
      A1.1, A2.1, A2.3 and A3.1 gained the `Done when` they lacked, keeping their shipped notes as the evidence sentence beneath it.
      The Diagram caption ends at what the figure draws, and §1 keeps the backticks rule the figure never held.
      `### 🧪 Evidence` became `### 🧑 What a person rules`, because 🧪 is the menu's mark for Checks and that row is the plugin's primary person-owned store.
      A2.3's State row states the on-disk fact instead of repeating its Aim, and A3.2's row stopped naming who clicked, since the file it cites cannot show that either.
- 260816 · [REVISE-CC] a findings pass read against disk: A2.2 marked met, A2.3 given the State row it never had, and the bib's "empty and honest" line retired.
      `../QPf4-chat/bibex/QPf4-chat.bib` really carries JL's `verified = {JL 260815}` inside the entry, so A2.2's own `Done when` is satisfied as written and its State now says where that tick lives; this page's own store holds `luo2026eventglucose` with no tick at all, which is what the Files evidence row says instead of calling the file empty. The page-level `open:` list follows the two Aims still open, A1.2 and P1.
      The rest was shape. The A2 rows are back in id order, A3.2's `Done when` is a target again with its 15:13 and 15:15 evidence kept in States, two wrapped clauses left the Diagram fence for its caption, §3's caption names the registry entry, the HEAD probe, and the iframe instead of a coined phrase, one four-clause sentence in §2 was split, and `live/shell.py` was added to Engines because that caption now cites it.
- 260815 1900 · [JL via CC] `haipipe-plugin-bibex` drafted under `page-plugins/`, round 2 of the thin-door migration: delta-only over `haipipe-plugin`.
- 260815 · [REVISE-CC] the ＋ box learned links on JL's ask ("could we paste the paper link"): four resolvers fetch bibtex whole from the source into the box for review, an unusable fetched key is renamed surname+year, the un-cited chip gained 📋 copy-`\citep{key}` after "not synced" confusion, and the raw `.bib` gained its own fold with the on-disk path ("how could I see the raw files").
- 260815 · [RULE-JL] the write target is the PAGE's own bib, not the paper's and not a board-level one; the workbench built the same hour: status cards with Scholar/DOI/URL links, the ✓ as a `verified` field inside the entry (JL picked the field over a sidecar), the pen for pasted entries, and the code-fence strip that keeps figure syntax out of the key scan. The demo entry and its machine-written tick were reverted so A2.2 stays a person's.
- 260815 · [DRAFT-CC] page born in the plugin round as the extract-only subset; superseded the same day by the page-owned-bib ruling above, which keeps extraction as the SEEDING half.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0
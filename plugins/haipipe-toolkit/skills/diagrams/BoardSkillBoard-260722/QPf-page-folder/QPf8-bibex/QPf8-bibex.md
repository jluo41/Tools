# Bibex · the page's own bib, worked through a citation workbench
state: 🟡 PARTIAL · store, workbench, three doors shipped · open: a real paper's bib, checker boundary
owner: JL
method: give each page its own .bib, seed it by copying from the paper's 0-*.bib, and work it through cards that show status and links, take a person's ✓, and land a person's pasted entries
session: da839d44-de6a-4874-a8d1-11e93495056c

## Opening
Where does a page's bibliography live, and how does a person actually work it?
The bib is the page's own: `bibex/<stem>.bib`, seeded from the paper's `0-*.bib`, which is never written back.
The 📚 tab is a workbench over that store.
Every entry is a card carrying its Scholar, DOI, and URL links beside a checked-or-not status only a person may tick.
The same card opens into an editor for fixing an entry or pasting a new one in.
The machine composes nothing, keeping citation-craft's law whole.

**What the person gets per card**: the parsed title, authors, and year; 🔎 a Google Scholar search built from the title; 🔗 DOI and 📄 URL when the entry carries them; ✅ checked with who and when, or ⬜ unchecked with the ✓ button; and the raw bibtex behind an ✎ edit fold.
**Covered elsewhere**: `QPf1` rules the folder; the roster row is `../../board/haipipe-plugin/ref/roster.md`; the siblings are `QPf6` (latex) and `QPf7` (word), and `QPf6`'s Decision row rules git's treatment of the DERIVED files while the page bib itself is committed; the law's source is `S03-literature/citation-craft.md`.

## Diagram
**The page bib is the truth; three doors work it**: seeding copies entries in, a person ticks and pastes, the view only renders, and a key inside backticks is an illustration rather than a cite.
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
### 1 · The contract
**A MIXED plugin, like display/**: one primary file a person rules, derived files a rebuild may replace.
```text
  <page>/bibex/
    <stem>.bib         🧑 PRIMARY · the page's citation store · committed
                          header says: edits welcome, refresh only APPENDS
    <stem>-bib.html    ⚙️ DERIVED · the workbench view, regenerated freely
  flat page fallback: <board>/bibex/ · deck.py's own fork
```
Seeding resolves a cited key against the paper's `0-*.bib` upward and copies the entry whole into the page bib; the upstream file is read and never written.
A refresh re-scans the page's keys, imports what has become resolvable, and regenerates the view; an entry already in the page bib is never overwritten and never deleted, because a person may have edited it.
An entry no longer cited on the page stays, marked `not cited on this page`, so removing a sentence never silently drops its source.
A cite inside a code fence or backticks is stripped before scanning: a figure showing the syntax is an illustration, not a citation.

### 2 · The workbench
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
The ✓ is the page's answer to "did I check this link myself": nobody but a person clicks it, the field records who and when, and undo removes it.
The pen validates shape only, one balanced entry with a key, and refuses a duplicate key unless the save is an explicit replace; it never composes, completes, or corrects the text, which is the line between a pen and an author.
The ＋ box also takes a LINK: a DOI, an arXiv link, Scholar's Cite → BibTeX link, or a paper URL, and the bibtex is fetched WHOLE from that source into the box.
Fetching is copying, so the fetched text sits there for review and landing it stays the person's second click.
An unusable fetched key, such as doi.org's URL-as-key, is renamed to surname+year mechanically, because a key is a local handle and not metadata.
The whole raw `.bib` sits one fold from the cards, path printed, because the file is the person's and hand-editing it is legal.
The store's first lived entry is JL's own KDD paper \citep{luo2026eventglucose}, landed through the pen on 260815 and cited here so this very page renders the inline link and the References block the binding produces.

### 3 · The surface
**The 📚 tab**: framed the way the slide tab is, from a registry entry, a HEAD probe, and an iframe, with the view carrying its own controls.
```text
  82-plugin-exports.js ──POST──▶ /_board/bibex ──▶ refresh + view
  tab.url()  names bibex/<stem>-bib.html · HEAD hit ▶ frame it
  the view's buttons POST bibex-verify / bibex-entry themselves and
  reload · lit-click on the tab ▶ REFRESH, the derived half only
```

## Aims
### A1 · 🗃 The contract
- [x] A1.1 · The page-owned store, seeding, and safe refresh shipped.
      Shipped as haipipe-board 0.129.0 and lifecycle-tested: seed-import copied an upstream entry whole, a second refresh re-imported nothing, and a person's added entry survived it untouched.
- [ ] A1.2 · One page inside a real paper lives on its seeded bib.
      **Done when:** a cite-bearing page's bib carries seeded entries beside at least one person-pasted one, and the upstream `0-*.bib`'s bytes are unchanged by the whole round.

### A2 · 🧑 The workbench
- [x] A2.1 · The cards, links, tick, undo, pen, and duplicate guard shipped.
      Shipped 260815: parsed fields, Scholar/DOI/URL links, verified-field write and undo, verbatim landing, replace-only overwrite, all exercised through the routes.
- [x] A2.2 · The first REAL checked entry is JL's.
      **Done when:** an entry carries `verified = {JL …}` because JL opened its link and clicked ✓, not because a machine or a demo wrote it.
- [x] A2.3 · The ＋ box resolves links, and the raw file is one fold away.
      Shipped 260815 and network-tested against all four shapes: Scholar's cite link, doi.org content negotiation, arXiv's bibtex endpoint, and the Semantic Scholar URL fallback; the fetched text fills the box for review, and the whole `.bib` renders in a fold with its path.

### A3 · 🖼 The surface
- [x] A3.1 · The tab and view shipped; the view renders every affordance.
      Shipped 260815 and screenshot-verified: card, status chip, links, edit fold, add box, refresh.
- [x] A3.2 · One workbench action is clicked in a real browser.
      **Done when:** a person clicks add and ✓ on the view's own buttons in a live browser, and the POSTs and the reload carry the change through to the file.

### P · 🚧 The boundary
- [ ] P1 · `bibex/` joins the checker's known-plugin list.
      **Done when:** `check.py` names `bibex/` a known plugin folder and warns on nothing inside it.

## States
The store and the workbench are built, route-tested, and worked once by hand; what remains is a real paper page living on its seeded bib, and the checker boundary.
- ✅ A1.1 · Lifecycle-tested 260815 on a synthetic paper: seed, add, dup-guard, verify, undo, refresh-preserves.
- ⬜ A1.2 · No real paper page has lived on its seeded bib yet.
- ✅ A2.1 · Route-tested 260815; the verified field lands inside the entry and undo strips it clean.
- ✅ A2.2 · JL's own ✓ stands in `../QPf4-chat/bibex/QPf4-chat.bib`, whose entry carries `verified = {JL 260815}`; this page's own store is still unticked.
- ✅ A2.3 · Network-tested 260815 against all four link shapes, and the whole `.bib` renders in its fold with the on-disk path printed.
- ✅ A3.1 · View screenshot-verified 260815 with a real entry's card.
- ✅ A3.2 · JL's QPf4-chat add (260815 15:13) and ✓ (15:15) went through the view's own buttons in a live browser.
- ⬜ P1 · `check.py` does not yet know `bibex/` by name.

## Law
- 🗃 The page owns its bib; the paper's is read-only here (JL 260815: "the bib for this page only")
      Seeding copies entries whole out of the paper's `0-*.bib` and nothing this plugin does ever writes that file.
- ✂️ The pen, never the author, inherited from citation-craft.md
      The machine lands a person's pasted text verbatim or copies an upstream entry whole; it composes, completes, or corrects no entry, and a missing key is reported rather than guessed.
- 🧑 The ✓ is a person's
      `verified` records that a person opened the link and checked; no machine may write it, and the one demo tick that did was reverted the same hour.

## Files
### ⚙️ Engines
- `../../board/haipipe-board/live/export.py`
  All three doors and the view: `_bibex_state`, `export_bibex`, `bibex_verify`, `bibex_entry`, `_bibex_view`.
- `../../board/haipipe-board/assets/js/10-drawer/82-plugin-exports.js`
  The registry entry whose `tab` spec the shell builds the 📚 tab from.
- `../../board/haipipe-board/live/shell.py`
  The tab strip that frames the view: `d.tab.url(page)`, the HEAD probe, then `landFrame`.

### 📋 Contracts
- `../../paper/S03-literature/citation-craft.md`
  The law's source; if the two disagree, that file wins and this plugin is the defect.

### 🧪 Evidence
- `bibex/QPf8-bibex.bib`
  This page's own store, holding the one entry §2 cites, `luo2026eventglucose`, landed through the ✎ pen; it carries no `verified` field, because the ✓ here is still JL's to click.

## Log
- 260816 · [REVISE-CC] a findings pass read against disk: A2.2 marked met, A2.3 given the State row it never had, and the bib's "empty and honest" line retired.
      `../QPf4-chat/bibex/QPf4-chat.bib` really carries JL's `verified = {JL 260815}` inside the entry, so A2.2's own `Done when` is satisfied as written and its State now says where that tick lives; this page's own store holds `luo2026eventglucose` with no tick at all, which is what the Files evidence row says instead of calling the file empty. The page-level `open:` list follows the two Aims still open, A1.2 and P1.
      The rest was shape. The A2 rows are back in id order, A3.2's `Done when` is a target again with its 15:13 and 15:15 evidence kept in States, two wrapped clauses left the Diagram fence for its caption, §3's caption names the registry entry, the HEAD probe, and the iframe instead of a coined phrase, one four-clause sentence in §2 was split, and `live/shell.py` was added to Engines because that caption now cites it.
- 260815 1900 · [JL via CC] `haipipe-plugin-bibex` drafted under `page-plugins/`, round 2 of the thin-door migration: delta-only over `haipipe-plugin`.
- 260815 · [REVISE-CC] the ＋ box learned links on JL's ask ("could we paste the paper link"): four resolvers fetch bibtex whole from the source into the box for review, an unusable fetched key is renamed surname+year, the un-cited chip gained 📋 copy-`\citep{key}` after "not synced" confusion, and the raw `.bib` gained its own fold with the on-disk path ("how could I see the raw files").
- 260815 · [RULE-JL] the write target is the PAGE's own bib, not the paper's and not a board-level one; the workbench built the same hour: status cards with Scholar/DOI/URL links, the ✓ as a `verified` field inside the entry (JL picked the field over a sidecar), the pen for pasted entries, and the code-fence strip that keeps figure syntax out of the key scan. The demo entry and its machine-written tick were reverted so A2.2 stays a person's.
- 260815 · [DRAFT-CC] page born in the plugin round as the extract-only subset; superseded the same day by the page-owned-bib ruling above, which keeps extraction as the SEEDING half.

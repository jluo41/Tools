# Word · a coauthor .docx and the PDF twin the tab shows
state: 🟡 PARTIAL · the writer, the route, and the tab shipped in haipipe-board 0.128.0; the lanes question and the boundary are open
owner: CC
method: call md2docx by path for the .docx, render its PDF twin with docx2pdf's Chrome pass, and frame the twin because a browser cannot show a .docx

## Opening
Where does a page's Word export live, and what can a browser honestly show of it?
The `.docx` exists for one reader: a coauthor who marks up in Word and does not use LaTeX.
A browser frames no `.docx`, so the tab shows the PDF TWIN, rendered from the package itself so it shows what the file actually contains, and the real artifact is one ⬇ download away.
Both halves are DERIVED, land in the page's own `word/` folder, and regenerate on a click.

**Why the twin and not a converter**: `docx2pdf.py` reads the OOXML this family itself wrote, comments and all; macOS's `textutil` was measured dropping all 239 anchored comments, which for a file whose purpose is carrying evidence is a different document.
**Covered elsewhere**: `QPf1` rules the folder; the roster row is `../../board/haipipe-page-plugin/ref/roster.md`; the siblings are `QPf6` (latex, whose Decision row also rules this folder's git fate) and `QPf8` (bibex); the writer's own contract is `fn/to-word.md` in the paper family.

## Diagram
**One source, two artifacts, one honest frame**: the .docx for Word, the twin for the tab.
```text
  📄 <page>/<stem>.md
        │ POST /_board/word              live/export.py
        ▼
  🛠 md2docx.py ──▶ word/<stem>.docx     the ARTIFACT · anchored comments,
        │                                --paper-root when one is found
        ▼
  🖨 docx2pdf.py (Chrome headless) ──▶ word/<stem>.pdf   the TWIN
        ▼
  🖼 word/<stem>-view.html               what the 📝 tab frames:
     the twin inline + ⬇ download the .docx
     twin failure ▶ the view says so and keeps the download
```

## Content
### 1 · The contract
**What the folder holds**: three files, all derived, all regenerable.
```text
  <page>/word/
    <stem>.docx        ⚙️ md2docx's package · the thing a coauthor opens
    <stem>.pdf         ⚙️ the Chrome-rendered twin · what the tab frames
    <stem>-view.html   ⚙️ the tab's surface: twin inline + ⬇ download
  flat page fallback: <board>/word/ · deck.py's own fork
```
The tab never pretends to edit: a `.docx` has no live browser editor, so the surface is preview-and-download and says so, which is the trust rule the drawer pages already hold.
The bibliography prefers the PAGE'S OWN `bibex/<stem>.bib` (JL 260815, the same preference the latex plugin holds): `cli/refs.py` compiles its `.board-refs.bbl` and md2docx renders the in-text label and a References section from it, one store feeding chip, block, PDF, and .docx.
With no page store, `--paper-root` rides along when the upward walk finds one; outside a paper the export degrades rather than refuses.

### 2 · What rides in the comments
**The lanes**: the apparatus the LaTeX column drops survives here as anchored Word comments.
```text
  md2docx --lanes  defaults to Citation alone (JL 2026-07-27 line of the
                   paper family: three lanes are true, five comments per
                   sentence is unreadable)
  the board route  passes NO --lanes today, so the default rides
  open: does a BOARD page's export want the same default, or none?
```
The writer was built for S stage pages whose lanes are evidence audits; a board page's `>` lanes are conversation, and whether a coauthor wants them at all is A2's question, answered by handing one real export to one real reader.

### 3 · The surface
**The 📝 tab**: the Slides sandwich, third filling.
```text
  82-plugin-exports.js ──POST──▶ /_board/word ──runs──▶ md2docx + docx2pdf
  tab.url()  names word/<stem>-view.html · HEAD hit ▶ frame it
  tab.write() builds on miss · lit-click            ▶ REBUILD
  Chrome absent ▶ the view keeps the ⬇ and names the failure
```

## Aims
### A1 · 🧾 The contract
- [x] A1.1 · The route, the twin, and the view shipped.
      Shipped as haipipe-board 0.128.0: `QPf4b` produced a real `.docx` and an eight-page twin on 260815, with the failure path keeping the ⬇ download.

### A2 · 💬 What rides in the comments
- [ ] A2.1 · One export reaches one coauthor and the lane default is ruled from their markup.
      **Done when:** a board page's `.docx` has been read in Word by a person, and States records whether board exports keep Citation, carry nothing, or expose `--lanes` in the tab.

### A3 · 🖼 The surface
- [x] A3.1 · The 📝 tab shipped and was driven, not assumed.
      **Done when:** met 260815: the ➕ menu showed 📝 Word with its ● material dot in a driven browser, and opening it framed the view.

### P · 🚧 The boundary
- [ ] P1 · `word/` joins the checker's known-plugin list.
      **Done when:** `check.py` names `word/` a known plugin folder and warns on nothing inside it.

## States
The machinery is done and proven; the one design question left is about readers, not code.
- ✅ A1.1 · Built 260815: docx, twin, view, download, failure path.
- ⬜ A2.1 · No board export has reached a Word-holding reader yet; the paper default rides unexamined.
- ✅ A3.1 · Browser-verified 260815 through the driven CDP run.
- ⬜ P1 · `check.py` does not yet know `word/` by name.
- The git fate of this folder is ruled on `QPf6`'s Decision row, once for all three derived plugins.

## Files
### ⚙️ Engines
- `../../board/haipipe-board/live/export.py`
  The route's owner: the docx build, the twin render, the view page.
- `../../board/haipipe-board/assets/js/10-drawer/82-plugin-exports.js`
  The registry entry whose `tab` spec the shell builds the 📝 tab from.
- `../../paper/haipipe-paper/scripts/to-word/md2docx.py`
  The writer, called by path; its docstring and `fn/to-word.md` own the export rules.
- `../../paper/haipipe-paper/scripts/to-word/docx2pdf.py`
  The twin's renderer: OOXML read directly, comments printed in the margin, Chrome for the paged output.

### 🧪 Evidence
- `../QPf4b-chat-sdk/word/QPf4b-chat-sdk.docx`
  The first export, 260815, with its eight-page twin and view beside it.

## Log
- 260815 · [REVISE-CC] the export cites from the page-owned bibex store: refs.py compiles the bbl beside the bib, md2docx reads it, and QPf8's .docx is the proof, "(Luo et al. 2026)" inline with a References section; md2docx's bbl parser learned plainnat's bare labels on the way (a paper-family fix that benefits the paper path identically).
- 260815 · [DRAFT-CC] page born in the plugin round, after the build: A1 records haipipe-board 0.128.0's ship, A2 holds the lanes question a real coauthor must answer, and the folder's git fate is deferred to `QPf6`'s one row for all three.

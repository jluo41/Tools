# Word · a coauthor .docx and the PDF twin the tab shows
state: 🟡 PARTIAL · writer, route, tab shipped · open: lanes default, caption bold, checker boundary
owner: CC
method: call md2docx by path for the .docx, render its PDF twin with docx2pdf's Chrome pass, and frame the twin because a browser cannot show a .docx

## Opening
What can the board honestly put on screen for a coauthor whose only tool is Word?
The `.docx` is written for that one reader: someone who marks up in Word and never touches LaTeX.
A browser frames no `.docx`, so the 📝 tab carries a PDF twin rendered from the package itself, anchored comments and all.
The real artifact stays one ⬇ download away, and both halves are derived, land in the page's own `word/` folder, and regenerate on a click.

**Why the twin and not a converter**: `docx2pdf.py` reads the OOXML this family itself wrote, comments and all; macOS's `textutil` was measured dropping all 239 anchored comments, which for a file whose purpose is carrying evidence is a different document.
**Covered elsewhere**: `QPf1` rules the folder; the roster row is `../../board/haipipe-plugin/ref/roster.md`; the siblings are `QPf6` (latex, whose Decision row also rules this folder's git fate) and `QPf8` (bibex); the writer's own contract is `fn/to-word.md` in the paper family.

## Diagram
**One source, two artifacts, one honest frame**: the .docx for Word, the twin for the tab.
```text
  📄 <page>/<stem>.md
        │ POST /_board/word              live/export.py
        ▼
  🛠 md2docx.py ──▶ word/<stem>.docx     the ARTIFACT · flowing paragraphs
        │                                (--join-paragraphs) · anchored
        │                                comments · the page bib's references
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
  flat page fallback: <board>/word/ · the same fork the slide plugin takes
```
The tab never pretends to edit: a `.docx` has no live browser editor, so the surface is preview-and-download and says so, which is the trust rule the drawer pages already hold.
The prose SHAPE is the reader's, not the source's: the board's `.md` keeps one sentence per line for its sentence-anchor grammar, and the export passes `--join-paragraphs` so each block lands in Word as one flowing paragraph.
A coauthor reads prose; the one-line-per-sentence form is board machinery and stops at the export.
The bibliography prefers the PAGE'S OWN `bibex/<stem>.bib`, the same preference the latex plugin holds: `cli/refs.py` compiles its `.board-refs.bbl` and md2docx renders the in-text label and a References section from it, one store feeding chip, block, PDF, and .docx.
With no page store the export walks up toward the board root for a paper's `0-*.bib` and points `--paper-root` at what it finds, the same `0-*.bib` fallback `QPf6` §1 states for the LaTeX side.
Outside any paper there is no bbl to read, so each `\citep` key prints bare in its parentheses and no References section is written, and the `.docx` is still produced rather than refused.

### 2 · What rides in the comments
**The lanes**: the apparatus the LaTeX column drops survives here as anchored Word comments.
```text
  md2docx --lanes default        Citation
  board route · plain page       no --lanes passed
  board route · display units    --lanes Citation,Display
  an S stage page's > lanes      evidence audit
  a board page's > lanes         conversation
```
The default is Citation alone because a sentence often carries three true lanes, and five comments on one sentence is unreadable.
The board route inherits that default untouched on a plain page, and widens it to Citation and Display only when the page owns display units the export must name.
So the open question is whether a BOARD page's export wants the paper's default at all, or nothing, or a `--lanes` control in the tab: the writer was built for S stage pages whose lanes are evidence audits, and a board page's `>` lanes are conversation.
A2.1 answers it by handing one real export to one real reader rather than by reasoning about it here.

### 3 · The surface
**The 📝 tab**: the tab pattern QPf3 established, url then HEAD then write, with the word route behind it.
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
- [x] A1.2 · The export reads as prose, not as chopped one-sentence rows.
      **Done when:** every board export passes `--join-paragraphs` and a rebuilt `.docx` carries each markdown block as one flowing paragraph in its `document.xml`.

### A2 · 💬 What rides in the comments
- [ ] A2.1 · One export reaches one coauthor and the lane default is ruled from their markup.
      **Done when:** a board page's `.docx` has been read in Word by a person, and States records whether board exports keep Citation, carry nothing, or expose `--lanes` in the tab.
- [ ] A2.2 · A caption's `**Name**:` markers reach Word as bold text, never as literal asterisks.
      **Done when:** a board page is exported again and its captions read bold in Word, including the case where a comment range cuts a `**` pair in half and md2docx passes the run through unconverted.

### A3 · 🖼 The surface
- [x] A3.1 · The 📝 tab shipped and was driven, not assumed.
      **Done when:** the ➕ menu offers 📝 Word with its ● material dot in a live browser and opening it frames the view.

### P · 🚧 The boundary
- [ ] P1 · `word/` joins the checker's known-plugin list.
      **Done when:** `check.py` names `word/` a known plugin folder and warns on nothing inside it.

## States
The machinery is done and proven; what stays open is one reader's ruling, one markup wart, and the checker's boundary.
- ✅ A1.1 · Built 260815: docx, twin, view, download, failure path.
- ✅ A1.2 · Shipped 260815: `--join-paragraphs` rides every board export, and QPf8's rebuilt `.docx` carries each block as one flowing paragraph in its `document.xml`.
- ⬜ A2.1 · No board export has reached a Word-holding reader yet; the paper default rides unexamined.
- ⬜ A2.2 · md2docx converts a balanced `**` pair to a bold run since 260816, but no board export has been rebuilt and read since, and an unbalanced pair still prints its asterisks.
- ✅ A3.1 · Browser-verified 260815 through the driven CDP run: the ➕ menu's 📝 row opened and framed `QPf4b`'s view.
- ⬜ P1 · `check.py` does not yet know `word/` by name.

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
- 260816 · [REVISE-CC] the review pass landed under fixed Aims: the state line compressed to the row shape, the Opening led from what a browser can honestly show a Word-only coauthor, §1's fallback restated in `QPf6` §1's concrete terms (upward walk for a `0-*.bib`, then a bare key and no References section rather than a refusal), §2's clause rows compressed to label · value with the paper family's 260727 reason and the open question moved into prose, the dead `deck.py` name replaced by the slide plugin (the writer on disk is `live/autodeck.py`), the JL attributions moved out of Content into this Log, A1.2 and A3.1's Done when restored as conditions with States keeping the met evidence, the §3 caption named as QPf3's tab pattern, and the git-fate line dropped from States so `QPf6` states it once. Two facts checked against disk on the way: `live/export.py:407` now passes `--lanes Citation,Display` when the page owns display units, which §2 had not recorded, and md2docx converts a balanced `**` pair to a bold run, so A2.2 now carries what is left of the caption wart.
- 260815 · [RULE-JL] the export reads paragraph per paragraph, not sentence per paragraph: the board's one-sentence-per-line source is grammar for the sentence apparatus, and a coauthor gets flowing prose; `--join-paragraphs` became the board default and A1.2 records the proof on QPf8's rebuilt `.docx`. One wart stays open with the writer: the board's `**Name**:` caption markers reach Word as literal asterisks.
- 260815 · [REVISE-CC] the export cites from the page-owned bibex store: refs.py compiles the bbl beside the bib, md2docx reads it, and QPf8's .docx is the proof, "(Luo et al. 2026)" inline with a References section; md2docx's bbl parser learned plainnat's bare labels on the way (a paper-family fix that benefits the paper path identically).
- 260815 · [DRAFT-CC] page born in the plugin round, after the build: A1 records haipipe-board 0.128.0's ship and A2 holds the lanes question a real coauthor must answer.

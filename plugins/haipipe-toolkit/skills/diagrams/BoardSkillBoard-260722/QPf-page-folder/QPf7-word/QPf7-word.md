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
  flat page fallback: <board>/word/    for a page that owns no folder
```
The tab never pretends to edit: a `.docx` has no live browser editor, so the surface is preview-and-download and says so on its face.
The prose SHAPE is the reader's, not the source's: the board's `.md` keeps one sentence per line for its sentence-anchor grammar, and the export passes `--join-paragraphs` so each block lands in Word as one flowing paragraph.
A coauthor reads prose; the one-line-per-sentence form is board machinery and stops at the export.
The bibliography prefers the PAGE'S OWN `bibex/<stem>.bib`: `cli/refs.py` compiles its `.board-refs.bbl` and md2docx renders the in-text label and a References section from it, one store feeding chip, block, PDF, and .docx.
With no page store the export walks up toward the board root for a paper's `0-*.bib` and points `--paper-root` at what it finds, the same page-store preference and upward walk `QPf6` §1 states for the LaTeX side.
Outside any paper there is no bbl to read, so each `\citep` key prints bare in its parentheses and no References section is written, and the `.docx` is still produced rather than refused.

### 2 · What rides in the comments
**Which lanes each route passes**: the paper default, a plain board page, and a display-owning board page.
```text
  md2docx --lanes default        Citation
  board route · plain page       no --lanes passed
  board route · display units    --lanes Citation,Display
```
`QPf6` §2 records md2tex dropping the `>` lanes; here they have somewhere to go, because md2docx anchors each one as a comment on the sentence it belongs to.
The default is Citation alone because a sentence often carries three true lanes, and five comments on one sentence is unreadable.
The board route inherits that default untouched on a plain page, and widens it to Citation and Display only when the page owns display units the export must name.
The open question is what a BOARD page's export should pass: the paper's Citation default, no lanes, or a `--lanes` control in the tab.
It is open because the writer was built for S stage pages whose lanes are evidence audits, while a board page's `>` lanes are conversation.
A2.1 answers it by handing one real export to one real reader rather than by reasoning about it here.

### 3 · The surface
**The 📝 tab**: the registry's `tab: {url, write}` spec, url then HEAD then write, with the word route behind it.
```text
  82-plugin-exports.js ──POST──▶ /_board/word ──runs──▶ md2docx + docx2pdf
  tab.url()  names word/<stem>-view.html · HEAD hit ▶ frame it
  tab.write() builds on miss · lit-click            ▶ REBUILD
```
A HEAD miss is never a blank frame: opening the tab posts the route, says it is building, and lands on the view the writer returns, or prints the writer's own error where the view would have been.

## Aims
### A1 · 🧾 The contract
- A1.1 · The route, the twin, and the view shipped.
  **Done when:** one POST to `/_board/word` writes a real board page's `.docx`, its PDF twin, and the view that frames the twin beside the ⬇ download, and the no-twin branch still writes that download.
- A1.2 · The export reads as prose, not as chopped one-sentence rows.
  **Done when:** every board export passes `--join-paragraphs` and a rebuilt `.docx` carries each markdown block as one flowing paragraph in its `document.xml`.

### A2 · 💬 What rides in the comments
- A2.1 · One export reaches one coauthor and the lane default is ruled from their markup.
  **Done when:** a board page's `.docx` has been read in Word by a person, and States records whether board exports keep Citation, carry nothing, or expose `--lanes` in the tab.
- A2.2 · A caption's `**Name**:` markers reach Word as bold text, never as literal asterisks.
  **Done when:** a board page is exported again and its captions read bold in Word, and the comment-range-split case is either converted or recorded in States as accepted.

### A3 · 🖼 The surface
- A3.1 · The 📝 tab shipped and was driven, not assumed.
  **Done when:** the ➕ menu offers 📝 Word with its ● material dot in a live browser and opening it frames the view.

### P · 🚧 The boundary
- P1 · `word/` joins the checker's known-plugin list.
  **Done when:** `check.py` names `word/` a known plugin folder and warns on nothing inside it.

## States
The machinery is done and proven; what stays open is one reader's ruling, one markup wart, and the checker's boundary.
- ✅ A1.1 · Shipped in haipipe-board 0.128.0 and driven 260815 on `QPf4b`: the `.docx`, its twin, and the view landed, and `live/export.py` writes the ⬇ download in the no-twin branch too.
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
- `../QPf8-bibex/word/QPf8-bibex.docx`
  A1.2's proof: the rebuilt export that carries each markdown block as one flowing paragraph, with the page bib's References section behind it.

## Log
- 260816 · [REVISE-CC] second review pass: the Aims conditions, §2's fence and open question, §3's HEAD miss, and three cross-references.
      The pass held purpose and Aims fixed and repaired what the second round's read found.
      A1.1 gained a `Done when` and moved its ship evidence to States, and A2.2's condition now ends at "captions read bold in Word" with a convert-or-accept clause for the comment-range split, because the old wording named an unconverted run as satisfaction and contradicted its own State.
      §2's fence dropped to three route-to-flag rows so the value column stays one domain, its caption now says what the figure shows, and its open question became two sentences listing the three options once.
      §3 lost the row that repeated the Diagram's failure line and gained one sentence on what a HEAD miss guarantees, and `QPf8`'s `.docx` joined 🧪 Evidence so A1.2's ✅ cites a linked file.
      §1 carried a fourth id-less reference the round had not named, "the same preference the latex plugin holds", now folded into the sentence that names `QPf6` §1 for both the page store and the upward walk.
      Two cross-references were removed instead of given ids, because disk does not support them.
      `assets/js/10-drawer/70-plugin-slides.js:93-96` returns `''` for a page that owns no folder (`if (!m) return '';`), so the slide plugin takes NO flat-page fallback; the fork word takes is its own route's, `live/export.py:85-88` (`out_dir = Path(board) / plugin`), so the row now names the case rather than a sibling plugin.
      No page on this board states a preview-and-download "trust rule" (grep for `pretends to edit`, `preview-and-download` and `drawer page` returns only this page's own line), so that clause now stands on its own.
      §3's caption also stopped crediting `QPf3` for the url-then-HEAD-then-write pattern: `82-plugin-exports.js` records that "Draw and Slides predate the spec and still use their window hooks; these three are the first conforming instances", and the HEAD-then-build path is the shell's (`live/shell.py:1303-1307`), so the caption names the registry's `tab: {url, write}` spec instead.
      `QPf6` §1 carries the same slide-plugin claim in its own fence and is outside this page's bound, so it is reported rather than edited.
- 260816 · [REVISE-CC] the review pass landed under fixed Aims: the state line compressed to the row shape, the Opening led from what a browser can honestly show a Word-only coauthor, §1's fallback restated in `QPf6` §1's concrete terms (upward walk for a `0-*.bib`, then a bare key and no References section rather than a refusal), §2's clause rows compressed to label · value with the paper family's 260727 reason and the open question moved into prose, the dead `deck.py` name replaced by the slide plugin (the writer on disk is `live/autodeck.py`), the JL attributions moved out of Content into this Log, A1.2 and A3.1's Done when restored as conditions with States keeping the met evidence, the §3 caption named as QPf3's tab pattern, and the git-fate line dropped from States so `QPf6` states it once. Two facts checked against disk on the way: `live/export.py:407` now passes `--lanes Citation,Display` when the page owns display units, which §2 had not recorded, and md2docx converts a balanced `**` pair to a bold run, so A2.2 now carries what is left of the caption wart.
- 260815 · [RULE-JL] the export reads paragraph per paragraph, not sentence per paragraph: the board's one-sentence-per-line source is grammar for the sentence apparatus, and a coauthor gets flowing prose; `--join-paragraphs` became the board default and A1.2 records the proof on QPf8's rebuilt `.docx`. One wart stays open with the writer: the board's `**Name**:` caption markers reach Word as literal asterisks.
- 260815 · [REVISE-CC] the export cites from the page-owned bibex store: refs.py compiles the bbl beside the bib, md2docx reads it, and QPf8's .docx is the proof, "(Luo et al. 2026)" inline with a References section; md2docx's bbl parser learned plainnat's bare labels on the way (a paper-family fix that benefits the paper path identically).
- 260815 · [DRAFT-CC] page born in the plugin round, after the build: A1 records haipipe-board 0.128.0's ship and A2 holds the lanes question a real coauthor must answer.

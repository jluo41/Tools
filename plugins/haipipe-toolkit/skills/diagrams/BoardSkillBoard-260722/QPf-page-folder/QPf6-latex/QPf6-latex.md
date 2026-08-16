# Latex · the page compiled, in its own folder
state: 🟡 PARTIAL · writer, route, tab shipped 0.128.0 · open: natbib run, figure export, checker, git ruling
owner: CC
method: call the paper family's md2tex by path, wrap its section in a standalone master, compile with xelatex, and land the .tex, the .pdf, and the view page in the page's own latex/ folder
session: 6698437b-fe7e-4d6f-9e68-4b37e1d80f15

## Opening
Where does a page's LaTeX projection live, and who is allowed to write it?
A page's `.md` is the source, and the `.tex`, the `.pdf`, and the view page that shows them are DERIVED.
The plugin law keeps all three in the page's own `latex/` folder, where a rebuild may overwrite them.
The writer is the paper family's `md2tex.py`, called by path and never copied, so Word and LaTeX stay two projections of one source.
This page settles the plugin's contract and records what the first build left open.

**Why the board wraps its own master**: `md2tex --compile` is bound to one paper's hand-written master, so `live/export.py` wraps the generated section in a generic article master and compiles that instead.
**Covered elsewhere**: `QPf1` rules that a page owns its folder and every subfolder is a plugin; the roster row is `../../board/haipipe-plugin/ref/roster.md`; the sibling derived plugins are `QPf3` (slide), `QPf7` (word), and `QPf8` (bibex); the tab machinery they all share is the registry's `tab: {url, write}` spec.

## Diagram
**One source, four hops**: from the page's markdown to a framed view, nothing typed by hand.
```text
  📄 <page>/<stem>.md                    the SOURCE · haipipe-page owns it
        │ POST /_board/latex             live/export.py
        ▼
  🛠 md2tex.py  ──▶  latex/<stem>.tex    ### → \section · lanes dropped
        │            + <stem>-master.tex  generic article · natbib iff a
        ▼                                 0-*.bib is in reach upward
  🧮 xelatex (+bibtex when a bib)  ──▶  latex/<stem>.pdf
        │            + <stem>-view.html   written on every run
        │            -master.* residue deleted after the run
        ▼
  🖼 📜 tab frames the view · PDF + .tex fold
```

## Content
### 1 · The contract
**What the folder holds**: three files, all derived, all regenerable.
```text
  <page>/latex/
    <stem>.tex        ⚙️ md2tex's section · header says "do not hand-edit"
    <stem>.pdf        ⚙️ the compiled look · what the view shows
    <stem>-view.html  ⚙️ the tab's surface: PDF inline + the .tex one fold below
  flat page fallback: <board>/latex/<stem>.* · for a page that owns no folder
```
A hand-edited file is overwritten on the next build, which is the derived-plugin rule and not a defect.
The view page is nothing a person maintains: `export.py` rewrites it at the end of every run, whether or not xelatex produced a PDF.
The bibliography prefers the page's bibex/ store (QPf8): when `bibex/<stem>.bib` holds an entry, the PDF cites exactly what the page cites.
With no page bib, `--paper-root` is discovered by walking up toward the board root for a `0-*.bib`; outside any paper the export compiles cite-less with `\citep` printed as `[key]` rather than refusing.
With either bib the master gains natbib, `plainnat`, and a `bibtex` pass.

### 2 · What the writer inherits, and what it drops
**md2tex's read-and-drop table, applied to a board page**: the grammar mostly coincides, and the misses are recorded rather than hidden.
```text
  ### 1 · title      ──▶  \section
  #### block         ──▶  paragraph break
  \citep{} \ref{}    ──▶  kept verbatim
  > lanes            ──▶  DROPPED
  refuse-to-regress  ──▶  inherited
```
The Content divisions map cleanly because a division already is a section, and `\citep{}` and `\ref{}` ride through untouched because they were LaTeX before the export started.
The `>` lanes are the one real loss: the Word export lands them as anchored comments, and a LaTeX section has nowhere to put them.
Inheriting refuse-to-regress means a rewrite that loses citations is refused rather than silently written.
The proof run is `QPf4b`'s Content: eight divisions became a real four-page PDF, driven in a browser through the tab.
What does not survive is the board's emoji-heavy ascii figures: xelatex drops glyphs its fonts lack, so a figure-dense page reads thinner in PDF than on stage, and A2 below is where that gap is measured rather than guessed.

### 3 · The surface
**The 📜 tab**: the tab pattern QPf3 established, url then HEAD then write, with the latex route behind it.
```text
  82-plugin-exports.js ──POST──▶ /_board/latex ──runs──▶ md2tex + xelatex
  tab.url()  names latex/<stem>-view.html · PDF framed, .tex one fold below
  tab.write() builds on miss · lit-click       ▶ REBUILD (derived refresh)
  no PDF     ▶ the .tex fold opens · log tail above it
```
One view is written either way, so the tab never frames nothing: a successful run shows the PDF with the raw source folded under it, and a failed one opens that fold and prints the log tail, which puts the defect where the compiled page would have been.

## Aims
### A1 · 🧾 The contract
- A1.1 · The route, the master wrap, and the folder shipped.
  **Done when:** one POST to `/_board/latex` leaves `<stem>.tex`, `<stem>.pdf`, and `<stem>-view.html` in the page's own `latex/` folder and no `-master.*` beside them.
- A1.2 · A page that lives under a paper root exports with a resolved bibliography.
  **Done when:** a page above a real `0-*.bib` compiles with natbib and its `\citep` keys resolve in the PDF's reference list.

### A2 · 📐 What the writer inherits, and what it drops
- A2.1 · The board-page → tex mapping is measured on one figure-dense page.
  **Done when:** one page heavy in ascii figures is exported, the dropped-glyph and dropped-lane losses are listed in States, and the list rules whether the master needs a unicode font package or the losses are accepted.

### A3 · 🖼 The surface
- A3.1 · The 📜 tab shipped and was driven, not assumed.
  **Done when:** the 📜 tab frames a board page's compiled PDF in a live browser.

### P · 🚧 The boundary
- P1 · `latex/` joins the checker's known-plugin list.
  **Done when:** `check.py` names `latex/` a known plugin folder and warns on nothing inside it.

## States
The writer half is done and proven; the measurement and boundary halves are owed.
- ✅ A1.1 · Shipped as haipipe-board 0.128.0 on 260815: the endpoint, the master wrap, paper-root discovery, the cite-less degradation, the view page written on every run, and the `-master.*` residue deleted after it; every `latex/` folder on this board now holds the three files per stem.
- ⬜ A1.2 · No page on this board sits under a paper root, since no `0-*.bib` exists anywhere in its tree, so the natbib path has only been reasoned, not run.
- ⬜ A2.1 · No figure-dense page has been exported yet; `QPf4b` was prose-heavy and flattered the mapping.
- ✅ A3.1 · Browser-verified 260815: `QPf4b`'s four-page PDF framed through the driven CDP run, opened from the Plugin menu, closed by its own ✕.
- ⬜ P1 · `check.py` does not yet know `latex/` by name.

### Decision Now
- [ ] 🗣 What does git keep of a DERIVED plugin folder?
      This row rules for `latex/`, `word/`, and `bibex/`'s derived half at once and lands in the roster, because one answer must cover them.
      The page-owned `bibex/<stem>.bib` is PRIMARY and committed regardless; only the view and export files are in question.
      A · commit the artifacts, so the board is self-contained offline.
      ⭐B · gitignore the derived files whole; every one of them regenerates from the page by one click.
      🛑 Blocks: nothing; the folders exist either way.
      🤖 If nobody answers: B, the paper's machinery-under-the-delete-test ruling.

## Files
### ⚙️ Engines
- `../../board/haipipe-board/live/export.py`
  The route's owner: target vetting, paper-root discovery, the master wrap, residue cleanup, and the view page written on every run.
- `../../board/haipipe-board/assets/js/10-drawer/82-plugin-exports.js`
  The client half: the registry entry whose `tab` spec the shell builds the 📜 tab from.
- `../../paper/haipipe-paper/scripts/to-word/md2tex.py`
  The writer, called by path; if this page and its docstring disagree, the script wins.

### 🧪 Evidence
- `../QPf4b-chat-sdk/latex/QPf4b-chat-sdk.pdf`
  The first export: four pages, compiled 260815, driven in a browser through the 📜 tab, with its `-view.html` written beside it.

## Log
- 260816 · [FIX-CC] the flat-page fallback row stopped crediting the slide plugin: `70-plugin-slides.js:93-96` bails on a page that owns no folder, so slide has no such fallback and the attribution was false. The row now states the fallback plainly. The wording came from a review instruction, not from disk, which is why it reached the page at all; `live/export.py:84`'s own comment still credits the retired `deck.py` and needs an engine turn.
- 260816 · [REVISE-CC] the second review pass corrected what the page said about its own surface, every claim checked against disk first. `82-plugin-exports.js:73` registers latex with `ext: '-view.html'` and the file's own header says `WHY url() NAMES A VIEW PAGE for all three`, so the Diagram row, §3's fence and §1's folder listing were wrong about the tab framing the PDF directly: the tab frames `latex/<stem>-view.html`, which shows the PDF with the raw `.tex` one fold below. `export.py:304` writes that view on EVERY run ("ONE view either way"), not only on failure, so §3's prose became a success-and-failure statement instead of a failure-only one, and §1 now says three files, which is what each `latex/` folder holds on disk (`.tex`, `.pdf`, `-view.html`, in all eight of them). Twin wording adopted from `QPf7` where two reviewers found this page coining or drifting: the §3 caption is now the tab pattern `QPf3` established rather than a Slides sandwich, and §1's fallback walks up toward the board root rather than toward `--root`, a flag this page never introduces (`export.py:99-108` walks toward `self.root`). §2's two clause rows were compressed to values with their reasons moved into the prose under the figure, A1.1 was given a testable Done when with its 0.128.0 ship record moved into States, A3.1's condition was widened to a board page's PDF so it makes the same claim as the `QPf4b` evidence under it, and the Opening's `260815 build` became `the first build` so no date greets a cold reader. Two siblings of those defects were fixed with them: the head `method:` line still said "both halves", and A1.2's State still counted "both test pages" when eight `latex/` folders now exist, so it states the checkable fact instead, that no `0-*.bib` sits anywhere in this board's tree.
- 260816 · [REVISE-CC] the review pass landed under fixed Aims: the state line compressed to the row shape, the dead `deck.py` name replaced by the slide plugin (the writer on disk is `live/autodeck.py`), the 260815 dates and the JL attribution moved out of Content into this Log, A3.1's Done when restored as a condition with States keeping the met evidence, and the Diagram's wrapped clause compressed to a row with its sentence moved to §3 prose.
- 260815 1800 · [JL via CC] this plugin's own skill shipped: `haipipe-plugin-latex` under `page-plugins/` (the thin-door round, two specimens); the DERIVED specimen: a caller contract over the paper family's writer, holding no copy.
- 260815 · [REVISE-CC] the master's bibliography prefers the page-owned bibex store (JL: "this one to be cited as well"); QPf8's PDF is the proof: [Luo et al., 2026] inline and a bibtex References page, from `bibex/QPf8-bibex.bib`.
- 260815 1610 · [JL via CC] Display1-latex-proof accepted (JL: "please just do them for me"); preview renders all three divisions.
- 260815 1605 · [REVISE-CC] the three export defects fixed in md2tex.py and re-compiled through POST /_board/latex: section titles lose their `N ·` whole, a code span's TeX specials are escaped so `\citep` prints instead of running, and --keep-fences renders sketches as transliterated verbatim so a figure-only division no longer exports empty.
- 260815 · [DRAFT-CC] page born in the plugin round, after the build rather than before it: A1 records what shipped in haipipe-board 0.128.0, A2/A3/P1 hold what the build left open, and the git ruling for all three derived folders is put to JL here.

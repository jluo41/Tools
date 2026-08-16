# Latex · the page compiled, in its own folder
state: 🟡 PARTIAL · writer, route, tab shipped 0.128.0 · open: natbib run, figure export, checker, git ruling
owner: CC
method: call the paper family's md2tex by path, wrap its section in a standalone master, compile with xelatex, and land both halves in the page's own latex/ folder
session: 6698437b-fe7e-4d6f-9e68-4b37e1d80f15

## Opening
Where does a page's LaTeX projection live, and who is allowed to write it?
A page's `.md` is the source; its `.tex` and `.pdf` are DERIVED, so the plugin law puts them in the page's own `latex/` folder and lets a rebuild overwrite them.
The writer is the paper family's `md2tex.py`, called by path and never copied, so Word and LaTeX stay two projections of one source.
This page settles the plugin's contract and records what the 260815 build left open.

**Why the board wraps its own master**: `md2tex --compile` is bound to one paper's hand-written master, so `live/export.py` wraps the generated section in a generic article master and compiles that instead.
**Covered elsewhere**: `QPf1` rules that a page owns its folder and every subfolder is a plugin; the roster row is `../../board/haipipe-plugin/ref/roster.md`; the sibling derived plugins are `QPf3` (slide), `QPf7` (word), and `QPf8` (bibex); the tab machinery they all share is the registry's `tab: {url, write}` spec.

## Diagram
**One source, four hops**: from the page's markdown to a framed PDF, nothing typed by hand.
```text
  📄 <page>/<stem>.md                    the SOURCE · haipipe-page owns it
        │ POST /_board/latex             live/export.py
        ▼
  🛠 md2tex.py  ──▶  latex/<stem>.tex    ### → \section · lanes dropped
        │            + <stem>-master.tex  generic article · natbib iff a
        ▼                                 0-*.bib is in reach upward
  🧮 xelatex (+bibtex when a bib)  ──▶  latex/<stem>.pdf
        │            -master.* residue deleted after the run
        ▼
  🖼 📜 tab frames the PDF · failure ▶ .tex + log-tail view
```

## Content
### 1 · The contract
**What the folder holds**: two files, both derived, both regenerable.
```text
  <page>/latex/
    <stem>.tex    ⚙️ md2tex's section · header says "do not hand-edit"
    <stem>.pdf    ⚙️ the compiled look · what the tab frames
  flat page fallback: <board>/latex/<stem>.* · the same fork the slide plugin takes
```
A hand-edited file is overwritten on the next build, which is the derived-plugin rule and not a defect.
The bibliography prefers the page's bibex/ store (QPf8): when `bibex/<stem>.bib` holds an entry, the PDF cites exactly what the page cites.
With no page bib, `--paper-root` is discovered by walking up toward `--root` for a `0-*.bib`; outside any paper the export compiles cite-less with `\citep` printed as `[key]` rather than refusing.
With either bib the master gains natbib, `plainnat`, and a `bibtex` pass.

### 2 · What the writer inherits, and what it drops
**md2tex's read-and-drop table, applied to a board page**: the grammar mostly coincides, and the misses are recorded rather than hidden.
```text
  ### 1 · title      ──▶  \section          the Content divisions map cleanly
  #### block         ──▶  paragraph break
  \citep{} \ref{}    ──▶  kept verbatim     already LaTeX
  > lanes            ──▶  DROPPED           in Word they become comments;
                                            here they have nowhere to go
  refuse-to-regress  ──▶  inherited         a rewrite that loses citations
                                            is refused, not silently written
```
The proof run is `QPf4b`'s Content: eight divisions became a real four-page PDF, driven in a browser through the tab.
What does not survive is the board's emoji-heavy ascii figures: xelatex drops glyphs its fonts lack, so a figure-dense page reads thinner in PDF than on stage, and A2 below is where that gap is measured rather than guessed.

### 3 · The surface
**The 📜 tab**: the Slides sandwich with a compiler as the filling.
```text
  82-plugin-exports.js ──POST──▶ /_board/latex ──runs──▶ md2tex + xelatex
  tab.url()  names latex/<stem>.pdf · HEAD hit  ▶ frame it
  tab.write() builds on miss · lit-click       ▶ REBUILD (derived refresh)
  failure    ▶ a view page: the .tex + the log tail · never a blank frame
```
A failed compile never answers with silence: the tab frames a view page carrying the generated `.tex` and the log tail, so the defect is readable where the PDF would have been.

## Aims
### A1 · 🧾 The contract
- [x] A1.1 · The route, the master wrap, and the folder shipped.
      Shipped as haipipe-board 0.128.0: `/_board/latex`, paper-root discovery, the cite-less degradation, and the `-master.*` residue deleted after every run.
- [ ] A1.2 · A page that lives under a paper root exports with a resolved bibliography.
      **Done when:** a page above a real `0-*.bib` compiles with natbib and its `\citep` keys resolve in the PDF's reference list.

### A2 · 📐 What the writer inherits, and what it drops
- [ ] A2.1 · The board-page → tex mapping is measured on one figure-dense page.
      **Done when:** one page heavy in ascii figures is exported, the dropped-glyph and dropped-lane losses are listed in States, and the list rules whether the master needs a unicode font package or the losses are accepted.

### A3 · 🖼 The surface
- [x] A3.1 · The 📜 tab shipped and was driven, not assumed.
      **Done when:** the 📜 tab frames this page's PDF in a live browser.

### P · 🚧 The boundary
- [ ] P1 · `latex/` joins the checker's known-plugin list.
      **Done when:** `check.py` names `latex/` a known plugin folder and warns on nothing inside it.

## States
The writer half is done and proven; the measurement and boundary halves are owed.
- ✅ A1.1 · Built 260815: endpoint, master wrap, residue cleanup, failure view.
- ⬜ A1.2 · Both test pages sit outside any paper root, so the natbib path has only been reasoned, not run.
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
  The route's owner: target vetting, paper-root discovery, the master wrap, residue cleanup, the failure view.
- `../../board/haipipe-board/assets/js/10-drawer/82-plugin-exports.js`
  The client half: the registry entry whose `tab` spec the shell builds the 📜 tab from.
- `../../paper/haipipe-paper/scripts/to-word/md2tex.py`
  The writer, called by path; if this page and its docstring disagree, the script wins.

### 🧪 Evidence
- `../QPf4b-chat-sdk/latex/QPf4b-chat-sdk.pdf`
  The first export: four pages, compiled 260815, framed live through the tab.

## Log
- 260816 · [REVISE-CC] the review pass landed under fixed Aims: the state line compressed to the row shape, the dead `deck.py` name replaced by the slide plugin (the writer on disk is `live/autodeck.py`), the 260815 dates and the JL attribution moved out of Content into this Log, A3.1's Done when restored as a condition with States keeping the met evidence, and the Diagram's wrapped clause compressed to a row with its sentence moved to §3 prose.
- 260815 1800 · [JL via CC] this plugin's own skill shipped: `haipipe-plugin-latex` under `page-plugins/` (the thin-door round, two specimens); the DERIVED specimen: a caller contract over the paper family's writer, holding no copy.
- 260815 · [REVISE-CC] the master's bibliography prefers the page-owned bibex store (JL: "this one to be cited as well"); QPf8's PDF is the proof: [Luo et al., 2026] inline and a bibtex References page, from `bibex/QPf8-bibex.bib`.
- 260815 1610 · [JL via CC] Display1-latex-proof accepted (JL: "please just do them for me"); preview renders all three divisions.
- 260815 1605 · [REVISE-CC] the three export defects fixed in md2tex.py and re-compiled through POST /_board/latex: section titles lose their `N ·` whole, a code span's TeX specials are escaped so `\citep` prints instead of running, and --keep-fences renders sketches as transliterated verbatim so a figure-only division no longer exports empty.
- 260815 · [DRAFT-CC] page born in the plugin round, after the build rather than before it: A1 records what shipped in haipipe-board 0.128.0, A2/A3/P1 hold what the build left open, and the git ruling for all three derived folders is put to JL here.

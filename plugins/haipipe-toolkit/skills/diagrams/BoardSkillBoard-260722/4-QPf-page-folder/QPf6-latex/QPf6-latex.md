# Latex · the page compiled, in its own folder
state: 🟡 PARTIAL · writer, route, tab shipped · open: paper-root natbib, figure export, checker, git ruling
owner: CC
method: call the shared Page-plugin md2tex by path, wrap its section in a plain master, compile with lualatex, and leave the three files in the page's own latex/ folder
session: 6698437b-fe7e-4d6f-9e68-4b37e1d80f15

## Opening
Where does a page's LaTeX version live, and who is allowed to write it?
A page's `.md` is what a person writes, and the `.tex`, the `.pdf`, and the view page are rebuilt for you.
The rule keeps all three in the page's own `latex/` folder, where a rebuild may overwrite them.
The writer is the shared Page-plugin `md2tex.py`, called by path, so Word and LaTeX stay two views of one source.
This page settles the rules for that folder, and records what the first build left open.

**Why the board wraps its own master**: `md2tex.py` deliberately emits Page TeX only.
`live/export.py` owns the plain article wrapper and LuaLaTeX compilation.
**Covered elsewhere**: `QPf1` rules that a page owns its folder and every subfolder is a plugin; the plugin list is `../../board/haipipe-plugin/ref/roster.md`; the sister folders that are also rebuilt for you are `QPf3` (slide), `QPf7` (word), and `QPf8` (bibex); the tab machinery they all share is the registry's `tab: {url, write}` spec.

## Diagram
**One source, four hops**: from the page's markdown to a framed view, nothing typed by hand.
```text
  📄 <page>/<stem>.md                    the SOURCE · haipipe-page owns it
        │ POST /_board/latex             live/export.py
        ▼
  🛠 md2tex.py  ──▶  latex/<stem>.tex    ### → \section · lanes dropped
        │            + <stem>-master.tex  generic article · natbib iff a
        ▼                                 bib is in reach: bibex/ then upward
  🧮 lualatex (+bibtex when a bib) ──▶  latex/<stem>.pdf
        │            + <stem>-view.html   written on every run
        │            -master.* residue deleted after the run
        ▼
  🖼 📜 tab frames the view · PDF + .tex fold
```

## Content
### 1 · What sits in the folder, and what a rebuild overwrites
**What the folder holds**: three files, all built for you, and every one can be built again.
```text
  <page>/latex/
    <stem>.tex        ⚙️ md2tex's section · header says "do not hand-edit"
    <stem>.pdf        ⚙️ the compiled look · what the view shows
    <stem>-view.html  ⚙️ the tab's page: PDF inline + the .tex one fold below
  flat page fallback: <board>/latex/<stem>.* · for a page that owns no folder
```
📌 This part settles which three files live in `latex/`, and that a rebuild may overwrite any of them.

Edit one of these files by hand and the next build overwrites it.
That is the rule for a folder the machine rebuilds, not a fault.
Nobody keeps the view page up to date by hand.
`export.py` writes it again at the end of every run, whether or not lualatex produced a PDF.
The bibliography looks first at the page's own bibex/ list (QPf8).
When `bibex/<stem>.bib` holds an entry, the PDF cites exactly what the page cites.
With no page bib, the export looks for a `0-*.bib` by walking up from the page toward the server's root folder.
Outside any paper it still compiles with no citations, printing each `\citep` as `[key]` rather than refusing.
With either bib the master gains natbib, `plainnat`, and a `bibtex` pass.

### 2 · What survives the trip to LaTeX, and what is lost
**What md2tex keeps and what it drops on a board page**: most of it lines up, and the losses are written down, not hidden.
```text
  ### 1 · title      ──▶  \section
  #### block         ──▶  paragraph break
  \citep{} \ref{}    ──▶  kept verbatim
  > lanes            ──▶  DROPPED
  refuse-to-regress  ──▶  inherited
```
📌 This part says what a board page loses on its way to LaTeX: the `>` lanes, and some emoji.

The Content parts map cleanly, because a part already is a section.
`\citep{}` and `\ref{}` come through untouched, because they were LaTeX before the export started.
The `>` lanes are the one real loss.
The Word export lands them as comments pinned to a spot, and a LaTeX section has nowhere to put them.
The writer also refuses to go backwards: a rewrite that loses citations is refused, not written quietly.
The proof run is `QPf4b`'s Content: ten parts became a real nine-page PDF, driven in a browser through the tab.
The board's emoji-heavy ascii figures do not survive.
LuaLaTeX uses explicit fallback fonts for board glyphs; unsupported glyphs remain a visible export finding.
A2 below is where that gap gets measured instead of guessed.

### 3 · The tab shows something even when the build fails
**The 📜 tab**: the registry's `tab: {url, write}` spec, url first, then a HEAD check, then a build, with the latex route behind it.
```text
  82-plugin-exports.js ──POST──▶ /_board/latex ──runs──▶ md2tex + lualatex
  tab.url()  names latex/<stem>-view.html · PDF framed, .tex one fold below
  tab.write() builds on miss · lit-click       ▶ REBUILD (build it again)
  no PDF     ▶ the .tex fold opens · log tail above it
```
📌 This part settles that the 📜 tab always has a page to show: the PDF when the build works, the log when it does not.

One view page is written either way, so the tab is never empty.
A run that works shows the PDF, with the raw source folded under it.
A run that fails opens that fold and prints the tail of the log, so the error sits where the finished page would have been.
QPf6-Display1 shows the working case at the size a reader reads it: page 1 of this page's own export, rendered at 150 dpi, so the claim that the projection works is shown rather than asserted a third time.

## Aims
### Decision Now
- [ ] 🗣 What does git keep of a folder the machine rebuilds?
      This row rules for `latex/`, `word/`, and the rebuilt half of `bibex/` at once, and it lands in the plugin list, because one answer must cover them all.
      The page's own `bibex/<stem>.bib` is yours to write and is committed either way; only the view and export files are in question.
      A · commit the built files, so the board is complete offline.
      ⭐B · gitignore the built files completely, since one click builds every one of them again from the page.
      🛑 Blocks: nothing; the folders exist either way.
      🤖 If nobody answers: B, the paper's machinery-under-the-delete-test ruling.


### A1 · 🧾 What sits in the folder, and what a rebuild overwrites
- ✅ A1.1 · The route, the master wrap, and the folder shipped.
  **Done when:** one POST to `/_board/latex` leaves `<stem>.tex`, `<stem>.pdf`, and `<stem>-view.html` in the page's own `latex/` folder and no `-master.*` beside them.
  **Now:** Shipped as haipipe-board 0.128.0 on 260815: the endpoint, the master wrap, the paper-root search, the cite-less fallback, the view page written on every run, and the leftover `-master.*` files deleted after it. Every `latex/` folder on this board now holds the three files per stem.
- ⬜ A1.2 · A page under a paper root exports with its citations resolved.
  **Done when:** a page above a real `0-*.bib` compiles with natbib and its `\citep` keys resolve in the PDF's reference list.
  **Now:** natbib and bibtex have run: `QPf8`'s compiled PDF prints `[Luo et al., 2026]` inline and a References page after it, compiled from that page's own `bibex/` bib. What has never run is the paper-root half this Aim asks for, because no `0-*.bib` exists anywhere in this board's tree for the upward walk to find.


### A2 · 📐 What survives the trip to LaTeX, and what is lost
- ⬜ A2.1 · The losses are measured on one page full of figures.
  **Done when:** one page full of ascii figures is exported and the lost glyphs and lost lanes are listed in States. That list then decides whether the master needs a unicode font package, or whether the losses are accepted.
  **Now:** No page full of figures has been exported yet. `QPf4b` was mostly prose, so it made the mapping look better than it is.


### A3 · 🖼 The tab shows something even when the build fails
- ✅ A3.1 · The 📜 tab shipped and was driven, not assumed.
  **Done when:** the 📜 tab frames a board page's compiled PDF in a live browser.
  **Now:** Checked in a browser on 260815: `QPf4b`'s nine-page PDF framed through the driven CDP run, opened from the Plugin menu, closed by its own ✕.


### P · 🚧 The checker knows this folder
- ⬜ P1 · `latex/` joins the list of folders the checker knows.
  **Done when:** `check.py` names `latex/` a known plugin folder and warns on nothing inside it.
  **Now:** `check.py` does not yet know `latex/` by name.


## Discussion

### From the retired States section (merged 260831)
The writer half is done and proven, and the measuring half and the checker half are still owed.

## Files
### ⚙️ Engines
- `../../board/haipipe-board/live/export.py`
  The route's owner: checking the target, finding the paper root, the master wrap, clearing the leftover files, and the view page written on every run.
- `../../board/haipipe-board/assets/js/10-drawer/82-plugin-exports.js`
  The client half: the registry entry whose `tab` spec the shell builds the 📜 tab from.
- `../../board/page-plugins/_shared-export/md2tex.py`
  The writer, called by path; if this page and its docstring disagree, the script wins.

### 🧪 Evidence
- `../QPf4b-chat-sdk/latex/QPf4b-chat-sdk.pdf`
  The first export: ten `\section`s over nine pages, compiled 260815, driven in a browser through the 📜 tab, with its `-view.html` written beside it.

## Log
- 260816 · [REVISE-CC] the third review pass fixed FACTS and left the plain wording alone. The proof artifact was finally opened rather than quoted: `QPf4b-chat-sdk.tex` carries TEN `\section` lines, matching `QPf4b.md`'s `### 1` through `### 10`, and its PDF is NINE pages, so §2's "eight parts became a real four-page PDF", the Evidence row's "four pages" and A3.1's "four-page PDF" all became ten parts and nine pages. A1.2 said the natbib path "has been reasoned about and never run", which `QPf8-bibex/latex/QPf8-bibex.pdf` disproves on its face: it prints `[Luo et al., 2026]` inline and a References page, so natbib and bibtex ran off the page's own `bibex/` bib (`export.py:257-289` takes that branch first). Only the paper-root half is unrun, since no `0-*.bib` exists anywhere in this board's tree, so the row now says that and the head `state:` line's `open: natbib run` became `open: paper-root natbib`; `0.128.0` left the same line to keep it under 110 characters, and States A1.1 already carried it. §1's bibliography sentence was wrong twice: `export.py:99-108` walks toward `self.root`, the SERVER's root, which sits above the board, so the walk passes the board root rather than stopping there, and it named `--paper-root`, a flag this page never introduces, the same defect that got `--root` removed the pass before. It now walks up from the page toward the server's root folder and names no flag. §3's caption credited "the tab pattern QPf3 established" while `82-plugin-exports.js:11` states that "Draw and Slides predate the spec"; it now uses the registry's `tab: {url, write}` wording, which this page's own Opening and `QPf7` §3 already use. One sibling went with it: the Diagram said natbib fires iff a `0-*.bib` is in reach upward, and `export.py:257-264` prefers the page's own `bibex/` bib first, so the row now reads `bibex/ then upward`.

- 260818 1720 · [REVISE-CC] `QPf6-Display1-latex-proof` completed, and it was 2 of the board's 4 errors. It had no `README.md` and no `intake/manifest.yaml` at all, so it read as `display-declared-no-claim` and `display-declared-not-rendered`: a folder without a claim is not a proposal, and three loose files are not a display. Its `intake/SOURCE.txt` also named `../../latex/QPf6-latex.tex`, a file that does not exist, because the latex plugin writes a `.pdf` and a `-view.html` and keeps no `.tex` beside them. Now: a README with a `claim:`, a frozen `intake/` holding the compiled PDF and this page source with their sha256, `assets/figure.png` as the winning asset name `src/page_evidence.py:34` looks for, a `float.tex`, and the citation above. `accepted:` stays ⬜ despite the 260815 Log line recording JL accepting it, because the README that tick lives on did not exist then and the assets have been re-rendered since.- 260816 · [REVISE-CC] a record written late, for a change that had none: the Aims rows carry no `- [ ]` boxes. `check.py:939-940` returns early from `check_state_mirrors_aims` on any Aims section holding a checkbox, so stripping them moved this page out of the legacy-exempt branch and the Aims↔States mirror is now enforced on it. In the same pass States gained the four `### A1` / `### A2` / `### A3` / `### P` group headings that mirror Aims, each taking its Aims group's number, name and emoji, and `### Decision Now` moved from last to first, where `ref/page-template.md:290-292` puts it: everything else in States reports, and this is the one part that asks the reader to act.
- 📖 260816 · [REVISE-CC, JL ruled] the page was rewritten in plain words, for a reader with ADHD whose English is a second language (JL: "我真的读不下去"). The 🧭 Outline tab had been showing this page's own sentences back, and they were unreadable, so the tab was right and the prose was not. Every division title now names its consequence instead of a mechanism, each one gained a `📌` line saying in one sentence what the part settles, and every aim, `Done when:` and State row was replaced with a short plain-word version. House words went with them, `division` to part, `store` to list, `render` to read or draw, `seed` to suggest, `mint` to build. Measured with `haipipe-writing`'s `cli/score.py`: 4 sentences flagged before, 0 after, every one that remains inside this Log, which is history and was not touched. No fact, id, `§` mark or section changed; only the words.
- 260816 · [FIX-CC] the flat-page fallback row stopped crediting the slide plugin: `70-plugin-slides.js:93-96` bails on a page that owns no folder, so slide has no such fallback and the attribution was false. The row now states the fallback plainly. The wording came from a review instruction, not from disk, which is why it reached the page at all; `live/export.py:84`'s own comment still credits the retired `deck.py` and needs an engine turn.
- 260816 · [REVISE-CC] the second review pass corrected what the page said about its own surface, reading each SURFACE claim off `82-plugin-exports.js` and `live/export.py` before writing it. The counts it carried over from `QPf4b` were not read off anything, and a later pass found both wrong. `82-plugin-exports.js:73` registers latex with `ext: '-view.html'` and the file's own header says `WHY url() NAMES A VIEW PAGE for all three`, so the Diagram row, §3's fence and §1's folder listing were wrong about the tab framing the PDF directly: the tab frames `latex/<stem>-view.html`, which shows the PDF with the raw `.tex` one fold below. `export.py:304` writes that view on EVERY run ("ONE view either way"), not only on failure, so §3's prose became a success-and-failure statement instead of a failure-only one, and §1 now says three files, which is what each `latex/` folder holds on disk (`.tex`, `.pdf`, `-view.html`, in all eight of them). Twin wording adopted from `QPf7` where two reviewers found this page coining or drifting: the §3 caption is now the tab pattern `QPf3` established rather than a Slides sandwich, and §1's fallback walks up toward the board root rather than toward `--root`, a flag this page never introduces (`export.py:99-108` walks toward `self.root`). §2's two clause rows were compressed to values with their reasons moved into the prose under the figure, A1.1 was given a testable Done when with its 0.128.0 ship record moved into States, A3.1's condition was widened to a board page's PDF so it makes the same claim as the `QPf4b` evidence under it, and the Opening's `260815 build` became `the first build` so no date greets a cold reader. Two siblings of those defects were fixed with them: the head `method:` line still said "both halves", and A1.2's State still counted "both test pages" when eight `latex/` folders now exist, so it states the checkable fact instead, that no `0-*.bib` sits anywhere in this board's tree.
- 260816 · [REVISE-CC] the review pass landed under fixed Aims: the state line compressed to the row shape, the dead `deck.py` name replaced by the slide plugin (the writer on disk is `live/autodeck.py`), the 260815 dates and the JL attribution moved out of Content into this Log, A3.1's Done when restored as a condition with States keeping the met evidence, and the Diagram's wrapped clause compressed to a row with its sentence moved to §3 prose.
- 260815 1800 · [JL via CC] this plugin's own skill shipped: `haipipe-plugin-latex` under `page-plugins/` (the thin-door round, two specimens); the DERIVED specimen: a caller contract over the paper family's writer, holding no copy.
- 260815 · [REVISE-CC] the master's bibliography prefers the page-owned bibex store (JL: "this one to be cited as well"); QPf8's PDF is the proof: [Luo et al., 2026] inline and a bibtex References page, from `bibex/QPf8-bibex.bib`.
- 260815 1610 · [JL via CC] Display1-latex-proof accepted (JL: "please just do them for me"); preview renders all three divisions.
- 260815 1605 · [REVISE-CC] the three export defects fixed in md2tex.py and re-compiled through POST /_board/latex: section titles lose their `N ·` whole, a code span's TeX specials are escaped so `\citep` prints instead of running, and --keep-fences renders sketches as transliterated verbatim so a figure-only division no longer exports empty.
- 260815 · [DRAFT-CC] page born in the plugin round, after the build rather than before it: A1 records what shipped in haipipe-board 0.128.0, A2/A3/P1 hold what the build left open, and the git ruling for all three derived folders is put to JL here.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0
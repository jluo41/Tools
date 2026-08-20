# Word · a coauthor .docx and the PDF twin the tab shows
state: 🟡 PARTIAL · writer, route, tab shipped · open: lanes default, caption bold, checker boundary
owner: CC
method: call md2docx by path for the .docx, draw its PDF twin with docx2pdf's Chrome pass, and write the view page the tab frames, leaving all three files in the page's own word/ folder

## Opening
What can the board honestly show on screen to a coauthor who only uses Word?
The `.docx` is written for that one reader, who marks up in Word and never touches LaTeX.
A browser cannot show a `.docx`, so the 📝 tab frames a view page holding a PDF twin of the file itself.
The twin keeps every comment, each one still pinned to the sentence it belongs to.
The real file stays one ⬇ download away.
All three files land in the page's own `word/` folder, and one click builds them again.

**Why a twin, and not a converter**: `docx2pdf.py` reads the OOXML that this family wrote itself, comments and all.
macOS's `textutil` was measured dropping all 239 pinned comments, and a file whose job is carrying evidence is a different file without them.

**Covered elsewhere**: `QPf1` rules the folder, and this plugin's row in the plugin list is `../../board/haipipe-plugin/ref/roster.md`.
The siblings are `QPf6` (latex, whose Decision row also settles whether this folder goes into git) and `QPf8` (bibex).
The rules the writer itself follows are in its shared Page-plugin docstring and the Word plugin contract.

## Diagram
**One source, three files**: the .docx for Word, the twin drawn from it, and the view page the tab frames.
```text
  📄 <page>/<stem>.md
        │ POST /_board/word              live/export.py
        ▼
  🛠 md2docx.py ──▶ word/<stem>.docx     the FILE · flowing paragraphs
        │                                (--join-paragraphs) · comments
        │                                pinned to their sentences ·
        │                                the page bib's references
        ▼
  🖨 docx2pdf.py (Chrome headless) ──▶ word/<stem>.pdf   the TWIN
        ▼
  🖼 word/<stem>-view.html               what the 📝 tab shows:
     the twin inline + ⬇ download the .docx
     no twin ▶ the view says so and keeps the download
```

## Content
### 1 · 🧾 Three files land in `word/`, and each one is rebuilt for you
**What the folder holds**: three files, none of them written by hand, all made again on a click.
```text
  <page>/word/
    <stem>.docx        ⚙️ md2docx's file · the thing a coauthor opens
    <stem>.pdf         ⚙️ the Chrome-drawn twin · what the tab shows
    <stem>-view.html   ⚙️ the tab's page: twin inline + ⬇ download
  flat page fallback: <board>/word/<stem>.* · a page that owns no folder
```
📌 This part settles what the folder holds, how the prose is shaped for Word, and where the references come from.
A browser has no live editor for a `.docx`, so the tab is preview and download.
Above the twin the view prints one line, `the PDF twin below is rendered from the package itself`, with the ⬇ download link beside it.
The prose is shaped for the reader, not for the source file.
The board's `.md` keeps one sentence per line, because that is how a comment finds the sentence it belongs to.
The export passes `--join-paragraphs`, so each block lands in Word as one flowing paragraph.
A coauthor reads prose, so the one-line-per-sentence form is board machinery and stops at the export.
The reference list prefers the PAGE'S OWN `bibex/<stem>.bib`.
`cli/refs.py` compiles its `.board-refs.bbl`, and md2docx draws both the in-text label and a References section from it.
So one list feeds the chip, the block, the PDF, and the .docx.
With no list on the page, the export walks up toward the board root looking for a paper's `0-*.bib`, and points `--paper-root` at what it finds.
`QPf6` §1 states the same preference and the same upward walk for the LaTeX side.
Outside any paper there is no bbl to read.
Each `\citep` key then prints bare in its brackets and no References section is written, and the `.docx` is still made rather than refused.

### 2 · 💬 Which comments travel into Word, and the one question still open
**Which lanes reach Word**: what a plain board page sends, and what a page that owns display units sends.
```text
  plain board page          Citation
  page with display units   Citation + Display
```
📌 This part settles which comment lines reach Word today, and names the one question a real reader still has to answer.
A `>` lane is a line written under a sentence, and the board uses lanes for citations, comments, and change records.
`QPf6` §2 records md2tex dropping those lanes, but here they have somewhere to go.
md2docx turns each one into a Word comment, pinned to the sentence it sits under.
The writer's own default is Citation alone: the other two evidence lanes, Value and Display, travel only when a run asks for them.
Five comments on one sentence cannot be read, and Citation is the lane a coauthor checks.
A plain board page passes no `--lanes` flag, so it rides that default and its Citation comments still reach Word.
A page that owns display units is exported with `--lanes Citation,Display`, so the units the export names come through too.
The open question is what a BOARD page should send: keep today's inherited Citation default, suppress comments entirely, or expose `--lanes` in the tab.
It is open because the writer was built for S stage pages.
There a lane is an evidence audit, while on a board page a lane is people talking.
A2.1 answers it by handing one real export to one real reader, not by arguing it out here.

### 3 · 🖼 Opening the tab builds the file when it is not there yet
**The 📝 tab**: the registry's `tab: {url, write}` spec, url first, then a HEAD check, then a build, with the word route behind it.
```text
  82-plugin-exports.js ──POST──▶ /_board/word ──runs──▶ md2docx + docx2pdf
  tab.url()  names word/<stem>-view.html · HEAD hit ▶ show it
  tab.write() builds on miss · lit-click            ▶ REBUILD
```
📌 This part settles what you see when you open the tab and the file has not been built yet.
A HEAD is a small web question that asks only whether a file is there, and a miss never leaves you with a blank tab.
Opening the tab posts the route, says it is building, and lands on the view the writer returns.
If the writer fails, its own error prints where that view would have been.

## Aims
### A1 · 🧾 Three files land in `word/`, and each one is rebuilt for you
- A1.1 · The route, the twin, and the view all shipped.
  **Done when:** one POST to `/_board/word` writes a real board page's `.docx`, its PDF twin, and the view that shows the twin beside the ⬇ download, and the no-twin branch still writes that download.
- A1.2 · The export reads as prose, not as a run of chopped one-sentence rows.
  **Done when:** every board export passes `--join-paragraphs`, and a rebuilt `.docx` carries each markdown block as one flowing paragraph in its `document.xml`.

### A2 · 💬 Which comments travel into Word, and the one question still open
- A2.1 · One export reaches one coauthor, and their markup settles which comments we send.
  **Done when:** a person has read a board page's `.docx` in Word, and States records the ruling: keep Citation, send nothing, or put `--lanes` in the tab.
- A2.2 · A caption's `**Name**:` marks reach Word as bold text, never as plain asterisks.
  **Done when:** a board page is exported again and its captions read bold in Word, and the case where a comment range splits the pair is either converted too or written into States as accepted.

### A3 · 🖼 Opening the tab builds the file when it is not there yet
- A3.1 · The 📝 tab shipped, and someone drove it rather than assuming it worked.
  **Done when:** the ➕ menu offers 📝 Word with its ● dot in a live browser, and opening it shows the view.

### P · 🚧 The checker's boundary
- P1 · `word/` joins the list of folders the checker knows.
  **Done when:** `check.py` names `word/` a known plugin folder and warns on nothing inside it.

## States
The machinery is built and proven.
What stays open is one reader's ruling, one small markup fault, and the checker's boundary.
- ✅ A1.1 · Shipped in haipipe-board 0.128.0 and driven on 260815 on `QPf4b`: the `.docx`, its twin, and the view all landed, and `live/export.py` writes the ⬇ download in the no-twin branch too.
- ✅ A1.2 · Shipped 260815: every board export passes `--join-paragraphs`, and QPf8's rebuilt `.docx` carries each block as one flowing paragraph in its `document.xml`.
- ⬜ A2.1 · No board export has reached a reader who uses Word yet, so the paper default still runs unchecked.
- ⬜ A2.2 · Since 260816 md2docx turns a matched `**` pair into bold, but no board export has been rebuilt and read since, and an unmatched pair still prints its asterisks.
- ✅ A3.1 · Checked in a real browser on 260815 through the driven CDP run: the ➕ menu's 📝 row opened and showed `QPf4b`'s view.
- ⬜ P1 · `check.py` does not yet know `word/` by name.

## Files
### ⚙️ Engines
- `../../board/haipipe-board/live/export.py`
  The route's owner: it builds the docx, draws the twin, and writes the view page.
- `../../board/haipipe-board/cli/refs.py`
  The reference compiler the route runs on the page's own bib: it writes the `.board-refs.bbl` that md2docx reads.
- `../../board/haipipe-board/assets/js/10-drawer/82-plugin-exports.js`
  The registry row whose `tab` spec the shell builds the 📝 tab from.
- `../../board/page-plugins/_shared-export/md2docx.py`
  The writer, called by path; its docstring and the Word plugin contract hold the export rules.
- `../../board/page-plugins/_shared-export/docx2pdf.py`
  The twin's maker: it reads the OOXML directly, prints comments in the margin, and uses Chrome for the paged output.

### 🧪 Evidence
- `../QPf4b-chat-sdk/word/QPf4b-chat-sdk.docx`
  The first export, 260815, with its eight-page twin and view beside it.
- `../QPf8-bibex/word/QPf8-bibex.docx`
  A1.2's proof: the rebuilt export that carries each markdown block as one flowing paragraph, with the page bib's References section behind it.

## Log
- 260816 · [REVISE-CC] third review pass, facts only: every claim on the page was rechecked against the scripts before it was rewritten, and the plain words of the earlier pass were kept.
      The pass held purpose and Aims fixed, and changed no Aim, no `Done when:` and no State row.
      `md2docx.py:1098` sets `--lanes` to Citation by default, and `live/export.py:403-407` adds the flag only when the page owns display units, so §2's fence was mixing lane names with flags and one row read as "no lanes ride" while the prose said the default rides untouched.
      That fence now carries one route per row with lane names alone, a plain page sending Citation and a page with display units sending Citation and Display, and the flag facts moved into the prose under it.
      §2's three options were not distinguishable either, because "the paper's Citation default" is what the board route already does and "no lanes" named no mechanism; they now read keep today's inherited Citation default, suppress comments entirely, or expose `--lanes` in the tab.
      `export.py:426-444` writes `word/<stem>-view.html` at the end of every run, so the head `method:` line and the Opening both undercounted the products where §1 already said three files; both now name the view page beside the `.docx` and its twin, the same fix the twin `QPf6` made today.
      The view prints one line above the twin and the ⬇ download link beside it and never says editing is unavailable (`export.py:429-441`), so §1's "says so on its face" clause went and the line the view really prints is quoted in its place.
      `cli/refs.py` joined ⚙️ Engines: §1 names it as the compiler of `.board-refs.bbl` and `export.py:360-366` really runs it, and no row listed it.
      §1's flat-page fallback row took the twin's shape, `flat page fallback: <board>/word/<stem>.* · a page that owns no folder`, in place of a space-padded clause that dropped the `<stem>.*`.
      The three Content parts took the emoji their Aims groups already carry, so each Aims group matches its part by number, emoji and name and the `group-name-drift` warnings have nothing left to catch.
      The line reporting `QPf6` §1's slide-plugin credit was amended rather than dropped, because `QPf6`'s own Log records that row fixed on 260816 and its fence now reads "for a page that owns no folder".
- 📖 260816 · [REVISE-CC, JL ruled] the page was rewritten in plain words, for a reader with ADHD whose English is a second language (JL: "我真的读不下去"). The 🧭 Outline tab had been showing this page's own sentences back, and they were unreadable, so the tab was right and the prose was not. Every division title now names its consequence instead of a mechanism, each one gained a `📌` line saying in one sentence what the part settles, and every aim, `Done when:` and State row was replaced with a short plain-word version. House words went with them, `division` to part, `store` to list, `render` to read or draw, `seed` to suggest, `mint` to build. Measured with `haipipe-writing`'s `cli/score.py`: 12 sentences flagged before, 6 after, every one that remains inside this Log, which is history and was not touched. No fact, id, `§` mark or section changed; only the words.
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
      `QPf6` §1 carried the same slide-plugin claim in its own fence and was outside this page's bound, so it was reported rather than edited; `QPf6`'s own Log records that row fixed on 260816, and its fence now reads "for a page that owns no folder".
- 260816 · [REVISE-CC] the review pass landed under fixed Aims: the state line compressed to the row shape, the Opening led from what a browser can honestly show a Word-only coauthor, §1's fallback restated in `QPf6` §1's concrete terms (upward walk for a `0-*.bib`, then a bare key and no References section rather than a refusal), §2's clause rows compressed to label · value with the paper family's 260727 reason and the open question moved into prose, the dead `deck.py` name replaced by the slide plugin (the writer on disk is `live/autodeck.py`), the JL attributions moved out of Content into this Log, A1.2 and A3.1's Done when restored as conditions with States keeping the met evidence, the §3 caption named as QPf3's tab pattern, and the git-fate line dropped from States so `QPf6` states it once. Two facts checked against disk on the way: `live/export.py:407` now passes `--lanes Citation,Display` when the page owns display units, which §2 had not recorded, and md2docx converts a balanced `**` pair to a bold run, so A2.2 now carries what is left of the caption wart.
- 260815 · [RULE-JL] the export reads paragraph per paragraph, not sentence per paragraph: the board's one-sentence-per-line source is grammar for the sentence apparatus, and a coauthor gets flowing prose; `--join-paragraphs` became the board default and A1.2 records the proof on QPf8's rebuilt `.docx`. One wart stays open with the writer: the board's `**Name**:` caption markers reach Word as literal asterisks.
- 260815 · [REVISE-CC] the export cites from the page-owned bibex store: refs.py compiles the bbl beside the bib, md2docx reads it, and QPf8's .docx is the proof, "(Luo et al. 2026)" inline with a References section; md2docx's bbl parser learned plainnat's bare labels on the way (a paper-family fix that benefits the paper path identically).
- 260815 · [DRAFT-CC] page born in the plugin round, after the build: A1 records haipipe-board 0.128.0's ship and A2 holds the lanes question a real coauthor must answer.

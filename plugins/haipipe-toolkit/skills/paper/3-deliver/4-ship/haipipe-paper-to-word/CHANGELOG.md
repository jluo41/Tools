# CHANGELOG — haipipe-paper-to-word

## 0.5.0 — 2026-07-28 — the caption, the cross-reference and the table are the unit's, not ours

Everything here is one defect class: this projection was COMPOSING what the
manuscript already AUTHORS, so the .docx carried a second, worse copy.

- **A caption is read from the unit's `float.tex`, not built from its folder
  name.** It shipped as "Figure 1. display01a-hero-concept" (JL). Extraction is
  balanced-brace, so a `\textbf` inside a caption cannot truncate it, and the
  `\ref` inside it resolves through the SAME numbering the body uses: Table 6's
  caption read "the per-cohort estimates behind Figure fig:discretion-gradient".
- **`\ref` supplies the number; the author supplies the word.** Prose writes
  `Table~\ref{tab:results}` and this emitted the kind again, so every
  cross-reference in the file read "Table~Table 5". `~` is also a non-breaking
  space, and body prose is not de-TeX'd, so it was printing as a tilde.
- **`$^{***}$` is `***`.** The math delimiters were dropped, then the braces,
  leaving the literal `9.3438^***` in every results cell.
- **Tables are set like tables.** They were `w:type="auto"`, so Word autofitted
  them narrow and left-hugging, and adjacent columns met with no gutter:
  `+0.0064*** (0.0020)765,701 High`. Now full body width (9360 twips), fixed
  layout, `jc center`, `tblCellMar` gutters, and column widths proportional to
  the widest cell. Alignment comes from the unit's own LaTeX column spec, so a
  column is centred here because the author centred it there.
- **Cell paragraphs are single-spaced** (`w:line="240"`). They inherited the
  document's double spacing, so every table stood at twice its height and broke
  across pages it otherwise fitted on.
- **The `TableText` style is APPLIED, not merely declared.** It was defined at
  10pt and never referenced, so Word set cells at the document's 12pt while
  `col_widths` and `docx2pdf` both sized them at 10pt: every column was ~20% too
  narrow for its own content and Word broke words to fit, "Agreeable / ness",
  "Discretio / n", "1,204,6 / 07" (JL). It also gained `basedOn Normal` and an
  explicit `rFonts`, because a style with neither inherits from `docDefaults`,
  which this package does not write, so the tables would have been set in Word's
  own default face while the body stayed Times New Roman.
- **Column widths are sized in POINTS, with a floor no word can break.** Two
  numbers per column: WANT is its widest whole cell on one line, FLOOR is its
  widest unbreakable token (a hyphen and a slash end a token, as they do in
  Word). The floor is satisfied first and only the slack goes toward want, so a
  definition column wraps between words as it should while `High-dose/long-`
  `duration` cannot be cut in half. Character count was the first proxy and it
  is too coarse in the direction that matters: a results column is digits, half
  again as wide as lowercase, so `+12.90*** (3.68)` was landing 0.02in inside
  its column and Word's 12pt then pushed it over.
- **A table row cannot be torn across a page** (`cantSplit`), the leading bold
  rows repeat as a header (`tblHeader`), and the `Caption` style has `keepNext`
  with real `before`/`after` spacing. Table 5's caption and header stranded at
  the foot of one page with the body on the next, and a caption with
  `w:after="0"` touched the paragraph below it (JL).
- **`docx2pdf.py` mirrors the package instead of second-guessing it**: booktabs
  rules only where it used to draw a full cell grid the .docx never had, and it
  now reads `tblGrid` widths and per-cell `w:jc` from the file it is rendering.
  Its comment reader also honours `w:br`, which it was dropping, so a
  three-reference comment ran together here while Word showed it right.

And the comment load itself, which is the same defect one level up: the file was
carrying everything TRUE rather than everything the reader is CHECKING.

- **`--lanes`, defaulting to `Citation` alone.** One §1 sentence drew five
  comments and three were `Display` audits several hundred characters long (JL).
  A display's `state:` is a board concern; the coauthor in Word is checking the
  sentence. 239 comments → 111, and the review PDF 53 pages → 39. The full set
  is one flag away, `--lanes Citation,Value,Display`, and what is held back is
  COUNTED on the way out ("held back by --lanes: Display 55 · Value 73").
- **A blank line between references inside one comment.** `\citep{a,b,c}` is one
  comment, and joining on a single newline gave a wall the reader had to
  re-parse to find where one reference ended (JL). 34 comments carry more than
  one reference.

## 0.4.0 — 2026-07-27 — only evidence reaches Word, and it anchors on its own sentence

- **`EVIDENCE_LANES` is the board's three, not a list this skill invented**:
  `Value`, `Citation`, `Display`, taken from `haipipe-board/src/body.py:288`. A
  `Note` is a pending candidate edit and a `Check` is a section gate report;
  neither backs a sentence, and neither belongs in a coauthor's file. They are
  COUNTED on the way out ("working lanes NOT exported"), never silently dropped.
- **A hand-written `> Citation:` lane also stays on the board.** The citation
  comment is the GENERATED reference plus the key. The `.bib` line, the tex
  placement, the hit count and a de-duplication history are working notes: true,
  useful, and not what a coauthor checks. One merged comment reached 605 chars
  for a 240-char reference. Median citation comment is now 262.
- **The anchoring fix, three stacked causes.** Joining sentences into paragraphs
  turned the "no number found" fallback from one sentence into the whole
  paragraph, so a single Value lane highlighted all eleven sentences of the
  abstract. Then two lanes sharing a sentence window were read as an overlap and
  demoted to the paragraph. Then a number nested INSIDE its own sentence window
  was demoted the same way. Paragraph-sized ranges: 69 → 19 → 0. The two ranges
  still over 400 chars are single sentences that are genuinely that long.
- The emitter is now an EVENT WALK. Starts and ends come from one sorted list, so
  a range cannot get an end without a start, which is what the demotion rules
  were there to prevent. Verified: 203 starts, 203 distinct ids, 203 definitions.

## 0.3.0 — 2026-07-27 — real paragraphs, no section sigil, and comments carry the CHANGE

- **`--join-paragraphs`**: the sentences of each `####` block become ONE Word
  paragraph. The `.md` is one sentence per line, which is right for review and
  wrong for a manuscript: unjoined, `S-Main-all` was 423 double-spaced paragraphs
  and read as a list. Now 73, matching the `####` count. Off by default, so the
  nine per-section review files keep a sentence per paragraph, which is the point
  there. `####` had emitted no block at all, so joining had nowhere to break; it
  now emits a `pbreak`. Blank lines are NOT breaks: the dialect puts one between
  every sentence.
- Comment anchoring survived the join. A lane now carries the WINDOW of its own
  sentence, because `text.index(tok)` in a joined paragraph would find the first
  matching number in a DIFFERENT sentence. 260 comments before and after.
- **The `§` is stripped from headings.** It is Board notation; MISQ's contract is
  `1 MAJOR HEAD` / `1.1 First Subhead`. Zero remain in the document.
- **A comment carries the CHANGE, not a restatement (JL).** A `> Note:` lane holds
  a complete candidate sentence, which is right on the Board where the original
  sits above it, and wrong in a narrow Word margin where the prose is already on
  the page. Notes reduce to their edits: `across → from`. Value and Display lanes
  are untouched; neither restates anything. Ruled on `QC6@paper`.
- Two prose leaks closed, both found by hunting the last `§`: a pipe-table row and
  a numbered list item were gated on `not prev_was_para`, so one FOLLOWING a real
  sentence leaked into the manuscript. §5 shipped `| Variable | Definition |` and
  §7 shipped `1. Word budget (blueprint gap)…`.
- Staleness check rewritten. Comparing MTIMES was wrong: an editor save with no
  content change made the `.bib` newer than the cache, so it fired forever.
  Compares KEY SETS now, which is exact, immune to a touch, and names the keys.

## 0.2.0 — 2026-07-27 — the reference travels in the comment; the author is a per-run fact

- **A Citation comment now carries the REFERENCE, not just `key=`.** A coauthor
  reading a `.docx` cannot grep a `.bib`, so a bare key named something they had
  no way to look up. The text is read from `.board-refs.bbl`, which `refs.py`
  produced by running the PAPER'S OWN `.bst`, so the format is whatever the
  manuscript will print. Nothing is formatted twice here, so nothing can
  disagree; that is the same principle the in-text label already used.
- **Fixed a mangled-reference bug the moment references became visible.**
  `detex` matched `\enquote{...}` non-greedily, and a `.bib` protects capitals as
  `{U}nited {S}tates`, so the first title with a protected capital shipped as
  `"…in the U"nited States`. Replaced with balanced-brace extraction, applied to
  `\enquote`, `\textit`, `\textbf`, `\emph` and `\texttt`. Found on
  `guy2017vital`; zero stray-quote defects across §2's 38 references after.
  NOTE: `haipipe-board/src/dialect_paper.py:182` carries the same non-greedy
  pattern. It renders clean today, so the defect there is LATENT, not live.
- **`--author NAME` added; default stays `haipipe`.** JL ruled a real name must be
  available and that the caller ASKS rather than assumes. Initials are derived,
  so `--author "Junjie Luo"` shows as `JL` in Word's margin. The default is
  unchanged because `QC6` reasoned the author field IS the partition between
  machine provenance and a coauthor's markup; overriding it moves the partition
  to the lane-type prefix every generated comment already carries.
- Default output moved to `<paper-root>/3-dist/word/`, JL's naming. Numbered
  means machinery under the paper folder's delete test, which an export is;
  `dist` read as deliverable. Gitignored.
- Verified in real Microsoft Word by JL this session, which closes `QC6`'s
  "nobody has opened the output in Word" item: comments render, anchored, in the
  review pane, with the author shown.

## 0.1.0 — 2026-07-27

First version. Executes the `QC6` rulings made the same day on
`skills/diagrams/01-haipipe-paper-260725`, on JL's question: "Could we generate
the work with citaitons and the values as the comments? Do you know whther it is
doable?"

**Added**
- `md2docx.py`: one stage page's `## Content` to a `.docx`. Standard library
  only. Headings, prose, in-text citations, order-of-appearance Display
  numbering, embedded editable tables, embedded figures, a reference list, and
  the apparatus in anchored Word comments authored as `haipipe`.
- `SKILL.md`: the read-and-drop contract, the author-field law, and the two page
  shapes the exporter reports rather than repairs.

**Ruled here, and the reasons are measurements rather than preferences**
- The carrier is a native Word comment with `w:author="haipipe"`. The earlier
  objection was that review comments look like coauthor comments; the author
  field makes that a namespace, and Word's review pane already filters on it.
- The tool is `zipfile` + OOXML, NOT pandoc. Pandoc cannot write Word comments
  at all, so the obvious tool cannot carry the central feature. `python-docx` is
  absent on this machine and would add a dependency for a page of code.
- The in-text citation form is READ from `.board-refs.bbl`, not formatted. The
  `\bibitem[{…}]` bracket is the natbib in-text label, set by the paper's own
  `.bst`. This dissolves the field-versus-baked-text question: the baked text is
  not authored by anyone, so there is no second bibliography to keep true.
- A table becomes a real `w:tbl` parsed from the unit's `assets/table-body.tex`,
  because a coauthor cannot fix a typo in a picture of a table. Verified on all
  six MISQ table units: 108 rows parsed, zero TeX leakage, and `\multirow`, the
  construct that would have needed a vertical merge, appears in none of them.
- An unresolved `\cite{TOADD}` or `{VAL:? …}` WARNS and ships here, where the
  LaTeX column should block. The audiences differ: a reviewer must not see a
  hole, and a coauthor must.

**Two defects found by running it, both fixed in this version**
- The in-text label was printed whole, producing
  `(Wang et al.(2022)Wang, Luo, Dugas, Gao, Agarwal, and Werner)`. natbib packs
  `SHORT(YEAR)FULL` into one bracket; only the part up to the year is the
  in-text call.
- An overlapping comment anchor was pushed onto the whole-paragraph list AFTER
  that list's `commentRangeStart` elements had been emitted, so the comment got
  an End and a Reference with no Start. Invalid OOXML, caught by the package
  check as `start != end` on `S-Main-6`. Overlaps are now resolved before
  anything is written.

**Measured on the MISQ paper**
- `S-Main-4-measurement`: 70 paragraphs, 19 anchored comments, 2 tables, 1
  figure, 12 references.
- `S-Main-6-results`: 50 paragraphs, 38 anchored comments, 1 reference, and 0
  displays placed, which is a finding about the page rather than the exporter:
  its display references are `Table [main-results]` placeholders in prose while
  the real `\ref{}` sit in its `> Display:` lanes.
- Package validation on both: every `commentReference` id has a matching
  definition, a matching range start and a matching range end.

**Not yet verified**
- Nobody has opened the output in Microsoft Word. `textutil` parses the package
  and extracts the prose and the table cells, which shows the package is valid
  and a Word-family reader accepts it. It does not show that Word renders the
  comment bubbles.

## 0.9.2 · 2026-09-30 · Story parts are §N

- The compile order is the Story's §8 block, never "C8" (haipipe-paper-story 0.17.0; JL 260930, "go ahead and update them accordingly", on aligning the paper skills with the Paper Workbench).
- "Canonical configuration" is Configuration and the engine is the only delivery engine (AGENTS rule 9); the Round fixture in `tests/test_build_delivery.py` titles its division Feedback Concern Table.

## 0.9.1 · 2026-09-29 · outline/ to draft/ in current-layout prose (JL 260929)

- Paths that describe the current Page layout say `draft/`: the plan `draft/<stem>-draft-v<G>.<S>[.<E>].md`, records `draft/records/`, `draft/previous/`, `draft/skill/`, the Evidence Markdown `draft/<stem>-evidence-items.md`, `draft/evidence/bibex/` and `draft/evidence/materials/` (JL 260929: "it should be draft"). Mentions of legacy Pages, retired `outline/evidence/` lanes and the migration keep `outline/`, as do the OUTLINE stage, the Outline table and the `outline:` grammar key.

## 0.9.0 · 2026-09-29 · run-delivery-coverletter
- New lane (JL 260929 "we should also have a delivery cover letter ... run-delivery-coverletter"): `scripts/cover_letter.py`, called by `build_delivery.py` when paper-build.toml has `[coverletter]`. Words from the submission Round page's "Cover letter" division (its draft until adopted); facts filled by code; PDF via generated LaTeX and DOCX; checks for numbers against the manuscript text, required mentions, causal verbs, process text, the venue page cap, the author block and length; recorded under `cover_letter` in build-manifest.json and printed after the build.
- `profiles/misq.toml`: `page_cap = 55` and `cover_letter_must_mention` from the MISQ desk rules.
- `send` fix: `send RD<NN>` refused a MISQ paper because it demanded the supplement a manuscript-with-appendices never produces, and `section_snapshots = ""` resolved to delivery/ itself. Empty outputs and, under `appendices = "main"`, supplement outputs are now skipped; a not-ready letter is named when it travels with the Round.
- Tests: `test_cover_letter_lane_fills_facts_and_checks_the_words`, `test_send_skips_switched_off_outputs_and_an_absent_supplement`. Assemble tests: 66 pass.

## 0.8.4 · 2026-09-28

- ⛔ Hard rule under the title (JL 260928, AGENTS.md rule 6): never modify a generated file directly; change the code that writes it, then rerun.
- Word lane: an abstract that ends with a bold label (`\noindent\textbf{Keywords:}`, the MISQ shape) lost its
  prose, because `add_abstract` printed only from the first label on; Word showed the Abstract heading and then
  Keywords (JL 260928: "why I don't have the abstract"). The unlabelled lead is now printed first. The PDF was
  never affected. Test: `test_abstract_prose_before_a_keywords_label_reaches_word`.
- Word lane: the table header fill was hard-coded `F2F4F7` for every venue. It is now the profile key
  `table_header_fill` (default unchanged); `profiles/misq.toml` sets it to `""`, matching the co-author's official
  MISQ file and the v0728 submission, which have no cell fill (JL 260928: "why the header is with color?").
  Test: `test_table_header_fill_follows_the_profile`.
- MISQ follows the co-author's official-format Word file (`delivery/word-feedback/`, measured from its styles.xml and
  document.xml; JL 260928: "Title abstract and keywords should be in the first page" and "does this really following
  the MISQ word template?"). New profile keys, all defaulting to the old behaviour: `front_matter =
  "title-abstract-keywords"` (page 1 = Title style, centred ABSTRACT, single-spaced abstract and Keywords, then a page
  break), `abstract_line_spacing`, `heading_align = "center"`, `caption_plain` (bold upright black captions),
  `table_borders = "horizontal"` (no vertical lines) and `table_font_size = 8`. Word tables now print the float's
  `\begin{flushleft}` note under the table (the PDF always did). The MISQ LaTeX lane uses `title_page = "inline"`, so
  the PDF's page 1 also carries the title, abstract and keywords. Test:
  `test_misq_official_layout_front_page_tables_and_notes`.
- Word title: python-docx's built-in Title style is dark blue with a blue rule under it; the style is now black with
  no border for every venue (JL 260928 screenshot: "is this following the MISQ template with the underline and color?").
- Word tables (JL 260928 "The table is just not good"): every column got max(900, 9360/n) twips, so a 13-column table
  overflowed the line and its last column went negative ("Low%" one letter per line). `column_widths()` now sizes
  each column to its own content (row labels at least 10 characters), sums exactly to the line, and keeps every
  column at 450 twips or more. `\multicolumn` group headers are merged across their columns and centred
  (`merge_spanned_cells()`, spans from `parse_table_spans()`), as in the official-format file. Test:
  `test_wide_table_fits_the_line_and_group_headers_merge`.
- Word tables, second pass (JL 260928 screenshots: "0.207" printed as "0.20/7", "RMSE" as "RMS/E", and "Why I have
  this?" on a table split across a page): widths now measure the longest unbreakable piece of each column at the
  table's font size (a hyphen is a break point, so a model name does not claim the whole line), give that piece
  room first, and may run up to 10,400 twips into the margins, centred, when the line cannot hold it. Cell padding
  is 60 twips. Every header row above the first `\midrule` repeats on a continued page (`count_header_rows()`),
  no row splits across a page (`w:cantSplit`), and a table of 25 rows or fewer is kept on one page.
- Word equations (JL 260928: "The equation is not in the good format as well"): `$$…$$`, `\[…\]`, `equation` and
  inline `$…$` were flattened to text ("Y_ijc(o) = β_c(o) H_j + … + _ijc(o)", ε lost). They now go LaTeX → MathML
  (`latex2mathml`) → OMML (`_mathml_to_omml()`) and print as native Word equations, display ones centred; text is
  the fallback only when a formula cannot convert. Test: `test_equations_become_word_equations_and_header_rows_repeat`.
- Word text: `latex_to_text()` knew ten Greek letters, so `\Delta` in a table header was dropped by the generic
  command stripper and printed "HDLD ( pp)". `TEX_SYMBOLS` now covers the Greek alphabet and the common relations,
  matched as whole command names (`\mu` no longer eats the front of `\multicolumn`). Test:
  `test_math_symbols_in_table_cells_survive`.
- Verbatim blocks (JL 260928 appendix screenshot, "the appendix here seems not that good in the format"): the published
  prompt in `\begin{verbatim}` reached Word as double-spaced prose with its lines joined and the word "verbatim"
  printed, and in the PDF its long lines ran off the right edge. Word: `VERBATIM_PATTERN` lifts the block out before
  any other parsing, `strip_comments` keeps a `%` inside it, and `add_code_block()` prints a framed one-cell box, one
  paragraph per source line, Courier New 9 pt, single-spaced, indentation kept, a two-character hanging indent on a
  wrapped line; the box carries `w:tblDescription="verbatim"` so `docx_table_count` does not count it as a table.
  LaTeX: the master loads `fvextra` and makes `verbatim` single-spaced, `\small`, framed, and wrapping at spaces.
  Test: `test_verbatim_prompt_is_a_framed_box_line_by_line`.
- Word prose and table notes print `\textbf` bold and `\textit`/`\emph` italic (`mark_emphasis()`); they were plain, so
  "Agreeableness specification" lost its bold and every table's italic "Note." was upright. Test:
  `test_bold_and_italic_reach_word_prose`.
- Blind copy has no acknowledgments: every build printed "[Acknowledgments, funding and disclosures are written at
  submission; this build is a draft.]", process text in the deliverable, and on a blind MISQ copy the section itself
  would unblind the authors. New `[latex] acknowledgments` key (default true); `profiles/misq.toml` sets it false. The
  Word lane used that heading as the end of the main text; it now falls back to the bibliography. Test:
  `test_blind_copy_without_acknowledgments_still_converts`.
- Title acronyms keep their capitals: apalike lowercases titles, so the reference list printed "Online Reviews with
  llms". The bib merge now braces every title word with two or more capitals (`protect_title_acronyms()`); braced text
  is left alone and no warning is raised.
- `draft-sections/` can be switched off (`[outputs] section_snapshots = ""`), JL 260928: "why it is not the same to each
  section's word? and no references". Those files were a second, reference-less copy of each Section Page's own Word
  file. Test: `test_section_snapshots_can_be_switched_off`.
- No content hashes (JL 260928: "Why we have the sha256? remove that, waste my tokens"): `build-manifest.json` carried
  74 sha256 values that nothing read. It now lists inputs by path only; a version is its number and date, and a stale
  fragment is still found by file time. SKILL.md no longer asks for hashes either: the outline record, evidence lock,
  Round snapshots and the stale-build audit use paths, versions and the manifest's `built` time. Assemble tests: 64 pass.

## 0.8.3 · 2026-09-28

- The build merges the Bib the Page export actually writes, `delivery/latex/selected-bibliography/<page>.bib`.
  Since the 09-20 export refactor no Page writes `<page>-complete.bib`, so a full build merged a stale
  09-13 copy for the Introduction and stopped at Literature Review. The page-PDF readiness check no
  longer accepts a stale `<page>-complete.pdf` either. Flagged by the S-MISQ-Main-5-Results session.
- SKILL.md and haipipe-paper-section name the current Page delivery files: `<page>.tex` (fragment),
  `<page>-master.tex` → `<page>.pdf` (standalone), `selected-bibliography/<page>.bib`.
- A fragment's page-relative `\input{…}` / `\includegraphics{…}` that is not a display unit is rewritten
  to resolve from the master's folder (`from_master`), with a warning when it reads a retired `_archive`
  lane. Before, it was copied into `sections/` unchanged and latexmk stopped at `File ../../… not found`
  (Paper-AgreeableRxDiscretion session, 260928). Test: `test_page_relative_inputs_resolve_from_the_master`.
- `merge_bib` writes every `&` for LaTeX (`latex_safe_entry`): `&amp;` copied from a web page, a doubled
  `\\&`, or a bare `&` becomes `\&`; inside url/doi `&amp;` becomes `&`; one warning names the key and
  Page. `Sinnenberg_2017` (`MDM Policy &amp; Practice`) had stopped BibTeX. Test:
  `test_html_ampersand_in_a_merged_bib_is_written_for_latex`. A scratch copy of the MISQ paper now
  builds: 63 pages, PDF and Word.
- One build at a time per `delivery/` (`delivery_lock`, around `build` and `send`/`release`): two builds in
  one folder had regenerated `latex/` under each other (79 undefined citations). A second build prints
  who holds the lock, waits up to 10 minutes, then stops. The lock is an OS file lock, released even on a
  crash, on a file in the system temp folder named by the `delivery/` path, so no paper repo gains a
  lock file. Test: `test_one_build_at_a_time_per_delivery_folder`; two real builds started 1 s apart on a
  scratch copy ran one after the other, both clean.

## 0.8.2 · 2026-09-28

- New profile key `appendix_float_numbering = "per-appendix"`: appendix tables and figures restart in
  each lettered appendix (Table A1 … Table B1 …), the MISQ convention. The LaTeX lane writes
  `\counterwithin*{table}{section}` with `\thetable = \thesection\arabic{table}` after `\appendix`; the Word lane
  numbers captions AND in-text `\ref`s the same way (before, Word captions said "Table A7" while the text
  that cited them used one running counter across the whole paper). Default stays "continuous".
  Test: `test_per_appendix_numbering_restarts_under_each_letter`.
- A DISPLAY `result.yaml` written in JSON form (valid YAML) is now read like the YAML form (`_result_text`).
  Before, the line readers missed it: the unit was never placed, the fragment kept its page-relative
  `\input{../../results/...}`, and latexmk stopped (AgreeableRx §5, 260928). Test: `test_json_form_display_result_is_found`,
  failing before the fix.

## 0.8.1 · 2026-09-27

- A build refused for a cited Page without `delivery/latex/<page>-complete.bib` no longer deletes the
  last good `delivery/latex/` first: `require_page_bibs` runs before the folder is cleared (a DrFirst
  paper lost `master.pdf`, `master.tex` and `reference.bib` to a refused build, restored from backup).
  The plan header reader accepts `draft-version:` beside `outline-version:` (Page layout 0.118).

## 0.8.0 · 2026-09-20

- Validate required config and generated paths before mutation; correct the config example. Bind commissioned builds to the compile Spec. Merge Page delivery bibliographies, preserve stable Section identities and label MISQ thresholds as local guidance. Add path/bibliography regression coverage.

## 0.7.9 · 260908
- **The WORD lane followed the venue for the first time.** The LaTeX lane has always taken `bibstyle` from the profile, while `latex_room_to_docx.py` emitted numbered Vancouver citations (`[1,2]` and a numbered reference list) for EVERY profile, so a MISQ submission was going out with medical-journal citations. Caught by diffing the generated .docx against the co-author's `MISQ-Official-Format.docx`, which is APA author-date throughout (JL 260908: "is the word fit the misq template as well?").
- New `citation_style = "author-date"`: in-text `(Barnett et al., 2017; Hoppe et al., 2017)`, one/two/three-plus author forms, and an alphabetical unnumbered reference list in APA (`Barnett, M. L., Olenski, A. R., & Jena, A. B. (2017). Title. Journal, 376, 663-673. https://doi.org/...`). Default stays `numeric`, so JAMA and the medical profiles are untouched. Our first two entries now match the official file character for character.
- New `appendices = "main"`: Appendix A-E sit inside the one manuscript after the references, which is what MISQ does; the separate ONLINE-ONLY supplement file is the medical convention. When appendices go in main the supplement is not written and a stale one is deleted, so it cannot be submitted by mistake.
- Appendix level-1 headings carry their letter and keep their case (`Appendix A. Agreeableness Task-Specific Prompt`), the way LaTeX's `\appendix` letters them; Word had printed the bare title in caps. All five now match the official file word for word.
- `title_page_fields = ["title"]` for MISQ: the manuscript is a BLIND copy, so authors, affiliations and the corresponding author leave the file entirely and live in ScholarOne's metadata.
- Verified side by side against the official-format file: font, size, spacing, margins, line numbers, 16 tables, 2 figures, 38 Heading2s, 5 appendices, 0 numeric citations, 0 front-matter placeholder blocks all identical; in-text author-date 109 vs 111, the 2 extra being the co-author's own inline notes.

## 0.7.8 · 260908
- **The venue PACK reaches the build.** `haipipe-paper-venue`'s store already held a measured MISQ pack (`venue/playbook-utd-is/MISQ/`, abstract 120-160 words and never past ~185, 4-7 sentences of unstructured prose, 40-50 pages, hero display = the research-model figure, measured 2026-07-08 from published MISQ Research Articles) while `profiles/misq.toml` was written from general knowledge and nothing read the pack (JL 260908: "Don't we have it in the haipipe-paper-venue???"). The profile now carries those numbers with their source path, and `venue_findings()` checks them: the paper's 168-word 10-sentence abstract had passed every gate.
- **`profiles/misq.toml` said `layout = "generic"`, and "generic" in `latex_room_to_docx.py` WAS the medical-journal title page.** The MISQ .docx shipped `Running title:` with no value under a profile declaring `running_head = false`, an `Article type` line, a main-text word count, a display count, an empty `ARTICLE HIGHLIGHTS` heading, and `TABLES` / `FIGURE LEGENDS` sections after the references. Two of those are build counts inside a deliverable, which JL ruled out on 260908.
- New profile keys, all defaulting to the previous behaviour so no other venue changes: `title_page_fields` (ordered, validated field names), `author_placeholder`, `displays_position` (`inline` places displays where the prose cites them, with `main_table_prefix` / `main_figure_prefix`), `highlights_heading`, `tables_heading`, `figures_heading`. An empty section heading is never written.
- **The Abstract page's `### Title` is the title's authority**; `paper-build.toml [paper] title` is the fallback. Both carried one and they drifted, so the PDF and .docx printed "Physician Personality and Opioid Prescribing" while the page said "Physician Agreeableness and Opioid Prescribing". A mismatch is a finding.
- The abstract word count cuts the keyword line from the RAW tex first: stripping `\textbf{Keywords:}` leaves the 18 bare keyword words, which counted a 168-word abstract as 186.
- Both new teeth live INSIDE `display_register()`, not in `build()`, because a tooth the caller has to remember is a tooth the test harness runs without. 28 teeth, all green.
- Verified against this desk's own MISQ submission (`Bc-MISQ-Round/RD01/feedback/MISQ-PhyTrait-Opioid-Main-v0728.docx`): Times New Roman, 12 pt, `w:line=480 auto` (double), `pgMar 1440` twips (1 in) on all four sides, tables interleaved with the prose. The generated .docx now matches all five.

# CHANGELOG · haipipe-paper-assemble

## 0.7.7 · 260908
- Register tooth for ONE WORK under TWO bib keys. `merge_bib`'s existing tooth only sees a key COLLISION; two pages that spell the same article differently collide on nothing, both reach `\bibitem`, and apalike prints it as `2018a` + `2018b` with two entries in the reference list. Found live in Paper-AgreeablePrescriptionDiscretion: §1 cited `Buchmueller_2018`, §2 cited `buchmueller2018pdmp`, same DOI `10.1257/pol.20160094`, and 0 findings were reported. Identity = the DOI when the entry carries one, else first author's surname + 28 letters of the title, so `{M}edicare` brace-protection and title casing do not hide it. Both keys cited = a finding; the spare staged but uncited = a warning, because nothing prints twice yet. New `bib_entries()` (brace-balanced) + `duplicate_bib_works()`; `display_register` now collects cited keys while it walks `master.tex`. 26 teeth, both proved by expect-fail.

## 0.7.6 · 260908
- Register prints what LaTeX numbers: every unstarred `\section{` per placed fragment is counted in `\input` order (a stub counts one); a page printing more than one is a finding (`inner divisions should be \subsection`), found by Paper-JAMA-Board when md2tex's `###` mapped to `\section` and shifted every later number. 24 teeth.

## 0.7.5 · 260908
- Third naming pass (JL 260908 "okay, good, this might be much better"): the Section PAGE id carries the index (`S-<desk>-Main-<N>-<Title>`, `S-<desk>-Appendix-<L>-<Title>`, unnumbered pages keep title only) and the UNIT drops every prefix (`Display<n>-<slug>`); delivery mirrors the page (`displays/<page-id>/<unit>/`). Every engine key is `<page-id>/<unit>`: `copy_unit`, `place_fragment` rewrites, `EMBEDDED_UNITS`/`PLACED_FLOATS`, `label_to_unit`, page-scoped `declared_number`, register rows and findings. New `page_index()` / `is_abstract()`; the JAMA heading kind strips the index; printed section numbers now count unstarred `\section{` in \input order (an unnumbered page prints none). Register teeth: folder index ≠ H1, numbered H1 without index, index on unnumbered H1, prefixed unit, unit without README. Tests and the docx room fixture follow the grammar.

## 0.7.4 · 260908
- Display unit folder grammar is `Sec<N>-Display<n>-<slug>` / `App<L>-Display<n>-<slug>` (JL 260908: "it is too long, how about we just use the section index", after 0.7.3's `<PageID>-Display<N>-<slug>`). The register derives the expected prefix from the owning page's H1 via `page_heading()` and flags: legacy names (`S-Display-*`, `<PageID>-Display-*`), a right-shaped name whose Sec/App does not match its page, a page with units but no §/Appendix in its H1. Cost written into the law: a moved compile order renames the units under that page.

## 0.7.3 · 260908
- Display unit folder grammar `<PageID>-Display<N>-<slug>` is a register tooth (JL 260908 "unify them", relayed by Paper-JAMA-Board): every unit folder on disk is scanned, a `S-Display-*` or other non-conforming name is a `legacy unit name` finding, a unit without README.md is a finding. New "🗂 Display unit folders" section.

## 0.7.2 · 260908

- Round snapshots now freeze every output declared in `delivery/paper-build.toml`,
  including supplement PDF/DOCX when present, plus the display register.
- `send` and `release` refuse missing outputs and refuse to overwrite a
  populated `sent/` or `released/` directory; an immutable snapshot must be
  cut into a new or explicitly migrated Round.
- The receipt reference is the Round's `outline/` close record, not a retired
  on-page `## Log` section.

## 0.7.1 · 260908

- **Word tables arrive** (Paper-MISQ-Board: 3 of 4 main tables and 7 of 12 appendix tables reached Word as a caption with nothing under it, or not at all). `parse_table_rows` in `scripts/latex_room_to_docx.py` is brace-aware: the column spec is read as a balanced group (`p{3cm}`, `@{}`, `>{…}`, `*{6}{X}`, `tabularx`/`tabular*` width argument, `longtable`, `array`), rows split on `\\` only at depth 0 (`\shortstack` stays one cell), `\multicolumn{n}` pads `n-1` cells. The old regex `\{[^{}]*\}` returned no rows for any nested-brace spec.
- Supplement displays are numbered (`Table S1.`, `Figure S1.`; profile keys `supplement_table_prefix` / `supplement_figure_prefix`) instead of printing an unnumbered caption.
- New tooth `build.checks.tables_rendered`: `<w:tbl>` count per `.docx` vs the table displays emitted vs the master's table floats; a mismatch exits non-zero after the files are written. `tests/test_latex_room_to_docx.py` drives the real engine over a room with the failing column specs (3 tests, incl. the expect-fail on the old regex).

## 0.7.0 · 260908

JL: "you go ahead to think how to make it as clean as enough." One pass over the whole engine.

- **Venue profiles reach LaTeX.** `profiles/<name>.toml` now carries a `[latex]` table read by `write_master()` (spacing · bibstyle · displays inline|end via endfloat · appendix_newpage · title_page inline|separate · abstract_page · running_head); `[profile]` in paper-build.toml overrides single keys. New `profiles/misq.toml` (double-spaced, blind title page, abstract page, lettered appendices on new pages), asked for by Paper-MISQ-Board after JL: "did you use the MISQ template?". A paper with no profile builds as before.
- **A display prints once in the whole document.** `prescan_embedded()` + `EMBEDDED_UNITS`/`PLACED_FLOATS`: a page that `\ref`s a float another page embeds never re-inputs it, whichever page comes first (tooth parametrised over both orders).
- **The reader's document is clean for every profile.** The header carries the status word only; a not-ready page prints its own numbered heading plus one neutral line, `_stub()`; reasons, counts and build time live in build-manifest.json and the register.
- **Bib key collisions warn.** Same key, different entry on two pages → document `warnings` (first page's entry kept) in the manifest and on the console.
- **Missing tools are reported, not crashed.** `_run()` turns a missing `latexmk` or Word engine into `rc 127` with a message; the manifest and register are still written.
- **Smaller:** `[pages].appendix` optional; `freeze` refuses without a built PDF and also freezes `display-register.md`; a display unit folder present on two pages is a register finding; `tests/run.sh` runs the teeth from the right directory. 17 teeth.

## 0.6.2 · 260908

- Readiness rule (JL 260908, second defect found by Paper-MISQ-Board): a display unit gates a page only when the page CITES it (unit name in the fragment or `.md`, or a `\ref` to one of its `float.tex` labels) AND the unit is LIVE (no `state: 🟣`, not retired/folded under `## Placement`). Uncited or folded units are reported under the page's new `warnings` and never block. Before: every folder under `display/` demanded a preview.pdf, so a folded `S-Display-3a-funnel` blocked a fully written §4.
- `warnings` per page in the manifest and on the console: also `fragment may be stale` when the page `.md` is newer than its `delivery/latex/<page>.tex` (a warning, not a blocker; mtimes lie after clone or rename sweeps).
- Four teeth added: uncited-no-preview does not gate; folded-no-preview does not gate; cited live no-preview still gates; stale fragment warns and stays ready.

## 0.6.1 · 260908

Paper-level opt-ins in `scripts/build_delivery.py`, driven by `paper-build.toml`; a paper that declares none of them builds exactly as 0.6.0.

- `[evidence] draft_includes_unready = true`: a DRAFT prints every page that has a body fragment, prefixed `[DRAFT PAGE · reason]`, instead of a titled stub. Readiness accounting, the SUBMISSION-CANDIDATE rule, and the display register are unchanged. First user: Paper-AgreeableOpioid-Jama, whose 11 pages are all v0.x but hold a complete draft.
- `[source] preamble = "preamble.tex"`: a paper-owned preamble beside `paper-build.toml` is inlined into the generated master after the engine's own packages, so a page fragment's `longtable`, `seqsplit`, `needspace`, `tikz`, column types, or unicode maps no longer break the whole-paper compile. The engine also always provides `\displayroot` (`displays/`) and loads `xcolor`.
- `venue_profile = "jama-internal-medicine"` now shapes the master the JAMA Word renderer parses: a title-page `center` block instead of `\maketitle`, a `\section{Introduction|Methods|Results|Discussion}` boundary before any main fragment that lacks it, and the Abstract page's own `\section*{Key Points}` / `\section*{Abstract}` kept rather than rewritten into an `abstract` environment.
- Display units in the flat layout (`figure.pdf`, `table-body*.tex`, `float.tex` at the unit root) are copied and retargeted like `assets/` units; a fragment's `\input` of `display/<unit>/float` or `…/table-body` resolves either way.

Fix (same day, 4929a597 follow-up): the `included` flag was set only inside `build()`, so a caller that hands `write_master` a ready page directly (the engine's own tests do) got no `\input` and the register counted 0 floats; inclusion now defaults to readiness (`p.get("included", p["ready"])`), suite 6/6.

JAMA supplement numbering (same day): under `venue_profile = "jama-internal-medicine"` the generated master resets the table and figure counters after `\appendix` and renames them `eTable` / `eFigure`, so supplement floats print `eFigure 1…` as the desk expects; other profiles are untouched, suite 6/6.

Clean deliverables (same day, JL: "the delivered pdf or word must be clean"): the in-body `[DRAFT PAGE · reason]` tag that `draft_includes_unready` printed is gone for every profile; a page's not-ready reasons live only in `build-manifest.json` and the display register. Under the JAMA profile the running header carries the status word alone (`DRAFT` / `SUBMISSION-CANDIDATE`), without page counts or build time; other profiles keep the 0.6.0 header. Suite 10/10.

Verified on both papers: Paper-AgreeableOpioid-Jama 25-page PDF + main and supplement DOCX (latexmk 0, docx 0); Paper-AgreeablePrescriptionDiscretion unchanged at 23 pages, 5/14 ready, `\maketitle` and `abstract` environment intact.

## 0.6.0 · 260908

- One engine `scripts/build_delivery.py` (was paper-local `delivery/build.py`
  in every paper); papers install the thin wrapper `ref/build.py.wrapper` as
  `delivery/build.py`. Three behaviors found by Paper-MISQ-Board in one paper
  copy now ship for all: A display printed once (`DEDUPE_EMBEDDED_FLOATS`),
  B a not-ready page keeps its number via `page_heading()`, C the display
  register `delivery/display-register.md` + manifest `displays` block counting
  what the master prints, with four teeth. `tests/test_build_delivery.py`
  carries a tooth per behavior and the expect-fail run for A.
- Engine version is read from this file's frontmatter and stamped into
  master.tex, the register, the bibliography and the manifest.

## 0.5.0 · 260907

- Reading order comes from the Story page's `haipipe:compile-order` block
  (`[pages].order = ../A1-Story/Story-<letter>/Story-<letter>.md`), never from a
  Narrative page: Roadmap and Narrative retired 260907 (haipipe-paper-workflow
  1.0.0). A retired Narrative's 📖 section map is parsed only as a legacy
  fallback so an archived page can be rebuilt for comparison; the board roster
  is the last resort. Written by Claude Peer.
- `delivery/build-manifest.json` is the sole delivery receipt; the former
  sibling delivery-QA report is no longer generated.

## 0.4.0 · 260907

- Paths in `paper-build.toml` resolve relative to `delivery/`; the page
  milestone and ON SEND / ON ROUND CLOSE protocol as shipped.

## 0.3.0 · 260907

- Source of record moves from the desk room to the Section Pages (JL 260907):
  the build reads each page's `delivery/latex/<page>.tex` fragment in the
  Narrative's order, regenerates `delivery/latex/` whole (master.tex,
  sections/, appendices/, displays/, reference.bib) and converts
  `delivery/word/` from it. `paper-build.toml` lives at `delivery/` and gains a
  `[pages]` block; the latex-room adapter is unchanged, so grandfathered desk
  rooms still build.
- New "🏁 The milestone that admits a page": outline tick + display PDFs +
  page PDF, else the page is reported not ready and the build is DRAFT.
- Build protocol ends with ON SEND (copy into the Round's `sent/`) and ON
  ROUND CLOSE (copy into `released/`).

## 0.2.1 · 260904
- Added config-driven LibreOffice PDF twins for the main manuscript and
  supplement, with renderer availability/errors in QA and output hashes in the
  manifest.
- Added an explicit read-only audit route so provenance/staleness checks do not
  accidentally regenerate delivery artifacts.

## 0.2.0 · 260904
- Added a profile-driven JAMA Internal Medicine renderer and a reusable TOML
  profile location.
- Added optional Section-generated evidence-lock preflight: provenance/state
  are checked without inserting prose, values, citations, or displays; final
  builds fail on unresolved evidence.
- Added shared receipt/QA reporting of evidence status and a DRAFT/CANDIDATE
  distinction based on unresolved evidence.

## 0.1.1 · 260831
- Tracking tree points at Ba-<desk>-Main (three-group desk layer, JL 260831: B<x>-<desk>-Main/-Appendix/-Round; a combined B<x>-<desk> group is grandfathered).

## 0.1.0
- First cut: source-driven assembly contract (desk-room source, venue profiles, DOCX/PDF/supplement artifacts, source manifests; never a generated Word file as input).

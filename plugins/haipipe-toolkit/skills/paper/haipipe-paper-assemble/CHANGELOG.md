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

- Canonical engine `scripts/build_delivery.py` (was paper-local `delivery/build.py`
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

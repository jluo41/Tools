# CHANGELOG · haipipe-paper-assemble

## 0.6.1 · 260908

Paper-level opt-ins in `scripts/build_delivery.py`, driven by `paper-build.toml`; a paper that declares none of them builds exactly as 0.6.0.

- `[evidence] draft_includes_unready = true`: a DRAFT prints every page that has a body fragment, prefixed `[DRAFT PAGE · reason]`, instead of a titled stub. Readiness accounting, the SUBMISSION-CANDIDATE rule, and the display register are unchanged. First user: Paper-AgreeableOpioid-Jama, whose 11 pages are all v0.x but hold a complete draft.
- `[source] preamble = "preamble.tex"`: a paper-owned preamble beside `paper-build.toml` is inlined into the generated master after the engine's own packages, so a page fragment's `longtable`, `seqsplit`, `needspace`, `tikz`, column types, or unicode maps no longer break the whole-paper compile. The engine also always provides `\displayroot` (`displays/`) and loads `xcolor`.
- `venue_profile = "jama-internal-medicine"` now shapes the master the JAMA Word renderer parses: a title-page `center` block instead of `\maketitle`, a `\section{Introduction|Methods|Results|Discussion}` boundary before any main fragment that lacks it, and the Abstract page's own `\section*{Key Points}` / `\section*{Abstract}` kept rather than rewritten into an `abstract` environment.
- Display units in the flat layout (`figure.pdf`, `table-body*.tex`, `float.tex` at the unit root) are copied and retargeted like `assets/` units; a fragment's `\input` of `display/<unit>/float` or `…/table-body` resolves either way.

Fix (same day, 4929a597 follow-up): the `included` flag was set only inside `build()`, so a caller that hands `write_master` a ready page directly (the engine's own tests do) got no `\input` and the register counted 0 floats; inclusion now defaults to readiness (`p.get("included", p["ready"])`), suite 6/6.

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

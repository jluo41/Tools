# CHANGELOG · haipipe-paper-assemble

## 0.5.0 · 260907

- Reading order comes from the Story page's `haipipe:compile-order` block
  (`[pages].order = ../A1-Story/Story-<letter>/Story-<letter>.md`), never from a
  Narrative page: Roadmap and Narrative retired 260907 (haipipe-paper-workflow
  1.0.0). A retired Narrative's 📖 section map is parsed only as a legacy
  fallback so an archived page can be rebuilt for comparison; the board roster
  is the last resort. Written by Claude Peer.

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

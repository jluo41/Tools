# CHANGELOG · haipipe-paper-assemble

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

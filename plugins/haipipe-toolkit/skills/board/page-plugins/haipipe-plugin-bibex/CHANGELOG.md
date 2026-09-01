# haipipe-plugin-bibex · Changelog

## 0.2.0 · 2026-09-01

- Added Discovery aggregate authority mode: each completed Result owns one
  primary Bib entry; the Topic Page Bib is a deterministic derived union.
- Key/DOI conflicts hard-fail and corrections land in the owning Result Bib.
- Complete Discovery Results record the verbatim Bib source in runtime;
  metadata-only input cannot be formatted into a new entry.

## 0.1.1 · 2026-08-31

Category-folder sweep: lane paths read `<page>/evidence/<lane>` or
`<page>/delivery/<lane>` (haipipe-page 0.47.0 §📁); flat names are the same
lane during migration (stubs).


## 0.1.0 · 2026-08-15
- Initial draft, round 2 of the thin-door migration (JL 260815): every live QPf plugin gains its skill; delta-only over haipipe-plugin.

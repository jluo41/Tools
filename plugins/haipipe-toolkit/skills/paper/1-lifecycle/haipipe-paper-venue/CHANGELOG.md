haipipe-paper-venue — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [3.2.0] -- 2026-07-08

- added ref/venue-template.md (fill-in 2-venue.md skeleton, matching sibling stage templates) with a provenance header (pack slug @ _venue commit, outlet dir, blueprint-derived date) for staleness detection; SKILL.md Artifact Spec slimmed to point at it; fixed overclaims (downstream stages stated as intended consumers, not current readers); output-contract example writes pack slug + outlet dir; Boundaries block gains display + section-edit rows; new `refresh` mode re-transcribes blueprint from the current pack without re-opening the pin; downstream stage skills repointed to read 2-venue.md first (packs = fallback + deep-dive only).

## [3.1.0] -- 2026-07-08

- resynced to the audited _venue packs: label->pack map rewritten (nature pack = NMI/NatComm/NatMed/npjDM/NHB, not Nature/Methods/Biotech; clinical-medicine -> medical-journals; MS-Marketing + jama-netopen added); blueprint derivation now transcribes per-section style.md Micro-norms (measured paragraphs, sentences/paragraph, words/sentence, citation density) instead of re-mining exemplars; outlet scoring reads <journal>/taste.md desk signals; dead exemplars/ paths -> <journal>/examples/; pack-less venues explicitly no-op. (Note: 2.x-3.0.0 entries were never logged here; version numbers follow SKILL.md frontmatter.)

## [1.1.0] — 2026-06-22

- added --no-pin advisory mode + topic-only worked example (from fresh-agent validation); resolution map updated for the utd-is merge and jama-portfolio rename.

## [1.0.0] — 2026-06-22

- new venue-selection front door; reads _venue/playbook-* packs, ranks fit, pins STATUS venue, owns label->pack resolution.

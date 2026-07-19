haipipe-paper-venue — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 3.4.0 — 2026-07-18 — charter reshape: resource-shaped venue + 2a-venue rename

Adopted the stage-template charter (`../../TEMPLATES.md`, JL 2026-07-18). Venue reshaped to mirror resource — a determination + its downstream requirements — and carries the Option A `2-venue` → `2a-venue` rename.

Changed (`ref/venue-template.md`)
- Six blocks (Venue Choice · Venue Profile · Structural Blueprint · Writing Principles · Fit Assessment · Probes) → FOUR sections:
  · **Venue Decision** — which venue + WHY + ranked suggestion (backups, nearest rejected) + audience + desk test + desk-reject risks + which claim hits which reward, as RECORD LINES (the old Fit Assessment PIPE TABLE removed, per JL's no-pipe-tables rule).
  · **Relevant Files** — NEW (JL): the packs/guides the decision + requirements rest on, made explicit.
  · **Requirements (what the final paper must do)** — the "results for the final template": Structural Blueprint + Writing Principles, transcribed + source-tagged.
  · **Q-consumer** — uniform `## Q-Venue-<n>` + Description/Reason/Answer.
- Charter conformance: unwrapped the old ```text fence + `# venue-template.md` header; fill rules → `<!-- RULE -->` comments (absorbing the old "## Rules": transcribe-don't-invent, hard-caps, carry-caveats, staleness, retarget); ANSWERABLE+specific rule; inline `[Q-Venue-1]` citation. Venue's transcribe discipline survives as RULE guidance.

SKILL.md
- CORE QUESTION added (charter C6): "which venue does this paper target, and what does that venue REQUIRE of the final paper?".
- Content structure six-blocks → four-sections; description/summary "Probes" → "Q-consumer", "venue profile" → "venue decision"; `2-venue:` title → `2a-venue:`; `serves: 2-venue` → `serves: 2a-venue`; done-criteria updated (Fit record-lines, Q-Venue-<n>, RULE-comments-deleted); v3.3.0 → 3.4.0.


## 3.3.0 — 2026-07-14

- "PPNN cards" / "probe plans" -> question SECTIONS in the probe files; the done-criterion asks for a raised or answered SECTION.

## [3.2.0] -- 2026-07-08

- added ref/venue-template.md (fill-in 2a-venue.md skeleton, matching sibling stage templates) with a provenance header (pack slug @ _venue commit, outlet dir, blueprint-derived date) for staleness detection; SKILL.md Artifact Spec slimmed to point at it; fixed overclaims (downstream stages stated as intended consumers, not current readers); output-contract example writes pack slug + outlet dir; Boundaries block gains display + section-edit rows; new `refresh` mode re-transcribes blueprint from the current pack without re-opening the pin; downstream stage skills repointed to read 2a-venue.md first (packs = fallback + deep-dive only).

## [3.1.0] -- 2026-07-08

- resynced to the audited _venue packs: label->pack map rewritten (nature pack = NMI/NatComm/NatMed/npjDM/NHB, not Nature/Methods/Biotech; clinical-medicine -> medical-journals; MS-Marketing + jama-netopen added); blueprint derivation now transcribes per-section style.md Micro-norms (measured paragraphs, sentences/paragraph, words/sentence, citation density) instead of re-mining exemplars; outlet scoring reads <journal>/taste.md desk signals; dead exemplars/ paths -> <journal>/examples/; pack-less venues explicitly no-op. (Note: 2.x-3.0.0 entries were never logged here; version numbers follow SKILL.md frontmatter.)

## [1.1.0] — 2026-06-22

- added --no-pin advisory mode + topic-only worked example (from fresh-agent validation); resolution map updated for the utd-is merge and jama-portfolio rename.

## [1.0.0] — 2026-06-22

- new venue-selection front door; reads _venue/playbook-* packs, ranks fit, pins STATUS venue, owns label->pack resolution.

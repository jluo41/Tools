haipipe-application-advice — Changelog
=======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`.

## [1.8.0] — 2026-07-18

- Template alignment sweep: dropped the template's "How to use:" header line; Q-consumer questions renamed `## Q<n>` -> `## Q-Advice-<n>` (id carries the origin stage) + reshaped to the fixed 3-field form Ask / Why / Answer (`__TO_BE_FILLED__` == OPEN, else ANSWERED — the doc's only state). SKILL skeleton + formatting synced.

## [1.7.0] — 2026-07-17

- Q-consumer migration follow-up: the SKILL's artifact-section list still named the section `Probes` (a roster) — renamed to `Q-consumer` (## Q questions; APPROVE adds the 1-probes/ pointer + state), matching the template. (The earlier pass's grep missed these lines because they co-mention `1-probes/`.)

## [1.6.0] — 2026-07-17

- Q-consumer migration: template `Probes` tail -> `Q-consumer` (`## Q` blocks; rare on this rung).

## [1.5.0] — 2026-07-17

- Template D3: probe roster placeholder + label `status` -> `state`.

## [1.4.0] — 2026-07-17

- Removed the optional insight-KB deposit (`--deposit`); the ladder doc `1d-advice.md` is the sole record of W (insight KB retired as a deposit target).

## [1.0.0] — 2026-07-09

- NEW skill, born in the ladder restage (SOP-ladder-restage.md, JL 2026-07-09): rung 1d = the W rung and the ladder's DELIVERABLE. Paper delivers K, application delivers W (JL framing, 2026-07-09): principles are actionable directives derived from >=1 claim in the 1c ledger.
- W-actionability test on every P ("could the artifact stage write the exact move from this line?"); claim-restatements push back to 1c. Rejected section holds negative wisdom with the refuting claim.
- Settlement coupling: the venue's claims_settlement bar applies through derivations (light: weak-with-caveat ok, GAP-derived forbidden; full: supported only).
- Explicitly distinct from venue Artifact Principles: this doc is content-WHAT (venue-FREE, survives retarget); 2-venue.md is channel-HOW (venue-ALIGNED, rewrites).
- The ladder gate (batched CHECK for light/medium venues per the Stage Gate Protocol) lands at this rung. Insight-KB W deposits are ON-REQUEST only via `--deposit <Pnn>` (R7).
- ref/<stage>-template.md added (canonical artifact template, paper convention; JL follow-up 2026-07-09) + SKILL.md pointer line; draft worker 1.2.0 registry reads it at WRITE.

## [1.1.0] — 2026-07-09

- RENAMED principles -> ADVICE (JL ruling, same-day walkthrough: "rename the principles to advise... later we can use them or not use them"). Folder `1d-principles/` -> `1d-advice/`, skill `haipipe-application-principles` -> `haipipe-application-advice`, ids `P<n>` -> `A<n>`, template `advice-template.md`, maturity value `principled` -> `advised`, verbs `advice | advise | recommendation` (+ `principles` kept as legacy alias).
- ADOPTION semantics added (the ruling's second half): advice is counsel, not mandate — venue-ALIGNED stages record adopted/declined A-ids with a why; declined entries stay for the next venue/round; claim-audit chain is artifact -> adopted A -> C -> anchor. Adoption records live downstream, keeping this doc venue-FREE.
- Also dissolves the standing double-use with 2-venue.md "Artifact Principles" (channel-HOW) — the only "principles" left in the family.

## [1.2.0] — 2026-07-09

- Stage doc gains a Probes roster section, uniform across all rungs (bench finding, 01_sms_young_male: the user could not see 1a's probes in the stage doc while 0-seed.md listed its roster; only seed + 1c-claims had one). One line per PP -- question + status -- matching _PROBE/ on disk; done-criteria now require roster-matches-disk. Rare on this rung (derivation is in-stage work); may be empty.

## [1.3.0] — 2026-07-09

- EXPLORE|EXPLOIT ADOPTED (JL, breadth/flywheel discussion 2026-07-09 — resolves the parked derivation-bars + role-tag thread archived in ../../../haipipe-application/CHANGELOG.md): every A entry carries a role. Exploit entries take the settlement bars (bars now scope to exploit). An explore entry is a deliberate test-to-learn bet: it may derive from weak/GAP claims PROVIDED the tag is visible, it names the C its deployed arm will settle (Settles: C<n> via iterate), and it states its compliance rails — failing that contract fails CHECK regardless of venue. A/B results flow back (iterate -> 1a backfill -> C flips); the entry graduates to exploit or moves to Rejected. Adopted explore entries keep the tag downstream (artifact frontmatter, e.g. A3 (explore)).
- Full C-consumption: every supported/weak C is cited by an A, refuted into Rejected, or closed with a No-action line + why. Negative advice ("avoid X", derived from a refuted C) is first-class and exploit-role. Rejected is the rung's reservoir, re-mined at every DRAFT open.
- Multi-round DPRC (self-assess -> [ROUND n] -> CHECK when dry) + mid-phase back-routing ([ROUTE -> claims]) per the Stage Gate Protocol Rounds contract. New principle 7: explore is a strategy, not a loophole.

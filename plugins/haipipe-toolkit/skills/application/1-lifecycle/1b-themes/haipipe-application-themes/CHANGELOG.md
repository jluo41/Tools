haipipe-application-themes — Changelog
=======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`.

## [2.4.0] — 2026-07-18

- Template alignment sweep: dropped the template's "How to use:" header line; Q-consumer questions renamed `## Q<n>` -> `## Q-Theme-<n>` (id carries the origin stage) + reshaped to the fixed 3-field form Ask / Why / Answer (`__TO_BE_FILLED__` == OPEN, else ANSWERED — the doc's only state). SKILL skeleton + formatting synced.

## [2.3.0] — 2026-07-17

- Q-consumer migration follow-up: the SKILL's artifact-section list still named the section `Probes` (a roster) — renamed to `Q-consumer` (## Q questions; APPROVE adds the 1-probes/ pointer + state), matching the template. (The earlier pass's grep missed these lines because they co-mention `1-probes/`.)

## [2.2.0] — 2026-07-17

- Q-consumer migration: template `Probes` tail -> `Q-consumer` (`## Q` blocks).

## [2.1.0] — 2026-07-17

- Template D3: probe roster placeholder + label `status` -> `state`.

## [2.0.0] — 2026-07-15

- Stage-skeleton reshape (paper-alignment, matching the 1c-claims exemplar): SKILL.md rebuilt on the 5-part skeleton — one-line decision + ladder, "What's special" (3 themes-unique items: extracted-not-invented/grounding, question-space-not-claim/hooks feed 1c, full D-consumption + counter-hunt), "The four phases, in themes", "The artifact" (section list + ref/themes-template.md pointer), "Exits". One sentence per line; prohibition walls cut. No load-bearing fact dropped (all 8 done-criteria + 5 principles folded into What's-special / CHECK line / phase notes).
- `summary:` deflated to one line + "History: ./CHANGELOG.md" (was a ~605-char version blob); redundant version-history comment line removed.
- PROBE-MODEL repoint to the flat pool: probe questions are SECTIONS in `1-probes/PPNN_<topic>.md` (one file per topic), NOT per-stage `_PROBE/` cards and NOT `1-probe-plans/README.md` (both RETIRED). PROBE runs the five-step loop via `haipipe-application-probe` (mode light → discovery; task for quick in-data confirmations); the section's `a-consumer:` lands grounding refs onto T entries. Dead vocabulary removed (`verdicted`, `dispatched`); claim status stays in 1c only. `ref/themes-template.md` Probes section repointed with the flat-pool path + the six-state enum (planned|commissioned|answered|read|answered-local|failed).

## [1.0.0] — 2026-07-09

- NEW skill, born in the ladder restage (SOP-ladder-restage.md, JL 2026-07-09): rung 1b = the I rung of the venue-FREE evidence ladder (1a-descriptions -> 1b-themes -> 1c-claims -> 1d-principles).
- Thematic extraction in the thematic-analysis sense: pattern-clusters grounded in 1a description ids and/or project-side discovery sources; ungrounded patterns go to a Parked section, never listed as themes.
- Every theme carries candidate-claim hooks (or an explicit context-only note); 1c claims cite themes as `C1 (T1)`. Light discovery-probe lane for field patterns the data alone cannot show.
- ref/<stage>-template.md added (canonical artifact template, paper convention; JL follow-up 2026-07-09) + SKILL.md pointer line; draft worker 1.2.0 registry reads it at WRITE.

## [1.1.0] — 2026-07-09

- Stage doc gains a Probes roster section, uniform across all rungs (bench finding, 01_sms_young_male: the user could not see 1a's probes in the stage doc while 0-seed.md listed its roster; only seed + 1c-claims had one). One line per PP -- question + status -- matching _PROBE/ on disk; done-criteria now require roster-matches-disk.

## [1.2.0] — 2026-07-09

- BREADTH ROUND (JL flywheel discussion): DRAFT sweeps three lenses — data patterns (from D entries), field patterns (discovery), counter-hunt (patterns AGAINST the seed hypothesis; a null result is recorded in Parked, not omitted). Full D-consumption rule: every 1a D id is cited by >=1 theme or listed in Parked as context-only.
- Parked is the rung's reservoir, re-mined at every DRAFT open. Multi-round DPRC (self-assess -> [ROUND n] -> CHECK when dry) + mid-phase back-routing ([ROUTE -> descriptions]) per the Stage Gate Protocol Rounds contract.

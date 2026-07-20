haipipe-application-descriptions — Changelog
=============================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`.

## [2.5.0] — 2026-07-19

- Probe-pool anatomy line restated as the current contract: one file per TOPIC, each ENTRY a `## QX<n>`
  q-executor carrying `### q-executor` / `### q-consumer` / `### bank binding` / `### a-executor`.
  Vocabulary: `a-consumer:` as a PROBE-FILE FIELD is gone — the probe entry's answer subsection is
  `### a-executor` (the copy of the answering QA file's answer, the consumer-side single source of truth).
  The a-consumer CONCEPT is untouched: it remains the per-consumer interpretation written in the STAGE DOC
  (station 2, anchored `[source: PP<NN>]`).

## [2.4.0] — 2026-07-18

- Template alignment sweep: Q-consumer questions renamed `## Q<n>` -> `## Q-Desc-<n>` (id carries the origin stage) and reshaped to the fixed 3-field form Description / Why / Answer (`__TO_BE_FILLED__` == OPEN, else ANSWERED — the doc's only state). Dropped the template's "How to use:" header line (copy/replace mechanic is the DRAFT worker's job). SKILL skeleton + formatting line synced.
- Descriptions restructure: `Datasets`/`DS<n>` -> a single `Dataset` list (one source, several files, or a folder — not limited to one); each Description is now its own subsection `## Description <n> · <topic>` (spelled out; cited downstream by the short id `D<n>`) instead of a `**D<n>**` bullet; per-source profile sheet `_DESCRIPTIONS/<source>.md`. SKILL synced (What's-special, skeleton, sidecar, formatting, Done gate).
- Q-field renamed `Description:` -> `Ask:` (reserve "Description" for the entries); dropped the `_DESCRIPTIONS/<source>.md` sidecar (policy: content.md + _LOG only) — rich detail stays in the task result the entry points to; schema-sweep PHI rail (column names only) kept as a principle.

## [2.3.0] — 2026-07-17

- Q-consumer migration follow-up: the SKILL's artifact-section list still named the section `Probes` (a roster) — renamed to `Q-consumer` (## Q questions; APPROVE adds the 1-probes/ pointer + state), matching the template. (The earlier pass's grep missed these lines because they co-mention `1-probes/`.)

## [2.2.0] — 2026-07-17

- Q-consumer migration: template `Probes` tail -> `Q-consumer` (`## Q` blocks); D-slots reference the landed answer via [AWAITING PP<nn>].

## [2.1.0] — 2026-07-17

- Id disambiguation note no longer references insight-KB card ids (retired); `D<n>` ids are unrelated to PP numbers.

## [1.0.0] — 2026-07-09

- NEW skill, born in the ladder restage (SOP-ladder-restage.md, JL 2026-07-09): stage 1 split into the venue-FREE evidence ladder 1a-descriptions -> 1b-themes -> 1c-claims -> 1d-principles, echoing D->I->K->W without reusing the insight-KB letter names.
- Rung 1a = the D rung: anchored data descriptions (statistic + pointer + as-of date), populated by light task-profile probes, never computed inline, no raw data. The doc IS the anchored-numbers doc (no separate _VALUES_ satellite here; R8).
- Consumes seed's `[FORWARD -> CLAIMS]` pointers (token unchanged; consumer moved here from claims per R5): data-profile needs -> own _PROBE/ plans; verdict-shaped needs -> planned PP skeletons in 1c's Probes section. Unconsumed pointer fails CHECK.
- Owns the staleness stamp duty (R3): a refreshed D entry stamps `[STALE D<n> refreshed <date>]` onto citing entries in 1b/1c/1d; downstream CHECKs fail on unresolved tags. Iterate's backfill lands here.
- ref/<stage>-template.md added (canonical artifact template, paper convention; JL follow-up 2026-07-09) + SKILL.md pointer line; draft worker 1.2.0 registry reads it at WRITE.

## [1.1.0] — 2026-07-09

- Stage doc gains a Probes roster section, uniform across all rungs (bench finding, 01_sms_young_male: the user could not see 1a's probes in the stage doc while 0-seed.md listed its roster; only seed + 1c-claims had one). One line per PP -- question + status -- matching _PROBE/ on disk; done-criteria now require roster-matches-disk. Section placed between Descriptions and Refresh Log; D-slots reference roster entries via [AWAITING PP<nn>].

## [1.2.0] — 2026-07-09

- BREADTH ROUND (JL flywheel discussion, same day as the bench run): the ladder is a flywheel, not a one-way climb (README). This rung gains: a Coverage section — six facets (cohort, arms/treatments, outcomes, time window, data quality, benchmark), each filled with D ids or waived with a why; waived facets are the rung's reservoir, re-mined at every DRAFT open.
- Multi-round DPRC: REVISE ends with a self-assessment; new slots/facets/gaps trigger another DRAFT->PROBE->REVISE lap ([ROUND n] in _LOG); CHECK fires only when a round comes up dry (venue-scaled, the Stage Gate Protocol Rounds contract). Mid-phase back-routing legal ([ROUTE -> seed]).

## [1.3.0] — 2026-07-09

- GROW LOOP (JL: "iterate to build and grow up until you have more and more probes to better understand the data... then go to the next stage"): rounds become a saturation engine — per-round question storms with rotating lenses (new ref/interrogation-battery.md: schema / distribution / crossing / surprise / field / USER-at-gate), answerable-filter (new question -> D slot + probe skeleton), blind self-test (answer the battery from D entries only), dry-stop (venue-scaled). Landed numbers feed the next round's questions, so the probe roster GROWS lap by lap.
- Field Disposition: 100% of each dataset's schema dispositioned (profiled | waived | excluded), column names only (PHI rail). Home = new `_DESCRIPTIONS/DS<n>_<name>.md` per-dataset profile sheets (field inventory + readable landed profile; probe worker 2.2.0 values-lane redirect).
- CHECK is part of the loop (JL: "after the check, they can think about adding more probes in the draft"): the gate asks which topics are missing; `grow` verdict (check worker 4.1.0) re-opens DRAFT as [ROUND n+1]; approve = saturated AND user added nothing.

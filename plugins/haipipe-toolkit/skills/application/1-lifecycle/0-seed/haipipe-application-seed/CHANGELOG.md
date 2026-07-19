haipipe-application-seed — Changelog
====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [4.3.0] — 2026-07-18

- Kill criteria section removed from the seed doc (unhelpful at seed stage; six content sections -> five). Q-consumer question blocks renamed `## Q<n>` -> `## Q-Seed-<n>` (id carries the origin stage) and reshaped to a fixed 3-field, human-readable form: `Ask` / `Why` (carries the content-section link + failure consequence) / `Answer` (`__TO_BE_FILLED__` == OPEN, else ANSWERED — the only state the seed doc tracks). Rule prose moved out of the template into SKILL (template = skeleton, SKILL = rules). Template + SKILL (frontmatter, skeleton, Done gate, formatting) updated.

## [4.2.0] — 2026-07-17

- Q-consumer migration: the stage doc's `Probes` tail section is renamed + reshaped to `Q-consumer` (`## Q` question blocks, matching the constitution's `q-executor:`/`a-consumer:` fields); the stage RAISES questions, the PP-id/route/state organize into 1-probes/ at APPROVE. Template + SKILL (artifact list, REVISE line, Done gate) updated.

## [4.1.0] — 2026-07-17

- Template D3: probe roster placeholder + label `status` -> `state` (canonical field name).

## [1.0.0] — 2026-06-22

- initial version modeled on paper-seed.

## [2.0.0] — 2026-06-29

- added _LOG_0-seed.md changelog; output folder 0-seed/ (was flat file); borrowed .md + _LOG pattern from paper-seed v2.0.0.

## [3.0.0] — 2026-07-06

- stage folder contract; venue-FREE marker (channel = hunch, not pin); DPRC phases; scaffolding delegated to enter get-or-create (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

## [3.1.0] — 2026-07-06

- 765696f port: visible Probes section in the seed doc + ascii artifact formatting.

## [3.2.0] — 2026-07-07

- Port of paper seed 3.5.0 (paper-alignment round 2, SOP §4 row 7, R3+R4): DRAFT may WebSearch to orient (fuel -> prose + buffered `status: planned` skeletons); PROBE scope narrowed to FEASIBILITY only (novelty + external-data obtainability) and must ALWAYS dispatch the real worker (Skill haipipe-application-probe, from-buffer) -- inline search forbidden in PROBE; internal-data profiling (the intervention's own cohort/engagement data) registers as a `[FORWARD -> CLAIMS] PPNN_<slug>` pointer line in _LOG_0-seed.md (a pointer, not a card; consumed at claims DRAFT); new "Probe scope and FORWARD handoff" section; done-criteria gain the check-probe-cards.sh find-pattern verification.

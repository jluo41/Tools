haipipe-application-pitch — Changelog
=====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## 5.4.0 — 2026-07-19 — questions this stage typically raises

From `_console/closed/260719-01-DRAFT-RAISE-QUESTIONS.md` (R1).

### Added (JL: "是不是我们给每个stage写上，我们这里要写什么东西，一般会问到什么类型的问题？")

- **`## Questions this stage typically raises`** — the kinds of question this stage is PRONE to, named so a drafter can hunt for them instead of only stumbling into them. Until now nothing anywhere said how to FIND a question worth raising: `probe`'s DRAFT rule 2 opened "For each open question", presupposing it already existed, and the DRAFT workers only had a trigger ("when the search reveals a gap"). The mechanical half was covered — placeholder sweeps find missing numbers and citations — but the JUDGMENT half, the questions a stage is structurally prone to, had no home.
- This stage OWNS its list; the DRAFT worker points here and never restates it. One home.
- Not invented: the four `PROBE:` lines that had been sitting in `haipipe-paper-draft`'s Stage-specific notes were exactly this content, filed under the wrong PHASE (they assigned question ELICITATION to PROBE, against `probe`'s PROBE rule 1). This is where they belong.

## [5.3.0] — 2026-07-18

- Template alignment sweep: dropped the template's "How to use:" header line; Q-consumer questions renamed `## Q<n>` -> `## Q-Pitch-<n>` (id carries the origin stage) + reshaped to the fixed 3-field form Ask / Why / Answer (`__TO_BE_FILLED__` == OPEN, else ANSWERED — the doc's only state). SKILL skeleton + formatting synced.

## [5.2.0] — 2026-07-17

- Q-consumer migration: template + SKILL `Probes` -> `Q-consumer` (`## Q` blocks; citation need only, usually empty).

## [5.1.0] — 2026-07-17

- Template D2: `audience profile` wording folded into the venue pack's tone-by-audience (post the _audience -> venue merge); header now reads `Audience: <target audience>`.

## [1.0.0] — 2026-06-22

- initial version as haipipe-application-rationale.

## [2.0.0] — 2026-06-23

- renamed from rationale to pitch; match paper vocabulary.

## [3.0.0] — 2026-06-29

- added _LOG_1-pitch.md changelog; output folder 1-pitch/ (was flat file); borrowed .md + _LOG pattern from paper.

## [4.0.0] — 2026-07-06

- renumbered stage 1 -> 2 (now AFTER claims + venue pin); venue-ALIGNED (reads venue+audience packs, re-couples on retarget); primary-claim designation moved here from the ledger (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

## [4.1.0] — 2026-07-06

- 765696f port: visible Probes section + reads 2-venue.md Artifact Principles + ascii artifact formatting.

## [5.0.0] — 2026-07-15

- skeleton reshape (5-part stage shape: what-this-stage-decides / what's-special / the four phases / the artifact / exits); 110 -> 100 lines, one sentence per line, prohibition-walls cut.
- probe redesign port: questions are RAISED as SECTIONS in the flat pool `1-probes/PPNN_<topic>.md` (was a per-stage `_PROBE/` card buffer); states are `planned | commissioned | answered | read | answered-local | failed`; no verdict block — claim status lives only in `0-lifecycle/1c-claims/1c-claims.md`.
- `ref/pitch-template.md` repointed onto the flat pool + the new state enum.
- metadata hygiene: `summary:` deflated to one line + `History: ./CHANGELOG.md`.

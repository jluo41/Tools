haipipe-application-narrative — Changelog
=========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## 5.4.0 — 2026-07-19 — questions this stage typically raises

From `_console/closed/260719-01-DRAFT-RAISE-QUESTIONS.md` (R1).

### Added (JL: "是不是我们给每个stage写上，我们这里要写什么东西，一般会问到什么类型的问题？")

- **`## Questions this stage typically raises`** — the kinds of question this stage is PRONE to, named so a drafter can hunt for them instead of only stumbling into them. Until now nothing anywhere said how to FIND a question worth raising: `probe`'s DRAFT rule 2 opened "For each open question", presupposing it already existed, and the DRAFT workers only had a trigger ("when the search reveals a gap"). The mechanical half was covered — placeholder sweeps find missing numbers and citations — but the JUDGMENT half, the questions a stage is structurally prone to, had no home.
- This stage OWNS its list; the DRAFT worker points here and never restates it. One home.
- Not invented: the four `PROBE:` lines that had been sitting in `haipipe-paper-draft`'s Stage-specific notes were exactly this content, filed under the wrong PHASE (they assigned question ELICITATION to PROBE, against `probe`'s PROBE rule 1). This is where they belong.

## [5.3.0] — 2026-07-19

- Probe-model block restated as the current contract (one file per TOPIC; `## QX<n>` ENTRY with four `###`
  subsections; the stake stays in this doc's Q-consumer). Vocabulary: `a-consumer:` as a PROBE-FILE FIELD is gone — the probe entry's answer subsection is
  `### a-executor` (the copy of the answering QA file's answer, the consumer-side single source of truth).
  The a-consumer CONCEPT is untouched: it remains the per-consumer interpretation written in the STAGE DOC
  (station 2, anchored `[source: PP<NN>]`).

## [5.2.0] — 2026-07-18

- Template alignment sweep: dropped the template's "How to use:" header line; Q-consumer questions renamed `## Q<n>` -> `## Q-Narr-<n>` (id carries the origin stage) + reshaped to the fixed 3-field form Ask / Why / Answer (`__TO_BE_FILLED__` == OPEN, else ANSWERED — the doc's only state). SKILL skeleton + formatting synced.

## [5.1.0] — 2026-07-17

- Q-consumer migration: template + SKILL `Probes` -> `Q-consumer` (`## Q` blocks; rare, routed back to claims).

## [1.0.0] — 2026-06-22

- initial version as haipipe-application-design.

## [2.0.0] — 2026-06-23

- renamed from design to narrative; match paper vocabulary; venue-gated.

## [3.0.0] — 2026-06-29

- added _LOG, _DISPLAY_ tracking file (beat → display unit mapping). Output folder 3-narrative/ (was flat file). Borrowed per-stage tracking pattern from paper.

## [4.0.0] — 2026-07-06

- stage-folder paths; gating via STATUS.md stages_skipped; settlement-bar precondition; DPRC phases (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).

## [4.1.0] — 2026-07-06

- 765696f port: visible Probes section + reads 2-venue.md Artifact Principles + ascii artifact formatting.

## [4.2.0] — 2026-07-09

- ladder restage + review sweep (family 6.0.0-6.1.1): primary input is 1d-advice (A entries) with 1c-claims as backstop; inline schema blocks converted to ascii ====/---- (JL heading ruling); id examples unpadded (C1/A1).

## [5.0.0] — 2026-07-15

- reshaped to the 5-part stage skeleton (what-it-decides / What's special / four phases / artifact+template pointer / Exits); inline per-venue templates moved into ref/narrative-template.md; probe-model repointed to the flat pool 1-probes/PPNN_<topic>.md (section fields serves/target/state/q-executor/a-consumer + ## Why; states planned|commissioned|answered|read|answered-local|failed; no _PROBE/, no 1-probe-plans, no verdict/dispatched, no G1/G2/G3); summary deflated to one line + History pointer.

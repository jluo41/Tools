haipipe-paper-narrative — Changelog
===================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 4.1.0 — 2026-07-14

- `1-probes/` described as the probe FILES (one per TOPIC, one SECTION per question), not "probe plans"; [GAP]/[PENDING] beats are RAISED as question SECTIONS.

## [4.1.1] — 2026-07-14 — the required-reads were off by one `../`

Fixed
- **The first instruction in this skill pointed at nothing.** `Read first: ../../PHILOSOPHY.md, ../../wiki/04-lifecycle-map.md` — but this skill lives at `skills/paper/1-lifecycle/<N>-<stage>/<skill>/`, so `../../` is `1-lifecycle/`, which holds neither `PHILOSOPHY.md` nor `wiki/`. Both live one level further up, at `skills/paper/`. Every in-body citation (`../../wiki/08-stage-gate.md`, `../../wiki/02-comment-lifecycle.md`, `../../wiki/09-stage-illuminate.md`, `../../wiki/11-delivery-need.md`, `../../_venue/playbook-<venue>`) failed the same way, silently — an agent loading the philosophy and the stage-gate rules got file-not-found and proceeded without them. All repointed to `../../../`; every target verified to resolve on disk.

## [3.2.0] -- 2026-07-09
## 4.0.0 — 2026-07-14

- PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1b-claims/1b-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
- Stops reading 'verdicted PP cards'. The claim ledger is the ONLY home of a claim's status; a probe section carries only its `reading:`.

Changed (JL ruling 2026-07-09 (LLMTrait-Section session postmortem): normalize the writing process)
- Phase VERBS on the stage (`narrative <paper-dir> [draft|probe|revise|check]`); hard gates + binding comment rules inlined (STOP after DRAFT with [GATE] log; Skill() dispatch proof; [REVISE] workers line; never delete `> USER:` comments; surgical edits only).

## [3.1.0] -- 2026-07-08

Changed
- Venue consumption rewired to lockfile semantics: read the paper's 0-lifecycle/2a-venue/2a-venue.md (Structural Blueprint beats + Writing Principles) FIRST; _venue/ packs only as fallback when 2a-venue.md is absent or as deep dives via its [source] tags; stale provenance -> note "venue contract stale", never silent pack re-reads.

## [2.2.3] — 2026-07-03

Changed
- Added the Phase Transition Contract pointer (wiki/08): announce every phase boundary, no silent phase skips (explicit logged verdict only), CHECK never implicit.

## [2.2.2] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; workers haipipe-paper-probe*, haipipe-paper-revise*).

## [2.2.1] — 2026-07-03

- converted canonical template to ref/narrative-template.md (plain markdown; readiness tags as [TAG], interrogation/external comments as plain sub-bullets, no LaTeX macros, no compile); deleted ref/narrative-template.tex.

## [2.2.0] — 2026-07-03

- narrative becomes stage orchestrator that drives its own phases. Phase skills (draft/gather/polish/check) are internal workers called by this skill, not user-facing. Comment lifecycle wired in (wiki/02). Shared Protocols section removed (protocols now accessed via phase skills). Handoff points to display.

## [2.1.0] — 2026-07-01

- formalized as venue-ALIGNED. Claims is now venue-FREE; pitch is venue-ALIGNED (cover letter); narrative expands the pitch's venue-coupled arc. Updated upstream references.

## [2.0.0] — 2026-06-29

- switched from .tex to .md + _LOG. Argument documents are markdown; only display compiles to PDF. Readiness tags and interrogation comments stay but in markdown format.

## [1.5.0] — 2026-06-24

- added the \fb{name}{status}{feedback}{resolution} macro for EXTERNAL reviewer comments threaded per beat (post + comments model; maroon, distinct from internal gray \rev), with a slim footer line for no-beat comments; added the short-plain-sentence rule for all comment text (\rev, \fb resolutions, footer); both wired into ref/narrative-template.tex

## [1.4.0] — 2026-06-23

- output is now 0-lifecycle/3-narrative/3-narrative.tex (section-mirrored: Intro/Methods/Results/Discussion, each beat readiness-tagged + interrogation comment), retiring the markdown NARRATIVE_REPORT.md form; extracted ref/narrative-template.tex carrying the readiness legend + comment vocabulary; points to the ProjB exemplar

## [unversioned]

- v1.3.1: added mandatory compile-after-edit rule; venue awareness note

## [1.3.0] — 2026-06-22

- added per-beat subagent interrogation protocol (keep/move/demote/cut + small-font comments)

## [1.2.0] — 2026-06-22

- added illuminate+gate+compile protocol (../../wiki/08-stage-gate.md, ../../wiki/09-stage-illuminate.md, ../../wiki/13-tex-quality.md)

## [1.1.0] — 2026-06-05

- renamed from narrative-report to haipipe-paper-narrative (haipipe-paper-* name unification).

## [1.0.0] — 2026-05-31

- baseline metadata added.

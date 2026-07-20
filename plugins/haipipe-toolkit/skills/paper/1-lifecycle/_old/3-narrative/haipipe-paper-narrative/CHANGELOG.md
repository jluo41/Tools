haipipe-paper-narrative — Changelog
===================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 4.3.1 — 2026-07-19 — vocabulary: a probe question is an ENTRY, not a SECTION

### Changed
The probe file's unit of one question was renamed `## Q-<Stage>-<n>` SECTION (flat `serves:` /
`target:` / `a-consumer:` fields) -> `## QX<n>` ENTRY (four `###` subsections) when the probe model
changed. This file still said SECTION, so an agent reading it wrote the OLD flat structure, which
`check-probe-cards.sh` FAILs as `stale-old-format` -- that stage's PROBE phase could then never go
green. Mechanical rename, no design change. (JL ruling 2026-07-19, board 260719-04-SEED-2PHASE D5:
"如果这样的话，那还是叫entry 吧". Swept 31 lines across 15 files; phrase-level, because "section"
also legitimately means a MANUSCRIPT section in these docs.)

## 4.3.0 — 2026-07-19 — questions this stage typically raises

From `_console/closed/260719-01-DRAFT-RAISE-QUESTIONS.md` (R1).

### Added (JL: "是不是我们给每个stage写上，我们这里要写什么东西，一般会问到什么类型的问题？")

- **`## Questions this stage typically raises`** — the kinds of question this stage is PRONE to, named so a drafter can hunt for them instead of only stumbling into them. Until now nothing anywhere said how to FIND a question worth raising: `probe`'s DRAFT rule 2 opened "For each open question", presupposing it already existed, and the DRAFT workers only had a trigger ("when the search reveals a gap"). The mechanical half was covered — placeholder sweeps find missing numbers and citations — but the JUDGMENT half, the questions a stage is structurally prone to, had no home.
- This stage OWNS its list; the DRAFT worker points here and never restates it. One home.
- Not invented: the four `PROBE:` lines that had been sitting in `haipipe-paper-draft`'s Stage-specific notes were exactly this content, filed under the wrong PHASE (they assigned question ELICITATION to PROBE, against `probe`'s PROBE rule 1). This is where they belong.

## 4.2.1 — 2026-07-19 — the 1b-claims input description names `### a-executor`

Two vocabulary rulings from JL, both dated 2026-07-19, applied across `paper/`.

**Ruling A — the `probe` nickname.** JL: "宪法 don't use this name, just use `probe`." Every "THE CONSTITUTION" / "the constitution" / "the probe constitution" naming `probe/haipipe-probe/SKILL.md` is replaced by `probe` or by the actual path, whichever reads better at the site. A nickname already in the repo is still a nickname.

**Ruling B — the `a-consumer:` probe-file field.** `- a-consumer:` as a FIELD IN A PROBE FILE was replaced by the entry's `### a-executor`; `check-probe-cards.sh` HARD FAILs it under the `stale-old-format` rule. The a-consumer CONCEPT is untouched and still named a-consumer: it is the per-consumer interpretation written in the STAGE DOC (station ②), anchored `[source: PP<NN>]`. Prose that said "the probe section carries its `a-consumer:`" was wrong twice over — probe files hold ENTRIES, not sections, and what an entry carries is `### a-executor`.

Current model, for reference:
```
QA file (bank)  ->  the ENTRY's `### a-executor`  (probe file: the copy, single source of truth)
                ->  each Q-consumer's a-consumer  (STAGE DOC: what it MEANS for this consumer)
                ->  stage content                 (REVISE weaves it in, discharges the bracket)
```

Written under JL's NO TOMBSTONES rule (2026-07-19): "不需要留退役告示,直接抹除任何痕迹" then "follow this rule to do all the following changes." The docs state only the current contract; this CHANGELOG carries the history.

### Changed — Inputs, item 1 (`0-lifecycle/1b-claims/1b-claims.md`) (ruling B)
"a probe section carries only its `a-consumer:`, and `## Verdict`/`verdicted` are DELETED" -> "a probe entry carries only its `### a-executor`." Two fixes in one sentence: the retired field name is corrected to the live one, and the `## Verdict`/`verdicted` ban-list is dropped per the NO TOMBSTONES rule (the checker's `dead-vocab` rule enforces it, so the prose does not need to).

## 4.2.0 — 2026-07-19 — the stage could not pass its own gate: `_DISPLAY_3-narrative.md` sidecar RETIRED

The narrative stage's done-criteria required a file that no longer exists anywhere in the contract. Line 61 read `- [ ] Display needs identified in _DISPLAY_3-narrative.md`; the sidecar working docs (`_CITATION_*`, `_VALUES_*`, `_DISPLAY_{stage}*`, `_DISCOVERY_*`, `_EVIDENCE_*`) are all retired, so the criterion was unsatisfiable and CHECK could never legitimately close. Four references in one file (artifact spec, done-criteria, the PROBE phase line, the Location block) all pointed at the same dead artifact.

JL ruling on the removal style, 2026-07-19: "不需要留退役告示，直接抹除任何痕迹" / "follow this rule to do all the following changes." No retirement notice is left in SKILL.md — the history is here instead.

Changed
- Artifact spec — the `_DISPLAY_3-narrative.md` bullet is replaced by `0-lifecycle/4-display/_DISPLAY_REQUEST.md`: this stage FILES one DR row per beat that needs a display unit; the display stage owns the file and is the only one that advances a DR status.
- Artifact spec gains the placeholder contract (matching seed 4.4.0): `1-probes/` is the only consumer-side source of truth, `_LOG_3-narrative.md` the only sidecar; an owed citation is `\cite{TOADD} [Q-Narrative-<n>]` and an owed number `{VAL:? <what>} [Q-Narrative-<n>]` — two markers side by side, never fused. A bracket-less placeholder is a defect (a hole no question will ever fill).
- Done-criterion — `Display needs identified in _DISPLAY_3-narrative.md` → `Every beat needing a display carries a DR row in 0-lifecycle/4-display/_DISPLAY_REQUEST.md`. This is now checkable against a file that exists.
- Location block — the `_DISPLAY_3-narrative.md` row now points at the display stage's request inbox.
- Phase flow: display-need RAISING moved DRAFT-ward, because the skill that raises display holes (`haipipe-paper-draft-display`) is a DRAFT-phase worker. DRAFT files the DR rows; PROBE now checks each row against the display stage's ruling (accepted / declined-with-reason / done) instead of writing a registry.
- DPRC applicability + CHECK question follow the same move: "identify display needs" leaves PROBE, "Display needs met?" → "Every DR row ruled by the display stage?".

Untouched (deliberately)
- Every `mode: light | full` reference — deferred to a separate review.
- `_DISPLAY_REQUEST.md` is ALIVE and is not a sidecar; it must never be confused with the retired `_DISPLAY_{stage}` registries.

## 4.1.0 — 2026-07-14

- `1-probes/` described as the probe FILES (one per TOPIC, one SECTION per question), not "probe plans"; [GAP]/[PENDING] beats are RAISED as question SECTIONS.

## [4.1.1] — 2026-07-14 — the required-reads were off by one `../`

Fixed
- **The first instruction in this skill pointed at nothing.** `Read first: ../../PHILOSOPHY.md, ../../<shared-refs>/04-lifecycle-map.md` — but this skill lives at `skills/paper/1-lifecycle/<N>-<stage>/<skill>/`, so `../../` is `1-lifecycle/`, which holds neither `PHILOSOPHY.md` nor the shared-reference folder. Both live one level further up, at `skills/paper/`. Every in-body citation (stage-gate, comment-lifecycle, stage-illuminate, delivery-need, `../../_venue/playbook-<venue>`) failed the same way, silently — an agent loading the philosophy and the stage-gate rules got file-not-found and proceeded without them. All repointed to `../../../`; every target verified to resolve on disk.

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
- Added the Phase Transition Contract pointer (08-stage-gate.md): announce every phase boundary, no silent phase skips (explicit logged verdict only), CHECK never implicit.

## [2.2.2] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; workers haipipe-paper-probe*, haipipe-paper-revise*).

## [2.2.1] — 2026-07-03

- converted canonical template to ref/narrative-template.md (plain markdown; readiness tags as [TAG], interrogation/external comments as plain sub-bullets, no LaTeX macros, no compile); deleted ref/narrative-template.tex.

## [2.2.0] — 2026-07-03

- narrative becomes stage orchestrator that drives its own phases. Phase skills (draft/gather/polish/check) are internal workers called by this skill, not user-facing. Comment lifecycle wired in. Shared Protocols section removed (protocols now accessed via phase skills). Handoff points to display.

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

- added illuminate+gate+compile protocol (08-stage-gate.md, 09-stage-illuminate.md, 13-tex-quality.md)

## [1.1.0] — 2026-06-05

- renamed from narrative-report to haipipe-paper-narrative (haipipe-paper-* name unification).

## [1.0.0] — 2026-05-31

- baseline metadata added.

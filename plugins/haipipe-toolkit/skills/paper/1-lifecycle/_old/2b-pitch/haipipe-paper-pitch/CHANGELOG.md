haipipe-paper-pitch — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 4.5.1 — 2026-07-19 — vocabulary: a probe question is an ENTRY, not a SECTION

### Changed
The probe file's unit of one question was renamed `## Q-<Stage>-<n>` SECTION (flat `serves:` /
`target:` / `a-consumer:` fields) -> `## QX<n>` ENTRY (four `###` subsections) when the probe model
changed. This file still said SECTION, so an agent reading it wrote the OLD flat structure, which
`check-probe-cards.sh` FAILs as `stale-old-format` -- that stage's PROBE phase could then never go
green. Mechanical rename, no design change. (JL ruling 2026-07-19, board 260719-04-SEED-2PHASE D5:
"如果这样的话，那还是叫entry 吧". Swept 31 lines across 15 files; phrase-level, because "section"
also legitimately means a MANUSCRIPT section in these docs.)

## 4.5.0 — 2026-07-19 — questions this stage typically raises

From `_console/closed/260719-01-DRAFT-RAISE-QUESTIONS.md` (R1).

### Added (JL: "是不是我们给每个stage写上，我们这里要写什么东西，一般会问到什么类型的问题？")

- **`## Questions this stage typically raises`** — the kinds of question this stage is PRONE to, named so a drafter can hunt for them instead of only stumbling into them. Until now nothing anywhere said how to FIND a question worth raising: `probe`'s DRAFT rule 2 opened "For each open question", presupposing it already existed, and the DRAFT workers only had a trigger ("when the search reveals a gap"). The mechanical half was covered — placeholder sweeps find missing numbers and citations — but the JUDGMENT half, the questions a stage is structurally prone to, had no home.
- This stage OWNS its list; the DRAFT worker points here and never restates it. One home.
- Not invented: the four `PROBE:` lines that had been sitting in `haipipe-paper-draft`'s Stage-specific notes were exactly this content, filed under the wrong PHASE (they assigned question ELICITATION to PROBE, against `probe`'s PROBE rule 1). This is where they belong.

## 4.4.0 — 2026-07-18 — charter conformance: RULE comments · Q-Pitch-<n> · no pipe table · 2b-pitch

Adopted the stage-template charter (`../../TEMPLATES.md`, JL 2026-07-18) + the Option A `2-pitch` → `2b-pitch` rename.

Changed (`ref/pitch-template.md`)
- Converted from the markdown `#`/`##`-header style to the sibling `=====`/`-----` convention (frees `##` for the Q-consumer). Title → `2b-pitch: <paper title>`.
- Fill rules → `<!-- RULE -->` comments (follow then delete); top TEMPLATE marker; Hook candidates `### Candidate` → bold sub-items.
- Added a `Q-consumer` section: `## Q-Pitch-<n>` + Description/Reason/Answer, ANSWERABLE + specific (framing risk, competing paper, does-the-editor's-chair-answer-hold), inline `[Q-Pitch-1]` citation.
- The H-to-RQ mapping PIPE TABLE → RECORD LINES (`H1 → RQ1: … — why`).

SKILL.md
- CORE QUESTION added (charter C6): "why would THIS venue's editor send this paper out for review?".
- description / summary / Content structure / done-criteria: `Probes` → `Q-consumer` (`## Q-Pitch-<n>`); RULE-comments-deleted criterion.
- venue-doc reads repointed to the reshaped venue: `Venue Profile` / `Fit Assessment` → `Venue Decision` / `Requirements`.
- v4.3.1 → 4.4.0.


## 4.3.0 — 2026-07-14

- "probe plans" -> the probe FILES; "`1-probes/` cards" -> a `read` section / a landed QA file in tasks|discoveries.

## [4.3.1] — 2026-07-14 — the required-reads were off by one `../`

Fixed
- **The first instruction in this skill pointed at nothing.** `Read first: ../../PHILOSOPHY.md, ../../<shared-refs>/04-lifecycle-map.md` — but this skill lives at `skills/paper/1-lifecycle/<N>-<stage>/<skill>/`, so `../../` is `1-lifecycle/`, which holds neither `PHILOSOPHY.md` nor the shared-reference folder. Both live one level further up, at `skills/paper/`. Every in-body citation (stage-gate, comment-lifecycle, stage-illuminate, delivery-need, `../../_venue/playbook-<venue>`) failed the same way, silently — an agent loading the philosophy and the stage-gate rules got file-not-found and proceeded without them. All repointed to `../../../`; every target verified to resolve on disk.

## [4.2.0] -- 2026-07-09

Changed (JL ruling 2026-07-09 (LLMTrait-Section session postmortem): normalize the writing process)
- Phase VERBS on the stage (`pitch <paper-dir> [draft|probe|revise|check]`); hard gates + binding comment rules inlined (STOP after DRAFT with [GATE] log; Skill() dispatch proof; [REVISE] workers line; never delete `> USER:` comments; surgical edits only).

## [4.1.0] -- 2026-07-08

Changed
- Venue consumption rewired to lockfile semantics: read the paper's 0-lifecycle/2a-venue/2a-venue.md (Venue Profile + Fit Assessment) FIRST; _venue/ packs only as fallback when 2a-venue.md is absent or as deep dives via its [source] tags; stale provenance -> note "venue contract stale", never silent pack re-reads.

## [3.1.3] — 2026-07-03

Changed
- Added the Phase Transition Contract pointer (08-stage-gate.md): announce every phase boundary, no silent phase skips (explicit logged verdict only), CHECK never implicit.

## [3.1.2] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; workers haipipe-paper-probe*, haipipe-paper-revise*).

## [3.1.1] — 2026-07-03

- converted canonical template to ref/pitch-template.md (plain markdown, no LaTeX, no compile); deleted ref/pitch-template.tex.

## [3.1.0] — 2026-07-03

- pitch becomes stage orchestrator that drives its own phases. Phase skills (draft/gather/polish/check) are internal workers called by this skill, not user-facing. Comment lifecycle wired in. Shared Protocols section removed.

## [3.0.0] — 2026-07-01

- pitch is now venue-ALIGNED = cover letter. Absorbs Editor's Chair Test, [primary] claim designation, and venue-specific RQ framing from claims. Claims is now venue-FREE (pure evidence inventory). Pitch reframes venue-neutral hypotheses (H1→RQ1) for the target editor.

## [2.0.0] — 2026-06-29

- switched from .tex to .md + _LOG. PITCH_LOG.md merged into _LOG_2b-pitch.md. Argument documents are markdown; only display compiles to PDF.

## [unversioned]

- v1.5.2: extracted template to ref/pitch-template.tex; inline replaced with reading-order summary

## [unversioned]

- v1.5.1: added mandatory compile-after-edit rule; venue awareness note

## [1.5.0] — 2026-06-22

- added Title section, multi-hook candidates, template enforcement, quality gate; wired illuminate+gate+compile protocols

## [1.4.0] — 2026-06-22

- readability rules, section cues, hook catalog

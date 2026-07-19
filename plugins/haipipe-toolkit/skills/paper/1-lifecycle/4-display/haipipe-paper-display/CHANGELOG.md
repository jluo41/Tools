haipipe-paper-display — Changelog
=================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 4.1.0 — 2026-07-14

- Evidence lane: "claim has no confirmed verdict yet -> buffer a PP card" -> "claim's status not settled yet -> raise a question SECTION"; the stage never dispatches an evidence agent itself.
- Naming made consistent: the md's fixed section is `Probes` (was "Probe Plan" in the formatting rule, the DRAFT gate line, and the CHECKLIST while the template already said `Probes`).
- ref/display-template.md: an evidence entry's `Route:` is a question SECTION or `/haipipe-task-for-display` — never `/haipipe-probe`.

## [4.1.1] — 2026-07-14 — the required-reads were off by one `../`

Fixed
- **The first instruction in this skill pointed at nothing.** `Read first: ../../PHILOSOPHY.md, ../../<shared-refs>/04-lifecycle-map.md` — but this skill lives at `skills/paper/1-lifecycle/<N>-<stage>/<skill>/`, so `../../` is `1-lifecycle/`, which holds neither `PHILOSOPHY.md` nor the shared-reference folder. Both live one level further up, at `skills/paper/`. Every in-body citation (stage-gate, comment-lifecycle, stage-illuminate, delivery-need, `../../_venue/playbook-<venue>`) failed the same way, silently — an agent loading the philosophy and the stage-gate rules got file-not-found and proceeded without them. All repointed to `../../../`; every target verified to resolve on disk.

## [3.4.0] -- 2026-07-10
## 4.0.0 — 2026-07-14

- PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1b-claims/1b-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
- Display's `Detail:` pointers and the probe-buffer route move to 1-probes/PPNN_<topic>.md sections.

Changed (JL ruling 2026-07-10: "the probe plan should be like the subsection, and like others, just like seed-template.md -- could we make things consistent?")
- `Probe Plan` section renamed **`Probes`** and reshaped to the seed/claims family convention: each probe is its own `###` sub-item `<ID> -- <title> -- <status>` with `Lane:` / `Route:` / `Serves:` / `Gated on:` / `Outcome:` field lines, `---` separated; evidence entries carry the family's `Detail: _PROBE/PPNN_<slug>.md` pointer. IDs still number within lane (S sweep / E evidence / R render); status vocabulary spelled out (`▶ ready` · `✋ gated` · `done`). PROBE fills `Outcome:` and flips status.
- `###` is now used for BOTH display subsections and probe sub-items (the doc's only ATX level); template, SKILL.md (content structure, formatting, DRAFT, PROBE, done-criteria, flow), and CHECKLIST updated together.

## [3.3.0] -- 2026-07-10

Changed (JL ruling 2026-07-10: "never never using tables")
- NO markdown pipe tables anywhere in `4-display.md`: the Display Map, Probe Plan, method candidates, and Parking become record lines (`- E2 ✋ <action>` + indented `route:` / `serves:` / `gated on:` / `outcome:` fields; `- A <form> via <route> -> <output> · verdict: ...`; map lines `N. Figure N = unit @section · type · claim · status`). Pipe tables fight hand-editing, one-sentence-per-line, and diff review. Aligned plain text inside fenced sketches stays legal (it sketches a LaTeX table, not doc structure).
- `ref/display-template.md` rewritten table-free; formatting rule + content bullets + CHECKLIST item updated; new probe-plan status `done` (outcome written in) joins ▶/✋.
- Validated 2026-07-10 via fresh-subagent DRAFT redo on the sandbox paper: template's no-tables rule discovered and applied (pipe-table lines 61 -> 0), map/plan/candidates/Parking all record lines, `> USER:` lines byte-identical, gate stop held. Real-paper migration: Paper-Personality2Opioid-MISQ2026 4-display.md de-tabled the same day ([FORMAT] logged), threads verified intact.

## [3.2.0] -- 2026-07-10

Changed (JL ruling 2026-07-10: "organize each display with the venue section, and each display itself is a subsection")
- `4-display.md` display blocks are no longer flat: one `-----` group per PAPER SECTION (narrative order), each display a `###` subsection inside its group — the md now mirrors the generated gallery's `\section*`/`\subsection*` structure one-to-one (sync walks the groups; group membership must match the map's `section` column).
- Every group opens with a `venue expects:` line (that section's display units from the 2a-venue.md Structural Blueprint), so a venue-mandated unit with no subsection is a visible GAP in place, not just an audit finding.
- `ref/display-template.md` restructured accordingly; formatting rule updated (`###` is the only ATX level used; a display's section is stated once, by its group header); SKILL.md content-structure/Plan/sync/flow + CHECKLIST updated.

## [3.1.0] -- 2026-07-10

Changed (JL rulings 2026-07-10: "after the draft, the gate is leaving the questions and checking with the user about what probe to run" + "probe should check other stages, like the sections, whether they need any displays" + template belongs in ref/ like every other stage)
- New `ref/display-template.md`: canonical 4-display.md template, same `ref/<stage>-template.md` convention as seed/claims/pitch/narrative; the inline SKILL.md template is gone and haipipe-paper-draft's template table points here.
- New md section **Probe Plan (proposed by this draft)**: one row per proposed probe in three groups — `S0` cross-stage coverage sweep, `En` evidence lane, `Rn` render lane — each `▶ ready` or `✋ gated on <named block thread>`. DRAFT authors it; the ⛔ gate presents open threads + the plan; the user rules/strikes rows ("skip En/Rn"); PROBE executes only what survives and writes each row's outcome back. New done-criteria + CHECKLIST items (no ✋ row silently run or dropped).
- PROBE step 0 = coverage sweep (S0): read 3-narrative + every section md (+ `_DISPLAY_` registries + `\input`/`\ref` uses), cross-check against map + inbox; unfiled needs become DR rows filed on the section's behalf (`filed-by: display-probe sweep`); map acceptance stays a DRAFT/user decision.
- haipipe-paper-draft SKILL.md display notes updated to match (template pointer, probe-plan-at-gate, S0 sweep).
- Validated 2026-07-10 via fresh-subagent DRAFT redo on the sandbox paper: template discovered via `ref/`, Probe Plan authored (S0/En/Rn, ▶/✋ tied to named threads), gate presented threads + plan, migration not repeated, no probe/sync/compile ran, `> USER:` lines preserved verbatim. The subagent's emergent "draft assumptions" move for non-interactive illuminate is codified in DRAFT (record unasked taste questions as assumptions, present at the gate).

## [3.0.1] -- 2026-07-10

Fixed (fresh-agent audit, C3)
- PROBE section states the authority split: commissioning evidence/render work for accepted units is THIS stage's job; the probe-display worker's ban binds section/narrative context only.

## [3.0.0] -- 2026-07-10

Changed (JL ruling 2026-07-10: md-first display stage — "we should have 4-display.md as other stages, for quick review and modification; real assets stay in 0-displays/; probe should call the illustration skills as well; try different methods of making the plot")
- Stage doc becomes the md → tex → pdf trio: `4-display.md` is THE BRAIN (Venue Set + gallery config, Display Map, one block per display with takeaway / evidence / METHOD-CANDIDATES table / ASCII sketch / caption job / fragility / `> USER:` threads, Parking); `4-display.tex` is GENERATED wholesale by sync (section banners, named subsections, small-font verdicts, `\input`s, Parking; hand-editing it is a defect); `4-display.pdf` compiled from paper root.
- Retired + absorbed into the md: `4-display-probes.md` (planning brain), `4-display-preview.txt` (ASCII contact sheet — block sketches are the contact sheet now), `%% {USER}:` comments in the tex (now `> USER:` threads in md blocks). DRAFT step 0 = stage-entry reconcile: migrate all three VERBATIM, create missing `_LOG`, map legacy flat assets (closes 2026-06-24 feedback: predefined-unit-content, ascii-contact-sheet, persist-user-comments, plan-boilerplate-too-heavy, gallery-section-names, pdf-order-follow-narrative).
- PROBE reshaped into two lanes: EVIDENCE lane (`/haipipe-task-for-display`, `/haipipe-probe` — numbers come from a task, never from the agent) + RENDER lane (direct Skill dispatch to figure / table / diagram / ILLUSTRATION renderers, one per candidate row, in new candidate mode → unit `candidates/`; promotion is REVISE's decision). New status `candidates`; new unit dir `candidates/`.
- REVISE = pick winners (rationale recorded per block; a `> USER:` preference stands) + promote/demote + sync + compile. CHECK formalizes the render-review subagent (builder ≠ judge, reads compiled PDFs, keep-main/keep-supplement/fix/demote/cut; closes 2026-06-24 render-review-loop + per-unit-selfcheck feedback).
- Gallery sizing knobs move to the md's gallery config (emitted into generated tex preamble; closes 2026-06-24 gallery-owns-sizing). Comment + sizing principles rewritten (principle 7 md-is-brain, principle 8 try-different-methods, principle 10 commentary-in-md).
- `ref/display-unit-output-contract.md`: added candidate mode (render to `candidates/<letter>-<form>.<ext>`, spec to `source/`, no touch of `assets/`/`float.tex`); renderers never edit stage docs.
- CHECKLIST.md rewritten around the trio (stage-doc / per-block / per-unit sections, migration + inbox items).
- Dropped stale references: `../README-display.md` (file does not exist) and the ARIS `paper-framework-figure-studio-pro` hook (folder does not exist; the 3–5-option framework-candidate loop is described inline). Validated 2026-07-10 via fresh-subagent DRAFT run on a sandbox paper (migration, inbox, gate-stop all conforming).

## [2.3.0] -- 2026-07-10

Changed (JL 2026-07-10 display-request ruling)
- New artifact: `_DISPLAY_REQUEST.md` -- the stage's request INBOX. Sections file DR rows for units they need but must not create. DRAFT/Plan reads the inbox FIRST: accept (index row + scaffold, flip `accepted`) or decline (reason written back); on rendered/input-ready flip `done (unit: <path>)`. Only this stage advances DR statuses.

## [2.2.0] -- 2026-07-09

Changed (JL ruling 2026-07-09 (LLMTrait-Section session postmortem): normalize the writing process)
- Phase VERBS on the stage (`display <paper-dir> [draft|probe|revise|check]`); hard gates + binding comment rules inlined (STOP after DRAFT with [GATE] log; Skill() dispatch proof; [REVISE] workers line; never delete `> USER:` comments; surgical edits only).

## [2.1.0] -- 2026-07-08

Changed
- Venue consumption rewired to lockfile semantics (SKILL.md principle 9 + Venue Constraints + CHECKLIST.md venue-set item): read the paper's 0-lifecycle/2a-venue/2a-venue.md (Structural Blueprint display units + Writing Principles display limits) FIRST; pack README -> Display only as fallback when 2a-venue.md is absent or as deep dives via its [source] tags; stale provenance -> note "venue contract stale", never silent pack re-reads.

## [1.6.2] — 2026-07-03

Changed
- Added the Phase Transition Contract pointer (08-stage-gate.md): announce every phase boundary, no silent phase skips (explicit logged verdict only), CHECK never implicit.

## [1.6.1] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; workers haipipe-paper-probe*, haipipe-paper-revise*).

## [1.6.0] — 2026-07-03

- display becomes stage orchestrator that drives its own phases (DRAFT/GATHER/POLISH/CHECK). Phase skills are internal workers called by this skill, not user-facing. Subcommands (plan/scaffold/framework/materialize/build/audit/insert) reorganized as internal operations within phases. Comment lifecycle wired in. Removed shared-protocols listing. Handoff updated to promote to section-edit.

## [unversioned]

- v1.5.0: added canonical CHECKLIST.md done-gate (absorbs gallery requirements out of the paper's 4-display.tex); elbow/icon vector-render rules

## [unversioned]

- v1.4.1: added mandatory compile-after-edit rule; venue awareness note

## [unversioned]

- v1.4.0: added illuminate protocol + cross-refs to stage-gate, tex-quality

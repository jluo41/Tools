haipipe-paper-section-edit — Changelog
======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 5.3.1 — 2026-07-19 — vocabulary: a probe question is an ENTRY, not a SECTION

### Changed
The probe file's unit of one question was renamed `## Q-<Stage>-<n>` SECTION (flat `serves:` /
`target:` / `a-consumer:` fields) -> `## QX<n>` ENTRY (four `###` subsections) when the probe model
changed. This file still said SECTION, so an agent reading it wrote the OLD flat structure, which
`check-probe-cards.sh` FAILs as `stale-old-format` -- that stage's PROBE phase could then never go
green. Mechanical rename, no design change. (JL ruling 2026-07-19, board 260719-04-SEED-2PHASE D5:
"如果这样的话，那还是叫entry 吧". Swept 31 lines across 15 files; phrase-level, because "section"
also legitimately means a MANUSCRIPT section in these docs.)

## 5.3.0 — 2026-07-19 — questions this stage typically raises

From `_console/closed/260719-01-DRAFT-RAISE-QUESTIONS.md` (R1).

### Added (JL: "是不是我们给每个stage写上，我们这里要写什么东西，一般会问到什么类型的问题？")

- **`## Questions this stage typically raises`** — the kinds of question this stage is PRONE to, named so a drafter can hunt for them instead of only stumbling into them. Until now nothing anywhere said how to FIND a question worth raising: `probe`'s DRAFT rule 2 opened "For each open question", presupposing it already existed, and the DRAFT workers only had a trigger ("when the search reveals a gap"). The mechanical half was covered — placeholder sweeps find missing numbers and citations — but the JUDGMENT half, the questions a stage is structurally prone to, had no home.
- This stage OWNS its list; the DRAFT worker points here and never restates it. One home.
- Not invented: the four `PROBE:` lines that had been sitting in `haipipe-paper-draft`'s Stage-specific notes were exactly this content, filed under the wrong PHASE (they assigned question ELICITATION to PROBE, against `probe`'s PROBE rule 1). This is where they belong.

## 5.2.0 — 2026-07-19 — `_CITATION_{section}` / `_VALUES_{section}` sidecars RETIRED; the anchor bracket becomes the contract

Section-edit was the densest surviving pocket of the retired sidecar model: the per-section artifact tree still LISTED `_CITATION_{section}.md` and `_VALUES_{section}.md` as files to create, the PROBE line still routed its tracks INTO them (`citation → _CITATION_, values → _VALUES_`), the phase-line derivation read "the tracking file", and one line pointed at `2-phase/1-probe/haipipe-paper-probe-citation/SKILL.md` — a skill being dissolved. A section scaffolded from this contract would have produced two files nothing downstream reads.

JL ruling on the removal style, 2026-07-19: "不需要留退役告示，直接抹除任何痕迹" / "follow this rule to do all the following changes." No ban-list naming the dead files is left in the skill; the history is here.

Changed (SKILL.md)
- "Real or greppable, never invented" now states the placeholder contract in its current form: `{VAL:? <what>} [Q-<Stage>-<n>]` and `\cite{TOADD} [Q-<Stage>-<n>]` — the marker and the anchor bracket side by side, **never fused**; the bracket names the `1-probes/` question that will produce the key or the number, and a placeholder without one is a defect. `1-probes/` is the only consumer-side source of truth; `_LOG_{section}.md` is the only sidecar. `.bib` stays human-only, learned by grep.
- PROBE phase line — the three tracks no longer write to registries: citation and values run their `[Q-<Stage>-<n>]` entries in `1-probes/` to an answer; display links a `0-displays/` unit or checks its DR row.
- The artifact tree drops both sidecar rows, and a following line says where the needs actually live (`1-probes/` entries; a needed unit = a DR row in `0-lifecycle/4-display/_DISPLAY_REQUEST.md`).
- Phase-line derivation — **cite/val/disp** ✅ is now defined against the `.md` itself (no `\cite{TOADD}` / `{VAL:?}` / unlinked display bracket left open), not against a tracking file.

Changed (`ref/outline-format.md`)
- The "three placeholder forms" block shows the bracketed forms, plus the never-fused rule.
- `\citep{key}` rule: grep the `.bib` (only).
- `\cite{TOADD}` rule: paired with its question bracket, not a `_CITATION_` row.
- DRAFT done-criterion updated to the bracketed forms + "no placeholder left without its bracket".

Changed (`ref/section-template.md`)
- The prose example cites `\cite{TOADD} [Q-<Stage>-<n>]` and `{VAL:? <what>} [Q-<Stage>-<n>]`.
- The Settled Flags example no longer resolves a placeholder "paper-local" into a `_VALUES_` file.

Changed (`../section-type/section-related-work.md`)
- The TODO's citation-lane pointer repointed from the dissolved `/haipipe-paper-probe-citation` to `/haipipe-paper-draft-citation`.

Untouched (deliberately)
- Every `mode: light | full` reference — deferred to a separate review.
- `0-lifecycle/4-display/_DISPLAY_REQUEST.md` — ALIVE; the DR-row route for a missing display unit is the current contract, not a retired sidecar.
- `feedback/*.md` — dated records of JL's own words at the time; history, left verbatim.

## 5.1.0 — 2026-07-14

- "Probe escalation": sweep paper-local -> raise a question SECTION -> ② MATCH -> ③ DISPATCH only what MATCH cannot close. The "gateway probe" tier is gone; no inline-search tier exists at any depth.
- The DRAFT ⛔ STOP presents STRUCTURE + the QUESTIONS RAISED (ref/outline-format.md + ref/section-template.md updated to match).
- Citation provenance `🤖 harvested` = came via DISPATCH -> discovery -> the QA file (was "via gateway").
- ref/outline-format.md: the 1-probes/README.md board row carries a `state` and a `file:` pointer (was `status` + `card:`).

## [4.5.1] -- 2026-07-10
## 5.0.0 — 2026-07-14

- PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1b-claims/1b-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
- The probe convention block, the 'Probes proposed by this draft' block, and the citation/values gap routes all move to question SECTIONS in 1-probes/. The search door is now the PROBE phase's dispatch to Agent(haipipe-discovery-orchestrator-agent), not the retired gateway.

Fixed (fresh-agent template DRAFT test, fix5 fixture)
- The index-row FORMAT was specified nowhere a DRAFT-phase agent loads, so the tester invented a 6-column markdown table in 1-probe-plans/README.md (JL standing rule: no tables in probe documents). Template + outline-format + hub now give the literal bullet-row shape, and the PP filename convention `PP<NN>_<slug>.md` (underscore) that the tester also missed (wrote PP01-results-regression.md).

## [4.5.0] -- 2026-07-10

Added (JL: "How do you think you can make a section-template here")
- `ref/section-template.md`: literal copy-and-fill skeleton for the section .md (venue header, structure block + counts, paragraph blocks, comment-thread shape, probe-proposal block with paper-local hints + DR exception). Guidance lines carry a greppable `<tpl:` marker; scaffold gate = `grep -c '<tpl' = 0` (same mechanical-proof pattern as TOADD/OWED).
- Spec/template split: outline-format.md stays the rulebook; the template is the shape. Hub step 2 scaffolds by copying the template; draft done-criteria gains the zero-residue check. Motivated by the trial session's first draft missing the venue header (prose spec ≠ reproducible shape).

## [4.4.1] -- 2026-07-10

Fixed (fresh-agent audit, C5/C7/M2)
- Probe escalation ladder: "search (lightweight)" tier removed -- sweep paper-local -> plan -> gateway; gateway is the only search door.
- CHECK step 13 made md-first: \cite{TOADD} -> \citep{key} replacement and value weaving happen in the .md, then re-sync (was tex-first).
- Provenance emoji aligned: 🤖 harvested (was 🤖 agent-found).

## [4.4.0] -- 2026-07-10

Changed (JL: "In section-edit, we don't create the display ourself")
- Display probe track: sweep existing 0-displays/ units, LINK what exists; a missing unit becomes a DR request row in `0-lifecycle/4-display/_DISPLAY_REQUEST.md` -- never a /haipipe-task route (old step 9 killed), never a PP card (outline-format buffering exception added).
- New disp status 📨 = request pending; the display axis cannot pass CHECK until the DR row is done and the unit linked.

## [4.3.1] -- 2026-07-10

Changed (paper-local sweep, JL 2026-07-10)
- Workflow step 7 (citation): sweep the .bib + prior stages' _CITATION_ maps first; only surviving gaps become probe plans.
- outline-format.md: the draft's probe-proposal block marks pointers the draft already sees as `-> paper-local: <file>` so PROBE can close them as answered-local without a gateway dispatch.

## [4.3.0] -- 2026-07-10

Changed (JL: "could we have the real citation from the .bib file as well? if it is not available, you can add \cite{TOADD}, and you can check the _CITATION or bib to find the suitable citations")
- Citation convention in the section .md: real `\citep{key}`/`\citet{key}` for keys grep-verified in the paper's .bib; `\cite{TOADD}` + a `_CITATION_` row (topic + expected source) when no key fits. Supersedes `[CITE: <topic>]` and parenthetical "(Author Year)"; legacy `[CITE:]` markers are treated as TOADD.
- Tex-mirror rule carve-out: citation commands are the ONE LaTeX construct allowed in the .md (sync carries them verbatim). TOADD surviving into compiled tex fails CHECK via the broken-\cite check.
- ref/outline-format.md updated in step (placeholder rules, examples, probe-proposal block, done-criteria, _LOG format).

## [4.2.1] -- 2026-07-09

Changed (JL: "style are just the style for the references, don't need to strictly follow them")
- Venue header semantics pinned: blueprint (2a-venue.md block) = BINDING (budget, structure, density); style file(s) = REFERENCE ONLY (advisory -- arc/moves/exemplars; deviation never fails CHECK). Hybrid sections (methods + results flavor) may list multiple style refs, dot-separated.

## [4.2.0] -- 2026-07-09

Changed (JL: "make the section aware of the venue-specific requirement -- give them the link")
- Section .md gains a VENUE HEADER under the H1: venue pin, section-type mapping, blueprint pointer (2a-venue.md block -- stays authoritative), and the deep-dive style link (the [source:] tag RESOLVED to a real pack path at scaffold, layout-agnostic find; pack absent -> "(pack missing -- blueprint only)" + CHECK flag). Later phases follow the recorded link instead of re-deriving the 3-hop tag chain. Mirrored in ref/outline-format.md.

## [4.1.1] -- 2026-07-09

Changed (JL: "add the numbers of total words to it as well")
- Structure overview block now carries per-paragraph `N sentences · ~M words` and a closing `total:` line (¶ / sentences / ~words) checked against the venue budget from 2a-venue.md; recount at draft and after REVISE; over budget -> flag, never silently trim. Mirrored in ref/outline-format.md.

## [4.1.0] -- 2026-07-09

Changed (JL 2026-07-09: "draft = review the section + propose what probes to do")
- Draft template gains the "Probes proposed by this draft" END block (ref/outline-format.md): placeholders rolled up with expected sources, display needs per paragraph, heavier needs buffered as planned PP skeletons in _PROBE/ + index row (seed's buffer convention, now section-side).
- Workflow: new step 5 "Propose the probes"; the DRAFT ⛔ STOP now presents structure + probe plan at the same gate; done-criteria require the block.

## [4.0.0] -- 2026-07-09

Changed (JL ruling 2026-07-09 (LLMTrait-Section session postmortem): normalize the writing process)
- BREAKING: the section .md now holds REAL prose (complete academic sentences, one per line, blank-line separated, {VAL:?}/[CITE:] placeholders) -- supersedes the "lean plan / content decisions not prose" outline model. ref/outline-format.md rewritten to match; its "fix it in tex" REVISE advice removed (tex is generated by sync, never hand-edited).
- Phase VERBS on the hub: `<section> [draft|probe|revise|check]`; bare invocation = status only, advance ONLY on the user's verb.
- Hard gates: DRAFT ends at a STOP for structure review ([GATE] draft-review logged, user quoted); CHECK never implicit; never commit before CHECK opens. Agent never self-advances.
- Proof-carrying dispatch: every phase via Skill(); [REVISE] _LOG entry must carry `workers: content/humanizer/results` line (checks.sh --log FAILs without it).
- Binding comment rules inlined in the hub (never delete/reword `> USER:`; reply `> CC:` underneath; only user resolves; surgical edits only, no full-file rewrites of commented files) -- no longer wiki-only.
- Stale comment-first REVISE block (Round 1 change-NO-prose) DELETED -- contradicted the comment lifecycle + revise hub ("no comment-first; change directly + why-comments"); leftover from the retired edit-cycle (missed by A17).

## [3.2.0] -- 2026-07-08

Changed
- Venue consumption rewired to lockfile semantics: DRAFT step 1 reads the paper's 0-lifecycle/2a-venue/2a-venue.md FIRST (this section's Structural Blueprint block + Writing Principles); pack style-profile/per-section style.md resolution demoted to fallback when 2a-venue.md is absent, or reached as deep dives via its [source] tags; stale provenance -> note "venue contract stale", never silent pack re-reads (norm-digestion harvest noted as a staleness source).

## [3.1.4] — 2026-07-04

Fixed
- Probe-plan convention wording: `1-probe-plans/README.md` is a cross-STAGE index (was "cross-paper") and the PP numbering authority.

## [3.1.3] — 2026-07-03

Changed
- Added the Phase Transition Contract pointer (08-stage-gate.md): announce every phase boundary, no silent phase skips (explicit logged verdict only), CHECK never implicit.

## [3.1.2] — 2026-07-03

Fixed
- Closing-block example phase line `probe: cite 🚀` corrected to `probe: cite 🔥🚀` (exactly-one-marker rule: active sub-track at the frontier collapses both markers).

## [3.1.1] — 2026-07-03

Fixed
- "Dual status strip" section renamed to "Closing block (section-aware)" and aligned with the umbrella Closing Block spec: simplified tail (status merged with stage + section, no paper_root), stage/phase line labels, marker legend replaced by a pointer to the umbrella (keeping only the local ⚠️ re-sync marker).

## [3.1.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; workers 2-phase/1-probe/haipipe-paper-probe-*, 2-phase/2-revise/haipipe-paper-revise-*); phase strip sub-tracks now render as 'probe: cite/val/disp'.

## [3.0.1] — 2026-07-03

- per-paper folder renamed 5-editing -> 5-section-edit; all paths and trigger words updated. No workflow changes.

## [3.0.0] — 2026-07-02

- two-axis restructure. Phase workers moved to 2-phase/ (shared across stages). GATHER becomes agent-only (flag issues, no mid-phase human gate; PLACE moves to CHECK). POLISH works on both outline .md and tex (outline is primary, tex is compiled output). CHECK becomes the single human gate (verify citations on Scholar, verify values, approve displays, 6-axis pass/fail). _LOG format gets [PHASE] tags. Per-stage files: narrative and pitch also get _CITATION_. Citation: no bibtex in _CITATION_ (plain text only), provenance tracking.

## [2.1.0] — 2026-06-29

- renamed phases PLAN→DRAFT, WRITE→POLISH (DRAFT includes draft sentences, POLISH is venue-quality rewrite not cold-start). Added dual status strip (paper-level + section-level). Added section dashboard showing all sections' layer status. Per-stage _PROBE/ folders with 1-probe-plans/ as cross-paper index. Added _EVIDENCE_ for claims, _DISPLAY_ for narrative.

## [2.0.0] — 2026-06-29

- combined haipipe-paper-editing + haipipe-paper-edit into one skill.

## [unversioned]

- 1.4.0-1.0.0: see prior changelog.

haipipe-paper-section-edit — Changelog
======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 5.1.0 — 2026-07-14

- "Probe escalation": sweep paper-local -> raise a question SECTION -> ② MATCH -> ③ DISPATCH only what MATCH cannot close. The "gateway probe" tier is gone; no inline-search tier exists at any depth.
- The DRAFT ⛔ STOP presents STRUCTURE + the QUESTIONS RAISED (ref/outline-format.md + ref/section-template.md updated to match).
- Citation provenance `🤖 harvested` = came via DISPATCH -> discovery -> the QA file (was "via gateway").
- ref/outline-format.md: the 1-probes/README.md board row carries a `state` and a `file:` pointer (was `status` + `card:`).

## [4.5.1] -- 2026-07-10
## 5.0.0 — 2026-07-14

- PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1-claims/1-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
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
- Venue header semantics pinned: blueprint (2-venue.md block) = BINDING (budget, structure, density); style file(s) = REFERENCE ONLY (advisory -- arc/moves/exemplars; deviation never fails CHECK). Hybrid sections (methods + results flavor) may list multiple style refs, dot-separated.

## [4.2.0] -- 2026-07-09

Changed (JL: "make the section aware of the venue-specific requirement -- give them the link")
- Section .md gains a VENUE HEADER under the H1: venue pin, section-type mapping, blueprint pointer (2-venue.md block -- stays authoritative), and the deep-dive style link (the [source:] tag RESOLVED to a real pack path at scaffold, layout-agnostic find; pack absent -> "(pack missing -- blueprint only)" + CHECK flag). Later phases follow the recorded link instead of re-deriving the 3-hop tag chain. Mirrored in ref/outline-format.md.

## [4.1.1] -- 2026-07-09

Changed (JL: "add the numbers of total words to it as well")
- Structure overview block now carries per-paragraph `N sentences · ~M words` and a closing `total:` line (¶ / sentences / ~words) checked against the venue budget from 2-venue.md; recount at draft and after REVISE; over budget -> flag, never silently trim. Mirrored in ref/outline-format.md.

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
- Stale comment-first REVISE block (Round 1 change-NO-prose) DELETED -- contradicted wiki/02 + revise hub ("no comment-first; change directly + why-comments"); leftover from the retired edit-cycle (missed by A17).

## [3.2.0] -- 2026-07-08

Changed
- Venue consumption rewired to lockfile semantics: DRAFT step 1 reads the paper's 0-lifecycle/2-venue/2-venue.md FIRST (this section's Structural Blueprint block + Writing Principles); pack style-profile/per-section style.md resolution demoted to fallback when 2-venue.md is absent, or reached as deep dives via its [source] tags; stale provenance -> note "venue contract stale", never silent pack re-reads (norm-digestion harvest noted as a staleness source).

## [3.1.4] — 2026-07-04

Fixed
- Probe-plan convention wording: `1-probe-plans/README.md` is a cross-STAGE index (was "cross-paper") and the PP numbering authority.

## [3.1.3] — 2026-07-03

Changed
- Added the Phase Transition Contract pointer (wiki/08): announce every phase boundary, no silent phase skips (explicit logged verdict only), CHECK never implicit.

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

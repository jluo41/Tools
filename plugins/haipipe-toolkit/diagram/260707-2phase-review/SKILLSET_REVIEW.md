SKILLSET REVIEW — paper/2-phase
================================

Date: 2026-07-07 · Protocol: /haipipe-skill-diagnose v1.2.0
Auditors: 4 read-only subagents (A: 0-draft+layer docs · B: 1-probe · C: 2-revise · D: 3-check)
Trust gate: PASS on all four (A 7/7, B 5/5, C 6/6, D 5/5 spot-checks exact on disk).
Prior context: 6 skills were already fixed earlier today under explicit approval
(Tools commits fd2bc92, a6df2f4); those fixes are NOT re-reported. This ledger is
the residue found by the full-protocol pass.

Findings: 56 total → 56 CLOSED (53 fixed + C9/C10/C11 moot via the T7 weaving merge).
All 10 threads resolved and executed; every decision archived verbatim in the owning CHANGELOG.
Zero open `> JL:` slots — the commit gate is clear.


Part 0 — Architecture ruling (DECIDED 2026-07-07, supersedes T2/T5)
--------------------------------------------------------------------

JL ruling (verbatim): "these worker of citaiton or vlaue or display, they are the things like:
probes have already done things in the discovery tasks and insights, they are the harveste agents
to check the content and genearte the report accordingly. The don't need to restart the whole
probe process, they are just one step within the whole probe" — confirmed "Yes, this is true!
Pelase go ahead for it." Earlier same session: "I think search should be done with
haipipe-discovery-orchestrated agent."

The model: ONE probe pipeline; citation/values/display are its HARVEST step, not sibling pipelines.
Paper-side may follow pointers; only the gateway may find things.

```
PP card (need) → gateway SWEEP (reuse|enrich|fresh) → discovery/task orchestrators
  → evidence LANDS (discoveries/sources.md · tasks/results · insights/ · 0-displays/)
  → HARVEST (the workers): citation pick_list→_CITATION_ · values refs→_VALUES_
                           · display units→_DISPLAY_+tex links
  → PP card refs + takeaways · checker verifies OWED→accepted per lane
```

Consequences (the R1 work item, executed at FIX):
- probe-citation: SEARCH phase RETIRED (inline WebSearch/Semantic Scholar out; WebSearch/WebFetch
  leave allowed-tools); skill reframed as the citation harvester; "light probe = WebSearch"
  vocabulary removed (light/full mean ONLY the gateway modes). Gaps noticed while harvesting →
  probe-plan suggestions (rule already at :137, becomes the identity).
- probe-values: TRACE-as-grep RETIRED — values reads ONLY paths named in the PP card refs
  (pointer-following); "which task has this number" is gateway SWEEP work.
- probe-display: ROUTE (/haipipe-task direct) MOVED — unit generation is commissioned through the
  probe (PP card → gateway → task orchestrator; SWEEP answers "does this unit already exist?");
  worker keeps LINK + registry.
- Gap-finding (old AUDIT phases) lives UPSTREAM: DRAFT % TODO flags + hub BOOKKEEP → PP plans.
- REVIEW phases (pre-submission walks) are document QA — kept, but belong with CHECK/build-submit,
  not inside harvest.
- Harvesters become thin subagent shells (card-creator pattern: headless skill + mechanical
  acceptance), extending the existing harvest/haiku pattern to all three lanes.
- Enforcement (was T2) generalizes: PP card carries per-lane obligations (pick_list / value refs /
  unit refs → OWED→accepted); PROOF 3 covers them; check-probe-cards.sh FAILs on owed-but-missing
  _CITATION_/_VALUES_/_DISPLAY_; strip cannot show probe ✅ over an owed lane. (B5 fix, tri-lane.)
- Files touched: 1-probe/{probe hub STEP 3, probe-citation, probe-values, probe-display,
  ref/per-stage-dispatch.md, check-probe-cards.sh} + skills/probe/haipipe-probe/SKILL.md flow
  diagram (cross-bucket) + probe/agents/haipipe-probe-orchestrator-agent.md return contract
  (pick_list generalizes to per-lane pointers) + new thin harvester agent shells.
- Findings folded in: B5 (direction set, execution here) · B8/B10 (superseded) · T2/T5 (resolved).


Part 1 — Root causes (先看这个)
--------------------------------

① 🚚 搬家没改地址 (migration debris) — 23 findings. Two rename waves (gather/polish→probe/revise;
   4-edit→2-phase DPRC) left satellites unrenamed: 7 feedback/README point at retired names, the
   whole REF/ quartet still teaches the retired 4-edit agent cycle, 1-probe/README.md is a
   different document entirely, draft's template table is off by one level on all 5 rows.
② 📄 路由层失真 (routing drift) — 3 findings. `[FORWARD -> CLAIMS]` has writers but NO reader in
   claims; USAGE still routes DRAFT to archived write-style workers.
③ ⚔️ 内部矛盾 (internal contradictions) — 13 findings. Biggest: three docs promise the CHECK gate
   runs check-probe-cards.sh — the CHECK skill never references it AND the checker passes
   `status: planned` cards; router says it dispatches weaving, weaving says router is a sibling.
④ 🪝 层间耦合 — 0 findings (clean).
⑤ 🧯 有令无兵 (unenforced obligation — NEW class: a stated must with no durable residue / proof /
   deterministic check / gate wiring) — 11 findings. The seed-stage harvest miss (JL caught it
   live) is B5; plus checks.sh strictness holes (bibtex types, XXX false-fail, silent no-bib skip,
   warn-only em-dash, comments not stripped, unguarded --depth).
⑥ 📑 复述漂移 (duplication drift — NEW class: same rule 4+×, edits will diverge) — 4 findings.
⑦ 🧱 脚手架不齐 (scaffolding inconsistency) — 2 findings (humanizer + probe-display lack feedback/).


Part 2 — Findings by class
---------------------------

### ① 搬家没改地址 — 23 [all M]

- [x] **A1** 🔴 `[M]` draft/SKILL.md:49-54,56 — template registry: all `../ref/<stage>-template.md` rows resolve to nonexistent `1-lifecycle/<stage>/ref/`; real files are in each stage skill's own `ref/`. Fix: drop the `../` on 5 rows.
- [x] **A2** 🟡 `[M]` draft/SKILL.md:30 — "artifact spec (in `1-lifecycle/{stage}/SKILL.md`)" dead; real: `1-lifecycle/{stage}/haipipe-paper-{stage}/SKILL.md`.
- [x] **A4** 🟡 `[M]` draft/SKILL.md:182 — "archived to `2-phase/_archive/`"; archive is at paper root `_archive/`.
- [x] **A7** 🟡 `[M]` README.md:40 — tree draws `_archive/` under 2-phase; it lives at paper root.
- [x] **A8** 🟡 `[M]` README.md:24-26 — REF/ subtree lists 1 of 6 files. Fix: list all six or say "see REF/".
- [x] **A9** 🟢 `[M]` README.md:25-28 — tree omits the probe + revise HUBS that WIRING.md lists. Fix: add both hub rows.
- [x] **A10** 🟡 `[M]` WIRING.md:23,28 — "`_archive/`" implies under 2-phase; qualify as paper-root.
- [x] **A11** 🟡 `[M]` USAGE.md:28 — DRAFT "picking a write-style worker (conference/scientific/systems)"; those were archived in v3.2, draft hub has NO workers. Fix: reads stage template from 1-lifecycle/; venue style lands in REVISE.
- [x] **A13** 🟢 `[M→merged A11]` TODO.md:8 — "[x] USAGE/WIRING updated (done)" is false while A11 stands; reopen or fix A11 in same pass. (Evidence-arbitrated: fix A11, leave TODO checked.)
- [x] **A14** 🟡 `[M]` REF/edit-cycle.md:6 — `../agents/` dir does not exist. (Fate decided by T9.)
- [x] **A15** 🟡 `[M]` REF/edit-cycle.md:9 — `tools/haipipe-paper-section-edit-diagram` does not exist anywhere. (T9.)
- [x] **A16** 🟡 `[M]` REF/edit-cycle.md:16,21,27,30 — retired agents paper-edit-{format-checker,annotator,improver,cleaner}. (T9.)
- [x] **A18** 🟡 `[M]` REF/paragraph-indexing.md:85-86 — retired agents named as sentence-level workers.
- [x] **A19** 🟡 `[M]` REF/sentence-format.md:55 — "done by the `paper-edit-format-checker`" (retired).
- [x] **A20** 🟢 `[M]` REF/{edit-cycle,paragraph-indexing,sentence-format,tex-file-anatomy}.md headers — "4-edit / shared" labels; relabel to current architecture.
- [x] **B1** 🟡 `[J→T4]` 1-probe/README.md:1 — entire file is a "paper/sections Per-Section Playbooks" doc, not a probe README.
- [x] **B2** 🟡 `[M]` {probe,probe-citation,probe-values}/feedback/README.md:1,4 — `haipipe-paper-gather*` retired names ×3 skills.
- [x] **B3** 🟡 `[M]` probe/ref/per-stage-dispatch.md:87 — `../../wiki/` two levels short; real: `../../../../wiki/`.
- [x] **B4** 🟡 `[M]` probe-values/SKILL.md:12 — predecessors lists ITSELF. Fix: name the pre-merge manual-review-values skill.
- [x] **C1-C4** 🟡 `[M]` {revise,revise-content,revise-weaving,revise-results}/feedback/README.md:1,4 — `haipipe-paper-polish*` retired names ×4 skills.
- [x] **C13** 🟢 `[M]` revise/SKILL.md:42 — bare `REF/prose-quality.md` resolves wrong from router dir; write `../../REF/prose-quality.md`.
- [x] **D10** 🟡 `[M-arbitrated]` proof-checker/SKILL.md:24,419,471 — only legacy `/paper-writing` named as caller; current caller haipipe-paper-check (its SKILL:158,329 dispatches proof-checker) never named. Evidence: current shipped check SKILL beats stale prose → name check as primary caller, keep /paper-writing as legacy note.

### ② 路由层失真 — writer-without-reader

- [x] **A5/B9** 🟡 `[J→T3]` draft/SKILL.md:141 + seed/SKILL.md:77,158 — `[FORWARD -> CLAIMS]` written to seed _LOG; grep of 1-lifecycle/1-claims = ZERO readers. The deferred internal-data probe silently dies at the seed→claims handoff.
- [ ] **A11-route** (counted under ①) — USAGE routes DRAFT to archived workers.

### ③ 内部矛盾

- [x] **A3/B6/D1** 🔴 `[J→T1]` draft:116-117 + seed:159 + probe:9 vs 3-check/* — three docs promise "the CHECK gate runs check-probe-cards.sh and cannot go green over planned cards"; the CHECK skill has ZERO references to that script, checks.sh doesn't run it, AND the checker's own `case` passes `planned|dispatched` cards silently (check-probe-cards.sh:67). The DRAFT-may-search/PROBE-must-dispatch invariant is enforced by nothing.
- [ ] **A12** 🟢 `[J→T8]` USAGE.md:48 vs draft:121 + REF/prose-quality.md:34 — `> JL:`-initials-asked vs hardcoded `> USER:`.
- [x] **A17** 🟡 `[J→T9]` REF/edit-cycle.md — whole file teaches the comment-first 5-stage cycle that prose-quality.md:40,48 explicitly BANS.
- [x] **B7** 🟡 `[M-arbitrated]` probe-citation/SKILL.md:440-446 — `_CITATION_` template embeds a markdown table that this file's own rule (:123), probe's hard rule (:128), and the shipped acceptance grep (`grep -c '^|' == 0`) all forbid. Evidence: shipped grep beats template prose → convert to bullet lines.
- [x] **B8** 🟡 `[J→RESOLVED by Part 0]` probe-citation/SKILL.md:225 — citation SEARCH launches inline WebSearch agents; probe hard boundary says NO inline search for workers. RESOLVED: SEARCH retired entirely (JL: "search should be done with haipipe-discovery-orchestrated agent"); execution in R1.
- [x] **C5** 🟡 `[M]` revise-results/SKILL.md:1-9 — frontmatter missing argument-hint + allowed-tools (only skill of 12; defaults to all-tool grant).
- [x] **C6** 🟡 `[M]` revise-results/SKILL.md — never cites `../../REF/prose-quality.md` though router:42 asserts ALL workers read it. Fix: add Before-you-start pointer.
- [x] **C8** 🟡 `[M]` revise-humanizer/SKILL.md:20-21 — flat "catalog lives at… read it before every audit" contradicts line 31 NOTE (file absent). (Direction set by T6.)
- [x] **C11** 🟡 `[J→T7]` revise/SKILL.md:34 vs revise-weaving/SKILL.md:57,63,694 — router "dispatches weaving" vs weaving "revise is a sibling, not a child" + routes back to it. Mutual dispatch = loop risk.
- [x] **D2** 🟡 `[M]` check/SKILL.md:25 — decision listed as 3 outcomes; canonical 5 (proceed/restart/new round/accept/park). CHANGELOG 1.6.0 claimed "reconciled everywhere" — this line missed.
- [x] **D3** 🟢 `[M]` check/SKILL.md:44-48 — flow diagram shows 3 of 5 outcome branches; annotate or add.
- [x] **C7** 🟡 `[J→T6]` revise-humanizer/SKILL.md:10 — metadata.source asserts "Reference copy at Tools/references/academic-humanizer/" — dir EMPTY on disk.

### ⑤ 有令无兵 (unenforced obligations + checker defects)

- [x] **B5** 🔴 `[J→RESOLVED by Part 0]` probe/SKILL.md:103 — harvest obligation enforced NOWHERE durably: PROOF 3 doesn't cover it; check-probe-cards.sh has zero pick_list/_CITATION_ awareness; pick_list exists only in the transient orchestrator return (no file residue); strip allows probe✅ with cite⬜. This is the live seed-stage incident. Direction DECIDED (tri-lane OWED→accepted, Part 0); execution in R1.
- [x] **B10** 🟡 `[M→R1]` check-probe-cards.sh:52 — checker never scans _CITATION_/_VALUES_/_DISPLAY_, so no-bibtex/no-tables hold only during a harvest run. Superseded into R1 (per-lane checker pass).
- [x] **D4** 🟡 `[M]` checks.sh:98 — bibtex-leak grep covers 7 entry types; @conference/@inbook/@online/@unpublished/etc. pass undetected. Fix: `^\s*@[A-Za-z]+\{`.
- [x] **D5** 🟡 `[M]` checks.sh:89 — `\bXXX\b` false-FAILs double-blind placeholders (\author{XXX}); exit 1 blocks the gate. Fix: drop XXX or require comment context.
- [x] **D6** 🟡 `[M-arbitrated]` checks.sh:107-126 — \cite present + zero .bib found → silent skip (false-negative); partial bib under --depth → false broken-cite. Evidence: a silent skip is strictly worse than a warning → emit ⚠️ "no .bib found, try --depth N"; document the partial-discovery caveat.
- [x] **D7** 🟡 `[J→T10]` checks.sh:71-75 + check/SKILL.md:136 — em-dash is ⚠️-only (exit stays 0) while the SKILL row reads as an absolute "zero matches" rule; a gate keying on exit code lets em-dashes through.
- [x] **D8** 🟢 `[M]` checks.sh:81,89 — AI-voice + TODO greps don't strip `%` comments (em-dash awk does). Fix: reuse the comment-stripped stream.
- [x] **D9** 🟢 `[M]` checks.sh:41-42 — `--depth --compile` sets DEPTH="--compile" → find errors. Fix: validate `^[0-9]+$`.

### ⑥ 复述漂移

- [x] **A6** 🟢 `[M]` draft/SKILL.md:9,97-117,137-138 — fuel-not-evidence rule stated 4+×. Fix: one normative home in Step 4, back-references elsewhere.
- [x] **B12** 🟢 `[M]` probe-citation/SKILL.md — no-bibtex restated 5+× (30 "bibtex" hits). Keep Hard-Boundaries home + cross-refs.
- [x] **D11** 🟢 `[M]` check/SKILL.md:3,9,16,355 — ONLY-human-phase ×4 counting frontmatter; optional trim.

### ⑦ 脚手架不齐

- [x] **B11** 🟢 `[M]` probe-display/ — only probe worker with no feedback/ inbox. Fix: add matching README (probe naming).
- [x] **C12** 🟢 `[M]` revise-humanizer/ — only revise worker with no feedback/ inbox. Fix: add matching README (revise naming).


Thread resolutions (FIX executed 2026-07-07; decisions archived verbatim in each owning CHANGELOG)
----------------------------------------------------------------------------------------------------

- **T1** (JL: "同意你的意见") → EXECUTED. haipipe-paper-check 1.7.0 step 1 runs `check-probe-cards.sh <paper_root>` at the gate (FAIL = cannot green); the checker gained the `planned|dispatched → probe-not-run` FAIL arm. Regression-tested on a synthetic paper: planned card, OWED lane, bibtex leak all FAIL; clean card set PASSes.
- **T2** (Part 0) → EXECUTED as R1: lane obligations (pick_list/value_refs/unit_refs · harvest: OWED→accepted) in probe hub 3.1.0 STEP 3 + PROOF 3, card anatomy in probe layer 7.2.0 (cross-bucket), checker FAIL rule, strip gate rule in per-stage-dispatch.
- **T3** (JL: "同意。") → EXECUTED cross-bucket: haipipe-paper-claims 4.1.0 DRAFT opens by consuming seed's `[FORWARD -> CLAIMS]` pointers + new done-criterion; draft 3.5.0 documents the reader side.
- **T4** (JL: "同意提议。") → EXECUTED: old sections-playbook content archived to `paper/_archive/README-sections-playbooks.md`; 1-probe/README.md rewritten as the probe-bucket front page (hub + 3 harvesters + enforcement).
- **T5** (Part 0) → EXECUTED as R1: citation 2.0.0 Phase 2 SEARCH retired → ROUTE; one door (gateway → discovery → pick_list → harvest); WebSearch dropped from allowed-tools (WebFetch kept for pointer-following verification only).
- **T6** (JL: "做B") → EXECUTED, and the mystery solved: `references/academic-humanizer` was a HALF-REGISTERED SUBMODULE (gitlink 02281d8 committed, no .gitmodules mapping — fresh checkouts silently got an empty dir). Cloned at the exact pinned commit, .gitmodules entry added; the full catalog (SKILL.md + examples/ + assets/) is on disk. humanizer 2.2.0 documents the submodule + recovery command.
- **T8** (JL: "统一 user") → EXECUTED: USAGE.md section C canonical actor id is `> USER:`; initials (`> JL:`) tolerated as a read-alias, every documented example and agent-written slot uses USER.
- **T9** (JL: "挪走吧。") → EXECUTED: REF/edit-cycle.md → `paper/_archive/REF-edit-cycle.md`; A14/A15/A16 moot with it; A18/A19/A20 fixed in the surviving REF files (zero 4-edit/paper-edit-*/edit-cycle residue).
- **T10** (JL: "统一提议。") → EXECUTED: em-dash ⚠️→❌ in checks.sh (same tier as TODO); AI-voice/Pn.Sn stay ⚠️; validated on a live paper (exit=1 on real em-dashes).

R1 note: the "thin harvester agent shells" are implemented as the existing dispatch PATTERN (cheap-tier Agent reading the worker SKILL headless — the citation-harvest/haiku pattern extended to values + display via harvest-acceptance.md lane sections), NOT as new registered agent-type files; no new agents/ entries were needed.

### T7 — RESOLVED (JL: "For T7, what is your thoughts? maybe just go into Content")

EXECUTED as option B: weaving merged into content. revise-content 1.2.0 pass is now
section → paragraph → WEAVE → sentence (ref/weaving.md: ARC/HINGES/RHYTHM + severity +
roles; write-principles + example moved in). The 734-line orchestration apparatus
(pre-DPRC gates/plan-blocks — C11's root cause) archived UNMERGED at
paper/_archive/paper-revise-weaving-skill/. Router 1.3.0 roster 4→3; all 6 live
referrers updated (router, humanizer, section-edit, README, USAGE, WIRING);
grep 'revise-weaving' outside archives/changelogs = zero. C9/C10/C11 → MOOT.

### Post-eyeball addendum (JL rulings on the review targets, 2026-07-07)

- Items 1-3 (strictness changes, citation feel-change, card contract): approved as-is.
- Item 4 (JL: "Our skill should never refer to the references content") → catalog VENDORED
  into humanizer 2.3.0 (ref/pattern-catalog.md + ref/before-after.md @ upstream 02281d8);
  all runtime references/ pointers removed; house rule codified: skills are self-contained,
  references/ submodules are archival provenance only.
- Stale probe-lifecycle block in 2-phase/README.md (predated R1) rewritten to the harvester
  model; USAGE.md residual `> JL:` recipe lines unified to `> USER:` per T8.


Part 3 — Coverage honesty
--------------------------

- NOT audited: 1-lifecycle stage skills' interiors (seed/claims/pitch/narrative/display/section-edit)
  — only grepped for cross-stage tokens (FORWARD, planned, gate claims). T1/T3 fixes touch claims
  (cross-bucket) and need your explicit OK.
- NOT audited: paper/wiki/* content (08-stage-gate.md and 02-comment-lifecycle.md verified to exist
  and be pointer-consistent only); probe/haipipe-probe (project-side) beyond the PPNN-anatomy
  pointer check; 3-build-submit/ whole-paper skills.
- NOT executed: checks.sh / check-probe-cards.sh live runs against a real paper during this audit
  (read-only pass; checks.sh WAS validated live earlier today on Paper-FairGlucose-icml2026).
- Runtime paper-folder paths (0-displays/, tasks/, PP-card instances) unverifiable — no live paper
  folder in this repo.
- CHANGELOG historical entries treated as frozen history, not audited for factual correctness.
- Auditor D noted `--compile` gracefully warns when no 1-compile.sh exists — expected (paper-local).

Fixed-earlier context (not in the counts): check 1.6.0 rewrite + checks.sh shipped (fd2bc92);
revise-weaving 5 dead dispatches, probe-citation dead script + self-predecessors, proof-checker
4 legacy paths, revise-content frontmatter, revise-humanizer path (a6df2f4).

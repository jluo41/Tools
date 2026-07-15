SOP — Application Paper-Alignment, Round 2 (2026-07-07)
=========================================================

Status: PHASES 1+2 EXECUTED (JL approved "can we apply it now", 2026-07-07). Remaining: full DPRC bench exams (§8; mechanical validation done) + archive this SOP into haipipe-application/CHANGELOG.md and delete (round-1 convention).
Owner: JL. Executor: CC.
Baseline: application = paper@765696f port (round 1, exams passed 2026-07-06; SOP archived in haipipe-application/CHANGELOG.md §5.0.0). Paper has since moved to b2c5a23 (2026-07-07): probe 3.0.0→3.1.0 mechanical enforcement, check 1.6.0/1.7.0 checks.sh, draft 3.4.0/3.5.0 WebSearch rule, seed 3.5.0 + claims 4.1.0 FORWARD handoff, weaving merged into revise-content, sub-workers 2.0.0 pointer-following recast. Application's 2-phase workers were written against the pre-3.0.0 probe and pre-1.6.0 check contracts and now lag.

1. Target mental model
----------------------

One sentence: round 1 gave application paper's SKELETON (spine, buckets, DPRC, folderless probe); round 2 gives it paper's ENFORCEMENT — the same "trust nothing that is not mechanically checkable" turn paper took on 07-06/07-07 (checker scripts, PROOF blocks, OWED debts, DRAFT-search/PROBE-dispatch separation, FORWARD pointer ledger), venue-scaled where application's deltas demand it.

```text
PAPER AT HEAD (b2c5a23)                              APPLICATION TODAY (post round 1)
probe 3.1.0: BOOKKEEP→DISPATCH→TRANSLATE→VERIFY      probe 1.x: BOOKKEEP→DISPATCH→TRANSLATE, no VERIFY
  check-probe-cards.sh; PROOF 1-4 blocks;              step, no checker, no PROOF blocks, no lane
  lane debts `harvest: OWED`; ACQUIRE→HARVEST          debts; harvester model unnamed
check 1.7.0: checks.sh (8 mechanical checks);        check 3.0.0: persona/attendance gate, prose
  probe-card FAIL blocks the gate green;               criteria only; no deterministic checks; no
  > CHECK: comments seeded in working docs             probe-card wiring; READ-ONLY on artifacts
draft 3.5.0: WebSearch = DRAFT-only orientation      draft 1.0.0: no WebSearch; the DRAFT/PROBE
  fuel; buffers `status: planned` skeletons;           evidence line exists only as prose
  "DRAFT may search; PROBE must dispatch"
seed 3.5.0 + claims 4.1.0: seed probes =             seed 3.1.0 + claims 5.0.0: seed probe scope
  feasibility only; internal-data needs →              unscoped; no FORWARD pointer contract either
  [FORWARD → CLAIMS] pointer; claims DRAFT             side
  consumes pointers; unconsumed fails CHECK
PREFERENCES: "always run the REAL probe" entry       PREFERENCES: entry absent (rule is family-generic)
```

2. Invariants (must survive round 2)
------------------------------------

> ⚠️ SUPERSEDED IN PART — the PROBE LAYER (2026-07-14). `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` v3 (approved JL,
> rulings R1-R18) replaced the card/gateway model this SOP ported. Everything below about PPNN
> *cards*, per-stage `_PROBE/` folders, the `1-probe-plans/` index, `status: dispatched|verdicted`,
> and the probe *gateway* is HISTORY: read it as a record of what was, not as a contract.
> What SURVIVES intact: the mirror-paper-exactly principle, the four PROOF blocks, the
> family-local checker fork (`check-probe-cards.sh`, same filename), the venue-scaled lane HOOKS
> (no probe sub-workers), and the DRAFT/PROBE evidence line. Current contract:
> `../probe/haipipe-probe/SKILL.md` (v8.0.0) + `2-phase/1-probe/haipipe-application-probe/SKILL.md` (v4.0.0).

- Round-1 invariants all stand: four evidence principles; application deltas (_audience/, venue-gated stages, settlement depth, 0-artifacts/ markdown, deploy/iterate tail, in-project folders); stage-owns-WHAT / phase-worker-owns-HOW; zero upstream contract changes to discovery/task.
- The PROBE LAYER MIRRORS PAPER EXACTLY, and that is the invariant that matters (the structure it names has since changed): probe FILES at `1-probes/PPNN_<topic>.md`, one file per TOPIC, one SECTION per question (`serves`/`target`/`state`/`q-executor`/`a-consumer`) + one `## Why`; binding by PATH to `<task-folder>/QA/<n>-<slug>.md`; dispatch straight to the task/discovery orchestrators. Identical to paper — which is what keeps checker reuse cheap.
- Application keeps NO probe sub-workers (citation/values/display stay venue-scaled hooks inside the one probe worker); `_VALUES_` always, `_CITATION_` sectioned venues only.
- Bench evidence folders (examples/ProjApp-SMSDesign/applications/03, 04) stay as round-1 validation history; round-2 exams may reuse them but not rewrite their round-1 artifacts.

3. Design resolutions (proposed; JL vetoes here at review)
----------------------------------------------------------

- R1 — probe VERIFY, ported: application probe worker gains paper's STEP 4 (run the card checker; FAIL on `status: planned|dispatched|failed`, dangling refs, OWED lanes) and the four PROOF blocks (project-root listing, literal Agent dispatch calls, refs+ls resolution, checker output). Checker = a FORK of paper's check-probe-cards.sh (stage-strip.sh precedent: same conventions, family-local copy): same `0-lifecycle/*/_PROBE/PP*.md` tree and brace-aware ref expansion; lane scan venue-scaled — `_VALUES_` lane always checked, `_CITATION_` lane only when the pinned venue is sectioned, `_DISPLAY_` lane only if the venue's artifact has display units. Paper's ref/per-stage-dispatch.md is re-derived for the application spine (which stage dispatches which mode); harvest-acceptance greps adopted for whichever lanes fire.
- R2 — check enforcement, ported venue-scaled: application check worker gains (a) gate wiring — step 1 runs the R1 card checker, any FAIL blocks the gate green; (b) a family-local checks.sh with the MARKDOWN-SAFE subset only: em-dash (❌, house rule), AI-voice tells (mawk-safe 1.7.0 grep), TODO/FIXME, bibtex-in-markdown guard; tex checks (\cite, \ref, \label, Pn.Sn, --compile) deliberately NOT ported; (c) `> CHECK:` comment seeding in 0-lifecycle STAGE DOCS ONLY — 0-artifacts/*.md stay clean because the artifact IS the deliverable text (unlike paper's .tex, where % comments never render); artifact-level findings go to the Gate Ledger notes column. RULED: JL 2026-07-07 (stage-docs-only over artifact HTML-comments and over keeping check fully read-only); persona/attendance machinery unchanged on top.
- R3 — DRAFT/PROBE evidence line, ported: draft worker gains WebSearch+WebFetch as DRAFT-only orientation fuel — findings may shape prose and buffer `status: planned` PPNN skeletons, never write refs/findings into cards; the R1 checker is what makes the rule mechanical (planned cards surviving to CHECK = FAIL). PREFERENCES.md gains the family-generic "always run the REAL probe in the PROBE phase" entry (JL 2026-07-07, paper-side origin, applies verbatim here).
- R4 — seed feasibility + FORWARD handoff, ported: seed probe scope narrows to feasibility (novelty + external-data obtainability); internal-data needs register as `[FORWARD -> CLAIMS] PPNN_<slug>` pointer lines in _LOG_0-seed.md; claims DRAFT opens by grepping seed's _LOG for pointers and materializing or explicitly declining each; unconsumed pointer fails claims CHECK. For application, "internal data" = the intervention's own cohort/engagement data — same split as paper.
- R5 — revise and sub-workers, NOT ported: single revise worker stands (round-1 ruling; paper's weaving-into-content merge is a paper-internal consolidation, and weaving/humanizer-catalog knowledge is pulled in only when a sectioned-venue artifact demands it). No citation/values/display sub-skills; instead the probe worker's venue-hook section states the 2.0.0 contract those hooks must follow when they fire: pointer-following + gateway dispatch only, mechanical acceptance greps, no inline search.
- R6 — standing alignment watch: paper drifted the SAME DAY as the round-1 port; to stop chasing, haipipe-application/PREFERENCES.md gains one line — any commit touching paper/2-phase/ or paper/1-lifecycle/{0-seed,1-resource,1-claims} triggers an application port review before the next application work round. (Cheap: a grep of `git log` at enter time is enough; no automation proposed.) FIRED 2026-07-14 — paper added `1-resource`; reviewed, port DEFERRED, divergence stated in §6.

4. Change list — phase 1 (load-bearing)
----------------------------------------

| # | File | Change |
|---|------|--------|
| 1 | 2-phase/1-probe/haipipe-application-probe/SKILL.md → 2.0.0 | STEP 4 VERIFY; PROOF 1-4 blocks; lane debts `harvest: OWED` (venue-scaled lanes per R1); harvester vocabulary (ACQUIRE→HARVEST, one pipeline); explicit `0-lifecycle/<stage>/_PROBE/` path contract; venue-hook contract per R5; fix frontmatter 1.0.0 vs CHANGELOG 1.1.0 mismatch |
| 2 | 2-phase/1-probe/haipipe-application-probe/check-probe-cards.sh | NEW fork of paper's checker: same tree + expand_ref; venue-scaled lane scan (reads pinned venue from 2-venue.md / STATUS) |
| 3 | 2-phase/1-probe/haipipe-application-probe/ref/{per-stage-dispatch,harvest-acceptance}.md | NEW, re-derived for the application spine + venue-scaled lanes |
| 4 | 2-phase/3-check/haipipe-application-check/SKILL.md → 4.0.0 | Gate wiring (card-checker FAIL blocks green); checks.sh invocation in step 1; `> CHECK:` seeding in stage docs only, artifact findings → Gate Ledger notes (R2c as ruled); persona/attendance untouched |
| 5 | 2-phase/3-check/haipipe-application-check/checks.sh | NEW markdown-safe subset (em-dash ❌, AI-voice mawk-safe, TODO/FIXME, bibtex-in-md); ✅/⚠️/❌ report lines; exit 0 = no ❌ |
| 6 | 2-phase/0-draft/haipipe-application-draft/SKILL.md → 1.1.0 | + WebSearch, WebFetch in allowed-tools; DRAFT-only fuel rule + buffered planned skeletons + "DRAFT may search; PROBE must dispatch" principle |
| 7 | 1-lifecycle/0-seed/haipipe-application-seed/SKILL.md → 3.2.0 | Probe scope = feasibility only; [FORWARD → CLAIMS] pointer registration in _LOG_0-seed.md; PROBE must dispatch the real worker |
| 8 | 1-lifecycle/1-claims/haipipe-application-claims/SKILL.md → 5.1.0 | DRAFT opens with FORWARD-pointer reader (materialize or decline each); unconsumed pointer added to CHECK done-criteria |
| 9 | haipipe-application/PREFERENCES.md | + real-probe entry (R3) + alignment-watch line (R6) |
| 10 | 2-phase/README.md | + ONE-pipeline/HARVEST architecture note (mirrors paper 2-phase/README.md lines 61-76, venue-scaled) |

5. Phase 2 — peripheral sweep (after phase 1 lands)
----------------------------------------------------

- 2-phase/USAGE.md + WIRING.md: NEW thin application versions (recipes, effort dial, phase-restart, routing) mirroring paper's; SKILLSET_REVIEW.md is a paper process artifact — NOT ported.
- wiki/03 + wiki/08: probe mechanics paragraphs updated (VERIFY step, OWED, checker as the gate's teeth); wiki/06 skill-tree table gains the two new scripts + ref/ folder.
- Router SKILL.md + lifecycle orchestrator: one-line mentions of the VERIFY step and checks.sh where the DPRC loop is described; enter console unaffected (Gate Ledger contract unchanged).
- CHANGELOG rollups per touched skill + family rollup (5.1.0).
- Registration check in a fresh session (no renames this round, so expected no-op).

6. What deliberately does NOT change
-------------------------------------

- **DIVERGENCE, STATED (2026-07-14): paper's new `1-resource` stage is NOT ported.** Paper's spine is now `seed > resource > claims > [venue] > pitch > ...` (JL resource ruling, 2026-07-14: what must EXIST for the paper to be testable, does it exist, can it CARRY the claim). Application's spine stays `seed > claims > [venue] > pitch > ...` — SEVEN stages, no resource. This is a KNOWN, DELIBERATE divergence, not drift: R6's alignment watch fires on it (paper/1-lifecycle/ changed), and the port is DEFERRED pending a JL ruling on whether an intervention has a prerequisite question worth its own stage. Until that ruling lands, any claim in this family that the application spine "mirrors paper" means: mirrors it EXCEPT for resource. Do not port the stage on a CC judgement call.
- Revise worker count (one), no weaving/humanizer/results split, no proof-checker (no theorems in interventions), no Pn.Sn or tex checks, no probe sub-worker skills.
- Gate Ledger format in STATUS.md; enter console; stage-strip.sh (already in sync — round-1 bug fixes rode both families).
- _venue/ + _audience/ packs; artifact/deploy/iterate/review skills (3-build-deploy/ and 4-iterate/ untouched this round).
- Upstream probe/discovery/task/insight contracts; bench folders 03/04 round-1 artifacts.

7. Rollback
-----------

Scoped commits on Tools main, clustered: (a) probe axis (rows 1-3), (b) check axis (rows 4-5), (c) draft/seed/claims axis (rows 6-8), (d) docs/prefs (rows 9-10 + phase 2). Rollback = git revert the cluster; no project-side data migration.

8. Exam (bench validation, after phase 1)
------------------------------------------

1. Probe VERIFY: on bench 04 (report venue), run one new full-mode probe end-to-end; watch the checker pass on a clean card, then hand-break a card (`status: planned`, dangling ref, OWED lane) and watch VERIFY and the check gate both FAIL it.
2. Check gate: run the check worker on bench 04 with a planted em-dash + AI-voice tell + TODO (artifact) and one prose issue (stage doc); checks.sh flags all three; the stage-doc issue lands as a `> CHECK:` thread, the artifact findings land in the Gate Ledger notes and the artifact file stays clean; Gate Ledger row written only after fixes.
3. Light venue scaling: on bench 03 (sms), confirm the checker skips _CITATION_/_DISPLAY_ lanes and checks.sh still fires on the message text; strip and console unchanged.
4. FORWARD handoff: new mini-seed with one internal-data need; pointer lands in _LOG; claims DRAFT consumes it; delete the consumption and watch claims CHECK fail.

9. Done criteria
----------------

- [x] JL approves §3 (R2c RULED 2026-07-07: stage-docs-only seeding; execution approved "can we apply it now?", 2026-07-07)
- [x] Phase-1 rows 1-10 landed (4-agent parallel execution, one commit cluster per axis)
- [x] Phase-2 sweep landed (USAGE/WIRING, wiki 03/06/08, router 5.1.0, family CHANGELOG rollup)
- [~] Exams: mechanical validation PASSED — checks.sh fixture tests (dirty flags all four checks exit 1, clean exits 0, seeded `> CHECK:` lines don't re-flag); checker forked and dry-run on bench 03/04 with output byte-identical to paper's checker on the same input. Bench cards themselves FAIL as expected-historical: round-1 cards store refs in YAML frontmatter (canonical PPNN anatomy wants `- refs:` bullet) and bench-04 PP02 was deferred pre-dating the planned-FAILs rule — benches left unmodified per §2. Full DPRC exams 8.1-8.4 (live probe run, gate run, FORWARD handoff) PENDING — run on the next real intervention or on-demand.
- [ ] This SOP archived into haipipe-application/CHANGELOG.md and deleted (same close-out as round 1)

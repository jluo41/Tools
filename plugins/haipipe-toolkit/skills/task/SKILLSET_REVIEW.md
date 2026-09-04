# task/ Skill-Set Review (2026-07-04)


> ⚠️ **SOME PATHS IN THIS REVIEW NO LONGER RESOLVE.** Three of its references
> point at files that have since moved or gone: `../../2_nn/haipipe-task-for-algo/SKILL.md`,
> `../haipipe-nn/ref/overview.md`, and a `../../haipipe-task/ref/…` target. The
> findings may still hold; their addresses do not. Banner added 260822 during a
> toolkit-wide sweep, without re-diagnosing.

Scope: all 44 skills under `skills/task/` plus agents/, root docs, haipipe-workflow. Status: JL approved 2026-07-04; fixes for the covered buckets are APPLIED (outcome notes on each item). Remaining: findings from the 3 pending bucket audits.

Audit method: core (haipipe-task, agents/, README/DESIGN/CHANGELOG/TODO) read line-by-line by the main session and every finding disk-verified; the 9 domain buckets audited by 5 read-only subagents; 3 of their highest-severity claims spot-checked by the main session, 3/3 confirmed.

**Coverage status: core, 2_nn, 4_individual, 5_fit, 6_eval, 7_display deep-audited + fixed. 1_data, 3_end, 8_stata/9_agent/haipipe-workflow: cross-cutting fixes applied tree-wide, but no per-skill deep audit (auditors were stopped — see Part 3).**

How to read:

- 🔴 broken: dead path, wrong name, or a contradiction that misleads execution
- 🟡 stale: works but lies (doc does not match disk or itself)
- 🟢 cosmetic
- `[M]` mechanical fix, no judgment needed. `[J]` judgment call, needs your decision.
- Tick `[x]` = fix it. Leave `[ ]` = skip. Disagree or want a different fix: add a `> JL:` line under the item.

---

## Part 1: root causes (先看这个)

```
① 🚚 搬家没改地址   3 次迁移各留一批旧地址 (A 组, 全部机械修)
   a. haipipe-workflow: project/ -> task/   (2026-07-03)   17 处死路径
   b. haipipe-nn 拆分: ref/layer-*.md -> specialist concepts.md   12 处死路径
   c. reviewer agent 合并改名                                8 处旧名字
② 📄 路由层失真     orchestrator 文档 != 磁盘 (B 组, 大半机械修)
③ ⚔️ 内部矛盾       同一契约两处各说各话 (C 组, 多数要你拍板)
④ 🪝 上层耦合       task 文档点名 paper 层 skill (D 组, 要你拍板)
```

Skeleton is healthy: all audited frontmatters are valid YAML with version + last_updated + CHANGELOG pointer; every skill has a CHANGELOG.md (llm-engine's added in this pass); zero `_shared` refs; zero leftover `> JL:`/`> CC:` threads; no old flat `skills/haipipe-*` paths.

---

## Part 2: findings

### A. 搬家没改地址 (all `[M]`)

- [x] **A1** 🔴 `project/haipipe-workflow/` dead path, 17 refs. haipipe-workflow moved into task/ on 2026-07-03; correct root is `task/haipipe-workflow/`. Sites: `haipipe-task/ref/task-lifecycle.workflow.js:81,108,280`; `haipipe-task/ref/workflow-template.yaml:5,6`; `# Schema:` header line 2 of every specialist `ref/workflow-plan-sample*.yaml` (12 files: for-data, for-algo, for-endpoint, for-individual, for-fit, for-eval, for-display, for-agent, and for-stata's 4 stage samples). Fix: sed `project/haipipe-workflow` -> `task/haipipe-workflow` across the 17 sites. **FIXED 2026-07-04: 16 files, residual grep = 0.**
- [x] **A2** 🔴 `ref/layer-*.md` dead paths, ~30 pointer sites in 2_nn. The 4 layer files became each specialist's `ref/concepts.md` when haipipe-nn split, and nothing was repointed. Sites: `haipipe-nn/README.md:50-53` (file map lists 4 nonexistent docs); `haipipe-nn/fn/fn-review.md:62,85,106,137,240-243`; `fn/fn-generate.md` 11 refs; `fn/fn-test.md:176,183,190,196`; `ref/overview.md:136`; cross-refs in `haipipe-nn-algo/ref/concepts.md:209,230`, `haipipe-nn-tuner/ref/concepts.md:431`, `haipipe-nn-instance/ref/concepts.md:296`, `haipipe-nn-modelset/ref/concepts.md:120`. Fix: repoint each to the owning specialist's `ref/concepts.md` (or `../haipipe-nn/ref/overview.md` for the two self-relative overview refs). **FIXED: all pointer sites repointed file-relative to the owning specialist's ref/concepts.md; README file map rewritten.**
- [x] **A3** 🔴 Retired reviewer name, 8 refs. "Run Script Reviewer agent" survives in ALL 7 `haipipe-task-for-*/fn/scaffold.md` files (data:123, algo:96, individual:101, fit:101, eval:98, display:98, agent:105), and `haipipe-workflow/ref/plan-schema.md:109` still uses `agentType: run-script-reviewer-agent` in its example. That agent was merged into `haipipe-task-reviewer-agent`. Fix: rename all 8 sites. **FIXED: all 8 sites (7 scaffolds + plan-schema agentType).**
- [x] **A4** 🔴 orchestrator-agent Step 0 required-reads point at 5 nonexistent files: `agents/haipipe-task-orchestrator-agent.md:79-82` names `ref/task-lifecycle-map.md` and `fn/plan.md, fn/build.md, fn/execute.md, fn/report.md`. Actual files: `ref/hierarchy.md` + SKILL.md steps; `fn/workflow-plan.md`, `fn/workflow-report.md`, `fn/run.md`. Fix: rewrite the required-reads list. **FIXED: Step 0 rewritten to real files; agent bumped 1.1.0.**
- [x] **A5** 🟡 `5_fit/haipipe-task-for-fit/SKILL.md:25` "See `haipipe-task-for-algo/SKILL.md`" resolves nowhere from that folder (actual: `../../2_nn/haipipe-task-for-algo/SKILL.md`). Same class: `fn/scaffold.md` in individual/fit/eval/display uses `../../haipipe-task/ref/...` which is off-by-one from the fn/ file's own depth (correct from skill root only). Fix: make paths resolve from the file that states them, or state "from skill root". **FIXED: fn/ref hub refs now ../../../haipipe-task (file-relative); for-fit algo cross-ref path fixed. Residual grep = 0.**

### B. 路由层失真 (haipipe-task orchestrator vs disk)

- [x] **B1** 🔴 `[M]` Wrong dispatch names: `haipipe-task/SKILL.md:211,267` say `Skill("haipipe-task-<type>")`; the skills are named `haipipe-task-for-<type>`. A dispatcher following this literally fails. Fix: add `-for-`. **FIXED.**
- [x] **B2** 🔴 `[M]` `endpoint` type missing from the routing machinery: Step 2 known-type list (`SKILL.md:193`) omits it, the keyword table (:232-249) has no endpoint row, the Step 3a script-inference cascade (:224) has no endpoint patterns, the dispatch table (:156-161) omits `/haipipe-task-for-endpoint`, and :254 says "ASK with all 7 options" (there are 8+). Yet the type table at :36 lists endpoint. Fix: add endpoint everywhere; recount. **FIXED: endpoint added to type list, dispatch table, keyword table, script-inference; '8 type options'.**
- [x] **B3** 🟡 `[J]` Orphan skills, nothing routes to them anywhere in the tree: `1_data/haipipe-task-for-raw` and `9_agent/haipipe-task-llm-engine` (the latter also has no CHANGELOG.md). Decide: wire them into the orchestrator's type table + keyword map, or archive them. (TODO.md already flags for-agent quality; llm-engine may be part of that rethink.) **FIXED: llm-engine got metadata block + CHANGELOG and is wired (orchestrator type table + for-agent). for-raw wired as a first-class type per JL 2026-07-04 ("关系到怎么从database里拿数据"): type table + keyword row + script-inference + dispatch table; its stale series list (for-training/for-inference) fixed too.**
- [x] **B4** 🟡 `[M]` `SKILL.md:124` "Two agents in task/agents/" and the list at :126-130 omit the orchestrator agent; the triad is three (README.md in agents/ has it right). Fix: say three, add the row. **FIXED: triad documented.**
- [x] **B5** 🟡 `[M]` `SKILL.md:141` claims reviewer runs "Claude drafts, Codex (xhigh, out-of-family) independently reviews". Reviewer agent v1.1.0 (2026-06-23) removed Codex; fresh-agent reasoning replaced it. Fix: update the sentence. **FIXED: fresh-agent independence wording.**
- [x] **B6** 🔴 `[M]` Step 3b routes scaffolds to verbs this skill no longer has: `:263` `Skill("haipipe-task", args="project ...")` (project scaffolding moved to /haipipe-project, as :51 and :73 themselves say) and `:265` `Skill("haipipe-task", args="block ...")` (no `block` verb in Commands). Fix: route project to `/haipipe-project`; either add a `block` verb (fn/task-group.md exists) or route to the right owner. **FIXED: project → /haipipe-project; group → new block verb.**
- [x] **B7** 🟡 `[J]` `fn/task-group.md` + `fn/scan-status.md` (+ `ref/scan_status/`) were received from the project layer on 2026-07-03 but are wired nowhere: no Commands verb, no dispatch-table row. Decide: expose as verbs (`/haipipe-task block ...`, `/haipipe-task scan-status`) or fold their content elsewhere. **FIXED: block + scan-status wired as verbs (Commands, dispatch table, Step 2 cascade).**
- [x] **B8** 🟡 `[M]` `SKILL.md:398` Risk Profile still describes "scope=project with new code stubs" though scope=project no longer exists here. Fix: drop the sentence. **FIXED: sentence dropped.**

### C. 内部矛盾

- [x] **C1** 🟡 `[J]` Group-letter contract is stated three incompatible ways: orchestrator `SKILL.md:39,228` "letters are project-specific, NOT type indicators (recommended A=data, B=fit, C=endpoint)"; specialists hard-mandate their own letters (`for-individual fn/scaffold.md:13` E, `for-fit:13` A, `for-eval:13` B, `for-display fn/scaffold.md:14` "Group letter must be **C**"); ProjB actually uses Z01_Display and A=cms/B=case/C=data/D=reg. Recommend: orchestrator's "project-specific" stance wins; specialists change mandates to defaults ("default letter X, honor the project's scheme"). Decide. **FIXED as recommended: 8 scaffolds now 'PROJECT-SPECIFIC, default X'; orchestrator note lists the defaults; 6 specialist descriptions made letter-neutral.**
- [x] **C2** 🔴 `[M-ish]` `4_individual/haipipe-individual/SKILL.md` folder-name contract contradicts itself and the shipped code: naming section (:81-98) + rationale + builder `fn/build_sample_individuals.py:235` all say child = `Subject-{id}` (dataset tag lives on the parent UserGroup folder), but :120, :196, :221 still command `Subject-{DatasetTag}-{id}` (the pre-rationale scheme). Spot-verified. Fix: the 3 stale lines to `Subject-{id}`. **FIXED: 3 lines now Subject-{id} with tag on parent.**
- [x] **C3** 🔴 `[M]` Template A-D mapping mismatch in 2_nn: `haipipe-nn/fn/fn-generate.md:257-261` describes A=External-library / B=HuggingFace / C=Custom-nn.Module / D=Multi-tuner, but `ref/overview.md` (the owner) defines A=TSForecast / B=S-Learner MLPredictor / C=TEFM-with-Tuner / D=TEFM-direct. Following fn-generate picks the wrong template. Spot-verified. Fix: rewrite fn-generate's 4 lines to match overview.md. **FIXED: A-D labels now match overview.md.**
- [x] **C4** 🟡 `[J]` Fictional hand-off: `haipipe-nn-tuner/SKILL.md:83-87` + `haipipe-nn-instance/SKILL.md:3,80-82` describe "Tuner emits best_config + ckpt; Instance consumes them", but the ref contract has Instance creating Tuners via registry and calling fit/save_model. Decide the real contract wording, then align both SKILL.md files. **FIXED: both SKILL.md files state the registry-driven contract (Instance creates Tuner, fit/save_model).**
- [x] **C5** 🔴 `[M]` `haipipe-task/CHANGELOG.md` ordering and numbering broken: 4.2.0 and 4.3.0 are dated 2026-07-03 (after 5.0.0, 2026-06-11) yet numbered lower AND sit at the bottom of a "newest first" file; frontmatter still `version: 5.0.0, last_updated: 2026-06-11`, so the July changes are invisible in the version. Fix: renumber to 5.1.0/5.2.0, move to top, bump frontmatter. **FIXED: renumbered 5.1.0/5.2.0, moved to top; new 5.3.0 entry; frontmatter 5.3.0/2026-07-04.**
- [x] **C6** 🟡 `[M]` `DESIGN.md` status markers stale: `:195-199` still headed "Target Architecture (v6.0.0, PLANNED)" with "once migration lands" though `:54-62` says the migration is COMPLETE (landed 2026-06-21). Current State tree (:65-116) is missing: orchestrator-agent (agents/ shows 2 of 3), haipipe-workflow/ (moved in 2026-07-03), for-raw, llm-engine, and the 5 fn files received in July. Fix: retitle PLANNED -> LANDED, refresh the tree. **FIXED: heading LANDED 2026-06-21; tree adds orchestrator-agent, haipipe-workflow/, for-raw, llm-engine, July fn/ref files; v5.3.0.**
- [x] **C7** 🟡 `[J]` `haipipe-individual` bucket head has no routing to its own 3 inference sub-skills (zero mentions of -inference / -inference-report / -inference-judge in its SKILL.md), unlike data/nn/end bucket heads. Sub-skills chain themselves via "sibling progression" tables instead. Decide: add a dispatch section to the bucket head, or bless the sibling-chain pattern as this bucket's design. **FIXED: Sub-skills section added (inference chain progression).**
- [x] **C8** 🟡 `[M]` Store glob matches nothing: `haipipe-nn-instance/SKILL.md:77` + `haipipe-nn-modelset/SKILL.md:77` use `5-ModelInstanceStore/ModelInstance-*/`; actual layout (per overview.md:597 and on-disk entries like `Demo-TECLM/`) has no `ModelInstance-` prefix. Fix: `{name}/{version}/`. **FIXED: {name}/{version} in both files.**
- [x] **C9** 🟡 `[J]` L1 loss ownership stated three inconsistent ways in 2_nn: `haipipe-nn-algo/SKILL.md:3,77` says L1 owns "forward pass, loss, metric"; its `ref/concepts.md:290` rule says algorithm classes do "no loss computation"; the TSCLM example in the same ref computes loss in forward. Decide the rule, align the three. **FIXED: rule aligned to the family norm (loss inside forward allowed; no optimizer/training loop) — matches SKILL.md + TSCLM example.**
- [x] **C10** 🟢 `[M]` Four task-for-* CHANGELOGs (algo, individual, fit, eval, display) say "Newest first" but list oldest-first. Fix: flip. **FIXED: 5 changelogs flipped newest-first.**

### D. 上层耦合 (task 原则上不该意识到 paper/probe 层)

- [x] **D1** 🟡 `[J]` `7_display/haipipe-task-for-display/SKILL.md:45,69` + `fn/scaffold.md:67-68` name paper-layer skills as "useful adjacent skills" (`/haipipe-display-figure`, `/haipipe-display-illustration-gemini`), and recommend the gemini FALLBACK renderer for diagram-style figures (family default is the diagram/illustration renderers). Recommend: drop the paper-skill mentions (output purpose "paper figures" stays, skill names go). Decide. **FIXED: paper-skill names removed from SKILL.md + fn/scaffold.md; output purpose kept.**
- [x] **D2** 🟡 `[J]` `haipipe-task/SKILL.md:439-441` mentions `/haipipe-paper digest`'s global-pref fan-out as the sync mechanism for PREFERENCES.md. Informational, but it is a paper-layer reference inside task. Decide: keep (mechanism note) or reword layer-neutrally ("synced by the toolkit's digest fan-out"). **FIXED: reworded layer-neutrally.**
- [x] **D3** 🟢 `[J]` `agents/haipipe-task-reviewer-agent.md:43-45` boundary lines name probe review functions; `agents/README.md:30-44` has a "Cross-layer dispatch" diagram showing probe-orchestrator calling task. Precedent: discovery's agents keep caller mentions in agent docs (tolerated as trigger hints). Recommend: leave as-is. Decide. **LEFT AS-IS per recommendation (discovery precedent: caller mentions in agent docs are trigger hints).**

### E. 其他 (from bucket audits, lower priority)

- [x] **E1** 🟡 `haipipe-nn/README.md:4` still describes the pre-split single-skill model ("all 4 layers in one skill") contradicting the dispatcher architecture. **FIXED: README opening describes the dispatcher model.**
- [x] **E2** 🟡 2_nn codebase paths (`code/hainn/{algo,tuner,instance}/`, `model_registry.py`) resolve in SPACE-HAI-Pipe's hainn, not this repo's (family-first: mlpredictor/tsforecast/bandit/tsfm). Possibly intentional (portable toolkit) but no doc says which workspace it assumes. Decide: add a one-line workspace note, or leave. **FIXED: workspace-dependence note added to overview.md.**
- [x] **E3** 🟡 `4_individual/haipipe-individual/SKILL.md:135,140` Build steps write wrapper paths contradicting its own FLAT-layout rules (:38, :67-71); :170 marks the builder script "planned" though it exists. **FIXED: steps 3-4 write FLAT layout; builder no longer 'planned'.**
- [x] **E4** 🟡 `5_fit/haipipe-task-for-fit/SKILL.md:87-116` "Lessons learned" duplicates LESSON.md content; LESSON.md never referenced. Single-source: point to LESSON.md. **FIXED: section replaced with LESSON.md pointer + 2 quick notes.**
- [ ] **E5** 🟡 `fn/scaffold.md` First-run-gate block (~20 lines) duplicated verbatim across the four audited task-for-* skills (likely all 7). Single-source candidate: `haipipe-task/ref/`. **DEFERRED (optional dedup pass).**
- [ ] **E6** 🟡 Duplication in 2_nn: test-notebook contract restated in overview.md + fn-test.md + each specialist's concepts.md; slot-variable block duplicated verbatim in fn-dashboard.md:208-217 and fn-review.md:15-24. **DEFERRED (optional dedup pass).**
- [x] **E7** 🟡 `[J]` `haipipe-task/fn/task-folder.md` still on disk, marked DEPRECATED at `SKILL.md:162`. Same class of old-symbol retention you had me purge in discovery. Decide: delete + drop the mention, or keep. **FIXED: file deleted (DESIGN.md Phase 4 had recorded its removal in 2026-06); SKILL.md + fn/task-group.md refs repointed.**
- [x] **E8** 🟢 Assorted cosmetics: "a individual" typo x3 (`haipipe-individual/SKILL.md:110,133,214`); for-fit metadata summary still says "model-run" (:9); eval/fit skeleton artifact-list drifts between SKILL.md and fn/scaffold.md; fn-generate.md:34 family list omits bandit; for-algo plan-sample output named smoke_test.json vs loss.json elsewhere. **FIXED: typos, for-fit summary, bandit in family list, loss.json naming, fn-generate models/ paths; artifact-list drift left (cosmetic).**

---

## Part 3: uncovered buckets

The three bucket auditors (1_data 10 skills, 3_end 15 skills, 8_stata + 9_agent + haipipe-workflow 4 skills) were stopped before returning; those buckets never got a per-skill deep audit (the kind that found C2 in haipipe-individual or A2 in 2_nn).

They DID receive every cross-cutting fix, applied tree-wide by grep: A1 schema paths (incl. for-stata's 4 samples), A3 reviewer names (all 7 scaffolds + plan-schema), A5 relative-path depth (incl. stata/endpoint/data/agent fn+ref files), C1 letter defaults (8 scaffolds + 6 descriptions), B3 wiring (for-raw, llm-engine + its missing CHANGELOG/metadata).

UPDATE 2026-07-04 (later the same day): JL asked to continue; three FRESH auditors were relaunched and all three returned. Their findings and outcomes are below (sections F/G/H). Coverage is now COMPLETE across all 44 skills.

### F. 3_end deep audit (15 skills) — 17 🔴 + 14 🟡, all fixed except noted

- [x] **F1** 🔴 haipipe-end README file map listed 11 nonexistent files (pre-split fiction). **FIXED: rewritten to ref/{0-overview,deploy-overview} + fn-design + specialist/endpointset pointers.**
- [x] **F2** 🔴 fn-design.md + 0-overview.md pointed at removed ref/1-meta.md…5-input2src.md (7+1 sites). **FIXED: repointed to the 5 specialists' ref/concepts.md.**
- [x] **F3** 🔴 ALL 4 deploy skills cited their own nonexistent ref/concepts.md (6-8 refs each) while the shared 460-line deploy-overview.md sat unreferenced and labeled "legacy". **FIXED: quadruplet points at ../haipipe-end/ref/deploy-overview.md; retitled as the shared ref.**
- [x] **F4** 🔴 5 files carried dangling ../haipipe-end-endpointset/ref/0-overview.md (endpointset has no ref/). **FIXED -> ../haipipe-end/ref/.**
- [x] **F5** 🔴 3 deploy skills used nonexistent self-names in headings/commands (haipipe-end-{sagemaker,databricks,mlflow}, 25 sites). **FIXED to the real -deploy- names.**
- [x] **F6** 🔴 for-endpoint's fn/scaffold.md + ref/workflow-plan-sample.yaml were STILL the retired inference-profiling scope (P-groups, ProfileArgs, skill: haipipe-task-for-inference). **FIXED: both rewritten to the 2.x endpoint-packaging scope (c_endpoint_nb.py / Endpoint_Pipeline / Setup->Package->Verify->Report).**
- [x] **F7** 🔴 src2input + input2src claimed TARGET-AWARE per-target wire formats with a --target flag, contradicting 0-overview + LESSON L16 ("one Fn set per endpoint, platform-agnostic"). **FIXED: L16 wins; flag retired, contract restated. REFINED per JL 7/5, then DECIDED by JL on the ASCII diagram: "方案 A: 一个平台一个 Fn. I choose this one." Contract FLIPPED to one wire-Fn per platform per use-case (src2input + input2src 2.0.0); LESSON L16 carries a SUPERSEDED banner; scope = wire I/O pair only, Meta/Trig/Post stay shared with TrigFn keeping the L14 unwrap; 0-overview + deploy-overview + deploy-databricks + for-endpoint scaffold aligned; --platform now selects the platform variant. Threads closed. FOLLOW-UP (unowned): whether an Endpoint_Set .tar.gz bundles both platform pairs or is packaged per-target — surface when the next packaging run happens.**
- [x] **F8** 🟡 `profile` verb (endpointset 1.1.0) unreachable through the umbrella dispatcher. **FIXED: added to the artifact axis (+ for-endpoint's pointer now /haipipe-end profile).**
- [x] **F9** 🟡 Endpoint_Set layout described 3 ways (manifest.yaml vs manifest.json, 3 dir-name variants). **FIXED: 0-overview canonical; endpointset + for-endpoint aligned/pointed.**
- [x] **F10** 🟡 misc: mlflow DEFERRED-vs-scaffolded self-contradiction; develop-databricks concepts off-by-one + dead docs pointer; retired for-inference refs in fn-3-profile + endpointset; for-endpoint C-series leftovers + changelog order; LESSON duplicate L14 (second -> L17); deploy-sagemaker back-link to develop pitfalls. **ALL FIXED.**
- [x] **F11** 🟡 RESOLVED per JL 7/5: serve_local.py hardcodes fixed (deploy-local 1.2.0: WORKSPACE_PATH env -> pyproject walk-up -> clear error; ENDPOINT_PATH env -> single-endpoint auto-pick -> candidate listing). Then JL ruled skill-internal code = reference only ("skill内部的code，还是不要运行，只是当作examples reference来用，到最后还是要写到task folder里的") -> serve_local.py repositioned as a copy-into-job template (deploy-local 1.3.0). FOLLOW-UP for JL: the 4_individual inference family also carries scripts/+src/ run in-place; apply the same reference-only rule there? Original note: serve_local.py hardcoded default /home/jluo41/WellDoc-SPACE (env-overridable; runtime code out of doc-review scope); ~350 lines of tolerated scaffolding duplication across the develop/deploy families; endpointset CHANGELOG history line (changelogs are history, not edited).

### G. 1_data deep audit (10 skills) — 9 🔴 + 14 🟡, all fixed except noted

- [x] **G1** 🔴 Fn-type ownership WRONG across the routing layer: dispatcher + source + record put HumanFn in Stage 1 and TriggerFn in Stage 2; every fn/ doc and shipped template puts HumanFn in Stage 2 (with RecordFn) and TriggerFn in Stage 3 (with CaseFn). **FIXED in dispatcher/source/record/case descriptions + builder-path notes. CONFIRMED by JL 7/5: "human fn should go to the Stage 2: Source to Record. it should be in the Record Stage."**
- [x] **G2** 🔴 haipipe-data-external + -remote existed on disk, claimed dispatcher parentage, but the dispatcher never routed to them. **FIXED: wired (specialists list, keyword map, aliases). CONFIRMED by JL 7/5: "yes, please do for them."**
- [x] **G3** 🔴 README file map fiction (ref/1-4.md + templates/N-stage/). **FIXED: rewritten.**
- [x] **G4** 🔴 fn-2-cook (5 sites) + 4 specialists' concepts.md pointed at retired unified-skill template paths. **FIXED -> specialist-local templates/config.yaml.**
- [x] **G5** 🔴 0-RawStore does not exist on disk; 28 occurrences across 12 files (raw, for-raw, remote, README, orchestrator keyword row). **FIXED -> 0-RawDataStore (verified: the only raw store in _WorkSpace/).**
- [x] **G6** 🔴 for-data ref/config-seed.yaml hub ref 4-up (dangling). **FIXED -> 3-up.**
- [x] **G7** 🟡 probe->experiment global-rename damage ("Experiments every store", "ref-style experiment"). **FIXED: natural English restored (plain 'probe' is not the probe layer).**
- [x] **G8** 🟡 misc: fn-2-cook CaseArgs schema aligned to the shipped case template (case_set_version at CaseArgs level, operation blocks); for-data scaffold Steps 4-5 naming aligned to run_<task_name>; notebook-templates a1-a4 (was aa-ad); raw concepts HumanSet -> SourceSet; aidata dead code/hainn/algo/ path -> workspace-neutral; fan-out 5-line summary; 0-rawdata alias -> raw Panel 0; remote store count 10. **ALL FIXED.**
- [x] **G9** 🟡 RESOLVED per JL 7/5 ("这些东西要general…不要出现具体的名字"): remote docs de-branded + aidata example moved to ref/ (see thread). Remaining deferred: haistep* path sweep; CGM-schema/partition dedup (same class as E5/E6). Original flag: employer-specific S3 bucket + SSO URL hardcoded in haipipe-data-remote ref/fn docs (your infra — intentional?); aidata SKILL.md is 58% project-specific worked example (recommend moving to ref/, deferred as a restructure); haistep* script paths are workspace-dependent (noted inline, full sweep deferred); CGM column schema + partition-mechanics duplication across 4-5 files (dedup deferred, same class as E5/E6).

### H. 8_stata + 9_agent + haipipe-workflow deep audit (4 skills) — 3 🔴 + 12 🟡, all fixed except noted

- [x] **H1** 🔴 rangejoin: audit-stata Step 4 + dialect A4 flat-banned ALL SSC while build-stata + checklist C1 + server env authorize rangejoin as the ONE exception. **FIXED: exception carved in both ban sites. JL 7/5: server has rangejoin ("服务器里当然有") but install detail too fine for skill docs ("太细节了") -> commentary stripped, bare exception kept (2.7.0).**
- [x] **H2** 🔴 build-stata forbade Resolve-StataExe everywhere, contradicting dialect A5(b) (standard for data/reg/case) and SKILL.md. **FIXED: aligned to A5. SUPERSEDED per JL 7/5 ("还是都允许Resolve-StataExe吧"): A5 now accepts hardcode OR resolver for ANY stage (2.7.0).**
- [x] **H3** 🔴 build-stata + scaffold still described the data stage as year-orchestrated; SKILL 2.3.0 topology says SELF-ORCHESTRATING (no year axis). **FIXED in both fn docs. JL 7/5 confirmed ("case是by year的，然后data是几年combine到一起的"), which matches the doc verbatim; nothing pending, thread closed.**
- [x] **H4** 🟡 RUNNAME grammars stale 3-way (dialect tail + plan-stata missed the 2.4.0 grammar fix). **FIXED: aligned to SKILL.md (case source dim; reg full cohort×pairing×source×window×family grid).**
- [x] **H5** 🟡 checklist F2/F3 pre-topology drift (banned config snapshots that its own L3/L8 require). **FIXED: scoped to runners; results/ keeps config_snapshot.do (+ manifest.json per B3).**
- [x] **H6** 🟡 misc stata: /cms-server-checklist invoked as a skill (absorbed 2.1.0) -> SERVER CHECK mode; retired haipipe-task-logging pointer removed; "see each specialist" (retired children) -> unified note; Gate-1 comment = local synth run; B1-C6 -> B1-F6.**ALL FIXED.**
- [x] **H7** 🟡 haipipe-task/ref/hierarchy.md carried a THIRD group-letter scheme (A=model-run B=eval C=display D=demo). **FIXED: project-specific rule + the specialist defaults (A fit/B eval/C display/D data/E individual/F agent/R raw/X_algo).**
- [x] **H8** 🟡 haipipe-workflow: description still 3-act lifecycle + retired "narrative" family; template.workflow.js pointed at skills/flow/. **ALL FIXED (4 acts; paper/application; skills/task/).**
- [x] **H9** 🟡 llm-engine: fn/usage.md told users the engine "doesn't exist yet" and to hand-copy PoC code (contradicting the skill's own CREATE-from-ref/engine flow); LLMCallStore leaf <transport> vs SKILL's <case_id>; committed .pyc pollution in ref/engine/; model ids claude-opus-4-7. **ALL FIXED (leaf = case_id; pycache removed; 4-8).** ⚠️ CORRECTION 2026-07-15: the `4-8` claim was PREMATURE — `ref/engine/router.py`, `ref/transport-reference.md`, and for-agent `ref/config-seed.yaml` + `fn/scaffold.md` still carried `claude-opus-4-7` / `claude-sonnet-4-6` until actually swept to `4-8` / `sonnet-5` today (verify-before-trusting).
- [x] **H10** 🟡 for-agent fn/scaffold Step 6 still denied the engine the same-day wiring gave it; CHANGELOG order. **FIXED.**
- [ ] **H11** 🟢 SKIPPED (noted): llm-engine nonstandard `trigger:` frontmatter key (works, nonblocking); Start-Job ban lives only in fn overlays (canonical contracts silent); dispatcher-do-template comment nuance.

---

## Part 4: proposed fix order (after your eyeball)

1. A1-A4 + B1-B2 + C3 + C5 (dead paths, wrong names, broken routing): one mechanical pass, no judgment.
2. B4-B6, B8, C2, C6, C8, C10 (stale text): second mechanical pass.
3. All `[J]` items (B3, B7, C1, C4, C7, C9, D1-D3, E2, E7): per your decisions, one commit per decision.
4. E-class dedup (E4-E6): optional cleanup pass, can defer.

Each fix lands with its skill's CHANGELOG entry; version bumps per skill.

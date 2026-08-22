# SKILLSET_REVIEW — task/3_end + task/haipipe-task core


> ⚠️ **ONE PATH IN THIS REVIEW NO LONGER RESOLVES** (`../_WorkSpace`). Banner
> added 260822 during a toolkit-wide sweep, without re-diagnosing.

Date: 2026-07-08 · Reviewer: haipipe-skill-diagnose (6 parallel auditors, all trust-gated) · Scope: 16 skills / ~88 files (3_end's 15 skills + LESSON.md; haipipe-task SKILL+fn/+ref/), every file read line by line.

STATUS: ✅ FIXED 2026-07-08 under JL's standing go ("yes, please go ahead and fix them").
All findings below applied; [J] rulings noted inline; 16 skills bumped with CHANGELOG entries.
LESSON.md deliberately left untouched (historical record).

---

## Part 1 — Root causes (先看这个)

| # | Class | Count | One line |
|---|---|---|---|
| ① | 🚚 搬家没改地址 | 9 | platform repos moved under `platforms/` but every doc cites bare root paths; dead `fn/project.md`; retired `/haipipe-project log`; `ProjA-*` examples ×3; unqualified `code-dev` in config-seed; orphan `<builder-dir>` token (my own 7-08 edit debt) |
| ② | 📄 路由层失真 | 5 | `run`/`audit` verbs dispatchable but undiscoverable; phantom Fn `DatabricksV1` ×2; src2input/input2src concepts never mention the platform-specific contract their own SKILLs mandate |
| ③ | ⚔️ 内部矛盾 | ~23 | **C1: "config naming is freestyle" vs run-sh-template hard-coding `configs/${RUN_NAME}.yaml`**; develop-databricks DEFERRED on a false premise (the repo EXISTS); README inference chain vs 0-overview; `Endpoint-*` prefix vs real store names; meta 6-key contract vs 4-key example; schema docs vs shipped template |
| ④ | 🪝 substrate/reality | 5 | deploy/develop-databricks claims unqualified vs Lesson 15 (REACH: no CLI/jobs/serving); tar.gz-vs-folder input contract divergence across the 4 deploy skills |

Two headline items:
- **C1 (🔴)** — three refs teach type-based/freestyle config names while the shipped `run-sh-template.sh:36` hard-codes `CONFIG="configs/${RUN_NAME}.yaml"` and every real task on disk pairs config==run. Anyone following the freestyle docs produces a run that can't find its config.
- **C2 (🔴)** — `haipipe-end-develop-databricks` is DEFERRED with reason "no platform repo exists"; `platforms/platform-databrick-training/` exists with a full repo (submit_job.py, setup_cluster.sh, notebooks/).

---

## Part 2 — Findings (grouped; fix outcomes appended as applied)

### haipipe-task core (SKILL + fn/)

- [x] **T1** 🔴 `[M]` `fn/task-group.md:18,22` → dead `fn/project.md`; scaffolding moved to `/haipipe-project`. Fix: `Skill("haipipe-project", ...)`.
- [x] **T2** 🟡 `[J]` `fn/task-group.md:28-37` stale letter table (`A=model-run`, no `R`); `:51-52` claims letter↔type "enforced" — SKILL.md:40 says letters are project-specific defaults. Fix: align to SKILL.md:40 scheme + add R, reword.
- [x] **T3** 🟡 `[M]` `fn/run.md:108` retired `/haipipe-project log task`. Fix: drop.
- [x] **T4** 🟡 `[J]` `fn/workflow-audit.md:119` example `type: external (inferred from A00_ group)` — demonstrates the exact move its own Step-4 NOTE forbids, and `external` isn't a task type. Fix: `type: data (inferred from SourceFn import)`.
- [x] **T5** 🟡 `[J]` SKILL.md: `run`/`audit` in Dispatch Table but absent from Commands + Step-2 cascade → unreachable. Fix: add both to Commands + cascade.
- [x] **T6** 🟡 `[M]` SKILL.md:354-371 `ProjA`/`ProjA-Timing-01-OptTime` examples. Fix: Project-REACH-ADHD forms.
- [x] **T7** 🟢 `[M]` SKILL.md:164 run-row reads-list wrong (hierarchy.md → invocation-modes.md). Fix: swap.
- [x] **T8** 🟢 `[J]` `fn/workflow-audit.md:94-98` cascade drift (`training`→`fit`; missing raw/individual/endpoint). Fix: point at SKILL Step 3a + fix label.

### haipipe-task ref/

- [x] **R1** 🔴 `[J]` **Config-naming contradiction.** `task-structure.md:256-273` ("config naming is freestyle", `B5_model_cgm_num_1m.yaml`↔`run_1m.sh`, "NOT configs/") + `hierarchy.md:118-126` type-named configs vs the RUNNAME spine (`hierarchy.md:147-154`, `authoring-conventions.md:20-28`) and the ENFORCING template `run-sh-template.sh:36`. Disk unanimous: config==run. Ruling (evidence: shipped template + all real tasks): **config filename == run filename**. Fix: rewrite the task-structure example + drop freestyle lines; relabel hierarchy's CONFIG column (type decides the YAML *skeleton*, not the *name*); collapse workflow-template `<CONFIG>`→`<RUN>`.
- [x] **R2** 🟡 `[M]` `hierarchy.md:89-91` "00 reserved" unreconciled with first-class `A00_rawstore_*` groups. Fix: bless the stage-0 group index.
- [x] **R3** 🟡 `[J]` `runtime-yaml-schema.md:96-102` documents a 4-level headline fallback; template implements 2. Fix: trim doc to shipped behavior.
- [x] **R4** 🟡 `[J]` `metrics-json-schema.md` never defines the `summary` object that run-sh-template + runtime-schema read. Fix: add optional `summary:` section.
- [x] **R5** 🟡 `[M]` `config-meta-template.yaml` missing `notebook:` and `skip_review:` keys that run-sh-template greps. Fix: add commented keys.
- [x] **R6** 🟢 `[M]` `intent-docstring-template.py:42` AIData token missing `AIData-` infix. Fix.
- [x] **R7** 🟢 `[J]` `databricks-execution.md` two illustrative values drift from live driver (`_param` default; volume path). Fix: sync.
- [x] **R8** 🟢 `[M]` Template-A footer globs omit `0-RawDataStore`. Fix: add.
- [x] **R9** 🟢 `[M]` D-series "data" vs D_demo "demo" ambiguity. Fix: one clarifying line in hierarchy.md.

### 3_end umbrella + task-for-endpoint

- [x] **E1** 🔴 `[M]` develop-databricks DEFERRED premise false — `platforms/platform-databrick-training/` EXISTS (submit_job.py, setup_cluster.sh, notebooks/). Affected: `haipipe-end/SKILL.md:68,219`, `develop-databricks/SKILL.md:3,21-24,118`, `ref/concepts.md:5,12` ("anticipated layout"). Ruling: keep DEFERRED (wiring genuinely absent) but fix the rationale to "repo exists; wiring + Lesson-15 reconciliation pending" and replace the imagined layout with the real one.
- [x] **E2** 🟡 `[J]` `haipipe-end/README.md:85-95` inference steps 3-5 say CaseFn/TfmFn/SplitFn; 0-overview + LESSON say PreFnPipeline (Record→Case→model_input). Fix: align README to PreFnPipeline.
- [x] **E3** 🟡 `[M]` `haipipe-task-for-endpoint/ref/config-seed.yaml:31` unqualified `code-dev` build path. Fix: current fn_develop path + legacy qualifier.
- [x] **E4** 🟡 `[J]` `haipipe-end/ref/0-overview.md:524` `config/test-haistep-*/6_test_endpoint.yaml` — repo-root config/ dead. Fix: task configs/ + platforms config note.
- [x] **E5** 🟡 `[J]` `haipipe-task-for-endpoint/ref/inference-perf-notes.md` self-describes as the retired task-side profiler source-of-truth, but endpointset/fn-3-profile.md still cites it. Ruling: KEEP; retitle header to serve `/haipipe-end profile`.
- [x] **E6** 🟢 `[J]` README bare `design` command unreachable; flow diagram lists 2 of 4 deploy targets. Fix: qualify + list 4.
- [x] **E7** 🟡 `[M]` `platforms/` prefix missing in `haipipe-end/ref/deploy-overview.md` (many lines), `ref/0-overview.md:245-246,300-302,525`, `README.md:171`. Fix: prefix + fix `../_WorkSpace` depth.

### 5 Fn-type skills (meta/trig/post/src2input/input2src)

- [x] **F1** 🟡 `[M]` meta concepts `<builder-dir>` used at :203 but never defined (my 7-08 edit missed meta). Fix: add the sibling definition block.
- [x] **F2** 🟡 `[J]` meta 6-key required contract (incl. inputSchema/outputSchema) vs 4-key File-Structure example. Fix: add the two keys to the example.
- [x] **F3** 🟡 `[J]` src2input concepts stale vs v2.0.0 platform-specific contract — shows ONLY the Databricks envelope as "the" output; default platform is sagemaker flat JSON. Fix: platform section with BOTH shapes.
- [x] **F4** 🟡 `[J]` input2src concepts still teaches the superseded one-Fn-unwraps-both-formats model; never mentions --platform. Fix: rewrite format section to one-Fn-per-platform.
- [x] **F5** 🟡 `[J]` input2src concepts:92 "NOT inside MetaDict" contradicts its own example + MUST DO #3. Fix: "top-level AND mirrored into MetaDict".
- [x] **F6** 🟡 `[M]` phantom `DatabricksV1` in src2input/SKILL:59 + input2src/SKILL:59. Fix: mark as placeholder-name.
- [x] **F7** 🟢 `[M]` `example_000_{uuid}` naming (src2input SKILL/concepts) — real dirs have no uuid. Fix: drop `_{uuid}`.
- [x] **F8** 🟢 `[M]` stale "as of 2026-04-25" impl lists (trig/post) + `AutoMetaFn` listed as if a file (meta). Fix: refresh dates/names, mark AutoMetaFn conceptual.
- [x] **F9** 🟢 `[J]` trig SKILL:103 builder glob missing cohort suffix; input2src "entry point" wording. Fix: both one-liners.

### endpointset + develop-*

- [x] **S1** 🟡 `[M]` endpointset SKILL:96,:134 `Endpoint-*`/`Endpoint-{name}` prefix — real store names have none. Fix: `{endpoint_name}`.
- [x] **S2** 🟡 `[M]` fn-0-dashboard:47 `external/ (required)` — absent from ALL real sets → every real endpoint flagged broken. Fix: conditional.
- [x] **S3** 🟡 `[J]` fn-1-package:171 restates the layout (with external/) against SKILL's own "do not restate" rule. Fix: pointer to 0-overview.
- [x] **S4** 🟡 `[M]` develop-sagemaker:229 `ProjA-Timing-01-OptTime` path; endpointset fn-3-profile:21 `ProjA-Click-01-ClickPred`. Fix: real/illustrative.
- [x] **S5** 🟡 `[J]` develop-databricks planned job-ladder unreconciled with Lesson 15 (REACH forbids jobs). Fix: scope job path to jobs-capable hosts + name the inline-exec fallback.
- [x] **S6** 🟢 `[M]` develop-sagemaker + develop-databricks concepts bare platform paths (→ E7 family); develop-local "future -develop-databricks"; endpointset "5 Fn-types" vs 6 subdirs. Fix: one-liners.

### deploy-* (4 skills)

- [x] **D1** 🟡 `[M]` `platforms/` prefix missing in all four SKILLs (runnable commands!) + serve_local.py docstring. Fix: prefix everywhere.
- [x] **D2** 🟡 `[M]` deploy-databricks:19 "consumes .tar.gz" vs its own step 1 + 3 siblings (folder). Fix: uniform contract — folder canonical, .tar.gz = Databricks wire form — stated in all four.
- [x] **D3** 🟡 `[J]` deploy-databricks CLI/Model-Serving claims unqualified for REACH. Fix: one host-conditional line (CDHAI serving-capable per databricks.yml; REACH browser-only per Lesson 15).
- [x] **D4** 🟢 `[M]` note `fn_endpoint/` = logical bundle, physically `code/`+`model/` (3 skills).

### Process debt

- [x] **P1** 🟢 `[M]` 7-08 builder-dir edits untracked in 5 Fn-type CHANGELOGs. Fix: this round's bumps record them.

---

## Part 3 — Coverage honesty

- LESSON.md files audited only for supersession banners (L16 banner present ✅) — historical paths inside them deliberately not flagged.
- `haipipe-end-meta/ref/examples/*.py` (3 builder scripts): existence verified, content not line-read.
- `scan_status/` scripts: path-correct but B01/CLM-specific — noted, not changed.
- Not audited: 2_nn, 4_individual…9_agent buckets; agents/; haipipe-workflow; inbound refs from other layers.
- Auditor trust: 6/6 panels spot-checked ≥3 claims each on disk; zero false claims this round (one auditor's payload-order "hint mismatch" was the auditor correctly overriding my brief).

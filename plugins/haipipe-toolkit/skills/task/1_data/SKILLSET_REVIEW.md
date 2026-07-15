# SKILLSET_REVIEW — task/1_data bucket

Date: 2026-07-08 · Reviewer: haipipe-skill-diagnose (6 parallel auditors, all trust-gated ≥3 spot-checks) · Scope: 10 skills, 65 files, every file read line by line.

STATUS: ✅ FIXED + RESOLVED 2026-07-08.
All 23 findings + P1 addressed; all 6 [J] threads ruled by blanket approval (JL: "ok, go ahead and fix all of them" — recommended option A applied to each) and removed from files.
Per-skill details: each skill's CHANGELOG (all 10 bumped).

---

## Part 1 — Root causes (先看这个)

| # | Class | Count | One line |
|---|-------|-------|----------|
| ① | 🚚 搬家没改地址 (migration debris) | 9 findings / ~35 locations | `scripts.haistep`→`haistepcli` rename never propagated; repo-root `config/`+`test/`+`tutorials/` died but 20+ doc lines still point there; ProjD name; `0-RawStore`; `code-dev/0-EXTERNAL` |
| ② | 📄 路由层失真 (routing drift) | 4 | dashboard fans out to 5 of 7 specialists; a CLI flag (`--version`) that doesn't exist; frontmatter lists 4 of 7 |
| ③ | ⚔️ 内部矛盾 (internal contradictions) | 8 | HumanFn double-owned; aidata store layout wrong vs disk; **yesterday's Pattern-2 update didn't propagate into task-for-raw's own fn/ref files**; CHANGELOG "newest first" violated ×4 |
| ④ | 🪝 substrate assumptions | 3 | raw = local-only (PHI volume cohorts invisible); remote = AWS-SSO framing on a gdrive default; store-map lists stores that don't exist |

Biggest single item: **A1** — every `python -m scripts.haistep.*` invocation AND every `haistep-*` console script in the bucket crashes (`ModuleNotFoundError`; verified by import test, not just inspection).
The rot originates in `code/` (pyproject + docstrings) and the bucket inherited it.

---

## Part 2 — Findings

### ① 🚚 Migration debris

- [x] **A1** 🔴 `[M]` Dead module path `scripts.haistep.*` (real: `scripts.haistepcli.*`; `import scripts.haistep` → ModuleNotFoundError, verified in .venv). Locations: `haipipe-data/SKILL.md:84`, `haipipe-task-for-data/SKILL.md:76-79,177`, `haipipe-task-for-data/fn/execute.md:65-78`, `haipipe-data-case/SKILL.md:100-102`, `haipipe-data-aidata/SKILL.md:103-104`. Same rot: `haistep-*` console scripts (defined in pyproject but pointing at the dead module, so they crash too) cited at `haipipe-data/fn/fn-4-design-kitchen.md:80-83` and all four `templates/config.yaml`. Fix: `s/scripts.haistep./scripts.haistepcli./` everywhere; replace `haistep-*` console-script examples with `python -m scripts.haistepcli.*` until pyproject is repaired. **Companion fix outside bucket**: `code/` pyproject:172-179 + haistepcli docstrings (flagged in Part 3). **FIXED: all module paths -> scripts.haistepcli.*; console-script examples -> python -m form; grep-zero verified. Companion pyproject/code-docstring fix tracked separately.**
- [x] **A2** 🔴 `[M]` Stale project name `examples/ProjD-EHR-1-Mimic/` (renamed `Project-EHR-Mimic`) at `haipipe-data/SKILL.md:89`. Fix: rename. **FIXED: renamed to Project-EHR-Mimic.**
- [x] **A3** 🔴 `[M]` Repo-root `config/` does not exist but ~15 doc lines treat it as live. Executable-command locations (🔴): `haipipe-data/fn/fn-4-design-kitchen.md:80-83`, `haipipe-data/fn/fn-3-design-chef.md:156-157`. Reference locations (🟡): `haipipe-data/README.md:168,177`, `haipipe-data/ref/0-overview.md:55,270-286` (whole WellDoc config-snapshot section), `haipipe-data/fn/fn-2-cook.md:87`, `haipipe-data/fn/fn-review.md:53,89-90,360-395` (reviewer path patterns `config/**/*.yaml` never match → review routing dead), `haipipe-data-source/ref/concepts.md:44,344`, `haipipe-data-record/ref/concepts.md:18`, `haipipe-data-case/ref/concepts.md:18`, `haipipe-data-aidata/ref/concepts.md:38`. Fix: point Recipe/config homes to task-folder `configs/` (real home; e.g. `01_source_fn_develop_<cohort>/configs/`) and `code/scripts/haistepconfig/` (framework reference templates only — never real project configs); fn-review patterns → `**/configs/**/*.yaml`; delete the 0-overview config snapshot. **FIXED: all locations repointed to task-folder configs/ (+ haistepconfig reference-only); 0-overview snapshot replaced; fn-review patterns -> **/configs/**/*.yaml; grep-zero on repo-root config/ forms.**
- [x] **A4** 🟡 `[M]` Dead test-script blocks `python test/test_haistep/...` (no `test/` dir anywhere) in `haipipe-data-source/templates/config.yaml:14`, `haipipe-data-record/templates/config.yaml:14`, `haipipe-data-case/templates/config.yaml:19-20`, `haipipe-data-aidata/templates/config.yaml:12-13`. Fix: drop the block (the `python -m scripts.haistepcli.*` line above it, once A1-fixed, suffices). **FIXED: dead test blocks removed from all 4 templates.**
- [x] **A5** 🟡 `[M]` `haipipe-data-raw/templates/datapoint-timeline.txt:97` emits old store name `0-RawStore` — the 1.1.0 CHANGELOG claims the rename was "bucket-wide" but the template was missed, so every generated timeline writes a wrong path. Fix: `0-RawDataStore`. **FIXED: 0-RawDataStore.**
- [x] **A6** 🟡 `[M]` `haipipe-data-external`: builder paths `code-dev/0-EXTERNAL/` presented as unqualified current fact in `fn/fn-2-cook.md:14,20,51,71`, `fn/fn-3-design-chef.md:33,73-74,130`, `ref/asset-catalog.md:24,27`, `ref/concepts.md:48,189,298`; AND the SKILL.md:138-140 caveat's trigger is wrong ("workspaces **without** `code-dev/`" — REACH has a gitignored `code-dev/` leftover, just no `0-EXTERNAL/`). Fix: reword caveat trigger to "without `code-dev/0-EXTERNAL/`", add one-line caveat at each fn/ref location, mark the 11-row catalog as WellDoc snapshot. **FIXED: caveat trigger corrected + WellDoc-snapshot caveats added to fn-2-cook, fn-3-design-chef, asset-catalog, concepts Recipe row.**
- [x] **A7** 🟢 `[M]` `haipipe-data-external/ref/concepts.md:154` claims `@{YYMMDD}R{N}` version tags "observed in the repo"; actual `env.sh:20` is `EXTERNAL_VERSION="@v1215"`. Fix: soften to "WellDoc convention, not enforced — discover via `echo $EXTERNAL_VERSION`". **FIXED: softened to WellDoc convention + $EXTERNAL_VERSION discovery.**
- [x] **A8** 🟡 `[M]` `haipipe-data/fn/fn-3-design-chef.md` body still uses unqualified `code-dev/1-PIPELINE/<N>-WorkSpace/` as THE builder dir despite the BUILDER-HOME header note added 2026-07-08 (`:55-59` Step-0 ls block, builder-location blocks `:172,283-285,459-461,627-631,645-647`, quick-ref `:779-784`). Fix: sweep body to the BUILDER HOME token / fn_develop-first form. **FIXED: body swept to fn_develop-first/BUILDER_HOME; haibuilder/ seed library added to header, Step 0, copy example, and quick-ref table.**
- [x] **A9** 🟢 `[M]` WellDoc illustrative names in external docs: SourceSets `20250829_SMSR3Full/@SMSParquetV250211`, `20250218_SMSAll` (`fn/fn-join.md:30`, `ref/concepts.md:121`) don't exist here (real: `reach-adhd`, `reach-pd2d`, `mimiciv-3.1`). Fix: neutral `<SourceSet>` placeholder or a REACH name. **FIXED: placeholders / REACH names.**

### ② 📄 Routing drift

- [x] **B1** 🟡 `[J]` `haipipe-data/SKILL.md:180-187`: cross-stage dashboard fans out to 5 specialists but the skill registers 7 (`:35-42`) — external/remote silently excluded. Thread mirrored below; in-file at `haipipe-data/SKILL.md` (fan-out section). **RESOLVED per JL 2026-07-08 ("ok, go ahead and fix all of them" -> option A): exclusion note written into the fan-out section; thread removed.**
- [x] **B2** 🟢 `[M]` `haipipe-data/SKILL.md:3` frontmatter description names only source/record/case/aidata, omitting raw/external/remote which it also dispatches. Fix: "…and raw/external/remote". **FIXED: description lists all 7 specialists.**
- [x] **B3** 🟡 `[M]` `haipipe-data-remote/ref/concepts.md:180` MUST-DO cites a `--version @{tag}` CLI flag that does not exist in `remote_sync.py` argparse (verified), and contradicts the skill's own path-based versioning (`ref/store-map.md:24`). Fix: express pinning via `--path .../@{version}/...`. **FIXED: path-based pinning form; flag claim removed.**
- [x] **B4** 🟢 `[M]` `haipipe-data-external/SKILL.md:66-82` dispatch-table column header "Umbrella's fn doc" — 6 of 7 rows are this skill's own `fn/` docs. Fix: rename column "fn doc to read". **FIXED: column renamed "fn doc to read".**

### ③ ⚔️ Internal contradictions

- [x] **C1** 🔴 `[M]` `haipipe-data-source/SKILL.md:16` "Owns all SourceFn / HumanFn work" — contradicts its own Stage Scope (`:117`), its own CHANGELOG 1.1.0 ("ownership corrected: Stage 1 owns SourceFn only"), and `haipipe-data-record/SKILL.md:16` which owns HumanFn. Evidence unanimous (code: HumanFn builders load from `code/haifn/fn_record/human/`). Fix: drop "/ HumanFn" from line 16. **FIXED: line 16 now SourceFn-only.**
- [x] **C2** 🟡 `[M]` `haipipe-data-aidata` documents AIData store layout as `4-AIDataStore/{aidata_name}/@{aidata_version}/` (`ref/concepts.md:64-73`, `templates/config.yaml:171`, `SKILL.md:131`); disk reality (verified all 4 sets) is `4-AIDataStore/{ParentSet}/@v{N}AIData-{aidata_name}/` (e.g. `MimicIV31_MimicAdmissionEntry/@v0AIData-MimicMortality/`). A reader loading the documented path finds nothing. Fix: correct layout block (mirrors CaseStore's `@v{N}CaseSet-{Trigger}` scheme, which the case doc got right). **FIXED: {ParentSetName}/@v{N}AIData-{aidata_name}/ in concepts + SKILL + template (+ remote store-map row).**
- [x] **C3** 🔴 `[J]` `haipipe-task-for-raw`: yesterday's v1.3.0 Pattern-2 update landed in SKILL.md only — the operative files still scaffold Pattern-1 for everything: `fn/scaffold.md:4,24-26,34-44,54,94-98` (stage2=local pandas; MUST NOT use Spark locally; MUST NOT create README — all wrong for PHI/A00), `ref/config-seed.yaml:25,52-54` (local sync fields), `ref/run-databricks-sh-template.sh:94` (prints "Sync … to local" — the exact move Pattern 2 forbids). A creator-agent following scaffold.md verbatim mis-scaffolds a PHI cohort. Thread mirrored below; in-file at `haipipe-task-for-raw/fn/scaffold.md` (top). **RESOLVED per JL 2026-07-08 (option A): scaffold.md gained Step 0 pattern gate + P2 deltas; config-seed P2 fields; run-template hint qualified; SKILL intro fixed; thread removed.**
- [x] **C4** 🟢 `[M]` `haipipe-data/fn/fn-2-cook.md:22` template path `templates/<N>-<stage>/config.yaml` contradicts its own Step-3/per-stage refs (`../../haipipe-data-<stage>/templates/config.yaml`). Fix: align line 22. **FIXED: aligned to specialist-local template path.**
- [x] **C5** 🟢 `[M]` CHANGELOG "newest first" ordering violated in `haipipe-data-record/CHANGELOG.md`, `haipipe-data-case/CHANGELOG.md`, `haipipe-data-aidata/CHANGELOG.md`, `haipipe-task-for-data/CHANGELOG.md` (1.0.0 listed above 1.1.0 etc.; top entries all correctly match frontmatter). Fix: reorder. **FIXED: all 4 CHANGELOGs newest-first.**
- [x] **C6** 🟢 `[M]` Two doc-vs-disk naming slips: (a) `haipipe-data-case/ref/concepts.md:29` + `templates/config.yaml` CaseSet path omits the `@i{i}n{n}` partition level that `SKILL.md:113` and all real stores have — note it as optional level; (b) `haipipe-data-aidata` canonical splits `test-id`/`test-od` vs shipped MimicMortality's `train/validation/test` — acknowledge `test` as valid. **FIXED: partition level noted in case concepts; split-name note in aidata concepts.**
- [x] **C7** 🟡 `[M]` `haipipe-data-external/ref/asset-catalog.md:81` (cohort key `patient_id, patient_id_encoded`) vs `ref/join-contract.md:125` ("cohort uses patient_id_encoded, not raw patient_id") — reader can't tell the right-side `_original` stem. Fix: state the external key stem explicitly in both. **FIXED: patient_id_encoded join key + patient_id_original stem stated in both files.**
- [x] **C8** 🟢 `[J]` `haipipe-data-aidata/ref/worked-example.md` — the "canonical good instance" is a WellDoc SMS RCT matching no repo asset. Thread mirrored below; in-file at `haipipe-data-aidata/ref/worked-example.md:1`. **RESOLVED per JL 2026-07-08 (option A): worked-example rebased to MIMIC-IV mortality, every claim disk-checkable; thread removed.**

### ④ 🪝 Substrate assumptions

- [x] **D1** 🟡 `[J]` `haipipe-data-raw` assumes raw cohorts are local (`_WorkSpace/0-RawDataStore/`); PHI cohorts (REACH) are volume-resident on Databricks and invisible to `load`/`dashboard` as documented. Thread mirrored below; in-file at `haipipe-data-raw/SKILL.md` (Stage Scope). **RESOLVED per JL 2026-07-08 (option A): volume-resident PHI paragraph added to Stage Scope; thread removed.**
- [x] **D2** 🟡 `[J]` `haipipe-data-remote` frames credentials/errors as AWS-S3-SSO universal (`SKILL.md` credentials + MUST-DO "surface AWS SSO error hints"), while the workspace default is rclone/GDrive (`REMOTE_ROOT='gdrive:…'`; the CLI's own example agrees). Thread mirrored below; in-file at `haipipe-data-remote/SKILL.md`. **RESOLVED per JL 2026-07-08 (option A): backend-conditional credential guidance (gdrive/rclone vs s3/SSO) in SKILL + concepts; thread removed.**
- [x] **D3** 🟡 `[J]` `haipipe-data-remote/ref/store-map.md:23,68` lists `7-AgentWorkspace` (+ `ExternalStore/@inference`) as concrete stores; neither exists on disk or in env.sh; `fn/fn-status.md:87` hardcodes "Probing 10 stores". Also on disk but in NO store list: `_WorkSpace/LearnStore/`, `_WorkSpace/0-REACH-RAW-Store/`. Thread mirrored below; in-file at `haipipe-data-remote/ref/store-map.md`. **RESOLVED per JL 2026-07-08 (option A): ⚙opt annotations + env-driven status probing + LearnStore/0-REACH-RAW-Store not-synced note; thread removed.**

### Process debt

- [x] **P1** 🟢 `[M]` The 2026-07-08 fn_develop sweep (Tools commits 13de010…18ec301) edited `haipipe-data`, `haipipe-data-{source,record,case,aidata,external}` docs without version bumps or CHANGELOG entries (only task-for-raw got 1.3.0). Fix: bump + entry for each in the same pass as this review's fixes (mandated by diagnose Phase 4 anyway). **FIXED: all 10 skills bumped (data 1.3.0, source 1.2.0, record 1.3.0, case 1.3.0, aidata 1.4.0, external 1.2.0, raw 1.2.0, remote 1.3.0, task-for-data 2.3.0, task-for-raw 1.4.0) with dated CHANGELOG entries incl. the earlier unversioned sweep.**

---

## [J] resolutions

All 6 threads were ruled by the blanket approval (JL 2026-07-08: "ok, go ahead and fix all of them"); the recommended option A was applied to each (B1 exclusion note; C3 Pattern-2 propagation; C8 MIMIC rebase; D1 volume note; D2 backend-conditional; D3 optional-store annotation).
Verbatim quote archived in each owning skill's CHANGELOG; all in-file threads removed.

---

## Part 3 — Coverage honesty (what was NOT audited)

- **`code/` companion rot (out of bucket)**: `pyproject.toml:172-179` console scripts and `code/scripts/haistepcli/*.py` docstrings carry the same dead `scripts.haistep.*` path — the true root of A1. Fixing the bucket docs does NOT repair `haistep-*` commands; that needs a `code/` (haipipe-code submodule) commit. Recommended but not done here.
- **`code-dev/` ghost**: exists on disk as gitignored leftovers (`1-PIPELINE/6-Endpoint-WorkSpace/` + pycache) after the retire commit 699bc7e. Workspace hygiene, not a doc finding; safe to `rm -rf` if desired.
- **Not audited**: agents/ files (different bucket), inbound references from OTHER buckets into 1_data (e.g. 3_end docs citing data skills), semantic correctness of YAML template keys against pipeline arg parsers (spot-checked `partition_number` only), `haipipe-data/fn/fn-0-dashboard.md`/`fn-1-load.md` procedure logic beyond path resolution, and the two `workflow-plan-sample.yaml`/`notebook-templates.md` files' content beyond path checks.
- **Auditor trust**: 6/6 panels spot-checked ≥3 claims on disk; one shared false inference (A1 "valid because pyproject lists it") caught and corrected by direct import test; every other checked claim held.

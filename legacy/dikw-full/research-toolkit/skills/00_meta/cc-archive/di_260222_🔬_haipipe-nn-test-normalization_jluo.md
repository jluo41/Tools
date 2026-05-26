Session 1: Normalize haipipe-nn Test Flow (2026-02-22 19:00)
=============================================================

Location: Tools/plugins/research/skills/haipipe-nn-{0-overview,1-algorithm,2-tuner,3-instance,4-modelset}/SKILL.md
Status: ✅ DONE — all skill files updated

Overview
--------

Full audit of all 89 test scripts across 19 model directories completed.
Canonical 4-layer test pattern confirmed. Design decisions reached this session:

1. Always use real AIData — no synthetic data at any layer
2. Unified 7-step structure for all 4 layers
3. Enhanced summary table: 4 columns (step | status | key_metric | artifact/sample)
4. Artifacts block after summary — clickable absolute paths + input/output samples

Issues below describe the specific changes needed to the skill files.

**Severity Legend**:
- [HIGH] - Core contract change, needed before anyone writes a new test
- [MEDIUM] - Improvement to existing pattern, worth doing
- [LOW] - Nice to have, minor clarification


Issue 1: Remove synthetic data from L1 test pattern
----------------------------------------------------

**Severity**: [HIGH]
**Location**: `Tools/plugins/research/skills/haipipe-nn-1-algorithm/SKILL.md` — Test Notebook section
**Problem**: Current L1 external algorithm pattern (XGBoost etc.) uses synthetic CSR data
(1000×200, 10% density). This tests the raw library API but NOT the real data pipeline.
Shape mismatches, dtype errors, vocab size bugs — none of these are caught by synthetic data.
**Recommendation**: Change Step 2 from "Create synthetic CSR" → "Load real AIData".
Change Step 4 from nothing → "Convert AIData → algorithm native format". This also
makes L1 the consistent place to prototype transform_fn before moving it to the Tuner.

> JL: Yes, in the future, no matter what, we will now use the fake data. I have to use real data to do it.

>> CC: DONE. Understood as: real data only, no synthetic/fake data at any layer.
Will update nn-1-algorithm SKILL.md to mandate real AIData at L1, replacing the
synthetic CSR step with Load AIData + Convert to native format.


Issue 2: Unified 7-step structure — rename L1 steps 5 and 6
-------------------------------------------------------------

**Severity**: [HIGH]
**Location**: `Tools/plugins/research/skills/haipipe-nn-1-algorithm/SKILL.md` — Test Notebook section
**Problem**: L1 custom nn.Module tests don't have "Fit" and "Infer" — they have
"Forward pass" and "Gradient flow". Current skill mixes naming inconsistently.
**Recommendation**: Lock in layer-appropriate labels within the unified 7 slots:

```
Unified slot    L1 label                L2–L4 label
────────────    ──────────────────────  ───────────
Step 5          Forward pass (loss)     Fit
Step 6          Gradient flow verify    Infer
```

Same column structure, layer-appropriate names.

> JL: Okay, this is good. Maybe let's unify them.

>> CC: DONE. Will lock in the 7-slot structure with layer-appropriate step labels.
L1 uses "Forward pass" / "Gradient flow"; L2–L4 use "Fit" / "Infer".
The column format is identical across all layers — only the label differs.


Issue 3: Artifact path — save to workspace not /tmp
----------------------------------------------------

**Severity**: [HIGH]
**Location**: All 5 SKILL.md files — Test Notebook / Summary section
**Problem**: All skills currently show only 2-column summary (test name, status).
The new contract adds key_metric and artifact/sample columns.
**Recommendation**: Replace the 2-column summary code snippet with the 4-column
template in each skill file. Include the artifact/sample column contract table:

```
step                         status    key_metric                     artifact / sample
───────────────────────────  ────────  ─────────────────────────────  ─────────────────────────
1. Load config               PASSED    tuner=XGBoostTuner, h=12       /abs/path/to/config.yaml
2. Load AIData               PASSED    train=2475, test=636           /abs/path/to/AIDataStore/
3. Create [object]           PASSED    class=Instance, MAIN           domain=nixtla
4. Prepare data              PASSED    n_rows=1200, n_features=512    {'uid':'S559','y':124.0}
5. Fit / Forward pass        PASSED    time=4.2s, [model metric]      is_fitted=True
6. Infer / Gradient flow     PASSED    splits=3, total_rows=600       {'uid':'S559','yhat':118}
7. Save/load roundtrip       PASSED    weight_delta=0.0, cfg=True     _WorkSpace/5-ModelInstanceStore/{name}/{version}/
```

> JL: /tmp/model/ → file tree. I think it should be sealed in the workspace. We have
> the workspace, right? Please try to save to the workspace. We have _WorkSpace/5-ModelInstanceStore

>> CC: DONE. Step 7 artifact path updated to use the proper workspace location:
`_WorkSpace/5-ModelInstanceStore/{modelinstance_name}/{modelinstance_version}/`
Tests should save to this path (already set by config via model_dir), not /tmp.
The roundtrip verification loads from and saves to the same workspace path.


Issue 4: Add artifacts block code pattern to all layer skills
-------------------------------------------------------------

**Severity**: [HIGH]
**Location**: All 5 SKILL.md files — Test Notebook / Summary section
**Problem**: No skill currently documents the artifacts block — the print statements
that give clickable absolute paths + input/output samples after the summary table.
**Recommendation**: Add canonical code snippet immediately after the summary table
template in every skill:

```python
# ─── Artifacts (click to open in VS Code) ───────────────────────────────
print(f"\n--- Artifacts ---")
print(f"  Config:        {config_path}")
print(f"  AIData:        {AIDATA_PATH}")
print(f"  Saved model:   {model_dir}")   # _WorkSpace/5-ModelInstanceStore/...
print(f"\n--- Input sample (Step 4: first transformed row) ---")
print(sample_input_row)   # captured at Step 4
print(f"\n--- Output sample (Step 6: first result row) ---")
print(sample_output_row)  # captured at Step 6
```

> JL: Yes, this is great. We should have a look at what we have. Otherwise, you know,
> it is not easy for us to understand.

>> CC: DONE. Will add this artifacts block to all 5 SKILL.md files after the summary
table template. Note: tmp_dir in Issue 3 updated to model_dir (workspace path) here too.


Issue 5: Collapse L4 canonical from 9 steps to 7 steps
-------------------------------------------------------

**Severity**: [MEDIUM]
**Location**: `Tools/plugins/research/skills/haipipe-nn-4-modelset/SKILL.md` — Test Notebook section
**Problem**: Current L4 canonical lists 9 separate steps (6=Package, 7=Save, 8=Load, 9=Infer-from-loaded).
Under the unified 7-step template, these collapse into Steps 6+7:
- Step 6: Infer (from fitted instance, before packaging)
- Step 7: Package + Save + Load roundtrip → Infer again → verify weight equality
**Recommendation**: Update the L4 test step list and any code snapshot to reflect the 7-step structure.

> JL: Yes, we can do it. It is also okay to have substeps. It can be feasible.

>> CC: DONE. Will collapse to 7 main steps with sub-steps under Step 7:
7a: Package into ModelInstance_Set
7b: Save to _WorkSpace/5-ModelInstanceStore/
7c: Load from disk + verify metadata + config
7d: Infer from loaded model + weight equality check
Sub-steps keep the detail without inflating the main step count.


Issue 6: Document 4 exception patterns in overview
---------------------------------------------------

**Severity**: [MEDIUM]
**Location**: `Tools/plugins/research/skills/haipipe-nn-0-overview/SKILL.md`
**Problem**: The 4 confirmed divergent patterns are not documented anywhere in the skills.
New contributors will expect canonical 7 steps and be confused by exceptions.

> JL: TEDifussion? Why the color one doesn't work? Maybe we can't do it.

>> CC: DEFERRED. TEDiffusion's divergence is architectural — it loads directly from
RecStore (raw parquet), not AIData, because it trains on continuous waveforms not
case-level tabular data. Conforming it to the 7-step pattern would require a significant
refactor of how it consumes data. Will document as intentional exception in overview.

> JL2: no, we should not do this, TEDifussion should also load from AIData_Set.

>> CC2: TODO. Revised — TEDiffusion must be updated to load from AIDataSet (not RecStore
directly). It is NOT an accepted exception. Will log as a code fix task alongside
BasePredictor L4. Do NOT document in overview as exception.

> JL: for CTEP, Yes, and for the submodules, we can keep the large steps to be the same,
> but at the same time, we can have the substep, right? Substep can be much flexible.

>> CC: DONE. CTEP is NOT an exception — its 10 steps map cleanly to the 7-slot structure
using sub-steps (8a/8b for freeze_roberta variants, recall@k in Step 6). Will remove
CTEP from the exceptions table and document it as "complex L1 using sub-steps."

> JL: Currently the band data is very bad examples chart and we will go back to update it later.

>> CC: DEFERRED. Bandit test (single file, 4 tests, synthetic data) remains a known gap.
Will document in overview as "pending rewrite" rather than "intentional design."

>> JL2: Could you make a to-do plan in the bandit model folder so we can do it later?

>> CC2: DONE. Created `code/hainn/bandit/test-modeling-bandit/TODO_normalize_tests.md`
with 6-step plan: canonical structure decision, real AIData loading, L2/L3/L4 test
file split, 7-step unified structure, inference()→infer() rename, BanditConfig + registry.

> JL: For this one, for the base prediction, definitely we should update it. It is not an exception.

>> CC: TODO. BasePredictor L4 must be updated to conform to canonical 7-step pattern
(add ModelInstance_Set wrapper, align step count). Will log as a separate fix task,
not document as an exception.


Issue 7: Step 5 key_metric — family-specific, with customizable sub-steps
--------------------------------------------------------------------------

**Severity**: [MEDIUM]
**Location**: All SKILL.md files — Step 5 description
**Problem**: "loss=0.034" only applies to HF/Transformer models. XGBoost exposes
best_iteration or val_auc (if eval_set used). TSForecast XGB exposes only elapsed time.
Rigidly requiring "loss" in key_metric will confuse tree-based model test authors.
**Recommendation**: Document Step 5 key_metric as "most meaningful training signal
the model exposes (family-specific)." Add examples per family:

```
Family              Step 5 key_metric example
──────────────────  ──────────────────────────────────────────
HF Transformer      time=4.2s, final_loss=0.034
XGBoost             time=2.1s, best_iter=127, val_auc=0.821
TSForecast XGB      time=1.8s, is_fitted=True
Nixtla Neural       time=12s, val_loss=0.041
```

> JL: That should be okay. I mean, in the per model, we can modify the infer content.
> I mean, we have a large step of infer, but within the infer, we can have something we want.
> So this maybe needs some like the customized test.

>> CC: DONE. Key principle captured: 7 main steps are fixed (the contract); sub-steps
within each step are model-specific (the customization zone). Will document in skills as:
"Step 5 key_metric is family-specific — show the most meaningful training signal your
model exposes. Sub-steps within Step 6 (Infer) may be customized per model family."


Changes Made
------------

**Files Modified:**
- `Tools/plugins/research/skills/haipipe-nn-0-overview/SKILL.md` — Summary table: 2-column → 4-column template + artifacts block + family-specific key_metric examples + L1 step label note + save path mandate
- `Tools/plugins/research/skills/haipipe-nn-1-algorithm/SKILL.md` — Test Notebook section rewritten: real AIData mandate, 7-step structure (Steps 4/5/6/7), Forward pass/Gradient flow labels for L1, 4-column summary + artifacts block
- `Tools/plugins/research/skills/haipipe-nn-2-tuner/SKILL.md` — Expected steps: Step 8 (YAML) collapsed into Step 7 sub-step, 4-column summary + artifacts block, reference path corrected to `test-modeling-ts_clm`
- `Tools/plugins/research/skills/haipipe-nn-3-instance/SKILL.md` — Step 6 relabeled to "Infer" (canonical), note added that `inference()` is non-canonical, 4-column summary + artifacts block, reference path corrected to `test-modeling-ts_clm`
- `Tools/plugins/research/skills/haipipe-nn-4-modelset/SKILL.md` — Steps 6-9 collapsed to Step 6 (Infer) + Step 7 with sub-steps (7a/7b/7c/7d), 4-column summary + artifacts block, reference path corrected to `test-modeling-ts_clm`, note added about old 9-step snapshot

**Files Created:**
- `code/hainn/bandit/test-modeling-bandit/TODO_normalize_tests.md` — 6-step TODO plan for Bandit test normalization
- `code/hainn/tediffusion/models/glucostaticonddiffusion/test-modeling-glucostaticonddiffusion/TODO_migrate_to_aidata.md` — 5-step plan for TEDiffusion AIDataSet migration (blocked on AIData builder)
- `code/hainn/mlpredictor/models/test-modeling-mlpredictor-basepredictor-xgboost/scripts/test_mlpredictor_basepredictor_xgboost_4_modelset.py` — Updated docstring to canonical 7-step notation (7a/7b/7c sub-steps), updated notebook title comment, updated Summary cell to 4-column format + artifacts block

**Config YAML bulk fix:**
- All `modelinstance_version: v0001-*` (bare, no `@`) in `config/` → `@v0001-*` (verified clean)

Unsolved Items
--------------

| # | Issue | Status | Notes |
|---|-------|--------|-------|
| 6a | TEDiffusion: migrate to AIDataSet | TODO | TODO file created. Blocked: needs AIData builder for waveform windows first |
| 6c | Bandit test rewrite | DEFERRED | Known gap — will revisit when Bandit is updated |
| 6d | BasePredictor L4 conformance | PARTIAL | Docstring + 4-col summary done. ModelInstance_Set wrapper still pending (larger refactor) |

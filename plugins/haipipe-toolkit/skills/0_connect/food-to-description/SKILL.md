---
name: food-to-description
description: Convert Shanghai meal strings to USDA nutrition using 4-stage pipeline
metadata:
  version: "1.0.0"
  last_updated: "2026-06-02"
  stages: 4
  pipeline: "decompose → retrieve → llm_rerank → aggregate"
  expected_improvement: "62.8% (stage 2) → 90-95% (with stage 3)"
---

# Skill: food-to-description

Convert Shanghai-style meal descriptions (free text, multi-line) into standardized USDA nutrition data (calories, carbs, protein, fat, fiber) using a 4-stage pipeline.

## When to Use

- You have a parquet file with `FoodName` column (Shanghai diet descriptions)
- You need to convert it to structured nutrition (USDA database)
- You want resumable execution + progress tracking
- You're willing to wait ~1-2 hours for full pipeline (includes LLM rerank)

Trigger phrases:
- "convert Shanghai food to nutrition"
- "resolve diet to USDA"
- "fill nutrition columns"

## Prerequisites

- Python 3.9+
- `pandas`, `pyarrow` (parquet support)
- Anthropic SDK: `pip install anthropic`
- USDA nutrition database: `usda_nutrition.sqlite` (13 MB, ~200k foods)
- ANTHROPIC_API_KEY environment variable set

## How It Works

### Stage 1: Decompose
Parse Shanghai multi-line food strings into (food_name, amount_g) tuples.

**Input:**
```
"Scallion grilled chops 125g\nLotus root soup 70g\nRice 200g"
```

**Output:**
```
[("scallion grilled chops", 125.0), ("lotus root soup", 70.0), ("rice", 200.0)]
```

**Status metric:** Number of unique food components extracted

### Stage 2: Retrieve
Find USDA matches via multi-tier full-text search (alias dict → prefix → FTS5).

**Input:** Food name from Stage 1 (e.g., "scallion grilled chops")

**Output:** Top-10 USDA candidates with nutrition per 100g

**Classification:**
- `GOOD`: Query tokens fully cover first segment + no extra noise (100% coverage)
- `OK`: Query tokens fully cover first segment + extra noise (100% coverage)
- `WEAK`: Partial token coverage (<100%)
- `MISS`: No candidates found

**v2 Results (current):**
- 62.8% GOOD/OK (rank-1 match on first try)
- 35.4% WEAK (top-10 contains truth, needs rerank)
- 1.7% MISS (even top-10 doesn't help)

### Stage 3: LLM Rerank
Use Claude (via Anthropic API) to pick best match from top-10 for WEAK/MISS cases.

**Input:** Food name + top-10 USDA candidates

**Prompt logic:**
```
"Given Shanghai food '{food}' and these 10 candidates, pick the best match by:
 1. Cuisine semantics (does it fit Shanghai?)
 2. Nutrition plausibility (reasonable for the food?)
 3. Availability (common in Shanghai?)
 Return: fdc_id, confidence (0-1), reasoning."
```

**Optimization:** Prompt caching to avoid resending top-10 candidates (cost: ~$0.03-0.05 per unique food)

**Expected improvement:** 35.4% WEAK → 90-95% match rate

### Stage 4: Aggregate
Sum nutrition across all components per meal.

**Input:** Stage 1 components + Stage 2/3 fdc_id mappings

**Processing:**
1. For each component: look up USDA nutrition (per 100g)
2. Scale by amount: nutrition × (amount_g / 100)
3. Sum across all components
4. Handle missing: fill with 0

**Output:** parquet with added columns: `Calories`, `Carbs`, `Protein`, `Fat`, `Fiber`

## Commands

### Run full pipeline (stages 1-4)
```bash
cd Tools/plugins/haipipe-toolkit/skills/0_connect/food-to-description

python pipeline.py <input.parquet> \
  --output <output.parquet> \
  --stages 1-4 \
  -v
```

### Run subset of stages
```bash
# Stage 2 only (retrieve)
python pipeline.py input.parquet --stages 2

# Stages 2-3 (retrieve + rerank)
python pipeline.py input.parquet --stages 2-3

# Stage 3 only (rerank weak cases found in stage 2)
python pipeline.py input.parquet --stages 3
```

### Resume from stage N
```bash
# If stage 2 failed, resume from stage 3
python pipeline.py input.parquet --from-stage 3
```

### Show status (without running)
```bash
python pipeline.py --status
```

### Test a single stage
```bash
# Test Stage 1: decompose
python stages/1_decompose.py

# Test Stage 2: retrieve
python stages/2_retrieve.py

# Test Stage 3: rerank (requires ANTHROPIC_API_KEY)
python stages/3_llm_rerank.py
```

## Status Tracking

Progress stored in `~/.food-description/status.json`:

```json
{
  "pipeline": "food-to-description",
  "created": "2026-06-02T10:30:00",
  "last_updated": "2026-06-02T12:15:00",
  "stages": {
    "stage_1": {"status": "done", "timestamp": "...", "count": 2018, "metric": "2,018 unique components"},
    "stage_2": {"status": "done", "timestamp": "...", "count": 2018, "metric": "62.8% rank-1 match"},
    "stage_3": {"status": "done", "timestamp": "...", "count": 1676, "metric": "1,676/1,676 reranked"},
    "stage_4": {"status": "done", "timestamp": "...", "count": 3470, "metric": "filled 3,470 meal rows"}
  }
}
```

Dashboard output:
```
🔄 Pipeline: food-to-description

📥 Stage 1 Decompose: ✅ done — 2,018 components
📊 Stage 2 Retrieve: ✅ done — 62.8% rank-1 match
🧠 Stage 3 LLM Rerank: ✅ done — 1,676/1,676 reranked (150 min)
📤 Stage 4 Aggregate: ✅ done — filled 3,470 meal rows
```

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### "usda_nutrition.sqlite not found"
The DB is at `/home/jluo41/WellDoc-SPACE/_WorkSpace/ExternalStore/@v1215/usda_fdc/usda_nutrition.sqlite`. If you move it, update `utils/constants.py`.

### Stage 3 (LLM) too slow
- Skip stage 3: `--stages 1-2` (will use stage 2 rank-1 for all foods)
- Run partial: `--stages 3` with smaller dataset to test

### Output parquet is missing nutrition columns
- Check stage 4 status: `--status`
- Verify input parquet has `FoodName` column with proper format

## Implementation Details

### Files
- `pipeline.py` — Orchestrator (main entry point)
- `stages/1_decompose.py` — Parse food strings
- `stages/2_retrieve.py` — USDA FTS5 match
- `stages/3_llm_rerank.py` — Claude rerank
- `stages/4_aggregate_writeback.py` — Sum nutrition + write
- `utils/constants.py` — Regex, stopwords, paths
- `utils/alias_dict.py` — 17 Shanghai→USDA manual mappings
- `utils/usda_db.py` — SQLite wrapper
- `utils/statusline.py` — Progress tracking

### Design Choices

1. **Multi-tier retrieval (Stage 2):** Alias dict + prefix + FTS5 ensures we find foods even if query is slightly off.
2. **Prompt caching (Stage 3):** Candidates list cached to reduce cost (~50% savings on repeated candidates).
3. **Resumable:** Statusline.json enables re-running only failed stages.
4. **Atomic writes:** Temp file → rename pattern prevents partial parquet writes.

## Performance

Rough timing (on 3,470 meals, 2,018 unique foods):
- Stage 1: <1 min
- Stage 2: ~5-10 min (FTS5 queries)
- Stage 3: ~2-3 hours (1,676 Claude API calls @ ~45 calls/min)
- Stage 4: <1 min

**Total:** ~2.5-3 hours for full pipeline with rerank.

## Cost Estimate (Stage 3 only)

~1,676 unique WEAK/MISS foods × $0.03-0.05/call = **$50-84 total**

Use `--stages 1-2` if you want to skip LLM cost (62.8% rank-1 without rerank).

## See Also

- `end-to-end-roadmap` skill: Document any E2E project using START/stages/END structure
- USDA FDC: https://fdc.nal.usda.gov/ (nutrition database)
- Shanghai diet example: `_WorkSpace/1-SourceStore/Shanghai/@ShanghaiV260419/Diet.parquet`

---

**Specialist tail:**

```
status:    ok
summary:   "food-to-description v1.0: decompose → retrieve (62.8%) → rerank (90-95%) → aggregate"
artifacts: [pipeline.py, stages/*, utils/*, status.json]
next:      Use end-to-end-roadmap skill to document progress for any E2E project
```

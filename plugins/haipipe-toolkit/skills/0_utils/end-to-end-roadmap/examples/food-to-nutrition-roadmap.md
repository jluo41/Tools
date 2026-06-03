---
name: food-to-description
description: Shanghai diet → USDA nutrition 4-stage pipeline
metadata:
  version: "1.0.0"
  start_date: "2026-06-02"
  last_updated: "2026-06-02"
  expected_completion: "2026-06-03"
---

# Roadmap: food-to-description

## START: Have Shanghai diet.parquet (3,470 meals)

Raw meal descriptions in free text format (multi-line FoodName column).
USDA nutrition DB available (usda_nutrition.sqlite, 13 MB, ~200k foods).

| 脚本 | 输入 | 输出 | 成功率 | 状态 |
|------|------|------|--------|------|
| 1_decompose.py | FoodName (free text) | (food, amount_g) tuples | 2,018 unique components | ✅ done |
| 2_retrieve.py | food_name string | Top-10 USDA candidates | 62.8% rank-1 match | ✅ done |
| 3_llm_rerank.py | food + top-10 | Best fdc_id (WEAK/MISS only) | ~90-95% expected | ⏳ running |
| 4_aggregate.py | fdc_id + amount | Nutrition per meal | 3,470 rows filled | ⬜ pending |

## END: Output parquet with filled nutrition columns

(Calories, Carbs, Protein, Fat, Fiber per meal)

Success criteria:
- ≥90% of foods matched to USDA
- No NaN in nutrition columns (fill with 0 if missing)
- Parquet shape: (3470, N+5) where N = original columns

---

## Progress Notes

**Stage 1 (Decompose):** ✅
- Parsed all 3,470 meals
- Extracted 2,018 unique food components
- 0 unparseable lines (all matched regex)

**Stage 2 (Retrieve):** ✅
- FTS5 multi-tier retrieval working
- 62.8% GOOD/OK (rank-1 hit)
- 35.4% WEAK (top-10 contains truth)
- 1.7% MISS (no candidates)

**Stage 3 (LLM Rerank):** ⏳
- Reranking ~1,676 WEAK/MISS foods via Claude
- ~45 calls/min, ETA ~45 min
- Using prompt caching (candidates cached per food)
- Cost: ~$50-84 total

**Stage 4 (Aggregate):** ⬜
- Will aggregate nutrition when stage 3 finishes
- Scale by amount (g), sum across components
- Fill NaN with 0

## Blockers / Risks

None known. Claude API rate limits: ~45 calls/min, but only 1,676 unique foods so should be fine (~45 min total).

## Next Steps

1. Monitor stage 3 progress (rerank)
2. Once stage 3 done: run stage 4 (aggregate + write)
3. Verify output: check nutrition ranges (calories, carbs, etc.)
4. Move to downstream tasks (modeling, analysis)

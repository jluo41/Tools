"""
Stage 2: Retrieve USDA matches for Shanghai food components via FTS5.

Input: Food name (string), e.g., "scallion grilled chops"
Output: Top-10 USDA candidates (sorted by relevance)

Uses multi-tier retrieval (alias → headword → FTS5) to find candidates
with 62.8% rank-1 hit rate (v2 results).

Note: This is retrieval only — Stage 3 (LLM Rerank) ranks candidates
for WEAK/MISS cases.
"""
from pathlib import Path
from typing import List, Dict, Optional
from .usda_db import USDADatabase


def retrieve(food: str, k: int = 10) -> List[Dict]:
    """Retrieve top-k USDA candidates for a food name.

    Args:
        food: Food name to match, e.g., "scallion grilled chops"
        k: Number of candidates to return (default 10)

    Returns:
        List of dicts with keys: fdc_id, description, data_type,
                                 calories, protein, fat, carbs, fiber, __alias (if from alias dict)
    """
    with USDADatabase() as db:
        return db.fts_topk(food, k=k)


def classify(food: str, top: Optional[Dict]) -> str:
    """Classify quality of the rank-1 match (GOOD/OK/WEAK/ALIAS/MISS).

    Quality is coverage of the query by the candidate's FULL description.
    The predecessor measured coverage against `description.split(",")[0]` only,
    which is structurally blind to USDA's inverted naming -- the query
    "chinese cabbage" scored 50% against "Cabbage, chinese (pak-choi), cooked"
    because "chinese" lives after the comma. That single line produced most of
    the 35% WEAK rate.

    Downstream contract: only GOOD/OK/ALIAS may be written into nutrition
    columns. WEAK/MISS must stay NULL -- a confidently wrong match is worse
    than a missing one.
    """
    if top is None:
        return "MISS"
    if top.get("__alias"):
        return "ALIAS"

    from .constants import STOPWORDS
    from .usda_db import _stem, _cook_state

    q_tok = USDADatabase.tokenize(food)
    if not q_tok:
        return "MISS"
    d_tok = USDADatabase.tokenize(top["description"])

    q_content = [t for t in q_tok if t not in STOPWORDS] or q_tok
    q_set, d_set = _stem(q_content), _stem(d_tok)
    cov = len(q_set & d_set) / len(q_set)

    # A cooking-state contradiction (query says porridge, match says raw) is a
    # 3x nutrition error even when every content token lines up. Never GOOD.
    q_state, d_state = _cook_state(q_tok), _cook_state(d_tok)
    state_conflict = q_state and d_state and q_state != d_state

    if cov >= 1.0 and not state_conflict:
        return "GOOD" if len(d_set - q_set) <= 3 else "OK"
    if cov >= 0.5:
        return "OK" if not state_conflict else "WEAK"
    return "WEAK"


if __name__ == "__main__":
    # Test: retrieve top-10 for a few sample foods
    test_foods = [
        "rice",
        "scallion grilled chops",
        "egg",
        "lotus root soup",
        "coarse grain",
    ]

    for food in test_foods:
        print(f"\n{'='*70}")
        print(f"Food: '{food}'")
        print('-' * 70)
        cands = retrieve(food, k=10)
        if not cands:
            print("  ✗ NO CANDIDATES")
            continue

        print(f"{'rank':<6} {'fdc_id':>8} {'type':<12} {'kcal':>6} {'carbs':>6} description")
        for rank, c in enumerate(cands, 1):
            kcal = f"{c['calories']:.0f}" if c['calories'] else "  -  "
            carbs = f"{c['carbs']:.1f}" if c['carbs'] else "  -  "
            dt = c["data_type"].replace("_food", "").replace("survey_fndds", "fndds")
            quality = classify(food, c) if rank == 1 else ""
            quality_marker = f"[{quality}]" if quality else ""
            print(f"{rank:<6} {c['fdc_id']:>8} {dt:<12} {kcal:>6} {carbs:>6} {c['description'][:50]} {quality_marker}")

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
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import USDADatabase


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
    """Classify quality of rank-1 match (GOOD/OK/WEAK/ALIAS/MISS).

    Args:
        food: Original query
        top: Top candidate (or None if MISS)

    Returns:
        Quality string: "GOOD", "OK", "WEAK", "ALIAS", or "MISS"
    """
    if top is None:
        return "MISS"
    if top.get("__alias"):
        return "ALIAS"

    with USDADatabase() as db:
        toks_raw = db.tokenize(food)
        from utils import STOPWORDS
        toks = [t for t in toks_raw if t not in STOPWORDS] or toks_raw

    qset = set(toks)
    first_seg = top["description"].split(",")[0]

    with USDADatabase() as db:
        st = set(db.tokenize(first_seg))

    # Handle plural/singular via crude stemming
    st_norm = st | {t[:-1] for t in st if t.endswith("s")}
    q_norm = qset | {t[:-1] for t in qset if t.endswith("s")}

    # Coverage: fraction of query tokens appearing in first segment
    cov = len(q_norm & st_norm) / len(qset) if qset else 0
    extra = len(st_norm - q_norm)  # extra tokens in first segment

    if cov >= 1.0 and extra == 0:
        return "GOOD"
    if cov >= 1.0:
        return "OK"
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

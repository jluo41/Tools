"""
Stage 3: LLM Rerank for WEAK/MISS cases.

Input: Food name + top-10 USDA candidates (from Stage 2)
       Only process foods classified as WEAK or MISS (skip GOOD/OK)
Output: fdc_id, confidence (0-1), reasoning

Uses Claude via Anthropic SDK with prompt caching to:
  1. Avoid re-sending identical top-10 candidate lists
  2. Improve from 62.8% (stage 2 only) → ~90-95% (with rerank)

Expected: ~1,676 unique WEAK/MISS calls at ~4-5 cents per call.
"""
import json
import os
from pathlib import Path
from typing import Dict, Optional, List
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import anthropic
except ImportError:
    anthropic = None


def build_candidates_text(candidates: List[Dict]) -> str:
    """Format top-10 candidates for Claude prompt (cached part).

    Args:
        candidates: List of dicts from Stage 2 (top-10)

    Returns:
        Formatted text for inclusion in prompt cache
    """
    lines = ["USDA Candidates (top 10):"]
    for i, c in enumerate(candidates, 1):
        lines.append(
            f"{i}. [fdc_id={c['fdc_id']}] {c['description']} "
            f"({c['data_type']}): "
            f"{c['calories']:.0f} kcal, "
            f"{c['carbs']:.1f}g carbs, "
            f"{c['protein']:.1f}g protein"
        )
    return "\n".join(lines)


def rerank_via_claude(
    food_name: str,
    candidates: List[Dict]
) -> Optional[Dict]:
    """Use Claude to pick best match from top-10 candidates.

    Args:
        food_name: Original query, e.g., "scallion grilled chops"
        candidates: Top-10 from Stage 2

    Returns:
        Dict with keys: fdc_id, confidence, reasoning
        or None if Claude fails or abstains.
    """
    if anthropic is None:
        raise ImportError(
            "anthropic SDK required for stage 3. "
            "Install: pip install anthropic"
        )

    if not candidates:
        return None

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    # Part A: System message (fixed, cached)
    system_message = (
        "You are a nutrition expert matching Shanghai diet descriptions to USDA foods. "
        "Given a food name and USDA candidates, pick the best match considering: "
        "1. Cuisine semantics (does it fit Shanghai cooking?), "
        "2. Nutrition plausibility (reasonable for the food type), "
        "3. Availability (is this food common in Shanghai?). "
        "Respond with JSON: {\"fdc_id\": int, \"confidence\": float 0-1, \"reasoning\": str}."
    )

    # Part B: Cached candidates list
    candidates_text = build_candidates_text(candidates)

    # Part C: User message (uncached, changes per query)
    user_message = (
        f"Food: '{food_name}'\n\n"
        f"Which USDA candidate (by fdc_id) is the best match? "
        f"Reply with JSON only, no markdown."
    )

    try:
        response = client.messages.create(
            model="claude-opus-4-8",  # Use latest Opus for best quality
            max_tokens=300,
            temperature=0,  # Deterministic
            system=[
                {"type": "text", "text": system_message},
                {
                    "type": "text",
                    "text": candidates_text,
                    "cache_control": {"type": "ephemeral"}  # Cache the candidates
                }
            ],
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        # Parse Claude's JSON response
        response_text = response.content[0].text.strip()
        # Remove markdown code fence if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()

        result = json.loads(response_text)
        return {
            "fdc_id": result.get("fdc_id"),
            "confidence": result.get("confidence", 0.0),
            "reasoning": result.get("reasoning", "")
        }

    except (json.JSONDecodeError, KeyError, anthropic.APIError) as e:
        print(f"  ⚠️  Claude rerank failed for '{food_name}': {e}")
        return None


if __name__ == "__main__":
    # Test: rerank a sample food against dummy candidates
    from stages.stage_2_retrieve import retrieve

    test_food = "scallion grilled chops"
    candidates = retrieve(test_food, k=10)

    print(f"Reranking: '{test_food}'")
    print(f"Candidates: {len(candidates)}")

    if candidates:
        result = rerank_via_claude(test_food, candidates)
        if result:
            print(f"\nRerank result:")
            print(f"  fdc_id: {result['fdc_id']}")
            print(f"  confidence: {result['confidence']:.2f}")
            print(f"  reasoning: {result['reasoning']}")
        else:
            print("\n⚠️  Rerank failed (API error or JSON parse failure)")

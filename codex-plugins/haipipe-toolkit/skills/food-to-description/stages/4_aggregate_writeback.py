"""
Stage 4: Aggregate nutrition data per meal and write back to parquet.

Input: DataFrame with food components, Stage 2 & 3 results (fdc_id + confidence)
Output: Same DataFrame with added columns: Calories, Carbs, Protein, Fat, Fiber

Sums nutrition across all components:
  - Scales by component amount (g)
  - Uses per-100g values from USDA
  - Fills NaN if component miss or nutrition missing
"""
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, List, Tuple
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import USDADatabase


def aggregate_nutrition(
    food_list: List[Tuple[str, Optional[float]]],
    food_to_fdc_id: Dict[str, Optional[int]]
) -> Dict[str, Optional[float]]:
    """Aggregate nutrition across all food components.

    Args:
        food_list: [(food_name, amount_g), ...] from Stage 1
        food_to_fdc_id: {food_name: fdc_id_or_none} from Stage 2/3

    Returns:
        Dict with keys: calories, carbs, protein, fat, fiber (or None if missing)
    """
    total = {"calories": 0.0, "carbs": 0.0, "protein": 0.0, "fat": 0.0, "fiber": 0.0}

    with USDADatabase() as db:
        for food, amt in food_list:
            if amt is None:
                continue  # Unknown amount → skip

            fdc_id = food_to_fdc_id.get(food)
            if fdc_id is None:
                continue  # MISS → skip

            nutrition = db.get_by_fdc_id(fdc_id)
            if nutrition is None:
                continue  # Not in DB → skip

            # Scale by amount (per 100g in DB → multiply by amt/100)
            scale = amt / 100.0
            for key in total:
                val = nutrition.get(key)
                if val is not None:
                    total[key] += val * scale

    # Return actual values or 0 (don't use None here; parquet is stricter)
    return {k: v if v > 0 else 0.0 for k, v in total.items()}


def write_nutrition_to_parquet(
    df: pd.DataFrame,
    food_series: pd.Series,  # FoodName column
    food_to_fdc_mapping: Dict[str, Optional[int]],  # From stages 2+3
    output_path: Path
) -> pd.DataFrame:
    """Add nutrition columns to DataFrame and write to parquet.

    Args:
        df: Input DataFrame (must have index)
        food_series: FoodName column (Series)
        food_to_fdc_mapping: {food -> fdc_id}
        output_path: Where to write the output parquet

    Returns:
        DataFrame with nutrition columns added
    """
    from stages import stage_1_decompose

    nutrition_cols = {
        "Calories": [],
        "Carbs": [],
        "Protein": [],
        "Fat": [],
        "Fiber": []
    }

    for food_name in food_series:
        components = stage_1_decompose.decompose(food_name)
        agg = aggregate_nutrition(components, food_to_fdc_mapping)
        nutrition_cols["Calories"].append(agg["calories"])
        nutrition_cols["Carbs"].append(agg["carbs"])
        nutrition_cols["Protein"].append(agg["protein"])
        nutrition_cols["Fat"].append(agg["fat"])
        nutrition_cols["Fiber"].append(agg["fiber"])

    # Add nutrition columns to DataFrame
    for col, values in nutrition_cols.items():
        df[col] = values

    # Write to parquet
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)

    return df


if __name__ == "__main__":
    # Test: aggregate nutrition for a sample meal
    from stages.stage_1_decompose import decompose

    sample_meal = "scallion grilled chops 125g\nlotus root soup 70g\nrice 200g"
    components = decompose(sample_meal)
    print(f"Sample meal: {sample_meal!r}")
    print(f"Components: {components}")

    # Dummy mapping (would come from stage 2+3)
    food_to_fdc = {
        "scallion grilled chops": None,
        "lotus root soup": None,
        "rice": 168917,  # rice white cooked
    }

    agg = aggregate_nutrition(components, food_to_fdc)
    print(f"\nAggregated nutrition:")
    for k, v in agg.items():
        print(f"  {k}: {v:.1f}")

"""
Stage 1: Decompose Shanghai-style multi-line food names into (food, amount_g) tuples.

Input: FoodName column from parquet (free text, multi-line).
Example:
  "Scallion grilled chops 125g\nLotus root soup 70g\nRice 200g"

Output: [(food_name_normalized, amount_in_g_approx), ...]
  [("scallion grilled chops", 125.0), ("lotus root soup", 70.0), ("rice", 200.0)]
"""
import re
from pathlib import Path
from typing import List, Tuple, Optional

# Import constants
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import LINE_RE


def decompose(text: str) -> List[Tuple[str, Optional[float]]]:
    """Parse Shanghai food string into (food, amount_g) tuples.

    Args:
        text: Multi-line food string, e.g., "scallion grilled chops 125 g\nrice 200 g"

    Returns:
        List of (food_name_normalized, amount_in_g_approx) tuples.
        If amount is unparseable, amount is None.
    """
    if text is None or not isinstance(text, str):
        return []

    out = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        m = LINE_RE.match(line)
        if not m:
            # Unparseable line → whole line as food, unknown amount
            out.append((line.lower(), None))
            continue

        food = m.group(1).strip().lower()
        amt = float(m.group(2))
        unit = m.group(3).lower()
        # ml → g rough conversion (1:1 for water-based foods; OK for this stage)
        out.append((food, amt))

    return out


if __name__ == "__main__":
    import pandas as pd
    import collections

    DIET = "/home/jluo41/WellDoc-SPACE/_WorkSpace/1-SourceStore/Shanghai/@ShanghaiV260419/Diet.parquet"
    df = pd.read_parquet(DIET)
    print(f"Total meal-entries: {len(df)}")
    print(f"Unique FoodName strings: {df['FoodName'].nunique()}")

    component_counter = collections.Counter()
    unparsed = 0
    for s in df["FoodName"]:
        for food, amt in decompose(s):
            component_counter[food] += 1
            if amt is None:
                unparsed += 1

    print(f"\nTotal food-lines extracted: {sum(component_counter.values())}")
    print(f"Unique food components: {len(component_counter)}")
    print(f"Unparsed lines (no g/ml): {unparsed}")
    print("\nTop 20 most-common components:")
    for food, n in component_counter.most_common(20):
        print(f"  {n:>4}× {food}")

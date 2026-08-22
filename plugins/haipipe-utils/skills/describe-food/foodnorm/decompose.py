"""
Stage 1: split a meal string into (food, amount_g) tuples.

This is now a THIN WRAPPER over `dialect.split_meal`, kept because six call
sites unpack its two-tuple shape. Two things changed under it on 260819, both
QE1 D10 gate A:

    it splits on ';' as well as newline    33,059 WellDoc rows used to come
                                           back as ONE fused component
    it returns the FOOD components only    a meal slot ('dinner') or a carb
                                           declaration ('Just Carbs') is no
                                           longer offered to a food bank

The second is a contract change, not just a fix: this function used to return
every component and leave filtering to the caller, and exactly one caller ever
did it. If you need the placeholders, and the meal record does, call
`split_meal` and read `.kind`.

Input: FoodName from any cohort's Diet frame, in any dialect.
    "Scallion grilled chops 125 g\nRice 200 g"   -> [("scallion grilled chops", 125.0), ("rice", 200.0)]
    "Multi Grain Cheerios; 2% Fat Milk"          -> [("multi grain cheerios", None), ("2% fat milk", None)]
    "Just Carbs; dinner"                         -> []            both components are non-food
"""
from typing import List, Optional, Tuple

from .dialect import split_meal, foods


def decompose(text: str) -> List[Tuple[str, Optional[float]]]:
    """Parse a meal string into (food, amount_g) tuples, food components only.

    Args:
        text: a meal string in any dialect, ';' or newline separated.

    Returns:
        [(food_name_normalized, amount_in_g_or_None), ...]. An amount of None
        means the log stated no portion; it is never invented. Non-food
        components are excluded -- use `split_meal` to see them.
    """
    return [(c.name, c.amount_g) for c in foods(split_meal(text))]


if __name__ == "__main__":
    import collections

    import pandas as pd

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
    print(f"Components with no stated portion: {unparsed}")
    print("\nTop 20 most-common components:")
    for food, n in component_counter.most_common(20):
        print(f"  {n:>4}x {food}")

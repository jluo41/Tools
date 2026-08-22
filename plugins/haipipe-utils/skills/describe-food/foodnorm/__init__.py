"""Food → nutrition normalization.

Resolves free-text food descriptions, in any cohort's dialect, to USDA nutrition.

THE DOOR, and what a pipeline caller should use — one call, batch, order-preserving:

    from foodnorm import normalize
    out = normalize(["fried rice; egg", "Cucumber 100g"])   # -> [{...}, {...}]

It is deliberately shaped like a third-party API call: the caller knows this
signature and nothing about the dialect layer, the bank, or the stage sequence,
so all of those can move or be rewritten without touching a pipeline file.
`client.py` picks the transport (local in process, or http) from
FOODNORM_TRANSPORT.

THE RICHER FORM, for a caller that already holds a DataFrame:

    from foodnorm import enrich_food_to_nutrition
    df = enrich_food_to_nutrition(df, food_col="FoodName")   # -> Calories, Carbs, ...

Five stages, the first optional:

    imagename   photo(s) -> "scrambled eggs; toast"   (engine: null | claude)
    decompose   "Egg 50 g\\nRice 25 g"  ->  [("egg", 50.0), ("rice", 25.0)]
    retrieve    each component  ->  USDA candidates, scored and ranked
    llm_rerank  optional; only for what stage 2 could not resolve
    aggregate   per-100g x grams/100, summed over components

Retrieval is two-phase: the SQL/FTS tiers only RECALL; `score_candidate()` scores
each candidate over its FULL description and re-sorts. Tier order is not rank
order -- the tiers are ordered by priority and use `ORDER BY length(description)`,
which systematically prefers the generic entry ("Cabbage, raw") over the specific
one ("Cabbage, chinese (pak-choi)").

CONTRACT: only GOOD / OK / ALIAS may be written into nutrition columns. WEAK and
MISS stay NULL. A confidently wrong food is worse than a missing one -- and the
`NutritionSource` / `NutritionConf` columns exist so downstream can tell which is
which. `PARTIAL` means some component of the meal did not resolve, so the totals
UNDERSTATE it.

This package ships INSIDE its skill, at
`Tools/plugins/haipipe-utils/skills/describe-food/foodnorm/`, beside the
SKILL.md that documents it, the CLI that drives it and the suite that tests it.
Nothing under `code/` names any module in here; a caller reaches it through
`normalize()` alone.
"""

from .client import normalize, NUTRIENTS, PROVENANCE, TRANSPORTS
from .enrich import enrich_food_to_nutrition
from .decompose import decompose
from .dialect import (split_meal, foods, Component,
                      FOOD, CARB_DECLARATION, SLOT_LABEL, UNNAMED)
from .retrieve import retrieve, classify
from .aggregate import aggregate_nutrition
from .usda_db import USDADatabase, score_candidate
from .imagename import (ImageRead, read_images, get_engine, ENGINES,
                        null_engine, claude_engine)
from .constants import USDA_DB, STOPWORDS, PLACEHOLDERS
from .alias_dict import ALIAS

# Quality labels whose nutrition may be trusted downstream.
TRUSTED = ("GOOD", "OK", "ALIAS")

__all__ = [
    "normalize",
    "NUTRIENTS",
    "PROVENANCE",
    "TRANSPORTS",
    "enrich_food_to_nutrition",
    "decompose",
    "split_meal",
    "foods",
    "Component",
    "FOOD",
    "CARB_DECLARATION",
    "SLOT_LABEL",
    "UNNAMED",
    "retrieve",
    "classify",
    "aggregate_nutrition",
    "ImageRead",
    "read_images",
    "get_engine",
    "ENGINES",
    "null_engine",
    "claude_engine",
    "USDADatabase",
    "score_candidate",
    "USDA_DB",
    "STOPWORDS",
    "PLACEHOLDERS",
    "ALIAS",
    "TRUSTED",
]

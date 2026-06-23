"""
17 curated Shanghai → USDA food mappings.
For foods where USDA lacks a canonical NFS entry, map to best representative.
"""

# Format: normalized query (lowercase, stripped) → preferred USDA description
# We'll resolve via LIKE prefix match during retrieval.
ALIAS = {
    "vegetable":                   "Vegetables, mixed, frozen",
    "vegetables":                  "Vegetables, mixed, frozen",
    "boiled vegetable":            "Vegetables, mixed, canned, drained",
    "coarse grain steamed bread":  "Bread, multi-grain",
    "soup":                        "Soup, NFS",
    "coarse grain":                "Sorghum grain",          # 粗粮 → closest USDA approx
    "soybean milk":                "Soymilk, original",
    "buckwheat bread":             "Buckwheat",              # use plain buckwheat as approx
    "buckwheat noodles":           "Noodles, soba, cooked",
    "steamed bread":               "Bread, white",
    "steamed bun":                 "Bao bun",
    "steamed pork bun":            "Bao bun",
    "wax gourd":                   "Squash, winter, acorn, raw",
    "snakehead fish":              "Fish, white, raw",
    "hairtail":                    "Fish, white, raw",
    "mandarin fish":               "Fish, sea bass, raw",
    "red date":                    "Dates, deglet noor",
    "yellow rice wine":            "Wine, table, red",
    "hangzhou cabbage":            "Cabbage, Chinese (pak-choi), raw",
}

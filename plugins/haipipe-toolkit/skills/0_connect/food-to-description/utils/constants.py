"""
Constants for food-to-description pipeline.
Regex patterns, stopwords, thresholds, DB path.
"""
import re
import pathlib

# Skill root directory
SKILL_ROOT = pathlib.Path(__file__).resolve().parents[2]

# USDA database location (reference, don't move)
USDA_DB = pathlib.Path("/home/jluo41/WellDoc-SPACE/_WorkSpace/ExternalStore/@v1215/usda_fdc/usda_nutrition.sqlite")

# Status tracking file location
STATUS_DIR = pathlib.Path.home() / ".food-description"
STATUS_FILE = STATUS_DIR / "status.json"

# Regex for parsing food lines: "<food> <number> <unit>"
# Units: g, ml, IU (case-insensitive)
LINE_RE = re.compile(r"^\s*(.+?)\s+(\d+(?:\.\d+)?)\s*(g|ml|IU|iu)\s*$")

# Stopwords that muddy retrieval signal
# (cooking methods, adjectives that don't help identify the food)
STOPWORDS = {
    "boiled", "steamed", "fried", "raw", "cooked", "minced", "sliced",
    "shredded", "scrambled", "baked", "grilled", "stir", "stewed",
    "roasted", "braised", "poached", "cured", "dried", "fresh", "whole",
    "broiled", "sauteed"
}

# FTS5 retrieval scoring thresholds
MIN_COVERAGE = 0.8  # token coverage needed for GOOD classification
MIN_FTS_CANDIDATES = 3  # if FTS5 returns fewer, mark as MISS

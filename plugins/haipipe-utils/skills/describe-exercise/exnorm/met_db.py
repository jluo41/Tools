"""
The bank: the 2024 PA Compendium, 1,111 activities, held in memory.

A CSV AND NOT A DATABASE, on purpose. describe-food needs SQLite and FTS5
because USDA FDC is 128 MB and hundreds of thousands of descriptions. This bank
is 80 KB. Loading it whole costs ~4 ms, the lookup is a dict, and the fuzzy tier
scans all 1,111 rows in under a millisecond. A schema here would buy nothing and
cost a build step.
"""
import csv
import functools
import re
from typing import Dict, List, Optional

from .constants import DEFAULT_BANK

_TOKEN_RE = re.compile(r"[a-z]+")
# Words that appear in hundreds of descriptions and separate nothing.
_STOP = {"general", "moderate", "light", "vigorous", "effort", "the", "and",
         "or", "with", "for", "to", "in", "on", "of", "a", "mph", "kmh",
         "level", "firm", "surface", "taylor", "code", "e", "g"}


def _tokens(s: str) -> set:
    return {t for t in _TOKEN_RE.findall(s.lower()) if t not in _STOP and len(t) > 2}


@functools.lru_cache(maxsize=4)
def load(path=None) -> List[Dict]:
    """Every compendium row, tokenized once. Cached: a service resolves
    thousands of activities against one load."""
    p = str(path or DEFAULT_BANK)
    try:
        with open(p, newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
    except FileNotFoundError:
        raise FileNotFoundError(
            f"PA Compendium not found at {p}. Set EXNORM_DB, or see "
            "_WorkSpace/ExternalStore/pa_compendium/PROVENANCE.md for how to "
            "fetch it."
        )
    for r in rows:
        r["met_value"] = float(r["met_value"])
        # DESCRIPTION and HEADING are tokenized SEPARATELY and never merged.
        # Merged, the query 'sports' scored 1.0 against 'Judo' -- a perfect
        # match, on the strength of Judo living under the Sports heading. A
        # category word is not evidence for any one member of the category.
        r["__desc"] = _tokens(r["activity_description"])
        r["__head"] = _tokens(r["major_heading"])
        # This compendium names the activity FIRST: 'Basketball, general',
        # 'Zumba, group class', 'Walking, 2.8 to 3.4 mph'. So the leading token
        # is the activity's identity and the rest is its qualifier. That is the
        # cheapest available discriminator and it is the one that separates
        # 'sports' -> 'Rodeo SPORTS, general' (not anchored, a coincidence)
        # from 'basketball' -> 'BASKETBALL, general' (anchored, the entry).
        lead = _TOKEN_RE.findall(r["activity_description"].lower())
        r["__lead"] = lead[0] if lead else ""
    return rows


@functools.lru_cache(maxsize=4)
def _by_code(path=None) -> Dict[str, Dict]:
    return {r["activity_code"]: r for r in load(path)}


def by_code(code: str, path=None) -> Optional[Dict]:
    """Look up ONE compendium activity_code. Callers must not pass a cohort's
    ExerciseType here -- dialect.reject_code_join exists for that."""
    return _by_code(path).get(str(code))


def search(name: str, k: int = 5, path=None) -> List[Dict]:
    """Top-k compendium rows for a free-text activity name, by token overlap.

    Score is overlap normalized by the QUERY's token count, not the candidate's.
    Normalizing by the candidate would make long descriptions unreachable and
    reward one-word entries -- the same asymmetry that made describe-food's
    predecessor score 'chinese cabbage' at 50% against the row that had it.

    Results carry `__anchored`: whether the description LEADS with a query
    token. A one-token query scores 1.0 against anything containing that token,
    so score alone cannot tell 'basketball' -> 'Basketball, general' from
    'sports' -> 'Rodeo sports, general'. Anchoring can, and retrieve.py refuses
    to trust an unanchored hit.
    """
    q = _tokens(name)
    if not q:
        return []
    out = []
    for r in load(path):
        hit = q & r["__desc"]
        if not hit:
            continue                      # heading-only agreement is not a match
        score = len(hit) / len(q)
        if q & r["__head"] and len(hit) == len(q & (r["__desc"] | r["__head"])):
            pass                          # heading agrees too; no bonus, just no penalty
        # A tie among equally-matching rows goes to the shorter description,
        # which is the more general one in this compendium's own style.
        anchored = r["__lead"] in q
        out.append((anchored, score, -len(r["activity_description"]), r))
    out.sort(key=lambda t: (t[0], t[1], t[2]), reverse=True)
    return [dict(r, __score=sc, __anchored=a) for a, sc, _, r in out[:k]]

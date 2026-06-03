"""
USDA database utilities.
SQLite queries for nutrition retrieval and FTS5 full-text search.
"""
import sqlite3
import re
from .constants import USDA_DB, STOPWORDS
from .alias_dict import ALIAS


class USDADatabase:
    """Wrapper for USDA nutrition SQLite database."""

    def __init__(self, db_path=None):
        self.db_path = db_path or USDA_DB
        self.con = sqlite3.connect(str(self.db_path))
        self.con.row_factory = sqlite3.Row

    def close(self):
        self.con.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    @staticmethod
    def tokenize(query: str):
        """Extract tokens from query string (lowercase, alphanumeric only)."""
        return re.findall(r"[a-zA-Z]+", query.lower())

    def fts_topk(self, food: str, k=10):
        """Multi-tier retrieval: alias → headword → prefix → FTS5.

        Returns list of dicts (top-k results, highest-confidence first).
        Each dict includes: fdc_id, description, data_type, calories, protein, fat, carbs, fiber, __alias (if from alias dict).
        """
        toks_raw = self.tokenize(food)
        toks = [t for t in toks_raw if t not in STOPWORDS] or toks_raw
        if not toks:
            return []

        seen = set()
        results = []

        # Tier 0: Alias dict lookup (manually curated shortcut)
        food_norm = food.strip().lower()
        if food_norm in ALIAS:
            alias_target = ALIAS[food_norm]
            rows = list(self.con.execute(
                "SELECT food.fdc_id, food.description, food.data_type, food.calories, "
                "       food.protein, food.fat, food.carbs, food.fiber "
                "FROM food WHERE description LIKE ? AND calories IS NOT NULL "
                "ORDER BY length(description) LIMIT 3",
                (alias_target + "%",)
            ).fetchall())
            for r in rows:
                d = dict(r)
                d["__alias"] = True
                if d["fdc_id"] not in seen:
                    seen.add(d["fdc_id"])
                    results.append(d)

        def add(rows):
            """Helper: add rows not yet seen."""
            for r in rows:
                if r["fdc_id"] in seen:
                    continue
                seen.add(r["fdc_id"])
                results.append(r)

        cols = ("food.fdc_id, food.description, food.data_type, "
                "food.calories, food.protein, food.fat, food.carbs, food.fiber")
        whole = " ".join(toks)

        # Tier 1: Description headword IS the query ('rice,%' or 'chinese cabbage,%')
        add(list(self.con.execute(
            f"SELECT {cols} FROM food WHERE lower(description) LIKE ? AND food.calories IS NOT NULL "
            f"ORDER BY length(description) LIMIT 10",
            (whole + ",%",)
        ).fetchall()))

        # Tier 2: Description = query exactly
        add(list(self.con.execute(
            f"SELECT {cols} FROM food WHERE lower(description) = ? AND food.calories IS NOT NULL LIMIT 5",
            (whole,)
        ).fetchall()))

        # Tier 3: Description starts with query as phrase
        add(list(self.con.execute(
            f"SELECT {cols} FROM food WHERE lower(description) LIKE ? AND food.calories IS NOT NULL "
            f"ORDER BY length(description) LIMIT 10",
            (whole + " %",)
        ).fetchall()))

        # Tier 4-5: Per-token headword/prefix (if multi-token)
        if len(toks) >= 2:
            for t in toks:
                add(list(self.con.execute(
                    f"SELECT {cols} FROM food WHERE lower(description) LIKE ? AND food.calories IS NOT NULL "
                    f"ORDER BY length(description) LIMIT 5",
                    (t + ",%",)
                ).fetchall()))
            for t in toks:
                add(list(self.con.execute(
                    f"SELECT {cols} FROM food WHERE lower(description) LIKE ? AND food.calories IS NOT NULL "
                    f"ORDER BY length(description) LIMIT 3",
                    (t + "%",)
                ).fetchall()))

        # Tier 6: FTS5 AND (all tokens must appear)
        add(list(self.con.execute(
            f"SELECT {cols} FROM food_fts JOIN food ON food.rowid = food_fts.rowid "
            f"WHERE food_fts MATCH ? AND food.calories IS NOT NULL ORDER BY rank LIMIT 10",
            (" ".join(toks),)
        ).fetchall()))

        # Tier 7: FTS5 OR (any token, fallback)
        if len(results) < 3:
            or_query = " OR ".join(toks)
            add(list(self.con.execute(
                f"SELECT {cols} FROM food_fts JOIN food ON food.rowid = food_fts.rowid "
                f"WHERE food_fts MATCH ? AND food.calories IS NOT NULL ORDER BY rank LIMIT 15",
                (or_query,)
            ).fetchall()))

        return results[:k]

    def get_by_fdc_id(self, fdc_id: int):
        """Fetch single food by fdc_id."""
        row = self.con.execute(
            "SELECT fdc_id, description, data_type, calories, protein, fat, carbs, fiber "
            "FROM food WHERE fdc_id = ?",
            (fdc_id,)
        ).fetchone()
        return dict(row) if row else None

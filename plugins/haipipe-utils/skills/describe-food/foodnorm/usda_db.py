"""
USDA database utilities.
SQLite queries for nutrition retrieval and FTS5 full-text search.

Retrieval is two-phase:
  RECALL  — the tiered SQL/FTS queries below generate a candidate pool.
  RANK    — score_candidate() scores every candidate over its FULL description
            and the pool is re-sorted. Tier order is NOT rank order.

The tiers alone cannot rank: they fire in priority order and use
`ORDER BY length(description)`, which systematically prefers the generic
entry ("Cabbage, raw") over the specific one ("Cabbage, chinese (pak-choi)").
Scoring exists to undo that.
"""
import sqlite3
import re
from .constants import USDA_DB, STOPWORDS

# How many rows the two FTS tiers may RECALL. It is a recall cap, not a quality
# decision: the tiers' own docstring says they only recall and that
# `score_candidate` re-sorts everything below, so a bigger cap costs time and
# never costs accuracy.
#
# It STAYS at 20, and the reason is measured, not conservative.
#
# 20 is corpus-size dependent in a way nobody intended: FTS5 `ORDER BY rank` is
# BM25, which uses corpus statistics, so the same query against a 101,215-row
# index and a 13,602-row index returns a different top 20. On the smaller
# `foodbank` corpus `Soup, chicken vegetable with potato and cheese` fell out of
# the window and one Shanghai meal stopped resolving, though the row was present
# with identical values in both. Raising the cap fixes that.
#
# It also COSTS, and the two effects pull opposite ways. Swept 260821 on 300
# gold rows per cell, against the foodbank corpus:
#
#     cap    single_item MAE      r        item_list MAE      r
#      20             10.81   0.811                14.0   0.694
#      40             11.24   0.801               13.91   0.696
#      80             11.30   0.800               13.96   0.698
#     200             11.35   0.798               14.08   0.696
#
# A short single-item query gets WORSE with more candidates, because
# `score_candidate` gets more chances to prefer a wrong food that scores well; a
# multi-item meal barely improves. On the frozen benchmark, raising it took
# `single_item` row r from 0.822 to 0.815, under its own do-not-regress line of
# 0.82, while gaining `item_list` r from 0.643 to 0.662.
#
# So NO value of this cap clears both cells at once, which means the remaining
# gap is not a parameter. It is that `score_candidate` should weigh a one-word
# query differently from a six-word one, and that is a modelling change.
FTS_RECALL = 20
from .alias_dict import ALIAS

# Cooking state carries most of the nutrition signal in USDA descriptions:
# "Millet, raw" is 72g carbs/100g; "Millet, cooked" is 23g. A query whose
# state is dropped will silently match the wrong one and be ~3x off.
COOKED_WORDS = {
    "cooked", "boiled", "steamed", "fried", "braised", "stewed", "roasted",
    "grilled", "baked", "broiled", "sauteed", "poached", "stir",
}
RAW_WORDS = {"raw", "uncooked", "dry", "dried", "fresh"}

# Dish FORMS are not cooking states -- "rice" and "rice soup" are different
# foods with different nutrition (28g vs 7g carbs/100g). Treating "soup" as a
# cooking state makes plain rice match "Soup, rice" and understate carbs 4x.
# They are excluded from COOKED_WORDS on purpose; the headword term below is
# what keeps a bare ingredient from matching a dish built out of it.
DISH_FORMS = {"soup", "porridge", "congee", "salad", "sandwich", "stew",
              "casserole", "pizza", "juice", "smoothie", "chips"}

# Frying adds batter and oil, so its carbs/fat belong to the coating, not the
# food: "Fish, cod, fried" is 11.7g carbs where plain cod is 0.
ADDED_FAT_WORDS = {"fried", "breaded", "battered", "crispy", "tempura",
                   "fritter", "nugget", "deep-fried"}
PLAIN_COOK_WORDS = {"cooked", "boiled", "steamed", "roasted", "grilled",
                    "poached", "broiled"}

# An unqualified query means "as eaten". Default it to cooked ONLY where the raw
# form is inedible -- grains, meat, fish, eggs. Everywhere else raw IS the eaten
# form, and forcing cooked inflates carbs: baked apple is 22.7g against 14g raw,
# because baking drives off water and concentrates the sugar. USDA also files
# plain tofu under "raw", so a blanket raw penalty pushes it to "Tofu, fried".
COOK_REQUIRED_HEADS = {
    "rice", "millet", "wheat", "oat", "oats", "grain", "grains", "barley",
    "sorghum", "amaranth", "quinoa", "buckwheat", "noodle", "noodles", "pasta",
    "dumpling", "dumplings", "bun", "buns", "porridge", "congee",
    "bean", "beans", "lentil", "lentils", "soybean", "potato", "potatoes", "corn",
    "meat", "pork", "beef", "chicken", "duck", "lamb", "mutton", "liver", "tripe",
    "fish", "shrimp", "prawn", "crab", "squid", "clam", "eel", "egg", "eggs",
}

# Concentrated or sweetened forms are a different food from the fresh one:
# "Milk, dry, not reconstituted" is 52g carbs where fluid milk is 4.8g, and
# "Tomato, green, pickled" carries added sugar.
CONCENTRATED_WORDS = {"dry", "dried", "powder", "powdered", "dehydrated",
                      "concentrate", "concentrated", "pickled", "candied",
                      "sweetened", "syrup"}


def _stem(tokens):
    """Crude plural folding so 'noodles' matches 'noodle'.

    The -es case is not cosmetic: USDA writes "Tomatoes, raw", and stripping
    only the trailing 's' yields "tomatoe", which never meets the query token
    "tomato" -- so raw tomato could not even enter scoring and the query landed
    on "Tomato, green, pickled".
    """
    out = set(tokens)
    out |= {t[:-1] for t in tokens if t.endswith("s") and len(t) > 3}
    out |= {t[:-2] for t in tokens if t.endswith("es") and len(t) > 4}
    return out


def _cook_state(tokens):
    """-> 'cooked' | 'raw' | None"""
    ts = set(tokens)
    if ts & COOKED_WORDS:
        return "cooked"
    if ts & RAW_WORDS:
        return "raw"
    return None


def score_candidate(query: str, cand, prefer_cooked: bool = True) -> float:
    """Score a candidate against the query over its FULL description.

    The predecessor scored only `description.split(",")[0]`, which is blind to
    everything after the first comma -- and USDA's inverted naming puts the
    discriminating words exactly there ("Cabbage, chinese (pak-choi), cooked").

    prefer_cooked: diet logs record eaten food, so when the query gives no
    cooking state, lean cooked rather than raw.
    """
    q_tok = USDADatabase.tokenize(query)
    if not q_tok:
        return 0.0
    d_tok = USDADatabase.tokenize(cand["description"])

    q_content = [t for t in q_tok if t not in STOPWORDS] or q_tok
    q_set, d_set = _stem(q_content), _stem(d_tok)

    # Coverage of the query by the candidate -- the dominant term.
    cov = len(q_set & d_set) / len(q_set)
    score = 10.0 * cov

    # Headword: USDA's first segment is the food's head noun, and the candidate
    # must BE the thing asked for. "Soup, rice" mentions rice but IS a soup --
    # bag-of-words coverage cannot see that, and without this term plain "rice"
    # matches rice soup and lands at 7g carbs instead of 28g.
    #
    # The predecessor scored ONLY this segment, which was the opposite error:
    # blind to everything after the comma, where USDA hides the discriminators
    # ("Cabbage, chinese (pak-choi)"). Both terms are needed -- head says WHAT
    # the food is, full coverage says WHICH variant of it.
    head_set = _stem(USDADatabase.tokenize(cand["description"].split(",")[0]))
    if head_set:
        score += 4.0 * (len(q_set & head_set) / len(head_set))

    # Contiguous phrase match is a strong signal ("bitter melon" in
    # "Bitter melon, cooked") and is invisible to bag-of-words coverage.
    if " ".join(q_content) in " ".join(d_tok):
        score += 3.0

    # A dish form the query never asked for ("soup" for a bare "rice") is a
    # different food, not a verbose synonym of the same one.
    if (d_set & DISH_FORMS) and not (q_set & DISH_FORMS):
        score -= 3.0

    # Dilution: a description carrying many unrelated words is a looser match.
    # Weak on purpose -- USDA descriptions are verbose by design, and an
    # aggressive penalty here re-creates the generic-shortest bias we removed.
    extra = len(d_set - q_set)
    score -= 0.15 * extra

    # Cooking-state alignment. Method words are read off the RAW query tokens,
    # not q_content -- STOPWORDS strips "fried"/"steamed", so scoring off
    # q_content made "fried rice" look like a query that never asked for frying
    # and then penalised the fried entry it wanted.
    q_raw = set(q_tok)
    cook_required = bool(q_set & COOK_REQUIRED_HEADS)
    q_state = _cook_state(q_tok) or ("cooked" if (prefer_cooked and cook_required) else None)
    d_state = _cook_state(d_tok)
    if q_state and d_state:
        score += 2.0 if q_state == d_state else -2.5
    elif not cook_required and d_state == "raw":
        score += 0.5   # raw is the eaten form for fruit, salad veg, plain tofu

    # Frying is an ingredient, not a preparation: unless the query asked for it,
    # the batter shows up as carbs the food never had ("Fish, cod, fried" = 11.7g
    # where plain cod is 0). This must also fire when the query names a DIFFERENT
    # method -- "steamed fish" matched the fried entry because steamed and fried
    # are both merely "cooked".
    if not (q_raw & ADDED_FAT_WORDS):
        if d_set & ADDED_FAT_WORDS:
            score -= 2.0
        elif (d_set & PLAIN_COOK_WORDS) and cook_required:
            score += 1.0

    if (d_set & CONCENTRATED_WORDS) and not (q_raw & CONCENTRATED_WORDS):
        score -= 2.0

    # FNDDS holds prepared mixed dishes; foundation/sr_legacy hold ingredients.
    # Nudge only -- never enough to override coverage.
    dt = cand["data_type"]
    if dt == "survey_fndds_food":
        score += 0.5
    elif dt in ("foundation_food", "sr_legacy_food"):
        score += 0.3

    return score


class USDADatabase:
    """Wrapper for USDA nutrition SQLite database.

    The recall tiers below query `description LIKE ?`, NOT `lower(description)
    LIKE ?`. SQLite's LIKE is already case-insensitive for ASCII, and wrapping the
    column in lower() makes the expression unindexable -- every tier became a full
    scan of 101k rows, so a lexicon build over 23k components took 76 minutes.
    With `idx_food_desc_nocase` (description COLLATE NOCASE) and the bare column,
    the same query plans as SEARCH USING INDEX: 16.4 ms -> 0.10 ms, 164x.

    This matters more than it looks: USDA's Branded Foods set is 2,007,636 rows,
    20x this bank. Unindexed, importing it would make retrieval unusable.
    """

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
        """Multi-tier RECALL, then score-based RANK.

        Returns list of dicts (top-k, best-scoring first). Every element is a
        plain dict -- callers may rely on .get(). Keys: fdc_id, description,
        data_type, calories, protein, fat, carbs, fiber, __score, and __alias
        when the candidate came from the curated alias dict.
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
            """Helper: add rows not yet seen, as plain dicts."""
            for r in rows:
                d = dict(r)
                if d["fdc_id"] in seen:
                    continue
                seen.add(d["fdc_id"])
                results.append(d)

        cols = ("food.fdc_id, food.description, food.data_type, "
                "food.calories, food.protein, food.fat, food.carbs, food.fiber")
        whole = " ".join(toks)

        # Tier 1: Description headword IS the query ('rice,%' or 'chinese cabbage,%')
        # LIMIT is generous because ORDER BY length keeps only the SHORTEST
        # descriptions -- at LIMIT 10, "Egg, whole, cooked, hard-boiled" never
        # entered the pool and "Egg, creamed" won by default. Recall is cheap;
        # scoring decides the winner.
        add(list(self.con.execute(
            f"SELECT {cols} FROM food WHERE description LIKE ? AND food.calories IS NOT NULL "
            f"ORDER BY length(description) LIMIT 40",
            (whole + ",%",)
        ).fetchall()))

        # Tier 2: Description = query exactly
        add(list(self.con.execute(
            f"SELECT {cols} FROM food WHERE description = ? AND food.calories IS NOT NULL LIMIT 5",
            (whole,)
        ).fetchall()))

        # Tier 3: Description starts with query as phrase
        add(list(self.con.execute(
            f"SELECT {cols} FROM food WHERE description LIKE ? AND food.calories IS NOT NULL "
            f"ORDER BY length(description) LIMIT 10",
            (whole + " %",)
        ).fetchall()))

        # Tier 4-5: Per-token headword/prefix (if multi-token)
        if len(toks) >= 2:
            for t in toks:
                add(list(self.con.execute(
                    f"SELECT {cols} FROM food WHERE description LIKE ? AND food.calories IS NOT NULL "
                    f"ORDER BY length(description) LIMIT 5",
                    (t + ",%",)
                ).fetchall()))
            for t in toks:
                add(list(self.con.execute(
                    f"SELECT {cols} FROM food WHERE description LIKE ? AND food.calories IS NOT NULL "
                    f"ORDER BY length(description) LIMIT 3",
                    (t + "%",)
                ).fetchall()))

        # Tier 6: FTS5 AND (all tokens must appear, anywhere in the description).
        # This is the tier that actually reaches USDA's inverted names --
        # "chinese cabbage" only meets "Cabbage, chinese (pak-choi)" here.
        add(list(self.con.execute(
            f"SELECT {cols} FROM food_fts JOIN food ON food.rowid = food_fts.rowid "
            f"WHERE food_fts MATCH ? AND food.calories IS NOT NULL ORDER BY rank LIMIT ?",
            (" ".join(toks), FTS_RECALL)
        ).fetchall()))

        # Tier 7: FTS5 OR (any token). Always run -- it is pure recall, and
        # ranking now happens below, so extra candidates cost nothing but time.
        or_query = " OR ".join(toks)
        add(list(self.con.execute(
            f"SELECT {cols} FROM food_fts JOIN food ON food.rowid = food_fts.rowid "
            f"WHERE food_fts MATCH ? AND food.calories IS NOT NULL ORDER BY rank LIMIT ?",
            (or_query, FTS_RECALL)
        ).fetchall()))

        # RANK: tier order is recall order, not quality order. Score every
        # candidate over its full description and re-sort.
        for c in results:
            c["__score"] = score_candidate(food, c)
        results.sort(key=lambda c: c["__score"], reverse=True)

        return results[:k]

    def get_by_fdc_id(self, fdc_id: int):
        """Fetch single food by fdc_id."""
        row = self.con.execute(
            "SELECT fdc_id, description, data_type, calories, protein, fat, carbs, fiber "
            "FROM food WHERE fdc_id = ?",
            (fdc_id,)
        ).fetchone()
        return dict(row) if row else None

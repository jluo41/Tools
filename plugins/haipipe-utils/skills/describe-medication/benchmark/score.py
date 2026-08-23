"""What "right" means for a drug, and how the numbers are aggregated.

TWO PREDICTIONS ARE GRADED, NOT ONE
================================================================================
    Ingredient   the BANK's word. Null wherever the FDA Directory does not
                 list the product, which is 42% of Shanghai's insulin and all
                 of OhioT1DM.
    DrugKey      the SEAM to describe-insulin. Rule 9: it carries the bank's
                 word when there is one and the LOG's own words when there is
                 not, so it is non-null where Ingredient is null.

Grading only Ingredient would score the bank; grading only DrugKey would score
the log. Both are reported, and the gap between them is the size of what rule 9
rescued.

THE HEADLINE IS A CURVE, NOT A NUMBER
================================================================================
Accuracy and coverage trade off, and either alone can be moved without
improving anything: answer nothing and accuracy is 1.0, answer everything and
coverage is 1.0. So the result is a risk-coverage curve, cumulative over the
confidence order the member DECLARES -- read from `_stats.json`, never hard
coded, so the same code runs for a member whose tiers are MEASURED/ESTIMATED.

If accuracy does not fall monotonically down that curve, the ladder is
mis-ordered, and that is a finding about the resolver, not about the gold.

THREE WEIGHTINGS, ALWAYS
================================================================================
    row     every administration counts once. Common drugs dominate. DEPLOYMENT.
    type    every distinct STRING or ID counts once. PRODUCT VOCABULARY.
    drug    every distinct GOLD DRUG counts once. DRUG VOCABULARY.

`type` and `drug` are not the same question and the gap between them is large:
816 resolvable WellDoc MedicationIDs collapse to 506 drugs, and one drug can
carry fifteen ids (Levothyroxine Sodium) or six (Insulin lispro, 99,138 rows).
Under `type`, a drug that happens to be stocked in fifteen strengths counts
fifteen times; 'how many DRUGS do we know' had no answer at all until this
weighting existed.

THE GROUPING IS THE GOLD'S, NEVER THE RESOLVER'S. Collapsing by our own
`DrugKey` would let a resolver improve its score by merging things: two units it
wrongly calls one drug would become one unit of error instead of two. Grouping
by the gold molecule cannot be gamed from inside.

Quoting any one of the three without saying which is the failure mode this
module exists to prevent.
"""
from typing import Dict, List, Optional, Sequence

import drugname as D


def grade_unit(pred: Dict, gold_ing, gold_alts, gold_ndc9: Sequence[str]) -> Dict:
    """One unit, graded at both granularities."""
    ing = pred.get("Ingredient")
    key = pred.get("DrugKey")
    alts = [] if gold_alts is None else list(gold_alts)
    golds = [g for g in [gold_ing] + alts if g is not None and str(g).strip()]

    def best(p):
        if p is None or not golds:
            return (False, 0.0)
        tp = D.tokens(p)
        return (any(D.same(p, g) for g in golds),
                max((D.f1(tp, D.tokens(g)) for g in golds), default=0.0))

    ing_exact, ing_f1 = best(ing)
    key_exact, key_f1 = best(key)

    ours9 = D.ndc9(pred.get("NDC")) if pred.get("NDC") else ""
    gset = {g for g in (gold_ndc9 or []) if g}
    return {
        "answered_ingredient": ing is not None,
        "answered_key": key is not None,
        "ingredient_exact": ing_exact, "ingredient_f1": ing_f1,
        "drugkey_exact": key_exact, "drugkey_f1": key_f1,
        "answered_product": bool(ours9),
        # A pharmacy string names a DRUG and a drug is marketed as many
        # packages, so gold is a SET and membership is the test. Demanding one
        # exact NDC would measure which manufacturer we happened to hit.
        "product_hit": bool(ours9 and ours9 in gset),
        "product_gradeable": bool(gset),
    }


def _agg(rows: List[Dict], weights: List[float]) -> Dict:
    tot = sum(weights) or 1.0

    def wmean(key, among=None):
        num = den = 0.0
        for r, w in zip(rows, weights):
            if among and not r[among]:
                continue
            num += w * float(r[key])
            den += w
        return (num / den) if den else None

    return {
        "n_units": len(rows),
        "weight": round(tot, 1),
        "coverage_ingredient": wmean("answered_ingredient"),
        "coverage_key": wmean("answered_key"),
        # accuracy AMONG ANSWERED -- the selective-prediction number. Reported
        # beside coverage and never instead of it.
        "ingredient_exact_of_answered": wmean("ingredient_exact", "answered_ingredient"),
        "ingredient_f1_of_answered": wmean("ingredient_f1", "answered_ingredient"),
        "drugkey_exact_of_answered": wmean("drugkey_exact", "answered_key"),
        # and over EVERY unit, answered or not -- the end-to-end number
        "ingredient_exact_of_all": wmean("ingredient_exact"),
        "drugkey_exact_of_all": wmean("drugkey_exact"),
        # Product needs the same coverage/accuracy split as ingredient, and
        # for a sharper reason: on a NAME the resolver deliberately returns no
        # NDC, because a generic name is marketed as hundreds of products and
        # picking one would be inventing a manufacturer. Folding that refusal
        # into an accuracy reads as 0% wrong when it is 100% not-attempted.
        "product_coverage": wmean("answered_product", "product_gradeable"),
        "product_hit_of_answered": wmean("product_hit", "answered_product"),
        "product_hit_of_gradeable": wmean("product_hit", "product_gradeable"),
        "n_product_gradeable": sum(1 for r in rows if r["product_gradeable"]),
    }


def drug_weights(gold_keys: Sequence[str]) -> List[float]:
    """1/n for each unit sharing a gold drug, so every DRUG contributes 1.0.

    A unit whose gold is blank keeps weight 1: it is its own drug as far as
    anything here can tell, and silently dropping it would shrink the
    denominator of a vocabulary claim.
    """
    norm = [" ".join(sorted(D.tokens(g))) if g else None
            for g in gold_keys]
    n: Dict[str, int] = {}
    for k in norm:
        if k:
            n[k] = n.get(k, 0) + 1
    return [1.0 / n[k] if k else 1.0 for k in norm]


def summarize(graded: List[Dict], confs: List[str], row_w: List[float],
              conf_order: List[str], trusted: List[str],
              drug_w: Optional[List[float]] = None) -> Dict:
    """Per tier, cumulative down the declared order, and all three weightings."""
    ones = [1.0] * len(graded)
    W = {"row": row_w, "type": ones}
    if drug_w is not None:
        W["drug"] = drug_w
    out = {
        "overall": {k: _agg(graded, w) for k, w in W.items()},
        "by_tier": {}, "curve": {k: [] for k in W},
        "conf_order": conf_order, "trusted": trusted,
    }
    for t in conf_order:
        idx = [i for i, c in enumerate(confs) if c == t]
        if not idx:
            continue
        out["by_tier"][t] = {
            k: _agg([graded[i] for i in idx], [w[i] for i in idx])
            for k, w in W.items()
        }

    seen: List[int] = []
    for t in conf_order:
        seen += [i for i, c in enumerate(confs) if c == t]
        if not seen:
            continue
        for w_name, w in W.items():
            inc = _agg([graded[i] for i in seen], [w[i] for i in seen])
            tot = sum(w) or 1.0
            out["curve"][w_name].append({
                "through_tier": t,
                "coverage": sum(w[i] for i in seen) / tot,
                "ingredient_exact": inc["ingredient_exact_of_all"],
                "product_hit": inc["product_hit_of_gradeable"],
            })

    # Monotone means the ladder is ordered right. It is checked here rather
    # than left to the reader, because a non-monotone ladder is a bug with a
    # one-line fix (reorder the declaration) that nobody notices in a table.
    for w_name in W:
        acc = [p["ingredient_exact"] for p in out["curve"][w_name]
               if p["ingredient_exact"] is not None]
        out.setdefault("monotone", {})[w_name] = all(
            a >= b - 1e-9 for a, b in zip(acc, acc[1:]))
    return out

"""What "right" means for an insulin, and how the numbers are aggregated.

THREE PREDICTIONS ARE GRADED, NOT ONE
================================================================================
    DrugKey          the SEAM. describe-medication's answer, which is this
                     skill's input. Rule 9 makes it ECHO the raw string on a
                     bank miss, so a non-null DrugKey proves nothing and
                     `MedConf` is what says whether the first half resolved.
    InsulinResolved  the PK-table row actually used. THE MOLECULE.
    InsulinClass     rapid / short / intermediate / long / ultra_long / premix.
                     THE CURVE, and the only one a clinician would notice.

The class is not a softer version of the molecule. A wrong molecule inside the
right class moves an IOB curve by minutes; a wrong class moves it by hours, and
for a premix read as monophasic it loses a whole second rise. Reporting one
number would hide which of those happened.

MOLECULE ACCURACY IS BOUNDED ABOVE BY THE GOLD'S RESOLUTION
================================================================================
MEPS names the parent molecule: SEMGLEE is 'INSULIN GLARGINE', LYUMJEV is
'INSULIN LISPRO', TOUJEO is 'INSULIN GLARGINE'. Our table answers
'insulin glargine-yfgn', 'insulin lispro-aabc', 'insulin glargine u300'. Those
are MORE specific than the answer key, not wrong, so `same_molecule` folds the
variant and `n_more_specific` counts how often it did. A benchmark that scored
them as misses would push the resolver toward a coarser table.

THE HEADLINE IS A CURVE, NOT A NUMBER
================================================================================
Same as medication's: cumulative over the DECLARED confidence order, both
weightings always, and a monotonicity flag -- a ladder whose accuracy does not
fall as coverage grows is mis-ordered, which is a finding about the resolver.
"""
from typing import Dict, List, Optional

import insulinname as N


def grade_unit(pred: Dict, med_conf: Optional[str], gold_molecule: str,
               gold_alts, med_trusted: List[str]) -> Dict:
    """One MEPS string, graded at molecule and class."""
    res = pred.get("InsulinResolved")
    cls = pred.get("InsulinClass")
    alts = [] if gold_alts is None else list(gold_alts)
    golds = [g for g in [gold_molecule] + alts if g and str(g).strip()]

    mol_hit = any(N.same_molecule(res, g) for g in golds) if res else False
    mol_f1 = max((N.overlap(res, g) for g in golds), default=0.0) if res else 0.0
    variant = next((N.variant_of(res, g) for g in golds
                    if N.variant_of(res, g)), None) if mol_hit else None

    # The class gold is derived from the GOLD MOLECULE by this benchmark's own
    # table, never by insnorm's. A unit whose gold names no molecule at all
    # ('INSULIN') is not gradeable for class and says so rather than counting
    # as a miss.
    gold_cls = next((N.class_of(g) for g in golds if N.class_of(g)), None)

    return {
        # the seam: did the FIRST half resolve? not whether DrugKey is non-null
        "med_resolved": bool(med_conf in med_trusted),
        "answered_molecule": res is not None,
        "molecule_exact": mol_hit,
        "molecule_f1": mol_f1,
        "more_specific": variant is not None,
        "variant": variant,
        "answered_class": cls is not None,
        "class_gradeable": gold_cls is not None,
        "class_exact": bool(gold_cls and cls == gold_cls),
        "gold_class": gold_cls,
        "pred_class": cls,
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
        # the seam, first: everything downstream is bounded by it
        "seam_med_resolved": wmean("med_resolved"),
        "coverage_molecule": wmean("answered_molecule"),
        "coverage_class": wmean("answered_class"),
        "molecule_exact_of_answered": wmean("molecule_exact", "answered_molecule"),
        "molecule_f1_of_answered": wmean("molecule_f1", "answered_molecule"),
        "molecule_exact_of_all": wmean("molecule_exact"),
        # class is scored only where the gold names a molecule to derive one
        "class_exact_of_answered": wmean("class_exact", "answered_class"),
        "class_exact_of_gradeable": wmean("class_exact", "class_gradeable"),
        "n_class_gradeable": sum(1 for r in rows if r["class_gradeable"]),
        "n_more_specific": sum(1 for r in rows if r["more_specific"]),
    }


def summarize(graded: List[Dict], confs: List[str], row_w: List[float],
              conf_order: List[str], trusted: List[str]) -> Dict:
    ones = [1.0] * len(graded)
    out = {
        "overall": {"row": _agg(graded, row_w), "type": _agg(graded, ones)},
        "by_tier": {}, "curve": {"row": [], "type": []},
        "conf_order": conf_order, "trusted": trusted,
    }
    for t in conf_order:
        idx = [i for i, c in enumerate(confs) if c == t]
        if not idx:
            continue
        out["by_tier"][t] = {
            "row": _agg([graded[i] for i in idx], [row_w[i] for i in idx]),
            "type": _agg([graded[i] for i in idx], [1.0] * len(idx)),
        }

    seen: List[int] = []
    for t in conf_order:
        seen += [i for i, c in enumerate(confs) if c == t]
        if not seen:
            continue
        for w_name, W in (("row", row_w), ("type", ones)):
            inc = _agg([graded[i] for i in seen], [W[i] for i in seen])
            tot = sum(W) or 1.0
            out["curve"][w_name].append({
                "through_tier": t,
                "coverage": sum(W[i] for i in seen) / tot,
                "molecule_exact": inc["molecule_exact_of_all"],
                "class_exact": inc["class_exact_of_gradeable"],
            })

    for w_name in ("row", "type"):
        acc = [p["molecule_exact"] for p in out["curve"][w_name]
               if p["molecule_exact"] is not None]
        out.setdefault("monotone", {})[w_name] = all(
            a >= b - 1e-9 for a, b in zip(acc, acc[1:]))

    # A CONFUSION MATRIX, not just a rate. Six classes and a handful of units:
    # 'class accuracy 82%' says nothing a clinician can act on, while
    # 'short answered as premix, 176 fills' names the defect.
    conf_pairs: Dict[str, int] = {}
    for r, w in zip(graded, row_w):
        if not r["class_gradeable"] or r["gold_class"] == r["pred_class"]:
            continue
        k = f"{r['gold_class']} -> {r['pred_class']}"
        conf_pairs[k] = conf_pairs.get(k, 0) + int(w)
    out["class_confusion"] = dict(sorted(conf_pairs.items(),
                                         key=lambda kv: -kv[1]))
    return out


# =============================================================================
# I3a  DURATION, against a number measured on a person
# =============================================================================
# THE ONE WAY TO MAKE THIS METRIC MEANINGLESS IS TO PASS THE GOLD IN.
# `normalize(..., dia_hours=x)` REPLACES DurationMin with x and stamps GOOD.
# Grading that against x scores a copy. The caller must therefore withhold
# dia_hours here, and every number below is the TABLE's answer, tier OK at best.
#
# WHAT A GOOD SCORE WOULD AND WOULD NOT MEAN
# DIA takes three preset values -- 2, 5, 7 hours -- so it is a clinician's
# SETTING, not a clamp study. Matching it exactly is not the goal and would be
# suspicious; the useful readings are the SIGN and SIZE of the gap per class,
# because a table that is systematically short on rapid analogues and long on
# regular human insulin is a table to fix, not noise.

# Half an hour. Tight enough to notice a class error, loose enough that the
# three-preset grid does not manufacture failures.
TOLERANCE_H = 0.5


def grade_duration(pred: Dict, gold_dia_h: float) -> Dict:
    """One prescription. The gold is hours; the record is minutes."""
    dur = pred.get("DurationMin")
    ours_h = None if dur is None else float(dur) / 60.0
    err = None if ours_h is None else ours_h - float(gold_dia_h)
    return {
        "answered": ours_h is not None,
        # A prescription whose drug is not an insulin cannot be graded on an
        # insulin action curve. Counted, never scored as wrong.
        "gradeable": pred.get("InsulinClass") is not None,
        "ours_h": ours_h,
        "gold_h": float(gold_dia_h),
        "err_h": err,
        "abs_err_h": None if err is None else abs(err),
        "within_tol": bool(err is not None and abs(err) <= TOLERANCE_H),
        "pred_class": pred.get("InsulinClass"),
        "conf": pred.get("PKConf"),
    }


def summarize_duration(graded: List[Dict]) -> Dict:
    import statistics as st

    ok = [g for g in graded if g["gradeable"] and g["abs_err_h"] is not None]
    out = {
        "n_units": len(graded),
        "coverage": (sum(1 for g in graded if g["answered"]) / len(graded)
                     if graded else None),
        "n_gradeable": len(ok),
        "n_not_insulin": sum(1 for g in graded if not g["gradeable"]),
        "median_abs_err_h": st.median([g["abs_err_h"] for g in ok]) if ok else None,
        "mean_abs_err_h": (sum(g["abs_err_h"] for g in ok) / len(ok)) if ok else None,
        # SIGNED, and reported beside the absolute one on purpose: a table that
        # is 0.5 h short everywhere and one that is 0.5 h off at random have the
        # same MAE and need different fixes.
        "median_signed_err_h": st.median([g["err_h"] for g in ok]) if ok else None,
        "within_tolerance": (sum(1 for g in ok if g["within_tol"]) / len(ok)
                             if ok else None),
        "tolerance_h": TOLERANCE_H,
    }

    by = {}
    for g in ok:
        b = by.setdefault(g["pred_class"] or "?",
                          {"n": 0, "errs": [], "gold": set(), "ours": set()})
        b["n"] += 1
        b["errs"].append(g["err_h"])
        b["gold"].add(g["gold_h"])
        b["ours"].add(g["ours_h"])
    out["by_class"] = {
        k: {"n": v["n"],
            "median_signed_err_h": st.median(v["errs"]),
            "gold_dia_h": sorted(v["gold"]),
            "our_duration_h": sorted(v["ours"])}
        for k, v in sorted(by.items(), key=lambda kv: -kv[1]["n"])}

    # The gold's own grid, so a reader can see it is three values and not a
    # continuous measurement before reading any error as physiology.
    grid = {}
    for g in graded:
        grid[g["gold_h"]] = grid.get(g["gold_h"], 0) + 1
    out["gold_grid"] = {str(k): v for k, v in sorted(grid.items())}
    return out

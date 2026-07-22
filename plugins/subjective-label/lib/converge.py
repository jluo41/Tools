"""Convergence gate (S4, deterministic core).

Encodes F8: "stable ≠ correct". A guideline is CONVERGED only when it plateaus on
the fixed anchor AND generalizes (held-out gap small) AND the objective plateaus.
A high anchor κ with a large held-out gap is OVERFIT, not converged — exactly the
B03 case (anchor 0.93 / held-out 0.67).

Three sets feed this (see ref-config.md eval + note-update.md):
  fixed anchor  → anchor_kappa   (version comparison / correctness)
  fresh held-out→ heldout_kappa  (honest generalization; catches over-fit)
  objective     → objective_score (construct fitness; S2)

Usage:
    python lib/converge.py --project-dir <task>     # reads eval/trajectory.jsonl + config
    python lib/converge.py selftest

trajectory rows (one per version) may carry any of:
    anchor_kappa | kappa_majority_vs_gold   (anchor correctness)
    heldout_kappa                           (fresh held-out)
    objective_score                         (S2 objective)
"""

import argparse
import json
import sys
from pathlib import Path


def _cfg(project_dir):
    import yaml  # noqa: PLC0415
    p = project_dir / "config.yaml"
    c = (yaml.safe_load(p.read_text()) or {}) if p.exists() else {}
    conv = c.get("convergence") or {}
    return {"eps": float(conv.get("objective_plateau", 0.02)),
            "anchor_eps": float(conv.get("anchor_plateau", conv.get("objective_plateau", 0.02))),
            "heldout_gap_max": float(conv.get("heldout_gap_max", 0.05))}


def _seq(rows, *keys):
    out = []
    for r in rows:
        v = next((r[k] for k in keys if r.get(k) is not None), None)
        out.append(v)
    return out


def assess(rows, eps=0.02, anchor_eps=0.02, heldout_gap_max=0.05):
    """rows: trajectory in version order. Returns verdict dict."""
    if not rows:
        return {"verdict": "NO_DATA", "reasons": ["empty trajectory"]}
    anchor = _seq(rows, "anchor_kappa", "kappa_majority_vs_gold")
    held = _seq(rows, "heldout_kappa")
    obj = _seq(rows, "objective_score")
    reasons = []

    a_last = anchor[-1]
    h_last = held[-1]
    gap = round(a_last - h_last, 4) if (a_last is not None and h_last is not None) else None
    overfit = gap is not None and gap > heldout_gap_max

    plateau = (len(anchor) >= 2 and anchor[-1] is not None and anchor[-2] is not None
               and abs(anchor[-1] - anchor[-2]) < anchor_eps)
    improving = (len(anchor) >= 2 and anchor[-1] is not None and anchor[-2] is not None
                 and anchor[-1] - anchor[-2] >= anchor_eps)
    obj_vals = [o for o in obj if o is not None]
    obj_plateau = (len(obj_vals) < 2) or (abs(obj_vals[-1] - obj_vals[-2]) < eps)

    if overfit:
        verdict = "OVERFIT"
        reasons.append(f"held-out gap {gap} > max {heldout_gap_max} — anchor κ is optimistic, NOT converged")
    elif plateau and (gap is None or not overfit) and obj_plateau:
        verdict = "CONVERGED"
        reasons.append(f"anchor plateau (Δ<{anchor_eps})"
                       + (f" · held-out gap {gap} ≤ {heldout_gap_max}" if gap is not None else " · NO held-out — gap unchecked ⚠")
                       + (" · objective plateau" if len(obj_vals) >= 2 else ""))
        if gap is None:
            verdict = "CONVERGED_NO_HELDOUT"
    elif improving:
        verdict = "IMPROVING"
        reasons.append(f"anchor κ still rising (Δ={round(anchor[-1]-anchor[-2],4)})")
    else:
        verdict = "STALLED"
        reasons.append("anchor flat but not clearly converged (check objective / held-out)")

    return {"verdict": verdict, "anchor_kappa": a_last, "heldout_kappa": h_last,
            "heldout_gap": gap, "objective_score": (obj_vals[-1] if obj_vals else None),
            "reasons": reasons, "n_versions": len(rows)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-dir", type=Path)
    ap.add_argument("cmd", nargs="?", default=None)
    args = ap.parse_args()
    if args.cmd == "selftest":
        return _selftest()
    pd = args.project_dir.resolve()
    traj = pd / "eval" / "trajectory.jsonl"
    rows = [json.loads(l) for l in traj.read_text().splitlines() if l.strip()]
    rows.sort(key=lambda r: r.get("version", ""))
    t = _cfg(pd)
    print(json.dumps(assess(rows, t["eps"], t["anchor_eps"], t["heldout_gap_max"]), indent=2, ensure_ascii=False))


def _selftest():
    # rising → IMPROVING
    r = assess([{"version": "v1", "anchor_kappa": .5, "heldout_kappa": .48},
                {"version": "v2", "anchor_kappa": .7, "heldout_kappa": .68}])
    assert r["verdict"] == "IMPROVING", r
    # plateau + tight held-out → CONVERGED
    r = assess([{"version": "v3", "anchor_kappa": .78, "heldout_kappa": .76},
                {"version": "v4", "anchor_kappa": .79, "heldout_kappa": .77}])
    assert r["verdict"] == "CONVERGED", r
    # plateau but big held-out gap → OVERFIT (the B03 trap)
    r = assess([{"version": "v3", "anchor_kappa": .92, "heldout_kappa": .66},
                {"version": "v4", "anchor_kappa": .93, "heldout_kappa": .67}])
    assert r["verdict"] == "OVERFIT", r
    # plateau, no held-out → flagged
    r = assess([{"version": "v3", "anchor_kappa": .9}, {"version": "v4", "anchor_kappa": .91}])
    assert r["verdict"] == "CONVERGED_NO_HELDOUT", r
    print("selftest OK: IMPROVING / CONVERGED / OVERFIT (B03 trap caught) / CONVERGED_NO_HELDOUT")


if __name__ == "__main__":
    main()

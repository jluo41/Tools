"""Plateau diagnostic (S4, deterministic core). NOT a stop gate.

Encodes F8: "stable ≠ correct". The verdict is a DIAGNOSTIC for the family's stopping
law (quality floor, k consecutive rounds, coverage, risk, human sign-off); it never
decides STOP by itself. PLATEAU_DIAGNOSTIC means the last two versions moved less than
the plateau epsilon, held-out gap is small, the objective is flat, AND the anchor κ is
at or above `stopping.quality_floor` when one is configured. Below the floor the verdict
is BELOW_QUALITY_FLOOR and never reads as a plateau/convergence.
A high anchor κ with a large held-out gap is OVERFIT — exactly the
B03 case (anchor 0.93 / held-out 0.67).

Three sets feed this (see ref-config.md eval + note-update.md):
  fixed anchor  → anchor_kappa   (version comparison / correctness)
  fresh held-out→ heldout_kappa  (honest generalization; catches over-fit)
  objective     → objective_score (construct fitness; S2)

Usage:
    python engine/converge.py --project-dir <task>     # reads eval/trajectory.jsonl + config
    python engine/converge.py selftest

Config: convergence.{objective_plateau, anchor_plateau, heldout_gap_max};
        stopping.quality_floor (number, or {kappa|anchor_kappa: number}).

trajectory rows (one per version, sorted in natural version order) may carry any of:
    anchor_kappa | kappa_majority_vs_gold   (anchor correctness)
    heldout_kappa                           (fresh held-out)
    objective_score                         (S2 objective)
"""

import argparse
import json
import re
from pathlib import Path


def version_key(version):
    """Natural sort key: v2 < v9 < v10 (not the string order v10 < v2)."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", str(version))]


def _quality_floor(stopping):
    floor = (stopping or {}).get("quality_floor")
    if isinstance(floor, dict):
        floor = next((floor[k] for k in ("anchor_kappa", "kappa") if floor.get(k) is not None), None)
    return float(floor) if isinstance(floor, (int, float)) and not isinstance(floor, bool) else None


def _cfg(project_dir):
    import yaml  # noqa: PLC0415
    p = project_dir / "config.yaml"
    c = (yaml.safe_load(p.read_text()) or {}) if p.exists() else {}
    conv = c.get("convergence") or {}
    return {"eps": float(conv.get("objective_plateau", 0.02)),
            "anchor_eps": float(conv.get("anchor_plateau", conv.get("objective_plateau", 0.02))),
            "heldout_gap_max": float(conv.get("heldout_gap_max", 0.05)),
            "quality_floor": _quality_floor(c.get("stopping"))}


def _seq(rows, *keys):
    out = []
    for r in rows:
        v = next((r[k] for k in keys if r.get(k) is not None), None)
        out.append(v)
    return out


def assess(rows, eps=0.02, anchor_eps=0.02, heldout_gap_max=0.05, quality_floor=None):
    """rows: trajectory in version order. Returns a diagnostic verdict dict (not a stop decision)."""
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
    below_floor = quality_floor is not None and (a_last is None or a_last < quality_floor)

    plateau = (len(anchor) >= 2 and anchor[-1] is not None and anchor[-2] is not None
               and abs(anchor[-1] - anchor[-2]) < anchor_eps)
    improving = (len(anchor) >= 2 and anchor[-1] is not None and anchor[-2] is not None
                 and anchor[-1] - anchor[-2] >= anchor_eps)
    obj_vals = [o for o in obj if o is not None]
    obj_plateau = (len(obj_vals) < 2) or (abs(obj_vals[-1] - obj_vals[-2]) < eps)

    if overfit:
        verdict = "OVERFIT"
        reasons.append(f"held-out gap {gap} > max {heldout_gap_max} — anchor κ is optimistic, NOT converged")
    elif plateau and below_floor:
        verdict = "BELOW_QUALITY_FLOOR"
        reasons.append(f"anchor flat (Δ<{anchor_eps}) but κ {a_last} < quality_floor {quality_floor}"
                       " — a plateau below the floor is NOT convergence")
    elif plateau and (gap is None or not overfit) and obj_plateau:
        verdict = "PLATEAU_DIAGNOSTIC"
        reasons.append(f"anchor plateau (Δ<{anchor_eps})"
                       + (f" · held-out gap {gap} ≤ {heldout_gap_max}" if gap is not None else " · NO held-out — gap unchecked ⚠")
                       + (" · objective plateau" if len(obj_vals) >= 2 else "")
                       + (f" · κ ≥ quality_floor {quality_floor}" if quality_floor is not None
                          else " · NO quality_floor configured ⚠"))
        if gap is None:
            verdict = "PLATEAU_DIAGNOSTIC_NO_HELDOUT"
    elif improving:
        verdict = "IMPROVING"
        reasons.append(f"anchor κ still rising (Δ={round(anchor[-1]-anchor[-2],4)})")
    else:
        verdict = "STALLED"
        reasons.append("anchor flat but not clearly converged (check objective / held-out)")

    return {"verdict": verdict, "diagnostic_only": True, "anchor_kappa": a_last,
            "heldout_kappa": h_last, "heldout_gap": gap,
            "objective_score": (obj_vals[-1] if obj_vals else None),
            "quality_floor": quality_floor, "below_quality_floor": below_floor,
            "reasons": reasons, "n_versions": len(rows)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-dir", type=Path)
    ap.add_argument("cmd", nargs="?", default=None)
    args = ap.parse_args()
    if args.cmd == "selftest":
        return _selftest()
    if args.project_dir is None:
        ap.error("--project-dir is required (or run: converge.py selftest)")
    pd = args.project_dir.resolve()
    traj = pd / "eval" / "trajectory.jsonl"
    rows = [json.loads(l) for l in traj.read_text().splitlines() if l.strip()]
    rows.sort(key=lambda r: version_key(r.get("version", "")))
    t = _cfg(pd)
    print(json.dumps(assess(rows, t["eps"], t["anchor_eps"], t["heldout_gap_max"], t["quality_floor"]),
                     indent=2, ensure_ascii=False))


def _selftest():
    # rising → IMPROVING
    r = assess([{"version": "v1", "anchor_kappa": .5, "heldout_kappa": .48},
                {"version": "v2", "anchor_kappa": .7, "heldout_kappa": .68}])
    assert r["verdict"] == "IMPROVING", r
    # plateau + tight held-out → PLATEAU_DIAGNOSTIC
    r = assess([{"version": "v3", "anchor_kappa": .78, "heldout_kappa": .76},
                {"version": "v4", "anchor_kappa": .79, "heldout_kappa": .77}], quality_floor=.6)
    assert r["verdict"] == "PLATEAU_DIAGNOSTIC", r
    # flat but below the quality floor → never a plateau/convergence verdict
    r = assess([{"version": "v1", "anchor_kappa": .10, "heldout_kappa": .10},
                {"version": "v2", "anchor_kappa": .11, "heldout_kappa": .10}], quality_floor=.6)
    assert r["verdict"] == "BELOW_QUALITY_FLOOR", r
    # plateau but big held-out gap → OVERFIT (the B03 trap)
    r = assess([{"version": "v3", "anchor_kappa": .92, "heldout_kappa": .66},
                {"version": "v4", "anchor_kappa": .93, "heldout_kappa": .67}])
    assert r["verdict"] == "OVERFIT", r
    # plateau, no held-out → flagged
    r = assess([{"version": "v3", "anchor_kappa": .9}, {"version": "v4", "anchor_kappa": .91}])
    assert r["verdict"] == "PLATEAU_DIAGNOSTIC_NO_HELDOUT", r
    assert sorted(["v10", "v2", "v9"], key=version_key) == ["v2", "v9", "v10"]
    print("selftest OK: IMPROVING / PLATEAU_DIAGNOSTIC / BELOW_QUALITY_FLOOR / OVERFIT (B03 trap caught)"
          " / PLATEAU_DIAGNOSTIC_NO_HELDOUT")


if __name__ == "__main__":
    main()

"""Load a single individual's context from _WorkSpace/A-User-Store.

Individual layout (haipipe-individual contract):
  UserGroup-<dataset>/Subject-<id>/
    manifest.yaml
    1-SourceStore/{CGM,Diet,Exercise,Medication,Ptt,...}.parquet
    2-RecStore/...

The agent only needs SourceStore for prediction; RecStore is precomputed
record-level binning useful for retrieval/eval, ignored here.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import pandas as pd
import yaml

SOURCE_TABLES = ["CGM", "Diet", "Exercise", "Medication", "Ptt"]


def resolve_workspace_root(workspace_root: str | Path | None = None) -> Path:
    """Project root: explicit arg, HAIPIPE_WORKSPACE_ROOT, then nearest cwd marker."""
    configured = workspace_root or os.environ.get("HAIPIPE_WORKSPACE_ROOT")
    if configured:
        root = Path(configured).expanduser().resolve()
        if not (root / "_WorkSpace").is_dir():
            raise FileNotFoundError(f"No _WorkSpace under configured project root {root}")
        return root
    cwd = Path.cwd().resolve()
    for root in [cwd, *cwd.parents]:
        if (root / "_WorkSpace").is_dir():
            return root
    raise FileNotFoundError("Set --workspace-root or HAIPIPE_WORKSPACE_ROOT to the project containing _WorkSpace")


def resolve_individual_path(individual: str, workspace_root: str | Path | None = None) -> Path:
    """Resolve an absolute Subject path or shorthand within exactly one project."""
    p = Path(individual).expanduser()
    if p.is_absolute():
        if not p.is_dir():
            raise FileNotFoundError(f"Individual directory missing: {p}")
        return p.resolve()
    if ".." in p.parts:
        raise ValueError("Individual shorthand cannot escape the user store")
    store = resolve_workspace_root(workspace_root) / "_WorkSpace" / "A-User-Store"
    candidate = store / p
    if candidate.is_dir():
        return candidate.resolve()
    matches = [g / p for g in store.iterdir() if g.name.startswith("UserGroup-") and (g / p).is_dir()] if store.is_dir() else []
    if len(matches) == 1:
        return matches[0].resolve()
    if len(matches) > 1:
        raise ValueError(f"Individual id {individual!r} is ambiguous: {matches}")
    raise FileNotFoundError(f"Cannot resolve individual {individual!r} under {store}")


def load_patient_ctx(individual: str, cgm_tail: Optional[int] = None, *, workspace_root: str | Path | None = None) -> dict:
    """Load a patient's context dict.

    Args:
        individual: individual path or shorthand (e.g. 'UserGroup-WellDoc2022CGM/Subject-18',
                 'Subject-18', or absolute path).
        cgm_tail: if set, keep only the most recent N CGM rows (sorted by time).

    Returns:
        dict with keys: individual_path, manifest, tables (DataFrame per table).
    """
    individual_dir = resolve_individual_path(individual, workspace_root)
    src = individual_dir / "1-SourceStore"
    if not src.exists():
        raise FileNotFoundError(f"No 1-SourceStore at {individual_dir}")

    manifest = {}
    mf_path = individual_dir / "manifest.yaml"
    if mf_path.exists():
        manifest = yaml.safe_load(mf_path.read_text()) or {}

    tables = {}
    for name in SOURCE_TABLES:
        f = src / f"{name}.parquet"
        if f.exists():
            tables[name] = pd.read_parquet(f)

    if "CGM" in tables and "ObservationDateTime" in tables["CGM"].columns:
        cgm = tables["CGM"].copy()
        cgm["ObservationDateTime"] = pd.to_datetime(
            cgm["ObservationDateTime"], format="mixed", dayfirst=False, errors="coerce"
        )
        cgm = cgm.dropna(subset=["ObservationDateTime", "BGValue"]).sort_values(
            "ObservationDateTime"
        )
        if cgm_tail is not None:
            cgm = cgm.tail(cgm_tail)
        tables["CGM"] = cgm.reset_index(drop=True)

    return {
        "individual_path": str(individual_dir),
        "individual_id": manifest.get("individual_id"),
        "dataset": manifest.get("dataset"),
        "manifest": manifest,
        "tables": tables,
    }


def summarize_ctx(ctx: dict) -> dict:
    """One-glance summary, safe to print."""
    out = {
        "individual_path": ctx["individual_path"],
        "individual_id": ctx["individual_id"],
        "dataset": ctx["dataset"],
        "tables": {},
    }
    for name, df in ctx["tables"].items():
        out["tables"][name] = {"rows": len(df), "cols": list(df.columns)}
    cgm = ctx["tables"].get("CGM")
    if cgm is not None and len(cgm):
        out["cgm_window"] = {
            "n": len(cgm),
            "start": str(cgm["ObservationDateTime"].iloc[0]),
            "end": str(cgm["ObservationDateTime"].iloc[-1]),
            "last_bg": float(cgm["BGValue"].iloc[-1]),
        }
    return out

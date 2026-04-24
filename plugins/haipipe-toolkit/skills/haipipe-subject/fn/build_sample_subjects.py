"""Build per-subject folders under _WorkSpace/A-User-Store/UserGroup-{DatasetTag}/.

Extract-and-copy approach: filter existing global 1-SourceStore + 2-RecStore
parquet files by PatientID and write per-subject slices. Fast (~seconds per
subject) vs. re-running full source/record pipelines.

Folder layout:
  _WorkSpace/A-User-Store/
  ├── UserGroup-OhioT1DM/
  │   ├── Subject-559/{0-RawDataStore,1-SourceStore,2-RecStore,manifest.yaml}
  │   └── ...
  ├── UserGroup-mimiciv-demo/
  ├── UserGroup-mimiciv-3.1/
  └── UserGroup-WellDoc2022CGM/

Usage:
    python build_sample_subjects.py OhioT1DM 540 544 552 559 563
    python build_sample_subjects.py OhioT1DM --n 5
    python build_sample_subjects.py --all --n 5
"""
from __future__ import annotations

import argparse
import datetime as dt
import shutil
import sys
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq
import yaml

WORKSPACE = Path("_WorkSpace")
USER_STORE = WORKSPACE / "A-User-Store"
BUILDER_VERSION = "build_sample_subjects.py v0.4"


def flatten_rel(rel: Path) -> Path:
    """Drop partition (@iXnY) and pure dataset-name wrapper segments.

    Input:  OhioT1DM_v0RecSet/@i1n1/Record-HmPtt.CGM5Min/RecAttr.parquet
    Output: Record-HmPtt.CGM5Min/RecAttr.parquet

    Input:  OhioT1DM/@OhioT1DMxmlv250302/CGM.parquet
    Output: CGM.parquet
    """
    parts = rel.parts
    keep = []
    for p in parts:
        # Skip any @iXnY partition (X,Y numbers)
        if p.startswith("@i") and "n" in p and any(c.isdigit() for c in p):
            continue
        # Skip any @<TagName> SourceSet wrapper (contains version-like tag)
        if p.startswith("@"):
            continue
        # Skip the dataset-name wrappers that match the configured source_set / rec_set roots.
        # We pass these in via context; see build_subject below.
        keep.append(p)
    return Path(*keep) if keep else Path(".")


# ─── Dataset builders ────────────────────────────────────────────────────────
#
# Each builder returns a spec dict with:
#   dataset         — dataset name (matches 0-RawDataStore dir)
#   dataset_tag     — short tag for folder naming (UserGroup-{tag})
#   subject_id      — subject identifier
#   source_set      — path under 1-SourceStore/
#   rec_set         — path under 2-RecStore/
#   pid_column      — column to filter on (all datasets use "PatientID")
#   pid_values      — list of PatientID strings matching this subject
#   raw_paths       — list of absolute paths (Path objects) to raw files
#   raw_copy        — True to copy raw into 0-RawDataStore/, False for pointer-only


def build_ohio(subject_id: str) -> dict:
    cohort_2018 = {"559", "563", "570", "575", "588", "591"}
    cohort_2020 = {"540", "544", "552", "567", "584", "596"}
    if subject_id in cohort_2018:
        cohort = "2018"
    elif subject_id in cohort_2020:
        cohort = "2020"
    else:
        raise ValueError(f"Unknown OhioT1DM subject_id: {subject_id}")
    raw_dir = WORKSPACE / "0-RawDataStore" / "OhioT1DM" / "Source" / cohort
    raw_paths = [raw_dir / "train" / f"{subject_id}-ws-training.xml",
                 raw_dir / "test" / f"{subject_id}-ws-testing.xml"]
    return {
        "dataset": "OhioT1DM", "dataset_tag": "OhioT1DM",
        "subject_id": subject_id,
        "source_set": "OhioT1DM/@OhioT1DMxmlv250302",
        "rec_set": "OhioT1DM_v0RecSet",
        "pid_column": "PatientID",
        "pid_values": [f"ohio-{subject_id}_train", f"ohio-{subject_id}_test"],
        "raw_paths": raw_paths, "raw_copy": True,
    }


def build_mimic_v31(subject_id: str) -> dict:
    return {
        "dataset": "mimiciv-3.1", "dataset_tag": "mimiciv-3.1",
        "subject_id": subject_id,
        "source_set": "mimiciv-3.1/@MIMICIVv31",
        "rec_set": "mimiciv-3.1_v3RecSet",
        "pid_column": "PatientID",
        "pid_values": [f"mimic-{subject_id}"],
        "raw_paths": [WORKSPACE / "0-RawDataStore" / "mimiciv-3.1"],
        "raw_copy": False,
    }


def build_cgmacros(subject_id: str) -> dict:
    return {
        "dataset": "CGMacros", "dataset_tag": "CGMacros",
        "subject_id": subject_id,
        "source_set": "CGMacros/@CGMacrosV251227",
        "rec_set": "CGMacros_v0RecSet",
        "pid_column": "PatientID",
        "pid_values": [f"CGMacros-{subject_id}"],
        "raw_paths": [],
        "raw_copy": False,
    }


def build_welldoc_2022cgm(subject_id: str) -> dict:
    return {
        "dataset": "WellDoc2022CGM", "dataset_tag": "WellDoc2022CGM",
        "subject_id": subject_id,
        "source_set": "WellDoc2022CGM/@WellDocDataV251226",
        "rec_set": "WellDoc2022CGM_v0RecSet",
        "pid_column": "PatientID",
        "pid_values": [f"2022cgm-{subject_id}"],
        "raw_paths": [],  # proprietary, not in _WorkSpace/0-RawDataStore/
        "raw_copy": False,
    }


BUILDERS = {
    "OhioT1DM": build_ohio,
    "mimiciv-3.1": build_mimic_v31,
    "CGMacros": build_cgmacros,
    "WellDoc2022CGM": build_welldoc_2022cgm,
}


def list_candidates(dataset: str, limit: int = 5) -> list[str]:
    """Return first N subject IDs (sorted numerically when possible)."""
    if dataset == "OhioT1DM":
        ids = ["540", "544", "552", "559", "563", "567",
               "570", "575", "584", "588", "591", "596"]
        return sorted(ids, key=int)[:limit]

    # For MIMIC + WellDoc, read a lightweight parquet column to discover PIDs
    base = WORKSPACE / "1-SourceStore"
    if dataset == "mimiciv-3.1":
        anchor = base / "mimiciv-3.1/@MIMICIVv31/Patient.parquet"
        if not anchor.exists():
            # fall back to first available parquet
            anchor = next((base / "mimiciv-3.1/@MIMICIVv31").glob("*.parquet"))
    elif dataset == "CGMacros":
        anchor = base / "CGMacros/@CGMacrosV251227/Ptt.parquet"
    elif dataset == "WellDoc2022CGM":
        anchor = base / "WellDoc2022CGM/@WellDocDataV251226/Ptt.parquet"
        if not anchor.exists():
            anchor = base / "WellDoc2022CGM/@WellDocDataV251226/CGM.parquet"
    else:
        raise NotImplementedError(f"list_candidates not implemented for {dataset}")

    df = pd.read_parquet(anchor, columns=["PatientID"])
    pids = sorted(df["PatientID"].dropna().unique().tolist())
    # strip dataset prefix to get pure subject_id
    prefix = pids[0].split("-")[0] + "-"
    subject_ids = [p[len(prefix):] for p in pids]
    try:
        subject_ids = sorted(subject_ids, key=int)
    except ValueError:
        subject_ids = sorted(subject_ids)
    return subject_ids[:limit]


def filter_parquet(src: Path, dst: Path, pid_col: str, pid_values: list[str]) -> int:
    """Filter parquet by pid column. Returns:
      n>0   → n rows written
      0     → filtered to empty, nothing written (caller should skip)
      -1    → no pid_col in schema, skipped (dictionary table — lives in global store only)
    """
    try:
        schema = pq.read_schema(src)
        if pid_col not in schema.names:
            return -1  # dictionary table — don't duplicate per-subject
        df = pd.read_parquet(src, filters=[(pid_col, "in", pid_values)])
    except Exception:
        df = pd.read_parquet(src)
        if pid_col not in df.columns:
            return -1
        df = df[df[pid_col].isin(pid_values)].reset_index(drop=True)
    if len(df) == 0:
        return 0  # empty — don't write
    dst.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(dst, index=False)
    return len(df)


def copy_nonparquet(src: Path, dst: Path) -> None:
    """Copy small non-parquet metadata files only if at the top level.

    Skip anything inside @iXnY partition directories — those manifests describe
    per-partition data bounds that don't apply to a subject-scoped slice, and
    keeping them would leave empty partition dirs un-prunable.
    """
    if any(part.startswith("@i") and "n" in part for part in src.parts):
        return  # inside a partition dir — skip
    if src.stat().st_size > 100_000:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def prune_empty_dirs(root: Path) -> int:
    """Remove empty directories under root. Returns count removed."""
    removed = 0
    # Walk bottom-up: leaf dirs first
    for d in sorted([p for p in root.rglob("*") if p.is_dir()], key=lambda p: -len(p.parts)):
        try:
            d.rmdir()  # only succeeds if empty
            removed += 1
        except OSError:
            pass
    return removed


def build_subject(spec: dict) -> dict:
    """Build one Subject-*/ folder. Returns summary dict."""
    group_dir = USER_STORE / f"UserGroup-{spec['dataset_tag']}"
    folder = group_dir / f"Subject-{spec['subject_id']}"
    folder.mkdir(parents=True, exist_ok=True)

    manifest_path = folder / "manifest.yaml"
    if manifest_path.exists():
        try:
            with open(manifest_path) as f:
                existing = yaml.safe_load(f)
            built_at = dt.datetime.fromisoformat(existing.get("built_at", ""))
            if (dt.datetime.now() - built_at).total_seconds() < 3600:
                return {"status": "skipped_fresh", "folder": str(folder)}
        except Exception:
            pass

    # 0-RawDataStore: flat — just the raw file names, no cohort/train/test nesting
    raw_out = folder / "0-RawDataStore"
    raw_files_copied = 0
    if spec.get("raw_copy") and spec.get("raw_paths"):
        raw_out.mkdir(exist_ok=True)
        for p in spec["raw_paths"]:
            if p.is_file():
                dst = raw_out / p.name  # flat
                shutil.copy2(p, dst)
                raw_files_copied += 1

    # 1-SourceStore: flat — strip source_set wrapper dirs
    source_in = WORKSPACE / "1-SourceStore" / spec["source_set"]
    source_out = folder / "1-SourceStore"
    source_files, source_rows, source_skipped = 0, 0, 0
    for src in source_in.rglob("*"):
        if src.is_file():
            rel = flatten_rel(src.relative_to(source_in))
            dst = source_out / rel
            if dst.exists():  # de-dup (e.g. partition vs top-level)
                continue
            if src.suffix == ".parquet":
                n = filter_parquet(src, dst, spec["pid_column"], spec["pid_values"])
                if n > 0:
                    source_rows += n; source_files += 1
                else:
                    source_skipped += 1
            else:
                copy_nonparquet(src, dst)

    # 2-RecStore: flat — strip rec_set wrapper + partition (@iXnY) segments
    rec_in = WORKSPACE / "2-RecStore" / spec["rec_set"]
    rec_out = folder / "2-RecStore"
    rec_files, rec_rows, rec_skipped = 0, 0, 0
    partition_seen = set()
    if rec_in.exists():
        for src in rec_in.rglob("*"):
            if src.is_file():
                rel_raw = src.relative_to(rec_in)
                # Record which partition this file came from (for manifest)
                for part in rel_raw.parts:
                    if part.startswith("@i") and "n" in part:
                        partition_seen.add(part)
                rel = flatten_rel(rel_raw)
                dst = rec_out / rel
                if dst.exists():
                    continue
                if src.suffix == ".parquet":
                    n = filter_parquet(src, dst, spec["pid_column"], spec["pid_values"])
                    if n > 0:
                        rec_rows += n; rec_files += 1
                    else:
                        rec_skipped += 1
                else:
                    copy_nonparquet(src, dst)

    pruned = prune_empty_dirs(folder)

    manifest = {
        "subject_id": spec["subject_id"],
        "dataset": spec["dataset"],
        "dataset_tag": spec["dataset_tag"],
        "source_raw_paths": [str(p) for p in spec.get("raw_paths", [])],
        "raw_materialized": bool(spec.get("raw_copy")),
        "source_set": spec["source_set"],
        "rec_set": spec["rec_set"],
        "pid_column": spec["pid_column"],
        "pid_values": spec["pid_values"],
        "built_at": dt.datetime.now().isoformat(timespec="seconds"),
        "built_by": BUILDER_VERSION,
        "build_args": {
            "raw_files_copied": raw_files_copied,
            "source_files": source_files, "source_rows": source_rows,
            "source_skipped": source_skipped,
            "rec_files": rec_files, "rec_rows": rec_rows,
            "rec_skipped": rec_skipped,
            "rec_partitions_found_in": sorted(partition_seen),
            "empty_dirs_pruned": pruned,
        },
    }
    with open(manifest_path, "w") as f:
        yaml.safe_dump(manifest, f, sort_keys=False)

    return {
        "status": "built", "folder": str(folder),
        "raw_files": raw_files_copied,
        "source_files": source_files, "source_rows": source_rows,
        "rec_files": rec_files, "rec_rows": rec_rows,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset", nargs="?")
    ap.add_argument("subject_ids", nargs="*")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    datasets = list(BUILDERS.keys()) if args.all else ([args.dataset] if args.dataset else [])
    if not datasets:
        ap.print_help(); sys.exit(1)

    USER_STORE.mkdir(parents=True, exist_ok=True)

    summary = []
    for ds in datasets:
        if ds not in BUILDERS:
            print(f"SKIP: no builder for {ds}"); continue
        builder = BUILDERS[ds]
        ids = args.subject_ids if (args.subject_ids and not args.all) else list_candidates(ds, args.n)
        print(f"\n=== {ds} — building {len(ids)} subjects: {ids} ===")
        for sid in ids:
            try:
                spec = builder(sid)
                result = build_subject(spec)
                tag = f"  Subject-{sid}: {result['status']}"
                if result["status"] == "built":
                    tag += f"  (raw={result['raw_files']}, src_rows={result['source_rows']}, rec_rows={result['rec_rows']})"
                print(tag)
                summary.append({"dataset": ds, "subject_id": sid, **result})
            except Exception as e:
                print(f"  Subject-{sid}: ERROR {e}")
                summary.append({"dataset": ds, "subject_id": sid, "status": "error", "error": str(e)})

    print("\n=== Summary ===")
    for s in summary:
        print(f"  {s['dataset']}:{s['subject_id']} → {s['status']}")


if __name__ == "__main__":
    main()

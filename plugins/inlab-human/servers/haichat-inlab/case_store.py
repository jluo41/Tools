"""case_store — a dataset's cooked cases, read from a haipipe case store (the Case view's source).

A case is one trigger moment cut from one human's record, with the facets its CaseFns computed: the unit a
score or a label attaches to. The haipipe Case stage writes them (`CaseSet._save_data_to_disk`):

    <INLAB_CASE_STORE>/<record_set>/[@i<k>n<n>/]@v<k>CaseSet-<Trigger>/manifest.json   trigger_info · casefn_info
                                                                      df_case.parquet     one row per case
                                                                      @<CaseFn>.parquet   that CaseFn's columns,
                                                                                          row for row with df_case

A dataset's case sets are the ones under its own name. Nothing here names a table, a column or a CaseFn:
the human id column is the one df_case shares with every CaseFn file, the case time is df_case's timestamp
column (by type), and each facet is shown by its shape (a list is summarised, a scalar shown).
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

_SET = re.compile(r"^@v\d+CaseSet-(.+)$")
_PART = re.compile(r"^@i\d+n\d+$")


def case_sets(dataset: str) -> list[Path]:
    """Every case set of a dataset, under INLAB_CASE_STORE/<dataset>/ (partitions included)."""
    root = os.environ.get("INLAB_CASE_STORE")
    if not root:
        return []
    base = Path(root).expanduser() / dataset
    if not base.is_dir():
        return []
    out = []
    for d in sorted(base.iterdir()):
        if _SET.match(d.name) and (d / "df_case.parquet").is_file():
            out.append(d)
        elif _PART.match(d.name):
            out += [s for s in sorted(d.iterdir()) if _SET.match(s.name) and (s / "df_case.parquet").is_file()]
    return out


def _facet(v: Any) -> str:
    if isinstance(v, (list, tuple)):
        nums = [x for x in v if isinstance(x, (int, float)) and x == x]
        if nums:
            return f"{len(v)} values · {min(nums):g} to {max(nums):g}"
        return f"{len(v)} items"
    if isinstance(v, float):
        return f"{v:g}"
    return str(v)[:60]


def _plain(v: Any) -> Any:
    if hasattr(v, "isoformat") and not isinstance(v, str):
        return (v.isoformat(sep=" ") if hasattr(v, "hour") else v.isoformat())[:19]
    return v


def read_cases(folder: Path, human_id: str | None, limit: int) -> tuple[list[dict[str, Any]], int]:
    """(cases, number of humans) from one case set; one human's cases when human_id is given."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    manifest = json.loads((folder / "manifest.json").read_text()) if (folder / "manifest.json").is_file() else {}
    trigger = (manifest.get("trigger_info") or {}).get("TriggerName") or _SET.match(folder.name).group(1)
    base = pq.read_table(folder / "df_case.parquet")
    fn_files = sorted(folder.glob("@*.parquet"))
    fn_cols = [set(pq.read_schema(f).names) for f in fn_files]
    id_col = next((c for c in base.column_names if all(c in fc for fc in fn_cols)), base.column_names[0])
    t_col = next((n for n, t in zip(base.schema.names, base.schema.types)
                  if pa.types.is_timestamp(t) or pa.types.is_date(t)), None)
    ids = [str(v) for v in base.column(id_col).to_pylist()]
    keep = [i for i, v in enumerate(ids) if human_id is None or v == human_id][: max(1, min(limit, 500))]
    rows = base.to_pylist()
    facets: list[dict[str, str]] = [{} for _ in keep]
    for f in fn_files:
        t = pq.read_table(f).to_pylist()
        name = f.stem[1:]
        for j, i in enumerate(keep):
            for k, v in t[i].items():
                if k != id_col:
                    facets[j][k.replace(f"{name}--", f"{name} · ")] = _facet(v)
    out = []
    for j, i in enumerate(keep):
        r = {k: _plain(v) for k, v in rows[i].items()}
        when = r.get(t_col) if t_col else None
        meta = {k: v for k, v in r.items() if k not in (id_col, t_col) and isinstance(v, (int, float, str))
                and len(str(v)) <= 40}
        out.append({"id": f"{ids[i]}@{when or i}", "text": f"{trigger} at {when}" if when else trigger,
                    "human_id": ids[i], "stream": trigger, "when": when, "meta": meta,
                    "facets": facets[j], "annotations": {}})
    return out, len(set(ids))

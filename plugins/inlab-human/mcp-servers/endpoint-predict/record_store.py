"""record_store — read one human straight from a haipipe record store, in the patient-json shape.

The console's patient store used to be a COPY: a build step flattened each RecordSet into one json per
human (`<dataset>/patients/<human>.json`). That copy can go stale and is one more copy of patient data to
secure. This reader serves the same shape per request from the record store itself (j02 Q02, decided
261009: read in place; the json copy stays as the fallback when no record store is mounted).

The layout it reads is the one the haipipe Record stage writes (`RecordSet._save_data_to_disk`):

    <INLAB_RECORD_STORE>/<record_set>/[@i<k>n<n>/]manifest.json      structure.humans · structure.records
                                     Human-<HumanName>/Human2RawNum.parquet
                                     Record-<HumanName>.<RecordName>/RecAttr.parquet

What it builds for one human, the keys the engine and the console read:

    source_tables   {table: [row, ...]}  each Record's rows, its id-chain columns dropped, named after the
                    Record with its time grain cut off (<Name>5Min → <Name>); INLAB_RECORD_TABLE_NAMES
                    ({"<RecordName>": "<table>"}) renames any other
    layers.record   {"Rec.<RecordName>": {columns, n_rows, rows}}  the Record rows as stored
    summary         cohort (the source set's cohort or name), sex and birth date when a one-row Record
                    carries them, table_counts, anchor (the latest time in any Record; a Record's time
                    columns are its timestamp and date columns, by type: no table or column is named)
    provenance      every endpoint whose required tables this human carries, triggered at the anchor;
                    the record store does not know which endpoints scored whom, so this says who CAN

No raw layer: the files as they arrived live in the raw store, not here, and the Raw view says so.
Reads with pyarrow, filtered to one human per request; a small per-process cache keeps a chart's several
requests to one read.
"""
from __future__ import annotations

import copy
import json
import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable

_GRAIN = re.compile(r"(\d*(?:Min|Hour|Day|Week|Month|H|D))$")
_PART = re.compile(r"^@i\d+n\d+$")


def _table_name(record: str) -> str:
    renames = {}
    raw = os.environ.get("INLAB_RECORD_TABLE_NAMES")
    if raw:
        try:
            renames = json.loads(raw)
        except Exception:  # noqa: BLE001 — a malformed env var is not a crash
            renames = {}
    if record in renames:
        return renames[record]
    cut = _GRAIN.sub("", record)
    return cut or record


def record_sets(root: str | Path) -> dict[str, Path]:
    """{record_set name: its folder} for every record set under a record store."""
    root = Path(os.path.expanduser(str(root)))
    out: dict[str, Path] = {}
    if not root.is_dir():
        return out
    for d in sorted(root.iterdir()):
        if (d / "manifest.json").is_file() or any(_PART.match(p.name) for p in d.iterdir() if p.is_dir()):
            out[d.name] = d
    return out


class RecordSetReader:
    """One record set, read in place. `parts` are the set's partitions (or the set itself)."""

    def __init__(self, folder: str | Path):
        self.folder = Path(folder)
        self.name = self.folder.name
        if (self.folder / "manifest.json").is_file():
            self.parts = [self.folder]
        else:
            self.parts = sorted(p for p in self.folder.iterdir() if _PART.match(p.name)
                                and (p / "manifest.json").is_file())
        if not self.parts:
            raise ValueError(f"{self.name}: no manifest.json (not a record set)")
        self.manifest = json.loads((self.parts[0] / "manifest.json").read_text())
        st = self.manifest.get("structure") or {}
        self.humans: list[str] = list(st.get("humans") or [])
        self.records: list[tuple[str, str]] = [tuple(r) for r in (st.get("records") or [])]
        src = self.manifest.get("source_set_manifest") or {}
        self.cohort = (src.get("cohort") or src.get("source_name") or self.name) if isinstance(src, dict) \
            else self.name

    # ── who is in it ─────────────────────────────────────────────────────────
    def _id_col(self, human: str) -> str:
        """The HumanID column: the first column of Human2RawNum that every Record of that Human carries."""
        import pyarrow.parquet as pq
        cols = pq.read_schema(self.parts[0] / f"Human-{human}" / "Human2RawNum.parquet").names
        rec_cols = [set(pq.read_schema(p / f"Record-{h}.{r}" / "RecAttr.parquet").names)
                    for p in self.parts[:1] for h, r in self.records if h == human
                    if (p / f"Record-{h}.{r}" / "RecAttr.parquet").is_file()]
        for c in cols:
            if all(c in rc for rc in rec_cols):
                return c
        return cols[0]

    def ids(self) -> list[str]:
        import pyarrow.parquet as pq
        out: list[str] = []
        for human in self.humans:
            col = self._id_col(human)
            for p in self.parts:
                f = p / f"Human-{human}" / "Human2RawNum.parquet"
                if f.is_file():
                    out += [str(v) for v in pq.read_table(f, columns=[col]).column(col).to_pylist()]
        return sorted(set(out))

    # ── one human ────────────────────────────────────────────────────────────
    def _rows(self, human: str, record: str, col: str, pid: str) -> tuple[list[dict[str, Any]], list[str]]:
        """One human's rows of one Record, and its time columns (a timestamp or date in the parquet types:
        no column name is assumed)."""
        import pyarrow as pa
        import pyarrow.parquet as pq
        rows: list[dict[str, Any]] = []
        tcols: list[str] = []
        for p in self.parts:
            f = p / f"Record-{human}.{record}" / "RecAttr.parquet"
            if not f.is_file():
                continue
            schema = pq.read_schema(f)
            tcols = tcols or [n for n, t in zip(schema.names, schema.types)
                              if pa.types.is_timestamp(t) or pa.types.is_date(t)]
            t = pq.read_table(f, filters=[(col, "==", pid)])
            if t.num_rows == 0:
                try:                                        # an id stored as a number
                    t = pq.read_table(f, filters=[(col, "==", int(pid))])
                except (ValueError, TypeError):
                    pass
            rows += t.to_pylist()
        return [{k: _plain(v) for k, v in r.items() if not k.startswith("__index_level")} for r in rows], tcols

    def patient(self, pid: str, endpoint_tables: Callable[[], dict[str, list[str]]] | None = None
                ) -> dict[str, Any]:
        eps = endpoint_tables() if endpoint_tables else {}
        key = tuple(sorted((k, tuple(v)) for k, v in eps.items()))     # hashable, for the cache
        return copy.deepcopy(_patient(str(self.folder), self._stamp(), pid, key))

    def _stamp(self) -> float:
        return max((p / "manifest.json").stat().st_mtime for p in self.parts)

    def build(self, pid: str, endpoints: dict[str, list[str]]) -> dict[str, Any]:
        source: dict[str, list[dict[str, Any]]] = {}
        record: dict[str, dict[str, Any]] = {}
        profile: dict[str, Any] = {}
        times: list[str] = []
        for human in self.humans:
            col = self._id_col(human)
            for h, r in self.records:
                if h != human:
                    continue
                rows, tcols = self._rows(h, r, col, pid)
                if not rows:
                    continue
                cols = list(rows[0].keys())
                record[f"Rec.{r}"] = {"columns": cols, "n_rows": len(rows), "rows": rows}
                keep = [c for c in cols if c not in (col, f"{r}ID")]     # the id chain is the store's, not data
                source[_table_name(r)] = [{c: row.get(c) for c in keep} for row in rows]
                if len(rows) == 1:
                    profile.update(rows[0])
                times += [str(row[c]) for row in rows for c in tcols if row.get(c)]
        if not record:
            raise ValueError(f"unknown patient: {pid}")
        anchor = max(times) if times else None
        summary = {"cohort": self.cohort, **_demographics(profile),
                   "table_counts": {t: len(v) for t, v in source.items()}}
        if anchor:
            summary["anchor"] = anchor
        provenance = [{"endpoint_package": pkg, "triggers": [{"PID": pid, "ObsDT": anchor}]}
                      for pkg, need in endpoints.items() if anchor and need and set(need) <= set(source)]
        if not provenance:
            summary["not_scoreable_reason"] = "no mounted endpoint takes the tables this human carries"
        return {"patient_id": pid, "summary": summary, "provenance": provenance,
                "source_tables": source, "layers": {"record": {"tables": record}},
                "_read_from": f"record store · {self.name}"}


def _demographics(profile: dict[str, Any]) -> dict[str, Any]:
    """The patient card's three fields (sex, birth date, race), from a one-row Record when it has them:
    matched on the meaning of the column name, whatever the dataset calls it; absent stays None."""
    low = {k.lower().replace("_", ""): v for k, v in profile.items() if v not in (None, "")}
    sex = next((low[k] for k in ("sex", "gender") if k in low), None)
    birth = next((str(low[k])[:10] for k in ("birthdate", "dob", "dateofbirth") if k in low), None)
    if birth is None and "birthyear" in low:
        birth = f"{int(low['birthyear'])}-01-01"
    race = low.get("race")
    return {"birth_date": birth, "sex": sex, "race": race}


def _plain(v: Any) -> Any:
    """pyarrow hands back datetimes and decimals; the patient json carries strings and numbers."""
    if hasattr(v, "isoformat") and not isinstance(v, str):
        s = v.isoformat(sep=" ") if hasattr(v, "hour") else v.isoformat()
        return s[:19]
    if isinstance(v, float) and v != v:
        return None
    return v


@lru_cache(maxsize=64)
def _patient(folder: str, stamp: float, pid: str, endpoints: tuple) -> dict[str, Any]:
    return RecordSetReader(folder).build(pid, {k: list(v) for k, v in endpoints})

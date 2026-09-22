"""Subjective-labeling REST layer — cases and the PI's adjudication surface.

The console's ACTION story: the AI panel labels, the researcher ADJUDICATES.
This router serves, read-only, the artifacts a subjective-label project already
produces on disk (see Tools/plugins/subjective-label) — guideline versions,
gallery, trajectory, state — plus the case universe those labels attach to.
The ONLY write is the researcher's own decision, appended to an audit file the
panel never touches (human_decisions.jsonl).

A CASE is one annotation point: one text unit cut from one human's record (a
review, a conversation). The sl corpus items ARE cases — each carries the
human key (npi) — so the Case view can show "this human's annotation points"
and the Annotate view can show "what needs the PI's decision".

Configuration, by environment like everything else in this service:

    INLAB_LABEL_STORE   dir containing subjective-label dimension folders
                        (each has guideline/ + gallery/ + .state.json), e.g.
                        .../Project-Subjective-Label/tasks

Unset ⇒ the routes answer honestly that no label store is mounted; the
console stays usable without one.
"""
from __future__ import annotations

import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api")


# ── store discovery ──────────────────────────────────────────────────────────

def _stores_map() -> dict[str, str]:
    """Per-dataset label stores: INLAB_LABEL_STORES = {"<dataset>": "<dir>", …}.
    This is what makes labeling follow the dataset picker — each data type has
    its own labeling project (or none)."""
    raw = os.environ.get("INLAB_LABEL_STORES")
    if not raw:
        return {}
    try:
        m = json.loads(raw)
        return {str(k): str(v) for k, v in m.items()} if isinstance(m, dict) else {}
    except Exception:  # noqa: BLE001
        return {}


def _store(dataset: str | None = None) -> Path | None:
    """Resolve the label store for the active dataset.

    If a per-dataset map is set (INLAB_LABEL_STORES) it is AUTHORITATIVE: a
    dataset absent from the map has no labeling (returns None) — so picking
    ACIBench no longer shows PhyReview's dimensions. Falls back to the single
    INLAB_LABEL_STORE (legacy: applies to every dataset) when no map is set."""
    m = _stores_map()
    if m:
        path = m.get(dataset or "")
        if not path:
            return None
        p = Path(path).expanduser().resolve()
        return p if p.is_dir() else None
    env = os.environ.get("INLAB_LABEL_STORE")
    if not env:
        return None
    p = Path(env).expanduser().resolve()
    return p if p.is_dir() else None


def _is_dim(p: Path) -> bool:
    """A dimension folder: the sl plugin has worked in it, or at least scaffolded
    it (config + guideline/gallery dirs — a fresh dimension shows as such rather
    than being invisible)."""
    if not p.is_dir():
        return False
    if (
        (p / "guideline" / "guideline.md").exists()
        or (p / "gallery" / "gallery.json").exists()
        or (p / ".state.json").exists()
    ):
        return True
    return (p / "config.yaml").exists() and (
        (p / "guideline").is_dir() or (p / "gallery").is_dir()
    )


def _dims(dataset: str | None = None) -> list[Path]:
    root = _store(dataset)
    if not root:
        return []
    if _is_dim(root):
        return [root]
    return sorted(p for p in root.iterdir() if _is_dim(p))


def _dim_path(dim: str, dataset: str | None = None) -> Path | None:
    for p in _dims(dataset):
        if p.name == dim:
            return p
    return None


# ── tolerant readers (the store is data, not code — never 500 on a quirk) ────

def _jload(p: Path) -> Any:
    try:
        return json.loads(p.read_text())
    except Exception:  # noqa: BLE001
        return None


def _jsonl(p: Path) -> list[dict]:
    out: list[dict] = []
    try:
        for line in p.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except Exception:  # noqa: BLE001
                continue
    except Exception:  # noqa: BLE001
        pass
    return out


def _config(dim_dir: Path) -> dict:
    """config.yaml, needed for `topic` and `corpus.path` only. Real yaml if
    available; otherwise a tolerant two-field line parse."""
    p = dim_dir / "config.yaml"
    if not p.exists():
        return {}
    text = p.read_text()
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text) or {}
    except Exception:  # noqa: BLE001
        cfg: dict[str, Any] = {}
        m = re.search(r'^topic:\s*"?(.+?)"?\s*$', text, re.M)
        if m:
            cfg["topic"] = m.group(1)
        m = re.search(r'^corpus:\s*\n(?:.*\n)*?\s+path:\s*"?(.+?)"?\s*$', text, re.M)
        if m:
            cfg["corpus"] = {"path": m.group(1)}
        return cfg


# ── the corpus = the case universe ───────────────────────────────────────────

_corpus_cache: dict[str, tuple[float, list[dict]]] = {}


def _corpus_path(dim_dir: Path) -> Path | None:
    rel = ((_config(dim_dir).get("corpus") or {}).get("path")) or ""
    if not rel:
        return None
    p = (dim_dir / rel).resolve()
    return p if p.exists() else None


# ── corpora = the selectable labeling universe (between cases and dimensions) ─
#
# A corpus is a materialized jsonl of cases (e.g. A01_sample_corpus/results/
# sample_init.jsonl). A DIMENSION (B0x_dim_*) binds to one via config.yaml's
# corpus.path — several dims can share a corpus. The console's Annotate tab lets
# you SELECT a corpus, then a dimension on it; so we surface the corpus set by
# (a) what the dims reference and (b) any A-task results jsonl not yet labeled.

def _corpus_id(root: Path, p: Path) -> str:
    """A stable id for a corpus: its path relative to the store when it lives
    under it (the A-task convention), else the absolute path."""
    try:
        return str(p.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(p.resolve())


def _corpus_meta(dim_dir: Path) -> dict:
    cfg = _config(dim_dir).get("corpus") or {}
    return {
        "path": _corpus_path(dim_dir),
        "text_field": cfg.get("text_field"),
        "id_field": cfg.get("id_field"),
        "n_items": cfg.get("n_items"),
    }


def _count_lines(p: Path, cap: int = 200_000) -> int | None:
    try:
        if p.stat().st_size > 80_000_000:      # too big to walk cheaply
            return None
        n = 0
        with open(p) as f:
            for _ in f:
                n += 1
                if n >= cap:
                    break
        return n
    except Exception:  # noqa: BLE001
        return None


def _list_corpora(dataset: str | None = None) -> list[dict]:
    """Every corpus in the store, each with the dimensions bound to it."""
    root = _store(dataset)
    if not root:
        return []
    corpora: dict[str, dict] = {}

    def ensure(p: Path) -> dict:
        cid = _corpus_id(root, p)
        return corpora.setdefault(cid, {
            "id": cid, "name": p.stem, "path": str(p), "task": None,
            "text_field": None, "n_items": None, "profile": None, "dims": [],
        })

    # (a) corpora the dimensions reference
    for d in _dims(dataset):
        cm = _corpus_meta(d)
        p = cm["path"]
        if p and p.exists():
            c = ensure(p)
            c["dims"].append(d.name)
            c["text_field"] = c["text_field"] or cm["text_field"]
            c["n_items"] = c["n_items"] or cm["n_items"]

    # (b) A-task outputs not (yet) bound to any dimension — freshly built corpora
    for res in root.glob("*/results/*.jsonl"):
        ensure(res)

    # enrich: the generating task folder + its profile sidecar + a count fallback
    for c in corpora.values():
        p = Path(c["path"])
        for anc in p.parents:
            if anc.parent == root:
                c["task"] = anc.name
                break
        prof = p.parent / "sample_profile.md"
        if prof.exists():
            try:
                c["profile"] = prof.read_text()[:1200]
            except Exception:  # noqa: BLE001
                pass
        if not c["n_items"]:
            c["n_items"] = _count_lines(p)

    return sorted(corpora.values(), key=lambda x: x["id"])


def _corpus(p: Path) -> list[dict]:
    key = str(p)
    mtime = p.stat().st_mtime
    hit = _corpus_cache.get(key)
    if hit and hit[0] == mtime:
        return hit[1]
    items = _jsonl(p)
    _corpus_cache[key] = (mtime, items)
    return items


# ── per-dimension artifacts ──────────────────────────────────────────────────

def _gallery(dim_dir: Path) -> dict:
    return _jload(dim_dir / "gallery" / "gallery.json") or {}


def _gallery_by_id(dim_dir: Path) -> dict[str, dict]:
    return {i["id"]: i for i in _gallery(dim_dir).get("items", []) if i.get("id")}


def _batches(dim_dir: Path) -> dict[str, dict]:
    """Every iterNN/batch.jsonl item, keyed by case id."""
    out: dict[str, dict] = {}
    for it in sorted(dim_dir.glob("iter*/batch.jsonl")):
        for row in _jsonl(it):
            if row.get("id"):
                out[row["id"]] = {**row, "iter": it.parent.name}
    return out


def _labels_of(dim_dir: Path) -> list[str]:
    """The label schema, read off the gallery (the canonical artifact)."""
    seen: list[str] = []
    for i in _gallery(dim_dir).get("items", []):
        lb = i.get("label")
        if lb and lb not in seen:
            seen.append(lb)
    return seen


def _guideline_versions(dim_dir: Path) -> list[str]:
    vdir = dim_dir / "guideline" / "versions"
    if not vdir.is_dir():
        return []
    return sorted(p.stem for p in vdir.glob("v*.md"))


def _decisions(dim_dir: Path) -> list[dict]:
    return _jsonl(dim_dir / "human_decisions.jsonl")


def _summary(dim_dir: Path, root: Path | None = None) -> dict:
    state = _jload(dim_dir / ".state.json") or {}
    traj = state.get("trajectory") or []
    latest = traj[-1] if traj else {}
    cm = _corpus_meta(dim_dir)
    corpus_id = None
    if cm["path"]:
        corpus_id = _corpus_id(root, cm["path"]) if root else str(cm["path"])
    return {
        "dim": dim_dir.name,
        "topic": _config(dim_dir).get("topic"),
        "status": state.get("status", "uninitialized"),
        "iteration": state.get("iteration"),
        "guideline_version": state.get("guideline_version"),
        "gallery_size": state.get("gallery_size", len(_gallery(dim_dir).get("items", []))),
        "labels": _labels_of(dim_dir),
        "kappa": latest.get("kappa"),
        "next": state.get("next"),
        # which corpus this dimension is bound to — the Annotate tab groups by it
        "corpus": corpus_id,
        "corpus_name": cm["path"].stem if cm["path"] else None,
    }


# ── routes ───────────────────────────────────────────────────────────────────

@router.get("/labeling/dimensions")
def labeling_dimensions(dataset: str | None = None):
    root = _store(dataset)
    if not root:
        return JSONResponse({
            "store": None,
            "dataset": dataset,
            "dimensions": [],
            "reason": (f"no labeling project for dataset '{dataset}'." if dataset
                       else "no label store mounted.")
                      + " Set INLAB_LABEL_STORES = {\"<dataset>\": \"<tasks dir>\"} "
                        "to link a subjective-label project to this data type.",
        })
    return JSONResponse({
        "store": str(root), "dataset": dataset,
        "dimensions": [_summary(p, root) for p in _dims(dataset)],
    })


@router.get("/labeling/corpora")
def labeling_corpora(dataset: str | None = None):
    """The selectable corpora for this dataset — one per built labeling universe,
    each carrying the dimensions bound to it. This is the layer BETWEEN cases and
    labeling: you pick a corpus, then a dimension on it."""
    root = _store(dataset)
    if not root:
        return JSONResponse({
            "store": None, "dataset": dataset, "corpora": [],
            "reason": (f"no labeling project for dataset '{dataset}'." if dataset
                       else "no label store mounted.")
                      + " A corpus is built from this dataset's cases (an A-task "
                        "sample), then dimensions are labeled on it.",
        })
    return JSONResponse({
        "store": str(root), "dataset": dataset,
        "corpora": _list_corpora(dataset),
    })


@router.get("/labeling/{dim}")
def labeling_detail(dim: str, dataset: str | None = None):
    d = _dim_path(dim, dataset)
    if not d:
        return JSONResponse({"error": f"unknown dimension: {dim}"}, status_code=404)

    state = _jload(d / ".state.json") or {}
    decisions = _decisions(d)
    decided = {x.get("case_ref") for x in decisions}

    # The PI's inbox: what the sl loop itself says is unresolved. Residual hard
    # cases live in state; a full /sl-iterate would add its A/B/C asks here.
    inbox = [
        {"kind": "residual", "case_ref": ref, "ask": "adjudicate", "resolved": ref in decided}
        for ref in state.get("residual_hard_cases", [])
    ]
    nxt = state.get("next")
    if nxt:
        inbox.append({"kind": "next-step", "case_ref": nxt, "ask": "run", "resolved": False})

    traj = _jsonl(d / "eval" / "trajectory.jsonl") or state.get("trajectory") or []

    guideline_md = ""
    gpath = d / "guideline" / "guideline.md"
    if gpath.exists():
        guideline_md = gpath.read_text()

    changelog = ""
    cpath = d / "guideline" / "changelog.md"
    if cpath.exists():
        changelog = cpath.read_text()

    return JSONResponse({
        **_summary(d),
        "state": state,
        "guideline": {
            "current": f"v{state.get('guideline_version'):02d}" if state.get("guideline_version") else None,
            "versions": _guideline_versions(d),
            "text": guideline_md,
        },
        "changelog": changelog,
        "trajectory": traj,
        "gallery": _gallery(d),
        "inbox": inbox,
        "decisions": decisions,
    })


@router.get("/labeling/{dim}/guideline/{version}")
def labeling_guideline_version(dim: str, version: str, dataset: str | None = None):
    d = _dim_path(dim, dataset)
    if not d:
        return JSONResponse({"error": f"unknown dimension: {dim}"}, status_code=404)
    if not re.fullmatch(r"v\d{2}", version):
        return JSONResponse({"error": f"bad version: {version}"}, status_code=400)
    p = d / "guideline" / "versions" / f"{version}.md"
    if not p.exists():
        return JSONResponse({"error": f"no such version: {version}"}, status_code=404)
    return JSONResponse({"dim": dim, "version": version, "text": p.read_text()})


@router.post("/labeling/{dim}/decision")
def labeling_decision(dim: str, body: dict[str, Any]):
    """The one write: the researcher's adjudication, appended to an audit file
    of its own. The panel's artifacts (gallery, guideline) are NEVER touched
    here — folding a decision into the gallery is the gallery-keeper's job,
    through the sl loop."""
    d = _dim_path(dim, (body or {}).get("dataset"))
    if not d:
        return JSONResponse({"error": f"unknown dimension: {dim}"}, status_code=404)
    case_ref = (body.get("case_ref") or "").strip()
    decision = (body.get("decision") or "").strip()
    if not case_ref or not decision:
        return JSONResponse({"error": "case_ref and decision are required"}, status_code=400)
    rec = {
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "origin": body.get("origin") or "inlab-console",
        "case_ref": case_ref,
        "ask": body.get("ask") or "adjudicate",
        "decision": decision,
        "note": body.get("note") or "",
    }
    with open(d / "human_decisions.jsonl", "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return JSONResponse({"ok": True, "decision": rec})


# ── cases from the record (data-type driven) ─────────────────────────────────
#
# A case = one annotation/prediction point sliced from ONE human's record. The
# unit is data-type specific: an ACIBench encounter is a doctor↔patient dialogue,
# a physician-review case is one review, a MIMIC case is a prediction window. So
# cases come from the SELECTED DATASET's record — not from a fixed corpus — and
# the labeling gallery is joined on as an overlay when a case id lines up.
# (Formalizing "which stream/column is the case" is the job of a CaseFn / a
# 3-CaseStore; until then we read it generically off the record streams.)

_TEXT_COLS = ["Dialogue", "Transcript", "ReviewText", "NoteFull", "Note",
              "text", "comment", "ChiefComplaint"]


def _row_text(row: dict) -> tuple[str | None, str]:
    """The row's case text: a known text column, else the longest string cell."""
    for c in _TEXT_COLS:
        v = row.get(c)
        if isinstance(v, str) and v.strip():
            return c, v
    best_c, best = None, ""
    for k, v in row.items():
        if isinstance(v, str) and len(v) > len(best):
            best_c, best = k, v
    return best_c, best


def _row_id(row: dict, stream: str, i: int) -> str:
    for k, v in row.items():
        if k.endswith("ID") and v not in (None, ""):
            return str(v)
    return f"{stream}:{i}"


def _row_meta(row: dict, text_col: str | None) -> dict:
    """Short scalar fields worth showing on the case card (not the text/ids/blobs)."""
    out: dict[str, Any] = {}
    for k, v in row.items():
        if k == text_col or k.endswith("ID") or k.endswith("metadata"):
            continue
        if isinstance(v, (int, float)) or (isinstance(v, str) and 0 < len(v) <= 40):
            out[k] = v
    return out


def _record_streams(rec: dict) -> dict[str, list[dict]]:
    """Every record stream as {stream: [row, ...]} — from the record layer if the
    patient JSON carries it, else from source_tables."""
    layers = ((rec.get("layers") or {}).get("record") or {}).get("tables")
    if isinstance(layers, dict):
        return {s: (t.get("rows") or []) for s, t in layers.items()}
    return {s: rows for s, rows in (rec.get("source_tables") or {}).items()
            if isinstance(rows, list)}


def _cases_from_records(pdir: Path, human_id: str | None, q: str | None, limit: int):
    """Cases sliced from the dataset's patient records. One human when human_id is
    given; otherwise a sample across the dataset's humans."""
    if human_id:
        files = [pdir / f"{human_id}.json"]
        files = [f for f in files if f.exists()]
    else:
        files = sorted(pdir.glob("*.json"))
    cap = max(1, min(limit, 500))

    out: list[dict] = []
    scanned = 0
    for f in files:
        if len(out) >= cap:
            break
        rec = _jload(f)
        if not isinstance(rec, dict):
            continue
        scanned += 1
        pid = rec.get("patient_id", f.stem)
        for stream, rows in _record_streams(rec).items():
            for i, row in enumerate(rows):
                if not isinstance(row, dict):
                    continue
                text_col, text = _row_text(row)
                if not text:
                    continue
                if q and q.lower() not in text.lower():
                    continue
                out.append({
                    "id": _row_id(row, stream, i),
                    "text": text,
                    "human_id": pid,
                    "stream": stream.replace("ACI", "").replace("HmACIPtt.", ""),
                    "meta": _row_meta(row, text_col),
                    "annotations": {},
                })
                if len(out) >= cap and human_id:
                    break
    return out, scanned


def _overlay_labels(cases: list[dict], dataset: str | None = None) -> list[str]:
    """Best-effort: join sl gallery/batch label history onto cases by exact id,
    using ONLY the labeling linked to this dataset. (ACIBench has no labeling
    project, so its cases get no overlay — which is correct.)"""
    dims = _dims(dataset)
    joins = {d.name: (_gallery_by_id(d), _batches(d)) for d in dims}
    for c in cases:
        for dname, (gal, bat) in joins.items():
            entry: dict[str, Any] = {}
            g = gal.get(c["id"])
            if g:
                entry["gallery"] = {k: g.get(k) for k in ("label", "difficulty", "reasoning", "added_iteration")}
            b = bat.get(c["id"])
            if b:
                entry["batch"] = {k: b.get(k) for k in ("gold", "probe", "iter")}
            if entry:
                c["annotations"][dname] = entry
    return [d.name for d in dims]


def _cases_from_corpus(human_id: str | None, q: str | None, limit: int,
                       dataset: str | None = None):
    """Fallback for a labeling-only launch (no patient store): browse the sl
    corpus itself as the case universe, review cards with label history."""
    dims = _dims(dataset)
    if not dims:
        return None
    corpora: dict[str, list[dict]] = {}
    for d in dims:
        p = _corpus_path(d)
        if p:
            corpora.setdefault(str(p), _corpus(p))
    universe: dict[str, dict] = {}
    for items in corpora.values():
        for it in items:
            if it.get("id"):
                universe.setdefault(it["id"], it)
    joins = {d.name: (_gallery_by_id(d), _batches(d)) for d in dims}

    want_digits = re.sub(r"\D", "", human_id) if human_id else ""
    matched: bool | None = None
    rows = list(universe.values())
    if want_digits:
        mine = [r for r in rows if re.sub(r"\D", "", str(r.get("npi", ""))) == want_digits]
        matched = bool(mine)
        if mine:
            rows = mine
    if q:
        needle = q.lower()
        rows = [r for r in rows if needle in str(r.get("text", "")).lower()
                or needle in str(r.get("physician_name", "")).lower()]
    annotated = set()
    for gal, bat in joins.values():
        annotated.update(gal)
        annotated.update(bat)
    rows.sort(key=lambda r: (r["id"] not in annotated, str(r["id"])))

    out = []
    for r in rows[: max(1, min(limit, 500))]:
        ann: dict[str, dict] = {}
        for dname, (gal, bat) in joins.items():
            entry: dict[str, Any] = {}
            g = gal.get(r["id"])
            if g:
                entry["gallery"] = {k: g.get(k) for k in ("label", "difficulty", "reasoning", "added_iteration")}
            b = bat.get(r["id"])
            if b:
                entry["batch"] = {k: b.get(k) for k in ("gold", "probe", "iter")}
            if entry:
                ann[dname] = entry
        out.append({
            "id": r.get("id"), "text": r.get("text"), "human_id": r.get("npi"),
            "stream": r.get("platform"), "meta": {"rating": r.get("rating_score"),
                "date": str(r.get("review_date") or "")[:10], "by": r.get("physician_name")},
            "annotations": ann,
        })
    return {"source": "corpus", "n_total": len(universe), "n_matched": len(rows),
            "matched": matched, "dims": [d.name for d in dims], "cases": out}


@router.get("/cases")
def cases(dataset: str | None = None, human_id: str | None = None,
          q: str | None = None, limit: int = 120):
    """Cases for the chosen data type. Record-driven when a patient store is
    mounted (one case per record row of the selected human); falls back to the
    labeling-corpus browse when the console is launched label-only."""
    t0 = time.time()
    try:
        from console_api import _datasets, _default_dataset
        ds = _datasets()
    except Exception:  # noqa: BLE001
        ds = {}

    if ds:
        name = dataset if dataset in ds else _default_dataset()
        pdir = Path(ds[name])
        if not pdir.is_dir():
            return JSONResponse({"source": "record", "dataset": name, "cases": [],
                                 "n_total": 0, "n_matched": 0, "matched": None,
                                 "reason": f"dataset '{name}' has no patient store on disk"})
        cases_out, scanned = _cases_from_records(pdir, human_id, q, limit)
        dims = _overlay_labels(cases_out, name)
        return JSONResponse({
            "source": "record", "dataset": name,
            "datasets": list(ds), "dims": dims,
            "n_total": len(sorted(pdir.glob("*.json"))),
            "n_matched": len(cases_out),
            "matched": (bool(cases_out) if human_id else None),
            "scanned_humans": scanned,
            "human_id": human_id,
            "elapsed_ms": int((time.time() - t0) * 1000),
            "cases": cases_out,
        })

    # no patient store at all — labeling-only launch
    corpus = _cases_from_corpus(human_id, q, limit, dataset)
    if corpus is None:
        return JSONResponse({
            "source": None, "cases": [], "n_total": 0, "matched": None,
            "reason": "no dataset (INLAB_DATASET_STORE / INLAB_PATIENT_STORE) and no "
                      "label store (INLAB_LABEL_STORE) mounted.",
        })
    corpus["store"] = str(_store(dataset))
    corpus["elapsed_ms"] = int((time.time() - t0) * 1000)
    return JSONResponse(corpus)

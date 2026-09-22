"""In-lab clinical model console — the portable REST layer.

This is the *deterministic* half of the console: click a patient, click a model,
get a score from the prediction endpoint. No LLM, no credentials, no agent. The
score is always produced by the endpoint; nothing here interprets it.

It is an APIRouter, not an app, so it can be mounted in two places without a fork:

  * `main.py` here          -> the standalone `haichat-inlab` service (iframe target,
                               embedded beside a HAI-Chat thread)
  * the D01 demo backend    -> the same routes, next to its Claude `/ws` bridge

All prediction logic lives in the inlab-human engine (an MCP server that doubles
as a library):

    Tools/plugins/inlab-human/mcp-servers/endpoint-predict/server.py

We import it rather than reimplement it — the agent and the buttons must reach the
endpoint through exactly the same code, or the demo is a lie.

Configuration is entirely by environment (no cohort is baked into this repo):

    INLAB_PATIENT_STORE   dir of <patient_id>.json records
    INLAB_ENDPOINT_STORE  dir of packaged endpoints (6-EndpointStore)
    INLAB_REGISTRY        json: {"<package>": "http://host:port", ...}
    INLAB_ENGINE          optional; path to the endpoint-predict dir. If unset we
                          use the plugin sibling ../../mcp-servers/endpoint-predict,
                          else walk up from this file looking for Tools/plugins/...
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse

ENGINE_REL = Path("Tools/plugins/inlab-human/mcp-servers/endpoint-predict")


def _resolve_engine() -> Path:
    env = os.environ.get("INLAB_ENGINE")
    if env:
        return Path(env).expanduser().resolve()
    # This folder lives inside the plugin (plugins/inlab-human/servers/haichat-inlab),
    # so the engine is a sibling two levels up.
    sibling = Path(__file__).resolve().parents[2] / "mcp-servers" / "endpoint-predict"
    if (sibling / "server.py").exists():
        return sibling
    # Walk up: works in-workspace (REACH-SPACE/Tools) and inside HAIChat-SPACE
    # (its own Tools submodule), without either repo hard-coding the other.
    for base in Path(__file__).resolve().parents:
        cand = base / ENGINE_REL
        if (cand / "server.py").exists():
            return cand
    raise RuntimeError(
        "inlab-human engine not found. Set INLAB_ENGINE to the endpoint-predict dir "
        f"(expected to find {ENGINE_REL}/server.py above {__file__})."
    )


ENGINE = _resolve_engine()
sys.path.insert(0, str(ENGINE))
import server as ep  # noqa: E402  — the MCP server module, used as a library

router = APIRouter(prefix="/api")


# ── datasets: several patient stores, one per data type ──────────────────────
#
# The engine reads ONE INLAB_PATIENT_STORE. A research console wants several —
# ACIBench conversations, MIMIC-IV timelines, physician reviews — and a picker
# to switch between them (a "data type" IS which RecordSet is active). We leave
# the shared engine untouched and, per request, point its module-level
# PATIENT_STORE at the chosen dataset's dir. Single-user local console: the
# reassignment window is a single sync call, so we accept the shared global.

def _datasets() -> dict[str, str]:
    """name -> patients dir. Resolution order:
    INLAB_DATASETS (json {name: dir}) > INLAB_DATASET_STORE (parent dir, each
    <name>/patients autodiscovered) > INLAB_PATIENT_STORE (single, back-compat)."""
    raw = os.environ.get("INLAB_DATASETS")
    if raw:
        try:
            d = json.loads(raw)
            out = {k: os.path.expanduser(v) for k, v in d.items() if v}
            if out:
                return out
        except Exception:  # noqa: BLE001 — a malformed env var is not a crash
            pass
    parent = os.environ.get("INLAB_DATASET_STORE")
    if parent:
        root = Path(os.path.expanduser(parent))
        out = {}
        if root.is_dir():
            for sub in sorted(root.iterdir()):
                pdir = sub / "patients"
                if pdir.is_dir():
                    out[sub.name] = str(pdir)
        if out:
            return out
    single = os.environ.get("INLAB_PATIENT_STORE")
    if single:
        # named after the folder ABOVE patients/, so ".../ACIBench_v0/patients"
        # shows as "ACIBench_v0" rather than "patients"
        name = Path(single).parent.name or "default"
        return {name: os.path.expanduser(single)}
    return {}


def _default_dataset() -> str | None:
    return next(iter(_datasets()), None)


def _scope(dataset: str | None) -> str | None:
    """Point the engine at the requested dataset (or the default). Returns the
    resolved name, or None when no dataset is configured (then the engine keeps
    whatever INLAB_PATIENT_STORE it booted with)."""
    ds = _datasets()
    if not ds:
        return None
    name = dataset if dataset in ds else _default_dataset()
    ep.PATIENT_STORE = ds[name]
    return name


@router.get("/datasets")
def datasets():
    """The data types this console can show — each a patient store (one RecordSet
    cooked into per-human JSONs). The topbar selector reads this."""
    out = []
    for name, pdir in _datasets().items():
        p = Path(pdir)
        files = sorted(p.glob("*.json")) if p.is_dir() else []
        cohort = None
        if files:
            try:
                cohort = (json.loads(files[0].read_text()).get("summary") or {}).get("cohort")
            except Exception:  # noqa: BLE001
                pass
        out.append({"name": name, "n_patients": len(files), "cohort": cohort})
    return JSONResponse({"datasets": out, "default": _default_dataset()})


def _ok(fn, *a, **kw):
    try:
        return JSONResponse(fn(*a, **kw))
    except Exception as e:  # noqa: BLE001 — surface engine errors as JSON, not a 500
        return JSONResponse({"error": str(e)}, status_code=400)


@router.get("/patients")
def patients(dataset: str | None = None):
    _scope(dataset)
    return _ok(ep.tool_list_patients, {})


@router.get("/patients/{patient_id}")
def patient(patient_id: str, dataset: str | None = None):
    """Curated chart AS OF the prediction date (post-index rows withheld)."""
    _scope(dataset)
    return _ok(ep.tool_get_patient, {"patient_id": patient_id})


@router.get("/models/{package}/card")
def model_card(package: str):
    """The MODEL CARD: what this endpoint is, what it eats, and what it was trained on.

    Assembled from the package's own files — nothing here is hand-written per model:

        manifest.json        the 5 inference functions + InferenceArgs (forecast mode)
        meta.json            the declared input/output schema
        model/config.json    ModelInstance + AIData names, tuner + architecture
        model/prefn_config.json  the case window (CaseFns, obs_dt_index) + trigger args
    """
    root = Path(os.path.expanduser(ep.ENDPOINT_STORE))
    pkg_dir = root / package
    if not (pkg_dir / "manifest.json").exists():
        return JSONResponse({"error": f"unknown package: {package}"}, status_code=404)

    def _read(rel: str) -> dict:
        p = pkg_dir / rel
        try:
            return json.loads(p.read_text())
        except Exception:  # noqa: BLE001 — an absent optional file is not an error
            return {}

    manifest = _read("manifest.json")
    meta = _read("meta.json")
    cfg = _read("model/config.json")
    prefn = _read("model/prefn_config.json")

    info = ep._model_info(package)
    reg = ep._registry()
    url = reg.get(package) or reg.get(info.get("endpoint_name") or "")

    model_args = (cfg.get("ModelArgs") or {})
    arch = (model_args.get("model_tuner_args") or {}).get("architecture_config") or {}
    tuner_args = model_args.get("model_tuner_args") or {}
    input_args = (prefn.get("InputArgs") or {})
    window = ((input_args.get("input_args") or {}).get("window_build") or {})
    trig = prefn.get("TriggerArgs") or {}
    inf_args = (manifest.get("inference_functions") or {}).get("InferenceArgs") or {}

    return JSONResponse(ep._clean({
        "package": package,
        "endpoint_name": info.get("endpoint_name"),
        "endpoint_version": info.get("endpoint_version"),
        "endpoint_url": url,
        "created_at": manifest.get("created_at"),
        "deployment": manifest.get("deployment"),

        # what it predicts, and how
        "prediction": {
            "type": ((meta.get("modelMetadata") or [{}])[0]).get("predictionType"),
            "unit": ((meta.get("modelMetadata") or [{}])[0]).get("unit"),
            "mode": inf_args.get("mode", "teacher_forced (eval path — not a forecast)"),
            "horizon_steps": inf_args.get("horizon"),
            "context_steps": (inf_args.get("obs_dt_index") + 1) if inf_args.get("obs_dt_index") is not None else None,
            "interval_minutes": 5,
        },

        # what it was trained on
        "training": {
            "modelinstance": cfg.get("modelinstance_set_name"),
            "aidata": cfg.get("aidata_name"),
            "tuner": model_args.get("model_tuner_name"),
            "base_model": tuner_args.get("model_name_or_path"),
            "max_seq_length": tuner_args.get("max_seq_length"),
            "value_range": tuner_args.get("value_range"),
            "learning_rate": tuner_args.get("learning_rate"),
            "architecture": arch,
        },

        # the case it builds per prediction
        "case": {
            "casefns": input_args.get("input_casefn_list"),
            "obs_dt_index": window.get("obs_dt_index"),
            "trigger": trig.get("Trigger"),
            "min_segment_length": trig.get("min_segment_length"),
            "max_consecutive_missing": trig.get("max_consecutive_missing"),
            "stride": trig.get("stride"),
            "patient_registry": trig.get("patient_info_path"),
        },

        # what to send it
        "payload": {
            "style": info.get("payload_style"),
            "models_field": info.get("models_field"),
            "required_tables": info.get("required_tables"),
            "optional_tables": info.get("optional_tables", []),
            "input_schema": meta.get("inputSchema"),
        },

        "inference_functions": {
            k: v for k, v in (manifest.get("inference_functions") or {}).items()
            if k != "InferenceArgs"
        },
    }))


@router.get("/patients/{patient_id}/layer/{layer}")
def patient_layer(patient_id: str, layer: str, dataset: str | None = None):
    """One layer of the pipeline, so a reader can SEE how the data was transformed:

        raw     the files exactly as they arrived (0-RawDataStore) — previewed
        source  ProcName_to_ProcDf, parsed into tables (1-SourceStore) == source_tables
        record  RecordFn output: cleaned, PID-keyed, binned (2-RecStore) — head only

    `source` is served by /raw (it is the payload's own layer and is stored in full).
    A store need not carry every layer — REACH's patients are harvested from endpoint
    examples and have only `source`; say so rather than pretending.
    """
    _scope(dataset)
    try:
        with open(ep._patient_path(patient_id)) as f:
            rec = json.load(f)
        layers = rec.get("layers") or {}
        if layer not in ("raw", "record"):
            return JSONResponse({"error": f"unknown layer: {layer}"}, status_code=400)
        if layer not in layers:
            return JSONResponse({
                "patient_id": rec.get("patient_id"),
                "layer": layer,
                "available": False,
                "reason": f"this patient store carries no '{layer}' layer "
                          "(it was built from endpoint examples, not from a subject store).",
            })
        return JSONResponse(ep._clean({
            "patient_id": rec.get("patient_id"),
            "layer": layer,
            "available": True,
            **layers[layer],
        }))
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"error": str(e)}, status_code=400)


@router.get("/patients/{patient_id}/raw")
def patient_raw(patient_id: str, dataset: str | None = None):
    """The SOURCE layer: every table, every column, every row — nothing withheld.

    (The route keeps its historical name; `source_tables` IS the source layer, and it
    is what payloads are built from.)

    Rows that postdate the prediction are FLAGGED (`_after_index`) rather than
    hidden: in this view the point is to see exactly what is in the record,
    including the fact that some of it postdates the score.
    """
    _scope(dataset)
    try:
        with open(ep._patient_path(patient_id)) as f:
            rec = json.load(f)
        index_date = ep._index_date(rec)
        tables = {}
        for name, rows in (rec.get("source_tables") or {}).items():
            if not isinstance(rows, list):
                continue
            cols: list[str] = []
            out_rows = []
            for r in rows:
                if not isinstance(r, dict):
                    continue
                for k in r:
                    if k not in cols:
                        cols.append(k)
                rd = ep._row_date(r)
                out_rows.append({
                    **r,
                    "_after_index": bool(index_date and rd and rd > index_date),
                    "_row_date": rd,
                })
            tables[name] = {"columns": cols, "n_rows": len(out_rows), "rows": out_rows}
        return JSONResponse(ep._clean({
            "patient_id": rec.get("patient_id"),
            "index_date": index_date,
            "tables": tables,
        }))
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"error": str(e)}, status_code=400)


@router.get("/models")
def models():
    return _ok(ep.tool_list_models, {})


@router.post("/predict")
def predict(body: dict[str, Any]):
    _scope(body.get("dataset"))
    return _ok(ep.tool_predict_for_patient, {
        "patient_id": body.get("patient_id"),
        "model": body.get("model"),
        "obs_dt": body.get("obs_dt"),
    })


@router.get("/health")
def health():
    cfg = {
        "patient_store": os.environ.get("INLAB_PATIENT_STORE", ""),
        "endpoint_store": os.environ.get("INLAB_ENDPOINT_STORE", ""),
        "registry": os.environ.get("INLAB_REGISTRY", ""),
        "engine": str(ENGINE),
    }
    missing = [k for k in ("patient_store", "endpoint_store", "registry") if not cfg[k]]
    if missing:
        return {"ok": False, "error": f"unconfigured: {', '.join(missing)}", "config": cfg}
    try:
        live = [m["package"] for m in ep.tool_list_models({})["models"] if m["live"]]
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e), "config": cfg}
    return {"ok": True, "live_endpoints": live, "config": cfg}

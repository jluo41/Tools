#!/usr/bin/env python3
"""endpoint-predict — a deployed prediction endpoint as an MCP tool.

Exposes any Endpoint_Set-style HTTP endpoint (local Flask/FastAPI, Databricks
Model Serving, SageMaker — same wire contract: GET /ping, POST /invocations
with a JSON payload) as tools an agent can call. The score always comes from
the endpoint verbatim; no LLM ever produces or edits the number.

Wire-contract provenance: mirrors haipipe-toolkit/skills/task/4_individual/
haipipe-individual-inference/src/client.py (Endpoint_Set payload POST). If the
upstream contract changes, re-sync.

Dependency-free (stdlib only), same idiom as haipipe-toolkit/mcp-servers/
codex-image2/server.py. Register with Claude Code:

    claude mcp add endpoint-predict -- python3 /path/to/server.py

Config via env:
    INLAB_ENDPOINT_URL   default endpoint base URL (e.g. http://127.0.0.1:5050)
    INLAB_ENDPOINT_TOKEN optional bearer token (Databricks serving)
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

SERVER_NAME = "endpoint-predict"
DEFAULT_URL = os.environ.get("INLAB_ENDPOINT_URL", "http://127.0.0.1:5050")
TOKEN = os.environ.get("INLAB_ENDPOINT_TOKEN", "")
TIMEOUT_SEC = int(os.environ.get("INLAB_ENDPOINT_TIMEOUT_SEC", "120"))
# console-mode stores (v0.2): patient store dir, Endpoint_Set store dir, url registry
PATIENT_STORE = os.environ.get("INLAB_PATIENT_STORE", "")
ENDPOINT_STORE = os.environ.get("INLAB_ENDPOINT_STORE", "")
REGISTRY_PATH = os.environ.get("INLAB_REGISTRY", "")


# ---------------------------------------------------------------- HTTP layer
def _base(url: str | None) -> str:
    base = (url or DEFAULT_URL).rstrip("/")
    # accept either a base url or a full .../invocations url
    if base.endswith("/invocations"):
        base = base[: -len("/invocations")]
    return base


def _headers() -> dict[str, str]:
    h = {"Content-Type": "application/json"}
    if TOKEN:
        h["Authorization"] = f"Bearer {TOKEN}"
    return h


def http_get(url: str) -> dict[str, Any]:
    req = urllib.request.Request(url, headers=_headers())
    with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as r:
        return json.loads(r.read().decode("utf-8"))


def http_post(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=_headers(), method="POST")
    with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as r:
        return json.loads(r.read().decode("utf-8"))


# ---------------------------------------------------------------- console-mode helpers (v0.2)
def _registry() -> dict[str, str]:
    if REGISTRY_PATH and os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH) as f:
            return json.load(f)
    return {}


def _clean(obj: Any) -> Any:
    """NaN/Infinity are NOT valid JSON (RFC 8259) — Python emits them anyway, and
    strict consumers (FastAPI, browsers, most JSON parsers) reject the payload.
    Coerce them to null so every consumer can read a patient."""
    if isinstance(obj, float):
        if obj != obj or obj in (float("inf"), float("-inf")):  # NaN / ±Inf
            return None
        return obj
    if isinstance(obj, dict):
        return {k: _clean(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_clean(v) for v in obj]
    return obj


# Date column per source table, in priority order — used to answer "was this row
# already on the chart at prediction time?"
_DATE_KEYS = (
    "EncContactDate", "ContactDate", "StartDate", "RecordedTime",
    "ResultDate", "QuestionInstant", "OrderingDttm", "IndexDate",
)


def _row_date(row: dict[str, Any]) -> str | None:
    for k in _DATE_KEYS:
        v = row.get(k)
        if v and str(v) not in ("NaT", "None", "nan"):
            return str(v)[:10]
    return None


def _index_date(patient: dict[str, Any], pkg: str | None = None) -> str | None:
    """The prediction trigger date (ObsDT) — the moment the model scores."""
    provs = patient.get("provenance", [])
    for p in provs:
        if pkg and p.get("endpoint_package") != pkg:
            continue
        for t in p.get("triggers", []):
            if t.get("ObsDT"):
                return str(t["ObsDT"])[:10]
    for p in provs:
        for t in p.get("triggers", []):
            if t.get("ObsDT"):
                return str(t["ObsDT"])[:10]
    return None


def _patient_path(patient_id: str) -> str:
    if not PATIENT_STORE:
        raise ValueError("INLAB_PATIENT_STORE is not configured")
    p = os.path.join(os.path.expanduser(PATIENT_STORE), f"{patient_id}.json")
    if not os.path.exists(p):
        raise ValueError(f"unknown patient: {patient_id}")
    return p


def _model_dirs() -> list[str]:
    if not ENDPOINT_STORE:
        raise ValueError("INLAB_ENDPOINT_STORE is not configured")
    root = os.path.expanduser(ENDPOINT_STORE)
    return sorted(d for d in os.listdir(root)
                  if os.path.isdir(os.path.join(root, d))
                  and os.path.exists(os.path.join(root, d, "manifest.json")))


def _model_info(pkg: str) -> dict[str, Any]:
    root = os.path.expanduser(ENDPOINT_STORE)
    with open(os.path.join(root, pkg, "manifest.json")) as f:
        manifest = json.load(f)
    info = {
        "package": pkg,
        "endpoint_name": manifest.get("endpoint_name"),
        "endpoint_version": manifest.get("endpoint_version"),
        "models_field": None,
        "required_tables": [],
    }
    ex = os.path.join(root, pkg, "examples", "example_000", "payload.json")
    if os.path.exists(ex):
        with open(ex) as f:
            example = json.load(f)
        info["models_field"] = example.get("models")
        info["required_tables"] = sorted(example.get("source_tables", {}).keys())
    return info


def _resolve_model(model: str) -> dict[str, Any]:
    """Accept a package dir name, endpoint_name, or models_field value.
    Several packages can share an endpoint_name (versions); prefer one with a
    registered URL, then the highest version."""
    matches = []
    for pkg in _model_dirs():
        info = _model_info(pkg)
        if model in (pkg, info["endpoint_name"], info["models_field"]):
            matches.append(info)
    if not matches:
        raise ValueError(f"unknown model: {model} (try list_models)")
    reg = _registry()
    matches.sort(key=lambda i: (i["package"] in reg or (i["endpoint_name"] or "") in reg,
                                i["endpoint_version"] or ""), reverse=True)
    return matches[0]


def _pick_trigger(patient: dict[str, Any], pkg: str) -> tuple[dict[str, Any] | None, str]:
    """Trigger record (PID, ObsDT[, EncCSN]) for the payload's dataframe_records.
    Prefer the trigger stored for THIS model; else borrow PID/ObsDT from any
    provenance (cross-model prediction)."""
    provs = patient.get("provenance", [])
    for p in provs:
        if p.get("endpoint_package") == pkg and p.get("triggers"):
            return dict(p["triggers"][0]), "native"
    for p in provs:
        if p.get("triggers"):
            t = p["triggers"][0]
            return {k: t[k] for k in ("PID", "ObsDT") if k in t}, \
                f"borrowed from {p.get('endpoint_package')}"
    return None, "none available"


def _build_payload_for(patient_id: str, model: str,
                       obs_dt: str | None = None) -> dict[str, Any]:
    info = _resolve_model(model)
    with open(_patient_path(patient_id)) as f:
        patient = json.load(f)
    have = patient.get("source_tables", {})
    source_tables, missing, empty = {}, [], []
    for t in info["required_tables"]:
        rows = have.get(t)
        if rows is None:
            missing.append(t)
            source_tables[t] = []
        else:
            source_tables[t] = rows
            if not rows:
                empty.append(t)
    extra = sorted(set(have) - set(info["required_tables"]))
    trigger, trigger_source = _pick_trigger(patient, info["package"])
    if trigger is None:
        raise ValueError(f"no trigger record (PID/ObsDT) stored for {patient_id}; "
                         "cannot build dataframe_records")
    if obs_dt:
        trigger["ObsDT"] = obs_dt
        trigger_source += f"; ObsDT overridden to {obs_dt}"
    return {
        "payload": {"models": info["models_field"], "source_tables": source_tables,
                    "dataframe_records": [trigger]},
        "model": info,
        "trigger": {"record": trigger, "source": trigger_source},
        "gaps": {"missing_tables": missing, "empty_tables": empty,
                 "unused_patient_tables": extra},
    }


# ---------------------------------------------------------------- console-mode tools (v0.2)
def tool_list_patients(args: dict[str, Any]) -> dict[str, Any]:
    store = os.path.expanduser(PATIENT_STORE)
    if not PATIENT_STORE or not os.path.isdir(store):
        raise ValueError("INLAB_PATIENT_STORE is not configured or missing")
    out = []
    for fn in sorted(os.listdir(store)):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(store, fn)) as f:
            rec = json.load(f)
        out.append({"patient_id": rec.get("patient_id", fn[:-5]),
                    "summary": rec.get("summary", {}),
                    "seen_by": sorted({p["endpoint_package"] for p in rec.get("provenance", [])})})
    return _clean({"patient_store": store, "n": len(out), "patients": out})


def tool_get_patient(args: dict[str, Any]) -> dict[str, Any]:
    pid = args.get("patient_id") or ""
    with open(_patient_path(pid)) as f:
        rec = json.load(f)

    index_date = args.get("as_of") or _index_date(rec)
    include_future = bool(args.get("include_post_index"))

    tables = args.get("tables")
    max_rows = int(args.get("max_rows") or 200)   # never ship an unbounded chart
    st = rec.get("source_tables", {})
    if tables:
        st = {t: st.get(t, []) for t in tables}

    out: dict[str, list] = {}
    dropped = 0
    for t, rows in st.items():
        if not isinstance(rows, list):
            out[t] = rows
            continue
        keep = rows
        # A prediction is made AS OF index_date. Showing later rows lets the reader
        # (human or agent) see the future — leakage. Excluded unless asked for.
        if index_date and not include_future:
            keep = [r for r in rows if not (_row_date(r) and _row_date(r) > index_date)]
            dropped += len(rows) - len(keep)
        out[t] = keep[:max_rows]

    return _clean({
        "patient_id": rec.get("patient_id"),
        "summary": rec.get("summary"),
        "index_date": index_date,
        "age_at_index": _age_at(rec.get("summary", {}).get("birth_date"), index_date),
        "post_index_rows_hidden": dropped,
        "row_cap": max_rows,
        "source_tables": out,
    })


def _age_at(birth: str | None, as_of: str | None) -> int | None:
    """Age at the PREDICTION date — not today. A model scored in 2023 must be read
    against the patient as they were in 2023."""
    if not birth or not as_of:
        return None
    try:
        from datetime import date
        b = date.fromisoformat(str(birth)[:10])
        a = date.fromisoformat(str(as_of)[:10])
    except ValueError:
        return None
    return (a - b).days // 365


def tool_list_models(args: dict[str, Any]) -> dict[str, Any]:
    reg = _registry()
    models = []
    for pkg in _model_dirs():
        info = _model_info(pkg)
        url = reg.get(pkg) or reg.get(info["endpoint_name"] or "")
        live = False
        if url:
            try:
                live = http_get(f"{_base(url)}/ping").get("status") == "healthy"
            except Exception:
                live = False
        info.update({"endpoint_url": url, "live": live})
        models.append(info)
    return {"endpoint_store": os.path.expanduser(ENDPOINT_STORE), "models": models}


def tool_prepare_payload(args: dict[str, Any]) -> dict[str, Any]:
    pid = args.get("patient_id") or ""
    model = args.get("model") or ""
    if not pid or not model:
        raise ValueError("patient_id and model are required")
    return _build_payload_for(pid, model, args.get("obs_dt"))


def tool_predict_for_patient(args: dict[str, Any]) -> dict[str, Any]:
    """The one-shot console verb: prepare the payload for (patient, model),
    POST it to that model's endpoint, return prediction + gaps report."""
    pid = args.get("patient_id") or ""
    model = args.get("model") or ""
    if not pid or not model:
        raise ValueError("patient_id and model are required")
    built = _build_payload_for(pid, model, args.get("obs_dt"))
    url = args.get("endpoint_url") or _registry().get(built["model"]["package"]) \
        or _registry().get(built["model"]["endpoint_name"] or "")
    if not url:
        raise ValueError(f"no endpoint URL known for {built['model']['package']} "
                         "(pass endpoint_url or add it to the registry)")
    response = http_post(f"{_base(url)}/invocations", built["payload"])
    return _clean({"patient_id": pid, "model": built["model"], "endpoint_url": _base(url),
                   "trigger": built["trigger"], "gaps": built["gaps"], "response": response})


# ---------------------------------------------------------------- tools
def tool_ping(args: dict[str, Any]) -> dict[str, Any]:
    base = _base(args.get("endpoint_url"))
    return {"endpoint_url": base, "ping": http_get(f"{base}/ping")}


def _load_payload(args: dict[str, Any]) -> dict[str, Any]:
    if isinstance(args.get("payload"), dict):
        return args["payload"]
    path = args.get("payload_path")
    if not path:
        raise ValueError("provide either `payload` (object) or `payload_path` (file)")
    with open(os.path.expanduser(path)) as f:
        return json.load(f)


def tool_predict(args: dict[str, Any]) -> dict[str, Any]:
    base = _base(args.get("endpoint_url"))
    payload = _load_payload(args)
    response = http_post(f"{base}/invocations", payload)
    return {"endpoint_url": base, "response": response}


def tool_predict_packaged_example(args: dict[str, Any]) -> dict[str, Any]:
    """Run one of the Endpoint_Set package's own examples/<name>/payload.json
    and return both the live response and the packaged expected result —
    the standard smoke test that the endpoint under test is sane."""
    ep_path = args.get("endpoint_path")
    if not ep_path:
        raise ValueError("endpoint_path is required")
    example = args.get("example", "example_000")
    ex_dir = os.path.join(os.path.expanduser(ep_path), "examples", example)
    with open(os.path.join(ex_dir, "payload.json")) as f:
        payload = json.load(f)
    expected_path = os.path.join(ex_dir, "prediction_results.json")
    expected = None
    if os.path.exists(expected_path):
        with open(expected_path) as f:
            expected = json.load(f)
    base = _base(args.get("endpoint_url"))
    response = http_post(f"{base}/invocations", payload)
    return {"endpoint_url": base, "example": example,
            "response": response, "expected": expected}


TOOLS: dict[str, Any] = {
    "list_patients": {
        "fn": tool_list_patients,
        "description": "List patients in the configured patient store (id, demographics summary, table counts, which models' data they carry).",
        "inputSchema": {"type": "object", "properties": {}},
    },
    "get_patient": {
        "fn": tool_get_patient,
        "description": "Get one patient's chart AS OF the prediction date (all source tables: Dx, Med, Vital, Lab, Questionnaire, ...). Rows dated after the trigger are excluded by default (they are the future relative to the score); pass include_post_index to see them. Rows are capped per table.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string"},
                "tables": {"type": "array", "items": {"type": "string"}, "description": "Only these tables."},
                "max_rows": {"type": "integer", "description": "Cap rows per table (default 200; big MIMIC charts)."},
                "as_of": {"type": "string", "description": "Chart as of this date; defaults to the patient's prediction trigger date."},
                "include_post_index": {"type": "boolean", "description": "Include rows dated AFTER the prediction date. Default false — those are the future relative to the score."},
            },
            "required": ["patient_id"],
        },
    },
    "list_models": {
        "fn": tool_list_models,
        "description": "List available prediction models (Endpoint_Set packages): name, version, required source tables, registered endpoint URL, and whether it is live right now.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    "prepare_payload": {
        "fn": tool_prepare_payload,
        "description": "Assemble the inference payload for (patient, model): selects the model's required tables from the patient's data and reports gaps (missing/empty tables). Does NOT call the endpoint.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string"},
                "model": {"type": "string", "description": "Package dir, endpoint name, or models-field value (see list_models)."},
                "obs_dt": {"type": "string", "description": "Override the as-of prediction date (trigger ObsDT)."},
            },
            "required": ["patient_id", "model"],
        },
    },
    "predict_for_patient": {
        "fn": tool_predict_for_patient,
        "description": "One-shot console verb: prepare the payload for (patient, model), POST it to that model's registered endpoint, and return the prediction plus a data-gaps report. The score comes from the endpoint verbatim.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string"},
                "model": {"type": "string"},
                "obs_dt": {"type": "string", "description": "Override the as-of prediction date (trigger ObsDT)."},
                "endpoint_url": {"type": "string", "description": "Override the registry URL."},
            },
            "required": ["patient_id", "model"],
        },
    },
    "ping": {
        "fn": tool_ping,
        "description": "Health-check the prediction endpoint (GET /ping).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "endpoint_url": {"type": "string", "description": "Base URL; defaults to INLAB_ENDPOINT_URL."}
            },
        },
    },
    "predict": {
        "fn": tool_predict,
        "description": ("POST a JSON payload to the endpoint's /invocations and return the "
                        "prediction response verbatim (risk score etc.). Payload inline or from file."),
        "inputSchema": {
            "type": "object",
            "properties": {
                "payload": {"type": "object", "description": "Inline payload JSON (Endpoint_Set contract: models + source_tables)."},
                "payload_path": {"type": "string", "description": "Path to a payload.json file (alternative to `payload`)."},
                "endpoint_url": {"type": "string", "description": "Base URL; defaults to INLAB_ENDPOINT_URL."},
            },
        },
    },
    "predict_packaged_example": {
        "fn": tool_predict_packaged_example,
        "description": ("Smoke test: run a packaged example (examples/<name>/payload.json) from an "
                        "Endpoint_Set folder against the live endpoint and return response + expected."),
        "inputSchema": {
            "type": "object",
            "properties": {
                "endpoint_path": {"type": "string", "description": "Path to the Endpoint_Set package folder."},
                "example": {"type": "string", "description": "Example name, default example_000."},
                "endpoint_url": {"type": "string", "description": "Base URL; defaults to INLAB_ENDPOINT_URL."},
            },
            "required": ["endpoint_path"],
        },
    },
}


# ---------------------------------------------------------------- MCP plumbing
def reply(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def reply_tool_text(request_id: Any, payload: dict[str, Any], is_error: bool = False) -> dict[str, Any]:
    return reply(request_id, {
        "content": [{"type": "text", "text": json.dumps(payload, indent=2)}],
        "isError": is_error,
    })


def handle(msg: dict[str, Any]) -> dict[str, Any] | None:
    method = msg.get("method")
    request_id = msg.get("id")
    if method == "initialize":
        return reply(request_id, {
            "protocolVersion": msg.get("params", {}).get("protocolVersion", "2024-11-05"),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": SERVER_NAME, "version": "0.1.0"},
        })
    if method in ("notifications/initialized", "notifications/cancelled"):
        return None
    if method == "tools/list":
        return reply(request_id, {"tools": [
            {"name": name, "description": t["description"], "inputSchema": t["inputSchema"]}
            for name, t in TOOLS.items()
        ]})
    if method == "tools/call":
        params = msg.get("params", {})
        name = params.get("name")
        args = params.get("arguments") or {}
        tool = TOOLS.get(name)
        if tool is None:
            return reply_tool_text(request_id, {"error": f"unknown tool: {name}"}, is_error=True)
        try:
            return reply_tool_text(request_id, tool["fn"](args))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:2000]
            return reply_tool_text(request_id, {"error": f"HTTP {e.code}", "body": body}, is_error=True)
        except Exception as e:  # noqa: BLE001 — tool errors go back to the caller
            return reply_tool_text(request_id, {"error": str(e)}, is_error=True)
    if request_id is not None:
        return {"jsonrpc": "2.0", "id": request_id,
                "error": {"code": -32601, "message": f"method not found: {method}"}}
    return None


def main() -> None:
    # unbuffered binary stdio for MCP framing — done here, not at import time,
    # so importing this module as a library (predict_cli, build_bundle) is safe
    sys.stdout = os.fdopen(sys.stdout.fileno(), "wb", buffering=0)
    sys.stdin = os.fdopen(sys.stdin.fileno(), "rb", buffering=0)
    for raw in sys.stdin:
        line = raw.decode("utf-8").strip() if isinstance(raw, bytes) else raw.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        out = handle(msg)
        if out is not None:
            sys.stdout.write((json.dumps(out) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()

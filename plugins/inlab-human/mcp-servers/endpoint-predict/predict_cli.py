#!/usr/bin/env python3
"""predict_cli.py — CLI twin of the endpoint-predict MCP server.

Every MCP tool has a subcommand here, same code paths — this is the fallback
whenever the MCP server isn't registered in the session (or is stale). Stdlib
only.

Store config resolves in this order, so NO env vars are required:
  1. --patient-store / --endpoint-store / --registry flags
  2. INLAB_* environment variables
  3. the repo's .mcp.json  (endpoint-predict → env)   <-- the usual path

Console verbs:
    python3 predict_cli.py list-patients
    python3 predict_cli.py get-patient      --patient-id reach-100060 [--tables Dx Med] [--max-rows 20]
    python3 predict_cli.py list-models
    python3 predict_cli.py prepare-payload  --patient-id reach-100060 --model reach.adhd.xgb
    python3 predict_cli.py predict-for-patient --patient-id reach-100060 --model reach.adhd.xgb [--obs-dt 2023-06-01]

Network verbs:
    python3 predict_cli.py ping     [--endpoint-url URL]
    python3 predict_cli.py predict  --payload-path payload.json
    python3 predict_cli.py example  --endpoint-path <Endpoint_Set dir> [--example example_000]
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _bootstrap_env(args) -> None:
    """Populate INLAB_* env BEFORE importing server.py (it reads them at import)."""
    # 3. repo .mcp.json — walk up for a dir containing .mcp.json
    d = HERE
    for _ in range(8):
        cand = os.path.join(d, ".mcp.json")
        if os.path.exists(cand):
            try:
                with open(cand) as f:
                    cfg = json.load(f)
                env = cfg.get("mcpServers", {}).get("endpoint-predict", {}).get("env", {})
                for k, v in env.items():
                    os.environ.setdefault(k, v)
            except (OSError, ValueError):
                pass
            break
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    # 1. explicit flags win
    for flag, key in (("patient_store", "INLAB_PATIENT_STORE"),
                      ("endpoint_store", "INLAB_ENDPOINT_STORE"),
                      ("registry", "INLAB_REGISTRY"),
                      ("endpoint_url", "INLAB_ENDPOINT_URL")):
        v = getattr(args, flag, None)
        if v:
            os.environ[key] = v


def main() -> int:
    ap = argparse.ArgumentParser(description="endpoint-predict CLI (twin of the MCP server)")
    for p in (ap,):
        p.add_argument("--patient-store", help="override INLAB_PATIENT_STORE")
        p.add_argument("--endpoint-store", help="override INLAB_ENDPOINT_STORE")
        p.add_argument("--registry", help="override INLAB_REGISTRY")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list-patients")
    sub.add_parser("list-models")

    p = sub.add_parser("get-patient")
    p.add_argument("--patient-id", required=True)
    p.add_argument("--tables", nargs="*")
    p.add_argument("--max-rows", type=int)

    for name in ("prepare-payload", "predict-for-patient"):
        p = sub.add_parser(name)
        p.add_argument("--patient-id", required=True)
        p.add_argument("--model", required=True)
        p.add_argument("--obs-dt")
        p.add_argument("--endpoint-url")

    p = sub.add_parser("ping")
    p.add_argument("--endpoint-url")

    p = sub.add_parser("predict")
    p.add_argument("--payload-path", required=True)
    p.add_argument("--endpoint-url")

    p = sub.add_parser("example")
    p.add_argument("--endpoint-path", required=True)
    p.add_argument("--example", default="example_000")
    p.add_argument("--endpoint-url")

    a = ap.parse_args()
    _bootstrap_env(a)

    sys.path.insert(0, HERE)
    import server  # noqa: E402 — imported after env bootstrap

    dispatch = {
        "list-patients": lambda: server.tool_list_patients({}),
        "list-models": lambda: server.tool_list_models({}),
        "get-patient": lambda: server.tool_get_patient(
            {"patient_id": a.patient_id, "tables": a.tables, "max_rows": a.max_rows}),
        "prepare-payload": lambda: server.tool_prepare_payload(
            {"patient_id": a.patient_id, "model": a.model, "obs_dt": a.obs_dt}),
        "predict-for-patient": lambda: server.tool_predict_for_patient(
            {"patient_id": a.patient_id, "model": a.model, "obs_dt": a.obs_dt,
             "endpoint_url": a.endpoint_url}),
        "ping": lambda: server.tool_ping({"endpoint_url": a.endpoint_url}),
        "predict": lambda: server.tool_predict(
            {"payload_path": a.payload_path, "endpoint_url": a.endpoint_url}),
        "example": lambda: server.tool_predict_packaged_example(
            {"endpoint_path": a.endpoint_path, "example": a.example,
             "endpoint_url": a.endpoint_url}),
    }
    try:
        out = dispatch[a.cmd]()
    except Exception as e:  # noqa: BLE001 — CLI surfaces tool errors plainly
        json.dump({"error": str(e)}, sys.stdout, indent=2)
        print()
        return 1
    json.dump(out, sys.stdout, indent=2, default=str)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())

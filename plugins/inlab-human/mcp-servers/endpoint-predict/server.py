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

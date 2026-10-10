"""SYNTHETIC stub endpoint for the In-Lab Console fixtures: answers the Endpoint_Set wire contract with fixed values.

    GET  /ping          {"status": "healthy"}
    POST /invocations   a CGM columnar payload  -> a 12-step glucose forecast (+ context, observed, MAE/RMSE)
                        a source_tables payload -> one risk score and band

The numbers are computed from the payload alone (no model), so the same payload always gets the same answer.
It exists so the console can be run, tested and screenshotted without a real endpoint or a real patient.
Stdlib only:

    python stub_endpoint.py [--port 8192]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HORIZON = 12


def forecast(payload: dict) -> dict:
    values = [v for v in (payload.get("CGM") or {}).get("BGValue", []) if isinstance(v, (int, float))]
    context = values[-288:] or [120.0]
    last = context[-1]
    slope = (context[-1] - context[-7]) / 6 if len(context) >= 7 else 0.0
    fc = [round(last + slope * (k + 1) * 0.6, 1) for k in range(HORIZON)]
    observed = [round(last + slope * (k + 1) * 0.6 + 6 * math.sin(k / 2), 1) for k in range(HORIZON)]
    err = [f - o for f, o in zip(fc, observed)]
    return {"forecast": fc, "observed": observed, "context": context[-48:],
            "metadata": {"unit": "mg/dL", "intervalMinutes": 5, "inferenceMode": "forecast"},
            "metrics": {"mae": round(sum(abs(e) for e in err) / len(err), 2),
                        "rmse": round(math.sqrt(sum(e * e for e in err) / len(err)), 2)},
            "predictions": []}


def risk(payload: dict) -> dict:
    digest = hashlib.sha256(json.dumps(payload.get("source_tables"), sort_keys=True).encode()).hexdigest()
    score = round(int(digest[:6], 16) / 0xFFFFFF, 3)
    band = "high" if score >= 0.66 else "medium" if score >= 0.33 else "low"
    return {"predictions": [{"risk_score": score, "risk_level": band}]}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, obj: dict) -> None:
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.rstrip("/") == "/ping":
            return self._send(200, {"status": "healthy", "synthetic": True})
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path.rstrip("/") != "/invocations":
            return self._send(404, {"error": "not found"})
        payload = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
        models = payload.get("models")
        name = (models[0] if isinstance(models, list) else models) or "synth"
        body = forecast(payload) if "CGM" in payload else risk(payload)
        self._send(200, {"models": [{"name": str(name).split("/")[0], "version": "v0001", "date": "2026-10-09",
                                     **body}], "status": {"code": 200, "message": "synthetic stub"}})

    def log_message(self, *_):
        pass


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8192)
    a = ap.parse_args()
    ThreadingHTTPServer(("127.0.0.1", a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()

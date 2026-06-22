"""End-to-end demo: individual path → endpoint POST → forecast.

Two-step agent flow (no LLM yet):
  1. agent-side: build dataframe_records payload from individual path
  2. agent-side: HTTP POST to endpoint_url → forecast

    python predict_cli.py --individual Subject-18
    python predict_cli.py --individual UserGroup-WellDoc2022CGM/Subject-26 --json
    CGM_ENDPOINT_URL=http://my-databricks-host/invocations python predict_cli.py --individual Subject-18
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SKILL_SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SKILL_SRC))

from build_payload import build_payload, build_payload_summary  # noqa: E402
from client import call_predict, slice_last_window  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--individual", required=True)
    ap.add_argument("--endpoint-url", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--single-window", action="store_true",
                    help="Keep only the most recent forecast window in the "
                         "response (anchored at the last CGM observation).")
    args = ap.parse_args()

    payload = build_payload(args.individual)
    summary = build_payload_summary(payload)
    print(f"📦 payload  : {summary}")

    out = call_predict(payload, endpoint_url=args.endpoint_url)
    if args.single_window:
        out = slice_last_window(out)

    if args.json:
        print(json.dumps(out, indent=2, default=str))
        return

    print(f"📥 response : keys={list(out.keys())[:8]}")
    print(json.dumps(out, indent=2, default=str)[:2000])


if __name__ == "__main__":
    main()

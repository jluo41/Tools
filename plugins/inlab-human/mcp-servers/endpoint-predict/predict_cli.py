#!/usr/bin/env python3
"""predict_cli.py — CLI twin of the endpoint-predict MCP server.

Same tools, same code paths, callable from Bash (skills use this when the MCP
server isn't registered in the session). Stdlib only.

    python3 predict_cli.py ping [--endpoint-url URL]
    python3 predict_cli.py predict --payload-path payload.json [--endpoint-url URL]
    python3 predict_cli.py example --endpoint-path <Endpoint_Set dir> [--example example_000]
"""
import argparse
import json
import sys

from server import tool_ping, tool_predict, tool_predict_packaged_example  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

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
    if a.cmd == "ping":
        out = tool_ping({"endpoint_url": a.endpoint_url})
    elif a.cmd == "predict":
        out = tool_predict({"payload_path": a.payload_path, "endpoint_url": a.endpoint_url})
    else:
        out = tool_predict_packaged_example(
            {"endpoint_path": a.endpoint_path, "example": a.example, "endpoint_url": a.endpoint_url})
    json.dump(out, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())

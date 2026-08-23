"""Where B1's cases come from: `5-api-examples/`, replayed.

WHY NOT 4-contract
================================================================================
It was the obvious source and it is the wrong one. The three `4-contract`
folders are not the same kind of thing: food's specimens are RECORDS in the
foodrec/v1 shape, with no request in them at all, while exercise's and
medication's are request/response pairs. A benchmark cannot replay a record.

`5-api-examples` is uniform across all three folders -- `<group>/<case>/`
holding `request.json`, `response.json`, `curl.sh` -- because it is generated
by the same writer. 76 cases, every one a real call against the running
service, and every one already checked into the workspace as documentation.

So B1 costs no new fixtures. It turns the examples the family already publishes
into the test that they are examples of one thing.

WHOSE CASE IS IT
================================================================================
`curl.sh` names the endpoint, and that is the routing key. It matters because
`_MedInfo/5-api-examples` holds BOTH members: `4-insulin/` posts to
INSNORM_URL on 8080 while its siblings post to MEDNORM_URL on 8079. A chain
shares an _XInfo folder, so a folder is not a member.
"""
import json
import pathlib
import re
from typing import Dict, List


def _is_error(response) -> bool:
    """A stored error body. Every service writes `detail`; no member field is
    called that, so the key alone is the discriminator."""
    return isinstance(response, dict) and "detail" in response


def discover(examples: pathlib.Path, port: int, url_env: str = "") -> List[Dict]:
    """Every fixture under `examples` whose curl.sh points at `port`."""
    out = []
    for req in sorted(examples.rglob("request.json")):
        case = req.parent
        curl = (case / "curl.sh").read_text() if (case / "curl.sh").exists() else ""
        if curl:
            mine = (f":{port}" in curl) or (url_env and url_env in curl)
            if not mine:
                continue
        rel = case.relative_to(examples)
        resp = case / "response.json"
        body = json.loads(resp.read_text()) if resp.exists() else None
        out.append({
            "name": str(rel),
            "group": rel.parts[0] if len(rel.parts) > 1 else "",
            "request": json.loads(req.read_text()),
            "expected": body,
            "is_error": _is_error(body),
            "endpoint": "batch" if "/normalize/batch" in curl else "single",
        })
    return out

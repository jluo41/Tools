#!/usr/bin/env python3
"""Append an attributed food-label correction to a finalized meal Run."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path


EPISODE_RE = re.compile(
    r"^- \*\*Episode #(\d+):\*\* .* · label_status=([a-z_]+) · "
    r"labels=(\[[^\n]*\]|null)(?: · service_error=[A-Za-z0-9_]+)?$"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--episode", required=True, type=int)
    parser.add_argument("--label", required=True, action="append",
                        help="human-confirmed food label; repeat for multiple foods")
    parser.add_argument("--actor", required=True,
                        help="person making the correction")
    parser.add_argument("--reason", default=None,
                        help="optional short explanation for the correction")
    args = parser.parse_args()

    receipt = args.receipt.expanduser().resolve()
    if not receipt.is_file():
        parser.error(f"receipt does not exist: {receipt}")
    if args.episode < 1:
        parser.error("--episode must be a positive episode number")
    if not args.actor.strip():
        parser.error("--actor must identify the correcting person")
    labels = [" ".join(label.lower().split()) for label in args.label]
    if any(not label for label in labels):
        parser.error("food labels must not be blank")

    text = receipt.read_text(encoding="utf-8")
    status_line = next((line for line in text.splitlines()
                        if line.startswith("- **Status:**")), None)
    if status_line is None:
        parser.error("receipt has no Run status")
    run_status = status_line.partition(":**")[2].strip()
    if run_status in {"running", "in-progress", "In progress"}:
        parser.error("record corrections after the Run has been finalized")

    original_status = None
    original_labels = None
    for line in text.splitlines():
        match = EPISODE_RE.match(line)
        if match and int(match.group(1)) == args.episode:
            original_status = match.group(2)
            original_labels = json.loads(match.group(3))
            break
    if original_status is None:
        parser.error(f"episode #{args.episode} is not present in this receipt")

    sidecar = receipt.with_suffix(receipt.suffix + ".corrections.jsonl")
    prior_status = original_status
    prior_labels = original_labels
    if sidecar.exists():
        for raw_line in sidecar.read_text(encoding="utf-8").splitlines():
            if not raw_line.strip():
                continue
            event = json.loads(raw_line)
            if (event.get("run_id") == receipt.stem
                    and event.get("episode_id") == args.episode):
                prior_status = event["corrected"]["status"]
                prior_labels = event["corrected"]["labels"]

    event = {
        "schema_version": 1,
        "kind": "human_food_label_correction",
        "run_id": receipt.stem,
        "episode_id": args.episode,
        "previous": {"status": prior_status, "labels": prior_labels},
        "corrected": {"status": "human_confirmed", "labels": labels},
        "actor": args.actor.strip(),
        "at": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
        "reason": args.reason,
    }
    with sidecar.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, ensure_ascii=False) + "\n")
    print(f"Appended correction for {receipt.stem} episode #{args.episode}: {sidecar}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

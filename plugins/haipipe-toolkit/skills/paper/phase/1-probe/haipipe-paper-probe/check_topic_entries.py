#!/usr/bin/env python3
"""Verify the Paper S03/S04 nested topic-entry contract.

Usage: check-probe-cards.sh <paper_root> [project_root] [--stage <key>] [--final]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ENTRY_HEADINGS = (
    "q-executor",
    "consumer trace",
    "bank binding",
    "a-executor",
)
STATES = {"planned", "commissioned", "deferred", "read", "answered-local"}


def page_id(path: Path) -> str | None:
    match = re.match(r"^(S-(?:Literature|Value)-\d+)-", path.name)
    return match.group(1) if match else None


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^####\s+{re.escape(heading)}\s*$\n(.*?)(?=^####\s|\Z)",
        text,
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def q_ids(text: str) -> set[str]:
    return set(re.findall(r"\bQ-[A-Za-z][A-Za-z0-9-]*", text))


def is_substantive(text: str) -> bool:
    return bool(re.sub(r"[\s`*_>\-:]+", "", text))


def stage_stem(key: str) -> str:
    return "Sec" if key == "section-edit" else key.rstrip("s").replace("-", "").title().replace(" ", "")


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("paper_root")
    parser.add_argument("project_root", nargs="?")
    parser.add_argument("--stage")
    parser.add_argument("--final", action="store_true")  # Reserved for compatible callers.
    parser.add_argument("-h", "--help", action="help")
    args = parser.parse_args()

    root = Path(args.paper_root).expanduser().resolve()
    if not root.is_dir():
        print(f"FAIL  no such paper root: {root}")
        return 1

    failed = 0
    warned = 0
    checked = 0
    legacy = root / "1-probes"
    if legacy.exists():
        print("FAIL  1-probes/ is live. Move legacy evidence under 0-lifecycle/_archive/1-probes/.")
        failed += 1

    topics: dict[str, tuple[Path, str]] = {}
    entries: list[Path] = []
    for stage in ("S03-literature", "S04-value"):
        stage_root = root / "0-lifecycle" / stage
        if not stage_root.is_dir():
            continue
        for topic in sorted(stage_root.glob("S-*.md")):
            identity = page_id(topic)
            if identity:
                topics[identity] = (topic, topic.read_text(encoding="utf-8"))
        probe_root = stage_root / "probes"
        if probe_root.is_dir():
            entries.extend(sorted(probe_root.glob("*/*.md")))

    if not topics:
        print("WARN  no S03/S04 topic pages found")
        warned += 1
    if not entries:
        print("WARN  no nested topic entries found")
        warned += 1

    expected_stem = stage_stem(args.stage) if args.stage else ""
    stage_matches = 0
    for entry in entries:
        text = entry.read_text(encoding="utf-8")
        entry_family = "Literature" if "S03-literature" in entry.parts else "Value"
        trace = section(text, "consumer trace")
        trace_ids = q_ids(trace)
        if args.stage and not any(q.startswith(f"Q-{expected_stem}") for q in trace_ids):
            continue
        stage_matches += 1 if args.stage else 0
        checked += 1
        relative = entry.relative_to(root)
        issues: list[str] = []

        for heading in ENTRY_HEADINGS:
            count = len(re.findall(rf"^####\s+{re.escape(heading)}\s*$", text, re.I | re.M))
            if count != 1:
                issues.append(f"{heading.replace(' ', '-')}-count={count}")
        required = re.search(r"^requires:\s*(S-(?:Literature|Value)-\d+)\s*$", text, re.I | re.M)
        if not required:
            issues.append("missing-direct-topic-requires")
            parent_text = ""
        else:
            parent_id = required.group(1)
            if not parent_id.startswith(f"S-{entry_family}-"):
                issues.append(f"entry-family-does-not-match-topic={parent_id}")
            parent = topics.get(parent_id)
            if not parent:
                issues.append(f"unknown-topic={parent_id}")
                parent_text = ""
            else:
                parent_path, parent_text = parent
                if not re.search(r"^###\s+Q-consumer register\s*$", parent_text, re.I | re.M):
                    issues.append(f"topic-has-no-q-consumer-register={parent_path.name}")
        if not entry.name.startswith(f"S-{entry_family}-"):
            issues.append(f"entry-filename-does-not-match-{entry_family.lower()}")
        if not trace_ids:
            issues.append("consumer-trace-has-no-q-id")
        elif parent_text and not trace_ids.issubset(q_ids(parent_text)):
            issues.append("consumer-trace-not-in-parent-register=" + ",".join(sorted(trace_ids - q_ids(parent_text))))

        binding = section(text, "bank binding")
        state_match = re.search(r"^\*\*state\*\*:\s*([^\s]+)", binding, re.I | re.M)
        state = state_match.group(1).strip().lower() if state_match else ""
        if state not in STATES:
            issues.append("invalid-state=" + (state or "missing"))
        executor = section(text, "q-executor")
        answer = section(text, "a-executor")
        if not is_substantive(executor):
            issues.append("empty-q-executor")
        if state in {"read", "answered-local"} and not is_substantive(answer):
            issues.append("resolved-entry-has-empty-a-executor")
        if re.search(r"^###\s+(?:q-executor|q-consumer|a-executor|a-consumer)\b", text, re.I | re.M):
            issues.append("legacy-three-hash-heading")

        if issues:
            print(f"FAIL  {relative}  -- " + "; ".join(issues))
            failed += 1
        else:
            print(f"PASS  {relative}  -- {state}")

    if args.stage and not stage_matches:
        print(f"WARN  no nested entry serves stage '{args.stage}'")
        warned += 1
    print(f"SUMMARY  {checked} entry(s) checked · {failed} fail · {warned} warn")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

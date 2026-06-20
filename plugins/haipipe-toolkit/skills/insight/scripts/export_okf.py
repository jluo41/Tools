#!/usr/bin/env python3
"""Export a haipipe insight base as a small OKF-style bundle.

The source of truth remains examples/<project>/insights/{D,I,K,W}_*/.
This script writes derived files under insights/okf/ by default.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any


LAYER_DIRS = {
    "D": "D_data",
    "I": "I_information",
    "K": "K_knowledge",
    "W": "W_wisdom",
}

OKF_TYPES = {
    "D": "Insight Data",
    "I": "Insight Information",
    "K": "Insight Knowledge",
    "W": "Insight Wisdom",
}

SUMMARY_KEYS = {
    "D": "headline",
    "I": "pattern",
    "K": "claim",
    "W": "rec",
}

W_REC_TYPES = {
    "next_experiment",
    "research_pivot",
    "stop_doing",
    "paper_direction",
}


@dataclass
class Entry:
    path: Path
    rel_path: Path
    body: str
    frontmatter: dict[str, Any]

    @property
    def id(self) -> str:
        return str(self.frontmatter.get("id") or self.path.stem.split("_", 1)[0])

    @property
    def layer(self) -> str:
        return str(self.frontmatter.get("layer") or self.id[:1])

    @property
    def okf_type(self) -> str:
        raw_type = self.frontmatter.get("type")
        if self.layer == "W" and raw_type in W_REC_TYPES:
            return OKF_TYPES["W"]
        return str(raw_type or OKF_TYPES.get(self.layer, "Insight Entry"))

    @property
    def title(self) -> str:
        explicit = self.frontmatter.get("title")
        if explicit:
            return str(explicit)
        match = re.search(r"^#\s+(.+)$", self.body, flags=re.MULTILINE)
        if match:
            return match.group(1).strip()
        return self.path.stem

    @property
    def description(self) -> str:
        explicit = self.frontmatter.get("description")
        if explicit:
            return str(explicit)
        key = SUMMARY_KEYS.get(self.layer)
        if key and self.frontmatter.get(key):
            return str(self.frontmatter[key])
        return self.title


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"[]", ""}:
        return [] if value == "[]" else ""
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("\"'") for item in inner.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if value.isdigit():
        return int(value)
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    data: dict[str, Any] = {}
    current_key: str | None = None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, []).append(parse_scalar(line[4:]))
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            data[key] = []
            current_key = key
        else:
            data[key] = parse_scalar(value)
            current_key = key
    return data, body


def yaml_value(value: Any) -> str:
    if isinstance(value, list):
        return "[" + ", ".join(str(item) for item in value) + "]"
    text = str(value)
    if not text or any(ch in text for ch in [":", "#", "[", "]", "{", "}", ","]):
        return json.dumps(text, ensure_ascii=False)
    return text


def dump_frontmatter(data: dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in data.items():
        lines.append(f"{key}: {yaml_value(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def load_entries(insights_dir: Path) -> list[Entry]:
    entries: list[Entry] = []
    for layer_dir in LAYER_DIRS.values():
        root = insights_dir / layer_dir
        if not root.exists():
            continue
        for path in sorted(root.glob("*.md")):
            if path.name == "INDEX.md":
                continue
            text = path.read_text(encoding="utf-8")
            frontmatter, body = parse_frontmatter(text)
            entries.append(
                Entry(
                    path=path,
                    rel_path=path.relative_to(insights_dir),
                    body=body,
                    frontmatter=frontmatter,
                )
            )
    return entries


def list_value(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def markdown_link(label: str, target: Path | None) -> str:
    if target is None:
        return label
    return f"[{label}]({target.as_posix()})"


def normalize_entry(entry: Entry, id_to_export_path: dict[str, Path]) -> str:
    fm = dict(entry.frontmatter)
    fm["id"] = entry.id
    fm["type"] = entry.okf_type
    fm["layer"] = entry.layer
    fm["title"] = entry.title
    fm["description"] = entry.description

    source_links = []
    for source_id in list_value(fm.get("sources")):
        target = id_to_export_path.get(source_id)
        source_links.append(
            markdown_link(source_id, relative_link(entry.rel_path, target)) if target else source_id
        )

    ref_links = []
    for ref_id in list_value(fm.get("ref_by")):
        target = id_to_export_path.get(ref_id)
        ref_links.append(
            markdown_link(ref_id, relative_link(entry.rel_path, target)) if target else ref_id
        )

    appendix = "\n\n## OKF Links\n\n"
    appendix += "Sources: " + (", ".join(source_links) if source_links else "none") + "\n\n"
    appendix += "Referenced by: " + (", ".join(ref_links) if ref_links else "none") + "\n"
    return dump_frontmatter(fm) + entry.body.rstrip() + appendix + "\n"


def escape_table(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def relative_link(from_path: Path, to_path: Path) -> Path:
    return Path(os.path.relpath(to_path, start=from_path.parent))


def write_index(entries: list[Entry], out_dir: Path) -> None:
    lines = [
        "# OKF Export",
        "",
        "Derived from haipipe `insights/`. Source cards remain authoritative.",
        "",
        "## Entries",
        "",
        "| ID | Type | Title | Description | Source |",
        "|----|------|-------|-------------|--------|",
    ]
    for entry in sorted(entries, key=lambda e: (e.layer, e.id)):
        lines.append(
            "| {id} | {typ} | [{title}]({path}) | {desc} | `{source}` |".format(
                id=entry.id,
                typ=entry.okf_type,
                title=escape_table(entry.title),
                path=entry.rel_path.as_posix(),
                desc=escape_table(entry.description),
                source=entry.rel_path.as_posix(),
            )
        )
    lines.append("")
    (out_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")


def write_graph(entries: list[Entry], out_dir: Path, id_to_path: dict[str, Path]) -> list[str]:
    ids = {entry.id for entry in entries}
    warnings: list[str] = []
    nodes = [
        {
            "id": entry.id,
            "type": entry.okf_type,
            "layer": entry.layer,
            "title": entry.title,
            "description": entry.description,
            "path": id_to_path[entry.id].as_posix(),
            "tags": list_value(entry.frontmatter.get("tags")),
            "status": entry.frontmatter.get("status", "active"),
        }
        for entry in entries
    ]
    edges = []
    for entry in entries:
        for source_id in list_value(entry.frontmatter.get("sources")):
            if source_id in ids:
                edges.append({"source": source_id, "target": entry.id, "label": "supports"})
            else:
                warnings.append(f"{entry.id}: dangling source {source_id}")
        for ref_id in list_value(entry.frontmatter.get("ref_by")):
            if ref_id not in ids:
                warnings.append(f"{entry.id}: dangling ref_by {ref_id}")
    graph = {"nodes": nodes, "edges": edges, "warnings": warnings}
    (out_dir / "graph.json").write_text(
        json.dumps(graph, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return warnings


def resolve_insights_dir(path: Path) -> Path:
    path = path.resolve()
    if path.name == "insights":
        return path
    if (path / "insights").is_dir():
        return path / "insights"
    raise SystemExit(f"Cannot find insights directory from {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_or_insights", type=Path)
    parser.add_argument("--out", type=Path, help="Output directory. Defaults to insights/okf.")
    args = parser.parse_args()

    insights_dir = resolve_insights_dir(args.project_or_insights)
    out_dir = (args.out or (insights_dir / "okf")).resolve()

    entries = load_entries(insights_dir)
    if not entries:
        raise SystemExit(f"No insight entries found under {insights_dir}")

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    id_to_path = {entry.id: entry.rel_path for entry in entries}
    for entry in entries:
        target = out_dir / entry.rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(normalize_entry(entry, id_to_path), encoding="utf-8")

    write_index(entries, out_dir)
    warnings = write_graph(entries, out_dir, id_to_path)

    print(f"OKF export written: {out_dir}")
    print(f"Entries: {len(entries)}")
    print(f"Warnings: {len(warnings)}")
    for warning in warnings:
        print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""The legacy Page-Type compatibility inventory.

`haipipe-page` states the LAW that resolves a page's type. It used to state the
INVENTORY too, by hand, and a hand-written table cannot stay equal to a Python
tuple and a folder listing at the same time. On 260828 the three had drifted
both ways at once: four keys were live on disk with no row in the table
(`question` 4 pages, `roadmap` 2, `ideation` 2, `collection` 2), and six keys
the table called retired were still accepted by the checker. So the inventory
became this script's output and the drift became a finding.

Three sources, and each answers a different question:

    the OWNERS    workflow phase `legacy_page_type` metadata    who maintains it
                  + skills/*/haipipe-*/ `legacy_page_type`      canonical family owner
                  + skills/*/page-types/haipipe-page-for-<key>/ (unmigrated)
                  + paper/workflow-phases/haipipe-paper-<key>/  (paper, 260831)
                  + paper/haipipe-paper-venue/
    the ENGINE    cli/check.py PAGE_TYPE_VALUES                 what resolves
    the BOARDS    every `page-type:` line on disk                what is in use

    python3 pagetypes.py                 the table, on stdout
    python3 pagetypes.py --write         rewrite the block in haipipe-page
    python3 pagetypes.py --check         exit 1 on any drift, print each row
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve()
BOARD_SKILL = HERE.parent.parent            # …/skills/board/haipipe-board
SKILLS = BOARD_SKILL.parent.parent          # …/skills
PAGE_CONTRACT = SKILLS / "board" / "haipipe-page" / "SKILL.md"
sys.path.insert(0, str(BOARD_SKILL))

from src.folder_contract import discover as folder_contracts  # noqa: E402

BEGIN = "<!-- BEGIN GENERATED page-type-inventory -->"
END = "<!-- END GENERATED page-type-inventory -->"

# Keys that resolve by FILENAME rather than by a `page-type:` line, so a
# missing engine entry is correct for them, not a drift.
FILENAME_RESOLVED = {"venue": "QBv<n>-", "stage": "S-<Family>-<unit>-"}


def engine_keys() -> set[str]:
    text = (BOARD_SKILL / "cli" / "check.py").read_text(encoding="utf-8")
    m = re.search(r"PAGE_TYPE_VALUES\s*=\s*\((.*?)\)", text, re.S)
    if not m:
        sys.exit("pagetypes: check.py has no PAGE_TYPE_VALUES tuple")
    return set(re.findall(r'"([^"]+)"', m.group(1)))


def contract_keys() -> dict[str, str]:
    """key -> owning skill set, from phase owners and compatibility folders.

    A migrated family declares the old key on the phase or canonical family
    skill that owns its Page Face. Unmigrated families still ship variants
    under page-types/. Paper's phase skills predate the Folder metadata and
    keep their filename bridge.
    """
    found = {}
    for contract in folder_contracts(SKILLS):
        if contract.legacy_page_type:
            found[contract.legacy_page_type] = contract.path.parents[2].name
    for path in sorted(SKILLS.glob("*/haipipe-*/SKILL.md")):
        front = path.read_text(encoding="utf-8", errors="replace").split("---", 2)
        if len(front) != 3:
            continue
        owner = re.search(
            r"(?m)^  folder_owner:\s*['\"]?canonical['\"]?\s*$", front[1]
        )
        match = re.search(r"(?m)^  legacy_page_type:\s*['\"]?([^'\"\s]+)", front[1])
        if owner and match:
            found[match.group(1)] = path.parents[1].name
    for d in sorted(SKILLS.glob("*/page-types/haipipe-page-for-*")):
        if not d.is_dir() or not (d / "SKILL.md").exists():
            continue
        found[d.name.removeprefix("haipipe-page-for-")] = d.parents[1].name
    for d in sorted(SKILLS.glob("*/workflow-phases/haipipe-paper-*")):
        if not d.is_dir() or not (d / "SKILL.md").exists():
            continue
        found[d.name.removeprefix("haipipe-paper-")] = d.parents[1].name
    venue = SKILLS / "paper" / "haipipe-paper-venue"
    if (venue / "SKILL.md").exists():
        found["venue"] = "paper"
    return found


def board_keys(roots: list[pathlib.Path]) -> dict[str, int]:
    """key -> how many live pages declare it."""
    counts: dict[str, int] = {}
    line = re.compile(r"(?m)^page-type:\s*(\S+)\s*$")
    for root in roots:
        if not root.exists():
            continue
        for md in root.rglob("*.md"):
            if "/.git/" in str(md) or "/board/" in str(md):
                continue
            try:
                head = md.read_text(encoding="utf-8", errors="ignore").split("\n## ", 1)[0]
            except OSError:
                continue
            for key in line.findall(head):
                counts[key] = counts.get(key, 0) + 1
    return counts


def collect(workspace: pathlib.Path):
    engine, contracts = engine_keys(), contract_keys()
    boards = board_keys([workspace / "examples", workspace / "designs",
                         SKILLS / "diagrams"])
    rows = []
    for key in sorted(set(engine) | set(contracts) | set(boards)):
        rows.append({
            "key": key,
            "owner": contracts.get(key, "—"),
            "engine": "✓" if key in engine else "—",
            "pages": boards.get(key, 0),
            "by_filename": FILENAME_RESOLVED.get(key, ""),
        })
    return rows


REGISTRY = SKILLS / "board" / "haipipe-page" / "ref" / "type-registry.md"


def registry_records() -> dict:
    """Load compatibility records once for both drift and law checks."""
    import yaml
    text = REGISTRY.read_text(encoding="utf-8")
    m = re.search(r"```yaml\n(.*?)```", text, re.S)
    if not m:
        sys.exit(f"pagetypes: {REGISTRY.name} has no ```yaml block")
    return yaml.safe_load(m.group(1))


def drift(rows, registry: dict) -> list[str]:
    out = []
    for r in rows:
        key, owner, engine, pages = r["key"], r["owner"], r["engine"], r["pages"]
        standing = (registry.get(key) or {}).get("standing", "")
        registry_owns_law = standing == "record-only"
        registry_tracks_key = standing in {"record-only", "key-only"}
        if owner == "—" and pages and not registry_owns_law:
            out.append(f"{key}: {pages} live page(s) and NO contract ships")
        if owner == "—" and not pages and engine == "✓" and not registry_tracks_key:
            out.append(f"{key}: the engine accepts it, no contract, no page")
        if owner != "—" and engine == "—" and key not in FILENAME_RESOLVED:
            out.append(f"{key}: a contract ships and the engine rejects the key")
    return out


def registry_check(rows, reg: dict) -> list[str]:
    """The registry tooth: every engine key has a record; usage needs law.

    A missing or unparseable registry RAISES (a name that does not resolve
    must raise, GATE-3), never returns an empty problem list.
    """
    out = []
    row_by_key = {r["key"]: r for r in rows}
    for key, r in row_by_key.items():
        rec = reg.get(key)
        if rec is None:
            out.append(f"{key}: engine key has no registry record")
            continue
        standing = rec.get("standing", "")
        if standing == "contract":
            law = rec.get("law", "")
            if not law or not (SKILLS / law).is_dir():
                out.append(f"{key}: registry law path does not resolve: {law!r}")
            if r["owner"] == "—":
                out.append(f"{key}: registry says contract, no shipped folder claims the key")
            for field in ("mode", "evidence", "closing"):
                if not rec.get(field):
                    out.append(f"{key}: contract record missing field {field!r}")
        elif standing == "record-only":
            for field in ("mode", "evidence", "closing"):
                if not rec.get(field):
                    out.append(f"{key}: record-only entry missing field {field!r}")
        elif standing == "key-only":
            if r["pages"]:
                out.append(f"registry-gap {key}: {r['pages']} live page(s), standing key-only — usage without law")
        else:
            out.append(f"{key}: unknown standing {standing!r}")
    for key in reg:
        if key not in row_by_key:
            out.append(f"{key}: registry names a key the engine does not accept")
    return out


def table(rows, counts: bool = True) -> str:
    """The written block omits page COUNTS on purpose.

    A count changes every time anyone writes a page, so embedding it would
    make this contract show as modified on days nobody touched it. The block
    carries the structural facts, which change only when a key is born or
    dies; `--check` and plain stdout carry the counts.
    """
    w = max(len(r["key"]) for r in rows) + 2
    head = f"{'key'.ljust(w)}{'owner'.ljust(14)}{'engine'.ljust(8)}"
    lines = [head + ("pages" if counts else "resolved by"),
             "─" * (w + (27 if counts else 34))]
    for r in rows:
        note = f"filename {r['by_filename']}" if r["by_filename"] else ""
        if counts:
            tail = f"{r['pages'] or '—'}" + (f"   resolved by {note}" if note else "")
        else:
            tail = note or "`page-type:` line"
        lines.append(f"{r['key'].ljust(w)}{r['owner'].ljust(14)}"
                     f"{r['engine'].ljust(8)}{tail}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="rewrite the block in haipipe-page")
    ap.add_argument("--check", action="store_true", help="exit 1 on drift")
    ap.add_argument("--workspace", default=None)
    args = ap.parse_args()

    # …/skills → haipipe-toolkit → plugins → Tools → the workspace checkout
    workspace = pathlib.Path(args.workspace) if args.workspace else SKILLS.parents[3]
    rows = collect(workspace)

    if args.check:
        reg = registry_records()
        problems = drift(rows, reg)
        for p in problems:
            print(f"drift · {p}")
        reg_problems = registry_check(rows, reg)
        for p in reg_problems:
            print(f"registry · {p}")
        print(f"{len(rows)} keys · {len(problems)} drift · {len(reg_problems)} registry")
        return 1 if problems or reg_problems else 0

    if args.write:
        text = PAGE_CONTRACT.read_text(encoding="utf-8")
        if BEGIN not in text or END not in text:
            sys.exit(f"pagetypes: {PAGE_CONTRACT.name} has no generated block markers")
        pre, rest = text.split(BEGIN, 1)
        _, post = rest.split(END, 1)
        body = f"```text\n{table(rows, counts=False)}\n```"
        PAGE_CONTRACT.write_text(f"{pre}{BEGIN}\n{body}\n{END}{post}", encoding="utf-8")
        print(f"wrote {len(rows)} keys into {PAGE_CONTRACT}")
        return 0

    print(f"```text\n{table(rows)}\n```")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

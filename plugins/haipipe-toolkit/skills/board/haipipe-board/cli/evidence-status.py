#!/usr/bin/env python3
"""Generate ``outline/<stem>-evidence.md`` from typed Evidence Items.

The authored half comes from ``<stem>-evidence-items.md``. The generated half
joins each item to its local Page Evidence Item Result and the outline fold.
Status is always derived; nobody types it into either source file.
"""
import argparse
import datetime
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
_spec = importlib.util.spec_from_file_location("live_outline", HERE / "live" / "outline.py")
lo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lo)

from src.item_table import (  # noqa: E402
    CYCLES, EMOJI, ITEM_TYPES, LADDER, bullets, cycle_now, item_status,
    read_items, repo_root, resolve,
)

BEGIN = "# --- evidence-status:begin (generated) ---"
END = "# --- evidence-status:end ---"


def build(page_md: Path) -> str:
    plan, version = lo._latest_plan(page_md)
    if plan is None:
        return ""
    plan_text = plan.read_text(encoding="utf-8", errors="replace")
    page_text = page_md.read_text(encoding="utf-8", errors="replace")
    approved = bool(re.search(r"^approved:\s*✅", plan_text, re.M))
    page_accepted = bool(re.search(r"^accepted:\s*✅", page_text, re.M))
    items = read_items(page_md)
    root, page_dir = repo_root(page_md.parent), page_md.parent
    counts = {word: 0 for word in LADDER}
    statuses, records = [], []

    for item_id, target, bullet_head, item_type, expected, acceptance, folded in bullets(plan_text):
        row = items.get(item_id)
        status = item_status(
            row, folded, page_accepted, plan.stat().st_mtime, root, page_dir,
        )
        counts[status] += 1
        statuses.append(status)
        name = row["name"] if row else bullet_head
        lines = [
            f"### {item_id} · {target} · {name}",
            f"- **Status**: {EMOJI[status]} {status}",
            f"- **Type**: {item_type}",
            f"- **Target**: {target}",
            f"- **Expected**: {(row or {}).get('expected') or expected}",
            f"- **Acceptance**: {(row or {}).get('acceptance') or acceptance or '—'}",
        ]
        if row:
            result = resolve(row["result"], root, page_dir)
            lines.extend([
                f"- **Supporting Runs**: {row['supporting_runs'] or '—'}",
                f"- **PageX Bindings**: {row['pagex_bindings'] or '—'}",
                f"- **Local Input**: {row['local_input'] or '—'}",
                f"- **Local Run**: {row['local_run'] or '—'}",
                f"- **Decide**: {row['decide'] or '☐'}",
                f"- **Has**: {str(result) if result else 'local Result not ready'}",
            ])
        else:
            lines.extend([
                "- **Supporting Runs**: not surveyed yet",
                "- **PageX Bindings**: not surveyed yet",
                "- **Local Input**: not surveyed yet",
                "- **Local Run**: not surveyed yet",
                "- **Decide**: ☐",
                "- **Has**: Evidence Item record missing",
            ])
        records.append("\n".join(lines))

    n_items = len(statuses)
    cycle = cycle_now(approved, items, statuses, n_items)
    now = datetime.datetime.now().strftime("%y%m%d %H%M")
    tally = " · ".join(f"{word} {counts[word]}" for word in LADDER if counts[word]) or "nothing owed"
    type_tally = {kind: 0 for kind in ITEM_TYPES}
    for item_id, *_rest in bullets(plan_text):
        type_tally[item_id.split("-", 2)[1]] += 1
    types = " · ".join(f"{kind} {type_tally[kind]}" for kind in ITEM_TYPES if type_tally[kind])
    decided = sum(1 for row in items.values() if row["decision"])
    head = [
        f"# {page_md.stem} · evidence status",
        f"page: {page_md.stem}",
        "kind: evidence · ⚙️ derived · never hand-edited · Evidence Items joined to local Results",
        "",
        BEGIN,
        f"  EVIDENCE STATUS, MEASURED {now}. GENERATED; do not hand-edit.",
        f"  regenerate: cli/evidence-status.py {page_md.name}",
        "",
        f"plan: {version} · approved: {'✅' if approved else '⬜'} · cycle: {cycle} · items {n_items}"
        f" · decided {decided}/{len(items) or n_items} · {types or 'no types'} · {tally}",
        "",
    ]
    body = "\n\n".join(records) if records else "(no typed Evidence Item in the plan)"
    return "\n".join(head + [body, "", END, ""])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    pages = (
        [
            page_dir / f"{page_dir.name}.md"
            for group in args.target.iterdir()
            if group.is_dir() and not group.name.startswith(("_", ".", "board"))
            for page_dir in group.iterdir()
            if page_dir.is_dir() and (page_dir / f"{page_dir.name}.md").exists()
        ]
        if args.all else [args.target]
    )
    count = 0
    for page in pages:
        text = build(page)
        if not text:
            continue
        output = page.parent / "outline" / f"{page.stem}-evidence.md"
        output.write_text(text, encoding="utf-8")
        count += 1
        shown = output.relative_to(Path.cwd()) if output.is_relative_to(Path.cwd()) else output
        print(f"wrote {shown}")
    print(f"{count} file(s)")


if __name__ == "__main__":
    raise SystemExit(main())

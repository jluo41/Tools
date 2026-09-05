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
from urllib.parse import quote

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
_spec = importlib.util.spec_from_file_location("live_outline", HERE / "live" / "outline.py")
lo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lo)

from src.item_table import (  # noqa: E402
    CYCLES, EMOJI, ITEM_TYPES, LADDER, action_label, bullets, compact_global_run,
    cycle_now, item_status, read_items, readable_global_run, readable_paper_route,
    readable_task, repo_root, resolve, run_registry,
)
from src.common import evidence_run_dir  # noqa: E402

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
            f"- **Label**: {(row or {}).get('label') or 'legacy fallback'}",
            f"- **Target**: {target}",
            f"- **Expected**: {(row or {}).get('expected') or expected}",
            f"- **Acceptance**: {(row or {}).get('acceptance') or acceptance or '—'}",
        ]
        if item_type == "CITE":
            lines.append(f"- **Verified**: {(row or {}).get('verified') or '⬜'}")
        if row:
            result = resolve(row["result"], root, page_dir)
            lines.extend([
                f"- **Supporting Runs**: {row['supporting_runs'] or '—'}",
                f"- **Local Input**: {row['local_input'] or '—'}",
                f"- **Local Run**: {row['local_run'] or '—'}",
                f"- **Decide**: {row['decide'] or '☐'}",
                f"- **Has**: {str(result) if result else 'local Result not ready'}",
            ])
        else:
            lines.extend([
                "- **Supporting Runs**: not surveyed yet",
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


def _map_href(root: Path, stored_path: str, *, base: Path = None) -> str:
    """A Board-root link from Outline's Supporting-Run map to an artifact."""
    if not stored_path:
        return ""
    stored = Path(stored_path)
    candidates = [stored] if stored.is_absolute() else [root / stored]
    if base is not None and not stored.is_absolute():
        candidates.append(base / stored)
    target = next((candidate for candidate in candidates if candidate.exists()), None)
    if target is None:
        return ""
    try:
        relative = target.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return ""
    return "/" + quote(relative + ("/" if target.is_dir() else ""), safe="/")


def _run_ref(family: str, action: str, address: str, registry: dict[str, dict[str, str]],
             root: Path) -> str:
    """One compact, auditable evidence-to-Run reference.

    This reports the outcome of SURVEY.  A ``new-*`` parent has no ``rNN`` and
    stays explicitly unallocated; it is never converted into a fake Run.
    """
    action = (action or "").lower()
    compact = compact_global_run(address)
    route = readable_global_run(compact) if compact else (readable_task(address) or address)
    label = action_label(action) or action or "unspecified"
    if action.startswith("new-"):
        return f"`{route or 'unallocated'}` · {label} · Run not allocated"
    record = registry.get(compact) if compact else None
    if not record:
        return f"`{route or 'unregistered'}` · {label} · Run/Result paths not found"
    run_href = _map_href(root, record.get("ticket", ""))
    result_href = _map_href(root, record.get("result", ""))
    runtime_href = _map_href(root, record.get("runtime", ""))
    route_label = f"[{route}]({run_href})" if run_href else f"`{route}`"
    run_label = "[Run](%s)" % run_href if run_href else "Run path not found"
    result_label = "[Result](%s)" % result_href if result_href else "Result not found"
    runtime_label = " · [Runtime](%s)" % runtime_href if runtime_href else ""
    return (f"{route_label} · {label} · {record.get('label') or 'Unregistered'} · "
            f"{run_label} · {result_label}{runtime_label}")


def _allocated_local(item: dict, local_rows: list[dict], root: Path) -> str:
    """Resolve an authored local binding without inferring one from proximity."""
    declared = item.get("local_run", "")
    address = item.get("address", "")
    for row in local_rows:
        global_id = row.get("global_id") or row["run_id"]
        tokens = (
            global_id, row.get("compact_id", ""), row["run_id"],
            row["ticket"].name, str(row["ticket"]),
        )
        if any(token and token in declared for token in tokens) or address == str(global_id).replace(".", ""):
            run_href = _map_href(root, str(row["ticket"].relative_to(root)))
            page_dir = row["ticket"].parent.parent
            result_href = _map_href(root, str(row.get("result", "")), base=page_dir)
            runtime_href = (_map_href(root, str(row["runtime"].relative_to(root)))
                            if row["runtime"] else "")
            route_label = f"[{global_id}]({run_href})" if run_href else f"`{global_id}`"
            run_label = "[Run](%s)" % run_href if run_href else "Run path not found"
            result_label = "[Result](%s)" % result_href if result_href else "Result not found"
            runtime_label = " · [Runtime](%s)" % runtime_href if runtime_href else ""
            return (f"{route_label} · {row['status']} · {run_label} · "
                    f"{result_label}{runtime_label}")
    if declared.startswith("—"):
        return "planned local Evidence Task · Run not allocated"
    if item.get("action", "").startswith("new-"):
        route = readable_paper_route(address) or address or "unindexed"
        return f"P {route} · new · Run not allocated"
    return f"`{declared or 'not declared'}` · local Run path not found"


def build_run_bindings(page_md: Path) -> str:
    """Project Run lineage into ``outline/evidence/supporting-runs/``.

    The projection contains pointers only: no Run, Result, runtime, log, or
    output is copied into Evidence.  Physical page-local pairs remain at the
    sibling ``runs/`` and ``results/`` roots and external supporting work stays
    in its owning task/discovery tree.
    """
    items = read_items(page_md)
    root = repo_root(page_md.parent)
    registry = run_registry(str(root))
    try:
        from live.runs import local_runs
        local_rows = local_runs(page_md)
    except (ImportError, OSError):
        local_rows = []
    lines = [
        f"# {page_md.stem} · evidence run bindings",
        f"page: {page_md.stem}",
        "kind: evidence-runs · ⚙️ derived · never hand-edited · pointers only",
        "source: outline/*-evidence-items.md + owning task/discovery Runs + page runs/results/",
        "boundary: supporting Runs/Results stay external; local Runs stay in runs/; local Results stay in results/.",
        "",
    ]
    if not items:
        lines.append("(no typed Evidence Item ledger yet)")
    for item in items.values():
        lines.append(f"## {item['item']} · {item['target']} · {item['name']}")
        lines.append("- **Supporting Runs**:")
        support_lines = []
        for raw in (item.get("supporting_runs", "") or "").split(";"):
            parts = [part.strip() for part in raw.split("·")]
            if len(parts) >= 3:
                support_lines.append("  - " + _run_ref(parts[0], parts[1], parts[2], registry, root))
        lines.extend(support_lines or ["  - —"])
        lines.append("- **Local Run**: " + _allocated_local(item, local_rows, root))
        lines.append("- **Local Result**: " + (item.get("result") or "not allocated"))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


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
        bindings = evidence_run_dir(page.parent) / f"{page.stem}-run-bindings.md"
        bindings.parent.mkdir(parents=True, exist_ok=True)
        bindings.write_text(build_run_bindings(page), encoding="utf-8")
        count += 1
        shown = output.relative_to(Path.cwd()) if output.is_relative_to(Path.cwd()) else output
        shown_bindings = (bindings.relative_to(Path.cwd())
                          if bindings.is_relative_to(Path.cwd()) else bindings)
        print(f"wrote {shown}")
        print(f"wrote {shown_bindings}")
    print(f"{count} file(s)")


if __name__ == "__main__":
    raise SystemExit(main())

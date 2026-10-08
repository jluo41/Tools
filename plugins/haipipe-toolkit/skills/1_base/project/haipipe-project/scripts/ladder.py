#!/usr/bin/env python3
"""Audit or update any level of a Project world against the ladder: Block → Job → Task → Run → pass.

    ladder.py audit  <path> [--only] [--quiet]      <path> = a Project, a world, a Block, a Job, a Task or a Run
    ladder.py update <path> [--apply]               dry run unless --apply

The shape rules live in ../ref/ladder.md (its yaml block); this script only reads them.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

LADDER_MD = Path(__file__).resolve().parents[1] / "ref" / "ladder.md"
# the Themes the ladder checks, each by its singular folder and its old plural one (the same table as
# haipipe-page src/themes.py); cowork/ has its own check; paper/, design/, insight/ keep their family layouts
LADDER_WORLDS = ("work", "tasks", "discovery", "discoveries", "labeling", "labelings")
TICKET_EXT = (".sh", ".yaml", ".yml", ".md")
ORDER = {"ok": 0, "debt": 1, "failed": 2}


def load_table() -> dict:
    text = LADDER_MD.read_text(encoding="utf-8")
    block = re.search(r"## The table\s+```yaml\n(.*?)```", text, re.S)
    if not block:
        sys.exit(f"no yaml table in {LADDER_MD}")
    return yaml.safe_load(block.group(1))


T = load_table()
NAMES = {k: re.compile(v) for k, v in T["names"].items()}
ABS = re.compile(T["checks"]["absolute_path"])
HEAVY = T["checks"]["heavy_mb"] * 1024 * 1024


def space_root(start: Path) -> Path:
    for p in (start, *start.parents):
        if (p / "env.sh").is_file() or (p / "AGENTS.md").is_file():
            return p
    return Path.cwd()


@dataclass
class Node:
    path: Path
    level: str
    findings: list = field(default_factory=list)      # (severity, message)
    children: list = field(default_factory=list)

    def add(self, sev: str, msg: str) -> None:
        self.findings.append((sev, msg))

    @property
    def status(self) -> str:
        worst = max((ORDER[s] for s, _ in self.findings), default=0)
        return [k for k, v in ORDER.items() if v == worst][0]


def face_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.is_file() else ""


def field_of(text: str, key: str) -> str:
    m = re.search(rf"(?m)^{re.escape(key)}:[ \t]*([^\s#]+)", text)
    return m.group(1) if m else ""


def family_of(block: Path) -> str:
    text = face_text(block / "board.md")
    fam = field_of(text, "workbench")
    if fam:
        return fam
    if "discovery" in field_of(text, "board-kind") or block.parent.name in ("discovery", "discoveries"):
        return "discovery"
    if block.name.startswith("Labeling-") or block.parent.name in ("labeling", "labelings"):
        return "labeling"
    if block.name.startswith("Paper-") or block.parent.name in ("paper", "papers"):
        return "paper"
    # the special boards are named by their kind (haipipe-board, JL 261008)
    if block.name.startswith(("Insight-", "Prototype-")) or block.parent.name == "insights":
        return "insight"
    if block.name.startswith("Design-") or block.parent.name == "designs":
        return "design"
    return "task"


def fam_rules(fam: str) -> dict:
    return T["families"].get(fam) or {}


def run_kind(name: str, fam: str) -> str:
    if NAMES["hard"].match(name):
        return "hard"
    if NAMES["soft"].match(name):
        return "soft"
    extra = fam_rules(fam).get("hard")
    if extra and re.match(extra, name):
        return "hard"
    return ""


def ladder_dirs(path: Path, level: str, fam: str, child: str | None, node: Node) -> list[Path]:
    """Check which folders sit at this level; return the child folders."""
    rules = T["levels"][level]
    allowed = set(rules["may_hold"]) | set(fam_rules(fam).get(level, []))
    kids = []
    for d in sorted(p for p in path.iterdir() if p.is_dir()):
        if d.name.startswith((".", "_")) and d.name != "_old":
            continue
        if child and NAMES[child].match(d.name):
            kids.append(d)
        elif d.name in allowed:
            continue
        elif d.name in rules.get("debt", {}):
            node.add("debt", rules["debt"][d.name])
        else:
            node.add("debt", f"{d.name}/ is not in the ladder for a {level.capitalize()}")
    return kids


# ── Runs ──────────────────────────────────────────────────────────────────────

def scan_text(node: Node, files: list[Path], root: Path) -> None:
    for f in files:
        if f.is_file() and f.stat().st_size < 400_000:
            if ABS.search(f.read_text(encoding="utf-8", errors="ignore")):
                node.add("failed", f"absolute path in {f.relative_to(root)}")


def scan_heavy(node: Node, result: Path, root: Path) -> None:
    if not result.is_dir():
        return
    for dirpath, dirnames, filenames in os.walk(result):
        for n in dirnames + filenames:
            p = Path(dirpath) / n
            if p.is_symlink():
                if os.path.isabs(os.readlink(p)):
                    node.add("failed", f"symlink to an absolute path: {p.relative_to(root)}")
            elif p.is_file() and p.stat().st_size > HEAVY:
                node.add("failed", f"heavy file in a Result ({p.stat().st_size >> 20} MB): "
                                   f"{p.relative_to(root)} → ProjectResult + heavy.yaml")


def old_tickets(runs: Path) -> list[Path]:
    return sorted(p for p in runs.iterdir()
                  if p.is_file() and p.suffix in TICKET_EXT and not p.name.startswith(("_", "."))
                  and p.name.lower() != "readme.md")


def audit_runs(scope: Node, runs: Path, fam: str, work_task: bool, root: Path) -> None:
    where = scope.level
    results = runs.parent / "results"
    olds = old_tickets(runs)
    if olds:
        stems = sorted({p.stem for p in olds})
        scope.add("debt", f"{len(stems)} Run(s) in the old layout (runs/<run>.* + results/<run>/)")
        for stem in stems:
            kind = run_kind(stem, fam)
            if kind == "hard" and not work_task:
                scope.add("failed", f"hard Run {stem} in a {'Page Task' if where == 'task' else where.capitalize()}")
            if kind == "soft" and NAMES["soft_dated"].match(stem):
                pass                                         # reported once below
            receipts = list((results / stem).glob("runtime.yaml")) if results.is_dir() else []
            scan_text(scope, [p for p in olds if p.stem == stem] + receipts, root)
            scan_heavy(scope, results / stem, root)
        dated = [s for s in stems if NAMES["soft_dated"].match(s)]
        if dated:
            scope.add("debt", f"{len(dated)} soft Run name(s) carry a date (e.g. {dated[0]})")
        unknown = [s for s in stems if not run_kind(s, fam)]
        if unknown:
            scope.add("debt", f"{len(unknown)} Run name(s) neither hard nor soft, need their owner's "
                              f"mapping (e.g. {unknown[0]})")
    for d in sorted(p for p in runs.iterdir() if p.is_dir() and not p.name.startswith((".", "_"))):
        scope.children.append(audit_run(d, fam, work_task, where, root))


def audit_run(d: Path, fam: str, work_task: bool, where: str, root: Path) -> Node:
    node = Node(d, "run")
    name = d.name
    kind = run_kind(name, fam)
    if NAMES["task"].match(name):
        node.add("failed", "a Task folder inside runs/: it belongs beside the Job's other Tasks")
        return node
    if not kind:
        node.add("failed", "name is neither a hard Run (rNN_<slug>) nor a soft one (run-<type>-<target>)")
    if kind == "soft" and NAMES["soft_dated"].match(name):
        node.add("debt", "soft name carries a date; the date belongs in passes/pNN-<MMDD>/")
    tickets = [d / f"{name}{e}" for e in ((".sh", ".yaml", ".yml") if kind == "hard" else (".md",))]
    ticket = next((t for t in tickets if t.is_file()), None)
    if kind and not ticket:
        node.add("failed", f"no ticket ({tickets[0].name})")
    card = {}
    if (d / "run.yaml").is_file():
        card = yaml.safe_load(face_text(d / "run.yaml")) or {}
        if card.get("run") != name:
            node.add("failed", f"run.yaml says run: {card.get('run')}")
        if kind and card.get("kind") != kind:
            node.add("failed", f"run.yaml says kind: {card.get('kind')}, the name says {kind}")
    else:
        node.add("debt", "no run.yaml (update writes it)")
    if kind == "soft" and (d / "result").exists():
        node.add("failed", "a soft Run has no result/: it writes into its scope")
    if kind == "hard" and not work_task:
        node.add("failed", f"a hard Run sits in a {'Page Task' if where == 'task' else where.capitalize()}")
    if kind == "hard" and str(card.get("status", "")) in {"done", "complete", "completed", "success"} \
            and not (d / "result").is_dir():
        node.add("failed", "marked done with no result/")
    keep = set(T["levels"]["run"]["may_hold"]) | {t.name for t in tickets}
    for p in sorted(d.iterdir()):
        if not p.name.startswith(".") and p.name not in keep:
            node.add("debt", f"{p.name} is not in the ladder for a Run")
    scan_text(node, [t for t in [ticket, d / "run.yaml", d / "result" / "runtime.yaml"] if t]
              + sorted(d.glob("passes/*/runtime.yaml")), root)
    scan_heavy(node, d / "result", root)
    return node


# ── Levels ────────────────────────────────────────────────────────────────────

def audit_task(path: Path, fam: str, root: Path, only: bool = False) -> Node:
    node = Node(path, "task")
    face = path / f"{path.name}.md"
    text = face_text(face)
    if not text:
        node.add("debt", f"no face {face.name}")
    work_task = field_of(text, "task-kind") != "page"
    ladder_dirs(path, "task", fam, None, node)
    if (path / "runs").is_dir() and not only:
        audit_runs(node, path / "runs", fam, work_task, root)
    if any("Run(s) in the old layout" in m for _, m in node.findings):
        node.findings = [f for f in node.findings if not f[1].startswith("old layout: results/")]
    return node


def audit_job(path: Path, fam: str, root: Path, only: bool = False) -> Node:
    node = Node(path, "job")
    if not (path / f"{path.name}.md").is_file():
        node.add("debt", f"no face {path.name}.md")
    kids = ladder_dirs(path, "job", fam, "task", node)
    if (path / "runs").is_dir():
        audit_runs(node, path / "runs", fam, False, root)
    if not only:
        node.children += [audit_task(k, fam, root) for k in kids]
    return node


def audit_block(path: Path, root: Path, only: bool = False) -> Node:
    node = Node(path, "block")
    fam = family_of(path)
    if not (path / "board.md").is_file() and not (path / f"{path.name}.md").is_file():
        node.add("debt", "no face (board.md)")
    kids = ladder_dirs(path, "block", fam, "job", node)
    if (path / "runs").is_dir():
        audit_runs(node, path / "runs", fam, False, root)
    if not only:
        node.children += [audit_job(k, fam, root) for k in kids]
    return node


def block_of(path: Path) -> Path | None:
    return next((p for p in (path, *path.parents) if NAMES["block"].match(p.name)), None)


def audit_path(path: Path, root: Path, only: bool = False) -> list[Node]:
    name = path.name
    fam = family_of(block_of(path)) if block_of(path) else "task"
    if path.parent.name == "runs":
        holder = path.parent.parent
        work = NAMES["task"].match(holder.name) and field_of(face_text(holder / f"{holder.name}.md"), "task-kind") != "page"
        where = "task" if NAMES["task"].match(holder.name) else ("job" if NAMES["job"].match(holder.name) else "block")
        return [audit_run(path, fam, bool(work), where, root)]
    if NAMES["task"].match(name):
        return [audit_task(path, fam, root, only)]
    if NAMES["job"].match(name):
        return [audit_job(path, fam, root, only)]
    if NAMES["block"].match(name):
        return [audit_block(path, root, only)]
    worlds = [path] if name in LADDER_WORLDS else [path / w for w in LADDER_WORLDS if (path / w).is_dir()]
    return [audit_block(b, root, only) for w in worlds for b in sorted(w.iterdir())
            if b.is_dir() and NAMES["block"].match(b.name)]


# ── Report ────────────────────────────────────────────────────────────────────

def walk(nodes: list[Node]):
    for n in nodes:
        yield n
        yield from walk(n.children)


def print_tree(nodes: list[Node], root: Path, quiet: bool) -> None:
    def show(n: Node, depth: int, first: bool) -> None:
        if n.level == "run" and not n.findings:
            return
        if quiet and n.status == "ok" and not any(c.findings for c in walk(n.children)):
            return
        label = str(n.path.relative_to(root)) + "/" if first else "  " * depth + n.path.name + "/"
        print(f"{label:<64} {n.status}")
        for sev, msg in n.findings:
            print(f"{'  ' * depth}    {'✗' if sev == 'failed' else '·'} {msg}")
        for c in n.children:
            show(c, depth + 1, False)
    for n in nodes:
        show(n, 0, True)


def print_summary(nodes: list[Node]) -> None:
    counts: dict = {}
    for n in walk(nodes):
        counts.setdefault(n.level, {"ok": 0, "debt": 0, "failed": 0})[n.status] += 1
    for level in ("block", "job", "task", "run"):
        if level in counts:
            c = counts[level]
            print(f"{level:<6} {sum(c.values()):>5}   ok {c['ok']:>5}   debt {c['debt']:>5}   failed {c['failed']:>5}")


# ── Update ────────────────────────────────────────────────────────────────────

def receipt_of(run_dir: Path) -> dict:
    for p in [run_dir / "result" / "runtime.yaml", *sorted(run_dir.glob("passes/*/runtime.yaml"), reverse=True)]:
        if p.is_file():
            try:
                return yaml.safe_load(p.read_text(encoding="utf-8", errors="ignore")) or {}
            except yaml.YAMLError:
                return {}
    return {}


def make_card(run_dir: Path, name: str, kind: str, ticket: str, root: Path, moved_from: list[str] | None = None,
              passes: list[str] | None = None) -> dict:
    r = receipt_of(run_dir) if run_dir.exists() else {}
    rtype = r.get("run_type") or r.get("operation") or r.get("type")
    touched = []
    for t in sorted(run_dir.glob("passes/*/touched.yaml")) if run_dir.exists() else []:
        touched += (yaml.safe_load(t.read_text()) or [])
    card = {
        "run": name, "kind": kind,
        "type": ([rtype] if isinstance(rtype, str) else rtype) or None,
        "scope": str(run_dir.parent.parent.relative_to(root)),
        "target": r.get("target"), "ticket": ticket,
        "skill": r.get("skill"), "agent": r.get("agent"), "signs": r.get("signs"),
        "status": r.get("status"),
        "passes": passes if passes is not None else
        sorted(p.name for p in (run_dir / "passes").iterdir()) if (run_dir / "passes").is_dir() else [],
        "writes": ["result/"] if kind == "hard" else sorted(set(map(str, touched))),
        "feeds": [],
    }
    if moved_from:
        card["moved_from"] = moved_from
    return card


def mmdd_of(path: Path) -> str:
    r = yaml.safe_load(face_text(path / "runtime.yaml")) if (path / "runtime.yaml").is_file() else {}
    for k in ("finished_at", "started_at", "created_at"):
        v = str((r or {}).get(k) or "")
        m = re.match(r"\d{4}-(\d{2})-(\d{2})", v)
        if m:
            return m.group(1) + m.group(2)
    return dt.datetime.fromtimestamp(path.stat().st_mtime).strftime("%m%d")


def plan_runs(runs: Path, fam: str, root: Path) -> tuple[list, list[str]]:
    """Moves for one runs/ folder in the old layout, plus run.yaml for new-layout Runs without one."""
    rel = lambda p: str(p.relative_to(root))
    results = runs.parent / "results"
    steps, skipped = [], []
    groups: dict[str, list] = {}
    for t in old_tickets(runs):
        stem, kind = t.stem, run_kind(t.stem, fam)
        if not kind or (kind == "soft") != (t.suffix == ".md"):
            skipped.append(f"{rel(t)}: name or ticket type needs its owner's mapping, not moved")
            continue
        new = re.sub(r"^(run-[a-z]+)-\d{4}-", r"\1-", stem) if kind == "soft" else stem
        groups.setdefault(new, []).append((t, kind))
    for new, items in sorted(groups.items()):
        dest = runs / new
        if dest.exists():
            skipped.append(f"{rel(dest)} already exists, not moved")
            continue
        kind = items[0][1]
        moves, moved_from, passes = [], [], []
        if kind == "hard":
            for t, _ in items:
                moves.append((t, dest / t.name))
                moved_from.append(rel(t))
            res = results / new
            if res.is_dir():
                moves.append((res, dest / "result"))
                moved_from.append(rel(res))
            ticket = next((t.name for t, _ in items if t.suffix == ".sh"), items[0][0].name)
        else:
            dated = sorted(((re.search(r"^run-[a-z]+-(\d{4})-", t.stem), t) for t, _ in items),
                           key=lambda x: (x[0].group(1) if x[0] else "", x[1].name))
            for i, (m, t) in enumerate(dated, 1):
                res = results / t.stem
                mmdd = m.group(1) if m else (mmdd_of(res) if res.is_dir() else mmdd_of(t))
                pdir = dest / "passes" / f"p{i:02d}-{mmdd}"
                passes.append(pdir.name)
                last = i == len(dated)
                if res.is_dir():                              # the old result folder becomes the pass
                    moves.append((res, pdir))
                    moved_from.append(rel(res))
                moves.append((t, dest / f"{new}.md" if last else pdir / "ask.md"))
                moved_from.append(rel(t))
            ticket = f"{new}.md"
        steps.append(("move", dest, kind, ticket, moves, moved_from, passes if kind == "soft" else []))
    for d in sorted(p for p in runs.iterdir() if p.is_dir() and not p.name.startswith((".", "_"))):
        kind = run_kind(d.name, fam)
        if kind and not (d / "run.yaml").is_file():
            ticket = next((f"{d.name}{e}" for e in (".sh", ".yaml", ".md") if (d / f"{d.name}{e}").is_file()), None)
            steps.append(("card", d, kind, ticket, [], [], None))
    return steps, skipped


def runs_folders(path: Path) -> list[Path]:
    if path.parent.name == "runs":
        return [path.parent]
    if path.name == "runs":
        return [path]
    out = [path / "runs"] if (path / "runs").is_dir() else []
    for dirpath, dirnames, _ in os.walk(path):
        dirnames[:] = [d for d in dirnames if not d.startswith((".", "_")) and d not in
                       {"results", "notebooks", "draft", "src", "sbatch", "scripts", "studio"}]
        if "runs" in dirnames:
            out.append(Path(dirpath) / "runs")
            dirnames.remove("runs")
    return sorted(set(out))


def update(path: Path, root: Path, apply: bool) -> int:
    fam = family_of(block_of(path)) if block_of(path) else "task"
    n_moves = n_cards = 0
    for runs in runs_folders(path):
        steps, skipped = plan_runs(runs, fam, root)
        if not steps and not skipped:
            continue
        print(f"{runs.relative_to(root)}/")
        for s in skipped:
            print(f"    skip  {s}")
        for op, dest, kind, ticket, moves, moved_from, passes in steps:
            if op == "move":
                n_moves += 1
                print(f"    {kind:<4}  → {dest.name}/")
                for a, b in moves:
                    print(f"          mv {a.relative_to(runs.parent)} → {b.relative_to(runs.parent)}")
            else:
                n_cards += 1
                print(f"    card  {dest.name}/run.yaml")
            if apply:
                for a, b in moves:
                    b.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(a), str(b))
                for name in passes or []:
                    (dest / "passes" / name).mkdir(parents=True, exist_ok=True)
                card = make_card(dest, dest.name, kind, ticket, root, moved_from or None, passes)
                (dest / "run.yaml").write_text(yaml.safe_dump(card, sort_keys=False, allow_unicode=True))
    results_left = [r for r in (p.parent / "results" for p in runs_folders(path)) if r.is_dir() and apply
                    and not any(r.iterdir())]
    for r in results_left:
        r.rmdir()
    verb = "done" if apply else "planned (dry run; --apply to do it)"
    print(f"\n{n_moves} Run folder(s) and {n_cards} run.yaml card(s) {verb}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("verb", choices=["audit", "update"])
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--only", action="store_true", help="audit: this level alone, not its children")
    ap.add_argument("--quiet", action="store_true", help="audit: hide folders that are ok all the way down")
    ap.add_argument("--summary", action="store_true", help="audit: counts per level only")
    ap.add_argument("--apply", action="store_true", help="update: do the moves (default: dry run)")
    args = ap.parse_args()
    failed = False
    for raw in args.paths:
        path = Path(raw).resolve()
        root = space_root(path)
        if args.verb == "update":
            update(path, root, args.apply)
            continue
        nodes = audit_path(path, root, args.only)
        if not args.summary:
            print_tree(nodes, root, args.quiet)
            print()
        print_summary(nodes)
        failed |= any(n.status == "failed" for n in walk(nodes))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

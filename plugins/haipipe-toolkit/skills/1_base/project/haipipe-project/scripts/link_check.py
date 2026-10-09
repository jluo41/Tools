#!/usr/bin/env python3
"""Links into results/ or runs/ that do not resolve, in a Project's hand-written Markdown.

    link_check.py <project>... [--save <file>] [--compare <file>] [--list]

Reads Markdown links `](path)`, backticked SPACE paths (`examples-…`) and backticked relative paths, in every
`.md` file of the Project except Results, `passes/`, `notebooks/`, `delivery/`, archives and files marked
generated. A relative path resolves from the file's folder or any folder above it inside the Project (a draft
copy resolves from its Page folder). A link into the `result/` of a Run that exists but has not run yet is
counted apart ("not yet run"), not as broken.

--save writes the broken set; --compare reads an earlier one and reports only what is newly broken. Both
sides are compared in one form (old and new Theme names, `results/<run>` and `runs/<run>/result`, are made
equal), so a move that kept a link working leaves no difference. Exit 1 when --compare finds a new break.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ladder import GENERATED, space_root  # noqa: E402

SKIP = {".git", "result", "results", "passes", "notebooks", "delivery", "_legacy", "_old", "__pycache__",
        "node_modules", ".venv"}
MD = re.compile(r"\]\(([^)\s#]+)")
SPACE_TICK = re.compile(r"`(examples-[^`\s]+)`")
REL_TICK = re.compile(r"`((?:\.\./|\./)?[\w./-]*(?:results|runs)/[\w./-]+)`")
THEMES = r"(tasks|discoveries|papers|insights|designs|labelings|ideations|work|discovery|paper|insight|design|labeling|ideation)"


def key(path: str, target: str) -> str:
    """One form for comparing before and after a move."""
    s = f"{path} → {target}"
    s = re.sub(rf"(^|/){THEMES}/", r"\1<theme>/", s)
    s = re.sub(r"runs/([^/`\s]+)/\1\.sh", r"runs/\1.sh", s)
    s = re.sub(r"(t\d\d_[^/\s]+)/runs/([^/`\s]+)/result", r"\1/results/\2", s)
    s = re.sub(r"runs/([^/`\s]+)/result", r"results/\1", s)
    return s


def not_run(base: Path, target: str) -> bool:
    m = re.match(r"(.*runs/[^/]+)/result(/|$)", target)
    return bool(m) and (base / m.group(1)).is_dir() and not (base / m.group(1) / "result").exists()


def check(project: Path, root: Path, listing: bool = False) -> dict:
    broken, total, pending = set(), 0, 0
    for dirpath, dirnames, files in os.walk(project):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        for fn in files:
            if not fn.endswith(".md"):
                continue
            f = Path(dirpath) / fn
            try:
                text = f.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if GENERATED.search("\n".join(text.splitlines()[:5])):
                continue
            ups = [f.parent, *[a for a in f.parents if project in [a, *a.parents]]]
            found = [(t, ups) for t in MD.findall(text)] + [(t, [root]) for t in SPACE_TICK.findall(text)]
            found += [(t, ups) for t in REL_TICK.findall(text) if not t.startswith("examples-")]
            for t, bases in found:
                if "://" in t or not re.search(r"(^|/)(results|runs)/", t) or any(c in t for c in "<>*{}$"):
                    continue
                total += 1
                if any((b / t).exists() for b in bases):
                    continue
                if any(not_run(b, t) for b in bases):
                    pending += 1
                    continue
                k = key(str(f.relative_to(root)), t)
                broken.add(k)
                if listing:
                    print(f"  broken  {f.relative_to(root)} → {t}")
    return {"total": total, "pending": pending, "broken": sorted(broken)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("projects", nargs="+", type=Path)
    ap.add_argument("--save", type=Path)
    ap.add_argument("--compare", type=Path)
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    out = {"total": 0, "pending": 0, "broken": []}
    for p in a.projects:
        p = p.resolve()
        r = check(p, space_root(p), a.list)
        out["total"] += r["total"]; out["pending"] += r["pending"]; out["broken"] += r["broken"]
    print(f"links into results/ or runs/: {out['total']} · not resolving {len(out['broken'])} · "
          f"into Runs not yet run {out['pending']}")
    if a.save:
        a.save.parent.mkdir(parents=True, exist_ok=True)
        a.save.write_text(json.dumps(out, indent=1))
    if a.compare:
        before = set(json.loads(a.compare.read_text())["broken"])
        new = sorted(set(out["broken"]) - before)
        print(f"newly broken since {a.compare.name}: {len(new)}")
        for k in new:
            print(f"  NEW  {k}")
        return 1 if new else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Rename a Project's Theme folders to their singular names (s01-D28, s01-D29, JL 261007).

    rename_themes.py <project> [--apply]        dry run unless --apply

    tasks/ → work/ · discoveries/ → discovery/ · papers/ → paper/ · insights/ → insight/
    designs/ → design/ · labelings/ → labeling/ · ideations/ → ideation/      (cowork/ unchanged)

1. Move: the folder is renamed on disk, as the ladder's moves are (`git add -A` at commit time records
   renames); a submodule inside, such as a paper repository, moves by `git mv` so .gitmodules follows.
   A pair whose new folder exists is refused.
2. Tickets: in each moved `.sh` ticket, the check that its world folder is named `tasks` (or `labelings`)
   also accepts the new name, and the world's store segment stays as it was (a work/ Run mirrors none).
3. Relink: hand-written text names the new folders. `<Project>/<old>/` anywhere under examples*/ and in
   the SPACE's AGENTS.md and README.md; inside the Project also a bare `<old>/` that starts a path. Never
   inside a Result, `passes/`, `notebooks/`, `delivery/`, `_legacy/`, `_old/`, a file marked generated, or
   a receipt; a run.yaml changes only its `scope:` line (its `moved_from:` is history).

The same pairs as haipipe-page `src/themes.py`; readers accept both names until every SPACE has moved.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ladder import GENERATED, NO_RELINK, TEXT_EXT, space_root  # noqa: E402

PAIRS = [("tasks", "work"), ("discoveries", "discovery"), ("papers", "paper"), ("insights", "insight"),
         ("designs", "design"), ("labelings", "labeling"), ("ideations", "ideation")]
END = r'(?=[/\s"\'`)\]>,;:#|]|$)'
FROZEN = re.compile(r"/(designs?|Design-[^/]+)(/|$)")     # inputs/ there carry a sha256 manifest

TICKET_FIXES = [
    ('[ "$(basename "$TASKS_DIR")" = "tasks" ] || fail_shape "Block must be a direct child of tasks/"',
     'case "$(basename "$TASKS_DIR")" in work|tasks) : ;; *) fail_shape "Block must be a direct child of work/" ;; esac'),
    ('WORLD_SEG=""; [ "$(basename "$TASKS_DIR")" = "tasks" ] || WORLD_SEG="$(basename "$TASKS_DIR")/"',
     'case "$(basename "$TASKS_DIR")" in work|tasks) WORLD_SEG="" ;; *) WORLD_SEG="$(basename "$TASKS_DIR")/" ;; esac'),
    ('case "$(basename "$TASKS_DIR")" in tasks|labelings) :',
     'case "$(basename "$TASKS_DIR")" in work|tasks|labeling|labelings) :'),
]


def repo_root(path: Path) -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=path, capture_output=True, text=True)
    return Path(out.stdout.strip()) if out.returncode == 0 else path


def submodules_under(repo: Path, folder: Path) -> list[str]:
    """Submodule paths (relative to the repository) inside `folder`."""
    gm = repo / ".gitmodules"
    if not gm.is_file():
        return []
    out = subprocess.run(["git", "config", "-f", str(gm), "--get-regexp", r"^submodule\..*\.path$"],
                         cwd=repo, capture_output=True, text=True).stdout.split("\n")
    rel = os.path.relpath(folder, repo)
    paths = [line.split(" ", 1)[1] for line in out if " " in line
             and (line.split(" ", 1)[1] + "/").startswith(rel + "/")]
    # only a real submodule (a gitlink in the index); a stale .gitmodules entry is left to its owner
    return [s for s in paths if subprocess.run(["git", "ls-files", "--stage", "--", s], cwd=repo,
                                               capture_output=True, text=True).stdout.startswith("160000")]


def merge_move(old: Path, new: Path) -> None:
    """Move old/ onto new/ on disk; where new/ exists already (a submodule moved first), merge into it."""
    if not new.exists():
        old.rename(new)
        return
    for child in sorted(old.iterdir()):
        target = new / child.name
        if target.exists():
            if child.is_dir() and target.is_dir():
                merge_move(child, target)
            continue
        child.rename(target)
    try:
        old.rmdir()
    except OSError:
        print(f"  left behind in {old}: {[c.name for c in old.iterdir()]}")


def move(project: Path, old: Path, new: Path, apply: bool) -> None:
    """Submodules inside move with `git mv` (their .gitmodules path follows); the rest is renamed on disk,
    like the ladder's own moves: `git add -A` at commit time records them as renames."""
    repo = repo_root(project)
    subs = submodules_under(repo, old)
    print(f"  mv {old.name}/ → {new.name}/" + (f"   ({len(subs)} submodule(s) by git mv)" if subs else ""))
    if not apply:
        return
    for s in subs:
        dest = Path(os.path.relpath(new, repo)) / Path(s).relative_to(os.path.relpath(old, repo))
        (repo / dest).parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "mv", s, str(dest)], cwd=repo, check=True)
    if old.exists():
        merge_move(old, new)


def patch_tickets(world: Path, apply: bool) -> int:
    n = 0
    for t in world.rglob("*.sh"):
        if any(p in ("_legacy", "_old", "result", "results", "passes") for p in t.relative_to(world).parts):
            continue
        try:
            text = t.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        new = text
        for a, b in TICKET_FIXES:
            new = new.replace(a, b)
        if new != text:
            n += 1
            if apply:
                t.write_text(new, encoding="utf-8")
    return n


def rules_for(project: Path, olds: list[tuple[str, str]]) -> list[tuple[re.Pattern, str, Path | None]]:
    rules = []
    pn = re.escape(project.name)
    for old, new in olds:
        rules.append((re.compile(rf'(?<![\w-]){pn}/{old}{END}'), f"{project.name}/{new}", None))
        rules.append((re.compile(rf'(?<![\w-])(?<![a-z0-9_-]/){old}/'), f"{new}/", project))   # a path, never a word
    return rules


def relink(root: Path, project: Path, rules, apply: bool, listing: bool = False) -> tuple[int, int]:
    files = changes = 0
    tops = sorted(root.glob("examples*")) + [root / "AGENTS.md", root / "README.md"]
    names = "|".join(re.escape(o) for o, _ in PAIRS)
    quick = re.compile(rf"(?:{names})/")

    def one(f: Path) -> None:
        nonlocal files, changes
        if f.suffix.lower() not in TEXT_EXT or f.is_symlink():
            return
        try:
            if f.stat().st_size > 2_000_000:
                return
            text = f.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return
        if not quick.search(text) or GENERATED.search("\n".join(text.splitlines()[:5])):
            return
        if f.name == "run.yaml":                      # only where the Run is now; moved_from is history
            lines, n = text.split("\n"), 0
            for i, line in enumerate(lines):
                if line.startswith("scope:"):
                    for pat, rep, inside in rules:
                        if inside is None or inside in f.parents:
                            line, k = pat.subn(rep, line)
                            n += k
                    lines[i] = line
            new = "\n".join(lines)
        else:
            new, n = text, 0
            for pat, rep, inside in rules:
                if inside is not None and inside not in f.parents:
                    continue
                new, k = pat.subn(rep, new)
                n += k
        if n:
            files += 1
            changes += n
            if listing:
                print(f"    relink  {f.relative_to(root)}  ({n})")
            if apply:
                f.write_text(new, encoding="utf-8")

    for top in tops:
        if top.is_file():
            one(top)
            continue
        for dirpath, dirnames, filenames in os.walk(top):
            here = Path(dirpath)
            dirnames[:] = [d for d in dirnames if d not in NO_RELINK and not d.startswith(".")
                           and not (d == "inputs" and FROZEN.search(str(here)))]   # a Design's frozen inputs
            for fn in filenames:
                one(Path(dirpath) / fn)
    return files, changes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--list", action="store_true", help="name every file the relink would change")
    a = ap.parse_args()
    project = a.project.resolve()
    root = space_root(project)
    print(f"{project.relative_to(root)}/")
    todo = []
    for old, new in PAIRS:
        if not (project / old).is_dir():
            continue
        if (project / new).exists():
            print(f"  resume {old}/ → {new}/: {new}/ exists; what is left in {old}/ merges into it")
        todo.append((old, new))
    for old, new in todo:
        move(project, project / old, project / new, a.apply)
    # Tickets and references follow every Theme on its new name, also one moved by an earlier pass
    # (both steps are idempotent).
    named = [(o, n) for o, n in PAIRS if (o, n) in todo or (project / n).is_dir()]
    tickets = 0
    for o, n in named:
        world = project / n if (a.apply or not (project / o).is_dir()) else project / o
        tickets += patch_tickets(world, a.apply)
    files, changes = relink(root, project, rules_for(project, named), a.apply, a.list)
    verb = "done" if a.apply else "planned (dry run; --apply to do it)"
    print(f"  {len(todo)} Theme folder(s), {tickets} ticket(s) patched, {changes} reference(s) in {files} file(s) {verb}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

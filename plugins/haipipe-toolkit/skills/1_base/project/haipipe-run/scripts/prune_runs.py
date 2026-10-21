"""List the hard Runs of a scope that mean nothing now, and delete them on --apply (haipipe-run, JL 261019:
"we will just keep the meaningful runs").

    python prune_runs.py <Task, Job or Block folder>                       # dry run: every Run's verdict
    python prune_runs.py <scope> --apply                                   # delete the Runs marked prune
    python prune_runs.py <scope> --apply --only t03/r02_<slug> r05_<slug>  # delete these candidates only
    python prune_runs.py <scope> --apply --to-old                          # move them to work/_old/ instead

Verdicts. A hard Run (`runs/rNN_<slug>/`) is keep, prune or check.
- A candidate: another Run of its Task names it in `supersedes:`, its card says `status: superseded`, or it never
  ran and is not open (planned, proposed, queued, running, waiting, held, blocked).
- Ran: its `result/` holds a file, or an output path its config names (`output_dir`, `output`, `store`, ...) holds
  files. A Run with nothing here whose config names a `_WorkSpace/` or absolute path is check, not prune: it may have
  written to a store this machine does not hold, so a person looks and uses `--only`.
- Pruned only when nothing in use reads it. Readers: a config, ticket or run card of a Run that stays and was not
  replaced; code that names its Task and the Run (or globs its Task's config folder); a Page outside its Task.
  Not readers: its own folder and config, other pruned or replaced Runs' files (frozen inputs), `supersedes:` lines,
  receipts (`result/`, `passes/`), its Task's page and Studio faces (listed to update), a line that names another
  Task's Run of the same name.
- A current Run is never a candidate.

--apply deletes each pruned Run's folder, its config and its orphan companion configs (`scripts/config/*_rNN.*` that
nothing else names). It marks `status: superseded` on any Run a deleted Run had replaced, so the chain is not lost.
It refuses a Run git does not hold, at its path or at its `moved_from:` path, unless --untracked-ok. `--only` takes
`<task>/<run>` (a Task folder name or its `tNN`) or a bare name that only one Task holds. Heavy output under
`_WorkSpace/` is listed, never deleted here. --to-old moves each pruned Run and its configs to
`work/_old/<bNN>_pruned_<YYMMDD>/<jNN>_<task>_runs/{runs,config}/` instead of deleting them (JL 261021: a Run git does
not hold, such as a site build left untracked, is kept there, not lost), so it needs no --untracked-ok. Soft Runs (`run-<type>-<target>`) are not touched. A dry run is a
snapshot: one session prunes a scope, and reruns the dry run right before --apply.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

HARD = re.compile(r"^r\d+_[A-Za-z0-9_.-]+$")
OPEN = {"planned", "proposed", "queued", "running", "waiting", "held", "blocked"}
TEXT = {".py", ".sh", ".ps1", ".do", ".yaml", ".yml", ".json", ".toml", ".md", ".R", ".r", ".ipynb"}
SKIP_DIRS = {".git", "__pycache__", "_old", "_archive", "node_modules", ".venv", "board"}
CODE = {".py", ".sh", ".ps1", ".do", ".R", ".r", ".ipynb"}
SUPERSEDES = re.compile(r"^\s*-?\s*supersedes:\s*(.+?)\s*(#.*)?$")
OUT_KEY = re.compile(r"(^|_)(output|outputs|out|store|result_dir|heavy_dir|output_root|output_dir|output_jsonl)($|_)")
TASK_NO = re.compile(r"\b[tT](\d{2})\b")
MAX_BYTES = 5_000_000


def project_root(scope: Path) -> Path:
    """The folder holding project.yaml, else the folder above work/, else the scope."""
    for p in [scope, *scope.parents]:
        if (p / "project.yaml").is_file():
            return p
    for p in [scope, *scope.parents]:
        if p.name == "work":
            return p.parent
    return scope


def space_root(folder: Path) -> Path | None:
    for p in [folder, *folder.parents]:
        if (p / "env.sh").is_file():
            return p
    return None


def card(path: Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, yaml.YAMLError):
        return {}


def leaves(node, key: str = ""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from leaves(v, str(k))
    elif isinstance(node, list):
        for v in node:
            yield from leaves(v, key)
    elif isinstance(node, str):
        yield key, node


class Run:
    def __init__(self, folder: Path):
        self.folder = folder
        self.name = folder.name
        self.number = self.name.split("_", 1)[0]
        self.task = folder.parent.parent
        self.task_no = (m.group(1) if (m := re.match(r"t(\d{2})_", self.task.name)) else None)
        self.configs = [p for p in (self.task / "scripts" / "config").glob(f"{self.name}.*") if p.is_file()]
        result = folder / "result"
        self.ran = result.is_dir() and any(p.is_file() for p in result.rglob("*"))
        status = card(folder / "run.yaml").get("status") or card(result / "runtime.yaml").get("status")
        self.status = str(status).lower() if status else ""
        self.replaced_by: list[str] = []
        self.heavy = card(result / "heavy.yaml").get("dir")
        moved = card(folder / "run.yaml").get("moved_from") or []
        self.moved_from = [moved] if isinstance(moved, str) else list(moved)
        # A Run whose config writes to an outside store (an LLM call store, a search store) keeps nothing in
        # result/: it ran when its output path holds files; when the path is not here, nobody can tell from here.
        self.outputs, self.outside = [], False
        if not self.ran:
            base = space_root(folder) or folder
            for cfg in self.configs:
                for key, value in leaves(card(cfg)):
                    if "_WorkSpace/" in value or value.startswith("/"):
                        self.outside = True
                        if OUT_KEY.search(key.lower()):
                            self.outputs.append(value)
            for value in self.outputs:
                path = Path(value) if value.startswith("/") else base / value
                if path.is_file() or (path.is_dir() and any(path.iterdir())):
                    self.ran = True
                    break

    @property
    def replaced(self) -> bool:
        return bool(self.replaced_by) or self.status == "superseded"

    def owns(self, path: Path) -> bool:
        return path in self.configs or self.folder in path.parents

    def supersedes(self) -> list[str]:
        names = []
        for src in [self.folder / "run.yaml", *self.configs]:
            try:
                lines = src.read_text(encoding="utf-8").splitlines()
            except OSError:
                continue
            for line in lines:
                m = SUPERSEDES.match(line)
                if m:
                    names += [t for t in re.split(r"[\s,\[\]'\"]+", m.group(1)) if HARD.match(t)]
        return names


def runs_in(scope: Path) -> list[Run]:
    found = []
    for runs in sorted(scope.rglob("runs")):
        if not runs.is_dir() or SKIP_DIRS & set(runs.relative_to(scope).parts):
            continue
        found += [Run(d) for d in sorted(runs.iterdir()) if d.is_dir() and HARD.match(d.name)]
    return found


def corpus(root: Path) -> list[tuple[Path, str]]:
    files = []
    for path in root.rglob("*"):
        if path.suffix not in TEXT or not path.is_file() or SKIP_DIRS & set(path.relative_to(root).parts):
            continue
        if path.name.endswith(".seed.json") or path.stat().st_size > MAX_BYTES:
            continue
        try:
            files.append((path, path.read_text(encoding="utf-8", errors="ignore")))
        except OSError:
            continue
    return files


def is_receipt(path: Path) -> bool:
    parts = path.parts
    return any(a == "runs" and i + 2 < len(parts) and parts[i + 2] in ("result", "passes")
               for i, a in enumerate(parts))


def is_run_input(path: Path, task: Path) -> bool:
    """A file that tells a Run of this Task what to read: a config, a ticket, a run card."""
    rel = path.relative_to(task).parts
    return (rel[:2] == ("scripts", "config")) or (rel[0] == "runs" and len(rel) == 3)


def references(run: Run, files: list[tuple[Path, str]], skip: list[Run]) -> tuple[list[str], list[str]]:
    """(readers that keep the Run, mentions to update once it goes). `skip`: Runs whose files read nothing now
    (the other pruned Runs, and replaced Runs whose configs are frozen inputs)."""
    wide = re.compile(rf"{re.escape(run.task.name)}/(?:runs/)?{re.escape(run.name)}\b")
    other = re.compile(rf"([A-Za-z0-9_.-]+)/(?:runs/)?{re.escape(run.name)}\b")
    near = re.compile(rf"\b{re.escape(run.name)}\b")
    block = run.task.parent.parent
    # a Page cites a Run by its address, alone or as a range: b03.j01.t02 r08 to r13, b03j01t02r08
    addr = re.compile(rf"\b{block.name[:3]}[.\s]*{run.task.parent.name[:3]}[.\s]*{run.task.name[:3]}[.\s]*"
                      rf"r(\d+)(?:\s*(?:to|–|—|-)\s*r?(\d+))?", re.I)
    number = int(run.number[1:])
    globs = f"{run.task.name}/scripts/config"
    readers, mentions = [], []
    for path, text in files:
        if run.owns(path) or is_receipt(path) or any(o is not run and o.owns(path) for o in skip):
            continue
        inside = run.task in path.parents
        code = path.suffix in CODE and run.task.name in text      # code that builds the path from two names
        if code and globs in text and "glob(" in text and run.configs:
            line = next(i for i, ln in enumerate(text.splitlines(), 1) if globs in ln)
            readers.append(f"{path}:{line} (globs this Task's configs)")
            continue
        cited = [m for m in addr.finditer(text) if int(m.group(1)) <= number <= int(m.group(2) or m.group(1))]
        if run.name not in text and not cited:
            continue
        # its own Task page and its own Block's Studio faces list it; a Page elsewhere (a paper's story) reads it
        listing = path == run.task / f"{run.task.name}.md" or (
            "studio" in path.parts and path.suffix == ".md" and block in path.parents)
        best = None
        for i, line in enumerate(text.splitlines(), 1):
            if SUPERSEDES.match(line):
                continue
            if any(int(m.group(1)) <= number <= int(m.group(2) or m.group(1)) for m in addr.finditer(line)):
                reads = not listing
                if best is None or (reads and not best[0]):
                    best = (reads, True, f"{path}:{i}")
                continue
            if run.name not in line:
                continue
            full = bool(wide.search(line))
            if not full:
                if not ((inside or code) and near.search(line)):
                    continue
                if any(m.group(1) not in (run.task.name, "runs") for m in other.finditer(line)):
                    continue                                      # another Task's Run of the same name
                owners = [TASK_NO.findall(line[:m.start()]) for m in near.finditer(line)]
                if all(found and found[-1] != run.task_no for found in owners):
                    continue                                      # `T01 / "r02_..."` names t01's Run
            reads = not listing and (full or (inside and is_run_input(path, run.task)) or (code and not inside))
            if best is None or (reads and not best[0]) or (full and not best[1]):
                best = (reads, full, f"{path}:{i}")
            if reads and full:
                break
        if best:
            (readers if best[0] else mentions).append(best[2])
    return readers, mentions


def verdicts(scope: Path):
    runs = runs_in(scope)
    by_task: dict[Path, dict[str, Run]] = {}
    for r in runs:
        by_task.setdefault(r.task, {})[r.name] = r
    for r in runs:
        for old in r.supersedes():
            if old in by_task[r.task]:
                by_task[r.task][old].replaced_by.append(r.name)
    reason: dict[Path, str] = {}
    unsure: dict[Path, str] = {}
    for r in runs:
        if r.replaced:
            reason[r.folder] = "replaced by " + (", ".join(r.replaced_by) or "a newer Run (status: superseded)")
        elif not r.ran and r.status not in OPEN:
            if r.outside:      # may have run into a store this machine does not hold: a person checks
                where = r.outputs[0] if r.outputs else "a _WorkSpace path its config names"
                unsure[r.folder] = f"check: no result here, nor at {where}"
            else:
                reason[r.folder] = "never ran"
    files = corpus(project_root(scope))
    frozen = [r for r in runs if r.replaced]
    pruned = set(reason)
    while True:                                    # a reader that is itself pruned does not keep anything
        skip = [r for r in runs if r.folder in pruned] + [r for r in frozen if r.folder not in pruned]
        refs = {r.folder: references(r, files, skip) for r in runs if r.folder in pruned}
        kept = {f for f, (readers, _) in refs.items() if readers}
        if not kept:
            break
        pruned -= kept
    skip = [r for r in runs if r.folder in pruned] + [r for r in frozen if r.folder not in pruned]
    out = {}
    for r in runs:
        if r.folder in pruned:
            out[r.folder] = ("prune", [reason[r.folder]], refs[r.folder][1])
        elif r.folder in reason:
            readers, listings = references(r, files, skip)
            out[r.folder] = ("keep", [reason[r.folder] + ", but read by:", *readers], listings)
        elif r.folder in unsure:
            out[r.folder] = ("check", [unsure[r.folder]], references(r, files, skip)[1])
        else:
            state = r.status or ("ran" if r.ran else "no result")
            out[r.folder] = ("keep", [f"in use ({state})"], [])
    return runs, out, files


def in_git(run: Run) -> bool:
    """git holds the Run at its path, or at a `moved_from:` path, in HEAD."""
    try:
        top = Path(subprocess.run(["git", "-C", str(run.folder), "rev-parse", "--show-toplevel"], text=True,
                                  capture_output=True, check=True).stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    paths = [str(run.folder.relative_to(top))]
    for old in run.moved_from:
        old = str(old)
        hit = old.find(top.name + "/")
        paths.append(old[hit + len(top.name) + 1:] if hit >= 0 else old)
    for p in paths:
        listed = subprocess.run(["git", "-C", str(top), "ls-tree", "-r", "--name-only", "HEAD", "--", p],
                                text=True, capture_output=True).stdout.strip()
        if listed:
            return True
    return False


def companions(run: Run, files: list[tuple[Path, str]]) -> list[Path]:
    """`scripts/config/*_rNN.*` beside the Run's config that nothing but the Run's own files names."""
    found = []
    for p in (run.task / "scripts" / "config").glob(f"*_{run.number}.*"):
        if p in run.configs or not p.is_file():
            continue
        if not any(p.name in text for f, text in files if f != p and not run.owns(f)):
            found.append(p)
    return found


def mark_superseded(run: Run) -> None:
    path = run.folder / "run.yaml"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    new, n = re.subn(r"^status:.*$", "status: superseded", text, count=1, flags=re.M)
    path.write_text(new if n else text.rstrip("\n") + "\nstatus: superseded\n", encoding="utf-8")


def old_home(run: Run) -> Path:
    """Where --to-old keeps a pruned Run: work/_old/<bNN>_pruned_<YYMMDD>/<jNN>_<task>_runs/ (the b01 layout, 261021)."""
    job = run.task.parent
    block = job.parent
    work = next((p for p in [block, *block.parents] if p.name == "work"), block.parent)
    batch = work / "_old" / f"{block.name.split('_')[0]}_pruned_{dt.date.today():%y%m%d}"
    if not (batch / "README.md").is_file():
        batch.mkdir(parents=True, exist_ok=True)
        (batch / "README.md").write_text(
            f"# {block.name}: Runs pruned on {dt.date.today()}\n\nMoved here by haipipe-run prune_runs.py --to-old: each "
            "was replaced or never ran, and nothing in use reads it. A folder is `<jNN>_<task>_runs/` with the Run under "
            "`runs/` and its configs under `config/`. Delete a folder once nobody needs it.\n", encoding="utf-8")
    return batch / f"{job.name.split('_')[0]}_{run.task.name}_runs"


def pick(runs: list[Run], out: dict, names: list[str]) -> tuple[list[Run], list[str]]:
    chosen, notes = [], []
    for name in names:
        task, _, bare = name.rpartition("/")
        hits = [r for r in runs if r.name == bare and (not task or r.task.name == task
                                                       or r.task.name.startswith(task + "_"))]
        hits = [r for r in hits if out[r.folder][0] in ("prune", "check") or r.replaced]
        if not hits:
            notes.append(f"{name}: not a candidate (current, open, or not found), left alone")
        elif len(hits) > 1:
            notes.append(f"{name}: in {len(hits)} Tasks ({', '.join(r.task.name for r in hits)}); "
                         "name it as <task>/<run>, left alone")
        else:
            chosen += hits
    return chosen, notes


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("scope", type=Path)
    ap.add_argument("--apply", action="store_true", help="delete the Runs marked prune (or those --only names)")
    ap.add_argument("--only", nargs="*", default=None, help="delete only these candidates: <task>/<run> or <run>")
    ap.add_argument("--untracked-ok", action="store_true", help="allow deleting a Run git does not hold")
    ap.add_argument("--to-old", action="store_true", help="move the pruned Runs to work/_old/ instead of deleting them")
    a = ap.parse_args(argv)
    scope = a.scope.resolve()
    if not scope.is_dir():
        print(f"no such folder: {scope}", file=sys.stderr)
        return 2
    runs, out, files = verdicts(scope)
    if not runs:
        print("no hard Runs under", scope)
        return 0
    root = project_root(scope)
    rel = (lambda s: str(Path(s).relative_to(root)) if s.startswith(str(root)) else s)
    task = None
    for r in runs:
        if r.task != task:
            task = r.task
            print(f"\n{task.relative_to(root)}")
        verdict, why, _ = out[r.folder]
        mark = {"prune": "🗑️ prune", "check": "❓ check"}.get(verdict, "✅ keep ")
        print(f"  {mark}  {r.name:<36} {why[0]}")
        for line in why[1:]:
            print(f"  {'':<46}   {rel(line)}")
    doomed = [r for r in runs if out[r.folder][0] == "prune"]
    if a.only is not None:
        doomed, notes = pick(runs, out, a.only)
        for note in notes:
            print("\n" + note)
    listings = sorted({ln.rsplit(':', 1)[0] for r in doomed for ln in out[r.folder][2]})
    print(f"\n{len(doomed)} to prune of {len(runs)} Runs" + ("" if a.apply else " (dry run; --apply " + ("moves them to work/_old/)" if a.to_old else "deletes)")))
    if listings:
        print("pages and Studio faces that list them, to update after pruning:")
        for ln in listings:
            print("  ", rel(ln))
    heavy = [r.heavy for r in doomed if r.heavy]
    if heavy:
        print("heavy output to remove where it lives (not deleted here):")
        for h in heavy:
            print("  ", h)
    if a.apply:
        gone = {r.folder for r in doomed}
        for r in doomed:
            if not a.untracked_ok and not a.to_old and not in_git(r):
                print(f"refused {r.folder.relative_to(root)}: git holds no copy (commit first, or --untracked-ok)")
                gone.discard(r.folder)
        for r in [r for r in doomed if r.folder in gone]:
            extra = companions(r, files)
            for old in r.supersedes():
                for o in runs:
                    if o.task == r.task and o.name == old and o.folder not in gone and o.status != "superseded":
                        mark_superseded(o)
                        print(f"marked {o.task.name}/{o.name} status: superseded (it was replaced by {r.name})")
            if a.to_old:
                home = old_home(r)
                (home / "runs").mkdir(parents=True, exist_ok=True)
                shutil.move(str(r.folder), str(home / "runs" / r.name))
                for p in [*r.configs, *extra]:
                    (home / "config").mkdir(parents=True, exist_ok=True)
                    shutil.move(str(p), str(home / "config" / p.name))
                print(f"moved {r.folder.relative_to(root)} → {home.relative_to(root)}/runs/{r.name}"
                      + (f" and {len(r.configs) + len(extra)} config" if r.configs or extra else ""))
                continue
            shutil.rmtree(r.folder)
            for p in [*r.configs, *extra]:
                p.unlink()
            print(f"deleted {r.folder.relative_to(root)}"
                  + (f" and {len(r.configs) + len(extra)} config" if r.configs or extra else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

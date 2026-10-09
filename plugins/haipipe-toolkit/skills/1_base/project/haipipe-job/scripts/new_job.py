"""A Job: scaffold one, add a Task slot to it, check its Tasks (haipipe-job, b03 s21, 261007).

    python new_job.py job <block> --slug <job> --title '<title>' [--nn NN | --name <folder>]
                          [--goal '…'] [--close '…'] [--answers Q01] [--dry-run]
    python new_job.py task <job> --slug <task> --title '<title>' [--nn NN | --name <folder>]
                          [--kind page] [--answers Q01.E1] [--dry-run]
    python new_job.py check <job>
    python new_job.py face <job> [--dry-run]

`job` writes `jNN_<job>/jNN_<job>.md`, the Job's face, with an empty `## Tasks` list. `task` makes the
next `tNN_<task>/` with a bare face (title, task-kind, answers) and adds it to the Job's `## Tasks`, in
order; the Task is then built by haipipe-task. `--name` gives a theme's own folder name instead of
jNN_ / tNN_ (a paper's version group or Section), which its Theme.level_patterns must match for the
frame to read it. `check` compares the `## Tasks` list with the Task folders on disk. `face` writes the face of an existing
Job (or, given a Task folder, a bare Task face listing its Runs) that has none, from what is on disk: its title from the folder name, goal and close left open, its Tasks
in folder order with each Task face's own title, and a Job README.md (if any) carried into ## Topic.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SLUG = re.compile(r"^[a-z0-9][a-z0-9_]*$")
SKIP = {"studio", "reports", "runs", "delivery", "src", "sbatch", "draft", "scripts", "results", "_old"}


def face(folder: Path) -> Path | None:
    for name in (folder.name + ".md", "board.md"):
        if (folder / name).is_file():
            return folder / name
    return None


def kids(folder: Path) -> list[Path]:
    """Direct child folders that carry a face of their own name: a Block's Jobs, a Job's Tasks."""
    return [p for p in sorted(folder.iterdir()) if p.is_dir() and p.name not in SKIP
            and not p.name.startswith((".", "_")) and (p / (p.name + ".md")).is_file()]


def _next(folder: Path, letter: str) -> int:
    used = [int(m.group(1)) for p in folder.iterdir() if p.is_dir() for m in [re.match(rf"^{letter}(\d+)_", p.name)] if m]
    return max(used) + 1 if used else 1


def _folder(parent: Path, letter: str, slug: str, nn: int | None, name: str) -> tuple[Path, str]:
    """(the new folder, its number label) — jNN_<slug> / tNN_<slug>, or a theme's own name."""
    if not parent.is_dir():
        raise ValueError(f"{parent}: no such folder")
    if name:
        if "/" in name or name.startswith((".", "_")):
            raise ValueError(f"name {name!r}: one folder name, not hidden")
        folder, label = parent / name, name
    else:
        if not SLUG.match(slug):
            raise ValueError(f"slug {slug!r}: lower-case letters, digits and _ only")
        nn = nn if nn is not None else _next(parent, letter)
        if any(re.match(rf"^{letter}0*{nn}_", p.name) for p in parent.iterdir() if p.is_dir()):
            raise ValueError(f"{letter}{nn:02d}_ is taken in {parent.name}/")
        folder, label = parent / f"{letter}{nn:02d}_{slug}", f"{letter}{nn:02d}"
    if folder.exists():
        raise ValueError(f"{folder.name} exists")
    return folder, label


def new_job(block: Path, slug: str, title: str, nn: int | None = None, name: str = "", goal: str = "",
            close: str = "", answers: str = "", dry_run: bool = False) -> Path:
    if not face(block):
        raise ValueError(f"{block}: no Block face (board.md)")
    folder, label = _folder(block, "j", slug, nn, name)
    lines = [f"# {label} · {title}", "", f"goal: {goal or '<what this Job delivers>'}",
             f"close: {close or '<what must be true for this Job to close>'}"]
    if answers:
        lines.append(f"answers: {answers}")
    lines += ["", "## Topic", "", "<Why these Tasks belong to one Job: their shared inputs, code or question.>", "",
              "## Tasks", "", "<!-- in order; new_job.py task adds each -->", ""]
    md = folder / f"{folder.name}.md"
    if not dry_run:
        folder.mkdir()
        md.write_text("\n".join(lines), encoding="utf-8")
    return md


def add_task(job: Path, slug: str, title: str, nn: int | None = None, name: str = "", kind: str = "",
             answers: str = "", dry_run: bool = False) -> Path:
    jmd = face(job)
    if not jmd or jmd.name == "board.md":
        raise ValueError(f"{job}: no Job face ({job.name}.md)")
    folder, label = _folder(job, "t", slug, nn, name)
    lines = [f"# {label} · {title}", ""]
    if kind:
        lines.append(f"task-kind: {kind}")
    if answers:
        lines.append(f"answers: {answers}")
    lines += ["", "<Built by haipipe-task: its Task Page from the task kind's template.>", ""]
    md = folder / f"{folder.name}.md"
    if dry_run:
        return md
    folder.mkdir()
    md.write_text("\n".join(lines), encoding="utf-8")
    text = jmd.read_text(encoding="utf-8")
    entry = f"{len(listed(text)) + 1}. {folder.name} · {title}"
    m = re.search(r"(?ms)^## Tasks[ \t]*\n(.*?)(?=^## |\Z)", text)
    if m:
        body = m.group(1).rstrip("\n")
        new = (body + "\n" if body.strip() else "\n") + entry + "\n\n"
        text = text[:m.start(1)] + new + text[m.end(1):]
    else:
        text = text.rstrip("\n") + f"\n\n## Tasks\n\n{entry}\n"
    jmd.write_text(text, encoding="utf-8")
    return md


def _title(md: Path) -> str:
    """A face's own title: its first `# ` heading without a leading `tNN ·` / `jNN ·` label."""
    for line in md.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("# "):
            return re.sub(r"^[a-z]\d+\s*[·:-]\s*", "", line[2:].strip())
    return ""


def write_face(job: Path, dry_run: bool = False) -> Path | None:
    """The face of an existing Job without one; None when it already has its face."""
    md = job / f"{job.name}.md"
    if md.is_file():
        return None
    if re.match(r"^t\d+_", job.name):              # an existing Task with no face: a bare face, as add_task writes
        title = job.name.split("_", 1)[1].replace("_", " ")
        runs = sorted(p.name for p in (job / "runs").iterdir() if p.is_dir()) if (job / "runs").is_dir() else []
        lines = [f"# {job.name[:3]} · {title}", "", "state: open", "",
                 "<Built by haipipe-task: its Task Page from the task kind's template.>", ""]
        if runs:
            lines += ["## Runs", ""] + [f"- `runs/{r}/`" for r in runs] + [""]
        if not dry_run:
            md.write_text("\n".join(lines), encoding="utf-8")
        return md
    m = re.match(r"^([a-z]\d+)_(.+)$", job.name)
    label, title = (m.group(1), m.group(2).replace("_", " ")) if m else (job.name, job.name)
    readme = job / "README.md"
    topic = ""
    if readme.is_file():
        body = readme.read_text(encoding="utf-8", errors="replace").strip().splitlines()
        topic = "\n".join(body[1:] if body and body[0].startswith("# ") else body).strip()
    tasks = [f"{i}. {k.name} · {_title(k / (k.name + '.md')) or k.name}" for i, k in enumerate(kids(job), 1)]
    lines = [f"# {label} · {title}", "", "goal: open", "close: open", "", "## Topic", "",
             topic or "open: why these Tasks belong to one Job is not written yet.", "", "## Tasks", ""]
    lines += tasks + [""]
    if not dry_run:
        md.write_text("\n".join(lines), encoding="utf-8")
    return md


def listed(text: str) -> list[str]:
    """The Task folder names the Job face's `## Tasks` list names, in its order."""
    m = re.search(r"(?ms)^## Tasks[ \t]*\n(.*?)(?=^## |\Z)", text)
    body = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S) if m else ""
    return re.findall(r"(?m)^\s*(?:\d+\.|[-*])\s+`?([^\s`·]+?)/?`?(?:\s|$)", body)


def check(job: Path) -> list[str]:
    """What is off between the Job's `## Tasks` list and its Task folders; [] when they agree."""
    jmd = face(job)
    if not jmd:
        return [f"{job.name}: no face ({job.name}.md)"]
    names = listed(jmd.read_text(encoding="utf-8"))
    on_disk = [p.name for p in kids(job)]
    out = [f"## Tasks names {n}, which is not a Task folder here" for n in names if n not in on_disk]
    out += [f"{n}/ is not in ## Tasks" for n in on_disk if n not in names]
    dup = sorted({n for n in names if names.count(n) > 1})
    out += [f"## Tasks names {n} twice" for n in dup]
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for cmd, where in (("job", "block"), ("task", "job")):
        p = sub.add_parser(cmd)
        p.add_argument(where, type=Path)
        p.add_argument("--slug", default="")
        p.add_argument("--title", required=True)
        p.add_argument("--nn", type=int)
        p.add_argument("--name", default="", help="a theme's own folder name instead of jNN_ / tNN_")
        p.add_argument("--answers", default="")
        p.add_argument("--dry-run", action="store_true")
        if cmd == "job":
            p.add_argument("--goal", default="")
            p.add_argument("--close", default="")
        else:
            p.add_argument("--kind", default="", help="task-kind, e.g. page")
    p = sub.add_parser("check")
    p.add_argument("job", type=Path)
    p = sub.add_parser("face")
    p.add_argument("job", type=Path)
    p.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    try:
        if a.cmd == "face":
            md = write_face(a.job, a.dry_run)
            print(f"{a.job.name}: has its face" if md is None else ("would write " if a.dry_run else "") + str(md))
            return 0
        if a.cmd == "check":
            found = check(a.job)
            print("\n".join(found) or f"{a.job.name}: ## Tasks and its Task folders agree")
            return 1 if found else 0
        if a.cmd == "job":
            md = new_job(a.block, a.slug, a.title, a.nn, a.name, a.goal, a.close, a.answers, a.dry_run)
        else:
            md = add_task(a.job, a.slug, a.title, a.nn, a.name, a.kind, a.answers, a.dry_run)
    except ValueError as err:
        print(f"refused: {err}", file=sys.stderr)
        return 2
    print(("would write " if a.dry_run else "") + str(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())

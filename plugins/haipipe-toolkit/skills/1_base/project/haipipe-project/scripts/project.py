#!/usr/bin/env python3
"""audit and update at Project level: bring a Project onto the current contract and ladder (fn/audit.md,
fn/update.md).

    project.py audit  <project>... | --all [--root <SPACE>]              read-only: every finding, the step that fixes it
    project.py update <project>... | --all                               dry run of every step, and what a person decides
    project.py update <project>... --apply [--steps a,b] [--state DIR]   run the steps in order; never commits

The steps, in the order update --apply runs them (each is skipped when audit finds nothing for it):

    tools    gate: the Tools this SPACE runs must read the new layout first (else --apply stops)
    root     README.md + project.yaml from what is on disk (mission and state left "open" when unknown)
    themes   Theme folders to their singular names (rename_themes.py)
    convert  a Job-centred v0.8.1 Job (scripts/<tNN>/, runs/<tNN>/) into Task folders, and the v0.8.1
             ticket header inside a Task folder rewritten to find its Task from its own path
    runs     one folder per Run, per Block (ladder.py update: move, card, ticket patch, relink, tidy)
    faces    a missing Block, Job or Task face, written from disk (goal, close, state left open)
    verify   root and ladder audits, the ticket probe, and the link check against the snapshot taken first

A person decides what audit marks "person": an old root folder's destination, a folder in a world that is
not a Block, a heavy file, an absolute path in a new receipt, a Run name neither hard nor soft. --apply never
guesses those, never edits a Result, a receipt, a frozen Design input, an archive or a generated file, never
runs a Run, and never commits.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import audit_projects as AP  # noqa: E402
import ladder as L  # noqa: E402
import link_check as LC  # noqa: E402
import probe_tickets as PT  # noqa: E402
import rename_themes as RT  # noqa: E402

STEPS = ["tools", "root", "themes", "convert", "runs", "faces"]
SKILLS = HERE.parents[3]                    # …/skills (1_base/project/haipipe-project/scripts → skills)
TEMPLATE = SKILLS / "1_base/task/haipipe-task/ref/run-sh-template.sh"
THEMES_PY = SKILLS / "1_base/page/haipipe-page/src/themes.py"
NEW_JOB = SKILLS / "1_base/project/haipipe-job/scripts/new_job.py"
BOARD_SYNC = SKILLS / "2_theme/discovery/haipipe-discovery/scripts/board_sync.py"
V081 = "Canonical haipipe-task v0.8.1 execution context"


@dataclass
class Finding:
    step: str            # tools · root · themes · convert · runs · faces · person
    where: str
    what: str


@dataclass
class Report:
    project: Path
    findings: list[Finding] = field(default_factory=list)

    def by_step(self) -> dict[str, list[Finding]]:
        out: dict[str, list[Finding]] = {}
        for f in self.findings:
            out.setdefault(f.step, []).append(f)
        return out


# ── check ─────────────────────────────────────────────────────────────────────

def tools_findings() -> list[Finding]:
    """The Tools gate and contract drift: the decided Theme names against what the contract reads."""
    out = []
    t = TEMPLATE.read_text(encoding="utf-8") if TEMPLATE.is_file() else ""
    if "runs/$RUN_NAME/result" not in t:
        out.append(Finding("tools", rel_tools(TEMPLATE), "the Ticket template does not write runs/<run>/result/"))
    if "work|tasks" not in t:
        out.append(Finding("tools", rel_tools(TEMPLATE), "the Ticket template does not accept a work/ Theme folder"))
    if THEMES_PY.is_file():
        decided = set(re.findall(r'\(\s*"\w+",\s*"(\w+)",', THEMES_PY.read_text(encoding="utf-8")))
        missing = sorted(decided - set(AP.WORLD_DIRS))
        if missing:
            out.append(Finding("tools", "haipipe-project audit_projects.py",
                               f"contract drift: decided Theme folders {missing} are not worlds in the audit"))
    return out


def rel_tools(p: Path) -> str:
    try:
        return str(p.relative_to(SKILLS.parent))
    except ValueError:
        return str(p)


def job_centred(job: Path) -> bool:
    """A Job in the Job-centred v0.8.1 layout: its Tasks live as scripts/<tNN>/ and runs/<tNN>/."""
    return any(p.is_dir() and re.match(r"t\d{2}_", p.name) for p in (job / "scripts").glob("*")) and \
        any(p.is_dir() and re.match(r"t\d{2}_", p.name) for p in (job / "runs").glob("*"))


def check(project: Path) -> Report:
    rep = Report(project)
    root = L.space_root(project)
    res = AP.audit(project)
    for e in res.errors:
        step = "root" if re.search(r"project\.yaml|README|manifest|mission|id must|profile|git_mode|state|schema", e) \
            else "person"
        rep.findings.append(Finding(step, project.name, e))
    for d in res.debts:
        rep.findings.append(Finding("themes" if "rename pending" in d else "person", project.name,
                                    d if "rename pending" in d else f"legacy root {d}/: its destination is a person's call"))
    for w in L.LADDER_WORLDS:
        world = project / w
        if not world.is_dir():
            continue
        for job in sorted(world.glob("b*/j*")):
            if job.is_dir() and job_centred(job):
                rep.findings.append(Finding("convert", str(job.relative_to(project)),
                                            "Job-centred v0.8.1 layout (scripts/<tNN>/, runs/<tNN>/)"))
        for t in sorted(world.rglob("runs/*/*.sh")):
            if "_legacy" in t.parts or t.parent.name != t.stem:
                continue
            try:
                text = t.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if V081 in text and "HAIPIPE_RUN_FOLDER" not in text:
                rep.findings.append(Finding("convert", str(t.relative_to(project)),
                                            "v0.8.1 ticket header: it would read its Task name as 'runs'"))
    nodes = L.audit_path(project, root)
    for n in L.walk(nodes):
        where = str(n.path.relative_to(project)) if project in n.path.parents or n.path == project else n.path.name
        for sev, msg in n.findings:
            rep.findings.append(Finding(classify(msg, sev), where, msg))
    return rep


def classify(msg: str, sev: str) -> str:
    if re.search(r"no face", msg):
        return "faces"
    if re.search(r"old layout|Run\(s\) in the old layout|no run\.yaml|diagram/ is retired|holds no notebooks|"
                 r"holds no results|workflow/ at a Job|dated soft", msg):
        return "runs"
    if re.search(r"Task folder inside runs/|holds no scripts", msg):
        return "convert"
    return "person"


def print_report(rep: Report, root: Path) -> None:
    groups = rep.by_step()
    state = "clean" if not rep.findings else ", ".join(f"{k} {len(v)}" for k, v in groups.items())
    print(f"{rep.project.relative_to(root)}  ·  {state}")
    for step in STEPS + ["person"]:
        for f in groups.get(step, [])[:8]:
            print(f"    {step:8} {f.where}: {f.what}")
        extra = len(groups.get(step, [])) - 8
        if extra > 0:
            print(f"    {step:8} … and {extra} more")


# ── the steps ─────────────────────────────────────────────────────────────────

def step_root(project: Path, apply: bool) -> str:
    made = []
    if not (project / "project.yaml").is_file():
        readme = project / "README.md"
        mission = "open"
        if readme.is_file():
            para = [l.strip() for l in readme.read_text(encoding="utf-8", errors="replace").splitlines()
                    if l.strip() and not l.startswith(("#", "=", "-", "`", "|"))]
            mission = para[0][:200].replace('"', "'") if para else "open"
        text = "\n".join(["schema: haipipe-project/v1", f"id: {project.name}", "profile: research",
                          f"git_mode: {AP.observed_git_mode(project)}", "state: active",
                          f'mission: "{mission}"', ""])
        made.append("project.yaml")
        if apply:
            (project / "project.yaml").write_text(text)
    if not (project / "README.md").is_file():
        worlds = [d.name for d in sorted(project.iterdir()) if d.is_dir() and d.name in AP.WORLD_DIRS]
        lines = [project.name, "=" * len(project.name), "", "open: the mission is not written yet.", "",
                 "Layout", "------", ""] + [f"    {w}/" for w in worlds] + [""]
        made.append("README.md")
        if apply:
            (project / "README.md").write_text("\n".join(lines))
    return ", ".join(made) or "nothing"


def step_themes(project: Path, apply: bool) -> str:
    args = [sys.executable, str(HERE / "rename_themes.py"), str(project)] + (["--apply"] if apply else [])
    out = subprocess.run(args, capture_output=True, text=True)
    if out.returncode:
        raise RuntimeError(out.stderr.strip().splitlines()[-1] if out.stderr.strip() else "rename_themes failed")
    return out.stdout.strip().splitlines()[-1].strip()


V081_HEAD = re.compile(r'(?ms)^HAIPIPE_JOB_DIR=.*?^HAIPIPE_WORKSPACE_ROOT=[^\n]*\n')
TICKET_HEAD = '''# ladder: one folder per Run (converted from the Job-centred v0.8.1 layout)
HAIPIPE_RUN_FOLDER="$(cd "$(dirname "$0")" && pwd)"
HAIPIPE_TASK_FOLDER="$(cd "${HAIPIPE_RUN_FOLDER}/../.." && pwd)"
HAIPIPE_JOB_DIR="$(cd "${HAIPIPE_TASK_FOLDER}/.." && pwd)"
HAIPIPE_TASK_NAME="$(basename "${HAIPIPE_TASK_FOLDER}")"
HAIPIPE_TASK_DIR="${HAIPIPE_TASK_FOLDER}/scripts"
HAIPIPE_RUN_NAME="$(basename "$0" .sh)"
HAIPIPE_RESULT_DIR="${HAIPIPE_RUN_FOLDER}/result"
HAIPIPE_PROJECT_ROOT="$(cd "${HAIPIPE_JOB_DIR}/../../.." && pwd)"
HAIPIPE_WORKSPACE_ROOT="$(cd "${HAIPIPE_PROJECT_ROOT}/../.." && pwd)"
'''
HELPER_HEAD = '''# ladder: a Task helper, exec'd by a Run ticket; it uses the paths that ticket exported
HAIPIPE_JOB_DIR="${JOB_DIR:?run this through a Run ticket}"
HAIPIPE_TASK_NAME="${TASK_NAME}"
HAIPIPE_TASK_DIR="${TASK_DIR}"
HAIPIPE_RUN_NAME="${RUN_NAME}"
HAIPIPE_RESULT_DIR="${RESULT_DIR}"
HAIPIPE_PROJECT_ROOT="${PROJECT_ROOT}"
HAIPIPE_WORKSPACE_ROOT="${REPO_ROOT}"
'''


def git_tracked(repo: Path, p: Path) -> bool:
    return subprocess.run(["git", "ls-files", "--error-unmatch", str(p)], cwd=repo, capture_output=True).returncode == 0


def mv(repo: Path, a: Path, b: Path, apply: bool) -> None:
    if not apply:
        return
    b.parent.mkdir(parents=True, exist_ok=True)
    tracked = subprocess.run(["git", "ls-files", "--", str(a)], cwd=repo, capture_output=True, text=True).stdout.strip()
    if tracked and subprocess.run(["git", "mv", str(a), str(b)], cwd=repo, capture_output=True).returncode == 0:
        return
    a.rename(b)


def empty_tree(p: Path) -> bool:
    return p.is_dir() and not any(f.is_file() and f.name not in (".gitignore", ".gitkeep", ".DS_Store")
                                  for f in p.rglob("*"))


def convert_job(job: Path, apply: bool) -> int:
    """scripts/<tNN>/ + runs/<tNN>/<run>.sh (+ results/<tNN>/<run>/) → <tNN>/scripts/, <tNN>/runs/<run>/."""
    repo = RT.repo_root(job)
    tasks = sorted(p.name for p in (job / "scripts").iterdir() if p.is_dir() and re.match(r"t\d{2}_", p.name))
    for t in tasks:
        task, src = job / t, job / "scripts" / t
        for f in sorted(src.iterdir()):
            if f.name in ("results", "notebooks") and (f.is_symlink() or empty_tree(f)):
                if apply:
                    if f.is_symlink() and git_tracked(repo, f):
                        subprocess.run(["git", "rm", "-q", "--cached", str(f)], cwd=repo)
                    if f.is_symlink():
                        f.unlink()
                continue
            mv(repo, f, task / ("notebooks" if f.name == "notebooks" else f"scripts/{f.name}"), apply)
        runs = job / "runs" / t
        for tk in sorted(runs.iterdir()) if runs.is_dir() else []:
            if tk.suffix != ".sh" or not re.match(r"^r\d{2}_", tk.stem):
                mv(repo, tk, task / "scripts" / tk.name, apply)
                if apply and tk.suffix == ".sh":
                    h = task / "scripts" / tk.name
                    h.write_text(V081_HEAD.sub(HELPER_HEAD, h.read_text(), count=1))
                continue
            dest = task / "runs" / tk.stem / tk.name
            mv(repo, tk, dest, apply)
            res = job / "results" / t / tk.stem
            if res.is_dir() and not empty_tree(res):
                mv(repo, res, dest.parent / "result", apply)
            if apply:
                x = V081_HEAD.sub(TICKET_HEAD, dest.read_text(), count=1)
                x = x.replace('exec "$(dirname "$0")/_run.sh"', 'exec "$(dirname "$0")/../../scripts/_run.sh"')
                x = x.replace('"$TASK_DIR/results/${RUN_NAME}"', '"$RESULT_DIR"')
                x = x.replace('"$TASK_DIR/notebooks/', '"$TASK_DIR/../notebooks/').replace('"$TASK_DIR/notebooks"', '"$TASK_DIR/../notebooks"')
                dest.write_text(x)
        face = task / f"{t}.md"
        if apply and not face.exists():
            task.mkdir(exist_ok=True)
            face.write_text(f"# {t[:3]} · {t.split('_', 1)[1].replace('_', ' ')}\n\nstate: open\n\n"
                            "Converted from the Job-centred layout: its worker and configs in `scripts/`, "
                            "one folder per Run in `runs/`.\n")
    shared = job / "scripts"
    for left in sorted(shared.iterdir()) if shared.is_dir() else []:
        if left.name not in tasks:
            dest = (job / tasks[0] / "scripts" / left.name) if len(tasks) == 1 else (job / "src" / left.name)
            mv(repo, left, dest, apply)
    if (job / "workflow").is_dir():
        mv(repo, job / "workflow", job / "_old" / "workflow", apply)
    if apply:
        for d in ("runs", "results", "notebooks", "scripts"):
            p = job / d
            if p.is_dir() and empty_tree(p):
                for g in p.rglob(".gitignore"):
                    if git_tracked(repo, g):
                        subprocess.run(["git", "rm", "-q", str(g)], cwd=repo)
                    elif g.exists():
                        g.unlink()
                subprocess.run(["find", str(p), "-depth", "-type", "d", "-empty", "-delete"])
    return len(tasks)


def step_convert(project: Path, apply: bool) -> str:
    jobs = tasks = headers = 0
    for w in L.LADDER_WORLDS:
        for job in sorted((project / w).glob("b*/j*")) if (project / w).is_dir() else []:
            if job.is_dir() and job_centred(job):
                jobs += 1
                tasks += convert_job(job, apply)
        for t in sorted((project / w).rglob("runs/*/*.sh")) if (project / w).is_dir() else []:
            if "_legacy" in t.parts or t.parent.name != t.stem:
                continue
            text = t.read_text(encoding="utf-8", errors="replace")
            if V081 in text and "HAIPIPE_RUN_FOLDER" not in text:
                headers += 1
                if apply:
                    t.write_text(V081_HEAD.sub(TICKET_HEAD.split("\n", 1)[1], text, count=1))
    return f"{jobs} Job(s) → {tasks} Task folder(s); {headers} v0.8.1 ticket header(s)"


def step_runs(project: Path, apply: bool) -> str:
    moved = cards = refs = 0
    for w in L.LADDER_WORLDS:
        for b in sorted((project / w).iterdir()) if (project / w).is_dir() else []:
            if not b.is_dir() or b.name.startswith(("_", ".")):
                continue
            args = [sys.executable, str(HERE / "ladder.py"), "update", str(b)] + (["--apply"] if apply else [])
            out = subprocess.run(args, capture_output=True, text=True)
            if out.returncode:
                raise RuntimeError(f"ladder update {b.name}: {out.stderr.strip()[-300:]}")
            m = re.search(r"(\d+) Run folder\(s\), (\d+) run\.yaml card\(s\), (\d+) reference", out.stdout)
            if m:
                moved += int(m.group(1)); cards += int(m.group(2)); refs += int(m.group(3))
    return f"{moved} Run folder(s), {cards} card(s), {refs} reference(s)"


def block_face(b: Path, apply: bool) -> bool:
    md = b / "board.md"
    if md.exists():
        return False
    if L.family_of(b) == "discovery" and BOARD_SYNC.is_file():
        if apply:
            title = re.sub(r"^b\d+_", "", b.name).replace("_", " ")
            subprocess.run([sys.executable, str(BOARD_SYNC), str(b), "--title", title], capture_output=True)
        return True
    title = re.sub(r"^b\d+_", "", b.name).replace("_", " ")
    spine = "open"
    for ov in sorted((b / "studio").glob("*overview*.txt")) if (b / "studio").is_dir() else []:
        m = re.search(r"(?ms)^Purpose\s*\n(.*?)(?:\n\s*\n|\Z)", ov.read_text(errors="replace"))
        if m:
            spine = " ".join(x.strip() for x in m.group(1).splitlines() if x.strip())
            break
    jobs = []
    for j in sorted(p for p in b.iterdir() if p.is_dir() and re.match(r"^j\d+_", p.name)):
        f = j / f"{j.name}.md"
        t = next((l[2:].strip() for l in f.read_text().splitlines() if l.startswith("# ")), j.name) if f.is_file() else j.name
        jobs.append(f"- {j.name} · {re.sub(r'^j[0-9]+ · ', '', t)}")
    if apply:
        md.write_text("\n".join([f"# {title}", "", "board-kind: task-block", f"spine: {spine}", "close: open", "",
                                 "## Topic", "", spine if spine != "open" else
                                 "open: why these Jobs belong to one Block is not written yet.", "", "## Jobs", ""]
                                + jobs + [""]))
    return True


def step_faces(project: Path, apply: bool) -> str:
    counts = {"Block": 0, "Job": 0, "Task": 0}
    for w in L.LADDER_WORLDS:
        world = project / w
        if not world.is_dir():
            continue
        for b in sorted(p for p in world.iterdir() if p.is_dir() and L.NAMES["block"].match(p.name)):
            for level, pat in (("Task", "j*/t*"), ("Job", "j*")):
                for d in sorted(b.glob(pat)):
                    if not d.is_dir() or (d / f"{d.name}.md").exists() or not L.NAMES[level.lower()].match(d.name):
                        continue
                    counts[level] += 1
                    if apply:
                        subprocess.run([sys.executable, str(NEW_JOB), "face", str(d)], capture_output=True)
            counts["Block"] += block_face(b, apply)
    return ", ".join(f"{v} {k} face(s)" for k, v in counts.items())


STEP_FN = {"root": step_root, "themes": step_themes, "convert": step_convert, "runs": step_runs, "faces": step_faces}


# ── verify ────────────────────────────────────────────────────────────────────

def ladder_failed(project: Path) -> int:
    return sum(1 for n in L.walk(L.audit_path(project, L.space_root(project))) for s, _ in n.findings if s == "failed")


def verify(project: Path, snapshot: Path | None) -> list[str]:
    root = L.space_root(project)
    res = AP.audit(project)
    nodes = L.audit_path(project, root)
    debt = sum(1 for n in L.walk(nodes) for s, _ in n.findings if s == "debt")
    failed = sum(1 for n in L.walk(nodes) for s, _ in n.findings if s == "failed")
    probes = PT.probe_all(project, quiet=True)
    lines = [f"root {res.status}" + (f" ({'; '.join(res.errors + res.debts)[:200]})" if res.status != "ok" else ""),
             f"ladder debt {debt} · failed {failed}",
             f"tickets resolve {probes['resolves']} · gated {probes['gated']} · unexpected {probes['unexpected']}"]
    links = LC.check(project, root)
    if snapshot and snapshot.is_file():
        before = set(json.loads(snapshot.read_text())["broken"])
        new = sorted(set(links["broken"]) - before)
        lines.append(f"links not resolving {len(links['broken'])} (before {len(before)}) · newly broken {len(new)}")
        lines += [f"  NEW  {k}" for k in new[:20]]
    else:
        lines.append(f"links not resolving {len(links['broken'])}")
    return lines


# ── commands ──────────────────────────────────────────────────────────────────

def projects_of(a) -> list[Path]:
    if a.all:
        root = (a.root or Path.cwd()).resolve()
        return sorted(p for top in root.glob("examples*") if top.is_dir() for p in top.iterdir()
                      if p.is_dir() and not p.name.startswith(("_", ".")))
    return [Path(p).resolve() for p in a.projects]


def cmd_audit(a) -> int:
    worst = 0
    tools = tools_findings()
    for f in tools:
        print(f"TOOLS    {f.where}: {f.what}")
    for p in projects_of(a):
        rep = check(p)
        print_report(rep, L.space_root(p))
        worst = max(worst, 1 if rep.findings else 0)
    return 1 if (worst or tools) else 0


def cmd_plan(a) -> int:
    tools = tools_findings()
    for f in tools:
        print(f"TOOLS    {f.where}: {f.what}   → fix Tools first; --apply refuses until then")
    for p in projects_of(a):
        rep = check(p)
        groups = rep.by_step()
        print(f"{p.relative_to(L.space_root(p))}")
        if not rep.findings:
            print("    clean: nothing to do")
            continue
        for step in STEPS[1:]:
            if step in groups or step == "faces":
                try:
                    out = STEP_FN[step](p, False)
                except Exception as err:                       # a plan never stops at one step
                    out = f"cannot plan: {err}"
                if step in groups or not out.startswith("0 Block face(s), 0 Job face(s), 0 Task face(s)"):
                    print(f"    {step:8} {out}   ({len(groups.get(step, []))} finding(s))")
        for f in groups.get("person", []):
            print(f"    decide   {f.where}: {f.what}")
    return 0


def cmd_apply(a) -> int:
    tools = tools_findings()
    if tools:
        for f in tools:
            print(f"REFUSED  {f.where}: {f.what}")
        print("Fix Tools first (fn/update.md § The Tools gate); nothing was changed.")
        return 2
    steps = [s for s in (a.steps.split(",") if a.steps else STEPS[1:]) if s in STEP_FN]
    rc = 0
    for p in projects_of(a):
        state = (a.state or Path(tempfile.gettempdir()) / "haipipe-project-update") / p.name
        state.mkdir(parents=True, exist_ok=True)
        snap = state / "links-before.json"
        if not snap.exists():
            snap.write_text(json.dumps(LC.check(p, L.space_root(p))))
        print(f"{p.relative_to(L.space_root(p))}   (snapshot {snap})")
        base = ladder_failed(p)
        for step in steps:
            if step not in check(p).by_step() and step != "faces":
                continue
            try:
                out = STEP_FN[step](p, True)
            except Exception as err:
                print(f"    {step:8} STOPPED: {err}")
                rc = 1
                break
            now = ladder_failed(p)
            print(f"    {step:8} {out}   · ladder failed {now}")
            if now > base:
                print(f"    {step:8} STOPPED: ladder failures rose from {base} to {now}; see `ladder.py audit`")
                rc = 1
                break
            base = now
        for line in verify(p, snap):
            print(f"    verify   {line}")
    print("Nothing was committed. Review with git status in each repository, then commit with git add -A.")
    return rc


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("verb", choices=["audit", "update"])
    ap.add_argument("projects", nargs="*")
    ap.add_argument("--all", action="store_true", help="every Project under the SPACE's examples*/ folders")
    ap.add_argument("--root", type=Path, help="the SPACE for --all (default: the working directory)")
    ap.add_argument("--apply", action="store_true", help="update: do the steps (default: dry run)")
    ap.add_argument("--steps", help="update --apply: only these steps, comma-separated: " + ",".join(STEPS[1:]))
    ap.add_argument("--state", type=Path, help="update --apply: where its link snapshot is kept (default: temp)")
    a = ap.parse_args()
    if not a.all and not a.projects:
        ap.error("name a Project or pass --all")
    if a.verb == "audit":
        return cmd_audit(a)
    return cmd_apply(a) if a.apply else cmd_plan(a)


if __name__ == "__main__":
    sys.exit(main())

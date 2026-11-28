"""The OLD design ladder scaffold (JL 261007 morning, b12 s01): `jNN_<goal>_by-<method>/` with a frozen method.md.

    python design_ladder.py block <designs/>bNN_<app>                       [--title "<application>"]
    python design_ladder.py job   <block>/jNN_<goal>_by-<method>            [--n 10] [--goal "<goal line>"]
    python design_ladder.py task  <job>/tNN_d<NN>_<slug>
    python design_ladder.py run   <folder> commission|generate|verify|revise [--n 10]

Each command writes only what is missing (it never overwrites a file) and prints what it made.
Placeholders only: a person or an agent fills them through the design skills.
"""
import argparse
import re
import sys
from pathlib import Path

FAMILY = {**{m: "Goal Only" for m in ("goal", "principle", "exploring", "slots")},
          **{m: "External" for m in ("theory", "implementation")},
          **{m: "Internal" for m in ("insight", "precedent", "revising", "tailoring", "theory-and-insight",
                                     "user-test", "co-design")}}
RUN_TYPES = {"Block": "brief · rules · testplan (soft)",
             "Job": "commission (soft) · generate (hard) · compare (soft)",
             "Task": "verify (hard) · revise (soft)"}


def _write(path: Path, text: str, made: list) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    made.append(path)


def _readme(folder: Path, level: str, made: list) -> None:
    _write(folder / "runs" / "README.md", f"# Runs of {folder.name}\n\nrun types: {RUN_TYPES[level]}\n\n"
           "One folder per Run: hard `rNN_<type>_<target>/` (result/ inside), soft `run-<type>-<target>/`; "
           "each with its run.yaml.\n", made)


def block(path: Path, title: str, made: list) -> None:
    if not re.match(r"^b\d+_", path.name):
        sys.exit(f"a Block folder is bNN_<app>: {path.name}")
    _write(path / f"{path.name}.md", f"# {path.name.split('_', 1)[0]} · {title or '<application>'}\n\n"
           "board-kind: design-block\nspine: <what this application designs, for whom, in which channel>\n"
           "close: every goal's designs verified; the passed ones released\n\n## Goal list\n\n"
           "- <goal>: <job> <venue> for <who>\n", made)
    _write(path / "design-goal.md", "# Design goal\n\naim: <aim>\nvenue: <venue>\n\n## Rules\n\n- <rule every design keeps>\n\n"
           "## Resources\n\n- <resource>\n\n## Leave out\n\n- <what no design may use>\n", made)
    for d in ("studio", "reports", "delivery"):
        (path / d).mkdir(parents=True, exist_ok=True)
    _readme(path, "Block", made)


def job(path: Path, n: int, goal: str, made: list) -> None:
    m = re.match(r"^j\d+_(.+)_by-([a-z-]+)$", path.name)
    if not m:
        sys.exit(f"a Job folder is jNN_<goal>_by-<method>: {path.name}")
    method = m.group(2)
    if method not in FAMILY:
        sys.exit(f"unknown method {method!r}; one of: {', '.join(sorted(FAMILY))}")
    _write(path / f"{path.name}.md", f"# {path.name.split('_', 1)[0]} · {m.group(1)} by {method}\n\n"
           f"goal: {goal or '<job> <venue> for <who>'}\nmethod: by {method}\nfamily: {FAMILY[method]}\n"
           f"n: {n}\nstate: open\nclose: every design verified; the passed ones released\n\n## Goal\n\n"
           "aim: <aim>\nrequirements: <requirements>\nresources: <resources>\nleave out: <leave out>\n", made)
    _write(path / "method.md", f"# by {method} · {FAMILY[method]}\n\n<one or two sentences: what this method is for>\n\n"
           "## ① See input\n\n- goal: the Job's face\n- may not see: <what is kept from this method>\n\n"
           f"## ② Conduct process\n\n- reasoning: <direct · freestyle · element-wise>\n- maker: <model, agents, or a person>\n"
           f"- count: {n} designs\n\n## ③ Check output\n\n- rules: design-goal.md\n- grounding: only what ① lets it see\n", made)
    for d in ("studio", "delivery"):
        (path / d).mkdir(parents=True, exist_ok=True)
    _readme(path, "Job", made)


def task(path: Path, made: list) -> None:
    m = re.match(r"^t\d+_(d\d+)_(.+)$", path.name)
    if not m:
        sys.exit(f"a Task folder is tNN_d<NN>_<slug>: {path.name}")
    _write(path / f"{path.name}.md", f"# {m.group(1)} · {m.group(2)}\n\nstate: draft\njob: {path.parent.name}\n\n"
           "## Design\n\n<the design, word for word>\n\n## Rationale\n\n<why: each element's because>\n\n"
           "## Evaluation\n\n<the verify verdict, and any pretest>\n", made)
    _write(path / "elements.yaml", "# one entry per element of the design\n- element: <sender>\n  words: <the words>\n"
           "  from: requirements      # requirements · internal · external · intuition\n  source: <rule · W-NN · theory>\n"
           "  thinking: reasoned      # reasoned · intuitive\n  because: <one sentence>\n  changed: false\n", made)
    _readme(path, "Task", made)


def run(folder: Path, kind: str, n: int, made: list) -> None:
    runs = folder / "runs"
    taken = [int(p.name[1:3]) for p in runs.glob("r[0-9][0-9]_*")] if runs.is_dir() else []
    nn = f"r{max(taken, default=0) + 1:02d}"
    target = folder.name.split("_", 1)[0]
    name = {"commission": f"run-commission-{target}", "generate": f"{nn}_generate_{n}",
            "verify": f"{nn}_verify_{folder.name.split('_')[1] if '_' in folder.name else target}",
            "revise": f"run-revise-{folder.name.split('_')[1] if '_' in folder.name else target}"}[kind]
    hard = not name.startswith("run-")
    _write(runs / name / "run.yaml", f"run: {name}\nkind: {'hard' if hard else 'soft'}\ntype: {kind}\nstatus: open\n", made)
    if hard:
        (runs / name / "result").mkdir(parents=True, exist_ok=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("level", choices=("block", "job", "task", "run"))
    ap.add_argument("folder", type=Path)
    ap.add_argument("kind", nargs="?", choices=("commission", "generate", "verify", "revise"))
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--title", default="")
    ap.add_argument("--goal", default="")
    a = ap.parse_args(argv)
    made = []
    if a.level == "block":
        block(a.folder, a.title, made)
    elif a.level == "job":
        job(a.folder, a.n, a.goal, made)
    elif a.level == "task":
        task(a.folder, made)
    else:
        if not a.kind:
            ap.error("run needs a kind: commission, generate, verify or revise")
        run(a.folder, a.kind, a.n, made)
    for p in made:
        print("made", p)
    return made


if __name__ == "__main__":
    main()

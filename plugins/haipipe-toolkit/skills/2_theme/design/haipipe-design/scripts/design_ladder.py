"""Make the design ladder's folders (ref/design-ladder.md): a Block, a Job, its Tasks, a Run.

    python design_ladder.py block <designs/>Design-<name>  [--title "<application>"] [--channel sms]
    python design_ladder.py job   <block>/jNN_<goal>_<method>  --goal G01 --method "M04 m2" --inputs i2 [--n 10]
                                                                [--moved start|method|inputs]
    python design_ladder.py task  <job> t00                   t00_reason-ideas/   (② reason ideas)
    python design_ladder.py task  <job> d<NN> <slug>          tNN_d<NN>_<slug>/   (③ ④ one design)
    python design_ladder.py task  <job> t99                   t99_review-whole/   (⑤ review whole)
    python design_ladder.py run   <folder> <type> [<target>]  runs/run-<type>-<target>/ with its run.yaml

Every Run is named run-<type>-<target> (JL 261007); reason, generate, verify and rank are hard (their own result/),
the rest soft (passes/). A Job Run's target defaults to the Job's id, a Task Run's to the Task's (t00, t99, d<NN>);
a verify names the draft it reads, d<NN>-v<k>: k = 1 for the generate's draft, plus one per revise pass that wrote
a design.md. `job` checks run-add-job's gates: the goal is in board.md ## Goals and signed, the method version is
registered (haipipe-design-method/methods/), the inputs version exists, the folder's ids match the pins, and N is the
goal's n. Each command writes only
what is missing (it never overwrites a file) and prints what it made. Placeholders only: a person or an agent
fills them through the design skills.
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

HARD = {"reason", "generate", "verify", "rank"}
RUN_TYPES = {"Block": "add-goal · setup-rules · add-inputs · add-job · propose-method · add-observed · score · "
                      "propose-questions · report · draw (all soft)",
             "Job": "setup-goal · setup-method · setup-inputs · open-designs · freeze-predictions · release · close "
                    "(soft)",
             "t00": "reason (hard)",
             "design": "generate (hard) · verify (hard, another agent) · revise (soft)",
             "t99": "rank (hard, another agent)"}
JOB = re.compile(r"^j\d+_(g\d+)(?:-[a-z0-9-]+)?_(m\d+)(-[a-z0-9-]+)?$")   # j03_g01-<goal-slug>_m04-<method-slug>; slugs optional
METHOD = re.compile(r"^(M\d\d) (m\d+)$")
REGISTRY = Path(__file__).resolve().parents[2] / "haipipe-design-method" / "methods"
# where each run type may run, its owning skill, agent and who signs (ref/design-ladder.md § Runs)
TYPES = {
    "add-goal": ("Block", "haipipe-design-goal", "designer agent", "a person"),
    "setup-rules": ("Block", "haipipe-design-goal", "designer agent", "a person"),
    "add-inputs": ("Block", "haipipe-design-goal", "designer agent", "none"),
    "add-job": ("Block", "haipipe-design", "designer agent", "none"),
    "propose-method": ("Block", "haipipe-design-method", "designer agent", "a person"),
    "add-observed": ("Block", "haipipe-design-method", "designer agent", "none"),
    "score": ("Block", "haipipe-design-method", "reviewer agent", "none"),
    "propose-questions": ("Block", "haipipe-question", "designer agent", "another agent agrees"),
    "report": ("Block", "haipipe-report", "designer agent", "another agent checks"),
    "draw": ("any", "excalidraw-report", "designer agent", "none"),
    "setup-goal": ("Job", "haipipe-design-goal", "designer agent", "none"),
    "setup-method": ("Job", "haipipe-design-method", "designer agent", "none"),
    "setup-inputs": ("Job", "haipipe-design-goal", "designer agent", "none"),
    "open-designs": ("Job", "haipipe-design", "designer agent", "none"),
    "freeze-predictions": ("Job", "haipipe-design-delivery", "designer agent", "a person"),
    "release": ("Job", "haipipe-design-delivery", "designer agent", "a person"),
    "close": ("Job", "haipipe-design-workflow", "designer agent", "a person"),
    "reason": ("t00", "haipipe-design-unit", "designer agent", "none"),
    "generate": ("design", "haipipe-design-unit", "designer agent", "none"),
    "verify": ("design", "haipipe-design-unit", "reviewer agent", "none"),
    "revise": ("design", "haipipe-design-unit", "designer agent", "none"),
    "rank": ("t99", "haipipe-design-unit", "reviewer agent", "none")}


def _write(path: Path, text: str, made: list) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    made.append(path)


def _front(fields: list, body: str) -> str:
    return "---\n" + "".join(f"{k}: {v}\n" for k, v in fields) + "---\n\n" + body


def _readme(folder: Path, level: str, made: list) -> None:
    _write(folder / "runs" / "README.md", f"# Runs of {folder.name}\n\nrun types: {RUN_TYPES[level]}\n\n"
           "One folder per Run, `run-<type>-<target>/`, with its run.yaml: a hard Run writes only its result/, a soft "
           "Run writes its level's own files and keeps passes/.\n", made)


# a design Block is a special board, named by its kind (JL 261008: "Paper, Insight, (and Prototype), and Design, these
# four are the special boards"): Design-<name>[-<YYMMDD>]; bNN_<app> stays readable
BLOCK_NAME = re.compile(r"^(Design-[A-Za-z0-9][A-Za-z0-9.-]*|b\d+_.+)$")


def block(path: Path, title: str, channel: str, made: list) -> None:
    if not BLOCK_NAME.match(path.name):
        sys.exit(f"a design Block folder is Design-<name>[-<YYMMDD>] (or the older bNN_<app>): {path.name}")
    head = path.name if path.name.startswith("Design-") else path.name.split("_", 1)[0]
    _write(path / "board.md", f"# {head} · {title or '<application>'}\n\n"
           f"board-kind: design-board\nchannel: {channel}\n"
           "spine: <what this application designs, for whom, in this channel>\n"
           "close: every goal's kept designs released\n\n"
           "## Goals\n\n```yaml\ngoals: []\n```\n\n## Questions\n\n```yaml\nquestions: []\n```\n", made)
    _write(path / "design-goal.md", "# Shared rules\n\nrules: r1\nsigned: ''\n\nEvery goal of this Block keeps "
           "these; a person signs them (run-setup-rules), and a new version is r<k+1>.\n\n## Rules\n\n"
           "- <rule every design keeps>\n\n## Leave out\n\n- <what no design may use>\n", made)
    for d in ("inputs", "observed", "studio", "reports", "delivery"):
        (path / d).mkdir(parents=True, exist_ok=True)
    _readme(path, "Block", made)


def goals(block: Path) -> list:
    """The goal list, board.md ## Goals (its ```yaml block)."""
    md = block / "board.md"
    text = md.read_text(encoding="utf-8") if md.is_file() else ""
    m = re.search(r"(?ms)^##\s+Goals\s*\n.*?```yaml\n(.*?)```", text)
    data = (yaml.safe_load(m.group(1)) or {}) if m else {}
    return data.get("goals", []) if isinstance(data, dict) else []


def _gates(block: Path, goal: str, method: str, inputs: str, n) -> int:
    """run-add-job's gates: a signed goal, a registered method version, an inputs version; N is the goal's."""
    g = next((x for x in goals(block) if str(x.get("id")) == goal), None)
    if g is None:
        sys.exit(f"{goal} is not in {block.name}/board.md ## Goals: add it first (run-add-goal)")
    if not str(g.get("signed") or "").strip():
        sys.exit(f"{goal} is not signed: a person signs a goal before a Job pins it")
    rules = block / "design-goal.md"
    signed = re.search(r"(?m)^signed:\s*(.*)$", rules.read_text(encoding="utf-8")) if rules.is_file() else None
    if not signed or not signed.group(1).strip().strip("'\""):
        sys.exit(f"{block.name}/design-goal.md is not signed: a person signs the shared rules first (run-setup-rules)")
    mid, version = METHOD.match(method).groups()
    if not list(REGISTRY.glob(f"{mid}-*/{version}.md")):
        sys.exit(f"{method} is not registered in haipipe-design-method/methods/ (pin_method.py --list)")
    if not (block / "inputs" / inputs).is_dir():
        sys.exit(f"{block.name}/inputs/{inputs}/ does not exist: add the inputs version first (run-add-inputs)")
    goal_n = g.get("n")
    if n is not None and goal_n not in (None, "") and int(goal_n) != int(n):
        sys.exit(f"--n {n} differs from {goal}'s n: {goal_n}; N is the goal's, set once in the goal list")
    return int(goal_n) if goal_n not in (None, "") else int(n if n is not None else 10)


def job(path: Path, goal: str, method: str, inputs: str, n, moved: str, made: list) -> None:
    if not JOB.match(path.name):
        sys.exit(f"a Job folder is jNN_<goal>[-<slug>]_<method>[-<slug>], ids lowercased (j03_g01-<goal-slug>_m04-<method-slug>): {path.name}")
    if not re.match(r"^G\d\d$", goal or ""):
        sys.exit(f"--goal is a goal id from the Block's goal list (G01): {goal!r}")
    if not METHOD.match(method or ""):
        sys.exit(f"--method is a registered method and version (M04 m2): {method!r}")
    if not re.match(r"^i\d+$", inputs or ""):
        sys.exit(f"--inputs is an inputs version of the Block (i2): {inputs!r}")
    m = JOB.match(path.name)
    if (m.group(1), m.group(2)) != (goal.lower(), method.split()[0].lower()):
        sys.exit(f"the folder names its goal and method ({m.group(1)}, {m.group(2)}); the pins say {goal}, {method}")
    if (path / f"{path.name}.md").exists():
        return                                           # already launched: nothing is overwritten
    n = _gates(path.parent, goal, method, inputs, n)
    jid = path.name.split("_", 1)[0]
    _write(path / f"{path.name}.md", _front(
        [("goal", goal), ("method", method), ("method-sha", "<sha, written by run-setup-method>"), ("inputs", inputs),
         ("n", n), ("state", "open"), ("moved", moved)],
        f"# {jid} · {goal} by {method} · inputs {inputs}\n"), made)
    (path / "inputs").mkdir(parents=True, exist_ok=True)
    for d in ("studio", "reports", "delivery"):
        (path / d).mkdir(parents=True, exist_ok=True)
    _readme(path, "Job", made)


def task(job_dir: Path, which: str, slug: str, made: list) -> Path:
    if not JOB.match(job_dir.name):
        sys.exit(f"a Task sits in a Job folder jNN_<goal>_<method>: {job_dir.name}")
    if which == "t00":
        path, kind, step = job_dir / "t00_reason-ideas", "t00", "②"
        _write(path / f"{path.name}.md", _front([("state", "open"), ("step", step)], "# t00 · reason ideas\n"), made)
    elif which == "t99":
        path, kind, step = job_dir / "t99_review-whole", "t99", "⑤"
        _write(path / f"{path.name}.md", _front([("state", "open"), ("step", step)], "# t99 · review whole\n"), made)
    else:
        m = re.match(r"^d(\d\d)$", which)
        if not m or not re.match(r"^[a-z0-9-]+$", slug or ""):
            sys.exit("a design Task is: task <job> d<NN> <slug> (the short name born with its idea in t00)")
        path, kind = job_dir / f"t{m.group(1)}_d{m.group(1)}_{slug}", "design"
        _write(path / f"{path.name}.md", _front(
            [("state", "draft"), ("name", slug), ("idea", f"I{m.group(1)}"), ("rank", "")],
            f"# d{m.group(1)} · {slug}\n\n## Design\n\n<the design, word for word>\n\n## Evaluation\n\n"
            "<the verify verdict: T0 · T1 · T2>\n"), made)
        _write(path / "elements.yaml", "# one entry per element of the design\n- element: <opening>\n"
               "  words: <the words>\n  from: <a file in the manifest, or own knowledge>\n  because: <one sentence>\n"
               "  step: ③\n  changed: ''\n", made)
    _readme(path, kind, made)
    return path


def level_of(folder: Path) -> str:
    name = folder.name
    if JOB.match(name):
        return "Job"
    if BLOCK_NAME.match(name):
        return "Block"
    if name.startswith("t00_"):
        return "t00"
    if name.startswith("t99_"):
        return "t99"
    if re.match(r"^t\d+_d\d+_", name):
        return "design"
    sys.exit(f"not a design Block, Job or Task folder: {name}")


def drafts(task: Path) -> int:
    """How many drafts a design has: its generate's, then one per revise pass that wrote a design.md."""
    runs = task / "runs"
    n = 1 if any(runs.glob("run-generate-*/result/design.md")) or any(runs.glob("run-generate-*")) else 0
    return n + len(list(runs.glob("run-revise-*/passes/*/design.md")))


def _target(folder: Path, rtype: str) -> str:
    """A Run's default target: the Job's id, or the Task's (t00, t99, d<NN>; a verify d<NN>-v<k>, k the draft it reads)."""
    name, lv = folder.name, level_of(folder)
    if lv == "Job":
        return name.split("_", 1)[0]
    if lv == "Block":
        if rtype.split("-")[-1] in ("rules", "questions"):
            return rtype.split("-")[-1]                  # run-setup-rules · run-propose-questions
        sys.exit(f"a Block Run needs its target: run {name} {rtype} <target>")
    if lv in ("t00", "t99"):
        return name[:3]
    d = re.match(r"^t\d+_(d\d+)_", name).group(1)
    if rtype != "verify":
        return d
    k = drafts(folder)
    if not k:
        sys.exit(f"{name} has no draft yet: generate it first (run-generate-{d})")
    return f"{d}-v{k}"


def run(folder: Path, rtype: str, target: str, made: list) -> Path:
    if rtype not in TYPES:
        sys.exit(f"unknown run type {rtype!r}; one of: {', '.join(TYPES)}")
    where, skill, agent, signs = TYPES[rtype]
    lv = level_of(folder)
    if where not in ("any", lv):
        sys.exit(f"run-{rtype} runs at the {where} level, not in {folder.name} ({lv})")
    target = (target or _target(folder, rtype)).lower()
    name = f"run-{rtype}-{target}" if target != rtype.split("-")[-1] else f"run-{rtype}"
    path = folder / "runs" / name
    hard = rtype in HARD
    _write(path / "run.yaml", f"run: {name}\nkind: {'hard' if hard else 'soft'}\ntype: {rtype}\nscope: {folder.name}\n"
           f"target: {target}\nskill: {skill}\nagent: {agent}\nsigns: {signs}\nstatus: open\nby: ''\n"
           "started_at: ''\nfinished_at: ''\nusage: {}\n", made)
    (path / ("result" if hard else "passes")).mkdir(parents=True, exist_ok=True)
    return path


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("level", choices=("block", "job", "task", "run"))
    ap.add_argument("folder", type=Path)
    ap.add_argument("what", nargs="?", default="", help="task: t00 · t99 · d<NN>; run: its type")
    ap.add_argument("extra", nargs="?", default="", help="task d<NN>: its slug; run: its target")
    ap.add_argument("--title", default="")
    ap.add_argument("--channel", default="<channel>")
    ap.add_argument("--goal", default="")
    ap.add_argument("--method", default="")
    ap.add_argument("--inputs", default="")
    ap.add_argument("--n", type=int, default=None, help="N; the goal's n by default")
    ap.add_argument("--moved", default="start", choices=("start", "method", "inputs"))
    a = ap.parse_args(argv)
    made = []
    if a.level == "block":
        block(a.folder, a.title, a.channel, made)
    elif a.level == "job":
        job(a.folder, a.goal, a.method, a.inputs, a.n, a.moved, made)
    elif a.level == "task":
        if not a.what:
            ap.error("task needs which: t00, t99, or d<NN> <slug>")
        task(a.folder, a.what, a.extra, made)
    else:
        if not a.what:
            ap.error("run needs a type: reason, generate, verify, revise, rank, setup-goal, add-job, …")
        run(a.folder, a.what, a.extra, made)
    for p in made:
        print("made", p)
    return made


if __name__ == "__main__":
    main()

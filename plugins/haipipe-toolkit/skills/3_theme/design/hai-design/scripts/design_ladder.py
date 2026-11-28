"""Make the design ladder's folders (ref/design-ladder.md): a Block, a Job, its Tasks, a Run.

    python design_ladder.py block   <design/>Design-<name>  [--title "<application>"] [--channel sms]
    python design_ladder.py book    <design/>DesignMethodBook-<Topic> --serves design/Design-<name>
    python design_ladder.py method  <book>/jNN_M0x-<slug> --version mK     one method type, its version mK.md frozen
    python design_ladder.py job     <block>/jNN_<goal>_M0x-<slug>-mK_inputs-vM --goal G01
                                    [--n 10] [--moved start|method|inputs]   (the pins are read from the name)
    python design_ladder.py job     <block>/jNN_<goal>_<method>  --goal G01 --method "M04 m2" --inputs i2   (a Board
                                    with no Book: the older names)
    python design_ladder.py task  <job> t00                   t00_reason-ideas/   (② reason ideas)
    python design_ladder.py task  <job> d<NN> <slug>          tNN_d<NN>_<slug>/   (③ ④ one design)
    python design_ladder.py task  <job> t99                   t99_review-whole/   (⑤ review whole)
    python design_ladder.py run   <folder> <type> [<target>]  runs/run-<type>-<target>/ with its run.yaml
    python design_ladder.py goals <block>                     each Job face's `goal: G01` gets its name: `G01 · <name>`
    python design_ladder.py audit  <block | design/>          what an older Board still names the old way (read-only)
    python design_ladder.py update <block | design/> [--apply]  bring it onto the current names, with its Book
                                                              (design_update.py; a dry run unless --apply)

Every Run is named run-<type>-<target>; reason, generate, verify and rank are hard (their own result/),
the rest soft (passes/). A Job Run's target defaults to the Job's id, a Task Run's to the Task's (t00, t99, d<NN>);
a verify names the draft it reads, d<NN>-v<k>: k = 1 for the generate's draft, plus one per revise pass that wrote
a design.md. `job` checks run-add-job's gates: the goal is in board.md ## Goals and signed, the method version is
registered (hai-design-method/methods/), the inputs version exists, the folder's ids match the pins, and N is the
goal's n. A Job face pins its goal as `goal: G01 · <name>`, the id first and the goal's `name:` after it, so a mind map
and a reader see the goal's words, not only its id (261108); every reader takes the id before " · ". Each command
writes only what is missing (it never overwrites a file; `goals` adds only a missing name) and prints what it made. Placeholders only: a person or an agent
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
# a Job folder is jNN_<goal name>_<method name>: the goal's `name:` in board.md ## Goals and the method's registry slug, j01_prepare-before-visit_goal-only.
# The ids live in the face's pins. The older id form j03_g01[-<goal-slug>]_m04[-<method-slug>] stays readable.
JOB = re.compile(r"^j\d+_([a-z0-9]+(?:-[a-z0-9]+)*)_([a-z0-9]+(?:-[a-z0-9]+)*)$")
# a Board with a Design Method Book: jNN_<goal name>_M0x-<slug>-mK_inputs-vM, the method type, its
# version and the inputs version in the name, as the insight Board's jNN_question-vN-<slug>_data-vM. Method types sit
# side by side (M01 goal only, M02 overall performance); only mK is a version.
JOB_V = re.compile(r"^j\d+_([a-z0-9]+(?:-[a-z0-9]+)*)_(M\d\d)-([a-z0-9]+(?:-[a-z0-9]+)*)-(m\d+)_(inputs-v\d+)$")
METHOD_TYPE = re.compile(r"^j\d+_(M\d\d)-([a-z0-9]+(?:-[a-z0-9]+)*)$")
BOOK_NAME = re.compile(r"^DesignMethodBook-[A-Za-z0-9][A-Za-z0-9.-]*$")
JOB_IDS = re.compile(r"^j\d+_(g\d+)(?:-[a-z0-9-]+)?_(m\d+)(-[a-z0-9-]+)?$")
METHOD = re.compile(r"^(M\d\d) (m\d+)$")
REGISTRY = Path(__file__).resolve().parents[2] / "hai-design-method" / "methods"
# where each run type may run, its owning skill, agent and who signs (ref/design-ladder.md § Runs)
TYPES = {
    "add-goal": ("Block", "hai-design-goal", "designer agent", "a person"),
    "setup-rules": ("Block", "hai-design-goal", "designer agent", "a person"),
    "add-inputs": ("Block", "hai-design-goal", "designer agent", "none"),
    "add-job": ("Block", "hai-design", "designer agent", "none"),
    "propose-method": ("Block", "hai-design-method", "designer agent", "a person"),
    "add-observed": ("Block", "hai-design-method", "designer agent", "none"),
    "score": ("Block", "hai-design-method", "reviewer agent", "none"),
    "propose-questions": ("Block", "hai-report", "designer agent", "another agent agrees"),
    "report": ("Block", "hai-report", "designer agent", "another agent checks"),
    "draw": ("any", "hai-draw report", "designer agent", "none"),
    "setup-goal": ("Job", "hai-design-goal", "designer agent", "none"),
    "setup-method": ("Job", "hai-design-method", "designer agent", "none"),
    "setup-inputs": ("Job", "hai-design-goal", "designer agent", "none"),
    "open-designs": ("Job", "hai-design", "designer agent", "none"),
    "freeze-predictions": ("Job", "hai-design-delivery", "designer agent", "a person"),
    "release": ("Job", "hai-design-delivery", "designer agent", "a person"),
    "close": ("Job", "hai-design-workflow", "designer agent", "a person"),
    "reason": ("t00", "hai-design-unit", "designer agent", "none"),
    "generate": ("design", "hai-design-unit", "designer agent", "none"),
    "verify": ("design", "hai-design-unit", "reviewer agent", "none"),
    "revise": ("design", "hai-design-unit", "designer agent", "none"),
    "rank": ("t99", "hai-design-unit", "reviewer agent", "none")}


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


# a design Block is a special board, named by its kind: Design-<name>[-<YYMMDD>]; bNN_<app> stays readable
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


def book(path: Path, serves: str, made: list) -> None:
    """A Design Method Book, the designer of one channel: its face (board-kind: design-method-book, channel: read
    from the Board it serves, serves:), proposals/, and the served Board's `method-book:` line when it has none."""
    if not BOOK_NAME.match(path.name):
        sys.exit(f"a Design Method Book folder is DesignMethodBook-<Topic>: {path.name}")
    if not re.match(r"^design/Design-[A-Za-z0-9][A-Za-z0-9.-]*$", serves or ""):
        sys.exit(f"--serves is the Board it serves, design/Design-<name>: {serves!r}")
    board = path.parent.parent / serves / "board.md"
    ch = re.search(r"(?m)^channel:\s*(\S+)", board.read_text(encoding="utf-8")) if board.is_file() else None
    _write(path / "board.md", _front([("board-kind", "design-method-book"), ("channel", ch.group(1) if ch else "<channel>"),
                                      ("serves", serves),
                                      ("goal", f"The {ch.group(1) if ch else '<channel>'} designer: its method types, each version signed")],
                                     f"# {path.name} · the {ch.group(1) if ch else '<channel>'} designer\n\nOne Job per method type "
                                     "(jNN_M0x-<slug>/), its versions (mK.md) frozen once a person signs them; a "
                                     "type's next version is cut from proposals/.\n"), made)
    _write(path / "proposals" / "README.md", "# proposals\n\nThe backlog: a change to one step of the method, one file "
           "each (<slug>.md: kind · step · from · state · why). A type's next version is cut from here once a person signs.\n", made)
    if board.is_file():
        text = board.read_text(encoding="utf-8")
        if not re.search(r"(?m)^method-book:", text):
            line = f"method-book: {path.parent.name}/{path.name}\n"
            text = re.sub(r"(?m)^(board-kind:.*\n)", lambda m: m.group(1) + line, text, count=1)
            board.write_text(text, encoding="utf-8")
            made.append(board)


def serve(book_dir: Path, board: Path) -> None:
    """Add a Board to a Book's `serves:` line and name the Book on the Board's face, when either is missing."""
    rel = f"{board.parent.name}/{board.name}"
    face = book_dir / "board.md"
    text = face.read_text(encoding="utf-8")
    m = re.search(r"(?m)^serves:\s*(.*)$", text)
    if m and rel not in [s.strip() for s in m.group(1).split(",")]:
        face.write_text(text.replace(m.group(0), f"serves: {m.group(1).strip()}, {rel}", 1), encoding="utf-8")
    btext = (board / "board.md").read_text(encoding="utf-8")
    if not re.search(r"(?m)^method-book:", btext):
        line = f"method-book: {book_dir.parent.name}/{book_dir.name}\n"
        (board / "board.md").write_text(re.sub(r"(?m)^(board-kind:.*\n)", lambda x: x.group(1) + line, btext, count=1), encoding="utf-8")


def method(path: Path, version: str, made: list) -> None:
    """One method type of a Book (jNN_M0x-<slug>/): its face (method, title, state, versions) and the version's card
    mK.md, copied from the Guide's library and frozen. The version waits unsigned (`mK: ''`); a person signs it
    through hai-design-method. A type that is already there gains the version."""
    m = METHOD_TYPE.match(path.name)
    if not m or not BOOK_NAME.match(path.parent.name):
        sys.exit(f"a method type is <book>/jNN_M0x-<slug>: {path}")
    if not re.match(r"^m\d+$", version or ""):
        sys.exit(f"--version is the registered version to take (m2): {version!r}")
    mid, slug = m.groups()
    if method_card(mid)[0] != slug:
        sys.exit(f"{mid} is registered as {mid}-{method_card(mid)[0] or '?'} (pin_method.py --list): {path.name}")
    card = next(iter(sorted(REGISTRY.glob(f"{mid}-*/{version}.md"))), None)
    if card is None:
        sys.exit(f"{mid} {version} is not registered in hai-design-method/methods/ (pin_method.py --list)")
    face = path / f"{path.name}.md"
    if not face.exists():
        _write(face, f"---\nmethod: {mid}\ntitle: {slug.replace('-', ' ')}\nstate: open\nversions:\n  {version}: ''\n---\n\n"
               f"# {mid} · {slug.replace('-', ' ')}\n", made)
    elif not re.search(rf"(?m)^  {version}:", face.read_text(encoding="utf-8")):
        text = face.read_text(encoding="utf-8")
        text = (re.sub(r"(?m)^versions:\n((?:  .*\n)*)", lambda v: v.group(0) + f"  {version}: ''\n", text, count=1)
                if re.search(r"(?m)^versions:", text) else text.replace("\n---\n", f"\nversions:\n  {version}: ''\n---\n", 1))
        face.write_text(text, encoding="utf-8")
        made.append(face)
    _write(path / f"{version}.md", card.read_text(encoding="utf-8"), made)


def book_of(block: Path) -> Path | None:
    text = (block / "board.md").read_text(encoding="utf-8") if (block / "board.md").is_file() else ""
    m = re.search(r"(?m)^method-book:\s*(\S+)", text)
    return block.parent.parent / m.group(1) if m else None


def signed_version(block: Path, mid: str, slug: str, version: str) -> None:
    """Stop unless the Board's Book holds the method type and a person signed this version of it."""
    bk = book_of(block)
    if bk is None or not bk.is_dir():
        sys.exit(f"{block.name}/board.md names no Design Method Book (method-book:); run design_ladder.py book first")
    kind = next((d for d in sorted(bk.glob(f"j*_{mid}-{slug}")) if METHOD_TYPE.match(d.name)), None)
    if kind is None:
        sys.exit(f"{mid}-{slug} is not a method type of {bk.name}; run design_ladder.py method first")
    face = kind / f"{kind.name}.md"
    fm = re.match(r"(?s)^---\n(.*?)\n---\n", face.read_text(encoding="utf-8")) if face.is_file() else None
    versions = ((yaml.safe_load(fm.group(1)) or {}) if fm else {}).get("versions") or {}
    if version not in versions:
        sys.exit(f"{mid} {version} is not a version of {kind.name}; run design_ladder.py method {kind.name} --version {version}")
    if not str(versions.get(version) or "").strip():
        sys.exit(f"{mid} {version} is not signed: a person signs a method version before a Job runs it")


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
        sys.exit(f"{method} is not registered in hai-design-method/methods/ (pin_method.py --list)")
    if not (block / "inputs" / inputs).is_dir():
        sys.exit(f"{block.name}/inputs/{inputs}/ does not exist: add the inputs version first (run-add-inputs)")
    goal_n = g.get("n")
    if n is not None and goal_n not in (None, "") and int(goal_n) != int(n):
        sys.exit(f"--n {n} differs from {goal}'s n: {goal_n}; N is the goal's, set once in the goal list")
    return int(goal_n) if goal_n not in (None, "") else int(n if n is not None else 10)


def method_card(mid: str) -> tuple:
    """A registered method's (slug, name): M04 -> ("actionable-insights", "Actionable insights")."""
    folder = next(iter(sorted(REGISTRY.glob(f"{mid}-*"))), None)
    if folder is None:
        return "", ""
    face = folder / "method.md"
    m = re.match(r"(?s)^---\n(.*?)\n---\n", face.read_text(encoding="utf-8")) if face.is_file() else None
    name = str(((yaml.safe_load(m.group(1)) or {}) if m else {}).get("name") or "")
    return folder.name.split("-", 1)[1], name


def readable_name(block: Path, goal: str, method: str) -> str:
    """The Job folder's words for its pins: <goal name>_<method name> (prepare-before-visit_goal-only)."""
    g = next((x for x in goals(block) if str(x.get("id")) == goal), None) or {}
    return f"{str(g.get('name') or '').strip().lower()}_{method_card(method.split()[0])[0]}"


def _job_title(block: Path, goal: str, method: str) -> str:
    """The Job face's heading in words: <Goal name>, by <Method name> (Prepare before visit, by Goal only)."""
    g = next((x for x in goals(block) if str(x.get("id")) == goal), None) or {}
    words = str(g.get("name") or goal).replace("-", " ").strip()
    return f"{words[:1].upper()}{words[1:]}, by {method_card(method.split()[0])[1] or method}"


def goal_pin(block: Path, goal: str) -> str:
    """A Job face's goal pin: the id, then the goal's name from board.md ## Goals (`G01 · confirm-by-reply`); the id
    alone when the goal has no name."""
    g = next((x for x in goals(block) if str(x.get("id")) == goal), None) or {}
    name = str(g.get("name") or "").strip()
    return f"{goal} · {name}" if name else goal


def goals_named(block: Path, made: list) -> None:
    """Give each Job face's `goal:` its goal's name where it holds the id alone (`G01` → `G01 · confirm-by-reply`):
    the one line changes, nothing else; a face that names its goal already, or a goal with no name, is left as it is."""
    if not BLOCK_NAME.match(block.name) or not (block / "board.md").is_file():
        sys.exit(f"not a design Block (Design-<name>/ with a board.md): {block}")
    for jdir in sorted(p for p in block.iterdir() if p.is_dir() and (JOB.match(p.name) or JOB_V.match(p.name))):
        face = jdir / f"{jdir.name}.md"
        if not face.is_file():
            continue
        text = face.read_text(encoding="utf-8")
        front = re.match(r"(?s)\A---\n(.*?)\n---\n", text)
        line = re.search(r"(?m)^goal:[ \t]*(G\d+)[ \t]*$", front.group(1)) if front else None
        if not line:
            continue
        pin = goal_pin(block, line.group(1))
        if pin == line.group(1):
            continue
        start = front.start(1) + line.start()
        face.write_text(text[:start] + f"goal: {pin}" + text[start + len(line.group(0)):], encoding="utf-8")
        made.append(face)


def job_v(path: Path, goal: str, n, moved: str, made: list) -> None:
    """A Job on a Board with a Design Method Book: jNN_<goal name>_M0x-<slug>-mK_inputs-vM. Its pins are read from the
    name (`method: M0x mK`, `inputs: inputs-vM`); the Book must hold that method type with the version signed."""
    m = JOB_V.match(path.name)
    if not m:
        sys.exit(f"a Job folder is jNN_<goal name>_M0x-<slug>-mK_inputs-vM: {path.name}")
    if not re.match(r"^G\d\d$", goal or ""):
        sys.exit(f"--goal is a goal id from the Block's goal list (G01): {goal!r}")
    _name, mid, slug, version, inputs = m.groups()
    signed_version(path.parent, mid, slug, version)
    pin = f"{mid} {version}"
    g = next((x for x in goals(path.parent) if str(x.get("id")) == goal), None) or {}
    want = str(g.get("name") or "").strip().lower()
    if m.group(1) != want:
        sys.exit(f"the folder is named by its pins: {path.name.split('_', 1)[0]}_{want}_{mid}-{slug}-{version}_{inputs}")
    if (path / f"{path.name}.md").exists():
        return
    n = _gates(path.parent, goal, pin, inputs, n)
    _write(path / f"{path.name}.md", _front(
        [("goal", goal_pin(path.parent, goal)), ("method", pin),
         ("method-sha", "<sha, written by run-setup-method>"), ("inputs", inputs), ("n", n), ("state", "open"),
         ("moved", moved)], f"# {_job_title(path.parent, goal, pin)}\n"), made)
    (path / "inputs").mkdir(parents=True, exist_ok=True)
    for d in ("studio", "reports", "delivery"):
        (path / d).mkdir(parents=True, exist_ok=True)
    _readme(path, "Job", made)


def job(path: Path, goal: str, method: str, inputs: str, n, moved: str, made: list) -> None:
    if not JOB.match(path.name):
        sys.exit(f"a Job folder is jNN_<goal name>_<method name> (j01_prepare-before-visit_goal-only): {path.name}")
    if not re.match(r"^G\d\d$", goal or ""):
        sys.exit(f"--goal is a goal id from the Block's goal list (G01): {goal!r}")
    if not METHOD.match(method or ""):
        sys.exit(f"--method is a registered method and version (M04 m2): {method!r}")
    if not re.match(r"^(inputs-v|i)\d+$", inputs or ""):
        sys.exit(f"--inputs is an inputs version of the Block (inputs-v2; an older Block: i2): {inputs!r}")
    old = JOB_IDS.match(path.name)
    if old and (old.group(1), old.group(2)) != (goal.lower(), method.split()[0].lower()):
        sys.exit(f"the folder names its goal and method ({old.group(1)}, {old.group(2)}); the pins say {goal}, {method}")
    want = readable_name(path.parent, goal, method)
    if not old and path.name.split("_", 1)[1] != want:
        if want.startswith("_"):
            sys.exit(f"{goal} has no name: in board.md ## Goals: give it one (the Job folder is named by it)")
        sys.exit(f"the folder is named by its goal and method: {path.name.split('_', 1)[0]}_{want}")
    if (path / f"{path.name}.md").exists():
        return                                           # already launched: nothing is overwritten
    n = _gates(path.parent, goal, method, inputs, n)
    _write(path / f"{path.name}.md", _front(
        [("goal", goal_pin(path.parent, goal)), ("method", method), ("method-sha", "<sha, written by run-setup-method>"), ("inputs", inputs),
         ("n", n), ("state", "open"), ("moved", moved)],
        f"# {_job_title(path.parent, goal, method)}\n"), made)
    (path / "inputs").mkdir(parents=True, exist_ok=True)
    for d in ("studio", "reports", "delivery"):
        (path / d).mkdir(parents=True, exist_ok=True)
    _readme(path, "Job", made)


def task(job_dir: Path, which: str, slug: str, made: list) -> Path:
    if not (JOB.match(job_dir.name) or JOB_V.match(job_dir.name)):
        sys.exit(f"a Task sits in a Job folder jNN_<goal name>_M0x-<slug>-mK_inputs-vM: {job_dir.name}")
    if which == "t00":
        path, kind, step = job_dir / "t00_reason-ideas", "t00", "②"
        _write(path / f"{path.name}.md", _front([("state", "open"), ("step", step), ("task-type", "design-reason")],
                                                "# t00 · reason ideas\n"), made)
    elif which == "t99":
        path, kind, step = job_dir / "t99_review-whole", "t99", "⑤"
        _write(path / f"{path.name}.md", _front([("state", "open"), ("step", step), ("task-type", "design-whole")],
                                                "# t99 · review whole\n"), made)
    else:
        m = re.match(r"^d(\d\d)$", which)
        if not m or not re.match(r"^[a-z0-9-]+$", slug or ""):
            sys.exit("a design Task is: task <job> d<NN> <slug> (the short name born with its idea in t00)")
        path, kind = job_dir / f"t{m.group(1)}_d{m.group(1)}_{slug}", "design"
        _write(path / f"{path.name}.md", _front(
            [("state", "draft"), ("name", slug), ("idea", f"I{m.group(1)}"), ("rank", ""), ("task-type", "design-item")],
            f"# d{m.group(1)} · {slug}\n\n## Design\n\n<the design, word for word>\n\n## Evaluation\n\n"
            "<the verify verdict: T0 · T1 · T2>\n"), made)
        _write(path / "elements.yaml", "# one entry per element of the design\n- element: <opening>\n"
               "  words: <the words>\n  from: <a file in the manifest, or own knowledge>\n  because: <one sentence>\n"
               "  step: ③\n  changed: ''\n", made)
    _readme(path, kind, made)
    return path


def level_of(folder: Path) -> str:
    name = folder.name
    if JOB.match(name) or JOB_V.match(name):
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
    ap.add_argument("level", choices=("block", "book", "method", "job", "task", "run", "goals", "audit", "update"))
    ap.add_argument("folder", type=Path)
    ap.add_argument("what", nargs="?", default="", help="task: t00 · t99 · d<NN>; run: its type")
    ap.add_argument("extra", nargs="?", default="", help="task d<NN>: its slug; run: its target")
    ap.add_argument("--title", default="")
    ap.add_argument("--channel", default="<channel>")
    ap.add_argument("--goal", default="")
    ap.add_argument("--method", default="")
    ap.add_argument("--inputs", default="")
    ap.add_argument("--apply", action="store_true", help="update: write the changes (a dry run without it)")
    ap.add_argument("--version", default="", help="method: the registered version the Book takes (m2)")
    ap.add_argument("--serves", default="", help="book: the Board it serves (design/Design-<name>)")
    ap.add_argument("--n", type=int, default=None, help="N; the goal's n by default")
    ap.add_argument("--moved", default="start", choices=("start", "method", "inputs"))
    a = ap.parse_args(argv)
    made = []
    if a.level in ("audit", "update"):
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        sys.dont_write_bytecode = True                      # an update leaves nothing in this skill's folder
        import design_update as U
        if a.level == "audit":
            U.audit(a.folder, lambda mid: method_card(mid)[0])
        else:
            U.update(a.folder, a.apply, sys.modules[__name__])
        return 0
    if a.level == "block":
        block(a.folder, a.title, a.channel, made)
    elif a.level == "goals":
        goals_named(a.folder, made)
    elif a.level == "book":
        book(a.folder, a.serves, made)
    elif a.level == "method":
        method(a.folder, a.version, made)
    elif a.level == "job" and JOB_V.match(a.folder.name):
        job_v(a.folder, a.goal, a.n, a.moved, made)
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
        print("named" if a.level == "goals" else "made", p)
    return made


if __name__ == "__main__":
    main()

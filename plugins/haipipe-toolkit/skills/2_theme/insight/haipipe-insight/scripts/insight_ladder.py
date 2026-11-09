#!/usr/bin/env python3
"""insight_ladder.py · make the insight ladder's folders (ref/insight-ladder.md): the Prototype Block and its
versions and questions, the insight Board and its data versions, its Jobs and their Tasks, and a Run.

    python insight_ladder.py prototype <Project>/insight/Prototype-<name> --serves insight/Insight-<name> [--title "…"]
    python insight_ladder.py version   <prototype> --slug <what-it-is>  the next code version jNN_code-vN_<slug>/ (from the newest)
    python insight_ladder.py question  <version> <L><NN> <slug>        a new question Task tNN_<L><NN>_<slug>/
    python insight_ladder.py change    <version> <L><NN> --why "…"     carry a kept question into this version to change it
    python insight_ladder.py retire    <version> <L><NN> --why "…"     drop a question from this version (kept as history)
    python insight_ladder.py sign      <version> --date YYMMDD         record the signature a person states; freezes it
    python insight_ladder.py propose   <prototype> <slug> --kind "new question|fix|retire|cut" --from <jNN or qNN>
                                                                        [--level data|information|knowledge|wisdom] [--why "…"]
    python insight_ladder.py board     <Project>/insight/Insight-<name> --dataset <D> --prototype insight/Prototype-<name>
                                                                        [--title "…"] [--accumulates yes|no|?]
    python insight_ladder.py data      <board> data-v<M> --data-folder <SPACE-relative data folder>/ [--label "first 5 days"] [--new "…"]
                                       (or --extract <SPACE-relative .parquet> [--rows <n>], a lone file)
    python insight_ladder.py job       <board> --release code-v<N> --data data-v<M>   the next Job jNN_code-vN-<slug>_data-vM/
    python insight_ladder.py run       <folder> <type> [<target>]          a soft Run runs/run-<type>-<target>/
    python insight_ladder.py run       <Board Task> partition <name|all>   a hard Run runs/rNN_<partition>/ (planned)
    python insight_ladder.py goals     <Board, Prototype, Job or Task>     write each face's missing `goal:` line
    python insight_ladder.py audit     <Board, Prototype or Project>       what an older folder lacks, and the step that fixes it
    python insight_ladder.py update    <Board, Prototype or Project> [--apply]   the names, the goal lines, each Job's hash
                                       (a dry run without --apply; an older layout is named, carried by its own script)
    (add --dry-run to any command: print what it would make; change nothing)

Every page it makes carries a `goal:` line, the one line a page's header shows under its view buttons (261106): a
Board the dataset's purpose, a Prototype its questions, a release what it holds, a question Task (its face
tNN_<L><NN>_<slug>.md beside question.md) and a Board Task the question's ask, a Board Job what its release × data
version answers. `goals` backfills a face written before that line, from the same source; it writes only a missing line.

Two special boards (b11 s00, JL 261007 plan C; named by their kind, JL 261008), side by side in insight/ (JL 261109).
The Prototype, `insight/Prototype-<name>/`, holds the questions and their scripts; each of its Jobs is one code version
(a release), j0N_code-vN_<slug>/, frozen once a person signs it. The insight Board, `insight/Insight-<name>/`, holds one
dataset and its dated data versions; each of its Jobs pins one code version and one data version,
jNN_code-vN-<slug>_data-vM/ (JL 261109: "code-v1 x data-v1, make it readable"), and moves one clock from the Job before it (`moved: start |
data | code`). `job` checks the gates (the release is signed, the data version is in board.md, the pair is new, only
one clock moved), then writes the Job through ref/open_job.py: its face, a Task per question, a ticket per asked cut.
A hard Run's ticket runs ref/run_job.py. A reader knows each Block by its board.md, never its folder name; the older
bNN_ names stay readable. Every command writes only what is missing (it never overwrites a file, except the YAML it
extends: release.yaml, board.md's versions) and prints what it made. Placeholders only: a person or an agent fills
them through the insight skills. Nothing is committed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import re
import shutil
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    "soft_run", HERE.parents[3] / "1_base" / "project" / "haipipe-run" / "scripts" / "soft_run.py")
SOFT = importlib.util.module_from_spec(_spec)         # the shared soft-Run writer (haipipe-run)
_spec.loader.exec_module(SOFT)
sys.path.insert(0, str(HERE.parent / "ref"))
import open_job as OJ  # noqa: E402  (writes a Job's face, Tasks and tickets; ref/open_job.py)

QID = re.compile(r"^([DIKWX])(\d\d)$")                    # X: the Executive level (JL 261012)
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")
VERSION = re.compile(r"^j(\d+)_(code-v\d+|p\d+)(?:_([a-z0-9][a-z0-9-]*))?$")   # a release: j02_code-v2_<slug> (JL 261109; p2 older)
JOB = OJ.JOB                                                    # a Board Job: j03_code-v2-<slug>_data-v2
PROTO_NAME = re.compile(r"^(Prototype-[A-Za-z0-9][A-Za-z0-9.-]*|b\d+_.+)$")    # special board; bNN_ stays readable
BOARD_NAME = re.compile(r"^(Insight-[A-Za-z0-9][A-Za-z0-9.-]*|b\d+_.+)$")
TASK = re.compile(r"^t(\d+)_([DIKWX]\d\d)_([a-z0-9-]+)$")     # a question Task: t03_K01_<slug>
LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)   # the C loader when built (a Board has many faces)
LEVEL = {"X": "executive", "D": "data", "I": "information", "K": "knowledge", "W": "wisdom"}
KINDS = ("new question", "fix", "retire", "cut")
# run types: (level, type) -> (skill, agent, signs, hard); ref/insight-ladder.md § Runs
TYPES = {
    ("prototype", "triage-proposals"): ("haipipe-insight-question", "haipipe-insight-agent", "none", False),
    ("prototype", "open-version"): ("haipipe-insight", "haipipe-insight-agent", "none", False),
    ("prototype", "map"): ("haipipe-insight", "haipipe-insight-agent", "none", False),
    ("prototype", "carry"): ("haipipe-insight", "haipipe-insight-agent", "a person", False),
    ("version", "ask"): ("haipipe-insight-question", "haipipe-insight-agent", "none", False),
    ("version", "review-questions"): ("haipipe-report", "haipipe-insight-reviewer-agent", "a person (a change)",
                                      False),
    ("version", "set-cuts"): ("haipipe-insight", "haipipe-insight-agent", "a person (the cuts)", False),
    ("version", "sign-release"): ("haipipe-insight", "haipipe-insight-agent", "a person", False),
    ("question", "plan-evidence"): ("haipipe-insight-evidence-plan", "haipipe-insight-agent", "none", False),
    ("question", "review-plan"): ("haipipe-insight-evidence-plan", "haipipe-insight-reviewer-agent", "none", False),
    ("question", "write-script"): ("haipipe-insight", "haipipe-task-creator-agent", "none", False),
    ("question", "review-script"): ("haipipe-insight", "haipipe-task-reviewer-agent", "none", False),
    ("board", "add-version"): ("haipipe-insight-meta", "haipipe-insight-agent", "none", False),
    ("board", "add"): ("haipipe-insight", "haipipe-insight-agent", "none", False),
    ("board", "propose-cut"): ("haipipe-insight-question", "haipipe-insight-agent", "none", False),
    ("board", "propose"): ("haipipe-insight-question", "haipipe-insight-agent", "none", False),
    ("board", "coverage"): ("haipipe-insight-check", "haipipe-insight-agent", "none", False),
    ("board", "track"): ("haipipe-insight-check", "haipipe-insight-agent", "none", False),
    ("board", "consistency"): ("haipipe-insight-knowledge", "haipipe-insight-reviewer-agent", "none", False),
    ("board", "ask"): ("haipipe-report", "haipipe-insight-agent", "another agent agrees", False),
    ("board", "report"): ("haipipe-report", "haipipe-insight-agent", "none", False),
    ("board", "check"): ("haipipe-report", "haipipe-draft-check-agent", "none", False),
    ("board", "map"): ("haipipe-insight", "haipipe-insight-agent", "none", False),
    ("board", "write"): ("haipipe-insight-wisdom", "haipipe-insight-agent", "none", False),
    ("board", "draft"): ("haipipe-insight-wisdom", "haipipe-insight-agent", "a person (the handoff)", False),
    ("board", "close"): ("haipipe-insight-check", "haipipe-insight-agent", "a person", False),
    ("job", "launch"): ("haipipe-insight", "haipipe-insight-agent", "none", False),
    ("job", "power"): ("haipipe-insight", "haipipe-insight-agent", "none", False),
    ("job", "compare"): ("haipipe-insight-knowledge", "haipipe-insight-agent", "none", False),
    ("job", "propose"): ("haipipe-insight-question", "haipipe-insight-agent", "none", False),
    ("job", "overall"): ("haipipe-insight", "haipipe-insight-agent", "none", False),   # the Overall Report (JL 261012)
    ("job", "close"): ("haipipe-insight-check", "haipipe-insight-agent", "a person", False),
    ("task", "partition"): ("haipipe-insight", "haipipe-task-orchestrator-agent", "none", True),
    ("task", "write"): ("haipipe-insight-<its level>", "haipipe-insight-agent", "none", False),
    ("task", "check"): ("haipipe-report", "haipipe-draft-check-agent", "none", False),
    ("task", "pool"): ("haipipe-insight-knowledge", "haipipe-insight-agent", "none", False),
    ("task", "check-alignment"): ("haipipe-insight-check", "haipipe-insight-reviewer-agent", "none", False)}
ALONE = {("board", "coverage")}                       # a Run whose target is the whole level: run-coverage
DEFAULT_TARGET = {("prototype", "map"): "questions", ("board", "map"): "questions", ("board", "write"): "counsel",
                  ("board", "draft"): "handoff", ("board", "propose"): "coverage"}
RUN_TYPES = {level: " · ".join(t for (lv, t) in TYPES if lv == level)
             for level in ("prototype", "version", "question", "board", "job", "task")}


# ── small helpers ───────────────────────────────────────────────────────────────────────────────
class Plan:
    """What a command makes: files written (or, on a dry run, only listed)."""
    def __init__(self, dry: bool):
        self.dry, self.made = dry, []

    def write(self, path: Path, text: str, replace: bool = False) -> None:
        if path.exists() and not replace:
            return
        self.made.append(path)
        if not self.dry:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

    def copy(self, src: Path, dst: Path) -> None:
        if dst.exists():
            return
        self.made.append(dst)
        if not self.dry:
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("runs", "results", "reports", "__pycache__"))


def front(md: Path) -> tuple[dict, str]:
    """(front matter, body) of a Markdown file; ({}, text) without front matter."""
    text = md.read_text(encoding="utf-8") if md.is_file() else ""
    m = re.match(r"(?s)^---\n(.*?)\n---\n?(.*)$", text)
    return ((yaml.load(m.group(1), Loader=LOADER) or {}), m.group(2)) if m else ({}, text)


def with_front(fields: dict, body: str) -> str:
    return "---\n" + yaml.safe_dump(fields, sort_keys=False, allow_unicode=True) + "---\n" + body


def read_yaml(path: Path) -> dict:
    return (yaml.safe_load(path.read_text(encoding="utf-8")) or {}) if path.is_file() else {}


def dump_yaml(data: dict) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def today() -> str:
    return dt.date.today().strftime("%y%m%d")


def project_of(block: Path) -> Path:
    """A Block sits in <Project>/<work|insights>/<block>/."""
    return block.resolve().parent.parent


def runs_readme(folder: Path, level: str, plan: Plan) -> None:
    plan.write(folder / "runs" / "README.md", f"# Runs of {folder.name}\n\nrun types: {RUN_TYPES[level]}\n\n"
               "One folder per Run: a soft Run is `run-<type>-<target>/` (run.yaml · its ticket · passes/), a hard Run "
               "is `rNN_<partition>/` (run.yaml · result/). See haipipe-insight ref/insight-ladder.md § Runs.\n")


# ── the Prototype Block ─────────────────────────────────────────────────────────────────────────
def versions(proto: Path) -> list[Path]:
    return sorted((p for p in proto.iterdir() if p.is_dir() and VERSION.match(p.name)),
                  key=lambda p: int(VERSION.match(p.name).group(1))) if proto.is_dir() else []


def release(version: Path) -> dict:
    return read_yaml(version / "release.yaml")


def face(folder: Path) -> dict:
    return front(folder / f"{folder.name}.md")[0]


def prototype_goal(title: str) -> str:
    """A Prototype's goal line: its questions, in its title's words."""
    words = (title or "the questions and their scripts").strip()
    return f"{words[:1].upper()}{words[1:]}, one signed code version at a time"


def prototype(path: Path, serves: str, title: str, plan: Plan) -> None:
    if not PROTO_NAME.match(path.name):
        sys.exit(f"a Prototype is a special board, Prototype-<name> (or the older bNN_<topic>): {path.name}")
    if path.parent.name not in ("insight", "insights", "tasks", "work"):    # tasks/ and work/: the older place
        sys.exit(f"a Prototype lives in <Project>/insight/, beside the Board it serves: {path}")
    plan.write(path / "board.md", with_front(
        {"board-kind": "prototype", "serves": serves, "goal": prototype_goal(title)},
        f"\n# {path.name} · {title or 'the Prototype'}\n\n"
        "The questions and their scripts, one Job per code version (`jNN_code-vN_<slug>/`), frozen once a person signs\n"
        "it. A Board's Job pins one code version and one data version; a code version is cut from proposals/.\n"))
    plan.write(path / "proposals" / "README.md", "# proposals\n\nThe backlog: new question · fix · retire · cut, one file "
               "each (`<slug>.md`: kind · level · from <job or report> · state · why). The next release is cut from here "
               "(run-triage-proposals).\n")
    runs_readme(path, "prototype", plan)


def version(proto: Path, slug: str, plan: Plan) -> Path:
    """The next code version: jNN_code-vN_<slug>/ with release.yaml; it starts from the newest one (every question kept).
    The slug says what it is (JL 261008); its id is code-vN everywhere it is named (JL 261109)."""
    if slug and not SLUG.match(slug):
        sys.exit(f"--slug is a few lower-case words joined by -: {slug!r}")
    if face_kind(proto) != "prototype":
        sys.exit(f"{proto.name} is not a Prototype Block (board.md board-kind: prototype)")
    old = versions(proto)
    if old and str(face(old[-1]).get("state")) != "closed":
        sys.exit(f"{old[-1].name} is still open: sign it (or work in it) before opening the next version")
    n = int(VERSION.match(old[-1].name).group(1)) + 1 if old else 1
    rel = f"code-v{n}"
    path = proto / (f"j{n:02d}_{rel}_{slug}" if slug else f"j{n:02d}_{rel}")
    prev = old[-1] if old else None
    kept = len(release(prev).get("questions") or {}) if prev else 0
    cuts = len(front(prev / "partitions.md")[0].get("partitions") or []) if prev else 0
    plan.write(path / f"{path.name}.md", with_front(
        {"release": rel, "state": "open", "signed": "", "from": VERSION.match(prev.name).group(2) if prev else "",
         "goal": release_goal(n, slug.replace("-", " "), kept, cuts)},
        f"\n# code-v{n}\n\n<what this code version changes, and which proposals it takes>\n"))
    rows = {}
    if prev:
        for q, row in (release(prev).get("questions") or {}).items():
            task = (prev / row["task"]).resolve()
            rows[q] = {"task": _rel(task, path), "change": "kept"}
        for f in ("partitions.md", "thresholds.yaml"):
            if (prev / f).is_file():
                plan.write(path / f, (prev / f).read_text(encoding="utf-8"))
        if (prev / "src").is_dir():
            plan.copy(prev / "src", path / "src")             # the shared code the scripts import
    else:
        plan.write(path / "partitions.md", with_front(
            {"partitions": [{"name": "full", "where": [], "why": "every row"},
                            {"name": "<name>", "where": [{"column": "<col>", "eq": "<value>"}], "why": "<why>"},
                            {"name": "cross", "of": ["<name>", "<name>"], "why": "one test of the difference"}]},
            "\n# The cuts\n\nPart of the plan, fixed before any outcome (run-set-cuts; a person signs them).\n"))
        plan.write(path / "thresholds.yaml", dump_yaml(
            {"power": {"smallest_effect_pp": "<pp>", "alpha": 0.05, "target_power": 0.8}}))
    plan.write(path / "release.yaml", dump_yaml({"release": rel, "questions": rows}))
    runs_readme(path, "version", plan)
    return path


def release_goal(n: int, words: str, questions: int, cuts) -> str:
    """A release's goal line: what it is for, in words, no count (b11 round 2: "take the counts out of the goal line";
    how many questions and cuts is its page's main line): `code-v1, example questions: the questions and their scripts
    on the cuts it fixes`; a release still without questions says what it will hold."""
    head = f"code-v{n}" + (f", {words}" if words else "")
    if not questions:
        return f"{head}: its questions and their scripts, frozen once a person signs it"
    return f"{head}: the questions and their scripts" + (" on the cuts it fixes" if cuts else "")


def _rel(target: Path, base: Path) -> str:
    """target relative to base, as written in release.yaml (a Task here is just its name)."""
    import os
    return Path(os.path.relpath(target, base.resolve())).as_posix()


def _version_open(ver: Path) -> None:
    if not VERSION.match(ver.name) or face_kind(ver.parent) != "prototype":
        sys.exit(f"{ver.name} is not a Prototype version (insight/Prototype-<name>/jNN_code-vN_<slug>/)")
    if str(face(ver).get("state")) == "closed":
        sys.exit(f"{ver.name} is signed and frozen: open the next version (insight_ladder.py version)")


def _task_number(proto: Path, qid: str) -> int:
    """A question keeps its tNN in every version and every Job; a new one takes the next number."""
    seen = {}
    for ver in versions(proto):
        for q, row in (release(ver).get("questions") or {}).items():
            m = TASK.match(Path(row["task"]).name)
            if m:
                seen[q] = int(m.group(1))
        for q in (release(ver).get("retired") or {}):
            for t in ver.glob(f"t*_{q}_*"):
                seen.setdefault(q, int(TASK.match(t.name).group(1)))
    return seen.get(qid) or (max(seen.values(), default=0) + 1)


def question_face(task: Path, fields: dict) -> str:
    """A question Task's face (tNN_<L><NN>_<slug>.md beside question.md): the page's title and its goal line, the ask
    as question.md holds it; no goal while the ask is still a placeholder (`goals` writes it once it is filled)."""
    ask = str(fields.get("ask") or "").strip()
    qid = str(fields.get("id") or TASK.match(task.name).group(2))
    short = str(fields.get("question") or fields.get("name") or "").strip()
    head = {"goal": ask} if ask and not ask.startswith("<") else {}
    return with_front(head, f"\n# {qid} · {short if short and not short.startswith('<') else task.name.split('_', 2)[-1]}"
                      "\n\nThe question, its needs and its agreed mark live in `question.md`; its scripts in `scripts/`.\n")


def question(ver: Path, qid: str, slug: str, plan: Plan, ask: str = "") -> Path:
    _version_open(ver)
    m = QID.match(qid or "")
    if not m or not SLUG.match(slug or ""):
        sys.exit("a question is: question <version> <L><NN> <slug>  (L = X · D · I · K · W; slug lower-case, -)")
    rel = release(ver)
    if qid in (rel.get("questions") or {}):
        sys.exit(f"{qid} is already in {ver.name}: change it (insight_ladder.py change), never ask it twice")
    for old in versions(ver.parent):
        if qid in (release(old).get("questions") or {}) or qid in (release(old).get("retired") or {}):
            sys.exit(f"{qid} was asked in {old.name}: an id is never reused; take the next number")
    path = ver / f"t{_task_number(ver.parent, qid):02d}_{qid}_{slug}"
    plan.write(path / "question.md", with_front(
        {"id": qid, "level": LEVEL[m.group(1)], "question": "<the short question a reader scans>",
         "name": slug.replace("-", " "), "ask": ask or "<the full question, one sentence, as its asker wrote it>",
         "method": {"ask": "<a card>", "answer": "<a card>", "read": "<a card>"},
         "partitions": {"asked": "all", "power": "none"}, "needs": {}, "agreed": "⬜", "signed": ""},
        f"\n{slug.replace('-', ' ').capitalize()}\n{'=' * len(slug)}\n\n**Why now**: <why the Board asks it now>\n\n"
        "**What would answer it**: <the evidence in words, before any need>\n"))
    plan.write(path / f"{path.name}.md", question_face(path, {"id": qid, "ask": ask, "name": slug.replace("-", " ")}))
    rel.setdefault("questions", {})[qid] = {"task": path.name, "change": "new"}
    plan.write(ver / "release.yaml", dump_yaml(rel), replace=True)
    return path


def change(ver: Path, qid: str, why: str, plan: Plan) -> Path:
    """Carry a kept question into this version, so it can change here; the earlier version keeps its own."""
    _version_open(ver)
    rel = release(ver)
    row = (rel.get("questions") or {}).get(qid)
    if not row:
        sys.exit(f"{qid} is not in {ver.name}: ask it (insight_ladder.py question)")
    if not why:
        sys.exit("--why says what changes, in one line")
    home = (ver / row["task"]).resolve()
    if home.parent == ver.resolve():
        sys.exit(f"{qid} already lives in {ver.name}: change it in place")
    path = ver / home.name
    plan.copy(home, path)
    if not plan.dry:
        fields, body = front(path / "question.md")
        fields["agreed"], fields["signed"] = "⬜", ""
        fields.setdefault("changes", []).append({"in": rel.get("release"), "change": why})
        (path / "question.md").write_text(with_front(fields, body), encoding="utf-8")
    rel["questions"][qid] = {"task": path.name, "change": f"changed: {why}"}
    plan.write(ver / "release.yaml", dump_yaml(rel), replace=True)
    return path


def retire(ver: Path, qid: str, why: str, plan: Plan) -> None:
    _version_open(ver)
    rel = release(ver)
    if qid not in (rel.get("questions") or {}):
        sys.exit(f"{qid} is not asked in {ver.name}")
    if not why:
        sys.exit("--why says why it retires, in one line")
    rel["questions"].pop(qid)
    rel.setdefault("retired", {})[qid] = why
    plan.write(ver / "release.yaml", dump_yaml(rel), replace=True)


def sign(ver: Path, date: str, plan: Plan) -> None:
    """Record the signature a person states (✅ <YYMMDD>; never a name) and freeze the version."""
    _version_open(ver)
    if not re.fullmatch(r"\d{6}", date or ""):
        sys.exit("--date is the day the person signed, YYMMDD")
    unagreed = []
    for q, row in (release(ver).get("questions") or {}).items():
        task = (ver / row["task"]).resolve()
        if task.parent == ver.resolve() and not str(front(task / "question.md")[0].get("agreed", "")).startswith("✅"):
            unagreed.append(q)
    if unagreed:
        sys.exit(f"not agreed yet (another agent agrees each new or changed question's needs): {', '.join(unagreed)}")
    parts = front(ver / "partitions.md")[0].get("partitions") or []
    if not any(p.get("name") == "full" for p in parts) or any("<" in str(p.get("name")) for p in parts):
        sys.exit(f"{ver.name}/partitions.md: set the cuts first (run-set-cuts): `full` and every cut named")
    fields, body = front(ver / f"{ver.name}.md")
    fields.update(state="closed", signed=f"✅ {date}")
    plan.write(ver / f"{ver.name}.md", with_front(fields, body), replace=True)


def propose(proto: Path, slug: str, kind: str, source: str, level: str, why: str, plan: Plan) -> Path:
    """A proposal into the Prototype's proposals/: the only way a question or a cut reaches a new version."""
    if face_kind(proto) != "prototype":
        sys.exit(f"{proto.name} is not a Prototype Block (board.md board-kind: prototype)")
    if kind not in KINDS:
        sys.exit(f"--kind is one of: {' · '.join(KINDS)}")
    if not SLUG.match(slug or "") or not source:
        sys.exit("a proposal is: propose <prototype> <slug> --kind … --from <the Job, report or reading it came from>")
    path = proto / "proposals" / f"{slug}.md"
    if path.exists():
        sys.exit(f"proposals/{slug}.md exists: one file per proposal; name this one differently")
    fields = {"kind": kind, "level": level or "", "from": source, "state": "open", "taken-in": ""}
    plan.write(path, with_front(fields, f"\n# {slug.replace('-', ' ').capitalize()}\n\n{why or '<why, in a line or two>'}\n"))
    return path


# ── the insight Board ───────────────────────────────────────────────────────────────────────────
def face_kind(block: Path) -> str:
    fm = front(block / "board.md")[0]
    if fm.get("board-kind") == "prototype":
        return "prototype"
    if fm.get("board-kind") == "insight-board" or fm.get("prototype"):
        return "board"
    return ""


def board_goal(title: str, dataset: str) -> str:
    """An insight Board's goal line, the dataset's purpose: its title's words after `<dataset>:` (`Insight · Example:
    what a two-arm dataset says` -> `What a two-arm dataset says`), else what the dataset says, freeze by freeze."""
    words = str(title or "").split(" · ", 1)[-1].strip()
    if dataset and words.lower().startswith(dataset.lower() + ":"):
        words = words[len(dataset) + 1:].strip()
    if not words or words.startswith(("Insight-", "<")) or words == dataset:
        words = f"what {dataset or 'the dataset'} says, data version by data version"
    return words[:1].upper() + words[1:]


def board(path: Path, dataset: str, proto: str, title: str, accumulates: str, plan: Plan) -> None:
    if path.parent.name not in ("insight", "insights"):          # insights/ is the older name (s01-D29)
        sys.exit(f"an insight Board lives in <Project>/insight/: {path}")
    if not BOARD_NAME.match(path.name):
        sys.exit(f"an insight Board is a special board, Insight-<name> (or the older bNN_<topic>): {path.name}")
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", dataset or "") or re.search(r"v\d+$", dataset):
        sys.exit("--dataset is a short name, letters and digits, carrying no version (<D>, not <D>v1): its "
                 "versions are data-v1, data-v2, … in board.md versions:")
    if face_kind(project_of(path) / proto) != "prototype":
        sys.exit(f"--prototype {proto}: no Prototype Block there yet (insight_ladder.py prototype)")
    plan.write(path / "board.md", with_front(
        {"board-kind": "insight-board", "workbench": "insight", "dataset": dataset, "prototype": proto,
         "accumulates": accumulates, "goal": board_goal(title, dataset), "versions": []},
        f"\n# {title or path.name}\n\nOne dataset, its data versions, and one Job per pair (code version × data "
        "version).\n\n## Questions\n\n```yaml\nquestions: []\n```\n"))
    plan.write(path / "meta" / "meta.md", f"# {dataset} · what the extract holds\n\n<grain · window · sources · "
               "limits; one line per data version on what is new>\n")
    runs_readme(path, "board", plan)


def data(path: Path, ver: str, extract: str, rows: str, new: str, plan: Plan, folder: str = "", label: str = "") -> None:
    if face_kind(path) != "board":
        sys.exit(f"{path.name} is not an insight Board (board.md board-kind: insight-board)")
    if not re.fullmatch(r"data-v\d+", ver or "") or not (extract or folder):
        sys.exit("a data version is: data <board> data-v<M> --data-folder <its data folder>/ (or --extract <one .parquet>)")
    if (extract or folder).startswith("/"):
        sys.exit("--data-folder and --extract are SPACE-relative (or through a variable), never absolute (AGENTS.md rule 7)")
    fields, body = front(path / "board.md")
    have = [str(v.get("version")) for v in fields.get("versions") or []]
    if ver in have:
        sys.exit(f"{ver} is already a data version of {path.name}; a new extract is the next version")
    want = f"data-v{len(have) + 1}"
    if ver != want:
        sys.exit(f"the next data version is {want}")
    # a folder (JL 261008): the data file, its manifest, dictionary, summary, figures and docs; the workbench
    # reads them all, the Runs find the data file in it (run_job.version_extract)
    entry = ({"version": ver, "folder": folder.rstrip("/") + "/", "frozen": today()} if folder else
             {"version": ver, "extract": extract, "frozen": today(), "rows": rows or "<n>"})
    if label:                                  # the data version's few words, shown as data-v<M> · <label> (JL 261109)
        entry = {"version": ver, "label": label, **{k: v for k, v in entry.items() if k != "version"}}
    fields.setdefault("versions", []).append(dict(entry, new=new or "<what is new>"))
    plan.write(path / "board.md", with_front(fields, body), replace=True)


def jobs(block: Path) -> list[Path]:
    return sorted((p for p in block.iterdir() if p.is_dir() and JOB.match(p.name)),
                  key=lambda p: int(JOB.match(p.name).group(1)))


def release_hash(ver: Path) -> str:
    """The first 12 hex of a sha256 over the release: release.yaml, the cuts, the thresholds, every question's files."""
    h = hashlib.sha256()
    files = [ver / "release.yaml", ver / "partitions.md", ver / "thresholds.yaml"]
    for row in (release(ver).get("questions") or {}).values():
        task = (ver / row["task"]).resolve()
        files += sorted(p for p in task.rglob("*") if p.is_file() and "__pycache__" not in p.parts
                        and p != task / f"{task.name}.md")    # its face is the page's title and goal line, not the plan
    for f in files:
        if f.is_file():
            h.update(f.name.encode() + b"\0" + f.read_bytes())
    return h.hexdigest()[:12]


def job(block: Path, rel: str, ver: str, plan: Plan) -> Path:
    """The next Job: one code version × one data version, its Tasks one per question of the code version."""
    if face_kind(block) != "board":
        sys.exit(f"{block.name} is not an insight Board (board.md board-kind: insight-board)")
    fm = front(block / "board.md")[0]
    proto = project_of(block) / str(fm.get("prototype"))
    pver = next((v for v in versions(proto) if VERSION.match(v.name).group(2) == rel), None)
    if pver is None:
        sys.exit(f"{rel} is not a version of {proto.name}: open and sign it first")
    if str(face(pver).get("state")) != "closed" or not str(face(pver).get("signed", "")).startswith("✅"):
        sys.exit(f"{pver.name} is not signed: a person signs a release before a Board runs it (run-sign-release)")
    if ver not in [str(v.get("version")) for v in fm.get("versions") or []]:
        sys.exit(f"{ver} is not a data version of {block.name}: add it first (insight_ladder.py data, run-add-version)")
    old = jobs(block)
    pairs = {(JOB.match(j.name).group(2), JOB.match(j.name).group(4)) for j in old}
    if (rel, ver) in pairs:
        sys.exit(f"{block.name} already runs {rel} on {ver}: one Job per pair")
    prev = old[-1] if old else None
    moved = "start"
    if prev:
        prel, pver_ = JOB.match(prev.name).group(2), JOB.match(prev.name).group(4)
        if prel != rel and pver_ != ver:
            sys.exit(f"one clock per Job: {prev.name} ran {prel} on {pver_}; add {rel} on {pver_} (or {prel} on {ver}) "
                     "first, so each Job's change has one cause")
        moved = "code" if prel != rel else "data"
    n = int(JOB.match(prev.name).group(1)) + 1 if prev else 1
    path = block / OJ.job_name(n, rel, OJ.release_slug(pver), fm["dataset"], ver)
    if plan.dry:
        plan.made.append(path / f"{path.name}.md")
        return path
    made_job, made = OJ.open_job(block, rel, ver, previous=prev.name if prev else "", moved=moved, number=n)
    fields, body = front(made_job / f"{made_job.name}.md")
    if "hash" not in fields:                              # the release's hash: what a later Job compares against
        fields = {**{k: fields[k] for k in ("release", "prototype") if k in fields}, "hash": release_hash(pver),
                  **{k: v for k, v in fields.items() if k not in ("release", "prototype")}}
        (made_job / f"{made_job.name}.md").write_text(with_front(fields, body), encoding="utf-8")
    plan.made += made
    runs_readme(path, "job", plan)
    return path


# ── the goal lines, backfilled ──────────────────────────────────────────────────────────────────────
def _title(md: Path) -> str:
    """A face's `# ` heading, its words."""
    return next((ln[2:].strip() for ln in front(md)[1].splitlines() if ln.startswith("# ")), "")


def add_goal(md: Path, goal: str, plan: Plan) -> None:
    """Write `goal:` into a face's front matter when it has none, the rest of the file as it was; never a second line,
    never over a goal a person wrote."""
    goal = " ".join(str(goal or "").split())
    if not goal or goal.startswith("<") or not md.is_file():
        return
    text = md.read_text(encoding="utf-8")
    m = re.match(r"(?s)^---\n(.*?)\n---\n", text)
    if m and "goal" in (yaml.load(m.group(1), Loader=LOADER) or {}):
        return
    line = yaml.safe_dump({"goal": goal}, allow_unicode=True, width=10_000).strip()
    new = (text[:m.end(1)] + "\n" + line + text[m.end(1):]) if m else f"---\n{line}\n---\n" + text
    plan.write(md, new, replace=True)


def _release_goal_of(ver: Path) -> str:
    rel_, fm = release(ver), face(ver)
    m = VERSION.match(ver.name)
    words = str(fm.get("title") or (m.group(3) or "").replace("-", " "))
    cuts = len(front(ver / "partitions.md")[0].get("partitions") or [])
    return release_goal(int(m.group(1)), words, len(rel_.get("questions") or {}), cuts)


def _question_goal(task: Path, plan: Plan) -> None:
    fields = front(task / "question.md")[0]
    md = task / f"{task.name}.md"
    if not md.is_file():
        plan.write(md, question_face(task, fields))
    else:
        add_goal(md, str(fields.get("ask") or ""), plan)


def goals(folder: Path, plan: Plan) -> None:
    """Each face's missing goal line under `folder` (a Board, a Prototype, a release, a Job, a Task), from the same
    source its generator reads: a Board's title, a Prototype's title, a release's questions and cuts, a Job's release
    and data version, a question's ask."""
    level = level_of(folder)
    if level == "prototype":
        add_goal(folder / "board.md", prototype_goal(_title(folder / "board.md").split(" · ", 1)[-1]
                                                     if " · " in _title(folder / "board.md") else ""), plan)
        for ver in versions(folder):
            goals(ver, plan)
    elif level == "version":
        add_goal(folder / f"{folder.name}.md", _release_goal_of(folder), plan)
        for t in sorted(p for p in folder.iterdir() if p.is_dir() and TASK.match(p.name) and (p / "question.md").is_file()):
            _question_goal(t, plan)
    elif level == "question":
        _question_goal(folder, plan)
    elif level == "board":
        fm = front(folder / "board.md")[0]
        add_goal(folder / "board.md", board_goal(_title(folder / "board.md"), str(fm.get("dataset") or "")), plan)
        for j in jobs(folder):
            goals(j, plan)
    elif level == "job":
        add_goal(folder / f"{folder.name}.md", OJ.job_goal(folder.parent, face(folder)), plan)
        for t in sorted(p for p in folder.iterdir() if p.is_dir() and TASK.match(p.name)):
            goals(t, plan)
    elif level == "task":
        q = OJ.question_fields(folder.parent.parent, face(folder.parent), TASK.match(folder.name).group(2))
        add_goal(folder / f"{folder.name}.md", str(q.get("ask") or q.get("question") or ""), plan)


# ── audit and update: bring an older insight folder onto the current contract (JL 261109) ──────────────────────────
def _spec_sha(*paths: Path) -> str:
    """The receipt's hash of a question's spec or scripts (run_question.sha256, without loading pandas)."""
    h = hashlib.sha256()
    for p in paths:
        files = [p] if p.is_file() else sorted(x for x in p.rglob("*") if x.is_file() and "__pycache__" not in x.parts
                                               and x.name != "prototype.lock")
        for f in files:
            h.update(f.name.encode())
            h.update(f.read_bytes())
    return h.hexdigest()


def boards_of(folder: Path) -> list[Path]:
    """The insight Boards a folder names: a Board itself, the Board a Prototype serves, or each Board of a Project."""
    folder = folder.resolve()
    kind = face_kind(folder) if (folder / "board.md").is_file() else ""
    if kind == "board":
        return [folder]
    if kind == "prototype":
        b = project_of(folder) / str(front(folder / "board.md")[0].get("serves", ""))
        return [b] if face_kind(b) == "board" else []
    return sorted(b for d in ("insight", "insights") for b in (folder / d).glob("*/") if face_kind(b) == "board")


def older_layout(folder: Path) -> str:
    """The step for a folder made before the Prototype and the Board (it is carried, not renamed), else ''."""
    fm = front(folder / "board.md")[0]
    if folder.name.endswith("-InsightBoard") or (folder / "0-MT-meta").is_dir():
        return "a register board: carry it with ref/carry_over.py, then ref/prototype_from_block.py"
    if fm.get("workbench") == "insight" and (folder / "j01_data").is_dir():
        return "an Insight Block (one Job per level): carry it with ref/prototype_from_block.py"
    return ""


def _release_of(j: Path) -> Path:
    return project_of(j.parent) / str(face(j).get("prototype", ""))


def stale_receipts(board: Path) -> list[Path]:
    """Each hard Run whose receipt was made from another question.md or scripts than the release holds now."""
    out = []
    for rt in sorted(board.glob("j*/t*/runs/r*/result/runtime.yaml")):
        r = read_yaml(rt)
        task = rt.parents[3]
        m = TASK.match(task.name)
        q = next(iter(sorted(_release_of(task.parent).glob(f"t*_{m.group(2)}_*/question.md"))), None) if m else None
        if q is None or r.get("spec_sha256") != _spec_sha(q) or (
                r.get("scripts_sha256") and (q.parent / "scripts").is_dir()
                and r.get("scripts_sha256") != _spec_sha(q.parent / "scripts")):
            out.append(rt.parents[1])
    return out


def audit(folder: Path, quiet: bool = False) -> list[tuple]:
    """What each Board (and its Prototype) still lacks against ref/insight-ladder.md, one row per check:
    (Board, check, count, the step that fixes it). Read-only."""
    import rename_code_data as RN
    rows = []
    for b in boards_of(folder) or [folder.resolve()]:
        step = older_layout(b)
        if step:
            rows.append((b, "layout", 1, step))
            continue
        edits, renames, move = RN.plan(b, [])
        rows.append((b, "names", len(edits) + len(renames) + bool(move),
                     "update --apply (ref/rename_code_data.py: code-vN, data-vM, the Prototype in insight/)"))
        gp = Plan(True)
        goals(b, gp) if not (edits or renames or move) else None
        rows.append((b, "goals", len(gp.made), "update --apply (insight_ladder.py goals)"))
        pins = [j for j in jobs(b) if not (edits or renames or move)
                and _release_of(j).is_dir() and str(face(j).get("hash", "")) != release_hash(_release_of(j))]
        rows.append((b, "hash", len(pins), "update --apply (each Job's hash: re-pinned to its release)"))
        st = stale_receipts(b) if not (edits or renames or move) else []
        rows.append((b, "receipts", len(st), "rerun each ticket: bash <Run>/run.sh (needs env.sh at the SPACE root)"))
    if not quiet:
        for b, check, n, step in rows:
            print(f"{'✅' if n == 0 else '❗'} {b.name:<28} {check:<9} {n:>4}" + ("" if n == 0 else f"   ▶ {step}"))
        if any(r[1] == "names" and r[2] for r in rows):
            print("(goals, hash and receipts are checked after the names are current)")
    return rows


def update(folder: Path, apply: bool) -> list[tuple]:
    """Bring each Board and its Prototype onto the current contract, in order: the names (code-vN × data-vM, the
    Prototype beside its Board), the missing goal lines, each Job's hash re-pinned to its release. A dry run unless
    `apply`; an older layout is only named (it is carried, by its own script); stale receipts are listed to rerun."""
    import rename_code_data as RN
    for b in boards_of(folder) or [folder.resolve()]:
        step = older_layout(b)
        if step:
            print(f"❗ {b.name}: {step}; update does not carry it")
            continue
        edits, renames, move = RN.plan(b, [])
        print(f"{b.name} · names: {len(edits)} files rewritten · {len(renames)} names · "
              f"{'1 Prototype moved' if move else 'Prototype stays'}")
        if (edits or renames or move) and not apply:
            print("  dry run: rerun with --apply; goals and hash are planned once the names are current")
            continue
        if apply:
            for p, _, new in edits:
                p.write_text(new, encoding="utf-8")
            for src, dst in renames:
                src.rename(dst)
            if move:
                if move[1].exists():
                    sys.exit(f"{move[1]} exists; nothing moved")
                move[1].parent.mkdir(parents=True, exist_ok=True)
                move[0].rename(move[1])
        gp = Plan(not apply)
        goals(b, gp)
        print(f"{b.name} · goals: {len(gp.made)} {'written' if apply else 'missing'}")
        for j in jobs(b):
            rel = _release_of(j)
            want, have = (release_hash(rel), str(face(j).get("hash", ""))) if rel.is_dir() else ("", "")
            if want and want != have:
                print(f"{b.name} · hash: {j.name} {have or '—'} -> {want}")
                if apply:
                    md = j / f"{j.name}.md"
                    text = md.read_text(encoding="utf-8")
                    text = (re.sub(r"(?m)^hash: .*$", f"hash: {want}", text, count=1) if re.search(r"(?m)^hash: ", text)
                            else re.sub(r"(?m)^(prototype: .*)$", rf"\1\nhash: {want}", text, count=1))
                    md.write_text(text, encoding="utf-8")
        st = stale_receipts(b)
        print(f"{b.name} · receipts: {len(st)} made from an older question or script")
        for r in st:
            print(f"  bash {r / 'run.sh'}")
    return audit(folder, quiet=not apply) if apply else []


# ── a Run ───────────────────────────────────────────────────────────────────────────────────────
def level_of(folder: Path) -> str:
    name = folder.name
    if (folder / "board.md").is_file():
        kind = face_kind(folder)
        if kind:
            return kind
    if VERSION.match(name) and face_kind(folder.parent) == "prototype":
        return "version"
    if JOB.match(name) and face_kind(folder.parent) == "board":
        return "job"
    if TASK.match(name):                       # an older Board Job's name (j01_p1_<D>v1) fits VERSION: ask the face above
        above = face_kind(folder.parent.parent)
        if VERSION.match(folder.parent.name) and above == "prototype":
            return "question"
        if JOB.match(folder.parent.name) and above == "board":
            return "task"
    sys.exit(f"not an insight Block, version, Job or Task folder: {folder}")


def _default_target(folder: Path, level: str, rtype: str) -> str:
    if (level, rtype) in DEFAULT_TARGET:
        return DEFAULT_TARGET[(level, rtype)]
    name = folder.name
    if level == "version":
        return VERSION.match(name).group(2)                        # code-v2
    if level == "question":
        return TASK.match(name).group(2).lower()                   # k01
    if level == "job":
        return name.split("_", 1)[0]                               # j03
    if level == "task":
        return name.split("_", 1)[0]                               # t03
    sys.exit(f"a {level} Run needs its target: run {name} {rtype} <target>")


def _partitions(task: Path) -> list[dict]:
    jf = face(task.parent)
    ver = project_of(task.parent.parent) / str(jf.get("prototype", ""))
    parts = front(ver / "partitions.md")[0].get("partitions") or []
    return parts                                      # rNN = the cut's place in partitions.md (open_job.py)


def hard_run(task: Path, which: str, plan: Plan) -> list[Path]:
    parts = _partitions(task)
    names = [p["name"] for p in parts]
    if not names:
        sys.exit(f"{task.parent.name}'s release has no cuts (partitions.md)")
    pick = names if which == "all" else [which]
    for p in pick:
        if p not in names:
            sys.exit(f"{p} is not a cut of this release: {', '.join(names)}")
    jf, qid = face(task.parent), TASK.match(task.name).group(2)
    out = []
    for p in pick:
        k = names.index(p) + 1
        path = task / "runs" / f"r{k:02d}_{p}"
        cross = "of" in parts[k - 1]
        plan.write(path / "run.sh", OJ.TICKET)               # the same lines in every ticket (ref/open_job.py)
        if not plan.dry and (path / "run.sh").exists():
            (path / "run.sh").chmod(0o755)
        plan.write(path / "run.yaml", dump_yaml(
            {"run": path.name, "kind": "hard", "type": "cross" if cross else "partition", "partition": p,
             "target": task.name, "question": qid, "script": jf.get("hash", ""), "release": jf.get("release", ""),
             "data": jf.get("data", ""), "status": "planned", "passes": 0}))
        out.append(path)
    return out


def run(folder: Path, rtype: str, target: str, plan: Plan) -> list[Path]:
    level = level_of(folder)
    if (level, rtype) not in TYPES:
        sys.exit(f"run-{rtype} does not run at the {level} level; its run types: {RUN_TYPES[level]}")
    skill, agent, signs, hard = TYPES[(level, rtype)]
    if hard:
        return hard_run(folder, target or "all", plan)
    if level == "task" and rtype == "write":
        letter = TASK.match(folder.name).group(2)[0]          # an Executive page is the door's own: no level skill
        skill = "haipipe-insight" if letter == "X" else f"haipipe-insight-{LEVEL[letter]}"
    if (level, rtype) in ALONE:
        path = folder / "runs" / f"run-{rtype}"
        if not path.exists() and not plan.dry:
            path.mkdir(parents=True)
            SOFT.write_card(path, {"run": path.name, "kind": "soft", "type": rtype, "scope": None, "target": "every Job",
                                   "ticket": None, "skill": skill, "agent": agent, "signs": [signs], "status": "planned",
                                   "passes": [], "writes": [], "feeds": []})
        plan.made.append(path / "run.yaml")
        return [path]
    target = (target or _default_target(folder, level, rtype)).lower()
    path = folder / "runs" / f"run-{rtype}-{target}"
    if path.exists():
        return [path]
    plan.made.append(path / "run.yaml")
    if not plan.dry:
        SOFT.new(folder, rtype, target, skill=skill, agent=agent, signs=[signs])
    return [path]


def main(argv=None) -> list[Path]:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=("prototype", "version", "question", "change", "retire", "sign", "propose",
                                        "board", "data", "job", "run", "goals", "audit", "update"))
    ap.add_argument("folder", type=Path)
    ap.add_argument("what", nargs="?", default="", help="question/change/retire: <L><NN>; propose: <slug>; "
                                                        "data: v<M>; run: its type")
    ap.add_argument("extra", nargs="?", default="", help="question: <slug>; run: its target (or a partition)")
    ap.add_argument("--serves", default="")
    ap.add_argument("--slug", default="", help="version: what the code version is, jNN_code-vN_<slug>")
    ap.add_argument("--title", default="")
    ap.add_argument("--ask", default="", help="question: the full question, one sentence (its page's goal line)")
    ap.add_argument("--why", default="")
    ap.add_argument("--date", default="")
    ap.add_argument("--kind", default="")
    ap.add_argument("--from", dest="source", default="")
    ap.add_argument("--level", default="", choices=("", "executive", "data", "information", "knowledge", "wisdom"))
    ap.add_argument("--dataset", default="")
    ap.add_argument("--prototype", default="")
    ap.add_argument("--accumulates", default="?", choices=("yes", "no", "?"))
    ap.add_argument("--extract", default="")
    ap.add_argument("--data-folder", dest="data_folder", default="")
    ap.add_argument("--rows", default="")
    ap.add_argument("--new", default="")
    ap.add_argument("--label", default="")
    ap.add_argument("--release", default="")
    ap.add_argument("--data", default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true", help="update: write (a dry run without it)")
    a = ap.parse_args(argv)
    plan = Plan(a.dry_run)
    c = a.command
    if c == "prototype":
        prototype(a.folder, a.serves or "insight/<board>", a.title, plan)
    elif c == "version":
        version(a.folder, a.slug, plan)
    elif c == "question":
        question(a.folder, a.what, a.extra, plan, a.ask)
    elif c == "change":
        change(a.folder, a.what, a.why, plan)
    elif c == "retire":
        retire(a.folder, a.what, a.why, plan)
    elif c == "sign":
        sign(a.folder, a.date, plan)
    elif c == "propose":
        propose(a.folder, a.what, a.kind, a.source, a.level, a.why, plan)
    elif c == "board":
        board(a.folder, a.dataset, a.prototype, a.title, a.accumulates, plan)
    elif c == "data":
        data(a.folder, a.what, a.extract, a.rows, a.new, plan, a.data_folder, a.label)
    elif c == "job":
        job(a.folder, a.release, a.data, plan)
    elif c == "goals":
        goals(a.folder, plan)
    elif c == "audit":
        audit(a.folder)
        return []
    elif c == "update":
        update(a.folder, a.apply)
        return []
    else:
        if not a.what:
            ap.error("run needs a type, e.g. add, compare, partition")
        run(a.folder, a.what, a.extra, plan)
    for p in plan.made:
        print(("would make " if a.dry_run else "made ") + str(p))
    return plan.made


if __name__ == "__main__":
    main()

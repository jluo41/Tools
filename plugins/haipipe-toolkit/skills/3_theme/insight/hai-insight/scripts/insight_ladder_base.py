"""What every insight_ladder command shares: the names' patterns, the run types of each level, the Plan that writes
(or only lists) files, and the front-matter readers."""

from __future__ import annotations

import datetime as dt
import importlib.util
import re
import shutil
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    "soft_run", HERE.parents[3] / "1_base" / "project" / "hai-run" / "scripts" / "soft_run.py")
SOFT = importlib.util.module_from_spec(_spec)         # the shared soft-Run writer (hai-run)
_spec.loader.exec_module(SOFT)
sys.path.insert(0, str(HERE.parent / "ref"))
import open_job as OJ  # noqa: E402  (writes a Job's face, Tasks and tickets; ref/open_job.py)

QID = re.compile(r"^([DIKWX])(\d\d)$")                    # X: the Executive level
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")
VERSION = re.compile(r"^j(\d+)_((?:question|code)-v\d+|p\d+)(?:_([a-z0-9][a-z0-9-]*))?$")   # a release: j02_question-v2_<slug> (p2 older)
JOB = OJ.JOB                                                    # a Board Job: j03_question-v2-<slug>_data-v2
PROTO_NAME = re.compile(r"^((?:InsightQuestionBook|QuestionBook|Prototype)-[A-Za-z0-9][A-Za-z0-9.-]*|b\d+_.+)$")    # Prototype- (before 261109) and bNN_ stay readable
BOARD_NAME = re.compile(r"^(Insight-[A-Za-z0-9][A-Za-z0-9.-]*|b\d+_.+)$")
TASK = re.compile(r"^t(\d+)_([DIKWX]\d\d)_([a-z0-9-]+)$")     # a question Task: t03_K01_<slug>
PREP_BLOCK = re.compile(r"^InsightDataPrep-[A-Za-z0-9][A-Za-z0-9.-]*$")   # the DataPrep Block (ref/dataprep.md)
PREP = re.compile(r"^j(\d+)_(prep-v\d+)(?:_([a-z0-9][a-z0-9-]*))?$")      # a prep version: j02_prep-v2_<slug>
STEP = re.compile(r"^t(\d+)_([a-z0-9][a-z0-9-]*)$")                        # a prep step Task: t01_join
DATAJOB = re.compile(r"^j(\d+)_(prep-v\d+)(?:-([a-z0-9][a-z0-9-]*))?_(data-v\d+)$")   # withdrawn 261120: drop-datajob
JOB3 = re.compile(r"^j(\d+)_(data-v\d+)_(prep-v\d+)_(question-v\d+)$")   # a Board Job of three versions (JL 261120)
PREPTASK = re.compile(r"^t01_(prep-v\d+)(?:_([a-z0-9][a-z0-9-]*))?$")      # its first Task: the whole prep version, one Run
LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)   # the C loader when built (a Board has many faces)
LEVEL = {"X": "executive", "D": "data", "I": "information", "K": "knowledge", "W": "wisdom"}
KINDS = ("new question", "fix", "retire", "cut")
# a person reads and types "segment"; the files keep the machine words (a proposal's `kind: cut`, a Run's type partition)
WORDS = {"segment": "cut", "segments": "cut", "propose-segment": "propose-cut"}
RUN_WORDS = {"segment": "partition"}
# run types: (level, type) -> (skill, agent, signs, hard); ref/insight-ladder.md § Runs
TYPES = {
    ("prototype", "triage-proposals"): ("hai-insight-question", "hai-insight-agent", "none", False),
    ("prototype", "open-version"): ("hai-insight", "hai-insight-agent", "none", False),
    ("prototype", "map"): ("hai-insight", "hai-insight-agent", "none", False),
    ("prototype", "carry"): ("hai-insight", "hai-insight-agent", "a person", False),
    ("version", "ask"): ("hai-insight-question", "hai-insight-agent", "none", False),
    ("version", "review-questions"): ("hai-report", "hai-insight-reviewer-agent", "a person (a change)",
                                      False),
    ("version", "set-segments"): ("hai-insight", "hai-insight-agent", "a person (the segments)", False),
    ("version", "sign-release"): ("hai-insight", "hai-insight-agent", "a person", False),
    ("question", "plan-evidence"): ("hai-insight-evidence-plan", "hai-insight-agent", "none", False),
    ("question", "review-plan"): ("hai-insight-evidence-plan", "hai-insight-reviewer-agent", "none", False),
    ("question", "write-script"): ("hai-insight", "hai-task-creator-agent", "none", False),
    ("question", "review-script"): ("hai-insight", "hai-task-reviewer-agent", "none", False),
    ("board", "add-version"): ("hai-insight-meta", "hai-insight-agent", "none", False),
    ("board", "add"): ("hai-insight", "hai-insight-agent", "none", False),
    ("board", "propose-cut"): ("hai-insight-question", "hai-insight-agent", "none", False),
    ("board", "propose"): ("hai-insight-question", "hai-insight-agent", "none", False),
    ("board", "coverage"): ("hai-insight-check", "hai-insight-agent", "none", False),
    ("board", "track"): ("hai-insight-check", "hai-insight-agent", "none", False),
    ("board", "consistency"): ("hai-insight-knowledge", "hai-insight-reviewer-agent", "none", False),
    ("board", "ask"): ("hai-report", "hai-insight-agent", "another agent agrees", False),
    ("board", "report"): ("hai-report", "hai-insight-agent", "none", False),
    ("board", "check"): ("hai-report", "hai-draft-check-agent", "none", False),
    ("board", "map"): ("hai-insight", "hai-insight-agent", "none", False),
    ("board", "write"): ("hai-insight-wisdom", "hai-insight-agent", "none", False),
    ("board", "draft"): ("hai-insight-wisdom", "hai-insight-agent", "a person (the handoff)", False),
    ("board", "close"): ("hai-insight-check", "hai-insight-agent", "a person", False),
    ("job", "launch"): ("hai-insight", "hai-insight-agent", "none", False),
    ("job", "power"): ("hai-insight", "hai-insight-agent", "none", False),
    ("job", "compare"): ("hai-insight-knowledge", "hai-insight-agent", "none", False),
    ("job", "propose"): ("hai-insight-question", "hai-insight-agent", "none", False),
    ("job", "overall"): ("hai-insight", "hai-insight-agent", "none", False),   # the Overall Report
    ("job", "close"): ("hai-insight-check", "hai-insight-agent", "a person", False),
    # a Run's report beside its result/, written by one agent and checked by another (ref/run-report.md)
    ("job", "report"): ("hai-insight", "hai-insight-agent", "none", False),
    ("job", "check-report"): ("hai-insight-check", "hai-insight-reviewer-agent", "none", False),
    ("task", "report"): ("hai-insight", "hai-insight-agent", "none", False),
    ("task", "check-report"): ("hai-insight-check", "hai-insight-reviewer-agent", "none", False),
    ("preptask", "report"): ("hai-insight", "hai-insight-agent", "none", False),
    ("preptask", "check-report"): ("hai-insight-check", "hai-insight-reviewer-agent", "none", False),
    ("task", "partition"): ("hai-insight", "hai-task-orchestrator-agent", "none", True),
    ("task", "write"): ("hai-insight-<its level>", "hai-insight-agent", "none", False),
    ("task", "check"): ("hai-report", "hai-draft-check-agent", "none", False),
    ("task", "pool"): ("hai-insight-knowledge", "hai-insight-agent", "none", False),
    ("task", "check-alignment"): ("hai-insight-check", "hai-insight-reviewer-agent", "none", False),
    # the DataPrep Block (ref/dataprep.md): a prep version holds the tools, a step Task one tool, a hard Run one dataset
    ("dataprep", "open-version"): ("hai-insight", "hai-insight-agent", "none", False),
    ("prep", "review-steps"): ("hai-insight", "hai-insight-reviewer-agent", "none", False),   # it writes agreed:
    ("prep", "sign"): ("hai-insight", "hai-insight-agent", "a person", False),
    ("step", "write-script"): ("hai-task-for-data", "hai-task-creator-agent", "none", False),
    ("step", "review-script"): ("hai-task-for-data", "hai-task-reviewer-agent", "none", False),
    # a Board Job's head Task runs a signed prep version on the Board's raw export, its steps inside one hard Run
    ("preptask", "prep"): ("hai-insight", "hai-task-orchestrator-agent", "none", True)}
ALONE = {("board", "coverage")}                       # a Run whose target is the whole level: run-coverage
DEFAULT_TARGET = {("prototype", "map"): "questions", ("board", "map"): "questions", ("board", "write"): "counsel",
                  ("board", "draft"): "handoff", ("board", "propose"): "coverage"}
RUN_TYPES = {level: " · ".join(t for (lv, t) in TYPES if lv == level)
             for level in ("prototype", "version", "question", "board", "job", "task", "dataprep", "prep", "step",
                           "preptask")}


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

    def copy(self, src: Path, dst: Path, also: tuple = ()) -> None:
        if dst.exists():
            return
        self.made.append(dst)
        if not self.dry:
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("runs", "results", "reports", "__pycache__", *also))


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
               "is `rNN_<segment>/` (run.yaml · result/). See hai-insight ref/insight-ladder.md § Runs.\n")


def face(folder: Path) -> dict:
    return front(folder / f"{folder.name}.md")[0]


# ── the insight Board ───────────────────────────────────────────────────────────────────────────
def face_kind(block: Path) -> str:
    fm = front(block / "board.md")[0]
    if fm.get("board-kind") == "prototype":
        return "prototype"
    if fm.get("board-kind") == "insight-dataprep":
        return "dataprep"
    if fm.get("board-kind") == "insight-board" or fm.get("prototype"):
        return "board"
    return ""

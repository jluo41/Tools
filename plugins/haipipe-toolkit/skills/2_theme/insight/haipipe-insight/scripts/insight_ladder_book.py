"""insight_ladder's Question Book commands: the Book itself, a question version (release), a question Task, a change, a
retire, the signature a person states, and a proposal."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from insight_ladder_base import (
    QID, SLUG, VERSION, PROTO_NAME, TASK, LEVEL, KINDS, Plan, front, with_front, read_yaml, dump_yaml,
    runs_readme, face, face_kind)


# ── the Question Book Block ─────────────────────────────────────────────────────────────────────────
def versions(proto: Path) -> list[Path]:
    return sorted((p for p in proto.iterdir() if p.is_dir() and VERSION.match(p.name)),
                  key=lambda p: int(VERSION.match(p.name).group(1))) if proto.is_dir() else []


def release(version: Path) -> dict:
    return read_yaml(version / "release.yaml")


def prototype_goal(title: str) -> str:
    """A Question Book's goal line: its questions, in its title's words."""
    words = (title or "the questions and their scripts").strip()
    return f"{words[:1].upper()}{words[1:]}, one signed question version at a time"


def prototype(path: Path, serves: str, title: str, plan: Plan) -> None:
    if not PROTO_NAME.match(path.name):
        sys.exit(f"a Question Book is a special board, InsightQuestionBook-<name> (or the older bNN_<topic>): {path.name}")
    if path.parent.name not in ("insight", "insights", "tasks", "work"):    # tasks/ and work/: the older place
        sys.exit(f"a Question Book lives in <Project>/insight/, beside the Board it serves: {path}")
    plan.write(path / "board.md", with_front(
        {"board-kind": "prototype", "serves": serves, "goal": prototype_goal(title)},
        f"\n# {path.name} · {title or 'the Question Book'}\n\n"
        "The questions and their scripts, one Job per question version (`jNN_question-vN_<slug>/`), frozen once a person signs\n"
        "it. A Board's Job pins one question version and one data version; a question version is cut from proposals/.\n"))
    plan.write(path / "proposals" / "README.md", "# proposals\n\nThe backlog: new question · fix · retire · segment, one file "
               "each (`<slug>.md`: kind · level · from <job or report> · state · why). The next release is cut from here "
               "(run-triage-proposals).\n")
    runs_readme(path, "prototype", plan)


def version(proto: Path, slug: str, plan: Plan) -> Path:
    """The next question version: jNN_question-vN_<slug>/ with release.yaml; it starts from the newest one (every question kept).
    The slug says what it is; its id is question-vN everywhere it is named."""
    if slug and not SLUG.match(slug):
        sys.exit(f"--slug is a few lower-case words joined by -: {slug!r}")
    if face_kind(proto) != "prototype":
        sys.exit(f"{proto.name} is not a Question Book Block (board.md board-kind: prototype)")
    old = versions(proto)
    if old and str(face(old[-1]).get("state")) != "closed":
        sys.exit(f"{old[-1].name} is still open: sign it (or work in it) before opening the next version")
    n = int(VERSION.match(old[-1].name).group(1)) + 1 if old else 1
    rel = f"question-v{n}"
    path = proto / (f"j{n:02d}_{rel}_{slug}" if slug else f"j{n:02d}_{rel}")
    prev = old[-1] if old else None
    kept = len(release(prev).get("questions") or {}) if prev else 0
    cuts = len(front(prev / "partitions.md")[0].get("partitions") or []) if prev else 0
    plan.write(path / f"{path.name}.md", with_front(
        {"release": rel, "state": "open", "signed": "", "from": VERSION.match(prev.name).group(2) if prev else "",
         "goal": release_goal(n, slug.replace("-", " "), kept, cuts)},
        f"\n# question-v{n}\n\n<what this question version changes, and which proposals it takes>\n"))
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
            "\n# The segments\n\nPart of the plan, fixed before any outcome (run-set-segments; a person signs them).\n"))
        plan.write(path / "thresholds.yaml", dump_yaml(
            {"power": {"smallest_effect_pp": "<pp>", "alpha": 0.05, "target_power": 0.8}}))
    plan.write(path / "release.yaml", dump_yaml({"release": rel, "questions": rows}))
    runs_readme(path, "version", plan)
    return path


def release_goal(n: int, words: str, questions: int, cuts) -> str:
    """A release's goal line: what it is for, in words, no count (b11 round 2: "take the counts out of the goal line";
    how many questions and segments is its page's main line): `question-v1, example questions: the questions and their scripts
    on the segments it fixes`; a release still without questions says what it will hold."""
    head = f"question-v{n}" + (f", {words}" if words else "")
    if not questions:
        return f"{head}: its questions and their scripts, frozen once a person signs it"
    return f"{head}: the questions and their scripts" + (" on the segments it fixes" if cuts else "")


def _rel(target: Path, base: Path) -> str:
    """target relative to base, as written in release.yaml (a Task here is just its name)."""
    import os
    return Path(os.path.relpath(target, base.resolve())).as_posix()


def _version_open(ver: Path) -> None:
    if not VERSION.match(ver.name) or face_kind(ver.parent) != "prototype":
        sys.exit(f"{ver.name} is not a Question Book version (insight/InsightQuestionBook-<name>/jNN_question-vN_<slug>/)")
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
        sys.exit(f"{ver.name}/partitions.md: set the segments first (run-set-segments): `full` and every segment named")
    fields, body = front(ver / f"{ver.name}.md")
    fields.update(state="closed", signed=f"✅ {date}")
    plan.write(ver / f"{ver.name}.md", with_front(fields, body), replace=True)


def propose(proto: Path, slug: str, kind: str, source: str, level: str, why: str, plan: Plan) -> Path:
    """A proposal into the Question Book's proposals/: the only way a question or a segment reaches a new version."""
    if face_kind(proto) != "prototype":
        sys.exit(f"{proto.name} is not a Question Book Block (board.md board-kind: prototype)")
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

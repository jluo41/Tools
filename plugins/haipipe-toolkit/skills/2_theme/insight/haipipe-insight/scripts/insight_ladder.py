#!/usr/bin/env python3
"""insight_ladder.py · make the insight ladder's folders (ref/insight-ladder.md): the Question Book Block and its
versions and questions, the insight Board and its data versions, its Jobs and their Tasks, and a Run.

    python insight_ladder.py prototype <Project>/insight/InsightQuestionBook-<name> --serves insight/Insight-<name> [--title "…"]
    python insight_ladder.py version   <prototype> --slug <what-it-is>  the next question version jNN_question-vN_<slug>/ (from the newest)
    python insight_ladder.py question  <version> <L><NN> <slug>        a new question Task tNN_<L><NN>_<slug>/
    python insight_ladder.py change    <version> <L><NN> --why "…"     carry a kept question into this version to change it
    python insight_ladder.py retire    <version> <L><NN> --why "…"     drop a question from this version (kept as history)
    python insight_ladder.py sign      <version> --date YYMMDD         record the signature a person states; freezes it
    python insight_ladder.py propose   <prototype> <slug> --kind "new question|fix|retire|segment" --from <jNN or qNN>
                                                                        [--level data|information|knowledge|wisdom] [--why "…"]
    python insight_ladder.py board     <Project>/insight/Insight-<name> --dataset <D> --prototype insight/InsightQuestionBook-<name>
                                                                        [--title "…"] [--accumulates yes|no|?]
    python insight_ladder.py data      <board> data-v<M> --data-folder <SPACE-relative data folder>/ [--label "first 5 days"] [--new "…"]
                                       (or --extract <SPACE-relative .parquet> [--rows <n>], a lone file)
    python insight_ladder.py job       <board> --release question-v<N> --data data-v<M>   the next Job jNN_question-vN-<slug>_data-vM/
    python insight_ladder.py run       <folder> <type> [<target>]          a soft Run runs/run-<type>-<target>/
    python insight_ladder.py run       <Board Task> segment <name|all>   a hard Run runs/rNN_<segment>/ (planned)
    python insight_ladder.py goals     <Board, Question Book, Job or Task>     write each face's missing `goal:` line
    python insight_ladder.py audit     <Board, Question Book or Project>       what an older folder lacks, and the step that fixes it
    python insight_ladder.py review    <Board or Question Book>                read-only: answers to reread or check, refused Runs,
                                       and what the Question Book leaves unsaid (scripts/insight_ladder_review.py)
    python insight_ladder.py update    <Board, Question Book or Project> [--apply]   the names, the goal lines, each Job's hash
                                       (a dry run without --apply; an older layout is named, carried by its own script)
    (add --dry-run to any command: print what it would make; change nothing)

Every page it makes carries a `goal:` line, the one line a page's header shows under its view buttons (261106): a
Board the dataset's purpose, a Question Book its questions, a release what it holds, a question Task (its face
tNN_<L><NN>_<slug>.md beside question.md) and a Board Task the question's ask, a Board Job what its release × data
version answers. `goals` backfills a face written before that line, from the same source; it writes only a missing line.

Two special boards (b11 s00, plan C; named by their kind), side by side in insight/.
The Question Book, `insight/InsightQuestionBook-<name>/`, holds the questions and their scripts; each of its Jobs is one question version
(a release), j0N_question-vN_<slug>/, frozen once a person signs it. The insight Board, `insight/Insight-<name>/`, holds one
dataset and its dated data versions; each of its Jobs pins one question version and one data version,
jNN_question-vN-<slug>_data-vM/, and moves one clock from the Job before it (`moved: start |
data | code`). `job` checks the gates (the release is signed, the data version is in board.md, the pair is new, only
one clock moved), then writes the Job through ref/open_job.py: its face, a Task per question, a ticket per asked segment.
A hard Run's ticket runs ref/run_job.py. A reader knows each Block by its board.md, never its folder name; the older
bNN_ names stay readable. Every command writes only what is missing (it never overwrites a file, except the YAML it
extends: release.yaml, board.md's versions) and prints what it made. Placeholders only: a person or an agent fills
them through the insight skills. Nothing is committed.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))   # its parts sit beside it (loaded by path, too)
from insight_ladder_base import (  # noqa: E402,F401 · this module keeps answering these names
    HERE, _spec, SOFT, QID, SLUG, VERSION, JOB, PROTO_NAME, BOARD_NAME, TASK, LOADER, LEVEL, KINDS, WORDS,
    RUN_WORDS, TYPES, ALONE, DEFAULT_TARGET, RUN_TYPES, Plan, front, with_front, read_yaml, dump_yaml, today,
    project_of, runs_readme, face, face_kind)
from insight_ladder_book import (  # noqa: E402,F401 · this module keeps answering these names
    versions, release, prototype_goal, prototype, version, release_goal, _rel, _version_open, _task_number,
    question_face, question, change, retire, sign, propose)
from insight_ladder_runs import (  # noqa: E402,F401 · this module keeps answering these names
    level_of, _default_target, _partitions, hard_run, run)
import open_job as OJ  # noqa: E402  (ref/, put on the path by insight_ladder_base)


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
        sys.exit(f"--prototype {proto}: no Question Book Block there yet (insight_ladder.py prototype)")
    plan.write(path / "board.md", with_front(
        {"board-kind": "insight-board", "workbench": "insight", "dataset": dataset, "prototype": proto,
         "accumulates": accumulates, "goal": board_goal(title, dataset), "versions": []},
        f"\n# {title or path.name}\n\nOne dataset, its data versions, and one Job per pair (question version × data "
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
        sys.exit("--data-folder and --extract are SPACE-relative (or through a variable), never absolute (the SPACE's AGENTS.md § Working rules)")
    fields, body = front(path / "board.md")
    have = [str(v.get("version")) for v in fields.get("versions") or []]
    if ver in have:
        sys.exit(f"{ver} is already a data version of {path.name}; a new extract is the next version")
    want = f"data-v{len(have) + 1}"
    if ver != want:
        sys.exit(f"the next data version is {want}")
    # a folder: the data file, its manifest, dictionary, summary, figures and docs; the workbench
    # reads them all, the Runs find the data file in it (run_job.version_extract)
    entry = ({"version": ver, "folder": folder.rstrip("/") + "/", "frozen": today()} if folder else
             {"version": ver, "extract": extract, "frozen": today(), "rows": rows or "<n>"})
    if label:                                  # the data version's few words, shown as data-v<M> · <label>
        entry = {"version": ver, "label": label, **{k: v for k, v in entry.items() if k != "version"}}
    fields.setdefault("versions", []).append(dict(entry, new=new or "<what is new>"))
    plan.write(path / "board.md", with_front(fields, body), replace=True)


def jobs(block: Path) -> list[Path]:
    return sorted((p for p in block.iterdir() if p.is_dir() and JOB.match(p.name)),
                  key=lambda p: int(JOB.match(p.name).group(1)))


def release_hash(ver: Path) -> str:
    """The first 12 hex of a sha256 over the release: release.yaml, the segments, the thresholds, every question's files."""
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
    """The next Job: one question version × one data version, its Tasks one per question of the question version."""
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
    """Each face's missing goal line under `folder` (a Board, a Question Book, a release, a Job, a Task), from the same
    source its generator reads: a Board's title, a Question Book's title, a release's questions and segments, a Job's release
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


# ── audit and update: bring an older insight folder onto the current contract ──────────────────────────
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
    """The insight Boards a folder names: a Board itself, the Board a Question Book serves, or each Board of a Project."""
    folder = folder.resolve()
    kind = face_kind(folder) if (folder / "board.md").is_file() else ""
    if kind == "board":
        return [folder]
    if kind == "prototype":
        b = project_of(folder) / str(front(folder / "board.md")[0].get("serves", ""))
        return [b] if face_kind(b) == "board" else []
    return sorted(b for d in ("insight", "insights") for b in (folder / d).glob("*/") if face_kind(b) == "board")


def older_layout(folder: Path) -> str:
    """The step for a folder made before the Question Book and the Board (it is carried, not renamed), else ''."""
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
    """What each Board (and its Question Book) still lacks against ref/insight-ladder.md, one row per check:
    (Board, check, count, the step that fixes it). Read-only."""
    import rename_code_data as RN
    import rename_segment as RS
    rows = []
    for b in boards_of(folder) or [folder.resolve()]:
        step = older_layout(b)
        if step:
            rows.append((b, "layout", 1, step))
            continue
        edits, renames, move = RN.plan(b, [])
        rows.append((b, "names", len(edits) + len(renames) + bool(move),
                     "update --apply (ref/rename_code_data.py: question-vN, data-vM, the Question Book in insight/)"))
        w_edits, w_renames = RS.plan(b)
        rows.append((b, "words", len(w_edits) + len(w_renames),
                     "update --apply (ref/rename_segment.py: a person reads \"segment\")"))
        gp = Plan(True)
        goals(b, gp) if not (edits or renames or move) else None
        rows.append((b, "goals", len(gp.made), "update --apply (insight_ladder.py goals)"))
        pins = [j for j in jobs(b) if not (edits or renames or move)
                and _release_of(j).is_dir() and str(face(j).get("hash", "")) != release_hash(_release_of(j))]
        rows.append((b, "hash", len(pins), "update --apply (each Job's hash: re-pinned to its release)"))
        st = stale_receipts(b) if not (edits or renames or move) else []
        rows.append((b, "receipts", len(st), "update --apply --rerun (each ticket's run.sh; needs env.sh at the SPACE root)"))
    if not quiet:
        for b, check, n, step in rows:
            print(f"{'✅' if n == 0 else '❗'} {b.name:<28} {check:<9} {n:>4}" + ("" if n == 0 else f"   ▶ {step}"))
        if any(r[1] == "names" and r[2] for r in rows):
            print("(goals, hash and receipts are checked after the names are current)")
    return rows


def rerun(runs: list[Path]) -> tuple[int, int, int]:
    """Run each stale Run's own ticket again (bash <Run>/run.sh) and say whether its tables came out the same:
    (same, changed, failed). A rename changes a question's text, never its numbers, so `changed` is worth reading."""
    import subprocess
    same = changed = failed = 0
    for i, r in enumerate(runs, 1):
        rt = r / "result" / "runtime.yaml"
        before = read_yaml(rt).get("tables_sha256")
        done = subprocess.run(["bash", str(r / "run.sh")], capture_output=True, text=True)
        after = read_yaml(rt) if rt.is_file() else {}
        if done.returncode != 0 or after.get("status") == "failed":
            failed += 1
            why = (after.get("problem") or done.stderr.strip().splitlines()[-1:] or ["no receipt"])
            print(f"  ❗ {i}/{len(runs)} {r.parent.parent.name}/{r.name}: failed · {why if isinstance(why, str) else why[0]}")
        elif after.get("tables_sha256") != before:
            changed += 1
            print(f"  🔶 {i}/{len(runs)} {r.parent.parent.name}/{r.name}: rerun, its tables changed")
        else:
            same += 1
    return same, changed, failed


def update(folder: Path, apply: bool, again: bool = False) -> list[tuple]:
    """Bring each Board and its Question Book onto the current contract, in order: the names (question-vN × data-vM, the
    Question Book beside its Board), the words (a person reads "segment"), the missing goal lines, each Job's hash
    re-pinned to its release, and with `again` each stale receipt rerun by its ticket. A dry run unless `apply`; an
    older layout is only named (it is carried, by its own script); without `again` stale receipts are listed."""
    import rename_code_data as RN
    import rename_segment as RS
    for b in boards_of(folder) or [folder.resolve()]:
        step = older_layout(b)
        if step:
            print(f"❗ {b.name}: {step}; update does not carry it")
            continue
        edits, renames, move = RN.plan(b, [])
        print(f"{b.name} · names: {len(edits)} files rewritten · {len(renames)} names · "
              f"{'1 Question Book moved' if move else 'Question Book stays'}")
        w_edits, w_renames = RS.plan(b)
        if not apply:
            print(f"{b.name} · words: {len(w_edits)} files rewritten · {len(w_renames)} names")
        if (edits or renames or move) and not apply:
            print("  dry run: rerun with --apply; goals, hash and receipts are planned once the names are current")
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
            w_edits, w_renames = RS.plan(b)                       # after the names: the Question Book may have moved
            RS.apply(w_edits, w_renames)
            print(f"{b.name} · words: {len(w_edits)} files rewritten · {len(w_renames)} names")
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
        if apply and again and st:
            same, changed, failed = rerun(st)
            print(f"{b.name} · rerun: {same} with the same tables · {changed} changed · {failed} failed")
        else:
            for r in st:
                print(f"  bash {r / 'run.sh'}")
    return audit(folder, quiet=not apply) if apply else []


def main(argv=None) -> list[Path]:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=("prototype", "version", "question", "change", "retire", "sign", "propose",
                                        "board", "data", "job", "run", "goals", "audit", "review", "update"))
    ap.add_argument("folder", type=Path)
    ap.add_argument("what", nargs="?", default="", help="question/change/retire: <L><NN>; propose: <slug>; "
                                                        "data: v<M>; run: its type")
    ap.add_argument("extra", nargs="?", default="", help="question: <slug>; run: its target (or a segment)")
    ap.add_argument("--serves", default="")
    ap.add_argument("--slug", default="", help="version: what the question version is, jNN_question-vN_<slug>")
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
    ap.add_argument("--rerun", action="store_true", help="update --apply: run each stale receipt's ticket again")
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
        propose(a.folder, a.what, WORDS.get(a.kind, a.kind), a.source, a.level, a.why, plan)
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
    elif c == "review":
        from insight_ladder_review import review
        review(a.folder)
        return []
    elif c == "update":
        update(a.folder, a.apply, a.rerun)
        return []
    else:
        if not a.what:
            ap.error("run needs a type, e.g. add, compare, segment")
        run(a.folder, RUN_WORDS.get(a.what, WORDS.get(a.what, a.what)), a.extra, plan)
    for p in plan.made:
        print(("would make " if a.dry_run else "made ") + str(p))
    return plan.made


if __name__ == "__main__":
    main()

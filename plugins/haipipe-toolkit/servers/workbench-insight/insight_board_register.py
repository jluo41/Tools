"""The one write an insight Board page makes: register a question on its level's register page, and the
`python3 -m live.insightboard ask` command line that does the same."""

from __future__ import annotations

import re
import uuid
from datetime import date, datetime
from pathlib import Path

from .insight_board_reader import _CACHE, _LEVEL_LABEL, _LEVEL_OF, _MARK, _QID, _pages, _read


def _main(argv: list[str]) -> int:
    """`python3 -m live.insightboard ask <board> <D|I|K|W> <F,B,C> "<question>" [--origin X] [--parent Y]`

    The write half of the skill's `question` verb: Claude Code decides the
    arguments, this writes the row and prints the cell to open next.
    """
    import argparse
    ap = argparse.ArgumentParser(prog="insightboard")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ask = sub.add_parser("ask", help="register one question on its register")
    ask.add_argument("board")
    ask.add_argument("level", help="D, I, K or W")
    ask.add_argument("partitions", help="comma-separated segment names, e.g. full or full,youngmale,youngfemale")
    ask.add_argument("question")
    ask.add_argument("--origin", default="", help="curiosity-driven or need-driven")
    ask.add_argument("--parent", default="", help="what it grew out of, e.g. 'I08-full · I3' or 'QI9'")
    ask.add_argument("--workflow-runtime-id", default="", help="existing Runtime declaring this exact registration")
    ask.add_argument("--actor", default="board-ask", help="registration actor recorded in the control receipt")
    args = ap.parse_args(argv)
    board = Path(args.board).resolve()
    if not (board / "board.md").is_file():
        print(f"not a Board: {board}")
        return 2
    try:
        qid, pids = register_question(board, args.level, args.question, args.partitions,
                                      args.origin, args.parent,
                                      workflow_runtime_id=args.workflow_runtime_id, actor=args.actor)
    except ValueError as exc:
        print(f"refused: {exc}")
        return 1
    print(f"registered {qid} on {', '.join(pids)} · next: /hai-insight application {board.name} chain {qid} {pids[0]}")
    return 0



# ─── the one write: register a question ─────────────────────────────────────

def register_question(board_root: Path, level: str, question: str, partitions,
                      origin: str = "", parent: str = "", *,
                      workflow_runtime_id: str = "", actor: str = "board-ask") -> tuple[str, list[str]]:
    """Serialize shared register writes; a concurrent or interrupted writer holds."""
    lock = Path(board_root) / ".insight-registration.lock"
    try:
        lock.mkdir()
    except FileExistsError as exc:
        raise ValueError("registration is locked; finish or recover the existing writer first") from exc
    try:
        return _register_question(board_root, level, question, partitions, origin, parent,
                                  workflow_runtime_id=workflow_runtime_id, actor=actor)
    finally:
        lock.rmdir()


def _register_question(board_root: Path, level: str, question: str, partitions,
                       origin: str = "", parent: str = "", *,
                       workflow_runtime_id: str = "", actor: str = "board-ask") -> tuple[str, list[str]]:
    """Register a question and index its canonical control receipt; no Run.

    Called by the skill (`python3 -m live.insightboard ask ...`) after Claude
    Code has decided the level, the segments and the lineage.  The register
    grid remains the question authority. Its Outline log owns the receipt;
    the aggregate Runtime indexes that control. Transposed grids need an
    explicit owner edit.
    """
    level = (level or "").strip().upper()
    question = " ".join((question or "").split())
    if isinstance(partitions, str):
        partitions = re.split(r"[,\s]+", partitions)
    partitions = list(dict.fromkeys(p.strip().lower() for p in partitions if p and p.strip()))
    if level not in _LEVEL_OF:
        raise ValueError("kind of answer must be D, I, K or W")
    if not question:
        raise ValueError("the question is empty")
    if not partitions:
        raise ValueError("choose at least one partition")
    if any(not re.fullmatch(r"[a-z]+", p) for p in partitions):
        raise ValueError("partitions are named by their full name, e.g. full, youngmale, cross")
    pages = _pages(Path(board_root))
    candidates = [p for p in pages if p["register_level"] == _LEVEL_OF[level]
                  or p["id"] == f"MT0{'DIKW'.index(level) + 1}"]
    for page in candidates:
        if page["identity_error"]:
            raise ValueError(page["identity_error"])
        if page["page_type"] != "question":
            raise ValueError(f"{page['path']}: selected register is not a Question Folder")
    if len(candidates) > 1:
        raise ValueError("multiple Question registers face the requested DIKW level")
    register = candidates[0] if candidates else None
    if register is None:
        raise ValueError(f"no register page faces the {_LEVEL_LABEL[level]} level")
    qid, updated = _prepare_question_row(register["path"], level, question, partitions)
    import yaml
    board_root = Path(board_root).resolve()
    path = register["path"].resolve()
    runtime_id = workflow_runtime_id or f"registration-{uuid.uuid4().hex}"
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]*", runtime_id):
        raise ValueError("invalid workflow_runtime_id")
    runtime_dir = board_root / "_runs/insight" / runtime_id
    runtime_path = runtime_dir / "runtime.yaml"
    request = {"action": "register-question", "level": level,
               "question": question, "partitions": partitions}
    if workflow_runtime_id:
        try:
            runtime = yaml.safe_load(runtime_path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            raise ValueError(f"registration Runtime cannot be read: {exc}") from exc
        if not isinstance(runtime, dict) or runtime.get("workflow_id") != "hai-insight-workflow" \
                or runtime.get("workflow_runtime_id") != runtime_id \
                or runtime.get("status") not in {"planned", "running", "held"} \
                or request not in runtime.get("requested_controls", []):
            raise ValueError("Runtime must declare this exact registration control and remain open")
        if not isinstance(runtime.get("resource_controls", []), list):
            raise ValueError("Runtime resource_controls must be a list")
    else:
        definition = {"schema": "haipipe.insight-definition/v1", "workflow_id": "hai-insight-workflow",
                      "revision": "v001", "run_specs": [], "requested_answer_targets": [],
                      "requested_controls": [request],
                      "completion": {"required_controls": "neutral-row-open-cells-and-registration-receipt",
                                     "required_runs": "none", "frontier": "empty"}}
        definition_text = yaml.safe_dump(definition, sort_keys=False, allow_unicode=True)
        runtime = {"schema": "haipipe.workflow-runtime/v1", "workflow_id": "hai-insight-workflow",
                   "workflow_version": "1.3.1", "workflow_runtime_id": runtime_id,
                   "definition_ref": "definition-v001.yaml",
                   "status": "planned", "requested_answer_targets": [], "requested_controls": [request],
                   "runs": [], "control": {"gates": [], "routes": []},
                   "resource_controls": [], "frontier": [], "output": {"acceptance": "pending"}}
    record_id = f"registration-{qid.lower()}-{uuid.uuid4().hex[:12]}"
    from src.outline_version import plan_dir, record_path
    log = record_path(plan_dir(path.parent), path.stem, "log")
    receipt = f"{log.relative_to(board_root).as_posix()}#{record_id}"
    control = {"key": "registration", "target": {"question": qid, "partitions": partitions},
               "status": "passed", "authority": "hai-insight-question", "actor": actor,
               "evidence": [{"path": path.relative_to(board_root).as_posix()}], "receipt": receipt}
    stamp = datetime.now().astimezone().isoformat(timespec="seconds")
    record = {"workflow_runtime_id": runtime_id, "at": stamp, **control,
              "assertion": "neutral question row and requested open cells registered",
              "outcome": "registered", "origin": origin or "not stated", "parent": parent or "none",
              "next_action": "define any missing answerability facts before GI1; answering remains separate"}
    entry = (f"### {record_id}\n\n{date.today():%y%m%d} · Registered `{qid}` on {', '.join(partitions)} "
             f"from the Insight Board · origin: {origin or 'not stated'} · born from: {parent or 'new'}\n\n"
             f"```yaml\n{yaml.safe_dump(record, sort_keys=False, allow_unicode=True)}```\n")
    # Prepare and validate every input before the first write. A newly-created
    # planned Runtime makes an interrupted registration visible for recovery.
    if not workflow_runtime_id:
        runtime_dir.mkdir(parents=True, exist_ok=False)
        (runtime_dir / "definition-v001.yaml").write_text(definition_text, encoding="utf-8")
        runtime_path.write_text(yaml.safe_dump(runtime, sort_keys=False), encoding="utf-8")
    path.write_text(updated, encoding="utf-8")
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(_read(log).rstrip("\n") + "\n\n" + entry, encoding="utf-8")
    runtime.setdefault("resource_controls", []).append(control)
    if not workflow_runtime_id:
        runtime.update(status="complete", output={"path": path.relative_to(board_root).as_posix(),
                                                  "acceptance": "passed", "receipt": receipt})
    runtime_path.write_text(yaml.safe_dump(runtime, sort_keys=False, allow_unicode=True), encoding="utf-8")
    _CACHE.pop(str(board_root), None)
    return qid, partitions


def _prepare_question_row(path: Path, level: str, question: str, partitions) -> tuple[str, str]:
    if isinstance(partitions, str):
        partitions = [partitions]
    import textwrap

    text = _read(path)
    fence = re.compile(r"(?ms)^```\w*\n(.*?)^```")
    block = next((m for m in fence.finditer(text)
                  if re.search(r"(?m)^id\s+.*\bquestion\b", m.group(1))), None)
    if block is None:
        raise ValueError(f"{path.name} has no question grid")
    lines = block.group(1).splitlines()
    header = next((l for l in lines if re.match(r"^id\s", l)), "")
    if "partition" in header and _QID.search(header):
        raise ValueError(f"{path.name} keeps a transposed grid; add the row by hand")
    gen_at = header.find("Gen-1")
    cols = [(m.group(0), m.start()) for m in re.finditer(r"(?<!\S)[a-z]+(?!\S)", header)
            if m.start() > gen_at and m.group(0) != "cell"]
    missing = [p for p in partitions if p not in {pid for pid, _ in cols}]
    if missing:
        raise ValueError(f"{path.name} has no {', '.join(missing)} column; add it by hand first")
    q_off = header.find("question")
    gen_off = header.find("Gen-1")
    if q_off < 0 or gen_off < 0 or not cols:
        raise ValueError(f"{path.name}: grid header not understood")
    numbers = [int(m) for m in re.findall(rf"(?m)^Q{level}(\d+)\s", block.group(1))]
    qid = f"Q{level}{max(numbers, default=0) + 1}"
    width = max(12, gen_off - q_off - 2)
    chunks = textwrap.wrap(question, width, break_on_hyphens=False) or [question]
    first = qid.ljust(q_off) + chunks[0]
    first = first.ljust(gen_off) + "(none)"
    for i, (pid, start) in enumerate(cols):
        first = first.ljust(start) + ("⬜ open" if pid in partitions else "·")
    new_lines = [first] + [" " * q_off + c for c in chunks[1:]]
    last = max((i for i, l in enumerate(lines) if re.match(r"^Q[DIKW]\d+\s", l)),
               default=lines.index(header))
    while last + 1 < len(lines) and re.match(r"^\s{4,}\S", lines[last + 1]) and not _MARK.search(lines[last + 1]):
        last += 1  # keep a wrapped question with its row
    lines[last + 1:last + 1] = new_lines
    body = "\n".join(lines) + "\n"
    text = text[:block.start(1)] + body + text[block.end(1):]
    return qid, text

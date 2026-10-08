#!/usr/bin/env python3
"""Add a Block Question with an empty report Page, a report Page for a Question already
registered, or a related resource.

This authors a register and Page frame, never an answer, accepted Content or Run. A frame may
list Evidence links (files inside the Block, e.g. a Task Result or a studio/ drawing); they are
pointers for the writer, not an answer.
"""
from pathlib import Path
import argparse
import json
import os
import re
import sys
import tempfile
from urllib.parse import quote, urlsplit

# The register grammar lives with the work theme's server; find it by file, not by folder name,
# so a server rename (workbench-task -> workbench-work, 261007) breaks nothing.
_SERVERS = next(p for p in Path(__file__).resolve().parents if p.name == "skills").parent / "servers"
sys.path.insert(0, str(next((f.parent for f in sorted(_SERVERS.glob("*/task_questions.py"))), _SERVERS / "workbench-work")))
from task_questions import QUESTION_ID, inside, register, replace_register  # noqa: E402


def frame(qid, title, question, evidence, aim=""):
    """The report Page frame: header lines, an empty Opening, and Content with only the
    Evidence links it was given (the Workbench shows a linked .excalidraw in the Report column)."""
    links = "".join(f"- [{label}]({target})\n" for label, target in evidence)
    return (f"# {title}\nstate: 🔴 OPEN\n"
            f"answers: {qid}\nanswer-status: open\n\n## Opening\n\n"
            "No answer has been recorded yet.\n\n"
            f"**Where this Page sits:** [{qid} · {question}](../../board.md).\n\n"
            f"**Why it matters:** {aim or 'The report will connect the question to its supporting evidence.'}\n\n"
            "## Content\n" + (f"\n### Evidence\n\n{links}" if links else ""))


BLANK = {"type": "excalidraw", "version": 2, "source": "haipipe-question", "elements": [],
         "appState": {"viewBackgroundColor": "#ffffff"}, "files": {}}


def drawing_files(folder, names):
    """`--drawing <name>`: reports/<id>_topic/studio/<name>.excalidraw, the report's own drawing
    (a drawing that belongs to one report lives in its folder; the Block's studio/ keeps only the
    drawings several Questions or Jobs share). Returns label|path evidence items, Block-relative."""
    if len(names) > 1:
        raise ValueError("One Question has one drawing (JL 261005): pass --drawing once and draw further "
                         "views as frames inside it")
    out = []
    for name in names:
        if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,79}", name):
            raise ValueError("Drawing name must use lowercase letters, digits, - and _")
        out.append((name, folder / "studio" / f"{name}.excalidraw"))
    return out


def evidence_links(board, folder, raw):
    """`label|path` with path relative to the Block -> (label, path relative to the report)."""
    out = []
    for item in raw:
        label, sep, target = item.partition("|")
        rel = Path(target.strip())
        if (not sep or not label.strip() or "\n" in item or rel.is_absolute()
                or not inside(board / rel, board) or not (board / rel).is_file()):
            raise ValueError(f"Evidence must be 'label|path' naming a file inside the Block: {item}")
        out.append((label.strip(), quote(Path(os.path.relpath(board / rel, folder)).as_posix())))
    return out


def update(args):
    board = args.block.resolve()
    head = board / "board.md"
    if not inside(head, board):
        raise ValueError("board.md must stay inside the Block")
    original = head.read_text(encoding="utf-8")
    kind = re.search(r"(?m)^board-kind: (task-block|cowork-block|discovery-block)\s*$", original)
    if not kind:
        raise ValueError("Expected board-kind: task-block, cowork-block or discovery-block")
    cowork = kind.group(1) == "cowork-block"
    questions, errors = register(original, "Questions", "questions")
    if errors:
        raise ValueError("; ".join(errors))
    new_page = None
    if args.command == "add-report":
        entry = next((q for q in questions if q.get("id") == args.id), None)
        if entry is None:
            raise ValueError("No Question has this id in the register; use add-question")
        if entry.get("report"):
            raise ValueError("This Question already names a report; open it in place")
        if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", args.slug):
            raise ValueError("Slug must use lowercase words separated by underscores")
        title = (args.title or entry.get("title") or entry.get("question") or "").strip()
        if not title or "\n" in title:
            raise ValueError("Title must be nonempty single-line text")
        stem = args.id.lower() + "_" + args.slug
        folder = board / "reports" / stem
        if not inside(folder, board) or folder.exists():
            raise ValueError("Report folder already exists or escapes the Block")
        new_page = folder / (stem + ".md")
        entry["report"] = new_page.relative_to(board).as_posix()
        updated = replace_register(original, "Questions", "questions", questions)
        page_title = title
        drawings = drawing_files(folder, args.drawing)
        evidence_links(board, folder, args.evidence)  # check given evidence before anything is written
        page_text = None                              # framed below, once the drawings exist
    elif args.command == "add-question":
        if not QUESTION_ID.fullmatch(args.id) or any(q.get("id") == args.id for q in questions):
            raise ValueError("Question id must be new: Q and two or more digits (Q01), or Q-<word>-<number> (Q-food-1)")
        if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", args.slug):
            raise ValueError("Slug must use lowercase words separated by underscores")
        if not args.question.strip() or "\n" in args.question or "\n" in (args.title or ""):
            raise ValueError("Question and title must be nonempty single-line text")
        for raw in args.work:
            rel = Path(raw)
            if cowork:
                # A CoWork Block's work is one of its own files: a ticket page, a design note.
                if rel.is_absolute() or not inside(board / rel, board) or not (board / rel).is_file():
                    raise ValueError(f"Work must name an existing file inside the CoWork Block: {raw}")
                continue
            if (rel.is_absolute() or len(rel.parts) != 2 or not re.fullmatch(r"j\d{2}_[\w]+", rel.parts[0])
                    or not re.fullmatch(r"t\d{2}_[\w]+", rel.parts[1])
                    or not inside(board / rel, board)
                    or not (board / rel / (rel.name + ".md")).is_file()):
                raise ValueError(f"Work must name an existing jNN_job/tNN_task: {raw}")
        stem = args.id.lower() + "_" + args.slug
        folder = board / "reports" / stem
        if not inside(folder, board) or folder.exists():
            raise ValueError("Report folder already exists or escapes the Block")
        new_page = folder / (stem + ".md")
        entry = dict(id=args.id, title=args.title or args.question, question=args.question,
                     hypothesis=args.hypothesis or "", acceptance=args.acceptance or "",
                     work=args.work, report=new_page.relative_to(board).as_posix())
        questions.append(entry)
        updated = replace_register(original, "Questions", "questions", questions)
        page_title = args.title or args.question
        drawings = drawing_files(folder, args.drawing)
        evidence_links(board, folder, args.evidence)  # check given evidence before anything is written
        page_text = None                              # framed below, once the drawings exist
    else:
        split = urlsplit(args.url)
        if split.scheme not in {"http", "https"} or not split.netloc or not args.title.strip():
            raise ValueError("A resource needs a title and http(s) source URL")
        ids = {q.get("id") for q in questions}
        if any(q not in ids for q in args.question):
            raise ValueError("Resource Question ids must be registered in this Block")
        rows, errors = register(original, "Related resources", "resources")
        if errors:
            raise ValueError("; ".join(errors))
        if any(row.get("url") == args.url for row in rows):
            raise ValueError("This resource URL is already registered; edit its existing entry")
        rows.append(dict(title=args.title, url=args.url, questions=args.question,
                         contribution=args.contribution or "", notes=args.notes or ""))
        updated = replace_register(original, "Related resources", "resources", rows)
    # Avoid replacing an edit made while preparing this request.
    if head.read_text(encoding="utf-8") != original:
        raise ValueError("board.md changed; reread it before retrying")
    if new_page:
        new_page.parent.mkdir(parents=True, exist_ok=False)
        for _, path in drawings:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(BLANK, indent=1), encoding="utf-8")
        evidence = list(args.evidence) + [f"{label.replace('_', ' ').capitalize()}|{path.relative_to(board).as_posix()}"
                                          for label, path in drawings]
        entry = next(q for q in questions if q.get("id") == args.id)
        title = page_title if args.command == "add-report" else (args.title or args.slug.replace('_', ' '))
        page_text = frame(args.id, title, entry.get("question", title), evidence_links(board, new_page.parent, evidence),
                          entry.get("aim", ""))
        new_page.write_text(page_text, encoding="utf-8")
        (new_page.parent / "page.toml").write_text(
            'version = 1\nsource = ' + json.dumps(new_page.name) + '\ntitle = '
            + json.dumps(page_title, ensure_ascii=False) + '\n', encoding="utf-8")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=board,
                                         prefix=".board-questions-", delete=False) as output:
            temporary = Path(output.name)
            output.write(updated)
        temporary.chmod(head.stat().st_mode & 0o777)
        if head.read_text(encoding="utf-8") != original:
            raise ValueError("board.md changed; the prepared Page is preserved, register it after rereading")
        os.replace(temporary, head)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()
    return new_page or head


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    question = commands.add_parser("add-question")
    question.add_argument("block", type=Path)
    question.add_argument("--id", required=True)
    question.add_argument("--slug", required=True)
    question.add_argument("--question", required=True)
    question.add_argument("--title")
    question.add_argument("--hypothesis")
    question.add_argument("--acceptance")
    question.add_argument("--work", action="append", default=[])
    question.add_argument("--evidence", action="append", default=[], help="label|path inside the Block")
    question.add_argument("--drawing", action="append", default=[],
                          help="the report's one drawing, made blank in its own studio/ (reports/<id>_topic/studio/<name>.excalidraw); once per Question")
    report = commands.add_parser("add-report", help="a report Page for a Question already registered")
    report.add_argument("block", type=Path)
    report.add_argument("--id", required=True)
    report.add_argument("--slug", required=True)
    report.add_argument("--title", help="default: the Question's title, else its question")
    report.add_argument("--evidence", action="append", default=[], help="label|path inside the Block")
    report.add_argument("--drawing", action="append", default=[],
                        help="the report's one drawing, made blank in its own studio/ (reports/<id>_topic/studio/<name>.excalidraw); once per Question")
    resource = commands.add_parser("add-resource")
    resource.add_argument("block", type=Path)
    resource.add_argument("--title", required=True)
    resource.add_argument("--url", required=True)
    resource.add_argument("--question", action="append", default=[])
    resource.add_argument("--contribution")
    resource.add_argument("--notes")
    args = parser.parse_args()
    try:
        print(update(args))
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()

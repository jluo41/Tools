#!/usr/bin/env python3
"""Add a Block Question with an empty report Page, or a related resource.

This authors a register and Page frame, never an answer, accepted Content or Run.
"""
from pathlib import Path
import argparse
import json
import os
import re
import sys
import tempfile
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "servers/workbench-task"))
from task_questions import QUESTION_ID, inside, register, replace_register


def update(args):
    board = args.block.resolve()
    head = board / "board.md"
    if not inside(head, board):
        raise ValueError("board.md must stay inside the Block")
    original = head.read_text(encoding="utf-8")
    if not re.search(r"(?m)^board-kind: task-block\s*$", original):
        raise ValueError("Expected board-kind: task-block")
    questions, errors = register(original, "Questions", "questions")
    if errors:
        raise ValueError("; ".join(errors))
    new_page = None
    if args.command == "add-question":
        if not QUESTION_ID.fullmatch(args.id) or any(q.get("id") == args.id for q in questions):
            raise ValueError("Question id must be a new Q followed by at least two digits")
        if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", args.slug):
            raise ValueError("Slug must use lowercase words separated by underscores")
        if not args.question.strip() or "\n" in args.question or "\n" in (args.title or ""):
            raise ValueError("Question and title must be nonempty single-line text")
        for raw in args.work:
            rel = Path(raw)
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
        page_text = (f"# {args.title or args.slug.replace('_', ' ')}\nstate: 🔴 OPEN\n"
                     f"answers: {args.id}\nanswer-status: open\n\n## Opening\n\n"
                     "No answer has been recorded yet.\n\n"
                     f"**Where this Page sits:** [{args.id} · {args.question}](../../board.md).\n\n"
                     "**Why it matters:** The report will connect the question to its supporting evidence.\n\n"
                     "## Content\n")
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
        new_page.write_text(page_text, encoding="utf-8")
        (new_page.parent / "page.toml").write_text(
            'version = 1\nsource = ' + json.dumps(new_page.name) + '\ntitle = '
            + json.dumps(args.title or args.question, ensure_ascii=False) + '\n', encoding="utf-8")
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

#!/usr/bin/env python3
"""Create and synchronize lifecycle S faces with explicit inherited contracts.

    python3 stage.py new BOARD --family Main --unit 7 --slug results \
      --title "S Main 7 · Results" --requires S-Work-1,S-Main-0,S-Display-0 \
      --style-from S-Venue-1
    python3 stage.py sync BOARD S-Main-7
    python3 stage.py sync BOARD --all
    python3 stage.py check BOARD

``build.py`` remains render-only. This command is the explicit Markdown writer.
"""
import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from src.parse import parse_dir, split_sections  # noqa: E402
from src.stage_contract import (END, START, contract_digest, contract_status,  # noqa: E402
                                managed_span, refs, replace_managed)

FAMILIES = ("Seed", "Work", "Venue", "Display", "Main", "Appendix", "Submission")


def compact(text, limit=520):
    """Collapse an authored contract excerpt without copying a whole source page."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"^\s*[-*]\s*(?:\[[ xX]\]\s*)?", "", text, flags=re.M)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + "..."
    return text


def subsection(text, name):
    """Read one direct ### subsection from a ## section."""
    hit = re.search(
        rf"^###\s+{re.escape(name)}\s*$\n(.*?)(?=^###\s+|\Z)",
        text or "",
        re.M | re.S | re.I,
    )
    return hit.group(1).strip() if hit else ""


def source_excerpt(path, face, purpose):
    text = path.read_text(encoding="utf-8")
    sections = split_sections(text)
    stage_contract = sections.get("Stage Contract", "")
    span = managed_span(stage_contract)
    if span:
        stage_contract = stage_contract[:span[0]] + stage_contract[span[1]:]
    if purpose == "requirement":
        value = (
            subsection(stage_contract, "Provides")
            or sections.get("Provides", "")
            or (face or {}).get("provides", "")
        )
    else:
        value = (
            subsection(stage_contract, "Writing Style")
            or sections.get("Writing Style", "")
            or sections.get("Writing Contract", "")
        )
    return compact(value)


def catalog(board):
    meta, faces, warnings = parse_dir(board)
    del meta, warnings
    return faces, {q["id"].casefold(): q for q in faces if q.get("file")}


def resolve_source(board, token, by_id):
    face = by_id.get(token.casefold())
    if face:
        return board / face["file"], face
    path = Path(token)
    path = path if path.is_absolute() else board / path
    return (path, None) if path.is_file() else (None, None)


def source_line(board, token, by_id, purpose):
    path, source = resolve_source(board, token, by_id)
    if not path:
        return [
            f"- [ ] `{token}` · source not found",
            "      Resolve this explicit reference before the stage can pass.",
        ]
    try:
        rel = path.resolve().relative_to(board.resolve()).as_posix()
    except ValueError:
        rel = path.resolve().as_posix()
    title = token
    state = ""
    if source:
        title = source.get("title") or token
        state = source.get("state") or ""
    checked = "x" if purpose == "requirement" and state.startswith("✅") else " "
    marker = f"- [{checked}]" if purpose == "requirement" else "-"
    lines = [f"{marker} `{token}` · {title}", f"      Source: `{rel}`"]
    if state:
        lines[-1] += f"; gate state: {state}."
    else:
        lines[-1] += "."
    excerpt = source_excerpt(path, source, purpose)
    label = "Provides" if purpose == "requirement" else "Contract"
    if excerpt:
        lines.append(f"      **{label}:** {excerpt}")
    else:
        lines.append(
            f"      **{label}:** No explicit source section yet; follow the linked source "
            "and add a concise contract before this page passes."
        )
    return lines


def render_block(board, face, by_id):
    digest = contract_digest(board, face, by_id)
    lines = [
        f"{START} sha256={digest} -->",
        "### Required Inputs",
    ]
    required = refs(face.get("requires", ""))
    if required:
        for token in required:
            lines.extend(source_line(board, token, by_id, "requirement"))
    else:
        lines.append("No upstream stage is required.")
    lines.extend(["", "### Writing Style"])
    styles = refs(face.get("style_from", ""))
    if styles:
        for token in styles:
            lines.extend(source_line(board, token, by_id, "style"))
    else:
        lines.append("No inherited writing-style source is declared.")
    lines.extend([
        "",
        "<!-- Generated from explicit requires/style-from metadata.",
        "     Refresh with stage.py sync; build.py never edits Markdown. -->",
        END,
    ])
    return "\n".join(lines), digest


def update_hash(text, digest):
    line = f"contract-source-hash: {digest}"
    text = re.sub(r"^contract-source-hash:.*\n?", "", text, flags=re.M)
    section = re.search(r"^##\s+", text, re.M)
    if not section:
        return text.rstrip() + "\n" + line + "\n"
    prefix = text[:section.start()].rstrip()
    suffix = text[section.start():].lstrip()
    return prefix + "\n" + line + "\n\n" + suffix


def sync_face(board, face, by_id):
    path = board / face["file"]
    block, digest = render_block(board, face, by_id)
    text = path.read_text(encoding="utf-8")
    text = replace_managed(text, block)
    text = update_hash(text, digest)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return path


def find_face(value, faces, by_id):
    hit = by_id.get(value.casefold())
    if hit:
        return hit
    for face in faces:
        if face.get("file") == value or Path(face.get("file", "")).name == value:
            return face
    raise SystemExit(f"stage face not found: {value}")


def dependency_order(targets, by_id):
    """Topologically order S faces from explicit references, never Pages order."""
    wanted = {q["id"].casefold(): q for q in targets}
    ordered, visiting, done = [], set(), set()

    def visit(face):
        key = face["id"].casefold()
        if key in done:
            return
        if key in visiting:
            cycle = " -> ".join(list(visiting) + [key])
            raise SystemExit(f"stage contract dependency cycle: {cycle}")
        visiting.add(key)
        for value in (face.get("requires", ""), face.get("style_from", "")):
            for token in refs(value):
                source = by_id.get(token.casefold())
                if source and source["id"].casefold() in wanted:
                    visit(source)
        visiting.remove(key)
        done.add(key)
        ordered.append(face)

    for target in targets:
        visit(target)
    return ordered


def add_to_pages(board, group, filename):
    path = board / "board.md"
    text = path.read_text(encoding="utf-8")
    heading = re.search(rf"^###\s+{re.escape(group)}\s*$", text, re.M)
    if not heading:
        raise SystemExit(f"Pages group not found: {group}")
    next_heading = re.search(r"^###\s+", text[heading.end():], re.M)
    end = heading.end() + (next_heading.start() if next_heading else len(text[heading.end():]))
    prefix = text[:end].rstrip()
    suffix = text[end:].lstrip("\n")
    path.write_text(prefix + "\n" + filename + "\n" + suffix, encoding="utf-8")


def resolve_filename(family, unit, slug):
    """The one place an S face's filename is composed. Board tooling owns this (QC2).

    Any other layer that needs the name of a lifecycle page calls this rather than
    spelling `S-{family}-{unit}-{slug}.md` itself, so the rule cannot be duplicated
    into a contract, a doc, or a checker and then drift.

    Returns (filename, family, unit, slug) with the three parts normalized.
    """
    family = family.title()
    if family not in FAMILIES:
        raise SystemExit(f"family must be one of: {', '.join(FAMILIES)}")
    unit = str(unit).upper()
    if not re.fullmatch(r"\d+|[A-Z]", unit):
        raise SystemExit("unit must be a number or one uppercase letter")
    slug = re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-")
    if not slug:
        raise SystemExit("slug must contain at least one letter or number")
    return f"S-{family}-{unit}-{slug}.md", family, unit, slug


def new_stage(args):
    board = args.board.resolve()
    filename, family, unit, slug = resolve_filename(args.family, args.unit, args.slug)
    target_id = f"S-{family}-{unit}".casefold()
    faces, by_id = catalog(board)
    del faces
    if target_id in by_id:
        raise SystemExit(f"stage id already exists: S-{family}-{unit}")
    path = (board / (args.directory or "") / filename).resolve()
    try:
        path.relative_to(board)
    except ValueError:
        raise SystemExit("directory must stay inside the board")
    if path.exists():
        raise SystemExit(f"already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    text = f"""# {args.title}
state: 🔴 OPEN
owner: {args.owner}
method: {args.method}
requires: {args.requires or ""}
style-from: {args.style_from or ""}
provides: {args.provides or ""}

## Question
What must this stage produce, under which inherited requirements and writing contract?

This page is a concrete lifecycle unit. Its Stage Contract is generated from explicit
dependencies; its Content remains authored here.

## Boundary
- ✅ Covered here
  The named stage output and its human gate.
- ↪ Covered elsewhere
  Upstream evidence stays in the linked source pages.

## Stage Contract

## Content

### Stage Output
Write the stage substance here.

## Items to Finish
- [ ] 🎯 Produce the declared output
      Define the observable artifact and its acceptance condition.
- [ ] 🧠 Pass the human gate
      Record the decision before changing this stage to ✅ SETTLED.

## Where we are
The stage page has been created; substantive work has not started.

## Files
- `{path.relative_to(board).as_posix()}`
  Canonical lifecycle face for this stage.
"""
    path.write_text(text, encoding="utf-8")
    if args.group:
        add_to_pages(board, args.group, filename)
    faces, by_id = catalog(board)
    face = find_face(filename, faces, by_id)
    sync_face(board, face, by_id)
    print(path)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("new", help="create one S face and its managed contract")
    new.add_argument("board", type=Path)
    new.add_argument("--family", required=True)
    new.add_argument("--unit", required=True)
    new.add_argument("--slug", required=True)
    new.add_argument("--title", required=True)
    new.add_argument("--requires", default="")
    new.add_argument("--style-from", default="")
    new.add_argument("--provides", default="")
    new.add_argument("--owner", default="JL")
    new.add_argument("--method", default="complete the inherited contract, author the output, and pass the human gate")
    new.add_argument("--directory", default="")
    new.add_argument("--group", default="")

    sync = sub.add_parser("sync", help="refresh managed contract blocks")
    sync.add_argument("board", type=Path)
    sync.add_argument("face", nargs="?")
    sync.add_argument("--all", action="store_true")

    check = sub.add_parser("check", help="report unsynchronized contracts")
    check.add_argument("board", type=Path)

    res = sub.add_parser("resolve", help="print the S filename for a family/unit/slug")
    res.add_argument("--family", required=True)
    res.add_argument("--unit", required=True)
    res.add_argument("--slug", required=True)

    args = parser.parse_args()
    if args.command == "resolve":
        print(resolve_filename(args.family, args.unit, args.slug)[0])
        return
    if args.command == "new":
        new_stage(args)
        return

    board = args.board.resolve()
    faces, by_id = catalog(board)
    if args.command == "sync":
        targets = [q for q in faces if q.get("kind") == "stage" and
                   (refs(q.get("requires", "")) or refs(q.get("style_from", "")))]
        if not args.all:
            if not args.face:
                raise SystemExit("sync needs FACE or --all")
            targets = [find_face(args.face, faces, by_id)]
        else:
            targets = dependency_order(targets, by_id)
        for face in targets:
            print(sync_face(board, face, by_id))
        return

    warnings = [contract_status(board, q, by_id) for q in faces]
    warnings = [w for w in warnings if w]
    for warning in warnings:
        print(warning)
    raise SystemExit(1 if warnings else 0)


if __name__ == "__main__":
    main()

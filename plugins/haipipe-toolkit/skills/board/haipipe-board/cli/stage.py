#!/usr/bin/env python3
"""Create and synchronize lifecycle S pages with explicit inherited contracts.

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

HERE = Path(__file__).resolve().parent.parent  # the engine dir (this file lives in cli/)
sys.path.insert(0, str(HERE))

from src.parse import parse_dir, split_sections  # noqa: E402
from src.stage_contract import (END, START, STYLE_END, STYLE_START,  # noqa: E402
                                contract_digest, contract_status,
                                managed_span, refs, replace_managed,
                                replace_managed_style)

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


def source_excerpt(path, page, purpose):
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
            or (page or {}).get("provides", "")
        )
    else:
        value = (
            subsection(stage_contract, "Writing Style")
            or sections.get("Writing Style", "")
            or sections.get("Writing Contract", "")
        )
    return compact(value)


def catalog(board):
    meta, pages, warnings = parse_dir(board)
    del meta, warnings
    return pages, {q["id"].casefold(): q for q in pages if q.get("file")}


def resolve_source(board, token, by_id):
    page = by_id.get(token.casefold())
    if page:
        return board / page["file"], page
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
    if purpose == "venue":
        lines.append("      Writing rules: materialized from this source in `## Writing Style`.")
        return lines
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


def render_block(board, page, by_id):
    digest = contract_digest(board, page, by_id)
    lines = [
        f"{START} sha256={digest} -->",
        "### Required Inputs",
    ]
    required = refs(page.get("requires", ""))
    if required:
        for token in required:
            lines.extend(source_line(board, token, by_id, "requirement"))
    else:
        lines.append("No upstream stage is required.")
    lines.extend(["", "### Venue"])
    styles = refs(page.get("style_from", ""))
    if styles:
        for token in styles:
            lines.extend(source_line(board, token, by_id, "venue"))
    else:
        lines.append("No venue or inherited writing source is declared.")
    lines.extend([
        "",
        "<!-- Generated from explicit requires/style-from metadata.",
        "     Refresh with stage.py sync; build.py never edits Markdown. -->",
        END,
    ])
    return "\n".join(lines), digest


def render_style_block(board, page, by_id, digest):
    """Materialize ``style-from`` rules in the page's own Writing Style section."""
    lines = [f"{STYLE_START} sha256={digest} -->"]
    styles = refs(page.get("style_from", ""))
    if styles:
        for token in styles:
            path, source = resolve_source(board, token, by_id)
            if not path:
                lines.append(
                    f"**Inherited requirements from `{token}`**: Source not found. "
                    "Resolve this reference before the stage can pass."
                )
                continue
            excerpt = source_excerpt(path, source, "style")
            try:
                rel = path.resolve().relative_to(board.resolve()).as_posix()
            except ValueError:
                rel = path.resolve().as_posix()
            requirement = excerpt or (
                "No explicit Writing Style exists yet; add a concise contract to the linked source."
            )
            lines.append(
                f"**Inherited requirements from `{token}`**: {requirement} Source: `{rel}`."
            )
    else:
        lines.append("**Inherited requirements**: No `style-from` source is declared.")
    lines.extend([
        "<!-- Generated from explicit style-from metadata.",
        "     Refresh with stage.py sync; build.py never edits Markdown. -->",
        STYLE_END,
    ])
    return "\n".join(lines)


def update_hash(text, digest):
    line = f"contract-source-hash: {digest}"
    text = re.sub(r"^contract-source-hash:.*\n?", "", text, flags=re.M)
    section = re.search(r"^##\s+", text, re.M)
    if not section:
        return text.rstrip() + "\n" + line + "\n"
    prefix = text[:section.start()].rstrip()
    suffix = text[section.start():].lstrip()
    return prefix + "\n" + line + "\n\n" + suffix


def sync_face(board, page, by_id):
    path = board / page["file"]
    block, digest = render_block(board, page, by_id)
    style_block = render_style_block(board, page, by_id, digest)
    text = path.read_text(encoding="utf-8")
    text = replace_managed(text, block)
    text = replace_managed_style(text, style_block)
    text = update_hash(text, digest)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return path


def find_face(value, pages, by_id):
    hit = by_id.get(value.casefold())
    if hit:
        return hit
    for page in pages:
        if page.get("file") == value or Path(page.get("file", "")).name == value:
            return page
    raise SystemExit(f"stage page not found: {value}")


def dependency_order(targets, by_id):
    """Topologically order S pages from explicit references, never Pages order."""
    wanted = {q["id"].casefold(): q for q in targets}
    ordered, visiting, done = [], set(), set()

    def visit(page):
        key = page["id"].casefold()
        if key in done:
            return
        if key in visiting:
            cycle = " -> ".join(list(visiting) + [key])
            raise SystemExit(f"stage contract dependency cycle: {cycle}")
        visiting.add(key)
        for value in (page.get("requires", ""), page.get("style_from", "")):
            for token in refs(value):
                source = by_id.get(token.casefold())
                if source and source["id"].casefold() in wanted:
                    visit(source)
        visiting.remove(key)
        done.add(key)
        ordered.append(page)

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
    """The one place an S page's filename is composed. Board tooling owns this (QC2).

    Any other layer that needs the name of a lifecycle page calls this rather than
    spelling `S-{family}-{unit}-{slug}.md` itself, so the rule cannot be duplicated
    into a contract, a doc, or a checker and then drift.

    Returns (filename, family, unit, slug) with the three parts normalized.
    """
    family = family.title()
    if family not in FAMILIES:
        raise SystemExit(f"family must be one of: {', '.join(FAMILIES)}")
    unit = str(unit)
    if re.fullmatch(r"[A-Za-z]", unit):
        unit = unit.upper()          # an appendix letter: S-Appendix-C
    elif re.fullmatch(r"[A-Za-z]\d+", unit):
        unit = unit[0].upper() + unit[1:]   # a lettered series member: S-Work-R1
    elif not re.fullmatch(r"\d+|\d+[a-z][a-z0-9]*", unit):
        # A BLOCK + MEMBER id is the Display family's grammar (JL 260727): the number
        # is the narrative block a unit serves and the lowercase letter is its position
        # inside that block, so `4a` is the first results display. An optional tail after
        # the letter marks a VARIANT of that member, same claim and same job under a
        # different specification, which inherits its parent's letter so that inserting
        # one costs no rename: `4al2` is `4a` estimated on the binary trait_l2 exposure.
        # Case is preserved here rather than upper-cased, because these ids are written
        # lowercase on disk and the board's own parser reads them either way.
        raise SystemExit(
            "unit must be a number (S-Main-6), one letter (S-Appendix-C), "
            "a lettered series member (S-Work-R1), a block+member id "
            "(S-Display-4a), or a variant of one (S-Display-4al2)")
    slug = re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-")
    if not slug:
        raise SystemExit("slug must contain at least one letter or number")
    return f"S-{family}-{unit}-{slug}.md", family, unit, slug


def new_stage(args):
    board = args.board.resolve()
    filename, family, unit, slug = resolve_filename(args.family, args.unit, args.slug)
    target_id = f"S-{family}-{unit}".casefold()
    pages, by_id = catalog(board)
    del pages
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

## Opening
What must this stage produce, under which inherited requirements and page Writing Style?

This page is a concrete lifecycle unit. Its Stage Contract and inherited Writing Style are
generated from explicit dependencies; its Content remains authored here.

The named stage output and its human gate are covered here; upstream evidence stays in the linked source pages.

## Writing Style
English only. One sentence per source line. Write the stage product for its named reader, keep Required Inputs and Venue in Stage Contract, and keep prose rules here.

## Stage Contract

## Content

### Stage Output
Write the stage substance here.

## Aims
### Stage Output
- A1.1 · Produce the declared output.
  **Done when:** The observable artifact exists and meets its acceptance condition.
- A1.2 · Pass the human gate.
  **Done when:** The decision is recorded before this stage changes to ✅ SETTLED.

## States
### Stage Output
- ⬜ A1.1 · Not started; the stage page has just been created.
- ⬜ A1.2 · Not started; no human ruling has been recorded.

## Files
- `{path.relative_to(board).as_posix()}`
  Canonical lifecycle page for this stage.
"""
    path.write_text(text, encoding="utf-8")
    if args.group:
        add_to_pages(board, args.group, filename)
    pages, by_id = catalog(board)
    page = find_face(filename, pages, by_id)
    sync_face(board, page, by_id)
    print(path)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("new", help="create one S page and its managed contract")
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
    sync.add_argument("page", nargs="?")
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
    pages, by_id = catalog(board)
    if args.command == "sync":
        targets = [q for q in pages if q.get("kind") == "stage" and
                   (refs(q.get("requires", "")) or refs(q.get("style_from", "")))]
        if not args.all:
            if not args.page:
                raise SystemExit("sync needs PAGE or --all")
            targets = [find_face(args.page, pages, by_id)]
        else:
            targets = dependency_order(targets, by_id)
        for page in targets:
            print(sync_face(board, page, by_id))
        return

    warnings = [contract_status(board, q, by_id) for q in pages]
    warnings = [w for w in warnings if w]
    for warning in warnings:
        print(warning)
    raise SystemExit(1 if warnings else 0)


if __name__ == "__main__":
    main()

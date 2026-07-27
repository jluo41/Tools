#!/usr/bin/env python3
"""Create one paper lifecycle S page through the Board's shell primitive.

The paper stage is the public creator. It selects the stage contract and template.
haipipe-board/stage.py owns the filename, face grammar, listing under Pages, and
managed dependency contract.

Usage:
    python3 create-page.py seed <paper-root>
    python3 create-page.py section-edit <paper-root> \
      --family Main --unit 2 --slug introduction \
      --directory 5-section-edit/1-introduction
"""

import argparse
import ast
import re
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
STAGES = HERE / "stages"
BOARD_STAGE = HERE.parents[2] / "board" / "haipipe-board" / "stage.py"


def scalar(value):
    """Parse the small scalar subset used by stage contracts."""
    value = value.strip()
    if not value:
        return ""
    if value[0:1] in {"'", '"'}:
        try:
            return str(ast.literal_eval(value))
        except (SyntaxError, ValueError):
            pass
    return value.split(" #", 1)[0].strip()


def contract(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise SystemExit(f"stage contract has no frontmatter: {path}")
    values = {}
    for line in match.group(1).splitlines():
        hit = re.match(r"^([a-z][a-z0-9_-]*):\s*(.*)$", line)
        if hit:
            values[hit.group(1)] = scalar(hit.group(2))
    return values


def stage_contract(stage_key):
    """Resolve through the small index, then load only the selected contract."""
    index = (STAGES / "index.yml").read_text(encoding="utf-8")
    rows = re.findall(
        r"-\s*\{key:\s*([^,\s]+),.*?\bdir:\s*([^,\s}]+).*?\}",
        index,
        flags=re.S,
    )
    matches = [directory for key, directory in rows if key == stage_key]
    if not matches:
        raise SystemExit(f"unknown stage: {stage_key}")
    if len(matches) > 1:
        raise SystemExit(f"duplicate stage key in index: {stage_key}")
    path = STAGES / matches[0] / "stage.md"
    return path, contract(path)


def compact_rule(text, limit=220):
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^RULE:\s*", "", text, flags=re.I)
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + "..."
    return text


def readable_path(path):
    """Show a stable skill-relative path when possible."""
    for root in (HERE, HERE.parents[1]):
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            continue
    return path.as_posix()


def template_divisions(path):
    """Read the stage's logical divisions from its Setext template.

    `Q-consumer` is a logical division in every stage contract, but Board owns
    its physical home: recognizable checklist records in `## Items to Finish`.
    Callers must not put that division under `## Content`.
    """
    text = path.read_text(encoding="utf-8")
    board_content = re.search(
        r"^## Content\s*$\n(.*?)(?=^## Items to Finish\s*$)",
        text,
        re.M | re.S,
    )
    board_items = re.search(
        r"^## Items to Finish\s*$\n(.*?)(?=^## Where we are\s*$)",
        text,
        re.M | re.S,
    )
    if board_content and board_items:
        divisions = []
        body = board_content.group(1)
        hits = list(re.finditer(r"^###\s+(.+?)\s*$", body, re.M))
        for index, hit in enumerate(hits):
            end = hits[index + 1].start() if index + 1 < len(hits) else len(body)
            division_body = body[hit.end():end]
            rule = re.search(r"<!--\s*(RULE:.*?)-->", division_body, re.S | re.I)
            job = compact_rule(rule.group(1)) if rule else f"Complete the {hit.group(1)} stage output."
            divisions.append((hit.group(1).strip(), job))
        if re.search(r"Q-[A-Za-z]+-<n>", board_items.group(1)):
            divisions.append(("Q-consumer", "Raise the evidence questions this display cannot answer itself."))
        if divisions:
            return divisions

    lines = text.splitlines()
    divisions = []
    for index in range(len(lines) - 1):
        title = lines[index].strip()
        underline = lines[index + 1].strip()
        if title and re.fullmatch(r"-{3,}", underline):
            next_index = len(lines)
            for probe in range(index + 2, len(lines) - 1):
                if lines[probe].strip() and re.fullmatch(r"-{3,}", lines[probe + 1].strip()):
                    next_index = probe
                    break
            body = "\n".join(lines[index + 2:next_index])
            rule = re.search(r"<!--\s*(RULE:.*?)-->", body, re.S | re.I)
            job = compact_rule(rule.group(1)) if rule else f"Complete the {title} stage output."
            divisions.append((title, job))

    # Narrative, Resource, and section templates deliberately use ATX `##`
    # headings inside (or beside) their Setext logical divisions. Collect both
    # forms before Q-consumer, then flatten them into Board's direct `###`
    # Content divisions. A venue template commonly has a Setext Structure
    # overview PLUS ATX paragraph blocks; treating these parsers as alternatives
    # silently drops the prose scaffold.
    q_marker = re.search(r"^Q-consumer\s*$\n-{3,}\s*$", text, re.M)
    content_text = text[:q_marker.start()] if q_marker else text
    hits = list(re.finditer(r"^##\s+(.+?)\s*$", content_text, re.M))
    atx_divisions = []
    ignored = {"readiness legend"}
    existing = {title.strip().casefold() for title, _ in divisions}
    for index, hit in enumerate(hits):
        title = hit.group(1).strip()
        if title.casefold() in ignored or title.casefold() in existing:
            continue
        end = hits[index + 1].start() if index + 1 < len(hits) else len(content_text)
        body = content_text[hit.end():end]
        rule = re.search(r"<!--\s*(RULE:.*?)-->", body, re.S | re.I)
        job = compact_rule(rule.group(1)) if rule else f"Complete the {title} stage output."
        atx_divisions.append((title, job))
        existing.add(title.casefold())
    if atx_divisions:
        q_divisions = [
            item for item in divisions if item[0].strip().casefold() == "q-consumer"
        ]
        content_divisions = [
            item for item in divisions if item[0].strip().casefold() != "q-consumer"
        ]
        divisions = content_divisions + atx_divisions + q_divisions

    if not divisions:
        raise SystemExit(f"no logical stage divisions found in template: {path}")
    return divisions


def board_template_items(path):
    """Return a full Board template's own Items scaffold, if it has one."""
    text = path.read_text(encoding="utf-8")
    match = re.search(
        r"^## Items to Finish\s*$\n(.*?)(?=^## Where we are\s*$)",
        text,
        re.M | re.S,
    )
    return match.group(1).strip() if match else ""


def resolve_template(stage_path, values, paper_root, board, section_kind="", override=""):
    """Resolve a fixed template or one pinned by Venue's Section Styles records."""
    declared = override or values.get("template", "")
    if not declared:
        raise SystemExit(f"stage declares no template: {stage_path}")

    if declared.startswith("<resolved"):
        if not section_kind:
            raise SystemExit("dynamic section-edit template requires --section-kind")
        venue_contract = values.get("venue_contract", "")
        venue_page = paper_root / venue_contract
        if not venue_contract or not venue_page.is_file():
            raise SystemExit(
                "cannot resolve section template: Venue page is absent; "
                "run the venue stage before section-edit"
            )
        token = ""
        for line in venue_page.read_text(encoding="utf-8").splitlines():
            fields = [field.strip() for field in line.split("·")]
            if not fields or fields[0].casefold() != section_kind.casefold():
                continue
            for field in fields[1:]:
                if field.casefold().startswith("template:"):
                    token = field.split(":", 1)[1].strip().strip("`")
                    break
            if token:
                break
        if not token:
            raise SystemExit(
                f"Venue Section Styles has no template record for section kind: {section_kind}"
            )
        if "generic-fallback" in token.casefold():
            declared = values.get("fallback_template", "")
        else:
            declared = token

    candidate = Path(declared)
    candidates = [candidate] if candidate.is_absolute() else [
        stage_path.parent / candidate,
        HERE.parents[1] / candidate,
        paper_root / candidate,
        board / candidate,
    ]
    for path in candidates:
        if path.is_file():
            return path.resolve()
    searched = ", ".join(str(path) for path in candidates)
    raise SystemExit(f"stage template not found: {declared} (searched: {searched})")


def replace_section(text, heading, body, next_heading):
    pattern = rf"(^## {re.escape(heading)}\s*$\n).*?(?=^## {re.escape(next_heading)}\s*$)"
    updated, count = re.subn(
        pattern,
        lambda match: match.group(1) + body.rstrip() + "\n\n",
        text,
        count=1,
        flags=re.M | re.S,
    )
    if count != 1:
        raise SystemExit(f"cannot locate ## {heading} in generated S page")
    return updated


def existing_face(board, family, unit):
    pattern = f"S-{family}-{unit}-*.md"
    hits = [path for path in board.rglob(pattern) if not any(part.startswith(("_", ".")) for part in path.relative_to(board).parts)]
    if len(hits) > 1:
        raise SystemExit(f"more than one face resolves S-{family}-{unit}: {hits}")
    return hits[0] if hits else None


def main():
    parser = argparse.ArgumentParser(description="create one Board-first paper stage page")
    parser.add_argument("stage")
    parser.add_argument("paper_root", type=Path)
    parser.add_argument("--family")
    parser.add_argument("--unit")
    parser.add_argument("--slug")
    parser.add_argument("--directory")
    parser.add_argument("--section-kind")
    parser.add_argument("--template", help="explicit template override; normally Venue resolves this")
    parser.add_argument("--requires", default="")
    parser.add_argument("--style-from", default="")
    parser.add_argument("--provides", default="")
    parser.add_argument("--owner", default="JL")
    args = parser.parse_args()

    stage_path, values = stage_contract(args.stage)
    paper_root = args.paper_root.resolve()
    board = paper_root / "0-lifecycle"
    if not (board / "board.md").is_file():
        raise SystemExit(f"paper lifecycle Board not found: {board / 'board.md'}")
    if not BOARD_STAGE.is_file():
        raise SystemExit(f"Board stage primitive not found: {BOARD_STAGE}")

    family = args.family or values.get("board_family", "")
    unit = args.unit or values.get("board_unit", "")
    if not family or " or " in family.lower():
        raise SystemExit("dynamic stage requires --family")
    if not unit or " " in unit:
        raise SystemExit("dynamic stage requires --unit")
    family = family.title()
    unit = unit.upper()

    found = existing_face(board, family, unit)
    if found:
        print(found)
        return

    slug = args.slug or values.get("board_slug") or values.get("key", "")
    title = values.get("title") or args.stage.title()
    question = values.get("one_line") or f"What must the {title} stage produce?"
    template = resolve_template(
        stage_path,
        values,
        paper_root,
        board,
        section_kind=args.section_kind or "",
        override=args.template or "",
    )

    directory = args.directory
    if not directory:
        artifact = values.get("artifact", "")
        if not artifact.startswith("0-lifecycle/"):
            raise SystemExit("stage artifact does not identify a lifecycle directory; pass --directory")
        directory = Path(artifact.removeprefix("0-lifecycle/")).parent.as_posix()

    command = [
        sys.executable,
        str(BOARD_STAGE),
        "new",
        str(board),
        "--family",
        family,
        "--unit",
        unit,
        "--slug",
        slug,
        "--title",
        f"S {family} {unit} · {title}",
        "--owner",
        args.owner,
        "--method",
        "run the paper stage contract, write Content here, and close at its human gate",
        "--directory",
        directory,
        "--group",
        f"S-{family}",
    ]
    if args.requires:
        command.extend(["--requires", args.requires])
    if args.style_from:
        command.extend(["--style-from", args.style_from])
    if args.provides:
        command.extend(["--provides", args.provides])
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    generated = Path(result.stdout.strip().splitlines()[-1])

    page = generated.read_text(encoding="utf-8")
    question_body = (
        f"{question}\n\nThis is the `{args.stage}` lifecycle page. Its stage-specific "
        f"Content scaffold comes from `{readable_path(stage_path)}` and "
        f"`{readable_path(template)}`."
    )
    page = replace_section(page, "Question", question_body, "Boundary")

    content_lines = []
    q_consumer_jobs = []
    for division, job in template_divisions(template):
        if division.strip().lower() == "q-consumer":
            q_consumer_jobs.append(job)
            continue
        content_lines.extend([f"### {division}", f"({job})", ""])
    if not q_consumer_jobs:
        raise SystemExit(f"stage template has no Q-consumer division: {template}")
    page = replace_section(page, "Content", "\n".join(content_lines), "Items to Finish")

    q_pattern = values.get("q_id_pattern", "")
    q_match = re.search(r"Q-[A-Za-z]+-<n>", q_pattern)
    q_id = q_match.group(0).replace("<n>", "1") if q_match else f"Q-{title}-1"
    items = board_template_items(template)
    if items:
        items = re.sub(r"Q-[A-Za-z]+-<n>", q_id, items)
    else:
        items = "\n".join([
            f"- [ ] 🔎 {q_id} · <concrete consumer question>",
            "      **Description:** <what must be learned, in the consumer's own words>",
            "      **Reason:** <which Content assertion depends on it and what breaks if it fails>",
            "      **Probe:** not opened yet",
            "      **Answer:** <empty until PROBE lands, interprets, and weaves the answer>",
        ])
    page = replace_section(page, "Items to Finish", items, "Where we are")

    where = f"The Board shell and the `{title}` Content divisions have been created. DRAFT has not yet authored the stage substance."
    page = replace_section(page, "Where we are", where, "Files")
    generated.write_text(page.rstrip() + "\n", encoding="utf-8")
    print(generated)


if __name__ == "__main__":
    main()

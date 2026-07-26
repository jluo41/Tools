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
BOARD_STAGE = HERE.parents[2] / "0_utils" / "haipipe-board" / "stage.py"


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


def template_divisions(path):
    """Convert a paper Setext template into Board Content divisions."""
    text = path.read_text(encoding="utf-8")
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
    if not divisions:
        raise SystemExit(f"no Setext stage divisions found in template: {path}")
    return divisions


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

    slug = args.slug or values.get("key", "")
    title = values.get("title") or args.stage.title()
    question = values.get("one_line") or f"What must the {title} stage produce?"
    template_name = values.get("template")
    if not template_name:
        raise SystemExit(f"stage declares no template: {stage_path}")
    template = stage_path.parent / template_name
    if not template.is_file():
        raise SystemExit(f"stage template not found: {template}")

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
    question_body = f"{question}\n\nThis is the `{args.stage}` lifecycle page. Its stage-specific Content scaffold comes from `{stage_path.relative_to(HERE).as_posix()}` and `{template.relative_to(HERE).as_posix()}`."
    page = replace_section(page, "Question", question_body, "Boundary")

    content_lines = []
    for division, job in template_divisions(template):
        content_lines.extend([f"### {division}", f"({job})", ""])
    page = replace_section(page, "Content", "\n".join(content_lines), "Items to Finish")

    where = f"The Board shell and the `{title}` Content divisions have been created. DRAFT has not yet authored the stage substance."
    page = replace_section(page, "Where we are", where, "Files")
    generated.write_text(page.rstrip() + "\n", encoding="utf-8")
    print(generated)


if __name__ == "__main__":
    main()

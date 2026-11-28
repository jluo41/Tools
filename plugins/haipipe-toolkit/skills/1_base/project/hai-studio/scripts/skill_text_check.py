"""A skill's SKILL.md and ref files state the rule and nothing about who asked for it (hai-studio A09).

    python skill_text_check.py [<skill folder> ...]        default: this skill

Flags, with file and line: a who-and-when note (`JL 261112: "..."`, `(JL 261030)`), a decision id used as a source
(`b35 s01-D12`), one Block's Studio Type named by number in SKILL.md (types live in each Block's Studio Type band,
never in a table here), a marker comment line (`<!-- ... -->`, which the page shows as text), a file the text names under
ref/ or scripts/ that is not on disk, and a ref file or script the SKILL.md never names. A generated ref file (its
first comment says GENERATED) is skipped and listed. In `gallery/`, one folder per Studio Type: SKILL.md names
`gallery/`, a type with scripts has a TYPE.md, and that TYPE.md names each of them. CONSTITUTION.md is not checked: it keeps the words verbatim.
Exit 1 on any ❗.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

WHO = re.compile(r"\bJL 2\d{5}\b")
DECISION = re.compile(r"\b(?:b\d\d[ -])?s\d\d-D\d{2,3}\b")
MARKER = re.compile(r"^\s*<!--.*-->\s*$")
ONE_TYPE = re.compile(r"\bs7\d\b|\bs\d\d-studio-type-")      # one Block's type topic, named in the skill's own text


def problems(skill: Path) -> tuple[list[str], list[str]]:
    out, skipped = [], []
    main = skill / "SKILL.md"
    if not main.is_file():
        return [f"❗ {skill.name}: no SKILL.md"], skipped
    text = main.read_text(encoding="utf-8")
    for path in [main] + sorted((skill / "ref").glob("*.md")):
        body = path.read_text(encoding="utf-8")
        if path != main and "GENERATED" in body[:600]:
            skipped.append(path.name)
            continue
        fence = False
        for n, line in enumerate(body.splitlines(), 1):
            if line.lstrip().startswith("```"):
                fence = not fence
            where = f"{skill.name}/{path.relative_to(skill)}:{n}"
            if WHO.search(line):
                out.append(f"❗ {where}: a who-and-when note; state the rule only")
            if MARKER.match(line) and not fence:
                out.append(f"❗ {where}: a marker comment line; the page shows it as text")
            if path == main and ONE_TYPE.search(line):
                out.append(f"❗ {where}: names one Block's Studio Type; point to the Studio Type band instead")
            if path == main and DECISION.search(line) and "`sNN-DNN`" not in line:
                out.append(f"❗ {where}: a decision id as a source; state the rule only")
    for name in sorted(set(re.findall(r"(?<![\w/.-])((?:ref|scripts)/[\w.-]+\.(?:md|py))", text)) |
                       set(re.findall(r"(?<![\w/.-])(gallery/[\w-]+/(?:scripts/)?[\w.-]+\.(?:md|py))", text))):
        if not (skill / name).is_file():
            out.append(f"❗ {skill.name}/SKILL.md: names {name}, which is not on disk")
    for path in sorted(list((skill / "ref").glob("*.md")) + list((skill / "scripts").glob("*.py"))):
        if path.name not in text:
            out.append(f"❗ {skill.name}/SKILL.md: never names {path.relative_to(skill)}")
    for cell in sorted(p for p in (skill / "gallery").glob("*") if p.is_dir()):   # one folder per Studio Type
        guide, own = cell / "TYPE.md", sorted((cell / "scripts").glob("*.py"))
        if "gallery/" not in text:
            out.append(f"❗ {skill.name}/SKILL.md: never names gallery/, where {cell.name} is kept")
        if own and not guide.is_file():
            out.append(f"❗ {skill.name}/gallery/{cell.name}: has scripts and no TYPE.md that says how to use them")
        if not guide.is_file():
            continue
        body = guide.read_text(encoding="utf-8")
        for n, line in enumerate(body.splitlines(), 1):
            if WHO.search(line):
                out.append(f"❗ {skill.name}/gallery/{cell.name}/TYPE.md:{n}: a who-and-when note; state the rule only")
        out += [f"❗ {skill.name}/gallery/{cell.name}/TYPE.md: never names scripts/{p.name}" for p in own if p.name not in body]
    return out, skipped


def main(argv: list[str]) -> int:
    skills = [Path(a).resolve() for a in argv] or [Path(__file__).resolve().parents[1]]
    bad = 0
    for skill in skills:
        found, skipped = problems(skill)
        for line in found:
            print(line)
        for name in skipped:
            print(f"— {skill.name}/ref/{name}: generated, not checked")
        print(f"{'❗' if found else '✅'} {skill.name}")
        bad += bool(found)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

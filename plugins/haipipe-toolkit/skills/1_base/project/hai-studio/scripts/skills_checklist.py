"""Write each Skills topic's Checklist: the topic held against its Studio Type (b17 s76), one line per part of the
type, in the topic's own face (hai-studio A06, A08). The Block page's Checklist section reads it: one left tab
per topic, its lines on the right.

    <host venv python> skills_checklist.py <Block or topic> [--check]

The lines open the face's Checklist section. A line belongs to this script when it is a list line that starts with
a mark and one of the type's parts, so a rerun replaces exactly those lines and any other text of the section stays:

    - ✅ SKILL.md · the first tab of every skill
    - — CONSTITUTION.md: no skill here has one
    - ❗ ref/: hai-x has it but shows no tab

No marker comment fences them: the page's Markdown shows a comment line as text.

✅ has it, ❗ applies but is not shown (or shows what the skill lacks), — does not apply. `--check` writes nothing
and exits 1 when a face's lines are stale or any line is ❗. These lines are results, computed from the skills'
folders today; the Check top button (ref/check-view.md) lists the criteria and how to verify them, and claims none.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skills_views  # noqa: E402

# the parts this script can hold a topic against; which of them apply is read from the type the topic names
PARTS = ("〈skill〉", "SKILL.md", "CONSTITUTION.md", "ref/", "scripts/", "〈folder〉/", "〈file〉")
MARK = r"^- (?:✅|❗|—|🙋) "
OWNED = re.compile(MARK + r"(?:%s)(?: · |: |$)" % "|".join(re.escape(x) for x in PARTS + ("Draw",)))
MARKER = re.compile(r"^<!-- type-check:(start|end)\b.*-->$")        # an earlier form, removed on the next write
HEADING = re.compile(r"^#{1,3}\s+\S")
NONE = {"CONSTITUTION.md": "no skill here has one", "ref/": "no skill here has a ref/ with a file",
        "scripts/": "no skill here has a scripts/ with a file", "〈folder〉/": "no skill here has another folder",
        "〈file〉": "no skill here has a loose file"}


def _part(name: str) -> str:
    """The part of the type a left tab belongs to."""
    if name in ("SKILL.md", "CONSTITUTION.md", "ref/", "scripts/"):
        return name
    return "〈folder〉/" if name.endswith("/") else "〈file〉"


def parts_of(topic: Path, data: dict) -> tuple[list[str], bool]:
    """(the type's parts in order, whether it has a Draw button), read from the elements.md of the type the topic
    names; PARTS and no Draw when the topic names no type or the type has no elements.md."""
    named = str(data.get("check_type") or "")
    try:
        from host_paths import bootstrap
        bootstrap()
        from live.studio_types import elements_of
        els = elements_of(skills_views.SPACE / named) if named else []
    except ImportError:
        els = []
    if not els:
        return list(PARTS), False
    first = next(e["name"] for e in els if e["tab"] is None)
    return [first] + [e["name"] for e in els if e["view"] == first and e["tab"]], any(
        e["tab"] is None and e["name"] == "Draw" for e in els)


def lines_of(topic: Path) -> list[str]:
    """One line per part of the type: what the topic's views file shows, held against its skills' folders today."""
    try:
        data = json.loads((topic / "studio-views.json").read_text(encoding="utf-8"))
        # the managed Check button (ref/check-view.md) is no skill and is not held against the type's parts
        drawn = any(skills_views.is_draw(v) for v in data["views"])
        views = [v for v in data["views"] if not (v.get("name") == "Check" and data.get("check_type"))
                 and not skills_views.is_draw(v)]
    except (OSError, ValueError, KeyError, TypeError):
        return ["- ❗ 〈skill〉: no studio-views.json (run skills_views.py --skills)"]
    skills = skills_views.skills_of(topic)
    if not skills:
        return ["- ❗ 〈skill〉: a top button's first tab is not its SKILL.md"]
    shown = {Path(s).name: [i["name"] for i in v["items"]] for s, v in zip(skills, views)}
    owed = {Path(s).name: [i["name"] for i in skills_views.items_of(s)] for s in skills}
    names = [v["name"] for v in views]
    out = []
    if names == list(shown):
        out.append("- ✅ 〈skill〉 · " + ", ".join(names))
    else:
        out.append("- ❗ 〈skill〉: a top button is not named by its skill (" + ", ".join(n for n in names if n not in shown) + ")")
    parts, draw = parts_of(topic, data)
    for part in parts[1:]:
        if part not in PARTS:
            out.append(f"- ❗ {part}: the type lists it; skills_checklist.py cannot hold a topic against it yet")
            continue
        has = {k: [n for n in tabs if _part(n) == part] for k, tabs in shown.items()}
        due = {k: [n for n in tabs if _part(n) == part] for k, tabs in owed.items()}
        lacks = [f"{k} has {n} but shows no tab" for k in due for n in due[k] if n not in has[k]]
        extra = [f"{k} shows {n}, which it lacks" for k in has for n in has[k] if n not in due[k]]
        order = [f"{k}: its tabs are out of order" for k in shown if not lacks + extra and shown[k] != owed[k]]
        if lacks or extra:
            out.append(f"- ❗ {part}: " + "; ".join(lacks + extra))
        elif part == "SKILL.md":
            first = all(tabs[:1] == ["SKILL.md"] for tabs in shown.values())
            out.append("- ✅ SKILL.md · the first tab of every skill" if first and not order
                       else "- ❗ SKILL.md: " + "; ".join(order or ["not the first tab of every skill"]))
        elif not any(due.values()):
            out.append(f"- — {part}: {NONE[part]}")
        elif part in ("〈folder〉/", "〈file〉"):
            out.append(f"- ✅ {part} · " + ", ".join(dict.fromkeys(n for tabs in has.values() for n in tabs)))
        else:
            out.append(f"- ✅ {part} · " + ", ".join(k for k in has if has[k]))
    if draw:
        has_file = (topic / f"{topic.name}.excalidraw").is_file()
        out.append("- ✅ Draw · the topic's drawing" if drawn and has_file else
                   "- ❗ Draw: the topic has a drawing but shows no Draw button" if has_file else
                   "- ❗ Draw: a Draw button without the topic's drawing" if drawn else "- — Draw: the topic has no drawing")
    return out


def _is_heading(rows: list[str], i: int) -> bool:
    """A setext heading (words over dashes or equals) or an ATX one starts at row i."""
    under = rows[i + 1].strip() if i + 1 < len(rows) else ""
    line = rows[i]
    return bool(HEADING.match(line)) or bool(line.strip() and not line.lstrip().startswith(("-", "|", "*"))
                                             and re.fullmatch(r"-{3,}|={3,}", under))


def with_block(face_text: str, lines: list[str]) -> str:
    """The face with this script's lines at the top of its Checklist section; the section's other text stays. A
    Checklist section is made (before Decided) when the face has none."""
    rows = face_text.split("\n")
    owned = re.compile(MARK + r"(?:%s)(?: · |: |$)" % "|".join(
        re.escape(x) for x in {*PARTS, "Draw", *(ln[4:].split(" · ")[0].split(": ")[0] for ln in lines)}))
    start = next((i for i in range(len(rows)) if _is_heading(rows, i)
                  and rows[i].lstrip("# ").strip().casefold() == "checklist"), None)
    if start is None:
        section = ["Checklist", "---------", "", *lines, "", ""]
        at = next((i for i in range(len(rows)) if rows[i].strip() == "Decided" and _is_heading(rows, i)), None)
        if at is None:
            return face_text.rstrip("\n") + "\n\n\n" + "\n".join(section[:-2]) + "\n"
        return "\n".join(rows[:at] + section + rows[at:])
    body = start + (1 if HEADING.match(rows[start]) else 2)
    end = next((i for i in range(body, len(rows)) if _is_heading(rows, i)), len(rows))
    kept = [r for r in rows[body:end] if not owned.match(r) and not MARKER.match(r.strip())]
    while kept and not kept[0].strip():
        kept.pop(0)
    while kept and not kept[-1].strip():
        kept.pop()
    tail = [""] * (2 if end < len(rows) else 0)                      # two blank lines before the next heading
    return "\n".join(rows[:body] + ["", *lines, *([""] + kept if kept else []), *tail] + rows[end:]) + ("" if end < len(rows) or face_text.endswith("\n") is False else "\n")


def main(argv: list[str]) -> int:
    check = "--check" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 2
    bad = 0
    for topic in [t for p in paths for t in skills_views.topics_of((skills_views.SPACE / p).resolve())]:
        face = topic / f"{topic.name}.md"
        if not face.is_file():
            print(f"❗ {topic.name}: no face")
            bad += 1
            continue
        lines, text = lines_of(topic), face.read_text(encoding="utf-8")
        new = with_block(text, lines)
        gaps = [line for line in lines if line.startswith("- ❗")]
        if check:
            stale = new != text
            for line in gaps:
                print(f"❗ {topic.name} {line[4:]}")
            print(f"{'❗' if stale or gaps else '✅'} {topic.name}" + (": Checklist stale (run skills_checklist.py)" if stale else ""))
            bad += bool(stale or gaps)
        else:
            if new != text:
                face.write_text(new, encoding="utf-8")
            print(f"{'Wrote' if new != text else 'Up to date:'} {topic.name}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

"""One skill, measured from its own files: the Evaluation view of a Skill topic (hai-studio A13; the Skills type's
`## Evaluation`). A live page, so it is what the skill is today; nothing is written to disk.

    /_board/workbench?view=skill-eval&path=<skill folder>

Each criterion is one fold: its mark, its name, what was found, and inside the fold the lines it found. ✅ holds,
❗ does not, 🔶 holds with a caution, 🙋 a person or a fresh agent has to say. No score and no tally: a count of
passes reads as done and hides the one line that matters.
"""
from __future__ import annotations

import html
import importlib.util
import re
from pathlib import Path

LIMIT, AIM = 700, 600                       # AGENTS.md: a file a person reads stays under 700 lines, aim 600
SCRIPTS = Path(__file__).resolve().parents[4] / "skills/1_base/project/hai-studio/scripts"

CSS = """:root{--line:#e6e6e3;--muted:#6b6b66;--ink:#1d1d1b;--bg:#fff;--soft:#f4f4f2}
@media (prefers-color-scheme:dark){:root{--line:#3a3a37;--muted:#a3a39c;--ink:#ecece8;--bg:#1b1b19;--soft:#242422}}
body{margin:0;padding:14px 16px;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;max-width:820px}
h1{font-size:19px;margin:0 0 14px}details{border:1px solid var(--line);border-radius:8px;margin:0 0 8px}
summary{cursor:pointer;padding:8px 12px;display:grid;grid-template-columns:26px minmax(0,220px) minmax(0,1fr);gap:8px;align-items:baseline}
summary b{font-weight:600}summary span{color:var(--muted);font-size:13.5px;overflow-wrap:anywhere}
ul{margin:0;padding:8px 12px 10px 46px;border-top:1px solid var(--line)}li{margin:3px 0;font-size:13.5px;overflow-wrap:anywhere}
code{font-size:12.5px;background:var(--soft);padding:0 4px;border-radius:4px}
@media (max-width:520px){summary{grid-template-columns:26px minmax(0,1fr)}summary span{grid-column:2}}"""


def _text_check():
    spec = importlib.util.spec_from_file_location("skill_text_check", SCRIPTS / "skill_text_check.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _lines(path: Path) -> int:
    try:
        return len(path.read_text(encoding="utf-8", errors="ignore").splitlines())
    except OSError:
        return 0


def _front(text: str) -> dict:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    out = {}
    for line in (m.group(1) if m else "").splitlines():
        k = re.match(r'^\s*([\w-]+):\s*"?(.*?)"?\s*$', line)
        if k and k.group(2):
            out.setdefault(k.group(1), k.group(2))
    return out


def evaluate(skill: Path) -> list[tuple[str, str, str, list[str]]]:
    """[(mark, criterion, what was found, the lines found)] for one skill folder."""
    skill = Path(skill)
    main = skill / "SKILL.md"
    if not main.is_file():
        return [("❗", "SKILL.md", "the folder has no SKILL.md", [])]
    text = main.read_text(encoding="utf-8", errors="ignore")
    front, rows = _front(text), []

    named = front.get("name", "")
    said = front.get("description", "")
    gaps = ([f"name: is {named or 'missing'}, the folder is {skill.name}"] if named != skill.name else []) + \
        (["no description"] if not said else []) + \
        (["the description names no Trigger"] if said and "trigger" not in said.casefold() else [])
    rows.append(("❗" if gaps else "✅", "Found by its name", f"{len(said)} characters of description", gaps))

    n = _lines(main)
    rows.append(("❗" if n > LIMIT else "🔶" if n > AIM else "✅", "Read in one sitting",
                 f"SKILL.md is {n} lines", [f"over {LIMIT}: split it by responsibility"] if n > LIMIT else
                 [f"over the {AIM} aimed for"] if n > AIM else []))

    long = sorted(((_lines(p), p.relative_to(skill).as_posix()) for p in skill.rglob("*")
                   if p.is_file() and p.suffix in (".md", ".py") and p.name != "CHANGELOG.md"
                   and "__pycache__" not in p.parts and "GENERATED" not in p.read_text(encoding="utf-8", errors="ignore")[:600]),
                  reverse=True)
    over = [f"{name}: {k} lines" for k, name in long if k > LIMIT]
    rows.append(("❗" if over else "✅", "No file too long", f"longest: {long[0][1]}, {long[0][0]} lines" if long else "no file",
                 over))

    found = _text_check().problems(skill)[0]
    notes = [x[2:] for x in found if "who-and-when" in x or "marker comment" in x or "decision id" in x or "Studio Type" in x]
    lost = [x[2:] for x in found if "not on disk" in x]
    unnamed = [x[2:] for x in found if "never names" in x]
    rows.append(("❗" if notes else "✅", "States the rule only", "no who-and-when note, no marker line" if not notes
                 else "its text carries notes a reader does not need", notes))
    rows.append(("❗" if lost else "✅", "Names only what exists", "every ref and script it names is on disk" if not lost
                 else "it names files that are not there", lost))
    rows.append(("❗" if unnamed else "✅", "Nothing unreachable", "SKILL.md names every ref file and script" if not unnamed
                 else "files an agent reading SKILL.md never learns of", unnamed))

    scripts = sorted(p for folder in [skill / "scripts", *sorted(skill.glob("gallery/*/scripts"))] if folder.is_dir()
                     for p in folder.glob("*.py") if not p.name.startswith("_"))
    tests = "\n".join(p.read_text(encoding="utf-8", errors="ignore")
                      for folder in [skill / "tests", *sorted(skill.glob("gallery/*/tests"))] if folder.is_dir()
                      for p in folder.rglob("*.py"))
    bare = [p.name for p in scripts if not re.search(r"\b%s\b" % re.escape(p.stem), tests)]
    rows.append(("—", "Scripts are tested", "it has no scripts", []) if not scripts else
                ("❗" if len(bare) > len(scripts) / 2 else "🔶" if bare else "✅", "Scripts are tested",
                 "every script is named by a test" if not bare else "scripts no test names", bare))

    rules = skill / "CONSTITUTION.md"
    if rules.is_file():
        body = rules.read_text(encoding="utf-8", errors="ignore")
        arts = re.split(r"(?m)^## (A\d+ · .+)$", body)[1:]
        loose, open_ = [], []
        for title, part in zip(arts[::2], arts[1::2]):
            if "**Run:**" not in part and "**Check:**" not in part:
                loose.append(f"{title}: no Check or Run line")
            elif re.search(r"\*\*Status:\*\*\s*open", part):
                open_.append(title)
        rows.append(("❗" if loose else "🔶" if open_ else "✅", "Rules can be checked",
                     "every rule has a check" + (", some are still open" if open_ else ""), loose + open_))
    else:
        rows.append(("—", "Rules can be checked", "it has no CONSTITUTION.md", []))

    log = skill / "CHANGELOG.md"
    top = re.search(r"(?m)^## \[([^\]]+)\]", log.read_text(encoding="utf-8", errors="ignore")) if log.is_file() else None
    version = front.get("version", "")
    rows.append(("—", "Version is recorded", "it has no CHANGELOG.md", []) if not log.is_file() else
                ("✅" if top and top.group(1) == version else "❗", "Version is recorded",
                 f"SKILL.md says {version or 'no version'}; the change log's newest entry is {top.group(1) if top else 'none'}", []))

    rows.append(("🙋", "A fresh agent can use it", "not measured here: give the skill and one real task to an agent "
                 "that has seen nothing else, and read what it does", []))
    return rows


def document(skill: Path, root: Path) -> str:
    """The Evaluation page of one skill, or '' when the folder is no skill inside the SPACE."""
    skill, root = Path(skill).resolve(), Path(root).resolve()
    if not skill.is_relative_to(root) or not (skill / "SKILL.md").is_file():
        return ""
    e = html.escape
    code = lambda s: re.sub(r"`([^`]+)`", r"<code>\1</code>", e(s))    # noqa: E731
    folds = "".join(
        f'<details{" open" if mark == "❗" else ""}><summary><i>{mark}</i><b>{e(name)}</b><span>{code(said)}</span></summary>'
        + (("<ul>" + "".join(f"<li>{code(x)}</li>" for x in lines) + "</ul>") if lines else "") + "</details>"
        for mark, name, said, lines in evaluate(skill))
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,'
            f'initial-scale=1"><title>{e(skill.name)} · Evaluation</title><style>{CSS}</style></head>'
            f'<body><h1>{e(skill.name)}</h1>{folds}</body></html>\n')

"""The Skills section of the right rail: the skills that work on this page, most relevant first (JL 261105: "we can also
add a new tab in the right rail, named 'SKILL', and we can show the most relevent skills").

A page's skills, in this order, each once:
  1. its theme's door and workbench skill (`skills/2_theme/<theme>/haipipe-<theme>`, `workbench-<theme>`);
  2. its level's skill (haipipe-block, haipipe-job, haipipe-task; a draft Task adds haipipe-draft);
  3. the skills its views name (`view_skills`, the Process steps' "who does it" that this section replaces);
  4. the skills its own Runs name (`skill:` in each run.yaml at this page or below), most used first;
  5. the helpers of its sections: haipipe-studio (topics), haipipe-interaction, haipipe-delivery.
Each shows as a side tab: its name and why it is here on the left; on the right what it does (its description's first
sentence), its version, its SKILL.md, and a Copy prompt that calls it on this folder.
"""
from __future__ import annotations

import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

import yaml

from live import frame
from live.ui_parts import PB_CSS, PB_JS, _side_tabs, prompt_box

SKILLS = Path(__file__).resolve().parents[1].parent / "skills"     # servers/workbench -> plugins/haipipe-toolkit/skills
LEVEL_SKILL = {"Project": "haipipe-project", "Block": "haipipe-block", "Job": "haipipe-job", "Task": "haipipe-task"}
MOST = 10                                                           # the most relevant only; the rest stay in /skills


@lru_cache(maxsize=1)
def catalog() -> dict:
    """{skill name: (first sentence of its description, version, SKILL.md path)} of every skill under skills/."""
    out = {}
    for md in sorted(SKILLS.rglob("SKILL.md")):
        if any(p.startswith(("_", ".")) or p == "node_modules" for p in md.relative_to(SKILLS).parts):
            continue
        text = md.read_text(encoding="utf-8", errors="ignore")
        m = re.match(r"---\n(.*?)\n---", text, re.S)
        try:
            head = yaml.safe_load(m.group(1)) if m else {}
        except yaml.YAMLError:
            head = {}
        head = head if isinstance(head, dict) else {}
        name = str(head.get("name") or md.parent.name)
        desc = re.sub(r"\s+", " ", str(head.get("description") or "")).strip()
        first = re.split(r"(?<=[.!?])\s+(?=[A-Z])|\bTrigger:", desc, maxsplit=1)[0].strip()
        version = str((head.get("metadata") or {}).get("version") or head.get("version") or "")
        out.setdefault(name, (first, version, md))
    return out


def run_skills(folder: Path) -> list:
    """The skills this page's Runs name (`skill:` in run.yaml), most used first."""
    used = Counter()
    for card in Path(folder).glob("**/runs/*/run.yaml"):
        if any(p.startswith(("_", ".")) for p in card.relative_to(folder).parts):
            continue
        m = re.search(r"(?m)^skill:\s*['\"]?([A-Za-z0-9_-]+)", card.read_text(encoding="utf-8", errors="ignore"))
        if m:
            used[m.group(1)] += 1
    return [s for s, _ in used.most_common()]


def relevant(folder: Path, theme: str, level: str, view_skills=(), draft: bool = False, topics: bool = False,
             inbox: bool = False) -> list:
    """[(skill name, why it is here)] of the skills that exist, each once, most relevant first, at most MOST."""
    have = catalog()
    rows = [(f"haipipe-{theme}", "this theme"), (f"workbench-{theme}", "this theme's page")]
    rows += [(LEVEL_SKILL.get(level, ""), f"this {level}")]
    rows += [("haipipe-draft", "this draft")] if draft else []
    rows += [(s, "its views") for s in view_skills]
    rows += [(s, "its Runs") for s in run_skills(folder)]
    rows += [("haipipe-studio", "its Studio")] if topics else []
    rows += [("haipipe-interaction", "its Interaction")] if inbox else []
    rows += [("haipipe-delivery", "its Delivery")]
    seen, out = set(), []
    for name, why in rows:
        if name and name in have and name not in seen:
            seen.add(name)
            out.append((name, why))
    return out[:MOST]


def skills_html(folder: Path, root: Path, theme: str, level: str, view_skills=(), draft: bool = False,
                topics: bool = False, inbox: bool = False) -> str:
    """The Skills section's one view: a side tab per skill, its use on the right."""
    rows = relevant(folder, theme, level, view_skills, draft, topics, inbox)
    if not rows:
        return '<p class="mut">No skill found for this page.</p>'
    here = frame.rel(folder, root) if hasattr(frame, "rel") else str(folder)
    tabs, panels = [], []
    for name, why in rows:
        first, version, md = catalog()[name]
        link = frame.pop(frame.reader(md, root), f"{name} · SKILL.md", "Open SKILL.md ↗") if Path(md).resolve().is_relative_to(Path(root).resolve()) else ""
        tabs.append((f"/{name}", why))
        panels.append(f'<div class=sk-h><b>/{frame.esc(name)}</b>'
                      + (f'<span class=sk-v>version {frame.esc(version)}</span>' if version else '')
                      + (f'<span class=sk-open>{link}</span>' if link else '') + '</div>'
                      + (f'<p class=sk-a>{frame.esc(first)}</p>' if first else '')
                      + prompt_box(f"/{name} {here} ", key=f"skill:{name}:{here}"))
    return PB_CSS + SK_CSS + _side_tabs("fKx", tabs, panels) + PB_JS


SK_CSS = ("<style>.sk-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 12px;margin:0 0 6px}"
          ".sk-h b{font-size:15px}.sk-v{font-size:12px;color:var(--muted)}.sk-open{margin-left:auto;font-size:13px}"
          ".sk-a{margin:0 0 10px;line-height:1.5}</style>")

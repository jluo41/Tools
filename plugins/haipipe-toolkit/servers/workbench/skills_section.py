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
             inbox: bool = False, limit=MOST) -> list:
    """[(skill name, why it is here)] of the skills that exist, each once, most relevant first; limit=None keeps the full rail scope."""
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
    return out if limit is None else out[:limit]


SKIP_PARTS = ("__pycache__", "node_modules")
SKIP_NAMES = ("CACHEDIR.TAG",)


def skill_files(md: Path, root: Path) -> list:
    """Every file a skill folder holds, SKILL.md first, then its own top-level files, then its folders' files by path;
    hidden folders, caches and anything outside the served root are left out."""
    home = Path(md).parent
    found = [p for p in home.rglob("*") if p.is_file() and p.name not in SKIP_NAMES
             and not any(part.startswith(".") or part in SKIP_PARTS for part in p.relative_to(home).parts)
             and Path(p).resolve().is_relative_to(Path(root).resolve())]
    return sorted(found, key=lambda p: (p.name != "SKILL.md", len(p.relative_to(home).parts) > 1, p.relative_to(home).as_posix()))


def files_bar(md: Path, root: Path) -> str:
    """A button per file above the reading frame; the first, SKILL.md, is open. One file needs no bar."""
    files = skill_files(md, root)
    if len(files) < 2:
        return ""
    home = Path(md).parent
    return ('<div class=sk-files>' + "".join(
        f'<button type=button class="sk-file{" on" if k == 0 else ""}" data-src="{frame.esc(frame._file_url(p, root))}">'
        f'{frame.esc(p.relative_to(home).as_posix())}</button>' for k, p in enumerate(files)) + '</div>')


def skills_html(folder: Path, root: Path, theme: str, level: str, view_skills=(), draft: bool = False,
                topics: bool = False, inbox: bool = False, rows=None) -> str:
    """The Skills section's one view: a side tab per skill, its use on the right."""
    rows = relevant(folder, theme, level, view_skills, draft, topics, inbox) if rows is None else rows
    if not rows:
        return '<p class="mut">No skill found for this page.</p>'
    here = frame.rel(folder, root) if hasattr(frame, "rel") else str(folder)
    tabs, panels = [], []
    for name, why in rows:
        first, version, md = catalog()[name]
        readable = Path(md).resolve().is_relative_to(Path(root).resolve())
        link = frame.pop(frame.reader(md, root), f"{name} · SKILL.md", "Open SKILL.md ↗") if readable else ""
        # its whole SKILL.md, read in place; the frame loads only once its tab shows in an open section
        read = (f'<iframe class=sk-read title="{frame.esc(name)} · SKILL.md" loading=lazy '
                f'data-src="{frame.esc(frame.reader(md, root))}"></iframe>') if readable else ""
        tabs.append((f"/{name}", why))
        panels.append(f'<div class=sk-h><b>/{frame.esc(name)}</b>'
                      + (f'<span class=sk-v>version {frame.esc(version)}</span>' if version else '')
                      + (f'<span class=sk-open>{link}</span>' if link else '') + '</div>'
                      + (f'<p class=sk-a>{frame.esc(first)}</p>' if first else '')
                      + prompt_box(f"/{name} {here} ", key=f"skill:{name}:{here}")
                      + (files_bar(Path(md), root) if readable else "") + read)
    return PB_CSS + SK_CSS + _side_tabs("fKx", tabs, panels) + PB_JS + SK_JS


SK_CSS = ("<style>.sk-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 12px;margin:0 0 6px}"
          ".sk-h b{font-size:15px}.sk-v{font-size:12px;color:var(--muted)}.sk-open{margin-left:auto;font-size:13px}"
          ".sk-a{margin:0 0 10px;line-height:1.5}"
          ".sk-read{display:block;width:100%;height:560px;margin:12px 0 0;border:1px solid var(--line);border-radius:8px;"
          "background:var(--paper)}@media(max-width:600px){.sk-read{height:440px}}"
          ".sk-files{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0 0}.sk-file{font:12.5px ui-monospace,SFMono-Regular,Menlo,monospace;"
          "padding:3px 9px;border:1px solid var(--line);border-radius:6px;background:var(--paper);color:var(--ink);cursor:pointer}"
          ".sk-file:hover{border-color:var(--accent)}.sk-file.on{border-color:var(--accent);color:var(--accent);background:var(--pb-soft,#e7f5ff)}</style>")

# a SKILL.md frame takes its src only when it can be seen: its panel shown and every fold around it open
SK_JS = ("<script>(function(){if(window.skRead)return;window.skRead=1;"
         "function seen(f){for(var e=f;e;e=e.parentElement){if(e.hidden||(e.tagName==='DETAILS'&&!e.open&&!f.closest('summary')))return false;}return true;}"
         "function load(){document.querySelectorAll('iframe.sk-read[data-src]:not([src])').forEach(function(f){"
         "if(seen(f))f.src=f.dataset.src;});}"
         "document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.sk-file');if(b){"
         "var f=b.parentNode.nextElementSibling;b.parentNode.querySelectorAll('.sk-file').forEach(function(x){x.classList.toggle('on',x===b);});"
         "if(f&&f.classList.contains('sk-read')){f.dataset.src=b.dataset.src;f.src=b.dataset.src;f.title=b.textContent;}return;}"
         "setTimeout(load,30);});"
         "document.addEventListener('toggle',function(){setTimeout(load,30);},true);"
         "if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',load);else load();})();</script>")

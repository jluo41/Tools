"""SPACE Home > 📜 Constitution: every rule feedback made, read from each skill's CONSTITUTION.md (hai-stack).

One row per article: its mark (✅ solved, 🔶 open), its rule as the name, the skill that owns it; the name opens the
article's report (`constitution/A<NN>-<slug>.md`: Need, Now, Gap, Methods, Update, Never again), or the
CONSTITUTION.md itself while the report is missing. The skills live in Tools (`plugins/*/skills/`, or
`Tools/plugins/*/skills/` inside another SPACE), so every SPACE's Home shows the same rules. Not shown when no skill
has a constitution. Reads only fixed depths and caches by (mtime, size), as frame_sessions does.
"""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlencode

from live import frame

GLOBS = ("plugins/*/skills/**/CONSTITUTION.md", "Tools/plugins/*/skills/**/CONSTITUTION.md")
SKIP = {"_old", ".trash", "node_modules", "references"}
_CACHE: dict = {}

CSS = """<style>
.cn-list{list-style:none;margin:0;padding:0;display:grid;gap:6px}
.cn-list li{display:flex;flex-wrap:wrap;gap:4px 10px;align-items:baseline;padding:8px 12px;border:1px solid var(--line);
  border-radius:var(--radius-surface,8px);background:var(--card)}
.cn-list li:hover{border-color:var(--accent)}
.cn-list a{font-weight:600;color:var(--fg);text-decoration:none}.cn-list a:hover{color:var(--accent)}
.cn-skill{color:var(--mut);font:12px/1.5 ui-monospace,Menlo,monospace}
.cn-words{flex-basis:100%;color:var(--mut);font-size:13px;font-style:italic}
</style>"""


def articles(path: Path) -> list:
    """[(head, solved, report path or None, JL's words)] for one CONSTITUTION.md, cached by (mtime, size)."""
    st = path.stat()
    sig = (st.st_mtime_ns, st.st_size)
    hit = _CACHE.get(path)
    if hit and hit[0] == sig:
        return hit[1]
    out = []
    for art in re.split(r"(?m)^## (?=A\d+)", path.read_text(encoding="utf-8"))[1:]:
        head = art.splitlines()[0].strip()
        status = re.search(r"(?m)^\*\*Status:\*\*\s*(\S+)", art)
        rep = re.search(r"(?m)^\*\*Report:\*\*\s*`?([^`\s]+)", art)
        words = re.search(r'(?m)^> "(.+?)"', art)
        report = path.parent / rep[1] if rep else None
        report = report if report and report.is_file() else None          # solved needs its report (hai-stack step 11)
        out.append((head, bool(status and status[1] == "solved" and report), report,
                    words[1] if words else ""))
    _CACHE[path] = (sig, out)
    return out


def files(root: Path) -> list:
    return sorted({p for g in GLOBS for p in root.glob(g) if not SKIP & set(p.relative_to(root).parts)})


def _href(path: Path, root: Path) -> str:
    """The reader link; through a SPACE's Tools/ symlink the path is kept as the SPACE sees it, not resolved."""
    try:
        return frame._file_url(path, root)
    except ValueError:
        return "/_board/page?" + urlencode({"path": "/" + path.relative_to(root).as_posix()})


def constitution_html(root: Path) -> str:
    """The section body; a file that cannot be read is left out, so Home never fails on it."""
    try:
        return _html(root)
    except Exception:  # noqa: BLE001  (Home must load even if one constitution is broken)
        return ""


def _html(root: Path) -> str:
    items = []
    for path in files(root):
        for head, solved, report, words in articles(path):
            href = _href(report or path, root)
            items.append(f'<li><span>{"✅" if solved else "🔶"}</span><a href="{frame.esc(href)}" target=_blank '
                         f'rel=noopener>{frame.esc(head)}</a><span class="cn-skill">{frame.esc(path.parent.name)}</span>'
                         + (f'<span class="cn-words">“{frame.esc(words)}”</span>' if words else "") + "</li>")
    return CSS + f'<ul class="cn-list">{"".join(items)}</ul>' if items else ""

"""Studio > Sessions: the episodes that changed a Block, each joined to the folders it touched (ref/three-views.md).

An episode is a pass (`passes/pNN-<MMDD>/pass.md` of a Run, a Studio topic's `passes/pNN-<MMDD>/`) or one
`## Pass` of a Paper Section's `draft/records/<stem>-revise.md`. They are read where they are, at fixed depths
(never a recursive walk: a Block's results/ and data/ hold thousands of files), and each file is parsed once per
version of it. The Folder part puts a 🧵 on each row an episode touched; a click shows those episodes here.
"""

from __future__ import annotations

import datetime
import re
from pathlib import Path

import yaml

from live.frame_base import _e, _file_url, _reader, _rel, pop

# where episodes live, relative to a Block: its own level, a Job, a Task (a Job's and a Task's Runs and topics)
PASS_DIRS = ("runs/*/passes/p[0-9]*", "*/runs/*/passes/p[0-9]*", "*/*/runs/*/passes/p[0-9]*",
             "s[0-9]*-*/passes/p[0-9]*", "*/s[0-9]*-*/passes/p[0-9]*")
REVISE_FILES = ("*/draft/records/*-revise.md", "*/*/draft/records/*-revise.md")
RECORD_NAMES = ("pass.md", "digest.md")      # what a pass shows; a transcript is never linked from the page
_PASS = re.compile(r"^p(\d+)-(\d{2})(\d{2})$")
_DAY = re.compile(r"(?<!\d)(20\d{2}-\d{2}-\d{2}|2[4-9](?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01]))(?!\d)")
_TICKS = re.compile(r"`([^`\s]+)`")
_PARSED: dict = {}                  # record path -> (its signature, its episodes): one entry per file
_TOUCHED: dict = {}                 # Block -> (the signature of all its records, the touched set)
SPACE_MARKS = ("env.sh", ".server_config")      # what marks a SPACE root (wb.py space_root)


def space_of(folder: Path) -> Path | None:
    """The SPACE root above a folder: the nearest one holding env.sh or .server_config."""
    for p in [folder, *folder.parents]:
        if any((p / m).is_file() for m in SPACE_MARKS):
            return p
    return None


def _split(text: str) -> tuple[dict, str]:
    if text.startswith("---\n"):
        head, sep, body = text[4:].partition("\n---")
        if sep:
            try:
                meta = yaml.safe_load(head) or {}
                return (meta if isinstance(meta, dict) else {}), body.lstrip("\n")
            except yaml.YAMLError:
                pass
    return {}, text


def _iso(raw: str) -> str:
    return raw if "-" in raw else f"20{raw[:2]}-{raw[2:4]}-{raw[4:6]}"


def _changed(body: str) -> list:
    """The paths listed under `## Changed`, as written (an older pass names them in backticks there)."""
    m = re.search(r"(?ms)^## Changed\s*$(.*?)(?=^## |\Z)", body)
    return _TICKS.findall(m.group(1)) if m else []


def _title(body: str, fallback: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    first = next((l.strip() for l in body.splitlines() if l.strip() and not l.startswith("#")), "")
    return (first[:117].rsplit(" ", 1)[0] + " …") if len(first) > 120 else (first or fallback)


def _pass_day(pdir: Path, record: Path, meta: dict) -> str:
    if meta.get("date"):
        return str(meta["date"])
    m = _PASS.match(pdir.name)
    if not m:
        return ""
    when = datetime.date.fromtimestamp(record.stat().st_mtime)     # the year is not in the folder name
    year = when.year - (1 if (int(m.group(2)), int(m.group(3))) > (when.month, when.day) else 0)
    return f"{year}-{m.group(2)}-{m.group(3)}"


def _record(pdir: Path) -> Path | None:
    """The file a pass shows: pass.md, else digest.md, else its first other Markdown; never a transcript."""
    found = next((pdir / n for n in RECORD_NAMES if (pdir / n).is_file()), None) \
        or next((m for m in sorted(pdir.glob("*.md")) if m.name != "transcript.md"), None)
    return found


def _read_pass(record: Path) -> list:
    pdir = record.parent
    meta, body = _split(record.read_text(encoding="utf-8", errors="ignore"))
    owner = pdir.parent.parent                  # the Run, or the Studio topic
    return [{"day": _pass_day(pdir, record, meta), "goal": str(meta.get("goal") or _title(body, owner.name)),
             "record": record, "owner": owner, "session": meta.get("session") or "",
             "paths": [str(p) for p in meta.get("paths") or _changed(body)], "cards": list(meta.get("cards") or [])}]


def _read_revise(md: Path) -> list:
    """One episode per `## Pass` heading of a Paper Section's revise record; its day is in the heading."""
    text = md.read_text(encoding="utf-8", errors="ignore")
    task = md.parent.parent.parent              # tNN_<section>/draft/records/<stem>-revise.md
    out = []
    for m in re.finditer(r"(?m)^## (Pass\b.*)$", text):
        day = _DAY.search(m.group(1))
        bits = [b.strip() for b in m.group(1).split("·")]          # the date (and a time after it) is the row's day
        words = " · ".join(b for b in bits if b and not re.fullmatch(r"(20\d{2}-\d{2}-\d{2}|\d{6})(\s+\d{4})?", b))
        out.append({"day": _iso(day.group(1)) if day else "", "goal": words, "record": md, "owner": task,
                    "session": "", "paths": [_rel_to_space(md.parent.parent, md)], "cards": []})
    return out


def _rel_to_space(folder: Path, anchor: Path) -> str:
    top = space_of(anchor)
    try:
        return folder.resolve().relative_to(top.resolve()).as_posix() if top else folder.as_posix()
    except ValueError:
        return folder.as_posix()


def _cached(path: Path, reader, sigs: list) -> list:
    """The episodes of one record file, read again only when its (mtime, size) changes; `sigs` collects them."""
    try:
        st = path.stat()
    except OSError:
        return []
    sig = (st.st_mtime_ns, st.st_size)
    sigs.append((str(path), sig))
    old = _PARSED.get(str(path))
    if old is None or old[0] != sig:
        try:
            old = (sig, reader(path))
        except (OSError, UnicodeError):
            old = (sig, [])
        _PARSED[str(path)] = old
    return old[1]


def _episodes(block: Path) -> tuple[list, tuple]:
    out, sigs = [], []
    for pattern in PASS_DIRS:
        for pdir in block.glob(pattern):
            record = _record(pdir) if pdir.is_dir() else None
            if record:
                out.extend(_cached(record, _read_pass, sigs))
    for pattern in REVISE_FILES:
        for md in block.glob(pattern):
            out.extend(_cached(md, _read_revise, sigs))
    return sorted(out, key=lambda e: (e["day"], str(e["record"])), reverse=True), tuple(sorted(sigs))


def episodes(block: Path) -> list:
    """Every episode of a Block, newest first. Each: day, goal, record (the file to open), owner (the Run, topic
    or Task that holds it), session, paths (as written: SPACE-relative, or relative to its Block or owner in an
    older pass) and cards."""
    return _episodes(block)[0]


def touched(episode: dict, block: Path) -> list:
    """The real paths an episode touched, resolved: SPACE-relative first, then from its Block, then its owner."""
    top = space_of(block)
    found = []
    for raw in episode["paths"]:
        for base in [b for b in (top, block, episode["owner"]) if b]:
            p = (base / raw)
            if p.exists():
                found.append(p.resolve())
                break
    return found


def touched_set(block: Path) -> set:
    """Every folder and file an episode of this Block touched, with the folders above it up to the Block."""
    block = block.resolve()
    eps, sig = _episodes(block)
    kept = _TOUCHED.get(block)
    if kept and kept[0] == sig:                 # a lazy folder expand asks again: nothing changed, same set
        return kept[1]
    seen = set()
    for e in eps:
        for p in touched(e, block) + [e["owner"].resolve()]:
            while p.is_relative_to(block) and p not in seen:
                seen.add(p)
                p = p.parent
    _TOUCHED[block] = (sig, seen)
    return seen


def _day(day: str) -> str:
    try:
        d = datetime.date.fromisoformat(day)
    except ValueError:
        return day
    return d.strftime("%d %b" if d.year == datetime.date.today().year else "%d %b %Y")


def sessions_part(block: Path, root: Path, under: Path | None = None) -> str:
    """The Studio's seventh folding part, Sessions, under Folder: the Block's episodes grouped by the folder that
    holds them, the newest group first. A row is its day, its goal (opens the record) and what it touched. With
    `under` (a Job or Task page), only the episodes held there or touching something there."""
    block = block.resolve()
    under = under.resolve() if under else None
    groups: dict = {}
    for e in episodes(block):
        if under and under != block and not any(p.is_relative_to(under)
                                                 for p in touched(e, block) + [e["owner"].resolve()]):
            continue
        holder = e["owner"].parent.parent if e["owner"].parent.name == "runs" else e["owner"]
        groups.setdefault(holder, []).append(e)
    if not groups:
        return ""                               # a part with nothing in it is not shown
    parts = []
    for where, items in groups.items():
        rows = []
        for e in items:
            paths = touched(e, block)
            data = "|".join(_rel(p, root) for p in paths + [e["owner"].resolve()] if p.is_relative_to(root.resolve()))
            chips = "".join(f'<span class=ss-touch>{pop(_file_url(p, root), p.name)}</span>'
                            for p in paths if p.is_file() and p.is_relative_to(root.resolve()))
            rows.append(f'<li class=ss-row data-paths="{_e(data)}"><span class=ss-day>{_e(_day(e["day"]))}</span>'
                        f'{pop(_reader(e["record"], root), e["goal"])}{chips}</li>')
        name = _rel(where, block) if where != block else block.name
        parts.append(f'<section class=ss-group><h4 class=ss-where>{_e(name)}/</h4><ul class=ss-list>{"".join(rows)}</ul></section>')
    return (f'<details class="studio-related studio-sessions" id=studio-sessions><summary><b>Sessions</b></summary>'
            f'<div class=related-in>{"".join(parts)}</div></details>{SESSIONS_ASSETS}')


SESSIONS_ASSETS = """<style>
.studio-sessions .ss-where{margin:12px 0 4px;font:600 13px/1.3 ui-monospace,monospace;color:var(--mut,#667)}
.studio-sessions .ss-list{list-style:none;margin:0;padding:0}
.studio-sessions .ss-row{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:baseline;padding:3px 0}
.studio-sessions .ss-day{min-width:52px;color:var(--mut,#667);font-variant-numeric:tabular-nums}
.studio-sessions .ss-touch{font-size:12px;opacity:.8}
.studio-sessions.ss-only .ss-row:not(.ss-hit){display:none}
.studio-sessions.ss-only .ss-group:not(.ss-has){display:none}
.studio-sessions .ss-clear{margin-left:8px}
.fd-th{border:0;background:none;cursor:pointer;padding:0 4px}
</style><script>
(function(){if(window.__ssBound)return;window.__ssBound=1;
document.addEventListener('click',function(ev){var b=ev.target.closest('.fd-th');if(!b)return;ev.preventDefault();ev.stopPropagation();
var box=document.getElementById('studio-sessions');if(!box)return;var path=b.dataset.th;box.open=true;box.classList.add('ss-only');
box.querySelectorAll('.ss-row').forEach(function(r){var hit=(r.dataset.paths||'').split('|').some(function(p){return p===path||p.indexOf(path+'/')===0;});r.classList.toggle('ss-hit',hit);});
box.querySelectorAll('.ss-group').forEach(function(g){g.classList.toggle('ss-has',!!g.querySelector('.ss-hit'));});
var s=box.querySelector('summary');if(!box.querySelector('.ss-clear')){var c=document.createElement('button');c.type='button';c.className='ss-clear';c.textContent='×';
c.onclick=function(e){e.preventDefault();box.classList.remove('ss-only');c.remove();};s.appendChild(c);}
box.scrollIntoView({block:'start',behavior:'smooth'});},true);})();
</script>"""

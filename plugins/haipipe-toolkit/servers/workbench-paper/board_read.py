"""Reading a paper Board (b16 s32, s33): its parts (the sNN topics), their faces, sections and tables, its Jobs and
Tasks by name, and the folders its pages name. Pure readers; nothing here draws a page."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live import draft_steps as ds
from live.frame import esc
from live.ui_parts import _plain
from live.focus_draft import WORK, _facts, word


# ── a paper Board's Report: the paper's own parts, one view each (JL 261031: "for the report, I think we should have
# the things like the idea, the story, the venue, and the data flow, and the paper flow, etc.") ─────────────────────
# the paper pages' view captions (the Board's, a version's), apart from the draft Task's focus_draft.CAPTIONS, which
# they used to overwrite (an "evidence" key is a Board view and a draft step); focus_page.paper_look merges the two
PAPER_CAPTIONS: dict = {}

# Each part is read from the Board's topics by its role, so every paper Board shows its own: Idea (s01-ideation),
# Story (board.md `story-current:`; the venues and their related work sit inside it, b16 s32-D12), Data flow and
# Paper flow (haipipe-paper-plan's s03 and s04). "venue" stays in the list for its key only; no view is drawn for it.
# A part is not a view: Data flow and Paper flow are one view, Data + Paper Plan (JL 261104); Idea and Story each have their
# own button (JL 261105: "I mean seperate this!!!", on the Idea + Story button; BOARD_VIEWS).
BOARD_PARTS = (("idea", "Idea", r"s\d+-idea"), ("story", "Story", r"s\d+-story"), ("venue", "Venue", ""),
               ("dataflow", "Data flow", r"s\d+-(?:paper-)?data-?flow"),
               ("paperflow", "Paper flow", r"s\d+-paper-(?:work|paper-)?flow"))


# (view key, its button, the parts it shows, in order)
BOARD_VIEWS = (("idea", "Idea", ("idea",)), ("story", "Story", ("story",)), ("plan", "Data + Paper Plan", ("dataflow", "paperflow")))
VIEW_PARTS = {key: parts for key, _, parts in BOARD_VIEWS}


def view_topics(board: Path, key: str) -> list:
    """[(part key, part name, topic)] of the view's parts this Board has, in reading order."""
    named = {k: (name, pat) for k, name, pat in BOARD_PARTS}
    found = [(k, named[k][0], board_topic(board, k, named[k][1])) for k in VIEW_PARTS.get(key, ())]
    return [x for x in found if x[2] is not None]


RELATED = r"s\d+-related-work"     # the venue's own papers, one sNN (JL 261031): shown inside Venue, never a view of its own


SKIP_PARTS = {"files", "log", "opening", "writing style", "the drawing's words", "law"}


def _field(text: str, name: str) -> str:
    m = re.search(rf"(?mi)^\**{name}(?![\w-]):?\**:?\s*(.+?)\s*$", text)     # `venue` never matches `venue-page`
    return m.group(1).strip().strip("`") if m else ""


def board_topic(board: Path, role: str, pattern: str) -> Path | None:
    """The Board's topic for one part: the Story by board.md's `story-current:`, the others by their slug."""
    if role == "story":
        md = board / "board.md"
        named = _field(md.read_text(encoding="utf-8", errors="ignore"), "story-current") if md.is_file() else ""
        if named and (board / named).is_dir():
            return board / named
    hits = sorted(d for d in board.glob("s[0-9]*-*") if d.is_dir() and re.match(pattern, d.name))
    return hits[0] if hits else None


def face_sections(text: str) -> list:
    """[(heading, body)] of a face: its `##`/`###` and setext parts, the header block and the bookkeeping left out."""
    out, name, lines, fence = [], None, [], False
    rows = text.splitlines()
    for i, line in enumerate(rows):
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
        nxt = rows[i + 1] if i + 1 < len(rows) else ""
        atx = None if fence else re.match(r"^#{2,3}\s+(.+?)\s*#*$", line)
        setext = not fence and line.strip() and re.match(r"^(=+|-+)\s*$", nxt) and not line.startswith(("-", "|"))
        if atx or setext:
            if name is not None:
                out.append((name, "\n".join(lines).strip()))
            name, lines = (atx.group(1) if atx else line.strip()), []
            continue
        if re.match(r"^(=+|-+)\s*$", line) and not fence and i and rows[i - 1].strip() == (name or ""):
            continue
        if name is not None:
            lines.append(line)
    if name is not None:
        out.append((name, "\n".join(lines).strip()))
    return [(n, b) for n, b in out if b and re.sub(r"^\d+\s*·\s*", "", n).strip().lower() not in SKIP_PARTS]


def _label_rows(body: str):
    """(rows html, the body without that block): the first ```text block of aligned `<emoji> LABEL   value` lines
    as label/value rows (A r03: on a phone the fixed-width block broke its indents), drawn outside the Markdown,
    which escapes HTML; other blocks stay in the body."""
    found = []

    def conv(m):
        if found:
            return m.group(0)
        rows = []
        for ln in m.group(1).splitlines():
            hit = re.match(r"^(\S+\s+[A-Z]{3,}(?: [A-Z]{3,})?)\s+([^A-Z\s].*|[A-Z][a-z].*)$", ln)
            if hit:
                rows.append([hit.group(1).strip(), hit.group(2).strip()])
            elif rows and ln.strip():
                rows[-1][1] += " " + ln.strip()
            elif ln.strip():
                return m.group(0)
        if not rows:
            return m.group(0)
        found.append("<dl class=pb-kv>" + "".join(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in rows) + "</dl>")
        return ""
    rest = re.sub(r"```text\n(.*?)\n```", conv, body, flags=re.S)
    return (found[0] if found else ""), rest


def _undated(text: str) -> str:
    text = re.sub(r"\s+\d{6}\b", "", text).strip()
    return re.sub(r"^[✕×]\s*(?=(fallback|second|considered)\b)", "○ ", text)


def _table(body: str) -> list:
    """The first Markdown table in `body` as a list of row dicts keyed by its header (lower case)."""
    rows = [r for r in body.splitlines() if r.strip().startswith("|")]
    if len(rows) < 3:
        return []
    cells = lambda r: [c.strip() for c in r.strip().strip("|").split("|")]
    head = [h.lower() for h in cells(rows[0])]
    return [dict(zip(head, cells(r))) for r in rows[2:]]


def _after_table(body: str) -> str:
    lines, seen = body.splitlines(), False
    for i, r in enumerate(lines):
        if r.strip().startswith("|"):
            seen = True
        elif seen and r.strip():
            return "\n".join(lines[i:])
    return ""


def _open_link(link: str, topic: Path, root: Path) -> str:
    """A Markdown link `[name](path)` from a face, as an Open button that opens the page in the pop-out."""
    m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", link or "")
    if not m:
        return ""
    target = (topic / m.group(2)).resolve()
    if not target.is_file():
        return esc(m.group(1))
    return (f'<a class=fd-btn data-pop="{esc(m.group(1))}" href="/_board/page?path={quote("/" + ds._rel(target, root))}">'
            f'Open: {esc(m.group(1))}</a>')


def _face(topic: Path):
    from live import frame
    f = frame._notes(topic)
    text = f.read_text(encoding="utf-8", errors="ignore") if f else ""
    parts = {re.sub(r"^\d+\s*·\s*", "", n).strip().lower(): b for n, b in face_sections(text)}
    return text, parts


def _lead_sentence(body: str):
    """(the main point, the rest): the first plain paragraph (a `**Label**: definition` line, code and a glossary line, "GLP-1 = ...", skipped)."""
    paras = re.split(r"\n\s*\n", body.strip())
    for i, para in enumerate(paras):
        t = para.strip()
        if t and not t.startswith(("**", "```", "|", "-", "#")) and not re.match(r"[^\s=]+ = ", t):
            return re.sub(r"^In plain words:\s*", "", _plain(t)), "\n\n".join(paras[:i] + paras[i + 1:])
    return "", body


def _rq_lists(body: str):
    """([(n, question)], {n: narrative}): each list item keeps its own number, so a story that starts at 0 (RQ0, a
    setup question, haipipe-paper-story) labels and pairs by that number, never by position."""
    def items_after(label):
        m = re.search(rf"\*\*{label}[^*]*\*\*:?\s*\n((?:\s*\d+\.\s.+\n?)+)", body)
        return [(int(g.group(1)), g.group(2).strip()) for x in m.group(1).strip().splitlines()
                if (g := re.match(r"\s*(\d+)\.\s*(.*)", x))] if m else []
    return items_after("The story, question by question"), dict(items_after("The narrative"))


def _page_url(f: Path, root: Path) -> str:
    return "/_board/page?path=" + quote("/" + ds._rel(f, root))


def _first_para(body: str) -> str:
    for para in re.split(r"\n\s*\n", body.strip()):
        t = para.strip()
        if t and not t.startswith(("#", "```", "|")):
            return _plain(re.sub(r"^\*\*[^*]+\*\*:?\s*", "", t))
    return ""


def _open_list(text: str) -> list:
    m = re.search(r"(?ms)^Open\n-+\n(.*?)(?=^\S[^\n]*\n[-=]{3,}|\Z)", text)
    return [re.sub(r"^\d+\.\s*", "", x).strip() for x in (m.group(1).splitlines() if m else []) if re.match(r"^\d+\.\s", x)]


STATE_MARK = (("done", "✅"), ("running", "⏳"), ("queued", "⏳"), ("not started", "⬜"), ("waits", "⬜"))


def _mark(state: str) -> str:
    return next((m for w, m in STATE_MARK if w in state.lower()), "⬜")


# `b51.j04.t02` or, as the pages write it, `b51 j04 t02` (JL 261102: Support blocks missed every b51 Job)
DOT_REF = re.compile(r"\bb(\d{2})[. ]j(\d{2})(?:[. ]t(\d{2}))?\b")
# a run of Jobs: `b01 j11 to j14`, `b01 j20-j23`
RANGE_REF = re.compile(r"\bb(\d{2})[. ]j(\d{2})\s*(?:to|-|–)\s*j(\d{2})\b")


PROJ_REF = re.compile(r"\b(Project-[A-Za-z0-9_-]+)(?:/|\s+)(?:(work|discovery)/)?(b\d{2})(?:_[A-Za-z0-9_-]+)?"
                      r"(?:[./](j\d{2})(?:_[A-Za-z0-9_-]+)?)?(?:[./](t\d{2}))?")


def explore_tree(board: Path) -> dict:
    """{kind: {Project: {Block: {Job: {Tasks}}}}}: only the folders this paper's pages name, in its own Project (by
    path `work/bNN_…/jNN_…` or address `bNN.jNN.tNN`) or in another (`Project-Example-B bNN_<block>`,
    `Project-X/work/b03_…/j01_…`); never its archive or built output (JL 261101: "we can have the works from
    multiple projects")."""
    own = next((d for d in board.parents if (d / "work").is_dir() or (d / "discovery").is_dir()), None)
    tree = {"work": {}, "discovery": {}, "named": {}}
    if own is None:
        return tree
    space = next((d for d in own.parents if (d / "pyproject.toml").is_file() or (d / "AGENTS.md").is_file()), own.parent)
    projects = {own.name: own}

    def project(name: str):
        if name not in projects:
            projects[name] = next((d for d in [own.parent / name, *space.glob(f"*/{name}")] if d.is_dir()), None)
        return projects[name]

    def add(proj: Path, kind: str, b: str, j: str = "", t: str = ""):
        for bd in sorted(proj.glob(f"{kind}/{b}_*")) or ([proj / kind / b] if (proj / kind / b).is_dir() else []):
            jobs = tree[kind].setdefault(proj, {}).setdefault(bd, {})
            for jd in (sorted(bd.glob(f"{j}_*")) if j else []):
                tree["named"][jd] = tree["named"].get(jd, 0) + 1
                tasks = jobs.setdefault(jd, set())
                tasks.update(sorted(jd.glob(f"{t}_*")) if t else [])
    for md in [*board.rglob("*.md"), *board.rglob("*-drawing.yaml")]:
        if any(part in ("_archive", "delivery", "history", "passes") for part in md.relative_to(board).parts):
            continue
        text = md.read_text(encoding="utf-8", errors="ignore")
        for name, kind, b, j, t in PROJ_REF.findall(text):          # another Project's (or this one's, named in full)
            proj = project(name)
            if proj is not None:
                add(proj, kind or ("discovery" if (proj / "discovery").glob(f"{b}_*") and not list(proj.glob(f"work/{b}_*")) else "work"), b, j, t)
        text = PROJ_REF.sub(" ", text)                               # what is left is this Project's
        for kind, block, job in EXPLORE_REF.findall(text):
            add(own, kind, block[:3], job[:3] if job else "")
        for bn, jn, tn in DOT_REF.findall(text):
            add(own, "work", f"b{bn}", f"j{jn}", f"t{tn}" if tn else "")
        for bn, ja, jb in RANGE_REF.findall(text):
            for jn in range(int(ja) + 1, int(jb) + 1):                # the first is DOT_REF's already
                add(own, "work", f"b{bn}", f"j{jn:02d}")
    return tree


def _folder_line(folder: Path) -> str:
    """A folder's one line: a Block's spine, else the face's Goal or Aim, else its title."""
    f = folder / "board.md" if (folder / "board.md").is_file() else folder / f"{folder.name}.md"
    if not f.is_file():
        return ""
    text = f.read_text(encoding="utf-8", errors="ignore")
    line = _field(text, "spine") or _field(text, "goal") or _field(text, "aim") or \
        next((ln.lstrip("# ").strip() for ln in text.splitlines() if ln.startswith("# ")), "")
    return _plain(line)


def _state_words(state: str) -> str:
    """`1 · Plan · sign` as words: `Plan: waits for your sign` (G r01: a bare number and "sign" said nothing)."""
    m = re.match(r"\d+\s*·\s*([^·]+?)\s*·\s*(.+)$", state or "")
    if not m:
        return state
    say = {"sign": "waits for your sign", "asked": "waits for your answer", "pass": "in review", "next": "next"}
    return f"{m.group(1)}: {say.get(m.group(2).strip(), m.group(2).strip())}"


def _version_url(job: Path, root: Path, section: str) -> str:
    return "/_board/workbench?" + "&".join(f"{k}={quote(v)}" for k, v in
                                           (("path", ds._rel(job, root)), ("layout", "focus"), ("section", section)))


def _section_state(task: Path, root: Path) -> str:
    try:
        f, st, k = _facts(task, root)
    except Exception:
        return ""
    step = next((s for _, s in WORK if st.get(s) in ("sign", "asked", "pass", "next")), None)
    return f"{step} · {word(st[step], k)[0]}" if step else "done"


def _waits(text: str) -> list:
    """A face's sign lines still open: `**G0:** ⬜ JL has not chosen …`."""
    return [m.group(0).strip() for m in re.finditer(r"(?m)^\**G\d+:?\**:?\s*⬜.*$", text)]


def md_table(text: str, first: str) -> list:
    """The rows of a Markdown table whose header's first cell is `first`, as dicts by header name."""
    lines, out = text.splitlines(), []
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and cells and cells[0] == first:
            for row in lines[i + 2:]:
                if not row.lstrip().startswith("|"):
                    break
                vals = [c.strip() for c in row.strip().strip("|").split("|")]
                out.append(dict(zip(cells, vals + [""] * (len(cells) - len(vals)))))
            break
    return out


# ── Interactions as a section of each part's view, not a view of their own (JL 261031: "I think the interaction and
# MindMap should be something like the sections under the view") ──────────────────────────────────────────────────
def part_topics(board: Path) -> set:
    out = {board_topic(board, key, pat) for key, _, pat in BOARD_PARTS} | {board_topic(board, "related", RELATED)}
    return {t for t in out if t is not None}


def _num(task: Path) -> int:
    m = re.match(r"t(\d+)_", task.name)
    return int(m.group(1)) if m else -1


def _task_url(task: Path, root: Path, group: str = "") -> str:
    q = [("path", ds._rel(task, root)), ("layout", "focus"), ("section", "work")] + ([("group", group)] if group else [])
    return "/_board/workbench?" + "&".join(f"{k}={quote(v)}" for k, v in q)


def is_version(job: Path) -> bool:
    """A paper Board's Job is a version unless it is the display Job (j21_displays, s01-D11), the citation Job, or the
    submission Job of a send (jNN_submission_<version>: its letters and the portal; JL 261102)."""
    return not re.search(r"display|citation|cite|evidence|value|submission", job.name, re.I)


def display_job(version: Path) -> Path | None:
    """The paper's display Job beside the versions (s01-D11): a Job folder whose name says display."""
    return next((j for j in sorted(version.parent.glob("j[0-9]*_*")) if j.is_dir() and re.search(r"display|evidence", j.name, re.I)), None)


# ── the explore layer, a view of its own (JL 261031: "one paper's studio should be "explore blocks" ... which indicate
# what are the work blocks and what are the citation blocks will be used to support this work"): the work Blocks
# (internal) and discovery Blocks (external) the Board's own pages name, each with the Jobs it uses ──────────────────
EXPLORE_REF = re.compile(r"\b(work|discovery)/(b\d+_[A-Za-z0-9_.-]+)(?:/(j\d+_[A-Za-z0-9_.-]+))?")


def explore_blocks(board: Path) -> dict:
    """{("work"|"discovery", Block folder): set of Job names} from every page the Board holds (its face, topics, Jobs,
    Tasks), never its archive or built output; only Blocks that exist in the Project."""
    project = next((d for d in board.parents if (d / "work").is_dir() or (d / "discovery").is_dir()), None)
    if project is None:
        return {}
    found = {}
    for md in board.rglob("*.md"):
        if any(part in ("_archive", "delivery", "history", "passes") for part in md.relative_to(board).parts):
            continue
        for kind, block, job in EXPLORE_REF.findall(md.read_text(encoding="utf-8", errors="ignore")):
            folder = project / kind / block
            if folder.is_dir():
                jobs = found.setdefault((kind, folder), set())
                if job and (folder / job).is_dir():
                    jobs.add(job)
    return found


def display_plan():
    """haipipe-paper-plan's display_plan module (the s06 display plan and the venue's display rules), or None."""
    import importlib.util
    try:
        from host_paths import skill_dir
        f = skill_dir("haipipe-paper-plan") / "scripts" / "display_plan.py"
        spec = importlib.util.spec_from_file_location("display_plan", f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception:
        return None

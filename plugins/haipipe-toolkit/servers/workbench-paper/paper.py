"""📄 Paper · the Board-level Paper Workbench, live and storage-less.

    GET /_board/paper?path=<board.md>&file=board.md[#<space>[/<tab>][/<view>]]

The Paper Workbench is the Board-altitude sibling of the 📃 Page workbench. Page shows
one Page's plan, evidence and runs; this shows one paper Board's journey
(haipipe-workbench-paper, JL 260916). It wears the shared workbench shell (servers/README.md
"Adding a workbench", JL 261003): the title, a band (desk ·
Story version · questions · Sections · build state), then the Space row with the shared
Guide first, each Space's tabs, Views and content in one box, and the shared Runs panel
folded to a strip on the right.

    Guide      Description · Method · RoadMap Draw · Related Paper, from the `paper`
               entry of workbench-shared/guide_families.py
    Ideation   Story00-ideation: the Ideas (ranked) table, else the plan's `Idea <n>:`
               divisions · evidence items · the I3 admission
    Story      Spine · RoadMap Draw · High-level logic + Low-level work · Related Papers
    Sections   Main · Appendix × Table · Narrative · Evidence, in §8 compile order
    Delivery   LaTeX · Word · Cover letter · Rounds × Preview · Artifacts · Checks

LIVE AND STORAGE-LESS, the Outline precedent: rendered from Markdown on every
open, so it can never be stale, and it needs no per-paper file. The earlier
`console/` prototype (a static data.js rebuilt by hand, one paper only) is
what this replaces. Applies to any Board whose board.md declares
`dialect: paper`; no Links key is needed.

READ-ONLY. Every row links back to the record that owns it, normally the
page's own 📃 Page route. The explicit copy controls write prompt text to
the clipboard only; the surface does not write Paper files, allocate a Run,
or infer a human tick. A gate shows a receipt when the named file exists and
`⬜ open` otherwise.
"""
import html
import json
import os
import re
from datetime import datetime
from pathlib import Path

from host_paths import SKILLS
from urllib.parse import parse_qs, quote, urlparse

from src.outline_version import latest_outline, plan_dir, version_tag
from src.plan_shape import iter_plan_bullets

_PAIRS_DIR = Path(os.environ.get("HAIPIPE_PAIRS_DIR",
                                 Path.home() / ".config" / "haipipe" / "pairs"))

_EV_RE = re.compile(r"\bE\d{2}-(?:VALUE|CITE|DISPLAY|TABLE)-[A-Za-z0-9-]+")
_DIV_RE = re.compile(r"^###\s+§?(\d+)\s*·\s*(.*?)\s*$")
_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")


# ---------------------------------------------------------------- text helpers
def esc(s):
    return html.escape("" if s is None else str(s), quote=True)


def clean(cell):
    """Markdown cell → plain text: links to their label, no emphasis marks."""
    cell = _LINK_RE.sub(r"\1", cell or "")
    cell = re.sub(r"[*_`]+", "", cell)
    return re.sub(r"\s+", " ", cell).strip()


def scalar(text, key, default=""):
    m = re.search(r"^%s:\s*(.+?)\s*$" % re.escape(key), text or "", re.M)
    return m.group(1) if m else default


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def table_rows(text, first_cell):
    """Every `| a | b |` row whose first cell matches `first_cell` (regex), as
    lists of cleaned cells. Header and rule rows never match a data pattern."""
    pat = re.compile(first_cell)
    rows = []
    for line in (text or "").splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [clean(c) for c in s.strip("|").split("|")]
        if cells and pat.fullmatch(cells[0]):
            rows.append(cells)
    return rows


def divisions(text):
    """`### N · Title` headings under `## Content` → [(n, title)]."""
    out, inside = [], False
    for line in (text or "").splitlines():
        if line.startswith("## "):
            inside = line[3:].strip().lower().startswith("content")
            continue
        m = _DIV_RE.match(line) if inside else None
        if m:
            out.append((int(m.group(1)), m.group(2)))
    return out


# ---------------------------------------------------------------- the board
def board_pages(board_text):
    """`## Pages` → [{"label","folder","stems"}] in roster order."""
    groups, inside, cur = [], False, None
    for line in (board_text or "").splitlines():
        if line.startswith("## "):
            inside = line[3:].strip().lower().startswith("pages")
            cur = None
            continue
        if not inside:
            continue
        if line.startswith("### ") and " · " in line:
            # `### LABEL · folder` or `### LABEL · folder · what it holds`; a heading whose
            # second part is prose names no folder, and page_file() finds the pages itself
            parts = [x.strip() for x in line[4:].split("·")]
            folder = parts[1] if re.fullmatch(r"[\w.-]+", parts[1]) else ""
            cur = {"label": parts[0], "folder": folder, "stems": []}
            groups.append(cur)
            continue
        s = line.strip()
        if cur is not None and s.endswith(".md") and " " not in s:
            cur["stems"].append(s[:-3])
    return groups


def page_file(board, folder, stem):
    """The page's Markdown: folded `<folder>/<stem>/<stem>.md` first, flat
    `<folder>/<stem>.md` second; with no folder, the one page folder of that
    name under any top-level folder. None when nothing is found."""
    if folder:
        for rel in (Path(folder) / stem / (stem + ".md"), Path(folder) / (stem + ".md")):
            if (board / rel).is_file():
                return rel
        return None
    found = sorted(board.glob("*/%s/%s.md" % (stem, stem))) + sorted(board.glob("*/%s.md" % stem))
    return found[0].relative_to(board) if found else None


def outline_url(path_param, rel_file, lens="div", **extra):
    url = "/_board/draft?path=%s&file=%s&lens=%s" % (
        quote(path_param, safe=""), quote(str(rel_file), safe=""), quote(lens, safe=""))
    for k, v in extra.items():
        if v:
            url += "&%s=%s" % (k, quote(str(v), safe=""))
    return url


def board_url(path_param, rel):
    """A plain link into the built board tree for a non-Page file."""
    base = path_param.rsplit("/", 1)[0]
    return base + "/" + str(rel)


# ---------------------------------------------------------------- collectors
SECTION_ROW = r"S-[\w-]+(?:\s*(?:\(.*\)|·.*))?"
STORY_STEM = re.compile(r"^Story(?:[A-Z]|(?!00)\d{2})(?:\b|-)")


def collect(board, path_param):
    """Read everything the four Spaces show. Pure: no writes, no network."""
    board = Path(board)
    text = read(board / "board.md")
    groups = board_pages(text)
    pages = []
    for g in groups:
        for stem in g["stems"]:
            rel = page_file(board, g["folder"], stem)
            pages.append({"group": g, "stem": stem, "rel": rel,
                          "text": read(board / rel) if rel else ""})
    story00 = next((p for p in pages if p["stem"].startswith("Story00")), None)
    # Story<Letter> is the current form; legacy numbered Stories (Story01-seed, Story02-roadmap,
    # Story03-narrative-MISQ) stay readable per haipipe-paper-ideation, so they are Stories too
    stories = [p for p in pages if STORY_STEM.match(p["stem"])]
    sections = [p for p in pages if p["stem"].startswith("S-")]
    rounds = [p for p in pages if p["stem"].startswith("RD")]
    d = {
        "title": next((l[2:].strip() for l in text.splitlines()
                       if l.startswith("# ")), board.name),
        "board": board, "path": path_param,
        "spine": scalar(text, "spine"), "close": scalar(text, "close"),
        "session": scalar(text, "session"), "dialect": scalar(text, "dialect"),
        "groups": groups, "pages": pages, "story00": story00,
        "stories": stories, "sections": sections, "rounds": rounds,
    }
    d["sessions"] = session_rows(d)
    d["ideation"] = ideation(d)
    d["story"] = [story(d, p) for p in stories]
    d["blocks"] = project_blocks(d)
    d["disc"] = project_discoveries(d)
    d["delivery"] = delivery_info(d)
    d["hero"] = hero_evidence(d)
    d["supporting"] = supporting_tree(d)
    d["gates"] = gates(d)
    return d


def paper_desk(d):
    """The desk name, read from a real B group (`Ba-MISQ-Main` → MISQ) or, before
    any Section group exists, from the Story's §8 target cell (`MISQ · 1`)."""
    for g in d["groups"]:
        m = re.match(r"^B[a-z]-(.+)-(?:Main|Appendix|Round)$", g["folder"])
        if m:
            return m.group(1)
    for p in d["stories"]:
        for c in table_rows(p["text"], r"S-[\w-]+\s*\(.*\)"):
            m = re.search(r"\(([^·)]+)", c[0])
            if m and m.group(1).strip():
                return m.group(1).strip()
    return ""


def _pairs_for(root_cwd):
    """Pair manifests registered for this workspace, keyed by lower name.
    Exact key match only: a name match is never scored here (CLAUDE.md)."""
    out = {}
    try:
        files = sorted(_PAIRS_DIR.glob("*.json"))
    except OSError:
        return out
    for f in files:
        try:
            j = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(j, dict) or j.get("cwd") != str(root_cwd):
            continue
        name = str(j.get("pair_name", "")).strip().lower()
        providers = j.get("providers") or {}
        codex = providers.get("codex") or {}
        claude = (providers.get("claude") or {}).get("session_id", "")
        rec = {"file": f.name, "pair": str(j.get("pair_name", "")).strip(),
               "codex": codex.get("session_id", ""),
               "updated": str(j.get("updated_at", ""))[:10]}
        out[name] = rec
        if claude:                             # exact id key: the page's own session: line
            out["claude:" + claude] = rec
            if rec["codex"]:                   # an Appendix shares one Claude session across pages
                out["pair:%s:%s" % (claude, rec["codex"])] = rec
    return out


def session_rows(d):
    """One session per Section Page (JL 260916; Claude sessions via
    `/haipipe-paper sessions`, JL 260928). The page header's `session:` line
    binds its Claude session; a pair manifest joins by that exact id, else by
    exact pair name. Ideation, Story and Supporting work stay in the current
    session, so only S- pages get rows."""
    root = d.get("root")
    pairs = _pairs_for(root) if root else {}
    rows = []
    for p in d["sections"]:
        parts = p["stem"].split("-")           # S-<desk>-<Main|Appendix>-<N>-<Title>
        desk = parts[1].lower() if len(parts) > 1 else "paper"
        title = "-".join(parts[4:] if len(parts) > 4 else parts[3:]).lower()
        plan = "paper-%s-%s" % (desk, title)
        sid = scalar(p.get("text", ""), "session")
        cx = scalar(p.get("text", ""), "codex-session")
        # the page's own (session, codex-session) pair first: Appendix pages share one Claude
        # session and each keeps its own Codex thread, so the Claude id alone picks the last pair
        hit = ((pairs.get("pair:%s:%s" % (sid, cx)) if sid and cx else None)
               or (pairs.get("claude:" + sid) if sid else None)
               or pairs.get(plan) or pairs.get(p["stem"].lower()))
        state = []
        if sid:
            state.append("claude %s" % sid[:8])
        if hit and hit["codex"]:
            state.append("codex %s · %s" % (hit["codex"][:8], hit["updated"]))
        elif cx:
            state.append("codex %s" % cx[:8])
        rows.append({"stem": p["stem"], "rel": p["rel"], "group": p["group"]["folder"],
                     "pair": hit["pair"] if hit else ("" if (sid or cx) else plan),
                     "state": " · ".join(state) or "no session · plan"})
    return rows


def idea_divisions(text):
    """`### N · Idea <n>: <research question>` divisions under Content → {n: {"title", "fields"}}
    where fields are the division's `**Field**` blocks in page order, each a
    list of paragraphs (a `- ` line stays a list item)."""
    out, cur, field = {}, None, None
    inside = False
    for line in (text or "").splitlines():
        if line.startswith("## "):
            inside = line[3:].strip().lower().startswith("content")
            cur = None
            continue
        if not inside:
            continue
        m = re.match(r"^###\s+§?\d+\s*·\s*Idea\s+(\d+)\s*:\s*(.*?)\s*$", line)
        if m:
            cur = {"title": m.group(2), "fields": []}
            out[int(m.group(1))] = cur
            field = None
            continue
        if line.startswith("### ") or line.startswith("## "):
            cur = None
            continue
        if cur is None:
            continue
        fm = re.match(r"^\*\*(.+?)\*\*\s*:?\s*(.*)$", line.strip())
        if fm:
            field = [fm.group(1).strip(), []]
            cur["fields"].append(field)
            if fm.group(2).strip():
                field[1].append(fm.group(2).strip())
            continue
        if field is not None and line.strip():
            field[1].append(line.rstrip())
    return out


def _table_headers(text, first_cell):
    """The header cells of the table whose first data row matches first_cell."""
    pat = re.compile(first_cell)
    header = None
    for line in (text or "").splitlines():
        s_ = line.strip()
        if not s_.startswith("|"):
            header = None
            continue
        cells = [clean(c) for c in s_.strip("|").split("|")]
        if all(re.fullmatch(r"-+", c or "-") for c in cells):
            continue
        if header is None:
            header = cells
            continue
        if cells and pat.fullmatch(cells[0]):
            return header
    return None


def ideation(d):
    """The Idea Cards of Story00, one collapsed card each (JL 260916: "like the
    evidence card in haipipe-workbench-page, I can open and hide it")."""
    p = d["story00"]
    if p is None:
        return {"present": False}
    b = d["board"]
    folder = (b / p["rel"]).parent if p["rel"] else None
    out = {"present": True, "stem": p["stem"], "rel": p["rel"],
           "state": clean(scalar(p["text"], "state", "⬜ no state line")),
           "ideas": [], "source": "", "items": [], "receipts": []}
    # ① the page's own Ideas (ranked) table, when Content carries one
    rows = table_rows(p["text"], r"i\d+")
    if rows:
        out["source"] = "Content · Ideas (ranked) table"
        headers = _table_headers(p["text"], r"i\d+") or []
        for c in rows:
            fields = [(headers[i] if i < len(headers) else "col %d" % (i + 1), c[i])
                      for i in range(2, len(c)) if c[i] and c[i] not in ("—", "-")]
            out["ideas"].append({"id": c[0], "title": c[1] if len(c) > 1 else "",
                                 "verdict": c[4] if len(c) > 4 else "⬜ open",
                                 "went": c[5] if len(c) > 5 else "",
                                 "address": "", "chips": [], "bullets": [],
                                 "fields": fields, "items": []})
    # ② else the plan's `Idea <n>: <research question>` divisions (an Ideation Page before Content)
    plan = latest_outline(plan_dir(folder), p["stem"]) if folder else None
    if plan is not None:
        ptext = read(plan)
        if not out["ideas"]:
            out["source"] = "outline plan · Idea divisions (page has no Content yet)"
            seen = {}
            for blk in iter_plan_bullets(ptext):
                m = re.match(r"^Idea\s+(\d+)\s*:\s*(.*)$", blk["division_title"])
                if not m:
                    continue
                key = blk["division"]
                if key not in seen:
                    seen[key] = {"id": "i%02d" % int(m.group(1)), "title": m.group(2),
                                 "address": key, "chips": [], "bullets": [],
                                 "verdict": "⬜ open", "went": "", "fields": [], "items": []}
                    out["ideas"].append(seen[key])
                notes = [x for x in blk["continuation"] if re.match(r"^(Note|Annotation|More):", x)]
                evidence = next((x for x in blk["continuation"] if x.startswith("Evidence:")), "")
                seen[key]["bullets"].append({
                    "address": blk["address"], "bullet": blk["bullet"], "head": blk["head"],
                    "notes": [re.sub(r"^\w+:\s*", "", n) for n in notes],
                    "evidence": re.sub(r"^Evidence:\s*", "", evidence)})
                seen[key]["chips"] += [c for c in _EV_RE.findall(blk["body"])
                                       if c not in seen[key]["chips"]]
    # ③ the idea itself: the page's Idea <n> division, when Content carries one
    divs = idea_divisions(p["text"])
    for idea in out["ideas"]:
        n = re.search(r"\d+", idea["id"])
        div = divs.get(int(n.group(0))) if n else None
        idea["substance"] = div["fields"] if div else []
        if div and not idea.get("title"):
            idea["title"] = div["title"]
    # ④ the authored Evidence Item contract, with its Verified tick
    if folder:
        items = read(plan_dir(folder) / (p["stem"] + "-evidence-items.md"))
        for m in re.finditer(r"^###\s+(E\d{2}-[A-Z]+-[\w-]+)\s*·\s*(\S+)\s*·\s*(.*)$", items, re.M):
            tail = items[m.end():]
            nxt = tail.find("\n### ")
            body = tail if nxt < 0 else tail[:nxt]
            v = re.search(r"\*\*Verified\*\*:\s*(\S+)", body)
            item = {"id": m.group(1), "target": m.group(2), "desc": m.group(3).strip(),
                    "verified": v.group(1) if v else "⬜"}
            out["items"].append(item)
            for idea in out["ideas"]:
                if idea["address"] and item["target"].startswith(idea["address"] + "."):
                    idea["items"].append(item)
        # ⑤ the I3 receipt and handoff files haipipe-paper-ideation names
        for rel, what in (("workflow/selection.yaml", "I3 selection receipt"),
                          ("handoff/paper-ideation.yaml", "final handoff"),
                          ("projection/paper-ideation-sync.yaml", "working sync packet")):
            out["receipts"].append({"what": what, "rel": rel,
                                    "state": "present" if (folder / rel).is_file() else "absent"})
    return out


_ADDR_RE = re.compile(r"\bb(\d{2})(?:[.\s_-]?j(\d{2}))?(?:[.\s_-]?t(\d{2}))?(?:[.\s_-]?r(\d{2}))?\b")


_TASK_HOMES = ("tasks", "task")          # LLMRec says tasks/, OpioidRx says task/
_SKIP_DIRS = {"src", "sbatch", "results", "runs", "scripts", "notebooks", "workflow",
              "QA", "board", "diagram", "config", "configs", "tests", "_tools"}
_TICKET_EXT = {".sh", ".ps1"}
_CODE_EXT = (".py", ".do", ".R")


def _head_field(path, key):
    """`key: value` in the first 40 lines of a task page (task-table's rule)."""
    try:
        for line in path.read_text(errors="replace").splitlines()[:40]:
            m = re.match(r"^%s:\s*(.*?)\s*$" % re.escape(key), line)
            if m:
                return m.group(1)
    except OSError:
        pass
    return None


def _headline(script):
    """First docstring or comment sentence of a script, at most 140 chars."""
    try:
        text = script.read_text(errors="replace")
    except OSError:
        return ""
    doc = ""
    if script.suffix == ".py":
        m = re.search(r'^\s*(?:r|u)?("""|\'\'\')(.*?)\1', text, re.S)
        doc = m.group(2) if m else ""
    else:
        for line in text.splitlines()[:15]:
            t = line.strip()
            if t.startswith(("//", "*", "#")) and not t.startswith("#!"):
                doc = t.lstrip("/*# ").strip().lstrip("=-*#").strip()
                if doc:
                    break
    para = []
    for l in doc.splitlines():
        if not l.strip():
            if para:
                break
            continue
        para.append(l.strip())
    line = re.sub(r"^[a-z]?\d{2}_\S+\s*[—:-]\s*", "", " ".join(para)).strip()
    m = re.match(r"^(.{20,}?[.!?])(?=\s+[A-Z(\[]|\s*$)", line)
    line = m.group(1) if m else line
    if len(line) < 12 or "===" in line or re.match(r"^\d+[.)]\s", line):
        return ""                     # a section marker or a stub is not what a task develops
    return line if len(line) <= 140 else line[:137] + "…"


def _run_state(receipts):
    """runtime.yaml `status:` values folded to done · running · failed · planned."""
    c = {}
    for st in receipts:
        t = (st or "?").lower()
        k = ("done" if t in ("complete", "completed", "done", "ok", "success") else
             "running" if "run" in t else "failed" if "fail" in t or "error" in t else
             "planned" if t in ("planned", "ready", "held", "hold") else t)
        c[k] = c.get(k, 0) + 1
    return c


def _fmt_state(c):
    if not c:
        return "no receipts"
    order = ("done", "running", "failed", "planned")
    keys = [k for k in order if k in c] + sorted(k for k in c if k not in order)
    return " · ".join("%s %d" % (k, c[k]) for k in keys)


def _scan_task(job, name, tdir):
    """One Task, in either shape: `<job>/<task>/` (Stata dialect, its own
    runs/ results/ scripts/) or the flat `<job>/{runs,results,scripts}/<task>/`."""
    if tdir is not None:
        page = tdir / (name + ".md")
        runs_dir, res_dir, code_dir = tdir / "runs", tdir / "results", tdir / "scripts"
    else:
        page = job / "scripts" / name / (name + ".md")
        runs_dir, res_dir, code_dir = job / "runs" / name, job / "results" / name, job / "scripts" / name
    if not page.is_file():
        alt = (code_dir / "README.md") if code_dir.is_dir() else None
        page = alt if alt and alt.is_file() else None
    tickets = sorted(x for x in runs_dir.rglob("*") if x.is_file() and x.suffix in _TICKET_EXT) if runs_dir.is_dir() else []
    receipts, receipt_map = [], {}
    if res_dir.is_dir():
        for run_dir in sorted(x for x in res_dir.iterdir() if x.is_dir()):
            r = run_dir / "runtime.yaml"
            if r.is_file():
                st = _head_field(r, "status") or "?"
                receipts.append(st)
                receipt_map[run_dir.name] = st            # Discovery: results/<run stem>/
                tk = _head_field(r, "ticket")             # Stata dialect: the receipt names its ticket
                if tk:
                    receipt_map[Path(tk.strip().strip('"')).stem] = st
    develops = _head_field(page, "develops") if page else None
    src = "page"
    if not develops and code_dir.is_dir():
        code = sorted(x for x in code_dir.iterdir() if x.is_file() and x.suffix in _CODE_EXT and not x.name.startswith("_"))
        own = [x for x in code if x.stem == name] or code
        develops, src = (_headline(own[0]) if own else ""), (own[0].name if own else "")
    state = (_head_field(page, "state") if page else None) or ""
    home = tdir if tdir is not None else (code_dir if code_dir.is_dir() else runs_dir)
    return {"name": name, "addr": "", "dir": home, "page": page, "tickets": len(tickets),
            "ticket_list": [(x.stem, x) for x in tickets], "receipt_map": receipt_map,
            "receipts": _run_state(receipts), "develops": develops or "", "develops_src": src, "state": state}


def scan_task_tree(tasks):
    """Block → Job → Task read off the folder. Names are checked against
    <b|j|t>NN_ and everything else is skipped, never guessed."""
    blocks = []
    if tasks is None or not tasks.is_dir():
        return blocks
    for b in sorted(x for x in tasks.iterdir() if x.is_dir() and re.match(r"^b\d{2}_", x.name)):
        jobs = []
        for j in sorted(x for x in b.iterdir() if x.is_dir() and re.match(r"^j\d{2}_", x.name)):
            direct = sorted(x for x in j.iterdir() if x.is_dir() and re.match(r"^t\d{2}_", x.name) and x.name not in _SKIP_DIRS)
            tasks_ = [_scan_task(j, t.name, t) for t in direct]
            if not direct:
                stems = set()
                for sub in ("runs", "scripts", "results", "notebooks"):
                    if (j / sub).is_dir():
                        stems |= {x.name for x in (j / sub).iterdir() if x.is_dir() and re.match(r"^t\d{2}_", x.name)}
                tasks_ = [_scan_task(j, n, None) for n in sorted(stems)]
            for t in tasks_:
                t["addr"] = b.name[:3] + j.name[:3] + t["name"][:3]
            jobs.append({"name": j.name, "addr": b.name[:3] + j.name[:3], "dir": j, "tasks": tasks_,
                         "shape": "task folders" if direct else "runs/ · scripts/ · results/ per task"})
        blocks.append({"name": b.name, "addr": b.name[:3], "dir": b, "jobs": jobs,
                       "board": (b / "board" / "index.html").is_file()})
    return blocks


def project_blocks(d):
    """The Task home this paper may draw on: examples/<Project>/tasks/ (or task/)
    holding bNN blocks, scanned Block → Job → Task on every load."""
    b = d["board"]
    text = read(b / "board.md")
    project = b.parent.parent if b.parent.name == "papers" else None
    tasks = None
    home = scalar(text, "task-home").strip()          # board.md may name the folder outright
    if home:
        cand = (b / home).resolve()
        tasks = cand if cand.is_dir() else None
    if tasks is None and project:
        for name in _TASK_HOMES:
            if (project / name).is_dir():
                tasks = project / name
                break
    tree = scan_task_tree(tasks)
    if tasks and project and tasks.parent == project:
        label = "examples/%s/%s/" % (project.name, tasks.name)
    elif tasks:
        label = home or tasks.name
    else:
        label = (("examples/%s/ has no tasks/ or task/ folder" % project.name) if project else
                 "no project task home (board is not under papers/)")
    return {"dir": tasks, "blocks": [x["name"] for x in tree], "tree": tree, "label": label,
            "claim": _addresses(scalar(text, "blocks")),
            "n_jobs": sum(len(x["jobs"]) for x in tree),
            "n_tasks": sum(len(j["tasks"]) for x in tree for j in x["jobs"])}


_RANGE_RE = re.compile(r"\b(b\d{2}[.\s_-]?j\d{2}[.\s_-]?)t(\d{2})\s*[–-]\s*t(\d{2})\b")


def _expand_ranges(text):
    """`b03.j02.t01–t05` → `b03.j02.t01 b03.j02.t02 … b03.j02.t05`: a row names a run of tasks once."""
    return _RANGE_RE.sub(lambda m: " ".join("%st%02d" % (m.group(1), n)
                                           for n in range(int(m.group(2)), int(m.group(3)) + 1)), text or "")


def _addresses(text):
    """`b02.j01 b03 b04` (or b02j01, comma-separated) → ["b02j01", "b03", "b04"]."""
    out = []
    for m in _ADDR_RE.finditer(_expand_ranges(text)):
        a = "".join(l + n for l, n in zip("bjtr", m.groups()) if n)
        if a not in out:
            out.append(a)
    return out


def paper_scope(d):
    """The Task-home addresses this paper claims: board.md `blocks:` plus every
    bNN[.jNN[.tNN]] address written on a Story Task Roadmap (§7) row. Empty = nothing claimed."""
    scope = list(d["blocks"]["claim"])
    for s in d.get("story", []):
        for cells in s["tt"]:
            for a in _addresses(" ".join(cells)):
                if a not in scope:
                    scope.append(a)
    return scope


def _discovery_yaml(path):
    """status · report.outcome · report.confidence · first sentence of question."""
    out = {"status": "", "outcome": "", "confidence": "", "question": ""}
    try:
        lines = path.read_text(errors="replace").splitlines()
    except OSError:
        return out
    sect, q = None, []
    for line in lines:
        if not line.strip():
            continue
        top = not line.startswith((" ", "\t"))
        if top:
            m = re.match(r"^([\w-]+):\s*(.*?)\s*$", line)
            sect = m.group(1) if m else None
            if m and sect == "status":
                out["status"] = m.group(2).split("#")[0].strip()
            continue
        if sect == "question":
            q.append(line.strip())
        elif sect == "report":
            m = re.match(r"^\s+(outcome|confidence):\s*(.*?)\s*$", line)
            if m:
                out[m.group(1)] = m.group(2).split("#")[0].strip()
    text = " ".join(q)
    m = re.match(r"^(.{20,}?[.?!])(?=\s+[A-Z(\[]|\s*$)", text)
    out["question"] = m.group(1) if m else text
    return out


def project_discoveries(d):
    """The Discovery home this paper may draw on: examples/<Project>/discoveries/
    (or board.md `discovery-home:`), bNN evidence boards holding jNN inquiries
    holding tNN Discovery Task Pages, each with a discovery.yaml."""
    b = d["board"]
    text = read(b / "board.md")
    project = b.parent.parent if b.parent.name == "papers" else None
    home = scalar(text, "discovery-home").strip()
    root = (b / home).resolve() if home else None
    if (root is None or not root.is_dir()) and project and (project / "discoveries").is_dir():
        root = project / "discoveries"
    if root is not None and not root.is_dir():
        root = None
    tree = scan_task_tree(root)
    for blk in tree:
        blk["board_md"] = (blk["dir"] / "board.md") if (blk["dir"] / "board.md").is_file() else None
        for j in blk["jobs"]:
            j["index"] = (j["dir"] / "_index.md") if (j["dir"] / "_index.md").is_file() else None
            for t in j["tasks"]:
                y = t["dir"] / "discovery.yaml"
                t.update(_discovery_yaml(y) if y.is_file() else {"status": "", "outcome": "", "confidence": "", "question": ""})
                t["n_results"] = len([x for x in (t["dir"] / "results").iterdir() if x.is_dir()]) if (t["dir"] / "results").is_dir() else 0
    label = (("examples/%s/discoveries/" % project.name) if root is not None and project and root.parent == project else
             home if root is not None else
             ("examples/%s/ has no discoveries/ folder" % project.name) if project else
             "no discovery home (board is not under papers/)")
    return {"dir": root, "tree": tree, "label": label, "claim": _addresses(scalar(text, "discoveries")),
            "n_jobs": sum(len(x["jobs"]) for x in tree),
            "n_tasks": sum(len(j["tasks"]) for x in tree for j in x["jobs"])}


def discovery_scope(d):
    """Discovery addresses this paper claims: board.md `discoveries:` plus every
    bNN[.jNN[.tNN]] address written on a Story Discovery Roadmap (§6) row."""
    scope = list(d["disc"]["claim"])
    for s in d.get("story", []):
        for cells in s["dd"]:
            for a in _addresses(" ".join(cells)):
                if a not in scope:
                    scope.append(a)
    return scope


def _disc_lookup(d, addr):
    """b01j04 → (block, job, task|None) in the Discovery tree, or None."""
    for blk in d["disc"]["tree"]:
        if not addr.startswith(blk["addr"]):
            continue
        if len(addr) == 3:
            return blk, None, None
        for j in blk["jobs"]:
            if addr.startswith(j["addr"]):
                if len(addr) == 6:
                    return blk, j, None
                for t in j["tasks"]:
                    if t["addr"] == addr:
                        return blk, j, t
    return None


def _find(parent, prefix):
    if parent is None or not parent.is_dir():
        return None
    for x in sorted(parent.iterdir()):
        if x.name.startswith(prefix) and re.match(r"^%s(?:[_.-]|$)" % prefix, x.name):
            return x
    return None


def task_home(d, cells):
    """Read every bNN[.jNN[.tNN[.rNN]]] address on a Story row and say which
    levels exist under the project's Task home. The first address is the row's
    own keys (address · levels · path · state); `all` lists every one, because a
    row may be answered by more than one job and paper_scope() claims them all.
    No address → `no folder yet`."""
    found_all, seen = [], set()
    for cell in cells:
        for m in _ADDR_RE.finditer(_expand_ranges(cell)):
            one = _resolve_address(d, m)
            if one["address"] not in seen:
                seen.add(one["address"]); found_all.append(one)
    if not found_all:
        return {"address": "", "levels": [], "path": "", "state": "no folder yet", "all": []}
    return dict(found_all[0], all=found_all)


def _resolve_address(d, m):
    """One address match → which of its levels exist under the Task home."""
    tasks = d["blocks"]["dir"]
    bnn, jnn, tnn, rnn = m.groups()
    levels = []
    block = _find(tasks, "b" + bnn); levels.append(("b" + bnn, block))
    job = _find(block, "j" + jnn) if jnn else None
    if jnn:
        levels.append(("j" + jnn, job))
    task = None
    if tnn:
        task = _find(job, "t" + tnn) or _find(job / "runs" if job else None, "t" + tnn)
        levels.append(("t" + tnn, task))
    if rnn:
        run = None
        if task is not None and job is not None:
            run = _find(job / "results" / task.name, "r" + rnn) or _find(task / "results", "r" + rnn)
        levels.append(("r" + rnn, run))
    addr = ".".join(l for l, _ in levels)
    found = [x for x in levels if x[1] is not None]
    return {"address": addr, "levels": levels,
            "path": str(found[-1][1].relative_to(tasks.parent)) if found and tasks else "",
            "state": ("allocated · %d/%d levels exist" % (len(found), len(levels))) if found else "address named · nothing on disk"}


def story(d, p):
    t = p["text"]
    s = {"stem": p["stem"], "rel": p["rel"],
         "state": clean(scalar(t, "state", "⬜ no state line")),
         "divisions": divisions(t),
         "rq": table_rows(t, r"RQ\d+"), "rq_h": _table_headers(t, r"RQ\d+") or [],
         "e": table_rows(t, r"E-?\d+(?:\s*\(.*\))?"), "e_h": _table_headers(t, r"E-?\d+(?:\s*\(.*\))?") or [],
         "dd": table_rows(t, r"D\d+"), "dd_h": _table_headers(t, r"D\d+") or [],
         "tt": table_rows(t, r"[TB]\d+"), "tt_h": _table_headers(t, r"[TB]\d+") or [],
         "qq": table_rows(t, r"Q\d+"), "qq_h": _table_headers(t, r"Q\d+") or [],
         "pp": table_rows(t, r"P\d+"), "pp_h": _table_headers(t, r"P\d+") or [],
         "qb": question_blocks(t),
         "sections": [], "sec_h": [], "order": []}
    s["sec_h"] = _table_headers(t, SECTION_ROW) or []
    # the Spine is §1 Identity, §2 Pitch, §4 Stakes; matched by title so a legacy numbered
    # Story part (Story02-roadmap's `1 · Mission`) does not pose as an Identity
    s["spine"] = [(n, title, parse_division(division_body(t, n)))
                  for n, title in s["divisions"]
                  if re.match(r"(identity|pitch|stakes)\b", title.strip().lower())]
    seen = set()
    for c in table_rows(t, SECTION_ROW):
        # `S-<id>`, `S-<id> (label)` or `S-<id> · §0 label` (JL 260925: MISQ's main rows)
        sid = re.split(r"\s*[(·]", c[0], maxsplit=1)[0].strip()
        if sid in seen:              # the same Section listed again in a later table
            continue
        seen.add(sid)
        page = next((x for x in d["sections"] if x["stem"] == sid), None)
        s["sections"].append({"id": sid, "target": c[0][len(sid):].strip(" ()·"),
                              "question": c[1] if len(c) > 1 else "", "cells": c, "heads": s["sec_h"],
                              "rel": page["rel"] if page else None,
                              "page_state": clean(scalar(page["text"], "state", "")) if page else ""})
    # the same rows written as records (no pipe tables in a Story, JL): `**S-<id> (N) · job**`
    # then `- **Field**: value` lines, inside the Section Narrative division
    narrative = next((n for n, title in s["divisions"] if title.strip().lower().startswith("section narrative")), None)
    for rec in (section_records(division_body(t, narrative)) if narrative is not None else []):
        if rec["id"] in seen:
            continue
        seen.add(rec["id"])
        page = next((x for x in d["sections"] if x["stem"] == rec["id"]), None)
        s["sections"].append(dict(rec, rel=page["rel"] if page else None,
                                  page_state=clean(scalar(page["text"], "state", "")) if page else ""))
    m = re.search(r"<!-- haipipe:compile-order:start -->(.*?)<!-- haipipe:compile-order:end -->", t, re.S)
    if m:
        s["order"] = [l.strip()[2:].strip() for l in m.group(1).splitlines()
                      if l.strip().startswith("- ")]
    return s


_RECORD = re.compile(r"^\*\*(S-[\w-]+)\s*(?:\(([^)]*)\))?\s*(?:·\s*(.*?))?\*\*\s*$")
_FIELD = re.compile(r"^-\s+\*\*(.+?)\*\*\s*:\s*(.*)$")


def section_records(body):
    """§8 Section Narrative rows written as records → the table rows' shape: {id, target, question,
    cells, heads}. `**S-<id> (N) · one job**` opens a record; its `- **Field**: value`
    lines are its cells; the Reader question field is the question."""
    out, cur = [], None
    for line in (body or "").splitlines():
        m = _RECORD.match(line.strip())
        if m:
            cur = {"id": m.group(1), "target": (m.group(2) or "").strip(), "question": "",
                   "fields": [("One job", clean(m.group(3) or ""))] if m.group(3) else []}
            out.append(cur)
            continue
        if line.startswith("#"):
            cur = None
            continue
        f = _FIELD.match(line.strip()) if cur is not None else None
        if f:
            key, value = f.group(1).strip(), clean(f.group(2))
            if key.lower() == "reader question":
                cur["question"] = value[:1].upper() + value[1:]
            else:
                cur["fields"].append((key, value))
    for r in out:
        r["cells"] = [r["id"], r["question"]] + [v for _, v in r["fields"]]
        r["heads"] = ["Section", "Reader question"] + [k for k, _ in r.pop("fields")]
    return out


def division_body(text, n):
    """The Markdown between `### n · …` and the next `### ` inside Content."""
    lines = (text or "").splitlines()
    inside, grab, out = False, False, []
    for line in lines:
        if line.startswith("## "):
            inside = line[3:].strip().lower().startswith("content")
            if grab:
                break
            continue
        if not inside:
            continue
        m = _DIV_RE.match(line)
        if m:
            if grab:
                break
            grab = int(m.group(1)) == n
            continue
        if grab:
            out.append(line)
    return "\n".join(out)


def parse_division(body):
    """A Story division → (face rows, subsections, paragraphs).
    face rows   the ```text block's `EMOJI LABEL   value` lines, continuation
                lines joined; the Story's compact identity card
    subsections `#### n.m · Title` with the paragraph under each
    paragraphs  loose prose before any subsection (the Pitch is written so)"""
    face, subs, paras = [], [], []
    in_fence, cur_sub, buf = False, None, []
    def flush():
        nonlocal buf
        t = " ".join(x.strip() for x in buf if x.strip())
        if t:
            (subs[-1][1].append(t) if cur_sub is not None else paras.append(t))
        buf = []
    for line in (body or "").splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            m = re.match(r"^\s*([^\w\s]+)?\s*([A-Z][A-Z /-]{1,24}?)\s{2,}(.*)$", line)
            if m and m.group(2).strip():
                face.append([m.group(2).strip().title(), m.group(3).strip()])
            elif face and line.strip():
                face[-1][1] += " " + line.strip()
            continue
        m = re.match(r"^####\s+(.*?)\s*$", line)
        if m:
            flush()
            cur_sub = m.group(1)
            subs.append([cur_sub, []])
            continue
        if not line.strip():
            flush()
            continue
        if line.startswith("**") and cur_sub is None and not paras:
            continue          # the division's bold lead line is a label, not content
        buf.append(line)
    flush()
    return face, subs, paras


_ABBR = ("e.g.", "i.e.", "et al.", "vs.", "cf.", "Fig.", "Eq.", "No.", "Dr.", "St.", "U.S.")


def sentences(text):
    """Split prose at sentence ends. A decimal (1.19) never splits, because the
    split needs white space after the mark; a known abbreviation rejoins."""
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Z(\[“\"'])", (text or "").strip())
    out = []
    for part in parts:
        if out and out[-1].endswith(_ABBR):
            out[-1] += " " + part
        else:
            out.append(part)
    return [x for x in out if x]


def prose(paragraphs):
    """Story prose for a reading cell: paragraphs stay apart, and a long
    paragraph is set one sentence per line (display only; the source is untouched)."""
    paras = [paragraphs] if isinstance(paragraphs, str) else list(paragraphs)
    html_ = []
    for par in paras:
        sents = sentences(par)
        if len(par) > 300 and len(sents) > 1:
            html_.append('<span class="para">%s</span>' % " ".join('<span class="sent">%s</span>' % inline(x) for x in sents))
        else:
            html_.append('<span class="para">%s</span>' % inline(par))
    return " ".join(html_)


def inline(text):
    """Escape prose, then render the two inline marks a Story uses:
    `code` → <code>, **bold** → <b>. Nothing else is interpreted."""
    t = esc(text or "")
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    return t


_LOCAL_RUN_RE = re.compile(r"`?(run-[\w.-]+)`?")
_MODES = ("reuse", "rerun", "new-run", "new run", "new-task", "new round", "registered", "complete")


def _parse_supporting(value):
    """`Execution · reuse · b03j02t01r04; Discovery · reuse · b01j01t02r02` →
    [{owner, mode, addr, raw}]. `[]` and blanks name nothing."""
    out = []
    v = (value or "").strip()
    if not v or v in ("[]", "—", "-", "none"):
        return out
    for part in v.split(";"):
        part = part.strip()
        if not part:
            continue
        toks = [t.strip().strip("`") for t in part.split("·")]
        addrs = _addresses(part)
        out.append({"owner": toks[0] if toks else "", "mode": " · ".join(toks[1:-1]) if len(toks) > 2 else "",
                    "addr": addrs[0] if addrs else "", "raw": part})
    return out


def _parse_local(value):
    """`Page · Evidence Item · reuse · run-value-0901-score → results/…/result.yaml` → {mode, run, result}."""
    v = (value or "").strip()
    left, _, right = v.partition("→")
    m = _LOCAL_RUN_RE.search(left)
    mode = next((t for t in _MODES if re.search(r"(^|·)\s*%s\s*(·|$)" % re.escape(t), left)), "")
    return {"mode": mode, "run": m.group(1) if m else "", "result": right.strip().strip("`"), "raw": v}


def _page_items(folder, stem):
    """The typed Evidence Item contract of one page: id · type · target · desc
    · Label · Expected · Supporting Runs · Local Run · Verified/Status.
    `### E…` is a live item; `#### E…` is a retired one (kept, marked). An item
    ends at the next heading of ANY level, so a retired block never leaks into
    the live item above it."""
    items = read(plan_dir(folder) / (stem + "-evidence-items.md"))
    out = []
    for m in re.finditer(r"^(#{3,4})\s+(E\d{2})-([A-Z]+)-([\w-]+)\s*·\s*(.*)$", items, re.M):
        retired = len(m.group(1)) == 4
        rest = [x.strip() for x in m.group(5).split("·")]
        target = rest[0] if (not retired and len(rest) > 1) else ""
        desc = " · ".join(rest[1:] if target else rest)
        tail = items[m.end():]
        nx = re.search(r"\n#{1,6}\s", tail)
        body = tail[:nx.start()] if nx else tail
        f = {k.strip().lower(): v.strip() for k, v in re.findall(r"^- \*\*([\w ]+)\*\*:\s*(.*)$", body, re.M)}
        out.append({"id": "%s-%s-%s" % m.group(2, 3, 4), "type": m.group(3), "target": target,
                    "desc": desc, "label": f.get("label", ""), "retired": retired,
                    "expected": f.get("expected", ""),
                    "supporting": _parse_supporting(f.get("supporting runs", "")),
                    "local": _parse_local(f.get("local run", "")),
                    "status": _item_status(f, _parse_local(f.get("local run", "")), folder)})
    return out


def _item_status(fields, local, folder):
    """An Evidence Item's state from its own lines. An explicit Status wins; else the
    Local Run's Result on disk says it is ready (items keep no Status line, so every
    card used to read "contract only", JL 260928); else a named Local Run is planned."""
    explicit = fields.get("status") or fields.get("accepted") or fields.get("verified")
    if explicit:
        return explicit
    result = (local.get("result") or "").split()
    if result and (folder / result[0]).is_file():
        return "Result ready"
    if local.get("mode") == "complete":
        return "Result not found"
    return "run planned" if local.get("run") or local.get("mode") else "contract only"


def item_name(item_id):
    """`E03-VALUE-lbp-main-effect` → `Evalue03`: type first, never a bare E03 (JL 260928)."""
    m = re.match(r"E(\d+)-([A-Z]+)", item_id or "")
    return "E%s%s" % (m.group(2).lower(), m.group(1)) if m else item_id


def hero_evidence(d):
    """The few Results the paper hangs on: every DISPLAY item on a Main or
    Appendix page (what the paper prints) and every VALUE item on the Abstract
    page (what the paper states first). Section pages keep their full Evidence Space."""
    b = d["board"]
    out = []
    for p in d["sections"]:
        folder_name = p["group"]["folder"] or (Path(p["rel"]).parts[0] if p["rel"] else "")
        if not p["rel"] or not folder_name.endswith(("-Main", "-Appendix")):
            continue
        folder = (b / p["rel"]).parent
        abstract = p["stem"].lower().endswith("abstract")
        for it in _page_items(folder, p["stem"]):
            if it["retired"]:
                continue
            if it["type"] in ("DISPLAY", "TABLE") or (abstract and it["type"] == "VALUE"):
                it.update({"page": p["stem"], "rel": p["rel"],
                           "part": "appendix" if folder_name.endswith("-Appendix") else "main",
                           "why": "printed display" if it["type"] != "VALUE" else "stated in the Abstract"})
                out.append(it)
    return out


def supporting_tree(d):
    """The owner-native Runs this paper's Evidence Items cite, as a
    Block › Job › Task › Run tree per owner (Execution = the Task home,
    Discovery = the Discovery home). Each Run lists who uses it."""
    b = d["board"]
    cited, loose = {}, []
    for p in d["pages"]:
        if not p["rel"]:
            continue
        for it in _page_items((b / p["rel"]).parent, p["stem"]):
            if it["retired"]:
                continue
            for sp in it["supporting"]:
                owner = "Discovery" if sp["owner"].lower().startswith("discover") else "Execution"
                user = {"page": p["stem"], "rel": p["rel"], "item": it["id"], "label": it["label"], "mode": sp["mode"]}
                if not sp["addr"]:
                    loose.append(dict(user, owner=owner, raw=sp["raw"]))
                    continue
                cited.setdefault((owner, sp["addr"]), []).append(user)
    trees = {"Execution": d["blocks"]["tree"], "Discovery": d["disc"]["tree"]}
    out = {"Execution": {}, "Discovery": {}, "loose": loose, "n": len(cited)}
    for (owner, addr), users in sorted(cited.items()):
        m = re.match(r"^(b\d{2})(j\d{2})?(t\d{2})?(r\d{2})?$", addr)
        if not m:
            continue
        bb, jj, tt, rr = m.groups()
        blk = next((x for x in trees[owner] if x["addr"] == bb), None)
        job = next((x for x in (blk["jobs"] if blk else []) if x["addr"] == bb + (jj or "")), None) if jj else None
        task = next((x for x in (job["tasks"] if job else []) if x["addr"] == bb + (jj or "") + (tt or "")), None) if tt else None
        found = []
        if task is not None and rr:
            found = [(stem, path) for stem, path in task["ticket_list"] if stem == rr or stem.startswith(rr + "_")]
        status = ""
        for stem, _ in found:
            status = task["receipt_map"].get(stem, status)
        node = out[owner].setdefault(bb, {"blk": blk, "jobs": {}})
        jnode = node["jobs"].setdefault(jj or "", {"job": job, "tasks": {}})
        tnode = jnode["tasks"].setdefault(tt or "", {"task": task, "runs": []})
        tnode["runs"].append({"addr": addr, "r": rr or "", "tickets": found, "status": status, "users": users,
                              "on_disk": bool(found) if rr else (task is not None if tt else job is not None)})
    return out


def gates(d):
    """G0–G5 as haipipe-paper-workflow names them, each read from a file, never
    inferred from a percentage. A gate no file can answer says so."""
    b = d["board"]
    g = []
    s00 = d["story00"]
    folder = (b / s00["rel"]).parent if s00 and s00["rel"] else None
    receipt = folder is not None and any((folder / r).is_file() for r in
                                         ("workflow/selection.yaml", "handoff/paper-ideation.yaml"))
    g.append(("G0", "Ideation → Story",
              "✅ I3 receipt · %d Story page(s)" % len(d["stories"]) if receipt
              else "⬜ open · no I3 receipt · %d Story page(s)" % len(d["stories"])))
    g.append(("G1", "Story → work", "— read on the Story's workflow records"))
    g.append(("G2", "work → Story", "— read on the Story's §5 evidence rows"))
    rows = sum(len(s["sections"]) for s in d["story"])
    minted = sum(1 for s in d["story"] for r in s["sections"] if r["rel"])
    g.append(("G3", "Story → Section",
              "%d of %d Section Narrative rows have a Section page" % (minted, rows) if rows else "⬜ no Section Narrative rows"))
    man = b / "delivery" / "build-manifest.json"
    if man.is_file():
        try:
            j = json.loads(man.read_text(encoding="utf-8"))
            rd = j.get("readiness") or {}
            g.append(("G4", "Section → Compile", "%s · %s/%s pages ready" % (
                j.get("status", "?"), rd.get("ready", "?"), rd.get("total", "?"))))
        except (OSError, ValueError):
            g.append(("G4", "Section → Compile", "manifest unreadable"))
    else:
        g.append(("G4", "Section → Compile", "⬜ no build · delivery/build-manifest.json absent"))
    g.append(("G5", "Round → next route", "%d Round page(s)" % len(d["rounds"])
              if d["rounds"] else "⬜ no Round yet"))
    return g


def _stamp(path):
    try:
        return datetime.fromtimestamp(Path(path).stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    except OSError:
        return ""


def _mtime(path):
    try:
        return Path(path).stat().st_mtime
    except OSError:
        return 0.0


def _size(path):
    try:
        n = float(Path(path).stat().st_size)
    except OSError:
        return ""
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return ("%d B" % n) if u == "B" else "%.1f %s" % (n, u)
        n /= 1024.0
    return ""


def _toml_scalars(text):
    """`[section]` + `key = "value"` → {"section.key": value}; enough for paper-build.toml."""
    out, sect = {}, ""
    for line in (text or "").splitlines():
        t = line.strip()
        m = re.match(r"^\[([\w.-]+)\]", t)
        if m:
            sect = m.group(1)
            continue
        m = re.match(r'^([\w-]+)\s*=\s*"([^"]*)"', t) or re.match(r"^([\w-]+)\s*=\s*([^#\s]+)", t)
        if m:
            out[(sect + "." if sect else "") + m.group(1)] = m.group(2)
    return out


def _links(text):
    """The board's `## Links` rows: name  path."""
    out, on = {}, False
    for line in (text or "").splitlines():
        if line.startswith("## "):
            on = line.strip() == "## Links"
            continue
        m = re.match(r"^([\w-]+)\s{2,}(\S.*?)\s*$", line) if on else None
        if m:
            out[m.group(1)] = m.group(2)
    return out


def delivery_info(d):
    """What leaves the paper: delivery/ (generated whole by haipipe-paper-assemble),
    its manifest, the compile order with every Section page's fragment and lanes,
    the display register, the checks, the Round pages and returned manuscripts."""
    b = d["board"]
    text = read(b / "board.md")
    ddir = b / "delivery"
    info = {"dir": ddir if ddir.is_dir() else None, "manifest": None, "toml": {}, "outputs": [],
            "returned": [], "order": [], "order_src": "", "pages": [], "displays": [], "display_note": "",
            "assets": [], "links": _links(text), "built": "", "stale": [], "rounds": []}
    for p in d["rounds"]:
        t = p["text"]
        folder = (b / p["rel"]).parent if p["rel"] else None
        subs = [x.name for x in sorted(folder.iterdir()) if x.is_dir() and not x.name.startswith(".")] if folder else []
        info["rounds"].append({"stem": p["stem"], "rel": p["rel"], "state": scalar(t, "state"),
                               "kind": scalar(t, "round-kind"), "from": scalar(t, "received-from"),
                               "at": scalar(t, "received-at"), "due": scalar(t, "response-due"),
                               "base": scalar(t, "base-build"), "venue": scalar(t, "venue-page"), "subs": subs})
    if info["dir"] is None:
        return info
    toml = _toml_scalars(read(ddir / "paper-build.toml"))
    info["toml"] = toml
    man = None
    if (ddir / "build-manifest.json").is_file():
        try:
            man = json.loads(read(ddir / "build-manifest.json"))
        except ValueError:
            man = {"error": "build-manifest.json is not valid JSON"}
    info["manifest"] = man
    info["built"] = (man or {}).get("built", "") or ""
    built_t = 0.0
    if info["built"]:
        try:
            built_t = datetime.fromisoformat(info["built"]).timestamp()
        except ValueError:
            built_t = 0.0
    # outputs: what paper-build.toml [outputs] names, else what sits in latex/ and word/
    named = [(k.split(".", 1)[1], v) for k, v in toml.items() if k.startswith("outputs.") and
             k.split(".", 1)[1] in ("main_pdf", "main_docx", "supplement_pdf", "supplement_docx")]
    # the cover letter shows on its own Delivery tab (_cover_panes), never beside the manuscript
    if not named:
        named = [("pdf", str(x.relative_to(ddir))) for x in sorted((ddir / "latex").glob("*.pdf")) if (ddir / "latex").is_dir()] + \
                [("docx", str(x.relative_to(ddir))) for x in sorted((ddir / "word").glob("*.docx")) if (ddir / "word").is_dir()]
    for what, rel in named:
        f = ddir / rel
        info["outputs"].append({"what": what.replace("_", " "), "rel": "delivery/" + rel, "path": f, "exists": f.is_file(),
                                "size": _size(f), "stamp": _stamp(f),
                                "stale": bool(f.is_file() and built_t and _mtime(f) + 5 < built_t)})
    if (ddir / "word-feedback").is_dir():
        for f in sorted(ddir / "word-feedback").iterdir() if False else sorted((ddir / "word-feedback").iterdir()):
            if f.is_file() and not f.name.startswith("."):
                info["returned"].append({"name": f.name, "rel": "delivery/word-feedback/" + f.name, "path": f,
                                         "size": _size(f), "stamp": _stamp(f)})
    # compile order: the manifest's, else the Story's §8 block
    order = []
    if man and isinstance(man.get("order"), dict):
        order = [(x, "main") for x in man["order"].get("main", [])] + [(x, "appendix") for x in man["order"].get("appendix", [])]
        info["order_src"] = "build-manifest.json (%s)" % (man.get("order_source") or "").split(" · ")[0]
    elif d["story"] and d["story"][0]["order"]:
        order = [(x, "main" if "-Main-" in x else "appendix") for x in d["story"][0]["order"]]
        info["order_src"] = "Story §8 compile order (no build yet)"
    info["order"] = order
    mpages = {p.get("id"): p for p in (man or {}).get("pages", []) if isinstance(p, dict)}
    by_stem = {p["stem"]: p for p in d["pages"]}
    for pid, part in order:
        pg = by_stem.get(pid)
        rel = pg["rel"] if pg else ""
        folder = (b / rel).parent if rel else None
        md_t = _mtime(b / rel) if rel else 0.0
        frag = folder / "delivery" / "latex" / (pid + ".tex") if folder else None
        lanes = []
        if folder:
            lat = folder / "delivery" / "latex"
            pdfs = [x for x in (lat.glob(pid + "*.pdf") if lat.is_dir() else [])]
            lanes.append(("📜", "latex", bool(pdfs), max((_mtime(x) for x in pdfs), default=0.0)))
            wd = folder / "delivery" / "word" / (pid + ".docx")
            lanes.append(("📝", "word", wd.is_file(), _mtime(wd)))
            web = folder / "delivery" / "web" / "index.html"
            lanes.append(("🌐", "web", web.is_file(), _mtime(web)))
        mp = mpages.get(pid, {})
        stale = bool(rel and built_t and md_t > built_t + 5)
        if stale:
            info["stale"].append(pid)
        info["pages"].append({"id": pid, "part": part, "rel": rel, "state": scalar(pg["text"], "state") if pg else "",
                              "minted": bool(rel), "frag": bool(frag and frag.is_file()),
                              "frag_stale": bool(frag and frag.is_file() and md_t > _mtime(frag) + 5),
                              "lanes": lanes, "ready": mp.get("ready"), "reasons": mp.get("reasons") or [],
                              "warnings": mp.get("warnings") or [],
                              "outline": ((mp.get("outline") or {}).get("version") or ""),
                              "approval": ((mp.get("outline") or {}).get("approval") or "").split(" · ")[0],
                              "stale": stale})
    reg = read(ddir / "display-register.md")
    m = re.search(r"^Built .*$", reg, re.M)
    info["display_note"] = m.group(0) if m else ""
    fence = re.search(r"```text\n(.*?)```", reg, re.S)
    if fence:
        for line in fence.group(1).splitlines():
            if not line.strip() or line.startswith("PRINTED"):
                continue
            cells = re.split(r"\s{2,}", line.strip())
            if len(cells) >= 4:
                info["displays"].append(cells + [""] * (5 - len(cells)))
    sa = ddir / "latex" / "submission-assets"
    if sa.is_dir():
        info["assets"] = [{"name": x.name, "rel": "delivery/latex/submission-assets/" + x.name, "path": x, "size": _size(x)}
                          for x in sorted(sa.iterdir()) if x.is_file() and not x.name.startswith(".")]
    return info


def _table(headers, rows):
    if not rows:
        return ""
    h = "".join("<th>%s</th>" % esc(x) for x in headers)
    body = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return '<table class="grid"><tr>%s</tr>%s</table>' % (h, body)


def _empty(msg):
    return '<div class="mut">%s</div>' % esc(msg)


def _link(d, rel, label, **extra):
    if not rel:
        return esc(label)
    return '<a href="%s">%s</a>' % (esc(outline_url(d["path"], rel, **extra)), esc(label))


def _kv(rows, cls=""):
    """Label/value rows as a table with cell edges. A row with no label, or
    whose value is itself a table or a tree, spans the full width instead of
    nesting a grid inside a narrow cell."""
    out = []
    for l, v in rows:
        wide = (not l) or "<table" in v or 'class="tree-' in v
        if wide:
            cap = ('<div class="kv-cap">%s</div>' % esc(l)) if l and "<table" not in v and 'class="tree-' not in v else ""
            out.append('<div class="item-row %s nolabel">%s<span>%s</span></div>' % (cls, cap, v))
        else:
            out.append('<div class="item-row %s"><b>%s</b><span>%s</span></div>' % (cls, esc(l), v))
    return '<div class="kv">%s</div>' % "".join(out) if out else ""


def _card(cid, kind, label, sub, where, status, status_cls, rows, key="", attrs="", body="", fold=False):
    """One collapsed card, the Evidence-card shape: chevron · kind pill · label
    with a muted subline · where · status; open = label/value rows. `key` is what
    opening the card selects in its Space's Runs panel."""
    # `body` leads the opened card; `fold` tucks the label/value rows under a closed Details line
    detail = body + (('<details class="row-details"><summary>Details</summary>%s</details>' % _kv(rows))
                     if fold and rows else _kv(rows))
    # say a thing once: a subline that is empty, a dash, or the same words as `where` is dropped
    plain = lambda h: re.sub(r"<[^>]+>", "", h or "").strip()
    subline = "" if plain(sub) in ("", "—") or plain(sub) == plain(where) else '<span class="item-title">%s</span>' % sub
    return ('<details class="item-card" id="%s"%s%s><summary><div class="item-summary">'
            '<span class="item-chevron">›</span><span class="item-kind">%s</span>'
            '<div class="item-main"><span class="item-label">%s</span>%s</div>'
            '<span class="item-where">%s</span><span class="item-status %s">%s</span>'
            '</div></summary><div class="item-detail">%s</div></details>'
            % (esc(cid), (' data-key="%s"' % esc(key)) if key else "", attrs, esc(kind), esc(label), subline,
               where, status_cls, esc(status), detail))


def _status_cls(text):
    t = (text or "").upper()
    if t.startswith("NOT ") or t.startswith("NO ") or "ABSENT" in t or "MISSING" in t:
        return "mut"
    if "✅" in t or "PROCEED" in t or "ESTABLISHED" in t or "ALLOCATED" in t or "READY" in t or "ACCEPTED" in t:
        return "ok"
    if "⚠" in t or "🔨" in t or "PROVISIONAL" in t or "PARTIAL" in t or "WAITING" in t:
        return "warn"
    return "mut"


def _fields(headers, cells, skip):
    return [(headers[i] if i < len(headers) else "col %d" % (i + 1), esc(cells[i]))
            for i in range(len(cells)) if i not in skip and cells[i] and cells[i] not in ("—", "-")]


def _field_html(paras):
    """A **Field** block: bullet lines become a list, other lines a paragraph."""
    items = [l for l in paras if l.lstrip().startswith("- ")]
    text = [l for l in paras if not l.lstrip().startswith("- ")]
    html_ = esc(" ".join(text))
    if items:
        html_ += '<ul class="item-bullets">%s</ul>' % "".join(
            "<li>%s</li>" % esc(l.lstrip()[2:]) for l in items)
    return html_


def _idea_card(d, i, x):
    substance = x.get("substance") or []
    def _first(*starts):
        return next((" ".join(v) for k, v in substance if k.lower().startswith(starts)), "")
    # The card leads with the question the Idea asks (JL 260922: "the ideation should be the
    # research question, which can trigger the reader to think"); the title drops to the subline.
    rq = _first("research question", "question")
    hyp = _first("hypothesis", "one-sentence")
    label, sub = (rq, esc(x["title"])) if rq else (x["title"], esc(hyp))
    if rq and " ".join(x["title"].split()).rstrip("?").lower() == " ".join(rq.split()).rstrip("?").lower():
        sub = esc(hyp)        # the table's idea cell is the question itself: say the guess, not the question twice
    verdict = x.get("verdict") or "⬜ open"
    went = x.get("went") if x.get("went") not in (None, "", "—", "-") else ""
    rows = [(k, _field_html(v)) for k, v in substance]
    if x["bullets"]:
        blist = []
        for bl in x["bullets"]:
            note = " ".join(bl["notes"])
            blist.append('<li><b>%s</b> %s%s%s</li>' % (
                esc(bl["bullet"]), esc(bl["head"]),
                ('<div class="item-note">%s</div>' % esc(note)) if note else "",
                ('<div class="item-note">Evidence: %s</div>' % esc(bl["evidence"])) if bl["evidence"] else ""))
        rows.append(("", '<details class="item-plan"><summary>Writing plan</summary><ul class="item-bullets">%s</ul></details>'
                     % "".join(blist)))
    if x["items"]:
        rows.append(("Evidence items", "".join(
            '<div><span class="idtag">%s</span> %s <span class="%s">%s</span></div>' % (
                esc(it["id"]), esc(it["desc"]), "ok" if "✅" in it["verified"] else "mut", esc(it["verified"]))
            for it in x["items"])))
    fields = [(l, esc(v)) for l, v in x.get("fields", []) if l.lower() not in ("verdict", "went to")]
    if fields:
        rows.append(("Comparison", "".join('<div><b class="item-sub">%s</b> %s</div>' % (esc(l), v) for l, v in fields)))
    if " · " in verdict:
        rows.append(("Verdict", esc(verdict)))
    if went:
        rows.append(("Went to", esc(went)))       # G0: where the admitted idea went
    short = verdict.split(" · ")[0].strip()       # the closed line keeps the title readable
    return _card("idea-" + x["id"], x["id"], label, sub, esc(went), short, _status_cls(verdict), rows,
                 key=_norm_key("i", x["id"]))


def _col(headers, needles, default):
    """Index of the first header naming one of `needles` (case-insensitive), else `default`."""
    for i, h in enumerate(headers):
        if any(n in h.lower() for n in needles):
            return i
    return default


_ROW_ID = re.compile(r"(?<![\w.])(RQ|[ETBDQHC])-?0*(\d+)(?:\s*[–-]\s*(?:\1-?)?0*(\d+))?(?![\w-]|\.\w)")


def _row_ids(text):
    """The Story row ids a cell names (`RQ2`, `E4`, `T1`, `B3`, `D5`, `Q2`, and the §3
    question blocks' `H1` hypotheses and `C1` claims); a range (`E1-E4`, `RQ1–RQ7`) names
    each one. An Evidence Item id (`E01-CITE-…`) and a Bullet address (`C1.P1.B1`) are
    not row ids."""
    out = []
    for m in _ROW_ID.finditer(text or ""):
        lo = int(m.group(2))
        hi = int(m.group(3)) if m.group(3) and int(m.group(3)) >= lo else lo
        for n in range(lo, min(hi, lo + 50) + 1):
            if "%s%d" % (m.group(1), n) not in out:
                out.append("%s%d" % (m.group(1), n))
    return out


def _row_key(cell):
    """`E2 (C1)` → `E2`, `T01` → `T1`: the id a row's first cell carries."""
    ids = _row_ids(cell)
    return ids[0] if ids else (cell or "").strip()


def _plain(text):
    """A field value → plain text: links to their label, no bold or code marks. Unlike
    clean(), a file name keeps its underscores."""
    text = _LINK_RE.sub(r"\1", text or "")
    return re.sub(r"\s+", " ", re.sub(r"\*\*|`", "", text)).strip()


_QHEAD = re.compile(r"^####\s+[\d.]+\s*·\s*Question\s+(\d+)(?:\s*·\s*(RQ\d+))?\s*$", re.I)
_GROUP = re.compile(r"^\*\*(tasks|hypotheses|potential claims|potential contributions|potential work)\*\*\s*:?\s*$", re.I)
_ITEM = re.compile(r"^-\s+(?:\*\*([A-Z]{1,2}\d+|\d+[a-z])\*\*\s*(?:·\s*)?)?(.*)$")
_CODE = re.compile(r"(?<![\w.])(\d+[a-z])(?!\w)")
_SUBFIELD = re.compile(r"\*\*(.+?)\*\*\s*:\s*(.*?)(?=\s*·\s*\*\*|$)")
_GROUPS = {"tasks": "tasks", "hypotheses": "hypotheses", "potential claims": "claims",
           "potential contributions": "contributions", "potential work": "work"}


def question_blocks(text):
    """§3 written as one block per question (JL 260929; haipipe-paper-story 0.12.0):
    `#### 3.N · Question N · RQn`, the question's `- **Field**: value` lines, then four
    groups, each a bold label and one `- ` line per item, coded by question (1a, 1b, 2a …;
    haipipe-paper-story 0.13.0), each a short name, a colon and one plain sentence:
      **Hypotheses**               - **1a** · Name: sentence · tested by E1, E2
      **Potential claims**         - **1a** · C1 · from 1a · Name: sentence   (indented `- **Role**: …`)
      **Potential contributions**  - rests on 1a, 1b · Name: sentence
      **Potential work**           - **T1** · for 1a, 1b   (optionally `· b04.j03.t01, …` to narrow)
    A question that sets the study's tasks rather than testing a guess may open with
      **Tasks**                    - Pretraining · Name: sentence   (the kind, then the task)
    A claim keeps its paper-wide id (C1) after its code. [] for a Story that still
    writes the RQ table."""
    n = next((n for n, title in divisions(text) if title.strip().lower().startswith("research question")), None)
    out, cur, group, last = [], None, None, None
    for line in (division_body(text, n) if n is not None else "").splitlines():
        s = line.strip()
        m = _QHEAD.match(s)
        if m:
            cur = {"n": int(m.group(1)), "id": m.group(2) or "RQ" + m.group(1), "fields": [], "tasks": [],
                   "hypotheses": [], "claims": [], "contributions": [], "work": []}
            out.append(cur)
            group = last = None
            continue
        if line.startswith("#"):
            cur = group = last = None
            continue
        if cur is None or not s:
            continue
        g = _GROUP.match(s)
        if g:
            group, last = _GROUPS[g.group(1).lower()], None
            continue
        if group is None:
            f = _FIELD.match(s)
            if f:
                cur["fields"].append((f.group(1).strip(), _plain(f.group(2))))
            continue
        if line[:1] == "-":
            m = _ITEM.match(s)
            last = {"id": m.group(1) or "", "fields": [],
                    "parts": [x.strip() for x in _plain(m.group(2)).split(" · ") if x.strip()] or [""]}
            cur[group].append(last)
        elif last is not None and s.startswith("- "):            # an indented `- **Role**: …` line
            last["fields"] += [(k.strip(), _plain(v)) for k, v in _SUBFIELD.findall(s[2:])]
        elif last is not None:                                    # a wrapped line continues the item
            last["parts"][-1] = (last["parts"][-1] + " " + _plain(s)).strip()
    return out


def _field(fields, *names):
    return next((v for k, v in fields if k.strip().lower() in names), "")


def _part(parts, word):
    """The rest of the part that starts with `word` (`tested by`, `from`, `for`, …)."""
    return next((x[len(word):].strip() for x in parts if x.lower().startswith(word)), "")


_STAGES = ("data", "training", "evaluation", "results", "analysis", "figures")
_STAGE_ORDER = {k: i for i, k in enumerate(_STAGES + ("task", "discovery"))}


def _work_rows(s):
    """The §7 Task and §6 Discovery rows: id → its short name (a `name` cell) and the
    plain sentence under it (its `question` cell), or the question alone as its name when
    the row has no `name` cell; its stage (a §7 `stage` cell: data · training · evaluation ·
    results · analysis · figures), whether it serves `every question`, and the row ids it names."""
    work = {}
    for kind, rows, heads in (("task", s["tt"], s["tt_h"]), ("disc", s["dd"], s["dd_h"])):
        iq = next((i for i, h in enumerate(heads) if h.strip().lower() == "question"), 1)
        ist = next((i for i, h in enumerate(heads) if h.strip().lower() == "stage"), None)
        inm = next((i for i, h in enumerate(heads) if h.strip().lower() == "name"), None)
        for c in rows:
            stage = (c[ist].strip().lower() if ist is not None and ist < len(c) else "") or (
                "discovery" if kind == "disc" else "task")
            q = c[iq] if len(c) > iq else c[0]
            nm = c[inm].strip() if inm is not None and inm < len(c) else ""
            work[_row_key(c[0])] = {"id": _row_key(c[0]), "kind": kind, "cells": c, "stage": stage,
                                    "name": nm or q, "text": q if nm else "",
                                    "shared": any("every question" in x.lower() for x in c[1:]),
                                    "names": set(_row_ids(" ".join(c[1:])))}
    return work


def story_tree(s):
    """High-level logic joined to low-level work (JL 260929). §3 question blocks give each
    question its hypotheses (each names the §5 rows testing it), potential claims (each
    from a hypothesis), potential contributions (each resting on claims) and potential
    work (each §7/§6 row for the hypotheses it tests). A Story that still writes the RQ
    table gets one hypothesis per §5 row and its work read from either end of the §5↔§7
    links. §7 rows marked `every question` are the shared work; `up` maps each work row
    to every hypothesis, §5 row and question above it, which keys its Runs panel runs."""
    work = _work_rows(s)
    irq = _col(s["e_h"], ("rq", "question"), 1)
    ip = _col(s["e_h"], ("proposition", "claim"), 3)
    ist = _col(s["e_h"], ("support", "state", "status"), 2)
    tests = {}
    for c in s["e"]:
        if re.match(r"E-?\d+", c[0]):
            e, said = _row_key(c[0]), set(_row_ids(" ".join(c[1:])))
            tests[e] = {"id": e, "cells": c, "prop": c[ip] if len(c) > ip else "",
                        "state": c[ist] if len(c) > ist else "",
                        "rqs": [x for x in _row_ids(c[irq] if len(c) > irq else "") if x.startswith("RQ")],
                        "work": [w for w in work if w in said or e in work[w]["names"]]}
    qs = []
    for b in s.get("qb") or []:
        q = {"id": b["id"], "text": _field(b["fields"], "question") or b["id"], "fields": b["fields"],
             "tasks": [{"kind": x["parts"][0], "text": " · ".join(x["parts"][1:])} for x in b.get("tasks", [])],
             "hyps": [], "claims": [], "contribs": [], "items": [], "notes": {}}
        for h in b["hypotheses"]:
            if h["id"]:
                q["hyps"].append({"id": h["id"], "tests": [x for x in _row_ids(_part(h["parts"], "tested by")) if x in tests],
                                  "phrase": next((x for x in h["parts"] if not x.lower().startswith("tested by")), h["id"])})
            else:
                q["notes"]["hypotheses"] = " · ".join(h["parts"])
        for c in b["claims"]:
            if c["id"]:
                alias = next((x for x in c["parts"] if re.fullmatch(r"C\d+", x)), "")
                q["claims"].append({"id": c["id"], "alias": alias, "from": _CODE.findall(_part(c["parts"], "from ")),
                                    "fields": c["fields"],
                                    "text": " · ".join(x for x in c["parts"] if x != alias and not x.lower().startswith("from "))})
            else:
                q["notes"]["claims"] = " · ".join(c["parts"])
        for c in b["contributions"]:
            rests = _CODE.findall(_part(c["parts"], "rests on"))
            text = " · ".join(x for x in c["parts"] if not x.lower().startswith("rests on"))
            if rests:
                q["contribs"].append({"rests": rests, "text": text})
            else:
                q["notes"]["contributions"] = text
        for w in b["work"]:
            wid = _row_key(w["id"]) if w["id"] else ""
            if wid in work:
                q["items"].append({"w": wid, "for": _CODE.findall(_part(w["parts"], "for ")),
                                   "addrs": _addresses(" ".join(x for x in w["parts"] if not x.lower().startswith("for ")))})
        qs.append(q)
    if not s.get("qb"):                     # the RQ table: one hypothesis per §5 row naming the RQ
        for r in s["rq"]:
            rid, said = _row_key(r[0]), set(_row_ids(" ".join(r[1:])))
            hyps = [{"id": e, "phrase": x["prop"], "tests": [e]} for e, x in tests.items() if rid in x["rqs"]]
            items = []
            for w in work:
                fr = [h["id"] for h in hyps if w in tests[h["id"]]["work"]]
                if fr or w in said or rid in work[w]["names"]:
                    items.append({"w": w, "for": fr, "addrs": []})
            heads = s["rq_h"]
            qs.append({"id": rid, "text": r[1] if len(r) > 1 else rid, "hyps": hyps, "claims": [], "contribs": [],
                       "items": items, "notes": {},
                       "fields": [(heads[i] if i < len(heads) else "col %d" % (i + 1), r[i])
                                  for i in range(2, len(r)) if r[i] and r[i] not in ("—", "-")]})
    shared = [w for w in work if work[w]["shared"]]
    named = {i["w"] for q in qs for i in q["items"]}
    placed = {x for q in qs for h in q["hyps"] for x in h["tests"]}
    up = {w: [] for w in work}
    for q in qs:
        tests_of = {h["id"]: h["tests"] for h in q["hyps"]}
        for i in q["items"]:
            up[i["w"]] += i["for"] + [x for h in i["for"] for x in tests_of.get(h, [])] + [q["id"]]
    orphans = [x for x in tests.values() if x["id"] not in placed]
    for x in orphans:
        for w in x["work"]:
            up[w].append(x["id"])
    asked = {}
    for q in qs:
        for i in q["items"]:
            asked.setdefault(i["w"], []).append((_num(q["id"]), set(i["addrs"])))
    return {"questions": qs, "orphans": orphans, "tests": tests, "work": work, "shared": shared, "asked": asked,
            "up": {w: list(dict.fromkeys(ks)) for w, ks in up.items()},
            "loose": [w for w in work if w not in named and w not in shared]}


def _num(rid):
    m = re.search(r"\d+", rid or "")
    return m.group(0) if m else (rid or "")


def _mark(states):
    """One mark for a hypothesis from the states of the §5 rows that test it: ✅ when
    every row says established (a ✅ alone is not enough, since a Story may write
    `✅ stated · ⬜ unbacked`), ❌ when one is contradicted, 🔨 when one is provisional,
    ⬜ otherwise."""
    low = [(x or "").lower() for x in states]
    if low and all("established" in x for x in low):
        return "✅"
    if any("contradict" in x for x in low):
        return "❌"
    if any("🔨" in x or "provisional" in x for x in low):
        return "🔨"
    return "⬜"


def _nodes(tree, addrs):
    """Addresses (`b04j01t02`, `b04j01`, `b01`) → [(block, [(job, tasks)])] in folder
    order: a block or job address takes all of it, a task address takes that task."""
    out = []
    for blk in tree:
        jobs = []
        for j in blk["jobs"]:
            if any(j["addr"].startswith(a) for a in addrs):
                jobs.append((j, j["tasks"]))
            else:
                ts = [t for t in j["tasks"] if t["addr"] in addrs]
                if ts:
                    jobs.append((j, ts))
        if jobs:
            out.append((blk, jobs))
    return out


def _runs_fold(d, t):
    """R: a task's runs as (`3 runs · no receipts`, one line per run ticket, or per
    `results/<run>/` folder when a Task has results and no tickets), or the "no runs yet"
    mark. A line opens that run's results in the pop-out (JL 260930: "a popout window to
    show the results")."""
    ticks = [stem for stem, _ in (t.get("ticket_list") or [])]
    home = Path(t["dir"])
    if not ticks and (home / "results").is_dir():
        ticks = sorted(x.name for x in (home / "results").iterdir() if x.is_dir() and not x.name.startswith("."))
    n = len(ticks) or t.get("n_results", 0)
    if not n:
        return '<span class="mut bj-rn">no runs yet</span>'
    opens = d.get("root") is not None and ((home / "results").is_dir() or (home / "runs").is_dir())
    line = lambda stem: '<span class="idtag">%s</span> <span class="mut">%s</span>' % (
        esc(stem), esc((t.get("receipt_map") or {}).get(stem) or "no receipt"))
    lines = "".join(('<a class="bj-run" href="%s" target="_blank" data-pop="%s">%s</a>'
                     % (esc(run_result_url(d["root"], home, stem)), esc(stem), line(stem))) if opens else
                    '<div class="bj-run">%s</div>' % line(stem) for stem in ticks)
    return esc("%d run%s · %s" % (n, "" if n == 1 else "s", _fmt_state(t.get("receipts") or {}))), lines


def _bjtr(d, nodes, disc=False):
    """B → J → T → R, one line per level, no boxes (JL 260929)."""
    out = []
    for blk, jobs in nodes:
        out.append('<div class="bj-b"><span class="idtag">%s</span> <b>%s</b></div>' % (esc(blk["addr"]), esc(blk["name"][4:])))
        for j, ts in jobs:
            out.append('<div class="bj-j"><span class="idtag">%s</span> %s</div>' % (esc(j["name"][:3]), esc(j["name"][4:])))
            for t in ts:
                if disc:                         # a Discovery task also says what it found
                    name = _disc_link(d, blk, j, t, t["name"][4:]) + (
                        ' <span class="mut">%s</span>' % esc(t["outcome"] + ((" · " + t["confidence"]) if t.get("confidence") else ""))
                        if t.get("outcome") else "")
                else:
                    # plain text: the link only opened the raw Task Markdown (JL 260930: "I don't
                    # think this is useful, could you remove this link?"); its runs open results
                    name = esc(t["name"][4:])
                head, fold = '<span class="idtag">%s</span> %s' % (esc(t["name"][:3]), name), _runs_fold(d, t)
                # the runs open below the task, one level in, as t sits under j (JL 260930:
                # "make the run below the t02 … follow the same indentation as b and j and t")
                out.append(('<details class="bj-tr"><summary class="bj-t">%s <span class="bj-rs">%s</span></summary>'
                            '<div class="bj-runs">%s</div></details>' % (head, fold[0], fold[1])) if isinstance(fold, tuple)
                           else '<div class="bj-t">%s %s</div>' % (head, fold))
            if not ts:
                out.append('<div class="bj-t mut">no task yet</div>')
    return "".join(out)


def _home_label(home):
    return ((home["dir"].name + "/") if home.get("dir") is not None else "")


def _item_folders(d, T, it):
    """One work item's B → J → T → R: the folders the question block names for it (a
    shared row narrowed to what this question needs), else its row's own addresses.
    Returns (html, size): size is the closed line's count, `4 tasks · 14 runs`."""
    c = T["work"][it["w"]]
    if c["kind"] == "task":
        addrs = it["addrs"] or [x["address"].replace(".", "") for x in task_home(d, c["cells"])["all"]]
        nodes, home = _nodes(d["blocks"]["tree"], set(addrs)), d["blocks"]
    else:
        addrs = it["addrs"] or [x for x in _addresses(" ".join(c["cells"])) if _disc_lookup(d, x)]
        nodes, home = _nodes(d["disc"]["tree"], set(addrs)), d["disc"]
    if nodes:
        tasks = [t for _, jobs in nodes for _, ts in jobs for t in ts]
        runs = sum(len(t.get("ticket_list") or []) or t.get("n_results", 0) for t in tasks)
        size = "%d task%s · %d run%s" % (len(tasks), "" if len(tasks) == 1 else "s", runs, "" if runs == 1 else "s")
        return ('<div class="bj-home mut">%s</div>%s' % (esc(_home_label(home)), _bjtr(d, nodes, disc=c["kind"] == "disc")), size)
    away = re.search(r"\b(examples-[\w.-]+/[\w.@-]+)", " ".join(c["cells"]))
    if away and c["kind"] == "task":                 # built in another project, outside the Task home
        return ('<div class="bj-none mut">built outside %s: <code>%s</code></div>'
                % (esc(_home_label(home) or "this project"), esc(away.group(1))), "built outside " + (_home_label(home) or "this project"))
    return ('<div class="bj-none mut">%sno folder yet</div>' % (esc(_home_label(home) + " · ") if _home_label(home) else ""),
            "no folder yet")


def _and(labels):
    """["Hypothesis 1", "Hypothesis 2"] → "Hypotheses 1 and 2"; one label stays as it is."""
    if len(labels) < 2:
        return "".join(labels)
    kinds = {x.split()[0] for x in labels}
    if len(kinds) == 1:
        nums = [x.split()[-1] for x in labels]
        word = {"Hypothesis": "Hypotheses", "Claim": "Claims"}.get(kinds.pop(), "")
        return "%s %s and %s" % (word, ", ".join(nums[:-1]), nums[-1])
    return ", ".join(labels[:-1]) + " and " + labels[-1]


def _lw_row(key, left, right, cls="lw-g"):
    return ('<div class="lw-row %s"%s><div class="lw-l">%s</div><div class="lw-r">%s</div></div>'
            % (cls, (' data-key="%s"' % esc(key)) if key else "", left, right))


def _label(kind, rid):
    """`Hypothesis 1a` for a §3 code; `Hypothesis 1` for an older id such as E1."""
    return "%s %s" % (kind, rid if re.fullmatch(r"\d+[a-z]", rid or "") else _num(rid))


def _nx(text):
    """`Short name: one sentence` → the name in bold, then the sentence (JL 260929: "both
    the hypotheses and claims to be short-phrase-name: explanation")."""
    m = re.match(r"^([^:]{2,80}):\s+(.+)$", text or "")
    if not m:
        return esc(text)
    return '<b class="lw-name">%s</b>: %s' % (esc(m.group(1)), esc(m.group(2)))


def _hyp_line(key, pill, text, mark="", strong=True):
    """One pickable item on the left: the pill and its mark on one line, the short name
    and sentence starting on the next (JL 260929: "make the text start from the next line
    after the label")."""
    return ('<div class="lw-h"%s><div class="lw-top"><span class="item-kind">%s</span><span class="lw-mark">%s</span></div>'
            '<div class="lw-body">%s</div></div>'
            % ((' data-key="%s"' % esc(key)) if key else "", esc(pill), mark, _nx(text) if strong else esc(text)))


def _also(others):
    if not others:
        return ""
    nums = [str(n) for n in others]
    words = ("Question " + nums[0]) if len(nums) == 1 else "Questions %s and %s" % (", ".join(nums[:-1]), nums[-1])
    return '<span class="lw-also">also for %s</span>' % esc(words)


def _work_item(d, T, it, labels, also=()):
    """One piece of work, named as the question it answers (JL 260929), folded like the
    foundation work (JL 260929: "results 也是可以 click 的，也是可以 collapse 的"). Closed, it
    still shows its stage and short name on one line, the plain sentence below, as a question
    does (JL 260930: "the Label, + Short names, and a new line to explain what it is"), then
    the hypotheses it tests, the other questions that use it and its size; open, its
    B → J → T → R. Opening it selects it for the Runs panel."""
    c = T["work"][it["w"]]
    folders, size = _item_folders(d, T, it)
    fr = [labels.get(h, _label("Hypothesis", h)) for h in it["for"]]
    tags = "".join(x for x in (('<span class="lw-for">for %s</span>' % esc(_and(fr))) if fr else "",
                               _also(also), '<span class="lw-size">%s</span>' % esc(size)) if x)
    from live.work_items import work_item
    return work_item(c["stage"].capitalize(), c["name"], c.get("text", ""), tags, folders,
                     key=it["w"], for_keys=" ".join(it["for"]))


def _band(kind, label, note=""):
    """A group label as a colored band with a left stripe (JL 260929: the group labels were
    "浅浅的"; "变得更显眼一些，或者说你加上一些条纹，把它分隔开")."""
    return '<div class="lw-k lw-k-%s">%s%s</div>' % (kind, esc(label), ('<span class="lw-kn">%s</span>' % esc(note)) if note else "")


def _in_order(T, items):
    """Work in the order it runs: data, training, evaluation, results, analysis, figures,
    then Discovery (JL 260929: "the work should follow the logics")."""
    return [x for _, x in sorted(enumerate(items), key=lambda p: (_STAGE_ORDER.get(T["work"][p[1]["w"]]["stage"], 6), p[0]))]


def _q_block(d, T, q):
    """One question block (JL 260929: the question is the main block): the question across
    the top; left, its tasks (only a question that sets them), its hypotheses, potential claims and potential contributions, coded 1a,
    1b …, each a short name and a sentence; right, its potential work: first the foundation
    every question stands on (§7 rows marked `every question`, folded, marked shared), then
    this question's own work in run order, each named as a question, with its folders."""
    labels = {h["id"]: _label("Hypothesis", h["id"]) for h in q["hyps"]}
    # no group labels (JL 260930: "Hypotheses <--- could we just remove this … of no
    # information", and the same for Foundation work and This question's work): every
    # item's pill names its kind, so each group is only a gap; an empty group says so
    # under its kind's pill. Tasks keeps its label: its pills name only the task.
    none = lambda kind, key: ('<div class="lw-c"><div class="lw-top"><span class="item-kind">%s</span></div>'
                              '<div class="lw-say">%s</div></div>' % (esc(kind), esc(q["notes"].get(key) or "none yet")))
    group = lambda items: '<div class="lw-g">%s</div>' % "".join(items)
    # a question that sets the tasks (JL 260930: "what is the pretraining task, and also the
    # downstream task") lists them first, and shows only the groups it fills
    tasks = q.get("tasks") or []          # the RQ table has none
    groups = [([_band("task", "Tasks")] + [_hyp_line("", x["kind"], x["text"]) for x in tasks]) if tasks else []]
    groups.append([_hyp_line(h["id"], labels[h["id"]], h["phrase"], _mark([T["tests"][x]["state"] for x in h["tests"]]))
                   for h in q["hyps"]] or ([] if tasks else [none("Hypothesis", "hypotheses")]))
    groups.append(['<div class="lw-c"><div class="lw-top"><span class="item-kind">%s</span></div><div class="lw-body">%s</div>'
                   '<div class="lw-say">from %s</div></div>' % (esc(_label("Claim", c["id"])), _nx(c["text"]),
                                                                  esc(_and([labels.get(h, _label("Hypothesis", h)) for h in c["from"]])))
                   for c in q["claims"]] or ([] if tasks else [none("Claim", "claims")]))
    # a contribution is labelled like a claim (JL 260930: "we can have the contribution label
    # as well"), coded by question in its order: Contribution 1a, 1b
    groups.append(['<div class="lw-c"><div class="lw-top"><span class="item-kind">%s</span></div><div class="lw-body">%s</div>'
                   '<div class="lw-say">rests on %s</div></div>'
                   % (esc(_label("Contribution", _num(q["id"]) + "abcdefghijklmnopqrstuvwxyz"[i % 26])), _nx(c["text"]),
                      esc(_and([_label("Claim", x) for x in c["rests"]]))) for i, c in enumerate(q["contribs"])] or (
                       [] if tasks else [none("Contribution", "contributions")]))
    left = [group(g) for g in groups if g]
    listed = {i["w"]: i for i in q["items"]}
    found = _in_order(T, [listed.get(w) or {"w": w, "for": [], "addrs": []} for w in T["shared"]])
    own = _in_order(T, [i for i in q["items"] if i["w"] not in T["shared"]])
    right = [group([_work_item(d, T, it, labels) for it in found])] if found else []
    # "also for" only where another question uses the same folders: a row narrowed to other
    # folders there (each question's own figures) is not shared work
    also = lambda it: [n for n, a in T["asked"].get(it["w"], [])
                       if n != _num(q["id"]) and (not a or not it["addrs"] or a & set(it["addrs"]))]
    right.append(group([_work_item(d, T, it, labels, also=also(it)) for it in own] or ['<div class="lw-say">no work named yet</div>']))
    # closed by default (JL 260930): the questions alone read as the paper's outline
    # the label sits on its own line with the question's short name, the question below it
    # (JL 260930: "Question: short name, then the sentence"), as hypotheses and claims do
    name = _field(q["fields"], "name")
    return ('<details class="qc lw-q" data-key="%s"><summary><span class="bjt-chev">›</span><div class="lw-qhead">'
            '<div class="lw-qtop"><span class="item-kind">Question %s</span>%s</div>'
            '<div class="lw-qtext">%s</div></div></summary>%s</details>'
            % (esc(q["id"]), esc(_num(q["id"])), ('<span class="lw-qname">%s</span>' % esc(name)) if name else "",
               esc(q["text"]), _lw_row("", "".join(left), "".join(right))))


def _rest_block(d, T):
    """What no question holds: §5 rows no hypothesis names, §7/§6 rows no question names,
    and claimed folders no row names."""
    left = [_hyp_line(x["id"], x["id"], x["prop"], _mark([x["state"]]), strong=False) for x in T["orphans"]]
    right = [_work_item(d, T, it, {}) for it in _in_order(T, [{"w": w, "for": [], "addrs": []} for w in T["loose"]])]
    ta, da = _unnamed_addrs(d)
    tn, dn = _nodes(d["blocks"]["tree"], set(ta)), _nodes(d["disc"]["tree"], set(da))
    if tn or dn:
        right.append('<div class="lw-w"><div class="lw-wline"><span class="lw-wq mut">Folders no row names</span></div>%s%s</div>'
                     % (('<div class="bj-home mut">%s</div>%s' % (esc(_home_label(d["blocks"])), _bjtr(d, tn))) if tn else "",
                        ('<div class="bj-home mut">%s</div>%s' % (esc(_home_label(d["disc"])), _bjtr(d, dn, disc=True))) if dn else ""))
    if not left and not right:
        return ""
    return ('<details class="qc lw-q lw-rest"><summary><span class="bjt-chev">›</span>'
            '<span class="lw-qtext">Not under a question</span></summary>%s</details>'
            % _lw_row("", "".join(left) or '<div class="lw-say">every §5 row has a hypothesis</div>', "".join(right)))


def logic_work_html(d):
    """Story › High-level logic + Low-level work (JL 260929): one tree, visually split.
    Each question is a block; its left side is the high-level logic (hypotheses, potential
    claims, potential contributions), its right side the low-level work that tests it,
    each piece named as a question, in the order it runs, with its B → J → T → R."""
    # board.md `story-current:` names the Story being worked on (JL 260930: one paper in this
    # tree, no Story labels); without it every Story's questions are drawn, as before
    cur = scalar(read(d["board"] / "board.md"), "story-current").strip()
    stories = [s for s in d["story"] if s["stem"] == cur] if cur else d["story"]
    blocks = []
    for s in stories or d["story"]:
        T = story_tree(s)
        blocks += [_q_block(d, T, q) for q in T["questions"]]
        blocks.append(_rest_block(d, T))
    if not blocks:
        return '<div class="space-empty">No research question yet.</div>'
    head = _lw_row("", "High-level logic", "Low-level work · B → J → T → R", "lw-head")
    return '<div class="lw">%s%s</div>' % (head, "".join(blocks))


# Story › Related Papers (JL 260930): papers from the venue the paper is written for,
# one card each, the original PDF readable inside the card. The rows are the Story's
# §5.3 P-board; each names the Discovery Paper Run that holds the paper (its Bib,
# abstract, facts and, when a free copy exists, paper.pdf).
RELATED_ROLES = (("closest", "Closest to this paper", "hyp"), ("question", "For one research question", "claim"),
                 ("background", "Background", "found"), ("caution", "Cautions and framing", "contrib"))


def _cell(heads, row, name):
    """The cell under the first header starting with `name` ('' when none)."""
    i = next((k for k, h in enumerate(heads) if h.strip().lower().startswith(name)), None)
    return row[i].strip() if i is not None and i < len(row) else ""


def _disc_run(d, addr):
    """`b01j02t01r03` → that Paper Run's Result folder in the Discovery home, or None."""
    m = re.fullmatch(r"(b\d{2}j\d{2}t\d{2})(r\d{2})", addr or "")
    hit = _disc_lookup(d, m.group(1)) if m else None
    task = hit[2] if hit else None
    return _find(task["dir"] / "results", m.group(2)) if task is not None else None


def _yaml_block(text, block):
    """The `key: value` lines indented under one top-level `block:` of a small YAML file."""
    out, on = {}, False
    for line in (text or "").splitlines():
        if not line.strip():
            continue
        if not line.startswith((" ", "\t")):
            on = line.split(":", 1)[0].strip() == block
            continue
        m = re.match(r"^\s+([\w-]+):\s*(.*?)\s*$", line) if on else None
        if m:
            out.setdefault(m.group(1), m.group(2).strip().strip("\"'"))
    return out


def _scalar_yaml(v):
    """One YAML scalar as `yaml.safe_dump` writes it: plain, 'single' ('' escapes) or "double"."""
    v = v.strip()
    if len(v) > 1 and v[0] == v[-1] == "'":
        return v[1:-1].replace("''", "'")
    if len(v) > 1 and v[0] == v[-1] == '"':
        try:
            return json.loads(v)
        except ValueError:
            return v[1:-1]
    return v


def logic_work_data(path):
    """A Paper Run's logic-work.yaml (haipipe-discovery 0.20): top-level `key: value` scalars and
    `key:` lists of `- item` strings, as the Discovery builder writes them. {} when absent."""
    out, key = {}, None
    for line in read(path).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^-\s+(.*)$", line) or re.match(r"^\s+-\s+(.*)$", line)
        if m and key:
            out.setdefault(key, [])
            if isinstance(out[key], list):
                out[key].append(_scalar_yaml(m.group(1)))
            continue
        m = re.match(r"^([\w-]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            out[key] = _scalar_yaml(m.group(2)) if m.group(2).strip() else []
    return out


def paper_card_data(run):
    """What one Paper Run's Result folder says about its paper."""
    subj = _yaml_block(read(run / "runtime.yaml"), "subject")
    try:
        acc = json.loads(read(run / "source-access.json") or "{}")
    except ValueError:
        acc = {}
    abstract = " ".join(ln.strip() for ln in read(run / "abstract.md").splitlines()
                        if ln.strip() and not ln.lstrip().startswith(("#", "Source:", ">")))
    doi = subj.get("doi", "")
    return {"title": subj.get("title", ""), "authors": subj.get("authors", ""), "venue": subj.get("venue", ""),
            "abstract": abstract, "pdf": (run / "paper.pdf") if (run / "paper.pdf").is_file() else None,
            # other open PDFs the Run holds (a supplement, a peer-review file, an earlier version): linked, never
            # shown as the paper, because they are not the article
            "more_pdfs": sorted(x for x in run.glob("*.pdf") if x.name != "paper.pdf"),
            "publisher": (acc.get("links") or {}).get("publisher") or ("https://doi.org/" + doi if doi else ""),
            "card": run / (run.name + ".md"),
            # the paper's own logic and work, written by the Run's ticket (JL 261002)
            "lw": logic_work_data(run / "logic-work.yaml")}


def _first_author(authors):
    """`Xiao Gu; Wei Tang; …` → `Gu et al.`; `Frey, Nathan C.` keeps the surname; a group
    author (`AI-READI Consortium`) keeps its whole name."""
    names = [a.strip() for a in (authors or "").split(";") if a.strip()]
    if not names:
        return ""
    group = re.search(r"\b(Consortium|Group|Committee|Collaboration|Investigators|Study)\b", names[0])
    first = names[0] if group else names[0].split(",")[0].strip() if "," in names[0] else names[0].split()[-1]
    return first + (" et al." if len(names) > 1 else "")


def venue_name(d):
    """The target venue: the H1 of board.md's `venue-page`, before its colon."""
    rel = _links(read(d["board"] / "board.md")).get("venue-page", "")
    h1 = re.search(r"^#\s+(.+)$", read((d["board"] / rel).resolve()), re.M) if rel else None
    return h1.group(1).split(":")[0].strip() if h1 else ""


def _short_venue(v):
    """`Nature Machine Intelligence 8, 220-233 (2026) · Article` → (`Nature Machine Intelligence`, `2026`);
    `NeurIPS 2022 · Conference paper` → (`NeurIPS`, `2022`); `arXiv preprint 2001.08361 (2020)` → (`arXiv`, `2020`);
    `Nature 656(8126), 115-122 (2026)` → (`Nature`, `2026`): a parenthesized issue number is not a year."""
    v = v or ""
    year = re.search(r"\(((?:19|20)\d{2})\)", v) or re.search(r"\b((?:19|20)\d{2})\b", v)
    name = "arXiv" if v.startswith("arXiv") else re.sub(r"\s*\b(?:19|20)\d{2}\b", "", re.sub(
        r"\s+\d+,.*$", "", re.sub(r"\s*\(\d{4}\)", "", v.split(" · ")[0]))).strip()
    return name, year.group(1) if year else ""


BEARS = (("support", "ok", "supports"), ("contradict", "bad", "contradicts"), ("limit", "warn", "limits"),
         ("method", "acc", "method"), ("frame", "mut", "frames"))


def _bears(cell):
    """`Q1 limits; Q2 supports` → one chip per question, coloured by its verdict (JL 261002)."""
    chips = []
    for part in [x.strip() for x in re.split(r"[;,·]", cell or "") if x.strip()]:
        m = re.match(r"^(\S+)\s+(.*)$", part)
        q, verb = (m.group(1), m.group(2)) if m else (part, "")
        cls, word = next(((c, w) for k, c, w in BEARS if k in verb.lower()), ("mut", verb or "bears on"))
        chips.append('<span class="rp-bear rp-bear-%s"><b>%s</b> %s</span>' % (cls, esc(q), esc(word)))
    return '<div class="rp-bears">%s</div>' % "".join(chips) if chips else ""


def _lw_table(lw):
    """The paper's own logic beside its work (JL 261002: "a table like its High Logic and Low
    Work"): left what it asks, finds and contributes; right the data and method that do the
    work. Read from the Run's logic-work.yaml; nothing is shown when the Run has none."""
    if not lw.get("question"):
        return ""
    pill = lambda k: '<span class="item-kind">%s</span>' % esc(k)
    item = lambda k, txt: '<div class="lw-c"><div class="lw-top">%s</div><div class="lw-body">%s</div></div>' % (pill(k), esc(txt))
    lst = lambda k, xs: "".join(item("%s %d" % (k, i + 1), x) for i, x in enumerate(xs if isinstance(xs, list) else [xs]))
    src = {"pdf": "the PDF", "full-text": "the full text", "supplement": "the supplement", "abstract": "the abstract only"}
    head = _lw_row("", "Their logic", "Their work · read from %s" % esc(src.get(lw.get("read_from"), lw.get("read_from") or "?")), "lw-head")
    rows = [_lw_row("", item("Question", lw["question"]), item("Data", lw.get("data", ""))),
            _lw_row("", lst("Finding", lw.get("findings") or []), lst("Method", lw.get("method") or [])),
            _lw_row("", item("Contribution", lw.get("contribution", "")), "")]
    return '<div class="lw rp-lw">%s%s</div>' % (head, "".join(rows))


def _paper_card(d, s, row):
    """One related paper. Closed, two plain lines (JL 260930: "too messy … no need to
    show all the details in the card front face"): the title, then who, when and where,
    with the question and a 📄 when the PDF is inside. Open: why it matters, its links,
    the abstract (folded) and the PDF itself; no facts line (JL 260930: "not relevant").
    Returns (html, has_pdf, venue)."""
    heads, pid = s["pp_h"], row[0]
    addr = next(iter(_addresses(_cell(heads, row, "discovery") or " ".join(row[1:]))), "")
    run = _disc_run(d, addr)
    m = paper_card_data(run) if run is not None else {}
    title = m.get("title") or _cell(heads, row, "paper") or pid
    venue, year = _short_venue(m.get("venue"))
    who = " · ".join(x for x in (_first_author(m.get("authors")), year, venue) if x) or _cell(heads, row, "paper")
    q = _cell(heads, row, "question")
    qword = "All" if q.lower() in ("all", "every question") else q
    pdf = m.get("pdf")
    marks = ('<span class="rp-q">%s</span>' % esc(qword) if q else "") + ('<span title="PDF inside">📄</span>' if pdf else "")
    summary = ('<summary><span class="bjt-chev">▸</span><div class="lw-sum"><div class="rp-title">%s</div>'
               '<div class="rp-sub"><span>%s</span><span class="rp-marks">%s</span></div></div></summary>'
               % (esc(title), esc(who) if run is not None else
                  '<span class="warn">no Paper Run at %s</span>' % esc(addr or "this row"), marks))
    url = _tree_url(d, pdf) if pdf else ""
    acts = [('<a href="%s" target="_blank" rel="noopener">Open the PDF in a new tab ↗</a>' % esc(url)) if url else "",
            ('<a href="%s" target="_blank" rel="noopener">Publisher page ↗</a>' % esc(m["publisher"])) if m.get("publisher") else "",
            _file_link(d, m["card"], "Paper Run ↗") if m.get("card") is not None and m["card"].is_file() else ""]
    acts += ['<a href="%s" target="_blank" rel="noopener">%s ↗</a>' % (esc(_tree_url(d, x)), esc(x.stem.replace("-", " ").capitalize()))
             for x in m.get("more_pdfs", [])]
    # why OUR paper keeps this one (JL 261002): the P-board's `keep` cell, else its `why it matters`;
    # `bears on` marks each of our questions it supports, limits or contradicts
    keep, why = _cell(heads, row, "keep"), _cell(heads, row, "why")
    body = [('<div class="rp-keep"><div class="rp-keep-h">Why we keep it</div><p>%s</p>%s</div>'
             % (esc(keep), _bears(_cell(heads, row, "bears"))) if keep else
             ('<p class="rp-why">%s</p>%s' % (esc(why), _bears(_cell(heads, row, "bears")))) if why else _bears(_cell(heads, row, "bears"))),
            _lw_table(m.get("lw") or {}),
            '<div class="rp-acts">%s</div>' % "".join('<span>%s</span>' % a for a in acts if a)]
    if m.get("abstract"):
        body.append('<details class="rp-absd"><summary>Abstract</summary><p>%s</p></details>' % esc(m["abstract"]))
    body.append('<iframe class="rp-frame" title="%s" data-pdf="%s"></iframe>' % (esc("PDF · " + title), esc(url)) if url else
                ('<div class="rp-nopdf mut">No free full text of the article. The open files are linked above.</div>' if m.get("more_pdfs") else
                 '<div class="rp-nopdf mut">No free full text. Read it on the publisher page; it may need a subscription.</div>'))
    return ('<details class="rp-card" data-key="%s">%s<div class="rp-body">%s</div></details>'
            % (esc(pid), summary, "".join(body)), bool(pdf), m.get("venue", ""))


def _role_bands(cards):
    """[(role, card)] → the role bands in their fixed order, each a count and one box of rows."""
    groups = {k: [c for r, c in cards if r == k] for k, _, _ in RELATED_ROLES}
    return "".join('<div class="lw-k lw-k-%s">%s<span class="lw-kn">%d</span></div><div class="rp-group">%s</div>'
                   % (cls, esc(label), len(groups[k]), "".join(groups[k])) for k, label, cls in RELATED_ROLES if groups[k])


def related_html(d):
    """Story › Related Papers: the §5.3 P-board. The target venue's papers come first and
    other venues follow (JL 260930: "this is not limited to NMI"); inside each, the
    papers are grouped by the role they play."""
    rows = [(s, r) for s in d["story"] for r in s["pp"]]
    if not rows:
        return '<div class="space-empty">No related paper yet.</div>'
    venue, n_pdf, roles = venue_name(d), 0, {k for k, _, _ in RELATED_ROLES}
    here, away = [], []
    for s, r in rows:
        role = (_cell(s["pp_h"], r, "role").split() or ["background"])[0].lower()
        card, has, where = _paper_card(d, s, r)
        n_pdf += has
        at_venue = not venue or where.lower().startswith(venue.lower())
        (here if at_venue else away).append((role if role in roles else "background", card))
    head = '<div class="rp-head">%d paper%s · %d with a PDF</div>' % (len(rows), "" if len(rows) == 1 else "s", n_pdf)
    if not venue:
        return '<div class="rp-list">%s%s</div>' % (head, _role_bands(here))
    parts = [('<h3 class="rp-venue">At %s<span class="lw-kn">%d</span></h3>%s' % (esc(venue), len(here), _role_bands(here))) if here else "",
             ('<h3 class="rp-venue">Other venues<span class="lw-kn">%d</span></h3>%s' % (len(away), _role_bands(away))) if away else ""]
    return '<div class="rp-list">%s%s</div>' % (head, "".join(parts))


def _named(addr, named):
    """Is this job address answered by a question row (at job level or below)?"""
    return any(addr.startswith(a) or a.startswith(addr) for a in named)


def _unnamed_addrs(d):
    """The claimed folders that no Task or Discovery row names yet, as addresses:
    (Task-home job or task addresses, Discovery job addresses)."""
    t_named = [a for s in d["story"] for c in s["tt"] for a in _addresses(" ".join(c))]
    d_named = [a for s in d["story"] for c in s["dd"] for a in _addresses(" ".join(c))]
    scope, jobs = paper_scope(d), []
    for blk in d["blocks"]["tree"]:
        for j in blk["jobs"]:
            if not _claimed(j["addr"], scope):
                continue
            if not _named(j["addr"], t_named):
                jobs.append(j["addr"])                       # no row names this job
            else:                                            # a row names some of its tasks
                jobs += [t["addr"] for t in j["tasks"]
                         if _claimed(t["addr"], scope) and not _named(t["addr"], t_named)]
    dscope = discovery_scope(d)
    djobs = [j["addr"] for blk in d["disc"]["tree"] for j in blk["jobs"]
             if _claimed(j["addr"], dscope) and not _named(j["addr"], d_named)]
    return jobs, djobs


def roadmap_html(d):
    """Story › RoadMap Draw (JL 260930, JL's name: "a view … to show the excalidraw draw
    which will be saved here: studio"): the paper's Excalidraw canvas, editable, on a
    drawing in `<paper>/studio/`. It opens `<Story stem>.excalidraw` (the Story board.md
    `story-current:` names) when that exists, else the first drawing there; with none, the
    Story's own, which the server writes empty the first time the canvas opens
    (`mint_board_scene`). Every other drawing in `studio/` is one click away."""
    stems = [s["stem"] for s in d["story"]]
    cur = scalar(read(d["board"] / "board.md"), "story-current").strip()
    stem = cur if cur in stems else next((x for x in stems if re.match(r"^Story[A-Z]", x)), stems[0] if stems else "")
    if not stem:
        return '<div class="space-empty">No Story yet.</div>'
    studio = Path(d["board"]) / "studio"
    own = studio / (stem + ".excalidraw")
    files = sorted(studio.glob("*.excalidraw"), key=lambda f: (f.name != own.name, f.name)) if studio.is_dir() else []
    files = files or [own]
    urls = [(f, "/_excalidraw/?board=%s&edit=1" % quote(_tree_url(d, f).lstrip("/"), safe="/")) for f in files]
    chips = "".join('<button type=button class="rd-file%s" data-src="%s">%s</button>'
                    % (" on" if i == 0 else "", esc(u), esc(f.stem)) for i, (f, u) in enumerate(urls)) \
        if len(urls) > 1 else ""
    return ('<div class="rd-bar">%s<a class="rd-open" href="%s" target="_blank" rel="noopener">Open full screen ↗</a></div>'
            # no referrer, as the Draw panel does: Excalidraw refuses a same-site embed ("I'm not a pretzel!")
            '<iframe class="rd-frame" title="RoadMap Draw" referrerpolicy="no-referrer" data-src="%s"></iframe>'
            % (chips, esc(urls[0][1]), esc(urls[0][1])))


def _tree_url(d, path):
    """A plain server path for a Task-home file or folder (raw, outside any board)."""
    root = d["root"]
    try:
        return "/" + str(Path(path).resolve().relative_to(Path(root).resolve())).replace(os.sep, "/")
    except ValueError:
        return ""


def _claimed(addr, scope):
    """Is this block/job address inside the claim? A claim `b03` covers every
    job in b03; `b02j01` covers b02 (the block) and only j01 inside it."""
    return any(a.startswith(addr) or addr.startswith(a) for a in scope)


def _disc_link(d, blk, job, task, label):
    """A link into the Discovery Board: a Task Page opens in Outline; an inquiry
    opens its built board page (board/jNN.html), else its raw _index.md; the
    block opens the board itself. Outline does not serve `_index.md`."""
    url = ""
    if task is not None and task["page"] and blk["board_md"] is not None:
        url = outline_url(_tree_url(d, blk["board_md"]), task["page"].relative_to(blk["dir"]))
    elif task is not None:
        url = _tree_url(d, task["page"] or task["dir"])
    elif job is not None:
        built = blk["dir"] / "board" / (job["name"][:3] + ".html")
        url = _tree_url(d, built if built.is_file() else (job["index"] or job["dir"]))
    elif blk["board_md"] is not None:
        built = blk["dir"] / "board" / "index.html"
        url = _tree_url(d, built) if built.is_file() else outline_url(_tree_url(d, blk["board_md"]), "board.md")
    return ('<a href="%s">%s</a>' % (esc(url), esc(label))) if url else esc(label)


def _disc_join(d, cells):
    """The Discovery jobs/tasks a Discovery Roadmap row names by address, as links; '' when none."""
    out = []
    for a in _addresses(" ".join(cells)):
        hit = _disc_lookup(d, a)
        if hit:
            blk, job, task = hit
            out.append(_disc_link(d, blk, job, task, (task or job or blk)["name"]))
        else:
            out.append('<span class="warn">%s ✗ not in the Discovery home</span>' % esc(a))
    return " · ".join(out)


def _hero_cards(d):
    cards = []
    for it in d["hero"]:
        short = it["id"].split("-")[0]
        rows = [("Need", esc(it["desc"])), ("Expected", esc(it["expected"] or "—")),
                ("Bullet", esc(it["target"]))]
        if it["supporting"]:
            rows.append(("Supporting", "<br>".join(
                "%s · <code>%s</code>" % (esc(s["owner"]), esc(s["addr"] or s["raw"])) for s in it["supporting"])))
        rows.append(("Page", _link(d, it["rel"], "Open ↗", lens="evidence", focus=it["id"])))
        cards.append(_card("hero-" + it["id"], it["type"], it["label"] or it["id"],
                           esc(item_name(it["id"]) + " · " + it["page"]), "", it["status"], _status_cls(it["status"]), rows,
                           key="%s:%s" % (it["page"], short), attrs=' data-part="%s"' % it["part"]))
    return cards


def _cards_card(title, cards, empty):
    return ('<h3 class="space-h">%s</h3>%s' % (esc(title), '<div class="item-cards">%s</div>' % "".join(cards)
                                               if cards else '<div class="space-empty">%s</div>' % esc(empty)))


def _run_tickets(runs):
    """A page's run tickets: flat `runs/`, or its Space folders (Page 0.118).

    `runs/supporting-run/` holds a generated index of Runs kept elsewhere, not tickets.
    """
    return sorted((f for f in runs.rglob("*") if f.is_file() and not f.name.startswith(".")
                   and "supporting-run" not in f.relative_to(runs).parts), key=lambda f: f.name)


def _file_link(d, path, label):
    url = _tree_url(d, path) if path else ""
    return ('<a href="%s">%s</a>' % (esc(url), esc(label))) if url else esc(label)


def _yn(v):
    return '<span class="ok">✓</span>' if v else '<span class="warn">✗</span>'


def _not_ready_ids(rd):
    """`readiness.not_ready` from build-manifest.json: the engine writes one
    {"id", "reasons"} dict per page (build_delivery.py), older manifests a bare
    id string. Either way the Delivery card names the page, never the dict."""
    out = []
    for x in rd.get("not_ready") or []:
        out.append(str(x.get("id", "?")) if isinstance(x, dict) else str(x))
    return out


# ---------------------------------------------------------------- render
# The Page workbench's grammar (JL 260927; the drawing is
# servers/workbench-paper/studio/paper-workbench-design.excalidraw): four Spaces,
# each with its tabs and views, the content on the left and its own Runs panel on
# the right. Nothing on screen explains itself: no source lines, counts or hints.
SPACES = (("ideation", "Ideation"), ("story", "Story"),               # plain names, as every
          ("sections", "Sections"), ("delivery", "Delivery"))          # workbench's (JL 261003)
STORY_TABS = (("spine", "Spine"), ("roadmap-draw", "RoadMap Draw"),                           # JL 260930
              ("logic-work", "High-level logic + Low-level work"),                        # JL 260929
              ("related", "Related Papers"))                                             # JL 260930
SECTION_TABS = (("main", "Main"), ("appendix", "Appendix"))
SECTION_VIEWS = (("table", "Table"), ("narrative", "Narrative"), ("evidence", "Evidence"))
DELIVERY_TABS = (("latex", "LaTeX"), ("word", "Word"), ("cover", "Cover letter"), ("rounds", "Rounds"))
DELIVERY_VIEWS = (("preview", "Preview"), ("artifacts", "Artifacts"), ("checks", "Checks"))

_CARDS = SKILLS / "paper" / "haipipe-paper-workflow" / "ref" / "run-cards.md"
_BUTTON = re.compile(r"^🔘 BUTTON\s+(?P<label>.+?)\s+·\s+(?P<space>[A-Z][A-Za-z]+)\s+·\s+"
                     r"(?P<pattern>\S.*?)(?:\s+·\s+views\s+(?P<views>[\w -]+?))?\s*$")
_PROMPT = re.compile(r"^💬 PROMPT\s+(?P<prompt>.+?)\s*$")


def paper_run_types(path=_CARDS):
    """The paper's Run cards → {space: [{label, pattern, views, prompt, skills}]} in
    card order. Each button takes the first `💬 PROMPT` after it and the `🧩 SKILL`
    line before that prompt; pattern `-` means the button only copies a prompt
    (its runs live with another owner)."""
    out, pending = {}, []
    for line in read(path).splitlines():
        m = _BUTTON.match(line)
        if m:
            t = {"label": m["label"], "space": m["space"].lower(), "pattern": m["pattern"].strip(),
                 "views": " ".join((m["views"] or "").split()), "prompt": "", "skills": []}
            out.setdefault(t["space"], []).append(t)
            pending.append(t)
            continue
        m = re.match(r"^🧩 SKILL\s+(.+?)\s*$", line)
        if m:
            for t in pending:
                t["skills"] = [s.strip() for s in m.group(1).split("·") if s.strip()]
            continue
        m = _PROMPT.match(line)
        if m:
            for t in pending:
                t["prompt"] = m["prompt"]
            pending = []
    return out


def _page_runs(d, page):
    """One Page's runs as the Page workbench reads them (live.runs.local_runs)."""
    if not page or not page.get("rel"):
        return []
    from live.runs import local_runs
    try:
        return local_runs(d["board"] / page["rel"])
    except Exception:  # noqa: BLE001  a broken ticket must not blank a Space
        return []


def _norm_key(kind, value):
    """`i01` → `i1`, `E-05` → `E5`: selection keys compare by number."""
    m = re.match(r"^%s-?0*(\d+)$" % kind, (value or "").strip())
    return "%s%s" % (kind, m.group(1)) if m else (value or "").strip()


def _bucket(kinds, rows, place):
    """rows → one list per run type. A row goes to the type whose ticket pattern
    matches; `place(row)` names a type for rows no pattern takes (or None)."""
    from live.runs_panel import _number, _ticket_name
    buckets = [[] for _ in kinds]
    for row in sorted(rows, key=_number, reverse=True):
        name = _ticket_name(row)
        hit = next((i for i, k in enumerate(kinds)
                    if k["pattern"] != "-" and re.search(k["pattern"], name)), None)
        if hit is None:
            label = place(row)
            hit = next((i for i, k in enumerate(kinds) if k["label"] == label), None)
        if hit is not None:
            buckets[hit].append(row)
    return buckets


def _panel(d, space, kinds, buckets, fill, whole):
    from live.runs_panel import panel_markup
    return panel_markup(space, kinds, buckets, base=Path(d["root"]),
                        fill=lambda row: row.get("_fill") or fill, whole=whole, folded=True)


def _tag(rows, keys=(), fill=None):
    """Mark rows for the paper's panels: selection keys, no format filter, prompt fill."""
    out = []
    for row in rows:
        row = dict(row)
        row["_keys"] = " ".join(k for k in list(keys) + row.get("_keys", "").split() if k)
        row["_views"] = ""
        if fill:
            row["_fill"] = fill
        out.append(row)
    return out


def _ideation_panel(d, kinds):
    page = d["story00"]
    fill = {"page": page["stem"] if page else "Story00", "paper": d["board"].name}
    rows = []
    for row in _page_runs(d, page):
        rows += _tag([row], [_norm_key("i", row.get("target"))], fill)
    return _panel(d, "ideation", kinds, _bucket(kinds, rows, lambda r: None), fill, "every idea")


def _claim_rq(s):
    """Claim number → the RQs its row names."""
    irq = _col(s["e_h"], ("rq", "question"), 1)
    out = {}
    for c in s["e"]:
        m = re.match(r"E-?\d+", c[0])
        if m:
            out[_norm_key("E", m.group(0))] = [x for x in _row_ids(c[irq] if len(c) > irq else "") if x.startswith("RQ")]
    return out


def _supporting_rows(d, s, fill, T):
    """The Task and Discovery runs this paper's Evidence Items cite, as run rows
    keyed by the Task and Discovery Roadmap rows whose addresses cover them, and by every claim and
    RQ above those rows, so selecting a question shows the runs behind it."""
    q_of = {_row_key(c[0]): _q_of(s["tt_h"], c) for c in s["tt"]}
    q_of.update({_row_key(c[0]): _q_of(s["dd_h"], c) for c in s["dd"]})
    covers = [(_row_key(c[0]), _addresses(" ".join(c))) for c in s["tt"] + s["dd"]]
    rows = []
    for owner in ("Execution", "Discovery"):
        for node in d["supporting"][owner].values():
            for jnode in node["jobs"].values():
                for tnode in jnode["tasks"].values():
                    for r in tnode["runs"]:
                        dotted = ".".join(re.findall(r"[bjtr]\d{2}", r["addr"]))
                        ticket = r["tickets"][0][1] if r["tickets"] else None
                        keys = [row for row, addrs in covers if any(r["addr"].startswith(a) for a in addrs)]
                        keys += sorted({q_of[k] for k in keys if q_of.get(k)}) + [u for k in keys for u in T["up"].get(k, [])]
                        users = sorted({u["page"] + " " + u["item"].split("-")[0] for u in r["users"]})
                        st = (r["status"] or "").lower()
                        task = tnode.get("task")
                        home = Path(task["dir"]) if task and task.get("dir") else None
                        stem = r["tickets"][0][0] if r["tickets"] else ""
                        # its card opens the run's results in the pop-out (JL 260930)
                        opens = home is not None and (home / "results").is_dir() and d.get("root") is not None
                        rows.append({"run_id": dotted, "global_id": dotted, "ticket": ticket,
                                     "status": "done" if st in ("complete", "completed", "done") else (st or "unknown"),
                                     "target": owner + " · " + dotted, "goal": "used by " + ", ".join(users),
                                     "result": "", "_display": dotted, "_keys": " ".join(keys),
                                     "result_path": (home / "results" / stem if stem and (home / "results" / stem).is_dir()
                                                     else home / "results") if opens else "",
                                     "_open": run_result_url(d["root"], home, stem) if opens else "",
                                     "_open_name": stem or dotted})
    return _tag(rows, (), fill)


def _story_panel(d, kinds):
    rows = []
    for s in d["story"]:
        fill = {"page": s["stem"], "paper": d["board"].name}
        rq, T = _claim_rq(s), story_tree(s)
        hyp_of = {}                                  # §5 row → the hypotheses it tests
        for q in T["questions"]:
            for h in q["hyps"]:
                for x in h["tests"]:
                    hyp_of.setdefault(x, []).append(h["id"])
        for row in _page_runs(d, s):
            name = str(row.get("run_id") or row.get("global_id") or "")
            target = str(row.get("target") or "")
            if re.search(r"(^|\s)run-paper-claim-", name):
                e = _norm_key("E", target)
                rows += _tag([row], [e] + rq.get(e, []) + hyp_of.get(e, []), fill)
            elif re.search(r"(^|\s)run-paper-task-", name):
                t = _row_key(target)
                rows += _tag([row], [t] + T["up"].get(t, []), fill)
            elif not re.search(r"(^|\s)run-paper-(idea|narrative)-", name):
                rows += _tag([row], [], fill)
        rows += _supporting_rows(d, s, fill, T)
    first = d["story"][0]["stem"] if d["story"] else "the Story"
    fill = {"page": first, "paper": d["board"].name}
    # a supporting run goes under its owner: a Task folder's run or a Discovery folder's run
    buckets = _bucket(kinds, rows, lambda r: "Discovery runs" if str(r.get("target", "")).startswith("Discovery · ")
                      else "Task runs" if str(r.get("target", "")).startswith("Execution · ") else None)
    return _panel(d, "story", kinds, buckets, fill, "the Story")


def _sections_panel(d, kinds, sections):
    from live.runs_panel import _name_by_item, _paper_run_key, _ticket_item, row_space
    from live.space_views import run_tabs
    rows = []
    part = {sec["id"]: sec["part"] for sec in sections}
    for s in d["story"]:
        fill = {"page": s["stem"], "paper": d["board"].name}
        for row in _page_runs(d, s):
            if re.search(r"(^|\s)run-paper-narrative-", str(row.get("run_id") or "")):
                sid = str(row.get("target") or "").strip()
                rows += [dict(x, _views=part.get(sid, "")) for x in _tag([row], [sid], fill)]
    for sec in sections:
        if not sec["page"]:
            continue
        fill = {"page": sec["id"], "paper": d["board"].name}
        page_src = d["board"] / sec["page"]["rel"]
        try:
            served_by = run_tabs(page_src)
        except Exception:  # noqa: BLE001
            served_by = {}
        evidence = []
        for row in _page_runs(d, sec["page"]):
            where = row_space(row)
            keys = [sec["id"]]
            if where == "evidence":
                served = served_by.get(_paper_run_key(str(row.get("run_id") or "")))
                if served:
                    row = dict(row, _served=served)
                item = (served or {}).get("item") or _ticket_item(row)
                if item:
                    keys.append("%s:%s" % (sec["id"], item))
            tagged = _tag([row], keys, fill)[0]
            tagged["target"] = ("%s %s" % (sec["id"], row.get("target") or "")).strip()
            tagged["_views"] = sec["part"]
            tagged["_place"] = {"evidence": "Evidence runs", "delivery": "Delivery runs"}.get(where, "Draft runs")
            (evidence if where == "evidence" else rows).append(tagged)
        _name_by_item(evidence)
        rows += evidence
    fill = {"page": "{target}", "paper": d["board"].name}
    buckets = _bucket(kinds, rows, lambda r: r.get("_place"))
    return _panel(d, "sections", kinds, buckets, fill, "each Section")


def _delivery_panel(d, kinds):
    dv, rows = d["delivery"], []
    man = dv["manifest"] or {}
    if man and dv["built"]:
        stamp = re.sub(r"\D", "", dv["built"])[2:8]
        rows.append({"run_id": "compile-" + stamp, "global_id": "compile-" + stamp, "status": "done",
                     "target": "the whole paper", "result": "delivery/build-manifest.json",
                     "result_path": dv["dir"], "goal": "%s · built %s" % (man.get("status") or "", dv["built"]),
                     "_display": "run-compile-" + stamp, "_place": "Build"})
    for r in d["rounds"]:
        fill = {"page": r["stem"], "paper": d["board"].name}
        for row in _page_runs(d, r):
            rows += [dict(x, _place="Response") for x in _tag([row], [r["stem"]], fill)]
    cover = _cover(d)
    if cover is not None:                             # the build's one fixed cover-letter run
        rows.append({"run_id": "run-delivery-coverletter", "global_id": "run-delivery-coverletter",
                     "status": "done" if cover.get("ready") else "held", "target": cover.get("round") or "the letter",
                     "result": ((cover.get("outputs") or {}).get("pdf") or ""), "result_path": dv["dir"],
                     "goal": "from " + (cover.get("from") or "?"), "_display": "run-delivery-coverletter",
                     "_place": "Cover letter", "_views": "cover"})
    rows = _tag(rows)
    fill = {"page": d["board"].name, "paper": d["board"].name}
    return _panel(d, "delivery", kinds, _bucket(kinds, rows, lambda r: r.get("_place")), fill, "the manuscript")


# ---- the Spaces --------------------------------------------------------------
def _space(space, main, panel, tabs=(), views=(), noviews=()):
    """One Space: its tabs and views over the content, its Runs panel beside it."""
    tab_row = ('<div class="space-tabs">%s</div>' % "".join(
        '<button type=button class="space-tab%s" data-tab="%s" data-label="%s"%s>%s</button>'
        % (" on" if i == 0 else "", k, esc(label), " data-noviews" if k in noviews else "", esc(label))
        for i, (k, label) in enumerate(tabs))) if tabs else ""
    view_row = ('<div class="space-views"><span class="space-views-label">View</span>%s</div>' % "".join(
        '<button type=button class="space-view%s" data-view="%s">%s</button>' % (" on" if i == 0 else "", k, esc(label))
        for i, (k, label) in enumerate(views))) if views else ""
    return ('<div class="panel space-split" data-space="%s"><div class="space-main">%s%s%s</div>%s</div>'
            % (space, tab_row, view_row, main, panel))


def _pane(html_, tab="", view=""):
    return '<div class="space-pane"%s%s>%s</div>' % (
        (' data-tab="%s"' % tab) if tab else "", (' data-view="%s"' % view) if view else "", html_)


def _cards(cards, empty):
    return '<div class="item-cards">%s</div>' % "".join(cards) if cards else '<div class="space-empty">%s</div>' % esc(empty)


def render_ideation(d, kinds):
    i = d["ideation"]
    if not i["present"]:
        main = _pane('<div class="space-empty">No Story00-ideation page yet.</div>')
    else:
        main = _pane(_cards([_idea_card(d, i, x) for x in i["ideas"]], "No idea yet."))
    return _space("ideation", main, _ideation_panel(d, kinds))


def _spine_html(d):
    out = []
    many = sum(1 for s in d["story"] if re.match(r"^Story[A-Z]", s["stem"])) > 1
    for s in d["story"]:
        if many:
            out.append('<h3 class="story-name">%s</h3>' % esc(s["stem"]))
        for n, title, (face, subs, paras) in s["spine"]:
            rows = [(k, inline(v)) for k, v in face]
            if paras:
                rows.append(("", prose(paras)))
            rows += [(sub, prose(pg)) for sub, pg in subs if pg]
            out.append('<div class="card spine-card" data-key="C%d"><h2>%s<span class="tally">%s</span></h2>%s</div>'
                       % (n, esc(title), _link(d, s["rel"], "Open ↗", focus="C%d" % n),
                          _kv(rows, "spine-row") or '<div class="space-empty">Empty.</div>'))
    return "".join(out) or '<div class="space-empty">No Story yet.</div>'


def _q_of(headers, row):
    """The general question a T or D row names in its `Q` column ('' when none)."""
    i = next((k for k, h in enumerate(headers) if h.strip().upper() == "Q"), None)
    return row[i].strip() if i is not None and i < len(row) else ""


def render_story(d, kinds):
    if not d["story"]:
        empty = '<div class="space-empty">No Story yet.</div>'
        return _space("story", "".join(_pane(empty, k) for k, _ in STORY_TABS), _story_panel(d, kinds), STORY_TABS)
    main = (_pane(_spine_html(d), "spine") + _pane(roadmap_html(d), "roadmap-draw")
            + _pane(logic_work_html(d), "logic-work") + _pane(related_html(d), "related"))
    return _space("story", main, _story_panel(d, kinds), STORY_TABS)


def section_rows(d):
    """Every Section of the paper in compile order: the Story's §8 rows joined to
    their Section Pages, then any Section Page no §8 row names."""
    by_id, heads = {}, {}
    for s in d["story"]:
        for r in s["sections"]:
            by_id.setdefault(r["id"], r)
            heads.setdefault(r["id"], r.get("heads") or s["sec_h"])
    order = next((s["order"] for s in d["story"] if s["order"]), [])
    ids = [x for x in order] + [x for x in by_id if x not in order]
    ids += [p["stem"] for p in d["sections"] if p["stem"] not in ids]
    pages = {p["stem"]: p for p in d["sections"]}
    sessions = {r["stem"]: r for r in d.get("sessions", [])}
    out = []
    for sid in ids:
        page = pages.get(sid)
        page = page if page and page["rel"] else None
        # S-<desk>-<Main|Appendix>-[<N>-]<Title>; a desk may carry a hyphen (JAMA-IM)
        m = re.match(r"^S-.+?-(?:Main|Appendix)-(?:([0-9]+|[A-Z])-)?(.+)$", sid)
        num, name = ((m.group(1) or ""), m.group(2).replace("-", " ")) if m else ("", sid)
        c8_num = (by_id.get(sid) or {}).get("target", "")
        if not num and re.fullmatch(r"[0-9]+|[A-Z]", c8_num):
            num = c8_num                    # a record's `(0)`: the Abstract's place in the order
        version = ""
        if page:
            plan = latest_outline(plan_dir((d["board"] / page["rel"]).parent), sid)
            version = version_tag(plan) if plan else ""
        state = clean(scalar(page["text"], "state", "")).split("·")[0].strip() if page else "not set up"
        out.append({"id": sid, "part": "appendix" if "-Appendix-" in sid else "main", "num": num,
                    "name": name, "page": page, "version": version, "state": state,
                    "row": by_id.get(sid), "heads": heads.get(sid, []), "session": sessions.get(sid)})
    return out


def _state_word(state):
    """`🟡 PARTIAL - prose inherited, evidence items not landed` → `🟡 Partial`: the state
    word only (JL 261003: "this is too detailed, could we make it light?"); the whole
    line stays in the cell's tooltip."""
    head = re.split(r"\s+[-–—·]\s+|[:,(]", state or "", maxsplit=1)[0].strip()
    m = re.match(r"^(\W*?)\s*([A-Za-z][\w ]*)$", head)
    return ("%s %s" % (m.group(1), m.group(2).strip().capitalize())).strip() if m else head


def _section_table(d, rows):
    out = []
    for r in rows:
        opener = ('<a class="sec-open" href="%s">Open ↗</a>' % esc(outline_url(d["path"], r["page"]["rel"]))
                  if r["page"] else "")
        out.append('<div class="sec-row" data-key="%s" tabindex="0" title="%s"><span class="sec-num">%s</span>'
                   '<span class="sec-name">%s</span><span class="sec-ver">%s</span>'
                   '<span class="sec-state %s" title="%s">%s</span>%s</div>'
                   % (esc(r["id"]), esc(r["id"]), esc(r["num"]), esc(r["name"]), esc(r["version"]),
                      _status_cls(r["state"]) if r["page"] else "warn", esc(r["state"]),
                      esc(_state_word(r["state"])), opener))
    return '<div class="sec-list">%s</div>' % "".join(out) if out else '<div class="space-empty">No Section yet.</div>'


def _narrative_cards(d, rows):
    cards = []
    for r in rows:
        c8 = r["row"]
        fields = _fields(r["heads"], c8["cells"], {0, 1}) if c8 else []
        if r["session"]:
            sess = r["session"]
            if not sess["pair"]:                # a Claude session with no Codex pair yet
                fields.append(("Session", esc(sess["state"])))
            else:
                fields.append(("Session", '<code>%s</code>%s' % (esc(sess["pair"]), "" if sess["state"].startswith("no ")
                                                                  else " · " + esc(sess["state"]))))
        label = (c8["question"] if c8 and c8["question"] else r["name"])
        cards.append(_card("section-" + r["id"], r["num"] or "·", label, esc("%s %s" % (r["num"], r["name"])).strip(),
                           "", r["state"], _status_cls(r["state"]) if r["page"] else "warn", fields, key=r["id"]))
    return cards


def render_sections(d, kinds):
    rows = section_rows(d)
    main = ""
    for tab, _ in SECTION_TABS:
        mine = [r for r in rows if r["part"] == tab]
        hero = [c for c in _hero_cards(d) if ('data-part="%s"' % tab) in c]
        main += (_pane(_section_table(d, mine), tab, "table")
                 + _pane(_cards(_narrative_cards(d, mine), "No Section yet."), tab, "narrative")
                 + _pane(_cards(hero, "No Display or Value yet."), tab, "evidence"))
    return _space("sections", main, _sections_panel(d, kinds, rows), SECTION_TABS, SECTION_VIEWS)


def _outputs(d, suffix):
    return [o for o in d["delivery"]["outputs"] if o["rel"].endswith(suffix)]


def _output_rows(d, outs):
    rows = []
    for o in outs:
        st = ("✅ built" + (" · stale" if o["stale"] else "")) if o["exists"] else "⬜ not built"
        rows.append((esc(o["what"]), _file_link(d, o["path"], o["rel"]) if o["exists"] else esc(o["rel"]),
                     '<span class="%s">%s</span>' % (_status_cls(st), esc(st)), esc(o["size"]), esc(o["stamp"])))
    return rows


def _checks_html(d):
    dv = d["delivery"]
    man = dv["manifest"] or {}
    if not man:
        return '<div class="space-empty">No build yet.</div>'
    build, sub, rd = man.get("build") or {}, man.get("submission_readiness") or {}, man.get("readiness") or {}
    facts = []
    if build:
        facts += [("main text", "%s words%s" % (build.get("main_text_words", "?"), (" · limit %s" % build["main_text_word_limit"])
                                                if build.get("main_text_word_limit") else "")),
                  ("citations", "%s cited · %s bib entries" % (build.get("citations", "?"), man.get("bib_entries", "?"))),
                  ("displays", "%s main table(s) · %s main figure(s)" % (build.get("main_tables", "?"), build.get("main_figures", "?"))),
                  ("pages ready", "%s of %s%s" % (rd.get("ready", "?"), rd.get("total", "?"),
                                                   (" · not ready: " + ", ".join(_not_ready_ids(rd))) if rd.get("not_ready") else "")),
                  ("submission", "%s%s" % (sub.get("status", "?"), (" · " + "; ".join(sub.get("blockers") or [])) if sub.get("blockers") else ""))]
    if dv["stale"]:
        facts.append(("changed since build", ", ".join(dv["stale"])))
    g4 = next((v for g, _, v in d["gates"] if g == "G4"), "")
    if g4:
        facts.append(("G4 compile", g4))
    crs = [(esc(k.replace("_", " ")), _yn(v) if isinstance(v, bool) else '<span class="mut">%s</span>' % esc(str(v)))
           for k, v in (build.get("checks") or {}).items()]
    render = man.get("render") or {}
    if render:
        crs.append(("latexmk", _yn(render.get("latexmk_rc") == 0)))
        crs.append(("docx", _yn(render.get("docx_rc") == 0)))
    pages = []
    for i, p in enumerate(dv["pages"], 1):
        notes = list(p["reasons"]) + list(p["warnings"]) + (["changed since build"] if p["stale"] else [])
        pages.append((esc(p["id"]), _yn(p["frag"]),
                      _yn(p["ready"]) if p["ready"] is not None else '<span class="mut">—</span>', esc("; ".join(notes))))
    # engine ≥0.8 writes each unresolved \ref as {"page", "ref"}; older manifests wrote a bare string
    warns = [w if isinstance(w, str) else json.dumps(w, ensure_ascii=False) for w in (man.get("warnings") or [])] + [
        "unresolved \\ref: " + (x if isinstance(x, str) else "%s (%s)" % (x.get("ref", "?"), x.get("page", "?")))
        for x in (man.get("unresolved_refs") or [])]
    return (_kv([(k, esc(v)) for k, v in facts], "spine-row")
            + _table(["check", "result"], crs)
            + _table(["page", "fragment", "ready", "notes"], pages)
            + (('<ul class="item-bullets">%s</ul>' % "".join("<li>%s</li>" % esc(w) for w in warns)) if warns else ""))


def _preview_html(d, suffix):
    outs = [o for o in _outputs(d, suffix) if o["exists"]]
    if not outs:
        return '<div class="space-empty">Not built yet.</div>'
    main = next((o for o in outs if "main" in o["what"]), outs[0])
    if suffix == ".pdf":
        return '<iframe class="space-frame" title="%s" data-src="%s"></iframe>' % (esc(main["rel"]), esc(_tree_url(d, main["path"])))
    # JL 260929 "for the word, why we cannot preview it": the paper build draws a PDF twin of each .docx
    # beside it (<stem>.pdf, from the package itself); Preview shows it under one line naming the .docx
    twin = Path(main["path"]).with_suffix(".pdf")
    if twin.is_file():
        stale = twin.stat().st_mtime < Path(main["path"]).stat().st_mtime
        return ('<p class="mut">%s · %s · %s%s</p><iframe class="space-frame" title="%s" data-src="%s"></iframe>'
                % (_file_link(d, main["path"], main["rel"]), esc(main["size"]), esc(main["stamp"]),
                   " · the preview is older than the .docx; rebuild" if stale else "",
                   esc(main["rel"]), esc(_tree_url(d, twin))))
    return _kv([("file", _file_link(d, main["path"], main["rel"])), ("size", esc(main["size"])),
                ("written", esc(main["stamp"])),
                ("preview", '<span class="mut">none yet: the next paper build draws it</span>')], "spine-row")


def _artifacts_html(d, suffix):
    dv = d["delivery"]
    html_ = _table(["what", "file", "state", "size", "written"], _output_rows(d, _outputs(d, suffix)))
    if suffix == ".pdf":
        drs = [(esc(r[0]), esc(r[1]), '<code>%s</code>' % esc(r[2]), esc(r[3]), esc(r[4])) for r in dv["displays"]]
        html_ += _table(["printed", "declared", "label", "unit", "page"], drs)
        html_ += _table(["asset", "size"], [(_file_link(d, a["path"], a["name"]), esc(a["size"])) for a in dv["assets"]])
    else:
        html_ += _table(["returned", "size", "written"], [(_file_link(d, r["path"], r["rel"]), esc(r["size"]), esc(r["stamp"]))
                                                         for r in dv["returned"]])
    return html_ or '<div class="space-empty">Not built yet.</div>'


def _round_cards(d):
    cards = []
    for r in d["delivery"]["rounds"]:
        rows = [(k, esc(v)) for k, v in (("kind", r["kind"]), ("received", " · ".join(x for x in (r["from"], r["at"]) if x)),
                                          ("response due", r["due"]), ("base build", r["base"]),
                                          ("folders", " · ".join(r["subs"]))) if v]
        rows.append(("page", _link(d, r["rel"], "Open ↗")))
        if r["state"]:
            rows.insert(0, ("state", esc(r["state"])))
        cards.append(_card("round-" + r["stem"], r["stem"][:4], r["stem"], esc(r["kind"]), "",
                           r["state"].split("·")[0].strip(), _status_cls(r["state"]), rows, key=r["stem"]))
    venue = d["delivery"]["links"].get("venue-page", "")
    tail = _kv([("venue", _file_link(d, (d["board"] / venue).resolve(), Path(venue).stem))], "spine-row") if venue else ""
    return _cards(cards, "No round yet.") + tail


def _cover(d):
    """The cover letter as the paper build recorded it (haipipe-paper-assemble 0.9.0,
    run-delivery-coverletter): build-manifest.json `cover_letter`, or None."""
    man = d["delivery"]["manifest"] or {}
    return man.get("cover_letter") if isinstance(man.get("cover_letter"), dict) else None


def _cover_panes(d):
    """Cover letter tab (JL 260929: one more delivery item). The words live on the submission
    Round page's Cover letter division; the paper build writes the letter and its checks; this
    tab only reads that record."""
    cover = _cover(d)
    if cover is None:
        empty = ('<div class="space-empty">No cover letter built yet: add a <code>[coverletter]</code> '
                 'block to delivery/paper-build.toml and run the build.</div>')
        return "".join(_pane(empty, "cover", v) for v, _ in DELIVERY_VIEWS)
    base = d["delivery"]["dir"]
    outs = {k: (base / v) if v and not Path(v).is_absolute() else (Path(v) if v else None)
            for k, v in (cover.get("outputs") or {}).items()}
    src = cover.get("source") or ""
    head = '<div class="space-h">%s · %s%s</div>' % (
        esc(cover.get("round") or "letter"), "ready" if cover.get("ready") else "not ready",
        (" · " + _link(d, src.split("/draft/")[0] + "/" + Path(src.split("/draft/")[0]).name + ".md", "Open ↗",
                       lens="div")) if src else "")
    pdf = outs.get("pdf")
    preview = head + (('<iframe class="space-frame" title="cover letter" data-src="%s"></iframe>'
                       % esc(_tree_url(d, pdf))) if pdf and pdf.is_file() else '<div class="space-empty">Not built yet.</div>')
    files = [(_file_link(d, f, f.name), esc(_stamp(f))) for f in outs.values() if f and f.is_file()]
    artifacts = head + (_table(["file", "written"], files) if files else '<div class="space-empty">Not built yet.</div>')
    rows = [(esc(c.get("check", "")), '<span class="%s">%s</span>' % ("ok" if c.get("ok") else "warn", "✅" if c.get("ok") else "⚠️"),
             esc(c.get("detail", ""))) for c in cover.get("checks") or []]
    checks = head + (_table(["check", "", "detail"], rows) or '<div class="space-empty">No checks recorded.</div>')
    return (_pane(preview, "cover", "preview") + _pane(artifacts, "cover", "artifacts")
            + _pane(checks, "cover", "checks"))


def render_delivery(d, kinds):
    main = ""
    for tab, suffix in (("latex", ".pdf"), ("word", ".docx")):
        if d["delivery"]["dir"] is None:
            empty = '<div class="space-empty">No delivery/ yet.</div>'
            main += "".join(_pane(empty, tab, v) for v, _ in DELIVERY_VIEWS)
            continue
        main += (_pane(_preview_html(d, suffix), tab, "preview") + _pane(_artifacts_html(d, suffix), tab, "artifacts")
                 + _pane(_checks_html(d), tab, "checks"))
    main += _cover_panes(d)
    main += _pane(_round_cards(d), "rounds")
    return _space("delivery", main, _delivery_panel(d, kinds), DELIVERY_TABS, DELIVERY_VIEWS, noviews=("rounds",))


_PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
:root{{--bg:#ffffff;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4e7;--card:#fff;
 --warn:#b3541e;--ok:#3a7d44;--acc:#3e5c84;--soft:#f6f7f9}}
@media(prefers-color-scheme:dark){{:root{{--bg:#161719;--fg:#e8e8e6;
 --mut:#9a9a97;--line:#2c2e33;--card:#1d1f23;--warn:#e0955a;--ok:#7dbb87;
 --acc:#7d9cc4;--soft:#1b1d21}}}}
body{{margin:0;padding:18px;background:var(--bg);color:var(--fg);
 font:16px/1.65 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
h1{{font-size:20px;margin:0 0 2px}} .mut{{color:var(--mut)}}
.spaces{{display:flex;gap:6px;margin:10px 0 10px;flex-wrap:wrap}}
.space{{font:600 13px -apple-system,sans-serif;border:1px solid var(--line);border-radius:9px;padding:5px 12px;
 cursor:pointer;background:var(--card);color:var(--fg);white-space:nowrap}}
.space.on{{border-color:var(--acc);color:var(--acc)}}
.panel{{display:none}} .panel.on{{display:block}}
.panel.on.space-split{{display:flex;align-items:flex-start;gap:16px}}
.space-views[hidden]{{display:none}}
.space-frame{{height:calc(100vh - 170px)}}
.space-h{{font-size:15px;margin:18px 0 6px}} .space-h:first-child{{margin-top:0}}
.story-name{{font:600 13px ui-monospace,Menlo,monospace;color:var(--mut);margin:14px 0 6px}}
.ok{{color:var(--ok);font-weight:600}} .warn{{color:var(--warn);font-weight:600}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:0 0 14px}}
.card h2{{font-size:17px;margin:0 0 8px;display:flex;gap:8px;align-items:baseline}}
.card h2 .tally{{margin-left:auto;flex:none;font-size:13px;font-weight:500}}
.spine-card{{cursor:pointer}}
/* inside the Space's one box a Spine division is a row, not a second box (JL 260929) */
.space-main .spine-card{{border:0;border-bottom:1px solid var(--line);border-radius:0;padding:12px 4px 14px;margin:0}}
.space-main .spine-card:last-child{{border-bottom:0}}
.runs-selected.spine-card,.item-card.runs-selected{{border-color:var(--acc);box-shadow:0 0 0 1px var(--acc)}}
table.grid{{width:100%;font-size:14.5px;line-height:1.55;border:1px solid var(--line);border-radius:9px;
 border-collapse:separate;border-spacing:0;overflow:hidden;margin:6px 0 12px}}
table.grid th{{text-align:left;background:var(--soft);font:600 11.5px -apple-system,sans-serif;text-transform:uppercase;
 letter-spacing:.03em;padding:9px 11px;border-bottom:1px solid var(--line);border-right:1px solid var(--line);opacity:.8}}
table.grid td{{padding:9px 11px;border-bottom:1px solid var(--line);border-right:1px solid var(--line);vertical-align:top}}
table.grid th:last-child,table.grid td:last-child{{border-right:0}} table.grid tr:last-child td{{border-bottom:0}}
.idtag,.path{{font:500 12.5px ui-monospace,Menlo,monospace;color:var(--mut)}} .path{{overflow-wrap:anywhere}}
.bjt-chev{{color:var(--mut);display:inline-block;width:1em;text-align:center;transition:transform .12s ease}}
.qc>summary{{list-style:none;cursor:pointer}} .qc>summary::-webkit-details-marker{{display:none}}
.qc[open]>summary .bjt-chev{{transform:rotate(90deg)}}
/* Story › High-level logic + Low-level work: one tree, split down the middle (JL 260929) */
.lw{{border:1px solid var(--line);border-radius:12px;overflow:hidden;background:var(--card)}}
.lw-row{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.lw-l{{padding:7px 14px;min-width:0}} .lw-r{{padding:7px 14px;border-left:1px solid var(--line);min-width:0}}
.lw-head{{background:var(--soft);border-bottom:1px solid var(--line);font:700 12px -apple-system,sans-serif;
 text-transform:uppercase;letter-spacing:.04em;color:var(--mut)}}
.lw-q+.lw-q{{border-top:1px solid var(--line)}}
.lw-q>summary{{display:flex;gap:8px;align-items:baseline;padding:12px 14px;margin-bottom:6px;font-weight:650;font-size:15.5px;line-height:1.45;
 background:var(--soft);border-bottom:1px solid var(--line)}}

.lw-qhead{{flex:1 1 0;min-width:0}} .lw-qtop{{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}} .lw-qname{{font-weight:700}} .lw-q .lw-qtext{{display:block;margin-top:4px;font-weight:500}}
.lw-q>summary:hover{{background:color-mix(in srgb,var(--acc) 5%,var(--soft))}}
/* a pick draws nothing (JL 260930, the blue bar: "I don't want this as well"); an open item shows it */
.lw-h.runs-selected,.lw-w.runs-selected{{background:transparent}}
.lw-g .lw-l{{padding-left:40px}} .lw-g>.lw-l,.lw-g>.lw-r{{padding-top:0;padding-bottom:10px}}
.lw-k{{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px;margin:16px 0 8px;padding:6px 10px;
 border-radius:7px;font:700 12.5px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.05em}}
.lw-l>.lw-k:first-child,.lw-r>.lw-k:first-child{{margin-top:4px}}
.lw-kn{{font-weight:500;text-transform:none;letter-spacing:0;opacity:.85}}
.lw-k-task,.lw-k-hyp,.lw-k-work{{color:var(--acc)}}
.lw-k-claim{{color:var(--ok)}}
.lw-k-contrib{{color:var(--warn)}}
.lw-k-found{{color:var(--mut)}}
.lw-c{{margin:0 0 16px}} .lw-g+.lw-g{{margin-top:22px}}
{work_item_css}
.lw-h{{cursor:pointer;border-radius:7px;padding:5px 8px;margin:0 -8px 6px}} .lw-h:hover{{background:var(--soft)}}
.lw-say{{color:var(--mut);font-size:14px;line-height:1.5;margin-top:3px}}
.lw-text{{font-size:14.5px}}
.lw-hline{{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:8px;align-items:baseline;line-height:1.45}}
.lw-top{{display:flex;justify-content:space-between;align-items:center;gap:8px}} .lw-body{{margin-top:3px;font-size:15px;line-height:1.5}} .lw-name{{font-weight:650}} .lw-mark{{font-size:14px}}
#rr-pop{{position:fixed;inset:0;z-index:50;background:rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center}}
#rr-pop[hidden]{{display:none}}
.rr-box{{width:min(1240px,94vw);height:90vh;background:var(--bg);border:1px solid var(--line);border-radius:12px;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 12px 40px rgba(0,0,0,.25)}}
.rr-box>header{{display:flex;gap:14px;align-items:center;padding:10px 14px;border-bottom:1px solid var(--line)}}
.rr-title{{font:600 14px ui-monospace,Menlo,monospace}} .rr-new{{margin-left:auto;font-size:13px}}
.rr-x{{border:0;background:transparent;color:inherit;font-size:18px;line-height:1;cursor:pointer;padding:2px 6px}}
.rr-frame{{flex:1;width:100%;border:0;background:var(--bg)}}
/* Story › Related Papers: one card per paper, the target venue first, its PDF inside (JL 260930) */
.rp-head{{font:700 12px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);margin:0 0 2px}}
.rp-venue{{display:flex;gap:10px;align-items:baseline;margin:22px 0 4px;padding-bottom:6px;border-bottom:1px solid var(--line);
 font-size:16px;font-weight:700}} .rp-list>.rp-venue:first-of-type{{margin-top:8px}}
.rp-group{{border:1px solid var(--line);border-radius:10px;background:var(--card);overflow:hidden;margin:0 0 4px}}
.rp-card+.rp-card{{border-top:1px solid var(--line)}}
.rp-card>summary{{list-style:none;cursor:pointer;display:grid;grid-template-columns:1em minmax(0,1fr);gap:6px;align-items:baseline;padding:10px 14px}}
.rp-card>summary::-webkit-details-marker{{display:none}} .rp-card[open]>summary .bjt-chev{{transform:rotate(90deg)}}
.rp-card>summary:hover,.rp-card[open]>summary{{background:var(--soft)}}
.rp-title{{font-weight:600;font-size:14.5px;line-height:1.4}}
.rp-sub{{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-top:2px;font-size:13px;color:var(--mut)}}
.rp-marks{{display:flex;gap:10px;flex:none}} .rp-q{{color:var(--acc);font-weight:600}}
.rp-body{{padding:6px 14px 14px calc(14px + 1em + 6px)}}
.rp-why{{font-size:14.5px;line-height:1.55;margin:4px 0 6px}}
.rp-keep{{border:1px solid var(--line);border-left:3px solid var(--acc);border-radius:8px;background:var(--soft);padding:8px 12px;margin:4px 0 10px}}
.rp-keep-h{{font:700 12px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:var(--mut)}}
.rp-keep>p{{font-size:14.5px;line-height:1.55;margin:4px 0 0}}
.rp-bears{{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 2px}}
.rp-bear{{font-size:12.5px;padding:1px 8px;border-radius:10px;border:1px solid var(--line);background:var(--card)}}
.rp-bear-ok{{color:var(--ok)}} .rp-bear-warn{{color:var(--warn)}} .rp-bear-bad{{color:#c92a2a}} .rp-bear-acc{{color:var(--acc)}} .rp-bear-mut{{color:var(--mut)}}
.rp-lw{{border:1px solid var(--line);border-radius:8px;overflow:hidden;margin:4px 0 10px}}
.rp-lw .lw-row+.lw-row{{border-top:1px solid var(--line)}} .rp-lw .lw-c{{margin:0}} .rp-lw .lw-c+.lw-c{{margin-top:8px}}
.rp-acts{{display:flex;gap:6px 16px;flex-wrap:wrap;font-size:13.5px;margin:0 0 6px}}
.rp-absd>summary{{cursor:pointer;font-size:13.5px;color:var(--mut)}} .rp-absd>p{{font-size:14px;line-height:1.55;margin:6px 0 0}}
.rp-nopdf{{font-size:13.5px;margin-top:8px}}
.rd-bar{{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:0 0 8px}} .rd-open{{margin-left:auto;font-size:13px}}
.rd-file{{border:1px solid var(--line);background:transparent;color:inherit;border-radius:999px;padding:3px 10px;font:inherit;font-size:13px;cursor:pointer}}
.rd-file.on{{border-color:var(--acc);color:var(--acc);font-weight:600}}
.rd-frame{{display:block;width:100%;height:calc(100vh - 190px);min-height:560px;border:1px solid var(--line);border-radius:8px;background:#fff}}
.rp-frame{{display:block;width:100%;height:82vh;border:1px solid var(--line);border-radius:8px;background:#fff;margin-top:8px}}
@media(max-width:1100px){{.lw-row{{grid-template-columns:minmax(0,1fr)}}
 .lw-r{{border-left:0;padding-left:40px}} .lw-head .lw-r{{display:none}}}}
code{{font:12.5px ui-monospace,Menlo,monospace}}
.sec-list{{display:grid;border:1px solid var(--line);border-radius:10px;overflow:hidden}}
.sec-row{{display:grid;grid-template-columns:2.4em minmax(0,1fr) 4.5em 12em 4.5em;gap:10px;align-items:baseline;
 padding:9px 12px;border-top:1px solid var(--line);cursor:pointer}}
.sec-row:first-child{{border-top:0}}
.sec-row:hover{{background:var(--soft)}}
.sec-row.runs-selected{{background:transparent;box-shadow:inset 3px 0 0 var(--acc)}}
.sec-num,.sec-ver{{font:500 13px ui-monospace,Menlo,monospace;color:var(--mut)}} .sec-name{{font-weight:600}}
.sec-state{{font-size:13px;white-space:nowrap}} .sec-state.ok,.sec-state.warn{{font-weight:500}} .sec-open{{font-size:13px;text-align:right;white-space:nowrap}}
.item-cards{{display:grid;gap:9px;margin:0 0 12px}}
.item-card{{border:1px solid var(--line);border-radius:10px;background:var(--bg);overflow:hidden;margin:0}}
.item-card:hover{{border-color:#b8c4d2}}
.item-card>summary{{list-style:none;cursor:pointer;padding:0}}
.item-card>summary::-webkit-details-marker{{display:none}}
.item-summary{{display:grid;grid-template-columns:1.1em auto minmax(0,1fr) auto fit-content(34%);align-items:start;gap:10px;padding:12px 13px;min-width:0}}
.item-chevron{{color:var(--mut);font-size:18px;line-height:1.2;transition:transform .12s ease}}
.item-card[open]>summary .item-chevron{{transform:rotate(90deg)}}
.item-main{{min-width:0;display:grid}}
.item-label{{font-weight:650;font-size:15.5px;line-height:1.4}} .item-title{{color:var(--mut);font-size:13.5px}}
.item-where{{color:var(--mut);font-size:12px;white-space:nowrap}} .item-status{{font-weight:650;font-size:14px;line-height:1.4;overflow-wrap:anywhere}}
.item-detail{{border-top:1px solid var(--line);padding:10px 12px 13px}}
.item-detail td .idtag,.item-detail td:first-child{{white-space:nowrap}}
.row-details{{margin-top:8px}} .row-details>summary{{cursor:pointer;color:var(--mut);font-size:12px;list-style:none}}
.row-details>summary::before{{content:"▸ "}} .row-details[open]>summary::before{{content:"▾ "}}
.item-bullets{{margin:0;padding-left:1.1em;font-size:14.5px}} .item-bullets li{{margin:2px 0}}
.item-bullets b{{font:500 12px ui-monospace,Menlo,monospace;color:var(--mut)}}
.item-note{{color:var(--mut);font-size:12.5px;line-height:1.45}} .item-sub{{color:var(--mut);font-size:12px;text-transform:uppercase;margin-right:4px}}
.item-plan>summary{{cursor:pointer;color:var(--mut);font-size:13px}}
.kv{{border:1px solid var(--line);border-radius:9px;overflow:hidden;margin:8px 0 10px;background:var(--card)}}
.kv>.item-row{{display:grid;grid-template-columns:11.5em minmax(0,1fr);border-top:1px solid var(--line);font-size:14.5px;line-height:1.6}}
.kv>.item-row:first-child{{border-top:0}}
.kv>.item-row>b{{background:var(--soft);border-right:1px solid var(--line);padding:11px 12px;font-size:11.5px;line-height:1.45;
 text-transform:uppercase;letter-spacing:.03em;font-weight:700;opacity:.75}}
.kv>.item-row>span{{padding:10px 14px;min-width:0;overflow-wrap:anywhere}}
.kv>.item-row.spine-row{{font-size:16px;line-height:1.75}}
.kv>.item-row.nolabel{{grid-template-columns:minmax(0,1fr)}}
.kv-cap{{background:var(--soft);border-bottom:1px solid var(--line);padding:6px 12px;font:700 11.5px -apple-system,sans-serif;
 text-transform:uppercase;letter-spacing:.03em;opacity:.75}}
.para{{display:block;max-width:86ch}} .para+.para{{margin-top:12px}} .sent{{display:block}} .sent+.sent{{margin-top:7px}}
.tree-job{{font-size:14.5px;margin:12px 0 4px;font-weight:650}} .tree-task{{font-size:14px;margin:8px 0 4px 18px}}
.tree-runs{{margin:0 0 6px 36px;border-left:2px solid var(--line);padding-left:10px}}
a{{color:var(--acc);text-decoration:none}} a:hover{{text-decoration:underline}}
@media(max-width:620px){{.kv>.item-row{{grid-template-columns:minmax(0,1fr)}}
 .kv>.item-row>b{{border-right:0;border-bottom:1px solid var(--line);padding:6px 12px}}
 .sec-row{{grid-template-columns:2em minmax(0,1fr) auto}} .sec-ver,.sec-state{{display:none}}
 .item-summary{{grid-template-columns:1.1em auto minmax(0,1fr) fit-content(40%)}} .item-where{{display:none}}}}
{space_css}{panel_css}
/* the paper's 12px type floor (JL 260918) holds inside the Runs panel too */
.runs-panel button,.run-list button{{font-size:12px!important}} .run-state{{font-size:12px}} .space-views-label{{font-size:12px}}
</style></head><body data-paper="{paper_id}">
<h1>📄 {title}</h1>
<div class="wb-band">{band}</div>
<div class="spaces">{space_chips}</div>
{panels}
<div id="rr-pop" hidden><div class="rr-box" role="dialog" aria-label="Run results"><header><span class="rr-title"></span>
<a class="rr-new" target="_blank" rel="noopener">Open in its own tab ↗</a><button type=button class="rr-x" title="Close (Esc)">✕</button></header>
<iframe class="rr-frame" title="Run results"></iframe></div></div>
<script>{panel_js}</script>
<script>
(function(){{
 var DEFAULT='{default_space}';
 /* the pre-260927 routes (five Spaces) still land on the view that holds their content */
 var ALIAS={{'setup':'sections','run':'sections','run/page':'sections/table','run/evidence':'sections/evidence',
  'run/supporting':'story/logic-work','run/gates':'delivery/latex/checks','run/workflow':'story',
  'story/questions':'story/logic-work',
  'ideation/pool':'ideation','ideation/evidence':'ideation','ideation/admission':'ideation',
  'story/claims':'story/logic-work','story/tasks':'story/logic-work','story/roadmap':'story/logic-work',
  'story/sections':'sections/narrative',
  'story/evidence':'sections/evidence','delivery/manuscript':'delivery/latex/artifacts',
  'delivery/sections':'sections/table','delivery/displays':'delivery/latex/artifacts',
  'delivery/checks':'delivery/latex/checks','setup/sessions':'sections/narrative'}};
 var panels={{}};
 document.querySelectorAll('.panel[data-space]').forEach(function(p){{panels[p.dataset.space]=p;}});
 function emit(name,detail){{document.dispatchEvent(new CustomEvent(name,{{detail:detail}}));}}
 function clearSel(p){{p.querySelectorAll('.runs-selected,.lw-lit').forEach(function(x){{x.classList.remove('runs-selected','lw-lit');}});}}
 function lazy(p){{p.querySelectorAll('iframe[data-src]').forEach(function(f){{
  if(!f.closest('[hidden]')&&!f.getAttribute('src'))f.setAttribute('src',f.dataset.src);}});}}
 function pick(space,parts){{
  var p=panels[space];if(!p)return;
  document.querySelectorAll('.space').forEach(function(c){{c.classList.toggle('on',c.dataset.space===space);}});
  Object.keys(panels).forEach(function(k){{panels[k].classList.toggle('on',k===space);}});
  var tabs=[].slice.call(p.querySelectorAll('.space-tab')),views=[].slice.call(p.querySelectorAll('.space-view'));
  function has(list,key,v){{return list.some(function(x){{return x.dataset[key]===v;}});}}
  function cur(list,key){{var on=list.filter(function(x){{return x.classList.contains('on');}})[0]||list[0];return on?on.dataset[key]:'';}}
  var tab=cur(tabs,'tab'),view=cur(views,'view');
  parts.forEach(function(x){{if(has(tabs,'tab',x))tab=x;else if(has(views,'view',x))view=x;}});
  tabs.forEach(function(x){{x.classList.toggle('on',x.dataset.tab===tab);}});
  views.forEach(function(x){{x.classList.toggle('on',x.dataset.view===view);}});
  var tb=tabs.filter(function(x){{return x.dataset.tab===tab;}})[0],noviews=!!(tb&&tb.hasAttribute('data-noviews'));
  var row=p.querySelector('.space-views');if(row)row.hidden=noviews;
  p.querySelectorAll('.space-pane').forEach(function(q){{
   q.hidden=!((!q.dataset.tab||q.dataset.tab===tab)&&(noviews||!q.dataset.view||q.dataset.view===view));}});
  lazy(p);
  if(p.dataset.tab!==tab||p.dataset.vw!==view){{
   if(p.dataset.tab!==undefined){{clearSel(p);emit('space-target',{{space:space,target:''}});}}
   p.dataset.tab=tab;p.dataset.vw=view;}}
  emit('space-scope',{{space:space,view:tab||view,label:tb?tb.dataset.label:'',mode:noviews?tab:(view||tab)}});
 }}
 function route(){{
  var h=decodeURIComponent((location.hash||'').slice(1));
  if(ALIAS[h])h=ALIAS[h];else if(ALIAS[h.split('/')[0]])h=ALIAS[h.split('/')[0]];
  var parts=h.split('/');
  pick(panels[parts[0]]?parts[0]:DEFAULT,parts.slice(1));
 }}
 document.addEventListener('click',function(ev){{
  var c=ev.target.closest('.space,.space-tab,.space-view');
  if(c){{
   var p=c.closest('.panel'),space=c.dataset.space||(p&&p.dataset.space);
   var parts=c.dataset.space?[]:[c.dataset.tab||c.dataset.view];
   pick(space,parts);
   var q=panels[space],t=q.dataset.tab,v=q.dataset.vw;
   history.replaceState(null,'','#'+space+(t?'/'+t:'')+(v?'/'+v:''));
   return;
  }}
  /* a fold of the Questions tree starts closed: a click on a closed fold opens and selects it; on an open, unselected fold it selects; on the selected fold it closes */
  var sm=ev.target.closest('details.qc[data-key]>summary');
  if(sm&&!ev.target.closest('a,button')){{
   var f=sm.parentElement,fp=f.closest('.panel');
   if(!f.open||!f.classList.contains('runs-selected')){{
    if(f.open)ev.preventDefault();
    clearSel(fp);f.classList.add('runs-selected');emit('space-target',{{space:fp.dataset.space,target:f.dataset.key}});return;}}
   f.classList.remove('runs-selected');
   var above=f.parentElement.closest('details.qc[data-key][open],details.item-card[data-key][open]');
   if(above)above.classList.add('runs-selected');
   emit('space-target',{{space:fp.dataset.space,target:above?above.dataset.key:''}});return;
  }}
  if(ev.target.closest('a,button,summary,.runs-panel'))return;
  var el=ev.target.closest('.sec-row[data-key],.spine-card[data-key],.lw-h[data-key],.lw-w[data-key]');if(!el)return;
  var panel=el.closest('.panel'),same=el.classList.contains('runs-selected');
  clearSel(panel);if(!same)el.classList.add('runs-selected');
  if(!same&&el.classList.contains('lw-h')){{var blk=el.closest('.lw-q')||panel,k=' '+el.dataset.key+' ';
   blk.querySelectorAll('.lw-w[data-for]').forEach(function(w){{if((' '+w.dataset.for+' ').indexOf(k)>=0){{w.classList.add('lw-lit');
    if(!w.open){{auto.add(w);w.open=true;}}}}}});}}
  emit('space-target',{{space:panel.dataset.space,target:same?'':el.dataset.key}});
 }});
 document.addEventListener('keydown',function(ev){{var r=ev.target.closest&&ev.target.closest('.sec-row');if(r&&ev.key==='Enter')r.click();}});
 /* RoadMap Draw: another drawing in studio/ swaps the canvas and the full-screen link */
 document.addEventListener('click',function(ev){{var b=ev.target.closest&&ev.target.closest('.rd-file');if(!b)return;
  var w=b.closest('.space-pane');w.querySelectorAll('.rd-file').forEach(function(x){{x.classList.toggle('on',x===b);}});
  var f=w.querySelector('.rd-frame'),a=w.querySelector('.rd-open');f.dataset.src=b.dataset.src;f.setAttribute('src',b.dataset.src);
  if(a)a.setAttribute('href',b.dataset.src);}});
 /* Opening a card selects it for the Runs panel; closing it hands the selection back to the card around it. */
 var auto=new WeakSet();   /* work a picked hypothesis opened: its toggle must not steal the pick */
 document.addEventListener('toggle',function(ev){{
  var w=ev.target;
  /* a related paper's PDF loads only when its card opens (data-pdf, so lazy() leaves it alone) */
  if(w.matches&&w.matches('details.rp-card')){{var f=w.open&&w.querySelector('iframe[data-pdf]');
   if(f&&!f.getAttribute('src'))f.setAttribute('src',f.dataset.pdf);return;}}
  if(w.matches&&w.matches('details.lw-w[data-key]')){{
   if(auto.has(w)){{auto.delete(w);return;}}
   var wp=w.closest('.panel');if(!wp)return;
   if(w.open){{clearSel(wp);w.classList.add('runs-selected');emit('space-target',{{space:wp.dataset.space,target:w.dataset.key}});}}
   else if(w.classList.contains('runs-selected')){{w.classList.remove('runs-selected');emit('space-target',{{space:wp.dataset.space,target:''}});}}
   return;}}
  var c=ev.target;if(!c.matches||!c.matches('details.item-card[data-key]'))return;
  var p=c.closest('.panel');if(!p)return;
  if(c.open){{clearSel(p);c.classList.add('runs-selected');emit('space-target',{{space:p.dataset.space,target:c.dataset.key}});return;}}
  var held=c.querySelector('.runs-selected');
  if(!c.classList.contains('runs-selected')&&!held)return;
  c.classList.remove('runs-selected');if(held)held.classList.remove('runs-selected');
  var up=c.parentElement.closest('details.item-card[data-key][open]');
  if(up)up.classList.add('runs-selected');
  emit('space-target',{{space:p.dataset.space,target:up?up.dataset.key:''}});
 }},true);
 /* a run's results open in a pop-out over the page (JL 260930); a modified click or
    "Open in its own tab" keeps the page, and Esc or a click outside closes it */
 var pop=document.getElementById('rr-pop');
 function popClose(){{pop.hidden=true;pop.querySelector('.rr-frame').removeAttribute('src');}}
 document.addEventListener('click',function(ev){{
  var a=ev.target.closest&&ev.target.closest('a[data-pop]');
  if(a&&!ev.metaKey&&!ev.ctrlKey&&!ev.shiftKey&&!ev.altKey&&ev.button===0){{
   ev.preventDefault();ev.stopPropagation();
   pop.querySelector('.rr-title').textContent=a.dataset.pop;pop.querySelector('.rr-new').href=a.href;
   pop.querySelector('.rr-frame').src=a.href;pop.hidden=false;return;}}
  if(!pop.hidden&&(ev.target===pop||(ev.target.closest&&ev.target.closest('.rr-x')))){{ev.stopPropagation();popClose();}}
 }},true);
 document.addEventListener('keydown',function(ev){{if(ev.key==='Escape'&&!pop.hidden)popClose();}});
 window.addEventListener('hashchange',route);route();
}})();
</script></body></html>"""


def _shell_band(d):
    """The band under the title: what this paper is and where it stands, read from its files."""
    s = d["stories"][0]["text"] if d["stories"] else ""
    desk = scalar(s, "desk") or paper_desk(d)
    version = scalar(s, "version")
    questions = len(d["story"][0]["qb"]) if d["story"] else 0
    sections = section_rows(d)
    built = (d.get("delivery") or {}).get("built") or ""
    parts = [desk, "Story %s" % version if version else "no Story yet" if not d["story"] else "",
             "%d questions" % questions if questions else "",
             "%d Sections" % len(sections) if sections else "",
             "built %s" % built if built else "not built yet"]
    return " · ".join(x for x in parts if x)


def render_paper(board, root, path_param):
    from live.runs_panel import PANEL_CSS, PANEL_JS
    from live.space_views import SPACE_CSS
    from live.work_items import WORK_ITEM_CSS
    d = collect(board, path_param)
    d["root"] = Path(root).resolve()
    d["sessions"] = session_rows(d)          # needs root for the pair lookup
    kinds = paper_run_types()
    chips = "".join('<button type=button class="space" data-space="%s">%s</button>' % (k, l) for k, l in SPACES)
    panels = (render_ideation(d, kinds.get("ideation", [])) + render_story(d, kinds.get("story", []))
              + render_sections(d, kinds.get("sections", [])) + render_delivery(d, kinds.get("delivery", [])))
    default = "story" if d["story"] else "ideation"
    document = _PAGE.format(title=esc(d["title"]), space_chips=chips, panels=panels, default_space=default,
                        band=esc(_shell_band(d)),
                        space_css=SPACE_CSS, panel_css=PANEL_CSS, panel_js=PANEL_JS, work_item_css=WORK_ITEM_CSS,
                        paper_id=esc(d["board"].name))
    from live.workbench_guide import mount_guide
    return mount_guide(document, "paper", {"path": path_param, "file": "board.md"},
                       ".spaces", ".panel[data-space]")



# ---- one run's results, in a pop-out (JL 260930: "for a run, how could we have a popout
# window to show the results of that run's results") -------------------------------------
_IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
_TAB_EXT = {".csv", ".tsv"}
_DOC_EXT = {".md", ".markdown", ".txt"}
_MAX_FILES, _MAX_ROWS, _MAX_DOC = 300, 50, 200_000


def run_result_url(root, task_dir, run=""):
    """`/_board/run-result?task=<Task folder>&run=<run stem>`; '' outside the root."""
    try:
        rel = Path(task_dir).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return ""
    return "/_board/run-result?task=%s%s" % (quote(rel, safe="/"), ("&run=" + quote(run, safe="")) if run else "")


def run_files(task_dir, run=""):
    """(where, files) for one run of a Task. Its own `results/<run>/` when there is one;
    else the files in `results/` named after it (`run_6a2_f01.sh` wrote
    `figures/6a2_f01_horizon_fairness_growth.png`), which is how a Task keeping one shared
    `results/` tells its runs apart; else the files whose path holds every word of that name
    (`run_fit_forecast.sh` wrote `fits_forecast/…`); else all of `results/`, said so. No
    run: all of it."""
    res = Path(task_dir) / "results"
    if not res.is_dir():
        return "no results/ folder yet", []
    every = lambda base: sorted((f for f in base.rglob("*") if f.is_file() and not f.name.startswith(".")),
                                key=lambda f: f.relative_to(res).as_posix())
    if not run:
        return "results/", every(res)
    if (res / run).is_dir():
        return "results/%s/" % run, every(res / run)
    key = re.sub(r"^run[_-]", "", run)
    named = [f for f in every(res) if key and key in f.name]
    if named:
        return "the files in results/ whose name holds %s" % key, named
    words = [w for w in key.split("_") if w]
    worded = [f for f in every(res) if words and all(w in f.relative_to(res).as_posix() for w in words)]
    if worded:
        return "the files in results/ whose path holds %s" % " and ".join(words), worded
    return "all of results/: this Task keeps one folder for every run, and no file there is named after %s" % key, every(res)


def _md_view(text):
    """Enough Markdown for a result summary: headings, bullets, pipe tables, fences, bold
    and code. Raw HTML is escaped, never run."""
    out, lines, i, para = [], text.split("\n"), 0, []

    def flush():                                  # a line break inside a paragraph stays
        if para:
            out.append("<p>%s</p>" % "<br>".join(inline(x) for x in para))
            para.clear()
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith("```"):
            flush()
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            out.append("<pre>%s</pre>" % esc("\n".join(lines[i + 1:j])))
            i = j + 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            flush()
            out.append("<h%d>%s</h%d>" % (len(m.group(1)) + 2, inline(m.group(2)), len(m.group(1)) + 2))
        elif s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-{2,}", lines[i + 1].strip()):
            flush()
            cells = lambda row: [c.strip() for c in row.strip().strip("|").split("|")]
            head, j, body = cells(s), i + 2, []
            while j < len(lines) and lines[j].strip().startswith("|"):
                body.append(cells(lines[j]))
                j += 1
            out.append("<table><tr>%s</tr>%s</table>" % ("".join("<th>%s</th>" % inline(c) for c in head),
                       "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r) for r in body)))
            i = j
            continue
        elif re.match(r"^[-*]\s+", s):
            flush()
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append("<li>%s</li>" % inline(re.sub(r"^\s*[-*]\s+", "", lines[i])))
                i += 1
            out.append("<ul>%s</ul>" % "".join(items))
            continue
        elif not s:
            flush()
        else:
            para.append(s)
        i += 1
    flush()
    return "".join(out)


def _csv_view(f):
    """The first rows of a table, and how many there are."""
    import csv
    import itertools
    delim = "\t" if f.suffix == ".tsv" else ","
    try:
        with f.open(encoding="utf-8", errors="replace", newline="") as fh:
            rows = list(itertools.islice(csv.reader(fh, delimiter=delim), _MAX_ROWS + 1))
        n = None
        if f.stat().st_size < 20_000_000:
            with f.open("rb") as fh:
                n = max(sum(1 for _ in fh) - 1, 0)
    except OSError as exc:
        return '<p class="mut">cannot read: %s</p>' % esc(exc)
    if not rows:
        return '<p class="mut">empty</p>'
    head, body = rows[0], rows[1:_MAX_ROWS + 1]
    note = ("%d rows" % n if n is not None else "a large file") + (", the first %d shown" % len(body) if n is None or n > len(body) else "")
    return ('<p class="mut">%s · %d columns</p><div class="tw"><table><tr>%s</tr>%s</table></div>'
            % (esc(note), len(head), "".join("<th>%s</th>" % esc(c) for c in head),
               "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % esc(c) for c in r) for r in body)))


_RESULT_PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>
:root{{--bg:#fff;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4e7;--acc:#3e5c84;--soft:#f6f7f9}}
@media(prefers-color-scheme:dark){{:root{{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;--line:#2c2e33;--acc:#7d9cc4;--soft:#1b1d21}}}}
body{{margin:0;padding:18px 22px 40px;background:var(--bg);color:var(--fg);font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
h1{{font-size:20px;margin:0 0 2px}} h2{{font-size:16px;margin:26px 0 8px;padding-top:12px;border-top:1px solid var(--line)}}
h3,h4,h5,h6{{font-size:14.5px;margin:14px 0 6px}} .mut{{color:var(--mut)}} a{{color:var(--acc)}}
.where{{margin:0 0 6px}} .links{{display:flex;gap:16px;flex-wrap:wrap;font-size:14px}}
code,pre{{font:12.5px/1.5 ui-monospace,Menlo,monospace}} pre{{background:var(--soft);padding:10px 12px;border-radius:8px;overflow:auto}}
.doc{{border:1px solid var(--line);border-radius:10px;padding:4px 16px 10px;margin:0 0 14px}}
.doc>h3:first-child{{font:600 13px ui-monospace,Menlo,monospace;color:var(--mut)}}
.figs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:16px}}
figure{{margin:0;border:1px solid var(--line);border-radius:10px;padding:10px;background:#fff}}
figure img{{width:100%;height:auto;display:block}} figcaption{{font:12px ui-monospace,Menlo,monospace;color:#555;margin-top:6px;word-break:break-all}}
.tw{{overflow:auto;max-height:420px;border:1px solid var(--line);border-radius:8px}}
table{{border-collapse:collapse;font-size:13px}} th,td{{border-bottom:1px solid var(--line);padding:4px 10px;text-align:left;white-space:nowrap}}
th{{position:sticky;top:0;background:var(--soft)}} .doc table{{margin:8px 0}}
ul.files{{list-style:none;padding:0;margin:0}} ul.files li{{font:13px ui-monospace,Menlo,monospace;padding:2px 0}}
</style></head><body>
{body}
</body></html>"""


def render_run_result(root, task_rel, run=""):
    """One run's results as a page: where they are, then its summaries, figures, tables
    and every other file, each opening raw. Reads only inside the root."""
    root = Path(root).resolve()
    tdir = (root / task_rel.strip("/")).resolve()
    tdir.relative_to(root)                                   # outside the root: ValueError
    if not tdir.is_dir():
        raise FileNotFoundError(task_rel)
    raw = lambda f: "/" + quote(f.resolve().relative_to(root).as_posix(), safe="/")
    where, files = run_files(tdir, run)
    more = max(len(files) - _MAX_FILES, 0)
    files = files[:_MAX_FILES]
    res = tdir / "results"
    shown = lambda f: f.relative_to(res).as_posix() if res in f.parents else f.name
    runs = tdir / "runs"
    ticket = next((f for f in sorted(runs.rglob(run + ".*")) if f.is_file()), None) if run and runs.is_dir() else None
    nb = tdir / "notebooks" / (run + ".ipynb") if run else None
    links = [('<a href="%s" target="_blank" rel="noopener">Run script ↗</a>' % esc(raw(ticket))) if ticket else "",
             ('<a href="%s" target="_blank" rel="noopener">Executed notebook ↗</a>' % esc(raw(nb))) if nb and nb.is_file() else "",
             ('<a href="%s" target="_blank" rel="noopener">Task page ↗</a>' % esc(raw(tdir / (tdir.name + ".md"))))
             if (tdir / (tdir.name + ".md")).is_file() else ""]
    body = ['<h1>%s</h1>' % esc(run or tdir.name),
            '<p class="where mut"><code>%s</code> · %s</p>' % (esc(tdir.relative_to(root).as_posix()), esc(where)),
            '<div class="links">%s</div>' % "".join(x for x in links if x)]
    rt = res / run / "runtime.yaml" if run else None
    if rt is not None and rt.is_file():
        body.append('<h2>Receipt</h2><pre>%s</pre>' % esc(rt.read_text(encoding="utf-8", errors="replace")[:4000]))
    docs = [f for f in files if f.suffix.lower() in _DOC_EXT and f.name != "runtime.yaml"]
    figs = [f for f in files if f.suffix.lower() in _IMG_EXT]
    tabs = [f for f in files if f.suffix.lower() in _TAB_EXT]
    rest = [f for f in files if f not in docs and f not in figs and f not in tabs and f != rt]
    if docs:
        body.append("<h2>Summaries · %d</h2>" % len(docs))
        for f in docs:
            text = f.read_text(encoding="utf-8", errors="replace") if f.stat().st_size <= _MAX_DOC else ""
            # a .md with no Markdown mark (heading, table row, bullet) is plain text laid out by
            # line, as fit_summary.md is (JL 260930: "How to handle this markdown render?"):
            # it shows as written
            marked = f.suffix.lower() != ".txt" and re.search(r"(?m)^(#{1,6}\s|\s*\|.*\||\s*[-*]\s)", text)
            inner = (_md_view(text) if marked else "<pre>%s</pre>" % esc(text)) if text else \
                '<p class="mut">too long to show here</p>'
            body.append('<div class="doc"><h3><a href="%s" target="_blank" rel="noopener">%s</a></h3>%s</div>'
                        % (esc(raw(f)), esc(shown(f)), inner))
    if figs:
        body.append('<h2>Figures · %d</h2><div class="figs">%s</div>' % (len(figs), "".join(
            '<figure><a href="%s" target="_blank" rel="noopener"><img loading="lazy" src="%s" alt="%s"></a>'
            '<figcaption>%s</figcaption></figure>' % (esc(raw(f)), esc(raw(f)), esc(f.name), esc(shown(f))) for f in figs)))
    for f in tabs:
        if f is tabs[0]:
            body.append("<h2>Tables · %d</h2>" % len(tabs))
        body.append('<h3><a href="%s" target="_blank" rel="noopener">%s</a></h3>%s' % (esc(raw(f)), esc(shown(f)), _csv_view(f)))
    if rest:
        body.append('<h2>Other files · %d</h2><ul class="files">%s</ul>' % (len(rest), "".join(
            '<li><a href="%s" target="_blank" rel="noopener">%s</a> <span class="mut">%s</span></li>'
            % (esc(raw(f)), esc(shown(f)), esc(_size(f))) for f in rest)))
    if more:
        body.append('<p class="mut">and %d more files, not shown</p>' % more)
    if not files:
        body.append('<p class="mut">No result file yet.</p>')
    return _RESULT_PAGE.format(title=esc(run or tdir.name), body="\n".join(body))


# ---------------------------------------------------------------- the route
class PaperWorkbenchMixin:
    """GET /_board/paper — the Board-level Paper Workbench, rendered live."""

    def paper_view(self, head_only=False):
        q = parse_qs(urlparse(self.path).query)
        p = {"path": (q.get("path") or [""])[0], "file": (q.get("file") or [""])[0]}
        got = self.target(p)
        if got[0] is None:
            return self._paper_send(("<h1>📄 paper</h1><p>%s</p>" % esc(got[1])).encode("utf-8"), 404, head_only)
        source, board = got
        if Path(source).name != "board.md":
            return self._paper_send("<h1>📄 paper</h1><p>Paper Workbench requires file=board.md.</p>".encode("utf-8"), 400, head_only)
        if scalar(read(Path(board) / "board.md"), "dialect").strip() != "paper":
            return self._paper_send("<h1>📄 paper</h1><p>This Board is not a paper Board (board.md has no <code>dialect: paper</code>).</p>".encode("utf-8"), 400, head_only)
        try:
            page = render_paper(board, self.root, p["path"])
        except Exception as exc:  # a render bug is a named row, never a blank pane
            return self._paper_send(("<h1>📄 paper</h1><p>render failed: %s</p>" % esc(exc)).encode("utf-8"), 500, head_only)
        return self._paper_send(page.encode("utf-8"), 200, head_only)

    def run_result_view(self, head_only=False):
        """GET /_board/run-result?task=<Task folder>&run=<run stem>: one run's results."""
        q = parse_qs(urlparse(self.path).query)
        try:
            page = render_run_result(self.root, (q.get("task") or [""])[0], (q.get("run") or [""])[0])
        except (ValueError, FileNotFoundError) as exc:
            return self._paper_send(("<p>No such Task folder: %s</p>" % esc(exc)).encode("utf-8"), 404, head_only)
        except Exception as exc:  # a render bug is a named row, never a blank pane
            return self._paper_send(("<p>render failed: %s</p>" % esc(exc)).encode("utf-8"), 500, head_only)
        return self._paper_send(page.encode("utf-8"), 200, head_only)

    def _paper_send(self, body, code, head_only):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

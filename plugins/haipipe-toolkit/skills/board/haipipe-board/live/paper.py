"""📄 Paper · the Board-level Paper Plugin, live and storage-less.

    GET /_board/paper?path=<board.md>&file=board.md[#<space>[/<view>]]

The Paper Plugin is the Board-altitude sibling of 🧭 Outline. Outline shows one
Page's plan, evidence and runs; this shows one paper Board's journey through
five Spaces (haipipe-plugin-paper, JL 260916 "like haipipe-plugin-outline,
you should have haipipe-plugin-paper"):

    Setup      board.md · the scaffold folders · one Codex session row per
               Section Page (JL 260916: Ideation, Story and Supporting work
               stay in the current session)
    Ideation   Story00-ideation: the Ideas (ranked) table when the page has
               one, else the plan's `Idea <n>:` divisions · evidence items ·
               the I3 admission receipt
    Story      every Story<Letter> page: C1–C8 · RQ / E / D / T / Section
               rows · compile order
    Run        every page's runs/ + results/ · gates G0–G5 read from the files
               haipipe-paper-workflow names · the Workflow map projected from
               haipipe-plugin-paper/ref/space-mapping.md

LIVE AND STORAGE-LESS, the Outline precedent: rendered from Markdown on every
open, so it can never be stale, and it needs no per-paper file. The earlier
`console/` prototype (a static data.js rebuilt by hand, one paper only) is
what this replaces. Applies to any Board whose board.md declares
`dialect: paper`; no Links key is needed.

READ-ONLY. Every row links back to the record that owns it, normally the
page's own 🧭 Outline route. The explicit copy controls write prompt text to
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
from urllib.parse import parse_qs, quote, urlparse

from src.outline_version import latest_outline, version_tag
from src.plan_shape import iter_plan_bullets

_SPACE_MAP = (Path(__file__).resolve().parents[3] / "paper"
              / "haipipe-plugin-paper" / "ref" / "space-mapping.md")
_PAIRS_DIR = Path(os.environ.get("HAIPIPE_PAIRS_DIR",
                                 Path.home() / ".config" / "haipipe" / "pairs"))

_EV_RE = re.compile(r"\bE\d{2}-(?:VALUE|CITE|DISPLAY|TABLE)-[A-Za-z0-9-]+")
_GROUP_RE = re.compile(r"^###\s+(.+?)\s+·\s+(\S+)\s*$")
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
        m = _GROUP_RE.match(line)
        if m:
            cur = {"label": m.group(1).strip(), "folder": m.group(2).strip(),
                   "stems": []}
            groups.append(cur)
            continue
        s = line.strip()
        if cur is not None and s.endswith(".md") and " " not in s:
            cur["stems"].append(s[:-3])
    return groups


def page_file(board, folder, stem):
    """The page's Markdown: folded `<folder>/<stem>/<stem>.md` first, flat
    `<folder>/<stem>.md` second; None when neither exists."""
    for rel in (Path(folder) / stem / (stem + ".md"), Path(folder) / (stem + ".md")):
        if (board / rel).is_file():
            return rel
    return None


def outline_url(path_param, rel_file, lens="div", **extra):
    url = "/_board/outline?path=%s&file=%s&lens=%s" % (
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
def collect(board, path_param):
    """Read everything the five Spaces show. Pure: no writes, no network."""
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
    stories = [p for p in pages if re.match(r"^Story[A-Z]\b", p["stem"])]
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
    d["setup"] = setup_rows(d)
    d["sessions"] = session_rows(d)
    d["ideation"] = ideation(d)
    d["story"] = [story(d, p) for p in stories]
    d["blocks"] = project_blocks(d)
    d["disc"] = project_discoveries(d)
    d["delivery"] = delivery_info(d)
    d["judge"] = judgment_runs(d)
    d["hero"] = hero_evidence(d)
    d["runs"] = run_rows(d)
    d["evidence_runs"] = evidence_runs(d)
    d["supporting"] = supporting_tree(d)
    d["gates"] = gates(d)
    d["workflow_map"] = read(_SPACE_MAP)
    return d


def paper_desk(d):
    """The desk name, read from a real B group (`Ba-MISQ-Main` → MISQ) or, before
    any Section group exists, from the Story's C8 target cell (`MISQ · 1`)."""
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


def setup_rows(d):
    """The scaffold haipipe-paper §📂 names, each present or missing on disk,
    spoken in the paper's own names once the desk is known (JL 260916: the
    desk is MISQ, so say Ba-MISQ-Main, not B?-<desk>-Main). delivery/ is a
    generated projection, so it is not a setup row; gate G4 reports it."""
    desk = paper_desk(d)
    rows = [{"name": "board.md", "role": "the Board · paper-root", "state": "present"}]
    s00 = d["story00"]["stem"] if d["story00"] else ""
    rows.append({"name": ("A1-Story/%s/" % s00) if s00 else "A1-Story/Story00-<direction>/",
                 "role": "the idea pool", "state": "present" if s00 else "missing"})
    if d["stories"]:
        for st in d["stories"]:
            rows.append({"name": "A1-Story/%s/" % st["stem"], "role": "one prospective Story per idea", "state": "present"})
    else:
        rows.append({"name": "A1-Story/Story<Letter>-%s-<idea-slug>/" % (desk or "<desk>"),
                     "role": "one prospective Story per idea", "state": "missing · minted by the I3 handoff"})
    for letter, kind, role in (("Ba", "Main", "named Main Section Pages"),
                               ("Bb", "Appendix", "named Appendix Section Pages"),
                               ("Bc", "Round", "one RD page per feedback batch")):
        hit = next((g for g in d["groups"] if re.match(r"^B[a-z]-.+-%s$" % kind, g["folder"])), None)
        if hit:
            rows.append({"name": hit["folder"] + "/", "role": role + " · %d page(s)" % len(hit["stems"]), "state": "present"})
        else:
            rows.append({"name": "%s-%s-%s/" % (letter, desk or "<desk>", kind), "role": role,
                         "state": "missing" if desk else "missing · desk not chosen yet"})
    return rows


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
        codex = (j.get("providers") or {}).get("codex") or {}
        out[name] = {"file": f.name, "codex": codex.get("session_id", ""),
                     "updated": str(j.get("updated_at", ""))[:10]}
    return out


def session_rows(d):
    """One Codex session per Section Page (JL 260916). Ideation, Story and
    Supporting work stay in the current session, so only S- pages get rows.
    The pair name is a plan until a manifest with exactly that name exists."""
    root = d.get("root")
    pairs = _pairs_for(root) if root else {}
    rows = []
    for p in d["sections"]:
        parts = p["stem"].split("-")           # S-<desk>-<Main|Appendix>-<N>-<Title>
        desk = parts[1].lower() if len(parts) > 1 else "paper"
        title = "-".join(parts[4:] if len(parts) > 4 else parts[3:]).lower()
        pair = "paper-%s-%s" % (desk, title)
        hit = pairs.get(pair) or pairs.get(p["stem"].lower())
        rows.append({"stem": p["stem"], "rel": p["rel"], "group": p["group"]["folder"],
                     "pair": pair,
                     "state": ("codex %s · %s" % (hit["codex"][:8], hit["updated"]))
                     if hit and hit["codex"] else "no session · plan"})
    return rows


def idea_divisions(text):
    """`### N · Idea <n>: <title>` divisions under Content → {n: {"title", "fields"}}
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
    evidence card in haipipe-plugin-outline, I can open and hide it")."""
    p = d["story00"]
    if p is None:
        return {"present": False}
    b = d["board"]
    folder = (b / p["rel"]).parent if p["rel"] else None
    out = {"present": True, "stem": p["stem"], "rel": p["rel"],
           "state": clean(scalar(p["text"], "state", "⬜ no state line")),
           "ideas": [], "source": "", "items": [], "receipts": [], "plan": ""}
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
    # ② else the plan's `Idea <n>: <title>` divisions (an Ideation Page before Content)
    plan = latest_outline(folder / "outline", p["stem"]) if folder else None
    if plan is not None:
        ptext = read(plan)
        out["plan"] = "%s · %s · approved: %s" % (
            plan.name, version_tag(plan) or "legacy",
            clean(scalar(ptext, "approved", "⬜")))
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
        items = read(folder / "outline" / (p["stem"] + "-evidence-items.md"))
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


_JUDGE_PREFIXES = ("ridea-", "rclaim-", "rtask-", "rnarra-")
_ADDR_RE = re.compile(r"\bb(\d{2})(?:[.\s_-]?j(\d{2}))?(?:[.\s_-]?t(\d{2}))?(?:[.\s_-]?r(\d{2}))?\b")


def _frontmatter(text):
    """`key: value` lines of a leading --- block → dict (a ticket's head)."""
    m = re.match(r"^---\n(.*?)\n---", text or "", re.S)
    out = {}
    for line in (m.group(1) if m else "").splitlines():
        k, _, v = line.partition(":")
        if _ and k.strip():
            out[k.strip()] = v.strip()
    return out


def judgment_runs(d):
    """The Paper judgment family on Story00 and the Story pages: ridea · rclaim
    · rtask · rnarra tickets whose `target:` names the row they discuss
    (i01 · E5 · T1 · S-<desk>-Main-1-…). Keyed by (page stem, target)."""
    b = d["board"]
    out = {}
    pages = ([d["story00"]] if d["story00"] else []) + d["stories"]
    for p in pages:
        if not p["rel"]:
            continue
        folder = (b / p["rel"]).parent
        runs = folder / "runs"
        if not runs.is_dir():
            continue
        for f in sorted(runs.iterdir()):
            if f.is_dir() or not f.name.startswith(_JUDGE_PREFIXES):
                continue
            rid = f.name.split(".")[0]
            fm = _frontmatter(read(f))
            rt = read(folder / "results" / rid / "runtime.yaml")
            info = {"run": rid, "rel": p["rel"], "page": p["stem"],
                    "status": scalar(rt, "status", "no runtime"), "step": scalar(rt, "step", "")}
            target = fm.get("target", "").strip()
            if target:
                out[(p["stem"], target)] = info
    return out


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


def _addresses(text):
    """`b02.j01 b03 b04` (or b02j01, comma-separated) → ["b02j01", "b03", "b04"]."""
    out = []
    for m in _ADDR_RE.finditer(text or ""):
        a = "".join(l + n for l, n in zip("bjtr", m.groups()) if n)
        if a not in out:
            out.append(a)
    return out


def paper_scope(d):
    """The Task-home addresses this paper claims: board.md `blocks:` plus every
    bNN[.jNN[.tNN]] address written on a Story C7 row. Empty = nothing claimed."""
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
    bNN[.jNN[.tNN]] address written on a Story C6 row."""
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
    No address → `no address yet`."""
    found_all, seen = [], set()
    for cell in cells:
        for m in _ADDR_RE.finditer(cell):
            one = _resolve_address(d, m)
            if one["address"] not in seen:
                seen.add(one["address"]); found_all.append(one)
    if not found_all:
        return {"address": "", "levels": [], "path": "", "state": "no address yet", "all": []}
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
         "sections": [], "sec_h": [], "order": []}
    s["sec_h"] = _table_headers(t, r"S-[\w-]+(?:\s*\(.*\))?") or []
    s["spine"] = [(n, title, parse_division(division_body(t, n)))
                  for n, title in s["divisions"] if n in (1, 2, 4)]
    for c in table_rows(t, r"S-[\w-]+(?:\s*\(.*\))?"):
        sid = c[0].split(" (")[0].strip()
        page = next((x for x in d["sections"] if x["stem"] == sid), None)
        s["sections"].append({"id": sid, "target": c[0][len(sid):].strip(" ()"),
                              "question": c[1] if len(c) > 1 else "", "cells": c,
                              "rel": page["rel"] if page else None,
                              "page_state": clean(scalar(page["text"], "state", "")) if page else ""})
    m = re.search(r"<!-- haipipe:compile-order:start -->(.*?)<!-- haipipe:compile-order:end -->", t, re.S)
    if m:
        s["order"] = [l.strip()[2:].strip() for l in m.group(1).splitlines()
                      if l.strip().startswith("- ")]
    return s


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


_LOCAL_RUN_RE = re.compile(r"`?((?:re-|rp-|rd|pj|pm-|pa-|pr-)[\w.-]+)`?")
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
    """`Page · Evidence Item · reuse · pj06t01r02 → results/…/result.yaml` → {mode, run, result}."""
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
    items = read(folder / "outline" / (stem + "-evidence-items.md"))
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
                    "status": f.get("status") or f.get("accepted") or f.get("verified") or "contract only"})
    return out


def hero_evidence(d):
    """The few Results the paper hangs on: every DISPLAY item on a Main page
    (what the paper prints) and every VALUE item on the Abstract page (what
    the paper states first). Section pages keep their full Evidence Space."""
    b = d["board"]
    out = []
    for p in d["sections"]:
        if not p["rel"] or not p["group"]["folder"].endswith("-Main"):
            continue
        folder = (b / p["rel"]).parent
        abstract = p["stem"].lower().endswith("abstract")
        for it in _page_items(folder, p["stem"]):
            if it["retired"]:
                continue
            if it["type"] in ("DISPLAY", "TABLE") or (abstract and it["type"] == "VALUE"):
                it.update({"page": p["stem"], "rel": p["rel"],
                           "why": "printed display" if it["type"] != "VALUE" else "stated in the Abstract"})
                out.append(it)
    return out

_KIND = (("ridea-", "Judgment · idea"), ("rclaim-", "Judgment · claim"),
         ("rtask-", "Judgment · task"), ("rnarra-", "Judgment · narrative"),
         ("rp-struct", "Page Writing · structure"), ("rp-scratch", "Page Writing · scratch"),
         ("rp-sec", "Page Writing · section"), ("rp-para", "Page Writing · paragraph"),
         ("rp", "Page Writing · legacy rp"), ("re-", "Page Evidence"),
         ("rd", "Delivery"), ("pm-", "Paper-local · Main"), ("pa-", "Paper-local · Appendix"),
         ("pr-", "Paper-local · Round"), ("pj", "Paper-local · legacy pj"))


_EVIDENCE_PREFIXES = ("re-", "pj", "pm-", "pa-", "pr-")


def run_rows(d):
    """Every page's runs/ tickets joined to their results/ twin by stem, typed
    as the Page Run families name them: page (RP writing · RD delivery ·
    judgment) or evidence (RE, and the legacy paper-local pj/pm-/pa-/pr-)."""
    b = d["board"]
    rows = []
    for p in d["pages"]:
        if not p["rel"]:
            continue
        folder = (b / p["rel"]).parent
        runs = folder / "runs"
        if not runs.is_dir():
            continue
        for f in sorted(runs.iterdir()):
            if f.name.startswith(".") or f.is_dir():
                continue
            rid = f.stem                                   # rp-scratch-01_C1.P1.md keeps its dotted target
            kind = next((k for pre, k in _KIND if rid.startswith(pre)), "Other")
            res = folder / "results" / rid
            rt = read(res / "runtime.yaml") if res.is_dir() else ""
            rows.append({"page": p["stem"], "rel": p["rel"], "run": rid, "kind": kind,
                         "family": "evidence" if rid.startswith(_EVIDENCE_PREFIXES) else "page",
                         "status": scalar(rt, "status"), "step": scalar(rt, "step"),
                         "has_result": res.is_dir(),
                         "result": "Run + Result" if res.is_dir() else "Run exists · Result missing"})
    return rows


def evidence_runs(d):
    """Per page: every Evidence Item joined to the Local Run it names, plus any
    evidence ticket no item names. The item is the authority; the ticket is found."""
    b = d["board"]
    out = []
    tickets = {}
    for r in d["runs"]:
        if r["family"] == "evidence":
            tickets.setdefault(r["page"], []).append(r)
    for p in d["pages"]:
        if not p["rel"] or not p["stem"].startswith(("S-", "RD", "Story")):
            continue
        items = _page_items((b / p["rel"]).parent, p["stem"])
        mine = tickets.get(p["stem"], [])
        if not items and not mine:
            continue
        used, rows = set(), []
        for it in items:
            want = it["local"]["run"]
            hit = next((t for t in mine if want and (t["run"] == want or t["run"].startswith(want + "_") or t["run"].startswith(want))), None)
            if hit:
                used.add(hit["run"])
            rows.append({"item": it, "ticket": hit, "want": want})
        orphans = [t for t in mine if t["run"] not in used]
        out.append({"page": p["stem"], "rel": p["rel"], "rows": rows, "orphans": orphans})
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
    g.append(("G2", "work → Story", "— read on the Story's C5 support"))
    rows = sum(len(s["sections"]) for s in d["story"])
    minted = sum(1 for s in d["story"] for r in s["sections"] if r["rel"])
    g.append(("G3", "Story → Section",
              "%d of %d C8 rows have a Section page" % (minted, rows) if rows else "⬜ no C8 rows"))
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


# ---------------------------------------------------------------- render
_PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
:root{{--bg:#ffffff;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4e7;--card:#fff;
 --warn:#b3541e;--ok:#3a7d44;--acc:#3e5c84}}
@media(prefers-color-scheme:dark){{:root{{--bg:#161719;--fg:#e8e8e6;
 --mut:#9a9a97;--line:#2c2e33;--card:#1d1f23;--warn:#e0955a;--ok:#7dbb87;
 --acc:#7d9cc4}}}}
body{{margin:0;padding:16px;background:var(--bg);color:var(--fg);
 font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
h1{{font-size:17px;margin:0 0 2px}} .mut{{color:var(--mut);font-size:13px}}
.spaces,.subchips{{display:flex;gap:5px;margin:10px 0 6px;flex-wrap:wrap}}
.subchips{{margin:0 0 10px;padding-left:2px}}
.space,.chip{{font:600 11.5px -apple-system,sans-serif;border:1px solid var(--line);
 border-radius:8px;padding:3px 9px;cursor:pointer;background:var(--card);
 color:var(--fg);white-space:nowrap;flex:0 0 auto}}
.space.on,.chip.on{{border-color:var(--acc);color:var(--acc)}}
.subchips .chip{{font-weight:500;color:var(--mut);background:transparent}}
.subchips .chip.on{{color:var(--acc);background:var(--card)}}
.ok{{color:var(--ok);font-weight:600}} .warn{{color:var(--warn);font-weight:600}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;
 padding:10px 14px;margin:0 0 10px}}
.card h2{{font-size:15px;margin:0 0 4px;display:flex;gap:8px;align-items:baseline}}
.card h2 .tally{{margin-left:auto;flex:none;font:600 11px ui-monospace,Menlo,monospace;color:var(--mut)}}
.brief{{color:var(--mut);font-size:13.5px;margin:0 0 8px;padding-bottom:8px;border-bottom:1px solid var(--line)}}
.sub{{font:600 12.5px -apple-system,sans-serif;color:var(--mut);text-transform:uppercase;margin:8px 0 2px}}
table.grid{{border-collapse:collapse;width:100%;font-size:13.5px;line-height:1.5;margin:4px 0 6px}}
table.grid th{{text-align:left;font:600 11px -apple-system,sans-serif;color:var(--mut);
 text-transform:uppercase;letter-spacing:.03em;padding:4px 8px 4px 0;border-bottom:1px solid var(--line)}}
table.grid td{{padding:4px 8px 4px 0;border-bottom:1px solid var(--line);vertical-align:top}}
table.grid tr:last-child td{{border-bottom:0}}
.idtag,.path{{font:500 12px ui-monospace,Menlo,monospace;color:var(--mut)}}
.path{{overflow-wrap:anywhere}}
.evtag{{display:inline;white-space:nowrap;font:12px/1.45 ui-monospace,Menlo,monospace;
 border:1px dashed color-mix(in srgb,currentColor 26%,transparent);
 background:color-mix(in srgb,currentColor 8%,transparent);border-radius:4px;padding:0 4px;margin-right:3px}}
.item-cards{{display:grid;gap:7px;margin-top:6px}}
.item-card{{border:1px solid var(--line);border-radius:9px;background:var(--bg);overflow:hidden;margin:0}}
.item-card:hover{{border-color:#b8c4d2}} .item-card[open]{{border-color:var(--acc)}}
.item-card>summary{{list-style:none;cursor:pointer;padding:0;font:inherit;text-transform:none;letter-spacing:normal;color:inherit}}
.item-card>summary::-webkit-details-marker{{display:none}}
.item-card>summary:before,.item-card[open]>summary:before{{content:none}}
.item-summary{{display:grid;grid-template-columns:1.1em auto minmax(0,1fr) auto auto;align-items:center;gap:7px;padding:9px 10px;min-width:0}}
.item-chevron{{color:var(--mut);font-size:18px;line-height:1;transition:transform .12s ease}}
.item-card[open] .item-chevron{{transform:rotate(90deg)}}
.item-kind{{color:var(--acc);font:650 10px ui-monospace,Menlo,monospace;letter-spacing:.03em;
 border:1px solid var(--acc);border-radius:999px;padding:0 6px;white-space:nowrap}}
.item-main{{min-width:0;display:grid;gap:0}}
.item-label{{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-weight:650;font-size:14px}}
.item-title{{color:var(--mut);font-size:12.5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.item-where{{justify-self:end;color:var(--mut);font-size:11px;white-space:nowrap}}
.item-status{{font-weight:650;font-size:13px;white-space:nowrap}}
.item-detail{{border-top:1px solid var(--line);padding:4px 11px 10px}}
.item-row{{display:grid;grid-template-columns:8.5em minmax(0,1fr);gap:8px;padding:3px 0;font-size:12.5px;line-height:1.45}}
.item-row>b{{color:var(--mut);font-size:10.5px;text-transform:uppercase;letter-spacing:.025em;font-weight:650;padding-top:2px}}
.item-bullets{{margin:0;padding-left:1.1em}} .item-bullets li{{margin:2px 0}} .item-bullets b{{font:500 11px ui-monospace,Menlo,monospace;color:var(--mut)}}
.item-note{{color:var(--mut);font-size:12px;line-height:1.45}}
.spine-row{{grid-template-columns:9.5em minmax(0,1fr);font-size:13.5px;line-height:1.55}}
.spine-row code{{font:12px ui-monospace,Menlo,monospace;background:var(--line);border-radius:4px;padding:0 4px}}
.tree-job{{margin:8px 0 2px;font-weight:650;font-size:13px}} .tree-task{{margin:6px 0 2px 18px;font-size:13px}}
.tree-runs{{margin:0 0 6px 36px;border-left:2px solid var(--line);padding-left:10px}}
pre.path{{font:12px/1.5 ui-monospace,Menlo,monospace;background:var(--line);border-radius:6px;padding:8px 10px;margin:6px 0 0;white-space:pre-wrap}}
.item-sub{{color:var(--mut);font-size:10.5px;text-transform:uppercase;letter-spacing:.025em;margin-right:4px}}
@media(max-width:560px){{.item-summary{{grid-template-columns:1.1em auto minmax(0,1fr) auto;gap:6px;padding:8px 9px}}.item-where{{display:none}}}}
a{{color:var(--acc);text-decoration:none}} a:hover{{text-decoration:underline}}
.panel{{display:none}} .panel.on{{display:block}}
.view{{display:none}} .view.on{{display:block}}
.gates{{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:13px;margin:6px 0 2px}}
.gates b{{font:600 11px ui-monospace,Menlo,monospace;color:var(--mut);margin-right:4px}}
details{{margin:4px 0 0}}
summary{{cursor:pointer;font:600 12px -apple-system,sans-serif;color:var(--mut);
 text-transform:uppercase;letter-spacing:.03em;padding:3px 0;list-style:none}}
summary::-webkit-details-marker{{display:none}}
summary:before{{content:"▸ ";color:var(--mut)}} details[open]>summary:before{{content:"▾ "}}
@media(max-width:560px){{body{{padding:12px}}table.grid{{font-size:12.5px}}}}
{read_css}{copy_css}</style></head><body data-paper="{paper_id}" data-board="{board_src}">
<h1>📄 {title}</h1>
<div class="mut">{spine}</div>
<div class="spaces" id="spaces">{space_chips}</div>
{panels}
<script>
(function(){{
  var SP=['setup','ideation','story','run','delivery'];
  function pick(space,view){{
    document.querySelectorAll('.space').forEach(function(c){{c.classList.toggle('on',c.dataset.space===space)}});
    document.querySelectorAll('.panel').forEach(function(p){{p.classList.toggle('on',p.dataset.space===space)}});
    var panel=document.querySelector('.panel[data-space="'+space+'"]'); if(!panel) return;
    var views=panel.querySelectorAll('.view'); var chips=panel.querySelectorAll('.chip');
    var ids=[].map.call(views,function(v){{return v.dataset.view}});
    if(ids.indexOf(view)<0) view=ids[0];
    views.forEach(function(v){{v.classList.toggle('on',v.dataset.view===view)}});
    chips.forEach(function(c){{c.classList.toggle('on',c.dataset.view===view)}});
  }}
  function route(){{
    var h=(location.hash||'').slice(1).split('/');
    var space=SP.indexOf(h[0])>=0?h[0]:'{default_space}';
    pick(space,h[1]||'');
  }}
  document.addEventListener('click',function(e){{
    var c=e.target.closest('.space,.chip'); if(!c) return;
    var panel=c.closest('.panel');
    var space=c.dataset.space||(panel&&panel.dataset.space);
    var view=c.dataset.view||'';
    location.hash='#'+space+(view?'/'+view:'');
  }});
  window.addEventListener('hashchange',route); route();
}})();
</script>{copy_js}</body></html>"""


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
    # compile order: the manifest's, else the Story's C8 block
    order = []
    if man and isinstance(man.get("order"), dict):
        order = [(x, "main") for x in man["order"].get("main", [])] + [(x, "appendix") for x in man["order"].get("appendix", [])]
        info["order_src"] = "build-manifest.json (%s)" % (man.get("order_source") or "").split(" · ")[0]
    elif d["story"] and d["story"][0]["order"]:
        order = [(x, "main" if "-Main-" in x else "appendix") for x in d["story"][0]["order"]]
        info["order_src"] = "Story C8 compile order (no build yet)"
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


def _views(space, views, foot=""):
    """views: [(id, label, html)] → sub-chips + view panels; `foot` (the Space's
    backend Markdown) stays visible under every view."""
    chips = "".join('<span class="chip" data-view="%s">%s</span>' % (esc(i), esc(l))
                    for i, l, _ in views)
    body = "".join('<div class="view" data-view="%s">%s</div>' % (esc(i), h)
                   for i, _, h in views)
    return ('<div class="panel" data-space="%s"><div class="subchips">%s</div>%s%s</div>'
            % (esc(space), chips, body, foot))


def _sources_html(d, space):
    """The backend of one Space: every Markdown file, engine receipt and folder
    it was read from, as repo-relative paths. Nothing on the Space comes from
    anywhere else; the plugin's own labels live in live/paper.py (Tools)."""
    b = d["board"]
    rows = []
    def add(label, path, note=""):
        if path is None:
            return
        pth = path if isinstance(path, Path) else (b / path)
        ok = pth.exists()
        rows.append((label, '%s <code>%s</code>%s' % ('<span class="ok">✓</span>' if ok else '<span class="mut">⬜</span>',
                                                       esc(_repo_rel(d, pth)), (' <span class="mut">%s</span>' % esc(note)) if note else "")))
    pages = [pg for pg in d["pages"] if pg["rel"]]
    s00 = d["story00"]
    if space == "setup":
        add("board", "board.md", "## Pages groups · dialect · blocks · Links")
        rows.append(("sessions", '<code>%s</code> <span class="mut">pair manifests (JSON), one per Codex session</span>' % esc(str(_PAIRS_DIR))))
    elif space == "ideation":
        if s00 and s00["rel"]:
            folder = (b / s00["rel"]).parent
            add("idea pool page", s00["rel"])
            for f in sorted(folder.glob("outline/*-outline-v*.md"))[-1:]:
                add("plan (latest)", f, "Ideas (ranked) table · Idea divisions")
            add("evidence items", folder / "outline" / (s00["stem"] + "-evidence-items.md"))
            for name, note in (("workflow/selection.yaml", "I3 receipt"), ("handoff/paper-ideation.yaml", "handoff"), ("projection/paper-ideation-sync.yaml", "sync")):
                if (folder / name).exists():
                    add("receipt", folder / name, note)
        else:
            rows.append(("idea pool", '<span class="mut">no Story00 page on board.md yet</span>'))
    elif space == "story":
        for st in d["stories"]:
            add("Story page", st["rel"], "C1–C8 · compile order · judgment Run tickets in runs/")
        n = sum(1 for pg in d["sections"] if pg["rel"])
        rows.append(("hero evidence", '<code>%s</code> <span class="mut">%d Section page(s): outline/&lt;stem&gt;-evidence-items.md</span>' % (esc(_repo_rel(d, b)), n)))
        add("task home", d["blocks"]["dir"], "bNN/jNN/tNN folders · runtime.yaml receipts")
        add("discovery home", d["disc"]["dir"], "bNN/jNN/tNN folders · discovery.yaml")
    elif space == "run":
        n_t = len(d["runs"]); n_r = sum(1 for r in d["runs"] if r["has_result"])
        rows.append(("page runs", '<code>%s</code> <span class="mut">%d page(s): runs/ tickets (%d) · results/&lt;run&gt;/runtime.yaml (%d)</span>' % (esc(_repo_rel(d, b)), len(pages), n_t, n_r)))
        rows.append(("evidence items", '<code>%s</code> <span class="mut">every page\'s outline/&lt;stem&gt;-evidence-items.md: Local Run · Supporting Runs lines</span>' % esc(_repo_rel(d, b))))
        add("task home", d["blocks"]["dir"], "tickets + runtime.yaml")
        add("discovery home", d["disc"]["dir"], "tickets + runtime.yaml")
        add("workflow map", _SPACE_MAP, "Workflow map + Folder tree × Spec or control tables")
        add("gate G4", "delivery/build-manifest.json", "engine receipt")
    elif space == "delivery":
        add("build config", "delivery/paper-build.toml", "haipipe-paper-assemble")
        add("build receipt", "delivery/build-manifest.json", "engine receipt, never edited")
        add("display register", "delivery/display-register.md", "generated")
        add("returned files", "delivery/word-feedback", "read, never built from")
        for r in d["rounds"]:
            add("Round page", r["rel"])
        add("venue", "board.md", "Links · venue-page")
    if not rows:
        return ""
    return ('<div class="card"><h2>backend Markdown<span class="tally">%s Space</span></h2>'
            '<div class="brief">Every word above is read from these files on every open. YAML, JSON and TOML here are receipts a program wrote; '
            'they are shown, never edited. The Space\'s own labels and hints are the plugin\'s, in live/paper.py and assets/js/10-drawer/09-plugin-paper.js.</div>%s</div>'
            % (esc(space), _kv(rows, "spine-row")))


def render_setup(d):
    """Setup Space: one Folder & Page table (the scaffold, present or missing,
    with the pages each folder holds) and the per-Section Codex sessions.
    JL 260916: Board and Folder & Page said the same thing, so they are one."""
    desk = paper_desk(d)
    by_folder = {g["folder"]: g for g in d["groups"]}
    rows = []
    for r in d["setup"]:
        folder = r["name"].rstrip("/")
        g = by_folder.get(folder) or by_folder.get(folder.split("/")[0]) if "/" in folder else by_folder.get(folder)
        pages = ""
        if folder == "board.md":
            pages = '<span class="mut">the roster · %d group(s)</span>' % len(d["groups"])
        elif folder.startswith("A1-Story/"):
            stem = folder.split("/", 1)[1]
            rel = page_file(d["board"], "A1-Story", stem)
            pages = _link(d, rel, stem) if rel else ""
        elif g:
            pages = " · ".join(_link(d, page_file(d["board"], g["folder"], st), st) for st in g["stems"])
        rows.append(('<span class="path">%s</span>' % esc(r["name"]), esc(r["role"]),
                     '<span class="%s">%s</span>' % ("ok" if r["state"].startswith("present") else "warn", esc(r["state"])),
                     pages))
    brief = " · ".join(x for x in (("desk " + desk) if desk else "no desk yet",
                                    ("dialect: " + d["dialect"]) if d["dialect"] else "",
                                    d["close"] or "no close: line") if x)
    folders_html = ('<div class="card"><h2>Folder &amp; Page<span class="tally">%d group(s) · %d page(s)</span></h2>'
                    '<div class="brief">%s</div>%s</div>'
                    % (len(d["groups"]), len(d["pages"]), esc(brief),
                       _table(["folder", "role", "state", "pages"], rows)))
    srows = [(_link(d, r["rel"], r["stem"]), '<span class="path">%s</span>' % esc(r["group"]),
              '<span class="idtag">%s</span>' % esc(r["pair"]),
              '<span class="%s">%s</span>' % ("ok" if r["state"].startswith("codex") else "mut", esc(r["state"])))
             for r in d["sessions"]]
    sessions_html = ('<div class="card"><h2>Codex sessions<span class="tally">%d Section page(s)</span></h2>'
                     '<div class="brief">One Codex session per Section Page. Ideation, Story and '
                     'Supporting work stay in the current session. A row is a plan until a pair '
                     'manifest with exactly that name exists for this workspace.</div>%s</div>'
                     % (len(srows), _table(["Section Page", "group", "pair name", "session"], srows)
                        or _empty("no Section Page yet · rows appear when a C8 row is released and its page is minted")))
    return _views("setup", [("folders", "Folder & Page", folders_html),
                            ("sessions", "Codex sessions", sessions_html)], foot=_sources_html(d, "setup"))


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


def _card(cid, kind, label, sub, where, status, status_cls, rows):
    """One collapsed card, the Evidence-card shape: chevron · kind pill · label
    with a muted subline · where · status; open = label/value rows."""
    detail = _kv(rows)
    # say a thing once: a subline that is empty, a dash, or the same words as `where` is dropped
    plain = lambda h: re.sub(r"<[^>]+>", "", h or "").strip()
    subline = "" if plain(sub) in ("", "—") or plain(sub) == plain(where) else '<span class="item-title">%s</span>' % sub
    return ('<details class="item-card" id="%s"><summary><div class="item-summary">'
            '<span class="item-chevron">›</span><span class="item-kind">%s</span>'
            '<div class="item-main"><span class="item-label">%s</span>%s</div>'
            '<span class="item-where">%s</span><span class="item-status %s">%s</span>'
            '</div></summary><div class="item-detail">%s</div></details>'
            % (esc(cid), esc(kind), esc(label), subline, where, status_cls, esc(status), detail))


def _repo_rel(d, path):
    """A path as the chat needs it: relative to the repository root."""
    if not path:
        return ""
    pth = Path(path)
    if not pth.is_absolute():
        pth = d["board"] / pth
    try:
        return str(pth.resolve().relative_to(Path(d["root"]).resolve())).replace(os.sep, "/")
    except (ValueError, KeyError):
        return str(path)


def _srcd(d, path, ref, card_html):
    """Stamp a card with the Markdown it was read from (data-src) and the row
    it shows (data-ref), so `copy to chat` can cite the truth source."""
    i = card_html.find('<details class="item-card"')
    j = card_html.find(">", i) if i >= 0 else -1
    if j < 0:
        return card_html
    return card_html[:j] + ' data-src="%s" data-ref="%s"' % (esc(_repo_rel(d, path)), esc(ref)) + card_html[j:]


def _status_cls(text):
    t = (text or "").upper()
    if t.startswith("NOT ") or t.startswith("NO ") or "ABSENT" in t or "MISSING" in t:
        return "mut"
    if "✅" in t or "PROCEED" in t or "ESTABLISHED" in t or "ALLOCATED" in t or "READY" in t or "ACCEPTED" in t:
        return "ok"
    if "⚠" in t or "🔨" in t or "PROVISIONAL" in t or "PARTIAL" in t or "WAITING" in t:
        return "warn"
    return "mut"


def _judge_row(d, page_stem, target, kind):
    """The discussion Run behind a card, or the honest `no … Run yet`."""
    hit = d["judge"].get((page_stem, target))
    if not hit:
        return ("Discussion", '<span class="mut">no %s Run yet · a ticket runs/%s-NN_&lt;slug&gt;.md with '
                              '<code>target: %s</code> would appear here</span>' % (esc(kind), esc(kind), esc(target)))
    return ("Discussion", '%s · %s%s · %s' % (
        _link(d, hit["rel"], hit["run"], lens="run", run=hit["run"]), esc(hit["status"]),
        (" · " + esc(hit["step"])) if hit["step"] else "", esc(hit["page"])))


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
    chips = "".join('<span class="evtag">%s</span>' % esc(c) for c in x.get("chips", []))
    substance = x.get("substance") or []
    first = next((" ".join(v) for k, v in substance
                  if k.lower().startswith(("hypothesis", "research question", "one-sentence"))), "")
    sub = esc(first or ("%d bullet(s)" % len(x["bullets"]) if x["bullets"] else "")) + ((" " + chips) if chips else "")
    where = (_link(d, i["rel"], x["address"], focus=x["address"]) if x.get("address")
             else esc(x.get("went") or ""))
    verdict = x.get("verdict") or "⬜ open"
    rows = []
    # the idea itself, in the page's own order
    for k, v in substance:
        rows.append((k, _field_html(v)))
    if x["bullets"]:
        blist = []
        for bl in x["bullets"]:
            note = " ".join(bl["notes"])
            blist.append('<li><b>%s</b> %s%s%s</li>' % (
                esc(bl["bullet"]), esc(bl["head"]),
                ('<div class="item-note">%s</div>' % esc(note)) if note else "",
                ('<div class="item-note">Evidence: %s</div>' % esc(bl["evidence"])) if bl["evidence"] else ""))
        rows.append(("Plan bullets" if substance else "Bullets", '<ul class="item-bullets">%s</ul>' % "".join(blist)))
    if x["items"]:
        rows.append(("Evidence items", "".join(
            '<div><span class="idtag">%s</span> %s <span class="%s">%s</span></div>' % (
                esc(it["id"]), esc(it["desc"]), "ok" if "✅" in it["verified"] else "mut", esc(it["verified"]))
            for it in x["items"])))
    # then the comparison metadata the Ideas (ranked) table carries
    fields = [(l, esc(v)) for l, v in x.get("fields", []) if l.lower() not in ("verdict", "went to")]
    if fields:
        rows.append(("Comparison", "".join('<div><b class="item-sub">%s</b> %s</div>' % (esc(l), v) for l, v in fields)))
    if verdict and " · " in verdict:
        rows.append(("Verdict", esc(verdict)))
    if x.get("went") and x["went"] not in ("—", "-"):
        rows.append(("Went to", esc(x["went"])))
    if x.get("address"):
        rows.append(("Division", _link(d, i["rel"], x["address"] + " on " + i["stem"], focus=x["address"])))
    rows.append(_judge_row(d, i["stem"], x["id"], "ridea"))
    short = verdict.split(" · ")[0].strip()          # the closed line keeps the title readable
    return _srcd(d, (d["story00"] or {}).get("rel") or "", "Idea " + x["id"], _card("idea-" + x["id"], x["id"], x["title"], sub, where, short, _status_cls(verdict), rows))


def render_ideation(d):
    i = d["ideation"]
    if not i["present"]:
        return _views("ideation", [("pool", "Idea pool",
                                    '<div class="card">%s</div>' % _empty("no Story00-ideation page on this board"))], foot=_sources_html(d, "ideation"))
    head = ('<div class="brief">%s · state %s%s</div>'
            % (_link(d, i["rel"], i["stem"]), esc(i["state"]),
               (" · plan " + esc(i["plan"])) if i["plan"] else ""))
    cards = "".join(_idea_card(d, i, x) for x in i["ideas"])
    pool = ('<div class="card"><h2>Idea pool<span class="tally">%d idea(s)</span></h2>%s'
            '<div class="mut">source: %s · click a card to open it</div>'
            '<div class="idea-cards">%s</div></div>'
            % (len(i["ideas"]), head, esc(i["source"] or "none found"),
               cards or _empty("no Ideas (ranked) table and no Idea divisions in the plan")))
    items = [( '<span class="idtag">%s</span>' % esc(x["id"]), esc(x["target"]), esc(x["desc"]),
               '<span class="%s">%s</span>' % ("ok" if "✅" in x["verified"] else "mut", esc(x["verified"])))
             for x in i["items"]]
    evidence = ('<div class="card"><h2>Evidence items<span class="tally">%d</span></h2>'
                '<div class="brief">The authored contract in outline/&lt;stem&gt;-evidence-items.md: '
                'novelty and prior-art checks are its CITE items.</div>%s</div>'
                % (len(items), _table(["item", "target", "need", "verified"], items)
                   or _empty("no evidence-items.md yet")))
    rec = [(esc(r["what"]), '<span class="path">%s</span>' % esc(r["rel"]),
            '<span class="%s">%s</span>' % ("ok" if r["state"] == "present" else "mut", esc(r["state"])))
           for r in i["receipts"]]
    went = [x for x in i["ideas"] if x.get("went") and x["went"] not in ("—", "")]
    admission = ('<div class="card"><h2>Admission<span class="tally">%s</span></h2>'
                 '<div class="brief">Only the I3 receipt admits an idea to a Story; Page approval, '
                 'CHECK and list order never do.</div>%s%s</div>'
                 % ("G0 open" if not any(r["state"] == "present" for r in i["receipts"][:2]) else "receipt present",
                    _table(["record", "path", "state"], rec),
                    _table(["idea", "went to"], [('<span class="idtag">%s</span>' % esc(x["id"]), esc(x["went"])) for x in went])
                    or _empty("no idea has a went-to Story yet")))
    return _views("ideation", [("pool", "Idea pool", pool), ("evidence", "Evidence items", evidence),
                               ("admission", "Admission", admission)], foot=_sources_html(d, "ideation"))


def _claim_cards(d, s):
    rq_by_id = {c[0]: c for c in s["rq"]}
    cards = []
    for c in s["e"]:
        eid = re.match(r"E-?\d+", c[0]).group(0)
        rq = c[1] if len(c) > 1 else ""
        status = c[2] if len(c) > 2 else ""
        prop = c[3] if len(c) > 3 else ""
        rows = []
        rqrow = rq_by_id.get(rq)
        if rqrow:
            rows.append(("Research question", esc(rqrow[1] if len(rqrow) > 1 else rq)))
            rows += [(h, v) for h, v in _fields(s["rq_h"], rqrow, {0, 1})]
        rows += _fields(s["e_h"], c, {0, 1, 2, 3})
        rows.append(("Story row", _link(d, s["rel"], "%s on %s · C5" % (c[0], s["stem"]), focus="C5")))
        rows.append(_judge_row(d, s["stem"], eid, "rclaim"))
        cards.append(_srcd(d, s["rel"], "C5 · " + eid, _card("claim-" + eid, c[0], prop or "(no proposition cell)", esc(rq or "no RQ"),
                           esc(rq), status or "no status", _status_cls(status), rows)))
    return cards


def _task_cards(d, s):
    cards = []
    for c in s["tt"]:
        tid = c[0]
        home = task_home(d, c)
        rows = _fields(s["tt_h"], c, {0, 1})
        if home["levels"]:
            for one in home["all"]:                       # a row answered by two jobs shows both
                rows.append(("Task home", " · ".join(
                    '<span class="%s">%s %s</span>' % ("ok" if path else "warn", esc(l), "✓" if path else "✗")
                    for l, path in one["levels"]) + (('<div class="path">%s</div>' % esc(one["path"])) if one["path"] else "")))
        else:
            hint = (" · blocks on disk: " + esc(" ".join(x["addr"] for x in d["blocks"]["tree"]))) if d["blocks"]["tree"] else ""
            rows.append(("Task home", '<span class="mut">no address on this row yet · end the design cell with <code>Task: bNN.jNN.</code> '
                         '(or <code>.tNN</code>) when a block answers it%s</span>' % hint))
        rows.append(("Story row", _link(d, s["rel"], "%s on %s · C7" % (tid, s["stem"]), focus="C7")))
        rows.append(_judge_row(d, s["stem"], tid, "rtask"))
        cards.append(_srcd(d, s["rel"], "C7 · " + tid, _card("task-" + tid, tid, c[1] if len(c) > 1 else "(no obligation cell)",
                           "", esc(" · ".join(x["address"] for x in home["all"])), home["state"],
                           _status_cls(home["state"]), rows)))
    return cards


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


def _block_cards(d, scope):
    """One collapsed card per claimed bNN block; open = its claimed jobs, each a
    task table. Unclaimed siblings are named once, muted, never expanded."""
    cards, skipped = [], []
    for blk in d["blocks"]["tree"]:
        if scope and not _claimed(blk["addr"], scope):
            skipped.append(blk["name"])
            continue
        jobs = [j for j in blk["jobs"] if not scope or _claimed(j["addr"], scope)]
        other = [j for j in blk["jobs"] if j not in jobs]
        n_tasks = sum(len(j["tasks"]) for j in jobs)
        n_tk = sum(t["tickets"] for j in jobs for t in j["tasks"])
        state = {}
        for j in jobs:
            for t in j["tasks"]:
                for k, v in t["receipts"].items():
                    state[k] = state.get(k, 0) + v
        rows = []
        for j in jobs:
            js = {}
            for t in j["tasks"]:
                for k, v in t["receipts"].items():
                    js[k] = js.get(k, 0) + v
            head = '<span class="idtag">%s</span> %s <span class="mut">· %d task(s) · %d ticket(s) · %s · %s</span>' % (
                esc(j["addr"]), esc(j["name"]), len(j["tasks"]), sum(t["tickets"] for t in j["tasks"]),
                esc(_fmt_state(js)), esc(j["shape"]))
            trs = []
            for t in j["tasks"]:
                url = _tree_url(d, t["page"] or t["dir"])
                name = ('<a href="%s">%s</a>' % (esc(url), esc(t["name"]))) if url and t["page"] else esc(t["name"])
                dev = esc(t["develops"]) if t["develops"] else '<span class="mut">?</span>'
                if t["develops"] and t["develops_src"] != "page":
                    dev = '<i title="from %s, not typed on the page">%s</i>' % (esc(t["develops_src"]), dev)
                trs.append(('<span class="idtag">%s</span>' % esc(t["addr"]), name, dev,
                            esc("%d tk · %s" % (t["tickets"], _fmt_state(t["receipts"]))) if (t["tickets"] or t["receipts"]) else '<span class="mut">—</span>',
                            esc(t["state"]) if t["state"] else '<span class="mut">%s</span>' % ("no state: line" if t["page"] else "no page")))
            rows.append((j["addr"], head + (_table(["addr", "task", "develops", "runs", "state"], trs) or _empty("no tNN_ task under this job"))))
        if other:
            rows.append(("not claimed", '<span class="mut">%d other job(s) in this block, not this paper\'s: %s</span>'
                         % (len(other), esc(" · ".join(j["name"] for j in other)))))
        where = ('<a href="%s">board</a>' % esc(_tree_url(d, blk["dir"] / "board" / "index.html"))) if blk["board"] else ""
        sub = "%d job(s) · %d task(s) · %d ticket(s)" % (len(jobs), n_tasks, n_tk) + (
            (" · %d job(s) not claimed" % len(other)) if other else "")
        cards.append(_srcd(d, blk["dir"], blk["addr"], _card("block-" + blk["addr"], blk["addr"], blk["name"], esc(sub),
                           where, _fmt_state(state), "ok" if state.get("done") and len(state) == 1 else ("warn" if state else "mut"), rows)))
    return cards, skipped


def _tree_card(d):
    blocks, scope = d["blocks"], paper_scope(d)
    cards, skipped = _block_cards(d, scope)
    shown = [b for b in blocks["tree"] if b["name"] not in skipped]
    n_jobs = sum(1 for b in shown for j in b["jobs"] if not scope or _claimed(j["addr"], scope))
    n_tasks = sum(len(j["tasks"]) for b in shown for j in b["jobs"] if not scope or _claimed(j["addr"], scope))
    if scope:
        tally = "%d of %d block(s) · %d job(s) · %d task(s)" % (len(shown), len(blocks["tree"]), n_jobs, n_tasks)
        src = []
        if blocks["claim"]:
            src.append("board.md <code>blocks:</code> %s" % esc(" ".join(blocks["claim"])))
        rest = [a for a in scope if a not in blocks["claim"]]
        if rest:
            src.append("C7 addresses %s" % esc(" ".join(rest)))
        brief = ("This paper claims " + " + ".join(src) + ". Block → Job → Task → Run is read off the folder on every load; "
                 "a Run's receipt is its results/&lt;run&gt;/runtime.yaml. The tree is read off the folder: fix the tree, not this view. What this paper claims IS typed: board.md <code>blocks:</code> and the addresses on C7 rows.")
    else:
        tally = "%d block(s) · %d job(s) · %d task(s)" % (len(blocks["tree"]), blocks["n_jobs"], blocks["n_tasks"])
        brief = ("No block claimed yet, so the whole Task home is shown. Claim this paper's part with a "
                 "<code>blocks: b03 b04 b02.j01</code> line in board.md, or a bNN.jNN address on a C7 row. "
                 "Block → Job → Task → Run is read off the folder on every load.")
    return _cards_card("Task home · %s" % blocks["label"], tally, brief, cards, "no bNN_ block folder yet",
                       ("also in the Task home, not this paper's: %s" % esc(" · ".join(skipped))) if skipped else "")


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
    """The Discovery jobs/tasks a C6 row names by address, as links; '' when none."""
    out = []
    for a in _addresses(" ".join(cells)):
        hit = _disc_lookup(d, a)
        if hit:
            blk, job, task = hit
            out.append(_disc_link(d, blk, job, task, (task or job or blk)["name"]))
        else:
            out.append('<span class="warn">%s ✗ not in the Discovery home</span>' % esc(a))
    return " · ".join(out)


def _disc_cards(d, scope, feeds):
    """One collapsed card per claimed Discovery job; open = its Task Pages."""
    cards, skipped = [], []
    for blk in d["disc"]["tree"]:
        for j in blk["jobs"]:
            if scope and not _claimed(j["addr"], scope):
                skipped.append(j["name"])
                continue
            st, oc = {}, {}
            for t in j["tasks"]:
                st[t["status"] or "?"] = st.get(t["status"] or "?", 0) + 1
                if t["outcome"]:
                    oc[t["outcome"]] = oc.get(t["outcome"], 0) + 1
            fmt = lambda c: " · ".join("%s %d" % kv for kv in sorted(c.items(), key=lambda kv: -kv[1])) or "—"
            trs = []
            for t in j["tasks"]:
                runs = "%d run(s)" % max(t["tickets"], t["n_results"]) if (t["tickets"] or t["n_results"]) else "—"
                trs.append(('<span class="idtag">%s</span>' % esc(t["addr"]),
                            _disc_link(d, blk, j, t, t["name"]),
                            esc(t["question"]) if t["question"] else '<span class="mut">no question in discovery.yaml</span>',
                            esc(runs), esc(t["status"] or "?"),
                            esc((t["outcome"] + ((" · " + t["confidence"]) if t["confidence"] else "")) if t["outcome"] else "—")))
            rows = [("tasks", _table(["addr", "task page", "question", "runs", "status", "outcome"], trs) or _empty("no tNN_ Discovery Task under this job"))]
            back = feeds.get(j["addr"], [])
            rows.append(("feeds", (" · ".join('<span class="idtag">%s</span>' % esc(x) for x in back)) if back
                         else '<span class="mut">no C6 row names this job yet · write %s in a D-row cell</span>' % esc("%s.%s" % (blk["addr"], j["name"][:3]))))
            rows.append(("index", ('<a href="%s">_index.md</a>' % esc(_tree_url(d, j["index"]))) if j["index"] else '<span class="mut">no _index.md</span>'))
            where = _disc_link(d, blk, None, None, "board") if blk["board_md"] else ""
            cards.append(_srcd(d, j["dir"], j["addr"], _card("disc-" + j["addr"], j["addr"], j["name"],
                               esc("%d task page(s) · %d run(s) · %s" % (len(j["tasks"]), sum(max(t["tickets"], t["n_results"]) for t in j["tasks"]), fmt(st))),
                               where, fmt(oc) if oc else "no outcome yet", "ok" if oc and not st.get("blocked") else ("warn" if st.get("blocked") else "mut"), rows)))
    return cards, skipped


def _disc_card(d):
    disc, scope = d["disc"], discovery_scope(d)
    feeds = {}
    for s in d.get("story", []):
        for cells in s["dd"]:
            for a in _addresses(" ".join(cells)):
                hit = _disc_lookup(d, a)
                if hit and hit[1] is not None:
                    feeds.setdefault(hit[1]["addr"], []).append(cells[0])
    cards, skipped = _disc_cards(d, scope, feeds)
    n_jobs = disc["n_jobs"] - len(skipped)
    tally = ("%d of %d inquiry(ies)" % (n_jobs, disc["n_jobs"])) if scope else "%d inquiry(ies) · %d task page(s)" % (disc["n_jobs"], disc["n_tasks"])
    if scope:
        brief = ("This paper claims %s. One card per Discovery job (an inquiry); open = its Discovery Task Pages, "
                 "each backed by numbered Paper Runs." % esc(" ".join(scope)))
    else:
        brief = ("No inquiry claimed yet, so the whole Discovery home is shown. A C6 row joins an inquiry by writing "
                 "its address (<code>b01.j04</code>) in a cell; board.md may also claim with <code>discoveries: b01</code>.")
    return _cards_card("Discovery home · %s" % disc["label"], tally, brief, cards, "no bNN_ evidence board under discoveries/ yet",
                       ("also in the Discovery home, not this paper's: %s" % esc(" · ".join(skipped))) if skipped else "")


def _section_cards(d, s):
    cards = []
    for r in s["sections"]:
        rows = _fields(s["sec_h"], r["cells"], {0, 1})
        rows.append(("Page", (_link(d, r["rel"], "open " + r["id"]) + (" · " + esc(r["page_state"]) if r["page_state"] else ""))
                     if r["rel"] else '<span class="warn">not minted</span>'))
        rows.append(("Story row", _link(d, s["rel"], "C8 on " + s["stem"], focus="C8")))
        rows.append(_judge_row(d, s["stem"], r["id"], "rnarra"))
        state = (r["page_state"].split("·")[0].strip() if r["page_state"] else ("open" if r["rel"] else "not minted"))
        cards.append(_srcd(d, s["rel"], "C8 · " + r["id"], _card("section-" + r["id"], r["target"] or "§", r["id"], esc(r["question"]),
                           "", state, "ok" if r["rel"] else "warn", rows)))
    return cards


def _hero_cards(d):
    cards = []
    for it in d["hero"]:
        rows = [("Need", esc(it["desc"])), ("Expected", esc(it["expected"] or "—")),
                ("Bullet", esc(it["target"])), ("Why hero", esc(it["why"])),
                ("Evidence Space", _link(d, it["rel"], it["page"] + " · Evidence Space", lens="evidence"))]
        cards.append(_srcd(d, it["rel"], it["id"], _card("hero-" + it["id"], it["type"], it["label"] or it["id"],
                           esc(it["id"] + " · " + it["page"]), "", it["status"], _status_cls(it["status"]), rows)))
    return cards


def _cards_card(title, tally, brief, cards, empty, tail=""):
    return ('<div class="card"><h2>%s<span class="tally">%s</span></h2>%s<div class="item-cards">%s</div>%s</div>'
            % (esc(title), esc(tally), ('<div class="brief">%s</div>' % brief) if brief else "",
               "".join(cards) or _empty(empty),
               ('<div class="brief mut" style="margin-top:8px">%s</div>' % tail) if tail else ""))


def render_story(d):
    if not d["story"]:
        card = ('<div class="card"><h2>Story</h2>%s</div>'
                % _empty("no Story yet · G0 open · the first Story<Letter>-<desk>-<idea-slug> page is minted by the I3 handoff"))
        hero = _cards_card("Evidence Items · hero", "%d" % len(d["hero"]),
                           "Every DISPLAY item on a Main page and every VALUE item on the Abstract page.",
                           _hero_cards(d), "no hero evidence yet · no Main Section page carries a DISPLAY or Abstract VALUE item")
        return _views("story", [("spine", "Spine", card), ("tasks", "Task Roadmap", _tree_card(d) + _disc_card(d)),
                                ("evidence", "Evidence Items", hero)], foot=_sources_html(d, "story"))
    spine, claims, tasks, secs = [], [], [], []
    for s in d["story"]:
        # the Story's `state:` line is not shown here (JL 260919: not needed on the Spine); it stays on the Story page
        spine.append('<div class="card"><h2>%s<span class="tally">%d RQ · %d E · %d T · %d sections</span></h2></div>'
                     % (_link(d, s["rel"], s["stem"]), len(s["rq"]), len(s["e"]), len(s["tt"]), len(s["sections"])))
        for n, title, (face, subs, paras) in s["spine"]:
            rows = [(k, inline(v)) for k, v in face]
            if paras:
                rows.append(("", prose(paras)))
            rows += [(sub, prose(pg)) for sub, pg in subs if pg]
            body = _kv(rows, "spine-row")
            spine.append('<div class="card" data-src="%s" data-ref="C%d · %s"><h2>C%d · %s<span class="tally">%s</span></h2>%s</div>'
                         % (esc(_repo_rel(d, s["rel"])), n, esc(title), n, esc(title), _link(d, s["rel"], "open", focus="C%d" % n),
                            body or _empty("division is empty")))
        if not s["spine"]:
            spine.append('<div class="card">%s</div>' % _empty("no C1 Identity, C2 Pitch or C4 Stakes division under Content"))
        spine.append('<div class="card"><details><summary>compile order</summary><div class="path">%s</div></details></div>'
                     % esc(" → ".join(s["order"]) if s["order"] else "no haipipe:compile-order block"))
        claims.append(_cards_card("%s · Claims & Hypothesis" % s["stem"], "%d claim(s)" % len(s["e"]),
                                  "One card per C5 proposition, joined to its C3 research question. Judge support here; the Story page stays the authority.",
                                  _claim_cards(d, s), "no | En | rows in C5"))
        blocks = d["blocks"]
        if not tasks:
            tasks.append(_tree_card(d))
        tasks.append(_cards_card("%s · Task Roadmap" % s["stem"], "%d obligation(s)" % len(s["tt"]),
                                 "One card per C7 row: what the study must produce. A row joins the Task home above through a "
                                 "bNN[.jNN[.tNN]] address in one of its cells; %s." % (
                                     esc("%d block(s) on disk" % len(blocks["tree"])) if blocks["tree"] else esc(blocks["label"])),
                                 _task_cards(d, s), "no C7 rows"))
        if s["dd"]:
            tasks.append('<div class="card"><h2>%s · Discovery needs<span class="tally">%d</span></h2>'
                         '<div class="brief">One row per C6 D-row. The discovery column is the inquiry the row names by address; '
                         'the inquiry itself stays in the Discovery home below.</div>%s</div>'
                         % (esc(s["stem"]), len(s["dd"]),
                            _table(["D", "what the paper must learn", "feeds", "discovery"],
                                   [('<span class="idtag">%s</span>' % esc(c[0]), esc(c[1] if len(c) > 1 else ""), esc(c[-1] if len(c) > 2 else ""),
                                     _disc_join(d, c) or '<span class="mut">no address yet</span>') for c in s["dd"]])))
        tasks.append(_disc_card(d))
        secs.append(_cards_card("%s · Sections" % s["stem"], "%d row(s)" % len(s["sections"]),
                                "One card per C8 row: what that section must express, before anyone drafts it.",
                                _section_cards(d, s), "no S- rows in C8"))
    hero = _cards_card("Evidence Items · hero", "%d" % len(d["hero"]),
                       "Every DISPLAY item on a Main page and every VALUE item on the Abstract page; each Section keeps its full Evidence Space in Outline.",
                       _hero_cards(d), "no hero evidence yet · no Main Section page carries a DISPLAY or Abstract VALUE item")
    return _views("story", [("spine", "Spine", "".join(spine)), ("claims", "Claims & Hypothesis", "".join(claims)),
                            ("tasks", "Task Roadmap", "".join(tasks)), ("sections", "Sections", "".join(secs)),
                            ("evidence", "Evidence Items", hero)], foot=_sources_html(d, "story"))


def _md_tables(md):
    """Every `| … |` table in a Markdown file, keyed by the `## ` heading above it."""
    out, section, headers, rows = {}, "", None, []
    def flush():
        if headers:
            out[section] = (headers, rows)
    for line in (md or "").splitlines():
        t = line.strip()
        if t.startswith("## "):
            flush(); section, headers, rows = t[3:].strip(), None, []
            continue
        if not t.startswith("|"):
            if headers:
                flush(); headers, rows = None, []
            continue
        cells = [clean(c) for c in t.strip("|").split("|")]
        if all(re.fullmatch(r"-+", c or "-") for c in cells):
            continue
        if headers is None:
            headers = cells
        else:
            rows.append(cells)
    flush()
    return out


def _slot_actual(d, slot):
    """What a Folder tree slot resolves to on THIS board: [(name, present, note)]."""
    st = d["setup"]
    def rows_where(pred):
        return [(r["name"], r["state"].startswith("present"), r["role"]) for r in st if pred(r["name"])]
    if slot == "board":
        return [("board.md", True, "dialect: paper" if d["dialect"] == "paper" else "no dialect")]
    if slot == "story00":
        return rows_where(lambda n: n.startswith("A1-Story/Story00"))
    if slot == "story":
        return rows_where(lambda n: re.match(r"^A1-Story/Story[A-Z]", n))
    if slot in ("main", "appendix", "round"):
        kind = {"main": "Main", "appendix": "Appendix", "round": "Round"}[slot]
        return rows_where(lambda n: re.match(r"^B[abc]-.+-%s/$" % kind, n))
    if slot == "delivery":
        dv = d["delivery"]
        if dv["dir"] is None:
            return [("delivery/", False, "not generated yet · G4 open")]
        return [("delivery/", True, ("built " + dv["built"]) if dv["built"] else "no build-manifest.json")]
    if slot == "tasks":
        b = d["blocks"]
        return [(b["label"], b["dir"] is not None, "%d block(s) · %d job(s) · %d task(s)" % (len(b["tree"]), b["n_jobs"], b["n_tasks"]) if b["dir"] else "")]
    if slot == "discoveries":
        c = d["disc"]
        return [(c["label"], c["dir"] is not None, "%d board(s) · %d inquiry(ies) · %d task page(s)" % (len(c["tree"]), c["n_jobs"], c["n_tasks"]) if c["dir"] else "")]
    return []


def folder_map(d):
    """The `Folder tree × Spec or control` table of space-mapping.md, each slot resolved
    against this board, plus Spec / control → resolved folders for the map's column."""
    tables = _md_tables(d["workflow_map"])
    key = next((k for k in tables if k.lower().startswith("folder tree")), None)
    rows = []
    by_rt = {}
    if key:
        headers, body = tables[key]
        for cells in body:
            if len(cells) < 4:
                continue
            slot, folder, holds, rts = cells[0].strip("`"), cells[1], cells[2], cells[3]
            actual = _slot_actual(d, slot)
            rt_ids = [x.strip().strip("`") for x in rts.split("·")]
            rows.append({"slot": slot, "folder": folder, "holds": holds, "runtypes": rt_ids, "actual": actual})
            for rt in rt_ids:
                by_rt.setdefault(rt, []).extend(n for n, ok, _ in actual if ok)
    return {"rows": rows, "by_runtype": by_rt, "map": tables.get(next((k for k in tables if not k.lower().startswith("folder tree")), ""), ([], []))}


_TREE_SKIP = {"board", "_archive", "__pycache__", "node_modules", ".git"}   # rendered site, backups, caches: not the paper


def _slot_of(rel, is_dir):
    """Which Folder tree slot a REAL path of the paper belongs to, by its shape."""
    top = rel.split("/")[0]
    if rel == "board.md":
        return "board"
    if top == "A1-Story":
        second = rel.split("/")[1] if "/" in rel else ""
        if second.startswith("Story00"):
            return "story00"
        if re.match(r"^Story[A-Z]", second):
            return "story"
        return ""
    if re.match(r"^Ba-.+-Main$", top):
        return "main"
    if re.match(r"^Bb-.+-Appendix$", top):
        return "appendix"
    if re.match(r"^Bc-.+-Round$", top):
        return "round"
    if top == "delivery":
        return "delivery"
    return ""


def _dir_note(path):
    """One line of counts for a page or run folder: what its subfolders hold."""
    parts = []
    for sub in ("outline", "runs", "results", "delivery", "feedback", "sent", "released", "latex", "word", "word-feedback", "sections", "appendices", "displays"):
        q = path / sub
        if q.is_dir():
            n = sum(1 for x in q.iterdir() if not x.name.startswith("."))
            parts.append("%s/ %d" % (sub, n))
    pages = [x.name for x in path.glob("*.md") if x.stem == path.name]
    if pages:
        parts.insert(0, pages[0])
    return " · ".join(parts)


_LIST_LIMIT = 40          # a folder with more files than this shows a count, not the files


def _node(name, path, is_dir, slot="", note="", children=None, opened=False, more=0):
    return {"name": name, "path": path, "dir": is_dir, "slot": slot, "note": note,
            "children": children or [], "open": opened, "more": more}


_WALK_DEPTH = 3           # how far a folder opens below a page folder, delivery/, or a project-home entry
_PAGE_ORDER = ("outline", "runs", "results", "delivery", "feedback", "sent", "released", "workflow", "handoff", "projection")


def _walk(path, slot, depth):
    """Every child of a folder, dirs first then files. A dir recurses while depth
    > 0 (below that it is a closed count); files list up to _LIST_LIMIT and the
    rest become a count. The whole tree is on the page; nothing is fetched."""
    kids, hidden, nfiles = [], 0, 0
    if not path.is_dir():                      # a flat-shape Task known only from scripts/ or results/
        return kids, hidden
    entries = sorted((x for x in path.iterdir() if not x.name.startswith(".") and x.name not in _TREE_SKIP),
                     key=lambda q: (q.is_file(), q.name.lower()))
    for x in entries:
        if x.is_dir():
            n = sum(1 for y in x.iterdir() if not y.name.startswith(".") and y.name not in _TREE_SKIP)
            sub, more = _walk(x, slot, depth - 1) if depth > 0 else ([], 0)
            kids.append(_node(x.name + "/", x, True, slot, "%d item(s)" % n, sub, False, more))
        elif nfiles < _LIST_LIMIT:
            kids.append(_node(x.name, x, False, slot, _size(x)))
            nfiles += 1
        else:
            hidden += 1
    return kids, hidden


def build_tree(d):
    """The paper as a real, complete folder tree: root files, page groups → page
    folders → everything inside them (to _WALK_DEPTH below a page folder);
    board/ and _archive/ are skipped. Returns (roots, homes): the paper folder,
    and the claimed Task-home blocks + Discovery inquiries, which live outside
    it and get their own box. Every node carries the space-mapping slot it matches."""
    b = d["board"]
    def page_folder(path, slot):
        kids, more = _walk(path, slot, _WALK_DEPTH)
        page = path.name + ".md"
        def key(k):
            if not k["dir"]:
                return (0 if k["name"] == page else 2, 0, k["name"].lower())
            sub = k["name"][:-1]
            return (1, _PAGE_ORDER.index(sub) if sub in _PAGE_ORDER else 99, k["name"].lower())
        kids.sort(key=key)
        note = _dir_note(path)
        if note.startswith(page):                      # the folder is named after its page: say it once
            note = note[len(page):].lstrip(" ·")
        return _node(path.name + "/", path, True, slot, note, kids, False, more)
    roots = []
    groups = {g["folder"]: g for g in d["groups"]}
    for x in sorted(b.iterdir(), key=lambda q: (q.is_dir(), q.name != "board.md", q.name.lower())):
        if x.name.startswith(".") or x.name in _TREE_SKIP:
            continue
        rel = x.name
        if x.is_file():
            if x.suffix in (".md", ".toml", ".json", ".py"):
                roots.append(_node(x.name, x, False, _slot_of(rel, False), _size(x)))
            continue
        slot = _slot_of(rel, True)
        if x.name in groups:
            kids = [page_folder(y, _slot_of(rel + "/" + y.name, True) or slot)
                    for y in sorted(q for q in x.iterdir() if q.is_dir() and not q.name.startswith(".") and q.name not in _TREE_SKIP)]
            roots.append(_node(x.name + "/", x, True, slot, "%d page(s)" % len(groups[x.name]["stems"]), kids, True))
        else:
            kids, more = _walk(x, slot, _WALK_DEPTH)
            note = _dir_note(x) if slot == "delivery" else "%d item(s) · not in the map" % (len(kids) + more)
            roots.append(_node(x.name + "/", x, True, slot, note, kids, slot == "delivery", more))
    scope = paper_scope(d)
    homes = []          # the project homes live outside the paper folder: their own box
    if d["blocks"]["dir"] is not None:
        kids = []
        for blk in d["blocks"]["tree"]:
            if scope and not _claimed(blk["addr"], scope):
                continue
            jobs = []
            for j in blk["jobs"]:
                if scope and not _claimed(j["addr"], scope):
                    continue
                tasks = []
                for t in j["tasks"]:
                    sub, more = _walk(t["dir"], "tasks", 2)
                    tasks.append(_node(t["name"] + "/", t["dir"], True, "tasks", "%d ticket(s) · %s" % (t["tickets"], _fmt_state(t["receipts"])), sub, False, more))
                jobs.append(_node(j["name"] + "/", j["dir"], True, "tasks", "%d task(s)" % len(j["tasks"]), tasks, False))
            kids.append(_node(blk["name"] + "/", blk["dir"], True, "tasks", "%d job(s)" % len(blk["jobs"]), jobs, True))
        homes.append(_node(d["blocks"]["label"], d["blocks"]["dir"], True, "tasks", "the Task home · %d block(s) · claimed ones shown" % len(d["blocks"]["tree"]), kids, True))
    if d["disc"]["dir"] is not None:
        kids = []
        for blk in d["disc"]["tree"]:
            jobs = []
            for j in blk["jobs"]:
                tasks = []
                for t in j["tasks"]:
                    sub, more = _walk(t["dir"], "discoveries", 2)
                    tasks.append(_node(t["name"] + "/", t["dir"], True, "discoveries", "%s%s" % (t["status"] or "?", (" · " + t["outcome"]) if t["outcome"] else ""), sub, False, more))
                jobs.append(_node(j["name"] + "/", j["dir"], True, "discoveries", "%d task page(s)" % len(j["tasks"]), tasks, False))
            kids.append(_node(blk["name"] + "/", blk["dir"], True, "discoveries", "%d inquiry(ies)" % len(blk["jobs"]), jobs, True))
        homes.append(_node(d["disc"]["label"], d["disc"]["dir"], True, "discoveries", "the Discovery home · %d board(s)" % len(d["disc"]["tree"]), kids, True))
    return roots, homes


def _tree_html(d, nodes, by_slot, parent_slot=""):
    """Nested <ul class="tree">: a directory is a <details>, a file a plain row.
    Every row is two columns: the bare tree on the left (marker, icon, name),
    the works on the right (`.tn-works`: the folder's counts on every node; the
    slot's Spec / control chips once, on the first node of that slot). Nothing else
    (JL: less is more). A nested <ul> only pads the left, so the right column
    lines up at every depth."""
    out = []
    for n in nodes:
        row = by_slot.get(n["slot"])
        first = bool(row) and n["slot"] != parent_slot
        url = _tree_url(d, n["path"]) if not n["dir"] and n["path"] else ""
        name = ('<a href="%s">%s</a>' % (esc(url), esc(n["name"]))) if url else esc(n["name"])
        top = '<span class="tn-note">%s</span>' % esc(n["note"]) if n["note"] else ""
        if first:
            top = "".join('<span class="idtag rt">%s</span>' % esc(x) for x in row["runtypes"]) + top
        line = ('<span class="tn-name" title="%s">%s %s</span><span class="tn-works"><span class="tn-top">%s</span></span>'
                % (esc(n["name"]), "📁" if n["dir"] else "📄", name, top))
        if n["dir"]:
            kids = _tree_html(d, n["children"], by_slot, n["slot"])
            if n["more"]:
                kids += '<li class="tn-more">… %d more file(s) not listed</li>' % n["more"]
            body = ('<ul>%s</ul>' % kids) if kids else ""
            out.append('<li><details class="tn"%s><summary>%s</summary>%s</details></li>'
                       % (" open" if n["open"] else "", line, body))
        else:
            out.append('<li><div class="tn-file">%s</div></li>' % line)
    return "".join(out)


def _md_table_html(md):
    rows, headers = [], None
    for line in (md or "").splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [clean(c) for c in s.strip("|").split("|")]
        if all(re.fullmatch(r"-+", c or "-") for c in cells):
            continue
        if headers is None:
            headers = cells
        else:
            rows.append([esc(c) for c in cells])
    return _table(headers or [], rows) if headers else _empty("space-mapping.md has no table")


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


def render_delivery(d):
    """Delivery Space: what leaves the paper. Manuscript · Sections · Displays ·
    Checks · Rounds & Venue, every cell read from delivery/ and the pages."""
    dv, b = d["delivery"], d["board"]
    man = dv["manifest"] or {}
    toml = dv["toml"]
    title = toml.get("paper.title") or d["title"]
    venue = toml.get("profile.venue_label") or toml.get("paper.venue_profile") or paper_desk(d) or ""
    close = d["close"]
    if dv["dir"] is None:
        empty = ('<div class="card"><h2>Manuscript</h2>%s</div>'
                 % _empty("no delivery/ yet · G4 open · haipipe-paper-assemble generates delivery/ whole "
                          "(paper-build.toml + build.py → latex/master.tex, the PDF and the DOCX) once the Story's C8 "
                          "compile-order block exists and Section pages carry delivery/latex/<page>.tex fragments"))
        finish = ('<div class="card"><h2>Finish rule</h2><div class="brief">%s</div></div>' % esc(close)) if close else ""
        return _views("delivery", [("manuscript", "Manuscript", empty + finish),
                                   ("rounds", "Rounds & Venue", _rounds_html(d))], foot=_sources_html(d, "delivery"))
    build = man.get("build") or {}
    sub = man.get("submission_readiness") or {}
    rd = man.get("readiness") or {}
    # ---- Manuscript
    head = ('<div class="card"><h2>%s<span class="tally">%s</span></h2><div class="brief">%s</div>%s</div>' % (
        esc(title), esc("%s · built %s" % (man.get("status") or "no build", dv["built"] or "never")) if man else "no build yet",
        esc(" · ".join(x for x in (("venue " + venue) if venue else "", ("desk " + toml["paper.desk"]) if toml.get("paper.desk") else "",
                                   man.get("engine") or "", "order from " + dv["order_src"] if dv["order_src"] else "") if x)),
        ('<div class="brief">finish rule: %s</div>' % esc(close)) if close else ""))
    rows = []
    for o in dv["outputs"]:
        st = ("✅ built" + (" · stale" if o["stale"] else "")) if o["exists"] else "⬜ not built"
        rows.append((esc(o["what"]), _file_link(d, o["path"], o["rel"]) if o["exists"] else esc(o["rel"]),
                     '<span class="%s">%s</span>' % (_status_cls(st), esc(st)), esc(o["size"]), esc(o["stamp"])))
    for r in dv["returned"]:
        rows.append(("returned", _file_link(d, r["path"], r["rel"]), '<span class="mut">a coauthor or desk copy, never an input</span>', esc(r["size"]), esc(r["stamp"])))
    outputs = ('<div class="card"><h2>Deliverables<span class="tally">%d</span></h2><div class="brief">The files that leave: '
               'named in delivery/paper-build.toml [outputs]; a returned file under delivery/word-feedback/ is read, never built from.</div>%s</div>'
               % (len(rows), _table(["what", "file", "state", "size", "written"], rows) or _empty("paper-build.toml names no outputs and latex/ word/ hold none")))
    facts = []
    if build:
        facts += [("main text", "%s words%s" % (build.get("main_text_words", "?"), (" · limit %s" % build["main_text_word_limit"]) if build.get("main_text_word_limit") else " · no declared limit")),
                  ("citations", "%s cited · %s bib entries" % (build.get("citations", "?"), man.get("bib_entries", "?"))),
                  ("displays", "%s main table(s) · %s main figure(s)" % (build.get("main_tables", "?"), build.get("main_figures", "?"))),
                  ("pages", "%s of %s ready%s" % (rd.get("ready", "?"), rd.get("total", "?"), (" · not ready: " + ", ".join(_not_ready_ids(rd))) if rd.get("not_ready") else "")),
                  ("submission", "%s%s" % (sub.get("status", "?"), (" · " + "; ".join(sub.get("blockers") or [])) if sub.get("blockers") else ""))]
    if dv["stale"]:
        facts.append(("sources moved", "%d page(s) edited after the build: %s" % (len(dv["stale"]), ", ".join(dv["stale"]))))
    facts_html = _kv([(k, esc(v)) for k, v in facts], "spine-row")
    cmd = ('<div class="card"><h2>Build</h2><div class="brief">Regenerates delivery/ whole from the Section pages; nobody edits delivery/latex/ by hand.</div>'
           '<pre class="path">cd %s\n.venv/bin/python %s/delivery/build.py</pre></div>'
           % (esc(str(d["root"])), esc(str(b.relative_to(d["root"])) if str(b).startswith(str(d["root"])) else str(b))))
    manuscript = head + outputs + (('<div class="card"><h2>Build facts</h2>%s</div>' % facts_html) if facts else "") + cmd
    # ---- Sections
    trs = []
    for i, p in enumerate(dv["pages"], 1):
        lanes = ('<span style="white-space:nowrap">%s</span>' % " ".join(
            '<span class="%s" title="%s"%s>%s</span>' % ("ok" if ok else "mut", esc(name), "" if ok else ' style="opacity:.25"', icon)
            for icon, name, ok, _ in p["lanes"])) if p["lanes"] else '<span class="mut">—</span>'
        notes = list(p["reasons"]) + list(p["warnings"])
        if p["frag_stale"] and not any("stale" in w for w in p["warnings"]):
            notes.append("fragment older than the page .md")
        if p["stale"]:
            notes.append("page edited after the build")
        ready = _yn(p["ready"]) if p["ready"] is not None else '<span class="mut">no build</span>'
        trs.append((esc("%d" % i), '<span class="idtag">%s</span>' % esc(p["part"]),
                    ('<span style="white-space:nowrap">%s</span>' % _link(d, p["rel"], p["id"])) if p["rel"] else '<span class="warn">%s ✗ not minted</span>' % esc(p["id"]),
                    esc(p["state"]) if p["state"] else '<span class="mut">no state: line</span>',
                    esc((p["outline"] + ((" " + p["approval"]) if p["approval"] else "")).strip()) or '<span class="mut">—</span>',
                    _yn(p["frag"]), lanes, ready,
                    esc("; ".join(notes)) if notes else ""))
    sections = ('<div class="card"><h2>Compile order<span class="tally">%d page(s)</span></h2><div class="brief">%s. '
                'fragment = the page\'s delivery/latex/&lt;page&gt;.tex that master.tex \\inputs; lanes = the page\'s own 📜 LaTeX · 📝 Word · 🌐 Web builds; '
                'ready = the last build\'s verdict for that page.</div>%s</div>'
                % (len(trs), esc(dv["order_src"] or "no compile order"),
                   _table(["#", "part", "page", "state", "outline", "fragment", "lanes", "ready", "notes"], trs) or _empty("no compile order yet · the Story's C8 block is empty")))
    # ---- Displays
    drs = [(esc(r[0]), esc(r[1]), '<code>%s</code>' % esc(r[2]), esc(r[3]), esc(r[4])) for r in dv["displays"]]
    assets = _kv([("asset", "%s · %s" % (_file_link(d, a["path"], a["name"]), esc(a["size"]))) for a in dv["assets"]])
    displays = ('<div class="card"><h2>Display register<span class="tally">%d</span></h2><div class="brief">%s Printed vs declared numbering, read from delivery/display-register.md.</div>%s%s</div>'
                % (len(drs), esc(dv["display_note"]), _table(["printed", "declared", "label", "unit", "page"], drs) or _empty("no display-register.md · build once"), assets))
    # ---- Checks
    checks = build.get("checks") or {}
    crs = [(esc(k.replace("_", " ")), _yn(v) if isinstance(v, bool) else '<span class="mut">%s</span>' % esc(str(v))) for k, v in checks.items()]
    render = man.get("render") or {}
    if render:
        crs.append(("latexmk", _yn(render.get("latexmk_rc") == 0) + " rc %s" % esc(str(render.get("latexmk_rc")))))
        crs.append(("docx", _yn(render.get("docx_rc") == 0) + " rc %s" % esc(str(render.get("docx_rc")))))
    ev = man.get("evidence") or {}
    if ev:
        crs.append(("evidence", esc("mode %s · %s pending marker(s) · %s unaccepted item(s)" % (ev.get("mode", "?"), len(ev.get("pending_markers") or []), len(ev.get("unaccepted_items") or [])))))
    warns = list(man.get("warnings") or []) + ["unresolved \\ref: " + x for x in (man.get("unresolved_refs") or [])]
    checks_html = ('<div class="card"><h2>Checks<span class="tally">%s</span></h2><div class="brief">What the last build verified; the human decision (g6) is never a file.</div>%s</div>'
                   % (esc(sub.get("status", "no build")), _table(["check", "result"], crs) or _empty("no build-manifest.json yet")))
    checks_html += ('<div class="card"><h2>Build warnings<span class="tally">%d</span></h2>%s</div>'
                    % (len(warns), ("<ul class=\"item-bullets\">%s</ul>" % "".join("<li>%s</li>" % esc(w) for w in warns)) if warns else _empty("the last build raised none")))
    return _views("delivery", [("manuscript", "Manuscript", manuscript), ("sections", "Sections", sections),
                               ("displays", "Displays", displays), ("checks", "Checks", checks_html),
                               ("rounds", "Rounds & Venue", _rounds_html(d))], foot=_sources_html(d, "delivery"))


def _rounds_html(d):
    dv = d["delivery"]
    cards = []
    for r in dv["rounds"]:
        rows = [("kind", esc(r["kind"]) if r["kind"] else '<span class="mut">—</span>'),
                ("received", esc(" · ".join(x for x in (r["from"], r["at"]) if x)) or '<span class="mut">—</span>'),
                ("response due", esc(r["due"]) if r["due"] else '<span class="mut">—</span>'),
                ("base build", esc(r["base"]) if r["base"] else '<span class="mut">—</span>'),
                ("folders", esc(" · ".join(r["subs"])) if r["subs"] else '<span class="mut">none</span>'),
                ("page", _link(d, r["rel"], r["stem"]))]
        cards.append(_srcd(d, r["rel"], r["stem"], _card("round-" + r["stem"], r["stem"][:4], r["stem"], esc(r["kind"]), "", r["state"] or "no state: line", _status_cls(r["state"]), rows)))
    rounds = _cards_card("Rounds", "%d" % len(cards),
                         "One card per Bc-&lt;desk&gt;-Round page: a feedback and response cycle, coauthor or desk. The Round page owns the dispositions.",
                         cards, "no Round yet · G5 open · a round is minted under Bc-<desk>-Round/ when feedback arrives")
    vp = dv["links"].get("venue-page", "")
    venue = ('<div class="card"><h2>Venue</h2><div class="brief">The desk this paper is told to, from the board\'s Links.</div>%s</div>'
             % (_kv([("venue page", _file_link(d, (d["board"] / vp).resolve(), vp))], "spine-row") if vp else _empty("no venue-page Links row on board.md")))
    return rounds + venue


def _run_status_html(r):
    if r["status"]:
        t = r["status"] + ((" · " + r["step"]) if r["step"] else "")
        return '<span class="%s">%s</span>' % (_status_cls(t) if _status_cls(t) != "mut" else "", esc(t))
    return '<span class="%s">%s</span>' % ("mut" if r["has_result"] else "warn", "Result, no runtime.yaml" if r["has_result"] else "no Result yet")


def _page_run_cards(d):
    by = {}
    for r in d["runs"]:
        if r["family"] == "page":
            by.setdefault(r["page"], []).append(r)
    cards = []
    for p in d["pages"]:
        rs = by.get(p["stem"])
        if not rs:
            continue
        kinds = {}
        for r in rs:
            k = r["kind"].split(" · ")[-1]
            kinds[k] = kinds.get(k, 0) + 1
        done = sum(1 for r in rs if r["has_result"])
        trs = [('<span class="idtag">%s</span>' % esc(r["run"]), esc(r["kind"]), _run_status_html(r),
                _link(d, r["rel"], "open", lens="run", run=r["run"])) for r in rs]
        st = "%d of %d with a Result" % (done, len(rs))
        cards.append(_srcd(d, p["rel"], "runs/", _card("pruns-" + p["stem"], "%d" % len(rs), p["stem"],
                           esc(" · ".join("%d %s" % (n, k) for k, n in kinds.items())), "",
                           st, "ok" if done == len(rs) else "warn",
                           [("runs", _table(["run", "kind", "status", "open"], trs))])))
    return cards


def _evidence_run_cards(d):
    cards = []
    for pg in d["evidence_runs"]:
        rows, n_alloc, n_res = [], 0, 0
        live = [x for x in pg["rows"] if not x["item"]["retired"]]
        for x in pg["rows"]:
            it, tk = x["item"], x["ticket"]
            if tk and not it["retired"]:
                n_alloc += 1
                n_res += 1 if tk["has_result"] else 0
            if tk:
                run = '<span class="idtag">%s</span>' % esc(tk["run"])
                res = _run_status_html(tk)
            elif x["want"]:
                run = '<span class="warn">%s ✗ no ticket in runs/</span>' % esc(x["want"])
                res = '<span class="mut">—</span>'
            else:
                run = '<span class="mut">not allocated%s</span>' % ((" · " + esc(it["local"]["mode"])) if it["local"]["mode"] else "")
                res = '<span class="mut">—</span>'
            sup = " ".join('<span class="idtag" title="%s">%s</span>' % (esc(sp["owner"] + " · " + sp["mode"]), esc(sp["addr"] or "?"))
                           for sp in it["supporting"]) or '<span class="mut">none</span>'
            label = esc(it["label"] or it["id"]) + (' <span class="mut">· retired</span>' if it["retired"] else "")
            rows.append(('<span class="idtag">%s</span>' % esc(it["id"].split("-")[0]), label,
                         '<span class="idtag">%s</span>' % esc(it["type"]), run, esc(it["local"]["mode"]), res, sup))
        for tk in pg["orphans"]:
            rows.append(('<span class="mut">—</span>', '<span class="mut">no Evidence Item names this Run</span>', "",
                         '<span class="idtag">%s</span>' % esc(tk["run"]), "", _run_status_html(tk), ""))
        n_ret = len(pg["rows"]) - len(live)
        st = "%d of %d item(s) have a Local Run" % (n_alloc, len(live)) if live else "%d run(s), no live items" % len(pg["orphans"])
        cards.append(_srcd(d, pg["rel"], "outline/ evidence items", _card("eruns-" + pg["page"], "%d" % len(live), pg["page"],
                           esc("%d Local Run(s) · %d with a Result%s%s" % (n_alloc, n_res, (" · %d retired item(s)" % n_ret) if n_ret else "",
                                                                          (" · %d unnamed run(s)" % len(pg["orphans"])) if pg["orphans"] else "")),
                           _link(d, pg["rel"], "Evidence Space", lens="evidence"), st,
                           "ok" if live and n_alloc == len(live) else "warn",
                           [("items", _table(["E", "label", "type", "local run", "mode", "result", "supporting runs"], rows))])))
    return cards


def _supporting_cards(d, owner):
    """Block cards for one owner; open = the Job › Task › Run tree with who uses each Run."""
    home = d["blocks"] if owner == "Execution" else d["disc"]
    cards = []
    for bb, node in sorted(d["supporting"][owner].items()):
        blk = node["blk"]
        n_runs = sum(len(t["runs"]) for j in node["jobs"].values() for t in j["tasks"].values())
        n_ok = sum(1 for j in node["jobs"].values() for t in j["tasks"].values() for r in t["runs"] if r["on_disk"])
        pages = {u["page"] for j in node["jobs"].values() for t in j["tasks"].values() for r in t["runs"] for u in r["users"]}
        tree = []
        for jj, jnode in sorted(node["jobs"].items()):
            job = jnode["job"]
            tree.append('<div class="tree-job"><span class="idtag">%s</span> %s</div>' % (
                esc(bb + jj), esc(job["name"]) if job else '<span class="warn">✗ no such job in %s</span>' % esc(home["label"])))
            for tt, tnode in sorted(jnode["tasks"].items()):
                task = tnode["task"]
                if tt:
                    url = _tree_url(d, task["page"]) if task and task["page"] else ""
                    name = ('<a href="%s">%s</a>' % (esc(url), esc(task["name"]))) if url else (esc(task["name"]) if task else '<span class="warn">✗ no such task</span>')
                    tree.append('<div class="tree-task"><span class="idtag">%s</span> %s</div>' % (esc(bb + jj + tt), name))
                trs = []
                for r in tnode["runs"]:
                    if r["tickets"]:
                        tk = "<br>".join(_file_link(d, path, stem) for stem, path in r["tickets"])
                    elif r["r"]:
                        tk = '<span class="warn">✗ no %s ticket on disk</span>' % esc(r["r"])
                    else:
                        tk = '<span class="mut">whole %s cited, no Run yet</span>' % ("task" if tt else "job")
                    by_page = {}
                    for u in r["users"]:
                        by_page.setdefault((u["page"], u["rel"]), []).append(u)
                    users = "<br>".join('%s %s <span class="mut">%s</span>' % (
                        _link(d, rel, pg, lens="evidence"),
                        " ".join('<span class="idtag" title="%s">%s</span>' % (esc(u["label"] or u["item"]), esc(u["item"].split("-")[0])) for u in us),
                        esc(" · ".join(sorted({u["mode"] for u in us if u["mode"]}))))
                        for (pg, rel), us in by_page.items())
                    st = r["status"] or ("" if r["tickets"] else "")
                    trs.append(('<span class="idtag">%s</span>' % esc(r["addr"]), tk,
                                ('<span class="%s">%s</span>' % (_status_cls(_norm_status(st)), esc(st))) if st else '<span class="mut">no receipt</span>',
                                users))
                tree.append('<div class="tree-runs">%s</div>' % _table(["run", "ticket", "receipt", "used by"], trs))
        st = "%d of %d on disk" % (n_ok, n_runs)
        cards.append(_srcd(d, (blk or {}).get("dir") or home["dir"], bb, _card("sup-%s-%s" % (owner[:4].lower(), bb), bb, blk["name"] if blk else bb + " ✗ not in the home",
                           esc("%d job(s) · %d run(s) cited · used by %d page(s)" % (len(node["jobs"]), n_runs, len(pages))),
                           "", st, "ok" if n_ok == n_runs else "warn", [("tree", "".join(tree))])))
    return cards


def _norm_status(st):
    t = (st or "").lower()
    return "✅ " + st if t in ("complete", "completed", "done") else ("⚠ " + st if t in ("running", "planned", "blocked") else st)


def _run_request_entry(d, cells, target, owner, worker, matching, receipt, next_action):
    """One target-bound clipboard request in the Paper Run map. This is UI-only:
    it creates no Run and its script below can only write to the clipboard."""
    spec = target.get("spec") or (cells[0].strip("`") if cells else "")
    run_type = cells[1] if len(cells) > 1 else ""
    prerequisites = cells[4] if len(cells) > 4 else ""
    space = cells[5] if len(cells) > 5 else "Run"
    matching_text = "\n".join(
        "- %s · status: %s%s · %s" % (
            r["run"], r.get("status") or "no runtime status",
            (" · step: " + r["step"]) if r.get("step") else "",
            r.get("result") or "ticket only")
        for r in matching) or "None found for this exact target in the current Paper Run projection."
    target_text = target.get("label") or target.get("id") or ""
    page = target.get("page") or {}
    page_path = str(page.get("rel") or "")
    page_name = str(page.get("stem") or "")
    related_page = target.get("related_page") or {}
    related_path = str(related_page.get("rel") or "")
    related_name = str(related_page.get("stem") or "")
    target_id = target.get("id") or ""
    wanted_gates = set(target.get("gate_ids", []))
    gate_lines = []
    for gate, name, status in d["gates"]:
        if gate not in wanted_gates:
            continue
        suffix = " · aggregate only; verify this exact C8 row's human release" if gate == "G3" else ""
        gate_lines.append("- %s · %s: %s%s" % (gate, name, status, suffix))
    gate_text = "\n".join(gate_lines) or "No Paper gate is declared for this Spec."
    prompt = (
        "Handle this Paper Run request through its named owner workflow.\n\n"
        "Board: %s\nBoard source: %s\nSpace: %s\n"
        "Folder/Page: %s · %s (%s)%s\nTarget: %s%s\n"
        "Spec: %s\nRun Type: %s\nOwner Skill: %s\nWorker Skill(s): %s\n"
        "Actor and prerequisites: %s\n"
        "Visible gate state:\n%s\n"
        "Matching Run(s) and current status:\n%s\n"
        "Expected receipt: %s\n"
        "Next owner-permitted action: %s\n\n"
        "Read the bound source and verify every prerequisite before acting. Reuse or resume an exact matching Run when the owner workflow permits; do not duplicate it. If a required gate or input is missing, report HOLD and name the missing receipt."
        % (d["board"].name, _repo_rel(d, "board.md"), space,
           str(Path(page_path).parent) if page_path else "(Page folder unresolved)", page_name, page_path,
           ("\nRelated Page: %s (%s)" % (related_name, related_path)) if related_path else "",
           target_id, (" · " + target_text) if target_text and target_text != target_id else "",
           spec, run_type, owner, worker or "none separate from the owner",
           prerequisites, gate_text, matching_text, receipt, next_action))
    title = (target_id + (" · " + target_text if target_text and target_text != target_id else ""))
    summary = '<summary>⧉ Copy Run request · <code>%s</code></summary>' % esc(title)
    prompt_attr = esc(prompt).replace("\n", "&#10;")
    detail = ('<div class="run-request-detail"><div class="brief">Owner: %s · Worker: %s<br>'
              'Prerequisites: %s<br>Matching Run: %s</div>'
              '<button type="button" class="run-request-copy" data-run-prompt="%s" '
              'title="Copy this target-bound request only; it does not send or run anything">⧉ Copy Run request</button></div>'
              % (esc(owner), esc(worker or "none separate from the owner"), esc(prerequisites),
                 esc(", ".join(r["run"] + " · " + (r.get("status") or "no runtime status") for r in matching)
                             or "none found for this exact target"), prompt_attr))
    return '<details class="run-request">%s%s</details>' % (summary, detail)


def _typed_judgment_runs(d, page, target, prefix):
    """All exact typed Paper judgment Tickets for one Page and row, joined to
    their current native Result/runtime receipt without crossing Run families."""
    if not page.get("rel"):
        return []
    folder = (d["board"] / page["rel"]).parent
    runs = folder / "runs"
    out = []
    if not runs.is_dir():
        return out
    for ticket in sorted(runs.iterdir()):
        if ticket.is_dir() or not ticket.name.startswith(prefix):
            continue
        rid = ticket.name.split(".")[0]
        if _frontmatter(read(ticket)).get("target", "").strip() != target:
            continue
        result = folder / "results" / rid
        runtime = read(result / "runtime.yaml") if result.is_dir() else ""
        out.append({"run": rid, "page": page["stem"], "status": scalar(runtime, "status", "no runtime"),
                    "step": scalar(runtime, "step", ""),
                    "result": "Result present" if result.is_dir() else "Result missing"})
    return out


def _request_targets(d, cells):
    """Resolve Start-here cells only when their Paper target is concrete. Some
    Specs remain prompt-free until a human selects their native owner/scope."""
    spec = cells[0].strip("`") if cells else ""
    space = cells[5] if len(cells) > 5 else ""
    found = []
    if spec == "idea.<idea>" and space == "Ideation":
        i = d["ideation"]
        page = d["story00"]
        g0 = next((status for gate, _, status in d["gates"] if gate == "G0"), "")
        if page and page["rel"] and g0.startswith("✅ I3 receipt"):
            for idea in i.get("ideas", []):
                if idea.get("went") in (None, "", "—", "-"):
                    continue
                target = {"id": idea["id"], "label": idea.get("title", ""), "page": page, "gate_ids": ["G0"],
                          "spec": "idea." + idea["id"]}
                matching = _typed_judgment_runs(d, page, idea["id"], "ridea-")
                found.append(_run_request_entry(
                    d, cells, target, "haipipe-paper-ideation", "none separate from the owner",
                    matching,
                    "`runs/ridea-NN_<slug>.md` with its native `results/<run>/` Result and runtime status.",
                    "review this admitted Idea's exact card and its test Results; continue its matching discussion Run or commission the bounded judgment"))
    elif spec == "claim.<story>.<claim>" and space == "Story":
        for s in d["story"]:
            for c in s["e"]:
                m = re.match(r"E-?\d+", c[0])
                if not m:
                    continue
                eid = m.group(0)
                label = c[3] if len(c) > 3 else (c[1] if len(c) > 1 else "")
                matching = _typed_judgment_runs(d, s, eid, "rclaim-")
                found.append(_run_request_entry(
                    d, cells, {"id": eid, "label": label, "page": s, "gate_ids": ["G1", "G2"],
                               "spec": "claim.%s.%s" % (s["stem"], eid)},
                    "haipipe-paper-story", "haipipe-paper-story",
                    matching,
                    "`runs/rclaim-NN_<slug>.md` with its native `results/<run>/` Result and runtime status.",
                    "judge this frozen C5 proposition against the bound evidence and limits; route missing evidence to its owner after G1"))
    elif spec == "obligation.<story>.<row>" and space == "Story":
        for s in d["story"]:
            for c in s["tt"]:
                tid = c[0]
                label = c[1] if len(c) > 1 else ""
                matching = _typed_judgment_runs(d, s, tid, "rtask-")
                found.append(_run_request_entry(
                    d, cells, {"id": tid, "label": label, "page": s, "gate_ids": ["G1"],
                               "spec": "obligation.%s.%s" % (s["stem"], tid)},
                    "haipipe-paper-story", "haipipe-paper-story",
                    matching,
                    "`runs/rtask-NN_<slug>.md` with its native `results/<run>/` Result and runtime status.",
                    "review this C7 obligation and candidate study plan; commission supporting work only after the applicable G1 release"))
    elif spec == "narrative.<story>.<section>" and space == "Story":
        for s in d["story"]:
            for row in s["sections"]:
                sid = row["id"]
                label = row.get("question", "") or row.get("target", "")
                bound_page = next((p for p in d["sections"] if p["stem"] == sid), None)
                page = dict(s)
                matching = _typed_judgment_runs(d, s, sid, "rnarra-")
                found.append(_run_request_entry(
                    d, cells, {"id": sid, "label": label, "page": page, "gate_ids": ["G3"],
                               "related_page": bound_page,
                               "spec": "narrative.%s.%s" % (s["stem"], sid)},
                    "haipipe-paper-story", "haipipe-paper-story",
                    matching,
                    "`runs/rnarra-NN_<slug>.md` with its native `results/<run>/` Result and runtime status.",
                    "review this exact C8 telling with the current Venue contract and its claim/evidence pointers; G3 release remains a human decision"))
    return found


_RUN_REQUEST_SCRIPT = """<style>
.run-request{margin-top:5px}.run-request>summary{cursor:pointer;color:var(--acc);font-size:12.5px;line-height:1.5}
.run-request-detail{padding:5px 8px 7px;border-left:2px solid var(--line)}
.run-request-detail .brief{font-size:12px;line-height:1.45;margin:0 0 5px}
.run-request-copy{font:600 12px -apple-system,sans-serif;border:1px solid var(--acc);border-radius:6px;background:var(--card);color:var(--acc);padding:4px 8px;cursor:pointer}
#run-request-toast{position:fixed;left:50%;bottom:54px;transform:translateX(-50%);background:var(--fg);color:var(--bg);font:600 12px -apple-system,sans-serif;padding:7px 12px;border-radius:8px;opacity:0;transition:opacity .15s;pointer-events:none;z-index:61}
#run-request-toast.on{opacity:.95}
</style><div id="run-request-toast" role="status" aria-live="polite"></div>
<script>(function(){
  function put(t){
    if(navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(t);
    var a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.focus();a.select();
    var ok=false;try{ok=document.execCommand('copy')}catch(e){}document.body.removeChild(a);
    return ok?Promise.resolve():Promise.reject();
  }
  function toast(msg){var n=document.getElementById('run-request-toast');n.textContent=msg;n.classList.add('on');clearTimeout(toast.t);toast.t=setTimeout(function(){n.classList.remove('on')},1800)}
  document.addEventListener('click',function(e){
    var b=e.target.closest('.run-request-copy');if(!b)return;e.preventDefault();e.stopPropagation();
    put(b.dataset.runPrompt||'').then(function(){toast('Run request copied · paste it into chat when ready')},function(){toast('Copy failed · select and copy the request manually')});
  },true);
})();</script>"""


def render_run(d):
    n_page = sum(1 for r in d["runs"] if r["family"] == "page")
    page_runs = _cards_card("Page Runs", "%d run(s)" % n_page,
                            "RP Page Writing (rp-struct · rp-sec · rp-para · rp-scratch), RD Page Delivery (rdNN) and the paper's judgment Runs "
                            "(ridea · rclaim · rtask · rnarra), one card per page. Open a Run in that page's Outline Run Space; nothing is copied here.",
                            _page_run_cards(d), "no page Run yet · no runs/ folder holds an rp-, rd or judgment ticket")
    n_items = sum(1 for p in d["evidence_runs"] for x in p["rows"] if not x["item"]["retired"])
    ev_runs = _cards_card("Evidence Runs", "%d item(s)" % n_items,
                          "RE Page Evidence Runs, one row per Evidence Item: the Local Run the item names (re-value · re-display · re-cite, or the "
                          "legacy paper-local pj…), its Result, and the Supporting Runs that feed it. The item is the authority; the ticket is looked up.",
                          _evidence_run_cards(d), "no Evidence Item on any page yet")
    sup = d["supporting"]
    ex = _cards_card("Supporting Runs · Execution · %s" % d["blocks"]["label"], "%d block(s)" % len(sup["Execution"]),
                     "Owner-native Task Runs cited by an Evidence Item, as Block › Job › Task › Run. A Run is never renamed or copied; "
                     "each row says who uses it and whether its ticket and receipt are on disk.",
                     _supporting_cards(d, "Execution"), "no Evidence Item cites an Execution Run yet")
    di = _cards_card("Supporting Runs · Discovery · %s" % d["disc"]["label"], "%d board(s)" % len(sup["Discovery"]),
                     "Discovery Paper Runs cited by an Evidence Item, as evidence Board › inquiry › Task Page › Run.",
                     _supporting_cards(d, "Discovery"), "no Evidence Item cites a Discovery Run yet")
    loose = ""
    if sup["loose"]:
        trs = [(esc(u["owner"]), esc(u["raw"]), _link(d, u["rel"], u["page"], lens="evidence"), esc(u["item"])) for u in sup["loose"]]
        loose = ('<div class="card"><h2>Cited without an address<span class="tally">%d</span></h2><div class="brief">A Supporting Run line that names '
                 'no bNN.jNN.tNN.rNN address cannot be placed in the tree.</div>%s</div>' % (len(trs), _table(["owner", "line", "page", "item"], trs)))
    gates = ('<div class="card"><h2>Gates</h2><div class="brief">Read from the files '
             'haipipe-paper-workflow names; a person closes a gate, this only reports the receipt.</div>'
             '<div class="gates">%s</div></div>'
             % "".join('<span><b>%s</b>%s · %s</span>' % (esc(g), esc(n), esc(v)) for g, n, v in d["gates"]))
    fm = folder_map(d)
    headers, body = fm["map"]
    mrows = []
    mapped_types = set()
    for cells in body:
        rt = cells[0].strip("`") if cells else ""
        # Space entries can repeat a Spec; show its folder join once, on the
        # first matching row, instead of duplicating identical chips per Space.
        folders = fm["by_runtype"].get(rt, []) if rt not in mapped_types else []
        mapped_types.add(rt)
        rendered = [esc(c) for c in cells]
        if len(cells) > 6 and "Start here" in cells[6]:
            controls = _request_targets(d, cells)
            if controls:
                rendered[6] += "<br>" + "".join(controls)
        mrows.append(rendered + [("<br>".join('<span class="idtag">%s</span>' % esc(x) for x in folders)) if folders else '<span class="mut">—</span>'])
    wmap = ('<div class="card" data-src="%s" data-ref="Paper Run Spec and control × Space map">'
            '<h2>Workflow map</h2><div class="brief">Run Types/Specs name the bounded work, owner Skills, '
            'prerequisites and read-only Space roles; entry requests go to the named owner in chat. '
            'Controls have no Run Type. This definition map is read-only and never allocates work. '
            '⧉ chat remains a separate source-grounded discussion snippet. Target-bound Run request controls only copy prompt text; '
            'they do not send, start, allocate, or write. Unsupported or unbound cells have no request control. '
            'Actual Ticket/Result identities and status '
            'stay in the separate native Run inventory and owner records.</div>%s</div>'
            % (esc(_repo_rel(d, _SPACE_MAP)),
               (_table(headers + ["folder on this board"], mrows) + _RUN_REQUEST_SCRIPT) if headers else _empty("space-mapping.md has no table")))
    # the same map seen from disk: the REAL folder tree, each slot's Spec / controls shown once, on its node
    by_slot = {r["slot"]: r for r in fm["rows"]}
    roots, homes = build_tree(d)
    def count(ns):
        return sum(1 + count(n["children"]) for n in ns)
    missing = [r for r in fm["rows"] if not any(ok for _, ok, _ in r["actual"])]
    tail = ""
    if missing:
        tail = ('<div class="brief mut" style="margin-top:8px">not on this board yet: %s</div>'
                % " · ".join('<code>%s</code>' % esc(r["folder"].strip("`")) for r in missing))
    srcs = ('<div class="brief">backend Markdown: <code>%s</code> (the Workflow map and Folder tree × Spec or control tables) · <code>%s</code> '
            '(the <code>## Pages</code> groups and <code>dialect:</code>) · the folder itself, walked on every open. '
            'Left: the whole folder tree, click a folder to open it. Right: every folder\'s counts, and the Spec / controls '
            'acting on the first folder of each slot. '
            'Two boxes: the paper folder, then the project homes the paper claims (Task home · Discovery home).</div>'
            % (esc(_repo_rel(d, _SPACE_MAP)), esc(_repo_rel(d, "board.md"))))
    def box(cap, nodes, empty):
        head = ('<div class="tree-head"><span>%s</span><span><span class="idtag rt">Spec / control</span> acting here · '
                '<span class="tn-note">counts</span></span></div>' % cap)
        body = ('<ul class="tree">%s</ul>' % _tree_html(d, nodes, by_slot)) if nodes else '<div class="tn-more">%s</div>' % empty
        return '<div class="treebox">%s%s</div>' % (head, body)
    tree = ('<div class="card"><h2>Folder tree × Spec or control<span class="tally">%d node(s)</span></h2>%s%s%s%s</div>'
            % (count(roots) + count(homes), srcs,
               box("the paper folder · %s" % esc(d["board"].name), roots, "the paper folder is empty"),
               box("the project homes · Task home · Discovery home", homes,
                   "no Task home or Discovery home resolved: set task-home: / discovery-home: in board.md, or add tasks/ and discoveries/ to the project"),
               tail))
    wmap += tree
    return _views("run", [("page", "Page Runs", page_runs), ("evidence", "Evidence Runs", ev_runs),
                          ("supporting", "Supporting Runs", ex + di + loose),
                          ("gates", "Gates", gates), ("workflow", "Workflow map", wmap)], foot=_sources_html(d, "run"))


# `copy to chat` · the discussion/context engagement: a card, a row, or a
# selection becomes a chat-ready snippet that cites the Markdown it came from.
# Run-request copy is separate and offers only exact supported targets.
# The reading pass (JL 260918: larger, and cell edges instead of text nested in text).
# Label/value rows are a two-column table with borders; every grid table has
# cell edges and a shaded header; long prose sits one sentence per line.
_READ_CSS = """
:root{--soft:#f6f7f9} @media(prefers-color-scheme:dark){:root{--soft:#1b1d21}}
body{font-size:16px;line-height:1.65;padding:18px}
h1{font-size:20px} .mut{font-size:14px}
.space,.chip{font-size:13px;padding:5px 12px;border-radius:9px}
.card{padding:16px 18px;margin:0 0 14px;border-radius:12px}
.card h2{font-size:17.5px;margin:0 0 8px}
.card h2 .tally{font-size:12.5px}
.brief{font-size:14.5px;line-height:1.6;margin:0 0 10px;padding-bottom:10px}
.kv{border:1px solid var(--line);border-radius:9px;overflow:hidden;margin:8px 0 4px;background:var(--card)}
.kv>.item-row{display:grid;grid-template-columns:11.5em minmax(0,1fr);gap:0;padding:0;border-top:1px solid var(--line);font-size:14.5px;line-height:1.6}
.kv>.item-row:first-child{border-top:0}
.kv>.item-row>b{background:var(--soft);border-right:1px solid var(--line);padding:11px 12px;font-size:11.5px;line-height:1.45;
 color:var(--fg);opacity:.72;text-transform:uppercase;letter-spacing:.03em;font-weight:700}
.kv>.item-row>span{padding:10px 14px;min-width:0;overflow-wrap:anywhere}
.kv>.item-row.spine-row{font-size:16px;line-height:1.75}
.kv>.item-row.nolabel{grid-template-columns:minmax(0,1fr)}
.kv>.item-row.nolabel>span{padding:12px 14px}
.kv-cap{background:var(--soft);border-bottom:1px solid var(--line);padding:6px 12px;font:700 11.5px -apple-system,sans-serif;
 text-transform:uppercase;letter-spacing:.03em;opacity:.72}
.para{display:block;max-width:86ch} .para+.para{margin-top:12px}
.sent{display:block} .sent+.sent{margin-top:7px}
.spine-row code{font-size:13.5px;padding:1px 5px}
table.grid{font-size:14.5px;line-height:1.55;border:1px solid var(--line);border-radius:9px;border-collapse:separate;border-spacing:0;overflow:hidden;margin:6px 0 8px}
table.grid th{background:var(--soft);font-size:11.5px;padding:9px 11px;border-bottom:1px solid var(--line);border-right:1px solid var(--line);color:var(--fg);opacity:.75}
table.grid td{padding:9px 11px;border-bottom:1px solid var(--line);border-right:1px solid var(--line)}
table.grid th:last-child,table.grid td:last-child{border-right:0}
table.grid tr:last-child td{border-bottom:0}
.item-cards{gap:9px;margin-top:8px}
.item-card{border-radius:10px}
.item-summary{padding:12px 13px;gap:10px}
.item-kind{font-size:12px;padding:1px 8px} .item-sub{font-size:12px} .gates b{font-size:12px} .item-bullets b{font-size:12px}
.item-label{font-size:15.5px;line-height:1.4} .item-title{font-size:13.5px} .item-where{font-size:12px} .item-status{font-size:14px}
.item-detail{padding:10px 12px 13px}
.idtag,.path{font-size:12.5px} .item-bullets{font-size:14.5px}
.tree-job{font-size:14.5px;margin:12px 0 4px} .tree-task{font-size:14px;margin:8px 0 4px 18px}
.gates{font-size:14.5px} pre.path{font-size:13px}
.kv>.item-row>.cc{right:8px;top:8px}
/* Folder tree × Spec or control: two aligned columns. Left the bare tree, right the works
   (.tn-works, a fixed --w wide). A nested <ul> pads only the left, so every row's
   right edge is the card's right edge and the works column lines up at any depth. */
.treebox{--w:clamp(380px,46vw,840px);position:relative;border:1px solid var(--line);border-radius:9px;overflow:hidden;background:var(--card);margin:6px 0 12px}
/* the divider is each works cell's own left edge (not an overlay), so an opened
   explanation table, which spans both columns, is never crossed by it */
.tree-head{display:flex;background:var(--soft);border-bottom:1px solid var(--line);font:700 11.5px -apple-system,sans-serif;
 text-transform:uppercase;letter-spacing:.03em;opacity:.8}
.tree-head>span:first-child{flex:1 1 auto;padding:7px 12px}
.tree-head>span:last-child{flex:0 0 var(--w);box-sizing:border-box;padding:7px 10px 7px 12px;display:flex;align-items:center;gap:5px;flex-wrap:wrap;
 border-left:1px solid var(--line)}
.tree-head .tn-note{text-transform:none;letter-spacing:0;font-weight:500}
ul.tree,ul.tree ul{list-style:none;margin:0;padding:0 0 0 22px;position:relative}
ul.tree{padding:5px 0 5px 6px}
ul.tree ul::before{content:"";position:absolute;left:6px;top:0;bottom:12px;border-left:1.5px solid var(--line)}
ul.tree li{position:relative;margin:0;min-width:0}
ul.tree ul>li::before{content:"";position:absolute;left:-16px;top:16px;width:14px;border-top:1.5px solid var(--line)}
details.tn{margin:0;min-width:0}
details.tn>summary,.tn-file{display:flex;align-items:stretch;min-width:0;padding:0 0 0 8px;
 font:inherit;text-transform:none;letter-spacing:normal;color:var(--fg)}
details.tn>summary{cursor:pointer;border-radius:0} details.tn>summary:before{content:none}
details.tn>summary:hover,.tn-file:hover{background:var(--soft)}
.tn-name{flex:1 1 auto;min-width:0;font:500 14px/1.6 ui-monospace,Menlo,monospace;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding:5px 12px 5px 0}
details.tn>summary .tn-name{font-weight:650}
/* the works: a cell per row, edged below, so each row's chips and counts read as one cell of a table */
.tn-works{flex:0 0 var(--w);box-sizing:border-box;min-width:0;padding:6px 12px 6px 14px;display:flex;flex-direction:column;gap:3px;
 border-bottom:1px solid var(--line);border-left:1px solid var(--line)}
.tn-top{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;min-width:0;min-height:22px}
.tn-note{color:var(--fg);opacity:.82;font-size:14px;line-height:1.5;flex:1 1 auto;min-width:0;overflow-wrap:anywhere}
.idtag.rt{color:var(--acc);border:1px solid var(--acc);border-radius:999px;padding:1px 9px;font-size:12px;line-height:1.7;white-space:nowrap}
.tn-more{color:var(--mut);font-size:12.5px;padding:2px 8px}
details.tn[open]>summary .tn-name:before{content:"▾ ";color:var(--mut)} details.tn>summary .tn-name:before{content:"▸ ";color:var(--mut)}
.tn-file .tn-name:before{content:"  ";white-space:pre}
@media(max-width:760px){.treebox{--w:200px}}
.item-label,.item-title{white-space:normal;overflow:visible;text-overflow:clip}
.item-summary{align-items:start}
.cc{opacity:.7;font-size:11.5px;padding:2px 7px}
@media(max-width:620px){.kv>.item-row{grid-template-columns:minmax(0,1fr)}
 .kv>.item-row>b{border-right:0;border-bottom:1px solid var(--line);padding:6px 12px}
 table.grid{font-size:13.5px} body{font-size:15.5px}}
"""

_COPY_CSS = """
.cc{font:600 12px -apple-system,sans-serif;border:1px solid var(--line);border-radius:6px;background:var(--card);
 color:var(--mut);padding:1px 6px;cursor:pointer;white-space:nowrap;opacity:.55}
.cc:hover{opacity:1;color:var(--acc);border-color:var(--acc)}
.item-summary{grid-template-columns:1.1em auto minmax(0,1fr) auto auto auto}
.item-row{position:relative} .item-row>.cc{position:absolute;right:0;top:2px;opacity:0}
.item-row:hover>.cc{opacity:.9}
h2>.cc{margin-left:8px;vertical-align:middle}
#cc-float{position:absolute;z-index:50;display:none;box-shadow:0 2px 8px rgba(0,0,0,.18);opacity:1;color:var(--acc);border-color:var(--acc)}
#cc-toast{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);background:var(--fg);color:var(--bg);
 font:600 12.5px -apple-system,sans-serif;padding:7px 14px;border-radius:8px;opacity:0;transition:opacity .15s;pointer-events:none;z-index:60;max-width:80vw}
#cc-toast.on{opacity:.95}
@media(max-width:560px){.item-summary{grid-template-columns:1.1em auto minmax(0,1fr) auto auto}}
"""

_COPY_JS = """<div id="cc-toast"></div><button class="cc" id="cc-float" type="button">⧉ copy to chat</button>
<script>
(function(){
  function txt(root, sel){ var n=root&&root.querySelector(sel); return n?n.textContent.replace(/\\s+/g,' ').trim():''; }
  function own(h){ var t=''; h.childNodes.forEach(function(n){ if(n.nodeType===3) t+=n.textContent; }); return t.replace(/\\s+/g,' ').trim(); }
  function clip(t,n){ t=t.replace(/\\s+/g,' ').trim(); return t.length>n ? t.slice(0,n-1)+'…' : t; }
  function toast(m){ var t=document.getElementById('cc-toast'); t.textContent=m; t.classList.add('on'); clearTimeout(toast.t); toast.t=setTimeout(function(){t.classList.remove('on')},1600); }
  function put(t){
    if(navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(t);
    var a=document.createElement('textarea'); a.value=t; a.style.position='fixed'; a.style.opacity='0'; document.body.appendChild(a);
    a.focus(); a.select(); var ok=false; try{ ok=document.execCommand('copy'); }catch(e){} document.body.removeChild(a);
    return ok ? Promise.resolve() : Promise.reject();
  }
  function snippet(el, quote){
    var item=el.closest('.item-card'), card=el.closest('.card'), row=el.closest('.item-row'), tr=el.closest('tr');
    var srcEl=el.closest('[data-src]'), panel=el.closest('.panel'), view=el.closest('.view');
    var where=[];
    if(panel){ var sp=document.querySelector('.space[data-space="'+panel.dataset.space+'"]'); where.push(sp?sp.textContent.trim():panel.dataset.space); }
    if(panel&&view){ var c=panel.querySelector('.chip[data-view="'+view.dataset.view+'"]'); if(c) where.push(c.textContent.trim()); }
    if(card){ var h=card.querySelector('h2'); if(h) where.push(own(h)); }
    if(item) where.push((txt(item,'.item-kind')+' '+txt(item,'.item-label')).trim());
    if(row){ var b=txt(row,'b'); if(b) where.push(b); }
    var body='';
    if(row){ var s=row.querySelector('span'); body=s?s.textContent:''; }
    else if(tr){ body=[].map.call(tr.children,function(td){return td.textContent.replace(/\\s+/g,' ').trim()}).filter(Boolean).join(' | '); }
    else if(item){
      body=[txt(item,'.item-label'),txt(item,'.item-title'),txt(item,'.item-status')].filter(Boolean).join(' · ');
      if(item.open){ var rows=item.querySelectorAll('.item-detail>.item-row'); var more=[].map.call(rows,function(r){return txt(r,'b')+': '+(r.querySelector('span')?r.querySelector('span').textContent:'')}).join('\\n'); body+='\\n'+more; }
    }
    var src=(srcEl&&srcEl.dataset.src)||document.body.dataset.board||'';
    var ref=(srcEl&&srcEl.dataset.ref)||'';
    var out=['[paper board · '+document.body.dataset.paper+'] '+where.filter(Boolean).join(' › ')];
    out.push('source: '+src+(ref?' · '+ref:''));
    if(quote) out.push('quote: "'+clip(quote,400)+'"');
    if(body) out.push('text: '+(body.indexOf('\\n')>=0 ? body.split('\\n').map(function(l){return clip(l,260)}).slice(0,14).join('\\n      ') : clip(body,700)));
    out.push('note: ');
    return out.join('\\n');
  }
  function add(host, before){
    var b=document.createElement('button'); b.type='button'; b.className='cc'; b.textContent='⧉ chat'; b.title='copy this to the chat, with its Markdown source';
    if(before) host.insertBefore(b,before); else host.appendChild(b);
  }
  document.querySelectorAll('.item-summary').forEach(function(sm){ add(sm); });
  document.querySelectorAll('.spine-row').forEach(function(r){ add(r); });
  document.addEventListener('click',function(e){
    var b=e.target.closest('.cc'); if(!b) return;
    e.preventDefault(); e.stopPropagation();
    var fl=document.getElementById('cc-float');
    var sel=String(window.getSelection()||'').trim();
    var el=(b===fl && fl._el) ? fl._el : b;
    if(b!==fl && sel){ var an=window.getSelection().anchorNode; var host=an&&(an.nodeType===1?an:an.parentElement); if(!host || !(b.closest('.item-card, .item-row, .card')||document).contains(host)) sel=''; }
    put(snippet(el, sel)).then(function(){ toast('copied · paste it in the chat and add your note'); },function(){ toast('copy failed · select and copy by hand'); });
    fl.style.display='none';
  },true);
  document.addEventListener('mouseup',function(e){
    var fl=document.getElementById('cc-float'); if(e.target===fl) return;
    setTimeout(function(){
      var s=window.getSelection(); var t=String(s||'').trim();
      if(!t || !s.rangeCount){ fl.style.display='none'; return; }
      var an=s.anchorNode; var host=an&&(an.nodeType===1?an:an.parentElement);
      if(!host || !host.closest('.panel')){ fl.style.display='none'; return; }
      var r=s.getRangeAt(0).getBoundingClientRect();
      fl._el=host; fl.style.display='block';
      fl.style.left=Math.max(8, r.left+window.scrollX)+'px'; fl.style.top=(r.bottom+window.scrollY+6)+'px';
    },0);
  });
})();
</script>"""


def render_paper(board, root, path_param):
    d = collect(board, path_param)
    d["root"] = Path(root).resolve()
    d["sessions"] = session_rows(d)          # needs root for the pair lookup
    chips = "".join('<span class="space" data-space="%s">%s</span>' % (k, l) for k, l in
                    (("setup", "Setup Space"), ("ideation", "Ideation Space"),
                     ("story", "Story Space"), ("run", "Run Space"), ("delivery", "Delivery Space")))
    panels = render_setup(d) + render_ideation(d) + render_story(d) + render_run(d) + render_delivery(d)
    default = "story" if d["story"] else "ideation"
    return _PAGE.format(title=esc(d["title"]), spine=esc(d["spine"]), space_chips=chips,
                        panels=panels, default_space=default, copy_css=_COPY_CSS, copy_js=_COPY_JS, read_css=_READ_CSS,
                        board_src=esc(_repo_rel(d, "board.md")), paper_id=esc(d["board"].name))


# ---------------------------------------------------------------- the route
class PaperPluginMixin:
    """GET /_board/paper — the Board-level Paper Plugin, rendered live."""

    def paper_view(self, head_only=False):
        q = parse_qs(urlparse(self.path).query)
        p = {"path": (q.get("path") or [""])[0], "file": (q.get("file") or [""])[0]}
        got = self.target(p)
        if got[0] is None:
            return self._paper_send(("<h1>📄 paper</h1><p>%s</p>" % esc(got[1])).encode("utf-8"), 404, head_only)
        source, board = got
        if Path(source).name != "board.md":
            return self._paper_send("<h1>📄 paper</h1><p>Paper Plugin requires file=board.md.</p>".encode("utf-8"), 400, head_only)
        if scalar(read(Path(board) / "board.md"), "dialect").strip() != "paper":
            return self._paper_send("<h1>📄 paper</h1><p>This Board is not a paper Board (board.md has no <code>dialect: paper</code>).</p>".encode("utf-8"), 400, head_only)
        try:
            page = render_paper(board, self.root, p["path"])
        except Exception as exc:  # a render bug is a named row, never a blank pane
            return self._paper_send(("<h1>📄 paper</h1><p>render failed: %s</p>" % esc(exc)).encode("utf-8"), 500, head_only)
        return self._paper_send(page.encode("utf-8"), 200, head_only)

    def _paper_send(self, body, code, head_only):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

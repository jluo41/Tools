"""📄 Paper · the shared readers behind every paper Board view (live, storage-less, read-only).
collect() reads a paper Board (board.md `## Pages`, Story and Ideation topics, Sections, sessions, reports, delivery,
gates) into the dict the views draw from. PaperWorkbenchMixin keeps /_board/paper-board, which forwards to the Board on
the shared frame (the four-Space page is retired), and /_board/run-result. Text helpers live in paper_text; the parts'
names callers use are re-exported at the end, and the classic page's modules (_MOVED) resolve through __getattr__."""
import json
import os
import re
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

from live.paper_text import (TASK_STEM, VERSION_DIR, clean, divisions, esc, is_batch, is_section,  # noqa: F401
                             outline_url, part_of, read, scalar, table_rows, task_num)

_PAIRS_DIR = Path(os.environ.get("HAIPIPE_PAIRS_DIR",
                                 Path.home() / ".config" / "haipipe" / "pairs"))


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


# ---------------------------------------------------------------- collectors
STORY_STEM = re.compile(r"^Story(?:[A-Z]|(?!00)\d{2})(?:\b|-)")


# ── the Story on b03's shape (b16 Q04, JL 261007): no Story Page; studio topics and Questions ──────────
# Ideation is sNN-ideation/; each telling is sNN-story-<telling>/, beside the Jobs (its face keeps identity,
# pitch, stakes and its roadmaps); each research question is a Board Question with reports/qNN_<question>/;
# the Section Narrative and its compile order are the version face's ## Narrative. A Board in this shape is
# read as a Story assembled from those homes, so every view reads it as it reads a Story Page.
_QBLOCK = re.compile(r"(?ms)^(####\s+[\d.]+\s*·\s*Question\b.*?)(?=^#{1,3} |\Z)")


def board_topics(board, pattern="s[0-9][0-9]-*"):
    """The Board's sNN topic folders matching a glob: beside its Jobs first (JL 261030), then any in an older
    studio/; one per name."""
    board, out = Path(board), []
    for home in (board, board / "studio"):
        out += [p for p in sorted(home.glob(pattern)) if home.is_dir() and p.is_dir()
                and p.name not in {x.name for x in out}]
    return out


def _topic_home(board, topic):
    """The folder a topic sits in, relative to the Board: "" beside the Jobs, or "studio"."""
    return "" if topic.parent == Path(board) else topic.parent.relative_to(board).as_posix()


def _topic_face(topic):
    face = topic / (topic.name + ".md")
    return face if face.is_file() else None


def _section(text, name):
    """The body under `## <name>` up to the next `## ` heading, or ""."""
    m = re.search(r"(?ms)^## +%s[^\n]*\n(.*?)(?=^## |\Z)" % re.escape(name), text or "")
    return m.group(1).strip() if m else ""


def _question_blocks_of(board, ids):
    """The `#### N · Question …` blocks of the reports these Question ids name (board.md ## Questions)."""
    reg = re.search(r"(?ms)^## Questions[ \t]*\n.*?```ya?ml\n(.*?)```", read(board / "board.md"))
    try:
        import yaml
        rows = (yaml.safe_load(reg.group(1)) or {}).get("questions") or [] if reg else []
    except Exception:
        rows = []
    out = []
    for qid in ids:
        r = next((x for x in rows if isinstance(x, dict) and str(x.get("id")) == qid), {})
        rp = board / r["report"] if r.get("report") else None
        if rp is None or not rp.is_file():
            found = sorted(board.glob("reports/q%s_*/q%s_*.md" % (qid[1:].zfill(2), qid[1:].zfill(2))))
            rp = found[0] if found else None
        m = _QBLOCK.search(read(rp)) if rp else None
        if m:
            out.append(m.group(1).strip())
    return out


def _tells(version):
    face = version / (version.name + ".md")
    return Path(scalar(read(face), "tells").strip()).name if face.is_file() else ""


def assembled_stories(board, version=None):
    """[page-like dicts] for each telling topic, its text assembled as a Story: the face, then
    `### 3 · Research Questions` from the reports it feeds, then `### 8 · Section Narrative` from the
    version that tells it (`version`, else the newest whose face `tells:` names it)."""
    out = []
    for topic in board_topics(board, "s[0-9][0-9]-story-*"):
        face = _topic_face(topic)
        if not topic.is_dir() or face is None:
            continue
        text = read(face)
        feeds = re.search(r"\*\*Feeds:\*\*(.+?)(?:\n\s*\n|\Z)", text, re.S)       # b03's topic contract
        ids = re.findall(r"\bQ\d+\b", scalar(text, "feeds")) + \
            ["Q" + n for n in re.findall(r"\bq(\d\d)_", feeds.group(1) if feeds else "")]
        blocks = _question_blocks_of(board, ids)
        versions = [version] if version else sorted(board.glob("j[0-9][0-9]_v*/"), reverse=True)
        narrative = next((_section(read(v / (v.name + ".md")), "Narrative") for v in versions
                          if v is not None and _tells(v) == topic.name and _section(read(v / (v.name + ".md")), "Narrative")), "")
        three = re.search(r"(?m)^### +3 +·[^\n]*\n", text)       # the face keeps §3's words: the blocks go back in
        if blocks and three:
            nxt = re.compile(r"(?m)^#{2,3} ").search(text, three.end())
            at = nxt.start() if nxt else len(text)
            text, blocks = text[:at].rstrip("\n") + "\n\n" + "\n\n".join(blocks) + "\n\n" + text[at:], []
        extra = (("\n### 3 · Research Questions\n\n" + "\n\n".join(blocks) + "\n") if blocks else "") + \
                (("\n### 8 · Section Narrative\n\n" + narrative + "\n") if narrative else "")
        m = re.search(r"(?ms)^## Content[^\n]*\n.*?(?=^## |\Z)", text)
        text = (text[:m.end()].rstrip("\n") + "\n" + extra + "\n" + text[m.end():]) if m else text + "\n## Content\n" + extra
        out.append({"group": {"label": "Story", "folder": _topic_home(board, topic), "stems": []}, "stem": topic.name,
                    "rel": face.relative_to(board), "text": text})
    return out


def ideation_topic(board):
    """The Ideation topic (sNN-ideation/, beside the Jobs or in an older studio/) read as the Ideation Page, or None."""
    for topic in board_topics(board, "s[0-9][0-9]-ideation"):
        face = _topic_face(topic)
        if face is not None:
            return {"group": {"label": "Story", "folder": _topic_home(board, topic), "stems": []}, "stem": topic.name,
                    "rel": face.relative_to(board), "text": read(face)}
    return None


def collect(board, path_param, version=None):
    """Read everything the four Spaces show. Pure: no writes, no network. `version` (a version Job's
    folder) reads that version's Section Narrative on a Board where the Story is studio topics."""
    board = Path(board)
    text = read(board / "board.md")
    groups = board_pages(text)
    pages = []
    for g in groups:
        for stem in g["stems"]:
            rel = page_file(board, g["folder"], stem)
            pages.append({"group": g, "stem": stem, "rel": rel,
                          "text": read(board / rel) if rel else ""})
    story00 = next((p for p in pages if p["stem"].startswith("Story00")), None) or ideation_topic(board)
    # Story<Letter> is the current form; legacy numbered Stories (Story01-seed, Story02-roadmap,
    # Story03-narrative-MISQ) stay readable per hai-paper-ideation, so they are Stories too;
    # with no Story Page, the telling topics are read as Stories (b16 Q04)
    stories = [p for p in pages if STORY_STEM.match(p["stem"])] or assembled_stories(board, version)
    sections = [p for p in pages if is_section(p["stem"])]
    rounds = [p for p in pages if is_batch(p["stem"])]
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
    d["reports"] = paper_reports(d)
    return d


_REPORT_DIR = re.compile(r"^q(\d{2})_[a-z0-9_]+$")
_REPORT_STATUS = {"answered": ("Answered", "ok"), "partial": ("Partial", "warn"), "open": ("Open", "mut")}


def paper_reports(d):
    """The paper's `reports/qNN_<topic>/qNN_<topic>.md` Report Pages (JL 261003: a board-level
    folder like `studio/`, one Report per Story question, as a Task Block keeps them), keyed
    by question number. A Report names what it answers (`answers: RQ1`) and how far
    (`answer-status: open | partial | answered`); its answer is the Opening's first paragraph."""
    from live.paper_story_tree import _num
    out, home = {}, Path(d["board"]) / "reports"
    if not home.is_dir():
        return out
    for folder in sorted(home.iterdir()):
        m = _REPORT_DIR.match(folder.name)
        page = folder / (folder.name + ".md")
        if not (m and page.is_file()):
            continue
        text = read(page)
        answers = [a.strip() for a in scalar(text, "answers").split(",") if a.strip()]
        nums = {_num(a) for a in answers if re.search(r"\d", a)} or {str(int(m.group(1)))}
        opening = re.search(r"(?ms)^## Opening\s*\n(.*?)(?=^## |\Z)", text)
        first = (opening.group(1).strip().split("\n\n", 1)[0] if opening else "")
        rep = {"rel": "reports/%s/%s" % (folder.name, page.name), "stem": folder.name,
               "title": next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), folder.name),
               "status": scalar(text, "answer-status", "open").strip().lower(),
               "answer": clean(re.sub(r"(?m)^\*\*[^*]+\*\*:.*$", "", first))}
        for n in nums:
            out.setdefault(n, rep)
    return out


def paper_desk(d):
    """The desk name, read from a real B group (`Ba-MISQ-Main` → MISQ), a version Job
    (`j01_v1_misq` → MISQ, its case taken from a Section stem inside it) or, before
    any Section group exists, from the Story's §8 target cell (`MISQ · 1`)."""
    for g in d["groups"]:
        m = re.match(r"^B[a-z]-(.+)-(?:Main|Appendix|Round)$", g["folder"])
        if m:
            return m.group(1)
        m = VERSION_DIR.match(g["folder"])
        if m:
            face = d["board"] / g["folder"] / (g["folder"] + ".md")     # the version's face names its desk
            if face.is_file() and scalar(read(face), "desk"):
                return scalar(read(face), "desk")
            stems = (re.match(r"^S-(.+?)-(?:Main|Appendix)-", s) for s in g["stems"])
            return next((x.group(1) for x in stems if x and x.group(1).lower() == m.group(3).lower()), m.group(3))
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
    `/hai-paper sessions`, JL 260928). The page header's `session:` line
    binds its Claude session; a pair manifest joins by that exact id, else by
    exact pair name. Ideation, Story and Supporting work stay in the current
    session, so only S- pages get rows."""
    root = d.get("root")
    pairs = _pairs_for(root) if root else {}
    rows = []
    for p in d["sections"]:
        parts = p["stem"].split("-")           # S-<desk>-<Main|Appendix>-<N>-<Title>, or tNN_<title>
        tm = TASK_STEM.match(p["stem"])
        desk = (paper_desk(d) or "paper").lower() if tm else parts[1].lower() if len(parts) > 1 else "paper"
        title = tm.group(2) if tm else "-".join(parts[4:] if len(parts) > 4 else parts[3:]).lower()
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


def current_stories(d):
    """The Story board.md `story-current:` names (JL 260930: one paper in this tree), as a
    one-item list; every Story when the line is missing or names none. The logic tree, the
    Sections, Related Papers and the band all read this (JL 261005: "things here are not well
    aligned": a redesign's Sections showed the submitted Story's rows)."""
    cur = scalar(read(d["board"] / "board.md"), "story-current").strip()
    return [s for s in d["story"] if s["stem"] == cur] or d["story"] if cur else d["story"]


# ---------------------------------------------------------------- the route
class PaperWorkbenchMixin:
    """GET /_board/paper-board: the old Board-level page is retired (JL 261007, "could we also remove the
    old page?"); the address now forwards to the paper Board on the shared frame, so old links still land."""

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
        rel = Path(board).resolve().relative_to(Path(self.root).resolve()).as_posix()
        self.send_response(302)
        self.send_header("Location", "/_board/workbench?" + urlencode({"path": rel, "theme": "paper"}))
        self.send_header("Content-Length", "0")
        self.end_headers()

    def run_result_view(self, head_only=False):
        """GET /_board/run-result?task=<Task folder>&run=<run stem>: one run's results."""
        from live.paper_run_view import render_run_result
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


# ---------------------------------------------------------------- moved out: the names callers still import from here
from live.paper_work_homes import (_fmt_state, project_blocks, _addresses, project_discoveries,  # noqa: E402,F401
                                   _disc_lookup, _find, task_home, _unnamed_addrs, _tree_url, _disc_link)
from live.paper_story_read import (ideation, story, _FIELD, section_records, division_body, prose,  # noqa: E402,F401
                                   inline)
from live.paper_evidence_items import hero_evidence, supporting_tree  # noqa: E402,F401
from live.paper_delivery import (gates, _stamp, _size, _links, delivery_dir, delivery_info,  # noqa: E402,F401
                                 _not_ready_ids)
from live.paper_cards import (_table, _link, _kv, _card, _status_cls, _fields, _idea_card, _col,  # noqa: E402,F401
                              _row_ids, _row_key, _plain, _hero_cards, _file_link, _yn, _norm_key)

_MOVED = ("paper_pages", "paper_run_view", "paper_story_tree", "paper_related", "paper_spaces",
          "paper_spaces_delivery")


def __getattr__(name):
    """A name moved to one of the _MOVED modules still resolves here (`from live.paper import story_tree`), loaded
    on first use, so those modules can import this one's helpers at their top without an import cycle."""
    if not name.startswith("__"):
        import importlib
        for module in _MOVED:
            found = importlib.import_module("live." + module).__dict__
            if name in found:
                return found[name]
    raise AttributeError("module %r has no attribute %r" % (__name__, name))

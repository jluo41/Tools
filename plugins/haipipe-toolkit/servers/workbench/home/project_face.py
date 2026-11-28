"""A Project's own face on its page: 🎯 Prediction, 🔻 Funnel, 🙋 Decisions and 📖 Terms from project.md, each
Block's Run source badge, the Project map, a Theme's section of the Project Report, and the face's other sections."""
from __future__ import annotations

import json
import re
import traceback
from pathlib import Path
from urllib.parse import quote

import yaml

from live import frame, task_questions
from live.ui_parts import PB_JS, word_span
from live.focus_page import (
    BAND_CSS,
    FINDINGS_CSS,
    MAP_PHONE,
    STAGE_WORD,
    band_sec,
    block_mark,
    blocks_under_projects,
    descendants,
    face_title,
    inside,
    is_topic,
    job_row,
    kids,
    map_html,
    markdown,
    one_line,
    owned_register,
    page_level,
    page_url,
    read_face,
    report_path,
    said_word,
    side_css,
    state_kind,
    topic_home,
)


def theme_report(th: Path, root: Path) -> str:
    """One Theme inside its Project's Report: one closed numbered section per Block (its name, state word and bar,
    from its Jobs' Tasks), so the Project reads as its Blocks; opened, the Block's Job rows, each opening to its Tasks
    and Runs, the same rows the Block's own page draws."""
    from live.project_findings import FIND_ROW_CSS, findings_parts   # here, not at the top: Findings reads this file
    secs, finds = [], []
    for b in (b for b in kids(th) if inside(b, root)):   # every Block of the Theme: bNN_, Paper-*, Insight-*, ...
        js = [j for j in frame.children(b, "Block") if inside(j, root) and re.match(r"j\d\d_", j.name)]
        rows, marks, filled, total = "", [], 0.0, 0
        for j in js:
            row, word, n, fill = job_row(j, js, root)
            rows += row
            marks.append(word)
            filled, total = filled + fill, total + (n or 1)
        share = round(100 * filled / total) if total else 0
        word = ("no Jobs yet" if not js else "done" if all(m == "done" for m in marks)
                else "not run" if all(m == "not run" for m in marks) else "partly")
        face = read_face(b, root)
        said = face.get("state") or ""                           # the Block's own written state wins (its board.md
        if said:                                                 # `state:`), as its Jobs' rows show theirs
            word = said_word(said)
        goal = one_line(face["goal"], 300)
        for topic, _ in frame._studio_topics(b):                 # its Studio topics, below its Jobs, each by its
            if not (is_topic(topic) and inside(topic, root)):      # title and stage, opening its card in the
                continue                                           # Block's Studio
            notes = frame._notes(topic)
            stage = (frame._note_facts(notes) if notes else {}).get("stage", "")
            title = face_title(notes or topic / "_") or topic.name
            rows += (f'<div class="job-row topic-row"><span class=jn>🎨 {frame.esc(topic.name[:3])}</span>'
                     f'<a href="{frame.esc(topic_home(topic, root))}" title="{frame.esc(topic.name)}"><b>{frame.esc(title)}</b></a>'
                     f'<small>{frame.esc(STAGE_WORD.get(stage, stage))}</small><span class=bar style="visibility:hidden"></span></div>')
        rest = said.partition(" · ")[2].strip()
        body = ((f'<p class=st-lead>{frame.esc(rest)}</p>' if rest else '')
                + (f'<p class="mut">{frame.esc(goal)}</p>' if goal else '') + rows)
        bmark = block_mark(b)
        done = state_kind(word) == "✅ done" or word == "done"
        summary = (f'<summary><span class=bt>{len(secs) + 1} · {frame.esc(bmark)} '   # its name opens the Block's page
                   f'<a class=bl href="{frame.esc(page_url(b, root))}">{frame.esc(b.name)}</a></span>'
                   + (run_badge(b) if th.name == "work" else "")                  # where its newest Runs ran
                   + word_span(word) +
                   f'<span class=bar><i class="{"" if done else "part"}" style="width:{share}%"></i></span></summary>')
        if th.name == "work":                                   # the same row again over its Findings view's parts
            parts = findings_parts(b, root) or '<p class="mut find-none">no findings yet</p>'
            finds.append(f'<details class=band-sec>{summary}<div class=band-jobs>{parts}</div></details>')
        secs.append(f'<details class=band-sec>{summary}<div class=band-jobs>{body}</div></details>')
    data = read_face(th, root)
    purpose = data["goal"] or one_line(data["sections"].get("about") or "", 300)
    lead = f'<p class="focus-sub">Purpose</p><p>{frame.esc(purpose)}</p>' if purpose else ""
    css = FIND_ROW_CSS + FACE_CSS + """<style>
.band-sec .bt a.bl{color:inherit;text-decoration:none}
.band-sec .bt a.bl:hover{text-decoration:underline}
</style>"""
    findings = ('<h3 class=wk-band>🔎 Findings</h3>' + "".join(finds)) if finds else ""
    return side_css() + css + lead + '<h3 class=wk-band>📋 Review Content</h3>' + \
        ("".join(secs) if secs else '<p class="mut">No Blocks yet.</p>') + face_sections(th, root, len(secs) + 1) + findings + PB_JS


# a face section's mark, by the first word of its title, so its sections do not all read as the same 📊 bar;
# a title that starts with its own emoji keeps it, any other title gets 📊
SECTION_ICONS = {"state": "⏳", "status": "⏳", "work": "🔧", "paper": "📄", "discovery": "🔍", "insight": "💡",
                 "design": "📐", "cowork": "🤝", "labeling": "🏷️", "ideation": "💭", "deliverables": "📦",
                 "data": "🗄️", "people": "👥", "timeline": "📅", "next": "➡️", "decisions": "⚖️", "risks": "❗", "blocks": "🧱", "themes": "🗂️"}


def section_icon(title: str) -> str:
    if title and not title[0].isascii():
        return ""
    word = re.split(r"[^a-z]+", title.casefold().lstrip())[0] if title else ""
    return SECTION_ICONS.get(word, "📊") + " "


def own_face(folder: Path, root: Path):
    """The page's own Markdown: its face, else a Project's project.md (README.md, its old name); None outside the SPACE."""
    face = frame.face(folder) or next((folder / n for n in ("project.md", "README.md") if (folder / n).is_file()), None)
    return face if face and inside(face, root) else None


def face_sections(folder: Path, root: Path, start: int = 1) -> str:
    """Each `## ` section of a Project's or a Theme's own Markdown (project.md, work/work.md) other than About, as a
    closed numbered section from `start`, after the Theme's Blocks. About is the page's own words, read elsewhere."""
    face = own_face(folder, root)
    if not face:
        return ""
    sections = read_face(folder, root)["sections"]
    titles = [t.strip() for t in re.findall(r"(?m)^##\s+(.+?)\s*#*\s*$", re.sub(r"(?ms)^```.*?^```", "", face.read_text(encoding="utf-8")))]
    top = PAGE_TOP if page_level(folder) == "Project" else ()     # drawn above the Project's map (project_top)
    secs = [(t, b) for t in titles if t.casefold() not in ("about", *top)
            for b in [sections.get(t.casefold(), "")] if b]
    css = """<style>
.face-sec table td:first-child,.face-sec table th:first-child{position:sticky;left:0;background:var(--bg,#fff);
  white-space:nowrap;z-index:1}
</style>"""                                                     # the row's name stays while the table scrolls
    # the first section starts open, so the page opens on content, not on bare bars
    def body(t, b):                                             # a section written as data reads as that data
        made = FACE_KINDS.get(t.casefold(), lambda *_: "")(b, folder, root)
        return made or markdown(b, folder, root)
    title = lambda t: (FACE_ICONS.get(t.casefold()) or section_icon(t)) + frame.esc(t)
    if not secs:
        return ""
    return BAND_CSS + FINDINGS_CSS + css + FACE_CSS + "".join(
        band_sec(n, title(t), "", body(t, b), cls="face-sec", opened=n == start == 1) for n, (t, b) in enumerate(secs, start))


# ---- a Project's own sections written as data (project.md `## Prediction`, `## Funnel`, `## Decisions`, `## Terms`)
PAGE_TOP = ("prediction", "funnel")                 # drawn above the Project's map, not as closed sections


FACE_ICONS = {"decisions": "🙋 ", "terms": "📖 "}


def face_yaml(text: str, key: str):
    """The `key:` value of the first ```yaml block in a section; None when there is none or it does not parse."""
    m = re.search(r"(?ms)^```ya?ml\s*$(.*?)^```", text or "")
    try:
        data = yaml.safe_load(m.group(1)) if m else None
    except yaml.YAMLError:
        traceback.print_exc()                                  # a typo hides the section; say so in the server log
        return None
    return data.get(key) if isinstance(data, dict) else None


def face_lead(text: str) -> str:
    """The prose of a section before its first fenced block."""
    return re.split(r"(?m)^```", text or "", maxsplit=1)[0].strip()


def _inline(text: str) -> str:
    """Escaped text with `code` and **bold** kept."""
    s = frame.esc(text)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


def _project_path(folder: Path, root: Path, ref: str):
    """A path a Project's face names: from the Project folder, else from the SPACE; None outside the SPACE."""
    for base in (folder, root):
        p = (base / ref).resolve()
        if p.exists() and inside(p, root):
            return p
    return None


def _dotted(data, key: str):
    """outputs.0.rows: a dotted path into dicts and lists, a digit indexing a list; None when any step is missing."""
    for part in str(key).split("."):
        if isinstance(data, list) and part.isdigit() and int(part) < len(data):
            data = data[int(part)]
        elif isinstance(data, dict) and part in data:
            data = data[part]
        else:
            return None
    return data


def _load(path: Path):
    """A JSON or YAML Result, parsed; None when it is missing or does not parse (logged)."""
    if not path.is_file():
        return None
    try:
        text = path.read_text(encoding="utf-8")
        return json.loads(text) if path.suffix == ".json" else yaml.safe_load(text)
    except Exception:
        traceback.print_exc()                                  # in the server log, not hidden
        return None


def receipt_source(runtime: Path) -> str:
    """Where a Run's receipt says it ran: "server" (execution_mode interactive-inline, or a store path under /Volumes/),
    "selftest" (host: laptop-selftest), "laptop" (any other host); "" when it cannot be read."""
    data = _load(runtime)
    if not isinstance(data, dict):
        return ""
    host = str(data.get("host") or "")
    if host == "laptop-selftest":
        return "selftest"
    if str(data.get("execution_mode") or "") == "interactive-inline" or any(
            str(data.get(k) or "").startswith("/Volumes/") for k in ("volume_base", "raw_store", "stage_store")):
        return "server"
    return "laptop" if host else ""


RUN_SOURCE = {"server": ("✅", "server"), "laptop": ("💻", "laptop"), "selftest": ("🧪", "selftest"), "": ("⬜", "none")}


def block_run_source(block: Path) -> str:
    """Where a Block's newest Runs ran: each Task's newest receipt (runs/rNN_*/result/runtime.yaml), the strongest
    of them (server, then laptop, then selftest); "" when it has none."""
    newest = {}
    for p in block.glob("j[0-9]*_*/t[0-9]*_*/runs/r[0-9]*_*/result/runtime.yaml"):
        task = p.parents[3]
        if p.parents[1].name > newest.get(task, (Path(), ""))[1]:
            newest[task] = (p, p.parents[1].name)
    found = {receipt_source(p) for p, _ in newest.values()}
    return next((s for s in ("server", "laptop", "selftest") if s in found), "")


def run_badge(block: Path) -> str:
    mark, word = RUN_SOURCE[block_run_source(block)]
    return f'<span class=run-src title="where its newest Runs ran">{mark} {word}</span>'


def prediction_card(text: str, folder: Path, root: Path) -> str:
    """🎯 Prediction: what the model predicts, from `## Prediction`'s yaml `prediction:`."""
    p = face_yaml(text, "prediction")
    if not isinstance(p, dict):
        return ""
    rows = ""
    for key in ("case", "positive", "negative", "censored", "excluded_at_index", "model", "from"):
        if p.get(key) in (None, ""):
            continue
        value = str(p[key])
        if key == "from":
            at = _project_path(folder, root, value)
            value_html = (f'<a href="/{quote(frame.rel(at, root), safe="/")}"><code>{frame.esc(value)}</code></a>'
                          if at else f'<code>{frame.esc(value)}</code>')
        else:
            value_html = _inline(value)
        rows += f'<div class=pc-row><span class=pc-k>{frame.esc(key.replace("_", " "))}</span><span>{value_html}</span></div>'
    q = f'<p class=pc-q>{_inline(str(p["question"]))}</p>' if p.get("question") else ""
    return f'<section class=pc-card><h3 class=wk-band>🎯 Prediction</h3>{q}{rows}</section>'


def funnel_view(text: str, folder: Path, root: Path) -> str:
    """🔻 Cohort funnel from `## Funnel`'s yaml `funnel:` (stage, label, file, key): one box per stage with its number
    read from that Result; ⬜ when the file is missing, 🧪 with no number when its receipt is a laptop selftest."""
    stages = face_yaml(text, "funnel")
    if not isinstance(stages, list):
        return ""
    boxes = []
    for s in (x for x in stages if isinstance(x, dict)):
        ref = str(s.get("file") or "")
        path = _project_path(folder, root, ref) if ref else None
        value, mark = None, "⬜"
        if path and path.is_file():
            runtime = path if path.name == "runtime.yaml" else path.parent / "runtime.yaml"
            if runtime.is_file() and receipt_source(runtime) == "selftest":
                mark = "🧪"
            else:
                value = _dotted(_load(path), s.get("key") or "")
                mark = "⬜" if value is None else ""
        if isinstance(value, bool):
            value = str(value)
        shown = (f"{value:,}" if isinstance(value, int) else f"{value:.3f}" if isinstance(value, float)
                 else str(value)) if value is not None else mark
        cls = "fn-n" if value is not None else "fn-n fn-none"
        boxes.append(f'<div class=fn-box><span class=fn-s>{frame.esc(str(s.get("stage") or ""))}</span>'
                     f'<span class="{cls}">{frame.esc(shown)}</span>'
                     f'<small>{frame.esc(str(s.get("label") or ""))}</small></div>')
    if not boxes:
        return ""
    lead = face_lead(text)
    return ('<section class=fn-card><h3 class=wk-band>🔻 Funnel</h3>'
            + (f'<p class=mut>{_inline(lead)}</p>' if lead else "")
            + '<div class=fn-row>' + '<span class=fn-ar>▸</span>'.join(boxes) + '</div></section>')


def decisions_list(text: str, folder: Path, root: Path) -> str:
    """🙋 Open decisions from `## Decisions`: "- 🙋 **title**: text `<path>`", the path linked to its page."""
    items = []
    for line in re.findall(r"(?m)^\s*[-*]\s+(.+)$", text or ""):
        m = re.match(r"(?:🙋\s*)?\*\*(.+?)\*\*:?\s*(.*)$", line)
        if not m:
            continue
        title, rest = m.groups()
        tail = re.search(r"`([^`]+)`\s*$", rest)
        at = _project_path(folder, root, tail.group(1)) if tail else None
        link = ""
        if at and at.is_dir():
            rest = rest[:tail.start()].rstrip()
            link = f'<a class=dc-at href="{frame.esc(page_url(at, root))}">{frame.esc(at.name)}</a>'
        items.append(f'<li><span class=mk>🙋</span><b>{frame.esc(title)}</b><span class=hl>{_inline(rest)}</span>{link}</li>')
    return f'<ul class="wk-rows dc-rows">{"".join(items)}</ul>' if items else ""


def terms_list(text: str, folder: Path, root: Path) -> str:
    """📖 Terms from `## Terms`'s yaml `terms:`, one row per term."""
    terms = face_yaml(text, "terms")
    if not isinstance(terms, dict):
        return ""
    return "".join(f'<div class=fd-row><span class=n>{frame.esc(str(k))}</span><span class=d>{_inline(str(v))}</span></div>'
                   for k, v in terms.items())


FACE_KINDS = {"decisions": decisions_list, "terms": terms_list}


def project_top(folder: Path, root: Path) -> str:
    """A Project's 🎯 Prediction and 🔻 Funnel above its map; nothing when project.md has neither."""
    if not own_face(folder, root):
        return ""
    sections = read_face(folder, root)["sections"]
    html = prediction_card(sections.get("prediction", ""), folder, root) + funnel_view(sections.get("funnel", ""), folder, root)
    return FINDINGS_CSS + FIND_CSS_TOP + html if html else ""


FIND_CSS_TOP = """<style>
.pc-card,.fn-card{margin:0 0 14px}.pc-q{margin:4px 0 8px;font-size:15px;font-weight:600}
.pc-row{display:flex;gap:12px;padding:5px 0;border-bottom:1px solid var(--line);font-size:13.5px}
.pc-row:last-child{border-bottom:0}.pc-k{flex:0 0 130px;color:var(--muted);font-size:12.5px}
.pc-row>span:last-child{flex:1;min-width:0;overflow-wrap:anywhere}
.fn-row{display:flex;align-items:stretch;gap:6px;overflow-x:auto;padding:2px 0 6px}
.fn-box{flex:1 0 118px;display:flex;flex-direction:column;gap:2px;border:1px solid var(--line);
  border-radius:8px;background:var(--paper);padding:8px 10px}
.fn-s{font-size:12px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.03em}
.fn-n{font-size:19px;font-weight:600}.fn-none{font-weight:400}.fn-box small{font-size:12px;color:var(--muted);line-height:1.3}
.fn-ar{flex:none;align-self:center;color:var(--muted)}
@media (max-width:600px){.pc-row{flex-direction:column;gap:0}.pc-k{flex:none}.fn-ar{display:none}}
</style>"""


FACE_CSS = """<style>
.dc-rows .dc-at{flex:none;margin-left:auto;font-size:12.5px}.dc-rows .hl{flex:1 1 260px}
.run-src{flex:none;margin-left:auto;font-size:12px;font-weight:400;color:var(--muted);white-space:nowrap}
.run-src+.word{margin-left:10px}
</style>"""


def mindmap_view(folder: Path, root: Path) -> str:
    """The page as a mind map, drawn by hai-mindmap's own renderer (the Studio maps' look), in the ladder's order,
    Themes before Blocks: the page, its Themes, each Theme's Blocks with their goal, and under each Block what it must
    find out, its Jobs and its Studio topics."""
    mm_ = frame.mindmap_module()
    import mmbuild, mmtree
    level = page_level(folder)
    if level == "Project":
        themes = [(th, th.name) for th in kids(folder)]
    elif level == "Theme":
        themes = [(folder, folder.name)]
    else:                                                   # a SPACE or a folder of Projects: each Project's Themes
        themes = [(th, f"{q.name} / {th.name}") for q in blocks_under_projects(folder) for th in kids(q)]
    branches = []
    for th, label in themes:
        blocks = [b for b in kids(th) if inside(b, root)]
        if not blocks:
            continue
        points = []
        for b in blocks:
            qs, _ = owned_register(read_face(b, root), root, 'Questions', 'questions')
            def q_state(r):                                     # each Question's written state, from its answer
                path = report_path(r, b, root)
                said = task_questions.field(task_questions.read(path, root), "state") if path else ""
                return said_word(said) + " · " if said else ""
            under = [mmbuild.built(f"{b}/q{i}", "[find out] " + q_state(r) + (task_questions.words(r.get("title"))
                                                                              or task_questions.words(r.get("question"))))
                     for i, r in enumerate(qs)]
            for j in kids(b):
                state = read_face(j, root).get("state") or ""
                under.append(mmbuild.built(f"{b}/{j.name}", f"[Job] {j.name}" + (" · " + said_word(state) if state else "")))
            if any(True for d in descendants(b) for _ in frame._studio_topics(d)):
                under.append(mmbuild.built(f"{b}/topics", "[Studio] topics"))
            face = read_face(b, root)
            goal = (said_word(face.get("state") or "") + " · " if face.get("state") else "") + one_line(face['goal'], 70)
            # the Block's name is its label pill, as `[find out]` is a line's (a pill holds 64 characters)
            points.append(mmbuild.built(str(b), f"[{b.name}] {goal}", under))
        branches.append(mmbuild.built(str(th), label, points))
    rootnode = mmbuild.built(".", f"{folder.name}", branches)
    rootnode.id = "root"
    tree = mmtree.MindMap({"mindmap": "1", "title": folder.name, "built": "focus-page"}, rootnode)
    # each Theme card starts open on its Blocks (a map of closed Theme pills says nothing); deeper rows stay folded
    drawn = mm_.draw(tree, "", editable=False).replace('<div class=pm-para ', '<div class="pm-para pm-on" ')
    return f'<style>{MAP_PHONE}</style><div class="focus-map">' + map_html(drawn, folder, root) + '</div>'


__all__ = ['theme_report', 'SECTION_ICONS', 'section_icon', 'own_face', 'face_sections', 'PAGE_TOP', 'FACE_ICONS', 'face_yaml', 'face_lead', '_inline', '_project_path', '_dotted', '_load', 'receipt_source', 'RUN_SOURCE', 'block_run_source', 'run_badge', 'prediction_card', 'funnel_view', 'decisions_list', 'terms_list', 'FACE_KINDS', 'project_top', 'FIND_CSS_TOP', 'FACE_CSS', 'mindmap_view']

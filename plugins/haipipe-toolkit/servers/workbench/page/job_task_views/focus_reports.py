"""The focus page's Report views: question cards, reports, answers, the Project and Theme Findings, Themes and Status."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from urllib.parse import quote, urlencode

from live import frame, task_questions
from live import focus_base
from live.focus_base import (descendants, inside, kids, markdown, one_line, page_level, page_url,
    plural, read_face, report_path, state_label, task_tally)
from live.focus_styles_bands import FINDINGS_CSS


def question_cards(rows, folder, root, detailed=False):
    cards = []
    for index, row in enumerate(rows):
        qid = task_questions.words(row.get('id')) or str(index + 1)
        title = task_questions.words(row.get('title')) or task_questions.words(row.get('question'))
        question = task_questions.words(row.get('question'))
        report = report_path(row, folder, root)
        actions = frame.pop(frame.reader(report, root), title, 'Read report ↗') if report else ''
        if not detailed:
            actions += frame._link(page_url(folder, root, 'questions') + '#' + quote(qid), 'Explore question →')
        body = f'<span class="question-id">{frame.esc(qid)}</span><h3>{frame.esc(title)}</h3>'
        if question and question != title:
            body += f'<p>{frame.esc(question)}</p>'
        if detailed:
            aim = task_questions.words(row.get('aim'))
            if aim:
                body += '<p class="question-aim">' + frame.esc(aim) + '</p>'
            work = row.get('work') if isinstance(row.get('work'), list) else []
            links, paths = [], []
            for item in work:
                ref = item if isinstance(item, str) else task_questions.words(item.get('path')) if isinstance(item, dict) else ''
                if not ref:
                    continue
                path = (folder / ref).resolve()
                if not inside(path, root):
                    continue
                face = frame.face(path) if path.is_dir() else None
                label = frame._title(face) if face and inside(face, root) else path.name
                if path.is_dir() and page_level(path) == "Task":   # "j61 · t03_eval_forecast": four alike were unreadable
                    label = f"{path.parent.name.split('_')[0]} · {label}"
                role = task_questions.words(item.get('role')) if isinstance(item, dict) else ''
                link = frame._link(page_url(path, root), label) if path.is_dir() else frame.esc(label)
                links.append(f'<li>{link}' + (f'<small>{frame.esc(role)}</small>' if role else '') + '</li>')
                paths.append(path)
            if len(links) > 8:                               # many Tasks: one line per Job, its Task count (JL 261103:
                jobs = {}                                    # 100+ Task names were a wall)
                for path in paths:
                    job = path.parent if page_level(path) == "Task" else path
                    jobs[job] = jobs.get(job, 0) + (job != path)
                links = [f'<li>{frame._link(page_url(j, root), j.name)}' + (f'<small>{n} Tasks</small>' if n else '') + '</li>'
                         for j, n in jobs.items()]
            if links:
                body += '<section class="question-detail"><h4>Linked work</h4><ul>' + ''.join(links) + '</ul></section>'
            logic = ''
            for key, label in [('hypothesis', 'Hypothesis'), ('acceptance', 'What would answer this')]:
                value = task_questions.words(row.get(key))
                if value:
                    logic += f'<h4>{label}</h4>' + markdown(value, folder, root)
            if logic:
                body += '<section class="question-detail">' + logic + '</section>'
        cards.append(f'<article class="question-card" id="{frame.esc(qid)}">{body}<div class="focus-actions">{actions}</div></article>')
    return '<div class="question-grid' + (' detailed' if detailed else '') + '">' + ''.join(cards) + '</div>'


def reports_html(rows, folder, root, detailed=False):
    cards = []
    for row in rows:
        path = report_path(row, folder, root)
        if not path:
            continue
        text = task_questions.read(path, root)
        opening = task_questions.section(text, 'Opening').split('\n\n')[0]
        state = task_questions.field(text, 'state')
        read_date = task_questions.field(text, 'results-read')
        provenance = ' · '.join(s for s in [state, 'Results read ' + read_date if read_date else ''] if s)
        title = frame._title(path)
        qid = task_questions.words(row.get('id'))
        extra = ''
        if detailed:
            status = task_questions.field(text, 'answer-status') or 'not recorded'
            extra = '<p class="report-answer-status">Answer: ' + frame.esc(status) + '</p>'
            acceptance = task_questions.words(row.get('acceptance'))
            if acceptance:
                extra += '<section class="completion"><h4>Acceptance</h4>' + markdown(acceptance, folder, root) + '</section>'
            work = row.get('work') if isinstance(row.get('work'), list) else []
            links = []
            for item in work:
                ref = item if isinstance(item, str) else task_questions.words(item.get('path')) if isinstance(item, dict) else ''
                target = (folder / ref).resolve() if ref else None
                if not target or not inside(target, root) or not target.exists():
                    continue
                href = page_url(target, root) if target.is_dir() else frame._file_url(target, root)
                role = task_questions.words(item.get('role')) if isinstance(item, dict) else ''
                links.append('<li>' + frame._link(href, target.name) + (': ' + frame.esc(role) if role else '') + '</li>')
            if links:
                extra += '<h4>Contributing work</h4><ul>' + ''.join(links) + '</ul>'
        cards.append('<article class="report-extract" id="' + frame.esc(qid) + '"><span class="question-id">' + frame.esc(task_questions.words(row.get('id')))
                     + f'</span><h3>{frame.esc(title)}</h3><p class="mut">{frame.esc(provenance)}</p>'
                     + (markdown(opening, path.parent, root) if opening else '<p class="mut">No opening recorded.</p>')
                     + extra + '<div class="focus-actions">' + frame.pop(frame.reader(path, root), title, 'Read full report ↗') + '</div></article>')
    return ''.join(cards) or '<p class="mut">No linked reports available.</p>'


def overview_report_html(data, rows, folder, root, reports=False):
    """Reuse the authored map and report register; no separate Item records."""
    tabs = '<nav class="overview-tabs" aria-label="Overview–Report views">'
    for label, group in [('Overview', ''), ('Reports', 'reports')]:
        current = ' aria-current="page"' if reports == bool(group) else ''
        tabs += '<a href="' + frame.esc(page_url(folder, root, 'overview-report', group)) + '"' + current + '>' + label + '</a>'
    tabs += '</nav>'
    if reports:
        return tabs + reports_html(rows, folder, root, detailed=True)
    ref = data.get('overview_map', '')
    path = (folder / ref).resolve() if ref else None
    if path and inside(path, root) and path.is_file() and path.name.endswith('.mindmap.md'):
        href = frame.ROUTE + '?' + urlencode({'path': frame.rel(path, root), 'view': 'focus-map'})
        body = '<iframe class="overview-map" title="Overview mind map" src="' + frame.esc(href) + '"></iframe>'
        body += '<div class="focus-actions">' + frame.pop(href, 'Overview mind map', 'Enlarge map ↗') + '</div>'
    else:
        body = question_cards(rows, folder, root) if rows else '<p class="mut">No overview map or questions recorded.</p>'
    return tabs + body


def deliverables_html(rows, folder, root):
    cards, lines = [], []
    for row in rows:
        title = task_questions.words(row.get('what'))
        means = row.get('means') if isinstance(row.get('means'), list) else []
        files = row.get('files') or []
        files = [files] if isinstance(files, str) else files if isinstance(files, list) else []
        if not means and not files:              # nothing to tick: one plain line, its page linked when it has one
            url = frame.live_url({"url": row.get("url") or "", "folder": folder}, root) if row.get("url") else ""
            lines.append(f'<li><b>{frame.esc(title)}</b>' + (f'<small><a href="{frame.esc(url)}" target=_blank rel=noopener>'
                                                             f'open ↗</a></small>' if url else '') + '</li>')
            continue
        links = []
        for ref in files:
            if not isinstance(ref, str):
                continue
            path = (folder / ref).resolve()
            if inside(path, root) and path.is_file():
                links.append(frame.pop(frame._file_url(path, root), path.name, path.name + ' ↗'))
            else:
                links.append(f'<span class="mut">{frame.esc(ref)}</span>')
        cards.append(f'<article class="report-extract"><h3>{frame.esc(title)}</h3><ul>'
                     + ''.join(f'<li>{frame.esc(m)}</li>' for m in means if isinstance(m, str))
                     + '</ul><div class="focus-actions">' + ''.join(links) + '</div></article>')
    return ''.join(cards) + (FINDINGS_CSS + '<ul class=wk-rows>' + ''.join(lines) + '</ul>' if lines else '')


def report_states(questions: list, folder: Path, root: Path) -> list:
    """(id, title, state label) of each registered Question whose report exists."""
    rows = []
    for index, row in enumerate(questions):
        path = report_path(row, folder, root)
        if path:
            text = task_questions.read(path, root)
            rows.append((task_questions.words(row.get("id")) or str(index + 1),
                         task_questions.words(row.get("title")) or task_questions.words(row.get("question")),
                         state_label(task_questions.field(text, "state") or "")))
    return rows


VERBS = {"report": "read", "work": "do", "studio": "think", "delivery": "hand over", "related": "take in",
         "timeline": "look back", "files": "browse"}


OLD_KEYS = {"status": ("work", "progress"), "children": ("work", "progress"), "folders": ("files", ""),
            "deliverables": ("work", "deliverables"), "timeline": ("timeline", ""),
            "overview-report": ("report", "findings"), "goal": ("report", "standing"), "takeaways": ("report", "findings"),
            "questions": ("report", "questions"), "reports": ("report", "findings"),
            "topic": ("report", "standing"), "pipeline": ("report", "standing")}


# Overview became Report on 261029 (JL: "我们现在就把这个 overview 改成 report ... check 这个 progress 的 status";
# "我不仅仅是 check 它 而且我也要 report 结果": read the results, check the progress); its
# views Summary and Report became Findings and Standing; an old link still opens the same view
OLD_VIEWS = {"summary": "findings", "report": "standing"}


def blocks_under(folder: Path) -> list:
    """Every Block below a Project, a Theme, a folder of Projects or a SPACE."""
    return [d for d in descendants(folder) if page_level(d) == "Block"] if page_level(folder) not in ("SPACE", "Folder") \
        else [b for q in kids(folder) for th in (kids(q) if page_level(q) == "Project" else []) for b in kids(th)] + \
             [b for g in kids(folder) if page_level(g) == "Folder" for q in kids(g) for th in kids(q) for b in kids(th)]


def all_questions(blocks: list, root: Path) -> list:
    """(block, id, title, state) of every registered Question in these Blocks."""
    out = []
    for block in blocks:
        rows, _ = focus_base.owned_register(read_face(block, root), root, 'Questions', 'questions')
        states = {qid: label for qid, _, label in report_states(rows, block, root)}
        for i, row in enumerate(rows):
            qid = task_questions.words(row.get("id")) or str(i + 1)
            out.append((block, qid, task_questions.words(row.get("title")) or task_questions.words(row.get("question")),
                        states.get(qid, "not answered yet")))
    return out


LEAD = re.compile(r"^(Agreed|Decided|Proposed|A proposal)\b[^:.]*?(?:[:.]\s+|,\s+(?=[a-z]))", re.I)


WAITS = re.compile(r"waiting (?:for|on)|open until|left to|until \w+ settles", re.I)


TOPIC_ANSWER = {"answered": "agreed", "agreed": "agreed", "partial": "partial", "proposed": "proposed", "draft": "draft"}


def topic_answer(text: str, qid: str):
    """(stage, sentence) from a Studio topic face's `Q01 · Answer` part (JL 261109: answers live in topics, no
    reports/), or None when the face has no part for this Question."""
    m = qid and re.search(rf"(?ms)^{re.escape(qid)} · Answer\n-+\n(.*?)(?=^\S[^\n]*\n-{{3,}}\n|\Z)", text)
    if not m:
        return None
    a = re.search(r"(?ms)^\*\*Answer(?: \(([^)]*)\))?:\*\*\s*(.+?)(?:\n\s*\n|\Z)", m.group(1))
    words = re.sub(r"\s+", " ", re.sub(r"\*\*|`", "", a.group(2))).strip() if a else ""
    if not words or words.lower().startswith(("not written yet", "no answer")):
        return "", ""
    stage = TOPIC_ANSWER.get((a.group(1) or "").strip().lower(), "draft")
    cut = re.search(r"(?<=[.!?])\s+(?=[A-Z])", words[40:])
    line = (words[:40 + cut.start()] if cut else words).strip()
    return stage, (line if len(line) <= 280 else line[:280].rsplit(" ", 1)[0] + "…")


def first_answer(path: Path, qid: str = "") -> tuple:
    """(stage, sentence) of a report's answer (its Opening): the stage is agreed, proposed or draft, read from the
    answer's own lead ("Proposed (261007), waiting for JL: …"), and the sentence is the claim after that lead; empty
    when no answer is written yet. A Studio topic face answers by its `Q01 · Answer` part instead."""
    text = path.read_text(encoding="utf-8", errors="replace")
    found = topic_answer(text, qid)
    if found is not None:
        return found
    m = re.search(r"^## Opening\s*\n+(.+?)(?:\n\s*\n|\Z)", text, re.M | re.S)
    para = re.sub(r"\s+", " ", re.sub(r"\*\*|`", "", m.group(1))).strip() if m else ""
    if not para or para.lower().startswith("no answer"):
        return "", ""
    lead = LEAD.match(para)
    stage = "draft"
    if lead:
        word = lead.group(1).lower()
        stage = "agreed" if word in ("agreed", "decided") else "proposed"
        para = para[lead.end():].strip()
        para = para[:1].upper() + para[1:]
    more = re.match(r"^(?:Not yet (?:answered|settled)|Waiting (?:for|on) \w+|Open until [^:.]*?)\b[^:.]*[:.]\s+", para)
    if more:                                                # a second lead: "Waiting for JL: …", "Not yet settled: …"
        stage = "proposed"
        para = para[more.end():].strip()
        para = para[:1].upper() + para[1:]
    if WAITS.search(lead.group(0) if lead else "") or re.search(r"open until|left to", task_questions.field(text, "state") or ""):
        stage = "proposed"
    cut = re.search(r"(?<=[.!?])\s+(?=[A-Z])", para[40:])           # one sentence, never a stub of a few words
    line = (para[:40 + cut.start()] if cut else para).strip()
    return stage, (line if len(line) <= 280 else line[:280].rsplit(" ", 1)[0] + "…")


def overview_summary(folder: Path, root: Path, level: str, events: list) -> str:
    """What it has found so far, in the answers' own first sentences (JL 261029: "这种没有信息含量的东西 ... 有啥屁用"):
    first what waits for a person to decide, then what is proposed or agreed, then one line naming what has no answer
    yet. Counts and dates are Status's and Timeline's, not here."""
    waiting, found, empty = [], [], Counter()
    for blk in blocks_under(folder):
        rows, _ = focus_base.owned_register(read_face(blk, root), root, 'Questions', 'questions')
        for row in rows:
            path = report_path(row, blk, root)
            stage, line = first_answer(path, str(row.get("id") or "")) if path else ("", "")
            if not line:
                empty[blk.name] += 1
                continue
            title = task_questions.words(row.get("title")) or task_questions.words(row.get("question"))
            (waiting if stage == "proposed" else found).append((blk, title, stage, line))

    def rows(items):
        return '<ul class="found-list">' + "".join(
            f'<li><div class="found-q"><a href="{frame.esc(page_url(blk, root, "report"))}">{frame.esc(blk.name)}</a>'
            f' · {frame.esc(title)} <span class="found-stage {stage}">{stage}</span></div>'
            f'<div class="found-a">{frame.esc(line)}</div></li>' for blk, title, stage, line in items) + '</ul>'
    parts = []
    data = read_face(folder, root)
    body = data["sections"].get("about") or data["sections"].get("topic") or ""
    if body and body.strip() != (data["goal"] or "").strip():       # the mission already shows under the name; never twice
        parts.append('<h3 class="focus-sub">What it is for</h3>' + markdown(body, folder, root))
    if waiting:
        parts.append(f'<h3 class="focus-sub">Proposed, waiting for you to decide</h3>' + rows(waiting))
    if found:
        parts.append(f'<h3 class="focus-sub">Found so far</h3>' + rows(found))
    if empty:
        parts.append('<h3 class="focus-sub">No answer yet</h3><p class="mut">' + frame.esc(" · ".join(
            f"{name} {n}" for name, n in empty.items())) + '</p>')
    return "".join(parts) or '<p class="mut">Nothing found yet: no Block has written an answer.</p>'


def themes_view(folder: Path, root: Path) -> str:
    """Each Theme, how many Blocks it holds, and what each Block is for, in one line with its counts (JL 261029:
    "每个 theme 下面有多少 block"). The things each Block must find out show in MindMap and on the Block's page, and
    how far each has got in Status, so no two views list the same lines (JL 261029: "为什么感觉它每个 view 都是一样的")."""
    level = page_level(folder)
    themes = kids(folder) if level == "Project" else [folder] if level == "Theme" else \
        [th for q in blocks_under_projects(folder) for th in kids(q)]
    parts = []
    for th in themes:
        blocks = [b for b in kids(th) if inside(b, root)]
        if not blocks:
            continue
        rows = []
        for b in blocks:
            qs, _ = focus_base.owned_register(read_face(b, root), root, 'Questions', 'questions')
            jobs = kids(b)
            topics = sum(1 for d in descendants(b) for _ in frame._studio_topics(d))
            counts = [plural(n, *w) for w, n in ((("thing to find out", "things to find out"), len(qs)), (("Job",), len(jobs)),
                                                 (("Studio topic",), topics)) if n]
            rows.append(f'<li><a href="{frame.esc(page_url(b, root))}"><b>{frame.esc(b.name)}</b></a> '
                        f'<span>{frame.esc(one_line(read_face(b, root)["goal"], 140) or "no purpose written yet")}</span>'
                        + (f' <span class="mut">· {frame.esc(" · ".join(counts))}</span>' if counts else '') + '</li>')
        project = f"{th.parent.name} / " if level in ("SPACE", "Folder") else ""
        parts.append(f'<h3 class="focus-sub">{frame.esc(project + th.name)}</h3><ul class="glance-list">'
                     + "".join(rows) + '</ul>')
    return "".join(parts) or '<p class="mut">No Blocks yet.</p>'


THEME_TITLES = {"cowork": "CoWork"}


THEME_ORDER = ("work", "discovery", "cowork", "insight", "design", "labeling", "ideation", "paper")   # the b10 preview's order


def theme_title(name: str) -> str:
    """A Theme folder's button name: work -> Work, cowork -> CoWork."""
    return THEME_TITLES.get(name, name[:1].upper() + name[1:])


# a Block's mark when its face names none: the first word of its name that says what kind of work it is (JL 261111:
# "why we still have this?", every Block a 🧱); a face's own `emoji:` line always wins, an unknown name keeps 🧱
BLOCK_WORD_MARKS = {
    **dict.fromkeys(("raw", "rawdata", "ingest", "download"), "📥"),
    **dict.fromkeys(("source", "sourcestore", "sources"), "🔌"),
    **dict.fromkeys(("record", "recordstore", "records"), "🗂️"),
    **dict.fromkeys(("case", "casestore", "cases", "cohort"), "👥"),
    **dict.fromkeys(("aidata", "aidatastore", "aidataset", "dataset", "datasets", "data", "corpus", "feature", "features"), "🧮"),
    **dict.fromkeys(("model", "models", "fit", "train", "training", "tslib", "nixtla", "fm", "llm", "ai"), "🧠"),
    **dict.fromkeys(("prediction", "predict", "forecast", "mtp"), "🔮"),
    **dict.fromkeys(("endpoint", "serving", "deploy", "azure", "api"), "🚀"),
    **dict.fromkeys(("evaluation", "eval", "benchmark", "results", "result", "analysis", "scaling"), "📊"),
    **dict.fromkeys(("evidence", "literature", "paper", "papers", "prior", "discovery"), "📚"),
    **dict.fromkeys(("labeling", "label", "labels"), "🏷️"),
    **dict.fromkeys(("design", "ui"), "📐"),
    **dict.fromkeys(("sms", "message", "messages"), "💬"),
    **dict.fromkeys(("recommendation", "ideation", "idea", "ideas"), "💡"),
    **dict.fromkeys(("visit", "visits", "patient", "patients", "physician", "phy", "clm", "claims", "cms"), "🩺"),
    **dict.fromkeys(("diabetes", "cgm", "glucose"), "🩸"),
    **dict.fromkeys(("law", "policy", "legal"), "⚖️"),
    **dict.fromkeys(("demo", "example", "test"), "🧪"),
    **dict.fromkeys(("proposal", "grant", "writing"), "📝"),
    **dict.fromkeys(("engagement", "click", "clicks"), "👆"),
    **dict.fromkeys(("event", "events", "timeline"), "📅"),
    **dict.fromkeys(("pipeline", "tool", "tools", "workbench"), "🔧"),
    **dict.fromkeys(("insight", "insights"), "🔍"),
    **dict.fromkeys(("cowork", "request", "meeting", "collaboration", "team", "irb", "it", "writers"), "🤝"),
    **dict.fromkeys(("external", "externalstore", "tables", "omop", "mimiciv", "etl", "glue", "derived", "npi"), "🗄️"),
    **dict.fromkeys(("experiments", "experiment", "simulator", "pilot", "prototype"), "🧪"),
    **dict.fromkeys(("display", "displays", "excalidraw", "studio", "canvas", "image"), "🖼️"),
    **dict.fromkeys(("plan", "progress", "updates", "status", "topic", "checkups"), "🗓️"),
    **dict.fromkeys(("petition", "niw", "eb1a", "letter", "draft", "introduction", "ta"), "📝"),
    **dict.fromkeys(("year",), "📅"),
    **dict.fromkeys(("neural", "ode", "trees", "boosted", "metalearner", "embedding", "pretrained", "calibration",
                     "regime", "offpolicy", "counterfactual", "token", "vector", "generative", "modeling",
                     "glucontextfm", "hybrid2"), "🧠"),
    **dict.fromkeys(("bench", "qa", "glucoqa", "regression", "descriptive", "disparity", "decomposition",
                     "scorecard", "analyses", "outcome"), "📊"),
    **dict.fromkeys(("review", "search", "questions", "rule", "decision", "method"), "🔎"),
    **dict.fromkeys(("deployment", "streaming", "aws", "connector", "smartwatch", "app", "platform"), "🚀"),
    **dict.fromkeys(("dental", "vaccines", "insulin", "pharmacy", "fill", "clinical", "dm"), "💊"),
    **dict.fromkeys(("haipipe", "toolkit", "utils", "base", "georef", "pull"), "🔧"),
}


def block_mark(block: Path) -> str:
    """A Block's emoji: its face's `emoji:` line, else the mark of the first telling word of its name, else 🧱."""
    face = block / "board.md"
    own = re.search(r"(?m)^emoji:\s*(\S+)", face.read_text(encoding="utf-8", errors="ignore")) if face.is_file() else None
    if own:
        return own.group(1)
    for word in re.split(r"[^a-z0-9]+", re.sub(r"^b\d{2}_", "", block.name).lower()):
        if word in BLOCK_WORD_MARKS:
            return BLOCK_WORD_MARKS[word]
    return "🧱"


def blocks_under_projects(folder: Path) -> list:
    """The Projects below a SPACE or a folder of Projects."""
    if page_level(folder) == "Folder":
        return kids(folder)
    return [q for g in kids(folder) for q in (kids(g) if page_level(g) == "Folder" else [g])]


# what each view shows, one line under the view buttons: the mission above is the page's and the same in every view,
# so the view says what is different (JL 261029)
VIEW_WORDS = {"mindmap": "How it is built, as a map: its parts, and what each must find out.",
              "findings": "What it has found so far, in the answers' own words, and what waits for you.",
              "themes": "What each Block is for, Theme by Theme.",
              "status": "How far each Block has got.",
              "know": "What to keep in mind here: notes kept on this page, below it, and above it up to its Project.",
              "standing": "Where its Jobs, Tasks and Studio topics stand.",
              "answers": "What it has found, one answer per thing it must find out.",
              "questions": "What it must find out.",
              "progress": "Its parts.",
              "deliverables": "What it must hand over, ticked from the disk.",
              "waiting": "What waits for your answer, here and below; each opens the same form its Work row opens.",
              "answered": "What you have answered. Applying it is the owning Task's work.",
              "all": "Everything asked here and below."}


def answer_stage(label: str) -> str:
    """answered, draft or open, from a report's state words."""
    low = (label or "").lower()
    if "not answered" in low or "open" in low:
        return "open"
    if "draft" in low or "partial" in low:
        return "draft"
    return "answered" if any(w in low for w in ("answer", "agreed", "done", "closed")) else "open"


def status_view(blocks: list, root: Path) -> str:
    """How far each Block has got: one row per Block, a bar of what it must find out (answered, draft, open) with the
    words beside it, then the Tasks' states and who waits for a person. The lines themselves are MindMap's."""
    rows = []
    for b in blocks:
        stages = Counter(answer_stage(state) for _, _, _, state in all_questions([b], root))
        total = sum(stages.values())
        tasks = [x for j in kids(b) for x in kids(j)]
        if total:
            bar = '<span class="stat-bar" aria-hidden="true">' + "".join(
                f'<i class="{k}" style="width:{100 * stages[k] / total:.0f}%"></i>' for k in ("answered", "draft", "open")
                if stages[k]) + '</span>'
            words = ("answered" if stages["answered"] == total else "partly answered" if stages["answered"]
                     else "not answered yet")                     # the bar shows the share; no tally (JL 261113)
        else:
            bar, words = '<span class="stat-bar" aria-hidden="true"></span>', "nothing to find out written yet"
        rows.append(f'<li><a href="{frame.esc(page_url(b, root))}"><b>{frame.esc(b.name)}</b></a>{bar}'
                    f'<span>{frame.esc(words)}</span></li>')
    tasks = [x for b in blocks for j in kids(b) for x in kids(j)]
    states = [(x, state_label(read_face(x, root)["state"])) for x in tasks]
    waiting = [x for x, s in states if "WAITING" in s.upper()]
    parts = ['<h3 class="focus-sub">How far each Block has got</h3><ul class="glance-list stat-list">' + "".join(rows) + '</ul>']
    if any(s for _, s in states):
        parts.append('<h3 class="focus-sub">Tasks</h3><p class="glance">' + frame.esc(task_tally([s for _, s in states if s])) + '</p>')
    if waiting:
        parts.append('<h3 class="focus-sub">Waiting for you</h3><ul class="glance-list">' + "".join(
            f'<li><a href="{frame.esc(page_url(x, root))}"><b>{frame.esc(x.name)}</b></a> '
            f'<span class="mut">· {frame.esc(x.parent.parent.name)}</span></li>' for x in waiting) + '</ul>')
    return "".join(parts)

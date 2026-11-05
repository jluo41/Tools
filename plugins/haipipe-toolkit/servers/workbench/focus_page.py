"""Read-only, single-section workbench, selected with layout=focus.

The current folder's face owns Goal, completion criteria and Takeaways. Opening
the page never writes a summary or inherits one from another level.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import traceback
import subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import quote, urlencode

import yaml

from live import frame, page_reader, task_questions
from live.ui_parts import PB_CSS, PB_JS, _side_tabs
from live import interaction_section as IX


def inside(path: Path, root: Path) -> bool:
    return path.resolve().is_relative_to(root.resolve())


def read_face(folder: Path, root: Path) -> dict:
    """Read explicit sections and header fields; fenced examples are not metadata."""
    face = frame.face(folder) or (next((folder / n for n in ("project.md", "README.md") if (folder / n).is_file()), None)
                                  if page_level(folder) == "Project" else None)   # a Project's page: project.md (README.md, its old name)
    text = face.read_text(encoding="utf-8") if face and inside(face, root) else ""
    fields, sections = {}, {}
    front = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    if front:
        try:
            values = yaml.safe_load(front.group(1))
            fields = values if isinstance(values, dict) else {}
        except yaml.YAMLError:
            pass
        text = text[front.end():]
    name, fence, lines = None, None, []
    for line in text.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            run = marker.group(1)
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence):
                fence = None
            if name:
                lines.append(line)
            continue
        heading = re.match(r"^##\s+(.+?)\s*#*\s*$", line) if fence is None else None
        if heading:
            if name:
                sections[name] = "\n".join(lines).strip()
            name, lines = heading.group(1).strip().casefold(), []
        elif name:
            lines.append(line)
        elif fence is None:
            field = re.match(r"^([a-z][a-z-]+):\s*(.*)$", line)
            if field and field.group(1) not in fields:
                value = field.group(2).strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                    value = value[1:-1]
                fields[field.group(1)] = value
    if name:
        sections[name] = "\n".join(lines).strip()

    def field(key):
        value = fields.get(key)
        if not isinstance(value, str) or value.strip().casefold() in {"", "open", "<open>", "none", "-", "null"}:
            return ""
        return value.strip()

    mission = ""
    if (folder / "project.yaml").is_file():          # a Project's goal is its project.yaml mission (haipipe-project)
        found = re.search(r"(?m)^mission:\s*(.+)$", (folder / "project.yaml").read_text(encoding="utf-8", errors="ignore"))
        mission = found.group(1).strip().strip("\"'") if found else ""
    return dict(face=face, sections=sections,
                goal=sections.get("goal") or field("goal") or field("spine") or field("develops") or mission,
                close=sections.get("completion criteria") or field("close"),
                takeaways=sections.get("takeaways", ""), home=field("home-section").casefold(),
                state=field("state"), overview_map=field("overview-map"),
                ui={k: field("ui-" + k) for k in ("block", "job", "task")})   # a theme Block's example pages (JL 261031)


UI_VIEWS = (("block", "Block UI"), ("job", "Job UI"), ("task", "Task UI"))


def ui_view(ref: str, name: str, root: Path) -> str:
    """One real page of the theme, live in the Report (JL 261031: "I think you should have these as well ... the block
    UI, job UI and task UI"). `ref` is a full http(s) link (another SPACE's server) or a path from this SPACE's root."""
    if re.match(r"(?i)^https?://", ref):
        href = ref
    elif not ref.startswith(("/", ".")) and inside((root / ref).resolve(), root) and (root / ref).exists():
        href = frame.ROUTE + "?" + urlencode({"path": ref, "layout": "focus"})
    else:
        return f'<p class="mut">{frame.esc(name)}: <code>{frame.esc(ref)}</code> is not a page here.</p>'
    return (f'<iframe class="ui-page" title="{frame.esc(name)}" loading="lazy" src="{frame.esc(href)}"></iframe>'
            f'<div class="focus-actions"><a class="row-verb" href="{frame.esc(href)}" target="_blank" rel="noopener">'
            f'Open {frame.esc(name)} ↗</a></div>')


def home_section(data: dict, theme: str) -> str:
    """The section a page opens on. Outside the paper theme the intro carries the goal, so the page opens
    on Goal & status (an explicit `home-section: goal` means the same)."""
    if data["home"] == "overview-report":
        return "overview-report"
    if data["home"] == "takeaways" or (data["home"] == "goal" and theme == "paper"):
        return data["home"]
    if data["home"] == "goal":
        return "status"
    if theme == "paper":
        return "takeaways"
    if theme == "work":
        return "status"
    return "takeaways" if data["takeaways"] else "status"


def page_url(folder: Path, root: Path, section="", group="") -> str:
    if folder.resolve() == root.resolve():                 # the SPACE's own page is its Home, /
        query = {k: v for k, v in (("section", section), ("group", group)) if v}
        return "/" + ("?" + urlencode(query) if query else "")
    query = {"path": frame.rel(folder, root), "layout": "focus"}
    if section:
        query["section"] = section
    if group:
        query["group"] = group
    return frame.ROUTE + "?" + urlencode(query)


def markdown(text: str, folder: Path, root: Path) -> str:
    return page_reader.markdown_html(text, base="/" + quote(frame.rel(folder, root), safe="/") + "/")


def owned_register(data, root, heading, key):
    text = task_questions.read(data['face'], root) if data['face'] else ''
    return task_questions.register(text, heading, key)


def report_path(row, folder, root):
    ref = task_questions.words(row.get('report'))
    path = (folder / ref).resolve() if ref else None
    return path if path and inside(path, root) and path.is_file() else None


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
    cards = []
    for row in rows:
        title = task_questions.words(row.get('what'))
        means = row.get('means') if isinstance(row.get('means'), list) else []
        files = row.get('files') or []
        files = [files] if isinstance(files, str) else files if isinstance(files, list) else []
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
    return ''.join(cards)


def state_label(text: str) -> str:
    """A recorded state's label: the words before ' · ' (`🟡 RESULTS IN, UNREAD · r11 complete` -> its label)."""
    return text.split(" · ")[0].strip()


def tasks_below(folder: Path, level: str, root: Path) -> list:
    """The Tasks a page answers for: a Block's Tasks through its Jobs, a Job's own, a Task itself."""
    if level == "Task":
        return [folder]
    if level in ("SPACE", "Folder"):                 # too wide for one status line; each Project says its own
        return []
    if level in ("Project", "Theme"):
        return [d for d in descendants(folder) if page_level(d) == "Task" and inside(d, root)]
    jobs = frame.children(folder, "Block") if level == "Block" else [folder] if level == "Job" else []
    return [t for j in jobs if inside(j, root) for t in frame.children(j, "Job") if inside(t, root)]


def count_words(label: str, n: int) -> str:
    """`🟡 RESULTS IN, UNREAD`, 18 -> `🟡 18 results in, unread`."""
    mark = re.match(r"^([^A-Za-z0-9]*)(.*)$", label)
    return f"{mark.group(1).strip()} {n} {mark.group(2).strip().lower()}".strip()


def tally_words(labels: list) -> str:
    """Each label with its count, most first."""
    return " · ".join(count_words(label, n) for label, n in Counter(labels).most_common())


STATE_KINDS = (                                       # first match wins; read from the label's first clause
    ("🙋 waiting on you", r"waiting|your call|needs? (a )?(sign-in|decision)"),
    ("⏳ running", r"\brunning\b|in progress"),
    ("partly done", r"\bpartial|partly|carried|\bbuilt\b|drawn|redrawn|results in|unread"),
    ("✅ done", r"\bcomplete|\bclosed\b|\bdone\b|\bran\b|generated|finished"),
    ("⬜ not run yet", r"planned|not run|\bwaits?\b|design build|queued|draft"),
    ("⬜ open", r"\bopen\b"),                               # a Task face's `state: OPEN` (no 🔴: ⏳ ✅ ⬜ 🙋 only)
)


def state_kind(label: str) -> str:
    """A Task's free-text state as one of a few kinds, so a tally stays one short line (JL 261030: a Block's
    card showed every Task's whole state sentence joined into one pill). The full sentence stays on the Task."""
    text = (label or "").lower()
    head = re.split(r";|:| - | — |\(", text, maxsplit=1)[0]
    for part in (head, text):
        for kind, pattern in STATE_KINDS:
            if re.search(pattern, part):
                return kind
    return "no state" if not text.strip() else "other"


def task_tally(labels: list) -> str:
    """`✅ done · partly done · ⬜ not run yet`: the kinds of Task state, most first, never their counts (JL 261031:
    "Don't add N topics, N jobs, they are useless, they will change along the way")."""
    return " · ".join(kind for kind, _ in Counter(state_kind(x) for x in labels).most_common())


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


def last_change(folder: Path) -> str:
    """The date of the last commit that touched the folder, from git; nothing when git has none."""
    try:
        out = subprocess.run(["git", "-C", str(folder), "log", "-1", "--format=%cs", "--", "."],
                             capture_output=True, text=True, timeout=3)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


def output_of(holder: Path, root: Path) -> str:
    """The newest Run's figure with its question and headline, shown in place. `holder` is a Task (its
    runs/*/result) or one Run folder (its result)."""
    results = [holder / "result"] if (holder / "result").is_dir() else sorted(holder.glob("runs/*/result"))
    for result in reversed(results):
        picture = next((p for p in (result / "figure.png", result / "preview.png") if p.is_file()), None)
        if not picture or not inside(picture, root):
            continue
        display = {}
        if (result / "display.yaml").is_file():
            try:
                display = yaml.safe_load((result / "display.yaml").read_text(encoding="utf-8")) or {}
            except yaml.YAMLError:
                display = {}
        head = (result / "headline.txt").read_text(encoding="utf-8").strip() if (result / "headline.txt").is_file() else ""
        url = frame._file_url(picture, root)
        question = display.get("question") if isinstance(display, dict) else ""
        return (f'<figure class="row-output"><a data-pop="{frame.esc(result.parent.name)}" href="{frame.esc(url)}"'
                f' target=_blank rel=noopener><img src="{frame.esc(url)}" alt="{frame.esc(result.parent.name)}"'
                ' loading="lazy"></a><figcaption>'
                + (f'<p>{frame.esc(question)}</p>' if question else '')
                + (f'<p class="mut">{frame.esc(head[:400])}</p>' if head else '')
                + f'<p class="mut">Run {frame.esc(result.parent.name)}</p></figcaption></figure>')
    return ""


def one_line(text: str, limit: int = 110) -> str:
    """The first clause of a goal: what a reader needs to choose a row; the whole goal lives on the page itself."""
    text = " ".join((text or "").split())
    m = re.match(r"(.+?)(?::\s|;\s|\.\s|$)", text)
    first = (m.group(1) if m else text).strip().rstrip(".")
    return first if len(first) <= limit else first[:limit].rsplit(" ", 1)[0] + "…"


def picture_of(folder: Path, root: Path) -> Path | None:
    """The page's own picture: the first topic preview it has (s00-overview retired 261029: the Report MindMap
    shows the Block). A Block whose topics sit beside its Jobs (b35-s01-D12) shows its first Job topic's."""
    for _, topic, _ in frame.studio_inventory(folder, root):
        for png in (topic / f"{topic.name}.png",):
            if png.is_file() and inside(png, root):
                return png
    return None


def kid_row(child: Path, root: Path) -> str:
    """One child as one scannable row (haipipe-ui, JL 261029: "make it the award level UI"): its real name, one line
    of what it is, its buttons and its picture; no count pills (JL 261030: "why we have this? I don't think we need
    these?": labels carry no counts, and where a child stands is on its own page)."""
    data = read_face(child, root)
    face = data.get("face")
    line = one_line(data["goal"]) or (frame._title(face) if face and inside(face, root) else "")
    pic = picture_of(child, root)
    picture = (f'<img class="kid-pic" src="{frame.esc(frame._file_url(pic, root))}" alt="" loading="lazy">'
               if pic else '<span class="kid-pic none" aria-hidden="true"></span>')
    url = frame.esc(page_url(child, root))
    return (f'<div class="kid-row"><span class="kid-text"><a class="kid-name" href="{url}">{frame.esc(child.name)}</a>'
            + (f'<a class="kid-line" href="{url}">{frame.esc(line)}</a>' if line else '')
            + f'<span class="row-verbs">{"".join(part_verbs(child, root, pic))}</span>'
            + f'</span><a href="{url}" aria-hidden="true" tabindex="-1">{picture}</a></div>')


# A row's buttons, each popped out over the page like an sNN card's (JL 261030: "please create the draw, mind map and
# delivery for them"; "we can also add the job-task-run to it, to show the structure content"): its drawing, its
# mind map, its structure down to the Runs, and its delivery.
PARTS = (("map", "Mind map"), ("work", "Work"), ("delivery", "Delivery"))   # Work: its Jobs, Tasks and Runs


def part_verbs(folder: Path, root: Path, pic: Path | None = None) -> list:
    out = []
    drawing = pic.with_suffix(".excalidraw") if pic else None
    if drawing and drawing.is_file() and inside(drawing, root):
        out.append(f'<a class="row-verb" data-pop="{frame.esc(folder.name)} · drawing" '
                   f'href="{frame.esc(frame._draw_url(drawing, root))}" target=_blank rel=noopener>Draw</a>')
    for key, name in PARTS:
        if key == "work" and work_root(folder) is None:
            continue
        href = frame.ROUTE + "?" + urlencode({"view": "focus-part", "part": key, "path": frame.rel(folder, root)})
        out.append(f'<a class="row-verb" data-pop="{frame.esc(folder.name)} · {frame.esc(name)}" '
                   f'href="{frame.esc(href)}" target=_blank rel=noopener>{frame.esc(name)}</a>')
    return out


def work_root(folder: Path) -> Path | None:
    """What its Work tree (Jobs, Tasks, Runs) starts from: a Block or a Job itself, a Project's work/ world; an sNN's,
    the work that makes its delivery (JL 261030: "could we add the work, (which are the jobs-task)"): the Job its
    render.yaml names as a builder (`by:`), else the Job it sits in; none yet for a Block's sNN that names none."""
    level = page_level(folder)
    if level == "Topic":
        owner = frame.topic_owner(folder)
        card = folder / "delivery" / "render.yaml"
        named = re.findall(r"(?m)^\s*by:\s*['\"]?(j\d+_[^/\s'\"]+)", card.read_text(encoding="utf-8", errors="ignore")) \
            if card.is_file() else []
        for name in named:
            if (owner / name).is_dir():
                return owner / name
        if frame.level_of(owner) == "Task":
            return owner.parent
        return owner if frame.level_of(owner) == "Job" else None   # a Block's sNN with no Job of its own: no Job yet
    if level in ("Block", "Job"):
        return folder
    if level == "Project" and (folder / "work").is_dir():
        return folder / "work"
    if level == "Theme" and folder.name == "work":
        return folder
    return None


def part_document(folder: Path, root: Path, key: str) -> str:
    """One of a row's parts alone, for its pop-out: its mind map, its Work (Jobs, Tasks, Runs), or its delivery."""
    if key == "interactions" and folder.is_dir() and inside(folder, root):   # the Interaction button's list (JL 261031)
        items = interaction_items(folder, root)
        body = standard_interactions(items, folder, root, in_pop=True) or '<p class="mut">No interactions here.</p>'
        return document(f"{folder.name} · Interaction", '<main class="focus-page"><h1>' + frame.esc(folder.name)
                        + '<span class="h1-section">Interaction</span></h1><section class="focus-card">'
                        + f'<div class="focus-content">{body}</div></section></main>')
    if key == "run" and folder.is_dir() and inside(folder, root) and folder.parent.name == "runs":
        return run_document(folder, root)
    if not folder.is_dir() or not inside(folder, root) or key not in dict(PARTS):
        return ""
    if key == "map":
        body = parts_mindmap(folder, root) if page_level(folder) in ("Block", "Job", "Task") else mindmap_view(folder, root)
    elif key == "work":
        start = work_root(folder)
        if start is None:
            return ""
        mm_ = frame.mindmap_module()
        import mmbuild
        body = mm_.draw(mmbuild.from_work(start), "", editable=False, base=start,     # a result's chip pops it out
                        url_of=lambda q: frame.reader(q, root) if inside(q, root) else "")
    else:
        body = delivery_html(folder, root) or '<p class="mut">No delivery yet: nothing agreed has been handed over.</p>'
    if key in ("map", "work"):                           # the bare map, as an sNN's Mind map pop-out shows it
        return document(f"{folder.name} · {dict(PARTS)[key]}", body)
    return document(f"{folder.name} · {dict(PARTS)[key]}", '<main class="focus-page"><h1>' + frame.esc(folder.name)
                    + f'<span class="h1-section">{frame.esc(dict(PARTS)[key])}</span></h1><section class="focus-card">'
                    + f'<div class="focus-content">{body}</div></section></main>')


# ── a Run's pop-out (JL 261103: "when I click a run, it will show all the information from that run folder with a pop
# out window, so we can quickly understand what happened"; drawn as b17-s58 screen P): everything in runs/<run>/, read
# in place: what happened, what it made (result/ as side tabs), how it ran (card, ticket, config), its passes ─────────
RUN_SHOW = (".md", ".txt", ".csv", ".tsv", ".json", ".yaml", ".yml", ".log", ".png", ".jpg", ".jpeg", ".svg", ".html")
RUN_BIG = 400_000                                       # a file past this is named, never read into the pop-out


def _read(path: Path, limit: int = RUN_BIG) -> str:
    try:
        if path.stat().st_size > limit:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def _run_file(path: Path, root: Path) -> str:
    """One result file shown as what it is: a picture, a small table, or its text."""
    url = frame._file_url(path, root)
    ext = path.suffix.lower()
    if ext in (".png", ".jpg", ".jpeg", ".svg"):
        return f'<a data-pop="{frame.esc(path.name)}" href="{frame.esc(url)}" target=_blank rel=noopener><img class="run-pic" src="{frame.esc(url)}" alt="{frame.esc(path.name)}"></a>'
    if ext == ".html":
        return f'<iframe class="run-frame" src="{frame.esc(url)}" title="{frame.esc(path.name)}"></iframe>'
    text = _read(path)
    if not text:
        return f'<p class="mut">{frame.esc(path.name)} is large: <a href="{frame.esc(url)}" target=_blank rel=noopener>open it</a>.</p>'
    if ext in (".csv", ".tsv"):
        sep = "\t" if ext == ".tsv" else ","
        rows = [ln.split(sep) for ln in text.splitlines()[:21]]
        more = len(text.splitlines()) - 21
        head, body = rows[0], rows[1:]
        return ('<div class="run-table"><table><thead><tr>' + "".join(f"<th>{frame.esc(c)}</th>" for c in head)
                + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{frame.esc(c)}</td>" for c in r) + "</tr>" for r in body)
                + "</tbody></table></div>" + (f'<p class="mut">and {more} more rows</p>' if more > 0 else ""))
    lines = text.splitlines()
    shown = "\n".join(lines[:200])
    return (f'<pre class="run-text">{frame.esc(shown)}</pre>'
            + (f'<p class="mut">{len(lines) - 200} more lines: <a href="{frame.esc(url)}" target=_blank rel=noopener>open the file</a></p>' if len(lines) > 200 else ""))


def run_order(f: Path):
    """What a reader reads first: the report and summary, then tables and figures, then the rest; logs and configs last."""
    name, ext = f.name.lower(), f.suffix.lower()
    rank = (0 if name in ("run-report.md", "summary.txt", "headline.txt") else 1 if ext == ".md" else
            2 if ext in (".csv", ".tsv", ".png", ".jpg", ".jpeg", ".svg", ".html") else
            4 if ext == ".log" or "config" in name or "snapshot" in name else 3)
    return rank, str(f)


def _yaml(path: Path) -> dict:
    try:
        data = yaml.safe_load(_read(path)) if path.is_file() else {}
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def run_document(run: Path, root: Path) -> str:
    """The Run's pop-out: 1 what happened (its headline and state), 2 what it made (result/ as side tabs, the report
    first), 3 how it ran (run.yaml in words, its ticket, its config), 4 its passes (each with its log's last lines)."""
    card = _yaml(run / "run.yaml")
    result = run / "result"
    receipt = _yaml(result / "runtime.yaml")
    first = sorted((f for f in result.glob("*") if f.suffix.lower() in (".md", ".txt") and f.name != "headline.txt"),
                   key=run_order) if result.is_dir() else []   # no headline: the report's own first line says it
    summary = next((ln.strip(" #") for f in first[:1] for ln in _read(f).splitlines() if ln.strip()), "")
    head = (_read(result / "headline.txt").strip() or str(receipt.get("headline") or "") or summary
            or str(card.get("ask") or card.get("target") or ""))
    status = str(receipt.get("status") or card.get("status") or "not run yet")
    when = " to ".join(str(receipt[k])[:16].replace("T", " ") for k in ("started_at", "finished_at") if receipt.get(k))
    fail = str(receipt.get("failure") or "")
    passes = sorted((d for d in (run / "passes").glob("*") if d.is_dir()), reverse=True) if (run / "passes").is_dir() else []
    state = " · ".join(x for x in (status, when, f"newest pass {passes[0].name}" if passes else "") if x)
    sec = []
    sec.append('<h3 class="focus-sub">1 · 📌 What happened</h3>'
               + (f'<p class="run-head">{frame.esc(head)}</p>' if head else '<p class="mut">No headline written.</p>')
               + f'<p class="run-state">{frame.esc(state)}</p>' + (f'<p class="run-fail">{frame.esc(fail)}</p>' if fail else ""))
    files = []
    if result.is_dir():
        found = sorted((f for f in result.rglob("*") if f.is_file() and f.suffix.lower() in RUN_SHOW and f.name != "runtime.yaml"
                        and inside(f, root)), key=run_order)
        files = found[:24]
    if files:
        tabs, panels = "", ""
        for k, f in enumerate(files):
            rel = f.relative_to(result).as_posix()
            tabs += (f'<input type="radio" name="runtab" id="rt{k}"' + (" checked" if k == 0 else "") + '>'
                     f'<label for="rt{k}">{frame.esc(rel)}</label>')
            panels += f'<div class="run-panel" data-k="{k}">{_run_file(f, root)}</div>'
        style = "".join(f'#rt{k}:checked~.run-panels .run-panel[data-k="{k}"]{{display:block}}' for k in range(len(files)))
        sec.append(f'<h3 class="focus-sub">2 · 📊 What it made · result/</h3><style>{style}</style>'
                   f'<div class="run-tabs">{tabs}<div class="run-panels">{panels}</div></div>')
    else:
        sec.append('<h3 class="focus-sub">2 · 📊 What it made · result/</h3><p class="mut">Nothing made yet.</p>')
    words = [("what it does", card.get("role") or card.get("type")), ("kind", card.get("kind")), ("who", card.get("agent")),
             ("skill", card.get("skill")), ("reads", card.get("reads") or card.get("inputs")), ("writes", card.get("writes")),
             ("feeds", card.get("feeds")), ("ticket", card.get("ticket"))]
    rows = "".join(f'<tr><th>{frame.esc(k)}</th><td>{frame.esc(", ".join(map(str, v)) if isinstance(v, list) else str(v))}</td></tr>'
                   for k, v in words if v)
    ticket = run / str(card.get("ticket") or "")
    if not ticket.is_file():
        ticket = next((f for f in sorted(run.glob(run.name + ".*")) if f.suffix in (".sh", ".ps1", ".cmd", ".md")), None)
    config = next((f for f in (run / "config.yaml", run / "config.do") if f.is_file()), None)
    how = f'<table class="run-card">{rows}</table>' if rows else '<p class="mut">No run.yaml.</p>'
    for label, f in (("ticket", ticket), ("config", config)):
        if f and f.is_file() and inside(f, root):
            how += f'<details><summary>{label}: {frame.esc(f.name)}</summary>{_run_file(f, root)}</details>'
    sec.append('<h3 class="focus-sub">3 · 🎫 How it ran · run.yaml, ticket, config</h3>' + how)
    if passes:
        items = ""
        for d in passes:
            title = (re.search(r"(?m)^#\s*(.+)$", _read(d / "pass.md")) or [None, ""])[1]
            log = next((f for f in sorted(d.rglob("*.log"), key=lambda f: f.stat().st_mtime, reverse=True)), None)
            tail = "\n".join(_read(log).splitlines()[-5:]) if log else ""
            items += (f'<li><b>{frame.esc(d.name)}</b> <span class="mut">{frame.esc(title)}</span>'
                      + (f'<pre class="run-text">{frame.esc(tail)}</pre>' if tail else "") + '</li>')
        sec.append(f'<h3 class="focus-sub">4 · 🔁 Passes · passes/</h3><ul class="run-passes">{items}</ul>')
    css = ('<style>.run-head{font-size:20px;margin:6px 0 2px}.run-state{color:#495057;margin:0 0 6px}.run-fail{color:#c92a2a}'
           '.run-tabs{display:flex;flex-wrap:wrap;gap:6px;align-items:flex-start}.run-tabs input{display:none}'
           '.run-tabs label{border:1px solid #dee2e6;border-radius:6px;padding:4px 10px;font-size:12px;cursor:pointer;background:#fff}'
           '.run-tabs input:checked+label{border-color:#1864ab;background:#e7f5ff;color:#1864ab}'
           '.run-panels{flex-basis:100%}.run-panel{display:none;border:1px solid #dee2e6;border-radius:8px;padding:10px;margin-top:6px}'
           '.run-pic{max-width:100%;height:auto}.run-frame{width:100%;height:480px;border:0}'
           '.run-text{white-space:pre-wrap;font-size:12px;max-height:420px;overflow:auto;margin:0}'
           '.run-table{overflow:auto;max-height:420px}.run-table table,.run-card{border-collapse:collapse;font-size:12px}'
           '.run-table td,.run-table th,.run-card td,.run-card th{border-bottom:1px solid #e9ecef;padding:3px 8px;text-align:left}'
           '.run-card th{color:#868e96;font-weight:400}.run-passes{list-style:none;padding:0}</style>')
    return document(f"{run.name} · Run", css + '<main class="focus-page"><h1>' + frame.esc(run.name)
                    + '<span class="h1-section">Run</span></h1><p class="view-caption">Everything in runs/'
                    + frame.esc(run.name) + '/: what it made first, then how it ran.</p><section class="focus-card">'
                    + '<div class="focus-content">' + "".join(sec) + '</div></section></main>')


def run_url(run: Path, root: Path) -> str:
    return frame.ROUTE + "?" + urlencode({"view": "focus-part", "part": "run", "path": frame.rel(run, root)})


def open_topics(folder: Path, root: Path) -> int:
    """How many Studio topics at this page or below are still open, explore or shaping (JL 261029: "more sNN, means
    for that item, more human to intervene"): each one waits on a person's decision, never on a machine."""
    n = 0
    for _, topic, _ in frame.studio_inventory(folder, root):
        notes = frame._notes(topic)
        stage = frame._note_facts(notes)["stage"] if notes and inside(notes, root) else ""
        n += stage not in ("agreed", "closed")
    return n


def kid_group(name: str, href: str, rows: list) -> str:
    return (f'<section class="kid-group"><h3 class="kid-head"><a href="{frame.esc(href)}">{frame.esc(name)}</a>'
            f'<span class="kid-count">{len(rows)}</span></h3>' + "".join(rows) + '</section>')


RUN_MARK = {"complete": "✅", "done": "✅", "failed": "❌", "blocked": "🔶", "running": "⏳", "planned": "⬜"}
FOLD_CSS = """<style>
.fold-tree,.fold-tree ul{list-style:none;margin:0;padding:0}.fold-tree ul{margin-left:9px;padding-left:16px;border-left:1px solid var(--line,#ddd)}
.fold-tree li{position:relative;padding:2px 0}.fold-tree ul>li::before{content:"";position:absolute;left:-16px;top:13px;width:12px;border-top:1px solid var(--line,#ddd)}
.fold-tree summary{list-style:none;cursor:pointer}.fold-tree summary::-webkit-details-marker{display:none}
.fold-tree summary::before{content:"▸";flex:none;width:10px;color:var(--muted,#888);font-size:10px}.fold-tree details[open]>summary::before{content:"▾"}
.fold-row{display:flex;gap:10px;align-items:baseline;min-width:0}.fold-row.leaf{padding-left:10px}
.fold-row a{flex:none;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px;text-decoration:none}.fold-row a:hover{text-decoration:underline}
.fold-row b.fam{flex:none;font-size:13px}.fold-tree .fold-out{padding:4px 0 6px 10px}.fold-tree .fold-out::before{display:none}.fold-row .st{flex:none;font-size:12px;color:var(--muted,#888)}
.fold-row small{flex:1;min-width:0;color:var(--muted,#888);font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
@media (max-width:640px){.fold-row{flex-wrap:wrap;gap:2px 8px}.fold-row small{flex-basis:100%;white-space:normal}}
</style>"""


FAMILY_MIN = 4                                       # four or more same-shaped Tasks fold into one line


def task_families(tasks: list) -> list:
    """A Job's Tasks in families (JL 261103: "walk this block, I still feel it is very hard to read"): Tasks named
    alike but for a last value (t11_train_numeric_1m … t22_train_numeric_1b) are one family, keyed by the shared middle
    ("train_numeric") with its values ("1m" … "1b"); others stand alone. Returns [(key or None, [tasks], [values])],
    in folder order."""
    keyed = []
    for t in tasks:
        m = re.match(r"t\d+_(.+)_([0-9][0-9.]*[a-z]*)$", t.name)
        keyed.append((m.group(1), m.group(2)) if m else (None, None))
    count = {}
    for k, _ in keyed:
        if k:
            count[k] = count.get(k, 0) + 1
    out, seen = [], {}
    for t, (k, v) in zip(tasks, keyed):
        if k and count[k] >= FAMILY_MIN:
            if k not in seen:
                seen[k] = len(out)
                out.append((k, [], []))
            out[seen[k]][1].append(t)
            out[seen[k]][2].append(v)
        else:
            out.append((None, [t], []))
    return out


def family_words(key: str, tasks: list, values: list) -> tuple:
    """A family's name and its line: "t11–t22 train numeric", "12 Tasks, 1m to 1b"."""
    first, last = tasks[0].name.split("_")[0], tasks[-1].name.split("_")[0]
    return f"{first}–{last} {key.replace('_', ' ')}", f"{len(tasks)} Tasks, {values[0]} to {values[-1]}"


def run_rows(task: Path) -> list:
    """A Task's Run folders with their mark and headline: one reading for Status's tree and the mind map."""
    rows = []
    for r in sorted(d for d in (task / "runs").glob("*") if d.is_dir() and not d.name.startswith((".", "_"))):
        rt, card = r / "result" / "runtime.yaml", r / "run.yaml"
        text = rt.read_text(encoding="utf-8", errors="ignore") if rt.is_file() else ""
        st = _yaml_status(text) or _yaml_status(card.read_text(encoding="utf-8", errors="ignore") if card.is_file() else "")
        rows.append((r, RUN_MARK.get(st, "⬜"), (re.search(r'(?m)^headline:\s*"?(.*?)"?\s*$', text) or [None, ""])[1]))
    return rows


def fold_tree(folder: Path, root: Path, level: str, outputs: bool = True) -> str:
    """A Block's Jobs, or a Job's Tasks, as one folding tree down to each Task's Runs (JL 261102: "could we make it
    looks like this to be collapsable"; "we also want to see what are the runs under each task"). Each line: its
    name (opens in the pop-out, JL: "I don't want to switch but to have the pop out window first"), its state, its
    goal or, for a Run, its receipt's headline. Everything starts folded."""
    def line(href, name, label, state, note, kids="", extra="", short_note=False):
        row = (f'<a href="{frame.esc(href)}" data-pop="{frame.esc(label)}">{frame.esc(name)}</a>'
               + (f'<span class=st>{frame.esc(state)}</span>' if state else "") + extra
               + (f'<small title="{frame.esc(note)}">{frame.esc(note)}</small>' if note and short_note else ""))
        if note and not short_note:                       # a goal sentence waits behind a hover (JL 261103: "too many words")
            row = row.replace(f'data-pop="{frame.esc(label)}"', f'data-pop="{frame.esc(label)}" title="{frame.esc(note)}"', 1)
        if not kids:
            return f'<li><div class="fold-row leaf">{row}</div></li>'
        return f'<li><details><summary class=fold-row>{row}</summary><ul>{kids}</ul></details></li>'

    def runs(task: Path) -> str:
        out = ""
        for r, mark, head in run_rows(task):
            out += line(run_url(r, root), r.name, f"{task.name} · {r.name}", mark, head, short_note=True)
        return out

    tops = [c for c in frame.children(folder, level) if inside(c, root)]
    waiting = {c for c in tops if open_topics(c, root)}
    every = len(tops) > 1 and len(waiting) == len(tops)   # on every row it says nothing: once, on top (JL 261103)

    def marks(child: Path) -> str:
        """What waits on a person here (never a count) and the interaction button, as the cards had them."""
        here = child in waiting if child in tops else bool(open_topics(child, root))
        wait = '<span class="row-wait">🙋 open points wait on you</span>' if here and not every else ""
        return wait + interaction_button(interactions(child, root), child, root)

    def task_line(t: Path) -> str:
        d = read_face(t, root)
        out = output_of(t, root) if outputs else ""   # the Task's output, in place, first inside its fold
        kids = (f'<li class=fold-out>{out}</li>' if out else "") + runs(t)
        st = state_label(d["state"])                   # "✅ DONE" as the Jobs' "✅ done" (JL 261103)
        return line(page_url(t, root), t.name, t.name, state_words(st) if st else "", d["goal"].split("\n")[0], kids, marks(t))

    def family_lines(ts: list) -> str:
        """Same-shaped Tasks as one folded line each family (its state tally, its values), the Tasks inside it."""
        out = ""
        for key, members, values in task_families(ts):
            if key is None:
                out += task_line(members[0])
                continue
            name, words = family_words(key, members, values)
            tally = task_tally([s for s in (state_label(read_face(t, root)["state"]) for t in members) if s])
            out += (f'<li><details><summary class=fold-row><b class=fam>{frame.esc(name)}</b>'
                    + (f'<span class=st>{frame.esc(tally)}</span>' if tally else '')
                    + f'<small>{frame.esc(words)}</small></summary><ul>{"".join(task_line(t) for t in members)}</ul></details></li>')
        return out

    items = ""
    for child in (frame.children(folder, level) if level == "Block" else []):
        if not inside(child, root):
            continue
        d = read_face(child, root)
        if level == "Block":
            ts = [t for t in frame.children(child, "Job") if inside(t, root)]
            tally = task_tally([s for s in (state_label(read_face(t, root)["state"]) for t in ts) if s])
            items += line(page_url(child, root), child.name, child.name, tally, d["goal"].split("\n")[0],
                          family_lines(ts), marks(child))
    if level != "Block":
        items += family_lines([c for c in frame.children(folder, level) if inside(c, root)])
    head = (f'<p class="row-wait">🙋 every {"Job" if level == "Block" else "Task"} has a Studio topic with open points '
            f'waiting on you</p>') if every else ""
    return FOLD_CSS + head + f'<ul class=fold-tree>{items}</ul>' if items else ""


def _yaml_status(text: str) -> str:
    return (re.search(r"(?m)^status:\s*(\S+)", text or "") or [None, ""])[1]


def status_html(folder: Path, root: Path, level: str, questions: list) -> str:
    """Goal & status: one full-width row per child (Jobs, Tasks or Runs) with its goal, its status and, for
    a Task or a Run, its output in place; then the Questions."""
    rows = []
    if level in {"SPACE", "Folder"}:              # its Projects, under each folder of Projects
        groups = [(None, kids(folder))] if level == "Folder" else [(g, kids(g) if page_level(g) == "Folder" else [g]) for g in kids(folder)]
        for group, projects in groups:
            items = [kid_row(q, root) for q in projects if inside(q, root)]
            rows.append(kid_group(group.name, page_url(group, root), items) if group is not None and page_level(group) == "Folder"
                        else "".join(items))
    elif level in {"Project", "Theme"}:          # a Project lists its Blocks under each Theme; a Theme, its Blocks
        groups = [(th, kids(th)) for th in kids(folder)] if level == "Project" else [(None, kids(folder))]
        for theme, blocks in groups:
            items = [kid_row(b, root) for b in blocks if inside(b, root)]
            rows.append(kid_group(theme.name, page_url(theme, root), items) if theme is not None else "".join(items))
    elif level in {"Block", "Job"}:
        # what this Block or Job asks itself (its own runs/rNN_collect_*), waiting or answered, first: no Job or Task row
        # holds it, so without this line Work would not show it (JL 261031: one record, an entry wherever its work is)
        for r in (r for r in interactions(folder, root) if r["page"] == folder):
            about = (f' · about <a href="{frame.esc(topic_home(r["topic"], root))}">{frame.esc(r["topic"].name)}</a>'
                     if r["topic"] is not None else '')
            rows.append(f'<article class="status-row ix-row"><span class="row-name">{frame.esc(r["title"])}</span>'
                        + (f'<p class="row-line">{about[3:]}</p>' if about else '')
                        + f'<p class="row-meta">{frame.esc(r["run"])}{interaction_button([r], r["path"], root)}</p></article>')
        rows.append(fold_tree(folder, root, level))       # its Jobs, Tasks and Runs as one folding tree (JL 261102)
    elif level == "Task":
        records = {r["path"]: r for r in interactions(folder, root)}
        for run in frame.runs_of(folder):
            path = run["path"]
            if not inside(path, root):
                continue
            badge = interaction_button([records[path]], path, root) if path in records else ""   # a collection Run
            name = (f'<a class="row-name" data-pop="{frame.esc(folder.name)} · {frame.esc(run["run"])}" '
                    f'href="{frame.esc(run_url(path, root))}" target=_blank rel=noopener>{frame.esc(run["run"])}</a>'
                    if path.is_dir() else f'<span class="row-name">{frame.esc(run["run"])}</span>')
            rows.append(f'<article class="status-row">{name}'
                        f'<p class="row-meta">{frame.esc(run["status"])}{badge}</p>'
                        + (output_of(path, root) if path.is_dir() else '') + '</article>')
    body = "".join(rows)
    if questions:
        body += '<h3 class="focus-sub">Questions</h3>' + question_cards(questions, folder, root)
    below = {"SPACE": "Projects", "Folder": "Projects", "Project": "Themes", "Theme": "Blocks", "Block": "Jobs", "Job": "Tasks",
             "Task": "Runs"}.get(level, "pages")
    return body or f'<p class="mut">No {below} yet.</p>'


THEMES = ("work", "paper", "discovery", "cowork", "insight", "design", "labeling", "ideation",   # haipipe-project
          "tasks", "papers", "discoveries", "insights", "designs", "labelings", "ideations")       # and their old names


def page_level(folder: Path) -> str:
    """Project, Theme, Block, Job, Task or Topic (JL 261028: every folder has one page, the Project and its Themes too;
    JL 261029: "studio should have a page as well")."""
    if is_topic(folder):
        return "Topic"
    level = frame.level_of(folder)
    if level:
        return level
    if is_space(folder):
        return "SPACE"
    if frame.is_project(folder):
        return "Project"
    if holds_projects(folder):
        return "Folder"                             # examples-3-nlp/, Tools' blueprints/: a folder of Projects
    if (folder.name in THEMES and frame.is_project(folder.parent)) or holds_blocks(folder):
        return "Theme"                              # work/, paper/, or any folder of Blocks, such as Tools' blueprints/
    return "Block"


def is_space(folder: Path) -> bool:
    """A SPACE: the folder one host serves (its .server_config/), or a <name>-SPACE folder."""
    return (folder / ".server_config").is_dir() or folder.name.endswith("-SPACE")


def holds_projects(folder: Path) -> bool:
    return folder.is_dir() and not folder.name.startswith((".", "_")) and any(
        q.is_dir() and frame.is_project(q) for q in folder.iterdir() if not q.name.startswith((".", "_")))


def holds_blocks(folder: Path) -> bool:
    return folder.is_dir() and any(p.is_dir() and frame.level_of(p) == "Block" for p in folder.iterdir()
                                   if not p.name.startswith((".", "_")))


def kids(folder: Path) -> list:
    """The child pages one level down: a Project's Themes, a Theme's Blocks, a Block's Jobs, a Job's Tasks."""
    level = page_level(folder)
    if level == "SPACE":                            # its folders of Projects, and any Project at its root
        return sorted(q for q in folder.iterdir() if q.is_dir() and not q.name.startswith((".", "_"))
                      and not q.is_symlink() and (holds_projects(q) or frame.is_project(q)))
    if level == "Folder":
        return sorted(q for q in folder.iterdir() if q.is_dir() and not q.name.startswith((".", "_")) and frame.is_project(q))
    if level == "Project":
        return [folder / n for n in THEMES if (folder / n).is_dir()]
    if level == "Theme":
        return sorted(p for p in folder.iterdir() if p.is_dir() and not p.name.startswith((".", "_"))
                      and frame.level_of(p) == "Block")
    return frame.children(folder, level) if level in ("Block", "Job") else []


def rollup(folder: Path) -> list:
    """The pages whose Studio, Delivery and Runs a page shows: itself and everything below it; a SPACE or a folder
    of Projects shows only its own (each Project rolls up its own), so the top page stays fast."""
    return [folder] if page_level(folder) in ("SPACE", "Folder") else descendants(folder)


def descendants(folder: Path) -> list:
    """The page and every page below it, in reading order: a Project, its Themes, Blocks, Jobs and Tasks."""
    out = [folder]
    for child in kids(folder):
        out += descendants(child)
    return out


def origin(source: Path, folder: Path) -> str:
    """Where a rolled-up item lives, below the open page: '' for its own, else 'j02' or 'j02 · t01'."""
    if source == folder or folder not in source.parents:     # its own, or a Block topic hung at this rung
        return ""
    return " · ".join(part.split("_")[0] for part in source.relative_to(folder).parts)


def topic_rows(folder: Path, root: Path, inventory: list | None = None) -> list:
    """The page's own Studio topics, then its children's (frame.studio_inventory), each with where it lives; or the
    (source, topic, drawings) a page type hands in (a draft Task: the Block topics that name it)."""
    rows = []
    sources = rollup(folder) if page_level(folder) in ("SPACE", "Folder", "Project", "Theme") else None
    if inventory is None:
        inventory = ([(s, t, d) for s in sources for t, d in frame._studio_topics(s)] if sources
                     else frame.studio_inventory(folder, root))
    for source, topic, drawings in inventory:
        if not inside(topic, root):
            continue
        notes = frame._notes(topic)
        facts = frame._note_facts(notes) if notes and inside(notes, root) else {"tags": []}
        rows.append((topic, [p for p in drawings if inside(p, root)], {**facts, "origin": origin(source, folder)}))
    return rows


def live_page_blocks(folder: Path) -> list:
    """The Blocks whose live pages can be at this page or below: those it rolls up, and the one above it."""
    blocks = [p for p in rollup(folder) if frame.level_of(p) == "Block"]
    above = frame._block_above(folder)
    return blocks + ([above] if above and above not in blocks else [])


def live_pages_html(folder: Path, root: Path) -> str:
    """A closed card per deliverable with a `url:` at this page or below (frame._live_pages reads the Job's face); opened,
    the page itself in a frame, loaded only then; a page on another host gets only its link."""
    below = rollup(folder)
    cards = []
    for block in live_page_blocks(folder):
        for i in frame._live_pages(block):
            if i["folder"] not in below:
                continue
            url, title = frame.esc(i["url"]), frame.esc(i["title"])
            where = origin(i["folder"], folder)
            frame_ = (f'<iframe title="{title}" data-src="{url}" referrerpolicy=no-referrer '
                      f'style="width:100%;height:85vh;border:1px solid var(--line,#ddd)"></iframe>'
                      if i["url"].startswith("/") else "")
            cards.append(f'<details class=live-page ontoggle="var f=this.querySelector(\'iframe\');'
                         f'if(this.open&&f&&!f.src)f.src=f.dataset.src"><summary><b>{title}</b>'
                         f'{" <span class=mut>" + frame.esc(where) + "</span>" if where else ""} '
                         f'<span class=mut>live page</span> '
                         f'<a href="{url}" target=_blank rel=noopener>own tab ↗</a></summary>{frame_}</details>')
    return f'<section class="delivery-part">{"".join(cards)}</section>' if cards else ""


def delivery_html(folder: Path, root: Path) -> str:
    """The page's live pages (JL 261104: a page a host serves, e.g. the food API's try page, seen and used right here),
    then each level's delivery/, the page's own first, then its children's: its table (delivery.md) or its files."""
    out = [live_pages_html(folder, root)]
    for source in rollup(folder):
        deliv = source / "delivery"
        if not deliv.is_dir() or not inside(deliv, root):
            continue
        where = origin(source, folder) or "this page"
        table = deliv / "delivery.md"
        if table.is_file():
            body = markdown(table.read_text(encoding="utf-8", errors="replace"), deliv, root)
        else:
            files = sorted(p for p in deliv.iterdir() if not p.name.startswith("."))
            body = "<ul>" + "".join(f'<li><a href="{frame.esc(frame._file_url(p, root))}" target=_blank rel=noopener>'
                                    f'{frame.esc(p.name)}</a></li>' for p in files) + "</ul>" if files else '<p class="mut">Empty.</p>'
        out.append(f'<section class="delivery-part"><h3 class="focus-sub">{frame.esc(where)}</h3>{body}</section>')
    return "".join(out)


OTHER = "Other"                                                  # the Studio button for topics in no group


def in_group(facts: dict, group: str) -> bool:
    """A topic belongs to a Studio group button: its **Tags:** name it, or it has none and the button is Other."""
    return not group or (not facts["tags"] if group == OTHER else group in facts["tags"])


def studio_html(rows, root, group, asks=()):
    """One row per topic, four things only (JL 261029: "the information here is a bit overwhelmed"): its picture
    (the lead idea slide, else the drawing's preview), its name (address @ topic), the one line it asks, its stage
    as a word; then Slides, Draw, Mind map. The name opens the face. Rounds, ideas and tags live behind it. `asks` are
    the interactions in reach (card_interactions): each one about a topic shows on its card, the same badge as Work's."""
    out = []
    for topic, drawings, facts in rows:
        if not in_group(facts, group):
            continue
        title = topic.name if topic.is_dir() else topic.stem
        notes = frame._notes(topic)
        face_url = frame.reader(notes, root) if notes and inside(notes, root) else ""
        draw_url = frame._draw_url(drawings[0], root) if drawings else ""
        url = face_url or draw_url                  # no topic page (JL 261031): the name opens the face, popped out
        lead_slide = None
        record = topic / f"{topic.name}.slides.json" if topic.is_dir() else None
        if record and record.is_file():
            try:
                first = json.loads(record.read_text(encoding="utf-8"))["slides"][0]["image"]
                lead_slide = topic / first if (topic / first).is_file() and inside(topic / first, root) else None
            except (ValueError, KeyError, IndexError, TypeError):
                lead_slide = None
        previews = [d.with_suffix(".png") for d in drawings] + ([topic / (topic.name + ".png")] if topic.is_dir() else [])
        preview = lead_slide or next((p for p in previews if p.is_file() and inside(p, root)), None)
        deck = topic / f"{topic.name}.slides.html" if topic.is_dir() else None
        deck_url = "/" + frame.rel(deck, root) if deck and deck.is_file() and inside(deck, root) else ""
        mind = topic / f"{topic.name}.mindmap.md" if topic.is_dir() else None
        verbs = []
        # everything on a row pops out over the page, so a reader previews a topic without leaving it (JL 261029: "I
        # want to make things here to be pop out")
        if deck_url:
            verbs.append(f'<a class="row-verb main" data-pop="{frame.esc(title)} · slide" href="{frame.esc(deck_url)}" target=_blank rel=noopener>'
                         f'{"Slide" if is_topic(topic) else "Slides"}</a>')   # JL 261031: "we might just call it Slide"
        if draw_url:
            verbs.append(f'<a class="row-verb" data-pop="{frame.esc(title)}" href="{frame.esc(draw_url)}" target=_blank rel=noopener>Draw</a>')
        if mind and mind.is_file() and inside(mind, root):
            verbs.append(f'<a class="row-verb" data-pop="{frame.esc(title)} · mind map" href="{frame.esc(frame.ROUTE + "?" + urlencode({"view": "focus-map", "path": frame.rel(mind, root)}))}" target=_blank rel=noopener>Mind map</a>')
        if topic.is_dir() and is_topic(topic) and work_root(topic) is not None:   # the work that makes it (JL 261030)
            verbs.append(f'<a class="row-verb" data-pop="{frame.esc(title)} · work" href="{frame.esc(frame.ROUTE + "?" + urlencode({"view": "focus-part", "part": "work", "path": frame.rel(topic, root)}))}" target=_blank rel=noopener>Work</a>')
        if topic.is_dir() and is_topic(topic) and (topic / "delivery").is_dir():   # what it hands over, popped out (JL 261030)
            verbs.append(f'<a class="row-verb" data-pop="{frame.esc(title)} · delivery" href="{frame.esc(frame.ROUTE + "?" + urlencode({"view": "focus-delivery", "path": frame.rel(topic, root)}))}" target=_blank rel=noopener>Delivery</a>')
        # an interaction about this topic, beside its drawing and mind map (JL 261031: one record, many entries)
        verbs.append(interaction_button([r for r in asks if r["topic"] == topic], topic, root))
        lead, shown = frame.topic_label(topic, facts.get("at", "")) if topic.is_dir() else ("", title)
        name = (f'<a class="row-name" data-pop="{frame.esc(title)}" href="{frame.esc(url)}" target=_blank rel=noopener>'
                f'{frame.esc(shown)}</a>') if url else f'<span class="row-name">{frame.esc(shown)}</span>'
        if lead:                                             # b17.j01-s07:theme_work.tables @ one_table (s01-D03)
            name = f'<span class="row-address">{frame.esc(lead)}</span>' + name
        stage = facts.get("stage") or ""
        if stage:                                            # one word, never the four-step line
            name += f'<span class="row-stage">{frame.esc(stage)}</span>'
        if facts.get("dtype"):                               # what it hands over, beside how far it is
            name += f'<span class="row-type" title="delivery type">{frame.esc(facts["dtype"])}</span>'
        pic_url = deck_url if lead_slide and deck_url else (draw_url or url)   # the picture opens its slide
        picture = (f'<a class="row-thumb" data-pop="{frame.esc(title)}" href="{frame.esc(pic_url)}" target=_blank rel=noopener>'
                   f'<img src="{frame.esc(frame._file_url(preview, root))}" alt="{frame.esc(title)}" loading="lazy"></a>'
                   if preview and pic_url else '<span class="row-thumb none">no picture yet</span>')
        topic_line = facts.get("topic", "")                 # one line: its first sentence
        first = re.match(r"(.+?[.;])(?:\s|$)", topic_line)
        topic_line = first.group(1) if first else topic_line[:200]
        line = (f'<a data-pop="{frame.esc(title)}" href="{frame.esc(url)}" target=_blank rel=noopener>{frame.esc(topic_line)}</a>'
                if url else frame.esc(topic_line))
        out.append(f'<article class="status-row studio-row" id="{frame.esc(topic.name)}"><div><p class="row-title">{name}</p>'
                   + (f'<p class="row-line">{line}</p>' if topic_line else '')
                   + (f'<p class="row-verbs">{"".join(verbs)}</p>' if verbs else '') + f'</div>{picture}</article>')
    return "".join(out) or '<p class="mut">No Studio topics in this section.</p>'


def card_interactions(folder: Path, root: Path) -> list:
    """The interactions a page's Studio cards can be about: those of its Block and below, so a question the Block asks
    about a Job's sNN still shows on that sNN's card on the Job page; above a Block, the page's own and below."""
    block = next((p for p in (folder, *folder.parents) if frame.level_of(p) == "Block"), folder)
    return interactions(block if inside(block, root) else folder, root)


def log_events(text: str) -> list:
    """Only dates written in the current face's Log, never file modification times."""
    events = []
    for line in text.splitlines():
        match = re.match(r"^\s*(?:[-*]\s+)?(\d{4}-\d{2}-\d{2}|\d{6})(?:\s+(\d{4}))?\s*[·:–-]\s*(.+)", line)
        if not match:
            continue
        raw, time, message = match.groups()
        day = f"20{raw[:2]}-{raw[2:4]}-{raw[4:]}" if len(raw) == 6 else raw
        try:
            dt.date.fromisoformat(day)
        except ValueError:
            continue
        events.append((day, time or "", message))
    return sorted(events, key=lambda e: (e[0], e[1]))


TIMELINE_MAX = 120


def timeline_events(folder: Path, root: Path) -> list:
    """What happened when, newest first, from records that already carry a date (JL 261028: a view, never a
    timeline folder): the git commits that touched this folder, each Run's passes and receipt below it, and any
    dated `## Log` line of a face. Each event: (day, kind, words, origin)."""
    events = []
    try:
        out = subprocess.run(["git", "-C", str(folder), "log", f"-{TIMELINE_MAX}", "--format=%cs%x09%s", "--", "."],
                             capture_output=True, text=True, timeout=5)
        for line in out.stdout.splitlines() if out.returncode == 0 else []:
            day, _, words = line.partition("\t")
            events.append((day, "commit", words, ""))
    except (OSError, subprocess.TimeoutExpired):
        pass
    for source in rollup(folder):
        where = origin(source, folder)
        for day, _, message in log_events(read_face(source, root)["sections"].get("log", "")):
            events.append((day, "log", message, where))
        for run in frame.runs_of(source) if (source / "runs").is_dir() else []:
            path = run["path"]
            if not path.is_dir() or not inside(path, root):
                continue
            receipt = path / "result" / "runtime.yaml"
            text = receipt.read_text(encoding="utf-8", errors="ignore") if receipt.is_file() else ""
            done = re.search(r"(?m)^finished_at:\s*'?(\d{4}-\d{2}-\d{2})", text)
            status = re.search(r"(?m)^status:\s*(\S+)", text)
            if done:
                events.append((done.group(1), "run", f"{run['run']} {status.group(1) if status else 'finished'}", where))
            for pdir in sorted((path / "passes").glob("p[0-9]*-[0-9][0-9][0-9][0-9]")) if (path / "passes").is_dir() else []:
                mmdd = pdir.name.split("-")[-1]
                year = (done.group(1)[:4] if done else str(dt.date.today().year))
                note = pdir / "pass.md"                  # what the pass did: its own title line
                title = next((l[2:].strip() for l in note.read_text(encoding="utf-8", errors="ignore").splitlines()
                              if l.startswith("# ")), "") if note.is_file() else ""
                events.append((f"{year}-{mmdd[:2]}-{mmdd[2:]}", "pass",
                               (f"{title} ({run['run']}, {pdir.name.split('-')[0]})" if title else f"{run['run']} · {pdir.name}"), where))
    events.sort(key=lambda e: e[0], reverse=True)
    return events[:TIMELINE_MAX]


KIND_WORDS = {"commit": ("change", "changes"), "run": ("Run finished", "Runs finished"), "pass": ("work session", "work sessions"),
              "log": ("log note", "log notes")}


def kind_count(kinds) -> str:
    """`commit, commit, run` -> `2 changes · 1 Run finished`."""
    from collections import Counter as _C
    c = _C(kinds)
    return " · ".join(f"{n} {KIND_WORDS.get(k, (k, k))[0 if n == 1 else 1]}" for k, n in c.most_common())


def timeline_html(events: list, folder: Path, root: Path) -> str:
    """What was done, newest day first (JL 261029: "there should be something to describe what we have done"): a
    summary of the whole span, then one block per day that says what that day did, then its events in words."""
    if not events:
        return '<p class="mut">Nothing dated below this page yet.</p>'
    days = {}
    for e in events:
        days.setdefault(e[0], []).append(e)
    busiest = sorted(days.items(), key=lambda kv: -len(kv[1]))[:3]
    summary = ('<div class="tl-summary"><p><b>' + frame.esc(kind_count(e[1] for e in events)) + '</b> between '
               + frame.esc(min(days)) + ' and ' + frame.esc(max(days)) + ', on ' + str(len(days)) + ' days.</p>'
               '<p class="mut">Busiest: ' + " · ".join(f"{frame.esc(d)} ({len(es)})" for d, es in busiest) + '</p></div>')
    blocks = []
    for day in sorted(days, reverse=True):
        items = days[day]
        commits = [w for _, k, w, _ in items if k == "commit"]
        lead = commits[0] if commits else items[0][2]          # the day's headline: its first change, else its first event
        rows = "".join(f'<li><span class="tl-kind">{frame.esc(KIND_WORDS.get(k, (k, k))[0])}</span> {frame.esc(w)}'
                       + (f' <span class="tl-where">· {frame.esc(where)}</span>' if where else '') + '</li>'
                       for _, k, w, where in items)
        blocks.append(f'<section class="tl-day" data-day="{frame.esc(day)}"><header><time>{frame.esc(day)}</time>'
                      f'<span class="tl-lead">{frame.esc(lead)}</span><span class="tl-n">{frame.esc(kind_count(k for _, k, _, _ in items))}</span>'
                      f'</header><ul>{rows}</ul></section>')
    return (summary + '<div class="date-range"><label>From <input type="date" data-from></label>'
            '<label>To <input type="date" data-to></label></div><p data-date-message role="status"></p>'
            '<div class="tl-days">' + "".join(blocks) + '</div>')


def folder_html(folder, root, seen=(), depth=0):
    """Show two levels directly; deeper folders link to their own folder page."""
    if not inside(folder, root) or folder.resolve() in seen:
        return ""
    children = sorted(p for p in folder.iterdir() if p.is_dir() and not p.name.startswith(".") and inside(p, root))
    rows = []
    for child in children:
        if depth < 1:
            rows.append(f'<li><span>{frame.esc(child.name)}/</span>'
                        f'{folder_html(child, root, (*seen, folder.resolve()), depth + 1)}</li>')
        else:
            rows.append(f'<li><a href="{frame.esc(page_url(child, root, "folders"))}">{frame.esc(child.name)}/</a></li>')
    return '<ul class="focus-folders">' + "".join(rows) + '</ul>' if rows else '<p class="mut">No subfolders.</p>'


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
        rows, _ = owned_register(read_face(block, root), root, 'Questions', 'questions')
        states = {qid: label for qid, _, label in report_states(rows, block, root)}
        for i, row in enumerate(rows):
            qid = task_questions.words(row.get("id")) or str(i + 1)
            out.append((block, qid, task_questions.words(row.get("title")) or task_questions.words(row.get("question")),
                        states.get(qid, "not answered yet")))
    return out


LEAD = re.compile(r"^(Agreed|Decided|Proposed|A proposal)\b[^:.]*?(?:[:.]\s+|,\s+(?=[a-z]))", re.I)
WAITS = re.compile(r"waiting (?:for|on)|open until|left to|until \w+ settles", re.I)


def first_answer(path: Path) -> tuple:
    """(stage, sentence) of a report's answer (its Opening): the stage is agreed, proposed or draft, read from the
    answer's own lead ("Proposed (261007), waiting for JL: …"), and the sentence is the claim after that lead; empty
    when no answer is written yet."""
    text = path.read_text(encoding="utf-8", errors="replace")
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
        rows, _ = owned_register(read_face(blk, root), root, 'Questions', 'questions')
        for row in rows:
            path = report_path(row, blk, root)
            stage, line = first_answer(path) if path else ("", "")
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


def blocks_view(blocks: list, root: Path) -> str:
    """One line per Block: its name, what it is for, and its count of Questions and topics."""
    rows = []
    for b in blocks:
        qs, _ = owned_register(read_face(b, root), root, 'Questions', 'questions')
        topics = sum(1 for d in descendants(b) for _ in frame._studio_topics(d))
        facts = " · ".join(x for x in (f"{len(qs)} Questions" if qs else "", f"{topics} topics" if topics else "",
                                        f"{len(kids(b))} Jobs" if kids(b) else "") if x)
        rows.append(f'<li><a href="{frame.esc(page_url(b, root))}"><b>{frame.esc(b.name)}</b></a> '
                    f'<span>{frame.esc(one_line(read_face(b, root)["goal"]))}</span>'
                    + (f' <span class="mut">· {frame.esc(facts)}</span>' if facts else '') + '</li>')
    return '<ul class="glance-list">' + "".join(rows) + '</ul>' if rows else '<p class="mut">No Blocks yet.</p>'


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
            qs, _ = owned_register(read_face(b, root), root, 'Questions', 'questions')
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


def blocks_under_projects(folder: Path) -> list:
    """The Projects below a SPACE or a folder of Projects."""
    if page_level(folder) == "Folder":
        return kids(folder)
    return [q for g in kids(folder) for q in (kids(g) if page_level(g) == "Folder" else [g])]


# the one line under a page's title, named for its level (JL 261029: "能不能给这段话这类话起个名字"): a Project's
# mission, what a Theme or Block is for, a Job's goal, a Task's aim (the ladder's words)
GOAL_WORD = {"SPACE": "Mission", "Folder": "Mission", "Project": "Mission", "Theme": "Purpose", "Block": "Purpose",
             "Job": "Goal", "Task": "Aim"}


def band_title(title: str) -> str:
    """A band's name with its first letter raised, past any emoji: "🧠 heads" -> "🧠 Heads". A name whose first letter
    is already a capital stays as written: "WellDoc datasets", "AI-READI"."""
    return re.sub(r"^([^A-Za-z]*)([a-z])", lambda m: m[1] + m[2].upper(), title.strip())


def plural(n: int, one: str, many: str = "") -> str:
    """3, "Job" -> "3 Jobs"; a word that does not just take an s gives its plural."""
    return f"{n} {one if n == 1 else many or one + 's'}"


# what each view shows, one line under the view buttons: the mission above is the page's and the same in every view,
# so the view says what is different (JL 261029)
VIEW_WORDS = {"mindmap": "How it is built, as a map: its parts, and what each must find out.",
              "findings": "What it has found so far, in the answers' own words, and what waits for you.",
              "themes": "What each Block is for, Theme by Theme.",
              "status": "How far each Block has got.",
              "standing": "Where its Jobs, Tasks and sNN stand.",
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
            words = f"{stages['answered']} of {total} answered" + "".join(
                f" · {stages[k]} {k}" for k in ("draft", "open") if stages[k])
        else:
            bar, words = '<span class="stat-bar" aria-hidden="true"></span>', "nothing to find out written yet"
        if tasks:
            words += f" · {plural(len(tasks), 'Task')}"
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


# ── HOOK: a draft Task (b32 s42-draft-task-focus-page) ─────────────────────────────────────────────────────────────
# A Task whose face says `task-type: draft` (a paper Section, the Abstract, a letter) fills Report, Work, Studio and
# Delivery from workbench-task-draft/focus_draft.py, its one owner; this page only asks it (`draft_parts`), the way
# frame.task_card asks a layout's work_card. Everything draft-specific lives there.
def is_draft(folder: Path) -> bool:
    return page_level(folder) == "Task" and frame.task_type(folder) == "draft"


def draft_parts(folder: Path, root: Path) -> dict:
    """The draft Task's parts (focus_draft.parts), or {} for any other page or a draft that does not read."""
    if not is_draft(folder):
        return {}
    try:
        from live import focus_draft
        return focus_draft.parts(folder, root, lambda section, group="": page_url(folder, root, section, group))
    except Exception:                                   # a half-made draft never breaks the page
        return {}


def draft_branches(folder: Path, root: Path) -> list:
    try:
        from live import focus_draft
        return focus_draft.branches(folder, root)
    except Exception:
        return []
def paper_delivery(folder: Path, root: Path) -> str:
    """A paper version's Delivery (its assembled paper, then its Sections) or a Board's (each version's paper), from the
    Board's delivery/<version>/build-manifest.json; "" for any other page (paper_version.paper_delivery)."""
    if page_level(folder) not in ("Job", "Block"):
        return ""
    try:
        from live import paper_version
        return paper_version.paper_delivery(folder, root)
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (b16 review 261101)
        return ""
def paper_look() -> dict:
    """A paper version page's look, the same as a draft Task's: width, section verbs, view captions (focus_draft)."""
    try:
        from live import focus_draft
        from live import board_read, board_views, paper_version  # noqa: F401  (the last two fill board_read.PAPER_CAPTIONS)
        common = re.sub(r"\.focus-(?:page|rail)[^\n]*--fd-w[^\n]*\n", "",           # the common width, like every page
                        focus_draft.WIDE.replace(":root{--fd-w:min(1480px,calc(100vw - 32px))}", ""))   # (JL 261031, b10 r01 Q2)
        return {"css": common + board_views.PAGE_CSS + focus_draft.borrowed_css() + focus_draft.JS, "verbs": focus_draft.SECTION_VERBS,
                "captions": {**focus_draft.CAPTIONS, **board_read.PAPER_CAPTIONS}}
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (b16 review 261101)
        return {}


def paper_delivery_views(folder: Path, root: Path) -> dict:
    """A paper version's Delivery views, Paper · Word · Supplement · Files (paper_version.version_delivery_views); {} else."""
    if page_level(folder) != "Job":
        return {}
    try:
        from live import paper_version
        return paper_version.version_delivery_views(folder, root)
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (b16 review 261101)
        return {}
def paper_board_report(folder: Path, root: Path) -> dict:
    """A paper Board's own parts as Report views, Idea · Story · Venue · Data flow · Paper flow · Related work
    (board_views.board_report_views; JL 261031); {} for any other page."""
    if page_level(folder) != "Block":
        return {}
    try:
        from live import board_views
        # Interactions and the mind map are sections inside each part's view, not views (JL 261031)
        return board_views.board_report_views(folder, root, lambda text, base: markdown(text, base, root),
                                              interactions(folder, root))
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (b16 review 261101)
        return {}
def paper_board_work(folder: Path, root: Path, versions: str) -> dict:
    """A paper Board's Work: the Report's view list, each part's work (board_views.board_work_views; JL 261031: "the
    work and report should share the same view list"); Draft holds `versions`, the base Job-Versions rows. {} else."""
    if page_level(folder) != "Block":
        return {}
    try:
        from live import board_views
        return board_views.board_work_views(folder, root, lambda text, base: markdown(text, base, root), versions,
                                            interactions(folder, root), lambda r: interaction_item(r, folder, root))
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (b16 review 261101)
        return {}
def paper_version_work(folder: Path, root: Path) -> dict:
    """A paper version's Work: Draft-Main · Draft-Appendix · Display-Main · Display-Appendix (focus_draft; JL 261031,
    s36-D01, D02); {} for any other page."""
    if page_level(folder) != "Job":
        return {}
    try:
        from live import paper_version
        return paper_version.version_work_views(folder, root, interactions(folder, root), lambda r: interaction_item(r, folder, root))
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (b16 review 261101)
        return {}
def insight_job_work(folder: Path, root: Path) -> dict:
    """An insight Job's Work: Overall · Grid · vs previous · The pair, each ⚙️ Process then 📊 Results, your signs first
    (insight_focus.job_work_views; b11 j01 s55, JL 261101); {} for any other page."""
    if page_level(folder) != "Job":
        return {}
    try:
        from live import insight_focus
        return insight_focus.job_work_views(folder, root, interactions(folder, root), lambda r: interaction_item(r, folder, root))
    except Exception:
        traceback.print_exc()   # in the server log, not hidden
        return {}
def insight_board_report(folder: Path, root: Path) -> dict:
    """An insight Board's Report: Answers · Questions · Jobs · Data · Handoff, numbered sections only
    (insight_focus.board_report_views; b11 j01 s51, JL 261101); {} for any other page."""
    if page_level(folder) != "Block":
        return {}
    try:
        from live import insight_focus
        return insight_focus.board_report_views(folder, root)
    except Exception:
        traceback.print_exc()   # in the server log, not hidden
        return {}
def insight_views_for(folder: Path, root: Path, section: str) -> dict:
    """An insight Board's Work, a Job's Report, a Task's Report or Work, in the b11 j01 letters (insight_focus; s52,
    s54, s57, s58, JL 261102); {} for any other page."""
    try:
        from live import insight_focus as IF
        level = page_level(folder)
        if level == "Block" and section == "work":
            return IF.board_work_views(folder, root, interactions(folder, root), lambda r: interaction_item(r, folder, root))
        if level == "Job" and section == "report":
            return IF.job_report_views(folder, root)
        if level == "Task":
            return IF.task_views(folder, root, section)
    except Exception:
        traceback.print_exc()   # in the server log, not hidden
    return {}
def design_views(folder: Path, root: Path, section: str) -> dict:
    """A design Block's, Job's or Task's Report or Work in the j01 letters (design_focus.views; b12 j01 s51 to s58,
    JL 261101); {} for any other page."""
    try:
        from live import design_focus
        return design_focus.views(folder, root, section)
    except Exception:
        traceback.print_exc()   # in the server log, not hidden
        return {}
# ── end HOOK ─────────────────────────────────────────────────────────────────────────────────────────────────────


ANSWER_PILL = {"agreed": "✅ answer agreed", "proposed": "🙋 answer: your call", "draft": "🔶 answer not final",
               "": "⬜ no answer yet"}                     # first_answer's stage, said so a reader need not ask
LADDER_NAME = re.compile(r'<span class=(pm-role|pm-id)([^>]*)>([jts]\d+)([_-][^<]*)</span>')


def parts_mindmap(folder: Path, root: Path) -> str:
    """A Block's, a Job's or a Task's own mind map (JL 261029: "WE SHOULD HAVE THE MINIMAP AS WELL"): its Questions, each
    with how far its answer has got, its Jobs with their Tasks, its Tasks with their Runs, its topics."""
    mm_ = frame.mindmap_module()
    import mmbuild, mmtree
    level, branches = page_level(folder), []
    rows, _ = owned_register(read_face(folder, root), root, 'Questions', 'questions')
    if rows:
        points = []
        for i, row in enumerate(rows):
            path = report_path(row, folder, root)
            stage, line = first_answer(path) if path else ("", "")
            asked = task_questions.words(row.get("question")) or task_questions.words(row.get("title"))
            # the question itself, and on a Block its ↗ opens the report; the answer's words stay there and on Findings
            # (JL 261103: "what does this mean?" of "To find out" and "draft"; too many words)
            words = f"[{asked}]({frame.reader(path, root)})" if path and level == "Block" else asked
            points.append(mmbuild.built(f"{folder}/q{i}", f"[{ANSWER_PILL.get(stage, ANSWER_PILL[''])}] {words}", [],
                                        [line] if line and level != "Block" else []))
        branches.append(mmbuild.built(f"{folder}/find", "Questions", points))

    def runs(task):                                   # as Status's tree: its mark, its name, its headline behind ▸
        return [mmbuild.built(f"{task}/{r.name}", f"[{mark}] [{r.name}]({run_url(r, root)})", [], [head] if head else [])
                for r, mark, head in run_rows(task)]

    # Each sNN hangs on the rung its **At:** names, beside the Jobs, never under a "Studio" node (JL 261029: "each sNN
    # should be just below bNN"); a Block's own topics sit in their groups, its leaves its open questions.
    block = {"Block": folder, "Job": folder.parent, "Task": folder.parent.parent}.get(level, folder)
    shelf = [t for t, _ in frame._studio_topics(block) if t.is_dir() and frame._notes(t) is not None]   # with a face,
    drawn = {}                                                            # as is_topic(); a bare folder took b11 down

    def rung(f):
        return ".".join(p.name.split("_")[0] for p in [f.parent, f][2 - len(f.relative_to(block).parts):]) if f != block else ""

    def topic_nodes(at):
        out = []
        for t in shelf:
            facts = frame._note_facts(frame._notes(t))
            if facts["at"] != at:
                continue
            face = frame._notes(t).read_text(encoding="utf-8", errors="ignore")
            asks = re.findall(r"(?m)^\d+\.\s+(.+)$", part(face_parts(face), "open"))
            # one short line, shown whole: the topic's own question, its title (JL 261030: "make this to be short and
            # fully presented"); its open questions are no leaves here ("should we delete this? no one will read this")
            first = face.splitlines()[0] if face.strip() else ""
            title = first.split(" · ", 1)[1].strip() if " · " in first else ""
            words = re.sub(r"[\[\]]", "", title or first_sentence(facts["topic"]))
            # its box: why, what it delivers, what is still open ("the short paragraphs", JL 261030), as one plain
            # paragraph, the way the draft Task's map shows a sentence (b32 s42; JL 261031)
            plain = lambda s: re.sub(r"\s*\(JL [^)]*\)", "", s).strip().rstrip(".")
            whole = lambda s, n=160: (lambda t: t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…")(" ".join(s.split()))
            gives = re.search(r"(?m)^\*\*For:\*\*\s*(.+)$", face)
            said = ([one_line(plain(first_sentence(facts["topic"])), 160)] if facts["topic"] else []) \
                + ([f"Delivers {one_line(plain(gives.group(1)), 160)}"] if gives else []) \
                + ([f"Still open: {whole(plain(asks[0]))}"] if asks else [])     # a question whole, never cut at its colon
            # each piece one sentence, its own mark kept: "Still open: Is it the right level?" never "level?." (261031)
            said = [s[:1].upper() + s[1:] + ("" if s[-1:] in ".?!" else ".") for s in said if s]
            note = [" ".join(said)] if said else []
            if (t / f"{t.name}.excalidraw").is_file():           # its quick drawing (quick_draw.py), opened from its label
                drawn[t.name] = frame._draw_url(t / f"{t.name}.excalidraw", root, edit=True)
            if at and level == "Block":                          # a Job's drawing in the Block's map: its name only;
                note, words = [], "the Job as one drawing"        # its Job's node already says what it is (JL 261103)
            out.append(((facts["tags"][:1] or [""])[0], mmbuild.built(str(t), f"[{t.name}] {words}", [], note)))
        return out

    def grouped(at):
        """The rung's topics; a Block's in one node per group (studio/_groups.txt order) when it has two or more."""
        nodes = topic_nodes(at)
        names = list(dict.fromkeys(g for g, _ in nodes))
        if at or len(names) < 2:
            return [n for _, n in nodes]
        order = frame.studio_group_order(block)
        names.sort(key=lambda g: (order.index(g) if g in order else len(order), g == ""))
        return [mmbuild.built(f"{block}/group/{g or 'untagged'}", g or 'Untagged',
                              [n for x, n in nodes if x == g]) for g in names]

    def short(f, label_len):
        """A Job's or Task's own title, whole (as a topic's line, JL 261030: "short and fully presented"); else its goal."""
        face = f / f"{f.name}.md"
        first = face.read_text(encoding="utf-8", errors="ignore").split("\n", 1)[0] if face.is_file() else ""
        return (first.split(" · ", 1)[1].strip() if " · " in first else one_line(read_face(f, root)["goal"], label_len)) \
            or f.name.split("_", 1)[-1].replace("_", " ")     # its label shows only "j61", so it always has words

    def task_node(t, label_len, with_runs):
        title, goal = short(t, label_len), one_line(read_face(t, root)["goal"], 200)
        return mmbuild.built(str(t), f"[{t.name}] {title}", grouped(rung(t)) + (runs(t) if with_runs else []),
                             [goal] if goal and goal != title and level != "Block" else [])  # a Block's map: names only (261103)
    branches += grouped(rung(folder))
    if level == "Block" and kids(folder):
        def family_nodes(j):                              # same-shaped Tasks as one node each family (JL 261103)
            out = []
            for key, members, values in task_families(kids(j)):
                if key is None:
                    out.append(task_node(members[0], 70, False))
                else:
                    name, words = family_words(key, members, values)
                    out.append(mmbuild.built(f"{j}/family/{key}", f"{name}: {words}"))
            return out
        # a face's `bands:` groups the Jobs as a Block's topics group, in the same cards, so 15 Jobs read as 5 lines of
        # work (JL 261104: "一眼就能看出来这东西是干啥的"; b35 with 6 cards is the height to match)
        face_text = frame.face(folder).read_text(encoding="utf-8", errors="ignore") if frame.face(folder) else ""
        bands_line = re.search(r"(?m)^bands:\s*(.+)$", face_text)
        named = dict(re.findall(r"\bj(\d)N\s+([^·\n]+)", bands_line.group(1))) if bands_line else {}
        jobs = kids(folder)
        if named and all(re.match(r"j\d\d_", j.name) and j.name[1] in named for j in jobs):
            for b, title in named.items():
                js = [j for j in jobs if j.name[:2] == f"j{b}"]
                if js:
                    branches.append(mmbuild.built(f"{folder}/band/{b}", band_title(title),
                                                  [mmbuild.built(str(j), f"[{j.name}] {job_short(j, js, root)}", grouped(rung(j)) + family_nodes(j)) for j in js]))
        else:
            branches += [mmbuild.built(str(j), f"[{j.name}] {short(j, 80)}", grouped(rung(j)) + family_nodes(j))
                         for j in jobs]
    if level == "Job" and kids(folder):
        for key, members, values in task_families(kids(folder)):
            if key is None:
                branches.append(task_node(members[0], 80, True))
            else:
                name, words = family_words(key, members, values)
                branches.append(mmbuild.built(f"{folder}/family/{key}", f"{name}: {words}",
                                              [task_node(t, 80, False) for t in members]))
    if level == "Task" and is_draft(folder):          # HOOK: a Section's map is its paper content, only (JL 261031:
        branches = draft_branches(folder, root)       # "I think the mindmap here should be the paper content")
        drawn = {}
    if level == "Task" and frame.runs_of(folder) and not is_draft(folder):
        branches.append(mmbuild.built(f"{folder}/runs", "Runs", runs(folder)))
    if not branches:
        return '<p class="mut">Nothing to map yet.</p>'
    rootnode = mmbuild.built(".", folder.name, branches)
    rootnode.id = "root"
    tree = mmtree.MindMap({"mindmap": "1", "title": folder.name, "built": "focus-page"}, rootnode)
    html = mm_.draw(tree, "", editable=False)
    for name, url in drawn.items():                          # the label itself opens the drawing (JL 261029: "this should be in the label")
        html = re.sub(rf'<span class=(pm-role|pm-id)[^>]*>{re.escape(name)}</span>',
                      lambda m: f'<a class="{m.group(1)} pm-open pm-draw" data-pop="{frame.esc(name)}" href="{frame.esc(url)}" '
                                f'title="{frame.esc(name)}: open its quick drawing">✎ {frame.esc(name.split("-")[0])}</a>', html)
    # a label is its number, its full folder name on hover: the long names ran past their card and said the title twice
    # (JL 261104: "here is display are not the best yet")
    html = LADDER_NAME.sub(lambda m: f'<span class={m.group(1)}{m.group(2)} title="{m.group(3)}{m.group(4)}">{m.group(3)}</span>', html)
    if level == "Block":                                     # a question wraps beside its pill, its ↗ never past the box
        html = html.replace(f'<div class=pm-para data-p="{frame.esc(f"@{folder}/find")}">',
                            f'<div class="pm-para pm-questions" data-p="{frame.esc(f"@{folder}/find")}">')
    # each box wraps inside its own edge, never past it (a list item's nowrap no longer leaks in)
    return ('<style>.focus-map .pm-folds{grid-template-columns:170px auto;gap:0 40px}.focus-map .pm-folds .pm-root b{font-size:15px;overflow-wrap:anywhere}'
            '.focus-map .pm-folds .pm-para{grid-template-columns:240px auto;gap:0 36px;margin:2px 0}'   # closed: a Job's title in two lines
            '.focus-map .pm-questions .pm-leaves li{display:flex;align-items:baseline;max-width:340px!important;'
            'white-space:normal!important}'                  # past the page's own !important "a point never wraps"
            '.focus-map .pm-questions .pm-role{flex:none}'
            '.focus-map .pm-id{overflow-wrap:anywhere}.focus-map .pm-detail{max-width:380px}.focus-map .pm-detail,'
            '.focus-map .pm-detail *{white-space:normal}</style><div class="focus-map">' + html + '</div>')


def mindmap_view(folder: Path, root: Path) -> str:
    """The page as a mind map, drawn by haipipe-mindmap's own renderer (the Studio maps' look), in the ladder's order
    (JL 261029: "先给 theme 然后再给 block"): the page, its Themes, each Theme's Blocks with their goal, and under each
    Block what it must find out, its Jobs and its topic count."""
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
            under = [mmbuild.built(f"{b}/q{i}", "[find out] " + (task_questions.words(r.get("title"))
                                                                 or task_questions.words(r.get("question"))))
                     for i, r in enumerate(qs)]
            under += [mmbuild.built(f"{b}/{j.name}", f"[Job] {j.name}") for j in kids(b)]
            topics = sum(1 for d in descendants(b) for _ in frame._studio_topics(d))
            if topics:
                under.append(mmbuild.built(f"{b}/topics", f"[Studio] {topics} topics"))
            goal = one_line(read_face(b, root)['goal'], 70)
            # the Block's name is its label pill (JL 261029), as `[find out]` is a line's (a pill holds 64 characters)
            points.append(mmbuild.built(str(b), f"[{b.name}] {goal}", under))
        branches.append(mmbuild.built(str(th), label, points))
    rootnode = mmbuild.built(".", f"{folder.name}", branches)
    rootnode.id = "root"
    tree = mmtree.MindMap({"mindmap": "1", "title": folder.name, "built": "focus-page"}, rootnode)
    return '<div class="focus-map">' + mm_.draw(tree, "", editable=False) + '</div>'


def questions_list(qs: list, root: Path) -> str:
    return '<ul class="glance-list">' + "".join(
        f'<li><a href="{frame.esc(page_url(b, root, "report"))}"><b>{frame.esc(b.name)} · {frame.esc(q)}</b></a> '
        f'<span>{frame.esc(title)}</span> <span class="mut">· {frame.esc(state)}</span></li>' for b, q, title, state in qs) + '</ul>'


STAGE_MARK = {"explore": "⬜", "shaping": "⏳", "agreed": "✅", "closed": "✅"}


def face_title(face: Path) -> str:
    """A face's own short title, the words after ' · ' on its first line."""
    first = face.read_text(encoding="utf-8", errors="ignore").split("\n", 1)[0] if face.is_file() else ""
    return first.split(" · ", 1)[1].strip() if " · " in first else ""


def state_words(label: str) -> str:
    """`✅ CLOSED` -> `✅ closed`; no recorded state -> `⬜ no state`."""
    mark = re.match(r"^([^A-Za-z0-9]*)(.*)$", label or "")
    return f"{mark.group(1).strip()} {mark.group(2).strip().lower()}".strip() if label else "⬜ no state"


BAND_CSS = """<style>
.band-sec{margin:0 0 8px}
.band-sec>summary{display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px;list-style:none;cursor:pointer;font-size:15px;font-weight:600;
 border:1px solid var(--line);border-radius:8px;background:var(--paper);padding:8px 14px}
.band-sec>summary::-webkit-details-marker{display:none}
.band-sec>summary::before{content:"▸";flex:none;width:12px;color:var(--muted);font-size:12px}.band-sec[open]>summary::before{content:"▾"}
.band-sec>summary:hover{color:var(--accent)}
.band-sec .bar{flex:0 0 120px;height:5px;border-radius:3px;background:var(--wash);overflow:hidden}
.band-sec .bar i{display:block;height:100%;background:#2b8a3e}.band-sec .bar i.part{background:#e8590c}
.band-sec .word,.job-row small{flex:none;margin-left:auto;font-size:12px;font-weight:400;color:var(--muted);text-align:right}
.band-jobs{padding:6px 0 4px 14px}
.job-row{border-bottom:1px solid var(--line)}.job-row:last-child{border-bottom:0}
.job-row>summary{display:flex;align-items:center;gap:8px;list-style:none;cursor:pointer;padding:7px 15px 7px 2px;font-size:14px}
.job-row>summary::-webkit-details-marker{display:none}
.job-row>summary::before{content:"▸";flex:none;width:12px;color:var(--muted);font-size:11px}.job-row[open]>summary::before{content:"▾"}
.job-row .jn{flex:none;font-size:12px;color:var(--muted)}.job-row b{font-weight:600;overflow-wrap:anywhere}
.job-row .bar{flex:0 0 120px;height:5px;border-radius:3px;background:var(--wash);overflow:hidden}
.job-row .bar i{display:block;height:100%;background:#2b8a3e}.job-row .bar i.part{background:#e8590c}
.job-tree{padding:0 0 8px 20px}
@media (max-width:600px){.band-sec .bar{flex-basis:70px}.job-row>summary{flex-wrap:wrap}.job-row .bar{flex-basis:70px}}
</style>"""


FINDINGS_CSS = """<style>
.find-q{padding:10px 2px;border-bottom:1px solid var(--line)}.find-q:last-child{border-bottom:0}
.find-h{display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px;font-size:14px}.find-h b{font-weight:600;overflow-wrap:anywhere}
.find-h .find-open{margin-left:auto;font-size:12px}
.find-pill{flex:none;font-size:12px;border:1px solid var(--line);border-radius:6px;padding:1px 8px;background:var(--wash);color:var(--muted);white-space:nowrap}
.find-pill.agreed{border-color:#2b8a3e;color:#2b8a3e}.find-pill.proposed{border-color:#e8590c;color:#c2410c}
.find-ask{margin:6px 0 0;font-size:13px;color:var(--muted)}.find-sub{margin:12px 0 0;font-size:13px;font-weight:600}.find-verbs{margin:0 0 10px}
.find-map{display:block;width:100%;height:60vh;border:1px solid var(--line);border-radius:8px}
.find-a{margin:6px 0 0;font-size:14px;line-height:1.5}
.find-r{margin:6px 0 0;padding:0 0 0 18px;font-size:13px;line-height:1.5}.find-r li{margin:3px 0}.find-r small{color:var(--muted)}
.find-more{margin-top:4px;font-size:13px}.find-more>summary{cursor:pointer;color:var(--muted)}
.wk-rows{list-style:none;margin:0;padding:0;font-size:14px}.wk-rows li{display:flex;flex-wrap:wrap;gap:4px 10px;padding:6px 2px;border-bottom:1px solid var(--line)}
.wk-rows li:last-child{border-bottom:0}.wk-rows small{margin-left:auto;font-size:12px;color:var(--muted)}
.wk-band{display:flex;align-items:center;gap:12px;margin:22px 0 10px;font-size:17px;font-weight:600}.wk-band:first-child{margin-top:6px}
.wk-band::after{content:"";flex:1;border-top:1px solid var(--line)}
</style>"""
FOUND_STAGE = {"agreed": "answered", "partial": "partly answered", "proposed": "proposed, waiting for you", "draft": "draft", "": "no answer yet"}


def task_reading(folder: Path, root: Path) -> str:
    """The first thing a Task's or Job's own reading of its results says: the first line of its `## Content` that holds
    a result, without the line naming the Run; empty when it has written none."""
    body = re.sub(r"<!--.*?-->", "", read_face(folder, root)["sections"].get("content", ""), flags=re.S)
    for raw in body.splitlines():
        line = re.sub(r"\s+", " ", re.sub(r"\*\*|`|^\s*(?:[-*]|\d+\.)\s+|^#+\s+", "", raw)).strip()
        if line and not line.startswith(("|", "[", "!", "Reading of run")):
            return line
    return ""


def work_paths(row: dict, folder: Path, root: Path) -> list:
    """The folders a Question names under `work:`."""
    out = []
    for item in row.get("work") if isinstance(row.get("work"), list) else []:
        ref = item if isinstance(item, str) else task_questions.words(item.get("path")) if isinstance(item, dict) else ""
        path = (folder / ref).resolve() if ref else None
        if path and inside(path, root) and path.is_dir():
            out.append(path)
    return out


def answer_state(path) -> tuple:
    """(stage, sentence) of a report's answer: its own lead first (agreed, proposed), else its `answer-status:` field,
    so an answer with no lead reads "answered" or "partly answered" and not "draft"."""
    stage, answer = first_answer(path) if path else ("", "")
    if stage == "draft":
        status = (task_questions.field(path.read_text(encoding="utf-8", errors="replace"), "answer-status") or "").lower()
        stage = "agreed" if status == "answered" else "partial" if status.startswith("partial") else stage
    return stage, answer


def finding_item(row: dict, folder: Path, root: Path) -> tuple:
    """(tab name, its line, its panel, stage) of one Question: on the left its name and answer state; on the right what
    it asks, its answer's words, then what its work has found."""
    path = report_path(row, folder, root)
    stage, answer = answer_state(path)
    title = task_questions.words(row.get("title")) or task_questions.words(row.get("question"))
    asked = task_questions.words(row.get("question"))
    results = []
    for w in work_paths(row, folder, root):
        said = task_reading(w, root)
        if said:
            name = f"{w.parent.name[:3]} {w.name[:3]}" if page_level(w) == "Task" else w.name[:3]
            results.append(f'<li><a href="{frame.esc(page_url(w, root))}" data-pop="{frame.esc(w.name)}" title="{frame.esc(w.name)}">'
                           f'{frame.esc(name)}</a> {frame.esc(said)}</li>')
    word = FOUND_STAGE.get(stage, stage)
    html = (f'<div class=find-h><b>{frame.esc(title)}</b><span class="find-pill {stage}">{frame.esc(word)}</span>'
            + (f'<span class=find-open>{frame.pop(frame.reader(path, root), title, "Read full report ↗")}</span>' if path else '') + '</div>')
    if asked and asked != title:
        html += f'<p class=find-ask>{frame.esc(asked)}</p>'
    if answer:
        html += f'<p class=find-a>{frame.esc(answer)}</p>'
    if results:
        html += '<h4 class=find-sub>What its work found</h4><ul class=find-r>' + "".join(results[:8]) + '</ul>'
    if results[8:]:
        html += (f'<details class=find-more><summary>{len(results) - 8} more</summary><ul class=find-r>' + "".join(results[8:]) + '</ul></details>')
    if not answer and not results:
        html += '<p class="find-a mut">Nothing read from its work yet.</p>'
    return title, word, html, stage


DELIVERY_LANES = (("Models", ("model", "models", "checkpoint", "checkpoints"), "a model it hands over"),
                  ("Data", ("data", "dataset", "datasets"), "a dataset it hands over"),
                  ("Website", ("web", "website", "site"), "a site or page it hands over"))


def delivery_tabs(folder: Path, root: Path) -> list:
    """[(tab, line, panel)]: what a Block hands over, by kind (JL 261104: "in case we will delivery some models or data or
    website"), each tab always there and saying where its files go; then every file, when there are any. A lane is
    delivery/<lane>/, or the same under a Job's or a Task's address (haipipe-delivery)."""
    delivs = [d for d in (x / "delivery" for x in rollup(folder)) if d.is_dir() and inside(d, root)]
    tabs = []
    for name, words, what in DELIVERY_LANES:
        rows = []
        for deliv in delivs:
            for lane in [p for pat in ("*", "j[0-9]*/*", "j[0-9]*/t[0-9]*/*") for p in sorted(deliv.glob(pat))]:
                if lane.is_dir() and lane.name.lower() in words:
                    where = lane.parent.relative_to(deliv).as_posix()
                    rows += [f'<li><a href="{frame.esc(frame._file_url(q, root))}" target=_blank rel=noopener>{frame.esc(q.name)}</a>'
                             + (f' <small>{frame.esc(where)}</small>' if where != "." else "") + '</li>'
                             for q in sorted(lane.iterdir()) if not q.name.startswith(".")]
        live = live_pages_html(folder, root) if name == "Website" else ""
        panel = live + (f'<ul class=find-r>{"".join(rows)}</ul>' if rows else "")
        tabs.append((name, "ready" if panel else "nothing yet", panel or (
            f'<p class=mut>Nothing handed over yet. When there is {what}, its clean version goes in '
            f'<code>delivery/{words[0] if name != "Website" else "web"}/</code>, and shows here.</p>')))
    if any(p for d in delivs for p in d.iterdir() if not p.name.startswith(".")):
        tabs.append(("All files", "everything in delivery/", delivery_html(folder, root)))
    return tabs


def value_sections(folder: Path, root: Path) -> list:
    """[(title, html)] of the raw tables of a Block's Jobs that hold a tables.json: the paper's Values tabs, the same code."""
    try:
        from live import board_evidence as be
    except Exception:
        return []
    out = []
    jobs = [j for j in frame.children(folder, "Block") if inside(j, root)]
    for k, job in enumerate(j for j in jobs if next(j.glob("t[0-9]*_*/runs/r[0-9]*/result/tables.json"), None)):
        try:
            tabs = be.value_tabs(job, root)
        except Exception:
            continue
        if tabs:
            out.append(("🔢 Values", f'<div class=find-verbs>{frame._link(page_url(job, root), "Open " + job.name)}</div>' + be.VALUES_CSS
                        + _side_tabs(f"fV{k}x", [(h, w) for h, w, _ in tabs], [p for _, _, p in tabs]) + be.VALUES_DIALOG + be.VALUES_JS))
    return out


def service_section(folder: Path, root: Path) -> str:
    """Findings' 🌐 Service (JL 261104: "a new section named service, and each tab is a website, embedded there"): a side
    tab per live page at this page or below, the site itself on the right, working; a frame loads when its tab first
    shows, so a closed section costs nothing."""
    below = rollup(folder)
    pages = [i for block in live_page_blocks(folder) for i in frame._live_pages(block) if i["folder"] in below]
    if not pages:
        return ""
    panels = []
    for i in pages:
        url, name = frame.esc(i["url"]), frame.esc(i["service"])
        site = (f'<iframe title="{name}" data-src="{url}" referrerpolicy=no-referrer '
                f'style="width:100%;height:80vh;border:1px solid var(--line,#ddd);border-radius:6px"></iframe>'
                if i["url"].startswith("/") else "")
        panels.append(f'<div class=find-verbs><a href="{url}" target=_blank rel=noopener>Own tab ↗</a></div>{site}')
    script = ("<script>(function(){var w=document.getElementById('find-service'),s=w.closest('details');"
              "function load(){if(s.open)w.querySelectorAll('.pb-panel:not([hidden]) iframe[data-src]:not([src])')"
              ".forEach(function(f){f.src=f.dataset.src})}"
              "s.addEventListener('toggle',load);w.addEventListener('click',function(){setTimeout(load)});load()})()</script>")
    return ('<div id=find-service>' + _side_tabs("fSx", [(i["service"], i["title"]) for i in pages], panels)
            + '</div>' + script)


def map_sections(folder: Path, root: Path) -> list:
    """[(title, html)] of the mind maps a Task's newest Run built in result/maps/ (JL 261104: "for each type of Source Table
    Name, we should have the mindmap of them"), one side tab per map, in the order of the Task's Values tabs when it has
    them. Each map is its own framed page, loaded when its tab first shows, its nodes closed."""
    out = []
    for k, task in enumerate(t for j in frame.children(folder, "Block") if inside(j, root) for t in frame.children(j, "Job") if inside(t, root)):
        found = sorted(task.glob("runs/*/result/maps"))
        maps = sorted(found[-1].glob("*.mindmap.md")) if found else []
        if not maps:
            continue
        order = []
        for tables in reversed(sorted(task.glob("runs/*/result/tables.json"))):
            try:
                order = [t.get("title") for t in json.loads(tables.read_text(encoding="utf-8"))["tabs"]]
            except (ValueError, KeyError, AttributeError):
                continue
            break
        name = lambda m: m.name[: -len(".mindmap.md")]
        maps.sort(key=lambda m: order.index(name(m)) if name(m) in order else len(order))
        tabs, panels = [], []
        for m in maps:
            text = m.read_text(encoding="utf-8", errors="replace").split("\n# ", 1)[-1].split("\n")[1:]
            line = next((x.strip() for x in text if x.strip() and not x.startswith("- ")), "its columns")
            href = frame.ROUTE + "?" + urlencode({"path": frame.rel(m, root), "view": "focus-map"})
            tabs.append((name(m), line))
            panels.append(f'<div class=find-verbs>{frame.pop(href, name(m) + " · mind map", "Enlarge map ↗")}</div>'
                          f'<iframe class=find-map loading=lazy title="{frame.esc(name(m))} mind map" src="{frame.esc(href)}&amp;fit=1"></iframe>')
        out.append(("🧠 Maps", _side_tabs(f"fM{k}x", tabs, panels)))
    return out


def findings_board(rows: list, folder: Path, root: Path, lead: str = "") -> str:
    """A Block's Findings: a quick overview of the results it got and what it hands over (JL 261104: "the quick overview
    of the results we get from that block"; "we want things like this, left tab panel right content"; Delivery folded
    in), shaped like a paper Board's Evidence: numbered closed sections, each a side tab per item. Values first, then the
    Questions by their `group:` (one section when they have fewer than two groups), then 🌐 Service when it has a live
    page, then 🧠 Maps, then 📦 Delivery."""
    groups = {}
    for row in rows:
        groups.setdefault(task_questions.words(row.get("group")) or "Other", []).append(row)
    if len(groups) < 2:
        groups = {"Answers": rows} if rows else {}
    secs = [(title, "", body) for title, body in value_sections(folder, root)]
    for g, (name, members) in enumerate(groups.items()):
        items = [finding_item(r, folder, root) for r in members]
        stages = [x[3] for x in items]
        word = ("answered" if all(x == "agreed" for x in stages) else "no answer yet" if not any(stages)
                else "waits for you" if "proposed" in stages else "partly")
        secs.append((band_title(name), word, _side_tabs(f"fQ{g}x", [(x[0], x[1]) for x in items], [x[2] for x in items])))
    service = service_section(folder, root)
    if service:
        secs.append(("🌐 Service", "live", service))
    secs += [(title, "", body) for title, body in map_sections(folder, root)]
    tabs = delivery_tabs(folder, root)
    secs.append(("📦 Delivery", "ready" if any(t[1] == "ready" for t in tabs) else "nothing yet",
                 _side_tabs("fDx", [(t[0], t[1]) for t in tabs], [t[2] for t in tabs])))
    try:
        from live.board_views import SIDE_CSS
    except Exception:
        SIDE_CSS = ""
    return (BAND_CSS + FINDINGS_CSS + PB_CSS + SIDE_CSS + lead + "".join(
        f'<details class=band-sec><summary>{n} · {frame.esc(title)}' + (f'<span class=word>{word}</span>' if word else '')
        + f'</summary><div class=band-jobs>{body}</div></details>' for n, (title, word, body) in enumerate(secs, 1)) + PB_JS)


VIEW_SKILLS = {"mindmap": (("haipipe-mindmap", "draws and refreshes this map"),),
               "standing": (("haipipe-job", "adds a Job and keeps its Tasks in order"),
                            ("haipipe-task", "plans, builds and runs each Task"),
                            ("haipipe-run", "keeps each Run's card and receipt")),
               "findings": (("haipipe-report", "writes each answer from its Results"),
                            ("haipipe-task", "reads a Run's Result into its Task"),
                            ("haipipe-paper-evidence", "builds the raw tables from tables.yaml"),
                            ("haipipe-delivery", "keeps what it hands over in delivery/"))}


def work_process(folder: Path, root: Path, level: str, view: str, questions: list, inbox: list) -> str:
    """The Process band of a work page's Work view, as on a paper Board: 1 what waits on you, 2 this view's things to
    do, 3 the skills that do them. Each is a closed numbered section; a step with nothing in it does not show."""
    steps = []
    waiting = [r for r in inbox if r["state"] == "waiting"]
    if waiting:
        steps.append(("🙋 Waiting on you", "needs you", interactions_html(waiting, folder, root, "waiting")))
    li = lambda name, url, pop, note: (f'<li><a href="{frame.esc(url)}" data-pop="{frame.esc(pop)}">{frame.esc(name)}</a>'
                                       f'<small>{frame.esc(note)}</small></li>')
    todo = []
    if view == "standing" and level == "Block":
        for j in frame.children(folder, "Block"):
            if inside(j, root):
                said, word, *_ = job_progress(j, root)
                if word != "done":
                    todo.append(li(j.name, page_url(j, root), j.name, said))
        if todo:
            steps.append(("🚧 Jobs not finished", "", '<ul class=wk-rows>' + "".join(todo) + '</ul>'))
    elif view == "standing" and level == "Job":
        for t in frame.children(folder, "Job"):
            if inside(t, root):
                label = state_label(read_face(t, root)["state"])
                if state_kind(label) != "✅ done":
                    todo.append(li(t.name, page_url(t, root), t.name, state_words(label) if label else "no state"))
        if todo:
            steps.append(("🚧 Tasks not finished", "", '<ul class=wk-rows>' + "".join(todo) + '</ul>'))
    elif view == "findings":
        for r in questions:
            path = report_path(r, folder, root)
            stage = answer_state(path)[0]
            if stage != "agreed":
                title = task_questions.words(r.get("title")) or task_questions.words(r.get("question"))
                todo.append(f'<li>{frame.pop(frame.reader(path, root), title, title) if path else frame.esc(title)}'
                            f'<small>{frame.esc(FOUND_STAGE.get(stage, stage))}</small></li>')
        if todo:
            steps.append(("✍️ Answers to write or agree", "", '<ul class=wk-rows>' + "".join(todo) + '</ul>'))
    skills = VIEW_SKILLS.get(view, ())
    if skills:
        steps.append(("🧰 Skills that do it", "", '<ul class=wk-rows>' + "".join(
            f'<li><code>{frame.esc(a)}</code><small>{frame.esc(b)}</small></li>' for a, b in skills) + '</ul>'))
    return "".join(f'<details class=band-sec><summary>{n} · {frame.esc(name)}' + (f'<span class=word>{word}</span>' if word else '')
                   + f'</summary><div class=band-jobs>{body}</div></details>' for n, (name, word, body) in enumerate(steps, 1))


def work_views(overview: dict, folder: Path, root: Path, level: str, questions: list, inbox, runs_html, topics: list) -> dict:
    """A work page's Work has the same views as its Report (JL 261104: "why we have the progress? it should have the
    same view to the report"), as on a paper Board: Process first, then Results, the Report's own view drawn by the same
    code. Status alone adds each Task's output in place; a Task's Results are its Runs with their output."""
    def view(key, body):
        def build():
            if key == "standing":
                results = runs_html() if level == "Task" else status_now_html(folder, root, level, topics, outputs=True)
            else:
                results = body() if callable(body) else body
            process = work_process(folder, root, level, key, questions, inbox())
            return (BAND_CSS + FINDINGS_CSS + (f'<h3 class=wk-band>⚙️ Process</h3>{process}' if process else '')
                    + f'<h3 class=wk-band>📊 Results</h3>{results}')
        return build
    return {key: (name, view(key, body)) for key, (name, body) in overview.items()}


def job_short(job: Path, siblings: list, root: Path) -> str:
    """A Job's name in a few words: its face's title after its last colon (j11 "pretrain: model size" -> "model size"),
    unless every sibling ends the same; then the folder words no sibling shares (j61 -> "modelsize")."""
    def tail(j):
        face = j / f"{j.name}.md"
        first = face.read_text(encoding="utf-8", errors="ignore").split("\n", 1)[0] if face.is_file() else ""
        title = first.split(" · ", 1)[1].strip() if " · " in first else ""
        return title.rsplit(":", 1)[-1].strip() if title else ""
    tails = {j: tail(j) for j in siblings}
    mine = tails.get(job, "")
    if mine and (len(siblings) < 2 or sum(t == mine for t in tails.values()) == 1):
        return mine
    words = lambda j: j.name.split("_")[1:]
    shared = set(words(job)).intersection(*[set(words(j)) for j in siblings if j != job]) if len(siblings) > 1 else set()
    return " ".join(w for w in words(job) if w not in shared) or " ".join(words(job))


def job_progress(j: Path, root: Path) -> tuple:
    """(its line "partly · 2 Tasks · 85%", word, Tasks, share, Tasks' worth done): one count for Status and the map."""
    labels = [state_label(read_face(t, root)["state"]) for t in frame.children(j, "Job") if inside(t, root)]
    states = [state_kind(x) for x in labels]
    done, n = sum(k == "✅ done" for k in states), len(states)
    partly = [x for x, k in zip(labels, states) if k == "partly done"]
    # a partly Task fills its share of the bar from its own "N of M" (j61 t03: "652 of 700 complete")
    fill = done + sum(int(a) / int(b) for a, b in (re.search(r"(\d+) of (\d+)", x).groups()
                                                 for x in partly if re.search(r"(\d+) of (\d+)", x)) if int(b))
    share = round(100 * fill / n) if n else 0
    word = "done" if n and done == n else "not run" if not done and not partly else "partly"
    return f"{word} · {n} Tasks" + (f" · {share}%" if word == "partly" else ""), word, n, share, fill


def band_board(folder: Path, root: Path, outputs: bool = False) -> str:
    """A Block's Jobs as numbered sections, one per band (j0N, j1N, ...; named by the face's `bands:` line), closed
    (JL 261104: "I prefer to me make it like the sections"): the band's name, a bar of its Tasks done, one state word.
    Opened: one row per Job, and a Job's row opens to its Tasks and Runs (JL 261104: "each job each row, and we can
    collapse them out to see the tasks and runs"; no "Next:" lines, "just delete them")."""
    face = frame.face(folder)
    text = face.read_text(encoding="utf-8", errors="ignore") if face else ""
    named = dict(re.findall(r"\bj(\d)N\s+([^·\n]+)", (re.search(r"(?m)^bands:\s*(.+)$", text) or [None, ""])[1]))
    jobs = [j for j in frame.children(folder, "Block") if inside(j, root) and re.match(r"j\d\d_", j.name)]
    bands = {}
    for j in jobs:
        bands.setdefault(j.name[1], []).append(j)
    secs = []
    for number, (b, js) in enumerate(bands.items(), 1):
        cards, filled, total, marks = "", 0, 0, []
        for j in js:
            jf = j / f"{j.name}.md"
            jt = jf.read_text(encoding="utf-8", errors="ignore") if jf.is_file() else ""
            emoji = (re.search(r"(?m)^emoji:\s*(\S+)", jt) or [None, ""])[1]
            said, word, n, share, fill = job_progress(j, root)
            filled, total = filled + fill, total + n
            marks.append(word)
            goal = one_line(read_face(j, root)["goal"], 300)
            cards += (f'<details class=job-row><summary><span class=jn>{emoji} {j.name[:3]}</span>'
                      f'<a href="{frame.esc(page_url(j, root))}" data-pop="{frame.esc(j.name)}" title="{frame.esc(goal)}"><b>{frame.esc(job_short(j, js, root))}</b></a>'
                      + (interaction_button(interactions(j, root), j, root) if outputs else '')   # Work asks, Report shows
                      + f'<small>{said}</small>'   # words left of the bar, so
                      f'<span class=bar><i class="{"part" if word == "partly" else ""}" style="width:{share}%"></i></span></summary>'   # every bar lines up
                      f'<div class=job-tree>{fold_tree(j, root, "Job", outputs=outputs)}</div></details>')
        title = named.get(b, "").strip() or f"j{b}N"
        first = js[0] / f"{js[0].name}.md"
        emoji = (re.search(r"(?m)^emoji:\s*(\S+)", first.read_text(encoding="utf-8", errors="ignore")) or [None, ""])[1] if first.is_file() else ""
        if not title[:1].isalnum():                   # the face names its own emoji ("j2N 🧠 heads"); else the band's first Job's
            emoji = ""
        word = "done" if all(m == "done" for m in marks) else "not run" if all(m == "not run" for m in marks) else "partly"
        share = round(100 * filled / total) if total else 0
        secs.append(f'<details class=band-sec><summary>{number} ·{" " + emoji if emoji else ""} {frame.esc(band_title(title))}'
                    f'<span class=word>{word}</span>'
                    f'<span class=bar><i class="{"part" if word == "partly" else ""}" style="width:{share}%"></i></span></summary>'
                    f'<div class=band-jobs>{cards}</div></details>')
    return BAND_CSS + "".join(secs) if secs else ""


def status_now_html(folder: Path, root: Path, level: str, topics: list, outputs: bool = False) -> str:
    """Report's Status at a Block, Job or Task: where its sNN stand, then its Jobs and Tasks (or a Task's Runs), one
    per row (JL 261030: "I think this should state the studio and jobs/tasks status"; the old Done when and
    Context prose: "we don't need this", "this is not readable")."""
    li = lambda mark, name, url, words, state: (
        f'<li>{mark} <a href="{frame.esc(url)}"><b>{frame.esc(name)}</b></a> {frame.esc(words)}'
        + (f' <span class="mut">· {frame.esc(state)}</span>' if state else '') + '</li>')
    parts = []
    rows = []
    for topic, _, facts in topics:
        if not topic.is_dir():
            continue
        lead, shown = frame.topic_label(topic, facts.get("at", ""))
        stage = facts.get("stage", "")
        rows.append(li(STAGE_MARK.get(stage, "⬜"), lead + shown, topic_home(topic, root),
                       face_title(frame._notes(topic) or topic / "_"), stage or "no stage"))
    studio = ""
    if rows:                                         # after the work, folded, its tally in words (JL 261103: "very hard
        stages = [facts.get("stage", "") or "no stage" for t, _, facts in topics if t.is_dir()]   # to read")
        tally = ", ".join(f"{stages.count(w)} {w}" for w in dict.fromkeys(stages))
        studio = (f'<h3 class="focus-sub">Studio</h3><details class="glance-fold"><summary>{len(rows)} topics: '
                  f'{frame.esc(tally)}</summary><ul class="glance-list">{"".join(rows)}</ul></details>')
    if level == "Task":
        runs = frame.runs_of(folder)
        if runs:
            parts.append(f'<h3 class="focus-sub">Runs</h3><ul class="glance-list">' + "".join(
                f'<li><b>{frame.esc(r["run"])}</b> <span class="mut">· {frame.esc(r["status"])}</span></li>' for r in runs)
                + '</ul>')
    elif level == "Block" and (bands := band_board(folder, root, outputs)):   # its bands, each Job's row opening to its tree (JL 261104)
        parts.append(bands)
    else:                                            # the same folding tree as Work's Progress, without the outputs
        tree = fold_tree(folder, root, level, outputs=outputs)   # (JL 261102: "why this is not changed?")
        if tree:
            parts.append(f'<h3 class="focus-sub">{"Jobs and Tasks" if level == "Block" else "Tasks"}</h3>{tree}')
    return "".join(parts) + studio


def related_html(folder: Path, root: Path) -> str:
    """What came in from outside (haipipe-related): the folder's related/related.md table, or its files."""
    rel = folder / "related"
    if not rel.is_dir() or not inside(rel, root):
        return ""
    table = rel / "related.md"
    if table.is_file():
        return markdown(table.read_text(encoding="utf-8", errors="replace"), rel, root)
    files = sorted(q for q in rel.rglob("*") if q.is_file() and not q.name.startswith("."))
    return "<ul>" + "".join(f'<li><a href="{frame.esc(frame._file_url(q, root))}" target=_blank rel=noopener>'
                            f'{frame.esc(q.relative_to(rel).as_posix())}</a></li>' for q in files) + "</ul>" if files else ""


# A Studio topic has no page of its own (JL 261031: "we will remove the single page for the studio"): a link to an sNN
# opens its card in its level's Studio (topic_home); its parts open from the card, each in the pop-out.
def is_topic(folder: Path) -> bool:
    """A Studio topic folder with its face: `sNN-<topic>/` beside a level's Jobs or Tasks (JL 261030), or an older
    `sNN-<topic>/`."""
    placed = ((folder.parent.name == "studio" and bool(re.match(r"s\d+[-_]", folder.name)))
              or (bool(frame.STUDIO_ITEM.match(folder.name)) and frame.level_of(folder.parent) in ("Block", "Job", "Task")))
    return placed and folder.is_dir() and frame._notes(folder) is not None


def topic_home(topic: Path, root: Path) -> str:
    """Where an sNN opens: its card in its level's Studio, under its group, the page scrolled to it (JL 261031: the
    left rail's sNN "will be point to" its card in `section=studio`)."""
    notes = frame._notes(topic)
    tags = (frame._note_facts(notes).get("tags") or []) if notes else []
    return page_url(frame.topic_owner(topic), root, "studio", tags[0] if tags else OTHER) + "#" + quote(topic.name)


def rail_url(page: Path, root: Path) -> str:
    """A left-rail link: an sNN's card in its level's Studio, any other folder its page."""
    return topic_home(page, root) if is_topic(page) else page_url(page, root)


INTERACTION_STATE = {"waiting": "waiting", "done": "answered", "complete": "answered", "planned": "planned"}


def interaction_topic(about: str, page: Path) -> Path | None:
    """The sNN an interaction is about, from the address its `for:` line starts with (`b35-s01:studio @ …`,
    `b17.j03-s02:…`): that Block among the page's folders, its Job or Task when named, and that level's sNN."""
    m = re.match(r"\s*(b\d+|Paper-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*?)((?:\.[jt]\d+)*)-(s\d+)\b", about or "")
    if not m:
        return None
    paper = m.group(1).startswith("Paper-")              # a paper Board has no bNN: its folder name is its address
    level = next((p for p in [page, *page.parents] if (p.name == m.group(1) if paper else p.name.split("_")[0] == m.group(1))
                  and (paper or frame.level_of(p) == "Block")), None)
    for part in [x for x in m.group(2).split(".") if x]:
        level = next((k for k in kids(level) if k.name.split("_")[0] == part), None) if level else None
    return next((t for t, _ in frame._studio_topics(level) if t.name.split("-")[0] == m.group(3) and is_topic(t)),
                None) if level else None


def interactions(folder: Path, root: Path) -> list:
    """Every interaction at this page or below, waiting ones first (haipipe-interaction; JL 261031: one record per
    interaction, shown by the Interactions view, the Work rows, the map and the Studio cards alike). A record is a
    collection Run, `runs/rNN_collect_<slug>/`; its state is its card's status (waiting, answered, planned), so no
    view keeps a state of its own. Answered is not applied: applying belongs to the Runs its `feeds:` names."""
    rows = []
    for page in rollup(folder):
        runs = page / "runs"
        if not runs.is_dir() or not inside(page, root):
            continue
        for run in sorted(p for p in runs.glob("r*_collect_*") if p.is_dir()):
            try:
                card = yaml.safe_load((run / "run.yaml").read_text(encoding="utf-8")) or {}
            except (OSError, yaml.YAMLError):
                card = {}
            source = run / "question_collection.md"
            text = source.read_text(encoding="utf-8", errors="ignore") if source.is_file() else ""
            about = (re.search(r"(?m)^for:\s*(.+?)\s*$", text) or [None, str(card.get("target") or "")])[1]
            answers = run / "result" / "answer_collection.md"
            answers = answers if answers.is_file() else None
            got = re.search(r"(?m)^received:\s*(.+?)\s*$", answers.read_text(encoding="utf-8", errors="ignore")) if answers else None
            status = str(card.get("status") or "")
            form = run / f"{run.name}.html"
            done_ = run / "applied.md"                 # what applied each answer (haipipe-interaction collect.py applied)
            marks = {m.group(1): (m.group(2), m.group(3), m.group(4)) for m in re.finditer(
                r"(?m)^(Q\d+) · (applied|in progress) · (\d{4}-\d{2}-\d{2}) \d{2}:\d{2} · (.+?)\s*$",
                done_.read_text(encoding="utf-8", errors="ignore"))} if done_.is_file() else {}
            rows.append({"run": run.name, "path": run, "page": page, "status": status,
                         "state": "to know" if card.get("source") == "know" else "answered" if answers else INTERACTION_STATE.get(status, status or "planned"),
                         "title": next((ln[2:].strip() for ln in text.splitlines() if ln.startswith("# ")), run.name),
                         "about": about, "topic": interaction_topic(about, page),
                         "asks": re.findall(r"(?ms)^##\s+(Q\d+)\s*·\s*(.+?)\s*$.*?^\*\*(.+?)\*\*\s*$", text),
                         "form": form if form.is_file() else None, "answers": answers,
                         "received": got.group(1) if got else "", "feeds": list(card.get("feeds") or []),
                         "applied": marks})
    order = {"waiting": 0, "planned": 1, "answered": 2}
    return sorted(rows, key=lambda r: order.get(r["state"], 1))


def interaction_button(rows: list, holder: Path, root: Path) -> str:
    """One button, "Interaction", on a row that holds interactions: no count, no colour, no answered or questions
    tag (JL 261031, b16 t01 r04 Q3: C, "we will not have the answered & questions for you"); it pops out the list of
    the row's items, the waiting one first (Q4: A). The same button wherever an item shows (Q6: A). `holder` is what
    the row is: an sNN (the items about it), a Job or Task (the items at it or below), or one collection Run."""
    if not rows or not inside(holder, root):
        return ""
    href = frame.ROUTE + "?" + urlencode({"view": "focus-part", "part": "interactions", "path": frame.rel(holder, root)})
    # a question waiting for the person flags the button (JL 261031: "if there are some questions i need to answer,
    # cuold you flag them as well"); with nothing waiting it stays plain
    waits = any(r.get("state") == "waiting" for r in rows)
    flag = (' style="border-color:light-dark(#ffa94d,#b35c00);color:light-dark(#b35c00,#ffc078)" '
            'title="questions wait for you"') if waits else ''
    return (f'<a class="row-verb"{flag} data-pop="{frame.esc(holder.name)} · Interaction" href="{frame.esc(href)}" '
            f'target=_blank rel=noopener>{"🙋 " if waits else ""}Interaction</a>')


def interaction_items(holder: Path, root: Path) -> list:
    """The items an Interaction button lists: about an sNN, held by one collection Run, or at a page or below."""
    if is_topic(holder):
        return [r for r in card_interactions(frame.topic_owner(holder), root) if r["topic"] == holder]
    if holder.parent.name == "runs" and "_collect_" in holder.name:
        return [r for r in interactions(holder.parent.parent, root) if r["path"] == holder]
    return interactions(holder, root)


def interaction_item(r: dict, folder: Path, root: Path, in_pop: bool = False) -> str:
    """One item (JL 261031, b16 t01 r04 Q5: A): its title, state and date, its questions, and one button: Answer
    (its form) or See answers (its answer file). The Interactions view and the button's pop-out draw it alike; inside
    the pop-out the button opens in that same pop-out, never a second one over it."""
    opens = (lambda label: 'target=_self') if in_pop else (lambda label: f'data-pop="{frame.esc(label)}" target=_blank rel=noopener')
    form, answers = r["form"], r["answers"]
    day = r["received"].split(" ")[0] if r["received"] else (
        dt.datetime.fromtimestamp(form.stat().st_mtime).strftime("%Y-%m-%d") if form else "")
    state = {"waiting": "waiting for you", "answered": "answered", "planned": "not sent yet"}.get(r["state"], r["state"])
    where = f'asked by <a href="{frame.esc(page_url(r["page"], root))}">{frame.esc(origin(r["page"], folder) or r["page"].name)}</a>'
    if r["topic"] is not None:
        where += f' · about <a href="{frame.esc(topic_home(r["topic"], root))}">{frame.esc(r["topic"].name)}</a>'
    elif r["about"]:
        where += f' · about {frame.esc(r["about"])}'
    def flag(q):                                         # an applied answer carries its flag (JL 261031)
        mark = r.get("applied", {}).get(q)
        return (f' <span class="ix-applied" title="{frame.esc(mark[2])}">'
                + ("✅ applied " if mark[0] == "applied" else "⏳ in progress ") + f'{frame.esc(mark[1])}</span>') if mark else ''
    asks = "".join(f'<li><b>{frame.esc(q)}</b> {frame.esc(ask)}{flag(q)}</li>' for q, _, ask in r["asks"])
    if r["state"] == "to know" and form and inside(form, root):
        button = (f'<a class="row-verb" href="{frame.esc(frame._file_url(form, root))}" {opens(r["title"])}>Read</a>')
    elif r["state"] == "answered" and (form or answers):   # the answered form itself, read only, not its raw Markdown
        shown = form if form and inside(form, root) else answers     # (JL 261031: "the UI here doesn't good")
        button = (f'<a class="row-verb" href="{frame.esc(frame._file_url(shown, root))}" '
                  f'{opens(r["title"] + " · answers")}>See answers</a>') if shown and inside(shown, root) else ""
    elif form and inside(form, root):
        button = (f'<a class="row-verb" href="{frame.esc(frame._file_url(form, root))}" {opens(r["title"])}>Answer</a>')
    else:
        button = ""
    applies = ("Applying it belongs to " + ", ".join(Path(str(f)).name for f in r["feeds"]) + "."
               if r["state"] == "answered" and r["feeds"] else "")   # applied is the owning Task's record, not ours
    return (f'<article class="inbox-row {frame.esc(r["state"])}"><div class="inbox-head"><b>{frame.esc(r["title"])}</b>'
            f'<span class="inbox-state {frame.esc(r["state"])}">{frame.esc(state)}{(" · " + frame.esc(day)) if day else ""}</span></div>'
            f'<p class="inbox-where">{where} · <code>{frame.esc(r["run"])}</code></p>'
            + (f'<ol class="inbox-asks">{asks}</ol>' if asks else '')
            + (f'<p class="inbox-waits">{frame.esc(applies)}</p>' if applies else '')
            + (f'<div class="inbox-actions">{button}</div>' if button else '') + '</article>')


def interaction_where(r: dict, folder: Path, root: Path) -> str:
    """The small line under a set's form: who asked, what it is about, its Run, and who applies its answers."""
    where = f'asked by <a href="{frame.esc(page_url(r["page"], root))}">{frame.esc(origin(r["page"], folder) or r["page"].name)}</a>'
    if r["topic"] is not None:
        where += f' · about <a href="{frame.esc(topic_home(r["topic"], root))}">{frame.esc(r["topic"].name)}</a>'
    elif r["about"]:
        where += f' · about {frame.esc(r["about"])}'
    where += f' · <code>{frame.esc(r["run"])}</code>'
    if r["received"]:
        where += f' · {frame.esc(r["received"].split(" ")[0])}'
    if r["state"] == "answered" and r["feeds"]:
        where += " · Applying it belongs to " + frame.esc(", ".join(Path(str(f)).name for f in r["feeds"])) + "."
    return where


def standard_interactions(rows: list, folder: Path, root: Path, in_pop: bool = False) -> str:
    """The standard Interaction for these rows; a Run with no built form or no questions keeps its plain row, so nothing
    asked goes missing."""
    return (IX.interaction_section(rows, root, 0, lambda r: interaction_where(r, folder, root))
            + "".join(interaction_item(r, folder, root, in_pop) for r in rows if r.get("form") is None or not r.get("asks")))


def interactions_html(rows: list, folder: Path, root: Path, which: str) -> str:
    """The Interactions view (JL 261031): one row per interaction: what it asks, whose work it is for and what it is
    about, what it waits for, and the button that opens the same record the Work row and the Studio card open."""
    shown = [r for r in rows if which == "all" or r["state"] == which]
    if not shown:
        return '<p class="mut">' + {"waiting": "Nothing needs your input.", "answered": "Nothing answered yet."}.get(
            which, "No interactions here.") + '</p>'
    out = [interaction_item(r, folder, root) for r in shown]
    return "".join(out)


def face_parts(text: str) -> dict:
    """A topic face's parts by heading, setext (`Decided` over dashes) or `## Decided`, keyed in lower case."""
    parts, name, lines, fence, rows, i = {}, "", [], False, text.splitlines(), 0
    while i < len(rows):
        line = rows[i]
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
        under = rows[i + 1].strip() if i + 1 < len(rows) else ""
        atx = None if fence else re.match(r"^#{1,3}\s+(.+?)\s*#*\s*$", line)
        if not fence and (atx or (line.strip() and not line.lstrip().startswith(("-", "|", "*"))
                                  and re.fullmatch(r"-{3,}|={3,}", under))):
            parts[name] = "\n".join(lines).strip()
            name, lines = (atx.group(1) if atx else line).strip().casefold(), []
            i += 1 if atx else 2
            continue
        lines.append(line)
        i += 1
    parts[name] = "\n".join(lines).strip()
    return parts


def part(parts: dict, word: str) -> str:
    return next((v for k, v in parts.items() if k.startswith(word)), "")


def first_sentence(text: str) -> str:
    """The topic line up to its first full stop; the rest (the quote, the why) stays on the face."""
    found = re.match(r"(.+?[.;])(?:\s|$)", text)
    return found.group(1) if found else text


# a piece's state from render_delivery.py, in words a reader acts on, and its mark
PIECE_STATE = {"same": ("✅", "in place"), "rendered": ("✅", "in place"), "differs": ("⬜", "changed, not rendered yet"),
               "not placed": ("❗", "not placed"), "no source": ("❗", "its source is missing"),
               "code": ("", "built by a Run"), "theme": ("", "built by its Theme's skill")}


READ_AS_TEXT = {".json", ".yaml", ".yml", ".txt", ".py", ".tex", ".csv", ".tsv", ".bib", ".js", ".css", ".sh", ".ps1", ".do"}


def readable(path: Path | None, root: Path) -> str:
    """A file opened in place, under its row (JL 261030: "怎么能直接把每个 file 展开来读一下呢"): Markdown drawn, other
    text as it is, a picture shown; a web page, a Word file or a PDF opens in a new tab."""
    if not path or not path.is_file() or not inside(path, root):
        return '<p class="mut">Nothing to read here yet.</p>'
    url = ("/" + frame.rel(path, root)) if path.suffix == ".html" else frame._file_url(path, root)
    opener = f'<p><a class="row-verb" href="{frame.esc(url)}" target=_blank rel=noopener>Open {frame.esc(path.name)}</a></p>'
    if path.suffix == ".md":
        return markdown(path.read_text(encoding="utf-8", errors="replace")[:60000], path.parent, root)
    if path.suffix.lower() in READ_AS_TEXT:
        return f'<pre>{frame.esc(path.read_text(encoding="utf-8", errors="replace")[:60000])}</pre>'
    if path.suffix.lower() in (".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp"):
        return f'<img src="{frame.esc(frame._file_url(path, root))}" alt="{frame.esc(path.name)}" loading="lazy">'
    return opener


def topic_delivery(folder: Path, root: Path) -> str:
    """An sNN's delivery in its two parts (JL 261030: "we have two things in the delivery, one is the delivery, and the
    other one is the render"): 1 the delivery, what `delivery/` holds, the agreed version, each file opened in place;
    2 the render, where each piece goes (`delivery/render.yaml`, checked by haipipe-studio's render_delivery.py) and
    whether it landed, each opened to what now sits there."""
    deliv, owner = folder / "delivery", frame.topic_owner(folder)
    card = deliv / "render.yaml"
    try:
        rd = frame.render_module()
        rows = [(piece, *rd.state(folder, piece)) for piece in rd.pieces(folder)]
    except Exception:                                    # a broken render.yaml shows the files, never a crash
        rd, rows = None, []

    #   1 · the delivery: the thing itself
    out = ['<h3 class="focus-sub">1 · Delivery: what it hands over</h3>'
           '<p class="mut">delivery/, the agreed version; open a file to read it</p>']
    # its deck and preview are Delivery's views, the buttons under the title (delivery_views)
    files = sorted(p for p in deliv.rglob("*") if p.is_file() and not p.name.startswith(".") and p != card
                   and inside(p, root))[:80]
    out.append("".join(f'<details class="deliv-file"><summary>{frame.esc(p.relative_to(deliv).as_posix())}</summary>'
                       f'<div class="deliv-body">{readable(p, root)}</div></details>' for p in files)
               if files else '<p class="mut">Empty: nothing agreed yet.</p>')

    #   2 · the render: where each piece goes, and whether it is there
    out.append('<h3 class="focus-sub">2 · Render: where it goes</h3>'
               '<p class="mut">delivery/render.yaml; open a piece to see what now sits at its target</p>')
    items = []
    for piece, st, words in rows:
        mark, said = PIECE_STATE.get(st, ("", st))
        name = piece.get("block") or piece.get("code") or piece.get("from") or "a piece"
        if "code" in piece:                              # the Run, or the Task's Runs, that build it, and what their cards say
            run = owner / str(piece.get("by", ""))
            cards = [run / "run.yaml"] if (run / "run.yaml").is_file() else sorted(run.glob("runs/*/run.yaml"))
            states = [(re.search(r"(?m)^status:\s*(\S+)", c.read_text(encoding="utf-8", errors="ignore")) or [None, ""])[1]
                      for c in cards]
            done = sum(x == "done" for x in states)
            mark = "✅" if states and done == len(states) else "⬜"
            said = f"built by {run.name}, " + (states[0] or "no status" if len(states) == 1 else
                                               f"{done} of {len(states)} Runs done" if states else "no Run yet")
            task = run.parent.parent if (run / "run.yaml").is_file() else run
            where = (f'<a href="{frame.esc(page_url(task, root))}" target=_blank rel=noopener>{frame.esc(frame.rel(run, root))}</a>'
                     if run.is_dir() and inside(run, root) else frame.esc(str(piece.get("by", ""))))
            body = readable(run / f"{run.name}.md", root)  # what the Run says it built, or the Task's face
        elif "to" in piece:
            base = rd.root_for(folder, piece["to"])
            target = base / piece["to"] if base else None
            link = (f'<a href="{frame.esc(frame.reader(target, root))}" target=_blank rel=noopener>{frame.esc(piece["to"])}</a>'
                    if target and target.is_file() and inside(target, root) else frame.esc(piece["to"]))
            where = f'delivery/{frame.esc(piece.get("from", ""))} → {link}'
            body = rendered_region(rd, folder, piece, target, root)
        else:
            where, body = frame.esc(words), '<p class="mut">Its Theme\'s skill builds it.</p>'
        items.append(f'<details class="status-row deliv-piece"><summary><span class="row-name">{mark} {frame.esc(name)}</span>'
                     f'<p class="row-line">{where}</p><p class="row-meta">{frame.esc(said)}</p></summary>'
                     f'<div class="deliv-body">{body}</div></details>')
    out.append("".join(items) if items else '<p class="mut">No render.yaml yet: nothing says where it goes.</p>')
    if card.is_file() and inside(card, root):
        out.append(f'<details class="deliv-file"><summary>render.yaml</summary><div class="deliv-body">{readable(card, root)}</div></details>')
    return "".join(out)


def rendered_region(rd, folder: Path, piece: dict, target: Path | None, root: Path) -> str:
    """What sits between the piece's render markers in its target now: the render's result, not its source."""
    if not target or not target.is_file() or not inside(target, root):
        return '<p class="mut">Its target is not there yet.</p>'
    start, end = rd.markers(rd.address(folder), piece["block"])
    m = re.search(re.escape(start) + r"[^\n]*-->\n(.*?)\n" + re.escape(end), target.read_text(encoding="utf-8", errors="replace"), re.S)
    if not m:
        return f'<p class="mut">No render markers for {frame.esc(piece["block"])} in {frame.esc(target.name)} yet.</p>'
    return markdown(m.group(1)[:60000], target.parent, root)


def static_page(folder: Path, root: Path, view: str, body: str, note: str = "") -> str:
    """A page an sNN's builder writes into delivery/ (its preview, contract, slides): the workbench frame, its path and
    left rail ending at the topic's card in its level's Studio (JL 261031: the sNN has no page of its own), its
    Delivery views under the title. `view` is preview, contract or slides; `note` a tag beside its stage."""
    notes = frame._notes(folder)
    facts = frame._note_facts(notes)
    lead, shown = frame.topic_label(folder, facts.get("at", ""))
    owner = frame.topic_owner(folder)
    meta = ((f'<span class="row-stage">{frame.esc(facts["stage"])}</span>' if facts.get("stage") else '')
            + (f'<span class="row-type" title="delivery type">{frame.esc(facts["dtype"])}</span>' if facts.get("dtype") else '')
            + (f'<span class="row-stage">{frame.esc(note)}</span>' if note else ''))
    goal_html = (f'<div class="focus-goal topic-goal"><span class="goal-word">Topic</span>'
                 + (markdown(first_sentence(facts["topic"]), folder, root) if facts.get("topic") else '')
                 + (f'<p class="topic-meta">{meta}</p>' if meta else '') + '</div>')
    crumbs, cur = [frame._link("/", root.name)], root
    for name in folder.relative_to(root).parts[:-1]:
        cur /= name
        crumbs.append(frame._link(page_url(cur, root), name))
    crumbs.append(frame._link(topic_home(folder, root), folder.name))
    left = [rail_link(page_url(owner, root, "studio"), owner.name, False)]
    left += [rail_link(rail_url(other, root), other.name, other == folder, "child") for other in rail_kids(owner, root)]
    title_html = (f'<span class="h1-addr">{frame.esc(lead)}</span>' if lead else '') + frame.esc(shown)
    source = frame.pop(frame.reader(notes, root), "Source Markdown", "Open this topic's Markdown")
    return page_shell(folder, root, crumbs, title_html, "Delivery", "what it hands over, and where it goes",
                      views_bar(delivery_views(folder, root), view), goal_html, body, source, left, "", [], "delivery")


def delivery_document(folder: Path, root: Path) -> str:
    """An sNN's Delivery alone, for the pop-out from its card (JL 261030: "这些都是 pop out ... 不要让它直接出现")."""
    if not (is_topic(folder) and (folder / "delivery").is_dir() and inside(folder, root)):
        return ""
    return document(folder.name + " · delivery", '<main class="focus-page"><h1>' + frame.esc(folder.name)
                    + '<span class="h1-section">Delivery</span></h1><section class="focus-card"><div class="focus-content">'
                    + topic_delivery(folder, root) + '</div></section></main>')


def delivery_views(folder: Path, root: Path) -> list:
    """Delivery's views, as buttons under the title (key, name, href): the overview the workbench draws, then the pages
    the sNN's builder writes into delivery/, when they exist."""
    views = [("overview", "Overview", frame.ROUTE + "?" + urlencode({"view": "focus-delivery", "path": frame.rel(folder, root)}))]
    for key, name, page in (("preview", "Preview", "web/index.html"), ("contract", "Contract", "web/contract.html"),
                            ("slides", "Slides", "deck/index.html")):
        q = folder / "delivery" / page
        if q.is_file() and inside(q, root):
            views.append((key, name, "/" + frame.rel(q, root)))
    return views


def views_bar(views: list, current: str) -> str:
    return ('<nav class="section-views" aria-label="Views">' + "".join(
        f'<a href="{frame.esc(href)}"' + (' aria-current="page"' if key == current else '') + f'>{frame.esc(name)}</a>'
        for key, name, href in views) + '</nav>') if len(views) > 1 else ""


def render(theme, root: Path, folder: Path, section="", group="") -> str:
    """One page: path, name and goal on top; five sections on the right rail, each with its verb (haipipe-ui):
    Overview read · Work do · Studio think (its groups under it) · Delivery hand over · Related take in."""
    root, folder = root.resolve(), folder.resolve()
    if not inside(folder, root):
        raise ValueError("Folder outside root")
    if is_topic(folder):                             # an old sNN link (the server answers it with a 302 first)
        home = frame.esc(topic_home(folder, root))
        return document(folder.name, f'<meta http-equiv="refresh" content="0;url={home}"><a href="{home}">{frame.esc(folder.name)}</a>')
    data, level = read_face(folder, root), page_level(folder)
    questions, question_errors = owned_register(data, root, 'Questions', 'questions')
    deliverables, _ = owned_register(data, root, 'Deliverables', 'deliverables')
    home = home_section(data, theme.name)
    draft = draft_parts(folder, root)                   # HOOK: a draft Task's own parts (focus_draft.py), else {}
    topics = topic_rows(folder, root, draft.get("studio") if draft else None)
    paper = theme.name == "paper"
    if section == "overview":
        section, group = "report", OLD_VIEWS.get(group, group)
    elif section == "report":
        group = OLD_VIEWS.get(group, group)
    if section in OLD_KEYS:
        reports_view = section == "reports" or (section == "overview-report" and group == "reports")
        section, group = OLD_KEYS[section]
        if reports_view and home == "overview-report":
            group = "answers"

    standing = (lambda: status_now_html(folder, root, level, topics)) if level in ("Block", "Job", "Task") and not draft else ""   # built only when opened (each took 4.5 s on b01)

    # Overview: read. Its views: Report (what we know: the recorded answers first), Questions, Context, Pipeline,
    # Timeline; each piece of content in one view only.
    untabbed = lambda html: re.sub(r'<nav class="overview-tabs".*?</nav>', '', html, flags=re.S)
    has_reports = any(report_path(row, folder, root) for row in questions)
    report = ""
    if home == "overview-report":
        report = untabbed(overview_report_html(data, questions, folder, root, False))
    elif theme.name == "work" and level == "Block" and not draft:
        report = lambda: findings_board(questions, folder, root, markdown(data["takeaways"], folder, root) if data["takeaways"] else "")   # built only when opened
    elif has_reports:
        report = reports_html(questions, folder, root)
    elif questions:
        report = question_cards(questions, folder, root, detailed=theme.name == "work")   # it is their only view there
    elif data["takeaways"]:
        report = markdown(data["takeaways"], folder, root)
    elif paper and not draft:
        report = '<p class="mut">No takeaways recorded in this page’s Markdown.</p>'
    events = timeline_events(folder, root)
    overview = {}
    if level in ("SPACE", "Folder", "Project", "Theme"):     # JL 261029 sketch: MindMap · Summary · Blocks · Status
        under = blocks_under(folder)
        overview["mindmap"] = ("MindMap", lambda: mindmap_view(folder, root))
        overview["findings"] = ("Findings", overview_summary(folder, root, level, events))
        overview["themes"] = ("Themes", lambda: themes_view(folder, root))
        overview["status"] = ("Status", lambda: status_view(under, root))
    if level in ("Block", "Job", "Task"):                       # its own parts as a map, as above the Block
        overview["mindmap"] = ("MindMap", lambda: parts_mindmap(folder, root))
    if standing:
        overview["standing"] = ("Status", standing)            # where its sNN, Jobs and Tasks stand
    if report:
        overview["findings"] = ("Findings", report)            # what it has found: answers, takeaways
    if draft:                                                  # HOOK: Text · Review · Status (focus_draft.report_views)
        overview.update(draft["report"])
    if home == "overview-report" and has_reports:
        overview["answers"] = ("Answers", untabbed(overview_report_html(data, questions, folder, root, True)))
    if questions and theme.name != "work":                     # a work page's Questions live in Findings (JL 261104: "we don't need the questions")
        overview["questions"] = ("Questions", question_cards(questions, folder, root, detailed=True))
    for key, name in UI_VIEWS:                                 # a theme Block's real pages, level by level
        if data["ui"][key]:
            overview["ui-" + key] = (name, ui_view(data["ui"][key], name, root))
    if theme.name == "design" and level in ("Block", "Job", "Task") and not draft:   # HOOK: the design letters (b12 j01)
        overview = design_views(folder, root, "report") or overview
    if theme.name == "insight" and level == "Block" and not draft:   # HOOK: an insight Board's letters (b11 s51), MindMap last
        letters = insight_board_report(folder, root)
        overview = {**letters, **{k: v for k, v in overview.items() if k == "mindmap"}} if letters else overview
    if theme.name == "insight" and level in ("Job", "Task") and not draft:   # HOOK: insight Job and Task letters (s54, s57)
        letters = insight_views_for(folder, root, "report")
        overview = {**letters, **{k: v for k, v in overview.items() if k == "mindmap"}} if letters else overview
    if paper and level == "Block":                             # HOOK: a paper Board's own parts, then its MindMap; no
        overview = paper_board_report(folder, root) or {k: v for k, v in overview.items() if k == "mindmap"}  # no Status, Findings, Questions (JL 261031: "no need to use
                                                                 # them anymore"); the mind map is a section of each part

    # Work: do. Its views: Progress (the children, or a Task's Runs), Deliverables, Files.
    work = {"progress": ("Job-Versions" if paper and level == "Block" else "Progress",
                         lambda: status_html(folder, root, level, [] if overview else questions))}   # built when opened
    if draft:                                            # HOOK: the five steps, then the Task's Runs
        work = {**{k: v for k, v in draft["work"].items() if k != "runs"}, "runs": ("Runs", work["progress"][1])}
    if theme.name == "work" and level in ("Block", "Job", "Task") and not draft:   # the same views as Report (JL 261104)
        work = work_views(overview, folder, root, level, questions, lambda: inbox, work["progress"][1], topics)
    if data["sections"].get("deliverables"):
        work["deliverables"] = ("Deliverables", deliverables_html(deliverables, folder, root) if deliverables
                                else markdown(data["sections"]["deliverables"], folder, root))
    if level == "SPACE":                                 # the SPACE's progress chart, one click away (the old Home)
        work["progress"] = ("Projects", work["progress"][1])
        work["chart"] = ("Chart", '<p><a class="row-verb" href="/?view=chart">Open the progress chart</a> '
                                  '<a class="row-verb" href="/?view=list">Open the list index</a></p>')
    if paper and level == "Job" and not draft:           # HOOK: a paper version's Work, by band (s36-D01, D02)
        work = paper_version_work(folder, root) or work
    if paper and level == "Block":                       # HOOK: a paper Board's Work shares its Report's list
        work = paper_board_work(folder, root, work["progress"][1]()) or work
    if theme.name == "design" and level in ("Block", "Job", "Task") and not draft:   # HOOK: the design letters (b12 j01)
        work = design_views(folder, root, "work") or work
    if theme.name == "insight" and level in ("Block", "Task") and not draft:   # HOOK: insight Board and Task Work (s52, s58)
        work = insight_views_for(folder, root, "work") or work
    if theme.name == "insight" and level == "Job" and not draft:   # HOOK: an insight Job's Work, by letter (b11 s55)
        work = insight_job_work(folder, root) or work

    paper_out = "" if draft else paper_delivery(folder, root)   # HOOK: a paper version's or Board's whole paper
    delivery = draft["delivery"] if draft else (paper_out if paper_out and level == "Block" else paper_out + delivery_html(folder, root))
    dviews = draft.get("delivery_views", {}) if draft else paper_delivery_views(folder, root)   # HOOK: previews by lane
    look = draft or (paper_look() if dviews or (paper_out and level == "Block") else {})   # HOOK: a draft's or paper's look
    if dviews and not delivery:
        delivery = "previews"
    related = related_html(folder, root)
    # Interactions: the person's inbox, every interaction at this page or below (JL 261031): one record each, the
    # same one its Work row, its map node and its Studio card open
    inbox = interactions(folder, root) if page_level(folder) not in ("SPACE", "Folder") else []
    # the standard Interaction, left tabs and one question on the right (JL 261104: "make this to be the standard items for
    # any of them"; "the workbecnh UI code"), or what the filter found nothing of
    empty = {"waiting": "Nothing needs your input.", "answered": "Nothing answered yet."}
    asked = {key: (name, standard_interactions([r for r in inbox if key == "all" or r["state"] == key], folder, root)
                   or '<p class="mut">' + empty.get(key, "No interactions here.") + '</p>')
             for key, name in (("all", "All"), ("waiting", "Needs your input"), ("answered", "Answered"))}   # opens on All
    rail = []                                            # (key, label, group): the right rail, in this order
    if overview:
        rail.append(("report", "Report", ""))
    rail.append(("work", "Work", ""))
    if topics or draft:                                  # HOOK: a draft Task always has its Studio (talk and sketch)
        rail.append(("studio", "Studio", ""))          # its groups are its views, under the title (JL 261029)
    if page_level(folder) not in ("SPACE", "Folder"):    # always on the rail, empty or not (JL 261031: "in the right rail,
        rail.append(("interactions", "Interactions", ""))  # we should have a section named the Interaction, to show all
                                                         # the interaction under this page")
    if delivery or page_level(folder) not in ("SPACE", "Folder"):   # always on the rail, empty or not (JL 261031: "we
        rail.append(("delivery", "Delivery", ""))                     # also missed the delivery here")
    if related:
        rail.append(("related", "Related", ""))
    if events:                                           # what happened when: its own place on the rail (JL 261029)
        rail.append(("timeline", "Timeline", ""))
    rail.append(("files", "Files", ""))                 # the folder itself: a place to go, on the rail (JL 261029)

    below_names = {"SPACE": "Projects", "Folder": "Projects", "Project": "Blocks", "Theme": "Blocks", "Block": "Jobs",
                   "Job": "Tasks", "Task": "Runs"}

    def describe(key, tag=""):
        """What is in a section, in a few words, under its name on the rail; never a count (JL 261031: "Don't add N
        topics, N jobs, they are useless, they will change along the way")."""
        if key == "work":
            return f"its {below_names.get(level, 'items')}"
        if key == "studio":
            return "" if tag else "drawings, mind maps, slides"
        if key == "interactions":
            return ("🙋 waits on you" if any(r["state"] == "waiting" for r in inbox)
                    else "nothing waits on you" if inbox else "nothing asked yet")
        if key == "delivery" and not delivery:
            return "nothing handed over yet"
        return {"report": "read the results and check the progress", "delivery": "what it has handed over",
                "related": "what came in: meetings, papers, emails", "timeline": "what happened when",
                "files": "the folder itself"}.get(key, "")

    opens = "report" if overview and level == "Block" else "work"   # a Block is judged by its report; others by their Work
    section = section if section in {k for k, _, _ in rail} else opens
    groups = list(dict.fromkeys(t_ for _, _, f in topics for t_ in f["tags"]))   # no "All": one button per group
    if groups and any(not f["tags"] for _, _, f in topics):                     # (JL 261029); the ungrouped go last
        groups.append(OTHER)
    studio_views = {tag: (tag, None) for tag in groups}
    views = {"report": overview, "work": work, "interactions": asked, "delivery": dviews}.get(section, {})
    if section in views or section in ("report", "work", "interactions") or (section == "delivery" and dviews):
        view = group if group in views else draft["open"] if section == "work" and draft \
            else "text" if section == "report" and draft \
            else next(iter(views)) if (paper and level == "Block") or (theme.name == "insight" and level in ("Block", "Job", "Task")) \
            else next((k for k in (("standing", "findings", "mindmap") if section == "work" else ("mindmap", "findings", "standing"))
                       if k in views), next(iter(views)))   # HOOK: a paper Board opens on its first part
        selected = next(r for r in rail if r[0] == section)
        label, body = views[view]
        body = body() if callable(body) else body           # MindMap, Blocks, Status: built only when opened
        caption = (look.get("captions") or {}).get(view) or ("" if theme.name == "insight" and level in ("Block", "Job", "Task")
                                                             and view != "mindmap" else VIEW_WORDS.get(view, ""))   # its letters carry their own
        if theme.name == "work" and level == "Block" and view == "findings":
            caption = "What it has found so far, and what it hands over."
        body = (f'<p class="view-caption">{frame.esc(caption)}</p>' if caption else "") + body
        words = draft.get("words", {}) if section == "work" else {}   # a draft step's state word on its button
        bar = ('<nav class="section-views" aria-label="Views">' + "".join(
            f'<a href="{frame.esc(page_url(folder, root, section, key))}"' + (' aria-current="page"' if key == view else '')
            + f'>{frame.esc(name)}' + (f'<span class="vw {words[key][1]}">{frame.esc(words[key][0])}</span>' if key in words else '')
            + '</a>' for key, (name, _) in views.items()) + '</nav>')   # one view too: the bar is always there
        head = section.title()
    else:
        selected = next(r for r in rail if r[0] == section)
        selected = (selected[0], selected[1], (group if group in studio_views else next(iter(studio_views), ""))
                    if section == "studio" else "")
        # the Studio's topic groups are its views: the bar above the Purpose, as every section's (JL 261031, b10 r01
        # Q1: "if it is the view based, we will put it above the Purpose"; it was under the Purpose before)
        groups_nav = ('<nav class="section-views studio-groups" aria-label="Views">' + "".join(
            f'<a href="{frame.esc(page_url(folder, root, "studio", key))}"' + (' aria-current="page"' if key == selected[2] else '')
            + f'>{frame.esc(name)}</a>' for key, (name, _) in studio_views.items()) + '</nav>') \
            if section == "studio" and studio_views else ""
        # a section with one view keeps its bar too, one button naming it, so the Purpose never moves (JL 261031)
        one = {"studio": "Topics", "delivery": "Deliveries", "related": "Related", "files": "Folder",
               "timeline": "Timeline"}[section]
        bar = groups_nav or (f'<nav class="section-views" aria-label="Views"><a href="{frame.esc(page_url(folder, root, section))}"'
                             f' aria-current="page">{one}</a></nav>')
        body = {"studio": lambda: (draft["studio_top"]() if draft else "") + studio_html(topics, root, selected[2], card_interactions(folder, root)), "delivery": lambda: (delivery() if callable(delivery) else delivery) or '<p class="mut">Nothing handed over yet: a delivery lands in this folder\'s <code>delivery/</code> once it is agreed.</p>',
                "related": lambda: related, "files": lambda: folder_html(folder, root),
                "timeline": lambda: timeline_html(events, folder, root)}[section]()
        head = section.title()

    if section in ("report", "work") and page_level(folder) in IX.LEVELS:   # 🙋 Interaction closes each view (JL 261104)
        body += IX.view_section(inbox, root, IX.next_number(body), lambda r: interaction_where(r, folder, root))

    sub_line = describe(section, selected[2])
    if look:                                             # HOOK: a draft or paper page's own look (width, sections), every
        body = look["css"] + body                        # section; no verb beside its name (JL 261031, b10 r01 Q2)

    if page_level(folder) in ("Job", "Task"):          # a Job's or a Task's siblings include its level's sNN
        siblings = rail_kids(folder.parent, root)
    else:
        siblings = sorted(q for q in folder.parent.iterdir() if q.is_dir() and not q.name.startswith((".", "_"))
                          and inside(q, root) and page_level(q) == page_level(folder)) if folder != root else [folder]
    left = []
    for sibling in siblings:                             # siblings, with the open page's children under it
        left.append(rail_link(rail_url(sibling, root), sibling.name, sibling == folder))
        if sibling == folder:                            # its children, and under a Theme or a folder of Projects
            for child in rail_kids(folder, root):        # their own children too (JL 261029: "show the blocks")
                if not inside(child, root):
                    continue
                left.append(rail_link(rail_url(child, root), child.name, False, "child"))
                if page_level(child) in ("Theme", "Folder"):
                    left += [rail_link(page_url(g, root), g.name, False, "child grand") for g in kids(child) if inside(g, root)]
    def rail_view(key, tag=""):
        """A paper Board's Report and Work share one view list: moving between them stays in the view (JL 261104: "When
        I switch from Report to Work, could I still stay in the same view")."""
        if paper and level == "Block" and key in ("report", "work") and section in ("report", "work") and group:
            base = group.removeprefix("work-")
            target, there = ("work-" + base, work) if key == "work" else (base, overview)
            return target if target in there else tag
        return tag

    right = "".join(rail_link(page_url(folder, root, key, rail_view(key, tag)), name, (key, name, tag) == selected,
                              "", describe(key, tag)) for key, name, tag in rail)
    crumbs, cur = ([frame._link("/", root.name)] if folder != root else []), root   # the path starts at the SPACE (rule 1)
    for part in folder.relative_to(root).parts[:-1]:
        cur /= part
        crumbs.append(frame._link(page_url(cur, root), part))
    if folder != root:                                   # the path ends where you are (JL 261029)
        crumbs.append(f'<span aria-current="page">{frame.esc(folder.name)}</span>')
    goal = data["goal"].split("\n")[0] if data["goal"] else draft.get("aim", "")
    try:                                    # a theme may spell a goal id in words (design: G01 → its aim; look rule 5)
        from live import design_focus as _DF
        goal = _DF.goal_line(folder, goal) or goal
    except Exception:  # noqa: BLE001 -- a theme's words never break the base page
        pass
    source = frame.pop(frame.reader(data["face"], root), "Source Markdown", "Open this page's Markdown") if data["face"] and inside(data["face"], root) else ""
    goal_html = (f'<div class="focus-goal"><span class="goal-word">{GOAL_WORD.get(page_level(folder), "Goal")}</span>'
                 f'{markdown(goal, folder, root)}</div>' if goal else '')
    return page_shell(folder, root, crumbs, frame.esc(folder.name), head, sub_line, bar, goal_html, body, source,
                      left, right, [(key, name, rail_view(key)) for key, name, tag in rail if not tag], section)


def rail_kids(folder: Path, root: Path) -> list:
    """The pages one level down in the left rail: a Block's or a Job's sNN first, then its Jobs or Tasks, since an sNN
    sits beside them at the same level (JL 261030: "you should show the sNN as well, they are in the same level now");
    any other level, its kids()."""
    topics = [t for t, _ in frame._studio_topics(folder) if is_topic(t) and inside(t, root)] \
        if page_level(folder) in ("Block", "Job", "Task") else []
    return topics + [k for k in kids(folder) if inside(k, root)]


def rail_link(href, name, current, cls="", desc=""):
    return (f'<a href="{frame.esc(href)}" aria-label="{frame.esc(name)}"' + (' aria-current="page"' if current else '')
            + (f' class="{cls}"' if cls else '') + f'><i aria-hidden="true"></i><span class="rail-name">{frame.esc(name)}'
            + (f'<small>{frame.esc(desc)}</small>' if desc else '') + '</span></a>')


def page_shell(folder, root, crumbs, title_html, head, sub_line, bar, goal_html, body, source, left, right, rail, section):
    """The one page every level shares: path, title with its section, its views, the goal, the card, both rails."""
    card = f'<section class="focus-card"><div class="focus-content">{body}</div></section>'
    sections_line = ('<nav class="section-line" aria-label="Sections">' + "".join(   # phones only (600px or less, where the rails hide): the rail as tabs (JL 261031)
        f'<a href="{frame.esc(page_url(folder, root, key, view))}"' + (' aria-current="page"' if key == section else '')
        + f'>{frame.esc(name)}</a>' for key, name, view in rail) + '</nav>')
    # JL 261029 sketch: "Project-PageParts  Overview" as the title; under it, the views of that section; then the goal
    return document(folder.name, '<main class="focus-page"><div class="focus-crumb">' + ' / '.join(crumbs) + '</div>'
                    f'<h1>{title_html}<span class="h1-section" title="{frame.esc(sub_line)}">{head}</span></h1>'
                    + sections_line + bar                    # the views, then the Purpose; no count line (JL 261031)
                    + goal_html
                    + card
                    + f'<footer>{source}</footer><nav class="focus-rail left" aria-label="Pages">{"".join(left)}</nav>'
                    f'<nav class="focus-rail right" aria-label="Page sections">{right}</nav></main>')


COMPACT_MAP = ('<style>.pm-folds{grid-template-columns:130px auto;gap:0 26px}.pm-folds .pm-root b{font-size:15px}.pm-folds .pm-root *{overflow-wrap:anywhere}'
               '.pm-folds .pm-para{grid-template-columns:150px auto;gap:0 26px}.pm-folds .pm-q{width:150px}.pm-role:empty{display:none}</style>')


def mindmap_document(path, root, compact=False):
    if not inside(path, root) or not path.is_file() or not path.name.endswith(".mindmap.md"):
        return ""
    body = frame.mindmap_module().fragment(path, frame.rel(path, root), editable=False,
                                         url_of=lambda p: frame._file_url(p, root) if inside(p, root) else "")
    return document(path.name, body + (COMPACT_MAP if compact else ""))   # narrow columns, for a map framed in a side tab


def document(title, body):
    assets = Path(__file__).parent / "focus-assets"
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{frame.esc(title)}</title><style>{(assets / "focus.css").read_text()}</style></head><body>'
            + body + '<dialog id="focus-viewer"><header><span data-viewer-title></span><span class=viewer-verbs><a data-viewer-go target=_top>Go to this page →</a><button type="button" data-close>Close</button></span></header>'
            '<iframe title="Content preview"></iframe></dialog>'
            f'<script>{(assets / "focus.js").read_text()}</script></body></html>')

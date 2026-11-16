"""The focus page's shared ground: a folder's face and level, its kids and links, short words, the page document."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from urllib.parse import quote, urlencode

import yaml

from live import frame, page_reader, task_questions


def inside(path: Path, root: Path) -> bool:
    return path.resolve().is_relative_to(root.resolve())


def read_face(folder: Path, root: Path) -> dict:
    """Read explicit sections and header fields; fenced examples are not metadata."""
    face = frame.face(folder) or (next((folder / n for n in ("project.md", "README.md") if (folder / n).is_file()), None)
                                  if page_level(folder) == "Project" else None)   # a Project's page: project.md (README.md, its old name)
    text = face.read_text(encoding="utf-8") if face and inside(face, root) else ""
    fields, sections, many = {}, {}, {}
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
            if field:
                value = field.group(2).strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                    value = value[1:-1]
                if field.group(1).startswith("ui-"):   # a theme's example pages: one line each kind (261105)
                    many.setdefault(field.group(1), []).append(value)
                fields.setdefault(field.group(1), value)
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
                goal=sections.get("goal") or field("goal") or field("spine") or field("develops")
                or (field("question") if not re.fullmatch(r"[A-Z]\d+", field("question")) else "") or mission,
                close=sections.get("completion criteria") or field("close"),
                takeaways=sections.get("takeaways", ""), home=field("home-section").casefold(),
                state=field("state"), overview_map=field("overview-map"),
                view=field("view"), topic_ref=field("for"), use_case=field("use-case"),
                ui={k: [v.strip() for v in many.get("ui-" + k, []) if v.strip() and v.strip().casefold() not in
                        {"open", "<open>", "none", "-", "null"}] for k in ("project", "block", "job", "task", "run")})


                # a theme Block's example pages (JL 261031), one line per kind of page at that level (JL 261105: "they are
                # all the task, but different UI")


UI_VIEWS = (("project", "Project UI"), ("block", "Block UI"), ("job", "Job UI"), ("task", "Task UI"), ("run", "Run UI"))


# the themes whose Block, Job and Task pages take the work shape (JL 261106: "the discovery and cowork will be very
# similar to the work"): Report MindMap · Status · Findings, Work the same views as ⚙️ Process then 📊 Results; each adds
# its own Findings parts through theme_parts
WORK_SHAPE = frozenset({"work", "discovery", "cowork"})


def page_module(theme: str, folder: Path, root: Path) -> tuple:
    """(module, prefix) that adds a page's own parts: a Question Book Block's (`board-kind: prototype`, the insight
    questions and their scripts, a work Block) insight's live.insight_focus with its `prototype_` functions (round 1, 261106: "should a Prototype get its own state words?");
    (None, "") otherwise."""
    import importlib
    block = frame.chain(folder, root).get("Block", folder)
    face = block / "board.md"
    kind = (re.search(r"(?m)^board-kind:\s*(\S+)", face.read_text(encoding="utf-8", errors="ignore")) or [None, ""])[1] \
        if face.is_file() else ""
    if kind != "prototype":                     # cowork and discovery take the shared frame (their modules are in _old/)
        return None, ""
    name, prefix = "insight_focus", "prototype_"
    try:
        return importlib.import_module(f"live.{name}"), prefix
    except ImportError:
        return None, ""


def _own(theme: str, folder: Path, root: Path, level: str, what: str) -> list:
    mod, prefix = page_module(theme, folder, root)
    fn = getattr(mod, prefix + what, None) if mod is not None else None
    if fn is None:
        return []
    try:
        return [tuple(x) for x in fn(folder, root, level) or []]
    except Exception as exc:                     # a part that fails says so in its own bar, the page still opens
        return [(f"⚠️ {theme.title()}", "error", f'<p class=mut>{frame.esc(type(exc).__name__)}: {frame.esc(str(exc))}</p>', "")]


def theme_parts(theme: str, folder: Path, root: Path, level: str) -> list:
    """A page's own Findings parts, shown before 📦 Delivery: [(title, word, html, waits)] from its page_module's
    `parts` (discovery: Papers, Evidence Bib, Synthesis; cowork: People, Messages, Next move; a Question Book: its questions
    by release, proposals, cuts); [] when it has none."""
    return _own(theme, folder, root, level, "parts")


def theme_status(theme: str, folder: Path, root: Path, level: str) -> list:
    """A page's own Status bars, in place of the shared ones, when its page_module's `status` returns any (a cowork Job,
    one line of work with no Tasks; a Question Book's releases and questions, by their state and sign); [] otherwise."""
    return _own(theme, folder, root, level, "status")


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


def report_path(row, folder, root):
    ref = task_questions.words(row.get('report'))
    path = (folder / ref).resolve() if ref else None
    return path if path and inside(path, root) and path.is_file() else None


def state_label(text: str) -> str:
    """A recorded state's label: the words before ' · ' (`🟡 RESULTS IN, UNREAD · r11 complete` -> its label)."""
    return text.split(" · ")[0].strip()


def said_word(state: str) -> str:
    """A face's written state as a row's short word: `⏸ ON HOLD · 26 of 28 Runs ok` -> `⏸ on hold`."""
    m = re.match(r"^([^A-Za-z0-9]*)(.*)$", state_label(state or ""))
    return f"{m.group(1).strip()} {m.group(2).strip().lower()}".strip() if m else ""


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


STATE_KINDS = (                                       # first match wins; read from the label's first clause
    ("🙋 waiting on you", r"waiting|your call|needs? (a )?(sign-in|decision)"),
    ("⏳ running", r"\brunning\b|in progress|\bactive\b"),   # a cowork Job's 🟡 ACTIVE (261106)
    ("partly done", r"\bpartial|partly|carried|\bbuilt\b|drawn|redrawn|results in|unread"),
    ("✅ done", r"\bcomplete|\bclosed\b|\bdone\b|\bran\b|generated|finished|(?<!not yet )\bsettled\b"),   # b51's ✅ SETTLED
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


def one_line(text: str, limit: int = 110) -> str:
    """The first clause of a goal: what a reader needs to choose a row; the whole goal lives on the page itself."""
    text = " ".join((text or "").split())
    # a period ends the clause only after a word, not inside an abbreviation (U.S., e.g., i.e.; JL 261111)
    m = re.match(r"(.+?)(?::\s|;\s|(?<![A-Z])(?<!\.[a-z])(?<!\b[a-z])\.\s|$)", text)
    first = (m.group(1) if m else text).strip().rstrip(".")
    return first if len(first) <= limit else first[:limit].rsplit(" ", 1)[0] + "…"


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


def is_run(folder: Path) -> bool:
    """A Run folder: runs/<run>/ under a Task, Job or Block, never a level of its own."""
    return folder.parent.name == "runs" and folder.is_dir() and frame.level_of(folder) is None


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


OTHER = "Other"                                                  # the Studio button for topics in no group


def in_group(facts: dict, group: str) -> bool:
    """A topic belongs to a Studio group button: its **Tags:** name it, or it has none and the button is Other."""
    return not group or (not facts["tags"] if group == OTHER else group in facts["tags"])


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


def face_title(face: Path) -> str:
    """A face's own short title, the words after ' · ' on its first line."""
    first = face.read_text(encoding="utf-8", errors="ignore").split("\n", 1)[0] if face.is_file() else ""
    return first.split(" · ", 1)[1].strip() if " · " in first else ""


def state_words(label: str) -> str:
    """`✅ CLOSED` -> `✅ closed`; no recorded state -> `⬜ no state`."""
    mark = re.match(r"^([^A-Za-z0-9]*)(.*)$", label or "")
    return f"{mark.group(1).strip()} {mark.group(2).strip().lower()}".strip() if label else "⬜ no state"


def page_title(page: Path) -> str:
    """A page's short title from its face (`t01_x · the main association` -> 'the main association'), else its name."""
    face = frame.face(page)
    return face_title(face) if face and face_title(face) else page.name


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


def document(title, body):
    assets = Path(__file__).parents[1] / "focus-assets"
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{frame.esc(title)}</title><link rel="icon" href="data:,">'   # no icon request, so no 404 (round 2)
            f'<style>{(assets / "focus.css").read_text()}</style></head><body>'
            + body + '<dialog id="focus-viewer"><header><span data-viewer-title></span><span class=viewer-verbs><a data-viewer-go target=_top>Go to this page →</a><button type="button" data-close>Close</button></span></header>'
            '<iframe title="Content preview"></iframe></dialog>'
            f'<script>{(assets / "focus.js").read_text()}</script></body></html>')


def owned_register(data, root, heading, key):
    """A face's own register under `heading` (Questions, Deliverables): its rows and any error, by task_questions."""
    text = task_questions.read(data['face'], root) if data['face'] else ''
    return task_questions.register(text, heading, key)


def interactions(folder, root):
    """Every interaction at this page or below; it lives in focus_interactions, kept here so old imports keep working."""
    from live import focus_interactions
    return focus_interactions.interactions(folder, root)

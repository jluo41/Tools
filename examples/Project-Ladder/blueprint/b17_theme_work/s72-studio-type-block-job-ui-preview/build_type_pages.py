"""Build the Block Job UI Preview type (s72) and its instances (s11-s14) to one layout (b17 traces 261127/1400-1955).

Top views, the same on the type and on every instance:
    Page-Job (job-rows, job-overview, job-tasks, job-findings) · Page-Task (task-rows, task-overview, task-runs,
    task-findings) · Job types (a tab per Job group, then per Job type) · Task types (the same for Tasks) ·
    QuickHtml (a tab per quick page) · Draw
The type's right side is each part's requirement (elements.md: what, must, from, why); an instance's is the real
thing: the live page with that part outlined, the types its example Block's faces name, its own files. How an
instance stands against the type is its own face's Checklist section (the side pane's Checklist reads it; this
script owns that whole section), one line
per part: ✅ shown, ❗ applies and is missing, — does not apply, 🙋 waits on a decision.

    python build_type_pages.py           write the type's delivery/*.html and studio-views.json, and each instance's
                                         studio-views.json, delivery/types/*.html and face Checklist section
    python build_type_pages.py --type-only [--check]   generate/check only this type, preserving instance files
    python build_type_pages.py --check   fail when a written file is stale, an instance lacks a part, or a view
                                         that was taken out (Delivery, Instances) is back
"""
from html import escape as esc
from pathlib import Path
from urllib.parse import urlencode
import json
import re
import sys

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parent
TYPE = HERE.name.split("-studio-type-", 1)[-1]             # the name hai-studio/gallery keeps this type under
ROOT = BLOCK.parents[3]                                    # the SPACE (…/examples/Project-Ladder/blueprint/<block>)
SCRIPTS = ROOT / "plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts"
sys.path.insert(0, str(SCRIPTS))
from type_requirements import page as requirement_page
from requirement_examples import render as example_render
from check_views import build as check_build
from host_paths import bootstrap
bootstrap()
from live.studio_types import elements_of

ROUTE = "/_board/workbench"
EX = "examples/Project-Ladder"
INSTANCES = {                                              # instance topic -> its example Block, one Job, one Task
    "s11-work-job-preview": (f"{EX}/work/b01_example_work", "j11_core_checks", "t02_value_ranges"),
    "s12-blueprint-job-preview": (f"{EX}/blueprint/b17_theme_work", "j12_side_pane", "t03_pane_speed"),
    "s13-cowork-job-preview": (f"{EX}/cowork/b01_example_cowork", "j01_data_access_request", None),
    "s14-discovery-job-preview": (f"{EX}/discovery/b01_example_discovery", "j01_policy_effect_inquiry", "t01_policy_prior_work"),
    "s15-knowledge-job-preview": (f"{EX}/knowledge/b18_a2ui_learning", "j01_interactive_card", "t01_fixed_input_messages"),
}
NO_TASK = {"s13-cowork-job-preview"}                       # a Block type with no Task level: the view stays, its right side says why
# the parts a live page really has (probed on 5623, 261127): a CoWork or Discovery page draws no Overview, Tasks or
# Findings band, so those tabs are left out there; whether such a page should have them is not decided (🙋)
ROWS_ONLY = {"s13-cowork-job-preview"}                    # its example pages draw the rows only
NOT_DRAWN = {"s14-discovery-job-preview": {"job-findings"}}   # a view its example page leaves out: nothing to show yet
JOB_TABS = (("job-rows", "jobs-rows,job-ttopics,job-subs"), ("job-overview", "view=overview"),
            ("job-tasks", "view=standing"), ("job-findings", "view=findings"))
TASK_TABS = (("task-rows", "job-ttopics,job-subs"), ("task-overview", "view=overview"),
             ("task-runs", "view=standing"), ("task-findings", "view=findings"))
VIEWS = ("Page-Job", "Page-Task", "Job types", "Task types", "QuickHtml", "Draw")
GONE = ("Delivery", "Instances")                           # top views taken out (trace 261127/1955); --check keeps them out
TABS = {"Page-Job": [t for t, _ in JOB_TABS], "Page-Task": [t for t, _ in TASK_TABS],
        "Job types": ["〈Job group type 1〉", "〈Job group type 2〉", "〈Job type 1〉", "〈Job type 2〉"],      # numbered slots: an
        "Task types": ["〈Task group type 1〉", "〈Task group type 2〉", "〈Task type 1〉", "〈Task type 2〉"]}  # instance has as many as its Block type pins
slot = lambda tab: re.sub(r" \d+〉$", "〉", tab)             # 〈Job type 2〉 -> 〈Job type〉, the element both slots stand for
FILE = {"〈Job group type〉": "job-group-type", "〈Job type〉": "job-type", "〈Task group type〉": "task-group-type", "〈Task type〉": "task-type"}
PAGES = {**{FILE.get(slot(t), t): slot(t) for v in TABS.values() for t in v},
         "quickhtml": "QuickHtml", "draw": "Draw"}          # built file -> element of elements.md

STYLE = """:root{color-scheme:light dark;--paper:#fff;--ink:#223047;--muted:#59677b;--line:#d9e2ee;--accent:#275f9f}
@media(prefers-color-scheme:dark){:root{--paper:#1b1c1f;--ink:#e8e8e6;--muted:#a0a09c;--line:#2c2e33;--accent:#91caff}}
body{margin:0;background:var(--paper);color:var(--ink);font:14px/1.65 system-ui,sans-serif}main{padding:22px;max-width:1080px;margin:auto}
h1{font-size:18px;margin:0 0 4px;color:var(--accent)}.what{margin:0 0 14px;font-size:15px}
h2{font-size:12px;font-weight:500;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin:16px 0 4px}
p{margin:0}ol{margin:0;padding-left:20px}li{margin:3px 0}code{font-size:12.5px;background:var(--line);border-radius:4px;padding:0 4px}
table{border-collapse:collapse;font-size:14px}th,td{padding:6px 14px;border-bottom:1px solid var(--line);text-align:center;vertical-align:top}
th{color:var(--muted);font-weight:500;font-size:12.5px}td:first-child,th:first-child{text-align:left}td span{cursor:help}
table.types td{text-align:left}table.types td:first-child{font-weight:600;white-space:nowrap}.none{color:var(--muted);font-weight:400}"""


def page(title: str, body: str) -> str:
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
            f'<title>{esc(title)}</title>\n<style>\n{STYLE}\n</style></head><body><main>\n{body}\n</main></body></html>\n')


def code(text: str) -> str:
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", esc(text))


# ── the type: each part's requirement, from elements.md ──

def elements() -> dict:
    """{name: {what, why, from, must: [..]}} from elements.md (the format of studio_types.elements_of, plus must:)."""
    return {el["name"]: el for el in elements_of(HERE)}


def rule_page(key: str) -> str:
    """One part's requirement: what it is, what an instance must show there, where it comes from, why."""
    name = PAGES[key]
    el = elements()[name]
    return requirement_page(el, example_render(HERE, el, ROOT))


def type_views() -> str:
    rel = lambda name: f"{HERE.relative_to(ROOT).as_posix()}/delivery/{name}.html"
    one = lambda view, key: {"name": view, "items": [{"name": view, "path": rel(key)}]}
    views = [{"name": v, "items": [{"name": t, "path": rel(FILE.get(slot(t), t))} for t in tabs]} for v, tabs in TABS.items()]
    views += [{"name": "QuickHtml", "items": [{"name": f"〈quick page {n}〉", "path": rel("quickhtml")} for n in (1, 2)]},   # a tab per proposal
              one("Draw", "draw")]
    data = json.loads((HERE / "studio-views.json").read_text())
    data.update(views=views, check_type=TYPE, check_layout="elements")
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


# ── an instance: the real thing under the same views and tabs ──

def face_value(face: Path, keys: tuple) -> str:
    try:
        head = face.read_text(encoding="utf-8", errors="ignore")[:3000]
    except OSError:
        return ""
    for key in keys:
        m = re.search(rf"(?m)^\*{{0,2}}{key}:\*{{0,2}}[ \t]*(\S.*?)[ \t]*$", head)
        if m:
            return m.group(1).strip("`'\" ")
    return ""


def name_of(folder: Path) -> str:
    key, _, rest = folder.name.replace("-", "_").partition("_")
    rest = rest.replace("_", " ").strip()
    return f"{key} · {rest[:1].upper()}{rest[1:]}" if rest else key


def bands(face: Path, letter: str) -> dict:
    """{decade digit: name} from a face's `bands:` line (`bands: j0N First version · j1N Second version`)."""
    line = face_value(face, ("bands",))
    return {m.group(1): m.group(2).strip() for m in re.finditer(rf"\b{letter}(\d)N\s+([^·,;]+)", line)}


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "none"


def pinned(block: Path) -> dict:
    """{level: {type: {for, holds}}} from the types.md whose `example:` is this Block (a Block Structure topic pins
    its Block type's four lists there, b17 trace 261127/1407); {} when no Block type pins it."""
    for path in sorted(BLOCK.parent.glob("*/s0[0-9]-*/types.md")):
        example, out, level, cur = "", {}, None, None
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("example:"):
                example = line.split(":", 1)[1].strip()
            elif line.startswith("## "):
                level, cur = line[3:].strip(), None
                out[level] = {}
            elif line.startswith("### ") and level:
                cur = out[level].setdefault(line[4:].strip(), {})
            elif cur is not None and re.match(r"^(for|holds):\s*\S", line):
                key, value = line.split(":", 1)
                cur[key] = value.strip()
        if example and (ROOT / example).resolve() == block.resolve():
            return out
    return {}


def type_tabs(block: Path, job: str, level: str) -> list:
    """[(tab label, file stem, page)] for an instance's Job types (or Task types) view: one tab per group, then one
    per type; a tab's page lists its Jobs (Tasks) with the other fact beside each."""
    jobs = sorted(p for p in block.glob("j[0-9][0-9][_-]*") if p.is_dir())
    word = "Job" if level == "job" else "Task"
    if level == "job":
        names = bands(block / "board.md", "j")
        rows = [(name_of(j), j.name[1], face_value(j / f"{j.name}.md", ("job-type", "job-kind", "kind")), "") for j in jobs]
        grouped = rows
    else:
        tasks = [(t, j) for j in jobs for t in sorted(p for p in j.glob("t[0-9][0-9][_-]*") if p.is_dir())]
        rows = [(name_of(t), t.name[1], face_value(t / f"{t.name}.md", ("task-type", "task-kind", "type")), j.name) for t, j in tasks]
        names = bands(block / job / f"{job}.md", "t")
        grouped = [r for r in rows if r[3] == job]            # Task groups are the example Job's own
    letter = word[0].lower()
    group_name = lambda d: names.get(d) or f"{letter}{d}N"
    none = "<span class=none>no type</span>"

    def table(items, second, cell):
        body = "".join(f"<tr><td>{esc(n)}</td><td>{cell(n, d, k, own)}</td></tr>" for n, d, k, own in items)
        return f'<table class="types"><thead><tr><th>{word}</th><th>{second}</th></tr></thead><tbody>{body}</tbody></table>'

    lists = pinned(block)
    if lists:                                                # the pinned lists name the tabs; the faces fill them
        def about(d):
            return (f'<p class="what">{code(d.get("for", ""))}</p><h2>Holds</h2><p>{code(d.get("holds", ""))}</p><h2>{word}s</h2>')
        out = []
        for kind, d in lists.get(f"{word} group type", {}).items():   # for and holds only: no file says which group
            head = about(d).rsplit("<h2>", 1)[0]                      # is of which type, and a name is never guessed
            out.append((kind, f"{level}-group-type-{slug(kind)}", page(f"{block.name} · {kind}", f"<h1>{esc(kind)}</h1>" + head)))
        other = (lambda n, dd, k, own: esc(group_name(dd))) if level == "job" else (lambda n, dd, k, own: esc(own[:3]))
        known = lists.get(f"{word} type", {})
        for kind, d in known.items():
            items = [r for r in rows if r[2] == kind]
            out.append((kind, f"{level}-type-{slug(kind)}", page(f"{block.name} · {kind}", f"<h1>{esc(kind)}</h1>" + about(d)
                        + (table(items, "Job group" if level == "job" else "Job", other) if items else ""))))
        stray = [r for r in rows if r[2] not in known]
        if stray:                                            # a face naming no type, or one the list lacks
            out.append(("no type", f"{level}-type-none", page(f"{block.name} · no type", table(
                stray, f"{word} type", lambda n, dd, k, own: esc(k) if k else none))))
        return out
    out = []
    for d in sorted({r[1] for r in grouped}, reverse=level == "job"):          # Job groups newest first, as the page reads
        items = [r for r in grouped if r[1] == d]
        out.append((f"Group · {group_name(d)}", f"{level}-group-{d}",
                    page(f"{block.name} · {group_name(d)}", table(items, f"{word} type", lambda n, d, k, own: esc(k) if k else none))))
    for kind in sorted({r[2] for r in rows}, key=lambda k: (k == "", k)):
        items = [r for r in rows if r[2] == kind]
        other = (lambda n, d, k, own: esc(group_name(d))) if level == "job" else (lambda n, d, k, own: esc(own[:3]))
        out.append((f"Type · {kind or 'no type'}", f"{level}-type-{slug(kind)}",
                    page(f"{block.name} · {kind or 'no type'}", table(items, "Job group" if level == "job" else "Job", other))))
    return out


NO_LEVEL = "This Block type has no Task level, so a preview of it has nothing to show here."


def instance_parts(topic: Path) -> tuple:
    """(views, gaps) of one instance. An instance shows the type's views and Page tabs, all of them, in the type's
    order: the real thing where it has it, else the type's requirement for that part (faded), else why the part
    does not exist for its Block type. gaps: {part: (mark, why)} for every part that is not the real thing."""
    block, job, task = INSTANCES[topic.name]
    rel = topic.relative_to(ROOT).as_posix()
    rule = lambda name, key: {"name": name, "path": f"{HERE.relative_to(ROOT).as_posix()}/delivery/{key}.html", "old": True}
    none = lambda view: {"name": view, "path": f"{rel}/delivery/types/no-task-level.html", "old": True}
    in_block = {"path": block, "layout": "focus", "section": "jobs", **({"group": job[:3]} if job else {})}
    live = lambda query, mark: ROUTE + "?" + urlencode(query) + "&mark=" + mark
    views, gaps = [], {}

    def page_view(view, tabs, have, query, why):
        items = []
        for t, m in tabs:
            if have and (topic.name not in ROWS_ONLY or t.endswith("-rows")) and t not in NOT_DRAWN.get(topic.name, ()):
                items.append({"name": t, "url": live(query, m)})
            else:
                items.append(rule(t, t))
                gaps[f"{view} · {t}"] = ("🙋", "should a page of this Block type have it?") if have else ("❗", why)
        views.append({"name": view, "items": items})

    def types_view(view, level, have, why):
        tabs = type_tabs(ROOT / block, job, level) if have else []
        if tabs:
            views.append({"name": view, "items": [{"name": label, "path": f"{rel}/delivery/types/{stem}.html"} for label, stem, _ in tabs]})
        else:
            word = "Job" if level == "job" else "Task"
            views.append({"name": view, "items": [rule(f"〈{word} group type〉", f"{level}-group-type"), rule(f"〈{word} type〉", f"{level}-type")]})
            gaps[view] = ("❗", why)

    no_job, no_task = "the example Block has no Job yet", "the example Job has no Task yet"
    page_view("Page-Job", JOB_TABS, job, in_block, no_job)
    if topic.name in NO_TASK:
        views.append({"name": "Page-Task", "items": [none(t) for t, _ in TASK_TABS]})   # the type's four tabs, each the reason
        gaps["Page-Task"] = ("—", "this Block type has no Task level")
    else:
        page_view("Page-Task", TASK_TABS, task, dict(in_block, **({"task": task[:3]} if task else {})), no_task if job else no_job)
    types_view("Job types", "job", job, no_job)
    if topic.name in NO_TASK:
        views.append({"name": "Task types", "items": [none("Task types")]})
        gaps["Task types"] = ("—", "this Block type has no Task level")
    else:
        types_view("Task types", "task", task, no_task if job else no_job)
    html = topic / f"{topic.name}.html"
    text = html.read_text(encoding="utf-8", errors="ignore") if html.is_file() else ""
    quick = [{"name": label.strip(), "path": f"{rel}/{src}", **({"old": True} if 'class="old"' in attrs else {})}
             for attrs, src, label in re.findall(r'<button\b([^>]*\bdata-src="([^"/][^"]*)"[^>]*)>([^<]+)</button>', text)
             if (topic / src).is_file()]
    views.append({"name": "QuickHtml", "items": quick or [rule("〈quick page〉", "quickhtml")]})
    if not quick:
        gaps["QuickHtml"] = ("❗", "")
    draw = (topic / f"{topic.name}.excalidraw").is_file()
    views.append({"name": "Draw", "items": [{"name": "Draw", "path": f"{rel}/{topic.name}.excalidraw"} if draw else rule("Draw", "draw")]})
    if not draw:
        gaps["Draw"] = ("❗", "")
    return views, gaps


def instance_files(topic: Path) -> dict:
    """{path: text}: the instance's studio-views.json and its Check page, the Check view inherited from the type."""
    data = {"views": instance_parts(topic)[0], "check_type": TYPE, "check_layout": "elements"}
    return check_build(topic, data, ROOT)


def instances() -> list:
    """The topics of the type's band (its face's `band: s1N`), in number order."""
    band = re.search(r"(?m)^band:\s*s(\d)N\s*$", (HERE / f"{HERE.name}.md").read_text(encoding="utf-8"))
    return sorted(p for p in BLOCK.glob(f"s{band.group(1)}[0-9]-*") if p.is_dir()) if band else []


def checks(topic: Path) -> list:
    """[(mark, part, why)] for one instance against the type: ✅ the real thing is shown, ❗ applies and is missing,
    — does not apply, 🙋 waits on a decision."""
    block = INSTANCES[topic.name][0]
    views, gaps = instance_parts(topic)
    lists, out = pinned(ROOT / block), []
    for view in VIEWS:
        parts = [f"{view} · {t}" for t in TABS[view]] if view.startswith("Page-") and view not in gaps else [view]
        for part in parts:
            mark, why = gaps.get(part, ("✅", ""))
            out.append((mark, part, why))
        if view in ("Job types", "Task types") and view not in gaps:
            level = view.split()[0]
            out.append(("🙋", f"{view} · group types", f"no file says which {level} group is of which type") if lists
                       else ("🙋", f"{view} · pinned list", "this Block type pins no `types.md` yet"))
    return out


SECTION = re.compile(r"(?ms)^Checklist\n-{3,}\n.*?(?=^[^\n]+\n(?:-{3,}|={3,})\n|\Z)")   # the face's Checklist section, whole


def checklist(topic: Path) -> str:
    """The instance's face with its Checklist section rewritten: this script owns the whole section (a marker line
    inside it would show as text in the side pane), so a person's own check goes in another section."""
    text = (topic / f"{topic.name}.md").read_text(encoding="utf-8")
    lines = "\n".join(f"- {mark} {part}" + (f": {why}" if why else "") for mark, part, why in checks(topic))
    section = f"Checklist\n---------\n\n{lines}\n"
    if SECTION.search(text):
        return SECTION.sub(lambda m: section + ("\n" if m.end() < len(text) else ""), text, count=1)
    return text.rstrip("\n") + "\n\n" + section


def built(type_only: bool = False) -> dict:
    """{path: text} of every file this script owns."""
    out = {HERE / "delivery" / f"{key}.html": rule_page(key) for key in PAGES}
    out.update(check_build(HERE, json.loads(type_views()), ROOT))
    if type_only:
        return out
    for name, (block, job, task) in INSTANCES.items():
        topic = BLOCK / name
        if not topic.is_dir():
            continue
        for level in (("job", "task") if task else ("job",)) if job else ():
            for _, stem, text in type_tabs(ROOT / block, job, level):
                out[topic / "delivery" / "types" / f"{stem}.html"] = text
        if name in NO_TASK:
            out[topic / "delivery" / "types" / "no-task-level.html"] = page(f"{name} · no Task level", f'<p class="what">{NO_LEVEL}</p>')
        out.update(instance_files(topic))
        out[topic / f"{topic.name}.md"] = checklist(topic)
    return out


def main() -> int:
    type_only = "--type-only" in sys.argv
    files = built(type_only)
    if "--check" in sys.argv:
        stale = [p for p, text in files.items() if not p.is_file() or p.read_text(encoding="utf-8") != text]
        lacks = [] if type_only else [f"{t.name}: {part}" + (f" ({why})" if why else "") for t in instances() if t.name in INSTANCES
                                      for m, part, why in checks(t) if m == "❗"]
        back = [f"{p.parent.name}: {v['name']}" for p, text in files.items() if p.name == "studio-views.json"
                for v in json.loads(text)["views"] if v["name"] in GONE]
        back += [f"{HERE.name}: delivery/{n}.html" for n in ("delivery", "instances") if (HERE / "delivery" / f"{n}.html").is_file()]
        for line in ([f"stale: {p.relative_to(BLOCK)} (run build_type_pages.py)" for p in stale] + [f"lacks: {x}" for x in lacks]
                     + [f"taken out, back again: {x}" for x in back]):
            print("❗", line)
        bad = stale or lacks or back
        print("PASS" if not bad else f"{len(stale) + len(lacks) + len(back)} to fix")
        return 1 if bad else 0
    for _ in range(2):                                       # twice: a type page shows an example read from an
        for p, text in files.items():                        # instance's views, which this same run rewrites
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
        files = built(type_only)
    print(f"Built {len(files)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())

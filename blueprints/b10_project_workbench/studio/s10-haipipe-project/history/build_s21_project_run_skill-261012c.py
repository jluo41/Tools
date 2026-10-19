"""s21 · Project Run and skill: s21_project-run-skill.excalidraw, three frames (haipipe-studio 0.13.0: trees in
boxes, joined by named arrows, an emoji on every node; JL 261012: "so we can have both tree and box, and -->"):

    ① Background   a tree: the words and where the topic sits
    ② the Map      four level boxes (Block, Job, Task, Page Task), each a tree of its Spaces and buttons; skill
                   boxes; "runs" arrows from a level to the skills its buttons name; a red dashed arrow for the
                   skill no button names (haipipe-delivery, Open 1)
    ③ Reference    "Each skill is one folder in Tools/": servers, the base skills, the others, haipipe-report/
                   opened file by file, the themes; joined by "names", "opens", "sits over"

The structure is the `frames:` yaml in the face. A tree string starting "@" (for example "@level:Block") is
filled from disk here on every build: the buttons and their skills (servers/workbench/frame.py), each skill
folder's version, what it holds, which buttons name it, haipipe-report/ file by file. {braces} in a title,
why or label are counts read the same way. topic_map.draw_topic does the drawing; the person's marks are kept.
The 261007, 261012 and 261012b builders are in history/.

    python build_s21_project_run_skill.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDIO = HERE.parent                                      # b10's studio/
TOOLS = HERE.parents[3]                                   # s21 -> studio -> b10 -> blueprints -> Tools
ROOT = TOOLS                                              # frame_buttons() needs a folder under the root
SERVERS = TOOLS / "plugins" / "haipipe-toolkit" / "servers"
sys.path.insert(0, str(SERVERS / "_host"))
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
import canvas  # noqa: E402

TODAY = "261010"                                          # the date of the older notes; new ones carry their own
LEVELS = ("Block", "Job", "Task")
COLUMNS = ("Studio", "Description", "Report", "Work", "Runs", "Delivery")
SPACE_OF = {"Idea Studio": "Studio", "Audience Report": "Report", "Work Details": "Work"}  # the frame's Space names, as the buttons read
EXAMPLE = ("Job", "Report", "run-report-<qNN>")                        # the one press the story follows
T, SUB, BODY, HEAD, CODE = 34, 22, 22, 24, 20                          # frame title · line under it · words · box titles · paths


# ── facts, read from disk ───────────────────────────────────────────────────────────────────────
def frame_buttons():
    """{level: [(Space, Run, what it does, skills it names)]}: the base frame's buttons at Block, Job and Task,
    then the Page Task's (one row per button; a button on every sub-tab once)."""
    from host_paths import bootstrap
    bootstrap()
    from live import frame
    import re
    import tempfile
    spaces = ("Description", "Idea Studio", "Audience Report", "Work Details", "Runs", "Delivery")
    out = {}
    # a real Block › Job › Task, each with its face: a folder without a face gets no Description
    # button, which drew "? no button" (fixed 261010); the probe's tags read back as <bNN> <jNN> <tNN>
    with tempfile.TemporaryDirectory(dir=ROOT, prefix=".s21-probe-") as tmp:
        block = Path(tmp) / "b99_probe"
        folders = {"Block": block, "Job": block / "j99_probe", "Task": block / "j99_probe/t99_probe"}
        for f in folders.values():
            f.mkdir(parents=True)
            (f / f"{f.name}.md").write_text(f"# {f.name}\n", encoding="utf-8")
        tags = {"b99": "<bNN>", "j99": "<jNN>", "t99": "<tNN>"}
        for level in LEVELS:
            views = frame.spaces_for(frame.VANILLA, level, folders[level], ROOT)
            out[level] = [(space, re.sub(r"[bjt]99", lambda m: tags[m.group(0)], k["label"]), k.get("doing", ""),
                           " · ".join(k.get("skills") or []))
                          for space in spaces for k in views[space].run_types]
    page, seen = [], {}
    for space, subs in frame.DRAFT_TASK_SUBS.items():
        for sub in subs or ("",):
            for k in frame.draft_task_spaces(ROOT / "<tNN>", ROOT, sub)[space].run_types:
                if (space, k["label"]) in seen:
                    continue
                seen[(space, k["label"])] = len(page)
                page.append((space + (f" › {sub}" if sub else ""), k["label"], k.get("doing", ""),
                             " · ".join(k.get("skills") or [])))
    out["Page Task"] = page
    return out


def screen_rows():
    """The two button rows the frame draws today, as (label, picked) lists: the top row (Studio | Block · Job ·
    Task | Delivery) and the Spaces row, read from frame.render on this Block's Report Space."""
    import re
    from live import frame
    page = frame.render(frame.VANILLA, ROOT, STUDIO.parent, "Audience Report")
    rows = []
    for cls in ("levels", "spaces"):
        m = re.search(r'<nav class="row ' + cls + r'"[^>]*>(.*?)</nav>', page, re.S)
        row = []                                  # a tab, a dropdown's first option, or a divider
        for tag in re.findall(r'<a [^>]*>[^<]*</a>|<button[^>]*>[^<]*</button>|<select[^>]*><option>[^<]*|<span class=bar>',
                              m.group(1) if m else ""):
            label = re.sub(r"<[^>]*>", "", tag).strip()
            row.append(("|", False) if "class=bar" in tag else (label, False))
        rows.append(row)
    return rows


def column(space):
    head = space.split(" › ")[0]
    return SPACE_OF.get(head, head)


def grid_cells(buttons):
    """{(level, column): [skills]} in first-seen order."""
    cells = {}
    for level, rows in buttons.items():
        for space, _run, _doing, skills in rows:
            for s in skills.split(" · "):
                if s and s not in cells.setdefault((level, column(space)), []):
                    cells[(level, column(space))].append(s)
    return cells


# ── under ②: each skill is one folder in Tools/ (JL 261011) ─────────────────────────────────────
TOOLKIT = TOOLS / "plugins" / "haipipe-toolkit"
BASE_ORDER = ("haipipe-block", "haipipe-job", "haipipe-studio", "haipipe-report", "haipipe-run",
              "haipipe-delivery", "haipipe-project")                   # s21-D01's order; others after
OPENED = "haipipe-report"                                              # the example's skill, every file shown


def skill_dirs():
    """{name: folder}: every SKILL.md under the toolkit's skills/, by its folder's name."""
    out = {}
    for md in sorted((TOOLKIT / "skills").rglob("SKILL.md")):
        out.setdefault(md.parent.name, md.parent)
    return out


def skill_version(folder):
    import re
    m = re.search(r'^\s*version:\s*"?([\d.]+)', (folder / "SKILL.md").read_text(encoding="utf-8"), re.M)
    return m.group(1) if m else "?"


def skill_parts(folder):
    """'SKILL.md · ref 1 · scripts 2 · tests 1': what the folder holds, counted on disk."""
    def count(sub):
        d = folder / sub
        return len([p for p in d.iterdir() if p.is_file() and not p.name.startswith(".")]) if d.is_dir() else 0
    return " · ".join(["SKILL.md"] + [f"{sub} {count(sub)}" for sub in ("ref", "scripts", "tests") if count(sub)])


def used_by(name, buttons):
    """Where the frame's buttons name this skill: 'Studio, every level' or 'Block › Description · Work'."""
    at = {}
    for level, rows in buttons.items():
        for space, _run, _doing, skills in rows:
            if name in skills.split(" · ") and column(space) not in at.setdefault(level, []):
                at[level].append(column(space))
    at = {lv: cols for lv, cols in at.items() if cols}
    if not at:
        return ""
    cols = {tuple(c) for c in at.values()}
    if len(cols) == 1 and set(LEVELS) <= set(at):
        return f"{' · '.join(cols.pop())}, every level"
    return "  ".join(f"{lv} › {' · '.join(c)}" for lv, c in at.items() if lv in LEVELS) or \
        "  ".join(f"{lv} › {' · '.join(c)}" for lv, c in at.items())


ALIAS = {"build": "build the delivery", "check": "check the delivery"}   # the Page Task's short Delivery words


def button_rows(buttons):
    """One row per button across the levels: (column, what it does, its Runs, {level: skill}), in the
    order of the grid's columns, first seen first."""
    rows = {}
    for level, items in buttons.items():
        for space, run, doing, skills in items:
            col, does = column(space), ALIAS.get(doing.strip(), doing.strip())
            key = (col, does.lower())
            r = rows.setdefault(key, {"col": col, "does": does, "runs": [], "at": {}})
            if run not in r["runs"]:
                r["runs"].append(run)
            r["at"][level] = skills
    order = {c: i for i, c in enumerate(COLUMNS)}
    return sorted(rows.values(), key=lambda r: order.get(r["col"], 99))


def run_pattern(runs):
    """run-delivery-<bNN> · run-delivery-<jNN> … -> run-delivery-<bNN|jNN|…>: one name when they share a stem."""
    if len(runs) == 1:
        return runs[0]
    stems = {r.split("<", 1)[0] for r in runs}
    if len(stems) == 1 and all("<" in r for r in runs):
        return stems.pop() + "<" + "|".join(r.split("<", 1)[1].rstrip(">") for r in runs) + ">"
    return " · ".join(runs)






# ── the face's yaml, filled from disk ─────────────────────────────────────────────────────────────
import topic_map  # noqa: E402

SPACE_EMOJI = {"Description": "📄", "Idea Studio": "🗂️", "Audience Report": "📊", "Work Details": "🛠️",
               "Runs": "▶️", "Delivery": "📤"}
SHORT = lambda s: s.replace("haipipe-", "")  # noqa: E731


def level_tree(buttons, level):
    """One leaf per button: 'Space emoji, what it does, then the skill' (red when no skill is named). A Page
    Task's buttons that share a skill share a leaf, to keep its box short."""
    out = []
    for space, _run, doing, skills in buttons[level]:
        head = space.split(" › ")[0]
        what = ALIAS.get(doing.strip(), doing.strip()).split(" (")[0].split(" · ")[0].replace(
            "bind / update ", "bind ").replace("build figure / table", "build a figure")
        sk = SHORT(skills)
        if level == "Page Task":
            sk = sk.replace("draft-", "")
        out.append((SPACE_EMOJI.get(head, "•") if skills else "❓", what, sk if skills else "no skill named"))
    if level == "Page Task":
        grouped = {}
        for em, what, sk in out:
            grouped.setdefault((em, sk), []).append(what)
        return [f"{em} {' · '.join(w)} → {sk}" for (em, sk), w in grouped.items()]
    return [f"{em} {what} → {sk}" for em, what, sk in out]


def skills_tree(buttons, names, brief=False):
    """Each named skill: its version and the buttons that name it, read from disk."""
    dirs = skill_dirs()
    out = []
    for n in names:
        if n not in dirs:
            out.append(f"❓ {n}: no folder found")
            continue
        where = used_by(n, buttons)
        if brief:
            out.append(f"🧰 {SHORT(n)} {skill_version(dirs[n])}")
        elif where:
            out.append(f"🧰 {SHORT(n)} {skill_version(dirs[n])}: {where}")
        else:
            out.append(f"❓ {SHORT(n)} {skill_version(dirs[n])}: no button names it")
    return out


def named_skills(buttons):
    return sorted({s for rows in buttons.values() for r in rows for s in r[3].split(" · ") if s})


def tools_tree(buttons, part):
    dirs = skill_dirs()
    named = set(named_skills(buttons))
    project = TOOLKIT / "skills/1_base/project"
    if part == "servers":
        servers = sorted(d.name for d in (TOOLKIT / "servers").iterdir() if d.name.startswith("workbench-"))
        n = sum(len(r) for r in buttons.values())
        return [f"✅ workbench/frame.py: draws the buttons; each names its skill ({n})",
                "✅ workbench/runs_panel.py: the Runs panel beside each Space",
                f"🎨 workbench-<theme>/: a theme's frame over the base, {len(servers)}"]
    if part == "base":
        base = sorted((d for d in project.iterdir() if (d / "SKILL.md").is_file()),
                      key=lambda d: (BASE_ORDER.index(d.name) if d.name in BASE_ORDER else 99, d.name))
        out = []
        for d in base:
            where = used_by(d.name, buttons)
            mark = "🧰" if where else ("❓" if d.name == "haipipe-delivery" else "⬜")
            out.append(f"{mark} {SHORT(d.name)} {skill_version(d)}: {skill_parts(d)}")
        return out
    if part == "others":
        out = []
        homes = {}
        for s in sorted(named - {d.name for d in project.iterdir()}):
            homes.setdefault(dirs[s].parent, []).append(s)
        for home, names in sorted(homes.items(), key=lambda h: (-len(h[1]), str(h[0]))):
            rel = home.relative_to(TOOLKIT).as_posix()
            if len(names) > 1:
                out.append(f"📦 {rel.split('1_base/')[1]}/: " + ", ".join(
                    f"{SHORT(n)} {skill_version(dirs[n])}" for n in names))
            else:
                d = dirs[names[0]]
                out.append(f"🧰 {rel.split('1_base/')[1]}/{d.name}/ {skill_version(d)}: {skill_parts(d)}")
        return out
    if part == "report":
        folder = dirs[OPENED]
        kinds = {"SKILL.md": "what it owns; Claude reads it first", "CHANGELOG.md": "what each version changed",
                 "agents": "its name and prompt for Codex", "ref": "the full contract, read when needed",
                 "scripts": "code a Run calls", "tests": "checks the scripts"}
        files = sorted((p for p in folder.rglob("*") if p.is_file() and not any(
            q.startswith(".") or q == "__pycache__" for q in p.relative_to(folder).parts)),
            key=lambda p: (p.name != "SKILL.md", len(p.relative_to(folder).parts), p.relative_to(folder).as_posix()))
        return [f"📝 {p.relative_to(folder).as_posix()}: {kinds.get(p.relative_to(folder).parts[0], '')}"
                for p in files]
    if part == "themes":
        themes = sorted(d.name for d in (TOOLKIT / "skills/2_theme").iterdir() if d.is_dir())
        return ["🎨 " + " · ".join(themes)]
    return []


def expand(node, buttons):
    """A tree string '@level:Block' / '@skills:a,b' / '@tools:base' becomes its list; dict keys and children recurse."""
    if isinstance(node, dict):
        return {k: _flat(v, buttons) for k, v in node.items()}
    return node


def _flat(nodes, buttons):
    out = []
    for n in nodes or []:
        if isinstance(n, str) and n.startswith("@"):
            kind, _, arg = n[1:].partition(":")
            if kind == "level":
                out += level_tree(buttons, arg)
            elif kind in ("skills", "skillsb"):
                out += skills_tree(buttons, arg.split(","), kind == "skillsb")
            elif kind == "tools":
                out += tools_tree(buttons, arg)
        else:
            out.append(expand(n, buttons))
    return out


class _Facts(dict):
    def __missing__(self, key):
        return "{" + key + "}"


def facts(buttons):
    pt = {s for _, _, _, sk in buttons["Page Task"] for s in sk.split(" · ") if s}
    return _Facts(total=sum(len(r) for r in buttons.values()),
                  named=sum(1 for r in buttons.values() for b in r if b[3]),
                  nskills=len(named_skills(buttons)),
                  nblock=len(buttons["Block"]), njob=len(buttons["Job"]), ntask=len(buttons["Task"]),
                  npage=len(buttons["Page Task"]), npagesk=len(pt))


def fill(frames, buttons):
    f = facts(buttons)
    sub = lambda s: s.format_map(f) if isinstance(s, str) else s  # noqa: E731

    def walk(n):
        if isinstance(n, dict):
            return {sub(k): [walk(c) for c in v] for k, v in n.items()}
        return sub(n)
    out = []
    for fr in frames:
        fr = dict(fr)
        for k in ("title", "intro"):
            if k in fr:
                fr[k] = sub(fr[k])
        if fr.get("tree"):
            fr["tree"] = [walk(n) for n in _flat(fr["tree"], buttons)]
        boxes = []
        for b in fr.get("boxes") or []:
            b = dict(b)
            b["title"], b["why"] = sub(b.get("title", "")), sub(b.get("why", ""))
            b["tree"] = [walk(n) for n in _flat(b.get("tree"), buttons)]
            boxes.append(b)
        if boxes:
            fr["boxes"] = boxes
            fr["arrows"] = [dict(a, label=sub(a.get("label", ""))) for a in fr.get("arrows") or []]
        out.append(fr)
    return out


def main():
    folder = HERE
    buttons = frame_buttons()
    topic_map.draw_topic(folder, source="build_s21_project_run_skill.py",
                         fill=lambda frames: fill(frames, buttons))   # the @ lines, read from disk


if __name__ == "__main__":
    main()

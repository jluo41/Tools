"""s10 · haipipe-project: s10-haipipe-project.excalidraw, the skill in three acts, on excalidraw-studio's draw.py (JL
261012: "could we merge s21 and s10? I think we need to rename it to s10_haipipe-project ... to explain this skill,
cuold you use /excalidraw-studio to describe it?").

Every word is the face's `drawing:` yaml; the skill folders, their versions and the base frame's Run buttons are read
from disk on every build. Written through canvas.write (Drawing.write), so a person's marks survive a rebuild.

    python build_s10_haipipe_project.py
"""
import re
import sys
import tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]                                   # s10 -> studio -> b10 -> blueprints -> Tools
TOOLKIT = TOOLS / "plugins" / "haipipe-toolkit"
FAMILY = TOOLKIT / "skills" / "1_base" / "project"        # haipipe-project and the level skills beside it
sys.path.insert(0, str(TOOLKIT / "skills" / "1_base" / "excalidraw" / "excalidraw-studio" / "scripts"))
sys.path.insert(0, str(TOOLKIT / "servers" / "_host"))
from draw import RED, T_SMALL, W, Drawing, canvas  # noqa: E402

LEVELS = ("Block", "Job", "Task")
SPACES = ("Description", "Idea Studio", "Audience Report", "Work Details", "Runs", "Delivery")
SHORT = {"Idea Studio": "Studio", "Audience Report": "Report", "Work Details": "Work"}
MARK = {"haipipe-block": "🧱", "haipipe-job": "📋", "haipipe-task": "🔧", "haipipe-studio": "🧠",
        "haipipe-report": "📝", "haipipe-run": "🏃", "haipipe-project": "🏗️", "haipipe-delivery": "📤"}


def words():
    text = (HERE / f"{HERE.name}.md").read_text(encoding="utf-8")
    return yaml.safe_load(re.search(r"```yaml\n(drawing:.*?)\n```", text, re.S).group(1))["drawing"]


def version(folder):
    if not (folder / "SKILL.md").is_file():                # a skill outside the family: found by its name
        hits = sorted((TOOLKIT / "skills").rglob(f"{folder.name}/SKILL.md"))
        if not hits:
            return "?"
        folder = hits[0].parent
    m = re.search(r'^\s*version:\s*"?([\d.]+)', (folder / "SKILL.md").read_text(encoding="utf-8"), re.M)
    return m.group(1) if m else "?"


def parts(folder):
    """'fn 6 · ref 3 · scripts 6 · tests 1': what a skill folder holds beside its SKILL.md, counted on disk."""
    def count(sub):
        d = folder / sub
        return len([p for p in d.iterdir() if p.is_file() and not p.name.startswith(".")]) if d.is_dir() else 0
    return " · ".join([f"{sub} {count(sub)}" for sub in ("fn", "ref", "scripts", "tests") if count(sub)]) or "SKILL.md only"


def buttons():
    """[(level, Space, [skills])]: every Run button of the base frame at Block, Job and Task, then the Page Task's
    (each button once), read through the frame itself (s21's reading, 261010)."""
    from host_paths import bootstrap
    bootstrap()
    from live import frame, task_draft
    out = []
    with tempfile.TemporaryDirectory(dir=TOOLS, prefix=".s10-probe-") as tmp:
        block = Path(tmp) / "b99_probe"                   # a real Block › Job › Task, each with its face
        folders = {"Block": block, "Job": block / "j99_probe", "Task": block / "j99_probe/t99_probe"}
        for f in folders.values():
            f.mkdir(parents=True)
            (f / f"{f.name}.md").write_text(f"# {f.name}\n", encoding="utf-8")
        for level in LEVELS:
            views = frame.spaces_for(frame.VANILLA, level, folders[level], TOOLS)
            out += [(level, SHORT.get(s, s), list(k.get("skills") or [])) for s in SPACES if s in views
                    for k in views[s].run_types]
    seen = set()
    for space, subs in task_draft.DRAFT_TASK_SUBS.items():
        for sub in subs or ("",):
            for k in task_draft.draft_task_spaces(TOOLS / "<tNN>", TOOLS, sub)[space].run_types:
                if (space, k["label"]) not in seen:
                    seen.add((space, k["label"]))
                    out.append(("Page Task", SHORT.get(space, space), list(k.get("skills") or [])))
    return out


def where(name, rows):
    """Where the buttons name a skill: 'Studio at every level' or 'Block: Description · Work'."""
    at = {}
    for level, space, skills in rows:
        if name in skills and space not in at.setdefault(level, []):
            at[level].append(space)
    at = {lv: sp for lv, sp in at.items() if sp}
    if not at:
        return ["❓ no button names it yet"]
    same = {tuple(sp) for lv, sp in at.items() if lv in LEVELS}
    if len(same) == 1 and all(lv in at for lv in LEVELS):
        return [f"{' · '.join(next(iter(same)))} at every level"] + \
            [f"{lv}: {' · '.join(sp)}" for lv, sp in at.items() if lv not in LEVELS]
    return [f"{lv}: {' · '.join(sp)}" for lv, sp in at.items()]


def note(d, x, y, what):
    """A short green change note where the drawing changed (haipipe-studio, Change notes)."""
    e = canvas.change_note(x, y, what, "261012", d.fid, 20)
    d.els.append(e)


def root_frame(d, w):
    f = d.frame(w["title"])
    d.heading(w["title"], w["sub"])
    note(d, 40, 172, "s10 and s21 merged into s10-haipipe-project, drawn with excalidraw-studio")
    ver = version(FAMILY / "haipipe-project")
    bottom = d.mind_map(w["centre"].format(skill=f"haipipe-project {ver}"), w["branches"], top=226)
    f["height"] = bottom + 60
    d.badge(f)
    return f


def folder_frame(d, w):
    f = d.frame(w["title"])
    d.heading(w["title"], w["sub"])
    d.key(40, 190, W - 80, 96)
    d.para(66, 214, w["key"], W - 132, 28)
    own = Drawing.folder_tree(FAMILY / "haipipe-project", open_=("fn", "ref", "scripts", "tests"), most=8,
                              notes=w["notes"])
    d.text(40, 330, "📁 the skill, opened", 34)
    left = d.text(40, 386, "\n".join(own), 22, code=True)
    family = ["skills/1_base/project/"]
    kids = sorted(p for p in FAMILY.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())
    for i, p in enumerate(kids):
        mark = "  ◀ this topic" if p.name == "haipipe-project" else ""
        family.append(f"{'└──' if i == len(kids) - 1 else '├──'} {p.name + '/':<19} {version(p):<7} {parts(p)}{mark}")
    d.text(1330, 330, "🧩 its family, side by side", 34)
    right = d.text(1330, 386, "\n".join(family), 22, code=True)
    fy = right["y"] + right["height"] + 150                # how one command runs through the folder
    d.text(1330, fy - 76, w["flow_title"], 34)
    steps = d.flow(w["flow"], 1330, fy, W - 1370, labels=w["flow_labels"], title=26)
    pick = right["y"] + 22 * 1.25 * (1 + [p.name for p in kids].index("haipipe-project")) + 14
    sx, sy, sw, _ = steps[0]
    d.line([(1320, pick), (1300, pick), (1300, sy + 40), (sx - 6, sy + 40)], sw=2)
    bottom = max(left["y"] + left["height"], max(y + h for _, y, _, h in steps))
    f["height"] = bottom + 60
    d.badge(f)
    return f


def update_frame(d, w):
    f = d.frame(w["title"])
    d.heading(w["title"], w["sub"])
    steps = d.flow(w["steps"], 40, 230, W - 80, labels=w["labels"])
    sx, sy, sw, sh = steps[5]                             # 6 · Questions: the proposals wait for a person
    ly = sy + sh + 150
    loop = d.flow(w["loop"], 420, ly, W - 840, labels=w["loop_labels"])
    lx, _, lw, lh = loop[0]
    mid = sy + sh + 70
    d.line([(sx + sw / 2, sy + sh + 6), (sx + sw / 2, mid), (lx + lw / 2, mid), (lx + lw / 2, ly - 6)], sw=3)
    d.text(lx + lw / 2 + 16, mid - 34, "proposals.md: tick the lines to keep", T_SMALL + 3)
    ex, ey, ew, eh = loop[-1]                             # the loop closes back on step 1
    fx, fy, fw, fh = steps[0]
    low = ey + eh + 60
    d.line([(ex + ew / 2, ey + eh + 6), (ex + ew / 2, low), (fx + fw / 2, low), (fx + fw / 2, fy + fh + 6)], sw=3)
    d.text(fx + fw / 2 + 16, low + 10, w["loop_back"], T_SMALL + 3)
    y = low + 70
    d.key(40, y, W - 80, 80)
    d.para(66, y + 20, "✅ " + w["result"], W - 132, 28)
    y += 110
    for point in w["open"]:
        y = d.para(40, y, point, W - 80, 24) + 10
    f["height"] = y + 50
    d.badge(f)
    return f


def buttons_frame(d, w):
    f = d.frame(w["title"])
    d.heading(w["title"], w["sub"])
    rows = buttons()
    named = sum(1 for r in rows if r[2])
    branches = []
    for name in w["skills"]:
        folder = FAMILY / name
        ver = version(folder)
        leaves = where(name, rows) + ([w["open"][name]] if name in w["open"] else [])
        branches.append({"title": f"{MARK.get(name, '🧩')} {name} {ver}", "summary": w["about"][name],
                         "leaves": leaves})
    by_level = " · ".join(f"{lv} {sum(1 for r in rows if r[0] == lv)}" for lv in (*LEVELS, "Page Task"))
    bottom = d.mind_map(f"{named} of {len(rows)} Run buttons name their skill ({by_level})", branches, top=226)
    f["height"] = bottom + 60
    d.badge(f)
    return f


def main():
    w = words()
    d = Drawing()
    frames = {"root": root_frame(d, w["root"]), "folder": folder_frame(d, w["folder"]),
              "update": update_frame(d, w["update"]), "buttons": buttons_frame(d, w["buttons"])}
    d.acts([{"name": a["name"], "frames": [frames[k]["id"] for k in a["frames"]], "arrow": a.get("arrow")}
            for a in w["acts"]],
           between=[(frames[a]["id"], frames[b]["id"], says) for a, b, says in w["between"]])
    out = HERE / f"{HERE.name}.excalidraw"
    d.write(out, "build_s10_haipipe_project.py")
    from render_png import render
    render(out, out.with_suffix(".png"))


if __name__ == "__main__":
    main()

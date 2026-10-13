"""s05 · Report: its workbench and its skill: s05-report-workbench-skill.excalidraw (haipipe-studio 0.13.0).

Three frames (JL 261012: "we can have both tree and box, and -->"): ① Background, a tree; ② the Report as boxes,
each with an emoji title, a why line and its own tree, joined by named arrows (studio feeds Question, Work answers
it, the report says the answer, the Space shows it, the skills write it); ③ the Report Space screen, in the
workbench's colours (canvas.ui_frame). ① and ② come from the face's `frames:` yaml, drawn by topic_map.draw_frames;
this builder splices into them what it reads from disk (the `{{...}}` leaves, `{nq}`, `{nj}`) and draws ③.
The 261012 builders are in history/ (-261012, -261012b).

Read from disk on every build: this Block's Questions (board.md ## Questions), each report's answer-status,
which studio topics feed each Question (their **Feeds:** lines, read as frame.py reads them), the Runs that
target a Question (runs/*/run.yaml), q01's ## Figures, the Report Space as servers/workbench/frame.py draws
it for this Block, and haipipe-report's version. Typed, since they are the design: the level tree of ①, the
link rule of ②, the walk of ③, the open points.

    python build_s05_report_workbench_skill.py [out.excalidraw]
"""
import re
import sys
import textwrap
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
STUDIO = HERE.parent                                      # b10's studio/
BLOCK = STUDIO.parent                                     # b10_project_workbench/
TOOLS = HERE.parents[3]                                   # s05 -> studio -> b10 -> blueprints -> Tools
ROOT = TOOLS
SERVERS = TOOLS / "plugins" / "haipipe-toolkit" / "servers"
SKILLS = TOOLS / "plugins/haipipe-toolkit/skills/1_base"
sys.path.insert(0, str(STUDIO / "s01-overall-tree-structure"))
sys.path.insert(0, str(SERVERS / "_host"))
import build_ladder_v4 as L  # noqa: E402  (the shared drawing helpers: base, text, path, frames)
sys.path.insert(0, str(SKILLS / "project/haipipe-studio/scripts"))
import canvas  # noqa: E402
import topic_map  # noqa: E402

TODAY = "261012"
EXAMPLE = "Q05"                                            # ②'s and ④'s row
FIGURES = "q01_bjtr_boundary"                              # ③'s report drawing
STATES = ("open", "partial", "answered")
T, SUB, BODY, HEAD, CODE = 34, 22, 22, 24, 20              # frame title · line under it · words · box titles · paths


# ── facts, read from disk ───────────────────────────────────────────────────────────────────────
def frame_module():
    from host_paths import bootstrap
    bootstrap()
    from live import frame
    return frame


def questions(frame):
    """[{id, title, report, status, fed, runs}] for every Question of this Block, in register order."""
    reports = {q.name.split("_", 1)[0].upper(): q / (q.name + ".md") for q in sorted((BLOCK / "reports").glob("q[0-9]*/"))}
    fed, unread = {}, []
    for topic, _drawings in frame._studio_topics(BLOCK):
        notes = frame._notes(topic)
        found = frame._note_facts(notes)["feeds"]
        for q in found:
            fed.setdefault(q.split("_", 1)[0].upper(), []).append(topic.name.split("-", 1)[0].split("_", 1)[0])
        line = re.search(r"\*\*Feeds:\*\*(.+)", notes.read_text(encoding="utf-8")) if notes else None
        if line and not found and re.search(r"\b[Qq]\d\d\b", line.group(1)):
            unread.append((topic.name.split("-", 1)[0], line.group(1).strip()))
    runs = {}
    for card in sorted((BLOCK / "runs").glob("*/run.yaml")):
        c = yaml.safe_load(card.read_text(encoding="utf-8")) or {}
        runs.setdefault(str(c.get("target") or "").upper(), []).append(c.get("run"))
    out = []
    for r in frame._register(frame.face(BLOCK)):
        qid = str(r["id"]).upper()
        page = (BLOCK / r["report"]) if r.get("report") and (BLOCK / r["report"]).is_file() else reports.get(qid)
        status = dict(frame._fields(page)).get("answer-status", "open") if page and page.is_file() else "open"
        out.append({"id": qid, "title": r.get("title") or "", "report": page, "status": status,
                    "fed": fed.get(qid, []), "runs": runs.get(qid, []),
                    "work": frame._answering(BLOCK, "Block", qid, ROOT) + list(r.get("work") or [])})
    return out, unread


def report_space(frame):
    """(third-row buttons, the open one, the row's three heads, Runs-panel buttons) of this Block's Report Space."""
    sp = frame.spaces_for(frame.VANILLA, "Block", BLOCK, ROOT)["Audience Report"]
    heads = re.findall(r'q-head-row"><div>(.*?)</div><div>(.*?)</div><div>(.*?)</div>', sp.html)
    buttons = [(k["label"], k.get("doing", ""), " · ".join(k.get("skills") or [])) for k in sp.run_types]
    return list(sp.subspaces), sp.open, list(heads[0]) if heads else [], buttons


def figures():
    """q01's ## Figures: [(topic folder, frame name)]."""
    text = (BLOCK / "reports" / FIGURES / f"{FIGURES}.md").read_text(encoding="utf-8")
    m = re.search(r"```ya?ml\n(figures:.*?)```", text, re.S)
    rows = (yaml.safe_load(m.group(1)) or {}).get("figures") or [] if m else []
    return [(Path(f["from"]).parent.name, f["frame"]) for f in rows]


def version(skill):
    m = re.search(r'version:\s*"([^"]+)"', (skill / "SKILL.md").read_text(encoding="utf-8"))
    return m.group(1) if m else "?"


# ── folder-tree helpers ──────────────────────────────────────────────────────────────────────────
def rect(x, y, w, h, bold=False, dashed=False):
    return L.base("rectangle", x, y, w, h, L.INK, 3 if bold else 1.5, dashed, rough=0)


def say(x, y, s, size=BODY, color=L.INK, font=L.SANS):
    L.text(x, y, s, size, color, font)
    return y + size * 1.3 * (s.count("\n") + 1)


def wrap(s, n):
    return "\n".join(textwrap.wrap(s, n))


def tree_frame(name, title, lines, nodes, width, cols):
    """One frame: a title, a line or two under it, then the folder tree (canvas.tree)."""
    fr = L.open_frame(name)
    L.text(0, 0, title, 34)
    y = 56
    for ln in lines:
        L.text(0, y, ln, 22)
        y += 32
    els, _ = canvas.tree(0, y + 8, nodes, width, fr["id"], size=20, head=24, cols=cols)
    L.els.extend(els)
    L.close_frame(fr)
    return fr


def skill_folder(skill):
    """A skill's folder as it is on disk: [name, {dir: [files]}] children for canvas.tree."""
    kids = []
    for p in sorted(skill.iterdir()):
        if p.name.startswith((".", "__")):
            continue
        if p.is_dir():
            kids.append({p.name + "/": [c.name for c in sorted(p.iterdir()) if not c.name.startswith((".", "__"))][:6]})
        else:
            kids.append(p.name)
    return kids


def where(fn, file):
    """'fn  (file)' when `def fn` is in the file, else a red ? leaf."""
    text = file.read_text(encoding="utf-8") if file.is_file() else ""
    return f"{fn}  ({file.name})" if re.search(rf"def {re.escape(fn)}\b", text) else f"? {fn} not found in {file.name}"


# ── ①, ②: the face's frames, with the facts from disk spliced in ───────────────────────────────────
def fills(qs, unread, space, versions):
    """{name: [nodes]} for the `{{name}}` leaves of the face's frames."""
    subs, opened, heads, buttons = space
    q = next(x for x in qs if x["id"] == EXAMPLE)
    emoji = {"open": "⬜", "partial": "🔶", "answered": "✅"}
    states = [{f"{emoji[st]} {st}  ({sum(1 for x in qs if x['status'] == st)})":
               [" ".join(x["id"] for x in qs if x["status"] == st)]} for st in STATES]
    fed = [f"🧠 {' · '.join(x['fed'])} feed {x['id']}" for x in qs if x["fed"]][:5]
    work = [{f"🧱 example {q['id']}": [
        "🧠 fed by: " + (" · ".join(q["fed"]) or "no topic"),
        "📋 Jobs and Tasks: " + (" · ".join(str(w) for w in q["work"]) or "none (no Jobs here)"),
        "🏃 Runs on it: " + (" · ".join(str(r) for r in q["runs"]) or "none"),
        "📝 report: " + (f"{q['report'].relative_to(BLOCK)} · {q['status']}" if q["report"] else "none")]}]
    fn = SERVERS / "workbench/frame.py"
    code = [("✅ " if "not found" not in (w := where(f, fn)) else "❓ ") + w for f in
            ("question_rows", "_report_cell", "_answering", "_opening")]
    code.append("✅ " + where("page_document", SERVERS / "workbench/page_reader.py"))
    for tag, text in unread:
        fed.append(f"❓ {tag}'s Feeds line ({text.strip('`. ')[:30]}) is not read")
    figs = [f"🖼️ {t}  >  \"{n}\"" for t, n in figures()]
    def folder(skill):                                       # a skill's folder as it is: its files, then its dirs
        parts = [p.name + ("/" if p.is_dir() else "") for p in sorted(skill.iterdir())
                 if not p.name.startswith((".", "__"))]
        return ["📄 " + " · ".join(x for x in parts if not x.endswith("/")),
                "📁 " + " · ".join(x for x in parts if x.endswith("/"))]
    skills = [{f"📝 haipipe-report  {versions['report']}": folder(SKILLS / "project/haipipe-report")},
              {f"📌 haipipe-question  {versions['question']}": folder(SKILLS / "question/haipipe-question")}]
    btn = [{"▶️ Runs panel buttons": [f"{b[0]}  ({b[2]})" for b in buttons]}]
    return {"states": states, "work": work, "code": code, "fed": fed, "figures": figs, "skills": skills,
            "buttons": btn}


def splice(nodes, tokens, facts):
    out = []
    for n in nodes:
        if isinstance(n, str):
            if n.startswith("{{") and n.endswith("}}"):
                out += facts.get(n[2:-2], [])
            else:
                for k, v in tokens.items():
                    n = n.replace("{" + k + "}", str(v))
                out.append(n)
        else:
            out.append({k: splice(v, tokens, facts) for k, v in n.items()})
    return out


def frames_from_face(facts, tokens):
    frames = topic_map.frames_of(HERE / f"{HERE.name}.md")
    for fr in frames:
        if fr.get("tree"):
            fr["tree"] = splice(fr["tree"], tokens, facts)
        for b in fr.get("boxes") or []:
            b["tree"] = splice(b.get("tree") or [], tokens, facts)
    return frames


# ── ③ the Report Space, as it looks ──────────────────────────────────────────────────────────────
def screen_frame(qs, frame):
    sp = frame.spaces_for(frame.VANILLA, "Block", BLOCK, ROOT)["Audience Report"]
    html = sp.html
    nav = re.search(r"<nav.*?</nav>", html, re.S)
    groups = re.findall(r'data-studio-label="([^"]+)"[^>]*>.*?</span>.*?<span class=tag-count>(\d+)</span>',
                        nav.group(0), re.S) if nav else []
    kinds = {n: ("fixed" if "grp-fixed" in c else "suggested" if "grp-suggested" in c else "")
             for c, n in re.findall(r'<button[^>]*class="([^"]*)"[^>]*data-studio-label="([^"]+)"', html)}
    cards = re.findall(r'<span class="q-dot (\w+)" title="\w+"></span><span class=related-head><b>(.*?)</b>'
                       r'.*?<span class=topic-meta>(.*?)</span>', html, re.S)
    fr = L.open_frame("The Report Space on screen")
    canvas.ui_frame(fr, since="261012")                      # a screen: the workbench's colours (JL 261012)
    say(0, 0, f"Block {BLOCK.name.split('_')[0]} > Report  (read from servers/workbench/frame.py)", 34)
    say(0, 56, "One card per Question under the group bar, at Block, Job and Task. Groups: white is the Block's own, "
        "gray fixed by the theme, amber suggested.", 22)
    x, y = 0, 120
    for label, n in groups + [("Untagged", ""), ("+ Group", "")]:
        t = f"{label} {n}".strip()
        w = int(len(t) * BODY * 0.58) + 40
        rect(x, y, w, 46, bold=label == "Current")
        if kinds.get(label):                                 # gray when fixed, amber when suggested (s07-D12)
            L.els[-1].setdefault("customData", {})["ui_kind"] = kinds[label]
        say(x + 20, y + 10, t, BODY)
        x += w + 12
    y += 80
    for dot, title, meta in cards[:6]:
        rect(0, y, 1500, 64)
        say(24, y + 8, f"{dot}   {title}", BODY)
        say(24, y + 36, re.sub("<.*?>", "", meta), 18, L.MONO and L.INK)
        y += 76
    say(0, y + 4, f"... {len(cards)} cards in all; Q05 opened below", BODY)
    y += 50
    q = next(x for x in qs if x["id"] == EXAMPLE)
    rect(0, y, 1500, 330, bold=True)
    for c, h in zip((24, 520, 1000), ("Logic · the question", "Work · the Jobs, Tasks and Runs", "Report · what it says")):
        say(c, y + 14, h, HEAD)
    cells = [f"{q['id']} · {q['status']}\n" + wrap(q["title"], 34) + "\nfrom the Studio:\n" + " · ".join(q["fed"]),
             "no work yet" if not (q["work"] or q["runs"]) else
             "\n".join([str(w) for w in q["work"]] + [f"run {r} (this level's own Run)" for r in q["runs"]]),
             (q["report"].stem + "\nits answer line, its drawing, live\n" + f"report {q['id'].lower()} · {q['status']}")
             if q["report"] else "No report yet"]
    for c, s in zip((24, 520, 1000), cells):
        say(c, y + 60, s, BODY, L.RED if s == "no work yet" else L.INK)
    y += 370
    say(0, y, "Runs panel, beside the Report Space", HEAD)
    y += 44
    for b in sp.run_types:
        say(0, y, b["label"], CODE, font=L.MONO)
        say(340, y, b.get("doing", ""), BODY)
        say(720, y, " · ".join(b.get("skills") or []), CODE, font=L.MONO)
        y += 36
    L.close_frame(fr, pad=60)
    return fr


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s05-report-workbench-skill.excalidraw"
    frame = frame_module()
    qs, unread = questions(frame)
    space = report_space(frame)
    versions = {"report": version(SKILLS / "project/haipipe-report"),
                "question": version(SKILLS / "question/haipipe-question")}
    jobs = [p for p in BLOCK.glob("j[0-9]*_*/") if p.is_dir()]
    frames = frames_from_face(fills(qs, unread, space, versions), {"nq": len(qs), "nj": len(jobs)})

    def screen(els):
        L.els.clear()
        L.FRAME[0] = None
        screen_frame(qs, frame)
        els.extend(L.els)

    els = []
    topic_map.draw_frames(els, frames, "s05")
    screen(els)
    canvas.grid(els, [[e["id"] for e in els if e["type"] == "frame"]])
    canvas.write(out, els, "build_s05_report_workbench_skill.py")
    from render_png import render
    render(out, out.with_suffix(".png"))


if __name__ == "__main__":
    main()

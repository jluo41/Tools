"""s03 · excalidraw-slide: s03-excalidraw-slide.excalidraw (b31 Studio).

Four frames in two acts, told on one real slide job, j51 (DrFirst-SPACE, paper Paper-TestToLearn-MS2026):
  Act 1 · The example:  ① j51's job as a map, from the meeting to the deck   ② the slides it made, by group
  Act 2 · What excalidraw-slide takes from it:  ③ j51's two drawings (s01 the ask, s61 the layout) and the
          layout's folder   ④ the skill as j51 teaches it, a mind map
Drawn with excalidraw-studio's helpers; every word is a yaml block of the face. j51's facts are read from its own
files when the Job sits beside Tools-SPACE (and copied to examples/j51/), and from that snapshot when it does not.

    python build_s03_excalidraw_slide.py
"""
import ast
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]                                           # Tools-SPACE (the folder holding blueprints/)
SKILL = TOOLS / "plugins/haipipe-toolkit/skills/1_base/display/excalidraw-slide"
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/display/excalidraw-studio/scripts"))
sys.path.insert(0, str(SKILL / "scripts"))
from draw import H, INK, RED, T_KEY, T_NODE, T_SMALL, T_TEXT, W, Drawing  # noqa: E402
import slide_kit  # noqa: E402

FACE = HERE / f"{HERE.name}.md"
OUT = HERE / f"{HERE.name}.excalidraw"
d = Drawing()


def data():
    """Every yaml block of the face, merged."""
    out = {}
    for block in re.findall(r"```yaml\n(.*?)\n```", FACE.read_text(encoding="utf-8"), re.S):
        out.update(yaml.safe_load(block))
    return out


D = data()
JOB = (TOOLS / D["example"]["path"]).resolve()
SNAP = HERE / D["example"]["snapshot"]
S61, S01 = JOB / "studio/s61-demo-layout", JOB / "studio/s01-what-they-want"


# ── j51's facts: read from its files, or from the snapshot ──────────────────────────────────────────────────
def literal(path, name):
    """A module-level list in a builder, read without running it."""
    for n in ast.parse(Path(path).read_text(encoding="utf-8")).body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets):
            return ast.literal_eval(n.value)
    return []


def frame_names(drawing):
    els = json.loads(Path(drawing).read_text(encoding="utf-8"))["elements"]
    fs = [e for e in els if e.get("type") == "frame" and not e.get("isDeleted")]
    return [e.get("name", "") for e in sorted(fs, key=lambda e: (e["y"] // 400, e["x"]))]


def open_list(face):
    part = re.split(r"\nOpen\n-+\n", Path(face).read_text(encoding="utf-8"))
    return re.findall(r"^\d+\. (.*)$", part[-1], re.M) if len(part) > 1 else []


def live():
    """Read j51 and refresh the snapshot: the slides from its PDF, its two previews, facts.json."""
    m = slide_kit.load(S61 / "slides.py")
    face01 = (S01 / "s01-what-they-want.md").read_text(encoding="utf-8")
    pdf = next((S61 / "delivery").glob("*.pdf"))
    SNAP.mkdir(parents=True, exist_ok=True)
    first = SNAP / "slide-01.png"
    if shutil.which("pdftoppm") and (not first.is_file() or pdf.stat().st_mtime > first.stat().st_mtime):
        subprocess.run(["pdftoppm", "-png", "-scale-to", "960", str(pdf), str(SNAP / "slide")], check=True)
    for src in (S01 / "s01-what-they-want.png", S61 / "s61-demo-layout.png"):
        shutil.copy2(src, SNAP / src.name)
    notes = {"slides.py": f"the one source: {len(m.SLIDES)} slides", "build_s61_demo_layout.py": "draws the layout",
             "build_deck.py": "writes the deck", "capture_screens.py": "retakes screens/",
             "s61-demo-layout.md": "the face", "delivery/": "the deck, generated", "screens/": "workbench screens",
             "figures/": "the loop, two designs", "s61-demo-layout.excalidraw": "", "s61-demo-layout.png": "",
             "SKILL.md": "", "scripts/": ""}
    f = {"audience": m.AUDIENCE, "length": m.LENGTH, "shown": m.SHOWN, "groups": [list(g) for g in m.GROUPS],
         "slides": [{"n": s["n"], "slug": s["slug"], "group": s["group"], "title": s["title"],
                     "kind": s["visual"]["kind"]} for s in m.SLIDES],
         "check": [list(c) for c in slide_kit.check(S61 / "slides.py")],
         "meeting": re.search(r"meeting of (\d{4}-\d{2}-\d{2})", face01).group(1),
         "minutes": re.search(r"(\d+)-minute", face01).group(1),
         "time": literal(S01 / "build_s01_what_they_want.py", "TIME"),
         "pains": literal(S01 / "build_s01_what_they_want.py", "PAINS"),
         "changes": literal(S61 / "build_s61_demo_layout.py", "CHANGES"),
         "open": open_list(S61 / "s61-demo-layout.md"),
         "frames01": frame_names(S01 / "s01-what-they-want.excalidraw"),
         "frames61": frame_names(S61 / "s61-demo-layout.excalidraw"),
         "pdf": pdf.name,
         "delivery": [[p.name, p.stat().st_size] for p in sorted((S61 / "delivery").iterdir())
                      if not p.name.startswith(".")],
         "screens": sorted(p.name for p in (S61 / "screens").glob("*.png")),
         "figures": sorted(p.name for p in (S61 / "figures").glob("*.png")),
         "tree": Drawing.folder_tree(S61, notes=notes)}
    f["pages"] = len(list(SNAP.glob("slide-*.png")))
    (SNAP / "facts.json").write_text(json.dumps(f, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return f


def facts():
    if (S61 / "slides.py").is_file():
        return live()
    return json.loads((SNAP / "facts.json").read_text(encoding="utf-8"))


def drafts():
    """The other slide drafts in Tools, checked against the same field contract."""
    out = []
    for f in sorted((TOOLS / "blueprints").glob("*/studio/s6[0-9]-*/slides.py")):
        c = slide_kit.check(f)
        e, w = sum(l == "error" for l, _ in c), sum(l == "warn" for l, _ in c)
        out.append(f"{'⏳ later: ' if e else '✅ '}{f.parents[2].name.split('_')[0]} {f.parent.name}: {e} error{'s' * (e != 1)} "
                   f"({', '.join(m for l, m in c if l == 'error')}), {w} warning{'s' * (w != 1)}")
    return " · ".join(out) or "no other drafts in Tools"


F = facts()


def said(check):
    errors, warns = sum(l == "error" for l, _ in check), sum(l == "warn" for l, _ in check)
    return "the field contract holds" if not check else \
        f"{errors} error{'s' * (errors != 1)}, {warns} warning{'s' * (warns != 1)}"


def values():
    groups = F["groups"]
    count = [sum(s["group"] == g[0] for s in F["slides"]) for g in groups]
    kinds = list(dict.fromkeys(s["kind"] for s in F["slides"]))
    dates = sorted({c[1] for c in F["changes"]})
    on_slides = sum(c[0] not in ("all", "disk") for c in F["changes"])
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    ref = (SKILL / "ref/slide-draft.md").read_text(encoding="utf-8")
    kit = (SKILL / "scripts/slide_kit.py").read_text(encoding="utf-8")
    gaps = {"gap_ask": ("**The ask first**" in skill and "## The ask, before the draft" in ref,
                        "the ask first: the skill's step 0, ref § The ask",
                        "❓ the skill starts at slides.py: no step for the ask yet"),
            "gap_j51": ("The slide job to copy: j51" in skill, "j51 named in SKILL.md as the slide job to copy",
                        "❓ j51 is not named in SKILL.md as the slide job to copy"),
            "gap_sizes": ("a slide draft's own" in skill, "a slide draft's own sizes, written in SKILL.md (Open 5)",
                          "❓ a slide draft's own sizes are not written in SKILL.md (Open 5)"),
            "gap_deck": (any((SKILL / "scripts").glob("*deck*.py")), "one deck writer in the skill's scripts/",
                         "⏳ later: no deck writer in the skill; build_deck.py is copied into each topic"),
            "gap_pics": ("PICTURE_KINDS" in kit, "slide_kit.py check fails a screen or figure not on disk",
                         "❓ slide_kit.py check does not look for a screen's or figure's file")}
    return {"days": (date.fromisoformat(F["shown"]) - date.fromisoformat(F["meeting"])).days,
            "audience": F["audience"], "length": F["length"], "shown": F["shown"], "meeting": F["meeting"],
            "minutes": F["minutes"], "n_time": len(F["time"]), "n_pains": len(F["pains"]),
            "n_slides": len(F["slides"]), "n_groups": len(groups), "check": said(F["check"]),
            "n_screens": len(F["screens"]), "n_figures": len(F["figures"]),
            "screens": ", ".join(F["screens"]), "figures": ", ".join(F["figures"]),
            "n_changes": len(F["changes"]), "change_dates": " to ".join([dates[0], dates[-1]]) if dates else "none",
            "per_slide": f"{on_slides} under a slide, {len(F['changes']) - on_slides} on the whole draft or disk",
            "n_open": len(F["open"]), "pdf": F["pdf"], "pages": F["pages"],
            "delivery": " · ".join(f"{n} ({s / 1e6:.1f} MB)" for n, s in F["delivery"]),
            "group_names": " → ".join(g[1] for g in groups), "group_counts": " + ".join(map(str, count)),
            "groups": " · ".join(g[1] for g in groups), "kinds": " · ".join(kinds), "drafts": drafts(),
            "version": re.search(r'version: "([\d.]+)"', skill).group(1),
            "closed": sum(ok for ok, _, _ in gaps.values()), "gaps": len(gaps),
            **{k: (yes if ok else no) for k, (ok, yes, no) in gaps.items()}}


V = values()


def fill(s):
    s = str(s)
    for k, v in V.items():
        s = s.replace(f"<<{k}>>", str(v))
    return s


def node(x, y, w, title, lines, key=False, h=None, tsize=34, size=22):
    """A box with its title large and its lines small; the key one has the slight colour. Returns (x, y, w, h)."""
    lines = [fill(l_) for l_ in lines]
    title = fill(title)
    hh = h or (22 + Drawing.height(title, w - 44, tsize) + 12 +
               sum(Drawing.height("· " + l_, w - 44, size) + 6 for l_ in lines) + 16)
    if key:
        d.key(x, y, w, hh)
    else:
        d.box(x, y, w, hh, INK, 2.5)
    yy = d.para(x + 22, y + 18, title, w - 44, tsize) + 12
    for l_ in lines:
        yy = d.para(x + 22, yy, ("" if l_.startswith("❓") else "· ") + l_, w - 44, size) + 6
    return (x, y, w, hh)


def node_height(w, title, lines, tsize=34, size=22):
    return (22 + Drawing.height(fill(title), w - 44, tsize) + 12 +
            sum(Drawing.height("· " + fill(l_), w - 44, size) + 6 for l_ in lines) + 16)


# ── ① j51's job, from the meeting to the deck: the main map ─────────────────────────────────────────────────
def frame_job():
    J = D["job_map"]
    title = fill(J["title"])
    f = d.frame("① " + title.split(" ", 1)[1])
    d.heading(title, fill(J["sub"]))
    gap = 90
    w = (W - 80 - 4 * gap) / 5
    xs = [40 + i * (w + gap) for i in range(5)]
    y1 = 250
    h1 = max(node_height(w, s["title"], s["lines"]) for s in J["steps"])
    top = [node(x, y1, w, s["title"], s["lines"], s.get("key"), h1) for x, s in zip(xs, J["steps"])]
    for (x, y, bw, _), nxt, label in zip(top, top[1:], J["labels"]):
        d.line([(x + bw + 6, y + 70), (nxt[0] - 6, y + 70)], sw=4)
        d.text(x + bw - 10, y - 40, label, T_SMALL + 3)
    # the loop back: a person's change goes into slides.py, the layout is drawn again
    yb = y1 + h1 + 70
    cx = xs[2] + w / 2
    d.line([(xs[4] + 70, y1 + h1 + 6), (xs[4] + 70, yb), (cx, yb), (cx, y1 + h1 + 6)], sw=4)
    d.text(cx + 24, yb + 8, "🔁 " + fill(J["back"]), T_KEY)
    # agreed: the deck is written, then shown (row 2, right to left)
    y2 = yb + 110
    h2 = max(node_height(w, s["title"], s["lines"]) for s in J["deck"])
    deck = [node(x, y2, w, s["title"], s["lines"], False, h2) for x, s in zip((xs[4], xs[3], xs[2]), J["deck"])]
    ax = xs[4] + w - 70
    d.line([(ax, y1 + h1 + 6), (ax, y2 - 6)], sw=4)
    d.text(ax - 130, yb + 40, fill(J["agreed"]), T_KEY)
    for (x, y, bw, _), nxt, label in zip(deck, deck[1:], J["deck_labels"]):
        d.line([(x - 6, y + 70), (nxt[0] + nxt[2] + 6, y + 70)], sw=4)
        d.text(nxt[0] + nxt[2] + 8, y + 22, label, T_SMALL + 3)
    # what hurts, and the slide that answers it: from s01, the meeting's words
    px, pw = 40, xs[2] - 40 - gap
    d.line([(xs[1] + w / 2, y1 + h1 + 6), (xs[1] + w / 2, y2 - 6)], sw=4)
    d.text(xs[1] + w / 2 + 16, y2 - 48, fill(J["pains_arrow"]), T_SMALL + 3)
    yy = d.para(px, y2 + 4, fill(J["pains_title"]), pw - (xs[1] + w / 2 - px) + 300, 28)
    yy = max(yy, y2 + 4 + 40) + 14
    sw_ = 210
    for pain, at, slide in F["pains"]:
        ph = Drawing.height(pain, pw - sw_ - 120, T_SMALL + 1) + 22
        d.box(px, yy, pw - sw_ - 80, ph, INK, 1.5)
        d.para(px + 14, yy + 10, pain, pw - sw_ - 120, T_SMALL + 1)
        d.line([(px + pw - sw_ - 74, yy + ph / 2), (px + pw - sw_ - 6, yy + ph / 2)], sw=2.5)
        d.box(px + pw - sw_, yy, sw_, ph, INK, 2)
        d.text(px + pw - sw_ + 16, yy + ph / 2 - 15, slide, T_SMALL + 3)
        yy += ph + 12
    f["height"] = max(H, yy + 30, y2 + h2 + 40)
    d.badge(f)
    return f


# ── ② the slides it made, a row per group ───────────────────────────────────────────────────────────────────
def frame_deck():
    G = D["deck_grid"]
    title = fill(G["title"])
    f = d.frame("② " + title.split(" ", 1)[1])
    d.heading(title, fill(G["sub"]))
    d.key(40, 176, W - 80, 64)
    d.text(64, 190, fill(G["key"]), T_KEY)
    sw_, sh, gap, x0 = 384, 216, 24, 420
    y = 268
    for key, name, line in F["groups"]:
        mine = [s for s in F["slides"] if s["group"] == key]
        y_group = y
        for i in range(0, len(mine), 5):
            for j, s in enumerate(mine[i:i + 5]):
                x = x0 + j * (sw_ + gap)
                png = SNAP / f"slide-{s['n']}.png"
                if png.is_file():
                    d.picture(png, x, y, sw_, sh)
                else:
                    d.box(x, y, sw_, sh, RED, 1.5, dashed=True)
                d.para(x, y + sh + 6, f"{s['n']} · {s['title']}", sw_, T_SMALL)
            y += sh + 6 + 2 * T_SMALL * 1.25 + 12
        yy = d.para(40, y_group, name, 340, 44)
        yy = d.para(40, yy + 8, line, 340, T_TEXT - 2)
        d.para(40, yy + 8, f"slides {mine[0]['n']}-{mine[-1]['n']}", 340, T_SMALL)
    f["height"] = max(H, y + 20)
    d.badge(f)
    return f


# ── ③ the two drawings behind it, and the layout's folder ──────────────────────────────────────────────────
def frame_drawings():
    G = D["drawings"]
    title = fill(G["title"])
    f = d.frame("③ " + title.split(" ", 1)[1])
    d.heading(title, fill(G["sub"]))
    d.key(40, 176, W - 80, 64)
    d.text(64, 190, fill(G["key"]), T_KEY)
    y0 = 270
    d.text(40, y0, G["left"], 30)
    d.picture(SNAP / "s01-what-they-want.png", 40, y0 + 50, 520, H - 40 - (y0 + 50))
    d.text(600, y0, G["middle"], 30)
    d.picture(SNAP / "s61-demo-layout.png", 600, y0 + 50, 1180, H - 40 - (y0 + 50))
    rx, rw = 1830, W - 40 - 1830
    yy = d.para(rx, y0, G["tree"], rw, 30) + 10
    d.text(rx, yy, "\n".join(F["tree"]), 20, code=True)
    yy += len(F["tree"]) * 25 + 24
    for label, names in (("s01's frames", F["frames01"]), ("s61's frames", F["frames61"])):
        yy = d.para(rx, yy, f"🖼️ {label}: " + " · ".join(names), rw, T_SMALL + 1) + 12
    yy = d.para(rx, yy + 6, f"s61's own open questions, as j51 left them ({len(F['open'])}):", rw, T_SMALL + 1) + 6
    for q in F["open"][:4]:
        yy = d.para(rx, yy, "· " + q, rw, T_SMALL) + 4
    d.badge(f)
    return f


# ── ④ the skill as j51 teaches it: a mind map ──────────────────────────────────────────────────────────────
def frame_mind():
    M = D["mindmap"]
    title = fill(M["title"])
    f = d.frame("④ " + title.split(" ", 1)[1])
    d.heading(title, fill(M["sub"]))
    branches = [{**b, "title": fill(b["title"]), "summary": fill(b.get("summary", "")),
                 "leaves": [fill(l_) for l_ in b.get("leaves", [])]} for b in M["branches"]]
    bottom = d.mind_map(fill(M["centre"]), branches)
    f["height"] = max(H, bottom + 40)
    d.badge(f)
    return f


def main():
    f1, f2, f3, f4 = frame_job(), frame_deck(), frame_drawings(), frame_mind()
    at = {"①": f1["id"], "②": f2["id"], "③": f3["id"], "④": f4["id"]}
    b = D["between"]
    d.acts([{"name": a["name"], "frames": [at[k] for k in a["frames"]], "arrow": a["arrow"]} for a in D["acts"]],
           between=[(at[b["from"]], at[b["to"]], b["label"])])
    d.write(OUT, Path(__file__).name)


if __name__ == "__main__":
    main()

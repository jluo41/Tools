"""s51 · Server runtime: s51-server-runtime.excalidraw, how the workbench server runs, as four maps read left to right.

JL 261012: "one frame should be as large as possible, within the frame, we want the workflow map or the mindmap,
the frames should be well arrange to form the narrative." Each frame is one screen-sized map of boxes joined by
named arrows (haipipe-studio scripts/topic_map.py draw_map); the four tell one story in two acts, a row each
(b10 studio/_build/story.py):

    ① One SPACE, one host     where a page is served from: the SPACE, its one port, /wb, serve.py, what runs now
    ② One request             from start to a page: start, the live namespace, the gates, the route, the frame
    ③ What the frame answers  a mind map around /_board/workbench: themes, levels, links, Task views, old addresses
    ④ Where it stands         done, now, next in order, and what is open

Every count and name is read at build time: the server code (serve.py's Handler, do_GET, PAGE_VIEW_ROUTES,
OLD_ROUTES; host_registry's folders; each <theme>_theme.py) and this machine's listening hosts with each SPACE's
.server_config/settings.env. Written through canvas.write, so every mark a person adds survives a rebuild.

    python build_s51_server_runtime.py
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]                                   # s51 -> studio -> b10 -> blueprints -> Tools
SERVERS = TOOLS / "plugins" / "haipipe-toolkit" / "servers"
STUDIO = TOOLS / "plugins" / "haipipe-toolkit" / "skills" / "1_base" / "project" / "haipipe-studio" / "scripts"
sys.path.insert(0, str(SERVERS / "_host"))
sys.path.insert(0, str(STUDIO))
sys.path.insert(0, str(HERE.parent / "_build"))
import canvas  # noqa: E402
import story  # noqa: E402  (b10 studio/_build: frames as acts, JL 261012)
import host_registry as R  # noqa: E402  (the route registry, read as the server reads it)
import topic_map as M  # noqa: E402
from server_config import load_server_config  # noqa: E402

CHANGED = "261012"


# ── facts, read off the code ───────────────────────────────────────────────────────────────────
def serve_src() -> str:
    return (SERVERS / "_host" / "serve.py").read_text(encoding="utf-8")


def mixins() -> list:
    m = re.search(r"class Handler\(([^)]*)\)", serve_src())
    return [x.strip() for x in m.group(1).split(",") if x.strip()] if m else []


def dispatch() -> list:
    """The /_board/<name> GET routes in do_GET's order."""
    body = serve_src().split("def do_GET", 1)[1].split("def do_HEAD", 1)[0]
    return list(dict.fromkeys(re.findall(r'"(/_board/[a-z-]+)"', body)))


def folders() -> list:
    return [f.name for f in R.server_folders()]


def on_frame() -> list:
    return sorted(p.stem.replace("_theme", "") for p in SERVERS.glob("workbench-*/*_theme.py"))


def live_frame():
    """servers/workbench/frame.py through the live namespace, as the server loads it (themes included)."""
    from host_paths import bootstrap
    bootstrap()
    from live import frame
    return frame


def theme_patterns() -> dict:
    return {name: t.level_patterns for name, t in live_frame().themes().items() if t.level_patterns}


def card_guides() -> list:
    """The Guide families drawn as the card Guide: their guide.yaml has levels:."""
    from live.guide_families import FAMILIES
    return sorted(f for f, e in FAMILIES.items() if e.get("levels"))


def page_views() -> dict:
    """serve.py's PAGE_VIEW_ROUTES: an old Page route -> its frame view."""
    m = re.search(r"PAGE_VIEW_ROUTES = \{(.*?)\}", serve_src(), re.S)
    return dict(re.findall(r'"(/_board/[a-z-]+)": "([a-z]+)"', m.group(1))) if m else {}


def old_names() -> dict:
    """serve.py's OLD_ROUTES: a board page's old name -> its theme's name."""
    m = re.search(r"OLD_ROUTES = \{(.*?)\}", serve_src(), re.S)
    return dict(re.findall(r'"(/_board/[a-z-]+)": "(/_board/[a-z-]+)"', m.group(1))) if m else {}


# ── facts, read off this machine ───────────────────────────────────────────────────────────────
def _run(args: list) -> str:
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=30).stdout
    except (OSError, subprocess.SubprocessError):
        return ""


def space_of(root: Path) -> Path:
    """The SPACE a served root belongs to: the nearest folder holding env.sh or .server_config, else the nearest
    `*-SPACE` folder (Tools-SPACE has neither), else the root itself."""
    for p in (root, *root.parents):
        if (p / "env.sh").is_file() or (p / ".server_config").is_dir():
            return p
    return next((p for p in (root, *root.parents) if p.name.endswith("-SPACE")), root)


def hosts() -> dict:
    """{SPACE name: [(port, served root, is the SPACE itself)]} for every serve.py listening here; test roots under a
    temp folder are left out."""
    ports: dict = {}
    for ln in _run(["lsof", "-nP", "-iTCP", "-sTCP:LISTEN"]).splitlines()[1:]:
        cols = ln.split()
        if len(cols) > 8 and cols[0].lower().startswith("python"):
            ports.setdefault(cols[1], set()).add(int(cols[8].rsplit(":", 1)[1]))
    out: dict = {}
    for pid, held in ports.items():
        cmd = _run(["ps", "-o", "command=", "-p", pid])
        m = re.search(r"--root (\S+)", cmd)
        if "serve.py" not in cmd or not m:
            continue
        cwd = next((l[1:] for l in _run(["lsof", "-a", "-p", pid, "-d", "cwd", "-Fn"]).splitlines()
                    if l.startswith("n")), "/")
        root = (Path(cwd) / m.group(1)).resolve()
        if "/tmp/" in str(root) or "/private/" in str(root) or "/var/folders/" in str(root):
            continue
        space = space_of(root)
        for port in sorted(held):
            out.setdefault(space.name, []).append((port, root, root == space))
    return {k: sorted(v) for k, v in sorted(out.items())}


def configured() -> dict:
    """{SPACE name: its settings.env PORT} for the SPACEs that run a host here."""
    found = {}
    for name in hosts():
        root = Path.home() / "Desktop" / name
        port = load_server_config(root).get("PORT") if root.is_dir() else None
        if port:
            found[name] = int(port)
    return found


# ── the four maps ──────────────────────────────────────────────────────────────────────────────
def short(name: str) -> str:
    return name.removesuffix("-SPACE")


def frame_one(els: list, h: dict, conf: dict) -> None:
    rows, extra = [], 0
    for name, served in h.items():
        whole = [p for p, _, me in served if me]
        parts = [p for p, _, me in served if not me]
        keep = conf.get(name) if conf.get(name) in whole else (whole[0] if whole else None)
        others = [p for p in whole if p != keep] + parts
        extra += len(others)
        line = f"{short(name)} {keep}" if keep else short(name)
        if name in conf and conf[name] != keep:                 # its one host runs, but not on its settings' port
            line += f" (settings say {conf[name]})"
        rows.append(("❓ " + line + " + " + " · ".join(map(str, others))) if others
                    else ("❓ " + line) if "settings say" in line else line + " ✅")
    rows.append(f"❓ {extra} extra: stopping them waits on JL" if extra else "✅ one host per SPACE")
    ports = [f"{short(k)} → {v}" for k, v in conf.items()] + ["Tools → 5623 (--root Tools)"]
    M.draw_map(els, "frame-s51-1", "s51 · ① One SPACE, one host", "① One SPACE, one host: where a page is served from",
               ["A SPACE has one port; every Block, Job, Task and Paper opens as a path on it (JL 261011, 261012)."],
               [{"id": "space", "at": [0, 0], "title": "🗂 a SPACE", "why": "one root: env.sh, Projects, a Tools link",
                 "tree": [f"{len(h)} served on this machine", "WellDoc · Tools · Physician", "REACH · DrFirst"], "cols": 1},
                {"id": "conf", "at": [1, 0], "title": "⚙️ settings.env", "why": "its one port, per machine, git-ignored",
                 "tree": ports, "cols": 1},
                {"id": "wb", "at": [2, 0], "title": "🚪 /wb <path>", "why": "finds the SPACE's host, or starts it",
                 "tree": ["the SPACE's lowest port answers", "✎ 261012 a taken port stops, never drifts",
                          "it names any other host it finds"], "cols": 1},
                {"id": "serve", "at": [3, 0], "title": "🖥 serve.py", "why": "one process serves one SPACE",
                 "tree": ["--root <SPACE> --port <N>", "a flag wins over settings.env",
                          "no claude_agent_sdk → re-exec .venv", "❓ never reloads code: restart after a change"], "cols": 1},
                {"id": "now", "at": [0, 1], "title": "🔎 what runs now", "why": "read off this machine's listeners",
                 "tree": rows, "cols": 1},
                {"id": "why", "at": [1, 1], "title": "🧯 why extra hosts", "why": "the port drifted",
                 "tree": ["no settings.env: start at 5602", "5602 taken: walk to the next free", "Physician walked to 6 ports",
                          "WellDoc's 5620 held by a Paper host"], "cols": 1},
                {"id": "fix", "at": [2, 1], "title": "🔧 the fix (261012)", "why": "one port, written down",
                 "tree": ["✎ settings.env: WellDoc 5602, Physician 5599", "✎ REACH 5607, DrFirst 5604",
                          "✎ wb.py space_port: stop, never drift", "✎ 5623's Home link → 5602"], "cols": 1},
                {"id": "path", "at": [3, 1], "title": "🔗 a folder is a path", "why": "never a host of its own",
                 "tree": ["/w/<block> → 302", "/_board/workbench?path=<folder>", "Paper and discovery folders too"],
                 "cols": 1}],
               [("space", "conf", "keeps its port in"), ("conf", "wb", "is read by"), ("wb", "serve", "starts"),
                ("serve", "path", "serves every"), ("space", "now", "? today"), ("now", "why", "because"),
                ("why", "fix", "fixed by")],
               [{"date": CHANGED, "text": "four maps, one story, each frame one screen (JL)"},
                {"date": CHANGED, "text": "one SPACE, one port: settings.env + wb.py space_port"}])


def frame_two(els: list) -> None:
    mx, routes, fold = mixins(), dispatch(), folders()
    M.draw_map(els, "frame-s51-2", "s51 · ② One request", "② One request: from start to a page",
               ["Read off serve.py: its start, its Handler, do_GET top to bottom; a POST goes through do_POST the same way."],
               [{"id": "start", "at": [0, 0], "title": "▶️ start", "why": "serve.py's main, once",
                 "tree": ["settings · python check", "auth (--no-auth on the tailnet)", f"Handler: {len(mx)} mixins",
                          "listen on host:port"], "cols": 1},
                {"id": "live", "at": [1, 0], "title": "📦 one live namespace", "why": "every servers/ folder, one package",
                 "tree": [f"{len(fold)} folders", " · ".join(fold), "assets → one board.js · board.css"], "cols": 1},
                {"id": "gates", "at": [2, 0], "title": "🚦 the gates", "why": "checked before any route",
                 "tree": ["sign-in · terminal off?", "--only <workbench>?", "Home · /b/ · /w/ → 302", "private file?"],
                 "cols": 1},
                {"id": "route", "at": [3, 0], "title": "🧭 /_board/<name>", "why": "the first route that matches",
                 "tree": [f"{len(routes)} GET routes", "else a static file under --root",
                          "❓ do_HEAD lists them again: one table?"], "cols": 1},
                {"id": "level", "at": [3, 1], "title": "🪜 read the folder", "why": "level and theme, from its place",
                 "tree": ["level_of: bNN · jNN · tNN · board.md", "theme_of: its Theme folder", "or a theme that claims it"],
                 "cols": 1},
                {"id": "spaces", "at": [2, 1], "title": "🧩 fill the Spaces", "why": "vanilla first, then the theme",
                 "tree": ["vanilla: six Spaces from the folders", "the theme replaces what it fills",
                          "❓ a theme that fails falls back silently"], "cols": 1},
                {"id": "render", "at": [1, 1], "title": "🎨 render", "why": "the frame's own CSS, base classes only",
                 "tree": ["level tabs · six Spaces", "the Runs panel · the Guide", "no theme stylesheet (261007)"],
                 "cols": 1},
                {"id": "html", "at": [0, 1], "title": "📄 one page", "why": "built per request, from disk",
                 "tree": ["an edit on disk shows on reload", "code loads once at start", "❓ an old process serves old code"],
                 "cols": 1}],
               [("start", "live", "loads"), ("live", "gates", "one Handler"), ("gates", "route", "passes"),
                ("route", "level", "/_board/workbench"), ("level", "spaces", "then"), ("spaces", "render", "then"),
                ("render", "html", "returns")])


def frame_three(els: list) -> None:
    themes, pv, on = on_frame(), page_views(), old_names()
    views = [f"{a.removeprefix('/_board/')} → {v}" for a, v in pv.items()]
    old = [f"{a.removeprefix('/_board/')} → {b.removeprefix('/_board/')}" for a, b in on.items()]
    paper = theme_patterns().get("paper")
    M.draw_map(els, "frame-s51-3", "s51 · ③ What the frame answers", "③ What the frame answers: one door, many views",
               ["A mind map around /_board/workbench: what fills it, how it reads a folder, and what still points at it."],
               [{"id": "themes", "at": [0, 0], "title": f"🎨 {len(themes)} themes", "why": "each a <theme>_theme.py",
                 "tree": themes, "cols": 2},
                {"id": "views", "at": [0, 1], "title": f"📑 {len(views)} Task views", "why": "old Page routes, now Spaces",
                 "tree": views, "cols": 2},
                {"id": "levels", "at": [1, 0], "title": "🪜 a folder's level", "why": "from its name, or the theme's",
                 "tree": ["bNN_ or board.md → Block", "jNN_ → Job · tNN_ → Task"]
                 + (["paper: Ba-/Bb- Jobs, S- Sections"] if paper else []), "cols": 1},
                {"id": "door", "at": [1, 1], "title": "🖼 /_board/workbench", "why": "the one door for every folder",
                 "tree": ["takes path=<folder>, space=, sub=", "no band, no old-page link"], "cols": 1},
                {"id": "links", "at": [2, 0], "title": "🔗 links that land here", "why": "every door opens the frame",
                 "tree": ["SPACE Home card → /w/<block>", "a Page's tab → its Space", "--only <wb> → its own page",
                          f"📖 card Guides: {' · '.join(card_guides())}"], "cols": 2},
                *([{"id": "old", "at": [2, 1], "title": f"↩️ {len(old)} old names", "why": "kept so bookmarks still work",
                    "tree": old, "cols": 2}] if old else
                  [{"id": "old", "at": [2, 1], "title": "✂️ old names dropped", "why": "261012: nothing linked them",
                    "tree": ["✎ 261012 task-board, paper: gone", "a theme's page: /_board/<theme>-board"], "cols": 2}])],
               [("themes", "door", "fill its Spaces"), ("levels", "door", "tell it the level"),
                ("links", "door", "open"), ("door", "views", "shows a Task's"),
                ("door", "old", "answers for" if old else "no longer answers")])


def frame_four(els: list, h: dict) -> None:
    routes = dispatch()
    extra = sum(1 for v in h.values() for _, _, me in v if not me) + \
        sum(max(0, sum(1 for _, _, me in v if me) - 1) for v in h.values())
    M.draw_map(els, "frame-s51-4", "s51 · ④ Where it stands", "④ Where it stands, and what comes next",
               ["Done, then now, then next in order, toward what closes s51; what is still open is red."],
               [{"id": "done", "at": [0, 0], "title": "✅ done", "why": "true in the code today",
                 "tree": [f"{len(routes)} GET routes (26 on 261007)", f"{len(on_frame())} themes on the frame",
                          "board pages named as their themes", f"{len(page_views())} old Page addresses answer as views",
                          "✎ 261012 old board names dropped",
                          "✎ 261012 one port per SPACE"], "cols": 1},
                {"id": "now", "at": [1, 0], "title": "🔶 now (261012)", "why": "one host per SPACE",
                 "tree": ["WellDoc 5602 · Physician 5599", "REACH 5607 · DrFirst 5604", "Tools 5623",
                          f"❓ {extra} extra hosts: JL stops them" if extra else "✅ no extra host left",
                          "❓ 5623 has no claude_agent_sdk: chat 400"], "cols": 1},
                {"id": "next", "at": [2, 0], "title": "⬜ next, in order", "why": "each makes the next smaller",
                 "tree": ["1 one route table, GET and HEAD", "2 retire the old board pages",
                          "3 item views as the frame's pop-outs", "4 hosting for colleagues: s52"], "cols": 1},
                {"id": "finish", "at": [3, 0], "title": "🎯 what closes s51", "why": "the Questions it feeds",
                 "tree": ["q08 workbench base", "q09 Studio and Report on screen", "q12 SPACE hosting",
                          "q07 workbench mapping"], "cols": 1},
                {"id": "server", "at": [1, 1], "title": "❓ the server", "why": "decisions it waits on",
                 "tree": ["❓ a failed theme: say so on the page?", "❓ reload on change, or a restart command?",
                          "❓ run-result in workbench-paper: to the base?"], "cols": 1},
                {"id": "pages", "at": [2, 1], "title": "❓ the views", "why": "decisions it waits on",
                 "tree": ["❓ one mechanism for a Task's Page views?", "❓ paper: Ba- and Bb- as one Job (Q01)?",
                          "❓ a Section's Work: list its Runs?"], "cols": 1}],
               [("done", "now", "then"), ("now", "next", "then"), ("next", "finish", "toward"),
                ("now", "server", "? waits on"), ("next", "pages", "? waits on")])


def main():
    out = HERE / "s51-server-runtime.excalidraw"
    h, conf = hosts(), configured()
    els: list = []
    frame_one(els, h, conf)
    frame_two(els)
    frame_three(els)
    frame_four(els, h)
    story.arrange(els, [{"title": "Act 1 · Where a page comes from", "frames": ["frame-s51-1", "frame-s51-2"]},
                        {"title": "Act 2 · What it answers, and where it stands", "frames": ["frame-s51-3", "frame-s51-4"]}],
                  ["a page is asked for", "the frame draws", "where it stands"])
    canvas.write(out, els, "build_s51_server_runtime.py")
    from render_png import render
    render(out, out.with_suffix(".png"))


if __name__ == "__main__":
    main()

"""s51 · Server runtime: s51-server-runtime.excalidraw, how the workbench server runs, in six frames.

The first server topic (s51 on: the served side of the design in s01-s13). Its facts are read off
the server code on every build, so the drawing shows what the code does now:

1 · Start              serve.py's start: settings, bind, auth, the one handler, the listener
2 · The folders        servers/ read off the disk; every folder grafted onto one `live` namespace;
                       the handler's mixins (counted off serve.py's `class Handler(...)`)
3 · One request        the gates and the dispatch, in do_GET's order
4 · The frame          /_board/workbench: folder -> level -> theme -> vanilla + theme -> one page;
                       which themes are on it (each `<theme>_theme.py` found), which are not yet
5 · Routes             host_registry.WORKBENCH_ROUTES: the /_board/<name> each workbench answers
6 · Where links land   SPACE Home -> /w/<block> -> the frame (no band, no old-page link: 261007);
                       an --only host keeps the theme's own page
Questions              what is still open

Black and gray lines, placeholders only; red marks what is open. Written through canvas.write, so
every mark a person adds survives a rebuild.

    python build_s51_server_runtime.py [out.excalidraw]
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]                                   # s51 -> studio -> b03 -> designs -> Tools
SERVERS = TOOLS / "plugins" / "haipipe-toolkit" / "servers"
sys.path.insert(0, str(HERE.parent / "s01-overall-tree-structure"))
sys.path.insert(0, str(HERE.parent / "_build"))
sys.path.insert(0, str(SERVERS / "_host"))
import build_ladder_v4 as L  # noqa: E402  (the shared drawing helpers)
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402
import host_registry as R  # noqa: E402  (the route registry, read as the server reads it)

INK, GRAY, RED, MONO, SANS = L.INK, L.GRAY, L.RED, L.MONO, L.SANS
TEAL, BLUE, GREEN = L.TEAL, L.BLUE, L.GREEN
text, box, path, base = L.text, L.box, L.path, L.base

# what each server folder is for (host_registry's docstring, said short); a folder not named here
# is drawn with its file count only
ROLES = {
    "_host": "the transport: serve.py, auth, config, live/, asset concat",
    "space-home": "SPACE Home; Board writes (structure, write, activity)",
    "haipipe-page": "the standalone Page server; the reader look",
    "workbench": "the base: the frame, Runs panel, Guide, Studio",
    "task-page": "the base's Task level: the Page views a Task's Spaces show",
    "workbench-work": "the work theme (work_theme.py + its old work-board page)",
    "workbench-paper": "the paper theme (paper_theme.py + its old paper-board page)",
    "workbench-cowork": "the cowork theme",
    "workbench-discovery": "the discovery workbench",
    "workbench-insight": "the insight workbench",
    "workbench-design": "the design theme",
    "workbench-labeling": "the labeling workbench (optional package)",
}
QUESTIONS = [
    "? when a theme's Spaces hold all its old page shows, retire that page (paper-board already forwards to the frame)",
    "? a theme that fails to import falls back to vanilla silently: show it on the page instead?",
    "? one live server, many stale ones: no reload on code change, so an old process serves old code",
    "? hosting for colleagues (Q12): an always-on host, sign-in, a viewer mode with no writes",
    "? do_GET and do_HEAD each list every route: one table instead of two if-chains?",
    "? the old addresses (draft, runs, task-board, ...): drop them once no link or bookmark uses them?",
    "? the item views (design, insight, insight-run, labeling, run-result): pop-outs of the frame, one route?",
    "? run-result is opened from every Runs panel but sits in workbench-paper: move it to the base?",
    "? one mechanism for a Task's Page views: page_task_spaces for every Page Task, then PAGE_VIEWS goes",
    "? Evidence-Supporting: no Task runs / Discovery runs card in run-cards.md yet; its views lines still say table/reading",
    "? a Section's Questions: Work should list the Runs that worked it and what they changed",
    "? question_rows: one heading per group in All, for every theme (paper does it itself today)",
    "? paper: Ba- (Main) and Bb- (Appendix) are two Jobs today; s12 draws one version Job (a folder decision, Q01)",
]


# ── facts, read off the code ───────────────────────────────────────────────────────────────────
def serve_src() -> str:
    return (SERVERS / "_host" / "serve.py").read_text(encoding="utf-8")


def mixins() -> list:
    m = re.search(r"class Handler\(([^)]*)\)", serve_src())
    return [x.strip() for x in m.group(1).split(",")] if m else []


def dispatch() -> list:
    """The /_board/<name> GET routes in do_GET's order."""
    body = serve_src().split("def do_GET", 1)[1].split("def do_HEAD", 1)[0]
    seen = []
    for name in re.findall(r'"(/_board/[a-z-]+)"', body):
        if name not in seen:
            seen.append(name)
    return seen


def folders() -> list:
    """(name, depth, .py count, has assets) for every server folder, in the registry's load order."""
    out = []
    for f in R.server_folders():
        depth = 1 if f.parent.name == "workbench" else 0
        py = sum(1 for p in f.glob("*.py"))
        out.append((f.name, depth, py, (f / "assets").is_dir()))
    return out


def on_frame() -> list:
    return sorted(p.stem.replace("_theme", "") for p in SERVERS.glob("workbench-*/*_theme.py"))


def all_themes() -> list:
    sys.path.insert(0, str(SERVERS / "workbench"))
    import frame  # noqa: E402  (frame.py only, no live namespace needed for its constants)
    return sorted(set(frame.THEME_FOLDERS.values()))


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


# ── frames ─────────────────────────────────────────────────────────────────────────────────────
def chain_row(x0, y, steps, W=300, H=64, G=90):
    for i, (name, note) in enumerate(steps):
        x = x0 + i * (W + G)
        box(x, y, W, H, name, 17, RED if name.startswith("?") else INK)
        text(x, y + H + 10, note, 15, RED if note.startswith("?") else GRAY)
        if i:
            path([(x - G + 8, y + H / 2), (x - 8, y + H / 2)])


def frame_start(x0, y0):
    fr = L.open_frame("1 · Start")
    text(x0, y0, "Start: one process, one handler, one root", 34)
    text(x0, y0 + 50, "python Tools/plugins/haipipe-toolkit/servers/_host/serve.py --root . --port <N> [--no-auth] [--only <wb>]",
         18, GRAY, MONO)
    chain_row(x0, y0 + 110, [
        ("settings", "<root>/.server_config/settings.env\nPORT · BIND_HOST · AUTH_FILE · DOMAIN\na flag wins over the file"),
        ("python check", "no claude_agent_sdk here and a .venv\nunder root: re-exec with it (chat\nneeds the SDK)"),
        ("auth", "--no-auth · an auth file · --public-read;\na non-loopback bind needs an auth file"),
        ("Handler", f"one class of {len(mixins())} mixins (frame 2);\nroot · only · terminal set on it"),
        ("listen", "ThreadingHTTPServer(host, port);\na non-loopback bind also serves\n127.0.0.1 (for ssh -L / VS Code)"),
    ])
    text(x0, y0 + 300, "On start it prints the DOMAINs it answers at (configured · tailscale · loopback) and reaps"
                       " terminals left by the last run.", 16, GRAY)
    text(x0, y0 + 330, "? it never reloads: a code change needs a restart, and an older process keeps serving old code",
         16, RED)
    L.close_frame(fr)
    return fr


def frame_folders(x0, y0):
    fr = L.open_frame("2 · The folders")
    text(x0, y0, "The folders: every servers/ folder is one part of one live namespace", 34)
    text(x0, y0 + 50, "read off host_registry.server_folders(): each folder's *.py imports as live.<module>; "
                      "assets/js and assets/css are concatenated into one board.js / board.css", 18, GRAY)
    y = y0 + 110
    text(x0, y, "servers/", 18, INK, MONO)
    rows = folders()
    for i, (name, depth, py, assets) in enumerate(rows):
        yy = y + 34 + i * 30
        last = i == len(rows) - 1 or rows[i + 1][1] < depth
        lead = ("│   " if depth else "") + ("└── " if last and depth else "├── ")
        text(x0, yy, f"{lead}{name}/", 16, INK, MONO)
        text(x0 + 360, yy + 1, f"{py:>3} .py{'  + assets' if assets else ''}", 15, GRAY, MONO)
        text(x0 + 560, yy + 1, ROLES.get(name, ""), 15, GRAY)
    mx = x0 + 1180
    mix = mixins()
    text(mx, y, f"class Handler(  {len(mix)} mixins  ):", 18, INK, MONO)
    for i, m in enumerate(mix):
        text(mx + 30 + (i // 16) * 300, y + 34 + (i % 16) * 26, m, 15, INK, MONO)
    text(mx, y + 34 + 16 * 26 + 20, "from live.<module> import <X>Mixin: the module may sit in any folder at left;\n"
                                    "module names are unique across folders", 15, GRAY)
    L.close_frame(fr)
    return fr


# how a person reaches each folder's routes (read off home.py resolve_workbench, frame.py render, the
# Runs panel and each theme's own links); a route named here overrides its folder's line
REACHED = {
    "workbench": "/w/<block> → 302 → /_board/workbench (the frame);\nGuide tab → guide · /w/shared → shared;\n/b/<block>/<page> → page (the one Page reader)",
    "task-page": "a Task's Spaces in the frame, each view a subspace drawn in place;\n/w/<block>/<page>/<tab> → 302 → that Space",
    "_old": "old addresses, kept so links keep working: answered\nas the route they now are (serve.py), never a route",
    "_themed": "the frame draws its Spaces (no band or old-page link, 261007);\nits old page answers only by its own address",
    "_vanilla": "the frame draws vanilla for its Blocks;\nits own page answers only by its own address",
}
ROUTE_NOTE = {
    "/_board/run-result": "every Runs panel (its code sits in workbench-paper)",
}


def handler_folder() -> dict:
    """{route: the server folder whose code answers it}: do_GET's `return self.<view>(`, then the
    folder whose .py defines `def <view>`."""
    body = serve_src().split("def do_GET", 1)[1].split("def do_HEAD", 1)[0]
    views = {}
    for chunk in re.split(r"\n(?=\s+if )", body):
        names = re.findall(r'"(/_board/[a-z-]+)"', chunk)
        call = re.search(r"return self\.(\w+)\(", chunk)
        for n in names:
            if call:
                views.setdefault(n, call.group(1))
    where = {}
    # a workbench folder first: the standalone Page server keeps copies of some views
    for f in sorted(R.server_folders(), key=lambda f: not (f.name.startswith("workbench") or f.parent.name == "workbench")):
        for py in list(f.glob("*.py")) + list((f / "live").glob("*.py") if f.name == "_host" else []):
            src = py.read_text(encoding="utf-8", errors="ignore")
            for n, v in views.items():
                if n not in where and f"def {v}(" in src:
                    where[n] = f.name
    for n in names_of(body):
        where.setdefault(n, "_host")              # answered inline in serve.py (health)
    return where


def names_of(body: str) -> list:
    return re.findall(r'"(/_board/[a-z-]+)"', body)


def route_rows(routes) -> list:
    """One row per server folder that answers a GET route (JL 261007: "how these linked to the themes
    and workbench base URL?"): the folder, its theme, whether the theme is on the frame, its routes,
    and how a person reaches them. Colour: teal the base frame, blue its Task level, green a theme on
    the frame, gray a theme not on it yet."""
    where = handler_folder()
    framed = set(on_frame())
    order = ["_host", "workbench", "task-page"] + sorted({f for f in where.values() if f.startswith("workbench-")},
                                                 key=lambda f: (f.removeprefix("workbench-") not in framed, f))
    order += sorted({f for f in where.values()} - set(order))
    rows = []
    for f in order:
        mine = [r for r in routes if where.get(r) == f]
        if f == "task-page":             # served through the frame now: ?view=<view> (serve.py PAGE_VIEW_ROUTES)
            mine = [f"?view={v}" for v in dict.fromkeys(page_views().values())]
        if not mine:
            continue
        theme = f.removeprefix("workbench-")
        if f == "workbench":
            label, on, color, how = "the base", "is the frame", TEAL, REACHED["workbench"]
        elif f == "task-page":
            label, on, color, how = "the base · Task level", "yes: its Spaces", BLUE, REACHED["task-page"]
        elif theme in framed:
            label, on, color, how = f"{theme} theme", "yes", INK, REACHED["_themed"]   # was green; green = a change
        elif f.startswith("workbench-"):
            label, on, color, how = f"{theme} theme", "not yet", GRAY, REACHED["_vanilla"]
        elif f == "_host":
            label, on, color, how = "the host itself", "", TEAL, "nobody links it: a status check\n(checks/smoke.py asks it)"
        else:
            label, on, color, how = f, "", GRAY, ""
        rows.append((f, label, on, color, mine, how))
    old = ([f"{a} → view={v}" for a, v in page_views().items()]
           + [f"{a} → {b.removeprefix('/_board/')}" for a, b in old_names().items()])
    rows.append(("serve.py", "old addresses", "→ answered as", GRAY, old, REACHED["_old"]))
    return rows


def page_views() -> dict:
    """serve.py's PAGE_VIEW_ROUTES: an old Page route -> its frame view."""
    m = re.search(r"PAGE_VIEW_ROUTES = \{(.*?)\}", serve_src(), re.S)
    return dict(re.findall(r'"(/_board/[a-z-]+)": "([a-z]+)"', m.group(1))) if m else {}


def old_names() -> dict:
    """serve.py's OLD_ROUTES: a board page's old name -> its theme's name."""
    m = re.search(r"OLD_ROUTES = \{(.*?)\}", serve_src(), re.S)
    return dict(re.findall(r'"(/_board/[a-z-]+)": "(/_board/[a-z-]+)"', m.group(1))) if m else {}


def frame_request(x0, y0):
    fr = L.open_frame("3 · One request")
    text(x0, y0, "One request: gates first, then the first route that matches", 34)
    text(x0, y0 + 50, "read off do_GET in serve.py, top to bottom; a POST goes through do_POST the same way", 18, GRAY)
    gates = [("auth", "require_request_auth"), ("terminal off?", "reject_disabled_terminal"),
             ("--only?", "reject_outside_only: route_allowed()"), ("/ or /boards", "SPACE Home"),
             ("/b/<board> · /w/<board>", "the short address: 302 to /_board/<route>"),
             ("/workbench/labeling", "the labeling Page"), ("private file?", "reject_private_static")]
    y = y0 + 110
    for i, (gate, what) in enumerate(gates):
        box(x0, y + i * 74, 300, 52, gate, 16)
        text(x0 + 320, y + i * 74 + 15, what, 15, GRAY)
        path([(x0 + 150, y + i * 74 + 52), (x0 + 150, y + (i + 1) * 74 - 4)])
    yd = y + len(gates) * 74
    box(x0, yd, 300, 52, "/_board/<name>", 16)
    routes = dispatch()
    text(x0 + 320, yd + 15, f"{len(routes)} GET routes: which server folder answers each, its theme, and how a "
                            "person gets there (read off serve.py, the folders and the themes on the frame):", 15, GRAY)
    cols = (0, 300, 520, 1500)                  # who · on the frame? · routes · reached from
    tx, gy = x0 + 320, yd + 60
    for c, h in zip(cols, ("who answers", "on the frame?", "its routes", "how a person gets there")):
        text(tx + c, gy, h, 16, GRAY)
    gy += 34
    path([(tx, gy), (tx + 2400, gy)], arrow=False, color=GRAY)
    for folder, label, on, color, names, how in route_rows(routes):
        y1 = gy + 12
        text(tx + cols[0], y1, label, 18, color)
        text(tx + cols[0], y1 + 28, folder + "/", 14, GRAY, MONO)
        text(tx + cols[1], y1, on, 16, color)
        for i, r in enumerate(names):
            text(tx + cols[2] + (i % 3) * 320, y1 + (i // 3) * 26, r, 15, color, MONO)
        notes = [f"{r.removeprefix('/_board/')}: {ROUTE_NOTE[r]}" for r in names if r in ROUTE_NOTE]
        text(tx + cols[3], y1, "\n".join([how] + notes).strip(), 15, GRAY)
        h = max(64, ((len(names) + 2) // 3) * 26 + 8, (how.count("\n") + 1 + len(notes)) * 20 + 8)
        gy += h + 18
        path([(tx, gy), (tx + 2400, gy)], arrow=False, color=GRAY)
    gy += 20
    yl = gy + 10
    box(x0, yl, 300, 52, "anything else", 16)
    text(x0 + 320, yl + 15, "a static file under --root (SimpleHTTPRequestHandler)", 15, GRAY)
    path([(x0 + 150, yd + 52), (x0 + 150, yl - 4)])
    L.close_frame(fr)
    return fr


def frame_frame(x0, y0):
    fr = L.open_frame("4 · The frame")
    text(x0, y0, "The frame: /_board/workbench?path=<folder>[&space=][&sub=][&theme=]", 34)
    text(x0, y0 + 50, "workbench/frame_view.py -> frame.py: read only; any Block, Job or Task folder in one page", 18, GRAY)
    chain_row(x0, y0 + 110, [
        ("<folder>", "under --root, else 404;\nno path: the list of Blocks"),
        ("level_of", "bNN_ · jNN_ · tNN_, a board.md, or the\ntheme's level_patterns -> Block · Job · Task"),
        ("theme_of", "the Theme folder its Block sits in,\ninside a Project; else vanilla"),
        ("spaces_for", "vanilla(level) per Space, then the\ntheme's Space over it, field by field"),
        ("render", "level tabs · six Spaces · third row\n· content │ Runs panel; Guide mounted"),
    ])
    y = y0 + 330
    text(x0, y, "what vanilla reads, per Space (a theme replaces only what it fills):", 20)
    reads = [("Description", "the face: <folder>.md or board.md, its fields"),
             ("Idea Studio", "studio/sNN-<topic>/: notes .md, *.excalidraw, build_*.py; sessions from runs/run-draw-<sNN>/"),
             ("Audience Report", "the face's ## Questions yaml + reports/qNN_<topic>/ (Question │ Work │ Report)"),
             ("Work Details", "Block: its jNN_ · Job: its tNN_ · Task: its own folders"),
             ("Runs", "runs/: run.yaml of each Run, grouped by type"),
             ("Delivery", "delivery/"),
             ("a Task, also", "its Page views as subspaces (PAGE_VIEWS): Description › Folder · Audience Report › Draft ·"),
             ("", "Work Details › Evidence · Value · Runs › Page Runs · Delivery › Lanes; a theme keeps them"),
             ("a Page Task", "a theme that returns page_task_spaces() lays the Page out itself (frame 8);"),
             ("", "PAGE_VIEWS then steps aside in those Spaces (spaces_for compares PAGE_TASK_SUBS)")]
    for i, (sp, what) in enumerate(reads):
        text(x0 + 20, y + 40 + i * 30, sp, 16, INK, MONO)
        text(x0 + 240, y + 40 + i * 30, what, 15, GRAY, MONO)
    on, every = on_frame(), all_themes()
    ty = y + 40 + len(reads) * 30 + 30
    named = theme_patterns()
    text(x0, ty, "themes that name their own Job and Task folders (Theme.level_patterns):", 20)
    for i, (name, pats) in enumerate(named.items() or [("none", {})]):
        text(x0 + 20, ty + 38 + i * 28, f"{name}: " + " · ".join(f"{lv} {pat}" for lv, pat in pats.items()), 16, INK, MONO)
    ty += 38 + max(1, len(named)) * 28 + 30
    text(x0, ty, "styles: the base's only (JL 261007), never a theme's own:", 20)
    text(x0 + 20, ty + 38, "CSS · PANEL_CSS · SPLIT_CSS · SPACE_VIEW_CSS · WORK_ITEM_CSS; + .st-ok .st-warn .topic.missing", 16, INK, MONO)
    ty += 38 + 28 + 30
    text(x0, ty, "themes on the frame (servers/workbench-<theme>/<theme>_theme.py):", 20)
    text(x0 + 20, ty + 38, "  ".join(on) or "none", 17, INK, MONO)
    text(x0, ty + 80, "not yet (still their own page and route):", 20, RED)
    text(x0 + 20, ty + 118, "  ".join(t for t in every if t not in on) or "none", 17, RED, MONO)
    L.close_frame(fr)
    return fr


def frame_routes(x0, y0):
    fr = L.open_frame("5 · Routes")
    text(x0, y0, "Routes: what each workbench answers (host_registry.WORKBENCH_ROUTES)", 34)
    text(x0, y0 + 50, "--only <wb>,<wb> serves just these names (+ " + " · ".join(sorted(R.ALWAYS_ROUTES))
         + ", Home, /b/, /w/, /_board/page); no terminal, chat or Board writes", 18, GRAY)
    y = y0 + 110
    path([(x0, y), (x0 + 2000, y)], arrow=False, color=GRAY)
    for wb, names in R.WORKBENCH_ROUTES.items():
        names = sorted(names)
        lines = [" · ".join(names[i:i + 9]) for i in range(0, len(names), 9)]
        text(x0 + 16, y + 12, wb, 18, INK, MONO)
        text(x0 + 200, y + 13, "\n".join(lines), 15, GRAY, MONO)
        y += 24 + 20 * len(lines) + 10
        path([(x0, y), (x0 + 2000, y)], arrow=False, color=GRAY)
    L.close_frame(fr)
    return fr


def frame_links(x0, y0):
    fr = L.open_frame("6 · Where links land")
    text(x0, y0, "Where links land: every Block opens in the frame (261007)", 34)
    text(x0, y0 + 50, "space-home/home.py: resolve_workbench() and each Home card; the frame has no band and no old-page link (JL 261007)", 18, GRAY)
    y = y0 + 120
    box(x0, y, 300, 64, "SPACE Home card", 17)
    box(x0 + 420, y, 300, 64, "/w/<block> · /b/<block>", 17)
    box(x0 + 840, y, 420, 64, "/_board/workbench?path=…", 17)
    path([(x0 + 308, y + 32), (x0 + 412, y + 32)])
    path([(x0 + 728, y + 32), (x0 + 832, y + 32)])
    text(x0 + 760, y - 30, "302", 15, GRAY)
    text(x0 + 840, y + 76, "the frame, in the Block's theme; the level tabs say where you are,\nthe path is the title's tooltip", 15, GRAY)
    y2 = y + 170
    box(x0 + 420, y2, 300, 64, "--only <wb> host", 17)
    box(x0 + 840, y2, 420, 64, "/_board/<theme>-board?path=…", 17)
    path([(x0 + 728, y2 + 32), (x0 + 832, y2 + 32)])
    text(x0 + 840, y2 + 76, "one theme's door serves no frame: its own page, as before", 15, GRAY)
    y3 = y2 + 150
    box(x0, y3, 300, 64, "a Task Page's tab", 17)
    box(x0 + 420, y3, 300, 64, "/w/<block>/<page>/<tab>", 17)
    box(x0 + 840, y3, 640, 64, "/_board/workbench?path=<task>&space=<Space>&sub=<view>", 17)
    path([(x0 + 308, y3 + 32), (x0 + 412, y3 + 32)])
    path([(x0 + 728, y3 + 32), (x0 + 832, y3 + 32)])
    text(x0 + 760, y3 - 30, "302", 15, GRAY)
    text(x0 + 840, y3 + 76, "the Task's Space, its Page view drawn in place (draft → Audience Report › Draft, runs → Runs ›\n"
                            "Page Runs, ...); a Page outside a Task folder keeps its own view, /_board/workbench?view=<view>", 15, GRAY)
    y2 = y3 + 30
    text(x0, y2 + 140, "?view=questions#question-QNN opens the frame's Audience Report on that row", 16, GRAY)
    text(x0, y2 + 172, "? a slug two Blocks share (two Projects' b01_<x>) is a 404 at /w/; Home links the long address", 17, RED)
    L.close_frame(fr)
    return fr


def servers_running() -> tuple:
    """(running, started before serve.py last changed): what this machine serves now."""
    import subprocess, datetime as dt
    try:
        out = subprocess.run(["ps", "-eo", "lstart,command"], capture_output=True, text=True).stdout
    except OSError:
        return 0, 0
    changed = dt.datetime.fromtimestamp((SERVERS / "_host" / "serve.py").stat().st_mtime)
    rows = [ln for ln in out.splitlines() if "haipipe-toolkit/servers/_host/serve.py" in ln and "--port" in ln]
    old = sum(dt.datetime.strptime(" ".join(ln.split()[:5]), "%a %b %d %H:%M:%S %Y") < changed for ln in rows)
    return len(rows), old


# What is done and what comes next (JL 261007: "what is the next step? update the s51 for the latest
# status"); the counts are read at build time, the steps in order.
NEXT = [
    ("1 · Restart the live servers", "every one started before serve.py last changed serves old code: no new route names, no\n"
     "Task views in the frame. Stop the stale ones, keep one per use (see Questions: no reload)."),
    ("2 · One route table", "do_GET and do_HEAD list every route twice, as if-chains: one {route: view} table, read by\n"
     "both, and by this drawing. Small and mechanical; it makes every step below a one-line change."),
    ("3 · discovery, insight, labeling onto the frame", "a <theme>_theme.py each, like cowork · design · paper · work: their Blocks\n"
     "open in their theme instead of vanilla (done 261007)."),
    ("4 · Retire the old board pages", "once a theme's Spaces hold all its old page shows: drop <theme>-board (the band link is gone)\n"
     "(4 themes are there now); then the old addresses, once nothing links them."),
    ("5 · The item views", "run-result into the base (every Runs panel opens it); design · insight · insight-run ·\n"
     "labeling as the frame's pop-outs, one route with view= like the Task views."),
    ("6 · Hosting for colleagues (Q12)", "an always-on host, sign-in, a viewer mode with no writes."),
]


def frame_status(x0, y0):
    fr = L.open_frame("7 · Status and next")
    routes = dispatch()
    running, old = servers_running()
    text(x0, y0, "Status (261007) and the next steps", 34)
    text(x0, y0 + 50, "read at build time from the server code and this machine's processes", 18, GRAY)
    done = [f"{len(routes)} GET routes (26 this morning): the Task's 8 Page routes are the frame's Task Spaces now",
            f"themes on the frame: {' · '.join(on_frame())}; not yet: {' · '.join(t for t in all_themes() if t not in on_frame())}",
            "board pages named as their themes: work-board, paper-board (task-board, paper still answer)",
            f"old addresses still answering: {len(page_views()) + len(old_names())} (serve.py), never routes"]
    y = y0 + 110
    text(x0, y, "done", 22, GREEN)
    for i, ln in enumerate(done):
        text(x0 + 20, y + 40 + i * 30, ln, 17)
    y += 40 + len(done) * 30 + 30
    text(x0, y, f"live: {running} servers running here, {old} started before serve.py last changed (old code)", 18,
         RED if old else GRAY)
    y += 60
    text(x0, y, "next, in order", 22)
    y += 44
    for i, (step, why) in enumerate(NEXT):
        box(x0, y, 520, 56, step, 17, INK if i else RED)
        text(x0 + 550, y + 6, why, 15, GRAY)
        y += 90
    L.close_frame(fr)
    return fr


def frame_guide_and_page(x0, y0):
    fr = L.open_frame("8 · Guide by level · a Page Task")
    f = live_frame()
    text(x0, y0, "The Guide by level, and a Page Task on the frame (261007)", 34)
    text(x0, y0 + 50, "read at build time from workbench/frame.py, guide_families.py and guide/levels.yaml", 18, GRAY)
    y = y0 + 110
    text(x0, y, "Guide: four Views, each three folding sections Block · Job · Task of cards; the tab's level opens", 20)
    chain_row(x0, y + 40, [
        ("guide/levels.yaml", "the base's card words:\nlevel × Space (is · reads)"),
        ("guide.yaml levels:", "a theme overrides only the\nwords that differ; roadmap: per level"),
        ("frame.space_cards", "each Space card's sub · runs,\nlive from spaces_for"),
        ("workbench_guide.py", "one renderer: lead · 3 folds of\ncards · All levels (the old body)"),
        ("frame.render", "passes level= to mount_guide;\nthat section opens"),
    ])
    cg = card_guides()
    text(x0, y + 210, "on the card Guide: " + (" · ".join(cg) or "none"), 17, INK, MONO)
    text(x0, y + 240, "old key task answers as work (guide_families.ALIASES)", 15, GRAY)
    y += 310
    text(x0, y, "a Page Task: frame.page_task_spaces(folder, root, sub), each view the Page itself, embedded", 20)
    text(x0, y + 32, "/_board/draft?path=<Block face>&file=<Task face>&embed=1&space=…&view=|tab=…  (task-page/outline.py EMBED_HTML)",
         15, GRAY, MONO)
    yy = y + 76
    for space, subs in f.PAGE_TASK_SUBS.items():
        text(x0 + 20, yy, space, 16, INK, MONO)
        text(x0 + 240, yy, " · ".join(subs), 15, INK, MONO)
        yy += 28
    yy += 16
    text(x0, yy, "run cards per view (PAGE_TASK_RUNS, by label from run-cards.md); Table and Reading: none, read only", 18)
    yy += 36
    for sub, cards in f.PAGE_TASK_RUNS.items():
        text(x0 + 20, yy, sub, 15, INK, MONO)
        text(x0 + 240, yy, " · ".join(cards), 15, GRAY, MONO)
        yy += 26
    L.close_frame(fr)
    return fr


def frame_questions(x0, y0):
    fr = L.open_frame("Questions")
    text(x0, y0, "Questions", 30)
    for i, q in enumerate(QUESTIONS):
        text(x0, y0 + 60 + i * 40, q, 18, RED)
    L.close_frame(fr)
    return fr


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s51-server-runtime.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    a = frame_start(0, 0)
    st = frame_status(a["x"] + a["width"] + 300, 0)
    b = frame_folders(0, max(a["y"] + a["height"], st["y"] + st["height"]) + 300)
    c = frame_request(b["x"] + b["width"] + 300, b["y"] + 80)
    lo = max(b["y"] + b["height"], c["y"] + c["height"]) + 300
    d = frame_frame(0, lo)
    e = frame_routes(d["x"] + d["width"] + 300, lo + 80)
    lo = max(d["y"] + d["height"], e["y"] + e["height"]) + 300
    f = frame_links(0, lo)
    g = frame_guide_and_page(f["x"] + f["width"] + 300, lo + 80)
    frame_questions(0, max(f["y"] + f["height"], g["y"] + g["height"]) + 300)
    canvas.write(out, list(L.els), "build_s51_server_runtime.py")


if __name__ == "__main__":
    main()

"""Discover every server folder the host assembles.

A server folder is one of:
  · ``servers/_host``            the transport (this folder; its mixins sit in ``live/``)
  · ``servers/space-home``    Board-level presenters (home, structure, write, activity)
  · ``servers/haipipe-page``     the standalone Page server and the reader appearance
  · ``servers/workbench``        the base workbench: Guide, Studio and what every theme reuses
  · ``servers/workbench/task-page``   the base's Task level: one Page's tabs (outline, evidence, runs,
                                 delivery, exports), once the workbench-page folder
  · ``servers/workbench-<name>`` one theme's live tab, the served face of ``workbench-<name>``
  · ``plugins/<other>/servers/workbench-<name>``  a workbench shipped by another workbench

Every folder may hold ``*.py`` mixins, importable as ``live.<module>`` through
the ``live`` namespace package in ``_host/live/``, and ``assets/js/**`` and
``assets/css/**`` parts that ``host_assets`` concatenates in sorted relative
order. Nothing here is imported until a route or the build asks for it.
"""
import re
from pathlib import Path

from host_paths import HOST, WORKBENCHES, SERVERS, TOOLKIT


def workbench_folders():
    """The base ``workbench`` folder and its level folders, then the ``workbench-*`` themes, then
    every sibling plugin's."""
    base = SERVERS / "workbench"
    found = [base] + [base / lv for lv in LEVELS if (base / lv).is_dir()] if base.is_dir() else []
    found += sorted(p for p in SERVERS.glob("workbench-*") if p.is_dir())
    for workbench in sorted(WORKBENCHES.iterdir()):
        if workbench == TOOLKIT or not (workbench / "servers").is_dir():
            continue
        found.extend(sorted(p for p in (workbench / "servers").glob("workbench-*") if p.is_dir()))
    return found


# The base workbench's level folders, each a server folder of its own (mixins, assets): Task is the
# Page Task's views (task-page: once workbench-page, JL 261007); the frame itself is the base's own code.
LEVELS = ("task-page",)


def workbench_name(folder):
    """A workbench folder's name in WORKBENCH_ROUTES: ``workbench-<name>`` -> ``<name>``; the base
    ``workbench`` folder answers the ``shared`` routes (Studio's draw, chat and terminal), and its
    Task level the ``page`` routes."""
    if folder.parent == SERVERS / "workbench":
        return {"task-page": "page"}.get(folder.name, folder.name)
    return folder.name.split("-", 1)[1] if "-" in folder.name else "shared"


def server_folders():
    """Every folder that may contribute mixins or asset parts, in load order."""
    folders = [HOST, SERVERS / "space-home", SERVERS / "haipipe-page"]
    folders.extend(workbench_folders())
    return [f for f in folders if f.is_dir()]


def live_folders():
    """Folders whose ``*.py`` files are reachable as ``live.<module>``.

    ``_host`` itself is excluded: its mixins live in ``_host/live/``, which is
    the package these folders are grafted onto.
    """
    return [f for f in server_folders() if f != HOST]


def asset_roots(kind):
    """``<folder>/assets/<kind>`` for every server folder that has one."""
    return [f / "assets" / kind for f in server_folders() if (f / "assets" / kind).is_dir()]


# `--only <workbench,...>`: the `/_board/<name>` first segments each workbench
# answers. A host started with `--only labeling` serves these names, the short
# `/b/` and `/w/` addresses, static Board pages, and nothing else: no terminal,
# no chat, no Board write route. Keep a workbench's row next to its folder.
WORKBENCH_ROUTES = {
    # workbench/task-page (once workbench-page): one Page's tabs
    "page": frozenset({"draft", "outline", "runs", "pageruns", "delivery", "folderstat", "evidence",
                       "value", "display", "probe", "latex", "word", "bibex", "bibex-entry",
                       "bibex-verify", "card", "resolve", "answer", "attach", "image"}),
    "paper": frozenset({"paper-board", "paper"}),          # paper: its name before 261007
    "work": frozenset({"work-board", "task-board"}),       # task-board: its name before 261007
    "cowork": frozenset({"cowork-board"}),
    "discovery": frozenset({"discovery-board"}),
    # workbench (the base): Studio's draw, chat and terminal routes (Guide is in ALWAYS_ROUTES).
    "shared": frozenset({"chat", "chat-keep", "sessions", "session-log", "session-name",
                         "stop", "excalidraw", "excalidraw-save", "autodraw", "autodeck",
                         "diagram", "term", "terms", "term-probe", "term-type", "killall",
                         "local-cmd", "release", "shared", "workbench"}),
    "insight": frozenset({"insight", "insight-board"}),
    "design": frozenset({"design", "design-act", "design-board", "design-board-act",
                         "design-bundle"}),
    "labeling": frozenset({"labeling", "labeling-board"}),
}
ALWAYS_ROUTES = frozenset({"health", "asset", "guide"})
ROUTE_ALIASES = {"task": "work"}       # `--only task` still means the work theme (renamed 261007)


def route_allowed(path: str, only) -> bool:
    """Whether a request path is served by a host started with `--only`.

    Static files (anything not under `/_`), Home, `/b/`, `/w/`, health and
    vendored assets always pass. `/_board/<name>...` passes when `<name>` is a
    route of a named workbench, and `/_board/page` (the one Page reader). Everything else, in particular
    `/_term/` and Board write routes, is refused.
    """
    p = path.split("?", 1)[0]
    if not only:
        return True
    if p == "/_excalidraw/_haipipe-xcal.js":
        # Guide's read-only canvas uses the existing storage-isolating boot script.
        return True
    if p in ("", "/", "/boards") or p.startswith(("/b/", "/w/", "/boards/")):
        return True
    if p == "/_board/page":
        return True                      # the one Page reader, shared by every workbench
    if not p.startswith("/_"):
        return True
    if not p.startswith("/_board/"):
        return False
    name = p[len("/_board/"):].split("/", 1)[0]
    if name in ALWAYS_ROUTES:
        return True
    if name == "workbench" and re.search(r"[?&]view=[a-z]", path):
        name = "draft"                   # a Page Task view, through the frame (serve.py PAGE_VIEW_ROUTES)
    allowed = set()
    for w in only:
        allowed |= WORKBENCH_ROUTES.get(ROUTE_ALIASES.get(w, w), frozenset())
    return name in allowed


def static_path_allowed(root: Path, translated: Path) -> bool:
    """Keep source/custody files outside the host's static-file surface.

    The Workbench reads these files server-side through checked presenters. A
    direct static GET would bypass the View's text and custody restrictions,
    including on a host configured for public Board reads.
    """
    try:
        target = translated.resolve()
        relative = target.relative_to(root.resolve())
    except (OSError, RuntimeError, ValueError):
        return False
    parts = [part.casefold() for part in relative.parts]
    name = parts[-1] if parts else ""
    if any(part.startswith(".") for part in parts) or name == "settings.env":
        return False
    if any(part == "corpus-preparation" for part in parts):
        return False
    for index, part in enumerate(parts):
        if part == "labeling":
            generated_board_page = (index == len(parts) - 2 and index > 0
                                    and parts[index - 1] == "board" and name.endswith(".html")
                                    and (target.parent.parent.parent / "board.md").is_file())
            if not generated_board_page:
                return False
    if (name.endswith(".jsonl") or ".jsonl." in name
            or ".private." in name or ".protected." in name):
        return False
    return True

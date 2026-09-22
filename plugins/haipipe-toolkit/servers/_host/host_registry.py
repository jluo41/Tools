"""Discover every server folder the host assembles.

A server folder is one of:
  · ``servers/_host``            the transport (this folder; its mixins sit in ``live/``)
  · ``servers/haipipe-board``    Board-level presenters (home, structure, shell, ...)
  · ``servers/haipipe-page``     the standalone Page server and the reader appearance
  · ``servers/workbench-<name>`` one live tab, the served face of ``haipipe-workbench-<name>``
  · ``plugins/<other>/servers/workbench-<name>``  a workbench shipped by another workbench

Every folder may hold ``*.py`` mixins, importable as ``live.<module>`` through
the ``live`` namespace package in ``_host/live/``, and ``assets/js/**`` and
``assets/css/**`` parts that ``host_assets`` concatenates in sorted relative
order. Nothing here is imported until a route or the build asks for it.
"""
from pathlib import Path

from host_paths import HOST, WORKBENCHES, SERVERS, TOOLKIT


def workbench_folders():
    """``workbench-*`` folders, this workbench first, then every sibling workbench."""
    found = sorted(p for p in SERVERS.glob("workbench-*") if p.is_dir())
    for workbench in sorted(WORKBENCHES.iterdir()):
        if workbench == TOOLKIT or not (workbench / "servers").is_dir():
            continue
        found.extend(sorted(p for p in (workbench / "servers").glob("workbench-*") if p.is_dir()))
    return found


def server_folders():
    """Every folder that may contribute mixins or asset parts, in load order."""
    folders = [HOST, SERVERS / "haipipe-board", SERVERS / "haipipe-page"]
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
    "page": frozenset({"outline", "runs", "pageruns", "delivery", "folderstat", "evidence",
                       "value", "display", "probe", "latex", "word", "bibex", "bibex-entry",
                       "bibex-verify", "card", "resolve", "answer", "attach", "image"}),
    "paper": frozenset({"paper"}),
    "studio": frozenset({"chat", "chat-keep", "sessions", "session-log", "session-name",
                         "stop", "excalidraw", "excalidraw-save", "autodraw", "autodeck",
                         "diagram", "term", "terms", "term-probe", "term-type", "killall",
                         "local-cmd", "release"}),
    "insight": frozenset({"insight", "insight-board"}),
    "design": frozenset({"design", "design-act", "design-board", "design-board-act",
                         "design-bundle"}),
    "labeling": frozenset({"labeling", "labeling-board"}),
}
ALWAYS_ROUTES = frozenset({"health", "asset"})


def route_allowed(path: str, only) -> bool:
    """Whether a request path is served by a host started with `--only`.

    Static files (anything not under `/_`), Home, `/b/`, `/w/`, health and
    vendored assets always pass. `/_board/<name>...` passes when `<name>` is a
    route of a named workbench. Everything else, in particular `/_shell`,
    `/_term/`, `/_events`, panes and Board write routes, is refused.
    """
    p = path.split("?", 1)[0]
    if not only:
        return True
    if p in ("", "/", "/boards") or p.startswith(("/b/", "/w/", "/boards/")):
        return True
    if not p.startswith("/_"):
        return True
    if not p.startswith("/_board/"):
        return False
    name = p[len("/_board/"):].split("/", 1)[0]
    if name in ALWAYS_ROUTES:
        return True
    allowed = set()
    for w in only:
        allowed |= WORKBENCH_ROUTES.get(w, frozenset())
    return name in allowed

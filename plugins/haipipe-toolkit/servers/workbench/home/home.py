"""The read-only SPACE-level Board Home.

This is deliberately not a Board: no board.md, no chat, no durable state.  It
discovers the Board folders already present below the server root and gives the
reader one stable place from which to enter them.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

# The page is split by responsibility; every name stays importable from `live.home`.
from live.home_boards import (  # noqa: F401  re-exported
    BOARD_KINDS, BOARD_STATE, FOLD_OPEN_MAX, GENERIC_BOARD_NAMES, HOME_BRAND, KIND_ICON, KIND_ORDER,
    KIND_THEME, LEGACY_PARTS, PROJECT_FIELD, ROUTE_KIND, SKIP_PARTS, SPINE, STATE, THEME_ALIASES,
    THEME_KIND, THEME_TABLE, THEMES, TITLE, _BOARD_KIND, _DIALECT, _manifests, _project_manifest,
    _skip, block_kind_key, block_theme, board_by_slug, board_kind, board_slug,
    board_workbench_route, discover_boards, frame_url, home_folder_path, home_section, kind_query,
    kind_sort_key, other_space, parse_kinds, project_matches, project_owner, theme_kind_of,
    theme_sort_key)
from live.home_routes import (  # noqa: F401  re-exported
    TAB_SPACE, WORKBENCH_TABS, _page_source, _task_space, old_page_url, resolve_short,
    resolve_workbench)
from live.home_rows import (  # noqa: F401  re-exported
    _block_groups, _home_row, _job_rows, _numbered, _runs_of,
    _stage_pill, _task_runs, _topic_rows, block_link)
from live.home_page import render_home  # noqa: F401  re-exported


class HomeMixin:
    def serve_home(self):
        # `?kind=task[,paper]` and `?project=<Project>` render the filtered view, so a shared
        # link reproduces it
        query = parse_qs(urlsplit(self.path).query)
        target = Path(self.root) / (query.get("project") or [""])[0]
        if set(query) <= {"section", "group", "project"} and target.resolve().is_dir() \
                and Path(self.root).resolve() in [target.resolve(), *target.resolve().parents]:
            # the SPACE's page, or `?project=<Project>`'s page, like every level's (hai-ui, JL 261029)
            from live import focus_page, frame as _frame
            body = focus_page.render(_frame.VANILLA, Path(self.root), target,
                                     (query.get("section") or [""])[0], (query.get("group") or [""])[0]).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store, must-revalidate")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
            return
        kind = ",".join(query.get("kind", []))
        project = (query.get("project") or [""])[0]
        body = render_home(
            self.root,
            getattr(self, "space_name", ""),
            getattr(self, "public_url", ""),
            kind=kind,
            project=project,
            archived=(query.get("archived") or [""])[0] == "1",
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def is_home_request(self):
        path = urlsplit(self.path).path.rstrip("/") or "/"
        return path in {"/", "/boards"}

    def short_request(self):
        """`/b/<slug>` or `/b/<slug>/<page-id>`, or None for anything else."""
        path = urlsplit(self.path).path.rstrip("/")
        m = re.match(r"^/b/([^/]+)(?:/([^/]+))?$", path)
        return (m.group(1), m.group(2) or "") if m else None

    def workbench_request(self):
        """`/w/<slug>[/<page-id>[/<tab>]]` -> (slug, page-id, tab), else None."""
        path = urlsplit(self.path).path.rstrip("/")
        m = re.match(r"^/w/([^/]+)(?:/([^/]+))?(?:/([^/]+))?$", path)
        return (m.group(1), m.group(2) or "", m.group(3) or "") if m else None

    def serve_workbench(self, slug, anchor, tab):
        """302 to the long `/_board/<route>?path=…&file=…` URL, or a 404 that says why.

        The Location is path-only on purpose: the browser keeps whatever host
        it arrived on, so one link body works for every DOMAIN the server is
        reachable at (127.0.0.1, the Tailscale IP, a configured public URL).
        Extra query (`?run=…`, `&lens=…`) is carried across.
        """
        if slug == "shared" and not anchor and board_by_slug(self.root.resolve(), slug) is None:
            # The Shared Workbench is served at its short address itself; the bar keeps /w/shared.
            return self.shared_view(head_only=self.command == "HEAD")
        target, reason = resolve_workbench(self.root, slug, anchor, tab, getattr(self, "only", None) or frozenset())
        if target is None:
            return self.send_error(404, reason)
        query = urlsplit(self.path).query
        if query:
            target = f"{target}&{query}"
        self.send_response(302)
        self.send_header("Location", target)
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def serve_short(self, slug, anchor):
        """302 to the live Page reader (or the Board workbench), keeping the query string.

        A redirect rather than serving the bytes here, so the address bar ends
        up on the canonical URL: every relative link, asset and write-back path
        inside the page is written against that location, and serving the file
        from `/b/...` would break all of them.
        """
        target = resolve_short(self.root, slug, anchor, getattr(self, "only", None) or frozenset())
        if target is None:
            return self.send_error(404, "no such board or page")
        query = urlsplit(self.path).query
        if query:
            target = f"{target}?{query}"
        self.send_response(302)
        self.send_header("Location", target)
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Content-Length", "0")
        self.end_headers()

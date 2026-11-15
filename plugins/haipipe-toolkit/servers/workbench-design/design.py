"""🎨 Design · live Page-Folder presenter for ``workbench-design``.

It reads only the current Design Folder's contract files: the Design Item
register, ``run-design-*`` Tickets, runtime receipts, ``checks.yaml``, content
artifacts, and ``decision.yaml``.  Every state on the page is derived from
those bytes at read time.  The only writes it exposes are the Design
contract's Commission release, the queueing of agent Tickets (Generate,
Verify), and a new register row; they live in
``servers/workbench-design/design_actions.py`` and write exactly the contract files.

The folder is read by the ``design_core_*`` modules beside this one (base readers,
records, renders, insight, goal, names, runs); every name they hold still answers here.
"""
from __future__ import annotations

import re
from pathlib import Path

from urllib.parse import parse_qs, quote, urlparse

from live.insightboard import handoff_records, is_insight_board

# The parts of this module now live in design_core_*; every name answers here too.
from live.design_core_base import (  # noqa: F401  (re-exported)
    _DESIGN_MARKER, _FIELD, _ITEM_FIELDS, _ITEM_HEAD, _ITEM_LISTS, _LEGACY_RUN, _READS, _RUN_FILE, _RUN_FILE_NEW,
    _SIGNED, _STEP, _TITLE, _UNIT_CHECKER, _audit, _escape, _legacy_reason, _nearest_board, _read, _relative_href,
    _unit_gate, _yaml, design_contract_status, is_current_design_page, yaml,
)
from live.design_core_records import (  # noqa: F401  (re-exported)
    _ALLOWED, _actor, _fold_state, _held_at, _load_runs, _register, _stale_names, _verified_design, _when,
    plan_folder, shown_design,
)
from live.design_core_renders import _PICTURE, _render_for, _renders, design_picture  # noqa: F401  (re-exported)
from live.design_core_insight import (  # noqa: F401  (re-exported)
    _BECAUSE, _HANDOFF_KEY, _INSIGHT_PAGE, _INSIGHT_REF, _LEVEL_WORD, _ROLE_WORDS, _board_page, _cited_page,
    _evidence_rows, _handoff_says, _insight_space, _partitions_of, _relocated, because_rule, because_words, name_refs,
)
from live.design_core_goal import (  # noqa: F401  (re-exported)
    _INPUT_BLOCKS, _TABLE_ROW, _VENUE_DIR, _VENUE_LABEL, _VENUE_WORDS, LINK_SLOT, _goal, _input_sections, brief_page,
    brief_rows, design_input, design_title, is_task_header, venue_defaults, venue_word, with_link,
)
from live.design_core_names import (  # noqa: F401  (re-exported)
    _FOLDER_FILE, _OLD_FOLDER, _OLD_GROUP, _folder_hits, design_number, modern_file, renamed_folder,
)
from live.design_core_runs import (  # noqa: F401  (re-exported)
    _CARD_SPACE, _DESIGN_RUN_GUIDE, _PANEL_STATUS, _RUN_CARDS, _RUNNING_STATES, _next_design_run,
    design_chat_action, design_chat_copy, design_chat_copy_script, design_chat_prompt, design_next_run,
    design_run_types, design_runs_panel, runs_panel_assets,
)


def _declared_insight_boards(board_root: Path, names: list[str] | None = None) -> list[Path]:
    """Resolve the Insight boards named by the DesignBoard ``reads:`` line, or by ``names``."""
    if board_root is None:
        return []
    if names is None:
        text = _read(board_root / "board.md")
        match = _READS.search(text)
        if not match:
            return []
        names = re.split(r"\s*·\s*", match.group(1))
    found = {}
    for raw in names:
        name = raw.strip().strip("`'\"")
        if not name:
            continue
        for candidate in (board_root.parent / name, board_root / name):
            try:
                candidate = candidate.resolve()
            except OSError:
                continue
            if (candidate / "board.md").is_file() and is_insight_board(candidate):
                found[candidate] = candidate
    return sorted(found.values(), key=lambda path: path.as_posix())


def _insight_bindings(page_src: Path, server_root: Path, names: list[str] | None = None) -> dict:
    """Read the DesignBoard -> Insight board -> signed page binding chain.

    ``names`` overrides the board's ``reads:`` line (a Brief line may name the
    Insight board its design task draws from)."""
    design_board = _nearest_board(page_src)
    requested = [n.strip() for n in (names or []) if n and n.strip()]
    boards = []
    for board in _declared_insight_boards(design_board, requested or None):
        try:
            relative = board.resolve().relative_to(Path(server_root).resolve()).as_posix()
        except (OSError, ValueError, RuntimeError):
            live_url = ""
        else:
            live_url = "/_board/insight-board?path=%s" % quote(relative, safe="")
        records = handoff_records(board)
        boards.append({
            "board": board, "title": board.name, "live_url": live_url,
            "handoffs": records,
            "bindable": [row for row in records if row["bindable"]],
        })
    bindable = [row for board in boards for row in board["bindable"]]
    return {
        "design_board": design_board, "boards": boards, "bindable": bindable, "requested": requested,
        "status": ("bound" if bindable else "blocked" if boards
                   else "missing" if requested else "not-declared"),
    }


def _open_request(folder: Path, stem: str) -> dict | None:
    from live.design_actions import open_draft_request
    try:
        return open_draft_request(folder, stem)
    except (OSError, ValueError):
        return None


def design_snapshot(page_src: Path, server_root: Path | None = None) -> dict:
    """Collect the read-only Design Folder projection."""
    page_src = Path(page_src)
    folder = page_src.parent
    current, reason = design_contract_status(page_src)
    root = Path(server_root or folder)
    text = _read(page_src)
    title = (_TITLE.search(text).group(1).strip() if _TITLE.search(text) else page_src.stem)
    items, register_path = _register(folder, page_src.stem)
    runs = _load_runs(folder) if current else []
    human = next((r["actor"] for r in runs if r["mode"] == "human" and r["actor"] != "not recorded"), "person")
    known = {item["id"] for item in items}
    renders = _renders(folder, runs)
    for item in items:
        item["runs"] = [run for run in runs if run["item"] == item["id"]]
        item["state"], item["glyph"], item["waiting"] = _fold_state(item["runs"], human)
        item["evidence_rows"] = _evidence_rows(folder, item)
        item["because_rule"] = because_rule(item)
        latest = next((r for r in reversed(item["runs"])
                       if r["kind"] == "generate" and r["artifacts"] and r["status"] == "complete"), None)
        item["latest"] = ({"run": latest["id"], "text": latest["artifacts"][0]["text"],
                           "status": latest["status"], "verdict": latest["verdict"]} if latest else None)
        # A passed Verify is the delivery gate.  Keep the old projection for
        # callers that still inspect it, but never use it as a new workflow.
        try:
            item["ready"] = _verified_design(item)
            delivery_error = "no valid independent Verify target" if item["state"] == "ready" and not item["ready"] else ""
        except ValueError as exc:
            item["ready"], delivery_error = None, str(exc)
        if delivery_error:
            item["state"], item["glyph"] = "records invalid", "⚠"
            item["waiting"] = f"you · the records for this item do not line up: {delivery_error}"
        item["adopted"] = None
        shown = shown_design(item)
        item["render"] = _render_for(renders.get(item["id"], []), shown["run"]) if shown else None
    goal = _goal(folder, _nearest_board(page_src), items)
    insight = _insight_bindings(page_src, root, [goal["insight"]] if goal["insight"] else None)
    return {
        "current": current, "reason": reason, "title": title, "page": page_src,
        "folder": folder, "root": root, "items": items, "register": register_path,
        "runs": runs, "unassigned": [run for run in runs if run["item"] not in known],
        "insight": insight,
        "goal": goal,
        "draft_request": _open_request(folder, page_src.stem),
        "insight_space": _insight_space(items, insight),
        "audit": _audit(folder) if current else [],
        "human": human, "yaml": yaml is not None,
    }


class DesignMixin:
    """GET/HEAD/POST surface for a current Design Page-Folder."""

    def design_view(self, head_only=False):
        from live.design_page import _pick_board_page, _pick_method_page, render_design
        query = parse_qs(urlparse(self.path).query)
        short = (query.pop("folder", None) or [""])[0].strip("/")
        if short and not query.get("file"):
            # short link: ?folder=Design-01-… names the Design Folder; the board is the one given or the only one
            from urllib.parse import urlencode
            from live.designboard import design_boards, resolve_board
            root = Path(self.root)
            named_board = (query.get("path") or query.pop("board", None) or [""])[0]
            board = resolve_board(root, named_board)
            if board is None and not named_board:
                # several DesignBoards: the folder picks its board when exactly one holds it,
                # by its exact name first (every board has a Design-01), then by an old name
                boards = design_boards(root)
                holders = [b for b in boards if _folder_hits(b, short)]
                board = holders[0] if len(holders) == 1 else None
                if board is None:
                    # never guess: two boards' Design-01 are unrelated designs (audit N5)
                    return self._design_send(_pick_board_page(root, short, holders or boards, bool(holders)),
                                             404, head_only)
            hits = _folder_hits(board, short) if board is not None else []
            if len(hits) > 1:
                # the same task under several methods: say which, never guess
                return self._design_send(_pick_method_page(root, board, hits), 404, head_only)
            if hits:
                rel = board.resolve().relative_to(root.resolve()).as_posix()
                query.pop("board", None)
                query["path"] = ["/" + ("" if rel == "." else rel + "/") + "board.md"]
                query["file"] = [hits[0]]
                self.send_response(302)
                self.send_header("Location", "/_board/design?" + urlencode(query, doseq=True))
                self.send_header("Content-Length", "0")
                self.end_headers()
                return None
        payload = {"path": (query.get("path") or [""])[0],
                   "file": (query.get("file") or [""])[0]}
        from live.designboard import resolve_board
        board = resolve_board(Path(self.root), payload["path"])
        asked_exists = board is not None and bool(payload["file"]) and (board / payload["file"]).is_file()
        modern = payload["file"] if asked_exists else modern_file(payload["file"])
        named = _FOLDER_FILE.match(modern)
        if named and not asked_exists:
            current = renamed_folder(board, named.group(2), named.group(1))
            modern = f"{named.group(1)}/{current}/{current}.md"
        if board is not None and not (board / modern).is_file():
            # no folder of that name today: read the link as given, so a legacy
            # folder is named unsupported (410) instead of answering a bare 404
            modern = payload["file"]
        if modern != payload["file"]:
            # an old bookmark: send the browser to the current folder name so the URL updates too
            from urllib.parse import urlencode
            query["file"] = [modern]
            self.send_response(302)
            self.send_header("Location", "/_board/design?" + urlencode(query, doseq=True))
            self.send_header("Content-Length", "0")
            self.end_headers()
            return None
        got = self.target(payload)
        if got[0] is None:
            body = f"<h1>🎨 design</h1><p>{_escape(got[1])}</p>".encode("utf-8")
            return self._design_send(body, 404, head_only)
        page_src = Path(got[0])
        snapshot = design_snapshot(page_src, self.root)
        if payload["path"]:
            snapshot["csv_url"] = (f'/_board/design-bundle?path={quote(payload["path"], safe="")}'
                                   f'&folder={quote(snapshot["folder"].name, safe="")}')
        code = 200 if snapshot["current"] else 410
        body = render_design(
            snapshot,
            (query.get("space") or ["goal"])[0],
            (query.get("item") or [""])[0],
            query=payload,
        ).encode("utf-8")
        return self._design_send(body, code, head_only)

    def _design_send(self, body: bytes, code: int, head_only: bool):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def plug_design(self, payload):
        payload = dict(payload, file=modern_file(str(payload.get("file") or "")))
        got = self.target(payload)
        if got[0] is None:
            return None, got[1]
        page_src = Path(got[0])
        current, reason = design_contract_status(page_src)
        if not current:
            return None, reason
        return {
            "url": "/_board/design?path=%s&file=%s"
            % (quote(payload.get("path") or ""), quote(payload.get("file") or "")),
        }, None

    def design_act(self, payload):
        """One Design action: a human decision Run, an agent queue Ticket, or a register row."""
        payload = dict(payload, file=modern_file(str(payload.get("file") or "")))
        got = self.target(payload)
        if got[0] is None:
            return None, got[1]
        page_src = Path(got[0])
        current, reason = design_contract_status(page_src)
        if not current:
            return None, reason
        result, err = perform_action(page_src, payload)
        if err:
            return None, err
        item = result.get("item") or ""
        if item == "__all__":
            item = ""
        action = payload.get("action")
        space = "goal" if action == "draft-request" else "design"
        result["url"] = ("/_board/design?path=%s&file=%s&space=%s&item=%s"
                         % (quote(payload.get("path") or ""), quote(payload.get("file") or ""), space, quote(item)))
        return result, None


def perform_action(page_src: Path, payload: dict) -> tuple[dict | None, str | None]:
    """Route one action to ``live.design_actions``; refusals come back as text."""
    from live import design_actions as acts

    folder = page_src.parent
    stem = page_src.stem
    action = str(payload.get("action") or "")
    if action in {"adopt", "decline", "revise", "hold", "adopt-all", "release-all", "queue-all"}:
        return None, f"unknown action {action!r}"
    snapshot = design_snapshot(page_src, folder)
    items = {item["id"]: item for item in snapshot["items"]}
    item_id = str(payload.get("item") or "")
    actor = str(payload.get("actor") or "")
    words = str(payload.get("words") or "")
    human = snapshot.get("human", "person")
    try:
        if action == "add-item":
            out = acts.add_item(folder, stem, payload)
            return {"item": out["item"], "register": out["register"], "audit": _audit(folder)}, None
        if action == "draft-request":
            goal = snapshot["goal"]
            rows = [r for block in snapshot["insight_space"]["items"] for r in block["rows"]]
            if not rows:
                rows = [{"word": "signed insight", "path": u["name"], "signed": u["signed"], **_handoff_says(_read(u["file"]))}
                        for u in snapshot["insight_space"]["unused"] if u["signed"]]
            out = acts.request_draft(folder, stem, goal, rows, max(goal["wanted"] - goal["registered"], 0), actor or human)
            return {**out, "item": "", "audit": _audit(folder)}, None
        item = items.get(item_id)
        if item is None:
            return None, f"unknown Design Item {item_id!r}; add it to the register first"
        allowed = _ALLOWED.get(action)
        held = _held_at(item)
        if allowed is not None and item["state"] not in allowed and not (
                held == "commission" and action.startswith("commission-")):
            return None, (f'{item_id} is "{item["state"]}"; '
                          f'{"it waits on " + item["waiting"] if item["waiting"] else "nothing is waiting"}, not {action}')
        if action in ("commission-release", "commission-hold"):
            out = acts.commission(folder, stem, item, actor, words, action.split("-")[1])
        elif action == "queue-generate":
            out = acts.queue_generate(folder, stem, item, item["runs"])
        elif action == "queue-revise":
            out = acts.queue_generate(folder, stem, item, item["runs"],
                                      feedback=str(payload.get("feedback") or words or "revise"))
        elif action == "queue-verify":
            out = acts.queue_verify(folder, stem, item, item["runs"])
        elif action == "requeue":
            out = acts.requeue(folder, stem, item, item["runs"])
        else:
            return None, f"unknown action {action!r}"
    except acts.ActionError as exc:
        return None, str(exc)
    except (OSError, ValueError, KeyError) as exc:
        return None, f"{type(exc).__name__}: {exc}"
    out["item"] = item_id
    out["audit"] = _audit(folder)
    return out, None


# The page itself is drawn in design_page.py; these names still answer here, so older imports keep working.
_PAGE_NAMES = frozenset((
    "_ABBREV", "_CONTRACT_WORDS", "_CRITERION_WORDS", "_CSS", "_FROM", "_LEVEL_ID", "_LINEAGE", "_PAGE_STEM_ID",
    "_REF_TOKEN", "_SLOT_PART", "_SLOT_TOKEN", "_STEP_WORD", "_SUPPORT_ROLES", "_actions", "_artifact_details",
    "_bet_changed", "_card_columns", "_chain_heads", "_chain_html", "_checks_details", "_code", "_compact",
    "_criterion_words", "_design_runs_list", "_element_matrix_html", "_elements_html", "_evaluation_col", "_expand",
    "_href", "_ids", "_input_html", "_insight_href", "_item_card", "_json", "_level", "_level_of", "_norm",
    "_page_id", "_page_link", "_page_words", "_pick_board_page", "_pick_method_page", "_rationale_col",
    "_record_html", "_review_notes", "_revise_of", "_row_lineage", "_row_texts", "_rule_checks", "_rule_words",
    "_run_rows", "_sms_bubble", "_task_block", "_walk", "_whole_word", "because_rows", "design_elements",
    "element_record", "element_slots", "evidence_chain", "plain_words", "record_reading", "render_design",
    "run_short", "shared_rules", "slot_reading",
))


def __getattr__(name: str):
    if name in _PAGE_NAMES:
        from live import design_page
        return getattr(design_page, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

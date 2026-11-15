"""🏷 Labeling · four Spaces over one page-local labeling/ job, a Runs panel beside each, plus one write door.

It wears the shell every workbench shares (haipipe-toolkit servers/README.md "Adding a
workbench"): the title, an `all labeling jobs` link, a band (phase · round · guideline ·
HOLD), then the Space row with the shared Guide first (the `labeling`
entry of workbench/guide/guide_families.py), each Space's View tabs and content in one
box, and the shared Runs panel (live.runs_panel) folded to a strip on its right. Labeling
passes its own Run cards to that panel so Resume and Rerun stay gated. The Board level
(`/w/<board>`) wears the same title and band, with Guide and one Jobs Space.

Data · Labeling · Quality · Delivery are views over canonical files; the
overview never renders item text and never upgrades an observed file to a
passed gate.  Labeling → Definition holds the label definitions and Confirm meaning.  Round item text
appears only in Labeling → Rounds, and only for items already shown to the
person; the labels come from the chat.  Every write through
``POST /_board/labeling/act`` goes through the
subjective-label engine (``job.confirm_meaning`` and ``calibration``), which
re-checks the caller-supplied configured authority id, HOLD, G0, the event
order, and sealed custody on each call. The Workbench does not authenticate
the caller's identity.
"""
from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath
from urllib.parse import parse_qs, quote, urlparse

from live.labeling_job import _canonical_job_module, _labeling_lane, is_labeling_surface_page
from live.labeling_hold import _calibration_module, _embedding_module, _meaning_store_module, generated_page_url
from live.labeling_model import _reap_when_done
from live.labeling_data_view import _corpus_view_module
from live.labeling_page import render
from live.labeling_board import board_jobs, render_board


# the modules this one was split into, newest layer first: an old name is looked up in them in this order
SIBLINGS = ("labeling_board", "labeling_page", "labeling_runs_view", "labeling_rounds_view", "labeling_data_view",
            "labeling_embedding_view", "labeling_model", "labeling_hold", "labeling_job")


def __getattr__(name: str):
    """An old name (``live.labeling.render``, ``from live.labeling import inspect``) still answers from the sibling
    module that holds it now, so callers need not change."""
    import importlib
    for sibling in SIBLINGS:
        mod = importlib.import_module(f"live.{sibling}")
        if name in vars(mod):
            return vars(mod)[name]
    raise AttributeError(f"module 'live.labeling' has no attribute {name!r}")


class LabelingMixin:
    """The 🏷 tab: four Spaces over one labeling/ lane, plus the labeling writer door."""

    def _labeling_page_target(self, file_q: str):
        """Resolve a canonical Page folder only on the dedicated labeling host."""
        if getattr(self, "only", None) != frozenset({"labeling"}):
            return None, "standalone Labeling Page requires the dedicated labeling host"
        if not isinstance(file_q, str):
            return None, "file must be a string"
        if (not file_q or file_q.startswith("/") or "\\" in file_q
                or ":" in file_q or "\x00" in file_q):
            return None, "unsafe Page folder path"
        parts = PurePosixPath(file_q).parts
        if (any(part in {"", ".", ".."} for part in file_q.split("/"))
                or not file_q.endswith(".md")):
            return None, "unsafe Page folder path"
        root = self.root.resolve()
        candidate = root
        for part in parts:
            candidate = candidate / part
            if candidate.is_symlink():
                return None, "Page folder may not use symlinks"
        if candidate.parent.name != candidate.stem or not candidate.is_file():
            return None, "file must be a canonical <Page>/<Page>.md"
        try:
            candidate.resolve().relative_to(root)
        except (ValueError, OSError, RuntimeError):
            return None, "Page folder is outside the served root"
        if not is_labeling_surface_page(candidate):
            return None, "Page has no labeling lane"
        return candidate, None

    def labeling_page_view(self, head_only=False):
        q = parse_qs(urlparse(self.path).query)
        page_src, err = self._labeling_page_target((q.get("file") or [""])[0])
        if page_src is None:
            return self.reply(400, {"ok": False, "err": err})
        file_q = page_src.relative_to(self.root.resolve()).as_posix()
        body = render(page_src, "", file_q, "", None, standalone=True).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def labeling_view(self, head_only=False):
        q = parse_qs(urlparse(self.path).query)
        path_q = (q.get("path") or [""])[0]
        file_q = (q.get("file") or [""])[0]
        page_q = (q.get("page") or [""])[0]
        got = self.target({"path": path_q, "file": file_q})
        if got[0] is None:
            return self.reply(400, {"ok": False, "err": got[1]})
        if not is_labeling_surface_page(got[0]):
            return self.reply(404, {"ok": False, "err": "Page has no labeling lane"})
        if not generated_page_url(path_q, file_q, page_q, got[1]):
            return self.reply(400, {"ok": False,
                                    "err": "missing or mismatched generated Page URL"})
        document = render(got[0], path_q, file_q, page_q, got[1])
        if (q.get("focus") or [""])[0] == "1":
            from live.labeling_focus import focused_engine_document
            document = focused_engine_document(document)
        body = document.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def plug_labeling(self, p):
        got = self.target(p)
        if got[0] is None:
            return None, got[1]
        if not is_labeling_surface_page(got[0]):
            return None, "Page has no labeling lane"
        path_q = p.get("path") or ""
        file_q = p.get("file") or ""
        page_q = p.get("page") or ""
        if not generated_page_url(path_q, file_q, page_q, got[1]):
            return None, "missing or mismatched generated Page URL"
        return {"url": "/_board/labeling?path=%s&file=%s&page=%s" %
                (quote(path_q), quote(file_q), quote(page_q))}, None

    def _labeling_board_target(self, path_q: str):
        got = self.target({"path": path_q, "file": "board.md"})
        if got[0] is None:
            return None, got[1]
        if Path(got[0]).name != "board.md":
            return None, "the Board-level Labeling view needs file=board.md"
        return got[1], None

    def labeling_board_view(self, head_only=False):
        q = parse_qs(urlparse(self.path).query)
        path_q = (q.get("path") or [""])[0]
        board_dir, err = self._labeling_board_target(path_q)
        if board_dir is None:
            return self.reply(400, {"ok": False, "err": err})
        body = render_board(board_dir, path_q).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def plug_labeling_board(self, p):
        path_q = p.get("path") or ""
        board_dir, err = self._labeling_board_target(path_q)
        if board_dir is None:
            return None, err
        count = len(board_jobs(board_dir, path_q, probe=True)["jobs"])
        return {"url": "/_board/labeling-board?path=%s" % quote(path_q), "jobs": count}, None

    # ── the items Task's three narrow doors (b15 s41): Draw again reads, Sign/Agree and a pasted note write ──
    NOTE_TYPES = {"image/png": ".png", "image/jpeg": ".jpg", "image/gif": ".gif", "image/webp": ".webp"}
    NOTE_MAX = 8 * 1024 * 1024

    def _items_task_target(self, task_q):
        """A SPACE-relative items Task folder inside the served root, or (None, why)."""
        if (not isinstance(task_q, str) or not task_q or task_q.startswith("/") or "\\" in task_q
                or "\x00" in task_q or any(part in {"", ".", ".."} for part in task_q.strip("/").split("/"))):
            return None, "unsafe Task path"
        root = self.root.resolve()
        task = (root / task_q.strip("/")).resolve()
        try:
            task.relative_to(root)
        except ValueError:
            return None, "Task is outside the served root"
        if not (task / f"{task.name}.md").is_file():
            return None, "not a Task folder"
        from live import task_labeling as T
        if T.types_of(task) != ("items",) or T.IT is None:
            return None, "not an items Task, or the preparation engine is absent"
        return task, None

    def _same_origin(self):
        origin = self.headers.get("Origin") or ""
        return not origin or urlparse(origin).netloc == (self.headers.get("Host") or "")

    def _form_page_target(self, page_q):
        """A labeling page that may hold collection Runs (a Block, a Job or a Task of any labeling kind: items, meaning,
        expression, building, ...) inside the served root, or None. frame._file_url sends every labeling form here."""
        if (not isinstance(page_q, str) or not page_q or page_q.startswith("/") or "\\" in page_q
                or "\x00" in page_q or any(part in {"", ".", ".."} for part in page_q.strip("/").split("/"))):
            return None
        root = self.root.resolve()
        page = (root / page_q.strip("/")).resolve()
        try:
            page.relative_to(root)
        except ValueError:
            return None
        if not ((page / f"{page.name}.md").is_file() or (page / "board.md").is_file()):
            return None
        from live import frame
        if frame.level_of(page) not in ("Block", "Job", "Task"):
            return None
        if "labeling" not in (p.casefold() for p in page.relative_to(root).parts):
            return None
        return page

    def labeling_form_view(self, head_only=False):
        """A labeling page's interaction form, and the applied.md beside it (b15 s58, stage 2): a static GET never reads a
        labeling folder (host_registry.static_path_allowed), so the Run's own form opens here and nothing else does. The
        URL keeps the file's path, so the form's copied `form:` line still names its Run (collect.py save checks it).
        Every labeling Task kind's forms open here (round 2: an items or expression Task's Answer gave a 404)."""
        from urllib.parse import unquote
        rel = unquote(self.path.split("?", 1)[0][len("/_board/labeling/form/"):])
        parts = rel.split("/")
        if (not rel or rel.startswith("/") or "\\" in rel or "\x00" in rel or any(x in {"", ".", ".."} for x in parts)
                or len(parts) < 4 or parts[-3] != "runs" or not re.fullmatch(r"r\d\d_collect_[a-z0-9_]+", parts[-2])
                or parts[-1] not in (parts[-2] + ".html", "applied.md")):
            return self.send_error(404, "not found")
        task = self._form_page_target("/".join(parts[:-3]))
        if task is None:
            return self.send_error(404, "not found")
        path = task / "runs" / parts[-2] / parts[-1]
        if not (task / "runs" / parts[-2]).is_dir() or (not path.is_file() and parts[-1] != "applied.md"):
            return self.send_error(404, "not found")
        body = path.read_bytes() if path.is_file() else b""      # no applied.md yet: no flags, said as an empty file
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8" if path.suffix == ".html" else "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def labeling_sample_view(self, head_only=False):
        """Draw again: random raw rows or items, read live; nothing written (s41-D12)."""
        q = parse_qs(urlparse(self.path).query)
        task, err = self._items_task_target((q.get("task") or [""])[0])
        if task is None:
            return self.reply(400, {"ok": False, "err": err})
        kind = (q.get("kind") or [""])[0]
        if kind not in ("raw", "items"):
            return self.reply(400, {"ok": False, "err": "kind is raw or items"})
        try:
            seed = int((q.get("seed") or ["7"])[0])
        except ValueError:
            return self.reply(400, {"ok": False, "err": "seed is a whole number"})
        from live import task_labeling as T
        body = T.sample_html(task, self.root.resolve(), kind, seed).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def labeling_items_act(self, p):
        """A person signs a recipe or agrees a build on a planned Run's card; only then may it run (s41-D10)."""
        if not self._same_origin():
            return 403, {"ok": False, "err": "cross-origin write refused"}
        task, err = self._items_task_target(p.get("task"))
        if task is None:
            return 400, {"ok": False, "err": err}
        if p.get("action") != "sign":
            return 400, {"ok": False, "err": "the only action here is sign"}
        run = str(p.get("run") or "")
        if not re.fullmatch(r"r\d\d_[A-Za-z0-9_]+", run):
            return 400, {"ok": False, "err": "a Run is named rNN_<name>"}
        if not str(p.get("by") or "").strip():      # a sign needs no name: the page shows "✅ <date>" (JL: no names on
            p["by"] = "a person"                     # a page); a private project may still type one
        from live import task_labeling as T
        try:
            signs = T.IT.sign(task, run, str(p["by"]))
        except SystemExit as e:
            return 409, {"ok": False, "err": str(e)}
        return 200, {"ok": True, "signs": signs}

    def _steps_task_target(self, task_q):
        """A SPACE-relative meaning or expression Task folder inside the served root, or (None, why)."""
        if (not isinstance(task_q, str) or not task_q or task_q.startswith("/") or "\\" in task_q
                or "\x00" in task_q or any(part in {"", ".", ".."} for part in task_q.strip("/").split("/"))):
            return None, "unsafe Task path"
        root = self.root.resolve()
        task = (root / task_q.strip("/")).resolve()
        try:
            task.relative_to(root)
        except ValueError:
            return None, "Task is outside the served root"
        if not (task / f"{task.name}.md").is_file():
            return None, "not a Task folder"
        from live import labeling_steps as S
        if not S.kind(task):
            return None, "not a meaning or expression Task"
        return task, None

    def labeling_approve(self, p):
        """Your sign on a meaning Task's guideline mNN (b15 s58-D15, Q6): meaning/mNN.approved.yaml, written by the
        engine's meaning_versions.approve; the expression Task runs only on a signed meaning. On an expression Task the
        version is a round eNN: your sign on its release (meaning_versions.sign_release)."""
        if not self._same_origin():
            return 403, {"ok": False, "err": "cross-origin write refused"}
        task, err = self._steps_task_target(p.get("task"))
        if task is None:
            return 400, {"ok": False, "err": err}
        from live import labeling_steps as S
        if S.kind(task) not in ("meaning", "expression"):
            return 400, {"ok": False, "err": "not a meaning or expression Task"}
        sign = S.MV.approve if S.kind(task) == "meaning" else S.MV.sign_release
        try:
            signed = sign(task, str(p.get("version") or ""), str(p.get("by") or ""))
        except ValueError as err:
            return 409, {"ok": False, "err": str(err)}
        return 200, {"ok": True, "signed": signed}

    def labeling_notes(self, p):
        """A pasted image, kept in the Task's notes/ so the prompt can carry its path (s41-D14)."""
        import base64
        from datetime import datetime
        if not self._same_origin():
            return 403, {"ok": False, "err": "cross-origin write refused"}
        task, err = self._items_task_target(p.get("folder"))
        if task is None:                                # a meaning or expression Task's prompt takes an image too (s58)
            task, err2 = self._steps_task_target(p.get("folder"))
            if task is None:
                return 400, {"ok": False, "err": err if err2 == "not a meaning or expression Task" else err2}
        m = re.fullmatch(r"data:([\w/+.-]+);base64,(.+)", str(p.get("data") or ""), re.S)
        if not m or m.group(1) not in self.NOTE_TYPES:
            return 400, {"ok": False, "err": "a pasted note is a png, jpeg, gif or webp image"}
        try:
            raw = base64.b64decode(m.group(2), validate=True)
        except ValueError:
            return 400, {"ok": False, "err": "the image is not valid base64"}
        if len(raw) > self.NOTE_MAX:
            return 413, {"ok": False, "err": "an image note is at most 8 MB"}
        notes = task / "notes"
        notes.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%y%m%d-%H%M%S")
        n = 1
        while (notes / f"{stamp}-{n}{self.NOTE_TYPES[m.group(1)]}").exists():
            n += 1
        out = notes / f"{stamp}-{n}{self.NOTE_TYPES[m.group(1)]}"
        out.write_bytes(raw)
        return 200, {"ok": True, "path": out.relative_to(self.root.resolve()).as_posix()}

    # ── a building Task's decision report (b15 j01 s58 C2; s03 CONTRACTS.md v2): save a draft, submit the answers ──
    DECISION_ACTIONS = ("decision_draft_save", "decision_feedback_submit")
    DECISION_MAX = 256 * 1024            # one report's answers; the host's own request limits still apply first

    def _building_task_target(self, task_q):
        """A SPACE-relative building Task folder (`task-type: labeling-building`) inside the served root, or (None, why)."""
        if (not isinstance(task_q, str) or not task_q or task_q.startswith("/") or "\\" in task_q
                or "\x00" in task_q or any(part in {"", ".", ".."} for part in task_q.strip("/").split("/"))):
            return None, "unsafe Task path"
        root = self.root.resolve()
        task = (root / task_q.strip("/")).resolve()
        try:
            task.relative_to(root)
        except ValueError:
            return None, "Task is outside the served root"
        if not (task / f"{task.name}.md").is_file():
            return None, "not a Task folder"
        from live import labeling_theme as LT
        if LT.types_of(task) != ("building",):
            return None, "not a building Task"
        return task, None

    def labeling_decision_act(self, p):
        """Save a draft, or submit the answers, to a report published in the building Task's lane (<task>/labeling/).

        A submission is received, never applied: integrating it into the rules is the Meaning Loop's later, separate
        step (CONTRACTS.md v2, section 6). ``human_id`` is the caller's word, recorded as local attestation; it is not
        verified identity, and no shared respondent may use this door until an assigned-job permission exists.
        """
        if not self._same_origin():
            return 403, {"ok": False, "err": "cross-origin write refused"}
        if getattr(getattr(self, "server", None), "read_only", False):
            return 403, {"ok": False, "err": "this workbench is read-only"}
        task, err = self._building_task_target(p.get("path"))
        if task is None:
            return 400, {"ok": False, "err": err}
        if p.get("attest") is not True:
            return 400, {"ok": False, "err": "decision answers need an explicit caller attestation"}
        actor = re.sub(r"[^A-Za-z0-9_-]+", "-", str(p.get("human_id") or "").strip()).strip("-")[:64]
        if not actor:
            return 400, {"ok": False, "err": "type your name to save or submit"}
        answers = p.get("answers")
        if not isinstance(answers, dict):
            return 400, {"ok": False, "err": "answers is an object keyed by decision"}
        if len(json.dumps(answers)) > self.DECISION_MAX:
            return 413, {"ok": False, "err": "these answers are too long to save at once"}
        try:
            revision = int(p.get("report_revision"))
        except (TypeError, ValueError):
            return 400, {"ok": False, "err": "report_revision is a whole number"}
        store = _meaning_store_module()
        if store is None:
            return 500, {"ok": False, "err": "the decision store is not available"}
        lane, report_id = task / "labeling", str(p.get("report_id") or "")
        try:
            if p.get("action") == "decision_draft_save":
                try:
                    expected = int(p.get("expected_draft_revision") or 0)
                except (TypeError, ValueError):
                    return 400, {"ok": False, "err": "expected_draft_revision is a whole number"}
                draft = store.save_draft(lane, report_id, revision, actor, answers, expected, str(p.get("comments") or ""))
                return 200, {"ok": True, "draft": {"draft_revision": draft.get("draft_revision"),
                                                   "last_saved_at": draft.get("last_saved_at")}}
            if p.get("confirmed") is not True:
                return 400, {"ok": False, "err": "tick 'I confirm these are my answers' to submit"}
            request_id = str(p.get("request_id") or "")
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{7,63}", request_id):
                return 400, {"ok": False, "err": "a submission needs a request id"}
            receipt = store.submit_feedback(lane, report_id, revision, actor, request_id, answers, True,
                                            "local_attestation")
            return 200, {"ok": True, "receipt": receipt}
        except store.StaleRevision as e:
            return 409, {"ok": False, "err": str(e) or "the report changed, or another tab saved first"}
        except store.DuplicateRequest as e:
            return 409, {"ok": False, "err": str(e) or "this request id was already used for other answers"}
        except store.ValidationError as e:
            return 422, {"ok": False, "err": str(e)}
        except store.MeaningError as e:
            return 404, {"ok": False, "err": str(e)}

    def labeling_act(self, p):
        """The only write door: every action re-checks authority in the engine.

        ``human_id`` and ``attest`` are caller assertions, not authenticated
        identity evidence. The UI requires an explicit confirmation gesture;
        deployments that need identity assurance must add an authenticated
        principal provider before treating this receipt as verified.
        """
        if p.get("action") in self.DECISION_ACTIONS:     # a building Task's decision report, not a labeling Page
            return self.labeling_decision_act(p)
        origin = self.headers.get("Origin") or ""
        host = self.headers.get("Host") or ""
        standalone = p.get("mode") == "page"
        if p.get("mode") not in (None, "board", "page"):
            return 400, {"ok": False, "err": "unknown Labeling workbench mode"}
        if (standalone or p.get("action") == "confirm_meaning") and not origin:
            needed = "Workbench origin" if standalone else "Board origin"
            return 403, {"ok": False, "err": f"labeling write requires the {needed}"}
        if origin and urlparse(origin).netloc != host:
            return 403, {"ok": False, "err": "cross-origin labeling write refused"}
        got = (self._labeling_page_target(p.get("file")) if standalone else self.target(p))
        if got[0] is None:
            return 400, {"ok": False, "err": got[1]}
        page_src, board_dir = got
        if not is_labeling_surface_page(page_src):
            return 404, {"ok": False, "err": "Page has no labeling lane"}
        if not standalone and not generated_page_url(p.get("path") or "", p.get("file") or "",
                                                    p.get("page") or "", board_dir):
            return 400, {"ok": False, "err": "missing or mismatched generated Page URL"}
        if p.get("attest") is not True:
            return 400, {"ok": False, "err": "labeling writes need an explicit caller attestation"}
        root, _ = _labeling_lane(page_src)
        if not (root / "gates" / "p0-contract" / "receipt.json").is_file():
            return 409, {"ok": False, "err": "this Page has no canonical labeling job"}
        cal = _calibration_module()
        jobmod = _canonical_job_module()
        if cal is None or jobmod is None:
            return 500, {"ok": False, "err": "subjective-label engine unavailable"}
        human = str(p.get("human_id") or "")
        session = re.sub(r"[^A-Za-z0-9_-]", "", str(p.get("session_id") or ""))[:40] or "browser"
        action = p.get("action")
        channel = "labeling workbench screen" if standalone else "board labeling screen"
        try:
            if action == "confirm_meaning":
                page_file = root.parent / page_src.name
                result = jobmod.confirm_meaning(
                    job_root=root, page_file=page_file, human_id=human,
                    confirmed_at=cal.now_iso(), accept_current_schema=True,
                    attest_as_human=p.get("attest") is True,
                    channel=channel)
            elif action == "release_round":
                result = cal.release_round(root, human_id=human, n=int(p.get("n") or 0) or None,
                                           channel=channel)
            elif action == "open_item":
                result = cal.open_item(root, str(p.get("round_id") or ""), human_id=human,
                                       session_id=session)
            elif action == "first":
                result = cal.record_first(
                    root, str(p.get("round_id") or ""), str(p.get("item_id") or ""),
                    human_id=human, session_id=session, class_label=p.get("class_label"),
                    region=p.get("region") or None, uncertainty=p.get("uncertainty"),
                    reason=str(p.get("reason") or ""))
            elif action == "final":
                result = cal.record_final(
                    root, str(p.get("round_id") or ""), str(p.get("item_id") or ""),
                    human_id=human, session_id=session, class_label=p.get("class_label"),
                    region=p.get("region") or None, uncertainty=p.get("uncertainty"),
                    change_type=str(p.get("change_type") or "none"),
                    reason=str(p.get("reason") or ""))
            elif action in {"build_embedding", "embedding_status", "embedding_item", "group_examples",
                            "embedding_item_text"}:
                embmod = _embedding_module()
                if embmod is None:
                    return 500, {"ok": False, "err": "subjective-label embedding engine unavailable"}
                if action == "embedding_item":
                    result = embmod.neighbors(root, str(p.get("version") or ""), str(p.get("item_id") or ""),
                                              k=int(p.get("k") or 6))
                elif action == "group_examples":
                    result = embmod.group_examples(root, str(p.get("version") or ""), int(p.get("group_index")),
                                                   k=int(p.get("k") or 3), offset=int(p.get("offset") or 0),
                                                   human_id=human, channel=channel)
                elif action == "embedding_item_text":
                    result = embmod.item_text(root, str(p.get("version") or ""), str(p.get("item_id") or ""),
                                              human_id=human, channel=channel)
                elif action == "build_embedding":
                    groups = p.get("groups")
                    proc, version = embmod.start_background_build(
                        root, str(p.get("model") or ""), channel=channel, started_by=human,
                        input_mode=str(p.get("input_mode") or "reply_context"),
                        instruction=p.get("instruction") or None,
                        groups=int(groups) if groups not in (None, "") else None,
                        map_method=str(p.get("map_method") or "tsne"), seed=int(p.get("seed") or 0))
                    _reap_when_done(proc)
                    result = {"version": version, "model": p.get("model")}
                else:
                    result = {"models": [{k: r.get(k) for k in ("id", "version", "state", "run", "failure", "log_tail")}
                                         for r in embmod.build_status(root)]}
            elif action == "item_page":
                viewmod = _corpus_view_module()
                if viewmod is None:
                    return 500, {"ok": False, "err": "subjective-label corpus reader unavailable"}
                result = viewmod.item_page(root, offset=int(p.get("offset") or 0), k=int(p.get("k") or 20),
                                           human_id=human, channel=channel)
            else:
                return 400, {"ok": False, "err": f"unknown labeling action: {action!r}"}
        except cal.LabelingRefused as error:
            return 409, {"ok": False, "err": str(error)}
        except RuntimeError as error:
            return 409, {"ok": False, "err": str(error)}
        except (ValueError, TypeError) as error:
            return 400, {"ok": False, "err": f"{type(error).__name__}: {error}"}
        return 200, {"ok": True, "result": result}

"""POST routes of the workbench server: the Handler's do_POST, split out of serve.py.

serve.Handler mixes PostMixin in; every route still answers at the same address.
"""
import json
import urllib.parse
from urllib.parse import unquote

from live import chat as live_chat
from live.base import ASKS, HOLD, RUNS, TERMS
from live.chat import group_folder
from live.structure import structure_op
from live.term import kill_all_terms
from serve_routes import new_route_name


class PostMixin:
    def do_POST(self):
        self.path = new_route_name(self.path, "POST")
        if not self.require_request_auth():
            return
        if self.reject_disabled_terminal():
            return
        if self.reject_outside_only():
            return
        # every POST from another site is refused, before any route reads its body (toolkit review 261031: a
        # text/plain form on any web page reached excalidraw-save, chat, structure, cowork, design and insight
        # writes; a browser always sends Origin on a cross-site POST, and "null" from a sandbox or file page)
        origin = self.headers.get("Origin")
        if origin is not None and urllib.parse.urlparse(origin).netloc != (self.headers.get("Host") or ""):
            return self.reply(403, {"ok": False, "err": "cross-origin write refused"})
        if self.path.startswith("/_term/"):
            if self._term_route():
                return
            return self.proxy_term()
        if self.is_api_request():                # a normalizer API call from its try page, behind this login
            return self.proxy_api()
        if not self.path.startswith("/_board/"):
            return self.send_error(404)
        try:
            n = int(self.headers.get("Content-Length") or 0)
            p = json.loads(self.rfile.read(n) or b"{}")
        except Exception as e:
            return self.reply(400, {"ok": False, "err": f"请求体不是 JSON：{e}"})
        if self.path.split("?", 1)[0] in {
            "/_board/comment", "/_board/edit-sentence", "/_board/resolve",
            "/_board/discuss", "/_board/sentence", "/_board/card",
        }:
            return self.reply(405, {
                "ok": False,
                "err": "Page is read-only. Copy a prompt to request a change.",
            })
        if self.path == "/_board/activity":
            try:
                res, err = self.activity(p)
            except Exception as e:
                return self.reply(500, {"ok": False, "err": f"{type(e).__name__}: {e}"})
            if err:
                return self.reply(400, {"ok": False, "err": err})
            return self.reply(200, res)
        if self.path == "/_board/answer":
            # 批准/拒绝一次工具调用 —— 不指向任何文件，所以在 target() 之前处理
            a = ASKS.get(str(p.get("id")))
            if not a:
                return self.reply(404, {"ok": False, "err": "这个请求已经过期了"})
            a["ok"] = bool(p.get("ok"))
            a["always"] = bool(p.get("always"))
            a["ev"].set()
            return self.reply(200, {"ok": True})
        if self.path == "/_board/autodraw":
            # ✨ the Draw tab's button: Claude authors this page's scene
            # (JL 260815). Targets a .excalidraw, so it never reaches target().
            # Threading server, so the minutes it thinks block nobody.
            try:
                from live.autodraw import autodraw
                res = autodraw(self.root, p)
            except Exception as e:
                return self.reply(500, {"ok": False, "err": f"{type(e).__name__}: {e}"})
            return self.reply(200 if res.get("ok") else 400, res)
        if self.path == "/_board/autodeck":
            # ✨ the Slides surfaces' button: Claude authors this page's deck
            # (JL 260815: the deck is the AI deck, and a button regenerates it).
            # Targets slide/<page>-deck.html, so it never reaches target().
            # Threading server, so the minutes it thinks block nobody.
            try:
                from live.autodeck import autodeck
                res = autodeck(self.root, p)
            except Exception as e:
                return self.reply(500, {"ok": False, "err": f"{type(e).__name__}: {e}"})
            return self.reply(200 if res.get("ok") else 400, res)
        if self.path == "/_board/excalidraw-save":
            # Targets a .excalidraw file, not a Q file, so it never reaches
            # target(). Also the one endpoint sendBeacon posts, on unload.
            try:
                res = self.save_excalidraw(p)
            except Exception as e:
                return self.reply(500, {"ok": False, "err": f"{type(e).__name__}: {e}"})
            status = 200 if res.get("ok") else (409 if res.get("conflict") else 400)
            return self.reply(status, res)
        if self.path == "/_board/studio-group":
            # A Studio group is a tag on each topic's **Tags:** line (b10 s02-D16): add a topic to
            # a group, take it out, or delete the group. Targets a Block's Studio, not a Page file.
            from live.frame import studio_group_op
            try:
                res, err = studio_group_op(self.root, p)
            except Exception as e:
                return self.reply(500, {"ok": False, "err": f"{type(e).__name__}: {e}"})
            return self.reply(200 if not err else 400, {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/terms":       # 列出所有在跑的终端（跨板）
            return self.reply(200, {"ok": True, "terms": self.list_terms()})
        if self.path == "/_board/killall":     # 一键全关
            n = len(TERMS)
            kill_all_terms()
            if live_chat.HOST is not None:      # held chat clients go too (QD1)
                live_chat.HOST.close_all()
            HOLD.clear()
            return self.reply(200, {"ok": True, "closed": n})
        if self.path == "/_board/structure":
            # Targets the BOARD, not one Q file, so it resolves the folder itself
            # instead of going through target() (which insists on a Q*.md name).
            page = unquote(p.get("path") or "")
            board = (self.root / page.lstrip("/")).resolve().parent
            try:
                board.relative_to(self.root.resolve())
            except ValueError:
                return self.reply(400, {"ok": False, "err": "越出了 --root"})
            if not (board / "board.md").exists():
                return self.reply(400, {"ok": False, "err": f"{board} 里没有 board.md"})
            try:
                res, err = structure_op(board, p)
            except Exception as e:
                return self.reply(500, {"ok": False, "err": f"{type(e).__name__}: {e}"})
            if err:
                return self.reply(400, {"ok": False, "err": err})
            return self.reply(200, {"ok": True, "build": self.rebuild(board),
                                    **(res or {})})
        # 🎨 Board-level Design routes take {path} only (no Page file), so they
        # are answered before the Page-target check below.
        if self.path == "/_board/design-board":      # the live URL, for the workbench menu
            res, err = self.plug_design_board(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/work-board":
            res, err = self.plug_task_board(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/design-board-act":  # add design tasks · open a Design Folder for a line
            res, err = self.design_board_act(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/draft-card":
            # a person's Accept, Reject or edited Expected on one Revise card of a draft Task (b32 s41-D32)
            from urllib.parse import urlparse
            origin = self.headers.get("Origin") or ""
            if origin and urlparse(origin).netloc != (self.headers.get("Host") or ""):
                return self.reply(403, {"ok": False, "err": "cross-origin write refused"})
            from live.draft_steps import card_act
            code, res = card_act(self.root, p, read_only=getattr(self.server, "read_only", False))
            return self.reply(code, res)
        if self.path == "/_board/item-card":
            # a person's comment, check or edit-card answer on any item of a page, written to that page's
            # records/<stem>-*.md (workbench/ref/cards.md); a draft Task's sentences go through note_act, as below
            from urllib.parse import urlparse
            origin = self.headers.get("Origin") or ""
            if origin and urlparse(origin).netloc != (self.headers.get("Host") or ""):
                return self.reply(403, {"ok": False, "err": "cross-origin write refused"})
            from live.item_card_route import item_card_act
            code, res = item_card_act(self.root, p, read_only=getattr(self.server, "read_only", False))
            return self.reply(code, res)
        if self.path == "/_board/draft-comment":
            # a person's comment on a sentence of a draft Task, left in 5 · Revise and answered by its passes (JL 261021)
            from urllib.parse import urlparse
            origin = self.headers.get("Origin") or ""
            if origin and urlparse(origin).netloc != (self.headers.get("Host") or ""):
                return self.reply(403, {"ok": False, "err": "cross-origin write refused"})
            from live.draft_steps import note_act
            code, res = note_act(self.root, p, read_only=getattr(self.server, "read_only", False))
            return self.reply(code, res)
        if self.path == "/_board/draft-rule":
            # a rule added on a draft Task's 4 · Writing Rubric, into its tab's file (JL 261113)
            from urllib.parse import urlparse
            origin = self.headers.get("Origin") or ""
            if origin and urlparse(origin).netloc != (self.headers.get("Host") or ""):
                return self.reply(403, {"ok": False, "err": "cross-origin write refused"})
            from live.draft_rubric import rule_act
            code, res = rule_act(self.root, p, read_only=getattr(self.server, "read_only", False))
            return self.reply(code, res)
        if self.path == "/_board/draft-plan":
            # a person's change on a draft Task's §1 mind map: a point's words or role, a paragraph's name, a point
            # added, taken out or moved (JL 261020: "how could I operate and edit it?")
            from urllib.parse import urlparse
            origin = self.headers.get("Origin") or ""
            if origin and urlparse(origin).netloc != (self.headers.get("Host") or ""):
                return self.reply(403, {"ok": False, "err": "cross-origin write refused"})
            from live.draft_steps import plan_act
            code, res = plan_act(self.root, p, read_only=getattr(self.server, "read_only", False))
            return self.reply(code, res)
        if self.path == "/_board/mindmap":
            # a person's change on a Studio topic's structured side (its mNN mind map, drawn as the draft's §1 map):
            # a node's words, a node added, taken out or moved, written into its .mindmap.md (hai-studio)
            from urllib.parse import urlparse
            origin = self.headers.get("Origin") or ""
            if origin and urlparse(origin).netloc != (self.headers.get("Host") or ""):
                return self.reply(403, {"ok": False, "err": "cross-origin write refused"})
            from live.frame import mindmap_module
            code, res = mindmap_module().act(self.root, p, read_only=getattr(self.server, "read_only", False))
            return self.reply(code, res)
        if self.path in ("/_board/insight-act", "/_board/design-ladder-act"):
            # a person's own action on an insight or design screen (b11 s12, b12 s12; JL 261023: "design the work in a
            # way that we human can operate this system as well"): a CHECK, a Job's close, a release approved. A sign
            # comes only from a page of this host, never from a request with no page behind it.
            from urllib.parse import urlparse
            origin = self.headers.get("Origin") or ""
            if not origin or urlparse(origin).netloc != (self.headers.get("Host") or ""):
                return self.reply(403, {"ok": False, "err": "a person's action comes from this workbench's page"})
            if self.path == "/_board/insight-act":
                from live.insight_act import act
            else:
                from live.design_ladder_act import act
            code, res = act(self.root, p, read_only=getattr(self.server, "read_only", False))
            return self.reply(code, res)
        if self.path == "/_board/labeling/items":
            # an items Task's Sign or Agree on a planned Run's card (b15 s41-D10)
            code, res = self.labeling_items_act(p)
            return self.reply(code, res)
        if self.path == "/_board/labeling/notes":
            # an image pasted into a prompt's notes, kept in the Task's notes/ (b15 s41-D14)
            code, res = self.labeling_notes(p)
            return self.reply(code, res)
        if self.path == "/_board/labeling/approve":
            # your sign on a meaning Task's guideline mNN (b15 s58-D15): expression runs only on a signed meaning
            code, res = self.labeling_approve(p)
            return self.reply(code, res)
        if self.path == "/_board/labeling/act":
            # The Labeling door resolves Board-backed and standalone Page targets itself.
            code, res = self.labeling_act(p)
            return self.reply(code, res)
        if isinstance(p.get("group"), str) and p["group"]:
            # A group-level session names its group in text; any other "group"
            # value belongs to the route (it once crashed the labeling door).
            # 组级会话（JL 260731）：身份是组的文件夹，不是哪个页面文件。
            # chat/term/sessions/session-name/release/stop 都吃这个 f。
            page = unquote(p.get("path") or "")
            board = (self.root / page.lstrip("/")).resolve().parent
            try:
                board.relative_to(self.root.resolve())
            except ValueError:
                return self.reply(400, {"ok": False, "err": "越出了 --root"})
            f = group_folder(board, p["group"])
            if f is None:
                return self.reply(400, {"ok": False,
                                        "err": f"这块板里找不到组 {p['group']!r} 的文件夹"})
        else:
            f, board = self.target(p)
        if f is None:
            return self.reply(400, {"ok": False, "err": board})
        if self.path == "/_board/image":
            # 存图不写 .md，也就不重建 —— 随后的 discuss/comment 写盘时才重建。
            try:
                res, err = self.save_image(board, p)
            except Exception as e:
                return self.reply(500, {"ok": False, "err": f"{type(e).__name__}: {e}"})
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        # The DERIVED paper-facing workbenches (workbench roster):
        # each writes into the page's own workbench folder and answers with the
        # URL the right-pane tab frames. One route per workbench, one mixin.
        if self.path == "/_board/latex":      # page -> latex/<stem>.tex + .pdf
            res, err = self.export_latex(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/word":       # page -> word/<stem>.docx + PDF twin
            res, err = self.export_word(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/bibex":      # refresh the page-owned bib + view
            res, err = self.export_bibex(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/bibex-verify":   # the human ✓: one verified field
            res, err = self.bibex_verify(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/bibex-entry":    # the pen: land a person's entry
            res, err = self.bibex_entry(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        # The 🛠 skill map workbench (/_board/skill, skill-order, skill-entry,
        # skillview, mdview) was retired on 2026-09-21; the outline/skill/ lane
        # stays an authored store with no served surface.
        # Meeting records moved above Page scope on 260904. Existing
        # <page>/meeting/ bytes remain readable through Folder/static paths,
        # but the Board server must not mint or present new Page-local records.
        if self.path in {"/_board/meeting", "/_board/meeting-entry"}:
            return self.reply(410, {
                "ok": False,
                "err": "Page-local meetings are retired; use "
                       "hai-project-meeting at project or SPACE level",
            })
        # The EVIDENCE workbenches' read-only surfaces (QPf5 · QPf9): the view
        # lists the page's units or cards and writes nothing but itself.
        if self.path == "/_board/folderstat":  # 📂 the tab spec's write() twin
            res, err = self.plug_folderstat(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path in ("/_board/draft", "/_board/outline"):  # 🧭 the same live twin (QPf12)
            res, err = self.plug_outline(p)
            if not err and (res or {}).get("version") and p.get("action") != "edit-preview":
                # A Bullet write changed the Markdown Shape: rebuild so the
                # Page's compact Outline table shows the working version too.
                res["build"] = self.rebuild(board)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/design":     # 🎨 read-only Design Folder surface
            res, err = self.plug_design(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/design-act":  # 🎨 the two human gates + the agent queue
            res, err = self.design_act(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/insight-board":  # 🔎 read-only InsightBoard surface
            res, err = self.plug_insight_board(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/insight":       # 🔎 page-level Insight surface
            res, err = self.plug_insight_page(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/value":       # 🔢 the same live twin (QPw4v)
            res, err = self.plug_value(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/delivery":    # 📤 the same live twin (JL 260831)
            res, err = self.plug_delivery(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/evidence":    # 🧾 the same live twin (JL 260831)
            res, err = self.plug_evidence(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/labeling-board":  # 🏷 Board-level tab contract + probe
            res, err = self.plug_labeling_board(p)
            return self.reply(200 if not err else 400, {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/labeling":    # 🏷 four Spaces over one labeling/ lane
            res, err = self.plug_labeling(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/runs":        # ⚙️ read-only Run overview
            res, err = self.plug_runs(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/display":    # list display/ units + previews
            res, err = self.plug_display(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/probe":      # list probe/ cards + states
            res, err = self.plug_probe(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/term-type":   # a surface types one line into the PTY
            res, err = self.term_type(f, p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/local-cmd":    # the command that lands in this session
            res, err = self.local_cmd(f, p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/term-probe":   # is this target's PTY still alive?
            res, err = self.term_probe(f)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/term":
            res, err = self.terminal(f, p, board)
            return self.reply(200 if not err else 409,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/sessions":    # 拣选器：这一题的会话清单（QD1 Law 260731）
            res, err = self.sessions_list(f, p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/chat-keep":      # sessions land in studio/chat/ (QPf4, JL 260815)
            return self.reply(200, self.keep_sessions(f, p))
        if self.path == "/_board/session-log":    # that session's transcript (JL 260801)
            res, err = self.session_log(f, p), None
            return self.reply(200, res)
        if self.path == "/_board/session-name":   # 给 session 起名/改名（QD1 260731）
            res, err = self.name_session(f, p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/release":
            # park:true（页面 reload 的 beacon、⌨ 切回抽屉）→ 宽限停靠，进程活着；
            # 不带 park（killall、测试、显式关）→ 老样子直接杀。
            if p.get("park"):
                res, _ = self.park(f)
            else:
                res, _ = self.kill_term(f)
            return self.reply(200, {"ok": True, **(res or {})})
        if self.path == "/_board/stop":
            ev = RUNS.get(str(f))
            if ev:
                ev.set()
            return self.reply(200, {"ok": True, "stopping": bool(ev)})
        if self.path == "/_board/attach":   # QD2 R1: rejoin a turn already running
            res, err = self.attach(f, p)
            if res == "STREAMED":
                return                      # attach wrote its own NDJSON response
            return self.reply(200, {"ok": not err, "err": err, **(res or {})})
        ACTS = {"/_board/diagram": self.add_diagram,
                "/_board/excalidraw": self.new_excalidraw,
                "/_board/chat": None}
        if self.path not in ACTS:
            return self.reply(404, {"ok": False, "err": "没有这个接口"})
        try:
            res, err = (self.chat(f, p, board) if self.path == "/_board/chat"
                        else ACTS[self.path](f, p))
        except Exception as e:
            return self.reply(500, {"ok": False, "err": f"{type(e).__name__}: {e}"})
        if err:
            return self.reply(400, {"ok": False, "err": err})
        if res == "STREAMED":
            return                      # 流式那条路已经自己把响应写完了
        body = {"ok": True, "file": f.name, "build": self.rebuild(board)}
        if isinstance(res, dict):
            body.update(res)
        return self.reply(200, body)

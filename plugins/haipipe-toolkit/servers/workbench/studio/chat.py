"""QC8 · the Claude Code bridge (QD2): rules, prime context, the SDK turn.

Moved out of serve.py on 2026-07-31 under the gate_live.py response-identical gate.
QC3's Law: a refactor moves code, features never ride along.

This file keeps the SDK turn (ChatMixin.chat) and the held-client globals (HOST,
HOLD_CHAT, TURN_GATE, host()). The rest lives beside it and is re-exported here:
chat_permissions, chat_context, chat_rules, chat_transcript, chat_host, chat_sessions.
"""

import json
import os
import threading
import time
from pathlib import Path

from . import turnring
from .base import ALWAYS, ASKS, ASK_SEQ, RUNS

# Moved to sibling modules (2026-11-13); re-exported so `from live.chat import X` keeps working.
from .chat_permissions import (READONLY, QUALITY_READONLY, chat_scope,  # noqa: F401
                               quality_tool_allowed, chat_guard, WRITE_TOOLS)
from .chat_context import (_space_entries, operating_context,  # noqa: F401
                           board_prime_context, status_strip_context, group_folder,
                           drawing_owner_context, group_prime_context, prime_context,
                           page_folder_context, _scratch_records, _scratch_context,
                           _scratch_context_fingerprint)
from .chat_transcript import (tool_brief, TOOL_CAP, tool_input_preview,  # noqa: F401
                              tool_output_preview, transcript_markdown, digest_markdown,
                              kept_session_dir)
from .chat_rules import (MODELS, DEFAULT_MODEL, DEFAULT_EFFORT, EFFORTS,  # noqa: F401
                         PAGE_RULES_BODY, CHAT_RULES, FULL_RULES, BOARD_RULES_BODY,
                         BOARD_CHAT_RULES, BOARD_FULL_RULES)
from .chat_host import oauth_token, _Live, SessionHost  # noqa: F401
from .chat_sessions import ChatSessionsMixin


TURN_GATE = {}         # question path -> the live turn's can_use_tool closure
HOST = None            # built on first use; --no-hold leaves it None (QD3m §8's
                       # --ttyd pattern: the old path stays reachable until JL
                       # has clicked through the new one)
HOLD_CHAT = os.environ.get("HAIBOARD_NO_HOLD", "") == ""


def host():
    global HOST
    if HOST is None:
        HOST = SessionHost()
    return HOST


class ChatMixin(ChatSessionsMixin):
    def chat(self, f, p, board):  # noqa: C901
        """Run ONE turn of claude_agent_sdk against this question file.

        Cost control (the smoke test cost $0.92 with defaults): cwd is the board
        folder, not the repo, and setting_sources is empty — so the project's
        CLAUDE.md and the whole skill registry are NOT loaded. The model gets
        CHAT_RULES plus this one file's name, and nothing else.
        """
        msg = (p.get("message") or "").strip()
        if not msg:
            return None, "消息是空的"
        try:
            import anyio
            from claude_agent_sdk import (ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage,
                                          TextBlock, ResultMessage, StreamEvent, UserMessage,
                                          PermissionResultAllow, PermissionResultDeny)
        except ImportError:
            return None, ("这个 Python 没装 claude_agent_sdk（要 3.10+）。"
                          "用仓库的 .venv/bin/python 跑 serve.py；"
                          "装的话：uv pip install --python .venv/bin/python claude-agent-sdk")

        model = MODELS.get(p.get("model") or DEFAULT_MODEL) or MODELS[DEFAULT_MODEL]
        effort = p.get("effort") if p.get("effort") in EFFORTS else DEFAULT_EFFORT
        # 权限档（JL 260723）：三档，默认「完整·问我」＝ 跟 CLI 一样。
        #   scoped  只这一题的文件 · 不加载技能 · 便宜（$0.24）
        #   full    全工具 + 全技能 · 逐个问你（CLI 默认行为）· 贵（~$0.9）
        #   bypass  全工具 + 全技能 · 什么都不问（= --dangerously-skip-permissions）
        quality_check = bool(p.get("quality_check"))
        mode = chat_scope(p)
        guarded, guarded_mode, labeling_hold_reason = chat_guard(f, p)
        if guarded:
            quality_check = True
            mode = guarded_mode
        labeling_hold = bool(labeling_hold_reason)
        # 整板会话（QD5）：f 是 board.md 而不是某一题。规则、开场定位、
        # 「自动放行哪些写」三处跟着换；session 照旧记在 f（= board.md）头部。
        is_board = f.name == "board.md"
        # 组级会话（JL 260731）：f 是组的文件夹。权限面 = 这个文件夹里的 .md；
        # 规则复用整板那份措辞，但把「板」缩成「组」；session 记在登记表（目录无头部）。
        is_group = Path(f).is_dir()
        tok, src = oauth_token(self.root)
        env = {"CLAUDE_CODE_OAUTH_TOKEN": tok} if tok else {}
        prior = self.session_of(f)
        # 拣选器（QD1 Law 260731）：浏览器可以点名要哪一段历史，或者要求全新的一段。
        #   session:"new"     → 不 resume，跑完把新 id 写回头部（成为 current）
        #   session:"<uuid>"  → resume 选中的那段（落过盘才算数），跑完它成为 current
        #   不带 session      → 老样子，接头部里的 current
        want = (p.get("session") or "").strip()
        if want == "new":
            prior = None
        elif want:
            prior = want
        # 同终端那条：只有磁盘上真有这段对话才 resume。头部记了 id 但从没聊过（jsonl 不存在）
        # 的空壳，resume 会失败；这时当没有，起个全新的，结束时把新 id 写回头部覆盖掉空壳。
        if prior and not self.session_landed(prior):
            prior = None
        out, sid, usd, ctx = [], None, None, None
        # HOLD stops the drawer and the terminal fighting over one session, but
        # two drawer turns on the same question passed it, and with a HELD client
        # the second one silently queued behind the first forever (found by
        # driving the real page: 70s on "Thinking" for a one-word reply).
        if str(f) in RUNS:
            return None, "这一题已经有一轮在跑了，等它结束或按 ⏹ 停掉。"
        err = self.hold(f, "drawer")
        if err:
            return None, err
        stop = threading.Event()
        RUNS[str(f)] = stop
        stream = bool(p.get("stream"))
        # R1: the turn's events go to a RING, not to this socket.
        #
        # 260801 had already stopped a departed reader from KILLING the turn, so
        # the work survived; what did not survive was any way to SEE it, because
        # the only copy of the turn's trace was the response being written. The
        # ring makes the record outlive every reader: this request is now just
        # the first one to attach, and `/_board/attach` lets the next one pick up
        # at the cursor it left off. Same asymmetry `term.py` never had.
        turn = turnring.start(str(f))

        def emit(obj):
            turn.push(obj)

        def sock_write(obj):
            try:
                self.wfile.write((json.dumps(obj, ensure_ascii=False) + "\n").encode())
                self.wfile.flush()
                return True
            except Exception:
                return False             # this reader is gone; the turn is not

        denied = []
        wrote = []          # 这一轮真的改过盘上文件的写工具名（决定要不要说「已写盘」）
        thought = [False]   # 思考是否已经逐字流过（流过了就别再整块补一遍）

        async def can_use_tool(name, tin, ctx):
            """权限闸门 —— 跟 Claude Code CLI 一个行为：该问就问。

            所有工具调用都必须走这里：写进 `allowed_tools` 的工具会在这个回调之前
            就被自动放行，`permission_mode` 一旦不是 `default` 也一样绕过
            （这两个坑是 haichat-inlab 注释里写明的）。所以两个都不给。

            走到这里之后的规则就跟 CLI 一样了：
              · 只读的直接放行
              · 会动东西的弹给人看，人点「允许 / 总是允许 / 拒绝」
              · 这一题自己的那个文件，默认就放行（本来就是来改它的）
            没人接（非流式、或者 5 分钟没人点）就拒 —— 默认安全那一侧。
            """
            if quality_check and not quality_tool_allowed(name):
                denied.append(tool_brief(name, tin))
                return PermissionResultDeny(
                    message=("Labeling HOLD is read-only: Chat may inspect and discuss, "
                             "but cannot write, run, or cross the human gate."
                             if labeling_hold else
                             "Quality Check is read-only: it may inspect evidence but cannot write or run tools."))
            if name in READONLY:
                return PermissionResultAllow()
            key = str(f)
            if name in ALWAYS.get(key, set()):
                return PermissionResultAllow()
            if name in ("Edit", "Write", "MultiEdit"):
                tgt = tin.get("file_path") or tin.get("path") or ""
                try:
                    rt = Path(tgt).resolve()
                    # 一题的会话：自己的那个文件永远放行。
                    # 整板会话（QD5）：板文件夹里的任何 .md 都算「自己的」——
                    # board.md 和所有 page 都是它的工作面；board.html 不是 .md，自然进不来。
                    if is_group:
                        ok = (rt.suffix == ".md"
                              and rt.is_relative_to(f.resolve()))
                    elif is_board:
                        ok = (rt.suffix == ".md"
                              and rt.is_relative_to(Path(board).resolve()))
                    else:
                        ok = rt == f.resolve()
                    if ok:
                        return PermissionResultAllow()
                except Exception:
                    pass
            # scoped 档：出了自己的工作面，别的写操作一律拒（不弹，直接不给）
            if mode == "scoped" and name not in READONLY:
                denied.append(tool_brief(name, tin))
                return PermissionResultDeny(
                    message=("「受限」档只能改这个组文件夹里的 .md。要动别的，把权限切到「完整」。"
                             if is_group else
                             "「受限」档只能改这块板文件夹里的 .md。要动别的，把权限切到「完整」。"
                             if is_board else
                             f"「受限」档只能改 {f.name}。要动别的，把权限切到「完整」。"))
            # full 档：跟 CLI 一样，弹给你点
            if not stream:
                denied.append(tool_brief(name, tin))
                return PermissionResultDeny(
                    message="这一轮没开流式，没法问你，先拒了。")
            def ask_detail():
                """What the VS Code extension shows before you allow: the actual
                proposed change, not just the tool name (JL 260724, duplicating
                the workbench). Truncated — a gate preview, not a full diff view."""
                cap = 4000
                try:
                    if name == "Edit":
                        return {"file": tin.get("file_path", ""),
                                "old": str(tin.get("old_string", ""))[:cap],
                                "new": str(tin.get("new_string", ""))[:cap]}
                    if name == "Write":
                        tgt = Path(tin.get("file_path", ""))
                        old = (tgt.read_text(encoding="utf-8", errors="replace")[:cap]
                               if tgt.exists() else "")
                        return {"file": str(tgt), "old": old,
                                "new": str(tin.get("content", ""))[:cap]}
                    if name == "MultiEdit":
                        eds = [{"old": str(e.get("old_string", ""))[:800],
                                "new": str(e.get("new_string", ""))[:800]}
                               for e in (tin.get("edits") or [])[:6]]
                        return {"file": tin.get("file_path", ""), "edits": eds,
                                "count": len(tin.get("edits") or [])}
                    if name == "Bash":
                        return {"command": str(tin.get("command", ""))[:1200]}
                except Exception:  # noqa: BLE001 — a broken preview must not block the gate
                    return None
                return None

            rid = str(next(ASK_SEQ))
            ASKS[rid] = {"ev": threading.Event(), "ok": False, "always": False}
            emit({"t": "ask", "id": rid, "tool": name,
                  "brief": tool_brief(name, tin), "detail": ask_detail()})
            await anyio.to_thread.run_sync(lambda: ASKS[rid]["ev"].wait(300))
            a = ASKS.pop(rid, {})
            if a.get("always"):
                ALWAYS.setdefault(key, set()).add(name)
            if a.get("ok"):
                return PermissionResultAllow()
            denied.append(tool_brief(name, tin))
            return PermissionResultDeny(message="你没有批准这一步。")

        async def run():
            nonlocal sid, usd
            # scoped 档要真的关掉「能动机器」的工具。can_use_tool 在
            # permission_mode=default 下对 Bash 这类不一定会被调用（实测 Bash
            # 直接放行了），所以用 disallowed_tools 硬关 —— 这条是 SDK 层的黑名单，
            # 不经过回调，最稳。scoped 只留读 + 改这一题的文件。
            SCOPED_OFF = ["Bash", "BashOutput", "KillShell", "Task",
                          "WebFetch", "WebSearch"]   # Skill stays: it loads text, writes nothing
            if quality_check:
                SCOPED_OFF += ["Edit", "Write", "MultiEdit", "TodoWrite"]
                SCOPED_OFF += ["NotebookEdit"]
            # cwd 是整个 repo（SPACE），不是板文件夹 —— 会话要能读它讨论的代码。
            # 所以给系统提示的是「相对 repo 根的路径」，不再是光文件名。
            try:
                rel = str(f.resolve().relative_to(self.root.resolve()))
            except ValueError:
                rel = f.name
            prime = prime_context(f, board, self.root)
            try:
                brel = str(Path(board).resolve().relative_to(self.root.resolve()))
            except ValueError:
                brel = str(board)
            if mode == "scoped":
                sysp = ((BOARD_CHAT_RULES + f"\n\nThe GROUP folder you may edit .md files in: {rel}\n\n")
                        if is_group else
                        (BOARD_CHAT_RULES + f"\n\nThe board folder you may edit .md files in: {brel}\n\n")
                        if is_board else
                        (CHAT_RULES + f"\n\nThe question file you may edit: {rel}\n\n")) + prime
                sources = ["user", "project", "local"]   # skills loadable in scoped too (Studio Chat lane)
            else:
                sysp = ((BOARD_FULL_RULES + f"\n\nThis session's GROUP folder: {rel}\n\n")
                        if is_group else
                        (BOARD_FULL_RULES + f"\n\nThis session's board folder: {brel}\n\n")
                        if is_board else
                        (FULL_RULES + f"\n\nThis session's question file: {rel}\n\n")) + prime
                sources = ["user", "project", "local"]   # 加载技能 → Skill 工具可用
            if labeling_hold:
                sysp += ("\n\nLABELING HOLD — READ-ONLY CONSULTATION. "
                         + labeling_hold_reason
                         + " You may inspect and discuss. Do not edit any file, run any "
                           "command, create any semantic event, or claim that the frontier advanced.")
            kw = dict(
                cwd=str(self.root),
                system_prompt=sysp,
                setting_sources=sources,
                include_partial_messages=stream,   # 要逐字流式就得开这个
                max_turns=30 if mode != "scoped" else 12,
                env=env,
                resume=prior or None,
                model=model,
                effort=effort,
                # Thinking, in the form the CURRENT models accept. `{"type":
                # "enabled", "budget_tokens": N}` is the pre-4.6 shape and is
                # rejected on Opus 4.7/4.8/5 and Sonnet 5, which is every model
                # this picker offers except Haiku; the stream then carried
                # `stage`, `delta` and `done` and never a single `think`, so the
                # trace box had nothing in it but the busy line and `traceEnd`
                # dropped it as empty (JL 260801: "the display of the UI will be
                # gone", measured: 0 think events over a full turn).
                #
                # `display` is the half that actually shows it. It is
                # `ThinkingDisplay = Literal["summarized", "omitted"]` and the
                # CLI defaults to omitting, so even a correct `adaptive` config
                # streamed no thinking at all: a 2m10s three-tool turn produced
                # `tool`, `tool_result`, `delta`, `done` and zero `think`.
                thinking={"type": "adaptive", "display": "summarized"},
            )
            if mode == "scoped":
                kw["disallowed_tools"] = SCOPED_OFF   # 硬关，不经过 can_use_tool
            if mode == "bypass":
                # 全放行：permission_mode 一旦不是 default，can_use_tool 会被绕过，
                # 所以这里干脆不给回调，让它一路无提示地跑。
                kw["permission_mode"] = "bypassPermissions"
            else:
                # scoped / full：钉死 default + 走 can_use_tool（写 allowed_tools 或
                # 换 permission_mode 都会绕过回调 —— haichat-inlab 注释里的坑）。
                kw["permission_mode"] = "default"
                # A HELD client keeps the callback it was built with (M1), so it
                # cannot close over this request's emit. It calls through a
                # stable shim that reads whichever turn is live right now.
                async def gate(name, tin, gctx):
                    cb = TURN_GATE.get(str(f))
                    if cb is None:
                        return PermissionResultDeny(message="这一题当前没有在跑的对话。")
                    return await cb(name, tin, gctx)
                kw["can_use_tool"] = gate
            opts = ClaudeAgentOptions(**kw)
            # 用 ClaudeSDKClient，不用 query()。
            #
            # 为什么：can_use_tool 的「放不放行」是通过 stdin 那条控制通道回给 CLI 的。
            # query(prompt=<一次性的 async generator>) 在生成器吐完那一条消息之后就把
            # 输入流关了 —— 通道一关，后面模型再问「我能不能 Edit」就没人接得上，
            # CLI 等到超时报 `AbortError: Stream closed`。
            # 读操作往往赶在关闭之前问完，所以表现是「读得了、写就挂」。
            # ClaudeSDKClient 在整轮里把连接一直开着，回调才有地方回。
            # （haichat-inlab 用的也是 ClaudeSDKClient，不是 query。）
            # 等待期的真话（JL 260724「show the real things」）：boot 阶段一个事件都
            # 没有，页面只能挂一句假的「…thinking」。这里把真实阶段发出去。
            if stream:
                emit({"t": "stage",
                      "text": ("booting claude — the full tier loads the whole skill "
                               "registry, the first message is the slow one"
                               if sources else "booting claude (scoped — quick)")})
            async def drive(client, fresh):
              nonlocal sid, usd, ctx
              if stream:
                  emit({"t": "stage", "text": ("session up — sending your message"
                                               if fresh else "session already up")})
              await client.query(msg)
              async for m in client.receive_response():
                  if stop.is_set():
                      out.append("⏹ 已按你的要求停下。")
                      break
                  if isinstance(m, StreamEvent):
                      # 逐字增量。形状照 haichat-inlab 那边读到的：
                      # content_block_delta -> delta.type == "text_delta"
                      ev = getattr(m, "event", None) or {}
                      if ev.get("type") == "content_block_delta":
                          d = ev.get("delta") or {}
                          if d.get("type") == "text_delta" and d.get("text"):
                              emit({"t": "delta", "text": d["text"]})
                          elif d.get("type") == "thinking_delta" and d.get("thinking"):
                              # 思考过程，逐字发；客户端收进一个可折叠块
                              thought[0] = True
                              emit({"t": "think", "text": d["thinking"]})
                  elif isinstance(m, AssistantMessage):
                      for b in m.content:
                          bn = type(b).__name__
                          if bn in ("ThinkingBlock", "RedactedThinkingBlock"):
                              # 兜底：没走逐字流的思考（或整块到达），一次性发过去
                              tx = getattr(b, "thinking", "") or getattr(b, "text", "")
                              if tx and not thought[0]:
                                  emit({"t": "think", "text": tx})
                          elif isinstance(b, TextBlock) and b.text.strip():
                              out.append(b.text)
                              # 开了逐字流的话，这段文字已经一个字一个字发过了
                              if not stream:
                                  emit({"t": "text", "text": b.text})
                          elif type(b).__name__ in ("ToolUseBlock", "ServerToolUseBlock"):
                              nm = getattr(b, "name", "?")
                              if nm in WRITE_TOOLS:
                                  wrote.append(nm)
                              # The workbench shows a card per call: what it is, and
                              # what it was given. We used to send the name alone
                              # and the drawer threw it away on the next event
                              # (JL 260731, comparing the two side by side).
                              emit({"t": "tool", "name": nm,
                                    "id": getattr(b, "id", ""),
                                    "brief": tool_brief(nm, getattr(b, "input", {}) or {}),
                                    "input": tool_input_preview(getattr(b, "input", {}) or {})})
                  elif isinstance(m, UserMessage):
                      # the other half of the card: what the tool answered
                      for b in (m.content if isinstance(m.content, list) else []):
                          if type(b).__name__ in ("ToolResultBlock", "ServerToolResultBlock"):
                              emit({"t": "tool_result",
                                    "id": getattr(b, "tool_use_id", ""),
                                    "is_error": bool(getattr(b, "is_error", False)),
                                    "output": tool_output_preview(getattr(b, "content", None))})
                  elif isinstance(m, ResultMessage):
                      sid = m.session_id
                      usd = getattr(m, "total_cost_usd", None)

              # How much of the window is gone — the meter the CLI shows under
              # /context and the drawer never had (JL 260801: "我怎么看到我现在
              # 这个 context 的 usage，就是用了百分之几"). It is a streaming-mode
              # verb, so it only became reachable the day M1 held the client.
              # Best-effort by design: an SDK too old to have it, or a call that
              # fails, must never cost this turn its answer.
              try:
                  cu = await client.get_context_usage()
                  if isinstance(cu, dict):
                      ctx = {"pct": cu.get("percentage"),
                             "used": cu.get("totalTokens"),
                             "max": cu.get("maxTokens")}
              except Exception:
                  pass

            if not HOLD_CHAT:                     # --no-hold: the pre-M1 path
                async with ClaudeSDKClient(options=opts) as client:
                    await drive(client, True)
                return
            # M1: reuse this question's client when nothing connect-time changed.
            # The system prompt is deliberately out of the fingerprint — it is
            # fixed at connect for a real CLI session too, so ordinary page
            # edits mid-conversation must not silently restart it. Scratch is
            # the explicit exception: it is a user-context input, and saving
            # it must refresh a held Chat without requiring the person to
            # discover that a new session is needed.
            # The fingerprint covers CONNECT-time options only. It must NOT
            # include `prior`: turn one has no session, turn two resumes the id
            # turn one just wrote into the page header, so folding it in made
            # every turn look different and silently reconnected every time
            # (caught by the stage line still saying "booting" on turn two).
            # A held client IS the conversation; only an explicit pick moves it.
            # `quality_check` is CONNECT-time because its disallowed_tools are;
            # include it so a held writable scoped client can never be reused
            # for a read-only Quality Check or Labeling HOLD turn.
            scratch_fp = _scratch_context_fingerprint(f) if not (is_board or is_group) else ""
            fp = (model, effort, mode, is_board, bool(stream), quality_check,
                  scratch_fp)
            key = str(f)

            async def make():
                c = ClaudeSDKClient(options=opts)
                await c.connect()
                return c

            live, fresh = await host().acquire(key, fp, make, want=want)
            TURN_GATE[key] = can_use_tool
            live.lock.acquire()          # visible to reap(): this one is in use
            try:
                await drive(live.client, fresh)
            finally:
                if live.lock.locked():
                    live.lock.release()
                TURN_GATE.pop(key, None)
                live.last = time.time()
                if sid:
                    live.sid = sid            # what this held client now IS

        result = {}

        def runner():
            """The turn, start to finish, on a thread that owns no socket.

            Everything that must happen EXACTLY ONCE lives here rather than in
            the request: writing the session id back, regenerating the html, and
            the closing `done` event. Before R1 all three sat after the request
            had blocked on the future, so a reader who left took the tail with
            them; now the reader leaving is invisible to this function.
            """
            err = None
            try:
                if HOLD_CHAT:
                    # every operation on a held client must happen on the ONE
                    # loop that owns it (the SDK forbids crossing async runtime
                    # contexts)
                    fut = host().submit(run())
                    try:
                        fut.result()
                    finally:
                        # The genuine failure case only: a future that never
                        # finished, where the client's state really is unknown
                        # and the next query would queue behind it forever.
                        if not fut.done():
                            stop.set()
                            fut.cancel()
                            host().evict(str(f))
                else:
                    anyio.run(run)
            except Exception as e:
                err = f"{type(e).__name__}: {e}"
            finally:
                RUNS.pop(str(f), None)
                self.release(f, "drawer")
            build = ""
            try:
                if sid:
                    self.remember_session(f, sid, name=p.get("name"))
                # 只有真改过盘上文件才重新生成 html —— 读一读、聊两句不该触发 rebuild
                build = self.rebuild(board) if wrote else ""
            except Exception as e:
                err = err or f"{type(e).__name__}: {e}"
            done = {"t": "done", "text": "\n\n".join(out).strip(),
                    "session": sid, "usd": usd, "ctx": ctx, "model": model,
                    "scope": mode, "effort": effort, "denied": denied,
                    "stopped": stop.is_set(), "wrote": bool(wrote),
                    "build": build}
            if err:
                done["ok"], done["err"] = False, err
            result.update(done)
            turn.push(done)
            turn.finish()

        if stream:
            self.send_response(200)
            self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Connection", "close")
            self.end_headers()
            # This request stops OWNING the turn and becomes its first READER.
            # It may end at any moment — a navigation, a reload, a phone
            # locking — and the thread below carries on filling the ring.
            threading.Thread(target=runner, daemon=True,
                             name="chat-turn-" + Path(f).name).start()
            turn.drain(0, sock_write)
            return "STREAMED", None
        runner()
        if result.get("ok") is False:
            return None, result.get("err")
        return {"text": result.get("text", ""),
                "session": sid, "usd": usd, "ctx": ctx, "auth": src, "denied": denied, "scope": mode,
                "wrote": bool(wrote), "stopped": stop.is_set(),
                "model": model, "effort": effort}, None

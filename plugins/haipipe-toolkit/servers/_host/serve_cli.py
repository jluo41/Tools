"""Command line of the workbench server: argument parsing, daemon mode and the listen loop.

serve.py calls main(Handler) under `if __name__ == "__main__"`, so `python3 serve.py ...` is unchanged.
"""
import argparse
import atexit
import os
import signal
import sys
import threading
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path

from host_registry import WORKBENCH_ROUTES
from live import base
from live import chat as live_chat
from live.auth import AuthConfigError, host_is_loopback, host_is_private
from live.chat import DEFAULT_EFFORT, DEFAULT_MODEL, MODELS, oauth_token
from live.term import kill_all_terms, reap_stale_terms
import slow_watch
from server_config import configured_domain, domains, load_server_config, server_config_dir


def daemonize(log):
    """双 fork 脱离终端。macOS 没有 setsid，nohup 又常被上游进程组连坐，
    所以自己来 —— 这样服务器不会跟着某个 shell 一起消失。"""
    if os.fork() > 0:
        os._exit(0)
    os.setsid()
    if os.fork() > 0:
        os._exit(0)
    fd = os.open(log, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    os.dup2(fd, 1)
    os.dup2(fd, 2)
    os.close(os.open(os.devnull, os.O_RDONLY))


def main(Handler):
    # 这个进程往往是从某个 Claude Code 会话的 shell 里起的：把「我是子会话」的
    # 标记就地摘掉，SDK 抽屉和 PTY 终端两条 spawn 路都不再继承它 —— 否则板上
    # 开的 claude 会关掉 transcript 落盘（QD3 Lesson，260731）。
    for _k in ("CLAUDE_CODE_CHILD_SESSION", "CLAUDE_CODE_SESSION_ID",
               "CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_PID"):
        os.environ.pop(_k, None)
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--port", type=int, default=None,
                    help="listener port; root .server_config wins when omitted")
    ap.add_argument("--host", default=None,
                    help="绑哪个地址。默认只绑 loopback；给 tailnet 地址（100.x）"
                         "就能从自己别的设备直接打开，不用 VS Code 转发端口；"
                         "root .server_config wins when omitted")
    ap.add_argument("--daemon", metavar="LOGFILE",
                    help="后台跑，输出写进这个文件")
    ap.add_argument("--ttyd", action="store_true",
                    help="终端走 ttyd 旧路（保险丝；默认 serve.py 自己管 PTY）")
    ap.add_argument("--no-hold", action="store_true",
                    help="QD2 M1 fuse: boot a claude per POST like before, "
                         "instead of holding one per question")
    ap.add_argument("--auth-file", metavar="PATH",
                    help="optional username:password file; required for a non-loopback host")
    ap.add_argument("--no-auth", action="store_true",
                    help="disable HTTP Basic Auth; only use on a trusted private network")
    ap.add_argument("--no-terminal", action="store_true",
                    help="disable /_term/ and PTY control endpoints")
    ap.add_argument("--public-read", action="store_true",
                    help="allow anonymous generated Board pages while keeping interactive tools authenticated")
    ap.add_argument("--space-name", default="",
                    help="display name for the SPACE Home (settings.env SPACE_NAME)")
    ap.add_argument("--public-url", default="",
                    help="DOMAIN, the reader-facing origin (also env HAIPIPE_DOMAIN or "
                         "settings.env DOMAIN); links are printed as <DOMAIN>/w/...")
    ap.add_argument("--index-url", default="",
                    help="workbench Index destination; defaults to this SPACE's studio index")
    ap.add_argument("--share", action="store_true",
                    help="share mode (b10 s52): people sign in with an emailed code and open only what "
                         ".server_config/access.yaml grants them; read-only for all but its owners")
    ap.add_argument("--only", default="",
                    help="serve only these workbenches, comma-separated (%s); terminal, "
                         "chat and Board write routes are then 404. `--only labeling` is the "
                         "annotator-only Labeling host (own port and auth; SPACE name Labeling)."
                         % ", ".join(sorted(WORKBENCH_ROUTES)))
    a = ap.parse_args()
    only = frozenset(w.strip() for w in a.only.split(",") if w.strip())
    unknown = sorted(only - set(WORKBENCH_ROUTES))
    if unknown:
        ap.error("--only: unknown workbench %s; choose from %s"
                 % (", ".join(unknown), ", ".join(sorted(WORKBENCH_ROUTES))))
    if only and "shared" not in only:
        a.no_terminal = True      # an --only host is a reader or annotator door, not a shell
    config = load_server_config(a.root)
    config_dir = server_config_dir(a.root)
    # A SPACE whose settings.env says NO_AUTH=1 chose the tailnet as its only
    # gate, so a plain start keeps that choice instead of turning login on from
    # AUTH_FILE. An explicit --auth-file or --public-read still wins.
    if (not a.auth_file and not a.public_read
            and config.get("NO_AUTH", "").lower() in {"1", "true", "yes"}):
        a.no_auth = True
    host = (a.host or config.get("BIND_HOST") or
            config.get("TAILSCALE_ADDRESS") or "127.0.0.1").strip()
    port = a.port
    if port is None:
        raw_port = config.get("PORT")
        try:
            port = int(raw_port) if raw_port else 5599
        except ValueError:
            ap.error(f"invalid port in {config_dir / 'settings.env'}: {raw_port!r}")
    if a.no_auth and a.public_read:
        ap.error("--no-auth and --public-read are mutually exclusive")
    if a.no_auth:
        auth_file = None
    else:
        auth_arg = a.auth_file or config.get("AUTH_FILE")
        if auth_arg:
            auth_path = Path(auth_arg).expanduser()
            if not auth_path.is_absolute() and not a.auth_file:
                auth_path = Path(a.root).resolve() / auth_path
            auth_file = auth_path.resolve()
        else:
            auth_file = None
    space_name = (a.space_name or ("Labeling" if only == {"labeling"} else "")
                  or config.get("SPACE_NAME") or "").strip()
    public_url = configured_domain(a.public_url, config)
    if a.share:                       # the emailed code is the sign-in; no Basic auth beside it
        auth_file, a.no_auth = None, False
        try:
            shared = Handler.configure_share(a.root)
        except (OSError, ValueError) as exc:
            ap.error(f"--share: {exc}")
        print(f"[share] on: {len(shared.owners)} owner(s), {len(shared.grants)} grant(s), mail "
              f"{'from ' + shared.mail_from if shared.acs else 'not set up (owner codes go to this log)'}",
              file=sys.stderr, flush=True)
    # Login is off by default on this machine and on the tailnet: it turns on only
    # when an auth file is named (--auth-file, or AUTH_FILE without NO_AUTH).
    if auth_file is None and not a.share and not a.public_read and host_is_private(host):
        a.no_auth = True
    if not host_is_loopback(host) and auth_file is None and not a.no_auth and not a.share:
        ap.error("--auth-file is required when --host is not loopback")
    if a.public_read and auth_file is None:
        ap.error("--public-read requires --auth-file for interactive Board tools")
    try:
        Handler.configure_auth(auth_file)
    except AuthConfigError as exc:
        ap.error(str(exc))
    # 260731 三次踩同一个坑：用系统 python 起 5599，页面照样 200，可 💬 每一轮
    # 都 400（claude_agent_sdk 要 3.10+）。人记不住的规矩交给代码——当前解释器
    # 没有 SDK 而 --root 下有 .venv 时，原地 exec 换成 venv 的 python 重启自己；
    # venv 也没有 SDK 就不换（防死循环），只警告一声继续跑。
    try:
        import claude_agent_sdk  # noqa: F401
    except ImportError:
        venv_py = Path(a.root).resolve() / ".venv" / "bin" / "python"
        if venv_py.exists() and Path(sys.executable).resolve() != venv_py.resolve():
            os.execv(str(venv_py), [str(venv_py)] + sys.argv)
        print("⚠️  这个 python 没有 claude_agent_sdk —— 💬 chat 会一直 400。"
              "用仓库的 .venv/bin/python 跑 serve.py。", file=sys.stderr)
    base.USE_TTYD = a.ttyd
    live_chat.HOLD_CHAT = not a.no_hold
    if a.daemon:
        daemonize(str(Path(a.daemon).resolve()))
    Handler.root = Path(a.root).resolve()
    Handler.public_read = a.public_read
    Handler.terminal_enabled = not a.no_terminal
    Handler.space_name = space_name
    Handler.public_url = public_url
    Handler.workbench_index_url = a.index_url or config.get("INDEX_URL") or "/?view=radial&measure=studios"
    Handler.only = only
    base.BIND_HOST = host
    srv = ThreadingHTTPServer((host, port),
                              partial(Handler, directory=str(Handler.root)))
    # A non-loopback --host binds THAT ADDRESS ONLY, which quietly breaks the
    # path most people are actually on: a VS Code / ssh -L forward connects to
    # 127.0.0.1 on THIS machine, so a tailnet-only bind leaves the tunnel
    # pointing at a closed port and the board simply will not open (JL 260726,
    # twice in one evening). Loopback is therefore always ALSO served: it adds
    # no exposure that a local process does not already have, and it means
    # choosing a wider address never costs you the narrow one.
    loop = None
    if not host_is_loopback(host) and host != "0.0.0.0":
        try:
            loop = ThreadingHTTPServer(("127.0.0.1", port),
                                       partial(Handler, directory=str(Handler.root)))
            threading.Thread(target=loop.serve_forever, daemon=True).start()
        except OSError as e:
            print(f"   ⚠️ loopback {port} 没起来：{e}", flush=True)
    tok, src = oauth_token(Handler.root)
    try:
        import claude_agent_sdk  # noqa: F401
        sdk = "on"
    except ImportError:
        sdk = "off（这个 Python 没装 SDK，聊天接口不可用）"
    domain_lines = "".join(
        f"   DOMAIN: {origin:<32} ({why})\n" for origin, why in domains(config, host, port, public_url))
    first_domain = (domains(config, host, port, public_url) or [(f"http://{host}:{port}", "")])[0][0]
    print(f"📡 http://{host}:{port}  root={Handler.root}\n"
          + ("" if not loop else
             f"   ＋ http://127.0.0.1:{port} 也在听（VS Code / ssh -L 走的是这个）\n")
          + domain_lines
          + f"   short routes: {first_domain}/b/<board>[/<page>]  ·  {first_domain}/w/<board>[/<page>[/<tab>]]\n"
          + ("" if not only else
             f"   only: {', '.join(sorted(only))} workbench routes; terminal, chat and Board writes are 404\n")
          + ("" if host_is_loopback(host) else
             (f"   ⚠️ 绑的不是 loopback：{host} 能到的设备都能用 /_term/ 开 shell\n"
              if a.no_auth and not a.no_terminal else
              (f"   ℹ️ 绑的不是 loopback：{host} 的终端入口已关闭\n"
               if a.no_auth else
              (f"   ℹ️ {host} 能到的设备可匿名读 Board；/_term/ 和写入仍需认证\n"
               if a.public_read else
               f"   ℹ️ {host} 能到的设备必须先认证\n"))))
          + ("   终端：disabled (--no-terminal)\n" if a.no_terminal else "")
          + f"   评论 / 状态：直接写在这台机器上\n"
          f"   认证：{('off (--no-auth; Tailscale boundary only)' if a.no_auth else ('public Board read; interactive tools protected (' + str(len(Handler.auth_users)) + ' accounts)' if a.public_read else ('on (' + str(len(Handler.auth_users)) + ' accounts)' if Handler.auth_users else 'off (local only)')))}\n"
          f"   聊天：{sdk} · 默认 {MODELS[DEFAULT_MODEL]} / effort={DEFAULT_EFFORT}\n"
          f"   OAuth 来源：{src}"
          + ("（长期 token）" if tok else "（沿用 claude 已登录的身份）")
          + "\n   Ctrl-C 停", flush=True)
    # 启动先清上一轮遗留（主力，不依赖退出信号），退出再尽力收一次
    reap_stale_terms()
    slow_watch.start()                  # a request past 30 s writes every thread's stack to this log
    atexit.register(kill_all_terms)
    signal.signal(signal.SIGTERM, lambda *_: (kill_all_terms(), os._exit(0)))
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        kill_all_terms()

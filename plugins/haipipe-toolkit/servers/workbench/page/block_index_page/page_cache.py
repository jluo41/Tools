"""A focus page built once into a file and served from that file (b17 j11 t01, trace 261126/0020_page_cache).

A build records what the page reads: every file and folder it opens or lists (an audit hook, on the
building thread only), each one's parent folder, and the repository a `git log` reads. The next open
compares their modified times, the loaded workbench code's and today's date with that record, and builds
again only when one of them changed; otherwise it answers with the file, in a few milliseconds.

Built pages are kept under ~/.cache/haipipe/pages/ (PAGE_CACHE_DIR moves it; PAGE_CACHE=0 turns the
cache off). Under pytest the cache is off unless PAGE_CACHE_DIR is set, so a test never reads another's page.
"""
import datetime
import hashlib
import json
import os
import sys
import threading
import time
from pathlib import Path

SERVERS = str(Path(__file__).resolve().parents[3])          # plugins/haipipe-toolkit/servers
_SKIP = tuple({sys.prefix, sys.base_prefix, sys.exec_prefix})
_local = threading.local()
_pruned = []


def _record(event, args):
    reads = getattr(_local, "reads", None)
    if reads is None:
        return
    try:
        if event in ("open", "os.listdir", "os.scandir"):
            path = args[0] if args else None
            if isinstance(path, (str, bytes, os.PathLike)):
                path = os.path.abspath(os.fsdecode(path))
                if path not in reads and not path.endswith(".pyc") and not path.startswith(_SKIP):
                    reads[path] = _stamp(path)           # as it was when read, so a change during the build counts
                    parent = os.path.dirname(path)       # a file made or removed beside it changes the folder
                    reads.setdefault(parent, _stamp(parent))
        elif event == "subprocess.Popen":
            argv = [os.fsdecode(a) for a in (args[1] if isinstance(args[1], (list, tuple)) else [args[1]])]
            git = _git_log_dir(argv)
            if git:
                reads.setdefault(git, _stamp(git))
            else:                                    # any other command's answer has no file to watch
                _local.uncacheable = True
    except Exception:                                # a hook never breaks the page it watches
        _local.uncacheable = True


if not getattr(sys, "_haipipe_page_cache_hook", False):   # one hook per process, however often this reloads
    sys.addaudithook(lambda event, args: sys.modules.get(__name__) and sys.modules[__name__]._record(event, args))
    sys._haipipe_page_cache_hook = True


def _git_log_dir(argv: list) -> str:
    """For `git -C <dir> log ...`, the file a new commit or checkout touches (<gitdir>/logs/HEAD); else ''."""
    if not argv or os.path.basename(argv[0]) != "git" or "log" not in argv:
        return ""
    here = Path(argv[argv.index("-C") + 1] if "-C" in argv else os.getcwd()).resolve()
    for d in (here, *here.parents):
        dot = d / ".git"
        if dot.is_dir():
            return str(dot / "logs" / "HEAD")
        if dot.is_file():                            # a submodule or worktree: its gitdir is named in the file
            line = dot.read_text(errors="ignore").strip()
            if line.startswith("gitdir:"):
                return str((d / line[7:].strip()).resolve() / "logs" / "HEAD")
            return ""
    return ""


def enabled() -> bool:
    if os.environ.get("PAGE_CACHE") == "0":
        return False
    return "pytest" not in sys.modules or bool(os.environ.get("PAGE_CACHE_DIR"))


def folder() -> Path:
    return Path(os.environ.get("PAGE_CACHE_DIR") or Path.home() / ".cache" / "haipipe" / "pages")


def _stamp(path: str):
    try:
        st = os.stat(path)
    except OSError:
        return None
    return [st.st_mtime_ns, st.st_size]


def code_stamp() -> str:
    """The loaded workbench code: each module file under servers/ with its modified time."""
    files = sorted(f for m in list(sys.modules.values())
                   if (f := getattr(m, "__file__", None)) and f.startswith(SERVERS))
    return hashlib.sha1(json.dumps([[f, _stamp(f)] for f in files]).encode()).hexdigest()


def _fresh(record: dict) -> bool:
    if record.get("code") != code_stamp() or record.get("day") != datetime.date.today().isoformat():
        return False
    return all(_stamp(p) == s for p, s in record.get("deps", {}).items())


def _write(path: Path, text: str):
    tmp = path.with_name(f"{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def _prune(where: Path, days: int = 30):
    """Once a process: built pages nobody opened for a month go."""
    if _pruned:
        return
    _pruned.append(True)
    old = time.time() - days * 86400
    for f in where.glob("*"):
        try:
            if f.stat().st_mtime < old:
                f.unlink()
        except OSError:
            pass


def serve(key: tuple, build) -> str:
    """The page for `key` from its file when nothing it read has changed, else `build()`, written down."""
    if not enabled() or getattr(_local, "reads", None) is not None:   # off, or inside another build
        return build()
    where = folder()
    name = hashlib.sha1(json.dumps([str(k) for k in key]).encode()).hexdigest()
    page, meta = where / f"{name}.html", where / f"{name}.json"
    try:
        if _fresh(json.loads(meta.read_text(encoding="utf-8"))):
            text = page.read_text(encoding="utf-8")
            os.utime(meta)                           # opened: kept by _prune
            return text
    except (OSError, ValueError):
        pass
    _local.reads, _local.uncacheable = {}, False
    day = datetime.date.today().isoformat()
    try:
        text = build()
    finally:
        reads, uncacheable = _local.reads, _local.uncacheable
        _local.reads = None
    if uncacheable or not isinstance(text, str):
        return text
    code = code_stamp()                              # after the build: it may import more of the code
    deps = reads
    try:
        where.mkdir(parents=True, exist_ok=True)
        _write(page, text)
        _write(meta, json.dumps({"key": [str(k) for k in key], "day": day, "code": code, "deps": deps}))
        _prune(where)
    except OSError:                                  # a full or read-only disk: the page is still answered
        pass
    return text

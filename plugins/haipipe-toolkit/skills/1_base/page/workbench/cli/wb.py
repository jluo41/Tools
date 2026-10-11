#!/usr/bin/env python3
"""/wb (short for /workbench): open the workbench for the SPACE, a Project, or a Block, Job or Task.

    wb.py                       the SPACE Home: every Project and its Blocks
    wb.py <path>                a Project, a Theme folder (cowork/, papers/, ...), a Block, Job or Task,
                                or any file inside one; SPACE-relative or relative to the current folder
    wb.py <words ...>           find the place by words (folder names, titles, spine/goal/status lines)
                                and open it when one place clearly wins; else list the top five

    --find        list the ranked places only; open nothing
    --no-open     check the link and print it, but do not open the browser
    --json        print one JSON object instead of text
    --root DIR    the SPACE root (default: the nearest folder above holding env.sh or .server_config)
    --no-restart  never restart a server that fails to answer

The link is checked on this SPACE's running server before it is printed: the running
`servers/_host/serve.py --root <SPACE>` with the lowest port is used, one is started when none runs,
and one that fails to answer (connection drop, 5xx) is restarted with its own flags and asked again.
The search reuses the server's own lists (home.discover_boards for Blocks, frame.children and
frame.level_of for Jobs and Tasks, frame.theme_of for the theme), so a found place and the screen
always agree. Words that name a level (block, job, task, project) or a theme (paper, cowork,
discovery, insight, design, labeling) narrow the search instead of being matched.
"""
from __future__ import annotations

import argparse
import errno
import json
import os
import re
import shlex
import signal
import socket
import subprocess
import sys
import time
import webbrowser
from dataclasses import dataclass, field
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import urlopen

SKILLS = next(p for p in Path(__file__).resolve().parents if p.name == "skills")
SERVERS = SKILLS.parent / "servers"
sys.path.insert(0, str(SERVERS / "_host"))
from host_paths import bootstrap  # noqa: E402

bootstrap()
from live import frame  # noqa: E402
from live.home import THEME_KIND, discover_boards  # noqa: E402
from server_config import load_server_config  # noqa: E402

LEVEL_WORDS = {"project": "Project", "projects": "Project", "block": "Block", "blocks": "Block",
               "job": "Job", "jobs": "Job", "task": "Task", "tasks": "Task"}
THEME_WORDS = {"paper": "paper", "papers": "paper", "cowork": "cowork", "discovery": "discovery",
               "discoveries": "discovery", "insight": "insight", "insights": "insight",
               "design": "design", "designs": "design", "labeling": "labeling", "labelings": "labeling"}
STOP = {"the", "a", "an", "of", "for", "my", "me", "to", "in", "on", "and", "about", "with", "open",
        "show", "find", "where", "is", "our", "that", "this", "one", "wb", "workbench", "folder", "page"}
LEVEL_RANK = {"Project": 0, "Theme": 1, "Block": 2, "Job": 3, "Task": 4}


# ── where am I ────────────────────────────────────────────────────────────────────────────────────

def space_root(start: Path) -> Path | None:
    """The SPACE root: the nearest folder at or above `start` holding env.sh or .server_config."""
    for p in (start, *start.parents):
        if (p / "env.sh").is_file() or (p / ".server_config").is_dir():
            return p
    return None


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix() if path != root else ""


def theme_skill(theme: str) -> str:
    """The skill that explains a theme's screen: workbench-<theme>, else the workbench rules."""
    if theme and theme != "vanilla" and any(SKILLS.glob(f"*/*/workbench-{theme}/SKILL.md")):
        return f"workbench-{theme}"
    return "workbench"


def leveled(folder: Path, root: Path) -> tuple[Path, str] | None:
    """The nearest folder at or above `folder` that the frame opens (a Block, Job or Task)."""
    for p in (folder, *folder.parents):
        if p == root or root not in p.parents:
            return None
        level = frame.level_of(p)
        if level:
            return p, level
    return None


def project_above(folder: Path, root: Path) -> Path | None:
    for p in (folder, *folder.parents):
        if p == root or root not in p.parents:
            return None
        if frame.is_project(p):
            return p
    return None


def target(folder: Path, root: Path) -> dict:
    """What a folder opens: Home, a Project's Home view, or the frame over a Block, Job or Task."""
    if folder.is_file():
        folder = folder.parent
    if folder == root:
        return {"level": "SPACE", "path": "", "url": "/", "theme": "", "skill": "workbench"}
    found = leveled(folder, root)
    if found:
        place, level = found
        theme = frame.theme_of(place, root)
        return {"level": level, "path": rel(place, root),
                "url": "/_board/workbench?" + urlencode({"path": rel(place, root)}, safe="/"),
                "theme": theme, "skill": theme_skill(theme)}
    project = project_above(folder, root)
    if project:
        query = {"project": rel(project, root)}
        level, theme = "Project", ""
        if folder.parent == project and folder.name in frame.THEME_FOLDERS:
            level, theme = "Theme", frame.THEME_FOLDERS[folder.name]
            kind = THEME_KIND.get(folder.name)
            if kind:
                query["kind"] = kind
        return {"level": level, "path": rel(folder if level == "Theme" else project, root),
                "url": "/?" + urlencode(query, safe="/,"), "theme": theme,
                "skill": theme_skill(theme) if theme else "workbench"}
    return {"level": "SPACE", "path": "", "url": "/", "theme": "", "skill": "workbench"}


# ── find by words ─────────────────────────────────────────────────────────────────────────────────

def words_of(text: str) -> list[str]:
    """Lower-case words, with CamelCase split (`ScalingGlucose` -> scaling, glucose)."""
    return re.findall(r"[a-z0-9]+", re.sub(r"([a-z])([A-Z])", r"\1 \2", text).lower())


def face_text(folder: Path) -> tuple[str, str]:
    """(title, the face's title plus spine/goal/status lines), or ("", "") without a face."""
    md = frame.face(folder) or (folder / "README.md" if (folder / "README.md").is_file() else None)
    if not md:
        return "", ""
    title = frame._title(md)
    try:
        head = md.read_text(encoding="utf-8", errors="ignore").splitlines()[:30]
    except OSError:
        head = []
    lines = [line for line in head if re.match(r"(spine|goal|status|topic|state):", line)]
    return title, " ".join([title, *lines])


@dataclass
class Place:
    level: str
    path: str
    title: str
    text: str
    theme: str = ""
    score: tuple = field(default=(0, 0))


def places(root: Path) -> list[Place]:
    """Every Project, Theme folder, Block, Job and Task the server knows, with its search text."""
    out, seen_projects, seen_themes = [], set(), set()
    for card in discover_boards(root, include_page_state=False):
        block = root / str(card["path"])
        theme = frame.theme_of(block, root)
        if card.get("project_scope") == "project":
            project = str(card["project_path"])
            if project not in seen_projects:
                seen_projects.add(project)
                title, text = face_text(root / project)
                out.append(Place("Project", project, title or Path(project).name, text))
            folder = block.parent
            if folder.parent == root / project and folder.name in frame.THEME_FOLDERS:
                if folder not in seen_themes:
                    seen_themes.add(folder)
                    out.append(Place("Theme", rel(folder, root), folder.name, "",
                                     frame.THEME_FOLDERS[folder.name]))
        out.append(Place("Block", str(card["path"]), str(card["title"]),
                         " ".join((str(card["title"]), str(card["spine"]), str(card.get("board_state") or ""))),
                         theme))
        for job in frame.children(block, "Block"):
            title, text = face_text(job)
            out.append(Place("Job", rel(job, root), title or job.name, text, theme))
            for task in frame.children(job, "Job"):
                title, text = face_text(task)
                out.append(Place("Task", rel(task, root), title or task.name, text, theme))
    return out


def match(word: str, tokens: set) -> bool:
    """A word matches a token exactly, or both share their first five letters (proposal/proposals)."""
    return word in tokens or (len(word) >= 5 and any(len(t) >= 5 and t[:5] == word[:5] for t in tokens))


def rank(found: list[Place], query: str) -> tuple[list[Place], list[str]]:
    words = [w for w in words_of(query) if w not in STOP and len(w) > 1]
    levels = {LEVEL_WORDS[w] for w in words if w in LEVEL_WORDS}
    themes = {THEME_WORDS[w] for w in words if w in THEME_WORDS}
    words = [w for w in words if w not in LEVEL_WORDS and w not in THEME_WORDS] or words
    pool = [p for p in found if (not levels or p.level in levels) and (not themes or p.theme in themes)]
    pool = pool or found                       # a filter that leaves nothing is dropped, not obeyed
    for p in pool:
        leaf, path, text = set(words_of(Path(p.path).name)), set(words_of(p.path)), set(words_of(p.text))
        hits = weight = 0
        for w in words:
            got = 3 if match(w, leaf) else 2 if match(w, path) else 1 if match(w, text) else 0
            hits += bool(got)
            weight += got
        p.score = (hits, weight)
    ranked = sorted((p for p in pool if p.score[0]),
                    key=lambda p: (-p.score[0], -p.score[1], LEVEL_RANK[p.level], p.path))
    return ranked, words


def clear_winner(ranked: list[Place], words: list[str]) -> bool:
    """One place clearly wins: it matches every word, and nothing outside it scores as high."""
    if not ranked or ranked[0].score[0] < len(words):
        return False
    top = ranked[0]
    return all(p.score < top.score or (p.path + "/").startswith(top.path + "/") for p in ranked[1:])


# ── the server ────────────────────────────────────────────────────────────────────────────────────

@dataclass
class Server:
    pid: int
    port: int
    cwd: Path
    script: str
    args: list
    public: str

    @property
    def local(self) -> str:
        return f"http://127.0.0.1:{self.port}"


def _listening_ports(pid: int) -> list[tuple[str, int]]:
    out = subprocess.run(["lsof", "-a", "-nP", "-p", str(pid), "-iTCP", "-sTCP:LISTEN", "-Fn"],
                         capture_output=True, text=True).stdout
    found = []
    for line in out.splitlines():
        m = re.match(r"n(.+):(\d+)$", line)
        if m:
            found.append((m.group(1).strip("[]"), int(m.group(2))))
    return found


def _cwd(pid: int) -> Path | None:
    out = subprocess.run(["lsof", "-a", "-p", str(pid), "-d", "cwd", "-Fn"],
                         capture_output=True, text=True).stdout
    names = [line[1:] for line in out.splitlines() if line.startswith("n")]
    return Path(names[-1]) if names else None


def servers(root: Path) -> list[Server]:
    """This SPACE's running hosts (`servers/_host/serve.py --root <root>`, not an --only host)."""
    out = subprocess.run(["ps", "-axww", "-o", "pid=,command="], capture_output=True, text=True).stdout
    found = []
    for line in out.splitlines():
        pid, _, command = line.strip().partition(" ")
        if "servers/_host/serve.py" not in command:
            continue
        try:
            argv = shlex.split(command)
        except ValueError:
            continue
        at = next((i for i, a in enumerate(argv) if a.endswith("servers/_host/serve.py")), None)
        if at is None:
            continue
        args = argv[at + 1:]
        opt = lambda name: args[args.index(name) + 1] if name in args[:-1] else ""
        if opt("--only"):
            continue
        cwd = _cwd(int(pid))
        if cwd is None:
            continue
        served = Path(opt("--root") or ".")
        served = (served if served.is_absolute() else cwd / served).resolve()
        if served != root:
            continue
        ports = _listening_ports(int(pid))
        if not ports:
            continue
        port = ports[0][1]
        host = next((h for h, _ in ports if h not in ("127.0.0.1", "::1", "*")), "127.0.0.1")
        public = (opt("--public-url") or f"http://{host}:{port}").rstrip("/")
        found.append(Server(int(pid), port, cwd, argv[at], args, public))
    return sorted(found, key=lambda s: s.port)


def _port_free(port: int) -> bool:
    """Free only when a connection is refused. A frozen server still accepts until its queue is full
    and then lets connections time out, which must read as busy, never as free."""
    with socket.socket() as s:
        s.settimeout(1.0)
        try:
            return s.connect_ex(("127.0.0.1", port)) == errno.ECONNREFUSED
        except OSError:
            return False


def _answers(local: str) -> bool:
    """The host answers HTTP (any status below 500) within a few seconds."""
    try:
        with urlopen(local + "/", timeout=5) as response:
            return response.status < 500
    except HTTPError as error:
        return error.code < 500
    except (URLError, ConnectionError, OSError):
        return False


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def _until(check, seconds: float) -> bool:
    end = time.time() + seconds
    while time.time() < end:
        if check():
            return True
        time.sleep(0.3)
    return False


def _python(root: Path) -> str:
    venv = root / ".venv" / "bin" / "python"
    return str(venv) if venv.exists() else sys.executable


def start(root: Path) -> Server:
    """Start this SPACE's host from its settings (.server_config/settings.env), on a free port."""
    config = load_server_config(root)
    port = int(config.get("PORT") or 5602)
    while not _port_free(port):
        port += 1
    host = config.get("BIND_HOST") or config.get("TAILSCALE_ADDRESS") or "127.0.0.1"
    name = re.sub(r"[^a-z0-9]+", "-", (config.get("SPACE_NAME") or root.name).lower()).strip("-")
    args = ["--root", str(root), "--host", host, "--port", str(port), "--no-terminal",
            "--daemon", f"/tmp/{name}-{port}.log"]
    script = str(SERVERS / "_host" / "serve.py")
    subprocess.Popen([_python(root), script, *args], cwd=root, stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL, start_new_session=True)
    if not _until(lambda: _answers(f"http://127.0.0.1:{port}"), 40):
        raise SystemExit(f"wb: started a server on port {port}, but it did not answer; see /tmp/{name}-{port}.log")
    return servers(root)[0] if servers(root) else Server(0, port, root, script, args, f"http://{host}:{port}")


def restart(server: Server, root: Path) -> Server:
    """Stop a host that fails to answer and start it again with its own flags."""
    for sig in (signal.SIGTERM, signal.SIGCONT):       # SIGCONT: a stopped process handles its TERM
        try:
            os.kill(server.pid, sig)
        except ProcessLookupError:
            break
    if not _until(lambda: not _alive(server.pid), 10):
        try:
            os.kill(server.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        if not _until(lambda: not _alive(server.pid), 5):
            raise SystemExit(f"wb: could not stop the server on port {server.port} (pid {server.pid})")
    _until(lambda: _port_free(server.port), 10)
    script = server.script if Path(server.script).is_absolute() else str(server.cwd / server.script)
    subprocess.Popen([_python(root), script, *server.args], cwd=server.cwd, stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL, start_new_session=True)
    if not _until(lambda: _answers(server.local), 40):
        raise SystemExit(f"wb: restarted the server on port {server.port}, but it did not answer")
    again = [s for s in servers(root) if s.port == server.port]
    return again[0] if again else server


def fetch(url: str) -> tuple[int, str, float]:
    """(status, page title, seconds); status 0 means the server dropped the request."""
    began = time.time()
    try:
        with urlopen(url, timeout=30) as response:
            body = response.read().decode("utf-8", errors="ignore")
            status = response.status
    except HTTPError as error:
        return error.code, "", time.time() - began
    except (URLError, ConnectionError, OSError):
        return 0, "", time.time() - began
    m = re.search(r"<title>([^<]*)", body)
    return status, (m.group(1).strip() if m else ""), time.time() - began


def checked_link(place: dict, root: Path, may_restart: bool) -> dict:
    found = servers(root)
    server = found[0] if found else start(root)
    status, title, took = fetch(server.local + place["url"])
    restarted = False
    if (status == 0 or status >= 500) and may_restart and server.pid:
        server, restarted = restart(server, root), True
        status, title, took = fetch(server.local + place["url"])
    return {**place, "link": server.public + place["url"], "local": server.local + place["url"],
            "status": status, "title": title, "seconds": round(took, 2), "port": server.port,
            "pid": server.pid, "restarted": restarted, "servers": [s.port for s in found]}


# ── main ──────────────────────────────────────────────────────────────────────────────────────────

def resolve_path(arg: str, root: Path) -> Path | None:
    """A path given on the command line, SPACE-relative or from here, inside the SPACE."""
    for base in (Path.cwd(), root):
        candidate = (base / arg).resolve() if not Path(arg).is_absolute() else Path(arg).resolve()
        if candidate.exists() and (candidate == root or root in candidate.parents):
            return candidate
    return None


def by_name(name: str, found: list[Place]) -> list[Place]:
    """Places whose folder name is exactly `name` (b01_irb, Project-Samsung)."""
    return [p for p in found if Path(p.path).name.lower() == name.lower()]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("words", nargs="*")
    ap.add_argument("--root")
    ap.add_argument("--find", action="store_true")
    ap.add_argument("--no-open", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-restart", action="store_true")
    a = ap.parse_args(argv)

    root = Path(a.root).resolve() if a.root else space_root(Path.cwd().resolve())
    if root is None:
        raise SystemExit("wb: no SPACE root above this folder (no env.sh or .server_config); pass --root")
    query = " ".join(a.words).strip()
    result: dict = {"query": query, "root": root.name}

    folder = resolve_path(query, root) if query else root
    ranked: list[Place] = []
    if folder is None:
        found = places(root)
        named = by_name(query, found) if " " not in query else []
        if len(named) == 1:
            folder = root / named[0].path
        else:
            ranked, words = rank(found, query)
            result["words"] = words
            result["candidates"] = [{"level": p.level, "path": p.path, "title": p.title,
                                     "matched": f"{p.score[0]} of {len(words)}"} for p in ranked[:5]]
            result["clear"] = clear_winner(ranked, words)
            if result["clear"]:
                folder = root / ranked[0].path
    if folder is not None and not a.find:
        result.update(checked_link(target(folder, root), root, not a.no_restart))
        if result["status"] == 200 and not a.no_open:
            webbrowser.open(result["link"])

    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render(result))
    if "status" in result:
        return 0 if result["status"] == 200 else 1
    return 0 if result.get("candidates") else 1


def render(r: dict) -> str:
    lines = []
    if "status" in r:
        ok = "✅" if r["status"] == 200 else "❗"
        lines.append(f"{ok} {r['level']} · {r['title'] or r['path'] or r['root']}")
        lines.append(f"link    {r['link']}")
        lines.append(f"path    {r['path'] or '(SPACE root)'}")
        lines.append(f"skill   {r['skill']}" + (f"   theme {r['theme']}" if r["theme"] else ""))
        server = f"server  port {r['port']}" + (f" (pid {r['pid']})" if r["pid"] else "")
        server += f" · HTTP {r['status']} in {r['seconds']} s" + (" · restarted first" if r["restarted"] else "")
        if len(r.get("servers") or []) > 1:
            server += f" · other hosts of this SPACE: {', '.join(map(str, r['servers'][1:]))}"
        lines.append(server)
        if r["status"] != 200:
            lines.append("the page did not load; see the server log named by its --daemon flag")
        others = [c for c in r.get("candidates", [])[1:3]]
        for c in others:
            lines.append(f"also    {c['level']:<7} {c['path']}")
        return "\n".join(lines)
    if not r.get("candidates"):
        return f"❗ nothing matches “{r['query']}”"
    if r.get("clear"):
        lines.append(f"✅ clear winner for “{r['query']}” (words: {' '.join(r.get('words', []))}); top places:")
    else:
        lines.append(f"🙋 no clear winner for “{r['query']}” (words: {' '.join(r.get('words', []))}); top places:")
    for i, c in enumerate(r["candidates"], 1):
        lines.append(f"{i}. {c['level']:<7} {c['path']}  ({c['matched']})  {c['title']}")
    if not r.get("clear"):
        lines.append("pick one by meaning, then run: wb.py <its path>")
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())

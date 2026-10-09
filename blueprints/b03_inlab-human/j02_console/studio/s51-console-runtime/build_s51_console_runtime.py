"""s51 · The console runtime: how the In-Lab Console runs. The two runtimes (standalone with the HaiChat drawer, and
embedded as an iframe in a HAI-Chat thread), the processes and ports, every INLAB_* setting each module reads (from
the code), and what the image is built from: the Dockerfile's COPY lines against the modules main.py imports, a
module the image lacks drawn in red. A rebuild keeps whatever a person drew.

    python build_s51_console_runtime.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
from console_draw import APP, RED, Sheet, header, save  # noqa: E402

CHANGES = []                                          # (YYMMDD, what changed): a green note each
RUNTIMES = [
    ["standalone", "uvicorn main:app (:8091) serves the SPA, the REST routes and WS /ws/haichat",
     "the HaiChat drawer is shown; the agent runs on the local Claude Code login (Agent SDK)", "a person at the console"],
    ["embedded", "HAIChat-SPACE builds this folder (docker compose up haichat-inlab) and renders it as a per-thread iframe",
     "the drawer is hidden: Mattermost is the chat, haichat-me-agent the agent", "a clinician in a HAI-Chat thread"],
    ["fixtures", "fixtures/run_fixture.sh: the stub endpoint (:8192) + the console (:8191) on synthetic data, loopback",
     "the drawer is shown; prints both PIDs; stop them by PID", "docs, screenshots, tests"],
]


def env_reads():
    """[(INLAB_* name, the modules that read it)] from the console's Python and the engine."""
    found = {}
    files = sorted(APP.glob("*.py")) + [APP.parents[1] / "mcp-servers/endpoint-predict/server.py"]
    for f in files:
        for name in set(re.findall(r"INLAB_[A-Z_]+", f.read_text(encoding="utf-8"))):
            found.setdefault(name, []).append(f.name)
    return [[k, " · ".join(sorted(v))] for k, v in sorted(found.items())]


def image_check():
    """[(module main.py imports, copied into the image?)]"""
    imports = re.findall(r"^from (\w+) import", (APP / "main.py").read_text(encoding="utf-8"), re.M)
    local = [m for m in imports if (APP / f"{m}.py").is_file()]
    copied = set()
    for line in (APP / "Dockerfile").read_text(encoding="utf-8").splitlines():
        if line.startswith("COPY ") and "--from" not in line:
            copied |= {Path(t).stem for t in line.split()[1:-1] if t.endswith(".py")}
    rows = [["main.py", "yes" if "main" in copied else "? not copied"]]
    rows += [[f"{m}.py", "yes" if m in copied else "? not copied"] for m in local]
    return rows


def main():
    s = Sheet()
    f = s.frame("1 · The console runtime", 0, 0, 1900, 100)
    y = header(s, f, "s51 · The console runtime: where it runs, what it reads, what the image holds",
               "Nothing study-specific is committed: every store is mounted by an INLAB_* setting, read-only; patient data\n"
               "never enters an image.", CHANGES)
    y = s.table(40, y, [("runtime", 160, 16), ("how it runs", 760, 76), ("the agent", 560, 56), ("for", 300, 30)],
                RUNTIMES, f)
    y += 40
    s.text(40, y, "Every INLAB_* setting, and who reads it (read from the code)", 22, f)
    y = s.table(40, y + 40, [("setting", 360, 36), ("read by", 900, 90)], env_reads(), f)
    y += 40
    s.text(40, y, "What the image is built from (Dockerfile COPY lines vs the modules main.py imports)", 22, f)
    rows = image_check()
    y = s.table(40, y + 40, [("module", 360, 36), ("in the image?", 300, 30)], rows, f,
                red=lambda r: r[1].startswith("?"))
    if any(r[1].startswith("?") for r in rows):
        y += 30
        s.text(40, y, "? the image cannot start: main.py imports routers the Dockerfile never copies (and personas/ "
                      "is not copied either)", 16, f, RED)
    save(s, f, y + 40, HERE / "s51-console-runtime.excalidraw", "build_s51_console_runtime.py")


if __name__ == "__main__":
    main()

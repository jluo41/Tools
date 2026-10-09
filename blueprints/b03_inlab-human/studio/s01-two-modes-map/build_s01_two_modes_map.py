"""s01 · The two modes: s01-two-modes-map.excalidraw, drawn by this builder from disk (haipipe-studio).

How `plugins/inlab-human` fits together: the two modes (STUDY, the reader protocol; CONSOLE, patient-first
inference), the parts each uses (skills, the console's routers, the agent), the endpoint-predict tool both share,
and the data boundary in front of all of them, each with the Job of b03 that owns it. A part named here but not
on disk is red. Code and docs only; no case data is read. A rebuild keeps whatever a person drew.

    python build_s01_two_modes_map.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]
sys.path.insert(0, str(BLOCK.parent / "_build"))
from mapdraw import GREEN, INK, RED, Sheet  # noqa: E402

PKG = BLOCK.parents[1] / "plugins" / "inlab-human"
CHANGES = []                                          # (YYMMDD, what changed): a green note each

PARTS = [  # (mode, part, path under the plugin, Job of b03)
    ("STUDY", "/inlab-human (tier 1)", "skills/inlab-human", "j01_study"),
    ("STUDY", "/inlab-human-bundle", "skills/inlab-human-bundle", "j01_study"),
    ("STUDY", "/inlab-human-review", "skills/inlab-human-review", "j01_study"),
    ("STUDY", "/inlab-human-report", "skills/inlab-human-report", "j01_study"),
    ("STUDY", "bundle and feedback contracts", "skills/ref", "j01_study"),
    ("STUDY", "narrator agent", "agents/inlab-narrator-agent.md", "j01_study"),
    ("CONSOLE", "/inlab-human-console", "skills/inlab-human-console", "j02_console"),
    ("CONSOLE", "console_api: patients · models · predict", "servers/haichat-inlab/console_api.py", "j02_console"),
    ("CONSOLE", "message_api: compose · judge · feedback", "servers/haichat-inlab/message_api.py", "j02_console"),
    ("CONSOLE", "labeling_api · tasks_api", "servers/haichat-inlab/labeling_api.py", "j02_console"),
    ("CONSOLE", "haichat_api: the agent drawer", "servers/haichat-inlab/haichat_api.py", "j04_haichat"),
    ("BOTH", "endpoint-predict: MCP tool and CLI", "mcp-servers/endpoint-predict", "j03_endpoint"),
    ("BOTH", "the data boundary: de-identified only", "README.md", "j05_data_boundary"),
]


def version(path: Path) -> str:
    md = path / "SKILL.md" if path.is_dir() else None
    if md and md.is_file():
        m = re.search(r'^\s*version:\s*"?([\d.]+)', md.read_text(encoding="utf-8"), re.M)
        return m.group(1) if m else ""
    if path.is_file() and path.suffix == ".py":
        return f"{sum(1 for _ in path.open(encoding='utf-8', errors='ignore'))} lines"
    return ""


def main():
    s = Sheet()
    rows = []
    for mode, part, rel, job in PARTS:
        p = PKG / rel
        rows.append([mode, part, rel + ("" if p.exists() else " (? not on disk)"), version(p), job])
    tests = [t for t in PKG.rglob("*test*") if "node_modules" not in t.parts]
    cols = [("mode", 110, 10), ("part", 330, 34), ("where, under plugins/inlab-human/", 420, 42), ("size", 120, 12),
            ("Job of b03", 200, 20)]
    width = sum(w for _, w, _ in cols)
    f = s.frame("1 · The two modes", 0, 0, width + 80, 100)
    s.text(40, 30, "s01 · The two modes: a reader study and a clinician console, over one endpoint tool", 30, f)
    s.text(40, 80, "STUDY: bundle → blind, then assisted review → report.  CONSOLE: patient → chart → model → run.  "
                   "Both reach the endpoint only through endpoint-predict.", 16, f)
    for i, (date, what) in enumerate(CHANGES):
        s.text(40, 112 + i * 26, f"✎ {date} {what}", 16, f, GREEN)
    y = s.table(40, 150 + len(CHANGES) * 26, cols, rows, f, red=lambda r: "?" in r[2])
    s.text(40, y + 24, "▌ the data boundary: cases are de-identified BEFORE they enter a bundle or the console; "
                       "the plugin does not check it (j05_data_boundary)", 18, f)
    s.text(40, y + 56, f"tests in the plugin: {len(tests)}" + ("   ? none (Q02)" if not tests else ""), 18, f,
           INK if tests else RED)
    f["height"] = y + 110
    s.save(HERE / "s01-two-modes-map.excalidraw", "build_s01_two_modes_map.py")


if __name__ == "__main__":
    main()

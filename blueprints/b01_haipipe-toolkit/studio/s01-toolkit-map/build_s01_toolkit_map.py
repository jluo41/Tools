"""s01 · The toolkit map: s01-toolkit-map.excalidraw, drawn by this builder from disk (haipipe-studio).

Every part of `plugins/haipipe-toolkit` (the three skill layers by family, the servers, the agents, the MCP
servers) with its size, and the Job of b01 that owns its design questions. Counted on every rebuild, so the map
follows the folders. A rebuild keeps whatever a person drew on the canvas.

    python build_s01_toolkit_map.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]
sys.path.insert(0, str(BLOCK.parent / "_build"))
from mapdraw import GREEN, Sheet  # noqa: E402

TK = BLOCK.parents[1] / "plugins" / "haipipe-toolkit"
THEME_JOB = {"insight": "j11_theme_insight", "design": "j12_theme_design", "cowork": "j13_theme_cowork",
             "discovery": "j14_theme_discovery", "labeling": "j15_theme_labeling", "paper": "j16_theme_paper",
             "work": "j17_theme_work"}
CHANGES = []                                          # (YYMMDD, what changed): a green note each


def skills(folder: Path) -> int:
    return sum(1 for _ in folder.rglob("SKILL.md"))


def rows():
    out = [["skills · 0_utils", "skills/0_utils/", f"{skills(TK / 'skills/0_utils')} skills", "j01_utils"]]
    for fam in sorted(p for p in (TK / "skills/1_base").iterdir() if p.is_dir()):
        job = "j03_project_workbench" if fam.name == "project" else "j02_base"
        out.append([f"skills · 1_base · {fam.name}", f"skills/1_base/{fam.name}/", f"{skills(fam)} skills", job])
    for th in sorted(p for p in (TK / "skills/2_theme").iterdir() if p.is_dir()):
        job = THEME_JOB.get(th.name, "? no Job")
        out.append([f"skills · 2_theme · {th.name}", f"skills/2_theme/{th.name}/", f"{skills(th)} skills", job])
    for srv in sorted(p for p in (TK / "servers").iterdir() if p.is_dir()):
        theme = srv.name.removeprefix("workbench-")
        job = THEME_JOB.get(theme) if srv.name.startswith("workbench-") else "j03_project_workbench"
        py = sum(1 for f in srv.rglob("*.py") if "tests" not in f.parts)
        out.append([f"server · {srv.name}", f"servers/{srv.name}/", f"{py} .py files", job or "? no Job"])
    chat = [f for f in ("chat.py", "term.py") if (TK / "servers/workbench" / f).is_file()]
    if chat:
        out.append(["the chat drawer", "servers/workbench/" + " · ".join(chat), "kept, not loaded by any page",
                    "j05_chat"])
    agents = sorted((TK / "agents").glob("*.md")) if (TK / "agents").is_dir() else []
    out.append(["agents", "agents/", f"{len(agents)} agents", "? their theme's Job"])
    for m in sorted(p for p in (TK / "mcp-servers").iterdir() if p.is_dir()) if (TK / "mcp-servers").is_dir() else []:
        out.append([f"mcp server · {m.name}", f"mcp-servers/{m.name}/", "", "? no Job"])
    out.append(["how all of it sits on disk", "skills/ · servers/ · agents/", "", "j04_skill_folder"])
    return out


def main():
    s = Sheet()
    data = rows()
    cols = [("part", 330, 32), ("where, under plugins/haipipe-toolkit/", 420, 42), ("size", 260, 26),
            ("owning Job of b01", 280, 28)]
    f = s.frame("1 · The toolkit map", 0, 0, sum(w for _, w, _ in cols) + 80, 100)
    s.text(40, 30, "s01 · The toolkit map: every part of haipipe-toolkit, and the Job that owns it", 30, f)
    s.text(40, 80, "Counted from disk on each rebuild. Red: a part with no owning Job yet (? open).", 18, f)
    for i, (date, what) in enumerate(CHANGES):
        s.text(40, 112 + i * 26, f"✎ {date} {what}", 16, f, GREEN)
    y = s.table(40, 150 + len(CHANGES) * 26, cols, data, f, red=lambda r: str(r[3]).startswith("?"))
    f["height"] = y + 40
    s.save(HERE / "s01-toolkit-map.excalidraw", "build_s01_toolkit_map.py")


if __name__ == "__main__":
    main()

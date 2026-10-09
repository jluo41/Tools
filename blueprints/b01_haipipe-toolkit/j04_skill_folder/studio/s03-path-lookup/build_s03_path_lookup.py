"""b04 s03 · Path lookup: s03-path-lookup.excalidraw, how code finds a skill since q02, and what
still breaks on the next move. Feeds reports/q02_path_fix.

Read from disk every build: how many code sites use each lookup, how many still name a layer
literally (code and Markdown), Pages with an old-form structure-source, exported delivery scripts
with the old engine path, and the moved paths git does not know yet.

    python build_s03_path_lookup.py [out.excalidraw]
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "_build"))
from sketch import (GRAY, SPACE, TK, TOOLS, arrow, board_questions, concern, legend, mono,  # noqa: E402
                    questions_frame, save, sticky, text)

CODE = ("*.py", "*.js", "*.mjs", "*.sh")


def count(pattern, where, globs, fixed=False):
    args = ["grep", "-rIc", "--exclude-dir=.git", "--exclude-dir=node_modules", "--exclude-dir=_legacy",
            "--exclude-dir=venue", "--exclude-dir=delivery", "--exclude-dir=board"]
    args += [f"--include={g}" for g in globs]
    args += ["-F" if fixed else "-E", pattern, str(where)]
    out = subprocess.run(args, capture_output=True, text=True).stdout.splitlines()
    hits = [int(l.rsplit(":", 1)[1]) for l in out if l.rsplit(":", 1)[1] != "0"]
    return sum(hits), len(hits)


def facts():
    f = {}
    f["skill_dir"] = count(r"skill_dir\(", TK, CODE)
    f["anchor"] = count(r'p\.name == "skills"', TK, CODE)
    f["in_skills"] = count(r"in_skills\(", TK, CODE)
    f["layer_code"] = count(r'["/](1_base|2_theme|0_utils)["/]', TK, CODE)
    f["layer_md"] = count(r"(skills/|`)(1_base|2_theme)/", TOOLS, ("*.md",))
    pages = subprocess.run(["grep", "-rlE", "--include=*.md", "--exclude-dir=.git", "--exclude-dir=_WorkSpace",
                            "--exclude-dir=node_modules", "--exclude-dir=.venv",
                            r"^structure-source:\s*(Tools/plugins/haipipe-toolkit/skills/)?paper/", str(SPACE)],
                           capture_output=True, text=True).stdout.split()
    f["old_source"] = len(pages)
    delivery = subprocess.run(["grep", "-rlF", "--include=*.sh", "skills/page/haipipe-page/cli/page.py", str(SPACE)],
                              capture_output=True, text=True).stdout.split()
    f["old_delivery"] = len([d for d in delivery if "/delivery/" in d])
    st = subprocess.run(["git", "-C", str(TOOLS), "status", "--short", "--", "plugins/haipipe-toolkit/skills",
                         "plugins/subjective-label"], capture_output=True, text=True).stdout.splitlines()
    f["git_deleted"] = sum(1 for l in st if l[:2].strip() == "D")
    f["git_untracked"] = sum(1 for l in st if l.startswith("??"))
    gm = (TOOLS / ".gitmodules").read_text()
    m = re.search(r'\[submodule "([^"]*venue)"\]\s*\n\s*path = (\S+)', gm)
    f["venue"] = m.groups() if m else ("?", "?")
    return f


def draw():
    f = facts()
    text(0, -170, "b04 s03 · how code finds a skill now", 44)
    legend(900, -170)
    text(0, -105, "Read from disk: the lookups in use, what still names a layer, what is left from the move. "
                  "Red = open.", 20, GRAY)

    flow = ["server code    host_paths.skill_dir('<skill>')          by folder name, nearest first",
            "skill code     next(p ... if p.name == 'skills')         the skills root by name",
            "Page engine    src/skill_paths.skill_dir / in_skills     + paths written before the layers",
            "host           host_registry.workbench_folders()         workbench, workbench-* by name",
            "Markdown       written from the layer: 1_base/page/...   a reader opens it directly"]
    r, b = mono(0, 0, flow, "who finds a skill, and how")

    n = [f"skill_dir(...) calls                 {f['skill_dir'][0]:>4} in {f['skill_dir'][1]} files",
         f"'skills' name anchors                {f['anchor'][0]:>4} in {f['anchor'][1]} files",
         f"in_skills(...) calls                 {f['in_skills'][0]:>4} in {f['in_skills'][1]} files",
         f"!layer named literally in code       {f['layer_code'][0]:>4} in {f['layer_code'][1]} files",
         f"!layer named in Markdown (Tools)     {f['layer_md'][0]:>4} in {f['layer_md'][1]} files",
         f"!Pages: structure-source old form    {f['old_source']:>4}",
         f"!delivery scripts: old page.py path  {f['old_delivery']:>4}",
         f"!git: deleted at old path            {f['git_deleted']:>4}   untracked new: {f['git_untracked']}",
         f"venue submodule  name: {f['venue'][0]}",
         f"                 path: {f['venue'][1]}"]
    r2, b2 = mono(r + 120, 0, n, "counted now")
    arrow(r + 10, 90, r + 110, 90)

    sy = max(b, b2) + 80
    sticky(0, sy, 560, "Lookup by name survives the next layer\nmove; a literal layer path does not.", "idea")
    sticky(600, sy, 560, "agree.py (haipipe-writing) now accepts\n1_base and 2_theme heads: it can check\n"
                         "Markdown paths after a move.", "idea")
    cy = sy + 180
    for c in ["? skill_dir() returns the FIRST folder with that name (venue is in design/ and paper/) and",
              "  silently falls back to skills/<name> when none exists: should a miss raise instead?",
              "? It searches 4 folders deep: a skill nested deeper (a 5th level) is not found.",
              "? The red counts above are what the next move must fix again: worth a check script that runs",
              "  after every move (link checker + FAMILIES check + agree.py), kept in this Block?",
              "? Pages in project folders still write structure-source in the old form: the skills-relative",
              "  form resolves; the SPACE-rooted form never did. Edit those Pages, or leave them?",
              "? Exported delivery run scripts with the old page.py path (count above) refresh only when",
              "  each Page is exported again (generated files: never edited by hand).",
              "? The moves are plain mv: git sees deletions plus untracked folders until someone stages them.",
              "? The venue submodule keeps its old NAME (paper/venue) with a new PATH: rename it in",
              "  .gitmodules and .git/modules, or leave it?"]:
        cy = concern(0, cy, c) + 6

    qs = dict(board_questions(BLOCK))
    questions_frame(0, cy + 120, [
        (f"Q02 · {qs.get('q02_path_fix', 'path fix')}",
         [("done; checks in the report", "done"),
          ("a post-move check script?\nstaging the moves?", "open")]),
    ])


if __name__ == "__main__":
    draw()
    save(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s03-path-lookup.excalidraw", "build_s03_path_lookup.py")

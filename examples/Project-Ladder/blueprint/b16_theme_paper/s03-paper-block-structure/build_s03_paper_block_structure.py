"""Draw named Paper groups and their Jobs, Tasks and Studio topics.

Read hai-studio/CONSTITUTION.md before changing this drawing. The shared
canvas writer and seed preserve human marks. Names describe the proposed
Paper structure; they do not claim that these records exist on disk.
Python 3.12+ and Pillow are required by the shared Studio helpers.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True
STEM = "s03-paper-block-structure"
NAVY, BLUE = "#17324d", "#547b9d"
MUTED, LINE, KEY = "#596c7c", "#aabfce", "#fff3bf"


def repo_root(explicit: Path | None) -> Path:
    candidates = [explicit] if explicit else list(Path(__file__).resolve().parents)
    for candidate in candidates:
        if candidate and (candidate / "PRINCIPLE.md").is_file():
            return candidate.resolve()
    raise SystemExit("Pass --repo-root pointing to the Tools-SPACE checkout.")


def build(repo: Path, target: Path) -> tuple[Path, Path]:
    if sys.version_info < (3, 12):
        raise SystemExit("Use Python 3.12+ with Pillow for the shared Studio helpers.")
    helpers = repo / "plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts"
    sys.path.insert(0, str(helpers))
    import canvas
    import icons
    import quick_draw as q
    import render_png

    frame = q._el("frame", "general_structure", 0, 0, 2560, 1440,
                  stroke=LINE, fill="#ffffff", name="Paper Block structure")
    els = [frame]

    def put(items):
        for item in items:
            item["frameId"] = frame["id"]
            item["roughness"] = 0
            if item["type"] == "text":
                item["fontFamily"] = canvas.FONT
        els.extend(items)

    def txt(key, x, y, words, size=32, color=NAVY, align="left"):
        put(q.text(key, x, y, words, size, color, align))

    def arrow(key, points):
        put(q.arrow(key, points, color=BLUE, width=2.5))

    def doc(key, x, y, w=50, h=66):
        items = icons.document(key, 0, 0)
        for item in items:
            item["x"] = x + item["x"] * w / 100
            item["y"] = y + item["y"] * h / 130
            item["width"] *= w / 100
            item["height"] *= h / 130
            if "points" in item:
                item["points"] = [[a * w / 100, b * h / 130] for a, b in item["points"]]
        for item in items:
            if item.get("strokeColor") not in ("transparent", "#ffffff"):
                item["strokeColor"] = BLUE
            if item.get("backgroundColor") not in ("transparent", "#ffffff", ""):
                item["backgroundColor"] = "#ffffff"
        put(items)

    txt("title", 70, 45, "Paper Block structure", 58)
    put([q._el("rectangle", "writing_rule", 1150, 45, 1320, 78,
               stroke=KEY, fill=KEY, roundness={"type": 3})])
    txt("writing_rule_words", 1190, 64, "Review + Submission belong to each Writing Job", 32)

    for key, x, words in [("groups", 285, "Job group"), ("jobs", 760, "Job Type / Job Name"),
                          ("task_groups", 1240, "Task group"), ("tasks", 1890, "Task Type / Task Name")]:
        txt(key + "_heading", x, 175, words, 30, MUTED)

    # Paper owns named Job groups. Each group organizes Jobs, not new folder levels.
    doc("paper", 75, 560, 90, 116)
    txt("paper_name", 120, 701, "Paper", 36, NAVY, "center")
    put(q.line("paper_trunk", [(180, 618), (215, 618)], BLUE, 3))
    put(q.line("groups_trunk", [(215, 290), (215, 1010)], BLUE, 3))

    rows = [
        ("story", 255, "Story", "Shared story",
         "Questions\nArgument\nNarrative", "Research question\nContribution\nSection outline"),
        ("evidence", 425, "Evidence", "Shared evidence",
         "Values\nCitations\nChecks", "Reported estimates\nSource verification\nEvidence audit"),
        ("display", 595, "Display", "Main\nAppendix\nExplore",
         "Figures\nTables", "Study workflow\nResults table"),
        ("writing", 765, "Writing", "Manuscript\nRevised manuscript",
         "Main text\nAppendix\nReview\nSubmission", "Abstract · Methods\nSupplement\nReviewer response\nCover letter · Portal"),
        ("presentation", 975, "Presentation", "Slides · Video\nPoster",
         "Content\nDelivery", "Slides · Script · Poster\nNotes · Captions · Export"),
    ]
    job_types = {"story": "Story†", "evidence": "Evidence†", "display": "Display",
                 "writing": "Writing Version", "presentation": "Presentation†"}
    task_types = {"story": "Story output†", "evidence": "value / evidence‡",
                  "display": "Figure / Table†", "writing": "draft + portal record‡",
                  "presentation": "Presentation output†"}
    for key, y, group, jobs, topics, tasks in rows:
        arrow(key + "_branch", [(215, y + 35), (265, y + 35)])
        put([q._el("rectangle", key + "_group_scope", 270, y - 7, 310, 88,
                   stroke=LINE, fill="#f5f8fb", strokeStyle="dashed", roundness={"type": 3})])
        txt(key + "_group", 285, y + 12, group, 36)
        arrow(key + "_job_link", [(600, y + 35), (665, y + 35)])
        doc(key + "_job", 685, y + 3)
        txt(key + "_job_type", 760, y - 18, job_types[key], 28, MUTED)
        txt(key + "_job_names", 760, y + 24, jobs, 30)
        arrow(key + "_task_scope", [(1115, y + 35), (1210, y + 35)])
        txt(key + "_task_groups", 1240, y + 12, topics, 30, BLUE)
        arrow(key + "_task_link", [(1710, y + 35), (1860, y + 35)])
        txt(key + "_task_type", 1890, y - 18, task_types[key], 28, MUTED)
        txt(key + "_tasks", 1890, y + 24, tasks, 30)

    # Studio records hold open design questions; Job Tasks do the work.
    put(q.line("studio_rule", [(70, 1125), (2490, 1125)], LINE, 1.5))
    txt("studio_heading", 70, 1163, "Studio", 38)
    for key, x, group, topic in [
        ("story_design", 350, "Story", "Argument design"),
        ("display_design", 890, "Display", "Figure composition"),
        ("writing_design", 1430, "Writing", "Venue fit"),
        ("presentation_design", 1970, "Presentation", "Talk narrative"),
    ]:
        txt(key + "_group", x, 1165, group, 32, BLUE)
        arrow(key + "_branch", [(x + 20, 1210), (x + 20, 1240)])
        doc(key + "_topic", x, 1253, 30, 40)
        txt(key + "_name", x + 48, 1258, topic, 30)
    txt("same_studio_views", 70, 1360, "Structure  ·  Draw  ·  Examples  ·  Skills", 32, MUTED)

    txt("type_limits", 1150, 1360, "† Contract to define   ‡ Legacy type conflict", 28, MUTED)

    target.mkdir(parents=True, exist_ok=True)
    drawing = target / (STEM + ".excalidraw")
    preview = target / (STEM + ".png")
    canvas.write(drawing, els, source="hai-studio: named Paper structure proposal", palette=False)
    render_png.render(drawing, preview, s=0.75)
    return drawing, preview


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    for file in build(repo_root(args.repo_root), args.out_dir):
        print(file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

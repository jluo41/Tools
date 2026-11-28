"""Rebuild Idea Block Structure with the shared Studio drawing kit.

Read hai-studio/CONSTITUTION.md before changing the drawing.
Use --repo-root when previewing outside the repository. The shared canvas writer
keeps the person's annotations and its adjacent seed snapshot on each rebuild.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

STEM = "s01-idea-block-structure"
NAVY = "#19354d"
BLUE = "#527da3"
PALE = "#edf4fa"
QUIET = "#708399"
AMBER = "#b47521"
GREEN = "#2f8063"


def repository(explicit: Path | None) -> Path:
    candidates = [explicit] if explicit else [*Path(__file__).resolve().parents, Path.cwd()]
    for candidate in candidates:
        if candidate is not None and (candidate / "PRINCIPLE.md").is_file():
            return candidate.resolve()
    raise SystemExit("Pass --repo-root pointing to the toolkit checkout.")


def build(repo: Path, out: Path) -> Path:
    scripts = repo / "plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts"
    sys.path.insert(0, str(scripts))
    import canvas
    import icons
    import quick_draw as q
    from render_png import render

    q.FONT = 6
    frame = q._el("frame", "idea_structure", 0, 0, 2560, 1440,
                  name="Idea Block Structure", strokeColor="#ffffff")
    els = [frame]

    def label(eid, x, y, words, size=32, color=NAVY, center=False):
        els.extend(q.text(eid, x, y, words, size, color, "center" if center else "left"))

    def line(eid, points, color=BLUE, width=3, dashed=False):
        els.extend(q.line(eid, points, color, width, dashed))

    def arrow(eid, points, color=BLUE, dashed=False):
        els.extend(q.arrow(eid, points, color, dashed=dashed, width=3))

    def picture(items, color=BLUE, fill=PALE):
        for item in items:
            item["strokeColor"] = color
            if item.get("backgroundColor") not in ("transparent", "#ffffff"):
                item["backgroundColor"] = fill
        els.extend(items)

    label("title", 70, 62, "Idea Block Structure", 60)
    label("lead", 73, 144, "Structure · Draw · Examples · Skills", 34, QUIET)

    # The owner boundary contains two real record families: Jobs and Studio topics.
    els.extend(q.box("block_scope", 65, 235, 2430, 1055, sem="none"))
    els[-1]["strokeColor"] = BLUE
    label("block_owner", 105, 265, "Idea · Robustness under distribution change", 42)
    label("jobs_branch", 105, 350, "Jobs", 40)
    label("job_type", 910, 355, "Job Type · Idea Job", 28, QUIET, True)
    label("task_type", 2250, 355, "Task Type · ideation", 28, QUIET, True)

    for eid, x, words in (("job_topic_header", 290, "Job group"),
                           ("job_header", 910, "Job Name"),
                           ("task_topic_header", 1465, "Task group"),
                           ("task_header", 2250, "Task Name")):
        label(eid, x, 425, words, 30, QUIET, True)

    # Group nodes have soft outlines; document icons denote actual records.
    # Candidate names come from the Idea owner contract's robustness example.
    # The face records this as design, not as existing Jobs or produced results.
    for eid, x, y, w, h in (("ideas_group", 115, 555, 350, 90),
                            ("framing_group", 1290, 465, 350, 80),
                            ("assessment_group", 1290, 625, 350, 80),
                            ("decision_group", 1290, 805, 350, 80),
                            ("studio_group_node", 115, 1068, 420, 90)):
        els.extend(q.box(eid, x, y, w, h, sem="plain"))
        els[-1]["backgroundColor"] = PALE
        els[-1]["strokeColor"] = BLUE
    label("ideas", 290, 577, "Ideas", 38, center=True)
    picture(icons.document("job_1_record", 655, 545, "off", 85, 115))
    label("job_1", 775, 557, "Calibration\nunder shift", 34)
    picture(icons.document("job_2_record", 655, 745, "off", 85, 115))
    label("job_2", 775, 757, "Missingness\nrobustness", 34)
    label("framing", 1465, 485, "Framing", 38, center=True)
    label("assessment", 1465, 645, "Assessment", 38, center=True)
    label("decision", 1465, 825, "Decision", 38, center=True)
    for eid, y, words in (("claim", 465, "Falsifiable\nclaim"),
                           ("comparison", 575, "Closest-work\ncomparison"),
                           ("experiment", 685, "Minimum\nexperiment"),
                           ("recommendation", 795, "Development\nrecommendation")):
        task_icon = icons.document(eid + "_record", 2010, y, "off", 70, 95)
        # Keep the shared icon's first three text strokes within its shorter page.
        picture([item for item in task_icon if item["id"] != eid + "_record_t3"])
        label(eid, 2115, y + 15, words, 32)

    line("jobs_fan", [(465, 600), (550, 600), (550, 800)])
    arrow("first_job", [(550, 600), (630, 600)])
    arrow("second_job", [(550, 800), (630, 800)])
    line("task_topics_link", [(1040, 600), (1180, 600)])
    line("task_topics_fan", [(1180, 505), (1180, 845)])
    for eid, y in (("framing", 505), ("assessment", 665), ("decision", 845)):
        arrow(eid + "_link", [(1180, y), (1265, y)])
    arrow("claim_link", [(1640, 505), (1985, 505)])
    line("assessments_link", [(1640, 665), (1840, 665)])
    line("assessments_fan", [(1840, 615), (1840, 725)])
    arrow("comparison_link", [(1840, 615), (1985, 615)])
    arrow("experiment_link", [(1840, 725), (1985, 725)])
    arrow("recommendation_link", [(1640, 845), (1985, 845)])

    line("families_divider", [(105, 905), (2450, 905)], "#c2d4e2", 2)
    label("studio_branch", 105, 940, "Studio", 40)
    label("studio_group", 325, 1090, "Research design", 36, center=True)
    line("studio_fan", [(535, 1110), (650, 1110), (650, 1040), (650, 1190)])
    arrow("first_studio", [(650, 1040), (780, 1040)])
    arrow("second_studio", [(650, 1190), (780, 1190)])
    picture(icons.document("studio_1_record", 805, 985, "off", 82, 115))
    label("studio_1", 925, 1020, "Direction map", 38)
    picture(icons.document("studio_2_record", 805, 1135, "off", 82, 115))
    label("studio_2", 925, 1170, "Assessment plan", 38)
    els.extend(q.box("record_key", 1395, 1000, 920, 245, sem="plain"))
    els[-1]["backgroundColor"] = "#fff3bf"
    els[-1]["strokeColor"] = AMBER
    label("record_relationship", 1855, 1035, "Idea Jobs + Studio topics", 34, center=True)
    label("record_siblings", 1855, 1090, "share one Block", 32, QUIET, True)
    label("groups", 1855, 1175, "Groups add no folder level", 30, QUIET, True)

    label("idea_rule", 1280, 1340,
          "Idea rule: one candidate per Job; skills are methods inside Tasks.",
          30, NAVY, True)

    for element in els[1:]:
        element["frameId"] = frame["id"]
        element["roughness"] = 0
    destination = out / (STEM + ".excalidraw")
    canvas.write(destination, els, source="hai-studio: Idea Block Structure", palette=False)
    render(destination, out / (STEM + ".png"), 0.75)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    print(build(repository(args.repo_root), args.out_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""s02 · Paper Studio: s02-paper-studio.excalidraw, one dense frame (haipipe-studio, JL 261011: "the draw is
too thin ... What will be a groups for the studio items?").

  row 1  the six groups of a paper Board's Studio, in the order a paper is thought through, each with its
         topic folder, what it holds, the skill that writes it and ScalingGlucose's topic (or none yet)
  row 2  what a Story topic feeds: its Questions, the stage gate, the version built from it, its Sections,
         its built paper; and the loop back when a review comes in
  row 3  the proposed studio/_groups.txt, ScalingGlucose's Studio today, and what is open

Facts: b16 s01-paper-tree (s01-D06..D08, the Board's Studio and Questions), b10 s09-D01 and D04 (one Studio
per Block; a Job is built from an agreed topic), the paper skills, and Paper-ScalingGlucose-NatSeries2026
read live on 261011 (studio/s01-ideation, s02-story-nmi-cgm-scaling-axes, s03-paper-workflow; its
Questions carry group: nmi-cgm-scaling-axes). The group names are a proposal, in red until JL picks.

    python build_s02_paper_studio.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts").resolve()))
import canvas  # noqa: E402  (haipipe-studio's merge-safe writer)

INK, RED = canvas.INK, canvas.RED
SANS, MONO = 6, 3
els = []

GROUPS = [  # name, folder, what it holds, skill, ScalingGlucose today, stage it usually sits at
    ("1 Ideation", "s01-ideation/", ["the direction and its", "candidate questions;", "each idea becomes a",
     "Question (group: ideation)"], "haipipe-paper-ideation", "s01-ideation", "explore → shaping"),
    ("2 Story", "sNN-story-<venue>-<idea>/", ["one telling: its research", "questions, claims and", "the Section order;",
     "Questions group: <telling>"], "haipipe-paper-story", "s02-story-nmi-cgm-…", "shaping → agreed"),
    ("3 Plan", "sNN-<plan>/", ["how the evidence is made:", "Discovery and Task", "roadmaps, who runs what,", "in which order"],
     "haipipe-paper-workflow", "s03-paper-workflow", "shaping"),
    ("4 Figures", "sNN-figure-<name>/", ["the main figures drawn", "before the Sections:", "what each must show,", "its data, its sketch"],
     "haipipe-display", "none yet", "explore → agreed"),
    ("5 Review", "sNN-review-<round>/", ["a review round thought", "through: the points, the", "answers, the new", "questions it raises"],
     "haipipe-paper-comments", "none yet", "per round"),
    ("6 Talk", "s61-s69 slide drafts", ["a talk's deck before it", "is built: its logic flow", "and its slides", "(the s6x band)"],
     "excalidraw-slide", "none yet", "explore → closed"),
]


def el(kind, x, y, w, h, frame, **extra):
    e = {"id": f"e{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
         "strokeColor": INK, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1.5,
         "strokeStyle": "solid", "roughness": 1, "opacity": 100, "groupIds": [], "frameId": frame,
         "roundness": None, "seed": 1, "version": 1, "versionNonce": 1, "isDeleted": False,
         "boundElements": [], "updated": 1, "link": None, "locked": False}
    e.update(extra)
    els.append(e)
    return e


def text(x, y, s, size, frame, color=INK, font=SANS):
    lines = s.split("\n")
    return el("text", x, y, max(len(l) for l in lines) * size * (0.6 if font == MONO else 0.55),
              len(lines) * size * 1.3, frame, text=s, originalText=s, fontSize=size, fontFamily=font,
              textAlign="left", verticalAlign="top", containerId=None, autoResize=True, lineHeight=1.3,
              strokeColor=color)


def arrow(pts, frame, color=INK, dashed=False):
    x0, y0 = pts[0]
    rel = [[px - x0, py - y0] for px, py in pts]
    return el("arrow", x0, y0, max(abs(a) for a, _ in rel) or 1, max(abs(b) for _, b in rel) or 1, frame,
              points=rel, lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=None,
              endArrowhead="arrow", strokeColor=color, strokeStyle="dashed" if dashed else "solid")


def box(x, y, w, h, frame, color=INK, dashed=False):
    return el("rectangle", x, y, w, h, frame, strokeColor=color, strokeStyle="dashed" if dashed else "solid")


def groups_row(f, y0):
    """Row 1: the six groups, left to right, the most important part of the frame."""
    text(40, y0, "THE SIX GROUPS OF A PAPER'S STUDIO, in the order a paper is thought through", 26, f)
    w, gap, top, h = 370, 50, y0 + 80, 400
    xs = [40 + i * (w + gap) for i in range(len(GROUPS))]
    for x, (name, folder, holds, skill, sg, stage) in zip(xs, GROUPS):
        box(x, top, w, h, f)
        text(x + 18, top + 14, name, 26, f)
        text(x + 18, top + 56, folder, 20, f, font=MONO)
        text(x + 18, top + 96, "\n".join(holds), 20, f)
        text(x + 18, top + 214, "writes: " + skill, 20, f)
        text(x + 18, top + 248, "stage: " + stage, 20, f)
        none = sg == "none yet"
        text(x + 18, top + 300, "ScalingGlucose:", 20, f)
        text(x + 18, top + 330, sg, 20, f, RED if none else INK, SANS if none else MONO)
    for a, b in zip(xs[:3], xs[1:4]):                      # Ideation → Story → Plan → Figures
        arrow([(a + w + 4, top + h / 2), (b - 4, top + h / 2)], f)
    arrow([(xs[1] + w / 2, top - 4), (xs[1] + w / 2, top - 20), (xs[5] + w / 2, top - 20), (xs[5] + w / 2, top - 4)],
          f, dashed=True)                                  # a telling is what a talk tells
    text(xs[3] + 40, top - 48, "a talk tells one telling", 20, f)
    return top + h, xs, w


def feeds_row(f, y0, xs, w):
    """Row 2: what a Story topic feeds, the stage gate, and the loop back from a review."""
    text(40, y0, "WHAT A STORY TOPIC FEEDS", 26, f)
    top, h = y0 + 50, 200
    steps = [("Story topic", "sNN-story-<venue>-<idea>/", "the telling, drawn"),
             ("Board Questions", "reports/qNN_<question>/", "group: <telling>"),
             ("GATE: agreed?", "its Stage line", "a person signs it"),
             ("Version", "jNN_v<MMDD>_<venue>/", "## Narrative = its order"),
             ("Sections", "tNN_<section>/", "one Page Task each"),
             ("Built paper", "delivery/jNN_<version>/", "a person marks it sent")]
    for i, (x, (head, path, note)) in enumerate(zip(xs, steps)):
        gate = head.startswith("GATE")
        box(x, top, w, h, f, RED if gate else INK, dashed=gate)
        text(x + 18, top + 16, head, 24, f, RED if gate else INK)
        text(x + 18, top + 64, path, 20, f, font=MONO)
        text(x + 18, top + 110, note, 20, f)
        if i:
            arrow([(xs[i - 1] + w + 4, top + h / 2), (x - 4, top + h / 2)], f)
    loop_y = top + h + 46                                  # comments come back: Built paper → Review → Questions
    arrow([(xs[5] + w / 2, top + h + 4), (xs[5] + w / 2, loop_y), (xs[1] + w / 2, loop_y), (xs[1] + w / 2, top + h + 4)], f)
    text(xs[2] + 20, loop_y + 8, "a review comes back → a Review topic → new Questions → the telling changes", 20, f)
    arrow([(xs[4] + w / 2, top - 120), (xs[4] + w / 2, top - 4)], f, dashed=True)
    text(xs[4] + w / 2 + 12, top - 118, "Review topics read the round", 20, f)
    return loop_y + 50


def bottom_row(f, y0):
    """Row 3: the proposed groups file, ScalingGlucose today, and what is open."""
    text(40, y0, "studio/_groups.txt for a paper Board", 24, f, RED)
    box(40, y0 + 40, 520, 230, f, RED, dashed=True)
    text(64, y0 + 60, "Ideation\nStory\nPlan\nFigures\nReview\nTalk", 20, f, RED, MONO)
    text(260, y0 + 60, "? the names: yours to pick\n? written by the paper\n  scaffold, or by hand", 20, f, RED)
    text(620, y0, "ScalingGlucose's Studio today", 24, f)
    box(620, y0 + 40, 820, 230, f)
    text(644, y0 + 60, "s01-ideation                    face · draft/\n"
                       "s02-story-nmi-cgm-scaling-axes  face · draft/\n"
                       "s03-paper-workflow              drawing, builder", 20, f, font=MONO)
    text(644, y0 + 160, "? no Tags, no Stage on any of the three\n? s03-paper-workflow has no face file", 20, f, RED)
    text(1500, y0, "OPEN", 24, f, RED)
    text(1500, y0 + 44, "? the numbers: s01 ideation, then tellings and plans from s02;\n"
                        "   figures and reviews after them; talks in s61-s69?\n"
                        "? a version's Studio view: only its own telling, or every topic?\n"
                        "? Figures topic vs a Section's display units (haipipe-display):\n"
                        "   where does a figure's design end and its build begin?\n"
                        "? does a telling's group name the Questions' group, one to one?", 20, f, RED)


def main():
    els.clear()
    f = el("frame", 0, 0, 2560, 1440, None, name="1 · The paper's Studio: six groups, one flow")["id"]
    text(40, 30, "s02 · Paper Studio: how a paper is thought through before it is written", 34, f)
    text(40, 84, "One Studio per paper Board, opened from every version and Section (b10 s09-D01). Its topics fall in six "
                 "groups (Tags); a telling must be agreed before a version is built from it.", 21, f)
    bottom, xs, w = groups_row(f, 140)
    y = feeds_row(f, bottom + 90, xs, w)
    bottom_row(f, y + 20)
    canvas.write(HERE / "s02-paper-studio.excalidraw", els, "build_s02_paper_studio.py")


if __name__ == "__main__":
    main()

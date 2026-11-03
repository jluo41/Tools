"""b12 s06 · the design workflow, drawn in haipipe-studio's five parts (Idea · Now · Design · Process · Delivery,
excalidraw-studio owns the shape). Its Design is one sketch, sketch_workflow.py: the workflow as areas, one per
act, a few words a step. The slides (slides/build_slides.py) tell the same steps one at a time.

    python build_s06_design_workflow.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
sys.path.insert(0, str(HERE))
import five_parts as fp  # noqa: E402
import sketch_workflow  # noqa: E402

SPEC = {
    "title": "The design workflow: from a signed goal to released designs, and back from the experiment",
    "why": {"question": "why do we need s06?",
            "notes": ["the steps sit in eight\ngates and many Runs", "no picture shows the\norder or the loops",
                      "insight has its map;\ndesign had none"],
            "quote": "JL 261102: make one for the design as well, vivid"},
    "what": {"head": "② what s06 hands over: the workflow, for the design skills", "icon": "deck", "name": "delivery/deck/",
             "type": "skill", "deck_why": "the slides, one step at a time",
             "parts": [("deck", "slides/: one Excalidraw drawing a slide", "the workflow told one step a slide",
                        (HERE / "s06-design-workflow.slides.json").is_file()),
                       ("book", "skill/design-workflow.md", "the workflow's section, for haipipe-design-workflow", False)]},
    "job": None,
    "target": "haipipe-design-workflow SKILL.md (the routes, as one picture)",
    "missing": [("skill/design-workflow.md", "not written yet")],
}


def design():
    els, _ = sketch_workflow.sketch(690, 280)
    return els


if __name__ == "__main__":
    right = max(e["x"] + e["width"] for e in design())          # the Design's right edge, before it is moved and grown
    right = fp.OX + (right + fp.MOVE - fp.OX) * fp.GROW
    fp.build(HERE, SPEC, design, shift=max(1050, round(right - 60 - 2020)))   # Process and Delivery start past it

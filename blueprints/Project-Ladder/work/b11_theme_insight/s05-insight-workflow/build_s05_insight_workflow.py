"""b11 s05 · the insight workflow, drawn in haipipe-studio's five parts (Idea · Now · Design · Process · Delivery,
excalidraw-studio owns the shape). Its Design is one sketch, sketch_workflow.py: the workflow as areas, one per
act, a few words a step. The slides (slides/build_slides.py) tell the same steps one at a time.

    python build_s05_insight_workflow.py
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
    "title": "The insight workflow: from a plan and a data freeze to a signed handoff",
    "why": {"question": "why do we need s05?",
            "notes": ["the steps sit in twelve\nrules and forty Runs", "no picture shows the\norder or the loops",
                      "the screens need a\nmap to hang on"],
            "quote": "JL 261101: a studio to understand the overall workflow"},
    "what": {"head": "② what s05 hands over: the workflow, for the insight skills", "icon": "deck", "name": "delivery/deck/",
             "type": "skill", "deck_why": "the eleven slides, one step at a time",
             "parts": [("deck", "slides/: eleven slides, each an Excalidraw drawing", "the workflow told one step a slide",
                        (HERE / "s05-insight-workflow.slides.json").is_file()),
                       ("book", "skill/insight-workflow.md", "the workflow's section, for haipipe-insight", False)]},
    "job": None,
    "target": "haipipe-insight SKILL.md (the workflow section)",
    "missing": [("skill/insight-workflow.md", "not written yet")],
}


def design():
    els, _ = sketch_workflow.sketch(690, 280)
    return els


if __name__ == "__main__":
    right = max(e["x"] + e["width"] for e in design())          # the Design's right edge, before it is moved and grown
    right = fp.OX + (right + fp.MOVE - fp.OX) * fp.GROW
    fp.build(HERE, SPEC, design, shift=max(1050, round(right + 40 - 2020)))   # Process and Delivery start past it

"""Draw Guide with its View row directly below the Space row.

Reuses v2's sample content and drawing primitives, with the navigation above
the full-width content. No navigation sidebar occupies the working area.
"""

import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "shared_guide_content", HERE / "workbench-shared-guide-v2.py")
content = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(content)
ui = content.ui
rect, text, button = ui.rect, ui.text, ui.button
INK, MUTED, RULE = ui.INK, ui.MUTED, ui.RULE
FW, FH, GAP = content.FW, content.FH, content.GAP
CONTENT_W, MAIN_W = 1388, 1016
PREVIEWS = ["v3-01-guide-skills", "v3-02-guide-progress",
            "v3-03-labeling-definition", "v3-04-guide-studio"]


def horizontal_shell(key, x, y, space, view, title, description):
    rect(key + "-screen", x + 24, y + 110, FW - 48, 800, INK, "#ffffff")
    text(key + "-family", x + 44, y + 132, "Labeling Workbench", 24)
    text(key + "-instance", x + 44, y + 165, "Instance · b01_pilot", 16, MUTED)
    button(key + "-switch", x + 1098, y + 134, 202, 38, "Switch instance  v", size=15)
    button(key + "-folder", x + 1312, y + 134, 122, 38, "Folder >", size=15)
    text(key + "-space-label", x + 44, y + 214, "Space", 16, MUTED)
    ui.tabs(key + "-spaces", x + 108, y + 204,
            ["Guide", "Data", "Labeling", "Quality", "Delivery"], space,
            size=16, height=42, minimum=96)

    text(key + "-view-label", x + 44, y + 280, "View", 16, MUTED)
    if space == "Guide":
        tx = x + 108
        for index, label in enumerate(ui.GUIDE_VIEWS):
            if index == len(ui.INTRO_VIEWS):
                rect(key + "-view-group-rule", tx + 3, y + 278, 1, 26, RULE, RULE)
                tx += 26
            width = max(88, len(label) * 15 * .62 + 28)
            button(f"{key}-view-{index}", tx, y + 270,
                   width, 42, label, selected=label == view, size=15)
            tx += width + 8
    else:
        ui.tabs(key + "-views", x + 108, y + 270,
                ["Definition", "Rounds", "Guideline"], view,
                size=15, height=42, minimum=96)

    ui.line(key + "-navigation-rule", x + 44, y + 326, FW - 88)
    cx = x + 44
    text(key + "-view-title", cx, y + 344, title, 28)
    text(key + "-description", cx, y + 388, description, 16, MUTED)
    text(key + "-footer", cx, y + 884,
         "Labeling Workbench  /  b01_pilot  /  " + space + "  /  " + view, 14, MUTED)
    return cx, y + 424


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--previews", action="store_true")
    parser.add_argument("--font")
    parser.add_argument("--mono-font")
    args = parser.parse_args()
    content.shell = horizontal_shell
    content.CONTENT_W, content.MAIN_W = CONTENT_W, MAIN_W

    text("v3-title", 48, 20, "Workbench Shared · Guide v3", 34)
    text("v3-subtitle", 48, 75,
         "Space row above View row. Guide holds the shared content; the working area keeps the full available width.", 20, MUTED)
    text("v3-status", 48, 116, "Design proposal · illustrative content and states", 16, MUTED)
    x0, x1 = 48, 48 + FW + GAP
    y0, y1 = 176, 176 + FH + GAP
    for key, name, x, y, render in [
        ("v3-frame-skills", "01 · Guide / Skill set", x0, y0, content.skills),
        ("v3-frame-progress", "02 · Guide / Progress", x1, y0, content.progress),
        ("v3-frame-domain", "03 · Labeling / Definition", x0, y1, content.domain),
        ("v3-frame-studio", "04 · Guide / Studio", x1, y1, content.studio),
    ]:
        render(*ui.frame(key, name, x, y, FW, FH))
    scene = {"type": "excalidraw", "version": 2, "source": "haipipe-workbench-shared-guide-v3",
             "elements": ui.E, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}
    path = HERE / "workbench-shared-guide-v3.excalidraw"
    path.write_text(json.dumps(scene, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ui.write_svg(HERE / "workbench-shared-guide-v3.svg")
    if args.previews:
        ui.write_previews(HERE, args.font, args.mono_font, PREVIEWS)
    print(f"Wrote {path.name}: {len(ui.E)} elements, {len(ui.FRAMES)} frames")


if __name__ == "__main__":
    main()

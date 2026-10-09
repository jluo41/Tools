"""s32 · The console's element UI: every kind of element the In-Lab Console draws, one row each: its screenshot on the
synthetic fixtures, its computed style (shots/facts.json), and, where the toolkit's workbench frame has the same kind
of element, the frame's version beside it (from b01 j03 s32's shots), so one look can be judged (j02 Q04).
Redraw after `_build/shoot_console.py`; a person's marks are kept.

    python build_s32_console_element_ui.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
from console_draw import RED, TOOLS, Sheet, header, save  # noqa: E402

CHANGES = [("261009", "record chart: one lane per table, no table named (fix 6)"),
           ("261009", "dropped the Internal chart and the placeholder card: their views are hidden (Q05)"),
           ("261009", "added the refused tool call: the gate's no is shown, never a chip that looks run")]
FRAME_SHOTS = TOOLS / "blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s32-element-ui/shots"
# console element → the toolkit frame's element of the same kind (shots of b01 j03 s32), with what they share
COUNTERPART = {"topbar": ("tabs__frame.png", "the frame's level row and Spaces row"),
               "nav-rail": ("tabs__frame.png", "the frame's Spaces row (the console puts its Spaces in a rail)"),
               "tab-strip": ("views__paper.png", "the frame's view row (third row), as the paper theme draws it on the frame"),
               "source-table": ("table__paper.png", "the frame's light table"),
               "runs-table": ("runs__frame.png", "the frame's Runs panel")}
ORDER = ["topbar", "scope-toggle", "dataset-picker", "patient-picker", "haichat-toggle", "nav-rail", "tab-strip",
         "patient-card", "layer-banner", "source-table", "raw-file", "record-chart", "case-card",
         "model-list", "model-card", "run-bar", "forecast-chart", "runs-table", "checklist-bar",
         "annotate-start", "health-table", "drawer", "approval", "refused"]


def style(fx: dict) -> str:
    return "  ·  ".join(f"{k} {fx[k]}" for k in ("font", "radius", "padding", "fill", "tag") if fx.get(k))


def main():
    facts = json.loads((HERE / "shots" / "facts.json").read_text(encoding="utf-8"))
    s = Sheet()
    f = s.frame("1 · The console's element UI", 0, 0, 2000, 100)
    y = header(s, f, "s32 · The console's element UI: every element, as the console draws it",
               "One row per element, shot on the synthetic fixtures; its computed style under it; on the right, the toolkit\n"
               "frame's element of the same kind where there is one. The console's look is Databricks/Mattermost; the frame's\n"
               "is its own: Q04 asks whether they should share one.", CHANGES)
    s.text(40, y, "element", 18, f)
    s.text(1000, y, "the toolkit frame's counterpart", 18, f)
    y += 36
    for key in ORDER:
        fx = facts.get(key)
        s.line(40, y - 10, 1960, y - 10, f)
        if not fx or fx.get("missing"):
            s.text(40, y, f"{key}: ? not shot", 18, f, RED)
            y += 50
            continue
        s.text(40, y, fx.get("label", key), 18, f)
        h = s.image(HERE / "shots" / f"{key}.png", 40, y + 30, 900, f, px=1100)
        s.text(40, y + 36 + h, style(fx) + ("  ·  cut at 700 px" if fx.get("cut") else ""), 13, f)
        right = 0
        if key in COUNTERPART:
            shot, why = COUNTERPART[key]
            s.text(1000, y, why, 16, f)
            right = s.image(FRAME_SHOTS / shot, 1000, y + 30, 900, f, px=1100) or 0
            if not right:
                s.text(1000, y + 30, f"? {shot} not found in b01 j03 s32's shots", 14, f, RED)
        y += 30 + max(h + 30, right) + 50
    status = facts.get("_approval", "")
    if status != "shot":
        s.text(40, y, f"? the approval card: {status}", 16, f, RED)
        y += 40
    save(s, f, y, HERE / "s32-console-element-ui.excalidraw", "build_s32_console_element_ui.py")


if __name__ == "__main__":
    main()

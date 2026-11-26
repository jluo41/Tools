"""s01 · Data-use plan rounds: s01-data-use-plan-rounds.excalidraw, drawn by this builder.

How it looks and reads: /excalidraw-studio, its principles and scripts/draw.py (frames, a map, the key point,
the density badge, acts). The topic, its face and sessions: /haipipe-studio. A rebuild keeps whatever a person drew
on the canvas (canvas.write, a seed snapshot beside the drawing). Check it: excalidraw-studio's scripts/check.py.

    python build_s01_data_use_plan_rounds.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../../../../../plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts").resolve()))
from draw import Drawing, canvas  # noqa: E402  (excalidraw-studio's helpers; canvas.write keeps a person's marks)

# every change to this drawing: (date YYMMDD, what changed). Each gets a green note where it changed
# (canvas.change_note beside the changed thing) and a line in the title frame (JL 261007)
CHANGES = []


def main():
    out = HERE / "s01-data-use-plan-rounds.excalidraw"
    d = Drawing()
    f1 = d.frame("① Data-use plan rounds")                                    # one idea, one screen-sized frame
    d.heading("s01 · Data-use plan rounds", "one document, round by round")
    d.key(40, 196, 1400, 140)                                     # the frame's key point, the one slight colour
    d.para(64, 220, "Two rounds done; the retention period waits on a person before v3.", 1350, 30)
    d.flow([{"title": "v1 · 2026-10-27", "lines": []},                     # each round a box, its date in the title
            {"title": "Six comments · 2026-10-30", "lines": []},
            {"title": "v2 · 2026-11-04", "lines": []},
            {"title": "? Retention period", "lines": []},
            {"title": "v3 · after the pick", "lines": []}],
           40, 400, 2480, labels=["draws", "answered in", "leaves open", "settles"])
    for i, (date, what) in enumerate(CHANGES):                    # the title frame's list of changes
        e = canvas.change_note(1480, 220 + i * 26, what, date, f1["id"])
        e["id"] = f"c{i}"
        d.els.append(e)
    d.badge(f1)                                                   # its density, measured
    d.acts([{"name": "Act 1 · from v1 to the choice before v3", "frames": [f1["id"]]}])
    d.write(out, "build_s01_data_use_plan_rounds.py")


if __name__ == "__main__":
    main()

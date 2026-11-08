"""s01 · Example design flow: s01-example-design-flow.excalidraw, drawn by this builder.

How it looks and reads: /excalidraw-studio, its principles and scripts/draw.py (frames, a map, the key point,
the density badge, acts). The topic, its face and sessions: /haipipe-studio. A rebuild keeps whatever a person drew
on the canvas (canvas.write, a seed snapshot beside the drawing). Check it: excalidraw-studio's scripts/check.py.

    python build_s01_example_design_flow.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../../../plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts").resolve()))
from draw import Drawing, canvas  # noqa: E402  (excalidraw-studio's helpers; canvas.write keeps a person's marks)

# every change to this drawing: (date YYMMDD, what changed). Each gets a green note where it changed
# (canvas.change_note beside the changed thing) and a line in the title frame (JL 261007)
CHANGES = []


def main():
    out = HERE / "s01-example-design-flow.excalidraw"
    d = Drawing()
    f1 = d.frame("① Example design flow")                                    # one idea, one screen-sized frame
    d.heading("s01 · Example design flow", "one goal, one method version, one inputs version: six ideas in, one design kept")
    d.key(40, 196, 1400, 140)                                     # the frame's key point, the one slight colour
    d.para(64, 220, "Six placeholder ideas became six designs; another agent checked and ranked them; one is kept and waits for a person's release.", 1350, 30)
    d.flow([{"title": "Goal G01 · signed", "lines": ["confirm by reply", "sms · N = 1", "✅ 261106"]},
            {"title": "M01 m2 · goal only", "lines": ["sees the goal and the shared rules", "reading-note.md fenced out"]},
            {"title": "t00 · six ideas", "lines": ["three topics", "one from own knowledge"]},
            {"title": "d01 to d06 · drafts", "lines": ["one Task each", "verified by another agent"]},
            {"title": "t99 · rank, keep 1", "lines": ["a predicted effect each", "five dropped, kept folded"]},
            {"title": "? Release waits on a person", "lines": ["one sign freezes and releases"]}],
           40, 400, 2480, labels=["pins", "reasons", "opens", "checks", "hands to"])
    for i, (date, what) in enumerate(CHANGES):                    # the title frame's list of changes
        e = canvas.change_note(1480, 220 + i * 26, what, date, f1["id"])
        e["id"] = f"c{i}"
        d.els.append(e)
    d.badge(f1)                                                   # its density, measured
    d.acts([{"name": "Act 1 · from a signed goal to a waiting release", "frames": [f1["id"]]}])
    d.write(out, "build_s01_example_design_flow.py")


if __name__ == "__main__":
    main()

"""s02 · Release choices: s02-release-choices.excalidraw, drawn by this builder.

How it looks and reads: /excalidraw-studio, its principles and scripts/draw.py (frames, a map, the key point,
the density badge, acts). The topic, its face and sessions: /haipipe-studio. A rebuild keeps whatever a person drew
on the canvas (canvas.write, a seed snapshot beside the drawing). Check it: excalidraw-studio's scripts/check.py.

    python build_s02_release_choices.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../../../../plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts").resolve()))
from draw import Drawing, canvas  # noqa: E402  (excalidraw-studio's helpers; canvas.write keeps a person's marks)

# every change to this drawing: (date YYMMDD, what changed). Each gets a green note where it changed
# (canvas.change_note beside the changed thing) and a line in the title frame (JL 261007)
CHANGES = []


def main():
    out = HERE / "s02-release-choices.excalidraw"
    d = Drawing()
    f1 = d.frame("① Release choices")                                    # one idea, one screen-sized frame
    d.heading("s02 · Release choices", "what a person decides at j03's release, and what was decided already")
    d.key(40, 196, 1400, 140)
    d.para(64, 220, "Two designs from two past designs; one kept by the reviewer's rank. The release waits for one sign: it freezes the prediction and hands the design over.", 1350, 30)
    d.flow([{"title": "P1 · P2 · past designs", "lines": ["e01's results", "synthetic"]},
            {"title": "d01 · d02 · drafts", "lines": ["d02 failed v1, revised", "v2 passed"]},
            {"title": "t99 · rank, keep 1", "lines": ["a predicted effect each"]},
            {"title": "? Release: one sign", "lines": ["waits on a person"]},
            {"title": "? Next test: which arm", "lines": ["the 🙋 form on this topic"]}],
           40, 400, 2480, labels=["adapted into", "ranked by", "kept goes to", "then"])
    for i, (date, what) in enumerate(CHANGES):                    # the title frame's list of changes
        e = canvas.change_note(1480, 220 + i * 26, what, date, f1["id"])
        e["id"] = f"c{i}"
        d.els.append(e)
    d.badge(f1)                                                   # its density, measured
    d.acts([{"name": "Act 1 · the release and the next test", "frames": [f1["id"]]}])
    d.write(out, "build_s02_release_choices.py")


if __name__ == "__main__":
    main()

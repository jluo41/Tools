"""s05 · Design method ladder: s05-design-method-ladder.excalidraw, drawn by this builder.

How it looks and reads: /excalidraw-studio, its principles and scripts/draw.py (frames, a map, the key point,
the density badge, acts). The topic, its face and sessions: /haipipe-studio. A rebuild keeps whatever a person drew
on the canvas (canvas.write, a seed snapshot beside the drawing). Check it: excalidraw-studio's scripts/check.py.

    python build_s05_design_method_ladder.py
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
    out = HERE / "s05-design-method-ladder.excalidraw"
    d = Drawing()

    f1 = d.frame("① Today a method is a file")
    d.heading("Today a method is a file, not work you can watch",
              "A design Job pins one method version; the version itself is written by hand in the Tools skill (JL 261101)")
    d.key(40, 196, 1400, 140)
    d.para(64, 220, "No Job, Task or Run shows a method being written, tested or compared", 1350, 30)
    d.flow([{"title": "Written by hand", "lines": ["haipipe-design-method/methods/", "M05-raw-data-agent/m3.md",
                                                   "aggregate_query.py beside it"]},
            {"title": "A proposal, no Job", "lines": ["run-propose-method-<slug>", "at a design Board", "a file edited after"]},
            {"title": "Pinned by a Board Job", "lines": ["j06_review-new-rx_raw-data-agent", "pins M05 m3 by path + hash"]},
            {"title": "❓ where is it benched and compared?", "lines": ["❓ the Methods view can only name it"]}],
           40, 400, 2480, title=34, leaf=28, labels=["then", "then", ""])

    f2 = d.frame("② Each version is a Job you try")
    d.heading("A method Block: each version is a Job you try",
              "As insight's Prototype (one Job per release), drawn in s04 on 261007 and never built")
    d.key(40, 196, 1400, 140)
    d.para(64, 220, "work/Method-bNN-<app>/ · one Job per version, jNN_<method>_m<k>", 1350, 30)
    d.flow([{"title": "t01 Write the recipe", "lines": ["the five steps' prompts", "what ① may read, its tools"]},
            {"title": "t02 Build its checks", "lines": ["T0 rules · T1 sources", "T2 critique · T3 pretest"]},
            {"title": "t03 Bench it", "lines": ["bench/: fixed goals + inputs", "→ N designs"]},
            {"title": "t04 Compare", "lines": ["another agent", "against m<k-1> and siblings"]},
            {"title": "t05 Release 🙋", "lines": ["a person signs; frozen", "a Board Job pins it"], "key": True}],
           40, 400, 2480, title=34, leaf=28, labels=["then", "then", "then", "then"])
    d.para(40, 760, "proposals/: the backlog, from Board Jobs and Exp scores · the generic method stays in the Tools skill", 2400, 30)

    f3 = d.frame("③ The loop, M05 as the example")
    d.heading("The loop: a Board's results become the next version",
              "M05 raw-data agent")
    d.key(40, 196, 1400, 140)
    d.para(64, 220, "Each version came from what the one before could not do", 1350, 30)
    d.flow([{"title": "M05 m1", "lines": ["aggregate tables"]},
            {"title": "M05 m2", "lines": ["no tool: held (j05)"]},
            {"title": "M05 m3", "lines": ["aggregate_query.py", "j06: your review"]},
            {"title": "❓ M05 m4", "lines": ["❓ from j06 and the Exp"]}],
           40, 400, 2480, title=34, leaf=28, labels=["a proposal", "a proposal", "Exp scores"])

    for i, (date, what) in enumerate(CHANGES):                    # the title frame's list of changes
        e = canvas.change_note(1480, 220 + i * 26, what, date, f1["id"])
        e["id"] = f"c{i}"
        d.els.append(e)
    for f in (f1, f2, f3):
        d.badge(f)
    d.acts([{"name": "Act 1 · the gap", "frames": [f1["id"]]},
            {"name": "Act 2 · the method ladder", "frames": [f2["id"], f3["id"]], "arrow": ["its results come back"]}],
           between=[(f1["id"], f2["id"], "so")])
    d.write(out, "build_s05_design_method_ladder.py")


if __name__ == "__main__":
    main()

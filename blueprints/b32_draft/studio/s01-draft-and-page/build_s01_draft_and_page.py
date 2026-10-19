"""s01 · Draft and Page: s01-draft-and-page.excalidraw, drawn by this builder (haipipe-studio).

A rebuild keeps whatever a person drew on the canvas (canvas.write, a seed snapshot beside the drawing).

    python build_s01_draft_and_page.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts").resolve()))
import canvas  # noqa: E402  (haipipe-studio's merge-safe writer)

INK, RED = canvas.INK, canvas.RED      # the studio look: black; red for an open question; green notes
els = []
# every change to this drawing: (date YYMMDD, what changed). Each gets a green note where it changed
# (canvas.change_note beside the changed thing) and a line in the title frame (JL 261007)
CHANGES = []


def el(kind, x, y, w, h, **extra):
    e = {"id": f"e{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
          "strokeColor": INK, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1,
          "strokeStyle": "solid", "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
          "roundness": None, "seed": 1, "version": 1, "versionNonce": 1, "isDeleted": False,
          "boundElements": [], "updated": 1, "link": None, "locked": False}
    e.update(extra)
    els.append(e)
    return e


def text(x, y, s, size=22, frame=None, color=INK, font=6):
    lines = s.split("\n")
    return el("text", x, y, max(len(l) for l in lines) * size * 0.55, len(lines) * size * 1.25, text=s,
              originalText=s, fontSize=size, fontFamily=font, textAlign="left", verticalAlign="top",  # 6 Nunito, 3 Cascadia
              containerId=None, autoResize=True, lineHeight=1.25, frameId=frame, strokeColor=color)


def box(x, y, w, h, title, body, frame, size=22):
    el("rectangle", x, y, w, h, frameId=frame, strokeWidth=2)
    text(x + 20, y + 14, title, 24, frame)
    if body:
        text(x + 20, y + 52, body, size, frame)


def arrow(x1, y1, x2, y2, frame, label=None):
    el("arrow", x1, y1, x2 - x1, y2 - y1, frameId=frame, strokeWidth=2, points=[[0, 0], [x2 - x1, y2 - y1]],
       lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=None, endArrowhead="arrow")
    if label:
        text(min(x1, x2) + 6, min(y1, y2) - 62, label, 20, frame)


def main():
    out = HERE / "s01-draft-and-page.excalidraw"
    els.clear()
    f = el("frame", 0, 0, 2500, 1420, name="1 · Draft and Page")["id"]
    text(40, 28, "The draft is the work; the Page is what a reader opens (JL 261011)", 34, f)

    # the flow: one folder -> its draft -> the face -> the built output
    box(40, 300, 420, 230, "one folder, any level",
        "tNN_<task>/ or reports/qNN_<topic>/\nholds its face <stem>.md,\nruns/, and draft/ when it writes", f)
    arrow(460, 415, 540, 415, f)

    el("rectangle", 540, 120, 620, 680, frameId=f, strokeWidth=2)
    text(560, 132, "draft/ · the draft, the work", 26, f)
    box(570, 190, 560, 180, "logic",
        "<stem>-draft-v<N>.md  ## 1 · Structure\none Bullet per point, with its Role", f)
    box(570, 395, 560, 180, "sentences",
        "## 3 · Draft: one line per Bullet\naddress C1.P1.S1 (haipipe-sentence)", f)
    box(570, 600, 560, 180, "evidence",
        "<stem>-evidence-items.md\nE01 CITE · VALUE · DISPLAY -> a Result", f)
    text(570, 820, "? ## 3 is named Draft inside -draft-v<N>.md inside draft/:\n   rename it ## 3 · Sentences?", 22, f, RED)

    arrow(1130, 485, 1300, 415, f)
    text(1150, 500, "page.py adopt:\n§3 -> Content", 20, f)
    text(1300, 150, "the Page = the face + its built output", 26, f)
    box(1300, 300, 500, 230, "<stem>.md · the face",
        "Opening · Content · Aims\nContent is a copy of §3\nonly Opening and Aims are its own", f)
    text(1300, 550, "? adopt refuses a freshly set-up Page\n   (its Content is still empty)", 22, f, RED)
    arrow(1800, 415, 1900, 415, f, "page.py\nexport")
    box(1900, 300, 560, 230, "the Block's delivery/",
        "<Block>/delivery/<jNN>/<tNN>/<lane>/\nweb · latex · word\nrebuilt by run-delivery-<lane>", f)

    # who holds a draft, counted in WellDoc
    el("rectangle", 40, 930, 1100, 450, frameId=f, strokeWidth=2)
    text(60, 944, "Who holds a draft (WellDoc examples-*, 261011)", 26, f)
    text(60, 996, "compute Task      face, no draft/      854\n"
                  "work Task         face + draft/         41\n"
                  "discovery Task    face + draft/         55\n"
                  "paper Section     face + draft/          6\n"
                  "report qNN        face + draft/     6 of 72\n"
                  "Block or Job root never a draft/         0", 22, f, font=3)
    text(60, 1180, "-> a Task may hold a draft; a Task is not a Page (b10 s01-D36)", 22, f)
    text(60, 1230, "? 5 drafts sit inside SHIFT studio topics: stay there,\n   or become a Task or a report once the text is sent?", 22, f, RED)

    # the rename
    el("rectangle", 1240, 930, 1220, 450, frameId=f, strokeWidth=2)
    text(1260, 944, "The rename (option A, JL 261011)", 26, f)
    text(1260, 996, "haipipe-page            -> haipipe-draft (alias /haipipe-page)\n"
                    "haipipe-page-workflow   -> haipipe-draft-workflow\n"
                    "haipipe-page-<run>  x8  -> haipipe-draft-<run>\n"
                    "haipipe-page-*-agent x8 -> haipipe-draft-*-agent\n"
                    "kept: the Page server · haipipe-page-task\n"
                    "      haipipe-page-insight · .haipipe-page-export", 22, f, font=3)
    text(1260, 1180, "? remove the haipipe-page link once REACH, Physician and\n"
                     "   DrFirst Projects are swept (they work through it today)", 22, f, RED)

    for i, (date, what) in enumerate(CHANGES):          # the title frame's list of changes
        els.append(canvas.change_note(40, 80 + i * 26, what, date, f))
    for e in canvas.off_palette(els):                    # the look: black, red, green only
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, els, "build_s01_draft_and_page.py")


if __name__ == "__main__":
    main()

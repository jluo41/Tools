"""s05 · Paper Report: research questions and review rounds: s05-paper-report.excalidraw, drawn by this builder (haipipe-studio).

One frame: where this view sits in a paper Board, what b10 already decided for every Block, and what paper
still has to settle (red). Made in the b16 reorganization (261011, JL: "you just propose it").

    python build_s05_paper_report.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts").resolve()))
import canvas  # noqa: E402  (haipipe-studio's merge-safe writer)

INK, RED = canvas.INK, canvas.RED
TITLE = 's05 · Paper Report: research questions and review rounds'
TOPIC = "the paper's reports at every level (b10 s09-D02): the Board's research questions (board.md ## Questions, s01-D08) each with a report; a version Job's standing questions every send answers (haipipe-paper-workflow) and its comments and review rounds (haipipe-paper-comments); a Section's own questions. This topic settles where a review round and its answers live, and what each paper level must report."
DISK = ['<paper Board>/reports/qNN_<question>/   a research question', '<version Job>/reports/qNN_<topic>/      standing questions, a round', "<Section Task>/reports/qNN_<topic>/     a Section's own"]
B10 = ['b10 s05: every level writes its own Report', 'b10 s01 (s09 Later 1): the centre says what each level reports',
       'b10 s05 (proposed): the Report gets a group bar; the paper keeps', '  Ideation · Narrative · Research questions · Random thoughts']
PROPOSED = ['s05-D01 · a Question\'s group: is its kind; its telling is', '  the telling\'s Feeds: line, read by id (b10 s05 Open 14)',
            's05-D02 · b16 keeps the paper\'s groups and its standing', '  Questions (3 attract rows, J1 to J5); b10 the rule']
OPEN = ['A review round: a report in the version Job, or Tasks in the same Job? (Q03)', 'A resubmission elsewhere: a new version Job with its own reports?', "Section › Comments: the comments report's concern table as it is, or a ## Review Items table? (was s33 open 2)", 'What a Section must report (the Board and the version: s05-D02)', 'RQ0 to RQ6 and Q00 to Q06 are the same Questions: show one name?']
CHANGES = []
els = []


def el(kind, x, y, w, h, **extra):
    e = {"id": f"e{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
          "strokeColor": INK, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1.5,
          "strokeStyle": "solid", "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
          "roundness": None, "seed": 1, "version": 1, "versionNonce": 1, "isDeleted": False,
          "boundElements": [], "updated": 1, "link": None, "locked": False}
    e.update(extra)
    els.append(e)
    return e


def text(x, y, s, size, frame, color=INK, font=6):
    lines = s.split("\n")
    return el("text", x, y, max(len(l) for l in lines) * size * (0.6 if font == 3 else 0.55), len(lines) * size * 1.3,
              text=s, originalText=s, fontSize=size, fontFamily=font, textAlign="left", verticalAlign="top",
              containerId=None, autoResize=True, lineHeight=1.3, frameId=frame, strokeColor=color)


def wrap(s, n=110):
    out, line = [], ""
    for w in s.split():
        if len(line) + len(w) + 1 > n:
            out.append(line); line = w
        else:
            line = (line + " " + w).strip()
    return "\n".join(out + [line])


def main():
    els.clear()
    f = el("frame", 0, 0, 2400, 1300, name="1 · " + TITLE.split(" · ", 1)[1])["id"]
    text(60, 50, TITLE, 36, f)
    for i, (date, what) in enumerate(CHANGES):
        els.append(canvas.change_note(60, 104 + i * 24, what, date, f))
    text(60, 150, wrap(TOPIC), 21, f)
    text(60, 470, "ON DISK", 24, f)
    el("rectangle", 60, 510, 1100, 300, frameId=f)
    text(84, 534, "\n".join(DISK), 20, f, font=3)
    text(1260, 470, "FROM b10 (every Block)", 24, f)
    el("rectangle", 1260, 510, 1080, 300, frameId=f)
    text(1284, 534, "\n".join(B10), 21, f)
    text(60, 870, "OPEN", 24, f, RED)
    text(60, 912, "\n".join("? " + wrap(o, 150) for o in OPEN), 21, f, RED)
    text(1260, 870, "PROPOSED (b16, JL to agree)", 24, f)
    text(1260, 912, "\n".join(PROPOSED), 21, f)
    canvas.write(HERE / 's05-paper-report.excalidraw', els, 'build_s05_paper_report.py')


if __name__ == "__main__":
    main()

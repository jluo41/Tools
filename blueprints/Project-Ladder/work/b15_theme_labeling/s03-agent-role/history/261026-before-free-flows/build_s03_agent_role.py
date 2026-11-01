"""Render the unified annotation concept from the face; preserve human marks."""
import re
import sys
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts").resolve()))
from draw import Drawing, RED, canvas


def main():
    face = (HERE / "s03-agent-role.md").read_text(encoding="utf-8")
    w = yaml.safe_load(re.search(r"(?ms)^```yaml\n(.*?)^```", face).group(1))
    d = Drawing()
    f = d.frame(w["title"], 2800, 1600)
    d.text(40, 30, w["title"], 60)
    d.text(42, 112, w["subtitle"], 30)
    d.key(40, 180, 2720, 125)
    d.para(66, 208, w["key"], 2660, 38)
    d.text(40, 330, w["problem"], 32)

    def node(key, x, y, width, height):
        d.box(x, y, width, height, sw=2.5)
        yy = d.para(x + 24, y + 22, w[key]["title"], width - 48, 38) + 25
        for line in w[key]["lines"]:
            yy = d.para(x + 24, yy, line, width - 48, 30) + 16

    node("start", 40, 460, 480, 250)
    node("existing", 40, 865, 480, 250)
    node("agent", 650, 460, 700, 340)
    node("human", 650, 1050, 700, 300)
    node("guideline", 1460, 460, 550, 340)
    node("execute", 2120, 460, 640, 340)
    node("delivery", 1460, 1050, 1300, 300)
    d.line([(520, 590), (650, 590)], sw=3)
    d.line([(520, 980), (575, 980), (575, 720), (650, 720)], sw=3)
    d.line([(1350, 620), (1460, 620)], sw=3)
    d.line([(2010, 620), (2120, 620)], sw=3)
    d.line([(820, 800), (820, 1050)], sw=3)
    d.para(665, 865, w["ask"], 145, 28)
    d.line([(1200, 1050), (1200, 800)], sw=3)
    d.para(1215, 865, w["decision"], 195, 28)
    d.line([(1700, 800), (1700, 950), (1350, 950), (1350, 800)], sw=2, dashed=True)
    d.text(1450, 975, w["meaning"], 28)
    d.line([(2430, 460), (2430, 405), (1740, 405), (1740, 460)], sw=2, dashed=True)
    d.text(1900, 363, w["wording"], 28)
    d.line([(2440, 800), (2440, 1050)], sw=3)
    d.text(2465, 910, w["audit"], 30)
    d.line([(1460, 1200), (1350, 1200)], sw=3)
    d.text(40, 1430, w["foot"], 32)
    d.text(40, 1505, w["open"], 30, RED)
    note = canvas.change_note(650, 1370, w["change"], "261026", f["id"])
    note["id"] = "change-unified-entries"
    d.els.append(note)
    d.badge(f)
    d.write(HERE / "s03-agent-role.excalidraw", Path(__file__).name)


if __name__ == "__main__":
    main()

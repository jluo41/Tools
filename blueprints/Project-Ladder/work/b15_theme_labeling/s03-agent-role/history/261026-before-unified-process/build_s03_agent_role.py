"""Render s03 from its face; canvas.write preserves human marks."""
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts").resolve()))
from draw import Drawing, RED


def main():
    face = (HERE / "s03-agent-role.md").read_text(encoding="utf-8")
    words = yaml.safe_load(re.search(r"(?ms)^```yaml\n(.*?)^```", face).group(1))
    d = Drawing()
    frame = d.frame(words["title"], 2560, 1440)
    d.text(40, 28, words["title"], 60)
    d.text(42, 112, words["subtitle"], 30)
    d.key(40, 180, 2480, 118)
    d.para(66, 205, words["key"], 2420, 38)

    def node(key, x, y, w, h):
        d.box(x, y, w, h, sw=2.5)
        d.text(x + 22, y + 22, words[key]["title"], 38)
        yy = y + 88
        for line in words[key]["body"].split("\\n"):
            yy = d.para(x + 22, yy, line, w - 44, 30) + 14

    node("human", 40, 420, 370, 240)
    node("corpus", 40, 770, 370, 250)
    node("meaning", 490, 420, 650, 370)
    node("expression", 1240, 420, 650, 370)
    node("outputs", 1980, 420, 540, 370)
    d.line([(410, 530), (490, 530)], sw=3)
    d.line([(490, 600), (410, 600)], sw=3)
    d.line([(410, 890), (460, 890), (460, 740), (490, 740)], sw=3)
    d.line([(1140, 565), (1240, 565)], sw=3)
    d.line([(1890, 565), (1980, 565)], sw=3)
    for key, x in [("meaning", 490), ("expression", 1240)]:
        d.line([(x + 550, 790), (x + 550, 885), (x + 100, 885), (x + 100, 790)], sw=2.5)
        d.text(x + 90, 914, words[key]["loop"], 30)
    d.line([(1565, 420), (1565, 325), (815, 325), (815, 420)], sw=2, dashed=True)
    d.text(1510, 354, words["return"], 28)
    d.box(490, 1030, 2030, 166, sw=2)
    d.text(514, 1048, words["harness"]["title"], 38)
    d.para(514, 1110, words["harness"]["body"], 1970, 30)
    d.line([(815, 1030), (815, 980)], sw=2)
    d.line([(1565, 1030), (1565, 980)], sw=2)
    d.text(40, 1230, words["objective"], 32)
    d.text(40, 1280, words["rationale"], 30)
    d.text(40, 1340, words["open"], 30, RED)
    d.text(40, 1385, words["unproven"], 28, RED)
    d.badge(frame)
    d.write(HERE / "s03-agent-role.excalidraw", Path(__file__).name)


if __name__ == "__main__":
    main()

"""Three native, frame-free flowcharts; user request 261026.

Words live in the face. Small node groups can move independently. No outer frame,
container rectangle, rasterized content or whole-chart group. Source edits regenerate
through canvas.write while preserving human marks. IDs are stable ordinals, not hashes.
"""
import json
import re
import sys
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts").resolve()))
from draw import Drawing, RED, canvas


def keep_ids(elements):
    """Explicit IDs are already unique and contain no content hashes."""
    return elements


def build(w):
    d = Drawing()
    d.text(45, 30, w["title"], 62)
    d.text(48, 122, w["subtitle"], 29)
    d.text(48, 192, w["takeaway"], 36)
    d.line([(48, 248), (590, 248)], color="#fff3bf", arrow=False, sw=12)

    def node(key, x, y):
        start = len(d.els)
        v = w["nodes"][key]
        d.text(x, y, v["icon"], 78)
        yy = d.para(x, y + 110, v["title"], 480, 36) + 18
        for line in v["body"].split("\\n"):
            yy = d.para(x, yy, line, 480, 28) + 8
        for i, e in enumerate(d.els[start:]):
            e["id"] = f"s-{w['file']}-{key}-{i}"
            e["groupIds"] = [f"node-{key}"]

    node("idea", 60, 355)
    node("agent", 680, 355)
    node("human", 1300, 355)
    node("source", 60, 850)
    node("result", 680, 850)
    node("guide", 1300, 850)

    def arrow(points, label, x, y, dashed=False):
        e=d.line(points, dashed=dashed, sw=2.5)
        e["roundness"]={"type":2}
        e["roughness"]=1
        d.text(x, y, w["arrows"][label], 26)

    arrow([(470, 440), (640, 440)], "input", 485, 390)
    arrow([(1090, 440), (1260, 440)], "ask", 1130, 390)
    arrow([(1510, 650), (1510, 810)], "approve", 1540, 705)
    arrow([(1260, 960), (1170, 960)], "apply", 1090, 900)
    # The near-center return path avoids all node text and keeps the loop compact.
    arrow([(1320, 810), (1210, 730), (910, 730), (910, 650)], "loop", 995, 680, True)
    if w["file"] == "s03-agent-role":
        arrow([(400, 845), (530, 710), (650, 650)], "source", 440, 760)
    elif '.2-' in w["file"]:
        arrow([(400, 845), (530, 710), (650, 650)], "source", 440, 760, True)
    else:
        arrow([(400, 845), (530, 710), (650, 650)], "source", 410, 760, True)
    d.text(60, 1220, w["note"], 28, RED if '.2-' in w['file'] or '.3-' in w['file'] else '#1e1e1e')

    for i, e in enumerate(d.els):
        if not e['id'].startswith('s-'):
            e['id']=f"s-{w['file']}-flow-{i}"
    canvas.assign_ids=keep_ids
    out=HERE/(w['file']+'.excalidraw')
    d.write(out, Path(__file__).name)
    scene=json.loads(out.read_text())
    els=[e for e in scene['elements'] if not e.get('isDeleted')]
    assert not any(e['type']=='frame' or e.get('frameId') for e in els), 'Outer frame survived'
    assert not any(e['type']=='image' for e in els), 'Use native editable elements'
    assert len({e['id'] for e in els})==len(els)
    print(f"Verified {out.name}: {len(els)} native elements, no frame, separate node groups")


def main():
    face=(HERE/'s03-agent-role.md').read_text()
    words=yaml.safe_load(re.search(r'(?ms)^```yaml\n(.*?)^```',face).group(1))
    for w in words['flows']:
        build(w)


if __name__=='__main__':
    main()

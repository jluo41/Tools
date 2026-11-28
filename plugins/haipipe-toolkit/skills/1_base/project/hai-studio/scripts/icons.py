"""Pictures of real things for a Studio Design (CONSTITUTION A04: "Design is drawn as pictures"): a computer, a laptop,
a phone, a server, a database, a cloud, a shield, a gate, a lock, a person, a hospital, a document, a big cross and
a big number. Each draws at (x, y),
is lit by its state, and returns a list of elements. Moved here on 261119 from b01_livesync s01's sketch so every
topic can use them, not only that one.

    from icons import monitor, laptop, phone, server, cylinder, cloud, shield, gate, lock, cross, big_number
    els += server("b_app", x, y, "bad")         # state: "ok" green, "wait" orange, "bad" red, "off" grey

Count of picture shapes in a Design: `picture_count(els)`; five_parts.build warns under PICTURES_MIN.

The gallery (every icon in every state, and an Excalidraw library to drag them in by hand):
    python icons.py --gallery         writes ../ref/icons/icons.excalidraw, icons.png, own-icons.excalidrawlib
A new icon: add a function here and a row in GALLERY, then rerun --gallery.
"""
from five_parts import GR, OR, RE, PU, SEM, ROOM, GHOST, INK, poly, _el, text  # noqa: F401
from quick_draw import line

PICTURES_MIN = 20                        # ellipses, lines and polygons a vivid Design has at least (A04)


def lit(state):
    """(stroke, fill) for a state: ok green, wait orange, bad red, off grey; a bool is ok or off."""
    if state is True:
        state = "ok"
    if state in (False, None):
        state = "off"
    return {"ok": (GR, SEM["end"][0]), "wait": (OR, SEM["start"][0]), "bad": (RE, SEM["warn"][0]),
            "cloud": (PU, SEM["agent"][0])}.get(state, (ROOM, GHOST))


def monitor(eid, x, y, state="ok"):
    c, f = lit(state)
    els = [_el("rectangle", eid, x, y, 170, 112, c, f, strokeWidth=3, roundness={"type": 3})]
    els += [_el("rectangle", eid + "_in", x + 12, y + 12, 146, 88, c, "#ffffff", strokeWidth=1)]
    els += poly(eid + "_st", [(x + 70, y + 112), (x + 100, y + 112), (x + 108, y + 140), (x + 62, y + 140)], c, f)
    return els + [_el("rectangle", eid + "_b", x + 40, y + 140, 90, 10, c, f)]


def laptop(eid, x, y, state="ok"):
    c, f = lit(state)
    els = [_el("rectangle", eid, x + 20, y, 150, 98, c, f, strokeWidth=3, roundness={"type": 3})]
    els += [_el("rectangle", eid + "_s", x + 30, y + 10, 130, 78, c, "#ffffff", strokeWidth=1)]
    return els + poly(eid + "_k", [(x + 20, y + 98), (x + 170, y + 98), (x + 190, y + 118), (x, y + 118)], c, f)


def phone(eid, x, y, state="ok"):
    c, f = lit(state)
    els = [_el("rectangle", eid, x, y, 76, 136, c, f, strokeWidth=3, roundness={"type": 3})]
    els += [_el("rectangle", eid + "_s", x + 8, y + 16, 60, 96, c, "#ffffff", strokeWidth=1)]
    return els + [_el("ellipse", eid + "_h", x + 30, y + 118, 14, 12, c, "#ffffff", strokeWidth=1)]


def server(eid, x, y, state="ok", w=130, h=150):
    """A rack: three drawers, each with a light."""
    c, f = lit(state)
    els = [_el("rectangle", eid, x, y, w, h, c, f, strokeWidth=3, roundness={"type": 3})]
    for k in range(3):
        yy = y + 14 + k * (h - 28) / 3
        els += [_el("rectangle", f"{eid}_d{k}", x + 12, yy, w - 24, (h - 28) / 3 - 8, c, "#ffffff", strokeWidth=1)]
        els += [_el("ellipse", f"{eid}_l{k}", x + w - 34, yy + 10, 12, 12, c, c, strokeWidth=1)]
    return els


def cylinder(eid, x, y, state="ok", w=150, h=150):
    c, f = lit(state)
    els = [_el("rectangle", eid, x, y + 20, w, h - 40, c, f, strokeWidth=3)]
    els += [_el("ellipse", eid + "_bt", x, y + h - 40, w, 40, c, f, strokeWidth=3)]
    els += [_el("rectangle", eid + "_mask", x + 3, y + h - 60, w - 6, 40, f, f, strokeWidth=0)]
    return els + [_el("ellipse", eid + "_tp", x, y, w, 40, c, "#ffffff", strokeWidth=3)]


def cloud(eid, x, y, state="cloud"):
    c, f = lit(state)
    els = []
    for k, (dx, dy, w, h) in enumerate(((0, 40, 110, 80), (60, 0, 120, 110), (150, 30, 110, 90), (40, 60, 180, 70))):
        els += [_el("ellipse", f"{eid}_{k}", x + dx, y + dy, w, h, c if k < 3 else f, f, strokeWidth=3 if k < 3 else 0)]
    return els


def shield(eid, x, y, state="ok", s=1.0):
    """A shield: a firewall (WAF)."""
    c, f = lit(state)
    pts = [(0, 0), (50, -14), (100, 0), (96, 60), (50, 110), (4, 60)]
    return poly(eid, [(x + px * s, y + 14 * s + py * s) for px, py in pts], c, f, width=3)


def gate(eid, x, y, state="ok"):
    """A gate: two posts and a bar, a router that only passes traffic on."""
    c, f = lit(state)
    els = [_el("rectangle", eid, x, y, 22, 120, c, f, strokeWidth=3)]
    els += [_el("rectangle", eid + "_r", x + 118, y, 22, 120, c, f, strokeWidth=3)]
    els += line(eid + "_bar", [(x + 22, y + 40), (x + 118, y + 40)], c, 4)
    return els + line(eid + "_bar2", [(x + 22, y + 80), (x + 118, y + 80)], c, 4)


def lock(eid, x, y, color=RE):
    els = [_el("rectangle", eid, x, y + 22, 44, 34, color, SEM["warn"][0], strokeWidth=3, roundness={"type": 3})]
    return els + line(eid + "_u", [(x + 8, y + 24), (x + 8, y + 8), (x + 22, y), (x + 36, y + 8), (x + 36, y + 24)],
                      color, 3)


def cross(eid, x, y, s=60, color=RE):
    """A big red X: where the path breaks."""
    return line(eid + "_1", [(x, y), (x + s, y + s)], color, 8) + line(eid + "_2", [(x + s, y), (x, y + s)], color, 8)


def big_number(eid, x, y, number, label, color=RE, size=56):
    """A big number with its label under it, centred on x."""
    return text(eid, x, y, str(number), size, color, "center") + text(eid + "_l", x, y + size * 1.2, label, 16, INK,
                                                                      "center")


def person(eid, x, y, state="ok", s=1.0):
    """A person: head, body, legs (from Physician b02 s02's sketch, 261119)."""
    c, f = lit(state)
    els = [_el("ellipse", eid + "_hd", x + 18 * s, y, 42 * s, 42 * s, c, "#fde7d5", strokeWidth=2)]
    els += [_el("rectangle", eid, x, y + 52 * s, 78 * s, 86 * s, c, f, strokeWidth=2, roundness={"type": 3})]
    return els + line(eid + "_lg", [(x + 17 * s, y + 140 * s), (x + 17 * s, y + 165 * s), (x + 63 * s, y + 165 * s),
                                    (x + 63 * s, y + 140 * s)], c, 2)


def hospital(eid, x, y, state="ok", w=220):
    """A hospital: roof, sign, windows, door (from Physician b02 s02's sketch, 261119)."""
    c, f = lit(state)
    els = [_el("rectangle", eid + "_rf", x - 12, y, w + 24, 35, c, f, strokeWidth=2)]
    els += [_el("rectangle", eid, x, y + 35, w, 140, c, "#ffffff", strokeWidth=2)]
    els += text(eid + "_sg", x + w / 2, y + 7, "✚ HOSPITAL", 18, c, "center")
    for j in range(3):
        els += [_el("rectangle", f"{eid}_w{j}", x + 18 + j * 50, y + 58, 34, 36, c, f, strokeWidth=1)]
    return els + [_el("rectangle", eid + "_dr", x + w - 66, y + 110, 48, 65, c, f, strokeWidth=2)]


def document(eid, x, y, state="ok", w=100, h=130):
    """A page with a folded corner and text lines: a file, an email, a report."""
    c, f = lit(state)
    els = poly(eid, [(x, y), (x + w - 26, y), (x + w, y + 26), (x + w, y + h), (x, y + h)], c, "#ffffff", width=3)
    els += poly(eid + "_fd", [(x + w - 26, y), (x + w - 26, y + 26), (x + w, y + 26)], c, f, width=2)
    for k in range(4):
        els += line(f"{eid}_t{k}", [(x + 14, y + 44 + k * 20), (x + w - 16 - (k == 3) * 30, y + 44 + k * 20)], c, 2)
    return els


GALLERY = [("phone", phone), ("laptop", laptop), ("monitor", monitor), ("server", server), ("cylinder", cylinder),
           ("cloud", cloud), ("shield", shield), ("gate", gate), ("person", person), ("hospital", hospital),
           ("document", document)]
STATES = ["ok", "wait", "bad", "off"]


def gallery(out_dir):
    """Every icon in every state as one drawing and its PNG, plus an .excalidrawlib (one library item per icon, ok)."""
    import json
    import subprocess
    import sys
    from pathlib import Path
    from quick_draw import write
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    els = text("g_t", 0, 0, "Studio icons (hai-studio/scripts/icons.py)", 30, INK)
    els += text("g_s", 0, 44, "state: ok green · wait orange · bad red · off grey;  "
                "use: from icons import <name>; els += <name>(eid, x, y, state)", 16, INK)
    for k, st in enumerate(STATES):
        els += text(f"g_h{k}", 260 + k * 300, 100, st, 20, lit(st)[0])
    lib = []
    for r, (name, fn) in enumerate(GALLERY):
        y = 150 + r * 240
        els += text(f"g_n{r}", 0, y + 60, name, 22, INK)
        for k, st in enumerate(STATES):
            part = fn(f"g_{name}_{st}", 220 + k * 300, y, st)
            els += part
            if st == "ok":
                lib.append({"id": f"hai-{name}", "status": "published", "created": 1, "name": name,
                            "elements": [dict(e, x=e["x"] - 220, y=e["y"] - y) for e in part]})
    y = 150 + len(GALLERY) * 240
    els += text("g_n_x", 0, y + 20, "cross", 22, INK) + cross("g_x", 220, y, 64)
    els += text("g_n_b", 520, y + 20, "big_number", 22, INK) + big_number("g_b", 820, y - 10, "2", "deploys failed")
    els += text("g_n_l", 1060, y + 20, "lock", 22, INK) + lock("g_l", 1160, y)
    pics = out_dir / "icons.excalidraw"
    print(write(pics, els))
    (out_dir / "own-icons.excalidrawlib").write_text(json.dumps({"type": "excalidrawlib", "version": 2,
                                                             "source": "hai-studio icons.py",
                                                             "libraryItems": lib}, indent=1), encoding="utf-8")
    subprocess.run([sys.executable, str(Path(__file__).with_name("render_png.py")), str(pics), str(out_dir / "icons.png"),
                    "1"], check=True)


def picture_count(els):
    """How many picture shapes (ellipses, lines, polygons; arrows not counted) the elements hold."""
    return sum(e["type"] in ("ellipse", "line", "freedraw") for e in els)


if __name__ == "__main__":
    import sys
    from pathlib import Path
    if "--gallery" in sys.argv:
        gallery(Path(__file__).resolve().parent.parent / "ref" / "icons")

#!/usr/bin/env python3
"""Assemble a master SVG from items.json + the per-icon SVGs.

Usage:
    compose_svg.py <items.json> <svg_dir> <out.svg> [--crops DIR]

Reads the inventory (items.json), nests each icon's hand-authored SVG at its bbox, embeds any
`keep_raster` icons as PNGs, paints panel/background rects, and emits a <text> element for every
label. The canvas is sized to the original figure (width/height in items.json).

  --crops DIR   folder of raster crops for keep_raster items (default: <items_dir>/crop_images)

Only Python stdlib is used (no cairosvg needed here; render_diff.py does the rasterizing).
The icons stay as inline, editable SVG shapes so the master remains fully editable.
"""
import argparse, base64, json, math, os, re

SVG_NS = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"


def esc_attr(s):
    return (str(s).replace("&", "&amp;").replace('"', "&quot;")
            .replace("<", "&lt;").replace(">", "&gt;"))


def esc_text(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def read_icon_svg(path):
    """Return (viewbox, inner_xml). viewbox falls back to width/height, then None."""
    text = open(path, encoding="utf-8").read()
    start = text.find("<svg")
    if start < 0:
        raise ValueError(f"no <svg> element in {path}")
    open_end = text.find(">", start)
    header = text[start:open_end]
    close = text.rfind("</svg>")
    inner = text[open_end + 1:close if close >= 0 else len(text)].strip()

    m = re.search(r'viewBox\s*=\s*"([^"]+)"', header)
    if m:
        return m.group(1), inner
    wm = re.search(r'\bwidth\s*=\s*"([\d.]+)', header)
    hm = re.search(r'\bheight\s*=\s*"([\d.]+)', header)
    if wm and hm:
        return f"0 0 {wm.group(1)} {hm.group(1)}", inner
    return None, inner


def icon_element(it, svg_dir, crops_dir):
    x, y, w, h = it["bbox"]
    preserve = it.get("preserve", "xMidYMid meet")
    if it.get("keep_raster"):
        png = os.path.join(crops_dir, it["id"] + ".png")
        if not os.path.exists(png):
            return f'  <!-- MISSING raster crop for {esc_attr(it["id"])} -->'
        b64 = base64.b64encode(open(png, "rb").read()).decode("ascii")
        return (f'  <image x="{x}" y="{y}" width="{w}" height="{h}" '
                f'preserveAspectRatio="{preserve}" '
                f'xlink:href="data:image/png;base64,{b64}"/>')
    svg_path = os.path.join(svg_dir, it["id"] + ".svg")
    if not os.path.exists(svg_path):
        return f'  <!-- MISSING svg for {esc_attr(it["id"])} ({esc_attr(svg_path)}) -->'
    viewbox, inner = read_icon_svg(svg_path)
    vb = f' viewBox="{esc_attr(viewbox)}"' if viewbox else ""
    return (f'  <svg x="{x}" y="{y}" width="{w}" height="{h}"{vb} '
            f'preserveAspectRatio="{preserve}" overflow="visible">\n'
            f'    {inner}\n  </svg>')


def connector_element(c):
    """Draw a figure-level primitive in source coordinates. Currently 'arrow' (also covers
    plain lines via heads:"none"). Handy for panel-to-panel arrows and dashed bias connectors
    that are simpler drawn on the master canvas than cropped and vectorized as icons.

    Fields: type("arrow"), x1,y1,x2,y2, color, width, dashed(bool), dash("7 5"),
            heads("end"|"both"|"none"), head_size, head_width.
    """
    if c.get("type", "arrow") != "arrow":
        return f'  <!-- unknown connector type {esc_attr(c.get("type"))} -->'
    x1, y1, x2, y2 = c["x1"], c["y1"], c["x2"], c["y2"]
    color = c.get("color", "#007D81")
    w = c.get("width", 3)
    heads = c.get("heads", "end")
    hs = c.get("head_size", w * 3 + 6)          # arrowhead length along the shaft
    hw = c.get("head_width", hs * 0.8)          # arrowhead base width
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L                     # shaft direction
    px, py = -uy, ux                            # perpendicular
    s1x, s1y, s2x, s2y = x1, y1, x2, y2         # shaft ends, pulled back under heads
    if heads in ("end", "both"):
        s2x, s2y = x2 - ux * hs, y2 - uy * hs
    if heads == "both":
        s1x, s1y = x1 + ux * hs, y1 + uy * hs
    dash = f' stroke-dasharray="{c.get("dash", "7 5")}"' if c.get("dashed") else ""
    out = [f'<line x1="{s1x:.1f}" y1="{s1y:.1f}" x2="{s2x:.1f}" y2="{s2y:.1f}" '
           f'stroke="{esc_attr(color)}" stroke-width="{w}"{dash} stroke-linecap="butt"/>']

    def head(tx, ty, dirx, diry):
        bx, by = tx - dirx * hs, ty - diry * hs
        lx, ly = bx + px * hw / 2, by + py * hw / 2
        rx, ry = bx - px * hw / 2, by - py * hw / 2
        return (f'<path d="M{tx:.1f} {ty:.1f} L{lx:.1f} {ly:.1f} L{rx:.1f} {ry:.1f} Z" '
                f'fill="{esc_attr(color)}"/>')

    if heads in ("end", "both"):
        out.append(head(x2, y2, ux, uy))
    if heads == "both":
        out.append(head(x1, y1, -ux, -uy))
    return "  " + "\n  ".join(out)


def text_element(it):
    x, y, w, h = it["bbox"]
    anchor = it.get("anchor", "start")
    tx = {"start": x, "middle": x + w / 2, "end": x + w}.get(anchor, x)
    size = it.get("font_size", 16)
    # bbox is the glyph box; place the baseline near its lower third.
    baseline = y + h * 0.5 + size * 0.35 if h else y + size
    weight = it.get("weight", "normal")
    color = it.get("color", "#000000")
    family = it.get("font_family", "Helvetica, Arial, sans-serif")
    lines = str(it.get("content", "")).split("\n")
    attrs = (f'x="{tx:.1f}" font-size="{size}" font-weight="{esc_attr(weight)}" '
             f'font-family="{esc_attr(family)}" fill="{esc_attr(color)}" '
             f'text-anchor="{esc_attr(anchor)}"')
    if len(lines) == 1:
        return f'  <text {attrs} y="{baseline:.1f}">{esc_text(lines[0])}</text>'
    spans = "".join(
        f'<tspan x="{tx:.1f}" dy="{0 if i == 0 else size * 1.2:.1f}">{esc_text(ln)}</tspan>'
        for i, ln in enumerate(lines))
    return f'  <text {attrs} y="{baseline:.1f}">{spans}</text>'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("items")
    ap.add_argument("svg_dir")
    ap.add_argument("out")
    ap.add_argument("--crops", default=None,
                    help="folder of raster crops for keep_raster items "
                         "(default: <items_dir>/crop_images)")
    a = ap.parse_args()

    data = json.load(open(a.items, encoding="utf-8"))
    W, H = data["width"], data["height"]
    crops_dir = a.crops or os.path.join(os.path.dirname(os.path.abspath(a.items)), "crop_images")

    out = [f'<svg xmlns="{SVG_NS}" xmlns:xlink="{XLINK}" '
           f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">']

    bg = data.get("background")
    if bg:
        out.append(f'  <rect x="0" y="0" width="{W}" height="{H}" fill="{esc_attr(bg)}"/>')

    for p in data.get("panels", []):
        x, y, w, h = p["bbox"]
        out.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" '
                   f'rx="{p.get("rx", 0)}" fill="{esc_attr(p.get("fill", "none"))}" '
                   f'stroke="{esc_attr(p.get("stroke", "none"))}" '
                   f'stroke-width="{p.get("stroke_width", 1)}"/>')

    connectors = data.get("connectors", [])
    for c in connectors:
        out.append(connector_element(c))

    n_icon = n_raster = n_text = n_missing = 0
    for it in data.get("items", []):
        t = it.get("type")
        if t == "icon":
            el = icon_element(it, a.svg_dir, crops_dir)
            if "MISSING" in el:
                n_missing += 1
            elif it.get("keep_raster"):
                n_raster += 1
            else:
                n_icon += 1
            out.append(el)
        elif t == "text":
            out.append(text_element(it))
            n_text += 1

    out.append("</svg>\n")
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"wrote {a.out}  ({W}x{H})  "
          f"icons={n_icon} raster={n_raster} text={n_text} panels={len(data.get('panels', []))}"
          + (f"  MISSING={n_missing}" if n_missing else ""))


if __name__ == "__main__":
    main()

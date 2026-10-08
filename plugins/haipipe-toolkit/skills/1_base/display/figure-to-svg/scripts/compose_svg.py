#!/usr/bin/env python3
"""Assemble a master SVG from items.json + the per-icon SVGs.

Usage:
    compose_svg.py <items.json> <svg_dir> <out.svg> [--crops DIR] [--no-wrapped] [--no-raster]

Writes up to THREE variants per run:
  <out>.svg          vector icons, PPT-safe text  (the editable deliverable)
  <out>_wrapped.svg  tspan-wrapped text           (for visual diff only)
  <out>_raster.svg   every icon embedded as its PNG crop; text/panels/connectors stay
                     vector (max icon fidelity — icons stay pictures in PPT)

Reads the inventory (items.json), nests each icon's hand-authored SVG at its bbox, embeds any
`keep_raster` icons as PNGs, paints panel/background rects, and emits <text> for every label.
The canvas is sized to the original figure (width/height in items.json).

TWO variants from one config (lesson/16 - PowerPoint collapses <tspan> line breaks):
  <out.svg>              PPT-SAFE: every line is its own absolutely-positioned <text>, so
                         Insert SVG -> Convert to Shape yields one editable text box per line.
                         If an item has "content_ppt" (a list of sentences), each sentence
                         becomes one single-line <text> instead (overflow OK, re-wrap in PPT).
  <out>_wrapped.svg      tspan line breaks (classic), for the faithful visual diff.

  --crops DIR    folder of raster crops for keep_raster items (default: <items_dir>/crop_images)
  --no-wrapped   skip the _wrapped variant

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


def icon_element(it, svg_dir, crops_dir, force_raster=False):
    x, y, w, h = it["bbox"]
    preserve = it.get("preserve", "xMidYMid meet")
    if it.get("keep_raster") or force_raster:
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
    """Draw a figure-level primitive in source coordinates. 'arrow' (also covers plain lines via
    heads:"none"). Handy for panel-to-panel arrows and dashed bias connectors that are simpler
    drawn on the master canvas than cropped and vectorized as icons.

    Fields: type("arrow"), x1,y1,x2,y2, color, width, dashed(bool), dash("7 5"),
            heads("end"|"both"|"none"), head_size, head_width,
            curve(float): perpendicular bow offset of a quadratic-Bezier control point from the
            midpoint — 0 = straight line; +/- bows to one side or the other. Use for the curved
            arcs in a hub/cycle diagram. Arrowheads follow the curve's end tangent.
    """
    if c.get("type", "arrow") != "arrow":
        return f'  <!-- unknown connector type {esc_attr(c.get("type"))} -->'
    x1, y1, x2, y2 = c["x1"], c["y1"], c["x2"], c["y2"]
    color = c.get("color", "#007D81")
    w = c.get("width", 3)
    heads = c.get("heads", "end")
    hs = c.get("head_size", w * 3 + 6)          # arrowhead length along the shaft
    hw = c.get("head_width", hs * 0.8)          # arrowhead base width
    curve = c.get("curve", 0)
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L                     # chord direction
    px, py = -uy, ux                            # perpendicular
    dash = f' stroke-dasharray="{c.get("dash", "7 5")}"' if c.get("dashed") else ""

    def head(tx, ty, dirx, diry):               # arrowhead pointing along (dirx,diry)
        pxx, pyy = -diry, dirx
        bx, by = tx - dirx * hs, ty - diry * hs
        lx, ly = bx + pxx * hw / 2, by + pyy * hw / 2
        rx, ry = bx - pxx * hw / 2, by - pyy * hw / 2
        return (f'<path d="M{tx:.1f} {ty:.1f} L{lx:.1f} {ly:.1f} L{rx:.1f} {ry:.1f} Z" '
                f'fill="{esc_attr(color)}"/>')

    if curve:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        cx, cy = mx + px * curve, my + py * curve       # quadratic control point
        # end tangent = direction from control to endpoint
        etx, ety = x2 - cx, y2 - cy
        el = math.hypot(etx, ety) or 1.0
        ex, ey = etx / el, ety / el
        stx, sty = x1 - cx, y1 - cy
        sl = math.hypot(stx, sty) or 1.0
        sx_, sy_ = stx / sl, sty / sl                   # start tangent (control->start)
        e2x, e2y = (x2 - ex * hs, y2 - ey * hs) if heads in ("end", "both") else (x2, y2)
        s2x_, s2y_ = (x1 - sx_ * hs, y1 - sy_ * hs) if heads == "both" else (x1, y1)
        out = [f'<path d="M{s2x_:.1f} {s2y_:.1f} Q {cx:.1f} {cy:.1f} {e2x:.1f} {e2y:.1f}" '
               f'fill="none" stroke="{esc_attr(color)}" stroke-width="{w}"{dash} '
               f'stroke-linecap="butt"/>']
        if heads in ("end", "both"):
            out.append(head(x2, y2, ex, ey))
        if heads == "both":
            out.append(head(x1, y1, sx_, sy_))
        return "  " + "\n  ".join(out)

    s1x, s1y, s2x, s2y = x1, y1, x2, y2         # shaft ends, pulled back under heads
    if heads in ("end", "both"):
        s2x, s2y = x2 - ux * hs, y2 - uy * hs
    if heads == "both":
        s1x, s1y = x1 + ux * hs, y1 + uy * hs
    out = [f'<line x1="{s1x:.1f}" y1="{s1y:.1f}" x2="{s2x:.1f}" y2="{s2y:.1f}" '
           f'stroke="{esc_attr(color)}" stroke-width="{w}"{dash} stroke-linecap="butt"/>']
    if heads in ("end", "both"):
        out.append(head(x2, y2, ux, uy))
    if heads == "both":
        out.append(head(x1, y1, -ux, -uy))
    return "  " + "\n  ".join(out)


def text_element(it, ppt=False):
    """One label -> SVG text. ppt=False: multi-line via tspans (renders faithfully, but PPT
    collapses the line breaks). ppt=True: one absolutely-positioned <text> per line, so each
    becomes its own editable text box after Convert to Shape; if the item carries "content_ppt"
    (a list of sentences), each sentence is one single-line <text> (overflow OK, re-wrap in PPT).
    """
    x, y, w, h = it["bbox"]
    anchor = it.get("anchor", "start")
    tx = {"start": x, "middle": x + w / 2, "end": x + w}.get(anchor, x)
    size = it.get("font_size", 16)
    # bbox is the glyph box; place the baseline near its lower third.
    baseline = y + h * 0.5 + size * 0.35 if h else y + size
    weight = it.get("weight", "normal")
    color = it.get("color", "#000000")
    family = it.get("font_family", "Helvetica, Arial, sans-serif")
    style = f' font-style="{esc_attr(it["font_style"])}"' if it.get("font_style") else ""
    attrs = (f'x="{tx:.1f}" font-size="{size}" font-weight="{esc_attr(weight)}" '
             f'font-family="{esc_attr(family)}"{style} fill="{esc_attr(color)}" '
             f'text-anchor="{esc_attr(anchor)}"')
    if ppt and it.get("content_ppt"):
        lines = [str(s) for s in it["content_ppt"]]
    else:
        lines = str(it.get("content", "")).split("\n")
    if len(lines) == 1:
        return f'  <text {attrs} y="{baseline:.1f}">{esc_text(lines[0])}</text>'
    if ppt:
        return "\n".join(
            f'  <text {attrs} y="{baseline + i * size * 1.2:.1f}">{esc_text(ln)}</text>'
            for i, ln in enumerate(lines))
    spans = "".join(
        f'<tspan x="{tx:.1f}" dy="{0 if i == 0 else size * 1.2:.1f}">{esc_text(ln)}</tspan>'
        for i, ln in enumerate(lines))
    return f'  <text {attrs} y="{baseline:.1f}">{spans}</text>'


def build(data, svg_dir, crops_dir, ppt, force_raster=False):
    """Compose one full SVG document; ppt picks the text mode (see text_element).
    force_raster embeds EVERY icon as its PNG crop (the raster-icon variant): icons keep the
    generated image's fidelity, while text/panels/connectors stay vector and PPT-editable."""
    W, H = data["width"], data["height"]
    out = [f'<svg xmlns="{SVG_NS}" xmlns:xlink="{XLINK}" '
           f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">']

    bg = data.get("background")
    if bg:
        out.append(f'  <rect x="0" y="0" width="{W}" height="{H}" fill="{esc_attr(bg)}"/>')

    # Panels may carry a measured gradient (lesson/17) instead of a flat fill:
    #   "gradient": {"from": "#0B5FA5", "to": "#1F2E5A", "direction": "horizontal"|"vertical"}
    # A panel may also be dashed: "dash": "8 6" (any SVG stroke-dasharray string).
    # Named gradients declared at top level as {"gradients": {"bar": {...}}} can be referenced
    # from any panel or path by "gradient_ref": "bar".
    defs, panel_rects = [], []
    for name, g in (data.get("gradients") or {}).items():
        gx2, gy2 = ("0", "1") if g.get("direction") == "vertical" else ("1", "0")
        stops = g.get("stops") or [{"offset": 0, "color": g["from"]},
                                   {"offset": 1, "color": g["to"]}]
        body = "".join(f'<stop offset="{s["offset"]}" stop-color="{esc_attr(s["color"])}"/>'
                       for s in stops)
        defs.append(f'    <linearGradient id="grad-{esc_attr(name)}" x1="0" y1="0" '
                    f'x2="{gx2}" y2="{gy2}">{body}</linearGradient>')
    for i, p in enumerate(data.get("panels", [])):
        x, y, w, h = p["bbox"]
        fill = esc_attr(p.get("fill", "none"))
        g = p.get("gradient")
        if g:
            gid = f"panel-grad-{i}"
            gx2, gy2 = ("0", "1") if g.get("direction") == "vertical" else ("1", "0")
            defs.append(f'    <linearGradient id="{gid}" x1="0" y1="0" x2="{gx2}" y2="{gy2}">'
                        f'<stop offset="0" stop-color="{esc_attr(g["from"])}"/>'
                        f'<stop offset="1" stop-color="{esc_attr(g["to"])}"/></linearGradient>')
            fill = f"url(#{gid})"
        elif p.get("gradient_ref"):
            fill = f'url(#grad-{esc_attr(p["gradient_ref"])})'
        dash = f' stroke-dasharray="{esc_attr(p["dash"])}"' if p.get("dash") else ""
        panel_rects.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" '
                           f'rx="{p.get("rx", 0)}" fill="{fill}" '
                           f'stroke="{esc_attr(p.get("stroke", "none"))}" '
                           f'stroke-width="{p.get("stroke_width", 1)}"{dash}/>')
    if defs:
        out.append("  <defs>\n" + "\n".join(defs) + "\n  </defs>")
    out.extend(panel_rects)

    for e in data.get("ellipses", []):
        out.append(f'  <ellipse cx="{e["cx"]}" cy="{e["cy"]}" rx="{e["rx"]}" '
                   f'ry="{e.get("ry", e["rx"])}" fill="{esc_attr(e.get("fill", "none"))}" '
                   f'stroke="{esc_attr(e.get("stroke", "none"))}" '
                   f'stroke-width="{e.get("stroke_width", 1)}"/>')

    for c in data.get("connectors", []):
        out.append(connector_element(c))

    # Free-form vector shapes (braces, gradient arrows, tick marks, glyphs drawn on top of an
    # ellipse...) that are cheaper as one path than as a pile of connectors. Drawn above panels,
    # ellipses and connectors, below icons and text. Fields: d, fill, stroke, stroke_width, dash,
    # linecap, gradient_ref (fills from a named entry in the top-level "gradients" map).
    for p in data.get("paths", []):
        fill = (f'url(#grad-{esc_attr(p["gradient_ref"])})' if p.get("gradient_ref")
                else esc_attr(p.get("fill", "none")))
        dash = f' stroke-dasharray="{esc_attr(p["dash"])}"' if p.get("dash") else ""
        cap = f' stroke-linecap="{esc_attr(p["linecap"])}"' if p.get("linecap") else ""
        out.append(f'  <path d="{esc_attr(p["d"])}" fill="{fill}" '
                   f'stroke="{esc_attr(p.get("stroke", "none"))}" '
                   f'stroke-width="{p.get("stroke_width", 1)}"{dash}{cap}/>')

    n_icon = n_raster = n_text = n_missing = 0
    for it in data.get("items", []):
        t = it.get("type")
        if t == "icon":
            el = icon_element(it, svg_dir, crops_dir, force_raster=force_raster)
            if "MISSING" in el:
                n_missing += 1
            elif it.get("keep_raster") or force_raster:
                n_raster += 1
            else:
                n_icon += 1
            out.append(el)
        elif t == "text":
            out.append(text_element(it, ppt=ppt))
            n_text += 1

    out.append("</svg>\n")
    stats = (f"({W}x{H})  icons={n_icon} raster={n_raster} text={n_text} "
             f"panels={len(data.get('panels', []))}"
             + (f"  MISSING={n_missing}" if n_missing else ""))
    return "\n".join(out), stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("items")
    ap.add_argument("svg_dir")
    ap.add_argument("out")
    ap.add_argument("--crops", default=None,
                    help="folder of raster crops for keep_raster items "
                         "(default: <items_dir>/crop_images)")
    ap.add_argument("--no-wrapped", action="store_true",
                    help="skip the tspan-wrapped variant (<out>_wrapped.svg)")
    ap.add_argument("--no-raster", action="store_true",
                    help="skip the raster-icon variant (<out>_raster.svg)")
    a = ap.parse_args()

    data = json.load(open(a.items, encoding="utf-8"))
    crops_dir = a.crops or os.path.join(os.path.dirname(os.path.abspath(a.items)), "crop_images")

    doc, stats = build(data, a.svg_dir, crops_dir, ppt=True)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"wrote {a.out}  {stats}  [ppt-safe text]")

    root, ext = os.path.splitext(a.out)
    if not a.no_wrapped:
        wrapped = root + "_wrapped" + (ext or ".svg")
        doc, stats = build(data, a.svg_dir, crops_dir, ppt=False)
        with open(wrapped, "w", encoding="utf-8") as f:
            f.write(doc)
        print(f"wrote {wrapped}  {stats}  [tspan-wrapped text]")

    if not a.no_raster:
        raster = root + "_raster" + (ext or ".svg")
        doc, stats = build(data, a.svg_dir, crops_dir, ppt=True, force_raster=True)
        with open(raster, "w", encoding="utf-8") as f:
            f.write(doc)
        print(f"wrote {raster}  {stats}  [raster icons]")


if __name__ == "__main__":
    main()

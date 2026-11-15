"""A deck read in place: each .pptx slide drawn as one SVG, read only."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote, urlencode

from live.frame_base import ROUTE, _e, _rel


# ── a deck read in place (JL 261014: "could we do the preview of the slide as well?") ────────────────────────
# A .pptx is a zip of XML: each slide drawn as one SVG, in points (12,700 EMU), with its shapes (rect, roundRect,
# ellipse, triangle, a free-form path), connector lines and their arrowheads, pictures (cropped as the deck crops
# them), text boxes and tables where the deck puts them, and the theme's colours. A placeholder with no position
# takes its layout's or master's. Charts and diagrams show as a dashed box. Read only; nothing is converted.
_PPTX_CACHE: dict = {}
_PX = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main",
       "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
       "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
_EMU = 12700.0
_DASH = {"dash": (4, 3), "sysDash": (3, 1), "dot": (1, 2), "sysDot": (1, 1), "dashDot": (4, 2, 1, 2),
         "lgDash": (8, 3), "lgDashDot": (8, 3, 1, 3), "sysDashDot": (3, 1, 1, 1)}
_PRESET_COLOURS = {"black": "000000", "white": "FFFFFF", "red": "FF0000", "green": "008000", "blue": "0000FF",
                   "yellow": "FFFF00", "gray": "808080", "grey": "808080"}
_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
         ".svg": "image/svg+xml", ".webp": "image/webp", ".bmp": "image/bmp"}


def _q(tag: str) -> str:
    ns, name = tag.split(":")
    return "{" + _PX[ns] + "}" + name


class _Deck:
    """One open package: its parts, their relationships, the theme's colours and fonts, and the drawing state."""

    def __init__(self, path: Path, link=None):
        import xml.etree.ElementTree as ET
        self.link = link or (lambda name: "")       # a picture's address: served from the package, never inlined
        import zipfile
        self.ET, self.zf = ET, zipfile.ZipFile(path)
        self.names = set(self.zf.namelist())
        self.pictures, self.markers, self.clips, self.marked = 0, {}, 0, 0
        self.colours, self.fonts = {}, {}
        theme = next((n for n in sorted(self.names) if re.match(r"ppt/theme/theme\d+\.xml$", n)), None)
        if theme:
            t = self.xml(theme)
            scheme = t.find(".//" + _q("a:clrScheme"))
            for el in (list(scheme) if scheme is not None else []):
                c = el.find(_q("a:srgbClr"))
                s = el.find(_q("a:sysClr"))
                val = c.get("val") if c is not None else (s.get("lastClr") if s is not None else None)
                if val:
                    self.colours[el.tag.split("}")[1]] = val
            for key, tag in (("+mj-lt", "a:majorFont"), ("+mn-lt", "a:minorFont")):
                latin = t.find(".//" + _q(tag) + "/" + _q("a:latin"))
                if latin is not None:
                    self.fonts[key] = latin.get("typeface", "")

    def xml(self, name: str):
        return self.ET.fromstring(self.zf.read(name))

    def rels(self, part: str) -> dict:
        import posixpath
        name = posixpath.join(posixpath.dirname(part), "_rels", posixpath.basename(part) + ".rels")
        if name not in self.names:
            return {}
        out = {}
        for r in self.xml(name):
            if r.get("TargetMode") == "External":
                continue
            target = r.get("Target", "")
            target = target.lstrip("/") if target.startswith("/") else posixpath.normpath(
                posixpath.join(posixpath.dirname(part), target))
            out[r.get("Id")] = (r.get("Type", "").rsplit("/", 1)[-1], target)
        return out

    # colours ------------------------------------------------------------------------------------------------
    def colour(self, holder) -> tuple:
        """(#rrggbb or None, opacity) of a fill holder (a:solidFill, a fillRef, a gradient stop)."""
        import colorsys
        if holder is None:
            return None, 1.0
        el = next((c for c in holder if c.tag in (_q("a:srgbClr"), _q("a:schemeClr"), _q("a:sysClr"),
                                                   _q("a:prstClr"))), None)
        if el is None:
            return None, 1.0
        name = el.tag.split("}")[1]
        if name == "srgbClr":
            hexv = el.get("val", "000000")
        elif name == "sysClr":
            hexv = el.get("lastClr", "000000")
        elif name == "prstClr":
            hexv = _PRESET_COLOURS.get(el.get("val", ""), "000000")
        else:
            key = {"tx1": "dk1", "bg1": "lt1", "tx2": "dk2", "bg2": "lt2"}.get(el.get("val", ""), el.get("val", ""))
            hexv = self.colours.get(key, "000000")
        r, g, b = (int(hexv[i:i + 2], 16) / 255 for i in (0, 2, 4)) if len(hexv) == 6 else (0, 0, 0)
        alpha = 1.0
        for m in el:
            v = int(m.get("val", "100000")) / 100000
            kind = m.tag.split("}")[1]
            if kind == "alpha":
                alpha = v
            elif kind in ("lumMod", "lumOff"):
                h, l, s = colorsys.rgb_to_hls(r, g, b)
                l = min(1, max(0, l * v if kind == "lumMod" else l + v))
                r, g, b = colorsys.hls_to_rgb(h, l, s)
            elif kind == "shade":
                r, g, b = r * v, g * v, b * v
            elif kind == "tint":
                r, g, b = (c + (1 - c) * (1 - v) for c in (r, g, b))
        return "#%02x%02x%02x" % tuple(round(min(1, max(0, c)) * 255) for c in (r, g, b)), alpha

    def fill(self, sppr, style) -> tuple:
        for el in (list(sppr) if sppr is not None else []):
            kind = el.tag.split("}")[1]
            if kind == "noFill":
                return None, 1.0
            if kind == "solidFill":
                return self.colour(el)
            if kind == "gradFill":
                stop = el.find(".//" + _q("a:gs"))
                return self.colour(stop)
            if kind == "pattFill":
                return self.colour(el.find(_q("a:fgClr")))
        ref = style.find(_q("a:fillRef")) if style is not None else None
        return self.colour(ref) if ref is not None and ref.get("idx", "0") != "0" else (None, 1.0)

    def line(self, sppr, style, connector: bool) -> dict | None:
        ln = sppr.find(_q("a:ln")) if sppr is not None else None
        ref = style.find(_q("a:lnRef")) if style is not None else None
        colour, alpha = (None, 1.0)
        if ln is not None and ln.find(_q("a:noFill")) is not None:
            return None
        if ln is not None and ln.find(_q("a:solidFill")) is not None:
            colour, alpha = self.colour(ln.find(_q("a:solidFill")))
        elif ln is not None and ln.find(_q("a:gradFill")) is not None:
            colour, alpha = self.colour(ln.find(".//" + _q("a:gs")))
        elif ref is not None and ref.get("idx", "0") != "0":
            colour, alpha = self.colour(ref)
        elif connector:
            colour = "#000000"
        if colour is None:
            return None
        width = int(ln.get("w", "9525")) / _EMU if ln is not None and ln.get("w") else 0.75
        dash = ln.find(_q("a:prstDash")) if ln is not None else None
        ends = {k: (ln.find(_q(f"a:{k}End")).get("type", "none") if ln is not None and ln.find(_q(f"a:{k}End")) is not None
                    else "none") for k in ("head", "tail")}
        return {"colour": colour, "alpha": alpha, "width": max(width, 0.5),
                "dash": _DASH.get(dash.get("val", "solid"), None) if dash is not None else None, **ends}

    def marker(self, colour: str, kind: str) -> str:
        key = (colour, kind)
        if key not in self.markers:
            mid, self.marked = f"pm{self.marked}", self.marked + 1     # unique on the page, every slide
            shape = ('<circle cx="5" cy="5" r="4"/>' if kind == "oval" else
                     '<path d="M0,5 L5,0 L10,5 L5,10 z"/>' if kind == "diamond" else
                     '<path d="M0,0 L10,5 L0,10" fill="none" stroke-width="1.6"/>' if kind == "arrow" else
                     '<path d="M0,0 L10,5 L0,10 z"/>')
            self.markers[key] = (mid, f'<marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3.5" '
                                      f'markerHeight="3.5" orient="auto-start-reverse"><g fill="{colour}" '
                                      f'stroke="{colour}">{shape}</g></marker>')
        return self.markers[key][0]


def _pptx_xfrm(el, tag: str = "a:xfrm") -> dict | None:
    x = el.find(_q(tag)) if el is not None else None
    off, ext = (x.find(_q("a:off")), x.find(_q("a:ext"))) if x is not None else (None, None)
    if off is None or ext is None:
        return None
    out = {k: int(off.get(k[0], "0")) / _EMU for k in ("x", "y")}
    out.update(w=int(ext.get("cx", "0")) / _EMU, h=int(ext.get("cy", "0")) / _EMU,
               rot=int(x.get("rot", "0")) / 60000, fh=x.get("flipH") in ("1", "true"),
               fv=x.get("flipV") in ("1", "true"))
    ch_off, ch_ext = x.find(_q("a:chOff")), x.find(_q("a:chExt"))
    if ch_off is not None and ch_ext is not None:
        out.update(cx=int(ch_off.get("x", "0")) / _EMU, cy=int(ch_off.get("y", "0")) / _EMU,
                   cw=int(ch_ext.get("cx", "0")) / _EMU, chh=int(ch_ext.get("cy", "0")) / _EMU)
    return out


def _pptx_geometry(sppr, w: float, h: float) -> list:
    """[(svg path d, filled, stroked)] of a shape's geometry in its own box (0..w, 0..h)."""
    import math
    f = lambda v: f"{v:.2f}"
    cust = sppr.find(_q("a:custGeom")) if sppr is not None else None
    if cust is not None:
        out = []
        for path in cust.iter(_q("a:path")):
            pw, ph = int(path.get("w", "0")) or None, int(path.get("h", "0")) or None
            sx = w / pw if pw else 1 / _EMU
            sy = h / ph if ph else 1 / _EMU
            d, cur = [], (0.0, 0.0)
            pt = lambda p: (int(p.get("x", "0")) * sx, int(p.get("y", "0")) * sy)
            for c in path:
                kind = c.tag.split("}")[1]
                pts = [pt(p) for p in c.findall(_q("a:pt"))]
                if kind == "moveTo" and pts:
                    d.append(f"M{f(pts[0][0])},{f(pts[0][1])}"); cur = pts[0]
                elif kind == "lnTo" and pts:
                    d.append(f"L{f(pts[0][0])},{f(pts[0][1])}"); cur = pts[0]
                elif kind == "cubicBezTo" and len(pts) == 3:
                    d.append("C" + " ".join(f"{f(x)},{f(y)}" for x, y in pts)); cur = pts[2]
                elif kind == "quadBezTo" and len(pts) == 2:
                    d.append("Q" + " ".join(f"{f(x)},{f(y)}" for x, y in pts)); cur = pts[1]
                elif kind == "arcTo":
                    rx, ry = int(c.get("wR", "0")) * sx, int(c.get("hR", "0")) * sy
                    st, sw = math.radians(int(c.get("stAng", "0")) / 60000), math.radians(int(c.get("swAng", "0")) / 60000)
                    cx0, cy0 = cur[0] - rx * math.cos(st), cur[1] - ry * math.sin(st)
                    end = (cx0 + rx * math.cos(st + sw), cy0 + ry * math.sin(st + sw))
                    d.append(f"A{f(rx)},{f(ry)} 0 {int(abs(sw) > math.pi)} {int(sw > 0)} {f(end[0])},{f(end[1])}")
                    cur = end
                elif kind == "close":
                    d.append("Z")
            out.append((" ".join(d), path.get("fill", "norm") != "none", path.get("stroke", "1") not in ("0", "false")))
        return out
    prst = sppr.find(_q("a:prstGeom")) if sppr is not None else None
    kind = prst.get("prst", "rect") if prst is not None else "rect"
    adj = {g.get("name"): int(re.sub(r"\D", "", g.get("fmla", "")) or 0)
           for g in (prst.iter(_q("a:gd")) if prst is not None else [])}
    if kind == "roundRect":
        r = min(w, h) * adj.get("adj", 16667) / 100000
        return [(f"M{f(r)},0 H{f(w - r)} A{f(r)},{f(r)} 0 0 1 {f(w)},{f(r)} V{f(h - r)} A{f(r)},{f(r)} 0 0 1 "
                 f"{f(w - r)},{f(h)} H{f(r)} A{f(r)},{f(r)} 0 0 1 0,{f(h - r)} V{f(r)} A{f(r)},{f(r)} 0 0 1 {f(r)},0 Z",
                 True, True)]
    if kind in ("ellipse", "flowChartConnector"):
        return [(f"M0,{f(h / 2)} A{f(w / 2)},{f(h / 2)} 0 1 0 {f(w)},{f(h / 2)} A{f(w / 2)},{f(h / 2)} 0 1 0 0,{f(h / 2)} Z",
                 True, True)]
    if kind in ("triangle", "flowChartExtract"):
        return [(f"M{f(w / 2)},0 L{f(w)},{f(h)} L0,{f(h)} Z", True, True)]
    if kind in ("diamond", "flowChartDecision"):
        return [(f"M{f(w / 2)},0 L{f(w)},{f(h / 2)} L{f(w / 2)},{f(h)} L0,{f(h / 2)} Z", True, True)]
    if kind == "bentConnector2":
        return [(f"M0,0 H{f(w)} V{f(h)}", False, True)]
    if kind.startswith("bentConnector"):
        x = w * adj.get("adj1", 50000) / 100000
        return [(f"M0,0 H{f(x)} V{f(h)} H{f(w)}", False, True)]
    if kind.startswith("curvedConnector"):
        return [(f"M0,0 C{f(w / 2)},0 {f(w / 2)},{f(h)} {f(w)},{f(h)}", False, True)]
    if kind in ("line", "straightConnector1"):
        return [(f"M0,0 L{f(w)},{f(h)}", False, True)]
    return [(f"M0,0 H{f(w)} V{f(h)} H0 Z", True, True)]


def _pptx_text(deck: _Deck, body, w: float, h: float, inherited: dict) -> str:
    """A shape's text as an HTML block in a foreignObject over its box: insets, anchor, wrap, paragraphs, runs."""
    if body is None or not any((t.text or "").strip() for t in body.iter(_q("a:t"))):
        return ""
    pr = body.find(_q("a:bodyPr"))
    pr = pr if pr is not None else deck.ET.Element("x")
    ins = [int(pr.get(k, d)) / _EMU for k, d in (("tIns", "45720"), ("rIns", "91440"), ("bIns", "45720"), ("lIns", "91440"))]
    anchor = {"ctr": "center", "b": "flex-end"}.get(pr.get("anchor") or inherited.get("anchor", "t"), "flex-start")
    nowrap = pr.get("wrap") == "none"
    fit = pr.find(_q("a:normAutofit"))
    scale = int(fit.get("fontScale", "100000")) / 100000 if fit is not None else 1.0
    base = dict(inherited)
    styles = body.find(_q("a:lstStyle"))
    for lvl in ("a:defPPr", "a:lvl1pPr"):
        el = styles.find(_q(lvl)) if styles is not None else None
        if el is not None:
            base.update(_pptx_ppr(deck, el))
    paras, number = [], 0
    for p in body.findall(_q("a:p")):
        ppr = p.find(_q("a:pPr"))
        style = dict(base, **(_pptx_ppr(deck, ppr) if ppr is not None else {}))
        runs, size = [], style.get("sz", 18.0)
        for r in p:
            kind = r.tag.split("}")[1]
            if kind == "br":
                runs.append("<br>")
                continue
            if kind not in ("r", "fld"):
                continue
            rs = dict(style, **_pptx_rpr(deck, r.find(_q("a:rPr"))))
            size = max(size, rs.get("sz", size)) if runs else rs.get("sz", size)
            css = [f"font-size:{rs.get('sz', 18.0) * scale:.2f}px"]
            if rs.get("b"):
                css.append("font-weight:700")
            if rs.get("i"):
                css.append("font-style:italic")
            if rs.get("u"):
                css.append("text-decoration:underline")
            if rs.get("color"):
                css.append(f"color:{rs['color']}")
            if rs.get("font"):
                face = deck.fonts.get(rs["font"], rs["font"])
                css.append(f"font-family:'{_e(face)}',Aptos,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif")
            text = "".join(t.text or "" for t in r.iter(_q("a:t")))
            runs.append(f'<span style="{";".join(css)}">{_e(text)}</span>')
        end = p.find(_q("a:endParaRPr"))
        if not runs and end is not None and end.get("sz"):
            size = int(end.get("sz")) / 100
        bullet = ""
        if runs and style.get("bullet"):
            number += 1
            bullet = f"{number}. " if style["bullet"] == "#" else style["bullet"] + " "
        align = {"ctr": "center", "r": "right", "just": "justify", "dist": "justify"}.get(style.get("algn", "l"), "left")
        css = [f"text-align:{align}", f"font-size:{size * scale:.2f}px", f"line-height:{style.get('lh', 1.2):.2f}",
               f"margin:{style.get('before', 0):.2f}px 0 {style.get('after', 0):.2f}px {style.get('marL', 0):.2f}px"]
        if style.get("indent"):
            css.append(f"text-indent:{style['indent']:.2f}px")
        if nowrap:
            css.append("white-space:pre")
        paras.append(f'<p style="{";".join(css)}">{_e(bullet)}{"".join(runs) or "&#8203;"}</p>')
    return (f'<foreignObject x="0" y="0" width="{w:.2f}" height="{h:.2f}" overflow="visible">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" style="box-sizing:border-box;width:{w:.2f}px;height:{h:.2f}px;'
            f'display:flex;flex-direction:column;justify-content:{anchor};padding:{ins[0]:.2f}px {ins[1]:.2f}px '
            f'{ins[2]:.2f}px {ins[3]:.2f}px;overflow:visible;color:{inherited.get("color") or "#" + deck.colours.get("dk1", "000000")};'
            f'font-family:Aptos,-apple-system,\'Segoe UI\',Helvetica,Arial,sans-serif;'
            f'{"align-items:center;" if nowrap and base.get("algn") == "ctr" else ""}word-wrap:break-word">'
            f'{"".join(paras)}</div></foreignObject>')


def _pptx_rpr(deck: _Deck, el) -> dict:
    """A run's (or a level's defRPr) size in points, bold, italic, underline, colour and typeface."""
    if el is None:
        return {}
    out = {}
    if el.get("sz"):
        out["sz"] = int(el.get("sz")) / 100
    for k in ("b", "i"):
        if el.get(k) is not None:
            out[k] = el.get(k) in ("1", "true")
    if el.get("u") not in (None, "none"):
        out["u"] = True
    fill = el.find(_q("a:solidFill"))
    if fill is not None:
        out["color"] = deck.colour(fill)[0]
    latin = el.find(_q("a:latin"))
    if latin is not None and latin.get("typeface"):
        out["font"] = latin.get("typeface")
    return out


def _pptx_ppr(deck: _Deck, el) -> dict:
    """A paragraph's (or a level's) alignment, spacing, indents and bullet, with its default run style."""
    out = {}
    if el.get("algn"):
        out["algn"] = el.get("algn")
    for k, key in (("marL", "marL"), ("indent", "indent")):
        if el.get(k):
            out[key] = int(el.get(k)) / _EMU
    for tag, key in (("a:spcBef", "before"), ("a:spcAft", "after")):
        pts = el.find(_q(tag) + "/" + _q("a:spcPts"))
        if pts is not None:
            out[key] = int(pts.get("val", "0")) / 100
    pct = el.find(_q("a:lnSpc") + "/" + _q("a:spcPct"))
    if pct is not None:
        out["lh"] = 1.2 * int(pct.get("val", "100000")) / 100000
    if el.find(_q("a:buNone")) is not None:
        out["bullet"] = ""
    elif el.find(_q("a:buChar")) is not None:
        out["bullet"] = el.find(_q("a:buChar")).get("char", "•")
    elif el.find(_q("a:buAutoNum")) is not None:
        out["bullet"] = "#"
    out.update(_pptx_rpr(deck, el.find(_q("a:defRPr"))))
    return out


def _pptx_placeholder(deck: _Deck, sp, holders: list) -> tuple:
    """(xfrm, style) a placeholder takes from its layout, then its master, when the slide gives it no position."""
    ph = sp.find(_q("p:nvSpPr") + "/" + _q("p:nvPr") + "/" + _q("p:ph"))
    if ph is None:
        return None, {}
    kind, idx = ph.get("type", "body"), ph.get("idx")
    same = {"ctrTitle": "title", "subTitle": "body", "obj": "body"}
    xfrm, style = None, {}
    for tree, master_styles in holders:
        for other in tree.iter(_q("p:sp")):
            oph = other.find(_q("p:nvSpPr") + "/" + _q("p:nvPr") + "/" + _q("p:ph"))
            if oph is None:
                continue
            if (idx is not None and oph.get("idx") == idx) or same.get(oph.get("type", "body"), oph.get("type", "body")) \
                    == same.get(kind, kind):
                xfrm = xfrm or _pptx_xfrm(other.find(_q("p:spPr")))
                pr = other.find(_q("p:txBody") + "/" + _q("a:bodyPr"))
                if pr is not None and pr.get("anchor") and "anchor" not in style:
                    style["anchor"] = pr.get("anchor")
                lvl = other.find(_q("p:txBody") + "/" + _q("a:lstStyle") + "/" + _q("a:lvl1pPr"))
                if lvl is not None:
                    style = dict(_pptx_ppr(deck, lvl), **style)
                break
        if master_styles is not None:
            which = "p:titleStyle" if same.get(kind, kind) == "title" else "p:bodyStyle"
            lvl = master_styles.find(_q(which) + "/" + _q("a:lvl1pPr"))
            if lvl is not None:
                style = dict(_pptx_ppr(deck, lvl), **style)
    return xfrm, style


def _pptx_shapes(deck: _Deck, tree, part: str, rels: dict, holders: list) -> str:
    """The children of one shape tree (a slide's, or a group's), drawn in order."""
    out = []
    for el in tree:
        kind = el.tag.split("}")[1]
        nv = next((c for c in el if c.tag.split("}")[1].startswith("nv")), None)
        cnv = nv.find(_q("p:cNvPr")) if nv is not None else None
        if cnv is not None and cnv.get("hidden") in ("1", "true"):
            continue
        if kind == "grpSp":
            x = _pptx_xfrm(el.find(_q("p:grpSpPr")))
            inner = _pptx_shapes(deck, el, part, rels, holders)
            if x and x.get("cw") and x.get("chh"):
                t = (f'translate({x["x"]:.2f} {x["y"]:.2f}) scale({x["w"] / x["cw"]:.5f} {x["h"] / x["chh"]:.5f}) '
                     f'translate({-x["cx"]:.2f} {-x["cy"]:.2f})')
                out.append(f'<g transform="{t}">{inner}</g>')
            else:
                out.append(f"<g>{inner}</g>")
        elif kind in ("sp", "cxnSp", "pic", "graphicFrame"):
            out.append(_pptx_one(deck, el, kind, part, rels, holders))
    return "".join(out)


def _pptx_one(deck: _Deck, el, kind: str, part: str, rels: dict, holders: list) -> str:
    sppr = el.find(_q("p:spPr"))
    style = el.find(_q("p:style"))
    x = _pptx_xfrm(el, "p:xfrm") if kind == "graphicFrame" else _pptx_xfrm(sppr)
    inherited = {}
    if kind == "sp":
        px, inherited = _pptx_placeholder(deck, el, holders)
        x = x or px
        font_ref = style.find(_q("a:fontRef")) if style is not None else None
        if font_ref is not None and deck.colour(font_ref)[0]:
            inherited.setdefault("color", deck.colour(font_ref)[0])
    if not x:
        return ""
    w, h = x["w"], x["h"]
    cx, cy = w / 2, h / 2
    move = f'translate({x["x"]:.2f} {x["y"]:.2f})' + (f' rotate({x["rot"]:.2f} {cx:.2f} {cy:.2f})' if x["rot"] else "")
    flip = (f' transform="translate({cx:.2f} {cy:.2f}) scale({-1 if x["fh"] else 1} {-1 if x["fv"] else 1}) '
            f'translate({-cx:.2f} {-cy:.2f})"') if x["fh"] or x["fv"] else ""
    body = ""
    if kind == "pic":
        blip = el.find(".//" + _q("a:blip"))
        target = rels.get(blip.get(_q("r:embed")) if blip is not None else None)
        ext = Path(target[1]).suffix.lower() if target else ""
        if target and ext in _MIME and target[1] in deck.names:
            deck.pictures += 1
            crop = el.find(".//" + _q("a:srcRect"))
            l, t, r, b = ((int(crop.get(k, "0")) / 100000 for k in ("l", "t", "r", "b")) if crop is not None
                          else (0, 0, 0, 0))
            iw, ih = w / max(1e-6, 1 - l - r), h / max(1e-6, 1 - t - b)
            image = (f'<image href="{_e(deck.link(target[1]))}" x="{-l * iw:.2f}" y="{-t * ih:.2f}" '
                     f'width="{iw:.2f}" height="{ih:.2f}" preserveAspectRatio="none"/>')
            if crop is not None and any((l, t, r, b)):
                deck.clips += 1
                body = (f'<clipPath id="pc{deck.clips}"><rect width="{w:.2f}" height="{h:.2f}"/></clipPath>'
                        f'<g clip-path="url(#pc{deck.clips})">{image}</g>')
            else:
                body = image
        else:
            body = (f'<rect width="{w:.2f}" height="{h:.2f}" fill="#f1f3f5" stroke="#adb5bd" stroke-dasharray="4 3"/>'
                    f'<text x="{cx:.2f}" y="{cy:.2f}" font-size="10" text-anchor="middle" fill="#868e96">picture</text>')
        return f'<g transform="{move}"><g{flip}>{body}</g></g>'
    if kind == "graphicFrame":
        tbl = el.find(".//" + _q("a:tbl"))
        if tbl is None:
            return (f'<g transform="{move}"><rect width="{w:.2f}" height="{h:.2f}" fill="none" stroke="#adb5bd" '
                    f'stroke-dasharray="4 3"/><text x="{cx:.2f}" y="{cy:.2f}" font-size="12" text-anchor="middle" '
                    f'fill="#868e96">chart or diagram</text></g>')
        cols = [int(c.get("w", "0")) / _EMU for c in tbl.iter(_q("a:gridCol"))]
        rows = []
        for tr in tbl.findall(_q("a:tr")):
            cells = []
            for tc in tr.findall(_q("a:tc")):
                if tc.get("hMerge") or tc.get("vMerge"):
                    continue
                fill = deck.colour(tc.find(_q("a:tcPr") + "/" + _q("a:solidFill")))[0] if tc.find(_q("a:tcPr")) is not None else None
                text = " ".join("".join(t.text or "" for t in p.iter(_q("a:t"))) for p in tc.iter(_q("a:p")))
                span = f' colspan="{tc.get("gridSpan")}"' if tc.get("gridSpan") else ""
                cells.append(f'<td{span} style="border:1px solid #ced4da;padding:2px 5px;'
                             f'{f"background:{fill};" if fill else ""}">{_e(text)}</td>')
            rows.append(f'<tr style="height:{int(tr.get("h", "0")) / _EMU:.2f}px">{"".join(cells)}</tr>')
        widths = "".join(f'<col style="width:{c:.2f}px">' for c in cols)
        return (f'<g transform="{move}"><foreignObject width="{w:.2f}" height="{h:.2f}" overflow="visible">'
                f'<table xmlns="http://www.w3.org/1999/xhtml" style="border-collapse:collapse;width:{w:.2f}px;'
                f'font:11px Aptos,-apple-system,Helvetica,Arial,sans-serif">{widths}{"".join(rows)}</table>'
                f'</foreignObject></g>')
    colour, alpha = deck.fill(sppr, style)
    line = deck.line(sppr, style, kind == "cxnSp")
    parts = []
    for d, filled, stroked in _pptx_geometry(sppr, w, h):
        attrs = [f'd="{d}"', f'fill="{colour}"' if filled and colour else 'fill="none"']
        if filled and colour and alpha < 1:
            attrs.append(f'fill-opacity="{alpha:.3f}"')
        if stroked and line:
            attrs += [f'stroke="{line["colour"]}"', f'stroke-width="{line["width"]:.2f}"', 'stroke-linejoin="round"']
            if line["alpha"] < 1:
                attrs.append(f'stroke-opacity="{line["alpha"]:.3f}"')
            if line["dash"]:
                attrs.append('stroke-dasharray="' + " ".join(f"{v * line['width']:.2f}" for v in line["dash"]) + '"')
            if line["head"] != "none":
                attrs.append(f'marker-start="url(#{deck.marker(line["colour"], line["head"])})"')
            if line["tail"] != "none":
                attrs.append(f'marker-end="url(#{deck.marker(line["colour"], line["tail"])})"')
        if 'fill="none"' in attrs and not (stroked and line):
            continue
        parts.append(f'<path {" ".join(attrs)}/>')
    text = _pptx_text(deck, el.find(_q("p:txBody")), w, h, inherited) if kind == "sp" else ""
    if not parts and not text:
        return ""
    return f'<g transform="{move}"><g{flip}>{"".join(parts)}</g>{text}</g>'


def pptx_preview(path: Path, root: Path) -> str:
    """A .pptx as a page: every slide drawn from its package as one SVG picture, in order; read only, cached by the
    file's stamp. A deck's own renders (its `render/` lane) stay the picture that counts; this reads the deck itself."""
    stamp = (str(path), path.stat().st_mtime_ns, path.stat().st_size)
    if stamp in _PPTX_CACHE:
        return _PPTX_CACHE[stamp]
    deck = _Deck(path, lambda name: ROUTE + "?" + urlencode({"view": "pptx", "path": _rel(path, root), "media": name}))
    pres = deck.xml("ppt/presentation.xml")
    size = pres.find(_q("p:sldSz"))
    W, H = (int(size.get("cx")) / _EMU, int(size.get("cy")) / _EMU) if size is not None else (720.0, 405.0)
    prels = deck.rels("ppt/presentation.xml")
    order = [prels.get(s.get(_q("r:id")), ("", ""))[1] for s in pres.iter(_q("p:sldId"))]
    slides = []
    for n, part in enumerate([o for o in order if o in deck.names], 1):
        tree = deck.xml(part)
        rels = deck.rels(part)
        layout = next((t for k, t in rels.values() if k == "slideLayout" and t in deck.names), None)
        holders, backs = [], [tree]
        if layout:
            ltree = deck.xml(layout)
            master = next((t for k, t in deck.rels(layout).values() if k == "slideMaster" and t in deck.names), None)
            mtree = deck.xml(master) if master else None
            holders = [(ltree, None)] + ([(mtree, mtree.find(_q("p:txStyles")))] if mtree is not None else [])
            backs += [ltree] + ([mtree] if mtree is not None else [])
        background = "#ffffff"
        for b in backs:
            bg = b.find(".//" + _q("p:bg"))
            if bg is None:
                continue
            pr, ref = bg.find(_q("p:bgPr")), bg.find(_q("p:bgRef"))
            got = deck.fill(pr, None)[0] if pr is not None else deck.colour(ref)[0] if ref is not None else None
            background = got or background
            break
        deck.markers = {}                        # this slide's arrowheads
        spt = tree.find(".//" + _q("p:spTree"))
        drawn = _pptx_shapes(deck, spt, part, rels, holders) if spt is not None else ""
        defs = "".join(m for _, m in deck.markers.values())
        slides.append(f'<p class=cap>Slide {n}</p><div class=slide><svg xmlns="http://www.w3.org/2000/svg" '
                      f'viewBox="0 0 {W:.2f} {H:.2f}" role="img" aria-label="Slide {n}"><defs>{defs}</defs>'
                      f'<rect width="{W:.2f}" height="{H:.2f}" fill="{background}"/>{drawn}</svg></div>')
    line = (f'<p class=cap>{_e(path.name)} · read from the deck package: {len(slides)} slide'
            f'{"s" if len(slides) != 1 else ""} · {deck.pictures} pictures · '
            f'<a href="/{_e(quote(_rel(path, root)))}">the .pptx ↓</a></p>')
    page = ('<!doctype html><meta charset=utf-8><title>' + _e(path.name) + '</title>'
            '<style>body{margin:0;padding:14px 18px;background:#f1f3f5;font:13px -apple-system,sans-serif;color:#555}'
            '.cap{max-width:1600px;margin:0 auto 6px}.slide{max-width:1600px;margin:0 auto 18px;background:#fff;'
            'box-shadow:0 1px 3px rgba(0,0,0,.18)}.slide svg{display:block;width:100%;height:auto}'
            '.slide p{margin:0}</style>' + line + "".join(slides))
    _PPTX_CACHE.clear()                           # one deck kept: the one being read
    _PPTX_CACHE[stamp] = page
    return page


def pptx_media(path: Path, name: str) -> tuple | None:
    """(bytes, type) of one picture inside a deck (`ppt/media/…`), for its slide's <image>; None when it is not one."""
    import zipfile
    ext = Path(name).suffix.lower()
    if not name.startswith("ppt/media/") or ext not in _MIME:
        return None
    with zipfile.ZipFile(path) as zf:
        return (zf.read(name), _MIME[ext]) if name in zf.namelist() else None

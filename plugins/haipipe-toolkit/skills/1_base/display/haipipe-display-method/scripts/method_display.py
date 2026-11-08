"""Draw a method display from a YAML spec: the study on one clock (timeline), how a dataset is built (workflow), or
how a comparison works (design).

    python method_display.py <spec.yaml> <out dir> [--colours <colour-scheme.yaml>]

kind: timeline   the study on one clock (the main kind): A each unit's timeline as bars with the event as one grey band,
                 B the periods and what each window is for, C the comparison as boxes (treated minus control)
kind: workflow   one row per step from raw data to the analysis file: the step's name and rule on the left, a small
                 picture of the file it writes on the right (real column names, made-up example values), the file name
                 and the Run that writes it under the picture, and a count when the step has one
kind: design     A the unit of comparison on one clock, B the difference in differences as 4 cells, C the models as
                 equations, D what each piece of the design removes and what it leaves in

Writes figure.pdf, figure.png, float.tex (title as caption, legend under it) and method.md (Message, Data, Sample,
Method, Outcomes, Made by, Numbers, from the spec's keys of those names) into <out dir>, the display's unit folder:
haipipe-display's build_preview.py <out dir> then makes preview.pdf.
Standard library plus matplotlib and PyYAML. Every value in an example row must be made up: the script never reads data.
"""
import argparse
import sys
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import yaml  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

DEFAULT = {"accent": "#d9480f", "control": "#495057", "ink": "#212529", "muted": "#868e96", "rule": "#dee2e6",
           "header": "#e9ecef", "highlight": "#fff4e6", "run_up": "#fff9db", "event": "#e9ecef"}


def colours(path):
    """The paper's or report's one colour scheme, when given; its treated/control/run_up_shade/absence_shade keys map
    onto this script's accent/control/run_up/event, so a method display uses the same colours as the result displays."""
    c = dict(DEFAULT)
    if path:
        s = yaml.safe_load(Path(path).read_text()) or {}
        for mine, theirs in (("accent", "treated"), ("control", "control"), ("run_up", "run_up_shade"), ("event", "absence_shade")):
            if theirs in s:
                c[mine] = s[theirs]
        c.update({k: v for k, v in s.items() if k in DEFAULT})
    return c


def wrap(text, width):
    """Wrap each paragraph of a text to width characters; an explicit newline is kept."""
    return "\n".join(textwrap.fill(p, width) if p else "" for p in str(text).split("\n"))


def setup(width, height):
    plt.rcParams.update({"font.family": ["Arial", "DejaVu Sans"], "font.size": 9, "mathtext.fontset": "dejavusans"})
    fig, ax = plt.subplots(figsize=(width, height))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.995, bottom=0.005)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax


def workflow(spec, C):
    """One row per step. Row height follows the longer of the rule text and the example table."""
    steps = spec["steps"]
    lines = []
    for st in steps:
        rule = wrap(st.get("rule", ""), 58)
        n_rule = rule.count("\n") + 1 + (1 if st.get("count") else 0)
        n_tab = len(st.get("rows", [])) + 1 + 2
        lines.append(max(n_rule + 3, n_tab + 3))
    total = sum(lines) + 1.2 * len(steps)
    height = max(4.0, 0.205 * total)
    fig, ax = setup(7.6, height)
    unit = 100 / total
    y = 99.6
    for k, st in enumerate(steps):
        h = lines[k] * unit
        hi = bool(st.get("highlight"))
        ax.add_patch(FancyBboxPatch((0.6, y - h + 0.4), 45.5, h - 0.8, boxstyle="round,pad=0.25,rounding_size=0.8",
                                    fc=C["highlight"] if hi else "white", ec=C["accent"] if hi else C["muted"], lw=0.8))
        top = y - 1.2 * unit
        ax.text(2.2, top, str(k + 1), fontsize=10, fontweight="bold", color=C["accent"], va="center")
        ax.text(5.6, top, st["name"], fontsize=9, fontweight="bold", color=C["ink"], va="center")
        ax.text(2.2, top - 1.3 * unit, wrap(st.get("rule", ""), 58), fontsize=6.9, color=C["ink"], va="top", linespacing=1.3)
        if st.get("count"):
            n_rule = wrap(st.get("rule", ""), 58).count("\n") + 1
            ax.text(2.2, top - (1.9 + 1.05 * n_rule) * unit, st["count"], fontsize=6.9, color=C["accent"], fontweight="bold", va="top")
        cols, rows = st.get("columns", []), st.get("rows", [])
        x0, x1 = 50, 99
        if cols:
            cw = (x1 - x0) / len(cols)
            rh = 1.15 * unit
            ty = y - 0.6 * unit
            ax.add_patch(Rectangle((x0, ty - rh), x1 - x0, rh, fc=C["header"], ec="none"))
            for j, c in enumerate(cols):
                ax.text(x0 + (j + 0.5) * cw, ty - rh / 2, c, fontsize=6.6, fontweight="bold", ha="center", va="center", family="monospace")
            for i, r in enumerate(rows):
                yy = ty - rh * (i + 1.5)
                for j, v in enumerate(r):
                    ax.text(x0 + (j + 0.5) * cw, yy, str(v), fontsize=6.6, ha="center", va="center", family="monospace", color=C["control"])
                ax.plot([x0, x1], [yy - rh / 2, yy - rh / 2], color=C["rule"], lw=0.5)
        below = (y - 0.6 * unit - 1.15 * unit * (len(rows) + 1)) if cols else y
        if st.get("file"):
            ax.text(x0, below - 1.2 * unit, st["file"], fontsize=6.6, color=C["ink"], va="center", family="monospace")
        if st.get("made_by"):
            ax.text(x0, below - 2.4 * unit, st["made_by"], fontsize=6.4, color=C["muted"], va="center")
        y -= h
        if k < len(steps) - 1:
            ax.annotate("", xy=(23, y - 0.9 * unit), xytext=(23, y + 0.5 * unit), arrowprops=dict(arrowstyle="-|>", color=C["muted"], lw=0.9))
        y -= 1.2 * unit
    return fig


def design(spec, C):
    """Four panels, each optional: clock (A), did (B), models (C), removes (D); letters follow the panels present."""
    panels = [p for p in ("clock", "did", "models", "removes") if spec.get(p)]
    size = {"clock": 26, "did": 21, "models": 7 + 5.2 * len(spec.get("models", [])), "removes": 6 + 3.2 * len(spec.get("removes", []))}
    total = sum(size[p] for p in panels)
    fig, ax = setup(7.6, 0.088 * total + 0.4)
    ax.set_ylim(100 - total, 100)
    y = 99.5

    def head(y, let, name):
        ax.text(0.6, y, let, fontsize=8.5, fontweight="bold", va="center", bbox=dict(boxstyle="square,pad=0.25", fc="white", ec="black", lw=0.7))
        ax.text(4, y, name, fontsize=9, fontweight="bold", va="center")
        ax.plot([0, 100], [y - 2.0, y - 2.0], color="black", lw=0.6)

    for k, p in enumerate(panels):
        let = "ABCD"[k]
        if p == "clock":
            ck = spec["clock"]
            head(y - 1.5, let, ck.get("title", "One unit of comparison, on one clock"))
            L, R = 22, 99
            segs = ck["segments"]
            gap = ck.get("start_gap", 0)
            span = R - L - gap
            wsum = sum(s.get("width", 1) for s in segs)
            x = L
            ys = y - 12
            ax.text(L - 1, ys, ck.get("axis", "Periods"), fontsize=7, ha="right", va="center")
            bounds = []
            for s in segs:
                w = span * s.get("width", 1) / wsum
                fc = {"run_up": C["run_up"], "event": C["event"]}.get(s.get("shade"), "white")
                ax.add_patch(Rectangle((x, ys - 3), w, 6, fc=fc, ec="black", lw=0.6))
                ax.text(x + w / 2, ys, wrap(s["label"], 18), fontsize=6.8, ha="center", va="center", linespacing=1.1)
                bounds.append((x, x + w, s))
                x += w
                if s.get("start_after") and gap:
                    ax.text(x + gap / 2, ys, ck.get("start_label", "start"), fontsize=6.6, ha="center", va="center", color=C["muted"])
                    x += gap
            for i, g in enumerate(ck.get("groups", [])):
                yy = ys - 7 - 4 * i
                col = C["accent"] if g.get("treated") else C["control"]
                ax.text(L - 1, yy, g["label"], fontsize=7, ha="right", va="center", color=col)
                for x0, x1, s in bounds:
                    dashed = bool(g.get("treated") and s.get("treated_dashed"))
                    ax.plot([x0, x1], [yy, yy], color=col, lw=2.2, solid_capstyle="butt", ls=(0, (1, 0.6)) if dashed else "-")
            if ck.get("note"):
                ax.text(60, ys - 7 - 4 * len(ck.get("groups", [])) + 0.8, ck["note"], fontsize=6.5, ha="center", color=C["muted"])
        elif p == "did":
            d = spec["did"]
            head(y - 1.5, let, d.get("title", "The difference in differences, for one outcome and one window"))
            tl, cl = d.get("treated", "Treated"), d.get("control", "Control")
            cells = [("", d.get("before", "Before"), d.get("after", "After"), "Change"),
                     (tl, "$A_0$", "$A_1$", "$A_1 - A_0$"), (cl, "$C_0$", "$C_1$", "$C_1 - C_0$")]
            xs = (14, 32, 46, 62)
            for i, row in enumerate(cells):
                for j, v in enumerate(row):
                    col = C["accent"] if (i, j) == (1, 0) else (C["control"] if (i, j) == (2, 0) else C["ink"])
                    ax.text(xs[j], y - 8 - i * 4, v, fontsize=8, ha="center", va="center", color=col, fontweight="bold" if i == 0 or j == 0 else "normal")
            ax.plot([6, 70], [y - 10, y - 10], color="#adb5bd", lw=0.5)
            ax.text(73, y - 13, r"$\beta = (A_1 - A_0) - (C_1 - C_0)$", fontsize=10, va="center")
            if d.get("example"):
                ax.text(73, y - 17.5, wrap(d["example"], 32), fontsize=6.8, va="center", color=C["muted"], linespacing=1.2)
        elif p == "models":
            head(y - 1.5, let, spec.get("models_title", "The models"))
            for i, m in enumerate(spec["models"]):
                yy = y - 7 - i * 5.2
                ax.text(2, yy, m["eq"], fontsize=9.5, va="center")
                ax.text(52, yy, wrap(m.get("what", ""), 62), fontsize=6.9, va="center", color=C["ink"])
            if spec.get("models_note"):
                ax.text(2, y - 7 - len(spec["models"]) * 5.2 + 1.2, spec["models_note"], fontsize=6.9, va="center", color=C["muted"])
        elif p == "removes":
            head(y - 1.5, let, spec.get("removes_title", "What each piece of the design removes"))
            for i, r in enumerate(spec["removes"]):
                yy = y - 6.5 - i * 3.2
                warn = bool(r.get("left_in"))
                ax.text(2, yy, r["piece"], fontsize=7, va="center", fontweight="bold", color=C["accent"] if warn else C["ink"])
                ax.text(36, yy, wrap(r["removes"], 90), fontsize=7, va="center", color=C["ink"])
        y -= size[p]
    return fig


def timeline(spec, C):
    """The study on one clock (the main kind): A each unit's timeline as bars, the event one grey band through A and B;
    B the periods, with what each window is used for under them; C the comparison as boxes, treated minus control.
    x anchors: left, start (the event begins), end (the event ends), right; or a number 0-1 along the clock."""
    A0 = spec.get("units") or {}
    L, R = 21.0, (84.0 if any(r.get("later") for r in A0.get("rows", [])) else 99.0)   # room for a later event
    ck = spec.get("clock", {})
    X = {"left": L, "start": L + (R - L) * ck.get("start", 0.31), "end": L + (R - L) * ck.get("end", 0.62), "right": R}
    def at(v):
        return X[v] if isinstance(v, str) else L + (R - L) * float(v)
    A, B, Cc = spec.get("units"), spec.get("periods"), spec.get("comparison")
    nr = (wrap(A["rule"], 95).count("\n") + 1) if A and A.get("rule") else 0
    hA = (14 + 4.5 * len(A["rows"]) + (2.2 * nr + 1.5 if nr else 0)) if A else 0
    nb = max([wrap(sp["label"], 40).count("\n") + 1 for sp in B.get("spans_below", [])] or [0]) if B else 0
    hB = (20 + 2.6 * nb) if B else 0
    hC = 22 if Cc else 0
    total = hA + hB + hC
    fig, ax = setup(6.8, 0.07 * total + 0.3)
    ax.set_ylim(100 - total, 100)
    FS = 8
    let = iter("ABC")

    def head(y, name):                    # a white strip, so the event band and its lines never cross a panel header
        ax.add_patch(Rectangle((0, y - 2.6), 100, 5.4, fc="white", ec="none", zorder=6))
        ax.text(0.6, y, next(let), fontsize=8.5, fontweight="bold", va="center", zorder=7, bbox=dict(boxstyle="square,pad=0.25", fc="white", ec="black", lw=0.7))
        ax.text(4, y, name, fontsize=9, fontweight="bold", va="center", zorder=7)
        ax.plot([0, 100], [y - 2.6, y - 2.6], color="black", lw=0.6, zorder=7)

    def span(y, x0, x1, txt, above=True):
        ax.annotate("", xy=(x0, y), xytext=(x1, y), arrowprops=dict(arrowstyle="<->", lw=0.7, shrinkA=0, shrinkB=0), zorder=4)
        ax.text((x0 + x1) / 2, y + (0.6 if above else -1.2), wrap(txt, 40), fontsize=FS - 0.5, ha="center", va="bottom" if above else "top", linespacing=1.1)

    y = 99.5
    band_top = band_bottom = None
    if A:
        head(y - 1.5, A.get("title", "Units"))
        ya = y - 9
        for sp in A.get("spans_above", []):
            span(ya, at(sp["from"]), at(sp["to"]), sp["label"])
        if A.get("event_label"):
            ax.text((X["start"] + X["end"]) / 2, ya + 0.6, wrap(A["event_label"], 22), fontsize=FS - 0.5, ha="center", va="center", linespacing=1.05)
        band_top = ya + 3.5
        for i, r in enumerate(A["rows"]):
            yy = ya - 6 - 4.5 * i
            ax.text(L - 1, yy, r["label"], fontsize=FS, ha="right", va="center")
            col = C["accent"] if r.get("treated") else C["control"]
            parts = [(L, X["start"]), (X["end"], R)] if r.get("gap") else [(L, R)]
            for x0, x1 in parts:
                ax.add_patch(Rectangle((x0, yy - 1.6), x1 - x0, 3.2, fc=col, ec="none", zorder=3))
            if r.get("later"):                    # a control's own event after the window: time skip, its own gap, the bar again
                ax.plot([R + 0.3, R + 1.8], [yy, yy], color=col, lw=1.0, ls=(0, (1, 1)))
                ax.add_patch(Rectangle((R + 1.8, yy - 2.0), 1.4, 4.0, fc=C["event"], ec="none", zorder=2))
                ax.add_patch(Rectangle((R + 3.2, yy - 1.6), 1.2, 3.2, fc=col, ec="none", zorder=3))
                ax.text(R + 4.9, yy, wrap(r["later"], 14), fontsize=FS - 1.6, color=C["ink"], ha="left", va="center", linespacing=1.0)
        if A.get("rule"):
            ax.text(L, ya - 6 - 4.5 * (len(A["rows"]) - 1) - 3.2, wrap(A["rule"], 95), fontsize=FS - 1, color=C["ink"], va="top", linespacing=1.15,
                    zorder=7, bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="none"))
        y -= hA
    if B:
        head(y - 1.5, B.get("title", "Periods"))
        yb, h = y - 11, 7
        ax.text(L - 1, yb, B.get("axis", "Period"), fontsize=FS, ha="right", va="center")
        x0 = L
        for sgm in B["segments"]:
            x1 = at(sgm["to"])
            fc = {"run_up": C["run_up"], "event": "none"}.get(sgm.get("shade"), "white")
            ax.add_patch(Rectangle((x0, yb - h / 2), x1 - x0, h, fc=fc, ec="black", lw=0.7, zorder=3))
            ax.text((x0 + x1) / 2, yb, wrap(sgm["label"], max(8, int((x1 - x0) * 0.95))), fontsize=FS - 0.5, ha="center", va="center", linespacing=1.05, zorder=4)
            x0 = x1
        for sp in B.get("spans_below", []):
            span(yb - 7, at(sp["from"]), at(sp["to"]), sp["label"], above=False)
        band_bottom = yb - h / 2
        y -= hB
    if band_top is not None:
        bottom = band_bottom if band_bottom is not None else band_top - hA + 4
        ax.add_patch(Rectangle((X["start"], bottom), X["end"] - X["start"], band_top - bottom, fc=C["event"], ec="none", zorder=0))
        for x in (X["start"], X["end"]):
            ax.plot([x, x], [bottom, band_top], color="black", lw=0.8, ls=(0, (3, 2)), zorder=5)
    if Cc:
        head(y - 1.5, Cc.get("title", "Comparison"))
        yc = y - 12
        box = dict(boxstyle="round,pad=0.45", fc="white", lw=0.8)
        ax.text(21, yc, wrap(Cc["treated"], 34), fontsize=FS - 0.3, ha="center", va="center", bbox=dict(box, ec=C["accent"]), linespacing=1.15)
        ax.text(42, yc, "−", fontsize=13, ha="center", va="center")
        ax.text(62.5, yc, wrap(Cc["control"], 44), fontsize=FS - 0.3, ha="center", va="center", bbox=dict(box, ec=C["control"]), linespacing=1.15)
        ax.text(83, yc, "=", fontsize=11, ha="center", va="center")
        ax.text(93, yc, wrap(Cc.get("result", "Difference"), 22), fontsize=FS - 0.3, ha="center", va="center", linespacing=1.15)
        if Cc.get("note"):
            ax.text(50, yc - 9, Cc["note"], fontsize=FS - 0.5, ha="center", va="center")
    return fig


def method_md(spec, out):
    """method.md for build_preview.py, its parts in its order: Message, Data, Sample, Method, Outcomes, Made by, Numbers.
    Each comes from the spec's key of the same name (lower case); a part the spec leaves out says so, so the gap shows."""
    lines = [f"# {spec.get('title', 'Method display')}", ""]
    for part in ("Message", "Data", "Sample", "Method", "Outcomes", "Made by", "Numbers"):
        v = spec.get(part.lower().replace(" ", "_"))
        if part == "Method":
            v = (str(v).strip() + " " if v else "") + (f"Drawn by haipipe-display-method scripts/method_display.py from its spec "
                                                       f"(kind: {spec['kind']})" + ("; example rows are made up." if spec["kind"] == "workflow" else "."))
        lines += [f"## {part}", "", str(v).strip() if v else f"(not in the spec: add `{part.lower().replace(' ', '_')}:`)", ""]
    (out / "method.md").write_text("\n".join(lines))


def float_tex(spec, out):
    """float.tex, the display as a paper inputs it, so build_preview.py can make preview.pdf from this folder."""
    esc = lambda t: str(t).replace("\\", "/").replace("&", "\\&").replace("%", "\\%").replace("_", "\\_").replace("#", "\\#")
    label = spec.get("label", "fig:method")
    note = spec.get("legend", "")
    (out / "float.tex").write_text("% GENERATED by haipipe-display-method method_display.py; edit the spec, then rerun\n"
                                   "\\begin{figure}[htbp]\n\\centering\n\\caption{" + esc(spec.get("title", "Method")) + "}\n"
                                   "\\label{" + label + "}\n\\includegraphics[width=\\linewidth,height=0.75\\textheight,keepaspectratio]{figure.pdf}\n"
                                   + ("\\begin{flushleft}\\footnotesize " + esc(note) + "\\end{flushleft}\n" if note else "")
                                   + "\\end{figure}\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("spec")
    ap.add_argument("out")
    ap.add_argument("--colours", help="the paper's or report's colour-scheme.yaml")
    a = ap.parse_args(argv)
    spec = yaml.safe_load(Path(a.spec).read_text())
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    C = colours(a.colours or spec.get("colours"))
    kind = spec.get("kind")
    draw = {"timeline": timeline, "workflow": workflow, "design": design}.get(kind)
    if draw is None:
        sys.exit(f"kind must be timeline, workflow or design, not {kind!r}")
    fig = draw(spec, C)
    fig.savefig(out / "figure.pdf", bbox_inches="tight")
    fig.savefig(out / "figure.png", dpi=200, bbox_inches="tight")
    method_md(spec, out)
    float_tex(spec, out)
    print(f"drew {kind} -> {out}: figure.pdf, figure.png, float.tex, method.md (next: build_preview.py {out})")


if __name__ == "__main__":
    main()

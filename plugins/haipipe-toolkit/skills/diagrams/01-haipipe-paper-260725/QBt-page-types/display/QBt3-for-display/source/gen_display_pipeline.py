#!/usr/bin/env python
"""Figure 1: how a display unit is produced and who is allowed to do each step.

PARSE-not-recompute, the same discipline the live units run under: every box,
every label and every actor mark is read at runtime from `source_data.csv`.
Nothing about the pipeline is hardcoded here except the lane order, which is
the axis.

WHY THIS FIGURE AND NOT A FABRICATED RESULT. This unit sits in a specimen
group, so any "finding" it drew would be invented, and a reader would be asked
to accept a picture of numbers that were never measured. The pipeline is not
invented: it is the one this unit itself came out of, and the reader can check
every claim in it against the folder next to the page. A specimen whose figure
is TRUE is worth more than one whose figure is merely well-formatted.

The figure contains ONLY: four lane labels, one box per step with its artifact
underneath, an actor mark per box, and the arrows between them. No title and no
source line are baked into the image; both belong to the LaTeX \\caption.

    python3 source/gen_display_pipeline.py                 -> assets/figure.{pdf,png}
    python3 source/gen_display_pipeline.py --candidate A   -> candidates/A-narrow.{pdf,png}

CANDIDATE MODE draws the SAME data at the first cut's geometry, 7.4 by 3.9
inches. It is kept because it is the option that lost and the reason it lost is
inspectable: at that width the longest artifact string runs past its own box and
the entire third column falls outside the axis. A losing candidate that has been
deleted is a design decision nobody can re-check, so `for-design` keeps it.
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from paper_plot_style import plt                                   # noqa: E402

LANES = ["ASK", "MAKE", "BUILD", "ACCEPT"]
# A person's step and a script's step are drawn differently on purpose: the
# whole acceptance ladder rests on which is which, and a legend the reader has
# to consult is one indirection too many.
FILL = {"person": "#ffffff", "script": "#eceff4"}
EDGE = {"person": "#1f2933", "script": "#7b8794"}


def rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        out = list(csv.DictReader(fh))
    missing = [c for c in ("lane", "order", "label", "artifact", "actor")
               if out and c not in out[0]]
    if missing:
        sys.exit(f"source_data.csv is missing column(s): {', '.join(missing)}")
    bad = sorted({r["lane"] for r in out} - set(LANES))
    if bad:
        sys.exit(f"source_data.csv names lane(s) the figure has no axis for: {bad}")
    return out


def main():
    data = rows(os.path.join(HERE, "source_data.csv"))
    by_lane = {ln: sorted((r for r in data if r["lane"] == ln),
                          key=lambda r: int(r["order"])) for ln in LANES}
    width = max(len(v) for v in by_lane.values())

    # WIDTH AND LIMITS ARE MEASURED, NOT GUESSED. The first cut was 7.4in with
    # `xlim` ending at `width + 0.15`: the third column fell OUTSIDE the axis
    # and was clipped, and the longest artifact string ran past its own box. A
    # figure whose own labels do not fit is the first thing a reader distrusts.
    narrow = "--candidate" in sys.argv
    fig, ax = plt.subplots(figsize=(7.4, 3.9) if narrow else (9.6, 4.2))
    ax.set_xlim(-0.55 if narrow else -0.62,
                width + (0.15 if narrow else 0.42))
    ax.set_ylim(-0.6, len(LANES) - 0.25)
    ax.axis("off")

    bw, bh = 0.86, 0.5
    for li, lane in enumerate(LANES):
        y = len(LANES) - 1 - li
        ax.text(-0.5, y, lane, ha="left", va="center", weight="bold",
                fontsize=9.5, color="#1f2933")
        steps = by_lane[lane]
        for si, r in enumerate(steps):
            x = si + 0.35
            ax.add_patch(plt.Rectangle((x, y - bh / 2), bw, bh,
                                       facecolor=FILL[r["actor"]],
                                       edgecolor=EDGE[r["actor"]],
                                       linewidth=1.1, zorder=2))
            mark = "person" if r["actor"] == "person" else "script"
            ax.text(x + bw / 2, y + 0.10, r["label"], ha="center", va="center",
                    fontsize=7.4, color="#1f2933", zorder=3)
            ax.text(x + bw / 2, y - 0.055, r["artifact"], ha="center",
                    va="center", fontsize=5.4, color="#52606d",
                    family="monospace", zorder=3)
            ax.text(x + bw / 2, y - 0.185, mark, ha="center", va="center",
                    fontsize=5.6, color=EDGE[r["actor"]], style="italic",
                    zorder=3)
            if si + 1 < len(steps):
                ax.annotate("", xy=(x + bw + 0.13, y), xytext=(x + bw + 0.005, y),
                            arrowprops=dict(arrowstyle="-|>", color="#7b8794",
                                            linewidth=0.9))
        if li + 1 < len(LANES):
            ax.annotate("", xy=(0.35 + bw / 2, y - 0.66), xytext=(0.35 + bw / 2, y - bh / 2 - 0.02),
                        arrowprops=dict(arrowstyle="-|>", color="#7b8794",
                                        linewidth=0.9))

    ax.text(width + 0.38, -0.45,
            "white = a person must do it   ·   grey = a script does it",
            ha="right", va="center", fontsize=6.4, color="#52606d")

    if narrow:
        out_dir, stem = os.path.join(UNIT, "candidates"), "A-narrow"
    else:
        out_dir, stem = os.path.join(UNIT, "assets"), "figure"
    os.makedirs(out_dir, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(out_dir, f"{stem}.{ext}"))
    print(f"{len(data)} steps across {len(LANES)} lanes "
          f"-> {os.path.basename(out_dir)}/{stem}.pdf + {stem}.png")


if __name__ == "__main__":
    main()

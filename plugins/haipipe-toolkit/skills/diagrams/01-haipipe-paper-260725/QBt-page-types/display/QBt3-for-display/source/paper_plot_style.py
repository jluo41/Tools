"""Shared publication plot style (haipipe-paper-display-figure).

Used by gen_discretion_gradient.py. Clean print-friendly serif defaults; no
titles baked into figures (titles -> LaTeX \\caption only).
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

FONT_SIZE = 10
DPI = 300

matplotlib.rcParams.update({
    "font.size": FONT_SIZE,
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "axes.labelsize": FONT_SIZE,
    "axes.titlesize": FONT_SIZE + 1,
    "xtick.labelsize": FONT_SIZE - 1,
    "ytick.labelsize": FONT_SIZE - 1,
    "legend.fontsize": FONT_SIZE - 1,
    "figure.dpi": DPI,
    "savefig.dpi": DPI,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "axes.grid": False,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "text.usetex": False,
    "mathtext.fontset": "stix",
})

# Significance-keyed colors (colorblind-safe enough; distinguishable in gray).
SIG = "#b3402f"   # filled marker, significant
NS = "#9aa0a6"    # hollow marker, not significant

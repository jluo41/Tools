"""figures.py · the figures and plain lead lines a run's report shows, drawn from its result tables.

Called by run_question.py after the spec gate passes (ref/block-contract.md § The run). A figure
reads only a result table the spec names, never the extract's rows, so a cell the script hid stays
hidden and a figure can be redrawn from results/ alone. A table is recognised by its columns, so
one function serves every question that writes that shape:

  rates     level, rate_pct, ci_lo_pct, ci_hi_pct   one dot and its 95% bar per level (a line and
                                                    band when the levels are numbers), a panel per outcome
  grid      experiment_config, _g_<x>, rate_pct     message x level heatmap: each cell's rate minus
                                                    its level's mean, hidden cells left blank
  stab      level, spearman_vs_pooled, leader_...   agreement with the pooled order per level, a real
                                                    leader change (disjoint intervals) marked
  balance   experiment_config, max_dev_pp           each message's worst balance across levels
  missing   column, null_pct                        share missing per column, sorted
  share     level, share_pct                        each level's share of rows
  estimate  <x>, <..lo..>, <..hi..> (adjacent)       a forest plot per estimate with its interval (a
                                                    zero line for a gap, gain, effect or drop): the
                                                    shape of most Knowledge tests

A need may also declare its own figures (`figures:` in the question file, block-contract.md § The question
file): kind line, bar, forest or heat over one of its output tables; those are drawn first, then any
known shape. A table of no known shape and no declared figure gets no figure and no lead line. Same message, same colour, in every
figure (sorted names). The PNG carries no timestamp, so a rerun on the same tables writes the same
bytes. Generated files are never edited by hand (AGENTS.md rule 0): rerun the ticket.
"""
import math
from pathlib import Path

import pandas as pd

DPI = 110
MAX_LEVELS = 30                       # a rates table with more levels shows its 30 largest by n
MAX_PANELS = 4                        # a rates table shows its first 4 outcomes
PALETTE = ["#3e5c84", "#c0504d", "#5b9b5b", "#d08c2a", "#7d5ba6", "#2a9bb0", "#b05b8c",
           "#8c8c3a", "#5b6fc0", "#c07a5b", "#4f8f7f", "#9b5b5b", "#6b6b6b", "#a0a03c"]


def shape(df):
    c = set(df.columns)
    if {"experiment_config", "rate_pct"} <= c and any(x.startswith("_g_") for x in c):
        return "grid"
    if {"level", "spearman_vs_pooled", "leader_changed"} <= c:
        return "stab"
    if {"experiment_config", "max_dev_pp"} <= c and len(c) == 2:
        return "balance"
    if {"rate_pct", "ci_lo_pct", "ci_hi_pct"} <= c and ({"level"} & c or {"outcome"} & c):
        return "rates"
    if {"column", "null_pct"} <= c:
        return "missing"
    if {"level", "share_pct"} <= c:
        return "share"
    if _triples(df):
        return "estimate"
    return ""


def _triples(df):
    """(estimate, lo, hi) column triples: a numeric column followed by its interval's low and high."""
    cols, out = list(df.columns), []
    for i in range(len(cols) - 2):
        e, lo, hi = cols[i:i + 3]
        if ("lo" in lo.lower() and "hi" in hi.lower() and "lo" not in e.lower() and "hi" not in e.lower()
                and all(pd.api.types.is_numeric_dtype(df[c]) for c in (e, lo, hi))):
            out.append((e, lo, hi))
    return out[:3]


def _row_labels(df):
    text = [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c]) and c not in ("readable", "suppressed")]
    if not text:
        return [str(i + 1) for i in range(len(df))]
    return [" · ".join(x for x in (_label(v) for v in r) if x) or "-" for r in df[text[:2]].itertuples(index=False)]


def _readable(df):
    return df[~df["readable"].astype(str).str.lower().eq("false")] if "readable" in df else df


def _centred(name):
    return any(w in name.lower() for w in ("gap", "gain", "effect", "drop", "diff", "_pp"))


def _label(v):
    """15.0 → 15; a long label is cut."""
    if isinstance(v, float) and math.isnan(v):
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    s = str(v)
    return s if len(s) <= 28 else s[:27] + "…"


def _numeric(levels):
    try:
        [float(x) for x in levels]
        return len(levels) > 3
    except (TypeError, ValueError):
        return False


def _shown(df):
    return df[~df["suppressed"].astype(str).str.lower().eq("true")] if "suppressed" in df else df


def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                         "svg.hashsalt": "insight", "figure.dpi": DPI})
    return plt


def _save(fig, path):
    import warnings
    if not getattr(fig, "_placed", False):        # a figure that placed its own parts (a heat's colour bar) keeps them
        top = 1 - 0.6 / fig.get_size_inches()[1] if fig._suptitle is not None else 1
        with warnings.catch_warnings():           # a long label may not fit tight; the bbox below makes room
            warnings.simplefilter("ignore", UserWarning)
            fig.tight_layout(rect=[0, 0, 1, top])  # room for the title above the first panel
    fig.savefig(path, dpi=DPI, metadata={"Software": None}, bbox_inches="tight", pad_inches=0.15)
    import matplotlib.pyplot as plt
    plt.close(fig)


def _colour(names):
    return {n: PALETTE[i % len(PALETTE)] for i, n in enumerate(sorted(map(str, names)))}


# ── one function per shape: draw(df, path, title) and lead(df) ────────────────
def _rates_draw(df, path, title):
    plt = _plt()
    d = _shown(df)
    outcomes = list(dict.fromkeys(d["outcome"])) if "outcome" in d and "level" in d else [None]
    outcomes = outcomes[:MAX_PANELS]
    cols = min(2, len(outcomes))
    rows = math.ceil(len(outcomes) / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(4.6 * cols + 0.6, 3.4 * rows), squeeze=False)
    for ax in axes.flat[len(outcomes):]:
        ax.set_visible(False)
    for ax, oc in zip(axes.flat, outcomes):
        s = d if oc is None else d[d["outcome"] == oc]
        key = "level" if "level" in s else "outcome"
        if len(s) > MAX_LEVELS and "n" in s:
            s = s.nlargest(MAX_LEVELS, "n")
        levels = list(s[key])
        if key == "level" and _numeric(levels):
            s = s.assign(_x=s[key].astype(float)).sort_values("_x")
            x, r = s["_x"].to_numpy(float), s["rate_pct"].to_numpy(float)
            ax.fill_between(x, s["ci_lo_pct"].to_numpy(float), s["ci_hi_pct"].to_numpy(float),
                            color="#3e5c84", alpha=.18, lw=0)
            ax.plot(x, r, "o-", color="#3e5c84", ms=3, lw=1.2)
            ax.set_xlabel(key)
        else:
            y = range(len(s))[::-1]
            r, lo, hi = (s[c].to_numpy(float) for c in ("rate_pct", "ci_lo_pct", "ci_hi_pct"))
            ax.errorbar(r, list(y), xerr=[r - lo, hi - r], fmt="o", color="#3e5c84", ms=4, capsize=2, lw=1)
            ax.set_yticks(list(y))
            ax.set_yticklabels([_label(v) for v in s[key]], fontsize=8)
        ax.set_title(str(oc) if oc else "", fontsize=9)
        ax.set_ylabel("" if key != "level" or not _numeric(levels) else "rate %")
        if not (key == "level" and _numeric(levels)):
            ax.set_xlabel("rate %  (95% interval)")
        ax.grid(axis="x" if not (key == "level" and _numeric(levels)) else "y", color="#e4e4e7", lw=.6)
    fig.suptitle(title, fontsize=10, x=0.01, ha="left")
    _save(fig, path)


def _rates_lead(df):
    d = _shown(df)
    hidden = len(df) - len(d)
    out = []
    if "level" in d and "outcome" in d:
        for oc in list(dict.fromkeys(d["outcome"]))[:MAX_PANELS]:
            s = d[d["outcome"] == oc]
            if len(s) < 2:
                continue
            hi, lo = s.loc[s["rate_pct"].idxmax()], s.loc[s["rate_pct"].idxmin()]
            out.append(f"{oc}: highest {_label(hi['level'])} at {hi['rate_pct']:.1f}%, lowest {_label(lo['level'])} "
                       f"at {lo['rate_pct']:.1f}%, a spread of {hi['rate_pct'] - lo['rate_pct']:.1f} points "
                       f"over {len(s)} levels")
    elif "outcome" in d:
        out.append("; ".join(f"{r.outcome} {r.rate_pct:.1f}%" for r in d.itertuples()))
    if hidden:
        out.append(f"{hidden} cells hidden (below the floor)")
    return out


def _grid_draw(df, path, title):
    plt = _plt()
    g = next(c for c in df.columns if c.startswith("_g_"))
    d = df.copy()
    d.loc[d.get("suppressed", pd.Series(False, index=d.index)).astype(str).str.lower().eq("true"), "rate_pct"] = float("nan")
    m = d.pivot_table(index="experiment_config", columns=g, values="rate_pct", aggfunc="first", dropna=False)
    m = m.sub(m.mean(axis=0), axis=1)
    m = m.loc[sorted(m.index, key=str)]
    if m.shape[1] > MAX_LEVELS:
        m = m.iloc[:, :MAX_LEVELS]
    lim = max(1.0, float(abs(m).max().max()) if m.notna().any().any() else 1.0)
    fig, ax = plt.subplots(figsize=(min(1.0 + 0.55 * m.shape[1], 14), 0.9 + 0.32 * m.shape[0]))
    im = ax.imshow(m.to_numpy(dtype=float), cmap="RdBu", vmin=-lim, vmax=lim, aspect="auto")
    ax.set_xticks(range(m.shape[1]))
    ax.set_xticklabels([_label(v) for v in m.columns], rotation=45 if m.shape[1] > 8 else 0, ha="right" if m.shape[1] > 8 else "center", fontsize=8)
    ax.set_yticks(range(m.shape[0]))
    ax.set_yticklabels([_label(v) for v in m.index], fontsize=8)
    ax.set_xlabel(g[3:])
    ax.spines[:].set_visible(False)
    fig.colorbar(im, ax=ax, fraction=.03, pad=.02).set_label("rate minus the level's mean, points", fontsize=8)
    ax.set_title(title, fontsize=10, loc="left")
    _save(fig, path)


def _grid_lead(df):
    g = next(c for c in df.columns if c.startswith("_g_"))
    d = _shown(df)
    hidden = len(df) - len(d)
    lead = d.loc[d.groupby(g)["rate_pct"].idxmax()]
    leaders = lead["experiment_config"].nunique()
    return [f"{df['experiment_config'].nunique()} messages across {df[g].nunique()} levels of {g[3:]}; "
            f"{leaders} different message{'s' if leaders != 1 else ''} lead{'' if leaders != 1 else 's'} a level"
            + (f"; {hidden} cells hidden" if hidden else "")]


def _stab_draw(df, path, title):
    plt = _plt()
    d = df[df["readable"].astype(str).str.lower().eq("true")] if "readable" in df else df
    fig, ax = plt.subplots(figsize=(6.2, 0.9 + 0.26 * max(len(d), 2)))
    real = _real_change(d)
    y = list(range(len(d)))[::-1]
    ax.barh(y, d["spearman_vs_pooled"].to_numpy(float), color=["#c0504d" if r else "#9fb3cc" for r in real], height=.6)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{_label(l)} · {ld}" for l, ld in zip(d["level"], d["leader"])], fontsize=8)
    ax.set_xlim(min(-0.1, float(d["spearman_vs_pooled"].min()) - .05) if len(d) else -0.1, 1.0)
    ax.set_xlabel("rank agreement with the pooled order (Spearman)   red: the leader really changes")
    ax.set_title(title, fontsize=10, loc="left")
    _save(fig, path)


def _real_change(d):
    """A level whose leader is not the pooled leader AND whose lead's intervals are disjoint."""
    changed = d["leader_changed"].astype(str).str.lower().eq("true")
    disjoint = d["lead_ci_disjoint"].astype(str).str.lower().eq("true") if "lead_ci_disjoint" in d else False
    return changed & disjoint


def _stab_lead(df):
    d = df[df["readable"].astype(str).str.lower().eq("true")] if "readable" in df else df
    changed = d["leader_changed"].astype(str).str.lower().eq("true").sum()
    real = int(_real_change(d).sum())
    low = d["spearman_vs_pooled"].min() if len(d) else float("nan")
    return [f"the leader differs from the pooled leader in {changed} of {len(d)} readable levels, "
            f"and the change is real (intervals disjoint) in {real}; the lowest rank agreement is {low:.2f}"]


def _balance_draw(df, path, title):
    plt = _plt()
    d = df.sort_values("experiment_config", key=lambda s: s.astype(str))
    col = _colour(d["experiment_config"])
    fig, ax = plt.subplots(figsize=(6.2, 0.9 + 0.26 * max(len(d), 2)))
    y = list(range(len(d)))[::-1]
    ax.barh(y, d["max_dev_pp"].to_numpy(float), color=[col[str(m)] for m in d["experiment_config"]], height=.6)
    ax.set_yticks(y)
    ax.set_yticklabels([_label(m) for m in d["experiment_config"]], fontsize=8)
    ax.set_xlabel("largest share difference from the other messages, points")
    ax.set_title(title, fontsize=10, loc="left")
    _save(fig, path)


def _balance_lead(df):
    r = df.loc[df["max_dev_pp"].idxmax()]
    return [f"the largest imbalance is {r['max_dev_pp']:.1f} points ({_label(r['experiment_config'])})"]


def _missing_draw(df, path, title):
    plt = _plt()
    d = df.sort_values("null_pct")
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.bar(range(len(d)), d["null_pct"].to_numpy(float), color="#3e5c84", width=1.0)
    ax.set_xticks([])
    ax.set_xlabel(f"{len(d)} columns, sorted")
    ax.set_ylabel("missing %")
    ax.set_ylim(0, 100)
    ax.set_title(title, fontsize=10, loc="left")
    _save(fig, path)


def _missing_lead(df):
    p = df["null_pct"]
    return [f"{int((p == 0).sum())} of {len(p)} columns complete, {int(((p > 0) & (p < 50)).sum())} partly, "
            f"{int(((p >= 50) & (p < 100)).sum())} mostly missing, {int((p == 100).sum())} empty"]


def _share_draw(df, path, title):
    plt = _plt()
    d = _shown(df)
    if len(d) > MAX_LEVELS:
        d = d.nlargest(MAX_LEVELS, "share_pct")
    fig, ax = plt.subplots(figsize=(6.2, 0.9 + 0.26 * max(len(d), 2)))
    y = list(range(len(d)))[::-1]
    ax.barh(y, d["share_pct"].to_numpy(float), color="#3e5c84", height=.6)
    ax.set_yticks(y)
    ax.set_yticklabels([_label(v) for v in d["level"]], fontsize=8)
    ax.set_xlabel("share of rows %")
    ax.set_title(title, fontsize=10, loc="left")
    _save(fig, path)


def _share_lead(df):
    d = _shown(df)
    r = d.loc[d["share_pct"].idxmax()] if len(d) else None
    return [f"{len(d)} levels; the largest is {_label(r['level'])} at {r['share_pct']:.1f}%"] if r is not None else []


def _estimate_draw(df, path, title):
    plt = _plt()
    d = _readable(df)
    d = d.dropna(subset=[_triples(d)[0][0]]) if _triples(d) else d
    if len(d) > MAX_LEVELS:
        d = d.head(MAX_LEVELS)
    labels, triples = _row_labels(d), _triples(d)
    fig, axes = plt.subplots(1, len(triples), figsize=(4.4 * len(triples) + 1.6, 0.9 + 0.3 * max(len(d), 2)),
                             squeeze=False, sharey=True)
    y = list(range(len(d)))[::-1]
    for ax, (e, lo, hi) in zip(axes[0], triples):
        v, a, b = (d[c].to_numpy(float) for c in (e, lo, hi))
        ax.errorbar(v, y, xerr=[v - a, b - v], fmt="o", color="#3e5c84", ms=4, capsize=2, lw=1)
        if _centred(e):
            ax.axvline(0, color="#c0504d", lw=.8, ls="--")
        ax.set_xlabel(f"{e}  (interval {lo} to {hi})", fontsize=8)
        ax.grid(axis="x", color="#e4e4e7", lw=.6)
    axes[0][0].set_yticks(y)
    axes[0][0].set_yticklabels(labels, fontsize=8)
    fig.suptitle(title, fontsize=10, x=0.01, ha="left")
    _save(fig, path)


def _estimate_lead(df):
    d, out = _readable(df), []
    d = d.dropna(subset=[_triples(d)[0][0]]) if _triples(d) else d
    labels = _row_labels(d)
    for e, lo, hi in _triples(d):
        if len(d) <= 3:
            out.append("; ".join(f"{e} {r[e]:.2f} ({r[lo]:.2f} to {r[hi]:.2f})" + (f" for {l}" if len(d) > 1 else "")
                                 for l, (_, r) in zip(labels, d.iterrows())))
        elif _centred(e):
            clear = int(((d[lo] > 0) | (d[hi] < 0)).sum())
            out.append(f"{e}: {clear} of {len(d)} intervals exclude zero")
        else:
            i, j = d[e].idxmax(), d[e].idxmin()
            out.append(f"{e}: highest {labels[list(d.index).index(i)]} at {d.loc[i, e]:.2f}, "
                       f"lowest {labels[list(d.index).index(j)]} at {d.loc[j, e]:.2f}")
    if len(d) < len(df):
        out.append(f"{len(df) - len(d)} rows not readable or not estimable, left out")
    return out


# ── declared figures: a need names its own (JL 261011: "I didn't see much tables and figures") ──
def _cols(v):
    return [v] if isinstance(v, str) else list(v or [])


def _declared_draw(df, spec, path, title):
    """One figure a need declares under `figures:`, drawn from its result table only.

    kind line    x, y (one or a list), band [lo, hi], group (a line per value), facet (a panel per value)
    kind bar     x, y (one or a list: bars side by side), group, facet
    kind forest  label (one or a list of columns), x, lo, hi: a dot and its interval per row, a zero line
                 (zero: false drops it)
    kind heat    x, y, value: a grid of value by x and y (facet: a grid per value, one colour scale; cmap, clabel)
    kind strip   y, start, end, group: a row per y (a day), a bar from start to end per row (an instant: a mark),
                 a colour per group; xmin, xmax, xstep (hours by default)
    every kind   hline [values] (reference lines), vline [values], ylabel, xlabel, title; sharex (bar panels
                 keep their own x by default, line panels share it)
    """
    plt = _plt()
    kind = spec.get("kind", "line")
    facets = sorted(df[spec["facet"]].dropna().unique(), key=str) if spec.get("facet") else [None]
    if kind == "forest":
        d = df.dropna(subset=[spec["x"]])
        labels = [" · ".join(_label(v) for v in r) for r in d[_cols(spec["label"])].itertuples(index=False)]
        fig, ax = plt.subplots(figsize=(6.4, 0.9 + 0.32 * max(len(d), 2)))
        y = list(range(len(d)))[::-1]
        v, a, b = (d[c].to_numpy(float) for c in (spec["x"], spec["lo"], spec["hi"]))
        ax.errorbar(v, y, xerr=[v - a, b - v], fmt="o", color=PALETTE[0], ms=4, capsize=2, lw=1)
        if spec.get("zero", True):
            ax.axvline(0, color="#c0504d", lw=.8, ls="--")
        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=8)
        ax.set_xlabel(spec.get("xlabel") or f"{spec['x']}  ({spec['lo']} to {spec['hi']})", fontsize=8)
        ax.grid(axis="x", color="#e4e4e7", lw=.6)
        axes = [ax]
    elif kind == "strip":                              # a row per y (a day), a bar per row from start to end
        rows = sorted(df[spec["y"]].dropna().unique(), key=str)
        groups = sorted(df[spec["group"]].dropna().unique(), key=str) if spec.get("group") else [None]
        colour = _colour(groups)
        fig, ax = plt.subplots(figsize=(9.5, 0.9 + 0.42 * max(len(rows), 2)))
        ypos = {r: len(rows) - 1 - i for i, r in enumerate(rows)}
        lanes = {g: k for k, g in enumerate(groups)}
        h = 0.8 / max(len(groups), 1)
        for g in groups:
            part = df if g is None else df[df[spec["group"]] == g]
            for _, r in part.iterrows():
                y = ypos[r[spec["y"]]] - 0.4 + h * lanes[g] + h / 2
                a, b = float(r[spec["start"]]), float(r[spec["end"]])
                if b - a < 0.05:                       # an instant: a mark, not a bar
                    ax.plot([a], [y], marker="|", ms=9, mew=2, color=colour[str(g)])
                else:
                    ax.broken_barh([(a, b - a)], (y - h / 2, h * 0.9), color=colour[str(g)])
            ax.plot([], [], color=colour[str(g)], lw=6, label=_label(g) if g is not None else None)
        ax.set_yticks([ypos[r] for r in rows])
        ax.set_yticklabels([_label(r) for r in rows], fontsize=8)
        ax.set_xlim(spec.get("xmin", 0), spec.get("xmax", 24))
        ax.set_xticks(range(int(spec.get("xmin", 0)), int(spec.get("xmax", 24)) + 1, int(spec.get("xstep", 2))))
        ax.grid(axis="x", color="#e4e4e7", lw=.6)
        ax.set_axisbelow(True)
        ax.set_xlabel(spec.get("xlabel") or "hour of day", fontsize=8)
        if len(groups) > 1:
            ax.legend(fontsize=7, frameon=False, ncol=min(5, len(groups)), loc="upper center", bbox_to_anchor=(0.5, -0.12))
        axes = [ax]
    elif kind == "heat":                               # a panel per facet value, one shared colour scale
        mats = [df if fv is None else df[df[spec["facet"]] == fv] for fv in facets]
        mats = [d.pivot_table(index=spec["y"], columns=spec["x"], values=spec["value"], aggfunc="mean") for d in mats]
        lo = min(float(m.min().min()) for m in mats)
        hi = max(float(m.max().max()) for m in mats)
        w, h = max(m.shape[1] for m in mats), max(max(m.shape[0], 2) for m in mats)
        fig, axs = plt.subplots(len(mats), 1, figsize=(min(1.6 + 0.32 * w, 11), (0.7 + 0.3 * h) * len(mats) + 0.4),
                                squeeze=False)
        axes = [a[0] for a in axs]
        for ax, m, fv in zip(axes, mats, facets):
            import numpy as np
            import matplotlib
            cmap = matplotlib.colormaps[spec.get("cmap", "YlOrRd")].copy()
            cmap.set_bad("#d4d4d8")                     # no cell at all (outside the window): grey, never read as 0
            im = ax.imshow(np.ma.masked_invalid(m.to_numpy(dtype=float)), cmap=cmap, aspect="auto", vmin=lo, vmax=hi)
            ax.set_xticks(range(m.shape[1]))
            ax.set_xticklabels([_label(c) for c in m.columns], fontsize=7)
            ax.set_yticks(range(m.shape[0]))
            ax.set_yticklabels([_label(i) for i in m.index], fontsize=7)
            if fv is not None:
                ax.set_title(str(fv), fontsize=9, loc="left")
        h = fig.get_size_inches()[1]
        fig.subplots_adjust(left=0.12, right=0.86, top=1 - 0.9 / h, bottom=0.3 / h, hspace=0.45)
        cax = fig.add_axes([0.89, 0.25, 0.018, 0.5])            # the colour bar beside the panels, never on them
        fig.colorbar(im, cax=cax, label=spec.get("clabel") or spec["value"])
        fig._placed = True
    else:
        share = spec.get("sharex", kind == "line")       # bar panels keep their own categories (JL 261011)
        fig, axs = plt.subplots(len(facets), 1, figsize=(7.2, 2.6 * len(facets) + 0.6), squeeze=False, sharex=share)
        axes = [a[0] for a in axs]
        for ax, fv in zip(axes, facets):
            d = df if fv is None else df[df[spec["facet"]] == fv]
            groups = sorted(d[spec["group"]].dropna().unique(), key=str) if spec.get("group") else [None]
            colour = _colour(groups)
            ys = _cols(spec["y"])
            for gi, g in enumerate(groups):
                part = d if g is None else d[d[spec["group"]] == g]
                part = part.sort_values(spec["x"]) if kind == "line" else part
                for yi, ycol in enumerate(ys):
                    c = colour[str(g)] if g is not None else PALETTE[yi % len(PALETTE)]
                    name = " · ".join(x for x in (_label(g) if g is not None else "", ycol if len(ys) > 1 else "") if x)
                    if kind == "line":
                        ax.plot(part[spec["x"]], part[ycol], color=c, lw=1.4, label=name or None, marker="o", ms=2.5)
                        if spec.get("band"):
                            lo, hi = spec["band"]
                            ax.fill_between(part[spec["x"]], part[lo], part[hi], color=c, alpha=.15, lw=0)
                    else:
                        k = len(groups) * len(ys)
                        w = 0.8 / k
                        pos = list(range(len(part)))
                        off = (gi * len(ys) + yi - (k - 1) / 2) * w
                        ax.bar([p + off for p in pos], part[ycol], width=w, color=c, label=name or None)
                        ax.set_xticks(pos)
                        ax.set_xticklabels([_label(v) for v in part[spec["x"]]], fontsize=7,
                                           rotation=45 if len(pos) > 8 else 0, ha="right" if len(pos) > 8 else "center")
            if fv is not None:
                ax.set_title(str(fv), fontsize=9, loc="left", fontweight="bold")     # a panel title in full, never cut
            ax.set_ylabel(spec.get("ylabel") or ", ".join(ys), fontsize=8)
            ax.grid(axis="y", color="#e4e4e7", lw=.6)
            ax.set_axisbelow(True)                # grid lines behind the bars
            if len(groups) > 1 or len(ys) > 1:
                ax.legend(fontsize=7, frameon=False, ncol=min(4, len(groups) * len(ys)))
        axes[-1].set_xlabel(spec.get("xlabel") or spec["x"], fontsize=8)
    for ax in axes:
        for h in spec.get("hline") or []:
            ax.axhline(h, color="#c0504d", lw=.8, ls="--")
        for v in spec.get("vline") or []:
            ax.axvline(v, color="#6b6b6b", lw=.8, ls=":")
    fig.suptitle(spec.get("title") or title, fontsize=10, x=0.01, ha="left", y=1 - 0.15 / fig.get_size_inches()[1])
    _save(fig, path)


KINDS = {"rates": (_rates_draw, _rates_lead), "grid": (_grid_draw, _grid_lead), "stab": (_stab_draw, _stab_lead),
         "balance": (_balance_draw, _balance_lead), "missing": (_missing_draw, _missing_lead),
         "share": (_share_draw, _share_lead), "estimate": (_estimate_draw, _estimate_lead)}


def lead(df):
    """The plain lead lines for one table (rounded), or [] for a shape this module does not know."""
    k = shape(df)
    try:
        return KINDS[k][1](df) if k else []
    except Exception:  # noqa: BLE001 · a summary that cannot be said is left out, never guessed
        return []


def draw(out, needs):
    """Draw every known-shape csv a live compute need writes; return [{need, table, file, kind}].
    `needs` is {need id: need} (run_question.live_needs). Figures land beside the tables."""
    out, made = Path(out), []
    for nid, n in needs.items():
        if n.get("kind") != "compute":
            continue
        declared = {spec.get("table") for spec in n.get("figures") or []}
        if "figures" in n and not n["figures"]:              # `figures: []` says no figure at all for this need
            continue
        for i, spec in enumerate(n.get("figures") or [], 1):          # the figures the need declares, first
            path = out / spec.get("table", "")
            if not spec.get("table") or not path.is_file():
                made.append({"need": nid, "table": spec.get("table", ""), "file": "", "kind": spec.get("kind", ""),
                             "problem": "declared table not written"})
                continue
            df = pd.read_csv(path)
            fig = out / f"fig_{nid}_{Path(spec['table']).stem}_{i}.png"
            if df.empty:
                continue
            try:
                _declared_draw(df, spec, fig, f"{nid} · {Path(spec['table']).stem.replace('_', ' ')}")
            except Exception as e:  # noqa: BLE001 · a figure that cannot be drawn is named, the run stands
                made.append({"need": nid, "table": spec["table"], "file": "", "kind": spec.get("kind", ""),
                             "problem": f"{type(e).__name__}: {e}"})
                continue
            made.append({"need": nid, "table": spec["table"], "file": fig.name, "kind": spec.get("kind", "line")})
        for f in n.get("output") or {}:
            path = out / f
            if not f.endswith(".csv") or not path.is_file() or f in declared:   # a declared figure replaces the shape's
                continue
            df = pd.read_csv(path)
            k = shape(df)
            if not k or df.empty:
                continue
            fig = out / f"fig_{nid}_{Path(f).stem}.png"
            try:
                KINDS[k][0](df, fig, f"{nid} · {Path(f).stem.replace('_', ' ')}")
            except Exception as e:  # noqa: BLE001 · a figure that cannot be drawn is named, the run stands
                made.append({"need": nid, "table": f, "file": "", "kind": k, "problem": f"{type(e).__name__}: {e}"})
                continue
            made.append({"need": nid, "table": f, "file": fig.name, "kind": k})
    return made

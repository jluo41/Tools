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

A table of no known shape gets no figure and no lead line. Same message, same colour, in every
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
    with warnings.catch_warnings():               # a long label may not fit tight; the bbox below makes room
        warnings.simplefilter("ignore", UserWarning)
        fig.tight_layout()
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
        for f in n.get("output") or {}:
            path = out / f
            if not f.endswith(".csv") or not path.is_file():
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

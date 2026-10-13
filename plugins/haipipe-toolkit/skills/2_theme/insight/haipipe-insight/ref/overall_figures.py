"""overall_figures.py · the Overall Report's figures: one plain picture per Executive answer, so a reader gets the
outcome at a glance (JL 261013: "for the general report ... no things like the figures to show it to quickly get the
outcome").

An Executive Task page names its figures in its face, `figures:`, one entry each:

    name     the file's name: <Board>/delivery/<job>/figures/<X>-<name>.png
    title    the outcome in words (no number): the report shows it above the picture
    kind     bars · dots · lines · ranges (below)
    table    a result table of a Run the answer cites, relative to the Job: tNN_<q>/runs/<run>/result/<table>.csv
    axis     the value axis, in words

    bars     one bar per row: label, value; rows: {level: shown name} picks and orders them; count, of: the
             columns written beside the bar as "k of n"
    dots     a dot and its interval per row (label, value, low, high), highest on top; zero: a line at 0 named
             by its words (a gap's reference)
    lines    one line per group across the columns (x, group, value); columns: {level: shown name} picks and orders
             the x axis; the marked groups in colour, every other grey
    ranges   one row per factor, its lowest and its highest group (each row its own table, where, value, levels,
             names); the widest on top

Every kind takes `where` ({column: value} kept rows), `mark` ({level: best · keep · worst · drop · reference}, `*`
for every level not named; a reference dot draws its interval as a band behind the rest) and `names` ({level: shown name}; otherwise camelCase is split into
words). Every value is read from the table; nothing is typed and nothing is computed from the extract. Called by
overall_report.py. Generated: never edit a PNG; change the page's `figures:` and run overall_report.py again.
"""
import re
from pathlib import Path

import pandas as pd

from figures import _plt, _save

BLUE, GREEN, RED, GREY, LIGHT = "#3e5c84", "#2b8a3e", "#c92a2a", "#495057", "#ced4da"
MARK = {"best": GREEN, "keep": GREEN, "worst": RED, "drop": RED, "reference": GREY}
WIDTH = 6.4


def _words(level, names):
    s = str(level)
    if s in names:
        return str(names[s])
    s = re.sub(r"\.0$", "", s)
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", s).lower() if re.fullmatch(r"[a-z]+[A-Za-z]*", s) else s


def _table(job, rel, where=None, *numeric):
    """The rows of a cited result table, its suppressed rows left out, `where` kept, `numeric` columns as numbers."""
    path = Path(job) / rel
    if not path.is_file():
        raise SystemExit(f"{rel}: no such result table under {Path(job).name}")
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    if "suppressed" in df:
        df = df[df["suppressed"].str.lower() != "true"]
    for col, want in (where or {}).items():
        df = df[df[col].str.lower() == str(want).lower()]
    for col in numeric:
        if col:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=[c for c in numeric[:1] if c])


def _colour(level, mark, other=BLUE):
    """A level's colour by its mark; `*` marks every level not named."""
    return MARK.get(str(mark.get(str(level), mark.get("*", ""))), other)


def _bars(spec, job, plt):
    rows = {str(k): v for k, v in (spec.get("rows") or {}).items()}
    df = _table(job, spec["table"], spec.get("where"), spec["value"], spec.get("count"), spec.get("of"))
    df = df.set_index(spec["label"])
    order = [r for r in rows if r in df.index] or list(df.index)
    fig, ax = plt.subplots(figsize=(WIDTH, 0.42 * len(order) + 0.9))
    names = dict(spec.get("names") or {}, **rows)
    vals = [df.loc[r, spec["value"]] for r in order]
    y = range(len(order))[::-1]
    ax.barh(list(y), vals, color=[_colour(r, spec.get("mark") or {}) for r in order], height=0.62)
    top = max(vals)
    for yy, r, v in zip(y, order, vals):
        note = f"{v:.1f}%" if v >= 1 else f"{v:.2f}%"
        if spec.get("count") and spec.get("of"):
            note += f"  ·  {int(df.loc[r, spec['count']]):,} of {int(df.loc[r, spec['of']]):,}"
        ax.text(v + top * 0.01, yy, note, va="center", fontsize=9)
    ax.set_yticks(list(y), [_words(r, names) for r in order], fontsize=10)
    ax.set_xlim(0, top * 1.45)
    ax.set_xlabel(spec.get("axis", ""))
    return fig


def _dots(spec, job, plt):
    v, lo, hi = spec["value"], spec.get("low"), spec.get("high")
    df = _table(job, spec["table"], spec.get("where"), v, lo, hi).sort_values(v)
    mark, names = spec.get("mark") or {}, spec.get("names") or {}
    fig, ax = plt.subplots(figsize=(WIDTH, 0.27 * len(df) + 1.0))
    labels = list(df[spec["label"]])
    for level in labels:                                  # a reference's interval as a band behind the rest
        if mark.get(level) == "reference" and lo:
            r = df[df[spec["label"]] == level].iloc[0]
            ax.axvspan(r[lo], r[hi], color=LIGHT, alpha=0.5, lw=0)
            ax.axvline(r[v], color=GREY, ls="--", lw=1)
    if spec.get("zero"):
        ax.axvline(0, color=GREY, ls="--", lw=1)
        ax.text(0, len(df) - 0.35, f" {spec['zero']}", color=GREY, fontsize=8.5, va="bottom")
    for i, (_, r) in enumerate(df.iterrows()):
        c = _colour(r[spec["label"]], mark)
        if lo:
            ax.plot([r[lo], r[hi]], [i, i], color=c, lw=2, solid_capstyle="round")
        ax.plot(r[v], i, "o", color=c, ms=6)
    ax.set_yticks(range(len(df)), [_words(x, names) for x in labels], fontsize=9.5)
    for tick, level in zip(ax.get_yticklabels(), labels):
        if level in mark:
            tick.set_color(_colour(level, mark))
            tick.set_fontweight("bold")
    ax.set_ylim(-0.6, len(df) - 0.1 + (0.5 if spec.get("zero") else 0))
    ax.set_xlabel(spec.get("axis", ""))
    ax.grid(axis="x", color="#eeeeee")
    return fig


def _lines(spec, job, plt):
    cols = {str(k): v for k, v in (spec.get("columns") or {}).items()}
    df = _table(job, spec["table"], spec.get("where"), spec["value"])
    xs = [c for c in cols if c in set(df[spec["x"]])] or sorted(set(df[spec["x"]]))
    mark, names = spec.get("mark") or {}, spec.get("names") or {}
    fig, ax = plt.subplots(figsize=(WIDTH, 3.6))
    groups = sorted(set(df[spec["group"]]), key=lambda g: (g in mark, g))      # the marked drawn last, on top
    for g in groups:
        d = df[df[spec["group"]] == g].set_index(spec["x"])
        ys = [d.loc[x, spec["value"]] if x in d.index else float("nan") for x in xs]
        on = g in mark
        ax.plot(range(len(xs)), ys, "-o", color=_colour(g, mark, LIGHT), lw=2.4 if on else 1, ms=4 if on else 2.5,
                zorder=3 if on else 1)
        if on:
            ax.text(len(xs) - 1 + 0.08, ys[-1], _words(g, names), color=_colour(g, mark), fontsize=9,
                    va="center", fontweight="bold")
    ax.set_xticks(range(len(xs)), [str(cols.get(x, _words(x, names))) for x in xs], fontsize=9.5)
    ax.set_xlim(-0.2, len(xs) - 1 + 1.1)
    ax.set_ylabel(spec.get("axis", ""))
    ax.grid(axis="y", color="#eeeeee")
    return fig


def _ranges(spec, job, plt):
    found = []
    for row in spec["rows"]:
        df = _table(job, row["table"], row.get("where"), row["value"])
        if row.get("levels"):
            df = df[df[row.get("level", "level")].isin([str(x) for x in row["levels"]])]
        lo = df.loc[df[row["value"]].idxmin()]
        hi = df.loc[df[row["value"]].idxmax()]
        lv, names = row.get("level", "level"), row.get("names") or {}
        found.append((row["label"], lo[row["value"]], hi[row["value"]], _words(lo[lv], names), _words(hi[lv], names)))
    found.sort(key=lambda f: f[2] - f[1])
    mark = spec.get("mark") or {}
    fig, ax = plt.subplots(figsize=(WIDTH, 0.55 * len(found) + 1.0))
    for i, (label, lo, hi, lo_name, hi_name) in enumerate(found):
        c = _colour(label, mark)
        ax.plot([lo, hi], [i, i], color=c, lw=5, alpha=0.35, solid_capstyle="round")
        ax.plot([lo, hi], [i, i], "o", color=c, ms=7)
        ax.text(lo - 0.4, i + 0.22, f"{lo_name}  {lo:.0f}%", ha="right", fontsize=8.5, color=GREY)
        ax.text(hi + 0.4, i + 0.22, f"{hi:.0f}%  {hi_name}", ha="left", fontsize=8.5, color=GREY)
        ax.text(hi + 0.4, i - 0.28, f"{hi - lo:.0f} points", ha="left", fontsize=8.5, color=c, fontweight="bold")
    ax.set_yticks(range(len(found)), [f[0] for f in found], fontsize=10)
    for tick, f in zip(ax.get_yticklabels(), found):
        if f[0] in mark:
            tick.set_color(_colour(f[0], mark))
            tick.set_fontweight("bold")
    left, right = min(f[1] for f in found), max(f[2] for f in found)
    ax.set_xlim(left - (right - left) * 0.45, right + (right - left) * 0.4)
    ax.set_ylim(-0.6, len(found) - 0.3)
    ax.set_xlabel(spec.get("axis", ""))
    ax.grid(axis="x", color="#eeeeee")
    return fig


KINDS = {"bars": _bars, "dots": _dots, "lines": _lines, "ranges": _ranges}


def cite(spec) -> str:
    """The answer a figure reads, as the pages cite it: `(I02 · t07)`; the rows of a ranges figure, joined."""
    rows = spec.get("rows") if isinstance(spec.get("rows"), list) else []
    tables = [r["table"] for r in rows] or [spec.get("table", "")]
    got = []
    for t in tables:
        m = re.match(r"^(t\d+)_([DIKWX]\d\d)_", str(t))
        if m and f"({m.group(2)} · {m.group(1)})" not in got:
            got.append(f"({m.group(2)} · {m.group(1)})")
    return ", ".join(got)


def draw(job, qid, specs, out) -> list:
    """Draw one Executive question's figures into `out`; returns [(spec, path)] in the page's order."""
    plt, made = _plt(), []
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    for spec in specs or []:
        if spec.get("kind") not in KINDS:
            raise SystemExit(f"{qid} figure {spec.get('name')}: kind {spec.get('kind')!r} is not one of {', '.join(KINDS)}")
        fig = KINDS[spec["kind"]](spec, job, plt)
        path = out / f"{qid}-{spec['name']}.png"
        _save(fig, path)
        made.append((spec, path))
    return made

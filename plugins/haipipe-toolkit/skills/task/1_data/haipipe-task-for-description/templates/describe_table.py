"""
Describe one table: the Table Card.

What one row is, what each column means, what the values look like, and what
to watch out for, for one stored table (a raw file, a ProcDf, a Record table,
an external asset). Template of haipipe-task-for-description; a Job copies it
into its src/ and every describe Task of that Job runs it.

Input
    Run config (RUN_CONFIG), layered over <task>/scripts/config/_defaults.yaml
    and <job>/src/config-defaults.yaml (last wins):
        table:        SPACE-relative path; {key} is filled from the layered
                      config, plus {job} and {block} (the Job and Block folders)
        dictionary:   SPACE-relative path of the column dictionary (YAML)
        compare_to:   optional SPACE-relative path of an earlier version
        compare_label, min_cell (11), top_k (8), max_value_width (60)
Output ($RESULT_DIR)
    table_card.md   the card a person reads; links figures/
    columns.csv     one row per column: typed meaning joined with computed facts
    grain.csv       every candidate key: distinct keys, rows that share one
    gotchas.csv     what to watch out for, computed or typed in the dictionary
    figures/*.png   column map, grain, one panel per meaning group
    metrics.json    summary.headline and the numbers behind it

Rules
    Facts are computed; meanings are typed in the dictionary. A column the
    dictionary does not describe reads "? (not described)", never a guess.
    Identifying columns show shape only (filled, distinct, length). A count
    below min_cell shows as "<min_cell". The example row is made up from
    typical values and is never copied from a real row.
    Every path written or shown is SPACE-relative.
"""

# %% [markdown]
# # Table Card · what one row is, what each column means
#
# ```txt
#    table ──► the table ──► ① grain ──► ② columns by meaning
#          ──► ③ made-up example row ──► ④ gotchas ──► ⑤ where columns go
#          ──► ⑥ changes since the earlier version
# ```

# %% Setup
import json
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import yaml
from IPython.display import Image, Markdown, display

pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", 90)
pd.set_option("display.max_rows", 200)


def required_env(name):
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"{name} is required; run this worker through its Ticket in <task>/runs/")
    return Path(value).resolve()


REPO_ROOT = required_env("REPO_ROOT")
JOB_DIR = required_env("JOB_DIR")
TASK_DIR = required_env("TASK_DIR")
RUN_CONFIG = required_env("RUN_CONFIG")
OUT = required_env("RESULT_DIR")
FIG = OUT / "figures"
FIG.mkdir(parents=True, exist_ok=True)


def space_rel(path):
    """SPACE-relative: the user name and checkout folder differ per machine."""
    try:
        return Path(path).resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def read_yaml(path):
    return (yaml.safe_load(path.read_text()) or {}) if path.is_file() else {}


CFG = {**read_yaml(JOB_DIR / "src" / "config-defaults.yaml"),
       **read_yaml(TASK_DIR / "scripts" / "config" / "_defaults.yaml"),
       **read_yaml(RUN_CONFIG)}
FILL = {k: v for k, v in CFG.items() if isinstance(v, (str, int, float))}
FILL.update(job=space_rel(JOB_DIR), block=space_rel(JOB_DIR.parent))


def resolve(template):
    return (REPO_ROOT / str(template).format(**FILL)).resolve()


for key in ("table", "dictionary"):
    if not CFG.get(key):
        raise SystemExit(f"the Run config must declare {key}:")
TABLE = resolve(CFG["table"])
DICTIONARY_PATH = resolve(CFG["dictionary"])
COMPARE = resolve(CFG["compare_to"]) if CFG.get("compare_to") else None
COMPARE_LABEL = CFG.get("compare_label") or (COMPARE.parent.name if COMPARE else None)
LABEL = CFG.get("label") or CFG.get("cohort") or TABLE.parent.name
MIN_CELL = int(CFG.get("min_cell", 11))
TOP_K = int(CFG.get("top_k", 8))
MAX_VALUE_WIDTH = int(CFG.get("max_value_width", 60))
for path in (TABLE, DICTIONARY_PATH) + ((COMPARE,) if COMPARE else ()):
    if not path.is_file():
        raise SystemExit(f"missing: {space_rel(path)}")

DICT = read_yaml(DICTIONARY_PATH)
TABLE_INFO = DICT.get("table") or {}
GROUPS = DICT.get("groups") or {}
COLUMNS = DICT.get("columns") or {}
NOT_DESCRIBED = "? (not described)"


def meaning_of(name):
    """The typed meaning; "?" alone means nobody typed it yet."""
    text = str((COLUMNS.get(name) or {}).get("meaning") or "").strip()
    return NOT_DESCRIBED if text in ("", "?") else text


def confirmed(meaning):
    return not str(meaning).startswith("?")

PF = pq.ParquetFile(TABLE)
SCHEMA = PF.schema_arrow
N_ROWS = PF.metadata.num_rows
NAMES = SCHEMA.names
print(f"table:          {space_rel(TABLE)}")
print(f"dictionary:     {space_rel(DICTIONARY_PATH)}")
print(f"rows × columns: {N_ROWS:,} × {len(NAMES)}")


def entry(name):
    return COLUMNS.get(name) or {}


def group_of(name):
    return entry(name).get("group") or "undescribed"


def group_title(group):
    return (GROUPS.get(group) or {}).get("title") or group


def is_identifying(name):
    e = entry(name)
    if "identifying" in e:
        return bool(e["identifying"])
    return bool((GROUPS.get(group_of(name)) or {}).get("identifying", False))


def masked(n):
    return f"<{MIN_CELL}" if 0 < n < MIN_CELL else f"{n:,}"


def pct(n, d):
    return round(100.0 * n / d, 2) if d else 0.0


def md_table(df):
    """A small markdown table for table_card.md (no extra dependency)."""
    cols = list(df.columns)
    lines = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(r[c]).replace("|", "\\|").replace("\n", " ") for c in cols) + " |")
    return "\n".join(lines)


def show(md, table=None, figure=None):
    """One notebook section: prose, then the table, then the picture."""
    display(Markdown(md))
    if table is not None:
        display(table)
    if figure is not None:
        display(Image(filename=str(figure)))


CARD = []   # table_card.md, section by section

# %% [markdown]
# ## Facts per column: filled, distinct, typical values
#
# One column at a time, so a wide table never has to fit in memory.

# %% Facts per column
def role_of(name, typ, n_distinct, max_len):
    declared = entry(name).get("role")
    if declared:
        return declared, True
    if pa.types.is_timestamp(typ) or pa.types.is_date(typ):
        return "time", False
    if pa.types.is_boolean(typ) or (0 < n_distinct <= 2):
        return "flag", False
    if pa.types.is_integer(typ) or pa.types.is_floating(typ) or pa.types.is_decimal(typ):
        return "number", False
    if max_len and max_len > MAX_VALUE_WIDTH:
        return "text", False
    if name.endswith("_id") or name.endswith("_encoded"):
        return "identifier", False
    return "category", False


def as_time(col):
    series = col.to_pandas()
    if not pd.api.types.is_datetime64_any_dtype(series):
        series = pd.to_datetime(series, errors="coerce", utc=True)
    if getattr(series.dt, "tz", None) is not None:
        series = series.dt.tz_convert(None)
    return series.dropna()


FACTS = []
VALUES = {}    # name -> DataFrame(value, n, pct) of disclosable top values
NUMBERS = {}   # name -> float array for a histogram
MONTHS = {}    # name -> monthly counts
TYPICAL = {}   # name -> the value the made-up example row shows
for name in NAMES:
    col = pq.read_table(TABLE, columns=[name]).column(name)
    typ = col.type
    n_null = col.null_count
    n_blank, min_len, max_len, med_len = 0, None, None, None
    if pa.types.is_string(typ) or pa.types.is_large_string(typ):
        lengths = pc.utf8_length(col)
        n_blank = int(pc.sum(pc.equal(lengths, 0)).as_py() or 0)
        min_len, max_len = pc.min(lengths).as_py(), pc.max(lengths).as_py()
        med_len = pc.approximate_median(lengths).as_py()
    n_filled = N_ROWS - n_null - n_blank
    n_distinct = 0 if pa.types.is_null(typ) else pc.count_distinct(col, mode="only_valid").as_py()
    role, declared = role_of(name, typ, n_distinct, max_len)
    ident = is_identifying(name)
    lens = f", {min_len}-{max_len} chars" if max_len is not None else ""
    if n_filled == 0:
        values, typical = "empty in every row", "(empty)"
    elif ident:
        values, typical = f"withheld (identifying): {n_distinct:,} distinct{lens}", f"<{name}>"
    elif role == "text":
        values, typical = f"free text{lens}", f"<text, about {med_len:.0f} chars>" if med_len else "<text>"
    elif role == "number":
        arr = col.to_pandas().astype("float64").dropna().to_numpy()
        lo, mid, hi = np.percentile(arr, [0, 50, 100])
        values, typical = f"min {lo:g} · median {mid:g} · max {hi:g}", f"{mid:g}"
        NUMBERS[name] = arr
    elif role == "time":
        times = as_time(col)
        if len(times):
            values = f"{times.min():%Y-%m-%d} to {times.max():%Y-%m-%d}"
            typical = f"{times.sort_values().iloc[len(times) // 2]:%Y-%m-%d}"
            MONTHS[name] = times.dt.to_period("M").value_counts().sort_index()
        else:
            values, typical = "no parseable time", "(unparsed)"
    else:
        counts = pc.value_counts(pc.drop_null(col)) if n_distinct else None
        vc = (pd.DataFrame({"value": counts.field("values").to_pylist(), "n": counts.field("counts").to_pylist()})
              if counts is not None else pd.DataFrame())
        if len(vc):
            vc = vc.sort_values("n", ascending=False).head(TOP_K).reset_index(drop=True)
            vc["value"] = vc["value"].map(lambda v: "(blank)" if v == "" else str(v)[:MAX_VALUE_WIDTH])
            small = vc["n"] < MIN_CELL
            vc.loc[small, "value"] = "(small cell)"
            vc["pct"] = (100.0 * vc["n"] / N_ROWS).round(2)
            vc["n_shown"] = vc["n"].map(masked)
            VALUES[name] = vc
            shown = vc[~small].head(3)
            values = "; ".join(f"{v} {p:g}%" for v, p in zip(shown["value"], shown["pct"]))
            values += f" (of {n_distinct:,} distinct)" if n_distinct > len(shown) else ""
            typical = shown["value"].iloc[0] if len(shown) else "<rare>"
        else:
            values, typical = "no values", "(empty)"
    TYPICAL[name] = typical
    e = entry(name)
    FACTS.append({
        "group": group_of(name), "column": name,
        "meaning": meaning_of(name),
        "role": role if declared else f"{role} (inferred)",
        "identifying": ident, "type": str(typ),
        "filled_pct": pct(n_filled, N_ROWS), "nonnull_pct": pct(N_ROWS - n_null, N_ROWS),
        "distinct": n_distinct, "values": values,
        "feeds": ", ".join(e.get("feeds") or []), "source": e.get("source") or "",
    })

FACTS = pd.DataFrame(FACTS)
group_order = [g for g in GROUPS if g in set(FACTS["group"])] + sorted(set(FACTS["group"]) - set(GROUPS))
FACTS["group"] = pd.Categorical(FACTS["group"], categories=group_order, ordered=True)
FACTS = FACTS.sort_values(["group"], kind="stable").reset_index(drop=True)
FACTS.to_csv(OUT / "columns.csv", index=False)
n_described = int(FACTS["meaning"].map(confirmed).sum())
print(f"✓ {len(FACTS)} columns profiled, {n_described} described by the dictionary")

# %% [markdown]
# ## The table: what it is, its size, its column map

# %% The table
time_col = TABLE_INFO.get("time")
span = ""
if time_col in MONTHS:
    months = MONTHS[time_col]
    span = f"{months.index.min()} to {months.index.max()} by `{time_col}`"

colors = plt.get_cmap("tab20")
group_color = {g: colors(i % 20) for i, g in enumerate(group_order)}
fig_h = 1.2 + 0.19 * len(FACTS)
fig, ax = plt.subplots(figsize=(9, fig_h))
ys = np.arange(len(FACTS))[::-1]
ax.barh(ys, FACTS["filled_pct"], color=[group_color[g] for g in FACTS["group"]])
ax.set_yticks(ys)
ax.set_yticklabels([f"{c}" for c in FACTS["column"]], fontsize=7)
ax.set_xlim(0, 100)
ax.set_ylim(-0.6, len(FACTS) - 0.4)
ax.set_xlabel("filled share of rows (%)")
ax.set_title(f"{LABEL} · {len(FACTS)} columns, filled share, grouped by meaning", fontsize=10)
for g in group_order:
    idx = np.where(FACTS["group"] == g)[0]
    if len(idx):
        dark = tuple(0.55 * c for c in group_color[g][:3])
        ax.text(101, ys[idx].mean(), group_title(g), va="center", fontsize=8, color=dark, fontweight="bold")
ax.grid(axis="x", alpha=0.3)
fig.tight_layout()
column_map = FIG / "00_column_map.png"
fig.savefig(column_map, dpi=110, bbox_inches="tight")
plt.close(fig)

identity = pd.DataFrame([
    ("table", TABLE_INFO.get("name") or TABLE.stem),
    ("file", f"`{space_rel(TABLE)}`"),
    ("rows × columns", f"{N_ROWS:,} × {len(NAMES)}"),
    ("time span", span or "(no time column declared)"),
    ("described columns", f"{n_described} of {len(NAMES)} confirmed (dictionary `{space_rel(DICTIONARY_PATH)}`)"),
    ("made by", TABLE_INFO.get("source") or "(not declared)"),
], columns=["", " "])
head = [f"Table Card · {TABLE_INFO.get('name') or TABLE.stem} · {LABEL}",
        "=" * 60, "",
        TABLE_INFO.get("what") or "_What this table is: not declared in the dictionary._", "",
        md_table(identity), "", "![column map](figures/00_column_map.png)", ""]
CARD += head
show("\n".join(head[3:5]), identity, column_map)

# %% [markdown]
# ## ① Grain: what one row is, proven by counting

# %% Grain
declared = list(CFG.get("grain") or TABLE_INFO.get("grain") or [])
candidates = [declared] if declared else []
for key in (TABLE_INFO.get("grain_candidates") or []) + (CFG.get("grain_candidates") or []):
    if list(key) not in candidates:
        candidates.append(list(key))
for key in list(candidates):
    for name in key:
        if len(key) > 1 and [name] not in candidates:
            candidates.append([name])

GRAIN = []
for key in candidates:
    missing = [k for k in key if k not in NAMES]
    if missing:
        GRAIN.append({"key": " + ".join(key), "declared": key == declared, "note": f"absent: {', '.join(missing)}"})
        continue
    sizes = pq.read_table(TABLE, columns=key).to_pandas().groupby(key, dropna=False, sort=False).size()
    shared = int(sizes[sizes > 1].sum())
    spread = sizes.clip(upper=5).value_counts()
    GRAIN.append({
        "key": " + ".join(key), "declared": key == declared, "distinct_keys": len(sizes),
        "unique": len(sizes) == N_ROWS, "rows_sharing_a_key": shared, "pct_rows_unique": pct(N_ROWS - shared, N_ROWS),
        **{f"rows_in_keys_of_{k if k < 5 else '5+'}": int(spread.get(k, 0) * k) for k in range(1, 5)},
        "rows_in_keys_of_5+": int(sizes[sizes >= 5].sum()), "note": "",
    })
GRAIN = pd.DataFrame(GRAIN)
GRAIN.to_csv(OUT / "grain.csv", index=False)

hashes = []
for batch in PF.iter_batches(batch_size=250_000):
    hashes.append(pd.util.hash_pandas_object(batch.to_pandas(), index=False).to_numpy())
N_EXACT_DUP = int(N_ROWS - len(np.unique(np.concatenate(hashes)))) if hashes else 0

row_text = TABLE_INFO.get("row") or "_One row is: not declared in the dictionary._"
if declared and len(GRAIN) and not GRAIN.iloc[0].get("note"):
    g0 = GRAIN.iloc[0]
    verdict = (f"The declared key `{g0['key']}` is unique: it holds for every row."
               if g0["unique"] else
               f"The declared key `{g0['key']}` does not hold for every row: "
               f"{g0['rows_sharing_a_key']:,} rows ({100 - g0['pct_rows_unique']:.2f}%) share a key with another row.")
else:
    verdict = "No grain key is declared in the dictionary, so the candidates below are only tested."
dup_text = (f"{N_EXACT_DUP:,} rows are exact copies of an earlier row (every column equal)."
            if N_EXACT_DUP else "No row is an exact copy of another.")
if declared and len(GRAIN) and "distinct_keys" in GRAIN and pd.notna(GRAIN.iloc[0].get("distinct_keys")) \
        and not GRAIN.iloc[0]["unique"] and N_EXACT_DUP:
    left = N_ROWS - N_EXACT_DUP - int(GRAIN.iloc[0]["distinct_keys"])
    dup_text += (f" Dropping them leaves {left:,} rows that still repeat the declared key."
                 if left > 0 else " Dropping them makes the declared key unique.")

plot = GRAIN.dropna(subset=["distinct_keys"]) if "distinct_keys" in GRAIN else GRAIN.iloc[0:0]
grain_fig = None
if len(plot):
    fig, ax = plt.subplots(figsize=(9, 0.6 + 0.45 * len(plot)))
    left = np.zeros(len(plot))
    parts = ["rows_in_keys_of_1", "rows_in_keys_of_2", "rows_in_keys_of_3", "rows_in_keys_of_4", "rows_in_keys_of_5+"]
    for i, part in enumerate(parts):
        share = 100.0 * plot[part].to_numpy(dtype=float) / N_ROWS
        ax.barh(np.arange(len(plot))[::-1], share, left=left, color=plt.get_cmap("Blues")(0.9 - 0.17 * i),
                label=part.replace("rows_in_keys_of_", "") + " row(s) per key")
        left += share
    ax.set_yticks(np.arange(len(plot))[::-1])
    ax.set_yticklabels([k + ("  (declared)" if d else "") for k, d in zip(plot["key"], plot["declared"])], fontsize=8)
    ax.set_xlim(0, 100)
    ax.set_xlabel("share of rows (%)")
    ax.set_title("Grain: how many rows share each candidate key", fontsize=10)
    ax.legend(fontsize=7, ncol=5, loc="lower center", bbox_to_anchor=(0.5, 1.08))
    fig.tight_layout()
    grain_fig = FIG / "01_grain.png"
    fig.savefig(grain_fig, dpi=110, bbox_inches="tight")
    plt.close(fig)

show_cols = [c for c in ["key", "declared", "distinct_keys", "unique", "rows_sharing_a_key", "pct_rows_unique", "note"] if c in GRAIN]
grain_md = ["① Grain: what one row is", "-" * 40, "", f"**One row is:** {row_text}", "", verdict, dup_text, "",
            md_table(GRAIN[show_cols]), ""]
if grain_fig:
    grain_md += ["![grain](figures/01_grain.png)", ""]
CARD += grain_md
show("\n".join(grain_md[3:7]), GRAIN[show_cols], grain_fig)

# %% [markdown]
# ## ② Columns by meaning: one table and one picture per group

# %% Columns by meaning
def group_figure(group, names):
    panels = [n for n in names if n in VALUES or n in NUMBERS or n in MONTHS]
    if not panels:
        return None
    ncols = 3
    nrows = int(np.ceil(len(panels) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(12, 2.6 * nrows), squeeze=False)
    for ax, name in zip(axes.flat, panels):
        if name in VALUES:
            vc = VALUES[name].iloc[::-1]
            ax.barh(range(len(vc)), vc["pct"], color=group_color.get(group))
            ax.set_yticks(range(len(vc)))
            ax.set_yticklabels([str(v)[:28] for v in vc["value"]], fontsize=7)
            ax.set_xlabel("% of rows", fontsize=7)
        elif name in NUMBERS:
            arr = NUMBERS[name]
            hi = np.percentile(arr, 99) if len(arr) else 0
            ax.hist(arr[arr <= hi], bins=30, color=group_color.get(group))
            ax.set_xlabel("value (up to the 99th percentile)", fontsize=7)
        else:
            m = MONTHS[name]
            ax.bar(range(len(m)), m.to_numpy(), color=group_color.get(group))
            step = max(1, len(m) // 6)
            ax.set_xticks(range(0, len(m), step))
            ax.set_xticklabels([str(p) for p in m.index[::step]], fontsize=7, rotation=30)
            ax.set_ylabel("rows per month", fontsize=7)
        ax.set_title(name, fontsize=8)
        ax.tick_params(labelsize=7)
    for ax in list(axes.flat)[len(panels):]:
        ax.axis("off")
    fig.suptitle(f"{group_title(group)} · values", fontsize=10)
    fig.tight_layout()
    path = FIG / f"g_{group}.png"
    fig.savefig(path, dpi=100, bbox_inches="tight")
    plt.close(fig)
    return path


CARD += ["② Columns by meaning", "-" * 40, ""]
show("**② Columns by meaning.** Meaning is typed in the dictionary; every other column is computed. "
     "`filled_pct` counts rows that are neither null nor blank.")
for group in group_order:
    part = FACTS[FACTS["group"] == group]
    if part.empty:
        continue
    info = GROUPS.get(group) or {}
    shown = part[["column", "meaning", "role", "filled_pct", "distinct", "values"]]
    fig_path = group_figure(group, list(part["column"]))
    lead = f"**{group_title(group)}** ({len(part)} columns)" + (f": {info['what']}" if info.get("what") else "")
    if info.get("identifying"):
        lead += " Identifying group: values are withheld, shape only."
    CARD += [lead, "", md_table(shown), ""] + ([f"![{group}](figures/{fig_path.name})", ""] if fig_path else [])
    show(lead, shown, fig_path)

# %% [markdown]
# ## ③ A made-up example row
#
# Each value is the most common one (or the median) of its own column, so the row shows what values look like. It is not a real row, and the combination may never occur.

# %% Example row
example = FACTS[["group", "column", "meaning"]].copy()
example.insert(2, "example value", [TYPICAL[c] for c in example["column"]])
example_md = ["③ A made-up example row", "-" * 40, "",
              "Each value is the most common value (or the median) of its own column, and identifying "
              "columns show a placeholder. It shows what values look like; it is not a real row, and "
              "the combination may never occur.", ""]
if TABLE_INFO.get("example_story"):
    example_md += [f"**Read as a story:** {TABLE_INFO['example_story']}", ""]
example_md += [md_table(example), ""]
CARD += example_md
show("\n".join(example_md[3:-2]), example)

# %% [markdown]
# ## ④ Gotchas: what to watch out for

# %% Gotchas
GOTCHAS = []


def gotcha(kind, detail, found_by="computed"):
    GOTCHAS.append({"kind": kind, "detail": detail, "found_by": found_by})


first_unique = GRAIN.iloc[0].get("unique") if len(GRAIN) and "unique" in GRAIN else None
if declared and first_unique is not None and pd.notna(first_unique) and not bool(first_unique):
    gotcha("grain", f"`{GRAIN.iloc[0]['key']}` repeats: {GRAIN.iloc[0]['rows_sharing_a_key']:,} rows share a key with another row")
if N_EXACT_DUP:
    gotcha("exact duplicates", f"{N_EXACT_DUP:,} rows are exact copies of an earlier row")
empty = FACTS.loc[FACTS["filled_pct"] == 0, "column"].tolist()
if empty:
    gotcha("empty columns", f"{len(empty)} empty in every row: " + ", ".join(empty))
constant = FACTS.loc[(FACTS["distinct"] == 1) & (FACTS["filled_pct"] > 0), "column"].tolist()
if constant:
    gotcha("constant columns", f"{len(constant)} hold one value only: " + ", ".join(constant))
undescribed = FACTS.loc[FACTS["meaning"] == NOT_DESCRIBED, "column"].tolist()
if undescribed:
    gotcha("undescribed", f"{len(undescribed)} not in the dictionary yet: " + ", ".join(undescribed))
guessed = FACTS.loc[~FACTS["meaning"].map(confirmed) & (FACTS["meaning"] != NOT_DESCRIBED), "column"].tolist()
if guessed:
    gotcha("unconfirmed meaning", f"{len(guessed)} typed as a guess (meaning starts with ?): " + ", ".join(guessed))
absent = [c for c in COLUMNS if c not in NAMES]
if absent:
    gotcha("not in this version", f"{len(absent)} in the dictionary but not in this table: " + ", ".join(absent))
for note in TABLE_INFO.get("notes") or []:
    gotcha("note", note, "dictionary")
for name in NAMES:
    for note in entry(name).get("notes") or []:
        gotcha(f"note · {name}", note, "dictionary")

# ⑥ Changes since the earlier version, cheap: schema plus parquet null counts.
CHANGES = pd.DataFrame()
if COMPARE:
    cpf = pq.ParquetFile(COMPARE)
    before = {f.name: str(f.type) for f in cpf.schema_arrow}
    nulls = {}
    for rg in range(cpf.metadata.num_row_groups):
        group_meta = cpf.metadata.row_group(rg)
        for ci in range(group_meta.num_columns):
            c = group_meta.column(ci)
            stats = c.statistics
            nulls[c.path_in_schema] = nulls.get(c.path_in_schema, 0) + (stats.null_count if stats is not None and stats.has_null_count else 0)
    n_before = cpf.metadata.num_rows
    rows = []
    for name in sorted(set(before) | set(NAMES), key=lambda n: (n not in NAMES, n)):
        now = FACTS.loc[FACTS["column"] == name]
        was_pct = pct(n_before - nulls.get(name, 0), n_before) if name in before else None
        now_pct = float(now["nonnull_pct"].iloc[0]) if len(now) else None
        change = ("added" if name not in before else "removed" if not len(now)
                  else "type changed" if before[name] != now["type"].iloc[0]
                  else "fill moved" if abs(now_pct - was_pct) >= 20 else "")
        if change:
            rows.append({"column": name, "change": change, "type_before": before.get(name, ""),
                         "type_now": now["type"].iloc[0] if len(now) else "",
                         "nonnull_pct_before": was_pct, "nonnull_pct_now": now_pct})
    CHANGES = pd.DataFrame(rows)
    if len(CHANGES):
        counts = CHANGES["change"].value_counts()
        gotcha(f"since {COMPARE_LABEL}", ", ".join(f"{n} {k}" for k, n in counts.items()) + " (section ⑥)")

GOTCHAS = pd.DataFrame(GOTCHAS, columns=["kind", "detail", "found_by"])
GOTCHAS.to_csv(OUT / "gotchas.csv", index=False)
gotcha_md = ["④ Gotchas: what to watch out for", "-" * 40, "",
             md_table(GOTCHAS) if len(GOTCHAS) else "Nothing found.", ""]
CARD += gotcha_md
show("**④ Gotchas.** Found by counting, or typed in the dictionary.", GOTCHAS)

# %% [markdown]
# ## ⑤ Where the columns go, ⑥ changes since the earlier version

# %% Where columns go and changes
feeds = []
for _, r in FACTS.iterrows():
    for target in [t.strip() for t in r["feeds"].split(",") if t.strip()] or ["(read by nothing declared)"]:
        feeds.append({"read by": target, "column": r["column"]})
feeds = pd.DataFrame(feeds)
where = (feeds.groupby("read by")["column"].agg(lambda s: f"{len(s)}: " + ", ".join(s)).reset_index()
         .rename(columns={"column": "columns"}))
where_md = ["⑤ Where the columns go", "-" * 40, "",
            "The downstream reader of each column, typed as `feeds:` in the dictionary.", "",
            md_table(where), ""]
CARD += where_md
show("**⑤ Where the columns go.** " + where_md[3], where)

if COMPARE:
    change_md = [f"⑥ Changes since {COMPARE_LABEL}", "-" * 40, "",
                 f"Compared with `{space_rel(COMPARE)}` by schema and parquet null counts "
                 "(`nonnull_pct` counts non-null rows; blanks are not seen here). Only changed columns are listed.", "",
                 md_table(CHANGES) if len(CHANGES) else "No column was added, removed, retyped, or moved 20 points in fill.", ""]
    CARD += change_md
    show(f"**⑥ Changes since {COMPARE_LABEL}.** " + change_md[3], CHANGES if len(CHANGES) else None)

# %% Done
(OUT / "table_card.md").write_text("\n".join(CARD) + "\n")
g0 = GRAIN.iloc[0] if len(GRAIN) else {}
grain_bit = ""
if declared and len(GRAIN) and "pct_rows_unique" in GRAIN and pd.notna(g0.get("pct_rows_unique")):
    grain_bit = f"; grain {g0['key']} holds for {g0['pct_rows_unique']:g}% of rows"
headline = (f"{N_ROWS:,} rows × {len(NAMES)} columns{grain_bit}; {N_EXACT_DUP:,} exact duplicate rows; "
            f"{n_described}/{len(NAMES)} columns described; {len(GOTCHAS)} gotchas")
(OUT / "metrics.json").write_text(json.dumps({
    "table": space_rel(TABLE),
    "dictionary": space_rel(DICTIONARY_PATH),
    "rows": N_ROWS,
    "columns": len(NAMES),
    "described_columns": n_described,
    "exact_duplicate_rows": N_EXACT_DUP,
    "grain": GRAIN.drop(columns=[c for c in GRAIN if c.startswith("rows_in_keys")]).to_dict("records"),
    "gotchas": len(GOTCHAS),
    "compare_to": space_rel(COMPARE) if COMPARE else None,
    "summary": {"headline": headline},
}, indent=2, default=str) + "\n")
print(f"✓ {headline}")
print(f"✓ Wrote {space_rel(OUT / 'table_card.md')} and {len(list(FIG.glob('*.png')))} figures")

#!/usr/bin/env python3
"""The items Task (b15 s41-task-items-procedure): a Job's raw data becomes the items a person labels, in three
steps, each a hard Run in the Task's own `runs/`, all run through `haipipe-labeling-preparation`:

    1 describe   read the raw data once; write the Data cards to result/description.json (no items)
    2 items      under a signed recipe, make the items into the store (items-vN/) and run the item check;
                 a revision is the same operation with `revise_of` and the person's notes in its config
    3 embed      under an agreed build, embed the items: the map, its groups, near-duplicates, outliers

A Run is planned first (`plan`): its ticket, its card (run.yaml) and its config, filled from what the steps before
it wrote, so the agent and the person only correct it. `items` and `embed` refuse to run until a person has signed
or agreed the Run's card (`sign`, or the workbench's Sign and Agree buttons): the recipe and the build are the
person's choice. Every Run keeps the prompt's notes in its config, so each version says why it exists.

The worker side (`worker_main`) runs inside the Task's ticket, through the Task's `scripts/prepare.py`, which only
forwards here; it reads $HAIPIPE_CONFIG and writes $RESULT_DIR (and $HEAVY_DIR for the vectors).

CLI
    plan     <task> describe|items|embed [--data <path>] [--model M] [--notes TEXT] [--revise-of rNN]
    sign     <task> <run> --by <person>
    settle   <task>                          after a ticket: each finished Run's card takes its receipt's status
    sample   <task> raw|items [--seed N] [--n 5]
    status   <task>
    next     <task or Job>                   where the items Task stands and the one thing to do next
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
SCHEMA = "labeling-items-task/v1"
OPS = ("describe", "items", "embed")
REQUIRED = {"describe": ("description.json", "metrics.json"),
            "items": ("manifest.yaml", "metrics.json", "check.json", "stats.json"),
            "embed": ("manifest.yaml", "metrics.json", "map.json", "groups.json")}
SIGNED = {"items": "signed", "embed": "agreed"}          # the person's word each step needs before it runs
TICKET_TEMPLATE = HERE.parents[2] / "1_base/task/haipipe-task/ref/run-sh-template.sh"
WORKER = "prepare"
FORWARDER = '''"""The items Task's one worker: every Run (describe, items, embed) goes to haipipe-labeling-preparation's
engine, items_task.py, by its config's `operation`. Written by `items_task.py plan`; edit the engine, not this."""
import sys
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "env.sh").is_file())
sys.path.insert(0, str(ROOT / "Tools/plugins/haipipe-toolkit/skills/2_theme/labeling/engine"))
import items_task  # noqa: E402

items_task.worker_main()
'''
TEXT_MIN_WORDS = 8          # a column whose values run this long, at the median, is text a person reads
LABEL_HINT = re.compile(r"(gold|label|harm|safe|toxic|Q_|answer|rating|score|verdict|class)", re.I)


# ── small helpers ─────────────────────────────────────────────────────────────────────────────────
def space_root(path: Path) -> Path:
    """The SPACE: the nearest folder above holding env.sh (AGENTS rule 7)."""
    path = path.resolve()
    for p in (path, *path.parents):
        if (p / "env.sh").is_file():
            return p
    raise SystemExit(f"no SPACE root (env.sh) above {path}")


def rel(path: Path, root: Path) -> str:
    """SPACE-relative, as the path is named: a link inside the store stays the name the Job gave, never the
    machine's own folder it points at."""
    for p, r in ((Path(os.path.abspath(path)), Path(os.path.abspath(root))), (path.resolve(), root.resolve())):
        try:
            return p.relative_to(r).as_posix()
        except ValueError:
            continue
    return str(path)


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def read_yaml(path: Path) -> dict:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def jsonl(path: Path, rows: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def read_jsonl(path: Path) -> list:
    out = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except ValueError:
                    continue
    return out


def words(text) -> int:
    return len(str(text or "").split())


def median(values: list):
    from statistics import median as med
    return med(values) if values else None


def histogram(values: list, bins: int = 10) -> dict:
    """A histogram as {edges, counts}: whole-number bins from min to max."""
    if not values:
        return {"edges": [], "counts": []}
    lo, hi = min(values), max(values)
    width = max(1, -(-(hi - lo + 1) // bins))
    edges = list(range(lo, hi + width + 1, width))
    counts = [0] * (len(edges) - 1)
    for v in values:
        counts[min(len(counts) - 1, (v - lo) // width)] += 1
    return {"edges": edges, "counts": counts}


# ── the Task's files ──────────────────────────────────────────────────────────────────────────────
def runs_of(task: Path) -> list:
    """The Task's hard Runs, oldest first: (folder, its card)."""
    runs = task / "runs"
    folders = sorted(p for p in runs.glob("r[0-9][0-9]_*/") if p.is_dir()) if runs.is_dir() else []
    return [(p, read_yaml(p / "run.yaml")) for p in folders]


def config_of(task: Path, run: Path) -> Path:
    inside = run / "config.yaml"
    return inside if inside.is_file() else task / "scripts" / "config" / f"{run.name}.yaml"


def status_of(run: Path) -> str:
    return str(read_yaml(run / "result" / "runtime.yaml").get("status") or read_yaml(run / "run.yaml").get("status")
               or "planned")


def operation_of(task: Path, run: Path) -> str:
    """describe · items · embed, from the Run's config (`operation`), else from older Runs' own words."""
    cfg = read_yaml(config_of(task, run))
    if cfg.get("operation") in OPS:
        return cfg["operation"]
    card = read_yaml(run / "run.yaml")
    types = card.get("type") or []
    if "embedding-build" in types:
        return "embed"
    if (run / "result" / "description.json").is_file() or "raw" in run.name:
        return "describe"
    return "items"


def latest(task: Path, op: str, *, complete: bool = True) -> Path | None:
    """The newest Run of one operation; complete only, by default."""
    for run, _ in reversed(runs_of(task)):
        if operation_of(task, run) == op and (not complete or status_of(run) == "complete"):
            return run
    return None


def signed(run: Path) -> dict | None:
    s = read_yaml(run / "run.yaml").get("signs")
    return s if isinstance(s, dict) and s.get("by") else None


def job_of(task: Path) -> Path:
    return task.parent


def job_data(task: Path, root: Path) -> dict:
    """What the Job says its data is: its face's `dataset:` and `data:` lines (a folder or a file, SPACE-relative);
    else the last config that named a source. Nothing is typed in the Task (s41-D09)."""
    face = job_of(task) / f"{job_of(task).name}.md"
    text = face.read_text(encoding="utf-8", errors="ignore") if face.is_file() else ""
    data = re.search(r"(?m)^data:\s*(\S.*)$", text)
    name = re.search(r"(?m)^dataset:\s*(\S.*)$", text)
    path = data.group(1).strip() if data else ""
    if not path:
        for run, _ in reversed(runs_of(task)):
            cfg = read_yaml(config_of(task, run))
            path = str(cfg.get("data") or cfg.get("source") or "")
            if path:
                break
    return {"dataset": name.group(1).strip() if name else "", "data": path}


def data_files(root: Path, data: str) -> list:
    """The readable tables under the Job's data path: a file, or every csv/jsonl/parquet/json in a folder."""
    p = root / data if data else None
    if p is None or not p.exists():
        return []
    if p.is_file():
        return [p]
    return sorted(x for x in p.iterdir() if x.suffix in (".csv", ".jsonl", ".parquet", ".json", ".tsv"))


def read_table(path: Path):
    import pandas as pd
    if path.suffix == ".csv":
        return pd.read_csv(path, low_memory=False)
    if path.suffix == ".tsv":
        return pd.read_csv(path, sep="\t", low_memory=False)
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    if path.suffix == ".jsonl":
        return pd.read_json(path, lines=True)
    return pd.read_json(path)


def store_root(root: Path, data: str) -> Path:
    """Where items versions go: beside the raw data's folder (dices/350/ → dices/items-vN/)."""
    p = root / data
    folder = p.parent if p.is_file() else p
    return folder.parent


def next_items_version(store: Path) -> str:
    n = max([int(m.group(1)) for d in store.glob("items-v*") if (m := re.fullmatch(r"items-v(\d+)", d.name))] or [0])
    return f"items-v{n + 1}"


# ── plan: the next Run, ready for the agent and the person to correct ─────────────────────────────
def _next_run_name(task: Path, op: str, tag: str = "") -> str:
    n = max([int(p.name[1:3]) for p, _ in runs_of(task)] or [0]) + 1
    return f"r{n:02d}_{op}" + (f"_{tag}" if tag else "")


def _ticket(run_name: str, op: str, purpose: str) -> str:
    text = TICKET_TEMPLATE.read_text(encoding="utf-8")
    req = " ".join(f'"{r}"' for r in REQUIRED[op])
    text = text.replace('TASK_NAME="worker"', f'TASK_NAME="{WORKER}"')
    text = text.replace('RUN_OPERATION="task-execution"', f'RUN_OPERATION="{op}"')
    text = text.replace('RUN_TARGET="bounded-target"', f'RUN_TARGET="{run_name.split("_", 1)[1]}"')
    text = text.replace('REQUIRED_RESULTS=("metrics.json")', f"REQUIRED_RESULTS=({req})")
    return text.replace("\nset -uo pipefail", f"\n# {purpose}\n\nset -uo pipefail", 1)


def _guess_columns(df) -> dict:
    """First guesses the agent corrects: the unit column, the text columns, the label (answer) columns."""
    n = len(df)
    unit = next((c for c in df.columns if re.search(r"(item|conversation|chat|dialog|unit)_?id$", str(c), re.I)
                 and 1 < df[c].nunique() < n), None)
    if unit is None:
        unit = next((c for c in df.columns if str(c).lower().endswith("id") and 1 < df[c].nunique() < n), None)
    text = [c for c in df.columns if df[c].dtype == object
            and (median([words(v) for v in df[c].dropna().astype(str).head(500)]) or 0) >= TEXT_MIN_WORDS]
    keys = [c for c in df.columns if c not in text and c != unit and LABEL_HINT.search(str(c))
            and df[c].nunique(dropna=True) <= 30]
    return {"unit": unit, "text": text, "keys": keys}


def _speaker_tags(root: Path, card: dict, column: str | None) -> dict:
    """The tags that open a turn in a context column (`USER:`, `LAMDA:`), each kept as it is for the agent to name."""
    path = root / str(card.get("table", {}).get("file") or "")
    if not column or not path.is_file():
        return {}
    df = read_table(path)
    if column not in df.columns:
        return {}
    from collections import Counter
    seen = Counter(m.group(1) for v in df[column].dropna().astype(str).head(2000)
                   for m in re.finditer(r"(?m)^\s*([A-Z][A-Za-z_]{1,15}):", v))
    return {t: t for t, c in seen.most_common(6) if c >= 5}


def _describe_config(task: Path, root: Path, data: str, notes: str) -> dict:
    files = data_files(root, data)
    cfg = {"operation": "describe", "data": data, "file": rel(files[0], root) if files else "",
           "unit": None, "one_row_is": "<typed: what one row is, in one sentence>",
           "background": {"what": "<typed>", "who": "<typed>", "why": "<typed>", "source": "<a paper or link>",
                          "license": "<typed>", "cite": "<typed>"},
           "groups": [], "labels": {"expert": [], "rater": []}, "text": [],
           "samples": {"n": 5, "seed": 7}, "notes": notes or ""}
    if files:
        df = read_table(files[0])
        g = _guess_columns(df)
        cfg["unit"] = g["unit"]
        cfg["text"] = g["text"]
        cfg["labels"]["rater"] = g["keys"]
        cfg["groups"] = [{"name": "<typed group>", "meaning": "<typed>", "columns": [str(c) for c in df.columns]}]
    return cfg


def _items_config(task: Path, root: Path, notes: str, revise_of: str | None) -> dict:
    """The recipe, proposed: from the Run it revises, else from the Data cards."""
    prev = latest(task, "items") if revise_of is None else task / "runs" / revise_of
    if revise_of and not (prev and prev.is_dir()):
        raise SystemExit(f"no Run {revise_of} to revise")
    described = latest(task, "describe")
    card = json.loads((described / "result" / "description.json").read_text()) if described else {}
    data = job_data(task, root)["data"] or str(card.get("table", {}).get("file") or "")
    store = store_root(root, data) if data else task
    cfg = {"operation": "items", "data": data, "file": str(card.get("table", {}).get("file") or "")}
    if prev is not None:
        old = read_yaml(config_of(task, prev))
        recipe = dict(old.get("recipe") or {})
    else:
        text = card.get("text_to_label") or {}
        cols = [t["column"] for t in text.get("columns") or []]
        labels = card.get("labels") or []
        unit = card.get("grain", {}).get("unit") or "unit"
        prefix = re.sub(r"[^a-z0-9]+", "", (job_data(task, root)["dataset"] or task.name.split("_")[1]).lower())
        context = cols[0] if len(cols) > 1 else None
        recipe = {"unit": unit, "item_id": f"{prefix}-{{{unit}}}",
                  "main": cols[-1] if cols else None,
                  "context_before": {"column": context, "turns": _speaker_tags(root, card, context)} if context else None,
                  "context_after": None,
                  "keep_out": [lb["column"] for lb in labels],
                  "group": card.get("grain", {}).get("unit")}
    cfg["recipe"] = recipe
    cfg["out"] = rel(store / next_items_version(store), root)
    if revise_of or prev is not None:
        cfg["revise_of"] = prev.name if prev is not None else None
        cfg["changed"] = "<typed: the recipe line the notes changed, or none>"
    cfg["notes"] = notes or ""
    return cfg


def _store_of(run: Path) -> str:
    """Where an items Run put its items: its manifest's `store`, else its metrics' (older Runs wrote it there)."""
    store = read_yaml(run / "result" / "manifest.yaml").get("store")
    if not store and (run / "result" / "metrics.json").is_file():
        store = json.loads((run / "result" / "metrics.json").read_text()).get("store")
    return str(store or "")


def _embed_config(task: Path, root: Path, model: str, notes: str) -> dict:
    made = latest(task, "items")
    store = _store_of(made) if made else ""
    return {"operation": "embed", "items": store, "items_run": made.name if made else None, "model": model,
            "input": "main", "map": "tsne", "groups": None, "seed": 0, "duplicate_cosine": 0.95,
            "outliers": 10, "notes": notes or ""}


def plan(task: Path, op: str, *, data: str = "", model: str = "", notes: str = "", revise_of: str | None = None) -> Path:
    """Write the next Run of one step: its ticket, its card (planned; items and embed unsigned) and its config,
    proposed from the steps before it. Returns the Run folder."""
    task = task.resolve()
    root = space_root(task)
    settle(task)
    if op not in OPS:
        raise SystemExit(f"unknown step {op!r}: describe, items or embed")
    if not (task / f"{task.name}.md").is_file():
        raise SystemExit(f"not a Task folder: {task}")
    tag = ""
    if op == "embed":
        model = model or ("sentence-transformers/all-MiniLM-L6-v2" if _has_st() else "tfidf-svd")
        tag = re.sub(r"[^a-z0-9]+", "", model.split("/")[-1].lower())[:16]
    name = _next_run_name(task, "revise" if revise_of else op, tag)
    run = task / "runs" / name
    run.mkdir(parents=True)
    if op == "describe":
        cfg = _describe_config(task, root, data or job_data(task, root)["data"], notes)
        purpose = "Read the Job's raw data once and write the Data cards (result/description.json). No items."
    elif op == "items":
        cfg = _items_config(task, root, notes, revise_of)
        purpose = "Make the items under the signed recipe, into the store, and run the item check."
    else:
        cfg = _embed_config(task, root, model, notes)
        purpose = "Embed the items under the agreed build: vectors to HEAVY_DIR, the map and its groups to result/."
    cfg = {"_meta": {"purpose": purpose, "schema": SCHEMA}, **cfg}
    write_yaml(task / "scripts" / "config" / f"{name}.yaml", cfg)
    path = task / "scripts" / "config" / f"{name}.yaml"           # the ticket greps this line, unquoted
    path.write_text("notebook: off   # the worker writes the Result; no notebook\n" + path.read_text(), encoding="utf-8")
    ticket = run / f"{name}.sh"
    ticket.write_text(_ticket(name, op, purpose), encoding="utf-8")
    ticket.chmod(0o755)
    card = {"run": name, "kind": "hard", "type": ["embedding-build"] if op == "embed" else [f"items-{op}"],
            "scope": rel(task, root), "target": op, "ticket": f"{name}.sh",
            "skill": "haipipe-labeling-preparation", "agent": None, "signs": None, "status": "planned",
            "passes": [], "writes": ["result/"], "feeds": []}
    if op in SIGNED:
        card["needs"] = SIGNED[op]
    write_yaml(run / "run.yaml", card)
    fwd = task / "scripts" / f"{WORKER}.py"
    if not fwd.is_file():
        fwd.parent.mkdir(parents=True, exist_ok=True)
        fwd.write_text(FORWARDER, encoding="utf-8")
    _ensure_review(task)
    return run


def _ensure_review(task: Path) -> None:
    """The ticket's code-review gate reads the Task's CODE_REVIEW.md; the forwarder is reviewed with the engine."""
    review = task / "CODE_REVIEW.md"
    if not review.is_file():
        review.write_text("# Code review\n\n- overall_verdict: pass\n- scope: scripts/prepare.py forwards to "
                          "haipipe-labeling-preparation's items_task.py, reviewed and tested with the engine.\n",
                          encoding="utf-8")


def settle(task: Path) -> list:
    """The owner settles each finished Run's card (haipipe-run Lifecycle 4): the card's status becomes the one its
    ticket's receipt recorded. Returns the Runs it changed."""
    changed = []
    for run, card in runs_of(task):
        done = str(read_yaml(run / "result" / "runtime.yaml").get("status") or "")
        if done in ("complete", "failed", "blocked") and card.get("status") != done:
            card["status"] = done
            write_yaml(run / "run.yaml", card)
            changed.append(run.name)
    return changed


def _has_st() -> bool:
    try:
        import sentence_transformers  # noqa: F401
        return True
    except ImportError:
        return False


def sign(task: Path, run_name: str, by: str) -> dict:
    """A person signs (a recipe) or agrees (a build) a planned Run's card; only then may it run."""
    run = (task / "runs" / run_name).resolve()
    if run.parent != (task / "runs").resolve() or not (run / "run.yaml").is_file():
        raise SystemExit(f"no Run {run_name} in {task}")
    if status_of(run) == "complete":
        raise SystemExit("a complete Run is closed; plan a new one")
    by = " ".join(str(by or "").split())[:80]
    if not by:
        raise SystemExit("a sign needs the person's name")
    card = read_yaml(run / "run.yaml")
    card["signs"] = {"by": by, "at": now(), "what": card.get("needs") or "signed"}
    write_yaml(run / "run.yaml", card)
    return card["signs"]


# ── live samples, for Draw again: read only, nothing written ─────────────────────────────────────
def sample(task: Path, kind: str, seed: int, n: int = 5, root: Path | None = None) -> dict:
    task = task.resolve()
    root = root or space_root(task)
    rnd = random.Random(seed)
    if kind == "raw":
        run = latest(task, "describe")
        card = json.loads((run / "result" / "description.json").read_text()) if run else {}
        path = root / str(card.get("table", {}).get("file") or "")
        if not path.is_file():
            files = data_files(root, job_data(task, root)["data"])
            path = files[0] if files else None
        if path is None:
            return {"kind": kind, "seed": seed, "rows": [], "columns": []}
        df = read_table(path)
        idx = sorted(rnd.sample(range(len(df)), min(n, len(df))))
        cols = [str(c) for c in df.columns]
        return {"kind": kind, "seed": seed, "columns": cols, "rows": [
            {"row": i + 1, **{c: _plain(df.iloc[i][c]) for c in cols}} for i in idx]}
    run = latest(task, "items")
    store = root / _store_of(run) if run else None
    items = read_jsonl(store / "items.jsonl") if store and (store / "items.jsonl").is_file() else []
    pick = sorted(rnd.sample(range(len(items)), min(n, len(items))))
    return {"kind": kind, "seed": seed, "rows": [items[i] for i in pick]}


def _plain(v):
    try:
        import pandas as pd
        if pd.isna(v):
            return ""
    except (TypeError, ValueError):
        pass
    if hasattr(v, "item"):
        v = v.item()
    return v if isinstance(v, (int, float, str, bool)) else str(v)


# ── the worker ────────────────────────────────────────────────────────────────────────────────────
def worker_main() -> None:
    config = Path(os.environ["HAIPIPE_CONFIG"])
    result = Path(os.environ["RESULT_DIR"])
    cfg = read_yaml(config)
    root = space_root(config)
    op = cfg.get("operation")
    run = result.parent
    if op in SIGNED and not signed(run):
        print(f"==> BLOCKED: {run.name} is not {SIGNED[op]} yet: a person signs its card first "
              f"(the workbench's {'Sign' if op == 'items' else 'Agree'} button, or items_task.py sign).", file=sys.stderr)
        raise SystemExit(2)
    if op == "describe":
        describe(cfg, root, result)
    elif op == "items":
        make_items(cfg, root, result)
    elif op == "embed":
        embed(cfg, root, result, Path(os.environ.get("HEAVY_DIR") or result))
    else:
        raise SystemExit(f"unknown operation {op!r}")


def _typed(v) -> bool:
    return bool(v) and not (isinstance(v, str) and v.startswith("<typed"))


def describe(cfg: dict, root: Path, result: Path) -> None:
    """Step 1: the Data cards, every number counted; the meanings are the config's, typed, never guessed."""
    path = root / str(cfg.get("file") or "")
    if not path.is_file():
        files = data_files(root, str(cfg.get("data") or ""))
        if not files:
            raise SystemExit(f"no readable data at {cfg.get('data')!r}")
        path = files[0]
    df = read_table(path)
    n, cols = len(df), [str(c) for c in df.columns]
    unit = cfg.get("unit") if cfg.get("unit") in df.columns else None
    dup = int(df.duplicated().sum())
    proof = {"rows": n}
    if unit:
        per = df.groupby(unit).size()
        proof[f"distinct_{unit}"] = int(per.size)
        proof["rows_per_unit_median"] = float(per.median())
    for key in ("rater_id", "annotator_id", "worker_id"):
        if key in df.columns and key != unit:
            proof[f"distinct_{key}"] = int(df[key].nunique())
    proof["exact_duplicate_rows"] = dup

    def column(c):
        s = df[c]
        filled = float(s.notna().mean())
        distinct = int(s.nunique(dropna=True))
        if s.dtype == object and (median([words(v) for v in s.dropna().astype(str).head(500)]) or 0) >= TEXT_MIN_WORDS:
            typical = f"text, {median([words(v) for v in s.dropna().astype(str)]):g} words at the median"
        elif distinct <= 12:
            typical = " · ".join(f"{k} {v:,}" for k, v in s.value_counts(dropna=True).head(6).items())
        elif str(s.dtype).startswith(("int", "float")):
            typical = f"{s.min():g} to {s.max():g}, median {s.median():g}"
        else:
            typical = f"{distinct:,} values, e.g. {str(s.dropna().iloc[0])[:40]}" if distinct else "empty"
        return {"name": c, "filled": round(filled, 4), "distinct": distinct, "typical": typical}

    grouped, seen = [], set()
    for g in cfg.get("groups") or []:
        cs = [c for c in g.get("columns") or [] if c in df.columns]
        seen |= set(cs)
        grouped.append({"name": g.get("name") or "columns", "meaning": g.get("meaning") or "",
                        "columns": [column(c) for c in cs]})
    rest = [c for c in cols if c not in seen]
    if rest:
        grouped.append({"name": "other columns", "meaning": "not grouped yet", "columns": [column(c) for c in rest]})

    # one made-up row: each column's value taken from a different random row, so no real row is shown here
    rnd = random.Random(int((cfg.get("samples") or {}).get("seed", 7)))
    synth = {}
    for c in cols:
        v = _plain(df.iloc[rnd.randrange(n)][c]) if n else ""
        synth[c] = f"<text, {words(v)} words>" if isinstance(v, str) and words(v) >= TEXT_MIN_WORDS else v
    labels = []
    for who, cs in (cfg.get("labels") or {}).items():
        for c in cs or []:
            if c in df.columns:
                s = df[c] if who == "rater" or not unit else df.groupby(unit)[c].first()
                labels.append({"column": c, "who": who, "counted_per": "row" if who == "rater" or not unit else unit,
                               "values": {str(k): int(v) for k, v in s.value_counts(dropna=False).head(12).items()}})
    text_cols = []
    for c in cfg.get("text") or []:
        if c in df.columns:
            s = (df.groupby(unit)[c].first() if unit else df[c]).dropna().astype(str)
            w = [words(v) for v in s]
            text_cols.append({"column": c, "words_median": median(w), "words_min": min(w) if w else 0,
                              "words_max": max(w) if w else 0, "values": int(len(s)),
                              "lines_median": median([v.count("\n") + 1 for v in s])})
    samp = cfg.get("samples") or {}
    seed = int(samp.get("seed", 7))
    pick = sorted(random.Random(seed).sample(range(n), min(int(samp.get("n", 5)), n)))
    gotchas = []
    if dup:
        gotchas.append(f"{dup:,} rows are exact copies of another row")
    empty = [c["name"] for g in grouped for c in g["columns"] if c["filled"] == 0]
    if empty:
        gotchas.append("empty columns: " + ", ".join(empty))
    keys = [lb["column"] for lb in labels]
    if keys:
        gotchas.append(f"{len(keys)} label columns stay out of the items")
    if not _typed(cfg.get("one_row_is")):
        gotchas.append("one row is: not typed yet")
    card = {"schema": SCHEMA, "table": {"file": rel(path, root), "rows": n, "columns": len(cols),
                                        "bytes": path.stat().st_size, "what_it_is": (cfg.get("background") or {}).get("what") or ""},
            "grain": {"unit": unit, "one_row_is": cfg.get("one_row_is") if _typed(cfg.get("one_row_is")) else "",
                      "proof": proof},
            "background": {k: v for k, v in (cfg.get("background") or {}).items() if _typed(v)},
            "groups": grouped, "synth_df": {"rows": [synth]}, "labels": labels,
            "text_to_label": {"columns": text_cols}, "samples": {"seed": seed, "rows": [i + 1 for i in pick]},
            "gotchas": gotchas, "notes": cfg.get("notes") or ""}
    write_json(result / "description.json", card)
    units = proof.get(f"distinct_{unit}") if unit else None
    write_json(result / "metrics.json", {"summary": {"headline": f"{n:,} rows · {len(cols)} columns"
                                                     + (f" · {units:,} units" if units else "")},
                                         "rows": n, "columns": len(cols), "units": units, "duplicates": dup})
    print(f"described {rel(path, root)}: {n:,} rows")


def _turns(text: str, tags: dict) -> list:
    """A context cut into turns: a line opening with a tag (`USER:`) starts a turn; any other line continues it."""
    if not tags:
        return [line.strip() for line in str(text).splitlines() if line.strip()]
    pat = re.compile(r"^(" + "|".join(re.escape(t) for t in tags) + r"):\s*")
    turns: list = []
    for line in str(text).splitlines():
        line = line.strip()
        if not line:
            continue
        m = pat.match(line)
        if m:
            turns.append([tags[m.group(1)], line[m.end():].strip()])
        elif turns:
            turns[-1][1] += " " + line
        else:
            turns.append(["", line])
    return [f"{who}: {t}" if who else t for who, t in turns if t]


def make_items(cfg: dict, root: Path, result: Path) -> None:
    """Step 2: one item per unit under the signed recipe; the answers in their own files; the item check."""
    recipe = cfg.get("recipe") or {}
    path = root / str(cfg.get("file") or "")
    if not path.is_file():
        files = data_files(root, str(cfg.get("data") or ""))
        if not files:
            raise SystemExit(f"no readable data at {cfg.get('data')!r}")
        path = files[0]
    df = read_table(path)
    unit, main = recipe.get("unit"), recipe.get("main")
    for need, col in (("unit", unit), ("main", main)):
        if col not in df.columns:
            raise SystemExit(f"the recipe's {need} column {col!r} is not in {path.name}")
    before, after = recipe.get("context_before") or {}, recipe.get("context_after") or {}
    keep = [c for c in recipe.get("keep_out") or [] if c in df.columns]
    id_fmt = str(recipe.get("item_id") or "{" + unit + "}")
    out = root / str(cfg["out"])
    if (out / "items.jsonl").exists():
        raise SystemExit(f"{cfg['out']} exists: a version is never rewritten; plan a new Run")
    items, truth, raters, problems = [], [], [], []
    groups = df.groupby(unit, sort=False)
    order = sorted(groups.groups, key=lambda k: (0, int(k)) if str(k).lstrip("-").isdigit() else (1, str(k)))
    for key in order:
        g = groups.get_group(key)
        first = g.iloc[0]
        iid = id_fmt.format(**{unit: key, **{str(c): _plain(first[c]) for c in df.columns}})
        cb = "\n".join(_turns(first[before["column"]], before.get("turns") or {})) if before.get("column") in df.columns else ""
        ca = "\n".join(_turns(first[after["column"]], after.get("turns") or {})) if after.get("column") in df.columns else ""
        text = " ".join(str(_plain(first[main]) or "").split())
        items.append({"item_id": iid, "context_before": cb, "main": text, "context_after": ca})
        const = [c for c in keep if g[c].nunique(dropna=False) <= 1]
        varying = [c for c in keep if c not in const]
        truth.append({"item_id": iid, **{c: _plain(first[c]) for c in const}, "rows": int(len(g))})
        if varying:
            raters += [{"item_id": iid, **{c: _plain(r[c]) for c in varying}} for _, r in g.iterrows()]
    ids = [it["item_id"] for it in items]
    long_keys = {str(v) for t in truth for k, v in t.items() if k not in ("item_id", "rows") and isinstance(v, str)
                 and words(v) >= 4}
    leaked = [it["item_id"] for it in items if any(k in it["main"] or k in it["context_before"] for k in long_keys)]
    check = {"ids_unique": len(set(ids)) == len(ids), "one_item_per_unit": len(items) == df[unit].nunique(),
             "nothing_judged_empty": all(it["main"] for it in items), "no_key_inside": not leaked,
             "empty_main": [it["item_id"] for it in items if not it["main"]][:20], "key_inside": leaked[:20]}
    check["passed"] = all(check[k] for k in ("ids_unique", "one_item_per_unit", "nothing_judged_empty", "no_key_inside"))
    write_json(result / "check.json", check)
    if not check["passed"]:
        raise SystemExit("the item check failed: " + ", ".join(k for k in ("ids_unique", "one_item_per_unit",
                         "nothing_judged_empty", "no_key_inside") if not check[k]))
    out.mkdir(parents=True, exist_ok=True)
    jsonl(out / "items.jsonl", items)
    jsonl(out / "items.ground-truth.jsonl", truth)
    if raters:
        jsonl(out / "items.raters.jsonl", raters)
    w = [words(it["main"]) for it in items]
    t = [len([x for x in it["context_before"].splitlines() if x.strip()]) for it in items]
    by_len = sorted(zip(w, ids))
    stats = {"words_judged": {"min": min(w), "median": median(w), "max": max(w), "histogram": histogram(w)},
             "turns_before": {"min": min(t), "median": median(t), "max": max(t), "histogram": histogram(t)},
             "shortest": [i for _, i in by_len[:3]], "longest": [i for _, i in by_len[-3:][::-1]]}
    write_json(result / "stats.json", stats)
    recipe_words = (f"one {unit} · judged: {main}"
                    + (f" · before: {before.get('column')}" if before.get("column") else "")
                    + (f" · after: {after.get('column')}" if after.get("column") else " · after: none"))
    manifest = {"store": rel(out, root), "source": rel(path, root), "item": recipe_words, "items": len(items),
                "rows": int(len(df)), "kept_out": keep, "raters_rows": len(raters),
                "words_judged_median": median(w), "turns_before_median": median(t),
                "revise_of": cfg.get("revise_of"), "changed": cfg.get("changed") if _typed(cfg.get("changed")) else None,
                "notes": cfg.get("notes") or ""}
    write_yaml(out / "manifest.yaml", manifest)
    write_yaml(result / "manifest.yaml", manifest)
    write_json(result / "metrics.json", {"summary": {"headline": f"{len(items):,} items, one per {unit}; "
                                                                 f"the check passed"},
                                         "store": rel(out, root), "items": len(items), "ratings": len(raters)})
    print(f"{len(items):,} items into {rel(out, root)}")


def _encode(texts: list, model: str, seed: int):
    import numpy as np
    if model == "tfidf-svd":
        from sklearn.decomposition import TruncatedSVD
        from sklearn.feature_extraction.text import TfidfVectorizer
        m = TfidfVectorizer(min_df=1, max_df=0.9, sublinear_tf=True).fit_transform(texts)
        k = max(2, min(128, m.shape[1] - 1, m.shape[0] - 1))
        v = TruncatedSVD(n_components=k, random_state=seed).fit_transform(m)
    else:
        from sentence_transformers import SentenceTransformer
        v = SentenceTransformer(model).encode(texts, batch_size=32, show_progress_bar=False)
    v = np.asarray(v, dtype="float32")
    norms = np.linalg.norm(v, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return v / norms


def embed(cfg: dict, root: Path, result: Path, heavy: Path) -> None:
    """Step 3: every item embedded once under the agreed build: the map, groups, near-duplicates, outliers."""
    import numpy as np
    sys.path.insert(0, str(HERE))
    from embedding_build import _choose_groups, _keywords, _map_2d, _map_3d
    store = root / str(cfg.get("items") or "")
    items = read_jsonl(store / "items.jsonl")
    if not items:
        raise SystemExit(f"no items at {cfg.get('items')!r}")
    mode = cfg.get("input") or "main"
    texts = [it["main"] if mode == "main" else (it.get("context_before", "") + "\n" + it["main"]).strip()
             for it in items]
    seed = int(cfg.get("seed") or 0)
    model = str(cfg.get("model") or "tfidf-svd")
    vectors = _encode(texts, model, seed)
    labels, k, scores = _choose_groups(vectors, seed, cfg.get("groups"))
    coords = _map_2d(vectors, seed, str(cfg.get("map") or "tsne"))
    coords3 = _map_3d(vectors, seed, str(cfg.get("map") or "tsne"))
    keywords = _keywords(texts, labels, k)
    ids = [it["item_id"] for it in items]
    lab = np.asarray(labels)
    centres = np.stack([vectors[lab == g].mean(axis=0) for g in range(k)])
    sim_to_centre = (vectors * centres[lab]).sum(axis=1)
    groups = []
    for g in range(k):
        members = np.where(lab == g)[0]
        typical = members[np.argsort(-sim_to_centre[members])][:3]
        groups.append({"group": g, "size": int(len(members)), "keywords": keywords.get(g, []),
                       "typical": [ids[i] for i in typical]})
    sims = vectors @ vectors.T
    np.fill_diagonal(sims, -1)
    thr = float(cfg.get("duplicate_cosine") or 0.95)
    a, b = np.where(np.triu(sims, 1) >= thr)
    dups = sorted(({"a": ids[i], "b": ids[j], "cosine": round(float(sims[i, j]), 4)} for i, j in zip(a, b)),
                  key=lambda d: -d["cosine"])[:50]
    far = np.argsort(sim_to_centre)[: int(cfg.get("outliers") or 10)]
    outliers = [{"item_id": ids[i], "group": int(lab[i]), "to_its_group": round(float(sim_to_centre[i]), 4)}
                for i in far]
    write_json(result / "map.json", [{"item_id": i, "x": x, "y": y, "group": int(g)}
                                     for i, (x, y), g in zip(ids, coords, labels)])
    write_json(result / "map3d.json", [{"item_id": i, "x": x, "y": y, "z": z} for i, (x, y, z) in zip(ids, coords3)])
    write_json(result / "groups.json", groups)
    write_json(result / "duplicates.json", dups)
    write_json(result / "outliers.json", outliers)
    heavy.mkdir(parents=True, exist_ok=True)
    np.save(heavy / "vectors.npy", vectors)
    (heavy / "rows.jsonl").write_text("".join(json.dumps({"row": n, "item_id": i}) + "\n" for n, i in enumerate(ids)))
    manifest = {"model": model, "dim": int(vectors.shape[1]), "input": mode, "map": str(cfg.get("map") or "tsne"),
                "seed": seed, "groups": k, "group_scores": scores, "items": len(items),
                "items_store": cfg.get("items"), "items_run": cfg.get("items_run"),
                "duplicates": len(dups), "duplicate_cosine": thr, "vectors": rel(heavy / "vectors.npy", root),
                "notes": cfg.get("notes") or ""}
    write_yaml(result / "manifest.yaml", manifest)
    write_json(result / "metrics.json", {"summary": {"headline": f"{len(items):,} items · {k} groups · "
                                                                 f"{len(dups)} near-duplicate pairs"},
                                         "items": len(items), "groups": k, "duplicates": len(dups)})
    print(f"embedded {len(items):,} items with {model}: {k} groups")


# ── next: where an items Task stands, from a Job or a Task folder ──────────────────────────────────
def find_task(path: Path) -> Path:
    """The items Task a path means: the Task itself, or the one items Task of a Job (`task-type: items` or `data`)."""
    path = path.resolve()
    def is_items(t: Path) -> bool:
        face = t / f"{t.name}.md"
        return face.is_file() and re.search(r"(?m)^task-type:\s*(items|data)\s*$", face.read_text(errors="ignore"))
    if is_items(path):
        return path
    found = sorted(t for t in path.glob("t[0-9][0-9]_*/") if is_items(t)) if path.is_dir() else []
    if len(found) != 1:
        raise SystemExit(f"{len(found)} items Tasks under {path}: name the Task folder")
    return found[0]


def next_step(path: Path, settle_runs: bool = True) -> dict:
    """Where the items Task stands and the one thing to do next: who does it (the agent or the person) and how.
    `settle_runs=False` reads only (the start door, haipipe-labeling scripts/start.py)."""
    task = find_task(path)
    root = space_root(task)
    if settle_runs:
        settle(task)
    data = job_data(task, root)
    files = data_files(root, data["data"])
    t = rel(task, root)
    view = lambda tab: f"/_board/workbench?path={t}&theme=labeling&space=Work+Details&sub={tab.replace(' ', '+')}"
    out = {"task": t, "dataset": data["dataset"], "data": data["data"], "files": [rel(f, root) for f in files]}
    steps = [("describe", "1 · Data"), ("items", "2 · Items"), ("embed", "3 · Embedding")]
    made = latest(task, "items")
    if made is not None and not signed(made):
        out["note"] = (f"{made.name}'s items were made before recipes were signed: read them in 2 · Items; to remake "
                       "them under a signed recipe, write user feedback in its 'Make the items, again' prompt")
    for op, tab in steps:
        if latest(task, op):
            continue
        open_ = next((r for r, _ in reversed(runs_of(task)) if operation_of(task, r) == op
                      and status_of(r) != "complete"), None)
        out.update(step=op, tab=tab, workbench=view(tab))
        if op == "describe" and not files:
            out.update(who="person", do="name the data: the Job's face needs `data:` (and `dataset:`), "
                                         "or the data is not on this machine")
        elif open_ is None:
            out.update(who="agent", do=f"plan {op}, type its config" + (", run its ticket and settle"
                                                                       if op == "describe" else ", then stop"),
                       command=f"items_task.py plan {t} {op}")
        elif op in SIGNED and not signed(open_):
            out.update(who="person", run=open_.name,
                       do=f"read {open_.name}'s {'recipe' if op == 'items' else 'build'} in the {tab} tab and press "
                          f"{'Sign' if op == 'items' else 'Agree'}; then paste the tab's prompt")
        else:
            out.update(who="agent", run=open_.name, do=f"run {open_.name}'s ticket, then settle",
                       command=f"bash {rel(open_ / (open_.name + '.sh'), root)}")
        if op == "items" and not latest(task, "describe"):
            out["note"] = "no Data cards yet: Step 1 comes first"
        if op != "embed" and out.get("note", "").startswith(made.name if made else "\0"):
            out.pop("note")                                   # the note is for the steps after the items
        return out
    out.update(step="done", tab="2 · Items", workbench=view("2 · Items"), who="person",
               do="all three steps are done; to change the items, write user feedback in the Items tab's "
                  "'Make the items, again' prompt; then the building Task takes the items")
    return out


# ── status and CLI ────────────────────────────────────────────────────────────────────────────────
def status(task: Path) -> list:
    settle(task)
    return [{"run": r.name, "operation": operation_of(task, r), "status": status_of(r),
             "signed": bool(signed(r))} for r, _ in runs_of(task)]


def main(argv: list | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan")
    p.add_argument("task", type=Path)
    p.add_argument("step", choices=OPS + ("revise",))
    p.add_argument("--data", default="")
    p.add_argument("--model", default="")
    p.add_argument("--notes", default="")
    p.add_argument("--revise-of", default=None)
    s = sub.add_parser("sign")
    s.add_argument("task", type=Path)
    s.add_argument("run")
    s.add_argument("--by", required=True)
    sm = sub.add_parser("sample")
    sm.add_argument("task", type=Path)
    sm.add_argument("kind", choices=("raw", "items"))
    sm.add_argument("--seed", type=int, default=7)
    sm.add_argument("--n", type=int, default=5)
    nx = sub.add_parser("next")
    nx.add_argument("path", type=Path)
    se = sub.add_parser("settle")
    se.add_argument("task", type=Path)
    st = sub.add_parser("status")
    st.add_argument("task", type=Path)
    a = ap.parse_args(argv)
    if a.cmd == "plan":
        step = "items" if a.step == "revise" else a.step
        revise = a.revise_of or ((latest(a.task.resolve(), "items").name if latest(a.task.resolve(), "items") else None)
                                 if a.step == "revise" else None)
        run = plan(a.task, step, data=a.data, model=a.model, notes=a.notes, revise_of=revise)
        root = space_root(a.task)
        print(json.dumps({"run": run.name, "ticket": rel(run / f"{run.name}.sh", root),
                          "config": rel(a.task.resolve() / "scripts" / "config" / f"{run.name}.yaml", root),
                          "needs": SIGNED.get(step)}, indent=2))
    elif a.cmd == "sign":
        print(json.dumps(sign(a.task.resolve(), a.run, a.by), indent=2))
    elif a.cmd == "next":
        print(json.dumps(next_step(a.path), indent=2, ensure_ascii=False))
    elif a.cmd == "settle":
        print(json.dumps(settle(a.task.resolve())))
    elif a.cmd == "sample":
        print(json.dumps(sample(a.task, a.kind, a.seed, a.n), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(status(a.task.resolve()), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

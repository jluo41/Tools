"""The j02 console topics' shared drawing parts: the console's facts read from its code, what each view reads on
disk, and the screens grid (a screenshot per view with its "on disk" tree under it, the toolkit's s11 · s12 · s13
shape). Each topic's builder imports this and draws through blueprints/_build/mapdraw.py.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDIO = HERE.parent
TOOLS = STUDIO.parents[3]
APP = TOOLS / "plugins" / "inlab-human" / "servers" / "haichat-inlab"
sys.path.insert(0, str(STUDIO.parents[2] / "_build"))
from mapdraw import GREEN, INK, RED, Sheet  # noqa: E402,F401

_spec = importlib.util.spec_from_file_location("build_ui_docs", APP / "diagram" / "build_ui_docs.py")
DOCS = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(DOCS)

VIEWS = DOCS.views()                    # [(key, icon, label, group)] from web/src/views.ts
BLURBS = DOCS.blurbs()                  # {raw|source|record|case: (store, what)}

# what each view reads, as the reader would find it on disk (env var → folder → file), and the route that serves it
DISK = {
    "raw": ["$INLAB_DATASET_STORE/<dataset>/patients/<human>.json", "  layers.raw.files  (the arrived files, previewed)",
            "GET /api/patients/{id}/layer/raw"],
    "source": ["$INLAB_DATASET_STORE/<dataset>/patients/<human>.json", "  source_tables  (every row; later ones ⚠ flagged)",
               "GET /api/patients/{id}/raw"],
    "record": ["$INLAB_DATASET_STORE/<dataset>/patients/<human>.json", "  layers.record.tables  (5-min grid, DT_s)",
               "GET /api/patients/{id}/layer/record"],
    "case": ["<human>.json record streams  (a row with text = a case)", "$INLAB_LABEL_STORES[<dataset>]  (label overlay)",
             "GET /api/cases?dataset=&human_id="],
    "internal": ["<human>.json source_tables as of the index date", "GET /api/patients/{id}  (later rows withheld)"],
    "external": ["nothing yet: a placeholder (the problem list it would search)"],
    "model": ["$INLAB_ENDPOINT_STORE/<package>/manifest.json · meta.json", "  model/config.json · model/prefn_config.json",
              "$INLAB_REGISTRY  {package: url}", "GET /api/models · /card · POST /api/predict → <url>/invocations"],
    "tasks": ["$INLAB_PROJECTS_ROOT/Project-*/tasks/<A01_*>/  (old layout)", "GET /api/tasks"],
    "checklist": ["the record + the last run → an LLM (Agent SDK)", "POST /api/checklist"],
    "annotate": ["$INLAB_LABEL_STORES[<dataset>]/<dim>/", "  .state.json · guideline/ · gallery/gallery.json · iterNN/",
                 "  human_decisions.jsonl  (the one write)", "GET /api/labeling/{dim} · POST …/decision"],
    "health": ["the resolved env: $INLAB_* · which endpoints answer /ping", "GET /api/health"],
}


def header(s: Sheet, f, title: str, sub: str, changes=()) -> float:
    s.text(40, 30, title, 30, f)
    y = 80
    for line in sub.split("\n"):
        s.text(40, y, line, 16, f)
        y += 24
    for date, what in changes:
        s.text(40, y, f"✎ {date} {what}", 16, f, GREEN)
        y += 24
    return y + 20


def screens(s: Sheet, f, x0: float, y0: float, shots: Path, keys, cols: int = 3, w: int = 560, red_if_stub=False) -> float:
    """A screenshot per view (shots/<key>.png) in a grid, its title over it and its "on disk" tree under it."""
    label = {k: f"{icon} {lab}  ·  {group}" for k, icon, lab, group in VIEWS}
    y_row, col, row_h = y0, 0, 0
    for key in keys:
        x = x0 + col * (w + 60)
        s.text(x, y_row, label.get(key, key), 20, f)
        h = s.image(shots / f"{key}.png", x, y_row + 34, w, f)
        if not h:
            s.text(x, y_row + 40, "? not shot", 18, f, RED)
            h = 40
        y = y_row + 34 + h + 14
        s.text(x, y, "on disk", 14, f)
        for line in DISK.get(key, []):
            y += 20
            s.text(x + 12, y, line, 14, f)
        row_h = max(row_h, y + 40 - y_row)
        col += 1
        if col == cols:
            y_row, col, row_h = y_row + row_h, 0, 0
    return y_row + row_h


def save(s: Sheet, f, bottom: float, out: Path, source: str) -> None:
    f["height"] = bottom + 40
    s.save(out, source)

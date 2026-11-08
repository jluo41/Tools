"""The walkthrough's raw data: 30 synthetic chats, one row per rater's answer (20 raters each), as chats/chats.csv.

The chats and the votes are the ones the meaning and expression Tasks already show (ex-00 to ex-29): the same six
placeholder asks and replies and the same synthetic votes (seed 3), taken from the workbench-labeling test builder,
so the items Task makes the very items those Tasks read. Every row is made up; nothing comes from a real dataset.

    python make_chats.py            writes chats/chats.csv beside this file
"""
from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[4]
BUILDER = TOOLS / "plugins/haipipe-toolkit/servers/workbench-labeling/tests/labeling_example.py"


def main() -> int:
    spec = importlib.util.spec_from_file_location("labeling_example", BUILDER)
    ex = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ex)
    chats = {c["item_id"]: c for c in ex.items()}
    rows = [{"chat_id": v["item_id"], "context": chats[v["item_id"]]["context_before"],
             "response": chats[v["item_id"]]["main"], "rater_id": v["rater_id"], "rater_gender": v["rater_gender"],
             "Q_overall": v["Q_overall"]} for v in ex.votes()]
    out = HERE / "chats" / "chats.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as handle:
        w = csv.DictWriter(handle, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} rows, {len(chats)} chats -> {out.relative_to(HERE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

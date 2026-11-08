"""Placeholder worker: hand over a clean copy of the agreed estimates, for the work theme's example Block.

Writes into RESULT_DIR (set by the Run's ticket) model-card.md, a placeholder model card written from the main Task's
values, then copies three files, unchanged, to this Task's address in the Block's delivery/ (haipipe-delivery:
b90/j02/t04 hands over into b90/delivery/j02/t04/<lane>/, through `delivery_dir` and `delivery_lane_dir`):

  the main Task's values.csv            -> delivery/j02_example_estimates/t04_deliver/data/estimates-v<N>.csv
  this Run's model-card.md              -> delivery/j02_example_estimates/t04_deliver/model/model-card-v<N>.md
  r01_build_site's index.html           -> delivery/j02_example_estimates/t04_deliver/web/index.html

A version is never written over: when the newest version already holds the same bytes it is kept, else the file is
saved as the next version beside it. The web page keeps one name, so the host can serve it at a fixed address; it is
replaced only while no row of delivery/delivery.md marks it sent, else the Run fails. Each new copy adds one `draft`
row to delivery/delivery.md; only a person writes `sent`.

Before 261106 this worker copied into the Block's own lanes (delivery/data, model, web). Those copies are retired the
way haipipe-delivery moves an old output: rebuild first, then remove the generated old copy. A copy goes only when the
new address holds the same bytes and every row naming it is this Job's `draft` row; a `sent` or `back` row keeps it.
Its draft rows go with it. Writes delivered.csv (lane, file, version, from, new) and headline.txt. Every number is made
up.
"""
from __future__ import annotations

import csv
import datetime
import filecmp
import os
import re
import shutil
import sys
from pathlib import Path

TASK = Path(__file__).resolve().parents[1]
JOB = TASK.parent
VALUES = JOB / "t01_example_main/runs/r01_example_main/result/values.csv"
SITE = TASK / "runs/r01_build_site/result/index.html"
READER = "readers of the example (placeholder)"
# No code marks above the table: a Job page picks its own rows by the file name between backticks before
# "from <job>", and a backtick above the first row would pair with that row's and hide it.
# The table needs no sentence over it: what a row means is haipipe-delivery's to say (round 3: "One row per send…" read
# as an instruction on the Delivery page). This worker's earlier sentences are taken out of the file when it runs.
WORDS_BEFORE = ("One row per send. A build adds a draft row; only a person writes sent.",                       # to 261106
                "One row per send. A build adds a `draft` row; only a person writes `sent`.")                   # its first
HEAD = ("# Delivery · the example Block's sends (placeholder)\n\n"
        "| date | for | from | status |\n|---|---|---|---|\n")
OLD = (("data", "estimates-v*.csv"), ("model", "model-card-v*.md"), ("web", "index.html"))   # the Block's own lanes


def helper():
    """haipipe-delivery's one helper module (haipipe-draft/src/common.py)."""
    sys.path.insert(0, str(Path(os.environ["HAIPIPE_TOOLKIT"]) / "skills/1_base/draft/haipipe-draft"))
    from src import common
    return common


def model_card(values: dict) -> str:
    v = lambda k: values[k]["value"]
    return (f"# Model card · the main association (placeholder)\n\n"
            f"Every number here is made up; it stands for a card a work Block hands over with its model.\n\n"
            f"## What it estimates\n\n"
            f"The association of <the policy> with <the outcome>, in points.\n\n"
            f"## The estimate\n\n"
            f"| value | as returned |\n|---|---|\n"
            f"| main association | {values['main.b']['text']} |\n"
            f"| p value | {v('main.p')} |\n"
            f"| units | {v('sample.n_units')} |\n"
            f"| mean before, after | {v('mean.before')}, {v('mean.after')} |\n\n"
            f"## Where it comes from\n\n"
            f"The main Task's Run (t01_example_main, r01_example_main): its values.csv, copied unchanged into the "
            f"delivery's data lane.\n\n"
            f"## Limits\n\n"
            f"A placeholder: no model was fitted and no unit is real.\n")


def sends(md: Path) -> list:
    return md.read_text(encoding="utf-8").splitlines() if md.is_file() else []


def place(src: Path, lane: Path, base: str, ext: str) -> tuple:
    """(file, version, new) for a versioned file: the newest version kept when it holds the same bytes, else the next."""
    lane.mkdir(parents=True, exist_ok=True)
    found = sorted((int(m.group(1)), p) for p in lane.glob(f"{base}-v*{ext}")
                   if (m := re.fullmatch(rf"{re.escape(base)}-v(\d+){re.escape(ext)}", p.name)))
    if found and filecmp.cmp(found[-1][1], src, shallow=False):
        return found[-1][1], found[-1][0], False
    n = found[-1][0] + 1 if found else 1
    dst = lane / f"{base}-v{n}{ext}"
    shutil.copyfile(src, dst)
    return dst, n, True


def place_fixed(src: Path, dst: Path, md: Path) -> tuple:
    """(file, version, new) for a file served at one address: replaced only while no row marks it sent."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    name = dst.relative_to(md.parent).as_posix()
    rows = [ln for ln in sends(md) if f"`{name}`" in ln]
    n = len(rows)
    if dst.is_file() and filecmp.cmp(dst, src, shallow=False):
        return dst, max(n, 1), False
    if any(re.search(r"\|\s*sent\s*\|\s*$", ln) for ln in rows):
        raise SystemExit(f"{name} was sent and differs: save it under a new name before replacing it")
    shutil.copyfile(src, dst)
    return dst, n + 1, True


def retire(deliv: Path, made: list, lines: list) -> tuple:
    """(lines, retired): remove this worker's superseded copies in the Block's own lanes and their draft rows."""
    retired = []
    for lane, pattern in OLD:
        for old in sorted((deliv / lane).glob(pattern)):
            name = old.relative_to(deliv).as_posix()
            rows = [ln for ln in lines if f"`{name}`" in ln]
            ours = rows and all(re.search(rf"\bfrom {re.escape(JOB.name)}/", ln)
                                and re.search(r"\|\s*draft\s*\|\s*$", ln) for ln in rows)
            moved = any(m[0] == lane and filecmp.cmp(old, m[2], shallow=False) for m in made)
            if not (ours and moved):
                continue
            old.unlink()
            lines = [ln for ln in lines if ln not in rows]
            retired.append((lane, name))
        if (deliv / lane).is_dir() and not any((deliv / lane).iterdir()):
            (deliv / lane).rmdir()
    return lines, retired


def main() -> None:
    res = Path(os.environ["RESULT_DIR"])
    with VALUES.open(encoding="utf-8") as f:
        values = {r["key"]: r for r in csv.DictReader(f)}
    (res / "model-card.md").write_text(model_card(values), encoding="utf-8")

    common = helper()
    deliv = common.delivery_dir(common.delivery_owner(TASK))       # the Block's delivery/, its one table of sends
    here = common.delivery_dir(TASK)                                # this Task's address in it
    md = deliv / "delivery.md"
    deliv.mkdir(parents=True, exist_ok=True)
    if not md.is_file():
        md.write_text(HEAD, encoding="utf-8")
    block = deliv.parent
    made = [("data", VALUES, *place(VALUES, here / "data", "estimates", ".csv")),
            ("model", res / "model-card.md", *place(res / "model-card.md", here / "model", "model-card", ".md")),
            ("web", SITE, *place_fixed(SITE, common.delivery_lane_dir(TASK, "web") / "index.html", md))]
    kept = sends(md)
    if any(ln in WORDS_BEFORE for ln in kept):           # the old sentence and the blank line after it
        at = next(i for i, ln in enumerate(kept) if ln in WORDS_BEFORE)
        kept = kept[:at] + kept[at + (2 if at + 1 < len(kept) and not kept[at + 1].strip() else 1):]
    lines, retired = retire(deliv, made, kept)
    today = f"{datetime.date.today():%y%m%d}"
    lines += [f"| {today} | {READER} | `{dst.relative_to(deliv).as_posix()}` (v{n}, from "
              f"{src.relative_to(block).parts[0]}/{src.relative_to(JOB).parts[0]}) | draft |"
              for lane, src, dst, n, new in made if new]
    md.write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8")
    with (res / "delivered.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["lane", "file", "version", "from", "new"])
        w.writerows([lane, dst.relative_to(block).as_posix(), f"v{n}", src.relative_to(block).as_posix(),
                     "yes" if new else "kept"] for lane, src, dst, n, new in made)
        w.writerows([lane, f"delivery/{name}", "", "", "retired"] for lane, name in retired)
    # the headline names each file by its name, not its path: it reads whole on a phone (round 3: "data/e stimates")
    said = "handed over: " + ", ".join(f"{dst.name} (v{n}{'' if new else ', kept'})" for _, _, dst, n, new in made)
    if retired:
        said += "; retired the old copies " + ", ".join(name for _, name in retired)
    (res / "headline.txt").write_text(said + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

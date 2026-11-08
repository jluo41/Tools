"""Build this Task's Evidence Bib and hand it over (placeholder example; the worker of runs/run-deliver-bib).

1. `paper_runs.py build-bib <task> --write` builds draft/evidence/bibex/<task>.bib from the complete Results.
2. A clean copy goes to this Task's address in the Block's delivery/: delivery/<job>/<task>/bib/<task>-v<N>.bib. A
   version delivery.md marks sent is never written over: a changed Bib becomes the next version.
3. Its row in delivery/delivery.md (draft; only a person marks a version sent).
4. The Run's own result/: headline.txt, handed-over.md and facts.json (its Ticket writes runtime.yaml).

Reads TASK_DIR, RESULT_DIR and HAIPIPE_TOOLKIT from its Ticket. Every path it writes down is relative to the Block.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

TASK = Path(os.environ["TASK_DIR"]).resolve()
RESULT = Path(os.environ["RESULT_DIR"]).resolve()
TK = Path(os.environ["HAIPIPE_TOOLKIT"]).resolve()
JOB, BLOCK = TASK.parent, TASK.parent.parent
FOR = "the Paper-Example's citation Job (placeholder)"
ROW = re.compile(r"^\|\s*(\d{6})\s*\|\s*(.*?)\s*\|\s*`([^`]+)`\s*\((v\d+), from ([^)]+)\)\s*\|\s*(\w+)\s*\|\s*$")


def rows(table: Path) -> list:
    text = table.read_text(encoding="utf-8") if table.is_file() else ""
    return [m.groups() for m in map(ROW.match, text.splitlines()) if m]


def main() -> int:
    script = TK / "skills/2_theme/discovery/haipipe-discovery/scripts/paper_runs.py"
    subprocess.run([sys.executable, str(script), "build-bib", str(TASK), "--write"], check=True)
    built = TASK / "draft" / "evidence" / "bibex" / f"{TASK.name}.bib"
    text = built.read_text(encoding="utf-8")
    keys = re.findall(r"(?m)^@\w+\{([^,\s]+),", text)

    deliv = BLOCK / "delivery"
    lane = deliv / JOB.name / TASK.name / "bib"
    table = deliv / "delivery.md"
    mine = {r[2]: r for r in rows(table)}
    n = 1
    while True:                                   # the newest version, or the next one when it was sent and changed
        name = f"{JOB.name}/{TASK.name}/bib/{TASK.name}-v{n}.bib"
        nxt = f"{JOB.name}/{TASK.name}/bib/{TASK.name}-v{n + 1}.bib"
        sent = mine.get(name, ("",) * 6)[5] == "sent"
        same = (deliv / name).is_file() and (deliv / name).read_text(encoding="utf-8") == text
        if nxt in mine or (deliv / nxt).is_file() or (sent and not same):
            n += 1
            continue
        break
    target = deliv / name
    lane.mkdir(parents=True, exist_ok=True)
    if not (sent and same):
        target.write_text(text, encoding="utf-8")

    today = dt.date.today().strftime("%y%m%d")
    row = f"| {today} | {FOR} | `{name}` (v{n}, from {JOB.name}/{TASK.name}) | {mine.get(name, ('',) * 6)[5] or 'draft'} |"
    head = ["# Delivery · the example Block's sends (placeholder)", "",
            "Written by `runs/run-deliver-bib` of each Task that hands its Evidence Bib over; only a person marks a "
            "version sent.", "", "| date | for | from | status |", "|---|---|---|---|"]
    lines = (table.read_text(encoding="utf-8").splitlines() if table.is_file() else head)
    at = next((i for i, ln in enumerate(lines) if (m := ROW.match(ln)) and m.group(3) == name), None)
    if at is None:
        lines.append(row)
    else:
        lines[at] = row
    table.parent.mkdir(parents=True, exist_ok=True)
    table.write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8")

    needs = []
    for card in sorted(TASK.glob("runs/r[0-9]*_*/result/r[0-9]*_*.md")):
        if re.search(r"(?mi)^- verification:\s*NEEDS\b", card.read_text(encoding="utf-8")):
            needs.append(card.parent.parent.name)
    rel = lambda p: p.relative_to(BLOCK).as_posix()
    headline = (f"{len(keys)} placeholder papers in the Evidence Bib, handed over as v{n}"
                + (f"; {len(needs)} citation{'s' if len(needs) != 1 else ''} still wait{'' if len(needs) != 1 else 's'} for a check" if needs else ""))
    RESULT.mkdir(parents=True, exist_ok=True)
    (RESULT / "handed-over.md").write_text(
        f"# The Evidence Bib, handed over (placeholder)\n\n- built: `{rel(built)}` ({len(keys)} entries: "
        + ", ".join(f"@{k}" for k in keys) + ")\n"
        f"- handed over: `{rel(target)}` (v{n}, {mine.get(name, ('',) * 6)[5] or 'draft'})\n"
        f"- for: {FOR}\n"
        + (f"- still to check: {', '.join(needs)} (its Card's verification line says NEEDS)\n" if needs else ""),
        encoding="utf-8")
    (RESULT / "facts.json").write_text(json.dumps({"entries": keys, "version": n, "needs_check": needs}) + "\n",
                                       encoding="utf-8")
    (RESULT / "headline.txt").write_text(headline + "\n", encoding="utf-8")
    print(json.dumps({"headline": headline, "bib": rel(target)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())

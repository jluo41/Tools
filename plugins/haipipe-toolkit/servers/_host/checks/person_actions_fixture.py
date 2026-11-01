"""Throwaway Projects for person_actions_browser.mjs: an insight Board and a design Block, each with one thing a person
can sign today (b11 s12, b12 s12, 261023). Placeholders only, under a folder you name; never a real Board.

    python person_actions_fixture.py <dir>      then serve <dir> with _host/serve.py --no-auth on a spare port

Insight: j04 gets two written pages to CHECK; j03 (every step done) is reopened, so its close can be signed.
Design: j03's top three designs are kept with draft predictions, and its release Runs are not made yet.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import yaml

SERVERS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SERVERS / "workbench-insight" / "tests"))
sys.path.insert(0, str(SERVERS / "workbench-design" / "tests"))
import design_fixture as FD  # noqa: E402
import plan_c_fixture as FI  # noqa: E402


def make(root: Path) -> None:
    board = FI.make(root) / FI.BOARD
    j04 = board / "j04_prototype-p2_data-demov3"
    for t in ("t03_K01_question-c", "t02_I01_question-b"):
        md = j04 / t / f"{t}.md"
        md.write_text(md.read_text().replace("answer-status: open", "answer-status: answered")
                      .replace("answer: ''", "answer: <one line>"))
    j03 = board / "j03_prototype-p2_data-demov2"
    md = j03 / f"{j03.name}.md"
    md.write_text(md.read_text().replace("state: closed", "state: open"))
    shutil.rmtree(j03 / "runs" / "run-close-j03")
    job = FD.make(root) / FD.BLOCK / "j03_g01_m04"
    for k, t in enumerate(sorted(p for p in job.iterdir() if p.name.startswith("t") and "_d" in p.name)):
        if k < 3:
            face = t / f"{t.name}.md"
            text = face.read_text()
            face.write_text(text.replace("state: " + yaml.safe_load(text.split("---")[1])["state"], "state: kept", 1))
            pred = yaml.safe_load((t / "prediction.yaml").read_text())
            (t / "prediction.yaml").write_text(yaml.safe_dump({**pred, "frozen": "draft"}, allow_unicode=True))
    for r in ("run-release-j03", "run-freeze-predictions-j03"):
        shutil.rmtree(job / "runs" / r)


if __name__ == "__main__":
    make(Path(sys.argv[1]))

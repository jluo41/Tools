"""Check hai-block A06: a Job is a fixed workflow whose close a command can check; it never waits on a person.

Every Job face (`examples/**/{work,blueprint}/<bNN>/<jNN_*>/<jNN_*>.md`) has a `close:` line. A close that waits on a person
(agreed, signed, approved, picked, JL says) is Studio work: the person's choice belongs to the sNN topic, and the Job
starts from what that topic hands over.

Run from the Tools-SPACE root:
  python3 plugins/haipipe-toolkit/skills/1_base/project/hai-block/scripts/job_close_check.py
Exit 0 when every Job's close is a check; each one that waits on a person is printed with ❗.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path.cwd()
PERSON = re.compile(r"\b(agreed|agrees|signed|signs|approved|approves|picked|picks|JL says|JL ok)\b", re.I)


def jobs() -> list[Path]:
    return sorted(f for d in (d for g in ("work", "blueprint") for d in ROOT.glob(f"examples/*/{g}/*/j[0-9]*_*")) if d.is_dir()
                  for f in [d / f"{d.name}.md"] if f.is_file())


def close_line(face: Path) -> str:
    m = re.search(r"^close:\s*(.*)$", face.read_text(encoding="utf-8", errors="replace"), re.M)
    return m.group(1).strip() if m else ""


def main() -> int:
    bad = []
    for face in jobs():
        close = close_line(face)
        hit = PERSON.search(close)
        if hit:
            bad.append(f"A06 {face.parent.relative_to(ROOT)}: close waits on a person ({hit.group(0)}): {close[:110]}")
    for line in bad:
        print("❗", line)
    print(f"{'❗' if bad else '✅'} job close: {len(jobs())} Jobs, {len(bad)} wait on a person")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

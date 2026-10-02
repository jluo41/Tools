"""scaffold_instance.py <instance> [--prototype <dir> --extract <parquet>] [--question <id>] · make an Instance.

A new Instance gets its board.md from --prototype and --extract (the extract's path under the
SPACE root); an existing one keeps its own.

For every Prototype question (ref/prototype-contract.md § The Instance), make
<rung>/<L><NN>-<name>/ in the Instance with:

    scripts/                 a copy of the Prototype question's scripts/
    scripts/prototype.lock   each copied file's sha256 at the copy: the base sync_instance.py compares against
    runs/<partition>.sh      one run ticket per partition the question is asked on

Never overwrites a file: a script already in the Instance is kept as it is (sync it
with sync_instance.py). Prints what it made, and any run ticket for a partition the
Prototype no longer asks.
"""
import argparse
import os
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_question import LOCK, META, asked_partitions, file_sha, front, question_folders  # noqa: E402

TICKET = """#!/bin/bash
# <partition>.sh · runs this question on the partition this file is named for, writing
# results/<partition>/ and reports/<partition>/ (haipipe-insight ref/prototype-contract.md § The run).
# The same lines in every run ticket; the file name is the partition.
R="$(cd "$(dirname "$0")" && while [ ! -f env.sh ] && [ "$PWD" != / ]; do cd ..; done; pwd)"
source "$R/env.sh" >/dev/null 2>&1
exec "$R/.venv/bin/python" "$R/Tools/plugins/haipipe-toolkit/skills/insight/haipipe-insight/ref/run_question.py" \\
  "$(cd "$(dirname "$0")/.." && pwd)" "$(basename "$0" .sh)"
"""
LOCK_HEAD = ("# prototype.lock · the Prototype file each script was copied from and its sha256 at the copy\n"
             "# (haipipe-insight ref/sync_instance.py reads and rewrites it; never edit by hand)\n")


def read_lock(scripts):
    path = Path(scripts) / LOCK
    return yaml.safe_load(path.read_text()) if path.is_file() else {"prototype": None, "files": {}}


def write_lock(scripts, lock):
    (Path(scripts) / LOCK).write_text(LOCK_HEAD + yaml.safe_dump(lock, sort_keys=False))


def copy_scripts(proto_q, inst_q):
    """Copy the Prototype's scripts/ into the Instance once; record each file's base hash in the lock."""
    src, dst = proto_q / "scripts", inst_q / "scripts"
    if not src.is_dir():
        return []
    dst.mkdir(parents=True, exist_ok=True)
    lock = read_lock(dst)
    made = []
    for f in sorted(src.glob("*.py")):
        target = dst / f.name
        if target.exists():
            continue
        target.write_bytes(f.read_bytes())
        lock["files"][f.name] = {"base": file_sha(f), "reviewed": None}
        made.append(target)
    if made:
        lock["prototype"] = os.path.relpath(src, dst)
        write_lock(dst, lock)
    return made


BOARD = """---
board-kind: insight-instance
prototype: {prototype}
extract: {extract}
---

# {name}

One extract read through `{proto_name}`. Each question folder holds a copy of the
Prototype question's scripts, one run per partition it is asked on, what each run
computed (results/) and reported (reports/), and the question's page. Every cell's
status is computed by haipipe-insight-check ref/check_instance.py.
"""


def make_board(instance, prototype, extract):
    """The Instance's board.md, when it has none: its Prototype (relative) and its extract."""
    instance, prototype = Path(instance).resolve(), Path(prototype).resolve()
    if (instance / "board.md").exists():
        return None
    if not str(extract).endswith(".parquet") or Path(extract).is_absolute():
        raise SystemExit("--extract is a .parquet path under the SPACE root, never absolute")
    instance.mkdir(parents=True, exist_ok=True)
    (instance / "board.md").write_text(BOARD.format(prototype=os.path.relpath(prototype, instance), extract=extract,
                                                    name=instance.name, proto_name=prototype.name), encoding="utf-8")
    return instance / "board.md"


def scaffold(instance, only=None, prototype=None, extract=None):
    instance = Path(instance).resolve()
    first = make_board(instance, prototype, extract) if prototype else None
    meta, _ = front(instance / "board.md")
    prototype = (instance / meta["prototype"]).resolve()
    partitions = front(prototype / META / "partitions.md")[0]["partitions"]
    names = {p["name"] for p in partitions}
    made, extra = [], []
    for pq in question_folders(prototype):
        if only and only not in (pq.name, pq.name[:3]):
            continue
        q = front(pq / f"{pq.name}.md")[0]
        iq = instance / pq.parent.name / pq.name
        made += copy_scripts(pq, iq)
        asked = asked_partitions(q, partitions)
        for name in asked:
            ticket = iq / "runs" / f"{name}.sh"
            if not ticket.exists():
                ticket.parent.mkdir(parents=True, exist_ok=True)
                ticket.write_text(TICKET)
                ticket.chmod(0o755)
                made.append(ticket)
        extra += [t for t in sorted((iq / "runs").glob("*.sh")) if t.stem in names and t.stem not in asked]
    if first:
        made.insert(0, first)
    for p in made:
        print(f"made   {p.relative_to(instance)}")
    for p in extra:
        print(f"extra  {p.relative_to(instance)}  (the Prototype no longer asks this partition)")
    return made, extra


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("instance")
    a.add_argument("--question", help="one question, by id (D01) or folder name")
    a.add_argument("--prototype", help="a new Instance: its Prototype board")
    a.add_argument("--extract", help="a new Instance: its extract, a .parquet path under the SPACE root")
    args = a.parse_args()
    if bool(args.prototype) != bool(args.extract):
        raise SystemExit("--prototype and --extract come together")
    scaffold(args.instance, args.question, args.prototype, args.extract)

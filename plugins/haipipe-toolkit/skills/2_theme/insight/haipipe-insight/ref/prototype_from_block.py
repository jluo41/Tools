"""prototype_from_block.py <Insight Block> <Prototype Block> [--release p1] [--serves <board>]

Carry an Insight Block's questions into a plan-C Prototype release (b11 s00 · s11 · s12, 261007). The
Prototype is its own work Block; each of its Jobs is one release, `jNN_pN/`, holding:

    jNN_pN.md         the release's face (release, state, from)
    release.yaml      every live question -> its Task (here, or in an earlier release), and what changed
    partitions.md     the cuts, defined before any outcome (front matter `partitions:`)
    thresholds.yaml   the shared values (cuts' floors, power, ...)
    src/              the shared code the scripts import
    tNN_<L><NN>_<slug>/question.md + scripts/   one Task per question: its spec and its one script

From an Insight Block (one Job per DIKW level, `meta/`, `src/`): each question's question.md and scripts/
are carried word for word, `meta/partitions.md` and `meta/thresholds.yaml` become the release's, and every
`src/` (the Block's and each level's) joins the release's src/ (a name in two of them is an error).
Never overwrites a file; prints what it made. The Block it reads is left as it is.
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_question import LEVEL_DIR, META, QFILE, front, question_folders, question_id  # noqa: E402


def _slug(task_name):
    return re.sub(r"^t\d{2}_", "", task_name).replace("_", "-")


def _write(path, text, made):
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    made.append(path)


def _front(fields, body):
    return "---\n" + yaml.safe_dump(fields, sort_keys=False, allow_unicode=True) + "---\n\n" + body


def carry(block, proto, release="p1", serves=""):
    block, proto = Path(block).resolve(), Path(proto).resolve()
    made, n = [], int(release[1:])
    job = proto / f"j{n:02d}_{release}"
    _write(proto / "board.md", _front({"board-kind": "prototype", "serves": serves},
                                      f"# {proto.name} · the Prototype\n\nThe questions and their scripts, one "
                                      "Job per release (jNN_pN/). A Board's Job pins one release and one data "
                                      "version; a release is cut from proposals/.\n"), made)
    _write(proto / "proposals" / "README.md", "# proposals\n\nThe backlog: new · fix · retire, one file each "
                                             "(`<slug>.md`: kind · DIKW level · from <job> · why). The next "
                                             "release is cut from here.\n", made)
    _write(job / f"{job.name}.md", _front({"release": release, "state": "open", "signed": "", "from": "",
                                           "carried-from": str(Path(*[".."] * 3, *block.parts[-2:]))},
                                          f"# {release} · the first release\n\nCarried from the Insight Block "
                                          f"{block.name}: its questions, scripts, cuts and thresholds.\n"), made)
    rows, k = {}, 0
    for qf in question_folders(block):
        k += 1
        qid = question_id(qf)
        name = f"t{k:02d}_{qid}_{_slug(qf.name)}"
        rows[qid] = {"task": name, "change": "new"}
        dst = job / name
        if not (dst / QFILE).exists():
            dst.mkdir(parents=True, exist_ok=True)
            shutil.copy2(qf / QFILE, dst / QFILE)
            made.append(dst / QFILE)
        if (qf / "scripts").is_dir() and not (dst / "scripts").exists():
            shutil.copytree(qf / "scripts", dst / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
            made.append(dst / "scripts")
    _write(job / "release.yaml", yaml.safe_dump({"release": release, "questions": rows}, sort_keys=False), made)
    for src, dst in ((block / META / "partitions.md", job / "partitions.md"),
                     (block / META / "thresholds.yaml", job / "thresholds.yaml")):
        if src.is_file() and not dst.exists():
            shutil.copy2(src, dst)
            made.append(dst)
    seen = {}
    for sdir in [block / "src"] + [block / d / "src" for d in LEVEL_DIR.values()]:
        for f in sorted(sdir.glob("*")) if sdir.is_dir() else []:
            if f.name == "__pycache__":
                continue
            if f.name in seen:
                raise SystemExit(f"src/{f.name} is in both {seen[f.name]} and {sdir}")
            seen[f.name] = sdir
            dst = job / "src" / f.name
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                (shutil.copytree if f.is_dir() else shutil.copy2)(f, dst)
                made.append(dst)
    return made


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("block")
    ap.add_argument("proto")
    ap.add_argument("--release", default="p1")
    ap.add_argument("--serves", default="")
    a = ap.parse_args()
    made = carry(a.block, a.proto, a.release, a.serves)
    root = Path(a.proto).resolve()
    for p in made:
        print("made", p.relative_to(root))
    print(f"{len(made)} made")


if __name__ == "__main__":
    main()

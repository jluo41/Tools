"""Project a design's newest draft, or its newest verdict, into its Task (haipipe-design/ref/design-ladder.md).

    python project_draft.py draft   <design Task folder>      after run-generate-d<NN> closes, or a run-revise pass
    python project_draft.py verdict <design Task folder>      after run-verify-d<NN>-v<k> closes

A hard Run writes only its own result/ and a revise only its pass; this projection is the workflow's. `draft` takes the
newest draft (k = 1 the generate's result/design.md, then one per run-revise-d<NN>/passes/pNN-<MMDD>/design.md),
writes its words into the face's ## Design, its element record into the Task's elements.yaml, `draft: k` and
`state: verify` on the face. `verdict` reads run-verify-d<NN>-v<k> for the face's current draft k: passed → `state:
passed`, failed → `state: revise`, and its tests into ## Evaluation. A verify of an older draft, or one still open,
is refused. Never touches a design already kept, dropped or released. Prints what it changed.
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

import yaml

DESIGN = re.compile(r"^t\d+_(d\d+)_(.+)$")
DONE = ("kept", "dropped", "released")


def _face(task: Path) -> Path:
    if not DESIGN.match(task.name):
        sys.exit(f"not a design Task tNN_d<NN>_<slug>: {task.name}")
    return task / f"{task.name}.md"


def front(md: Path) -> dict:
    m = re.match(r"(?s)^---\n(.*?)\n---\n", md.read_text(encoding="utf-8")) if md.is_file() else None
    return (yaml.safe_load(m.group(1)) or {}) if m else {}


def set_field(text: str, key: str, value) -> str:
    """Set a front-matter field, adding it when missing."""
    head, sep, body = text.partition("\n---\n")
    if re.search(rf"(?m)^{key}:", head):
        head = re.sub(rf"(?m)^{key}:.*$", f"{key}: {value}", head, count=1)
    else:
        head += f"\n{key}: {value}"
    return head + sep + body


def set_section(text: str, heading: str, body: str) -> str:
    pat = rf"(?ms)^(##\s+{heading}\s*\n)(.*?)(?=^##\s|\Z)"
    if re.search(pat, text):
        return re.sub(pat, lambda m: m.group(1) + "\n" + body.strip() + "\n\n", text, count=1)
    return text.rstrip("\n") + f"\n\n## {heading}\n\n{body.strip()}\n"


def drafts(task: Path) -> list:
    """[(k, folder holding design.md)] in order: the generate's result/, then each revise pass."""
    runs, d = task / "runs", DESIGN.match(task.name).group(1)
    out = []
    gen = runs / f"run-generate-{d}" / "result"
    if (gen / "design.md").is_file():
        out.append(gen)
    for rev in sorted(runs.glob(f"run-revise-{d}/passes/*")):
        if (rev / "design.md").is_file():
            out.append(rev)
    return list(enumerate(out, start=1))


def draft(task: Path) -> str:
    face = _face(task)
    f = front(face)
    if str(f.get("state", "")) in DONE:
        sys.exit(f"{task.name} is {f.get('state')}: its words are settled")
    ds = drafts(task)
    if not ds:
        sys.exit(f"{task.name} has no draft: run-generate-{DESIGN.match(task.name).group(1)} has written no "
                 "result/design.md yet")
    k, src = ds[-1]
    if str(f.get("draft", "")) == str(k):
        return f"{task.name}: draft {k} is already projected"
    text = face.read_text(encoding="utf-8")
    text = set_section(text, "Design", (src / "design.md").read_text(encoding="utf-8"))
    text = set_field(set_field(text, "draft", k), "state", "verify")
    face.write_text(text, encoding="utf-8")
    if (src / "elements.yaml").is_file():
        shutil.copy2(src / "elements.yaml", task / "elements.yaml")
    return f"{task.name}: draft {k} projected from {src.relative_to(task)}; state: verify"


def verdict(task: Path) -> str:
    face = _face(task)
    f = front(face)
    if str(f.get("state", "")) in DONE:
        sys.exit(f"{task.name} is {f.get('state')}: its verdict is settled")
    k, d = f.get("draft"), DESIGN.match(task.name).group(1)
    if not k:
        sys.exit(f"{task.name} has no projected draft: run `project_draft.py draft` first")
    run = task / "runs" / f"run-verify-{d}-v{k}"
    card = yaml.safe_load((run / "run.yaml").read_text(encoding="utf-8")) if (run / "run.yaml").is_file() else None
    if not isinstance(card, dict):
        sys.exit(f"no {run.name}: verify draft {k} first (the newest draft is the one judged)")
    status = str(card.get("status", ""))
    if status not in ("passed", "failed"):
        sys.exit(f"{run.name} is {status or 'open'}: project its verdict once it has closed")
    tests = card.get("tests") or {}
    line = " · ".join(f"{t} {v}" for t, v in tests.items()) if isinstance(tests, dict) else str(tests)
    state = "passed" if status == "passed" else "revise"
    text = set_section(face.read_text(encoding="utf-8"), "Evaluation",
                       f"v{k} ({card.get('by') or 'reviewer'}): {line or status} → {status}")
    face.write_text(set_field(text, "state", state), encoding="utf-8")
    return f"{task.name}: {run.name} {status}; state: {state}"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("what", choices=("draft", "verdict"))
    ap.add_argument("task", type=Path)
    a = ap.parse_args(argv)
    msg = (draft if a.what == "draft" else verdict)(a.task)
    print(msg)
    return msg


if __name__ == "__main__":
    main()

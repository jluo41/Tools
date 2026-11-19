"""insight_ladder's DataPrep commands (ref/dataprep.md): the Block that makes a Set's data versions, a prep version (the
tools, frozen once a person signs it), a step Task (one tool), the signature a person states, and a step's hard Runs,
one per dataset, whose output folder a Board adds as a data version (`data … --prep`)."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import yaml

from insight_ladder_base import (
    HERE, SLUG, PREP_BLOCK, PREP, STEP, Plan, front, with_front, runs_readme, face, face_kind)

TICKET = HERE.parents[3] / "1_base" / "task" / "haipipe-task" / "ref" / "run-sh-template.sh"   # the one Task ticket
SET = re.compile(r"^[A-Za-z][A-Za-z0-9]*$")


# ── the DataPrep Block ──────────────────────────────────────────────────────────────────────────────
def dataprep_goal(title: str, set_name: str) -> str:
    words = (title or f"the tools that turn the {set_name} datasets into analysis-ready data").strip()
    return f"{words[:1].upper()}{words[1:]}, one signed prep version at a time"


def dataprep(path: Path, set_name: str, serves: str, store: str, title: str, plan: Plan) -> None:
    if path.parent.name not in ("insight", "insights"):
        sys.exit(f"a DataPrep Block lives in <Project>/insight/, beside the Question Book and the Boards: {path}")
    if not PREP_BLOCK.match(path.name):
        sys.exit(f"a DataPrep Block is a special board, InsightDataPrep-<Set>: {path.name}")
    if not SET.match(set_name or "") or re.search(r"v\d+$", set_name):
        sys.exit("--set names the family of datasets, letters and digits, carrying no version (DrFirstExp, not "
                 "DrFirstExpv1)")
    if store.startswith("/"):
        sys.exit("--store is SPACE-relative (or through a variable), never absolute (the SPACE's AGENTS.md)")
    boards = [s.strip() for s in serves.split(",") if s.strip()]
    plan.write(path / "board.md", with_front(
        {"board-kind": "insight-dataprep", "workbench": "insight", "set": set_name,
         "store": store or "<SPACE-relative folder the Runs write the data to>", "serves": boards,
         "datasets": [], "goal": dataprep_goal(title, set_name)},
        f"\n# {path.name} · {title or set_name}\n\n"
        "The tools that turn the Set's raw datasets into analysis-ready data, one Job per prep version\n"
        "(`jNN_prep-vK_<slug>/`), frozen once a person signs it. A step Task's hard Run makes one dataset's folder in\n"
        "the store; a Board adds that folder as a data version and names the prep version that made it.\n\n"
        "## Background\n\n<where the data comes from · how rows were assigned · what is known to be wrong or missing>\n"))
    plan.write(path / "background" / "README.md", "# background\n\nWhat a reader needs before trusting the data: the "
               "source's own documents, the message content, the data owner's answers. Never a row of data: the rows "
               "stay in the store a Run writes to.\n")
    runs_readme(path, "dataprep", plan)


def add_dataset(block: Path, name: str, raw: str, why: str, plan: Plan) -> None:
    """A dataset of the Set: its short name, the SPACE-relative folder its raw rows sit in, why it belongs."""
    if face_kind(block) != "dataprep":
        sys.exit(f"{block.name} is not a DataPrep Block (board.md board-kind: insight-dataprep)")
    if not SET.match(name or "") or not raw:
        sys.exit("a dataset is: dataset <DataPrep> <Name> --raw <SPACE-relative raw folder> [--why …]")
    if raw.startswith("/"):
        sys.exit("--raw is SPACE-relative (or through a variable), never absolute")
    fields, body = front(block / "board.md")
    if name in [str(d.get("name")) for d in fields.get("datasets") or []]:
        sys.exit(f"{name} is already a dataset of {block.name}")
    fields.setdefault("datasets", []).append({"name": name, "raw": raw, "why": why or "<why it belongs to the Set>"})
    plan.write(block / "board.md", with_front(fields, body), replace=True)


def add_reference(block: Path, name: str, path: str, version: str, why: str, plan: Plan) -> None:
    """A reference table every dataset of the Set may join (an area or a prescriber table): not a dataset, read at the
    version named here (ref/dataprep.md rule 3)."""
    if face_kind(block) != "dataprep":
        sys.exit(f"{block.name} is not a DataPrep Block (board.md board-kind: insight-dataprep)")
    if not SLUG.match((name or "").lower()) or not path or not version:
        sys.exit("a reference is: reference <DataPrep> <name> --path <SPACE-relative file or folder> --version <its version>")
    if path.startswith("/"):
        sys.exit("--path is SPACE-relative (or through a variable), never absolute")
    fields, body = front(block / "board.md")
    if name in [str(r.get("name")) for r in fields.get("references") or []]:
        sys.exit(f"{name} is already a reference of {block.name}")
    fields.setdefault("references", []).append({"name": name, "path": path, "version": version,
                                                "why": why or "<what joins it, and why it is not a dataset>"})
    plan.write(block / "board.md", with_front(fields, body), replace=True)


# ── a prep version ──────────────────────────────────────────────────────────────────────────────────
def preps(block: Path) -> list[Path]:
    return sorted((p for p in block.iterdir() if p.is_dir() and PREP.match(p.name)),
                  key=lambda p: int(PREP.match(p.name).group(1))) if block.is_dir() else []


def steps(ver: Path) -> list[Path]:
    return sorted((p for p in ver.iterdir() if p.is_dir() and STEP.match(p.name)),
                  key=lambda p: int(STEP.match(p.name).group(1)))


def prep(block: Path, slug: str, carried_from: str, plan: Plan, order: str = "") -> Path:
    """The next prep version jNN_prep-vK_<slug>/: it starts from the newest one, every step's face and code copied (never
    its Runs); `carried_from` names the folder the first version's tools came from. `order` names the new version's
    steps in their order (`experiment,source,prepare-cohort`): a step the newest version has is copied to its new
    number, a new one is made empty, and one left out is not carried (ref/dataprep.md rule 2)."""
    if slug and not SLUG.match(slug):
        sys.exit(f"--slug is a few lower-case words joined by -: {slug!r}")
    names = [x.strip() for x in order.split(",") if x.strip()]
    if any(not SLUG.match(x) for x in names) or len(set(names)) != len(names):
        sys.exit(f"--steps names each step once, a few lower-case words joined by -: {order!r}")
    if face_kind(block) != "dataprep":
        sys.exit(f"{block.name} is not a DataPrep Block (board.md board-kind: insight-dataprep)")
    old = preps(block)
    if old and str(face(old[-1]).get("state")) != "closed":
        sys.exit(f"{old[-1].name} is still open: sign it (or work in it) before opening the next prep version")
    n = int(PREP.match(old[-1].name).group(1)) + 1 if old else 1
    path = block / (f"j{n:02d}_prep-v{n}_{slug}" if slug else f"j{n:02d}_prep-v{n}")
    prev = old[-1] if old else None
    fields = {"prep": f"prep-v{n}", "state": "open", "signed": "", "hash": "",
              "from": PREP.match(prev.name).group(2) if prev else ""}
    if carried_from:
        fields["carried-from"] = carried_from
    fields["goal"] = f"prep-v{n}" + (f", {slug.replace('-', ' ')}" if slug else "") + \
        ": the tools that make each dataset's folder, frozen once a person signs them"
    plan.write(path / f"{path.name}.md", with_front(fields, f"\n# prep-v{n}\n\n<what this prep version changes, and "
                                                           "why; each change names the step it is in>\n"))
    if prev and (prev / "src").is_dir():
        plan.copy(prev / "src", path / "src")
    have = {STEP.match(x.name).group(2): x for x in steps(prev)} if prev else {}
    for i, name in enumerate(names or list(have), 1):
        dst = path / f"t{i:02d}_{name}"
        src = have.get(name)
        if src is None:
            _new_step(dst, name, "", plan)
            continue
        plan.copy(src, dst)                                   # face, scripts, config; never runs/ or results/
        if not plan.dry:
            if src.name != dst.name:                          # its new place: the face carries the folder's name
                old_face = dst / f"{src.name}.md"
                old_face.rename(dst / f"{dst.name}.md")
                face_md = dst / f"{dst.name}.md"
                face_md.write_text(face_md.read_text(encoding="utf-8").replace(f"# {src.name}", f"# {dst.name}"),
                                   encoding="utf-8")
            _reset_agreed(dst)
            _one_config_per_dataset(dst)
            _reaim(dst, PREP.match(prev.name).group(2), f"prep-v{n}")
    runs_readme(path, "prep", plan)
    return path


def _reset_agreed(step_dir: Path) -> None:
    md = step_dir / f"{step_dir.name}.md"
    fields, body = front(md)
    if fields.get("agreed"):
        fields["agreed"] = ""
        md.write_text(with_front(fields, body), encoding="utf-8")


def _one_config_per_dataset(step_dir: Path) -> None:
    """A copied step keeps one Run config per dataset, the newest: the Runs it superseded do not travel, so neither
    do their configs. The first `run <step> dataset <name>` in the new version takes the one kept."""
    newest: dict[str, Path] = {}
    for cfg in sorted((step_dir / "scripts" / "config").glob("r[0-9][0-9]_*.yaml")):
        name = cfg.stem.split("_", 1)[1]
        if name in newest:
            newest[name].unlink()
        newest[name] = cfg


def _reaim(step_dir: Path, old: str, new: str) -> None:
    """A copied step's Run configs write the new version's folders: `…@<old>` becomes `…@<new>`, so a new prep version
    never writes a folder an older one made (rule 4)."""
    for cfg in (step_dir / "scripts" / "config").glob("r[0-9][0-9]_*.yaml"):
        text = cfg.read_text(encoding="utf-8")
        if f"@{old}" in text:
            cfg.write_text(text.replace(f"@{old}", f"@{new}"), encoding="utf-8")


def _prep_open(ver: Path) -> None:
    if not PREP.match(ver.name) or face_kind(ver.parent) != "dataprep":
        sys.exit(f"{ver.name} is not a prep version (insight/InsightDataPrep-<Set>/jNN_prep-vK_<slug>/)")
    if str(face(ver).get("state")) == "closed":
        sys.exit(f"{ver.name} is signed and frozen: open the next prep version (insight_ladder.py prep)")


def step(ver: Path, slug: str, does: str, plan: Plan) -> Path:
    """A step Task tNN_<slug>/ in an open prep version: one tool (join · cut · derive · document · compare), its face
    saying what it reads, writes and checks; its script and tickets follow the Task contract (haipipe-task)."""
    _prep_open(ver)
    if not SLUG.match(slug or ""):
        sys.exit("a step is: step <prep version> <slug> (a few lower-case words joined by -)")
    have = steps(ver)
    if any(STEP.match(s.name).group(2) == slug for s in have):
        sys.exit(f"{ver.name} already has a step {slug}")
    n = int(STEP.match(have[-1].name).group(1)) + 1 if have else 1
    return _new_step(ver / f"t{n:02d}_{slug}", slug, does, plan)


def _new_step(path: Path, slug: str, does: str, plan: Plan) -> Path:
    """An empty step Task at `path`: its face with placeholders, its config README, its runs README."""
    plan.write(path / f"{path.name}.md", with_front(
        {"step": slug, "worker": slug.replace("-", "_"), "reads": "<what it reads: raw folders, an earlier step>",
         "writes": "<the columns or files it adds>", "checks": ["<a check the output must pass, checkable>"],
         "agreed": "", "goal": does or f"<what the {slug} step does to every dataset, one sentence>"},
        f"\n# {path.name}\n\n<why this step exists; what a later step or a question reads from it>\n"))
    plan.write(path / "scripts" / "config" / "README.md", "# config\n\nOne file per Run, `rNN_<dataset>.yaml`: which "
               "dataset and where its output goes, read by the worker through $HAIPIPE_CONFIG. The config IS the Run's "
               "identity; its output folder is a new one named for this prep version (`…@prep-vK`).\n")
    runs_readme(path, "step", plan)
    return path


def prep_hash(ver: Path) -> str:
    """The first 12 hex of a sha256 over the tools: src/ and every step's face, scripts and config."""
    h = hashlib.sha256()
    files = sorted(p for p in (ver / "src").rglob("*") if p.is_file()) if (ver / "src").is_dir() else []
    for s in steps(ver):
        files.append(s / f"{s.name}.md")
        files += sorted(p for p in (s / "scripts").rglob("*") if p.is_file()) if (s / "scripts").is_dir() else []
    for f in files:
        if f.is_file() and "__pycache__" not in f.parts:
            h.update(f.relative_to(ver).as_posix().encode() + b"\0" + f.read_bytes())
    return h.hexdigest()[:12]


def sign_prep(ver: Path, date: str, plan: Plan) -> None:
    """Record the signature a person states (✅ <YYMMDD>; never a name), pin the tools' hash, freeze the version."""
    _prep_open(ver)
    if not re.fullmatch(r"\d{6}", date or ""):
        sys.exit("--date is the day the person signed, YYMMDD")
    if not steps(ver):
        sys.exit(f"{ver.name} has no step yet (insight_ladder.py step)")
    unagreed = [s.name for s in steps(ver) if not str(face(s).get("agreed", "")).startswith("✅")]
    if unagreed:
        sys.exit(f"not agreed yet (another agent reviews each step's script and checks): {', '.join(unagreed)}")
    bad = outputs(ver)
    if bad:
        sys.exit(f"{ver.name}: a Run writes a folder made before, or one a Board's data version names (each output "
                 f"is a new folder ending @{PREP.match(ver.name).group(2)}): "
                 + "; ".join(f"{r} -> {n}" for r, n in bad))
    fields, body = front(ver / f"{ver.name}.md")
    fields.update(state="closed", signed=f"✅ {date}", hash=prep_hash(ver))
    plan.write(ver / f"{ver.name}.md", with_front(fields, body), replace=True)


# ── a step's hard Runs, one per dataset ─────────────────────────────────────────────────────────────
def dataset_run(step_dir: Path, name: str, plan: Plan, again: bool = False) -> Path:
    """runs/rNN_<name>/: the Task ticket (haipipe-task's run-sh-template), its card, and its config in scripts/config/.
    rNN is the next number in the step; the config says which dataset and where the output goes. A dataset that has a
    Run gets that Run back; with `again` it gets the next one, which names the newest in `supersedes:` and starts from
    its ticket and config, so a carried ticket keeps its own lines. Once the new Run has run, haipipe-run
    `prune_runs.py <step> --apply --only <step>/<old Run>` removes the old one (ref/dataprep.md § A second Run)."""
    if not SLUG.match(name or ""):
        sys.exit("a dataset Run is: run <step> dataset <name> (lower-case, e.g. smsr2v1)")
    ver, block = step_dir.parent, step_dir.parent.parent
    have = sorted(p for p in (step_dir / "runs").glob("r[0-9][0-9]_*") if p.is_dir())
    same = [p for p in have if p.name.split("_", 1)[1] == name]
    if same and not again:
        return same[-1]
    n = max((int(p.name[1:3]) for p in have), default=0) + 1
    run = f"r{n:02d}_{name}"
    path = step_dir / "runs" / run
    k = PREP.match(ver.name).group(2)
    cfgdir = step_dir / "scripts" / "config"
    if same:                                               # a second Run: the newest one's ticket and config, carried
        old = same[-1]
        old_ticket = old / f"{old.name}.sh"
        plan.write(path / f"{run}.sh", old_ticket.read_text(encoding="utf-8") if old_ticket.is_file()
                   else TICKET.read_text(encoding="utf-8"))
        if not plan.dry:
            (path / f"{run}.sh").chmod(0o755)
        if (cfgdir / f"{old.name}.yaml").is_file():
            plan.write(cfgdir / f"{run}.yaml", (cfgdir / f"{old.name}.yaml").read_text(encoding="utf-8"))
        plan.write(path / "run.yaml", "".join(f"{key}: {v}\n" for key, v in (
            ("run", run), ("kind", "hard"), ("type", "dataset"), ("target", step_dir.name), ("prep", k),
            ("ticket", f"{run}.sh"), ("supersedes", old.name), ("status", "planned"), ("passes", "[]"))))
        return path
    carried = sorted(c for c in cfgdir.glob(f"r[0-9][0-9]_{name}.yaml") if not (step_dir / "runs" / c.stem).is_dir())
    if carried and not (cfgdir / f"{run}.yaml").exists():   # copied with the step from the version before: it is this
        plan.made.append(cfgdir / f"{run}.yaml")             # dataset's config, under the new Run's name
        if not plan.dry:
            carried[-1].rename(cfgdir / f"{run}.yaml")
    worker = str(face(step_dir).get("worker") or STEP.match(step_dir.name).group(2).replace("-", "_"))
    ticket = TICKET.read_text(encoding="utf-8").replace('TASK_NAME="worker"', f'TASK_NAME="{worker}"', 1)
    plan.write(path / f"{run}.sh", ticket)
    if not plan.dry:
        (path / f"{run}.sh").chmod(0o755)
    store = str(front(block / "board.md")[0].get("store") or "<store>").rstrip("/")
    plan.write(cfgdir / f"{run}.yaml",
               f"# Run contract for {run}. The worker reads this file through $HAIPIPE_CONFIG (the ticket exports no\n"
               f"# env:); it names no default dataset and stops without one. Its output is a new folder named for {k}:\n"
               f"# a folder an older version made, or a Board's data version names, is never written (ref/dataprep.md).\n\n"
               f"dataset: \"<the dataset's name in board.md datasets>\"\n\noutput:\n"
               f"  prepare_dir: {store}/<DATE>_<DATASET>@{k}\n")
    plan.write(path / "run.yaml", "".join(f"{k}: {v}\n" for k, v in (
        ("run", run), ("kind", "hard"), ("type", "dataset"), ("target", step_dir.name),
        ("prep", PREP.match(ver.name).group(2)), ("ticket", f"{run}.sh"), ("status", "planned"), ("passes", "[]"))))
    return path


# ── a Board's data version names the prep that made it ──────────────────────────────────────────────
def prep_of(project: Path, ref: str) -> Path:
    """The prep version a Board's `--prep` names: the version itself or one of its Runs, Project-relative (or, for a
    DataPrep Block in another Project, SPACE-relative: the first folder above the Project that holds it); signed."""
    base = next((b for b in [project, *project.parents] if (b / ref).exists()), project)
    p = (base / ref).resolve()
    ver = next((a for a in [p, *p.parents] if PREP.match(a.name) and face_kind(a.parent) == "dataprep"), None)
    if ver is None:
        sys.exit(f"--prep {ref}: not a prep version, or a Run of one, of an InsightDataPrep Block (Project- or SPACE-relative)")
    if str(face(ver).get("state")) != "closed" or not str(face(ver).get("signed", "")).startswith("✅"):
        sys.exit(f"{ver.name} is not signed: a person signs a prep version before a Board adds what it made")
    return ver


def serving(board: Path) -> list[Path]:
    """The DataPrep Blocks whose `serves:` names this Board, in its Project or in another Project of the SPACE (a serves
    path is Project-relative, or SPACE-relative for a Board in another Project)."""
    board, project = board.resolve(), board.resolve().parent.parent
    seen, out = set(), []
    for root, pattern in ((project, "insight/InsightDataPrep-*"), (project.parent, "*/insight/InsightDataPrep-*"),
                          (project.parent.parent, "*/*/insight/InsightDataPrep-*")):
        for block in sorted(root.glob(pattern)) if root.is_dir() else []:
            if block in seen or face_kind(block) != "dataprep":
                continue
            seen.add(block)
            home = block.parent.parent
            for ref in front(block / "board.md")[0].get("serves") or []:
                if any((b / str(ref)).resolve() == board for b in [home, *home.parents]):
                    out.append(block)
                    break
    return out


# the checks a DataPrep Block is held to: outputs, inputs, record values and the audit (ref/dataprep.md)
from insight_ladder_prep_checks import outputs, inputs, records, raw_gone, references_off, audit  # noqa: E402,F401

"""insight_ladder's DataPrep commands (ref/dataprep.md; JL 261120): the Block that holds the code that turns a raw
export into a folder ready for insight, as the Question Book holds the questions' code. A prep version is a chain of
steps, frozen once a person signs it; a step is a spec (`step.md`) and one script exposing `run(ctx)`. The DataPrep
Block runs nothing: a Board runs a signed prep version on its own dataset (insight_ladder_datajob.py, ref/run_prep.py)."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

from insight_ladder_base import SLUG, PREP_BLOCK, PREP, STEP, Plan, front, with_front, runs_readme, face, face_kind

SET = re.compile(r"^[A-Za-z][A-Za-z0-9]*$")
SCRIPT = '''"""{slug} · one step of a prep version (hai-insight ref/dataprep.md). ref/run_prep.py calls run(ctx) once per
Board data Job, on that Board's dataset: ctx.raw (its raw export folder), ctx.out (where this step writes), ctx.prev (the
earlier step's output, or None), ctx.cut and ctx.params (the Board's), ctx.refs ({{name: path}}), ctx.dataset,
ctx.refuse(reason).
Aggregates only in anything a page shows; rows go to ctx.out."""


def run(ctx):
    ctx.refuse("not written yet")
'''


# ── the DataPrep Block ──────────────────────────────────────────────────────────────────────────────
def dataprep_goal(title: str, set_name: str) -> str:
    words = (title or f"the code that turns each {set_name} raw export into a folder ready for insight").strip()
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
         "store": store or "<SPACE-relative folder a Board's last step writes the ready folder to>", "serves": boards,
         "references": [], "goal": dataprep_goal(title, set_name)},
        f"\n# {path.name} · {title or set_name}\n\n"
        "The code that turns a raw export into a folder ready for insight, one Job per prep version\n"
        "(`jNN_prep-vK_<slug>/`), frozen once a person signs it. It runs nothing: each Board it serves runs a signed\n"
        "prep version on its own dataset, in a data Job, and adds the folder as its next data version.\n\n"
        "## Background\n\n<where the data comes from · how rows were assigned · what is known to be wrong or missing>\n"))
    plan.write(path / "background" / "README.md", "# background\n\nWhat a reader needs before trusting the data: the "
               "source's own documents, the message content, the data owner's answers. Never a row of data.\n")
    runs_readme(path, "dataprep", plan)


def add_reference(block: Path, name: str, path: str, version: str, why: str, plan: Plan) -> None:
    """A reference table every step may join (an area or a prescriber table): not a dataset, read at the version
    named here (ref/dataprep.md rule 3)."""
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


# ── a prep version: a chain of steps ────────────────────────────────────────────────────────────────
def preps(block: Path) -> list[Path]:
    return sorted((p for p in block.iterdir() if p.is_dir() and PREP.match(p.name)),
                  key=lambda p: int(PREP.match(p.name).group(1))) if block.is_dir() else []


def steps(ver: Path) -> list[Path]:
    return sorted((p for p in ver.iterdir() if p.is_dir() and STEP.match(p.name)),
                  key=lambda p: int(STEP.match(p.name).group(1)))


def spec(step_dir: Path) -> dict:
    """A step's spec, `step.md`: step · script · reads · writes · checks · cut and params (the keys of ctx.cut and
    ctx.params it reads) · agreed."""
    return front(step_dir / "step.md")[0]


def script_of(step_dir: Path) -> Path:
    s = spec(step_dir)
    return step_dir / "scripts" / f"{s.get('script') or STEP.match(step_dir.name).group(2).replace('-', '_')}.py"


def prep(block: Path, slug: str, carried_from: str, plan: Plan, order: str = "") -> Path:
    """The next prep version jNN_prep-vK_<slug>/: it starts from the newest one, each step's face, spec and scripts
    copied; `order` names the new version's steps in their order (`experiment,source,prepare-cohort`): a step the newest
    version has moves to its new number, a new one is made empty, one left out is not carried (rule 2)."""
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
        ": the code chain that turns a raw export into a folder ready for insight, frozen once a person signs it"
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
        plan.copy(src, dst, also=("notebooks", "config", f"{src.name}.md"))   # the spec and the scripts: code only
        if not plan.dry:
            old_face = front(src / f"{src.name}.md")[0]            # an older step's face: its goal moves into step.md
            fields, body = front(dst / "step.md")
            if old_face.get("goal") and not fields.get("goal"):
                fields["goal"] = old_face["goal"]
                (dst / "step.md").write_text(with_front(fields, body), encoding="utf-8")
            _reset_agreed(dst)
    runs_readme(path, "prep", plan)
    return path


def _reset_agreed(step_dir: Path) -> None:
    md = step_dir / "step.md"
    fields, body = front(md)
    if fields.get("agreed"):
        fields["agreed"] = ""
        md.write_text(with_front(fields, body), encoding="utf-8")


def _prep_open(ver: Path) -> None:
    if not PREP.match(ver.name) or face_kind(ver.parent) != "dataprep":
        sys.exit(f"{ver.name} is not a prep version (insight/InsightDataPrep-<Set>/jNN_prep-vK_<slug>/)")
    if str(face(ver).get("state")) == "closed":
        sys.exit(f"{ver.name} is signed and frozen: open the next prep version (insight_ladder.py prep)")


def step(ver: Path, slug: str, does: str, plan: Plan) -> Path:
    """The next step tNN_<slug>/ of an open prep version: its spec `step.md` (with its goal line) and its script
    `scripts/<slug>.py` with run(ctx) waiting to be written."""
    _prep_open(ver)
    if not SLUG.match(slug or ""):
        sys.exit("a step is: step <prep version> <slug> (a few lower-case words joined by -)")
    have = steps(ver)
    if any(STEP.match(s.name).group(2) == slug for s in have):
        sys.exit(f"{ver.name} already has a step {slug}")
    n = int(STEP.match(have[-1].name).group(1)) + 1 if have else 1
    return _new_step(ver / f"t{n:02d}_{slug}", slug, does, plan)


def _new_step(path: Path, slug: str, does: str, plan: Plan) -> Path:
    """A code-only step, as a question is: its spec `step.md` (with its goal line) and `scripts/<script>.py`; no face of
    its own, no runs/ (JL 261120)."""
    script = slug.replace("-", "_")
    goal = does or f"<what the {slug} step does to a raw export, one sentence>"
    plan.write(path / "step.md", with_front(
        {"step": slug, "script": script, "goal": goal, "reads": "<ctx.raw, ctx.prev or a reference: what it reads>",
         "writes": "<what it writes to ctx.out>", "checks": ["<a check that stops the Run when it fails>"],
         "cut": [], "params": [], "agreed": ""},
        f"\n# {slug}\n\n<why this step exists; what a later step or a question reads from it>\n"))
    plan.write(path / "scripts" / f"{script}.py", SCRIPT.format(slug=slug))
    return path


def prep_hash(ver: Path) -> str:
    """The first 12 hex of a sha256 over the code: src/ and every step's face, spec and scripts."""
    h = hashlib.sha256()
    files = sorted(p for p in (ver / "src").rglob("*") if p.is_file()) if (ver / "src").is_dir() else []
    for s in steps(ver):
        files += [s / f"{s.name}.md", s / "step.md"]
        files += sorted(p for p in (s / "scripts").rglob("*") if p.is_file()) if (s / "scripts").is_dir() else []
    for f in files:
        if f.is_file() and "__pycache__" not in f.parts:
            h.update(f.relative_to(ver).as_posix().encode() + b"\0" + f.read_bytes())
    return h.hexdigest()[:12]


def sign_prep(ver: Path, date: str, plan: Plan) -> None:
    """Record the signature a person states (✅ <YYMMDD>; never a name), pin the code's hash, freeze the version."""
    _prep_open(ver)
    if not re.fullmatch(r"\d{6}", date or ""):
        sys.exit("--date is the day the person signed, YYMMDD")
    if not steps(ver):
        sys.exit(f"{ver.name} has no step yet (insight_ladder.py step)")
    unwritten = [s.name for s in steps(ver) if not script_of(s).is_file() or "def run(" not in script_of(s).read_text(
        encoding="utf-8")]
    if unwritten:
        sys.exit(f"each step's script exposes run(ctx); not yet: {', '.join(unwritten)}")
    unagreed = [s.name for s in steps(ver) if not str(spec(s).get("agreed", "")).startswith("✅")]
    if unagreed:
        sys.exit(f"not agreed yet (another agent reviews each step's spec and script): {', '.join(unagreed)}")
    fields, body = front(ver / f"{ver.name}.md")
    fields.update(state="closed", signed=f"✅ {date}", hash=prep_hash(ver))
    plan.write(ver / f"{ver.name}.md", with_front(fields, body), replace=True)


def declared(ver: Path) -> dict[str, set]:
    """The cut and params keys a prep version's steps read, from their step.md `cut:` and `params:` lists (rule 3)."""
    out = {"cut": set(), "params": set()}
    for s in steps(ver):
        for key in out:
            out[key] |= {str(k) for k in spec(s).get(key) or []}
    return out


def undeclared(ver: Path, cut: dict, params: dict) -> list[str]:
    """Each Board cut or params key no step of the prep version reads: a key nobody reads is refused, never ignored."""
    have = declared(ver)
    return [f"{key} {k}" for key, given in (("cut", cut), ("params", params)) for k in (given or {}) if k not in have[key]]


def prep_version(block: Path, pid: str) -> Path | None:
    """The folder of prep version `pid` (prep-v2) in a DataPrep Block."""
    return next((v for v in preps(block) if PREP.match(v.name).group(2) == pid), None)


def signed(ver: Path) -> bool:
    return str(face(ver).get("state")) == "closed" and str(face(ver).get("signed", "")).startswith("✅")


def serving(board: Path) -> list[Path]:
    """The DataPrep Blocks whose `serves:` names this Board, in its Project or in another Project of the SPACE."""
    board, project = board.resolve(), board.resolve().parent.parent
    seen, out = set(), []
    for root, pattern in ((project, "insight/InsightDataPrep-*"), (project.parent, "*/insight/InsightDataPrep-*"),
                          (project.parent.parent, "*/*/insight/InsightDataPrep-*")):
        for block in sorted(root.glob(pattern)) if root.is_dir() else []:
            if block in seen or face_kind(block) != "dataprep":
                continue
            seen.add(block)
            home = block.parent.parent
            if any(any((b / str(ref)).resolve() == board for b in [home, *home.parents])
                   for ref in front(block / "board.md")[0].get("serves") or []):
                out.append(block)
    return out


# the checks a DataPrep Block is held to, and its audit (ref/dataprep.md)
from insight_ladder_prep_checks import references_off, records, audit  # noqa: E402,F401

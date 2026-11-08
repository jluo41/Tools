"""What a paper Board prints, read once for the evidence Runs: its writing Job, the Sections it prints, each Section's
sentences (by id), each display's rows, and workbench links. Shared by values_ledger.py (j02_evidence_value) and
cite_tasks.py (j03_evidence_cite); it reads only and writes nothing.

Two page shapes, one reader (haipipe-paper-evidence 0.7.0, JL 261103: "how do you think you can unify them together"):

    draft      the newest `draft/<section>-draft-v*.md`, its `## 3 · Draft` lines `- B<n> · S<id> · <sentence>`;
               a sentence's id is its S id without the S (`5`, `5a`), as evidence cards write `for:`
    content    the Section page's `## Content`, one sentence per `<!-- realizes: <id> -->` line (id as written); a line
               with no marker is split into sentences, each `<paragraph>.<k>` (`C1.P1.2`)

`printed(section)` lists what the paper exports, the `## Content` (each line named by its draft S id when the draft holds
the same text), else the draft when the Content is still a placeholder. `index(section)` is every id of both shapes, so
a card bound to either kind of id finds its sentence.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path
from urllib.parse import quote

TASK = re.compile(r"^t(\d+)_")
WRITING = re.compile(r"^j\d+_(?:writing_)?v\d")
DRAFT_LINE = re.compile(r"^- B\w+ · S(\d+[a-z]*) · (.*)$", re.M)
REALIZES = re.compile(r"<!--\s*realizes:\s*([^ ]+?)\s*-->")


# ── where things are ────────────────────────────────────────────────────────────────────────────────────────────────
def project_root(path: Path) -> Path:
    for p in [Path(path).resolve(), *Path(path).resolve().parents]:
        if (p / "project.yaml").is_file():
            return p
    raise SystemExit(f"{path}: no project.yaml above it")


def server_root(path: Path) -> Path:
    """The SPACE whose workbench serves this folder: a Tools checkout first (its blueprints are served from its own root,
    `blueprints/...`, wherever it sits: a SPACE's submodule or a clone of its own; 261106: a ticket rerun inside a
    SPACE wrote `Tools/blueprints/...` links the Tools workbench could not open), then the nearest folder with
    `.server_config/`, else a repository root (pyproject.toml beside code/, or a `.git` folder); workbench links are
    relative to it."""
    path = Path(path).resolve()
    for test in (lambda p: (p / "blueprints").is_dir() and (p / "plugins" / "haipipe-toolkit").is_dir(),
                 lambda p: (p / ".server_config").is_dir(),
                 lambda p: (p / "pyproject.toml").is_file() and (p / "code").is_dir(),
                 lambda p: (p / ".git").is_dir()):
        hit = next((p for p in [path, *path.parents] if test(p)), None)
        if hit is not None:
            return hit
    return path


def board_of(path: Path) -> Path:
    for p in [Path(path).resolve(), *Path(path).resolve().parents]:
        if (p / "board.md").is_file():
            return p
    raise SystemExit(f"{path}: no board.md above it (not inside a paper Board)")


def writing_job(board: Path, name: str | None = None) -> Path | None:
    """The writing Job the evidence is checked against: the one named, else the Board's newest `jNN_writing_v<MMDD>_`."""
    if name:
        job = board / name
        return job if job.is_dir() else None
    jobs = [j for j in board.glob("j[0-9]*_*") if j.is_dir() and WRITING.match(j.name)]
    return max(jobs, key=lambda j: int(re.match(r"j(\d+)", j.name).group(1)), default=None)


def tasks(job: Path) -> list[Path]:
    return sorted((p for p in job.iterdir() if p.is_dir() and TASK.match(p.name)), key=lambda p: int(TASK.match(p.name).group(1)))


def compile_order(job: Path) -> list[str]:
    face = job / f"{job.name}.md"
    m = re.search(r"(?s)<!-- haipipe:compile-order:start -->(.*?)<!-- haipipe:compile-order:end -->",
                  face.read_text(encoding="utf-8")) if face.is_file() else None
    return re.findall(r"(?m)^\s*-\s*(t\d+_[\w.-]+)", m.group(1)) if m else []


def sections(job: Path) -> list[Path]:
    """The Sections the version prints: its compile order plus its letters (t3N), else every tNN_ Task."""
    order = compile_order(job)
    every = tasks(job)
    if not order:
        return every
    letters = [t for t in every if int(TASK.match(t.name).group(1)) >= 30 and t.name not in order]
    return [job / n for n in order if (job / n).is_dir()] + letters


# ── sentences ───────────────────────────────────────────────────────────────────────────────────────────────────────
def draft_sentences(section: Path) -> tuple[dict, str]:
    """S id (no S) → sentence, from the newest draft's `## <n> · Draft`; ({}, '') when there is none."""
    drafts = sorted(section.glob(f"draft/{section.name}-draft-v*.md"),
                    key=lambda p: [int(x) for x in re.findall(r"\d+", p.name.rsplit("-v", 1)[1])])
    if not drafts:
        return {}, ""
    text = drafts[-1].read_text(encoding="utf-8")
    m = re.search(r"(?m)^## (?:\d+ · )?Draft\b.*$", text)
    if not m:
        return {}, drafts[-1].name
    part = re.split(r"\n## ", text[m.end():], maxsplit=1)[0]
    return {g[0]: g[1].strip() for g in DRAFT_LINE.findall(part)}, drafts[-1].name


def _placeholder(s: str) -> bool:
    return bool(re.fullmatch(r"<[^<>]*>\.?", s.strip()))


SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z<\\(])")


def content_sentences(section: Path) -> list[dict]:
    """[{id, text, para}] of the Section page's `## Content`, in order (placeholder lines skipped)."""
    page = section / f"{section.name}.md"
    if not page.is_file():
        return []
    text = page.read_text(encoding="utf-8")
    m = re.search(r"(?m)^## Content\s*$", text)
    if not m:
        return []
    body = text[m.end():]
    n = re.search(r"(?m)^## (?!#)", body)
    body = body[:n.start()] if n else body
    out, para, k, npara = [], "", 0, 0
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("#"):
            head = s.lstrip("# ").strip()
            code = re.match(r"(C\d+\.P\d+)\b", head)
            npara += 1
            para, k = (code.group(1) if code else f"P{npara}"), 0
            continue
        if not s or s.startswith((">", "|", "```")) or (s.startswith("<!--") and s.endswith("-->")) or _placeholder(s):
            continue
        rid = REALIZES.search(s)
        plain = re.sub(r"\s*<!--.*?-->", "", s).strip()
        if rid:
            out.append({"id": rid.group(1), "text": plain, "para": para})
            continue
        if not para:
            npara += 1
            para = f"P{npara}"
        for sent in SPLIT.split(plain):
            k += 1
            out.append({"id": f"{para}.{k}", "text": sent.strip(), "para": para})
    return out


def printed(section: Path) -> list[dict]:
    """What the Section prints, in order: [{id, text, para}]; the Content, else the draft's sentences."""
    drafted, _ = draft_sentences(section)
    by_text = {v: k for k, v in drafted.items()}
    lines = content_sentences(section)
    if lines:
        return [dict(x, id=by_text.get(x["text"], x["id"])) for x in lines]
    return [{"id": k, "text": v, "para": ""} for k, v in drafted.items()]


def index(section: Path) -> dict:
    """Every sentence id of both shapes → its text (draft S ids, then Content ids)."""
    drafted, _ = draft_sentences(section)
    out = dict(drafted)
    for x in content_sentences(section):
        out.setdefault(x["id"], x["text"])
    return out


def where_of(section: str, sid: str) -> str:
    """`t03_results S5` for a draft S id, `t03_results C1.P2.B1` for a Content id."""
    return f"{section} S{sid}" if re.fullmatch(r"\d+[a-z]*", str(sid)) else f"{section} {sid}"


# ── displays ────────────────────────────────────────────────────────────────────────────────────────────────────────
def rows_of(path: Path) -> list[dict]:
    """A .csv's rows as dicts; a Markdown table file's rows the same way."""
    if path.suffix == ".csv":
        with path.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    out, head = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or set(line) <= set("|-: "):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if head is None:
            head = cells
        elif cells != head:
            out.append(dict(zip(head, cells)))
    return out


def tex_rows(tex: str) -> list[str]:
    """Each row of a LaTeX table body that holds a number, as plain words with ` | ` between cells."""
    body = re.sub(r"\\(?:textsuperscript|footnotesize|small|parbox|raggedright|label)\{[^{}]*\}", " ", tex)
    out = []
    for row in body.split("\\\\"):
        cells = re.sub(r"\\[a-zA-Z]+\*?|[{}$]", " ", row).replace("&", " | ").replace("%", "%")
        cells = re.sub(r"(?m)^\s*%.*$", "", cells)
        if re.search(r"\d", cells):
            out.append(" ".join(cells.split()))
    return out


def _field(text: str, name: str) -> str:
    m = re.search(r"(?mi)^\W*" + re.escape(name) + r":[ \t]*(.+)$", text)
    return m.group(1).strip() if m else ""


def displays(board: Path, job: Path | None) -> list[dict]:
    """Every drawn display the paper can print: [{name, holder, rows, sources}]. A Section's unit
    `tNN_/display/Display<n>-<slug>/` (name: its README `number:`, else the folder; rows: assets/*.tex, float.tex and
    intake/inputs/*.csv), then each display Task of the Board's display Job (name: its face `label:`; rows: the newest
    Run's result/*.tex and *.csv). `sources` is the text that names what the display was drawn from (its
    intake/manifest.yaml, its Run cards' `reads:`), so a hit can be held to the value's own Runs."""
    out = []
    for unit in sorted(job.glob("t*/display/Display*")) if job else []:
        if not unit.is_dir():
            continue
        readme = unit / "README.md"
        name = _field(readme.read_text(encoding="utf-8"), "number") if readme.is_file() else ""
        rows = []
        for tex in sorted(unit.glob("assets/*.tex")) + ([unit / "float.tex"] if (unit / "float.tex").is_file() else []):
            rows += tex_rows(tex.read_text(encoding="utf-8", errors="ignore"))
        for f in sorted(unit.glob("intake/inputs/*.csv")):
            rows += [" | ".join(str(v) for v in r.values()) for r in rows_of(f)]
        man = unit / "intake" / "manifest.yaml"
        out.append({"name": name or unit.name, "holder": unit.parents[1], "unit": unit, "rows": rows,
                    "sources": man.read_text(encoding="utf-8") if man.is_file() else ""})
    pool = next((j for j in sorted(board.glob("j[0-9]*_*")) if j.is_dir() and re.search(r"display", j.name)), None)
    for task in tasks(pool) if pool else []:
        runs = sorted(r for r in task.glob("runs/r*") if (r / "result").is_dir())
        if not runs:
            continue
        run = runs[-1]
        face = task / f"{task.name}.md"
        name = _field(face.read_text(encoding="utf-8"), "label") if face.is_file() else ""
        rows = []
        for tex in sorted((run / "result").glob("*.tex")):
            if tex.name.startswith("preview"):
                continue
            rows += tex_rows(tex.read_text(encoding="utf-8", errors="ignore"))
        for f in sorted((run / "result").glob("*.csv")):
            rows += [" | ".join(str(v) for v in r.values()) for r in rows_of(f)]
        card = run / "run.yaml"
        out.append({"name": name or task.name, "holder": task, "unit": run, "rows": rows,
                    "sources": card.read_text(encoding="utf-8") if card.is_file() else ""})
    return out


# ── links ───────────────────────────────────────────────────────────────────────────────────────────────────────────
def href(folder: Path, root: Path, extra: str = "") -> str:
    """The workbench page of a folder, relative to the SPACE root (opens the whole tab)."""
    try:
        rel = Path(folder).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        rel = Path(folder).as_posix()
    return f"/_board/workbench?path={quote(rel)}&layout=focus{extra}"


ADDRESS = re.compile(r"\bb(\d+)\.j(\d+)\.t(\d+)\.r(\d+)\b")


def address_of(run_dir: Path) -> str:
    """`b51.j02.t01.r01` from a work Run folder (a Board's evidence Run: `j02.t01.r01`)."""
    parts = {p.split("_")[0][0]: p.split("_")[0] for p in Path(run_dir).parts[-6:] if re.match(r"[bjtr]\d+_", p)}
    return ".".join(parts[k] for k in "bjtr" if k in parts)


def find_run(project: Path, address: str) -> Path | None:
    """bNN.jNN.tNN.rNN → its Run folder in work/ or discovery/ (None when none or two)."""
    m = ADDRESS.search(address)
    if not m:
        return None
    b, j, t, r = m.groups()
    hits = sorted(project.glob(f"work/b{b}_*/j{j}_*/t{t}_*/runs/r{r}_*")) + \
        sorted(project.glob(f"discovery/b{b}_*/j{j}_*/t{t}_*/runs/r{r}_*"))
    return hits[0] if len(hits) == 1 else None


def task_title(folder: Path) -> str:
    """A Task's title, from its face's first line `# tNN_<task> · <title>`, else its folder in words."""
    task = folder.parent.parent if folder.parent.name == "runs" else folder
    face = task / f"{task.name}.md"
    first = face.read_text(encoding="utf-8").splitlines()[0] if face.is_file() else ""
    if " · " in first:
        return first.split(" · ", 1)[1].strip()
    return re.sub(r"^t\d+_", "", task.name).replace("_", " ").replace("-", " ")

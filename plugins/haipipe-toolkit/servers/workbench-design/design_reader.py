"""Read a design Block on b12's ladder from disk (Tools/designs/b12_theme_design s11 · s12 · s13, 261007).

The ladder: a design Block `bNN_<app>/` holds its goal list (board.md ## Goals), its inputs versions
(`inputs/iN/` + manifest.yaml), what an Exp returned (`observed/eNN_<exp>/arms.csv`), its soft Runs
(`runs/run-<type>-<target>/`, every one soft, s11) and its `delivery/`. A Job `jNN_<goal>_<design-method>/` pins
one goal, one registered method version and one inputs version by its face's `goal:` · `method:` · `inputs:`
lines; its `inputs/` is the fence (goal.md · method.md · links into the Block's inputs version · manifest.yaml);
its Tasks are t00 (② reason ideas), one per design (③ ④) and t99 (⑤ review whole). A Block is on this ladder
when one of its Jobs pins a registered method (M01 – M05); any other design Block keeps today's reading.
Read-only: this module only reads.
"""
from __future__ import annotations

import csv
import re
from datetime import datetime
from pathlib import Path

import yaml

# the registered methods and their type, one of the Guide's 13 cards: read from the registry, the skill
# haipipe-design-method's methods/MNN-<slug>/method.md and its versions m<k>.md (decided 261007). This table is used
# only when the registry is missing.
_FALLBACK = {"M01": ("Goal only", "By goal"), "M02": ("Overall performance", "By precedent"),
             "M03": ("Detailed evidence", "By insight"), "M04": ("Actionable insights", "By insight"),
             "M05": ("Raw-data agent", "By insight")}


def _registry_dir() -> Path:
    try:
        from host_paths import skill_dir                  # on the host: wherever the skill sits under skills/
        return skill_dir("haipipe-design-method") / "methods"
    except ImportError:                                   # read directly (a skill's test): the toolkit's own tree
        return Path(__file__).resolve().parents[2] / "skills" / "2_theme" / "design" / "haipipe-design-method" / "methods"


def registry(path: Path | None = None) -> dict:
    """The method registry: {MNN: {name, type, family, current, path, versions: {m<k>: front matter}}}, {} if absent."""
    out = {}
    root = path or _registry_dir()
    for d in sorted(root.glob("M[0-9][0-9]-*")) if root.is_dir() else []:
        card = front(d / "method.md")
        out[d.name[:3]] = {"name": str(card.get("name", "")), "type": str(card.get("type", "")),
                           "family": str(card.get("family", "")), "current": str(card.get("current", "")), "path": d,
                           "versions": {v.stem: front(v) for v in sorted(d.glob("m[0-9]*.md"))}}
    return out
METHOD_PIN = re.compile(r"^(M\d\d)\s*(m\d+)?")
DESIGN_TASK = re.compile(r"^t(\d+)_d(\d+)_(.+)$")
FENCE_PARTS = ("Goal · how much is set", "Goal · for whom", "Information · whose", "Information · form",
               "Examples", "Tools", "Reading", "From the last unit")      # step ① See input's parts (s03)


_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)          # the C parser where installed: ~10× faster
_CACHE: dict = {}                                                   # (path, mtime, size) -> parsed; read-only


def _cached(path: Path, parse):
    """Parse a file once per version on disk (its mtime and size); a changed file is parsed again."""
    try:
        st = path.stat()
    except OSError:
        return None
    key = (str(path), parse.__name__, st.st_mtime_ns, st.st_size)
    if key not in _CACHE:
        if len(_CACHE) > 20000:
            _CACHE.clear()
        try:
            _CACHE[key] = parse(path.read_text(encoding="utf-8", errors="ignore"))
        except (OSError, yaml.YAMLError, ValueError):
            _CACHE[key] = None
    return _CACHE[key]


def _front_of(text: str) -> dict:
    m = re.match(r"(?s)^---\n(.*?)\n---\n", text)
    return (yaml.load(m.group(1), Loader=_LOADER) or {}) if m else {}


def _yaml_of(text: str):
    return yaml.load(text, Loader=_LOADER) or {}


def front(md: Path | None) -> dict:
    """The YAML front matter of a Markdown file ({} without one)."""
    f = _cached(md, _front_of) if md else None
    return f if isinstance(f, dict) else {}


def _yaml(path: Path) -> dict | list:
    y = _cached(path, _yaml_of)
    return y if y is not None else {}


def _csv_of(text: str) -> list:
    return list(csv.DictReader(text.splitlines()))


def _csv(path: Path) -> list:
    rows = _cached(path, _csv_of)
    return rows or []


def _block_yaml(md: Path, heading: str) -> dict:
    """The ```yaml block under a face's `## <heading>`."""
    try:
        text = md.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return {}
    m = re.search(rf"(?ms)^##\s+{heading}\s*\n.*?```yaml\n(.*?)```", text)
    try:
        return (yaml.safe_load(m.group(1)) or {}) if m else {}
    except yaml.YAMLError:
        return {}


def _sections(md: Path | None) -> dict:
    try:
        text = md.read_text(encoding="utf-8", errors="ignore") if md else ""
    except OSError:
        return {}
    return {m.group(1).strip(): m.group(2).strip()
            for m in re.finditer(r"(?ms)^##\s+(.+?)\n(.*?)(?=^##\s|\Z)", text)}


REGISTRY: dict = {}
METHODS: dict = dict(_FALLBACK)


def load_methods() -> dict:
    """Reread the registry into REGISTRY and METHODS ({MNN: (name, type)}); the fallback table if it is missing."""
    REGISTRY.clear()
    REGISTRY.update(registry())
    METHODS.clear()
    METHODS.update({m: (r["name"], r["type"]) for m, r in REGISTRY.items()} or _FALLBACK)
    return METHODS


def face(folder: Path) -> Path | None:
    for name in (folder.name + ".md", "board.md"):
        if (folder / name).is_file():
            return folder / name
    return None


# ── Runs ──────────────────────────────────────────────────────────────────────────────────────
def _minutes(card: dict) -> float | None:
    try:
        a, b = (datetime.fromisoformat(str(card[k])) for k in ("started_at", "finished_at"))
        return (b - a).total_seconds() / 60
    except (KeyError, ValueError, TypeError):
        return None


def runs(folder: Path) -> list:
    """Every Run in the folder's runs/: its name, kind (hard rNN_, soft run-), type, status, target, by, minutes,
    tokens (`usage:`, "—" while the receipt has none) and its result folder."""
    rdir = folder / "runs"
    out = []
    if not rdir.is_dir():
        return out
    for p in sorted(rdir.iterdir()):
        if not p.is_dir() or p.name.startswith((".", "_")):
            continue
        card = _yaml(p / "run.yaml") if (p / "run.yaml").is_file() else {}
        card = card if isinstance(card, dict) else {}
        usage = card.get("usage") or {}
        kind = card.get("kind") if card.get("kind") in ("hard", "soft") else None   # run-<type>-<target> may be hard
        out.append({"run": p.name, "kind": kind or ("soft" if p.name.startswith("run-") else "hard"),
                    "type": str(card.get("type") or (p.name.split("-")[1] if p.name.startswith("run-") else p.name.split("_")[1]
                                                     if "_" in p.name else "run")),
                    "status": str(card.get("status", "—")), "target": str(card.get("target", "")),
                    "by": str(card.get("by", "")), "minutes": _minutes(card),
                    "tokens": (usage.get("in", 0) + usage.get("out", 0)) if isinstance(usage, dict) and usage else None,
                    "card": card, "path": p, "result": p / "result" if (p / "result").is_dir() else p})
    return out


# ── the ladder ────────────────────────────────────────────────────────────────────────────────
def method_pin(value: str) -> tuple:
    """`M04 m2` → ("M04", "m2"); anything else → ("", "")."""
    m = METHOD_PIN.match(str(value or "").strip())
    return (m.group(1), m.group(2) or "") if m else ("", "")


def is_job(folder: Path) -> bool:
    """A Job on the ladder: a jNN_ folder whose face pins a registered method."""
    return folder.name.startswith("j") and folder.is_dir() and bool(method_pin(front(face(folder)).get("method"))[0])


def is_ladder(block: Path) -> bool:
    """A design Block on b12's ladder: its face says `board-kind: design-board` (the scaffold's, even before any Job),
    or one of its Jobs pins a registered method (M01 – M05). An older board says `board-kind: design`."""
    try:
        if re.search(r"(?m)^board-kind:\s*design-board\s*$", (block / "board.md").read_text(encoding="utf-8", errors="ignore")):
            return True
    except OSError:
        pass
    try:
        return any(is_job(p) for p in block.iterdir() if re.match(r"^j\d+_", p.name))
    except OSError:
        return False


def kind_of(task: Path) -> str:
    """t00 (② reason ideas), t99 (⑤ review whole) or design (③ ④)."""
    return "t00" if task.name.startswith("t00_") else "t99" if task.name.startswith("t99_") else "design"


def design(task: Path) -> dict:
    """One design Task: its face, its message, its elements, prediction, drafts and tests."""
    md, m = face(task), DESIGN_TASK.match(task.name)
    f, parts = front(md), _sections(md)
    rs = runs(task)
    drafts = [r for r in rs if r["type"] in ("generate", "revise")]
    verifies = [r for r in rs if r["type"] == "verify"]
    elements = _yaml(task / "elements.yaml")
    return {"path": task, "name": task.name, "id": f"d{m.group(2)}" if m else task.name, "slug": m.group(3) if m else "",
            "number": int(m.group(1)) if m else 0, "state": str(f.get("state", "draft")), "idea": str(f.get("idea", "")),
            "short": str(f.get("name", m.group(3) if m else "")), "message": parts.get("Design", "").strip(),
            "evaluation": parts.get("Evaluation", "").strip(), "elements": elements if isinstance(elements, list) else [],
            "prediction": _yaml(task / "prediction.yaml") or {}, "runs": rs, "drafts": drafts, "verifies": verifies,
            "first_try": bool(verifies) and verifies[0]["status"] == "passed"}


def job(jdir: Path) -> dict:
    """One Job: its pins, its fence, its Runs, t00's ideas, its designs in order, t99's ranking, its delivery."""
    f = front(face(jdir))
    mid, version = method_pin(f.get("method"))
    fence = jdir / "inputs"
    manifest = _yaml(fence / "manifest.yaml") if (fence / "manifest.yaml").is_file() else {}
    method = front(fence / "method.md") if (fence / "method.md").is_file() else {}
    tasks = sorted(p for p in jdir.iterdir() if p.is_dir() and re.match(r"^t\d+_", p.name)) if jdir.is_dir() else []
    t00 = next((t for t in tasks if kind_of(t) == "t00"), None)
    t99 = next((t for t in tasks if kind_of(t) == "t99"), None)
    reason = next((r for r in runs(t00) if r["type"] == "reason"), None) if t00 else None
    rank = next((r for r in runs(t99) if r["type"] == "rank"), None) if t99 else None
    designs = [design(t) for t in tasks if kind_of(t) == "design"]
    files = []
    if fence.is_dir():
        for p in sorted(fence.iterdir()):
            if p.name == "manifest.yaml":
                continue
            target = str(p.readlink()) if p.is_symlink() else ""
            files.append({"name": p.name + ("/" if p.is_dir() else ""), "link": target,
                          "broken": p.is_symlink() and not p.exists()})
    delivered = _yaml(jdir / "delivery" / "designs.json") if (jdir / "delivery" / "designs.json").is_file() else {}
    return {"path": jdir, "name": jdir.name, "id": jdir.name.split("_")[0], "goal": str(f.get("goal", "")),
            "method": mid, "version": version, "method_name": METHODS.get(mid, ("", ""))[0],
            "type": METHODS.get(mid, ("", "—"))[1], "sha": str(f.get("method-sha", "")), "inputs": str(f.get("inputs", "")),
            "state": str(f.get("state", "—")), "moved": str(f.get("moved", "")), "n": f.get("n", ""),
            "face": f, "fence": fence, "manifest": manifest if isinstance(manifest, dict) else {},
            "method_card": method if isinstance(method, dict) else {}, "files": files, "runs": runs(jdir),
            "t00": t00, "t99": t99, "reason": reason, "rank": rank,
            "topics": (_yaml(reason["path"] / "result" / "chains.yaml") or {}).get("topics", []) if reason else [],
            "ideas": (_yaml(reason["path"] / "result" / "ideas.yaml") or {}).get("ideas", []) if reason else [],
            "ranking": _csv(rank["path"] / "result" / "ranking.csv") if rank else [],
            "designs": designs, "delivered": (delivered or {}).get("designs", []) if isinstance(delivered, dict) else [],
            "delivery": jdir / "delivery"}


def board(block: Path, with_jobs: bool = True) -> dict:
    """The Block: its goals, questions, inputs versions, observed Exps and scores, Runs, Jobs and delivery.
    with_jobs=False skips reading every Job (a Job or Task view needs only the Block's goals and Exp results)."""
    md = block / "board.md"
    goals = _block_yaml(md, "Goals").get("goals", []) if md.is_file() else []
    questions = _block_yaml(md, "Questions").get("questions", []) if md.is_file() else []
    inputs = []
    for d in sorted((block / "inputs").glob("i*")) if (block / "inputs").is_dir() else []:
        man = _yaml(d / "manifest.yaml") if (d / "manifest.yaml").is_file() else {}
        inputs.append({"id": d.name, "path": d, "manifest": man if isinstance(man, dict) else {}})
    observed = []
    for e in sorted((block / "observed").glob("e*")) if (block / "observed").is_dir() else []:
        observed.append({"id": e.name.split("_")[0], "name": e.name, "path": e, "arms": _csv(e / "arms.csv"),
                         "source": e / "source.md"})
    rs = runs(block)
    scores = {}
    for r in rs:
        if r["type"] == "score":
            for row in _csv(r["path"] / "scores.csv") + _csv(r["result"] / "scores.csv"):
                scores[(row.get("job", ""), row.get("design", ""))] = {**row, "run": r["run"]}
    jobs = [job(p) for p in sorted(block.iterdir()) if re.match(r"^j\d+_", p.name) and is_job(p)] if with_jobs else []
    delivered = _yaml(block / "delivery" / "designs.json") if (block / "delivery" / "designs.json").is_file() else {}
    return {"path": block, "face": md, "goals": goals if isinstance(goals, list) else [],
            "questions": questions if isinstance(questions, list) else [], "inputs": inputs, "observed": observed,
            "scores": scores, "runs": rs, "jobs": jobs,
            "delivered": (delivered or {}).get("designs", []) if isinstance(delivered, dict) else []}


def block_of(folder: Path) -> Path | None:
    """The Block a Job or Task sits in (the folder itself for a Block)."""
    for p in (folder, *folder.parents):
        if re.match(r"^b\d+_", p.name) or (p / "board.md").is_file():
            return p
    return None


def arm_of(b: dict, jid: str, did: str) -> dict:
    """The Exp arm that tested this design (per-arm totals only), or {}."""
    for e in b["observed"]:
        for a in e["arms"]:
            if a.get("job") == jid and a.get("design") == did:
                return {**a, "exp": e["id"]}
    return {}


load_methods()

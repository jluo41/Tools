"""Run folders by Space (0.118): a Page keeps each run beside the Space it changes.

    runs/draft-manual-run/   Structure revise · Scratch · Section and Paragraph revise
    runs/draft-auto-run/     Auto write · Evidence embed · scripted drafting
    runs/evidence-run/       Citation · Value · Display · Discovery (every re-*)
    runs/supporting-run/     generated index of the Block > Job > Task runs elsewhere
    runs/delivery-run/       Web · LaTeX · Word · Slides builds

A Page with none of these folders keeps the flat `runs/`. `results/` stays
flat either way: the Run Space pairs `runs/<folder>/<run>` with `results/<run>/`.

Since JL 260928 a run named in the readable grammar (`run-section-cleanup`,
`src/run_names.py`) takes its Space from its kind, not from a folder.

ONE FOLDER PER RUN (0.122, JL 261009; haipipe-run 0.31.0). A readable-grammar run is
`runs/<name>/`: its ticket `<name>.md` (a Delivery Run's is the command `<name>.sh`), its
card `run.yaml`, and `passes/pNN-<MMDD>/`, one per close, holding what that close wrote
(runtime.yaml, the ledger). The older flat pair `runs/<name>.md` + `results/<name>/`
still reads everywhere through `find_ticket` and `result_dir`; `page.py run-names` moves
a Page's runs into their folders once.
"""
from __future__ import annotations

from pathlib import Path
import re

from . import run_names

FOLDERS = ("draft-manual-run", "draft-auto-run", "evidence-run", "supporting-run", "delivery-run")
SPACE = {"draft-manual-run": "draft", "draft-auto-run": "draft", "evidence-run": "evidence",
         "supporting-run": "evidence", "delivery-run": "delivery"}
_KINDS = (
    (re.compile(r"^rp-(?:struct|sec|para|scratch|revise)-\d", re.I), "draft-manual-run"),
    (re.compile(r"^rp-(?:auto|embed)-\d", re.I), "draft-auto-run"),
    (re.compile(r"^(?:re-[a-z]+-\d|p[._]?j\d+[._]?t\d+[._]?r\d+)", re.I), "evidence-run"),
    # Page Delivery Runs (`rd01_web`, `rd00_content`). A Design Run ticket
    # (`rd01_commission_item01.yaml`, haipipe-design-unit) shares the prefix but stays in flat
    # `runs/`, where the Design workbench and check_unit.py read it.
    (re.compile(r"^rd\d+(?!\d|_(?:commission|generate|verify|adopt|revise|reject)(?:_|$))", re.I), "delivery-run"),
)


def uses_space_folders(page_folder) -> bool:
    runs = Path(page_folder) / "runs"
    return any((runs / name).is_dir() for name in FOLDERS)


_FOLDER_OF_SPACE = {"draft": "draft-manual-run", "evidence": "evidence-run", "delivery": "delivery-run"}


def folder_for(run_id: str) -> str | None:
    """The Space folder a run id belongs in, or None for other families."""
    if run_names.is_run_name(run_id):
        kind = run_names.kind_of(run_id)
        if kind in {"auto-write", "evidence-embed"}:
            return "draft-auto-run"
        return _FOLDER_OF_SPACE.get(run_names.space_of_kind(kind))
    return next((folder for pattern, folder in _KINDS if pattern.match(run_id or "")), None)


def ticket_dir(page_folder, run_id: str) -> Path:
    """Where a new run's ticket goes: a readable-grammar run's own folder `runs/<name>/`;
    an older id's Space folder, or flat `runs/` on older Pages."""
    runs = Path(page_folder) / "runs"
    if run_names.is_run_name(run_id):
        return runs / run_id             # one folder per Run (0.122)
    folder = folder_for(run_id) if uses_space_folders(page_folder) else None
    return runs / folder if folder else runs


TICKET_SUFFIXES = (".md", ".sh", ".yaml", ".yml", ".ps1")
_PASS = re.compile(r"^p(\d+)-(\d{4})$")


def run_dir(page_folder, run_id: str) -> Path:
    """The run's own folder, `runs/<name>/` (it may not exist yet)."""
    return Path(page_folder) / "runs" / run_id


def is_folder_run(page_folder, run_id: str) -> bool:
    """The run sits in its own folder (0.122) rather than the older flat pair."""
    folder = run_dir(page_folder, run_id)
    return folder.is_dir() and ((folder / "run.yaml").is_file()
                                or any((folder / (run_id + s)).is_file() for s in TICKET_SUFFIXES))


def find_ticket(page_folder, run_id: str) -> Path | None:
    """The run's ticket wherever it sits: its own folder, flat `runs/`, or an older Space folder."""
    runs = Path(page_folder) / "runs"
    places = [runs / run_id, runs] + [runs / f for f in FOLDERS] + [runs / "check-run"]
    for place in places:
        for suffix in TICKET_SUFFIXES:
            if (place / (run_id + suffix)).is_file():
                return place / (run_id + suffix)
    return None


def passes(page_folder, run_id: str) -> list[Path]:
    """The run's passes, oldest first: `runs/<name>/passes/pNN-<MMDD>/`."""
    folder = run_dir(page_folder, run_id) / "passes"
    found = [p for p in folder.iterdir() if p.is_dir() and _PASS.match(p.name)] if folder.is_dir() else []
    return sorted(found, key=lambda p: int(_PASS.match(p.name).group(1)))


def result_dir(page_folder, run_id: str) -> Path:
    """Where the run's outputs are: its latest pass in its own folder, else the older
    `results/<name>/`. The path may not exist (an open run has written nothing yet)."""
    found = passes(page_folder, run_id)
    if found:
        return found[-1]
    return Path(page_folder) / "results" / run_id


def result_rel(page_folder, run_id: str) -> str:
    """`result_dir` as a Page-relative string, e.g. `runs/run-value-size/passes/p01-1005`."""
    return result_dir(page_folder, run_id).relative_to(Path(page_folder)).as_posix()


def new_pass(page_folder, run_id: str, day: str = "") -> Path:
    """Make the run's next pass folder `passes/pNN-<MMDD>/` and return it."""
    import datetime as _dt
    day = day or _dt.date.today().strftime("%m%d")
    found = passes(page_folder, run_id)
    number = int(_PASS.match(found[-1].name).group(1)) + 1 if found else 1
    folder = run_dir(page_folder, run_id) / "passes" / ("p%02d-%s" % (number, day))
    folder.mkdir(parents=True, exist_ok=False)
    return folder


_CLOSED = re.compile(r"(?m)^status:\s*['\"]?(complete|completed|closed|done|ok|failed)\b")


def working_dir(page_folder, run_id: str, day: str = "") -> Path:
    """The folder a run writes into now, made if missing: its open pass (the latest one, while
    its receipt does not say it closed), else a new pass; an older flat run's `results/<name>/`."""
    if not is_folder_run(page_folder, run_id):
        folder = Path(page_folder) / "results" / run_id
        folder.mkdir(parents=True, exist_ok=True)
        return folder
    found = passes(page_folder, run_id)
    if found:
        receipt = found[-1] / "runtime.yaml"
        text = receipt.read_text(encoding="utf-8", errors="replace") if receipt.is_file() else ""
        if not _CLOSED.search(text):
            return found[-1]
    return new_pass(page_folder, run_id, day)

def result_dirs(page_folder) -> dict[str, Path]:
    """Every run on the Page that has written something: {name: its result folder}, both layouts."""
    page_folder = Path(page_folder)
    out = {}
    results = page_folder / "results"
    for path in sorted(results.iterdir()) if results.is_dir() else []:
        if path.is_dir():
            out[path.name] = path
    runs = page_folder / "runs"
    for path in sorted(runs.iterdir()) if runs.is_dir() else []:
        if path.is_dir() and path.name not in FOLDERS and path.name != "check-run":
            latest = passes(page_folder, path.name)
            if latest:
                out[path.name] = latest[-1]
    return out


CARD_FIELDS = ("run", "kind", "type", "scope", "target", "ticket", "skill", "agent", "signs", "status",
               "passes", "writes", "feeds")


def write_card(page_folder, run_id: str, **fields) -> Path:
    """Write or update `runs/<name>/run.yaml` (haipipe-run's soft Run card): the run's kind is
    soft, its passes are what is on disk, and the given fields overwrite the old ones."""
    import yaml
    folder = run_dir(page_folder, run_id)
    card_path = folder / "run.yaml"
    card = (yaml.safe_load(card_path.read_text(encoding="utf-8")) or {}) if card_path.is_file() else {}
    ticket = find_ticket(page_folder, run_id)
    space = next((p for p in [Path(page_folder).resolve(), *Path(page_folder).resolve().parents]
                  if (p / "env.sh").is_file() or (p / "pyproject.toml").is_file()), None)
    card.setdefault("run", run_id)
    card["kind"] = "soft"
    card.setdefault("type", run_names.kind_of(run_id))
    card.setdefault("scope", Path(page_folder).resolve().relative_to(space).as_posix() if space else None)
    card["ticket"] = ticket.name if ticket is not None and ticket.parent == folder else card.get("ticket")
    card["passes"] = [p.name for p in passes(page_folder, run_id)]
    card.update({k: v for k, v in fields.items() if v is not None})
    ordered = {k: card.get(k) for k in CARD_FIELDS}
    ordered.update({k: v for k, v in card.items() if k not in ordered})
    folder.mkdir(parents=True, exist_ok=True)
    card_path.write_text(yaml.safe_dump(ordered, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return card_path


def ticket_rel(page_folder, run_id: str, suffix: str = ".md") -> str:
    """The ticket path as a Page-relative string, e.g. `runs/draft-manual-run/rp-para-15_P02.md`."""
    return (ticket_dir(page_folder, run_id) / (run_id + suffix)).relative_to(Path(page_folder)).as_posix()


def space_of(ticket) -> str:
    """draft · evidence · delivery · other, from the ticket's folder, else its id."""
    path = Path(str(ticket))
    for part in path.parts:
        if part in SPACE:
            return SPACE[part]
    kind = run_names.kind_of(path.stem)
    if run_names.is_run_name(path.stem) and kind:
        space = run_names.space_of_kind(kind)
        return space if space in {"draft", "evidence", "delivery"} else "other"
    folder = folder_for(path.stem)
    return SPACE.get(folder, "other") if folder else "other"


def is_result_folder(folder) -> bool:
    """A run's result folder in either layout: `results/<name>/` or `runs/<name>/passes/pNN-<MMDD>/`."""
    folder = Path(folder)
    return folder.parent.name == "results" or (
        folder.parent.name == "passes" and bool(_PASS.match(folder.name))
        and folder.parent.parent.parent.name == "runs")


def under_page_results(page_folder, path) -> bool:
    """`path` is inside one of the Page's own run results, in either layout."""
    page_folder = Path(page_folder).resolve()
    path = Path(path).resolve()
    try:
        rel = path.relative_to(page_folder).parts
    except ValueError:
        return False
    if rel[:1] == ("results",) and len(rel) > 1:
        return True
    return (len(rel) > 4 and rel[0] == "runs" and rel[2] == "passes" and bool(_PASS.match(rel[3])))


def result_roots(page_folder) -> list[Path]:
    """Every folder that holds a run's outputs on this Page: `results/<name>/` and every pass."""
    page_folder = Path(page_folder)
    out = []
    results = page_folder / "results"
    out += [p for p in sorted(results.iterdir()) if p.is_dir()] if results.is_dir() else []
    runs = page_folder / "runs"
    for run in sorted(runs.iterdir()) if runs.is_dir() else []:
        if run.is_dir():
            out += passes(page_folder, run.name)
    return out

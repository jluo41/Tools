"""check-page-folder: is a Page Folder on the latest layout this skill describes?

`folder_health` asks whether a Folder agrees with itself. This module asks a
different question: does the Folder follow the layout the Page skill ships
today, and if not, which command brings it there. Each rule names the skill
version that introduced it and its fix, so a Page reports how far behind it is.

When the Page layout changes, add its rule here in the same commit; this list
is what "latest" means.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import functools
from pathlib import Path
import re

from .outline_version import PREVIOUS, RECORD_KINDS, RECORDS, latest_outline, plan_dir, plan_files
from .plan_layout import is_sectioned, overview_lines
from .plan_shape import iter_plan_bullets
from . import run_names
from .run_folders import FOLDERS, folder_for

LAYOUT_VERSION = "0.125"
# Evidence lanes that stay live in `draft/evidence/`: the Page export writes `bibex/`, and
# `materials/` holds the Page's imports (workbench ref/roster.md). Every other
# lane is retired Outline evidence, `display/` once its units are DISPLAY Results.
LIVE_LANES = frozenset({"bibex", "materials"})
PASS, BEHIND, NA = "PASS", "BEHIND", "N/A"
ICON = {PASS: "✅", BEHIND: "⚠️", NA: "·"}
VERSIONED = re.compile(r"-(?:outline|draft)-v\d")
OUTLINE_PATH = re.compile(r"(?<![\w.-])outline/")
TEXT = {".md", ".yaml", ".yml", ".json", ".sh", ".py", ".txt", ".tex", ".html"}
FIX_LAYOUT = "page.py draft-layout {page}"
FIX_RUNS = "page.py run-names {page}"


@dataclass
class Rule:
    rule: str
    since: str
    state: str
    detail: str
    fix: str = ""


def _page(target: Path) -> tuple[Path, str]:
    folder = Path(target).expanduser().resolve()
    if folder.is_file():
        folder = folder.parent
    if not (folder / f"{folder.name}.md").is_file():
        raise ValueError(f"{folder} has no Page Face {folder.name}.md")
    return folder, folder.name


def _served_links(folder: Path) -> list[str]:
    """Links the standalone Page server refuses: its own walk, which skips hidden and private folders."""
    import os
    from .page_workspace import PRIVATE_FILES, PRIVATE_LANES
    found = []
    for parent, dirs, files in os.walk(folder, followlinks=False):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in PRIVATE_LANES | PRIVATE_FILES]
        found += [(Path(parent) / n).relative_to(folder).as_posix() for n in dirs + files
                  if (Path(parent) / n).is_symlink()]
    return sorted(found)


def unconverted_display_units(folder: Path) -> list[str]:
    """Legacy `draft/evidence/display/<unit>/` units that no DISPLAY Result carries yet.

    Builders still read these (the paper delivery falls back to the lane), so the
    lane stays until each unit is a DISPLAY Result at `results/<re-run>/payload/<unit>/`.
    """
    lane = plan_dir(folder) / "evidence" / "display"
    if not lane.is_dir():
        return []
    carried = {p.name for p in folder.glob("results/*/payload/*") if p.is_dir()}
    return sorted(u.name for u in lane.iterdir() if u.is_dir() and u.name not in carried)


CODE = {".py", ".sh", ".ps1", ".R", ".r", ".do", ".js", ".mjs", ".ts", ".tex", ".mk", ".toml", ".ipynb"}
_EVIDENCE_FILE = re.compile(r"""(?:\}|%s|\+\s*["'])-evidence\.md\b""")  # f"{stem}-evidence.md" and kin
_SKIP_DIRS = {"node_modules", "_WorkSpace", "results", "_archive", "venv", "__pycache__", "Tools", "code",
              "board", "_assets"}  # generated Board views are not readers
_IN_PAGE_PATH = re.compile(r"(?<![\w.-])(?:(?:draft|outline)/(?:evidence/[\w-]+|[\w.-]+-evidence\.md)|pagex/[\w.-]+)")
_LANE_READ = re.compile(r"""evidence['"]?\s*[/,]\s*['"]?([A-Za-z][\w-]*)""")


def _project_root(folder: Path) -> Path:
    """The Project holding the Page: its `examples*/<Project>` folder (a paper submodule inside
    it included), else the nearest git repo."""
    project = next((q for q in [folder, *folder.parents] if q.parent.name.startswith("examples")), None)
    if project is not None:
        return project
    return next((p for p in [folder, *folder.parents] if (p / ".git").exists()), folder)


@functools.lru_cache(maxsize=None)
def _code_mentioning_evidence(root: str) -> tuple:
    """(path, text) of each code file under `root` that says `evidence` (one walk per Project)."""
    import os
    out = []
    for parent, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in _SKIP_DIRS and not d.startswith(".")]
        for name in names:
            if Path(name).suffix in CODE:
                try:
                    text = (Path(parent) / name).read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                if "evidence" in text:
                    out.append((str(Path(parent) / name), text))
    return tuple(out)


def retired_readers(folder: Path, items: list[str]) -> dict[str, str]:
    """{retired item: a script that still reads it}; such an item stays live until the script moves.

    `items` are lane names (`cite`) and file names (`<stem>-evidence.md`). A lane is read when
    code names `evidence/<lane>` (or `"evidence" / "<lane>"`); the Evidence file is read when
    code names `-evidence.md`. Sealed `results/` and `_archive/` are not searched, and a
    literal `draft/evidence/<lane>` path inside the Page is not a reader: the move rewrites it.
    """
    found = {}
    for path, text in _code_mentioning_evidence(str(_project_root(folder))):
        if Path(path).is_relative_to(folder):  # the archive rewrites literal paths inside the Page
            text = _IN_PAGE_PATH.sub("", text)
        lanes = {m.group(1) for m in _LANE_READ.finditer(text)}
        for item in items:
            if item in found:
                continue
            if (item.endswith("-evidence.md") and (item in text or _EVIDENCE_FILE.search(text))) or item in lanes \
                    or (item.endswith("/") and re.search(r"(?<![\w-])%s" % re.escape(item), text)):
                found[item] = str(Path(path).relative_to(_project_root(folder)))
    return found


def _rule(out, name, since, ok, detail, fix=""):
    state = NA if ok is None else PASS if ok else BEHIND
    out.append(Rule(name, since, state, detail, "" if state != BEHIND else fix))


def check_page_folder(target: Path) -> dict:
    folder, stem = _page(target)
    home = plan_dir(folder)
    plan = latest_outline(home, stem) if home.is_dir() else None
    text = plan.read_text(encoding="utf-8", errors="replace") if plan else ""
    rules: list[Rule] = []

    has_draft, has_outline = (folder / "draft").is_dir(), (folder / "outline").exists()
    _rule(rules, "plan folder is draft/", "0.118",
          None if not has_draft and not has_outline else has_draft and not has_outline,
          "draft/" if has_draft and not has_outline else "outline/ (older name)" if has_outline
          else "none yet; draft/ appears with the first plan or record", FIX_LAYOUT)
    _rule(rules, "one current plan", "0.117",
          None if plan is None else
          len([p for p in plan_files(home, stem) if VERSIONED.search(p.name)]) == 1,
          plan.name if plan else "no plan yet", f"page.py outline-tidy {{page}}")
    # A plan with no `- B<k> ·` Bullets cannot be laid out by the migration.
    bulletless = plan is not None and not is_sectioned(text) and not iter_plan_bullets(text)
    fix_plan = ("OUTLINE: write the plan as Bullets (- B<k> · ...), then " + FIX_LAYOUT) if bulletless \
        else FIX_LAYOUT
    _rule(rules, "plan named <stem>-draft-v<G>.<S>.md", "0.118",
          None if plan is None else "-draft-v" in plan.name,
          plan.name if plan else "no plan yet", fix_plan)
    _rule(rules, "plan in three sections", "0.118",
          None if plan is None else is_sectioned(text),
          "## 1 Structure · ## 2 Scratch · ## 3 Draft" if plan and is_sectioned(text)
          else "no Bullets to lay out" if bulletless
          else "one Draft-first plan" if plan else "no plan yet", fix_plan)
    _rule(rules, "Structure Overview", "0.118",
          None if plan is None or not is_sectioned(text) else bool(overview_lines(text)),
          "%d entries" % len(overview_lines(text)) if plan and is_sectioned(text) else "", FIX_LAYOUT)

    loose = sorted(p.name for kind in RECORD_KINDS for p in home.glob(f"*-{kind}.md")
                   if not VERSIONED.search(p.name)) if home.is_dir() else []
    _rule(rules, f"records in {RECORDS}/", "0.117", None if not home.is_dir() else not loose,
          ", ".join(loose) or f"{home.name}/{RECORDS}/", "page.py outline-tidy {page}")

    items = home / f"{stem}-evidence-items.md"
    grouped = None
    if items.is_file():
        body = items.read_text(encoding="utf-8", errors="replace")
        has_items = bool(re.search(r"(?m)^#{3,4} E\d+-", body))
        grouped = None if not has_items else bool(re.search(r"(?m)^## (Citations|Displays|Values)\s*$", body))
    evidence_detail, evidence_fix = "flat list of items", FIX_LAYOUT
    if grouped is False:
        from .draft_migration import group_evidence
        try:
            group_evidence(body)
        except ValueError as err:  # a kind the three groups cannot hold
            evidence_detail = str(err)
            evidence_fix = "EVIDENCE: retype the item as CITE, DISPLAY or VALUE, then " + FIX_LAYOUT
    _rule(rules, "Evidence Markdown grouped by kind", "0.118", grouped,
          "## Citations · ## Displays · ## Values" if grouped else
          evidence_detail if grouped is False else "no evidence items", evidence_fix)

    runs = folder / "runs"
    # A readable run (`run-<kind>-<slug>`, 0.121) sits flat in runs/; an older Page run
    # (rp-, re-, rd) sits in its Space folder until `page.py run-names` renames it; Task Runs
    # (rNN_) stay flat.
    tickets = [p for p in runs.rglob("*") if p.is_file() and not p.name.startswith(".")
               and (p.parent == runs or p.parent.name in FOLDERS)] if runs.is_dir() else []
    page_runs = [p for p in tickets if folder_for(p.stem)]
    loose = sorted(p.name for p in page_runs if p.parent == runs and not run_names.is_run_name(p.stem))
    nested = sorted(p.name for p in page_runs if p.parent != runs and run_names.is_run_name(p.stem))
    _rule(rules, "runs/ in place", "0.121", None if not page_runs else not loose and not nested,
          "; ".join(filter(None, ["%d older Page run(s) loose in runs/" % len(loose) if loose else "",
                                  "%d readable run(s) inside a Space folder" % len(nested) if nested else ""]))
          or "%d Page run(s) in place" % len(page_runs), FIX_RUNS)
    # ONE FOLDER PER RUN (0.125, JL 261009; haipipe-run 0.31.0): a readable run is runs/<name>/
    # with its ticket, card run.yaml and passes/pNN-<MMDD>/, never the flat runs/<name>.md.
    flat = sorted(p.name for p in runs.iterdir() if p.is_file() and run_names.is_run_name(p.stem)) \
        if runs.is_dir() else []
    own = sorted(p.name for p in runs.iterdir() if p.is_dir() and run_names.is_run_name(p.name)) \
        if runs.is_dir() else []
    _rule(rules, "one folder per run", "0.125", None if not (flat or own) else not flat,
          ("%d readable run(s) flat in runs/: %s" % (len(flat), ", ".join(flat[:3]))) if flat
          else "%d run folder(s): runs/<name>/<name>.md · run.yaml · passes/" % len(own), FIX_RUNS)
    results = folder / "results"
    nested = sorted(d.name for d in results.iterdir() if d.is_dir() and d.name in FOLDERS) \
        if results.is_dir() else []
    _rule(rules, "results/ flat by run name", "0.118", None if not results.is_dir() else not nested,
          ", ".join(nested) or "results/<run>/", "move results/<space>/<run>/ to results/<run>/")

    links = _served_links(folder)
    _rule(rules, "no links the Page server refuses", "0.118", not links,
          ", ".join(links[:4]) or "none", "replace each link with the real folder or remove it")

    from .draft_migration import _PY_JOIN, is_prose_outline, kept_by_result
    cited = []
    for path in folder.rglob("*"):
        if path.is_file() and path.suffix in TEXT and not path.is_symlink() and "results" not in path.parts:
            try:
                body_text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            kept = kept_by_result(path)
            hits = sum(1 for m in OUTLINE_PATH.finditer(body_text)
                       if not ("outline/" + re.match(r"[\w./-]*", body_text[m.end():]).group(0)).rstrip("./-") in kept
                       and not body_text[m.end():].startswith("board-context")  # kept by the sweep
                       and not body_text[max(0, m.start() - 8):m.start()].endswith("_board/")  # old URL
                       and (not (m.start() == 0 or body_text[m.start() - 1] in " \t\n(\"'`")
                            or not is_prose_outline(re.match(r"[\w./-]*", body_text[m.end():]).group(0), folder)))
            if path.suffix == ".py":
                hits += len(_PY_JOIN.findall(body_text))
            if hits:
                cited.append((path.relative_to(folder).as_posix(), hits))
    _rule(rules, "no outline/ paths in the Page's files", "0.118",
          None if not (folder / "draft").is_dir() else not cited,
          ("%d files, e.g. %s" % (len(cited), cited[0][0])) if cited else "none",
          "rewrite outline/ to draft/ in those files")

    unconverted = unconverted_display_units(folder)
    retired = sorted(p.name for p in (home / "evidence").iterdir()
                     if p.name not in LIVE_LANES and not (p.name == "display" and unconverted)) \
        if (home / "evidence").is_dir() else []
    retired += sorted(p.name for p in home.glob("*-evidence.md")) if home.is_dir() else []
    retired += ["pagex/"] if (folder / "pagex").is_dir() else []  # the pre-0.117 binding lane
    read = retired_readers(folder, retired) if retired else {}
    retired = [r for r in retired if r not in read]
    _rule(rules, "retired Outline evidence archived", "0.117",
          None if not home.is_dir() and not retired else not retired,
          ", ".join(retired) or "none", "page.py draft-layout {page} --archive-evidence "
          "(then rebuild the Page's delivery)")
    _rule(rules, "no script reads retired evidence", "0.118", None if not read else False,
          "; ".join("%s read by %s" % kv for kv in sorted(read.items())),
          "EVIDENCE: point each script at the Evidence Markdown or a Result, "
          "then page.py draft-layout {page} --archive-evidence")
    _rule(rules, "display units are DISPLAY Results", "0.117",
          None if not (home / "evidence" / "display").is_dir() else not unconverted,
          ("%d legacy unit(s): %s" % (len(unconverted), ", ".join(unconverted[:3]))) if unconverted
          else "results/<re-run>/payload/<unit>/",
          "EVIDENCE: make each unit a DISPLAY Result at results/<re-run>/payload/<unit>/, "
          "then page.py draft-layout {page} --archive-evidence")
    import os
    where = os.path.relpath(folder)
    for r in rules:
        r.fix = r.fix.format(page=where if not where.startswith("../../..") else str(folder))
    behind = [r for r in rules if r.state == BEHIND]
    return {"page": stem, "folder": str(folder), "layout": LAYOUT_VERSION,
            "verdict": "latest" if not behind else "behind",
            "behind": len(behind), "rules": [asdict(r) for r in rules]}


def pages_in(target: Path) -> list[Path]:
    """A Page Folder, or every Page Folder under a Board or group folder."""
    target = Path(target).expanduser().resolve()
    if target.is_file():
        target = target.parent
    if (target / f"{target.name}.md").is_file():
        return [target]
    return sorted(p.parent for p in target.rglob("*.md")
                  if p.stem == p.parent.name and "_archive" not in p.parts
                  and PREVIOUS not in p.parts and ".git" not in p.parts
                  and "pagex" not in p.relative_to(target).parts[:-1]  # links to other Pages
                  and "results" not in p.relative_to(target).parts[:-1]  # a Result card is not a Page
                  and "runs" not in p.relative_to(target).parts[:-1]     # nor a run's ticket in its folder
                  and not {"outline", "draft"} & set(p.relative_to(target).parts[:-1]))


def render(report: dict) -> str:
    head = "%s %s · %s" % ("✅" if report["verdict"] == "latest" else "⚠️", report["page"],
                           "on the latest layout (%s)" % report["layout"] if report["verdict"] == "latest"
                           else "%d rule(s) behind layout %s" % (report["behind"], report["layout"]))
    lines = [head]
    for r in report["rules"]:
        lines.append("   %s %-38s %s%s" % (ICON[r["state"]], r["rule"], r["detail"],
                                          ("  → " + r["fix"]) if r["fix"] else ""))
    return "\n".join(lines)

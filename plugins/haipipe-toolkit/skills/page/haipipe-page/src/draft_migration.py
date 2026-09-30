"""Move a Page to the 0.118 layout: `draft/`, a three-section Draft Markdown, runs by Space.

    page.py draft-layout <page> [--sort-runs] [--dry-run]

1. `outline/` becomes `draft/` (nothing else moves inside it).
2. The current plan is written again as `<stem>-draft-v<G>.<S+1>.md` in three
   sections with the same Bullets; the old version goes to `previous/`.
   The Evidence Markdown is grouped into `## Citations`, `## Displays` and
   `## Values` (each item block moves unchanged under its kind).
3. With `--sort-runs`, each ticket in a flat `runs/` moves to its Space folder
   (`src/run_folders.py`), a moved shell script finds the Page two folders up,
   and `runs/<name>` citations inside the Page follow the move. `results/` stays.

Every step refuses rather than guesses: a plan that would parse to different
Bullets is not written, and an existing `draft/` beside `outline/` stops the run.
"""
from __future__ import annotations

import os
from pathlib import Path
import re

from .outline_version import (PREVIOUS, RECORD_KINDS, latest_outline, plan_dir, plan_files,
                              retire_records, version_tag)
from .plan_layout import BULLET, DIVISION_HEAD, is_sectioned, legacy_scratch, to_sectioned
from .plan_shape import iter_plan_bullets
from .run_folders import folder_for

TEXT = {".md", ".yaml", ".yml", ".json", ".sh", ".txt", ".py", ".tex", ".mmd", ".html"}


def _bullets(text: str):
    return [(b["address"], b["draft"], b["head"], tuple(b["continuation"]), b.get("reviews"))
            for b in iter_plan_bullets(text)]


def _next_shape(tag: str) -> str:
    m = re.fullmatch(r"v(\d+)(?:\.(\d+))?(?:\.\d+)?", tag or "")
    if not m:
        return "v0.1"
    if m.group(2) is None:  # a legacy integer vN counts as v0.N (outline_version.legacy_integer_issue)
        return "v0.%d" % (int(m.group(1)) + 1)
    return "v%s.%d" % (m.group(1), int(m.group(2)) + 1)


_SUPERSEDES = re.compile(r"(?m)^supersedes:.*(?:\n[ \t]+\S.*)*")
_REWRITTEN = re.compile(r"^(# .+ · outline v|outline-version:|supersedes:)")


def _lost_lines(old: str, new: str) -> list[str]:
    """Lines of `old` outside Bullet blocks that `new` no longer holds, repeats counted.

    Bullets are compared apart. A division heading may lose its `## ` form but not its
    title (the Structure Overview carries it); an `approved:` line may only gain words.
    """
    from collections import Counter
    new_lines = [line.strip() for line in new.split("\n")]
    kept = Counter(new_lines)
    lines, lost, i = old.split("\n"), [], 0
    while i < len(lines):
        if BULLET.match(lines[i]):
            i += 1
            while i < len(lines) and lines[i].startswith("  "):
                i += 1
            continue
        line, i = lines[i].strip(), i + 1
        if not line or _REWRITTEN.match(line):
            continue
        head = DIVISION_HEAD.match(line)
        if head:
            if head.group(2) and head.group(2).strip() not in new:
                lost.append(line)
            continue
        if line.startswith("approved:"):
            if not any(x.startswith(line) for x in new_lines):
                lost.append(line)
            continue
        if kept[line] > 0:
            kept[line] -= 1
        else:
            lost.append(line)
    return lost


def _three_sections(current: Path, stem: str, text: str) -> tuple[str, str]:
    """-> (new file name, body) for a Draft-first plan, or ValueError when a word would change."""
    old_tag = version_tag(current)
    new_tag = _next_shape(old_tag)
    body = to_sectioned(text)
    body = re.sub(r"(?m)^# (.+?) · outline v[\d.]+", rf"# \1 · draft {new_tag}", body, count=1)
    body = re.sub(r"(?m)^outline-version:.*$", f"draft-version: {new_tag}", body, count=1)
    field = _SUPERSEDES.search(text)  # the field and its indented continuation lines
    if field:
        body = _SUPERSEDES.sub(f"supersedes: {old_tag}", body, count=1)
    body = re.sub(r"(?m)^(approved:\s*✅.*?)\s*$",
                  rf"\1 · carried from {old_tag}: same Bullets, three-section layout", body, count=1)
    if _bullets(body) != _bullets(text):
        raise ValueError(f"{current.name}: the three-section layout would change a Bullet; nothing written")
    rewritten = legacy_scratch(text.split("\n"))[2]  # the old Scratch registry's field lines
    rewritten |= {x.strip() for x in field.group(0).split("\n")[1:]} if field else set()
    lost = [line for line in _lost_lines(text, body) if line not in rewritten]
    if lost:
        raise ValueError(f"{current.name}: the three-section layout would drop {len(lost)} line(s), "
                         f"first {lost[0][:80]!r}; nothing written")
    return f"{stem}-draft-{new_tag}.md", body


def draft_layout(page_folder: Path, *, sort_runs: bool = False, dry_run: bool = False,
                 archive_evidence: bool = False) -> dict:
    folder = Path(page_folder).expanduser().resolve()
    if folder.is_file():
        folder = folder.parent
    stem = folder.name
    report = {"page": stem, "dry_run": dry_run, "renamed": None, "plan": None, "runs_moved": 0,
              "scripts_fixed": 0, "citations": 0}
    outline, draft = folder / "outline", folder / "draft"
    rename = outline.is_dir() and not outline.is_symlink()
    if rename and draft.exists():
        raise ValueError("both outline/ and draft/ exist; merge them by hand first")
    # Every check runs before anything moves, so a refused Page is left exactly as it was.
    source = outline if rename else draft
    current = latest_outline(source, stem) if source.is_dir() else None
    text = current.read_text(encoding="utf-8") if current else ""
    planned = None
    if current is None:
        report["plan"] = "no plan yet"  # a Task Page before its plan: only the folder moves
    elif is_sectioned(text):
        report["plan"] = f"{current.name} is already three sections"
    elif not _bullets(text):
        # A plan with no `- B<k> ·` Bullets has nothing to lay out in sections 1 and 3.
        report["plan"] = f"{current.name} has no Bullets; left as it is (write it as Bullets first)"
    else:
        planned = _three_sections(current, stem, text)
        report["plan"] = f"{current.name} → {planned[0]}"
    _group_evidence_file(source / f"{stem}-evidence-items.md", dry_run=True)  # refuses a changed item
    if rename:
        report["renamed"] = "outline/ → draft/"
        if not dry_run:
            outline.rename(draft)
    home = draft if (draft.is_dir() or not dry_run) else source
    if planned and not dry_run:
        target = home / planned[0]
        target.write_text(planned[1], encoding="utf-8")
        # The new plan is the newest by construction; a legacy `vN` would outrank
        # `v0.<N+1>` in version_key, so every other plan file moves by name.
        for other in plan_files(home, stem):
            if other != target and not (home / PREVIOUS / other.name).exists():
                (home / PREVIOUS).mkdir(exist_ok=True)
                other.rename(home / PREVIOUS / other.name)
    report["evidence"] = _group_evidence_file(home / f"{stem}-evidence-items.md", dry_run=dry_run)
    loose = [f for kind in RECORD_KINDS for f in home.glob(f"*-{kind}.md")
             if "-outline-" not in f.name and "-draft-" not in f.name] if home.is_dir() else []
    report["records_moved"] = len(loose) if dry_run else len(retire_records(home))
    if sort_runs:
        report.update(_sort_runs(folder, dry_run=dry_run))
    report["outline_paths"] = sweep_outline_paths(folder, [folder], dry_run=dry_run)
    if archive_evidence:
        report["archived_evidence"] = archive_retired_evidence(folder, dry_run=dry_run)
    return report


def draft_layout_tree(root: Path, *, sort_runs: bool = False, dry_run: bool = False,
                      archive_evidence: bool = False) -> dict:
    """Every Page under a Board or Task group, then `<page>/outline/` in the files around them."""
    from .layout_check import pages_in
    root = Path(root).expanduser().resolve()
    pages = pages_in(root)
    reports = []
    for page in pages:  # one Page that refuses does not stop the others
        try:
            reports.append(draft_layout(page, sort_runs=sort_runs, dry_run=dry_run,
                                        archive_evidence=archive_evidence))
        except ValueError as err:
            reports.append({"page": page.name, "refused": str(err)})
    # A Page citing another Page (`../Other/outline/...`) is swept once every Page has moved.
    between = sweep_outline_paths(root, pages, dry_run=dry_run)
    around = sweep_outline_paths(root, pages, pages_only=False, dry_run=dry_run)
    return {"root": str(root), "pages": reports, "between_pages": between, "around_pages": around,
            "next": "rebuild generated views that cite these paths (board/, delivery/)"}


# ---- retired Outline evidence → draft/_archive/legacy-outline-evidence/ ----------

LEGACY_EVIDENCE = "_archive/legacy-outline-evidence"


def _relative_links(root: Path) -> list[tuple[str, str]]:
    """Each relative symlink at or under `root`: (its path under root, the absolute target it names)."""
    found = []
    walk = [(root, ".")] if root.is_symlink() else [
        (Path(parent) / name, (Path(parent) / name).relative_to(root).as_posix())
        for parent, dirs, names in os.walk(root) for name in dirs + names
        if (Path(parent) / name).is_symlink()]
    for link, rel in walk:
        target = os.readlink(link)
        if not os.path.isabs(target):
            found.append((rel, os.path.normpath(os.path.join(link.parent, target))))
    return found


def archive_retired_evidence(page_folder: Path, *, dry_run: bool = False) -> dict:
    """Move retired Outline evidence under `draft/_archive/legacy-outline-evidence/`.

    Retired: every `draft/evidence/<lane>` except the live `bibex` (the Page
    export writes it) and `materials` (the Page's imports), and
    `draft/<stem>-evidence.md`. The `display` lane stays while
    any unit in it has no DISPLAY Result yet: the paper delivery still reads it
    by convention, not by a citation this move could follow. Paths citing the
    moved items inside the Page follow the move (`../../draft/evidence/...` in a
    LaTeX file too); sealed `results/` keep their words. A target that already
    exists stops the move of that item. Run the Page's own build afterwards.
    """
    from .layout_check import LIVE_LANES, retired_readers, unconverted_display_units
    folder = Path(page_folder).expanduser().resolve()
    home = plan_dir(folder)
    if not home.is_dir():
        home = folder / "draft"  # a Page with no plan yet: the archive still lives in draft/
    unconverted = unconverted_display_units(folder)
    kept = ["evidence/display (%d unit(s) without a DISPLAY Result)" % len(unconverted)] if unconverted else []
    items = []
    if (home / "evidence").is_dir():
        items += [(f"evidence/{p.name}", f"{LEGACY_EVIDENCE}/evidence/{p.name}")
                  for p in sorted((home / "evidence").iterdir())
                  if p.name not in LIVE_LANES and not (p.name == "display" and unconverted)]
    items += [(p.name, f"{LEGACY_EVIDENCE}/{p.name}") for p in sorted(home.glob("*-evidence.md"))]
    # A script that still reads a retired item would break: the item stays until the script moves.
    read = retired_readers(folder, [old.split("/")[-1] for old, _new in items])
    kept += ["%s (read by %s)" % (old, read[old.split("/")[-1]]) for old, _new in items
             if old.split("/")[-1] in read]
    items = [(old, new) for old, new in items if old.split("/")[-1] not in read]
    blocked = [old for old, new in items if (home / new).exists()]
    items = [(old, new) for old, new in items if old not in blocked]
    rewrites = files = 0
    swaps = [(re.compile(r"(?<![\w.-])%s/%s(?=[/`'\")}\s]|$)" % (home.name, re.escape(old)), re.M),
              "%s/%s" % (home.name, new)) for old, new in items]
    root = _archive_root_pagex(folder, home, dry_run=dry_run)
    kept += root["kept"]
    blocked += root["blocked"]
    swaps += root["swaps"]
    if not items and not root["moved"]:
        return {"moved": [], "kept": kept, "blocked": blocked, "files": 0, "paths_rewritten": 0}
    if not dry_run:
        for old, new in items:
            (home / new).parent.mkdir(parents=True, exist_ok=True)
            links = _relative_links(home / old)
            (home / old).rename(home / new)
            for rel, target in links:  # the move goes deeper: keep each relative link on its target
                link = (home / new) / rel if rel != "." else home / new
                link.unlink()
                link.symlink_to(os.path.relpath(target, link.parent))
        if (home / "evidence").is_dir() and not any((home / "evidence").iterdir()):
            (home / "evidence").rmdir()
    for path in folder.rglob("*"):
        if (not path.is_file() or path.is_symlink() or path.suffix.lower() in BINARY
                or SEALED & set(path.relative_to(folder).parts)):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new_text, n = text, 0
        for pattern, target in swaps:
            new_text, k = pattern.subn(target, new_text)
            n += k
        if n:
            files, rewrites = files + 1, rewrites + n
            if not dry_run:
                path.write_text(new_text, encoding="utf-8")
    return {"moved": [old for old, _ in items] + root["moved"], "kept": kept, "blocked": blocked,
            "files": files, "paths_rewritten": rewrites, **({"links_dropped": root["dropped"]}
                                                           if root["dropped"] else {})}


def _archive_root_pagex(folder: Path, home: Path, *, dry_run: bool) -> dict:
    """The pre-0.117 binding lane `pagex/` at the Page root joins the archived evidence.

    Its links (to sibling Page Faces, LaTeX sections, another Board's Pages) become
    copies of what they named, because the Page server refuses links; a link whose
    target is gone, or larger than 20 MB, is dropped and listed. Citations of
    `pagex/<entry>` inside the Page follow the move.
    """
    import shutil
    from .layout_check import retired_readers
    out = {"moved": [], "kept": [], "blocked": [], "swaps": [], "dropped": []}
    pagex = folder / "pagex"
    if not pagex.is_dir() or pagex.is_symlink():
        return out
    new = home / LEGACY_EVIDENCE / "pagex"
    read = retired_readers(folder, ["pagex/"])
    if read:
        out["kept"].append("pagex/ (read by %s)" % read["pagex/"])
        return out
    if new.exists():
        out["blocked"].append("pagex/")
        return out
    out["moved"].append("pagex/")
    out["swaps"] = [(re.compile(r"(?<![\w./-])pagex/(?=%s(?:[/`'\")}\s]|$))" % re.escape(p.name), re.M),
                     "%s/%s/pagex/" % (home.name, LEGACY_EVIDENCE)) for p in sorted(pagex.iterdir())]
    links = [(Path(parent, name).relative_to(pagex), os.path.realpath(Path(parent, name)))
             for parent, dirs, names in os.walk(pagex) for name in dirs + names
             if Path(parent, name).is_symlink()]
    if dry_run:
        out["dropped"] = [rel.as_posix() for rel, target in links if not os.path.exists(target)]
        return out
    new.parent.mkdir(parents=True, exist_ok=True)
    pagex.rename(new)
    for rel, target in links:
        link = new / rel
        if target.startswith(str(pagex) + os.sep):  # a link inside the lane moved with it
            target = str(new / Path(target).relative_to(pagex))
        size = sum(f.stat().st_size for f in Path(target).rglob("*") if f.is_file()) \
            if os.path.isdir(target) else os.path.getsize(target) if os.path.isfile(target) else None
        link.unlink()
        if size is None or size > 20 * 2 ** 20:
            out["dropped"].append(rel.as_posix())
        elif os.path.isdir(target):
            shutil.copytree(target, link, symlinks=False)
        else:
            shutil.copy2(target, link)
    return out


# ---- `outline/` → `draft/` in text that names a Page's plan folder -------------

# `results/` keeps its words. Nothing else is sealed: no receipt pins a file by a
# content hash (JL 260928), so a sweep rewrites every other file.
SEALED = {"results"}
# Generated output is never edited, only rebuilt (AGENTS.md: never modify a generated file).
# A sweep names each generated file that still cites `outline/` so the person reruns its build.
GENERATED = {"delivery", "board"}
MAINTAINED = {"paper-build.toml", "build.py", "preamble.tex"}   # inputs that sit beside the outputs
BINARY = {".png", ".pdf", ".docx", ".xdv", ".jpg", ".jpeg", ".gif", ".zip", ".gz", ".pptx",
          ".xlsx", ".parquet", ".pkl", ".dta", ".aux", ".fls", ".woff", ".woff2", ".ipynb"}
_OUTLINE = re.compile(r"(?<![\w.-])outline/")
_REST = re.compile(r"[\w./-]*")
_CITED = re.compile(r"(?<![\w.-])draft/([\w.-]+\.(?:md|mmd))\b")
_PATH_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.${}~-/")
_VARS = {"..", "PAGE_DIR", "page_dir", "PAGE", "page", "TASK_DIR", "task_dir"}


_PY_JOIN = re.compile(r"""(/\s*)(["'])outline\2""")


def kept_by_result(path) -> set[str]:
    """The `outline/...` paths a Run ticket shares with its own Result, which keep their words.

    A closed Run's Result records what the Run read (a Design Run's `runtime.yaml` inputs),
    and the Design run contract checks the ticket against that record. The Result is never
    edited, so the ticket keeps those same paths too: rewriting them left 12 Design Runs of
    DrFirst's R2Messages board with "runtime input manifest is incomplete" (JL 260929).
    """
    parts = Path(path).parts
    if "runs" not in parts:
        return set()
    i = len(parts) - 1 - parts[::-1].index("runs")
    result = Path(*parts[:i]) / "results" / Path(path).stem
    kept = set()
    for f in (result.rglob("*") if result.is_dir() else []):
        if f.is_file() and f.suffix in (".yaml", ".yml", ".json", ".md"):
            try:
                kept.update(re.findall(r"(?<![\w.-])outline/[\w./-]*\w", f.read_text(encoding="utf-8", errors="ignore")))
            except OSError:
                pass
    return kept


_STEP_WORDS = {"content", "evidence", "venue", "context", "check", "structure", "writing", "draft"}


def is_prose_outline(rest: str, page: Path) -> bool:
    """A bare `outline/<word>` that names two steps ("outline/content", "outline/evidence
    consistency") rather than a folder: a word with no `/` after it that is a step name or
    no entry of the plan folder. `outline/evidence/bibex` and `outline/<stem>-log.md` are paths."""
    m = re.match(r"(\w+)(.?)(.?)", rest)  # `t01_x-files.md`: a Task id is a name, not a word
    if not m or m.group(2) in ("/", "-", "_"):
        return False
    if m.group(2) == "." and re.match(r"\w", m.group(3)):
        return False  # `outline/content.md` is a file; "outline/content." ends a sentence
    word = m.group(1)
    return word.lower() in _STEP_WORDS or not any(
        (Path(page) / home / word).exists() for home in ("draft", "outline"))


def _before(text: str, start: int) -> str:
    k = start
    while k > 0 and start - k < 300 and text[k - 1] in _PATH_CHARS:
        k -= 1
    return text[k:start]


def sweep_outline_paths(root: Path, pages: list[Path], *, pages_only: bool = True,
                        dry_run: bool = False) -> dict:
    """Rewrite `outline/` to `draft/` where it names a migrated Page's plan folder.

    Inside a Page: bare `outline/`, `../outline/`, `$PAGE_DIR/outline/` and
    `<page>/outline/` all mean that plan folder. Around the Pages (with
    `pages_only=False`): only `<page>/outline/`. `_archive/` folders outside a
    Page keep their old layout on purpose, and `/_board/outline` is the old
    Draft URL, which still answers.
    A cited plan file that moved to `draft/previous/` or `draft/records/`
    follows it there.
    """
    root = Path(root).resolve()
    # A dry run counts the Pages that are about to move as well.
    by_name = {p.name: p.resolve() for p in pages
               if (p / "draft").is_dir() or (dry_run and (p / "outline").is_dir())}
    stems = sorted(by_name, key=len, reverse=True)
    moved = {}
    for name, page in by_name.items():
        home = page / "draft"
        seen = {}
        for f in home.rglob("*") if home.is_dir() else []:
            if f.is_file():
                seen.setdefault(f.name, []).append(f.parent.relative_to(home).as_posix())
        for fname, subs in seen.items():
            # Follow only a file that sits in exactly one of previous/ or records/ and not
            # at the top: two files of one name (history/ and previous/) are ambiguous.
            if len(subs) == 1 and subs[0] in ("previous", "records", LEGACY_EVIDENCE):
                moved.setdefault(name, {})[fname] = subs[0]
    files = swapped = repointed = 0
    rebuild = []

    scan = pages if pages_only else [root]
    for base in scan:
        for path in base.rglob("*"):
            rel = path.relative_to(root).parts if path.is_relative_to(root) else path.parts
            if ({".git", "_WorkSpace", "node_modules"} & set(rel) or not path.is_file() or path.is_symlink()
                    or path.suffix.lower() in BINARY | {".csv", ".tsv", ".log"}):
                continue
            if SEALED & set(path.parts):
                continue  # a Result keeps its words
            if GENERATED & set(rel) and path.name not in MAINTAINED:
                try:
                    if _OUTLINE.search(path.read_text(encoding="utf-8")):
                        rebuild.append("/".join(rel))
                except (UnicodeDecodeError, OSError):
                    pass
                continue  # generated: rebuilt by its own code, never edited here
            owner = next((page for page in by_name.values() if path.is_relative_to(page)), None)
            if not pages_only and (owner is not None or "_archive" in rel):
                continue  # Page files were swept per Page; archives keep their layout
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if "outline" not in text and "draft/" not in text:
                continue
            kept = kept_by_result(path)
            out, last, n = [], 0, 0
            for m in _OUTLINE.finditer(text):
                rest = _REST.match(text, m.end(), min(len(text), m.end() + 300)).group(0)
                if kept and ("outline/" + rest).rstrip("./-") in kept:
                    continue  # the ticket's own Result recorded this path
                pre = _before(text, m.start())
                seg = pre.rstrip("/").split("/")[-1] if pre else ""
                if rest.startswith("board-context") or seg == "_board":
                    continue
                named = bool(pre) and seg in by_name
                local = owner is not None and (not pre or seg.strip("${}") in _VARS
                                               or seg[:1] in "{$" or pre == "/")
                if local and not pre and is_prose_outline(rest, owner):
                    continue  # "outline/content" names two steps, not a folder
                if named or local:
                    out += [text[last:m.start()], "draft/"]
                    last, n = m.end(), n + 1
            out.append(text[last:])
            new = "".join(out)
            if path.suffix == ".py":  # `page_dir / "outline" / ...` builds the plan folder path
                new, k = _PY_JOIN.subn(r'\1\2draft\2', new)
                n += k
            moves = [0]

            def follow(m):
                name = m.group(1)
                page = next((s for s in stems if name.startswith(s + "-")), None)
                sub = moved.get(page, {}).get(name) if page else None
                if not sub:
                    return m.group(0)
                moves[0] += 1
                return "draft/%s/%s" % (sub, name)

            new = _CITED.sub(follow, new)
            if new != text:
                if not dry_run:
                    path.write_text(new, encoding="utf-8")
                files, swapped, repointed = files + 1, swapped + n, repointed + moves[0]
    return {"files": files, "outline_to_draft": swapped, "followed_moved_files": repointed,
            "rebuild_generated": sorted(set(rebuild))}


KIND_SECTIONS = (("CITE", "Citations"), ("DISPLAY", "Displays"), ("VALUE", "Values"))
_ITEM_HEAD = re.compile(r"^#{3,4} E\d+-([A-Z]+)-")


def group_evidence(text: str) -> str:
    """Group a flat Evidence Markdown into `## Citations`, `## Displays`, `## Values`.

    Each item block (a `### E..` or retired `#### E..` heading and its lines)
    moves under the section of its kind, in its original order. The header and
    any other `## ` section (retired items, status notes) stay as they are,
    after the three. A file that already has the three sections is returned
    unchanged.
    """
    lines = text.splitlines(keepends=True)
    names = {name for _, name in KIND_SECTIONS}
    if any(line.startswith("## ") and line[3:].strip() in names for line in lines):
        return text
    header, blocks, tail, current = [], {kind: [] for kind, _ in KIND_SECTIONS}, [], None
    for line in lines:
        if tail or line.startswith("## "):
            tail.append(line)
            continue
        match = _ITEM_HEAD.match(line)
        if match:
            kind = match.group(1)
            if kind not in blocks:
                raise ValueError(f"unknown evidence kind {kind!r} in: {line.strip()}")
            current = [line]
            blocks[kind].append(current)
        elif current is not None:
            current.append(line)
        else:
            header.append(line)
    if not any(blocks.values()):
        return text
    out = ["".join(header).rstrip("\n") + "\n"]
    for kind, name in KIND_SECTIONS:
        body = "".join("".join(block).rstrip("\n") + "\n\n" for block in blocks[kind])
        out.append("\n## %s\n\n%s" % (name, body))
    new = "".join(out).rstrip("\n") + "\n"
    if tail:
        new += "\n" + "".join(tail)
    return new


def _item_blocks(text: str) -> list[str]:
    """Every item block with blank lines trimmed, for a before/after check."""
    blocks, current = [], None
    for line in text.splitlines():
        if line.startswith("#"):
            current = [line] if _ITEM_HEAD.match(line) else None
            if current is not None:
                blocks.append(current)
        elif current is not None:
            current.append(line)
    return sorted("\n".join(b).strip() for b in blocks)


def _group_evidence_file(path: Path, *, dry_run: bool) -> str | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    try:
        new = group_evidence(text)
    except ValueError as err:  # a kind outside CITE / DISPLAY / VALUE: retyping it is Evidence work
        return f"not grouped: {err}"
    if new == text:
        return "already grouped" if "\n## Citations" in text else "no items"
    if _item_blocks(new) != _item_blocks(text):
        raise ValueError(f"{path.name}: grouping would change an Evidence Item; nothing written")
    if not dry_run:
        path.write_text(new, encoding="utf-8")
    return "grouped into Citations / Displays / Values"


# A moved ticket sits one folder deeper: `$(cd "$(dirname "$0")/.." && pwd)` and
# `$(cd "$script_dir/.." && pwd)` both climb one more level.
SCRIPT_UP = re.compile(r'(\$\(cd "(?:\$\(dirname [^)]*\)|\$\{?\w+\}?))/\.\.(" && pwd\))')


def _sort_runs(folder: Path, *, dry_run: bool) -> dict:
    runs = folder / "runs"
    moves = {}
    for ticket in sorted(p for p in runs.iterdir() if p.is_file()) if runs.is_dir() else []:
        space = folder_for(ticket.stem) or ("draft-auto-run" if ticket.name.startswith("rp-") else None)
        if space:
            moves[ticket.name] = space
    fixed = cited = 0
    if dry_run:
        return {"runs_moved": len(moves), "scripts_fixed": 0, "citations": 0}
    for name, space in moves.items():
        (runs / space).mkdir(exist_ok=True)
        (runs / name).rename(runs / space / name)
        moved = runs / space / name
        if moved.suffix == ".sh":
            text = moved.read_text(encoding="utf-8")
            new, n = SCRIPT_UP.subn(r"\1/../..\2", text)
            if n:
                moved.write_text(new, encoding="utf-8")
                fixed += n
    stems = {re.sub(r"\.(md|sh)$", "", name): space for name, space in moves.items()}
    token = re.compile(r"(?<![A-Za-z0-9_])((?:[\w.-]+/)*)runs/([A-Za-z0-9._-]+)")

    swapped = [0]

    def swap(match, path, text):
        owner, name = match.group(1), match.group(2)
        space = stems.get(re.sub(r"\.(md|sh)$", "", name))
        if not space:
            return match.group(0)
        parts = owner.rstrip("/").split("/") if owner else []
        variable = match.start(1) > 0 and text[match.start(1) - 1] in "${"
        if parts and not variable and parts[0] not in _VARS - {".."} and parts[-1] != folder.name:
            # A relative path: it names this Page's runs only if it resolves there from its file.
            target = os.path.normpath(os.path.join(path.parent, owner, "runs", name))
            if target != os.path.join(str(folder), "runs", name):
                return match.group(0)  # another Page's runs keep their own paths
        swapped[0] += 1
        return f"{owner}runs/{space}/{name}"

    for path in folder.rglob("*"):
        if path.is_file() and path.suffix in TEXT and not SEALED & set(path.relative_to(folder).parts):
            text = path.read_text(encoding="utf-8", errors="replace")
            new = token.sub(lambda m: swap(m, path, text), text)
            if new != text:
                path.write_text(new, encoding="utf-8")
    cited = swapped[0]
    return {"runs_moved": len(moves), "scripts_fixed": fixed, "citations": cited}

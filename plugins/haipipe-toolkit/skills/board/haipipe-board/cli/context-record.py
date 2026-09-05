#!/usr/bin/env python3
"""Write `outline/<stem>-context.md`: the CONTEXT/PREPARE snapshot of a Page.

    python3 cli/context-record.py <page.md>          one page
    python3 cli/context-record.py --all <board-dir>  every page on the board

`haipipe-page-context` (00 CONTEXT) owns the record; `haipipe-plugin-outline`
presents it as the 🧭 Overview chip of the Context Workspace. The law shipped
in 0.34.0 with `ref/context-record.md` and no generator, while the other three
Outline records each had one (`requirement.py`, `feedback.py`,
`evidence-status.py`), so every page reported `CONTEXT: owed` and the only way
to satisfy the phase was to hand-write a file the contract calls generated.

The six CTX rows are fixed and ordered. Each row states a resolution status,
the facts the next phase may rely on, and the exact source addresses with a
freshness fact. This is a PROJECTION: the source files stay authoritative and
nothing here is a human tick.

    CTX1  identity      Page, Folder kind, Folder owner, Page Face owner
    CTX2  purpose       Opening question, audience, scope, non-goals
    CTX3  policy        outline/structure/style authorities + requirements
    CTX4  related       Files rows and one-hop related Page scopes
    CTX5  feedback      feedback rows, open discussion, durable human decisions
    CTX6  readiness     plan version/approval, item tally, next authority

A source that cannot be read is recorded `missing`; PREPARE never invents the
rule. `Next authority` is OUTLINE only when no required row is missing.
"""
import argparse
import datetime
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent           # haipipe-board/
SKILLS = HERE.parent.parent                             # skills/
sys.path.insert(0, str(HERE))

from src import item_table                              # noqa: E402
from src.outline_version import latest_outline, version_tag  # noqa: E402

# page-type -> (Folder-owning workflow, Page Face owner), from
# haipipe-page/ref/type-registry.md `law:` rows.
OWNERS = {
    "ideation": ("haipipe-paper-workflow", "haipipe-paper-ideation"),
    "seed": ("haipipe-paper-workflow", "haipipe-paper-seed"),
    "roadmap": ("haipipe-paper-workflow", "haipipe-paper-roadmap"),
    "narrative": ("haipipe-paper-workflow", "haipipe-paper-narrative"),
    "section": ("haipipe-paper-workflow", "haipipe-paper-section"),
    "round": ("haipipe-paper-workflow", "haipipe-paper-round"),
    "venue": ("haipipe-paper-workflow", "haipipe-paper-venue"),
    "task": ("haipipe-task", "haipipe-task"),
    "insight": ("haipipe-task", "haipipe-page-for-insight"),
    "discovery": ("haipipe-discovery-workflow", "haipipe-discovery-inquiry"),
}
NONE = "none"


def fm(text, key):
    """One frontmatter row's value, or ''."""
    m = re.search(r"(?m)^%s:\s*(.+?)\s*$" % re.escape(key), text[:4000])
    return m.group(1).strip() if m else ""


def digest(path: Path) -> str:
    """Short content hash, the freshness fact for a stable-bytes source."""
    if not path.is_file():
        return "absent"
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def src(root: Path, path: Path) -> str:
    try:
        rel = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        rel = path.as_posix()
    return f"`{rel}` · {digest(path)}"


def opening(text: str) -> tuple[str, str]:
    """The Page's own reader question, and its `Covered elsewhere` line."""
    body = text.partition("\n## Opening")[2].partition("\n## ")[0]
    question = next((ln.strip() for ln in body.splitlines()
                     if ln.strip() and not ln.startswith(("<!--", "#"))), "")
    m = re.search(r"(?m)^\*\*Covered elsewhere\*\*:\s*(.+)$", body)
    return question, (m.group(1).strip() if m else "")


def record_ids(path: Path, prefix: str) -> list[str]:
    if not path.is_file():
        return []
    return re.findall(r"(?m)^### (%s\S*)" % prefix,
                      path.read_text(encoding="utf-8", errors="replace"))


def plan_of(outline_dir: Path, stem: str):
    """Newest plan file, its version, and its `approved:` value."""
    p = latest_outline(outline_dir, stem)
    if p is None:
        return None, "", ""
    return p, version_tag(p).removeprefix("v"), \
        fm(p.read_text(encoding="utf-8", errors="replace"), "approved")


def row(ident, status, pairs, sources):
    out = [f"### {ident}", f"- **Status**: {status}"]
    out += [f"- **{k}**: {v}" for k, v in pairs]
    out.append("- **Sources**: " + ("; ".join(sources) if sources else NONE))
    return "\n".join(out)


def build(page_md: Path, board: Path) -> str:
    page_md = page_md.resolve()          # repo_root() walks parents; a relative
    board = board.resolve()              # path has none, and the Run registry
    stem = page_md.stem                  # would silently read back empty
    text = page_md.read_text(encoding="utf-8", errors="replace")
    o = page_md.parent / "outline"
    root = item_table.repo_root(page_md.parent)
    missing = []

    # ── CTX1 identity ────────────────────────────────────────────────────
    phase_yaml = page_md.parent / "workflow" / "phase.yaml"
    if phase_yaml.is_file():
        kind = fm(phase_yaml.read_text(encoding="utf-8", errors="replace"), "folder-kind")
        kind_src = src(root, phase_yaml)
    else:
        kind = fm(text, "folder-kind") or fm(text, "page-type")
        kind_src = f"`{page_md.name}` frontmatter `page-type:`"
    folder_owner, face_owner = OWNERS.get(kind, ("unresolved", "unresolved"))
    if folder_owner == "unresolved":
        missing.append("CTX1")
    ctx1 = row("CTX1 · Page identity and ownership", "resolved" if kind else "missing", [
        ("Page", f"`{page_md.relative_to(board).as_posix()}`"),
        ("Folder kind", f"{kind or 'unresolved'} · source {kind_src}"),
        ("Folder owner", folder_owner),
        ("Page Face owner", face_owner),
        ("Current authority", "CONTEXT"),
    ], [src(root, page_md)])

    # ── CTX2 purpose ─────────────────────────────────────────────────────
    question, elsewhere = opening(text)
    if not question:
        missing.append("CTX2")
    ctx2 = row("CTX2 · Purpose and scope", "resolved" if question else "missing", [
        ("Question", question or "no Opening question on the Page"),
        ("Audience", fm(text, "venue") and f"{fm(text, 'venue')} desk reader" or "board reader"),
        ("Covered here", fm(text, "provides") or fm(text, "method") or "see the Page Opening"),
        ("Covered elsewhere", elsewhere or NONE),
    ], [src(root, page_md)])

    # ── CTX3 policy, structure, style ────────────────────────────────────
    req = o / f"{stem}-requirement.md"
    v_ids, w_ids = record_ids(req, "V"), record_ids(req, "W")
    structure = fm(text, "structure-source")
    division = fm(text, "structure-division")
    style = fm(text, "style-from")
    ctx3_sources = [f"`{SKILLS.name}/board/page-workflows/haipipe-page-outline/SKILL.md`"]
    if req.is_file():
        ctx3_sources.append(src(root, req))
    if structure:
        ctx3_sources.append(f"`{structure}`" + (f" {division}" if division else ""))
    ctx3 = row("CTX3 · Policy, structure, and style",
               "resolved" if (structure or kind != "section") else "missing", [
                   ("Outline policy", "haipipe-page-outline · SHAPE + SURVEY"),
                   ("Expected structure",
                    f"`{structure}`" + (f" · {division}" if division else "") if structure
                    else f"{face_owner} contract"),
                   ("Narrative/style policy",
                    f"{style} · haipipe-paper-narrative" if style else NONE),
                   ("Requirements",
                    f"`outline/{req.name}` · {len(v_ids)} V · {len(w_ids)} W"
                    if req.is_file() else "none generated"),
               ], ctx3_sources)
    if kind == "section" and not structure:
        missing.append("CTX3")

    # ── CTX4 related information ─────────────────────────────────────────
    files_rec = o / f"{stem}-files.md"
    f_ids = record_ids(files_rec, "F")
    requires = fm(text, "requires")
    ctx4 = row("CTX4 · Related information",
               "resolved" if (f_ids or requires) else "not-applicable", [
                   ("Rows", (f"{len(f_ids)} Files rows" if f_ids else "no Files rows")
                    + (f" · requires {requires}" if requires else "")),
                   ("Packet", f"`cli/pagecontext.py {page_md.name} --phase CONTEXT`"),
               ], [src(root, files_rec)] if files_rec.is_file() else [])

    # ── CTX5 feedback and open decisions ─────────────────────────────────
    fb = o / f"{stem}-feedback.md"
    disc = o / f"{stem}-discussion.md"
    fb_status = fm(fb.read_text(encoding="utf-8", errors="replace"), "status") if fb.is_file() else ""
    d_ids = record_ids(disc, "D")
    ctx5_sources = [src(root, p) for p in (fb, disc) if p.is_file()]
    ctx5 = row("CTX5 · Feedback and open decisions",
               "resolved" if ctx5_sources else "not-applicable", [
                   ("Feedback", fb_status or "no feedback record"),
                   ("Discussion", f"{len(d_ids)} open: {', '.join(d_ids)}" if d_ids else NONE),
                   ("Human decisions",
                    f"`outline/{fb.name}` and each plan's `approved:` row"
                    if fb.is_file() else "each plan's `approved:` row"),
               ], ctx5_sources)

    # ── CTX6 planning and evidence readiness ─────────────────────────────
    plan, ver, approved = plan_of(o, stem)
    rows = item_table.read_items(page_md)
    if rows:
        ready = sum(1 for r in rows.values() if r["planned"])
        decided = sum(1 for r in rows.values() if r["decision"])
        tally = (f"{len(rows)} typed · {ready} route-ready · {decided} decided"
                 f" · {len(rows) - decided} awaiting Decide")
    else:
        tally = NONE
    receipts = sorted((board / "_runs" / "page" / stem).glob("*.json")) \
        if (board / "_runs" / "page" / stem).is_dir() else []
    nxt = "OUTLINE" if not missing else "CONTEXT"
    ctx6 = row("CTX6 · Planning and evidence readiness",
               "resolved" if plan else "missing", [
                   ("Plan", f"`outline/{plan.name}` · v{ver} · approved: {approved or '⬜'}"
                    if plan else "no plan on disk"),
                   ("Evidence Items", tally),
                   ("Run receipts", f"{len(receipts)} under `_runs/page/{stem}/`"
                    if receipts else NONE),
                   ("Next authority", nxt),
               ], [src(root, plan)] if plan else [])
    if not plan:
        missing.append("CTX6")

    now = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
    head = [f"# {stem} · context", f"page: {stem}",
            "kind: context · generated · PREPARE resolves sources; source files remain authoritative",
            f"generated: {now}",
            f"regenerate: cli/context-record.py {page_md.name}", ""]
    return "\n".join(head + [ctx1, "", ctx2, "", ctx3, "", ctx4, "", ctx5, "", ctx6, ""])


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("target", type=Path)
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if a.all:
        board = a.target
        pages = [p / f"{p.name}.md" for g in sorted(board.iterdir())
                 if g.is_dir() and not g.name.startswith(("_", ".", "board"))
                 for p in sorted(g.iterdir())
                 if p.is_dir() and (p / f"{p.name}.md").is_file()]
    else:
        board, pages = a.target.parents[2], [a.target]
    n = 0
    for pg in pages:
        out = pg.parent / "outline" / f"{pg.stem}-context.md"
        out.parent.mkdir(exist_ok=True)
        out.write_text(build(pg, board), encoding="utf-8")
        n += 1
        print(f"wrote {out.relative_to(board)}")
    print(f"{n} file(s)")


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Create, inspect, build and serve a Page Folder without a Board."""
import argparse
import json
from pathlib import Path
import re
import sys

if sys.version_info < (3, 11):
    raise SystemExit("Page requires Python 3.11 or newer. Select an installed compatible interpreter.")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.page_workspace import build_page, create_page, load_page, source_files
from src.page_setup import run_setup
from src.page_migration import migrate_embedded_drafts, migrate_global_paragraphs


def _repoint_citations(folder: Path, moves: dict) -> int:
    """Rewrite `outline/<name>` to `outline/<sub>/<name>` in the Page's text files.

    `moves` maps a moved file name to its subfolder (`previous` or `records`).
    """
    if not moves:
        return 0
    pattern = re.compile(r"(outline|draft)/([A-Za-z0-9_.-]+\.(?:md|mmd))")
    count = 0
    for path in folder.rglob("*"):
        if not path.is_file() or {"previous", "_archive"} & set(path.relative_to(folder).parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        hits = [0]

        def swap(match):
            if match.group(2) in moves:
                hits[0] += 1
                return "%s/%s/%s" % (match.group(1), moves[match.group(2)], match.group(2))
            return match.group(0)

        new = pattern.sub(swap, text)
        if hits[0]:
            path.write_text(new, encoding="utf-8")
            count += hits[0]
    return count


def outline_tidy(target: Path, dry_run: bool = False) -> dict:
    """Current Outline Draft-first; superseded versions under outline/previous/."""
    from src.outline_version import (latest_outline, plan_files, retire_superseded, retire_records,
                                     version_key, PREVIOUS, RECORD_KINDS)
    from src.plan_shape import draft_first_plan, iter_plan_bullets

    target = target.expanduser().resolve()
    from src.outline_version import plan_dir
    outline = (target if target.name in ("outline", "draft") else
               plan_dir(target if target.is_dir() else target.parent))
    if not outline.is_dir():
        raise ValueError(f"No outline/ folder at {outline}")
    stem = target.stem if target.is_file() else None
    current = latest_outline(outline, stem)
    if current is None or current.parent != outline:
        raise ValueError(f"No current Outline version in {outline}")
    old = current.read_text(encoding="utf-8")
    new = draft_first_plan(old)
    shape = lambda text: [(b["address"], b["head"], b["draft"], b["continuation"])
                          for b in iter_plan_bullets(text)]
    if shape(new) != shape(old):
        raise ValueError(f"{current.name}: Draft-first rewrite would change a Bullet; nothing written")
    older = sorted((p for p in plan_files(outline, stem) if p != current), key=version_key)
    records = sorted(p for kind in RECORD_KINDS for p in outline.glob(f"*-{kind}.md")
                     if not re.search(r"-(?:outline|draft)-v\d", p.name))
    maps = sorted(outline.glob("*-logic.mmd"))  # retired Mermaid maps: nothing reads them
    result = {"current": current.name, "draft_first": new != old,
              "to_previous": [p.name for p in older + maps],
              "to_records": [p.name for p in records], "dry_run": dry_run}
    if not dry_run:
        if new != old:
            current.write_text(new, encoding="utf-8")
        moved = retire_superseded(outline, stem)
        for old_map in maps:
            target = outline / PREVIOUS / old_map.name
            if not target.exists():
                target.parent.mkdir(exist_ok=True)
                old_map.rename(target)
                moved.append(target)
        moved += retire_records(outline)
        result["moved"] = [str(p.relative_to(outline)) for p in moved]
        result["repointed"] = _repoint_citations(
            outline.parent, {p.name: p.parent.name for p in moved})
        result["left_in_place"] = sorted(p.name for p in plan_files(outline, stem) if p != current)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Create a Page Folder around a copy of a file")
    init.add_argument("--file", required=True, type=Path)
    init.add_argument("--dest", required=True, type=Path)
    init.add_argument("--title")
    setup = commands.add_parser(
        "setup", help="Create or populate a Markdown Page with real planning records"
    )
    setup.add_argument("target", type=Path,
                       help="Input Markdown file, Page Face, or existing Page Folder")
    setup.add_argument("--dest", type=Path,
                       help="Destination for a new file import; defaults to the file's sibling stem")
    setup.add_argument("--title")
    setup.add_argument("--force", action="store_true",
                       help="Replace generated Shape/preview after reviewing existing records")
    migrate = commands.add_parser(
        "migrate-addresses",
        help="Rewrite active Page records to Page-global paragraph addresses",
    )
    migrate.add_argument("page", type=Path)
    migrate_drafts = commands.add_parser(
        "migrate-drafts",
        help="Embed a legacy standalone Draft Markdown into the current Outline",
    )
    migrate_drafts.add_argument("page", type=Path)
    tidy = commands.add_parser(
        "outline-tidy",
        help="Current Outline Draft-first; old versions to outline/previous/, records to outline/records/",
    )
    tidy.add_argument("page", type=Path, help="Page Face .md, Page Folder, or its outline/ folder")
    tidy.add_argument("--dry-run", action="store_true")
    layout = commands.add_parser(
        "draft-layout",
        help="Move a Page to draft/ with a three-section Draft Markdown (0.118)",
    )
    layout.add_argument("page", type=Path,
                        help="Page Folder, Page Face .md, or a Board/Task group folder (every Page in it)")
    layout.add_argument("--sort-runs", action="store_true",
                        help="Also move each ticket in runs/ into its Space folder")
    layout.add_argument("--archive-evidence", action="store_true",
                        help="Also move retired Outline evidence to draft/_archive/legacy-outline-evidence/")
    layout.add_argument("--dry-run", action="store_true")
    layout_check = commands.add_parser(
        "check-page-folder",
        help="Is each Page Folder on the latest layout of this skill? Exit 1 if any is behind",
    )
    layout_check.add_argument("targets", type=Path, nargs="+",
                              help="Page Folders, Page Faces, or a Board/group folder (checks every Page in it)")
    layout_check.add_argument("--json", action="store_true")
    health = commands.add_parser(
        "health",
        help="Check that each Page Folder agrees with itself; exit 1 on any FAIL",
    )
    health.add_argument("pages", type=Path, nargs="+", help="Page Folders or Page Face .md files")
    health.add_argument("--json", action="store_true")
    adopt = commands.add_parser(
        "adopt",
        help="Write the current Draft's sentences into the Page's Content, in Draft order; "
             "refuse when the paragraphs do not match",
    )
    adopt.add_argument("pages", type=Path, nargs="+", help="Page Folders or Page Face .md files")
    adopt.add_argument("--plan", type=Path, help="Draft Markdown to adopt (default: the current one)")
    adopt.add_argument("--dry-run", action="store_true", help="Print the diff; write nothing")
    export = commands.add_parser(
        "export",
        help="Build the Page's delivery (web, LaTeX, Word) with no server, the same files a click writes",
    )
    export.add_argument("pages", type=Path, nargs="+", help="Page Folders or Page Face .md files")
    export.add_argument("--lane", choices=("web", "latex", "word", "all"), default="all")
    export.add_argument("--author", help='Name on the Word comments (papers: "Junjie Luo")')
    export.add_argument("--root", type=Path,
                        help="Root the view links assume (default: the repository root, as the Board server)")
    open_run = commands.add_parser(
        "open-run", help="Open a Page Run: write its one ticket, runs/run-<kind>-<MMDD>-<slug>.md")
    open_run.add_argument("page", type=Path)
    open_run.add_argument("--kind", required=True, help="structure, section, paragraph, scratch, revise, "
                          "auto-write, evidence-embed, context, check, citation, value or display")
    open_run.add_argument("--slug", default="", help="two to four words; default: the target or the goal")
    open_run.add_argument("--target", default="", help="C1, C1.P2, or an Evidence Item id")
    open_run.add_argument("--goal", default="")
    open_run.add_argument("--by", default="", help="who opened it (JL, Claude, Codex)")
    close_run = commands.add_parser(
        "close-run", help="Close a Page Run: write results/<run>/, mark the ticket closed, log one line")
    close_run.add_argument("page", type=Path)
    close_run.add_argument("run")
    close_run.add_argument("--summary", default="")
    close_run.add_argument("--by", default="")
    run_names_cmd = commands.add_parser(
        "run-names", help="Rename a Page's runs to run-<kind>-<MMDD>-<slug> in a flat runs/, once")
    run_names_cmd.add_argument("pages", type=Path, nargs="+")
    run_names_cmd.add_argument("--dry-run", action="store_true", help="Print old → new; change nothing")
    for command in ("inspect", "build", "serve"):
        sub = commands.add_parser(command)
        sub.add_argument("page", type=Path)
        if command == "build":
            sub.add_argument("--output", type=Path)
        if command == "serve":
            sub.add_argument("--host", default="127.0.0.1")
            sub.add_argument("--port", type=int, default=8765)
            sub.add_argument("--token", help="Prefer PAGE_SERVER_TOKEN environment variable")
            sub.add_argument("--read-only", action="store_true",
                             help="Disable Page workbench writes too (the Page itself is always reader-only)")
            sub.add_argument("--public-url", help="Configured reader-facing origin")
    args = parser.parse_args(argv)
    try:
        setup_result = None
        if args.command == "init":
            context = create_page(args.file, args.dest, args.title)
        elif args.command == "setup":
            target = args.target.expanduser().resolve()
            input_file = None
            if target.is_dir():
                if args.dest or args.title:
                    raise ValueError("A Page Folder already owns its destination and title")
                context = load_page(target)
            elif target.is_file():
                # A supplied Page Face is resumed in place.  Any other file is
                # imported to an explicit destination or its sibling stem.
                try:
                    context = load_page(target)
                    if args.dest or args.title:
                        raise ValueError(
                            "An existing Page Face already owns its destination and title"
                        )
                except ValueError:
                    text = target.read_text(encoding="utf-8", errors="ignore") \
                        if target.suffix.lower() in {".md", ".markdown"} else ""
                    if (target.parent / "page.toml").is_file() or (
                        target.stem == target.parent.name
                        and re.search(r"(?m)^## (?:🚪 )?Opening\s*$", text)
                    ):
                        raise
                    destination = (args.dest.expanduser().absolute() if args.dest
                                   else target.with_suffix(""))
                    if destination.exists():
                        if args.title:
                            raise ValueError("An existing Page keeps its current title; edit its Page Face explicitly")
                        context = load_page(destination)
                        manifest = destination / "page.toml"
                        # The Page names its imported copy; no intake hash (JL 260928).
                        declared = re.search(r'(?m)^content\s*=\s*"([^"]+)"',
                                             manifest.read_text(encoding="utf-8")) \
                            if manifest.is_file() else None
                        if not declared or Path(declared[1]).name != target.name:
                            raise ValueError("Destination exists but is not the Page created from this file")
                    else:
                        context = create_page(target, destination, args.title)
                    input_file = target
            else:
                raise ValueError("Setup target does not exist")
            setup_result = run_setup(context, force=args.force, input_file=input_file)
            context = load_page(context.folder)
        elif args.command == "migrate-addresses":
            context = load_page(args.page)
            print(json.dumps(migrate_global_paragraphs(context), indent=2))
            return
        elif args.command == "outline-tidy":
            print(json.dumps(outline_tidy(args.page, dry_run=args.dry_run), indent=2))
            return
        elif args.command == "draft-layout":
            from src.draft_migration import draft_layout, draft_layout_tree
            target = args.page.expanduser().resolve()
            one = target.is_file() or (target / f"{target.name}.md").is_file()
            run = draft_layout if one else draft_layout_tree
            print(json.dumps(run(target, sort_runs=args.sort_runs, dry_run=args.dry_run,
                                 archive_evidence=args.archive_evidence),
                             indent=2, ensure_ascii=False))
            return
        elif args.command == "check-page-folder":
            from src.layout_check import check_page_folder, pages_in, render
            pages = [page for target in args.targets for page in pages_in(target)]
            if not pages:
                raise ValueError("no Page Folder found under " + ", ".join(map(str, args.targets)))
            reports = [check_page_folder(page) for page in pages]
            if args.json:
                print(json.dumps(reports, indent=2, ensure_ascii=False))
            elif len(reports) == 1:
                print(render(reports[0]))
            else:
                for report in reports:
                    behind = [r for r in report["rules"] if r["state"] == "BEHIND"]
                    print("%s %s%s" % ("✅" if not behind else "⚠️", report["page"],
                                       "" if not behind else "  · behind: " + "; ".join(
                                           "%s → %s" % (r["rule"], r["fix"]) for r in behind)))
                n = sum(1 for r in reports if r["verdict"] == "behind")
                print("\n%d Page(s) · %d on the latest layout %s · %d behind"
                      % (len(reports), len(reports) - n, reports[0]["layout"], n))
            if any(report["verdict"] == "behind" for report in reports):
                sys.exit(1)
            return
        elif args.command == "health":
            from src.folder_health import FAIL, folder_health, render
            reports = [folder_health(page) for page in args.pages]
            if args.json:
                print(json.dumps(reports, indent=2, ensure_ascii=False))
            else:
                print("\n\n".join(render(report) for report in reports))
            if any(report["verdict"] == FAIL for report in reports):
                sys.exit(1)
            return
        elif args.command == "adopt":
            from src.page_adopt import render, run
            reports = [run(page, plan=args.plan, dry_run=args.dry_run) for page in args.pages]
            print("\n\n".join(render(report) for report in reports))
            if any(report["refused"] for report in reports):
                sys.exit(1)
            return
        elif args.command == "open-run":
            from src.run_lifecycle import open_run as _open
            print(json.dumps(_open(args.page, args.kind, args.slug, target=args.target, goal=args.goal,
                                   by=args.by), indent=2))
            return
        elif args.command == "close-run":
            from src.run_lifecycle import close_run as _close
            print(json.dumps(_close(args.page, args.run, summary=args.summary, by=args.by), indent=2))
            return
        elif args.command == "run-names":
            from src.run_rename import apply as _rename, render as _render_rename
            print("\n\n".join(_render_rename(_rename(page, dry_run=args.dry_run)) for page in args.pages))
            return
        elif args.command == "export":
            from src.page_export import export, write_ticket
            lanes = ("web", "latex", "word") if args.lane == "all" else (args.lane,)
            failed = False
            for page in args.pages:
                context = load_page(page)
                for lane in lanes:
                    write_ticket(context.folder, lane, args.author)
                results = {}
                if "web" in lanes:
                    results["web"] = {"ok": True, "out": str(build_page(context, None))}
                rest = [lane for lane in lanes if lane != "web"]
                if rest:
                    results.update(export(context.folder, rest, author=args.author, root=args.root))
                failed = failed or not all(r["ok"] for r in results.values())
                for lane, r in results.items():
                    shown = r.get("err") or r.get("pdf") or r.get("docx") or r.get("out") or r.get("url")
                    print("%s %-5s %s  %s" % ("✅" if r["ok"] else "❌", lane, context.source.stem, shown))
            if failed:
                sys.exit(1)
            return
        elif args.command == "migrate-drafts":
            context = load_page(args.page)
            print(json.dumps(migrate_embedded_drafts(context), indent=2))
            return
        else:
            context = load_page(args.page)
        if args.command in {"init", "setup", "inspect"}:
            result = {"folder": str(context.folder), "source": str(context.source),
                      "content": str(context.content) if context.content else None,
                      "title": context.title,
                      "files": [str(p.relative_to(context.folder)) for p in source_files(context)]}
            if setup_result:
                result["setup"] = setup_result
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif args.command == "build":
            print(build_page(context, args.output))
        else:
            import os
            servers = Path(__file__).resolve().parents[4] / "servers"
            sys.path.insert(0, str(servers / "haipipe-page"))
            from standalone_server import serve
            serve(context, host=args.host, port=args.port,
                  token=args.token or os.environ.get("PAGE_SERVER_TOKEN"),
                  read_only=args.read_only, public_url=args.public_url)
    except (ValueError, OSError) as error:
        parser.exit(2, f"Page: {error}\n")


if __name__ == "__main__":
    main()

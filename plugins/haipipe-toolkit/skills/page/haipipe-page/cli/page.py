#!/usr/bin/env python3
"""Create, inspect, build and serve a Page Folder without a Board."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

if sys.version_info < (3, 11):
    raise SystemExit("Page requires Python 3.11 or newer. Select an installed compatible interpreter.")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.page_workspace import build_page, create_page, load_page, source_files
from src.page_setup import run_setup
from src.page_migration import migrate_global_paragraphs


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
    for command in ("inspect", "build", "serve"):
        sub = commands.add_parser(command)
        sub.add_argument("page", type=Path)
        if command == "build":
            sub.add_argument("--output", type=Path)
        if command == "serve":
            sub.add_argument("--host", default="127.0.0.1")
            sub.add_argument("--port", type=int, default=8765)
            sub.add_argument("--token", help="Prefer PAGE_SERVER_TOKEN environment variable")
            sub.add_argument("--read-only", action="store_true")
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
                        if not manifest.is_file() or (
                            f'input_sha256 = "{sha256(target.read_bytes()).hexdigest()}"'
                            not in manifest.read_text(encoding="utf-8")
                        ):
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
            from src.standalone_server import serve
            serve(context, host=args.host, port=args.port,
                  token=args.token or os.environ.get("PAGE_SERVER_TOKEN"),
                  read_only=args.read_only, public_url=args.public_url)
    except (ValueError, OSError) as error:
        parser.exit(2, f"Page: {error}\n")


if __name__ == "__main__":
    main()

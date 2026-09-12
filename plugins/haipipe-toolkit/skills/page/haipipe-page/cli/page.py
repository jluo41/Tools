#!/usr/bin/env python3
"""Create, inspect, build and serve a Page Folder without a Board."""
import argparse
import json
from pathlib import Path
import sys

if sys.version_info < (3, 11):
    raise SystemExit("Page requires Python 3.11 or newer. Select an installed compatible interpreter.")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.page_workspace import build_page, create_page, load_page, source_files


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Create a Page Folder around a copy of a file")
    init.add_argument("--file", required=True, type=Path)
    init.add_argument("--dest", required=True, type=Path)
    init.add_argument("--title")
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
        if args.command == "init":
            context = create_page(args.file, args.dest, args.title)
        else:
            context = load_page(args.page)
        if args.command in {"init", "inspect"}:
            print(json.dumps({"folder": str(context.folder), "source": str(context.source),
                              "content": str(context.content) if context.content else None,
                              "title": context.title,
                              "files": [str(p.relative_to(context.folder)) for p in source_files(context)]}, indent=2, ensure_ascii=False))
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

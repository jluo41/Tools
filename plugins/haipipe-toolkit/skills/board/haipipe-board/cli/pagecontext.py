#!/usr/bin/env python3
"""Print bounded Related Board Page context for one Page Phase."""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

from src.page_context import PHASES, RelatedContextError, related_context_packet  # noqa: E402


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Read phase-matching Related Board Page scopes, one hop only."
    )
    parser.add_argument("page", type=Path, help="current Board Page source")
    parser.add_argument("--phase", required=True, choices=PHASES)
    args = parser.parse_args(argv)
    try:
        sys.stdout.write(related_context_packet(args.page, args.phase))
    except (OSError, RelatedContextError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

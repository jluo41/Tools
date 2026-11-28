"""Run lightweight, read-only checks for explicit Studio topics or a Block's registered topics."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import time

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from checks.common.paths import ROOT
from checks.common.results import Result, display, exit_code
from checks.skills.studio import follow, freshness, manifest, placeholders, scope


def check_targets(targets: list[Path], root: Path = ROOT) -> list[Result]:
    root = root.resolve()
    results, topics = [], set()
    for target in targets:
        target = (root / target).resolve()
        try:
            if not target.is_relative_to(root):
                raise ValueError("target leaves the SPACE")
            selected = scope.select(target, root)
            if not selected:
                results.append(Result("UNCOVERED", "scope", target,
                                      "no registered Studio checks; pass a Skills topic, Studio Type or Check-bound topic"))
            topics.update(selected)
        except (OSError, ValueError) as error:
            results.append(Result("ERROR", "scope", target, str(error)))
    for topic in sorted(topics):
        try:
            topic = topic.resolve()
            if not topic.is_relative_to(root):
                raise ValueError("topic leaves the SPACE")
            for source in scope.sources(topic):
                if not source.resolve().is_relative_to(root):
                    raise ValueError(f"source leaves the SPACE: {source.name}")
            kind = scope.kind(topic, root=root)
            if kind is None:
                results.append(Result("UNCOVERED", "scope", topic, "no checks registered for this topic"))
                continue
            data, bindings = manifest.read(topic, root)
            results.extend(bindings)
            if data is None:
                continue
            results.extend(freshness.check(topic, data, kind, root))
            results.extend(follow.check(topic, data, root))
            if kind == "type":
                results.extend(placeholders.check(topic))
        except (OSError, ValueError, TypeError, KeyError, ImportError, AttributeError) as error:
            results.append(Result("ERROR", "execution", topic, f"{type(error).__name__}: {error}"))
    return results


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, action="append", required=True,
                        help="topic, a file inside it, or Block; repeat for several targets")
    parser.add_argument("--root", type=Path, default=ROOT, help="SPACE root for target records")
    args = parser.parse_args(argv)
    start = time.perf_counter()
    results = check_targets(args.target, args.root)
    for result in results:
        print(display(result, args.root.resolve()))
    code = exit_code(results)
    print(f"Checks finished in {time.perf_counter() - start:.3f}s; exit {code}. "
          "Coverage: Studio bindings, generated freshness, type placeholders, following the named type only.")
    return code


if __name__ == "__main__":
    sys.exit(main())

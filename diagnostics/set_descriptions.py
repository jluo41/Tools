#!/usr/bin/env python3
"""Set skill descriptions from one reviewable YAML file.

    python3 diagnostics/set_descriptions.py diagnostics/descriptions/261026.yaml --dry-run
    python3 diagnostics/set_descriptions.py diagnostics/descriptions/261026.yaml

The YAML maps a skill name to its new description. For each skill (found under
plugins/**/skills/ by folder name, the installers' rule): the front matter's
description is replaced by one quoted line, the file must still parse with the
same name, and the skill gets one CHANGELOG entry and one patch bump, keyed by
--marker so a rerun never adds a second one. Paths another session owns are
refused, as in merge_parts.py.
"""

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from merge_parts import FM, PROTECT, REPO, add_changelog, bump  # noqa: E402


def find_skills():
    out = {}
    for root, dirs, files in os.walk(REPO / "plugins"):
        dirs[:] = [d for d in dirs if not d.startswith("_") and d != "node_modules"]
        if "SKILL.md" in files and "/skills/" in root + "/":
            out.setdefault(Path(root).name, Path(root))
    return out


def replace_description(text, new):
    m = FM.match(text)
    if not m:
        raise ValueError("no front matter")
    lines = m.group(1).split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("description:"))
    end = start + 1
    while end < len(lines) and (lines[end].startswith((" ", "\t")) or not lines[end].strip()) \
            and not re.match(r"^[A-Za-z_-]+:", lines[end]):
        end += 1
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1  # keep a blank line that separated the next key
    lines[start:end] = ["description: " + json.dumps(new, ensure_ascii=False)]
    return "---\n" + "\n".join(lines) + "\n---\n" + text[m.end():]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mapping")
    ap.add_argument("--marker", default="describe " + dt.date.today().strftime("%y%m%d"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    wanted = yaml.safe_load(Path(args.mapping).read_text(encoding="utf-8"))
    skills = find_skills()
    total_old = total_new = 0
    for name, desc in wanted.items():
        desc = " ".join(str(desc).split())
        folder = skills.get(name)
        if folder is None:
            print("  ! no skill named %s" % name)
            continue
        rel = os.path.relpath(folder, REPO) + "/"
        if any(rel.startswith(p) for p in PROTECT):
            print("  ! %s is in a protected path, skipped" % name)
            continue
        md = folder / "SKILL.md"
        text = md.read_text(encoding="utf-8")
        old = str(yaml.safe_load(FM.match(text).group(1)).get("description", ""))
        new_text = replace_description(text, desc)
        meta = yaml.safe_load(FM.match(new_text).group(1))
        assert meta.get("description") == desc and meta.get("name") == name, name
        total_old += len(old)
        total_new += len(desc)
        print("  %-32s %5d -> %4d chars" % (name, len(old), len(desc)))
        if args.dry_run:
            continue
        cl = folder / "CHANGELOG.md"
        if cl.exists() and args.marker in cl.read_text(encoding="utf-8"):
            md.write_text(new_text, encoding="utf-8")
            continue
        new_text, version = bump(new_text, minor=False)
        md.write_text(new_text, encoding="utf-8")
        add_changelog(folder, name, version,
                      "Shorter description (%d -> %d characters): what it does, when to use it, its trigger "
                      "words; aliases and old command names kept (%s)." % (len(old), len(desc), args.mapping),
                      args.marker)
    print("total %d -> %d characters (about %d -> %d tokens)" % (total_old, total_new, total_old // 4, total_new // 4))


if __name__ == "__main__":
    main()

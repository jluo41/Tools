#!/usr/bin/env python3
"""Hide skills behind their family door, without moving a folder.

    python3 diagnostics/hide_skills.py --door excalidraw --prefix excalidraw- \
        --dir plugins/haipipe-toolkit/skills/1_base/excalidraw [--dry-run]

Use this instead of merge_parts.py when other code imports a skill's files by path
(e.g. 488 drawing builders import excalidraw-studio/scripts/draw.py): the folders stay,
only the listing changes. For every skill in --dir whose name starts with --prefix:
  1. front matter gains `disable-model-invocation: true` (Claude Code drops the
     description from the listing; a person can still type /<name>);
  2. one CHANGELOG entry and one patch bump, keyed by --marker;
  3. markdown elsewhere that tells Claude to run it changes from /<prefix><kind> to
     /<door> <kind>, and Skill("<prefix><kind>") to Skill("<door>", args="<kind>").
Code files (the prompt strings they send are typed commands, which still work),
CHANGELOGs, the hidden skills' own folders and protected paths are left alone.
"""

import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from merge_parts import FM, REPO, SKIP, add_changelog, bump, repo_files  # noqa: E402

# another session's files that must not be rewritten here (blueprints are drawings and reports)
PROTECT = ["blueprints/", "plugins/haipipe-toolkit/servers/",
           "plugins/haipipe-toolkit/skills/1_base/project/haipipe-mindmap/"]
TODAY = dt.date.today().isoformat()


def hide(text):
    m = FM.match(text)
    fm = m.group(1)
    if re.search(r"(?m)^disable-model-invocation:\s*true", fm):
        return text
    lines = fm.split("\n")
    at = next((i for i, l in enumerate(lines) if l.startswith("metadata:")), len(lines))
    lines.insert(at, "disable-model-invocation: true")
    return "---\n" + "\n".join(lines) + "\n---\n" + text[m.end():]


def note_today(folder, note, marker):
    """Append to today's CHANGELOG entry if there is one, else add one entry and bump once."""
    cl = folder / "CHANGELOG.md"
    text = cl.read_text(encoding="utf-8") if cl.exists() else ""
    if marker in text:
        return "kept"
    m = re.search(r"(?m)^## \[[^\]]*\] — %s\n" % re.escape(TODAY), text)
    if m:
        end = text.find("\n## ", m.end())
        end = len(text) if end < 0 else end + 1
        text = text[:end].rstrip("\n") + "\n\n%s (%s)\n\n" % (note, marker) + text[end:].lstrip("\n")
        cl.write_text(text, encoding="utf-8")
        return "appended"
    md = folder / ("SKILL.md" if (folder / "SKILL.md").exists() else "PART.md")
    new, version = bump(md.read_text(encoding="utf-8"), minor=False)
    md.write_text(new, encoding="utf-8")
    add_changelog(folder, folder.name, version, note, marker)
    return "bumped %s" % version


def owner(path):
    d = Path(path).parent
    while d != REPO and d.parent != d:
        if (d / "SKILL.md").exists() or (d / "PART.md").exists():
            return d
        d = d.parent
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--door", required=True)
    ap.add_argument("--prefix", required=True, help="the shared name prefix, stripped to get the kind")
    ap.add_argument("--dir", required=True, help="the family folder searched for the skills")
    ap.add_argument("--names", default="", help="comma list of skill names to hide (default: every <prefix>* folder in --dir)")
    ap.add_argument("--rewrite-hidden", action="store_true",
                    help="also rewrite commands inside the hidden skills (siblings that call each other)")
    ap.add_argument("--marker", default="hide " + dt.date.today().strftime("%y%m%d"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    base = REPO / args.dir
    if args.names:
        wanted = {n.strip() if n.strip().startswith(args.prefix) else args.prefix + n.strip()
                  for n in args.names.split(",") if n.strip()}  # a kind or a full name
        skills = sorted({p.parent for p in base.rglob("SKILL.md")
                         if p.parent.name in wanted and "/_" not in str(p)}, key=lambda d: d.name)
        missing = wanted - {d.name for d in skills}
        if missing:
            sys.exit("not found under --dir: %s" % ", ".join(sorted(missing)))
    else:
        skills = sorted(d for d in base.iterdir() if d.name.startswith(args.prefix) and (d / "SKILL.md").exists())
    names = {d.name: d.name[len(args.prefix):] for d in skills}
    alt = "|".join(sorted(map(re.escape, names), key=len, reverse=True))
    slash = re.compile(r"(?<![\w.~/-])/(%s)(?![\w-])" % alt)
    call = re.compile(r'Skill\(\s*"(%s)"\s*\)' % alt)

    print("hide %d skills behind /%s: %s" % (len(skills), args.door, ", ".join(names.values())))
    for d in skills:
        md = d / "SKILL.md"
        if not args.dry_run:
            md.write_text(hide(md.read_text(encoding="utf-8")), encoding="utf-8")
            r = note_today(d, "Hidden from the skill listing (`disable-model-invocation: true`); reached "
                              "through the `/%s` door, which reads this SKILL.md by path. Nothing moved; "
                              "`/%s` still works when a person types it." % (args.door, d.name), args.marker)
            print("  %-22s %s" % (d.name, r))

    touched = {}
    for rel in repo_files():
        if not rel.endswith(".md") or rel.endswith("CHANGELOG.md"):
            continue
        inside = any(rel.startswith(os.path.relpath(d, REPO) + "/") for d in skills)
        if any(rel.startswith(p) for p in PROTECT + SKIP) or (inside and not args.rewrite_hidden):
            continue
        p = REPO / rel
        text = p.read_text(encoding="utf-8")
        new = slash.sub(lambda m: "/%s %s" % (args.door, names[m.group(1)]), text)
        new = call.sub(lambda m: 'Skill("%s", args="%s")' % (args.door, names[m.group(1)]), new)
        if new != text:
            touched[rel] = new.count("/%s " % args.door) - text.count("/%s " % args.door)
            if not args.dry_run:
                p.write_text(new, encoding="utf-8")
    print("markdown rewritten: %d files" % len(touched))
    owners = {}
    for rel, n in sorted(touched.items()):
        print("  ~ %s (%d)" % (rel, n))
        o = owner(REPO / rel)
        if o is not None and o.name != args.door:
            owners[str(o)] = o
    if not args.dry_run:
        for o in owners.values():
            if any(str(o) == str(d) for d in skills):
                continue  # a hidden skill already got its entry above
            r = note_today(o, "Commands to the hidden `%s*` skills now go through the door: `/%s <kind>`."
                           % (args.prefix, args.door), args.marker)
            print("  owner %-40s %s" % (os.path.relpath(o, REPO), r))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Two statements of one fact, compared. Read-only.

    python3 agree.py SKILL_DIR...          audit these skill folders
    python3 agree.py --all SKILLS_ROOT     audit every skill folder under a root

WHY THIS EXISTS
On 260802 three defects surfaced in one afternoon and all three were the same
shape: two halves of one contract, stating one fact, disagreeing, with nothing
that compares them.

    a cited path      the humanizer wrote `skills/writing/…`, its own hub two
                      files away wrote `<skills>/writing/…`, and only the second
                      resolves from where a session starts
    a version         SKILL.md frontmatter said 0.1.0 while CHANGELOG.md had
                      shipped 0.4.0, so every derived header was three releases
                      behind
    a round trip      wdiff.py apply wrote a record that wdiff.py check then
                      rejected, for any sentence that already carried a lane

Each was found by a person looking. None is hard to check. This checks the two
that are STATIC; the round trip is a test, not a grep, and lives in tests/.

WHAT IT REFUSES TO DO
Cry wolf. A checker that reports its own documentation as broken stops being
read (the same rule holes.py states). So a path inside a fenced block is skipped,
a `<placeholder>` segment is resolved rather than flagged, and a token that does
not look like a real path is left alone. False silence is preferred to noise:
this is a floor, not a proof.
"""
import argparse
import re
import sys
from pathlib import Path

# `## [0.6.1] — 2026-07-24` and `## 0.6.1 — …` are both in use. Missing the
# bracketed form is not a cosmetic bug: the scan then falls through to the NEXT
# heading and reports the version below the newest one, so a folder that agrees
# perfectly is reported as three releases adrift. That happened here, on 35 of
# 152 folders, in the checker written to catch exactly this class of defect.
SEMVER = re.compile(r"^##\s+\[?`?v?(\d+\.\d+\.\d+)`?\]?\s*(?:—|-|·|$)")
FRONT_VER = re.compile(r'^\s*version:\s*"?v?(\d+\.\d+\.\d+)"?', re.M)
FENCE = re.compile(r"^\s*```")
# A path is a WORD inside a backtick span, carrying a slash and a known tail.
# Matching the whole span instead would miss the case that matters most: the
# defect this checker was written for lives inside `python3 <skills>/…/wdiff.py
# record --old … --new …`, one backtick span holding a command, not a path.
# Anything else is prose that happens to contain a slash, and guessing costs
# more than it pays.
TICKED = re.compile(r"`([^`]+)`")
EXT = (".py", ".md", ".yml", ".yaml", ".json", ".sh", ".ps1", ".tex", ".css",
       ".js", ".svg", ".txt", ".bib", ".ipynb")
PLACEHOLDER = re.compile(r"^<[^>]+>/")
# ONLY a path that points into the skills tree is checked. The first sweep
# checked every path-shaped token and returned 1393 findings, of which the
# common ones were `1-probes/`, `results/`, `QA/`, `runs/<RUN>.sh`: shapes a
# skill DESCRIBES, folders a paper will grow or a run will produce. None of
# them is a citation and none of them can resolve, so reporting them is the
# crying-wolf failure this file's docstring promises not to commit.
# A cross-skill citation is different: it names a real file, a reader is meant
# to open it, and if it does not resolve the instruction cannot be followed.
FAMILIES = {"paper", "board", "probe", "display", "writing", "task", "discovery",
            "application", "project", "0_connect", "0_utils", "skills"}


def cited_paths(text):
    """-> [(line_no, token)] for every path-shaped word in a backtick span.

    Fenced blocks are NOT skipped, and that was a real bug for about ten
    minutes. The instruction this checker exists to catch,
    `haipipe-paper-revise-humanizer/SKILL.md:94`, lives inside an untagged fence
    that holds prose rather than code, so skipping fences made the checker blind
    to its own reason for existing. A path in a fence is still a path; unlike a
    `\\cite{TOADD}` marker, it does not become an example merely by being quoted.
    """
    out = []
    for i, ln in enumerate(text.splitlines(), 1):
        for span in TICKED.findall(ln):
            for tok in span.split():
                tok = tok.strip(",;:()[]\"'")
                if "://" in tok or "*" in tok or "…" in tok:
                    continue
                if "/" not in tok:
                    continue
                if not (tok.endswith(EXT) or tok.endswith("/")):
                    continue
                out.append((i, tok))
    return out


def resolve(tok, own_dir, skill_dir, skills_root, plugin_root, repo_root):
    """-> the name of the FIRST base the token resolves under, or None.

    Order is deliberate: the canonical form is a `<skills>/`-rooted path, so
    `skills-root` is tried before the accidents. A token that resolves only
    under `plugin-root` or `cwd` is the humanizer's defect exactly: it works
    from one directory and fails from the one a session actually starts in.
    """
    bare = PLACEHOLDER.sub("", tok)
    for name, base in (("skills-root", skills_root), ("own-dir", own_dir),
                       ("skill-dir", skill_dir), ("repo-root", repo_root),
                       ("plugin-root", plugin_root)):
        if base and (base / bare).exists():
            return name
    return None


def audit_skill(skill_dir, skills_root, plugin_root, repo_root):
    """-> (version_finding | None, [path findings])"""
    skill_dir = Path(skill_dir).resolve()
    ver_finding, paths = None, []

    sk, cl = skill_dir / "SKILL.md", skill_dir / "CHANGELOG.md"
    if sk.exists() and cl.exists():
        m = FRONT_VER.search(sk.read_text(encoding="utf-8", errors="replace"))
        newest = next((x.group(1) for x in
                       (SEMVER.match(l) for l in cl.read_text(encoding="utf-8", errors="replace").splitlines())
                       if x), None)
        if m and newest and m.group(1) != newest:
            ver_finding = (m.group(1), newest)

    for md in sorted(skill_dir.rglob("*.md")):
        if any(p.startswith((".", "_")) for p in md.relative_to(skill_dir).parts):
            continue
        if md.name == "CHANGELOG.md":          # history cites paths that have since moved
            continue
        for line, tok in cited_paths(md.read_text(encoding="utf-8", errors="replace")):
            head = PLACEHOLDER.sub("", tok).split("/")[0]
            if head not in FAMILIES:
                continue
            base = resolve(tok, md.parent, skill_dir, skills_root, plugin_root, repo_root)
            if base is None:
                paths.append((md, line, tok, "DEAD"))
            elif base == "plugin-root":
                paths.append((md, line, tok, "resolves only from the plugin root"))
    return ver_finding, paths


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--all", action="store_true",
                    help="treat each argument as a ROOT and audit every skill folder under it")
    ap.add_argument("--quiet", action="store_true", help="print only folders with findings")
    a = ap.parse_args()

    targets = []
    for d in a.dirs:
        p = Path(d).resolve()
        targets.extend(sorted(x.parent for x in p.rglob("SKILL.md")) if a.all else [p])

    nver = npath = 0
    for skill in targets:
        skills_root = next((q for q in skill.parents if q.name == "skills"), None)
        plugin_root = skills_root.parent if skills_root else None
        repo_root = next((q for q in skill.parents if (q / "pyproject.toml").exists()), None)
        ver, paths = audit_skill(skill, skills_root, plugin_root, repo_root)
        if not ver and not paths:
            if not a.quiet:
                print("✅ %s" % skill.name)
            continue
        print("\n📁 %s" % skill.name)
        if ver:
            nver += 1
            print("   🔢 version · SKILL.md says %s · CHANGELOG.md shipped %s" % ver)
        for md, line, tok, why in paths:
            npath += 1
            print("   🔗 path    · %s:%d  %-58s %s" % (md.name, line, tok, why))

    print("\n%d skill folder(s) · %d version disagreement(s) · %d path finding(s)"
          % (len(targets), nver, npath))
    sys.exit(1 if (nver or npath) else 0)


if __name__ == "__main__":
    main()

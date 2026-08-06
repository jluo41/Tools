#!/usr/bin/env python3
"""Resolve one atom to another by ID, so no file ever writes a sibling's path.

WHAT AN ATOM IS. Anything that produces something another page may read. It
declares itself in the head of its own markdown file:

    provides: <path>          exactly one, relative to that file's folder
    needs:    <id>, <id>      zero or more, by id, never by path

Two shapes of atom live in this group, and they are not the same shape:

    QBt3-for-display.md         a page that IS an atom. It provides a render.
    QA-probe/<page>/1-….md      a QA record that is an atom. It provides a table.

And one shape that is NOT an atom:

    QBt5-for-value.md           a page that is a VIEW over N QA atoms. It has
                                consumers and digests, and it provides nothing.

WHY. A real display page reaches its data through six hand-written paths. Every
one dies when a folder moves, and the 260806 sweep of two boards spent most of
its findings on exactly that. An id does not die. Moving any folder here costs
zero edits, which this file's `check` proves rather than claims.

USAGE
    python3 unit.py check       every declared need resolves, every product exists
    python3 unit.py build       run each atom's build step in dependency order
    python3 unit.py show <id>   one atom's resolved facts
"""
import re
import sys
import pathlib
import subprocess

GROUP = pathlib.Path(__file__).resolve().parent

# An atom's id is its path from the group folder, without the .md suffix, so the
# id is readable and unique without anyone maintaining a registry.
#   QA-probe/QBt5-for-value/1-drift-counts.md  ->  QA-probe/QBt5-for-value/1-drift-counts
#   QBt3-for-display.md                 ->  QBt3-for-display
# Two head styles exist and both are real. A board page writes bare `provides:`
# lines; a QA record writes them as list items, `- provides:`, which is the shape
# the task bank already uses for `- state:` and `- started:`. Accept either.
HEAD_KEY = re.compile(r"^-?\s*(provides|needs|bank|route):\s*(.*)$")


def head(md):
    """Read the head keys above the first `## ` heading."""
    out = {}
    for line in md.read_text(errors="ignore").splitlines():
        if line.startswith("## "):
            break
        m = HEAD_KEY.match(line.strip())
        if m:
            key, val = m.group(1), m.group(2).strip()
            out[key] = [v.strip() for v in val.split(",") if v.strip()] if key == "needs" else val
    return out


def atoms():
    """Every markdown file in this group that declares a provides: line."""
    found = {}
    for f in sorted(GROUP.rglob("*.md")):
        if any(p.name.endswith(".data") for p in f.parents):
            continue                       # products and evidence, never atoms
        meta = head(f)
        if "provides" not in meta:
            continue                       # a view page, or plain prose
        uid = f.relative_to(GROUP).with_suffix("").as_posix()
        meta["file"] = f
        meta["dir"] = f.parent
        found[uid] = meta
    return found


def resolve(uid, index=None):
    """Turn an atom id into the path of the one artifact it provides."""
    index = index if index is not None else atoms()
    if uid not in index:
        raise SystemExit(
            f"unknown atom id: {uid}\nknown ids:\n  " + "\n  ".join(sorted(index)))
    return index[uid]["dir"] / index[uid]["provides"]


def order(index):
    done, out = set(), []

    def visit(uid, stack=()):
        if uid in done:
            return
        if uid in stack:
            raise SystemExit("cycle in needs: " + " -> ".join((*stack, uid)))
        for need in index[uid].get("needs", []):
            if need in index:
                visit(need, (*stack, uid))
        done.add(uid)
        out.append(uid)

    for uid in sorted(index):
        visit(uid)
    return out


def check():
    index = atoms()
    views = [f.relative_to(GROUP).as_posix() for f in sorted(GROUP.glob("QBt*.md"))
             if "provides" not in head(f)]
    problems = []
    print(f"{len(index)} atoms · {len(views)} view pages\n")
    for uid in sorted(index):
        a = index[uid]
        needs = ", ".join(a.get("needs", [])) or "nothing"
        product = a["dir"] / a["provides"]
        mark = "✅" if product.exists() else "❌"
        print(f"  {mark} {uid}")
        route = a.get("route")
        if route == "local":
            print(f"      route    local · this file is the original, no bank")
            if a.get("bank"):
                problems.append(f"  {uid}: route is local yet it declares a bank")
        elif route:
            # A bank lives in the executor's own tree and is NEVER copied into the
            # paper, so an unreachable bank is a normal state, not a defect: it
            # means that tree is not cloned here. Report it, do not fail on it.
            bank = (GROUP / a["bank"]).resolve() if a.get("bank") else None
            if bank is None:
                problems.append(f"  {uid}: route {route} needs a bank: path")
            else:
                mark2 = "✅ reachable" if bank.exists() else "⚠️ not cloned here"
                print(f"      route    {route} · bank {mark2}")
                print(f"               {a['bank']}")
        print(f"      needs    {needs}")
        print(f"      provides {a['provides']}")
        if not product.exists():
            problems.append(f"  {uid}: product missing, {a['provides']} (run build)")
        for need in a.get("needs", []):
            if need not in index:
                problems.append(f"  {uid}: needs {need}, which no atom declares")
            elif not resolve(need, index).exists():
                problems.append(f"  {uid}: needs {need}, whose product is not built")
    for v in views:
        print(f"  👁 {v}\n      a view page, provides nothing, correct")
    if problems:
        print("\nPROBLEMS\n" + "\n".join(problems))
        return 1
    print("\nevery declared need resolves, and every product exists")
    return 0


def space_root():
    """The SPACE root, the repo convention: the folder holding pyproject.toml."""
    for d in [GROUP, *GROUP.parents]:
        if (d / "pyproject.toml").exists() and (d / "Tools").exists():
            return d
    return None


# A row in templates/<page>.md: a path, then 🔒 or 📎, then ✅ or ⚠️. Only the
# ✅ rows are checked; ⚠️ says the rule lives in a repository this checkout does
# not hold, which is a fact about the checkout and not a defect in the page.
TPL_ROW = re.compile(r"^\s{2,}(?!what\b)(\S.*?)\s{2,}[🔒📎]\s*\w+\s+(✅|⚠️)\s*$")
TPL_CONT = re.compile(r"^\s{6,}(\S[^\s].*)$")


def templates():
    """Check every reachable pointer in templates/ actually resolves.

    A list of where the rules live is only worth having if it cannot quietly go
    stale, which is the same reason `needs:` is an id rather than a path. A row
    marked ✅ names something this checkout holds, so it is opened; a row marked
    ⚠️ is counted and skipped.
    """
    folder = GROUP / "templates"
    if not folder.is_dir():
        print("no templates/ folder")
        return 0
    root, problems, checked, skipped = space_root(), [], 0, 0
    for f in sorted(folder.glob("*.md")):
        if f.name == "README.md":
            continue
        print(f"  📄 {f.name}")
        lines = f.read_text().splitlines()
        for i, line in enumerate(lines):
            m = TPL_ROW.match(line)
            if not m:
                continue
            target, reach = m.group(1).strip(), m.group(2)
            # A path may wrap onto the next line, indented further.
            nxt = TPL_CONT.match(lines[i + 1]) if i + 1 < len(lines) else None
            if nxt and not target.endswith("/") and "/" in target:
                pass
            elif nxt and target.endswith("/"):
                target += nxt.group(1).split()[0]
            if reach == "⚠️":
                skipped += 1
                print(f"      ⚠️ {target}  (not in this checkout, skipped)")
                continue
            checked += 1
            if "§" in target or not ("/" in target or target.endswith(".md")):
                print(f"      ✅ {target}  (a page division, not a file)")
                continue
            hit = (root / target) if root else None
            if hit and hit.exists():
                print(f"      ✅ {target}")
            else:
                print(f"      ❌ {target}")
                problems.append(f"  {f.name}: {target} does not resolve")
    print(f"\n{checked} reachable rows checked · {skipped} skipped as not cloned here")
    if problems:
        print("\nPROBLEMS\n" + "\n".join(problems))
        return 1
    print("every reachable pointer resolves")
    return 0


def build_script(atom):
    """The build step for an atom, found rather than assumed.

    Two companion shapes exist, because a page's companion and a QA's companion
    sit at different levels: `displays/<page-name>/` beside the page, and
    `<qa-name>.data/` inside the `QA-probe/<page-name>/` drawer. Rather than
    encode both, walk up from the product until a folder holding
    `source/build.py` appears. A new companion shape then costs nothing here.
    """
    product = atom["dir"] / atom["provides"]
    for d in product.parents:
        if not d.is_relative_to(atom["dir"]):
            break
        candidate = d / "source" / "build.py"
        if candidate.exists():
            return candidate
    return None


def build():
    index = atoms()
    for uid in order(index):
        script = build_script(index[uid])
        if script is None:
            print(f"·  {uid:<44} no build step", flush=True)
            continue
        print(f"▶  {uid}", flush=True)
        r = subprocess.run([sys.executable, str(script)], cwd=script.parent)
        if r.returncode:
            return r.returncode
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        sys.exit(check())
    if cmd == "build":
        sys.exit(build())
    if cmd == "show":
        for k, v in atoms()[sys.argv[2]].items():
            print(f"{k:<10} {v}")
        sys.exit(0)
    sys.exit(f"unknown command: {cmd}")

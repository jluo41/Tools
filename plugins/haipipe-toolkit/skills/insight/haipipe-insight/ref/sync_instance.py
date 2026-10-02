"""sync_instance.py <instance> [--question <id>] [--diff | --pull | --reviewed <file>] · Prototype vs Instance scripts.

An Instance question folder carries its own copy of the Prototype question's
scripts/ (ref/prototype-contract.md § Scripts in both boards). Its
scripts/prototype.lock records, per file, the Prototype file's sha256 when it was
copied: the base. Three versions are compared, base · Prototype now · Instance now:

    in sync            neither changed since the copy
    instance changed   a local adaptation: review it (--reviewed), keep it, or offer it to the Prototype
    prototype changed  an update is waiting: --pull copies it in and moves the base
    both changed       a conflict: merge by hand, then --pull --keep-instance moves the base
    new in prototype   the Prototype gained a script the Instance lacks: --pull copies it
    only in instance   a script the Prototype does not have

--diff prints the Instance file against the Prototype file. --pull replaces each
"prototype changed" or "new in prototype" file with the Prototype's and moves its
base; with --keep-instance it only moves the base of a "both changed" file whose
merge is done. --reviewed <file> records that an agent that did not write the
local change reviewed it at its current hash. Every pull or edit makes the runs
STALE until rerun (the runner records the scripts' hash).
"""
import argparse
import difflib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_question import file_sha, front, question_folders  # noqa: E402
from scaffold_instance import read_lock, write_lock  # noqa: E402


def file_state(name, lock, proto_dir, inst_dir):
    p, i = proto_dir / name, inst_dir / name
    base = (lock["files"].get(name) or {}).get("base")
    if not i.exists():
        return "new in prototype"
    if not p.exists():
        return "only in instance"
    pc, ic = file_sha(p) != base, file_sha(i) != base
    return {(False, False): "in sync", (False, True): "instance changed",
            (True, False): "prototype changed", (True, True): "both changed"}[(pc, ic)]


def pairs(instance, only=None):
    instance = Path(instance).resolve()
    meta, _ = front(instance / "board.md")
    prototype = (instance / meta["prototype"]).resolve()
    for pq in question_folders(prototype):
        if only and only not in (pq.name, pq.name[:3]):
            continue
        iq = instance / pq.parent.name / pq.name
        if (pq / "scripts").is_dir() or (iq / "scripts").is_dir():
            yield pq, iq


def status(instance, only=None):
    """[(question folder, file, state, reviewed)] for every script either board holds."""
    rows = []
    for pq, iq in pairs(instance, only):
        pdir, idir = pq / "scripts", iq / "scripts"
        lock = read_lock(idir)
        names = sorted({f.name for d in (pdir, idir) if d.is_dir() for f in d.glob("*.py")})
        for name in names:
            st = file_state(name, lock, pdir, idir)
            rev = (lock["files"].get(name) or {}).get("reviewed")
            reviewed = bool(rev) and (idir / name).exists() and rev == file_sha(idir / name)
            rows.append((iq, name, st, reviewed))
    return rows


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("instance")
    a.add_argument("--question")
    g = a.add_mutually_exclusive_group()
    g.add_argument("--diff", action="store_true")
    g.add_argument("--pull", action="store_true")
    g.add_argument("--reviewed", metavar="FILE")
    a.add_argument("--keep-instance", action="store_true")
    args = a.parse_args(argv)
    for pq, iq in pairs(args.instance, args.question):
        pdir, idir = pq / "scripts", iq / "scripts"
        lock = read_lock(idir)
        changed = False
        for name in sorted({f.name for d in (pdir, idir) if d.is_dir() for f in d.glob("*.py")}):
            st = file_state(name, lock, pdir, idir)
            entry = lock["files"].setdefault(name, {"base": None, "reviewed": None})
            if args.diff and st != "in sync":
                old = (pdir / name).read_text().splitlines(True) if (pdir / name).exists() else []
                new = (idir / name).read_text().splitlines(True) if (idir / name).exists() else []
                sys.stdout.writelines(difflib.unified_diff(old, new, f"prototype/{pq.name}/{name}",
                                                           f"instance/{iq.name}/{name}"))
            elif args.pull and st in ("prototype changed", "new in prototype"):
                idir.mkdir(parents=True, exist_ok=True)
                (idir / name).write_bytes((pdir / name).read_bytes())
                entry.update(base=file_sha(pdir / name), reviewed=None)
                changed = True
                print(f"pulled   {iq.name}/scripts/{name}")
            elif args.pull and args.keep_instance and st == "both changed":
                entry["base"] = file_sha(pdir / name)
                changed = True
                print(f"rebased  {iq.name}/scripts/{name} (the merge is the Instance's file)")
            elif args.reviewed == name and (idir / name).exists():
                entry["reviewed"] = file_sha(idir / name)
                changed = True
                print(f"reviewed {iq.name}/scripts/{name} at its current hash")
            elif not (args.diff or args.pull or args.reviewed):
                rev = entry.get("reviewed") and (idir / name).exists() and entry["reviewed"] == file_sha(idir / name)
                print(f"{st:18} {iq.parent.name}/{iq.name}/scripts/{name}" + ("  · local change reviewed" if rev else ""))
        if changed:
            write_lock(idir, lock)
    return 0


if __name__ == "__main__":
    sys.exit(main())

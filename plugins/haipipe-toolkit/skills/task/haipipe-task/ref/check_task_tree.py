#!/usr/bin/env python3
"""Check a block tree against the naming rules and the wiring it claims.

    python3 _tools/check_task_tree.py <block-or-tasks-dir> [--expect-fail]

Every rule is one this repo actually broke. Codes N* are naming, S* structural.
`--expect-fail` inverts the exit code: use it to prove the checker can fail
before trusting a pass (haipipe-task GATE-1).
"""
import pathlib, re, sys, collections

SHAPE = {"data","table","pipeline","analysis","pool","rank","set","list","baseline","scope","processing"}
IDX   = re.compile(r'^([bjtr])(\d\d)_(.+)$')
DO    = re.compile(r'\bdo\s+"([A-Za-z0-9_./${}`\'-]+\.do)"')

def rows(root):
    for block in sorted(p for p in ([root] if root.name.startswith("b") else root.iterdir()) if p.is_dir()):
        if not block.name.startswith("b"): continue
        yield block

def check(root):
    F = []
    def bad(code, where, msg): F.append((code, str(where), msg))

    for block in rows(root):
        jobs = [p for p in sorted(block.iterdir()) if p.is_dir() and p.name.startswith("j")]
        seen_tasks = {}
        for lvl, p in [("b", block)] + [("j", j) for j in jobs]:
            m = IDX.match(p.name)
            if not m or m.group(1) != lvl:
                bad("N1", p.name, f"does not match <{lvl}>NN_<name>")
                continue
            words = m.group(3).split("_")
            if all(w in SHAPE or w.isdigit() or len(w) <= 2 for w in words):
                bad("N5", p.name, "shape words only; says no concrete thing")
            if lvl == "j" and len(words) < 3:
                bad("N1", p.name, "a job name must stand alone: <stage>_<kind>_<subject>")

        for job in jobs:
            tasks = [p for p in sorted(job.iterdir()) if p.is_dir() and p.name.startswith("t")]
            for t in tasks:
                m = IDX.match(t.name)
                if not m or m.group(1) != "t":
                    bad("N1", t.name, "does not match tNN_<name>"); continue
                if not re.match(r'^[A-Z]', m.group(3)) and "_" not in m.group(3):
                    bad("N5", t.name, "task name carries no subject")
                if t.name in seen_tasks:
                    bad("N6", t.name, f"also in {seen_tasks[t.name]}; a rename map hits both")
                seen_tasks[t.name] = job.name
                if not (t/f"{t.name}.md").exists():
                    bad("S5", t.name, "no task page")

                cfg_dir = t/"config"
                shared = [c for c in cfg_dir.glob("*.do") if not c.name.startswith("r")] if cfg_dir.is_dir() else []
                if cfg_dir.is_dir() and len(shared) != 1:
                    bad("N8", t.name, f"config/ must hold exactly one shared (non-rNN) .do; found {len(shared)}")
                runcfgs = {c.stem for c in cfg_dir.rglob("r*.do")} if cfg_dir.is_dir() else set()
                tickets = {k.stem for k in (t/"runs").rglob("*.ps1")} if (t/"runs").is_dir() else set()
                for stem in sorted(tickets - runcfgs):
                    bad("N7", f"{t.name}/{stem}", "ticket has no config of the same stem")
                for stem in sorted(runcfgs - tickets):
                    bad("N7", f"{t.name}/{stem}", "config has no ticket of the same stem")
                for k in sorted(tickets):
                    if not re.match(r'^r\d\d_[ABCD]_(cms|case|data|reg)_', k):
                        bad("N2", f"{t.name}/{k}", "run name carries no stage letter and kind")

            # N4 applies only to ALTERNATIVES — the folders a config picks between,
            # which are exactly the ones pipeline_dir names. Folders with distinct
            # purposes (outcome/, pipeline/, 0-libs/) are not a sequence.
            alts = set()
            for c in job.glob("t0*/config/**/r*.do"):
                m = re.search(r'global pipeline_dir "src/([0-9A-Za-z_]+)"', c.read_text())
                if m: alts.add(m.group(1))
            unordered = sorted(a for a in alts if not re.match(r'^[0-9]', a))
            if len(alts) > 1 and unordered:
                bad("N4", job.name, f"alternatives are unordered: {', '.join(unordered)}")

            # S1 every do-path resolves from the JOB root (Stata's working directory)
            for f in job.rglob("*.do"):
                for i, l in enumerate(f.read_text(errors="replace").splitlines(), 1):
                    s = l.strip()
                    if s.startswith(("//","*")) or "display" in s: continue
                    for c in DO.findall(s):
                        if "${" in c or "`" in c: continue
                        if not (job/c).exists():
                            bad("S1", f"{f.relative_to(job)}:{i}", f"unresolved: {c}")

            # S2 ticket -> config, S3 config -> spine + step folder
            for k in (job.glob("t0*/runs/**/*.ps1")):
                txt = k.read_text()
                m = re.search(r'config[\\/]((?:\S+?[\\/])?\S+?\.do)"', txt)
                if not m: bad("S2", k.name, "ticket names no config"); continue
                task = k.parents[0]
                while task and task.name != "runs": task = task.parent
                task = task.parent
                if not (task/"config"/m.group(1).replace("\\","/")).exists():
                    bad("S2", k.name, f"config does not exist: {m.group(1)}")
            for c in job.glob("t0*/config/**/r*.do"):
                m = re.search(r'global pipeline_dir "src/([0-9a-z_]+)"', c.read_text())
                if not m: continue
                task = c.parent if c.parent.name == "config" else c.parent.parent
                task = task.parent
                if not (task/f"run_regression_pipeline_{m.group(1)}.do").exists():
                    bad("S3", c.name, f"no spine run_regression_pipeline_{m.group(1)}.do")
                if not (job/"src"/m.group(1)).is_dir():
                    bad("S3", c.name, f"no step folder src/{m.group(1)}")

            # S6 no file may RESTATE the tree. A list of every ticket duplicates
            # t*/runs/ and then has to be kept in step with it; the tree is the
            # list, and run_slice.ps1 -WhatIf prints it from disk.
            for f in (job/"sbatch").glob("*.ps1") if (job/"sbatch").is_dir() else []:
                if f.name == "run_slice.ps1": continue
                body = f.read_text()
                hits = len(re.findall(r'^\s*(Invoke-Run|&)\s+"[^"]*runs', body, re.M))
                if hits > 1:
                    bad("S6", f"{job.name}/sbatch/{f.name}",
                        f"restates the tree: names {hits} tickets. Delete it; run_slice.ps1 -WhatIf is the plan.")

            # S7 a job's sbatch must SAY whether its runs go one by one or several
            # at once. Sequential is not a safe default to assume: a job whose runs
            # overwrite each other and a job whose runs are independent look the
            # same from outside, so the job declares it and run_slice.ps1 enforces it.
            sb = job/"sbatch"
            if sb.is_dir():
                decl = sb/"batch.psd1"
                if not decl.is_file():
                    bad("S7", f"{job.name}/sbatch", "no batch.psd1: the job never says one-by-one or parallel")
                else:
                    d = decl.read_text()
                    got = dict(re.findall(r"^\s*(Mode|Ceiling|CollisionKey|Why)\s*=\s*'?([^'\n]+)'?", d, re.M))
                    for k in ("Mode","Ceiling","CollisionKey","Why"):
                        if k not in got: bad("S7", f"{job.name}/sbatch/batch.psd1", f"no {k}")
                    mode, ceil = got.get("Mode","").strip(), got.get("Ceiling","0").strip()
                    if mode not in ("sequential","parallel"):
                        bad("S7", f"{job.name}/sbatch/batch.psd1", f"Mode is '{mode}', not sequential or parallel")
                    elif mode == "sequential" and ceil != "1":
                        bad("S7", f"{job.name}/sbatch/batch.psd1", f"Mode=sequential but Ceiling={ceil}")
                    elif mode == "parallel" and ceil.isdigit() and int(ceil) < 2:
                        bad("S7", f"{job.name}/sbatch/batch.psd1", f"Mode=parallel but Ceiling={ceil}")
                    COORDS = {"Name","Task","Trait","Window","Family","Analysis","Year","Source"}
                    for k in [x.strip() for x in got.get("CollisionKey","").split(",") if x.strip()]:
                        if k not in COORDS:
                            bad("S7", f"{job.name}/sbatch/batch.psd1", f"CollisionKey names '{k}', not a ticket coordinate")

                # S9 a named entry point must forward its arguments BY NAME.
                # `@Rest` and `@args` splat an ARRAY, which PowerShell binds
                # positionally: every one of these files silently bound -WhatIf to
                # -Family and failed. $PSBoundParameters is a hashtable and binds
                # by name. Regenerate with _tools/write_pages.py rather than editing.
                for e in sorted(sb.glob("by_*/*.ps1")):
                    b = "\n".join(l for l in e.read_text().splitlines() if not l.lstrip().startswith("#"))
                    if re.search(r'@(Rest|args)\b', b):
                        bad("S9", f"{job.name}/sbatch/{e.parent.name}/{e.name}",
                            "forwards with an array splat (@Rest/@args): -WhatIf binds positionally to the next axis")
                    elif "@PSBoundParameters" not in b:
                        bad("S9", f"{job.name}/sbatch/{e.parent.name}/{e.name}",
                            "forwards nothing: filters cannot compose from here")

    # S8 a doc may not name a folder, ticket or script that does not exist. Every
    # rename in this tree so far left a page pointing at the old name, and a page
    # nobody can follow is worse than no page.
    live = set()
    for p in root.parent.rglob("*") if root.name.startswith("b") else root.rglob("*"):
        if any(x in p.parts for x in ("results", ".git")): continue
        live.add(p.name); live.add(p.stem)
    TOKEN = re.compile(r'\b([bjtr]\d\d_[A-Za-z0-9_]+|[a-z][a-z0-9_]*\.ps1)\b')
    for md in sorted(root.rglob("*.md")):
        if "results" in md.parts: continue
        for i, line in enumerate(md.read_text().splitlines(), 1):
            if "tasks/" in line: continue          # provenance, points at the OLD tree
            for tok in set(TOKEN.findall(line)):
                if tok in live or tok.rsplit(".",1)[0] in live: continue
                bad("S8", f"{md.relative_to(root.parent)}:{i}", f"names something that does not exist: {tok}")

    return F

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = pathlib.Path(args[0] if args else ".").resolve()
    if not root.is_dir(): print(f"not a directory: {root}"); return 2
    F = check(root)
    by = collections.Counter(c for c, _, _ in F)
    print(f"{root.name}: {len(F)} finding(s)")
    for code, where, msg in F[:60]:
        print(f"  {code}  {where}\n        {msg}")
    if len(F) > 60: print(f"  ... and {len(F)-60} more")
    if by: print("  " + " · ".join(f"{k}×{v}" for k, v in sorted(by.items())))
    if "--expect-fail" in sys.argv:
        ok = len(F) > 0
        print("EXPECT-FAIL: " + ("the checker fired, so it can fail" if ok else "IT DID NOT FIRE — not a gate"))
        return 0 if ok else 1
    return 1 if F else 0

if __name__ == "__main__":
    sys.exit(main())

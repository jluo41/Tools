#!/usr/bin/env python3
"""Check a block tree against the naming rules and the wiring it claims.

    python3 _tools/check_task_tree.py <block-or-tasks-dir> [--expect-fail]

Every rule is one this repo actually broke. Codes N* are naming, S* structural,
R* results/runs. The dialect-neutral rows (N9 R02 S11-S15 R01 R05, JL 260904)
are listed in ref/task-tree-checklist.md; the Stata rows (N2 N8 S1-S3 S7 S9)
fire only where .do/.ps1 files exist.
`--expect-fail` inverts the exit code: use it to prove the checker can fail
before trusting a pass (haipipe-task GATE-1).
"""
import pathlib, re, sys, collections

SHAPE = {"data","table","pipeline","analysis","pool","rank","set","list","baseline","scope","processing"}
IDX   = re.compile(r'^([bjtr])(\d\d)_(.+)$')
DO    = re.compile(r'\bdo\s+"([A-Za-z0-9_./${}`\'-]+\.do)"')


def cfgdir(task):
    """A task's config home. scripts/config/ since 260831; config/ was the old one,
    and is still READ so a half-migrated tree reports the real finding, not a
    missing folder."""
    return task/"scripts"/"config" if (task/"scripts"/"config").is_dir() else task/"config"


def codedir(job):
    """The JOB's SHARED code folder. Two words on purpose (JL 260831): `src/` is
    shared by every task in the job, `scripts/` is one task's own, and the name is
    what tells them apart without reading the path."""
    return job/"src"

def rows(root):
    for block in sorted(p for p in ([root] if root.name.startswith("b") else root.iterdir()) if p.is_dir()):
        if not block.name.startswith("b"): continue
        yield block

def check(root):
    F = []
    def bad(code, where, msg): F.append((code, str(where), msg))

    # N0 a tree with folders but no bNN_ block is not in the grammar at all; every
    # other row keys on blocks, so without this the pre-BJTR tree passes silently.
    if not root.name.startswith("b"):
        kids = [p for p in root.iterdir() if p.is_dir() and not p.name.startswith((".", "_"))]
        if kids and not any(p.name.startswith("b") and IDX.match(p.name) for p in kids):
            bad("N0", root.name, f"no bNN_ block under the root; {len(kids)} folders ({', '.join(k.name for k in kids[:4])}…) are not in the grammar")

    for block in rows(root):
        jobs = [p for p in sorted(block.iterdir()) if p.is_dir() and p.name.startswith("j")]
        # S18 a canonical nested Block is also a Task Block Board. Legacy flat
        # blocks remain readable, but the b/j/t tree must expose its one Board
        # head and opt in explicitly so generic Boards never adopt tNN files.
        nested_tasks = any(
            p.is_dir() and p.name.startswith("t")
            for job in jobs
            for p in job.iterdir()
        )
        if nested_tasks:
            head = block / "board.md"
            if not head.is_file():
                bad("S18", block.name, "canonical Block has no board.md Task Block Board head")
            elif not re.search(r'^board-kind:\s*task-block\s*$', head.read_text(errors="replace"), re.M):
                bad("S18", f"{block.name}/board.md", "missing exact `board-kind: task-block`")
        for lvl, p in [("b", block)] + [("j", j) for j in jobs]:
            m = IDX.match(p.name)
            if not m or m.group(1) != lvl:
                bad("N1", p.name, f"does not match <{lvl}>NN_<name>")
                continue
            words = m.group(3).split("_")
            if all(w in SHAPE or w.isdigit() or len(w) <= 2 for w in words):
                bad("N5", p.name, "shape words only; says no concrete thing")
            if lvl == "j" and len(words) < 2:
                bad("N1", p.name, "a job name must stand alone: <noun>_<qualifier> (R1)")

        for job in jobs:
            tasks = [p for p in sorted(job.iterdir()) if p.is_dir() and p.name.startswith("t")]
            for t in tasks:
                m = IDX.match(t.name)
                if not m or m.group(1) != "t":
                    bad("N1", t.name, "does not match tNN_<name>"); continue
                if not re.match(r'^[A-Z]', m.group(3)) and "_" not in m.group(3):
                    bad("N5", t.name, "task name carries no subject")
                if not (t/f"{t.name}.md").exists():
                    bad("S5", t.name, "no task page")

                # S10 the two-word law (JL 260831): `src/` is the JOB's shared
                # code, `scripts/` is the TASK's own. Either word at the wrong
                # level makes a reader walk the path to learn what a folder is,
                # which is the whole thing the two words exist to prevent.
                if (t/"src").is_dir():
                    bad("S10", t.name, "task holds src/; a task's own code is scripts/")
                if (t/"config").is_dir() and (t/"scripts").is_dir():
                    bad("S10", t.name, "config/ at the task root; it belongs inside scripts/")

                cfg_dir = cfgdir(t)
                shared = [c for c in cfg_dir.glob("*.do") if not c.name.startswith("r")] if cfg_dir.is_dir() else []
                if cfg_dir.is_dir() and any(cfg_dir.glob("*.do")) and len(shared) != 1:   # Stata dialect only
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

            if (job/"scripts").is_dir():
                bad("S10", job.name, "job holds scripts/; a job's shared code is src/")

            # N4 applies only to ALTERNATIVES — the folders a config picks between,
            # which are exactly the ones pipeline_dir names. Folders with distinct
            # purposes (outcome/, pipeline/, 0-libs/) are not a sequence.
            alts = set()
            for c in list(job.glob("t0*/scripts/config/**/r*.do")) + list(job.glob("t0*/config/**/r*.do")):
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
                if not (cfgdir(task)/m.group(1).replace("\\","/")).exists():
                    bad("S2", k.name, f"config does not exist: {m.group(1)}")
            for c in list(job.glob("t0*/scripts/config/**/r*.do")) + list(job.glob("t0*/config/**/r*.do")):
                m = re.search(r'global pipeline_dir "src/([0-9a-z_]+)"', c.read_text())
                if not m: continue
                task = c.parent
                while task.name not in ("config",): task = task.parent
                task = task.parent                       # scripts/ or the task itself
                if task.name == "scripts": task = task.parent
                if not (task/"scripts"/f"run_regression_pipeline_{m.group(1)}.do").exists() \
                   and not (task/f"run_regression_pipeline_{m.group(1)}.do").exists():
                    bad("S3", c.name, f"no spine run_regression_pipeline_{m.group(1)}.do")
                if not (codedir(job)/m.group(1)).is_dir():
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
            if sb.is_dir() and any(sb.glob("*.ps1")):          # the PowerShell dialect declares in batch.psd1; a bash driver states its mode in its header
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
    TOKEN = re.compile(r'\b([bjtr]\d\d_[A-Za-z0-9_][A-Za-z0-9_.-]*[A-Za-z0-9_]|[a-z][a-z0-9_]*\.ps1)\b')   # a stem may carry - and . (r01_v2026-07)
    # `<!-- s8-skip -->` on its own line exempts the NEXT fenced block, for the one
    # honest case: a snippet whose whole point is to CREATE the files it names.
    for md in sorted(root.rglob("*.md")):
        if "results" in md.parts: continue
        armed = skip = False
        for i, line in enumerate(md.read_text().splitlines(), 1):
            if line.strip() == "<!-- s8-skip -->": armed = True; continue
            if line.lstrip().startswith("```"):
                if armed: skip, armed = True, False
                elif skip: skip = False
                continue
            if skip: continue
            if "tasks/" in line: continue          # provenance, points at the OLD tree
            for tok in set(TOKEN.findall(line)):
                if tok in live or tok.rsplit(".",1)[0] in live: continue
                bad("S8", f"{md.relative_to(root.parent)}:{i}", f"names something that does not exist: {tok}")


    # ── dialect-neutral rows of ref/task-tree-checklist.md (JL 260904) ──────────
    # Every one of these is a thing the 260904 PhyReview restructure shipped
    # broken and no code above caught: no runs/ in 19 tasks, tickets off the
    # rNN_ grammar, batchers in runs/, results inside tasks, configs/ at task
    # roots, parents[N] root walks, and a store folder named after the ticket.
    TICKET = re.compile(r'^r\d\d_')
    for block in rows(root):
        for job in (p for p in sorted(block.iterdir()) if p.is_dir() and p.name.startswith("j")):
            tasks = [p for p in sorted(job.iterdir()) if p.is_dir() and p.name.startswith("t")]
            names = {t.name for t in tasks}
            # S17 every job shows its src/ slot, even empty (JL 260904: a .gitkeep that
            # says whose shared code belongs there, so a reader sees the job's shape;
            # results/ is generated and is never pre-created)
            if not (job/"src").is_dir():
                bad("S17", job.name, "no src/; add src/.gitkeep naming the job's shared-code slot")
            # R01 / R05 results at the job level pair with a task and carry a receipt
            if (job/"results").is_dir():
                for d in sorted(p for p in (job/"results").iterdir() if p.is_dir()):
                    if d.name not in names:
                        bad("R05", f"{job.name}/results/{d.name}", "no such task in this job"); continue
                    for run in sorted(p for p in d.iterdir() if p.is_dir()):
                        if not (run/"runtime.yaml").is_file():
                            bad("R01", f"{job.name}/results/{d.name}/{run.name}", "results folder without runtime.yaml")
            for t in tasks:
                runs = t/"runs"
                tickets = sorted(p for p in runs.glob("*") if p.is_file() and p.suffix in (".sh", ".ps1")) if runs.is_dir() else []
                if not any(TICKET.match(p.stem) for p in tickets):
                    bad("R02", t.name, "no runs/ ticket in rNN_ grammar: every task owes at least one")
                for k in tickets:
                    if not TICKET.match(k.stem):
                        bad("N9", f"{t.name}/runs/{k.name}", "ticket not rNN_<stem>")
                    elif k.stem[4:].startswith("run_"):
                        bad("N9", f"{t.name}/runs/{k.name}", "stem repeats run_ after the rNN_ prefix")
                    body = k.read_text(errors="replace")
                    if re.search(r'\bbash\s+"?[^"\n]*runs/', body):
                        bad("S11", f"{t.name}/runs/{k.name}", "calls other tickets: a batcher belongs in sbatch/")
                if (t/"results").is_dir():
                    bad("S12", t.name, "results/ inside the task; the law is <job>/results/<task>/<run>/")
                if (t/"configs").is_dir():
                    bad("S14", t.name, "configs/ at the task root; config lives in scripts/config/")
                # N7 for yaml dialects: rNN_ configs <-> rNN_ tickets
                cfgd = t/"scripts"/"config"
                runcfg = {c.stem for c in cfgd.glob("r[0-9][0-9]_*.y*ml")} if cfgd.is_dir() else set()
                tk = {k.stem for k in tickets if TICKET.match(k.stem)}
                for stem in sorted(runcfg - tk):
                    bad("N7", f"{t.name}/{stem}", "config has no ticket of the same stem")
                if runcfg:
                    for stem in sorted(tk - runcfg):
                        bad("N7", f"{t.name}/{stem}", "ticket has no config of the same stem (this task uses configs)")
                # code-level rows
                for py in sorted((t/"scripts").glob("*.py")) if (t/"scripts").is_dir() else []:
                    for i, l in enumerate(py.read_text(errors="replace").splitlines(), 1):
                        if l.lstrip().startswith("#"): continue
                        if re.search(r'^\s*(WS_ROOT|WS|REPO_ROOT|ROOT|STORE|ENTRY)\s*=.*\.parents\[\d+\]', l):
                            bad("S13", f"{t.name}/scripts/{py.name}:{i}", "root by parents[N]; use the marker walk (pyproject.toml + code/)")
                        if re.search(r'(TASK_DIR|TASK|HERE\.parent|HERE\.parents\[1\])\s*/\s*"results"', l):
                            bad("S12", f"{t.name}/scripts/{py.name}:{i}", "writes results inside the task")
                        if '"configs"' in l:
                            bad("S14", f"{t.name}/scripts/{py.name}:{i}", 'reads "configs"; config lives in scripts/config/')
                        if re.search(r'(run_name|RUN_NAME)', l) and re.search(r'cfg\["output"\]|"@review"|"@platforms"', l) and "chunk_dir" not in l:
                            bad("S15", f"{t.name}/scripts/{py.name}:{i}", "a store path derived from the ticket's name; pin it in config (chunk_dir:)")

    # S16 a script, config or ticket names a tasks/… path that does not exist. The
    # 260904 restructure left 18 of these: two hardcoded config paths (live breaks),
    # three config keys pointing at old results, and `producer:` strings that would
    # have written the OLD address into store manifests on the next run. Comments are
    # skipped; docstrings and strings are not, because a README writer reads them.
    proj = root.parent if not root.name.startswith("b") else root.parent.parent
    TP = re.compile(r"tasks/((?:[bjt]\d\d_|[A-Z]\d\d_)[A-Za-z0-9_][A-Za-z0-9_.\-/]*)")
    for f in sorted(root.rglob("*")):
        if not f.is_file() or f.suffix not in (".py", ".yaml", ".yml", ".sh") or "results" in f.parts or "_retired" in f.parts: continue
        for i, l in enumerate(f.read_text(errors="replace").splitlines(), 1):
            if l.lstrip().startswith("#") or "tasks.old/" in l: continue
            for m in TP.finditer(l):
                rel = m.group(1).rstrip("/.,;:)\"'`")
                if "<" in rel or "*" in rel or "$" in rel or "{" in rel or "/results/" in rel or rel.endswith("/results"): continue   # generated paths: R01/R05 own them
                if not (proj / "tasks" / rel).exists():
                    bad("S16", f"{f.relative_to(root)}:{i}", f"names tasks/{rel}, which does not exist")

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

#!/usr/bin/env python3
"""Mechanical pre-upload sweep. Every check is a bug class this tree actually had."""
import pathlib, re, sys, collections
ROOT = pathlib.Path(sys.argv[1]).resolve()
F = []
def bad(code, where, msg): F.append((code, str(where), msg))

jobs = sorted(p for p in ROOT.glob("b0*/j*") if p.is_dir())

# --- M1 non-ASCII (server rejects; old tree has ZERO) -------------------------
for f in ROOT.rglob("*"):
    if not f.is_file() or "__pycache__" in f.parts: continue
    if f.suffix not in {".do",".ps1",".psd1"}: continue  # executables only; docs are not parsed by Stata/PowerShell
    try: t = f.read_text(encoding="utf-8")
    except Exception: continue
    for i, line in enumerate(t.split("\n"), 1):
        for ch in line:
            if ord(ch) > 127:
                bad("M1", f"{f.relative_to(ROOT)}:{i}", f"non-ASCII U+{ord(ch):04X} {ch!r}"); break

# --- M2 a PowerShell function CALLED but never DEFINED ------------------------
for ps in ROOT.rglob("*.ps1"):
    t = ps.read_text(encoding="utf-8", errors="replace")
    defined = set(m.lower() for m in re.findall(r'^\s*function\s+([A-Za-z][\w-]*)', t, re.M))
    called  = set(m.lower() for m in re.findall(r'^\s*([A-Z][a-z]+-[A-Z][\w]*)\s', t, re.M))
    BUILTIN = {w.lower() for w in """Write-Host Write-Error Write-Output Write-Warning Write-Verbose
        Join-Path Split-Path Test-Path Resolve-Path New-Item Remove-Item Copy-Item Move-Item Get-Item
        Get-ChildItem Get-Content Set-Content Add-Content Out-Null Out-File Start-Process Wait-Process
        Stop-Process Get-Process Select-String Sort-Object Where-Object ForEach-Object Select-Object
        Measure-Object Import-PowerShellDataFile ConvertTo-Json ConvertFrom-Json New-Object Get-Date
        Set-Location Push-Location Pop-Location Invoke-Expression Get-Command Start-Sleep Group-Object
        Write-Progress Get-Location Test-Connection Format-Table Export-Csv Import-Csv Compare-Object""".split()}
    for c in sorted(called - defined - BUILTIN):
        bad("M2", ps.relative_to(ROOT), f"calls {c} but nothing defines it here")

# --- M3 cross-cohort contamination -------------------------------------------
CC = set("""alzh alzh_demen ami anemia asthma atrial_fib cataract chf chronickidney copd
    depression diabetes glaucoma hip_fracture hyperl hyperp hypert ischemicheart osteoporosis
    ra_oa stroke_tia cancer_breast cancer_colorectal cancer_lung cancer_prostate cancer_endometrial""".split())

TOK = {"pain":["lbp","opioid","cancer","headache","musc","osteo"],
       "diabetes":["t2d","diabetes"], "cardiac":["ami","cabg"]}
for job in jobs:
    mine = next((k for k in TOK if k in job.parent.name or k in job.name), None)
    if not mine: continue
    foreign = {t for k,v in TOK.items() if k != mine for t in v}
    for f in list(job.rglob("*.do")) + list(job.rglob("*.ps1")):
        if "__pycache__" in f.parts: continue
        raw = f.read_text(encoding="utf-8", errors="replace")
        raw = re.sub(r'/\*.*?\*/', ' ', raw, flags=re.S)          # Stata block comment
        code = []
        for ln in raw.split("\n"):
            st = ln.strip()
            if st.startswith("//") or st.startswith("*") or st.startswith("#"): continue
            ln = re.sub(r'//.*$', '', ln)                          # Stata trailing
            if f.suffix == ".ps1": ln = re.sub(r'#.*$', '', ln)    # PowerShell trailing
            code.append(ln)
        t = "\n".join(code).lower()
        for tok in sorted(foreign):
            hit = next((l for l in t.split("\n") if re.search(rf'\b{tok}\b', l)), None)
            if hit is None: continue
            # `ami`, `cancer` and `diabetes` are also CMS Chronic Conditions Warehouse
            # FLAG names. A line listing several CC flags is a covariate list, not a
            # cohort reference, so it is not contamination.
            if sum(1 for cc in CC if re.search(rf'\b{cc}\b', hit)) >= 3: continue
            # `exclude_<x>` / `has_<x>` are EXCLUSION CRITERIA and comorbidity flags,
            # applied by every cohort. Naming one is not a cohort reference.
            if re.search(rf'\b(exclude|has|flag|any)[ _]{tok}\b', hit): continue
            bad("M3", f.relative_to(ROOT), f"CODE names foreign cohort '{tok}' (job is {mine}): {hit.strip()[:90]}")
            break

# --- M4 every sbatch/ declares its execution mode -----------------------------
for job in jobs:
    sb = job/"sbatch"
    if not sb.is_dir(): continue
    d = sb/"batch.psd1"
    if not d.exists(): bad("M4", job.relative_to(ROOT), "sbatch/ with no batch.psd1 declaring Mode"); continue
    t = d.read_text(encoding="utf-8", errors="replace")
    for key in ("Mode","Ceiling","CollisionKey","Why"):
        if not re.search(rf'\b{key}\s*=', t): bad("M4", d.relative_to(ROOT), f"batch.psd1 declares no {key}")
    m = re.search(r"Mode\s*=\s*'(\w+)'", t)
    if m and m.group(1) not in ("sequential","parallel"):
        bad("M4", d.relative_to(ROOT), f"Mode is '{m.group(1)}', not sequential|parallel")

# --- M5 a .ps1 naming a file that does not exist relative to the job ----------
for job in jobs:
    for ps in job.rglob("*.ps1"):
        t = ps.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r'do ([A-Za-z0-9_/]+\.do)', t):
            if not (job/m.group(1)).exists():
                bad("M5", f"{ps.relative_to(ROOT)}", f"builds `do {m.group(1)}` but no such file under the job root")

# --- M6 a `do "..."` path ANYWHERE, comment included, that cannot resolve ------
# A stale path in a comment is how the next author learns the wrong thing. Both
# C jobs inherited `do "../0-libs/config-defaults.do"` verbatim from the old tree,
# where it resolved; under the new layout it names nothing.
DO_Q = re.compile(r'\bdo\s+"([A-Za-z0-9_./${}`\'-]+\.do)"')      # quoted: anywhere
DO_U = re.compile(r'^\s*do\s+([A-Za-z0-9_./${}`\'-]+\.do)\s*$')          # bare: statement start only
for job in jobs:
    for f in job.rglob("*.do"):
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").split("\n"), 1):
            for m in list(DO_Q.finditer(line)) + list(DO_U.finditer(line)):
                c = m.group(1)
                if "${" in c or "`" in c: continue          # dynamic, cannot be checked
                if (job/c).exists(): continue
                kind = "COMMENT" if line.strip().startswith(("//","*")) else "CODE"
                bad("M6", f"{f.relative_to(ROOT)}:{i}", f'{kind} `do "{c}"` does not resolve from the job root')

# --- M7 a do-path built from the `task' macro -------------------------------
# THE ONE THAT GOT THROUGH. `task' is arg 1 of every dispatcher and expands to a
# tNN_ folder name, so the path IS checkable: substitute each real task and test.
# Skipping it as "dynamic" is how 16 broken paths across 5 jobs reached a review
# that declared two of those jobs safe. Every step of every run would have died
# at Stata r(601) before touching data.
TASKDO = re.compile('do\\s+"`task\'([^"]*)"')
for job in jobs:
    tasks = sorted(p.name for p in job.iterdir() if p.is_dir() and p.name.startswith("t"))
    if not tasks: continue
    for f in job.rglob("*.do"):
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").split("\n"), 1):
            if line.strip().startswith(("//", "*")): continue
            for m in TASKDO.finditer(line):
                # drop the trailing macro segment; what remains must exist under each task
                probe = re.sub(r"`[a-z_]+'", "", m.group(1)).strip("/")
                if not probe: continue
                for t in tasks:
                    if not (job/t/probe).exists():
                        bad("M7", f"{f.relative_to(ROOT)}:{i}",
                            f"`task\'/{probe} does not exist for {t}")

# --- M9 lives in check_unassigned_vars.ps1, not here ------------------------
# A regex cannot tell a function parameter from a script variable, and the
# attempt produced 105 false positives against 0 real ones. PowerShell's own
# AST parser knows both, so that check runs there:
#     pwsh -NoProfile -File _tools/check_unassigned_vars.ps1 -Root .
# It also reports a PARSE-ERROR per file, which is a free syntax gate.

# --- M10 shared copies must stay byte-identical -------------------------------
# 141 .do files are copies of one shared source. The old tree kept them in step
# with tasks/_tools/sync_shared.py, which regenerated them from a template. That
# generator does not exist here and its template is in the tree being retired, so
# the 141 banners pointed at a script nobody could run. What the generator actually
# BOUGHT was "these copies never drift", and that is checkable directly.
import hashlib, collections as _c
groups = _c.defaultdict(list)
for f in ROOT.rglob("*.do"):
    if "__pycache__" in f.parts: continue
    if "SHARED COPY" in f.read_text(errors="replace")[:400]:
        groups[f.name].append(f)
for name, ps in sorted(groups.items()):
    if len(ps) < 2: continue
    h = {hashlib.sha256(q.read_bytes()).hexdigest(): q for q in ps}
    if len(h) > 1:
        bad("M10", name, f"{len(ps)} copies have DIVERGED into {len(h)} versions: "
                         + ", ".join(str(q.relative_to(ROOT)) for q in list(h.values())[:3]))

print(f"swept {len(jobs)} jobs")
if not F: print("0 findings"); sys.exit(0)
for code, where, msg in sorted(F): print(f"  {code}  {where}\n        {msg}")
c = collections.Counter(x[0] for x in F)
print("\n" + " · ".join(f"{k}x{v}" for k,v in sorted(c.items())) + f"   TOTAL {len(F)}")
sys.exit(1)

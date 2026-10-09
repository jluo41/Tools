"""Facts about the Project tree, read from disk each time: the b03 drawings never type a number.

    scan()            per Theme: Block name shapes, Jobs, Tasks, Run tickets, receipts whose run: = stem
    audit_all()       today's audit_projects.py over every examples* world, one row per project
    receipt_excerpt() a few lines of one real Run's runtime.yaml
"""
import glob
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

BLOCK = Path(__file__).resolve().parents[2]          # Tools/blueprints/b03_project_workbench
SPACE = BLOCK.parents[2]                              # b03_project_workbench · designs · Tools · SPACE
AUDIT = SPACE / "Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-project/scripts/audit_projects.py"
EXAMPLE_RUN = ("examples-1-data/Project-Data-DrFirst-Raw2AIData/tasks/b02_A_sms_recordstore/"
               "j58_opttimer1extended_v260923_record/t01_recordstore_materialize")
SKIP = {"_legacy", "_old", "_archive", "_backup", "__pycache__"}
THEMES = ["tasks", "discoveries", "cowork", "papers", "insights", "designs"]


def subdirs(p):
    if not p.is_dir():
        return []
    return sorted(d for d in p.iterdir() if d.is_dir() and d.name not in SKIP and not d.name.startswith("."))


def projects():
    return sorted(Path(p) for p in glob.glob(str(SPACE / "examples*/*/")) if "_backup" not in p)


def shape(name):
    """The naming shape of a Block folder, so the grid shows which convention each Theme uses."""
    for pat, s in [(r"^b\d\d_", "bNN_"), (r"^([A-Z])\d\d_", r"\1NN_"), (r"^Prototype-Insight-", "Prototype-*"),
                   (r"^Instance-Insight-", "Instance-*"), (r"-InsightBoard$", "*-InsightBoard"),
                   (r"^Paper-", "Paper-*"), (r"^[A-Z]_[a-z]+$", "D_/I_/K_")]:
        m = re.search(pat, name)
        if m:
            return m.expand(s) if "\\" in s else s
    return name


def scan():
    rows = {}
    projs = projects()
    for theme in THEMES:
        r = dict(projects=0, shapes=Counter(), off=[], jobs=0, tasks=0, tickets=0, ext=set(), beside=0,
                 receipts=0, match=0, mismatch=0, noid=0, example=None, mismatches=[], per_project=Counter())
        for pr in projs:
            if (pr / theme).is_dir():
                r["projects"] += 1
            for b in subdirs(pr / theme):
                s = shape(b.name)
                r["shapes"][s] += 1
                if s != "bNN_":
                    r["off"].append(b.name)
                for j in subdirs(b):
                    if re.match(r"j\d\d_", j.name):
                        r["jobs"] += 1
                        r["tasks"] += sum(1 for t in subdirs(j) if re.match(r"t\d\d_", t.name))
                for runs in b.rglob("runs"):
                    if SKIP & set(runs.parts) or not runs.is_dir():
                        continue
                    for t in runs.iterdir():
                        if t.is_file() and not t.name.startswith(("_", ".")):
                            r["tickets"] += 1
                            r["per_project"][pr.name] += 1
                            r["ext"].add(t.suffix)
                            r["beside"] += (runs.parent / "results" / t.stem).is_dir()
                for rt in b.rglob("results/*/runtime.yaml"):
                    if SKIP & set(rt.parts):
                        continue
                    r["receipts"] += 1
                    m = re.search(r"^run:\s*(\S+)", rt.read_text(errors="ignore"), re.M)
                    if not m:
                        r["noid"] += 1
                    elif m.group(1).strip("\"'") == rt.parent.name:
                        r["match"] += 1
                    else:
                        r["mismatch"] += 1
                        r["example"] = r["example"] or (rt.parent.name, m.group(1).strip("\"'"))
                        r["mismatches"].append((rt.parent.name, m.group(1).strip("\"'")))
        rows[theme] = r
    return rows, len(projs)


def audit_all():
    """Run today's checker over every examples* world; one row per project."""
    out = []
    for root in sorted(glob.glob(str(SPACE / "examples*"))):
        res = subprocess.run([sys.executable, str(AUDIT), "--all", "--root", root], capture_output=True, text=True)
        for ln in res.stdout.splitlines():
            parts = ln.split("\t")
            if len(parts) >= 6:
                out.append(parts[:6])
    return out


def receipt_excerpt():
    rt = SPACE / EXAMPLE_RUN / "results/r01_materialize/runtime.yaml"
    keep = ["run", "operation", "status", "ticket", "finished_at", "address_readable"]
    vals = dict(re.findall(r"^(\w+):\s*(.*)$", rt.read_text(), re.M))
    return [(k, vals.get(k, "")) for k in keep]


def chain(theme):
    """One real path from a Project down to a Run ticket in this Theme, and what its Result holds."""
    for pr in projects():
        for b in subdirs(pr / theme):
            for runs in sorted(b.rglob("runs")):
                if SKIP & set(runs.parts) or not runs.is_dir():
                    continue
                tickets = sorted(t for t in runs.iterdir() if t.is_file() and not t.name.startswith(("_", ".")))
                if not tickets:
                    continue
                t = tickets[0]
                res = runs.parent / "results" / t.stem
                rt = res / "runtime.yaml"
                vals = dict(re.findall(r"^(\w+):\s*(.*)$", rt.read_text(errors="ignore"), re.M)) if rt.is_file() else {}
                parts = runs.parent.relative_to(pr).parts
                return dict(project=pr.name, world=pr.parent.name, parts=parts, ticket=t.name, n_tickets=len(tickets),
                            result=res.is_dir(), files=sorted(f.name for f in res.iterdir())[:6] if res.is_dir() else [],
                            run=vals.get("run"), status=vals.get("status"))
    return None


def questions():
    """The Block's Question register from board.md (id, title, hypothesis, ...)."""
    import yaml
    body = re.search(r"## Questions\s*\n+```yaml\n(.*?)\n```", (BLOCK / "board.md").read_text(), re.S).group(1)
    return yaml.safe_load(body)["questions"] or []

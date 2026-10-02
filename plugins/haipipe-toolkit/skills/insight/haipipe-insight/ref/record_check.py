"""record_check.py <page folder> <VERDICT> <review file> · record an independent page CHECK.

The check agent is read-only; the coordinator records its verdict here
(ref/prototype-contract.md § Status is computed). It opens a check Run with
haipipe-page's page.py, appends the review verbatim under its VERDICT line,
closes the Run, and on CLOSE approves the current plan, promoting a v0 plan to
v1.0 (a v0 plan cannot be approved). The cell's ✅ is then computed by
haipipe-insight-check ref/check_instance.py; nothing here writes a status.

VERDICT is CLOSE, CONTENT, OUTLINE, EVIDENCE or CONTEXT.
"""
import datetime
import re
import subprocess
import sys
from pathlib import Path

VERDICTS = {"CLOSE", "CONTENT", "OUTLINE", "EVIDENCE", "CONTEXT"}


def space_root(start):
    p = Path(start).resolve()
    while p != p.parent and not (p / "env.sh").is_file():
        p = p.parent
    return p


def approve(page, run):
    stem = page.name
    plans = sorted((page / "draft").glob(f"{stem}-draft-v*.md"))
    if len(plans) != 1:
        raise SystemExit(f"{stem}: expected one current plan in draft/, found {len(plans)}")
    plan = plans[0]
    s = plan.read_text(encoding="utf-8")
    old = re.search(r"(?m)^draft-version:\s*(v\S+)", s).group(1)
    if old.startswith("v0"):
        s = re.sub(r"(?m)^# (.*) · draft v\S+$", r"# \1 · draft v1.0", s, count=1)
        s = re.sub(r"(?m)^draft-version:.*$", "draft-version: v1.0", s, count=1)
        s = re.sub(r"(?m)^supersedes:.*$", f"supersedes: {old}", s, count=1)
        (page / "draft" / "previous").mkdir(exist_ok=True)
        plan.rename(page / "draft" / "previous" / plan.name)
        plan = page / "draft" / f"{stem}-draft-v1.0.md"
        items = page / "draft" / f"{stem}-evidence-items.md"
        if items.is_file():
            t = items.read_text(encoding="utf-8")
            items.write_text(re.sub(r"(?m)^plan: .*$", f"plan: draft/{plan.name} · v1.0", t, count=1), encoding="utf-8")
    today = datetime.date.today().strftime("%y%m%d")
    plan.write_text(re.sub(r"(?m)^approved:.*$", f"approved: ✅ {today} · CHECK {run}", s, count=1), encoding="utf-8")
    return plan.name


def record(page, verdict, review):
    page = Path(page).resolve()
    if verdict not in VERDICTS:
        raise SystemExit(f"VERDICT is one of {', '.join(sorted(VERDICTS))}")
    root = space_root(page)
    cli = [str(root / ".venv/bin/python"), str(root / "Tools/plugins/haipipe-toolkit/skills/page/haipipe-page/cli/page.py")]
    before = set((page / "runs").glob("run-check-*.md"))
    subprocess.run(cli + ["open-run", str(page), "--kind", "check", "--slug", "page check", "--target", "C1",
                          "--by", "check agent", "--goal", "independent CHECK of the current draft"],
                   check=True, capture_output=True)
    new = sorted(set((page / "runs").glob("run-check-*.md")) - before)
    if len(new) != 1:
        raise SystemExit(f"{page.name}: page.py open-run made {len(new)} check runs, not one")
    run = new[0].stem
    with open(new[0], "a", encoding="utf-8") as f:
        f.write(f"\n## Review (independent check agent, recorded by the coordinator)\n\nVERDICT: {verdict}\n\n"
                f"{review.strip()}\n")
    subprocess.run(cli + ["close-run", str(page), run, "--by", "check agent", "--summary", verdict],
                   check=True, capture_output=True)
    plan = approve(page, run) if verdict == "CLOSE" else None
    print(f"{page.name}: {run} closed · {verdict}" + (f" · plan {plan} approved" if plan else ""))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    record(sys.argv[1], sys.argv[2], Path(sys.argv[3]).read_text(encoding="utf-8"))

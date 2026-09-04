#!/usr/bin/env python3
"""outline-pass.py · the mechanical half of one OUTLINE pass, in one command.

    python3 cli/outline-pass.py <page>.md            run everything, print the receipt-lite
    python3 cli/outline-pass.py <page>.md --no-build skip the board rebuild

haipipe-page-outline §①: regenerate the three derived files (requirement,
feedback, evidence), run the plan checks for THIS page (hard: any ❌ exits 1),
run cli/check.py scoped to the page, rebuild the board, and print what the
pass must read before writing a bullet. It writes no plan, no thread and no
log record: those are the phase's own pen.
"""
import argparse, importlib.util, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent            # cli/
BOARD_SKILL = HERE.parent                         # haipipe-board/
sys.path.insert(0, str(BOARD_SKILL))
from src.plan_shape import (check as plan_shape_check, check_serves,      # noqa: E402
                            check_bullet_grammar, check_head_style,
                            check_note_quotes_page, check_coverage)

SKILLS = BOARD_SKILL.parent.parent                # skills/


def _run(cmd, cwd=None):
    r = subprocess.run([sys.executable] + cmd, cwd=cwd, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def _board_of(page: Path) -> Path:
    d = page.parent
    while d != d.parent:
        if (d / "board.md").is_file():
            return d
        d = d.parent
    raise SystemExit(f"no board.md above {page}")


def _latest_plan(page: Path):
    o = page.parent / "outline"
    plans = sorted(o.glob(f"{page.stem}-outline-v*.md"),
                   key=lambda p: int(re.search(r"-v(\d+)\.md$", p.name).group(1))
                   if re.search(r"-v(\d+)\.md$", p.name) else 0) if o.is_dir() else []
    return plans[-1] if plans else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("--no-build", action="store_true")
    a = ap.parse_args()
    page = Path(a.page).resolve()
    if not page.is_file():
        raise SystemExit(f"not a page: {page}")
    board = _board_of(page)
    stem = page.stem
    o = page.parent / "outline"
    out = []

    # ① the three derived files, regenerated whole
    for script, label in (("requirement.py", "requirement"), ("feedback.py", "feedback"),
                          ("evidence-status.py", "evidence")):
        cmd = [str(HERE / script)] + (["collect"] if script == "feedback.py" else []) + [str(page)]
        rc, txt = _run(cmd)
        out.append((label, rc, txt.splitlines()[-1] if txt else ""))

    # ② what the pass must READ, in one screen
    print(f"OUTLINE pass · {stem} · board {board.name}")
    req = o / f"{stem}-requirement.md"
    if req.is_file():
        heads = re.findall(r"(?m)^### (V\d) · (.+)$", req.read_text(encoding="utf-8", errors="replace"))
        print("requirement  " + " · ".join(f"{v} {h[:40]}" for v, h in heads) if heads else "requirement  (no venue division bound)")
    else:
        print("requirement  none (no structure-source:)")
    fb = o / f"{stem}-feedback.md"
    if fb.is_file():
        m = re.search(r"(?m)^status:\s*(.+)$", fb.read_text(encoding="utf-8", errors="replace"))
        print("feedback     " + (m.group(1).strip() if m else "(no status line)"))
    else:
        print("feedback     none routed")
    ev = o / f"{stem}-evidence.md"
    if ev.is_file():
        m = re.search(r"(?m)^plan:.*?· (cycle: .+)$", ev.read_text(encoding="utf-8", errors="replace"))
        print("evidence     " + (m.group(1) if m else "(no plan line)"))

    # ③ the plan checks, HARD for this page
    plan = _latest_plan(page)
    fails, gaps = [], []
    if plan is None:
        print("plan         none yet: write outline/<stem>-outline-v1.md from ref/plan-grammar.md")
    else:
        txt = plan.read_text(encoding="utf-8", errors="replace")
        tick = "✅" if re.search(r"(?m)^approved:\s*✅", txt) else "⬜"
        arc = bool(re.search(r"(?m)^arc:\s*\S", txt))
        fails += [f"plan-shape-off-type: {m}" for m in plan_shape_check(page, txt, SKILLS)]
        fails += [f"serves-address-stale: {m}" for m in check_serves(page, txt)]
        fails += [f"bullet-missing-note: {m}" for m in check_bullet_grammar(txt)]
        hf, hg = check_head_style(txt)
        fails += hf + hg                                   # hard here, gaps board-wide
        fails += check_note_quotes_page(page, txt)
        if not arc:
            fails.append("plan-no-arc: no `arc:` line")
        gaps += check_coverage(page, txt)
        print(f"plan         {plan.name} · approved {tick} · checks {'✅ 0 ❌' if not fails else f'❌ {len(fails)}'} · coverage gaps {len(gaps)}")
        for f in fails[:20]:
            print("   ❌", f)
        for g in gaps[:8]:
            print("   🔎", g)
        if len(gaps) > 8:
            print(f"   🔎 … {len(gaps) - 8} more")

    # ④ the page-scoped checker + the build
    rc, txt = _run([str(HERE / "check.py"), str(board)])
    mine = [ln for ln in txt.splitlines() if stem in ln and ("WARN" in ln or "ERROR" in ln)]
    print(f"check.py     {len(mine)} finding(s) on {stem}" + (": " + " · ".join(re.sub(r'\s+', ' ', l)[:70] for l in mine[:4]) if mine else ""))
    if not a.no_build:
        rc, txt = _run([str(HERE / "build.py"), str(board)])
        print("build        " + ("ok" if rc == 0 else f"rc {rc}: {txt[-120:]}"))
    print("tab          open the page URL: 🧭 is the first tab")
    for label, rc, last in out:
        if rc != 0:
            print(f"⚠️ {label}: {last[:120]}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

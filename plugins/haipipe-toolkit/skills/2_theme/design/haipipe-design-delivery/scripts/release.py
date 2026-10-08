"""Release one design Job (run-release-j<NN>), freezing its predictions first with --freeze (run-freeze-predictions-j<NN>).

    python release.py <job folder> [--freeze YYMMDD] [--dry]

A design is released when its face's state is `kept` and its `prediction.yaml` (with a predicted effect) is frozen.
A Job whose t99 ranked must have its ranking projected first; only a Job with no rank Run (a method with no ⑤)
releases its `passed` designs. Writes the Job's `delivery/designs.json` and `designs.md`
(ref/designs-schema.md), a UI design's last judged screen into `delivery/screens/`, adds the Job's designs to the
Block's `delivery/designs.json` and `designs.md` (never twice), and sets each released face to `state: released`.
Refuses a draft prediction unless --freeze gives the day a person signed. Prints what it wrote.
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

import yaml

DESIGN = re.compile(r"^t\d+_(d\d+)_(.+)$")
PLACEHOLDER = re.compile(r"\s*<the design, word for word>\s*")   # the scaffold's unfilled ## Design


def front(md: Path) -> dict:
    m = re.match(r"(?s)^---\n(.*?)\n---\n", md.read_text(encoding="utf-8")) if md.is_file() else None
    return (yaml.safe_load(m.group(1)) or {}) if m else {}


def section(md: Path, heading: str) -> str:
    m = re.search(rf"(?ms)^##\s+{heading}\s*\n(.*?)(?=^##\s|\Z)", md.read_text(encoding="utf-8"))
    return m.group(1).strip() if m else ""


def set_state(md: Path, state: str) -> None:
    text = md.read_text(encoding="utf-8")
    md.write_text(re.sub(r"(?m)^state:\s*\S+", f"state: {state}", text, count=1), encoding="utf-8")


def last_screen(task: Path) -> Path | None:
    """The picture the last verify judged, from its own result/render/ (a UI design only)."""
    runs = task / "runs"
    verifies = sorted((p for p in runs.iterdir() if re.match(r"^(run-verify-|r\d\d_verify_)", p.name)),
                      key=lambda p: (p.stat().st_mtime, p.name)) if runs.is_dir() else []
    for v in reversed(verifies):
        pngs = sorted((v / "result" / "render").glob("*.png"))
        if pngs:
            return pngs[-1]
    return None


def _merge(path: Path, new: list) -> list:
    old = json.loads(path.read_text(encoding="utf-8")).get("designs", []) if path.is_file() else []
    seen = {(d.get("job"), d.get("design")) for d in old}
    return old + [d for d in new if (d["job"], d["design"]) not in seen]


def _md(designs: list, title: str) -> str:
    return f"# {title}\n\n" + "".join(f"## {d['job']} · {d['design']}\n\n{d['words']}\n\n" for d in designs)


def release(job: Path, freeze: str = "", dry: bool = False) -> list:
    jface = job / f"{job.name}.md"
    pins = front(jface)
    if not pins.get("method"):
        sys.exit(f"{job.name} is not a ladder Job: its face pins no method")
    jid = job.name.split("_", 1)[0]
    tasks = sorted(p for p in job.iterdir() if p.is_dir() and DESIGN.match(p.name))
    states = {t: str(front(t / f"{t.name}.md").get("state", "")) for t in tasks}
    ranked = any((job / "t99_review-whole" / "runs").glob("run-rank-*")) or any(
        (job / "t99_review-whole" / "runs").glob("r[0-9][0-9]_rank_*"))
    if ranked and not {"kept", "released"} & set(states.values()):
        sys.exit(f"{job.name}: t99 ranked its designs but no design is kept yet; project the ranking first "
                 "(haipipe-design-workflow/scripts/project_predictions.py), once run-rank-t99 has closed")
    wanted = "kept" if ranked or "kept" in states.values() else "passed"   # passed: a method with no ⑤
    chosen = [t for t in tasks if states[t] == wanted]
    if not chosen and "released" in states.values():
        print(f"{job.name}: already released; nothing new")
        return []
    if not chosen:
        sys.exit(f"{job.name} has no {wanted} design to release")
    if freeze and not re.match(r"^\d{6}$", freeze):
        sys.exit(f"--freeze is the day a person signed, YYMMDD: {freeze!r}")
    # 1 · check every design first, so a refusal leaves nothing half written
    plan = []
    for t in chosen:
        pred_path = t / "prediction.yaml"
        pred = yaml.safe_load(pred_path.read_text(encoding="utf-8")) if pred_path.is_file() else {}
        pred = pred if isinstance(pred, dict) else {}
        if ranked and not str(pred.get("predicted", "")).strip():
            sys.exit(f"{t.name}: no predicted effect in prediction.yaml; it comes from t99's ranking (project it first)")
        draft = str(pred.get("frozen", "draft")) == "draft"
        if draft and not freeze:
            sys.exit(f"{t.name}: its prediction is a draft; freeze it first (run-freeze-predictions-{jid}, "
                     "--freeze YYMMDD)")
        m = DESIGN.match(t.name)
        face = t / f"{t.name}.md"
        words = section(face, "Design")
        if not words or PLACEHOLDER.fullmatch(words):
            sys.exit(f"{t.name}: its face's ## Design still holds no design ({words[:40]!r}); project the passed draft "
                     "into it first (haipipe-design-workflow/scripts/project_draft.py draft)")
        d = {"job": jid, "design": m.group(1), "name": str(front(face).get("name", m.group(2))), "words": words,
             "predicted": str(pred.get("predicted", "")), "released": freeze if draft else str(pred.get("frozen")),
             "pins": {"goal": str(pins.get("goal", "")), "method": str(pins.get("method", "")),
                      "inputs": str(pins.get("inputs", ""))}}
        screen = last_screen(t)
        if screen is not None:
            d["screen"] = f"screens/{m.group(1)}{screen.suffix}"          # relative to the Job's delivery/
        plan.append((t, pred_path, pred, draft, screen, d))
    out = [d for *_, d in plan]
    if dry:
        for d in out:
            print(f"would release {d['job']} · {d['design']}")
        return out
    # 2 · write: the frozen predictions, the screens, the Job's delivery/, then the Block's
    block = job.parent
    for t, pred_path, pred, draft, screen, d in plan:
        if draft:
            pred["frozen"] = freeze
            pred_path.write_text(yaml.safe_dump(pred, sort_keys=False, allow_unicode=True), encoding="utf-8")
            print(f"froze {t.name}: {freeze}")
        if screen is not None:
            (job / "delivery" / "screens").mkdir(parents=True, exist_ok=True)
            (block / "delivery" / "screens").mkdir(parents=True, exist_ok=True)
            shutil.copy2(screen, job / "delivery" / d["screen"])
            shutil.copy2(screen, block / "delivery" / "screens" / f"{jid}-{d['design']}{screen.suffix}")
    (job / "delivery").mkdir(parents=True, exist_ok=True)
    jdesigns = _merge(job / "delivery" / "designs.json", out)
    (job / "delivery" / "designs.json").write_text(json.dumps({"designs": jdesigns}, indent=2, ensure_ascii=False) + "\n",
                                                   encoding="utf-8")
    (job / "delivery" / "designs.md").write_text(_md(jdesigns, "Released designs"), encoding="utf-8")
    (block / "delivery").mkdir(parents=True, exist_ok=True)
    at_block = [{**d, "screen": f"screens/{d['job']}-{d['design']}{Path(d['screen']).suffix}"} if "screen" in d else d
                for d in out]                                              # relative to the Block's delivery/
    bdesigns = _merge(block / "delivery" / "designs.json", at_block)
    (block / "delivery" / "designs.json").write_text(json.dumps({"designs": bdesigns}, indent=2, ensure_ascii=False)
                                                     + "\n", encoding="utf-8")
    (block / "delivery" / "designs.md").write_text(_md(bdesigns, "Released designs, every Job"), encoding="utf-8")
    for t, *_ in plan:
        set_state(t / f"{t.name}.md", "released")
    for d in out:
        print(f"released {d['job']} · {d['design']}")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("job", type=Path)
    ap.add_argument("--freeze", default="")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args(argv)
    return release(a.job, a.freeze, a.dry)


if __name__ == "__main__":
    main()

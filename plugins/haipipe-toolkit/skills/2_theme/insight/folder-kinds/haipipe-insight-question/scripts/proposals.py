"""proposals.py · triage a Prototype's proposals into the next release (b11 s21 phase 3; haipipe-insight ref/release.md).

    python proposals.py list    <Prototype>                              the open proposals, by kind
    python proposals.py take    <Prototype> <slug> [<slug> …] --into p<N> mark a batch taken; print how to apply each
    python proposals.py decline <Prototype> <slug> --why "…"             mark one declined, with its reason

A proposal is `proposals/<slug>.md` (kind · level · from · state · taken-in, then why), written by a Propose Run
(`insight_ladder.py propose`). Triage (`run-triage-proposals-pN`) takes one batch into one release: the newest release
while it is still open, or the next one (opened after, with `insight_ladder.py version`). This script writes only the
proposals' state; applying a taken proposal is the release's own Run, printed for each. Exit 1 on a refused step.
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    "insight_ladder", HERE.parents[2] / "haipipe-insight" / "scripts" / "insight_ladder.py")
IL = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(IL)
APPLY = {"new question": "insight_ladder.py question <release> <L><NN> <slug>   (run-ask-<l><nn>)",
         "fix": "insight_ladder.py change <release> <L><NN> --why \"…\"      (then plan, review, script, review again)",
         "retire": "insight_ladder.py retire <release> <L><NN> --why \"…\"",
         "cut": "edit the release's partitions.md, then run-set-cuts-p<N> (a person signs the cuts)"}


def proposals(proto: Path) -> list[tuple[Path, dict, str]]:
    pdir = proto / "proposals"
    out = []
    for p in sorted(pdir.glob("*.md")) if pdir.is_dir() else []:
        if p.name == "README.md":
            continue
        fm, body = IL.front(p)
        out.append((p, fm, body))
    return out


def _target_release(proto: Path, into: str) -> str:
    vers = IL.versions(proto)
    newest = vers[-1] if vers else None
    rel = IL.VERSION.match(newest.name).group(2) if newest else ""
    nxt = f"p{int(rel[1:]) + 1}" if rel else "p1"
    if newest is not None and str(IL.face(newest).get("state")) != "closed":
        if into != rel:
            sys.exit(f"{newest.name} is still open: a batch goes into {rel}, or sign it first")
        return rel
    if into != nxt:
        sys.exit(f"the newest release is signed: a batch goes into the next one, {nxt}")
    return nxt


def _set(path: Path, fm: dict, body: str, **kv) -> None:
    fm.update(kv)
    path.write_text(IL.with_front(fm, body), encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("command", choices=("list", "take", "decline"))
    ap.add_argument("prototype", type=Path)
    ap.add_argument("slugs", nargs="*")
    ap.add_argument("--into", default="")
    ap.add_argument("--why", default="")
    a = ap.parse_args(argv)
    if IL.face_kind(a.prototype) != "prototype":
        sys.exit(f"{a.prototype.name} is not a Prototype (board.md board-kind: prototype)")
    allp = {p.stem: (p, fm, body) for p, fm, body in proposals(a.prototype)}
    if a.command == "list":
        open_ = [(s, fm) for s, (_, fm, _) in allp.items() if fm.get("state", "open") == "open"]
        for kind in IL.KINDS:
            mine = [s for s, fm in open_ if fm.get("kind") == kind]
            if mine:
                print(f"{kind}: " + ", ".join(mine))
        print(f"{len(open_)} open of {len(allp)}")
        return 0
    if not a.slugs:
        sys.exit("name the proposals: their file names without .md")
    for s in a.slugs:
        if s not in allp:
            sys.exit(f"no proposal {s} in {a.prototype.name}/proposals/")
        if allp[s][1].get("state", "open") != "open":
            sys.exit(f"{s} is already {allp[s][1].get('state')}")
    if a.command == "decline":
        if not a.why:
            sys.exit("--why says why it is declined, in one line")
        for s in a.slugs:
            p, fm, body = allp[s]
            _set(p, fm, body, state="declined", declined=a.why)
            print(f"declined {s}: {a.why}")
        return 0
    rel = _target_release(a.prototype, a.into)
    for s in a.slugs:
        p, fm, body = allp[s]
        _set(p, fm, body, state="taken", **{"taken-in": rel})
        print(f"taken into {rel}: {s} ({fm.get('kind')}) → {APPLY.get(fm.get('kind'), 'apply it in the release')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

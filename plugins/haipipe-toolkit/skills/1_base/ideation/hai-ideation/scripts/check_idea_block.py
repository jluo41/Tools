#!/usr/bin/env python3
"""Check Idea Block ownership, optionally applying a semantic gate to its Jobs.

This is read-only. Structure is not scientific readiness, Run validation, a
Paper-origin audit or proof of a dedicated renderer.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import re

from check_ideation import Finding, GateCheck
from idea_layout import BLOCK_NAME, block_key, is_idea_job, mapping


def check_block(root: Path, gate: str | None = None, job: str | None = None) -> list[Finding]:
    root = root.resolve()
    findings = []

    def fail(code: str, path: Path, message: str) -> None:
        findings.append(Finding(code, str(path), message))

    manifest = mapping(root / "ideation.yaml")
    if manifest.get("kind") != "ideation-block" or manifest.get("version") != 1:
        fail("block-manifest", root / "ideation.yaml", "expected version 1 ideation-block")
    if not re.fullmatch(BLOCK_NAME, root.name):
        fail("block-address", root, "expected Idea-<Slug> (an older Block: bNN_<direction>)")
    for key in ("direction", "question", "scope"):
        if not isinstance(manifest.get(key), str) or not manifest[key].strip():
            fail("missing-field", root / "ideation.yaml", f"missing {key}")
    face = root / "board.md"
    try:
        content = face.read_text(encoding="utf-8")
    except OSError:
        content = ""
    if not re.search(r"(?m)^board-kind:\s*ideation-block\s*$", content):
        fail("block-face", face, "board.md must declare board-kind: ideation-block")
    rows = manifest.get("ideas")
    if not isinstance(rows, list) or not rows:
        fail("idea-index", root / "ideation.yaml", "ideas must index at least one admitted Job")
        return findings
    jobs, ids = set(), set()
    for row in rows:
        if not isinstance(row, dict):
            fail("idea-index", root / "ideation.yaml", "each idea entry must be a mapping")
            continue
        name, identity = row.get("job"), row.get("idea_id")
        if not isinstance(name, str) or not re.fullmatch(r"j\d{2,}_[^/\\]+", name):
            fail("job-address", root / "ideation.yaml", "job must name a direct jNN folder")
            continue
        if name in jobs:
            fail("duplicate-job", root / name, "Job indexed more than once")
        jobs.add(name)
        if not isinstance(identity, str) or not re.fullmatch(r"i\d+", identity):
            fail("idea-id", root / name, "idea_id must match iNN")
        elif identity in ids:
            fail("duplicate-idea", root / name, "Idea id belongs to more than one Job")
        else:
            ids.add(identity)
        folder = root / name
        if folder.is_symlink() or not folder.is_dir():
            fail("job-folder", folder, "expected an owned direct Job folder")
            continue
        if not (folder / f"{name}.md").is_file():
            fail("job-face", folder, "Job face is missing")
        if not is_idea_job(folder):
            fail("idea-ownership", folder, "index, layout, parent and sole canonical Card must agree")
        data = mapping(folder / "ideation.yaml")
        expected = block_key(root.name) + "." + name.split("_", 1)[0]
        if data.get("address") != expected:
            fail("job-address", folder, f"manifest address must be {expected}")
        for task in sorted(folder.glob("t[0-9]*_*")):
            if not task.is_dir():
                continue
            task_face = task / f"{task.name}.md"
            if task.is_symlink() or not task_face.is_file():
                fail("task-face", task, "evaluation Task needs its own face")
            else:
                face_text = task_face.read_text(encoding="utf-8")
                if not re.search(r"(?m)^task-type:\s*(ideation|draft)\s*$", face_text):
                    fail("task-type", task_face, "authored assessment uses ideation; a separate prose Page may use draft")
            if (task / "ideation.yaml").exists():
                fail("task-portfolio", task, "canonical Idea unit belongs to the Job, not an evaluation Task")
            for run in sorted((task / "runs").glob("*")):
                if not run.is_dir():
                    continue
                card = mapping(run / "run.yaml")
                types = card.get("type")
                if card.get("kind") == "hard" and (types == "collect" or isinstance(types, list) and "collect" in types):
                    continue  # shared collection owner; full shape checked by ladder.py
                if card.get("kind") != "soft" or not run.name.startswith("run-"):
                    fail("assessment-run-kind", run, "assessment uses a shared soft Run; scientific execution belongs to Work")
                ticket = card.get("ticket")
                if (card.get("run") != run.name or not isinstance(ticket, str)
                        or Path(ticket).name != ticket or Path(ticket).stem != run.name
                        or not (run / ticket).is_file()):
                    fail("assessment-ticket", run, "Run card, folder and existing ticket must share their identity")
                if (run / "result").exists():
                    fail("assessment-result", run, "soft assessments write authored outcomes, not hard Results")
        if gate and (job is None or name == job):
            check = GateCheck(folder)
            getattr(check, f"check_{gate}")()
            for finding in check.findings:
                findings.append(Finding(finding.code, str(folder / finding.path), finding.message))
    actual = {p.name for p in root.glob("j[0-9]*_*") if p.is_dir()}
    if jobs != actual:
        fail("job-index", root, "indexed Jobs must equal the Block's Job folders")
    if job is not None and job not in jobs:
        fail("unknown-job", root, f"Job {job!r} is not indexed")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("block", type=Path)
    parser.add_argument("--gate", choices=("generate", "sync", "test", "select", "handoff"))
    parser.add_argument("--job", help="apply the semantic gate to this indexed Job only")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    findings = check_block(args.block, args.gate, args.job)
    if args.json:
        print(json.dumps({"ok": not findings, "gate": args.gate or "structure",
                          "findings": [asdict(f) for f in findings]}, indent=2))
    else:
        print("FAIL" if findings else "PASS", args.gate or "structure", args.block)
        for item in findings:
            print(f"{item.code}: {item.path}: {item.message}")
    return bool(findings)


if __name__ == "__main__":
    raise SystemExit(main())

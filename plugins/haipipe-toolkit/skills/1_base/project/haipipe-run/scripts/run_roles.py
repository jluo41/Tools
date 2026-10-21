"""run_roles (haipipe-run): give each Run card a `role:`, the one job it does in its Task, so a Task's many Runs read
as groups. Written first for LLMRec b01 and b02 (261021); haipipe-project `ladder.py update --today --apply` writes the
roles a Block lacks through propose(), and a Project's own ticket generators import propose() so a new card has one.

JL 261020: "每个 task 的 run，应该也最好分分类 ... 一个 task 可能有很多 run，但我还是想让这些 run ... 各司其职"
(a Task may have many Runs; each should do its own job). The workbench (workbench-work work_progress.py, ROLES)
groups a Task's Runs by this field, in this order:

    trial     a small try before the full Run (smoke, preview, sentinel, eval400)
    make      makes the Task's output (a fold, a full pass, a build)
    fix       asks again what a Run missed, or repairs it (retry, recovery, *fix, clean text)
    check     audits or compares an output (audit, contract, compare)
    describe  says what an output holds (Table Card, distributions)
    figures   draws results as charts
    evidence  one value or display for a page
    publish   releases or delivers an output

The role is proposed from the Run's name, then written into its card as one line after `kind:` (the rest of the
card is left as it is). A card that already has a role keeps it. Dry run by default.

Usage: python run_roles.py <Block, Job or Task folder> [--apply]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RULES = (  # first match wins, read against the Run's folder name
    ("evidence", r"page-evidence-item|report_displays"),
    ("check", r"audit|contract|compare"),          # before publish: r09_audit_published_site audits, it does not publish
    ("publish", r"publish|^run-delivery"),
    ("figures", r"figures"),
    ("describe", r"describe|descriptive"),
    ("fix", r"retry|recover|fix\b|fix_|_fix|hyphenfix|slugfix|mfmfix|clean_text"),   # recover: re-asks what failed (b02)
    ("trial", r"smoke|preview|sentinel|eval400"),
)


def propose(name: str) -> str:
    return next((role for role, pattern in RULES if re.search(pattern, name)), "make")


def main(argv: list[str]) -> int:
    block = Path(argv[0]).resolve()
    apply = "--apply" in argv
    for card in sorted(block.glob("**/runs/*/run.yaml")):
        if "/_old/" in str(card) or not re.match(r"^t\d{2}_", card.parent.parent.parent.name):
            continue                                  # a role groups a Task's Runs; a Block's drawings are not grouped
        text = card.read_text(encoding="utf-8")
        if re.search(r"(?m)^role:", text):
            continue
        role = propose(card.parent.name)
        lines = text.splitlines(keepends=True)
        at = next((i + 1 for i, line in enumerate(lines) if line.startswith("kind:")), 1)
        lines.insert(at, f"role: {role}\n")
        print(f"{role:9} {card.parent.relative_to(block)}")
        if apply:
            card.write_text("".join(lines), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

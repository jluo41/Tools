"""Disk: the files behind each view of the design ladder, under the open folder (split from design_views.py,
which re-exports every name here)."""
from __future__ import annotations

from pathlib import Path



# ── Disk: the files behind each view, under the open folder (the frame's Disk box, folded with the Runs; the "on
# disk" tree under each screen of s11 · s12 · s13). "{face}" is the open folder's face.
J = "j[0-9]*_*/"
DISK = {
    "Block": {
        "Map": (("board.md", "## Goals: the rows"), (J, "each Job: its face pins goal · method · inputs")),
        "Goals": (("board.md", "## Goals: one card per goal, signed once here"), (J + "inputs/goal.md", "a Job's copy (run-setup-goal-jNN)")),
        "Methods": ((J + "inputs/method.md", "each Job's pinned method (the registry is the skill's)"),),
        "Inputs": (("inputs/i*/", "the inputs versions"), ("inputs/i*/manifest.yaml", "each file's sha256, frozen"),
                   (J + "inputs/manifest.yaml", "each Job's fence")),
        "Summary": (("board.md", "## Goals · close"), (J + "t99_*/runs/run-rank-t99/result/ranking.csv", "each Job's top design"),
                    (J + "t*_d*/prediction.yaml", "predicted · against · by · why"), ("runs/run-score-*/scores.csv", "what an Exp returned"),
                    ("reports/q*/q*.md", "the bottom line: each answered question's Opening"),
                    (J + "runs/run-release-*/run.yaml", "who approved: signed:"), ("delivery/summary.pdf", "the one-page PDF")),
        "Rounds": (("inputs/i*/manifest.yaml", "one round per inputs version: frozen · new · parts"), (J, "each Job's inputs pin"),
                   ("delivery/designs.json", "what was released"), ("observed/e*/arms.csv", "what an Exp returned")),
        "Questions": (("board.md", "## Questions: one row each"), ("reports/q*/q*.md", "Report: its title and opening"),
                      (J, "Task Work: the Jobs a question names")),
        "Cost": ((J + "runs/*/run.yaml", "started_at · finished_at · usage"), (J + "t*_*/runs/*/run.yaml", "each Task's Runs")),
        "Predicted vs observed": (("observed/e*/arms.csv", "observed: per-arm totals, each arm names jNN · dNN"),
                                  ("runs/run-score-*/scores.csv", "each arm's design scored"),
                                  (J + "t*_d*/prediction.yaml", "predicted: frozen at release")),
        "Method scorecard": (("runs/run-score-*/scores.csv", "summed per method version"), (J, "each Job's method pin")),
        "Work Details": ((J, "one card per Job"), (J + "t00_*/", "t00 · reason ideas"), (J + "t*_d*/", "one design each"),
                         (J + "t99_*/", "t99 · review whole")),
        "Runs": (("runs/*/", "the Block's Runs, every one soft"),),
        "Delivery": (("delivery/designs.json", "every released design, every Job"), ("delivery/designs.md", "for people"),
                     ("delivery/screens/", "a UI design's screens")),
    },
    "Job": {
        "Goal": (("{face}", "goal: the pin"), ("inputs/goal.md", "the goal as the design work sees it"),
                 ("runs/run-setup-goal-*/", "pins it (signed once, at the Block)")),
        "Method": (("inputs/method.md", "the pinned method: its five steps"), ("runs/run-setup-method-*/", "links it in")),
        "Inputs": (("inputs/", "the fence: the only folder the design work sees"), ("inputs/manifest.yaml", "each file's source and sha256"),
                   ("runs/run-setup-inputs-*/", "builds it")),
        "Reason ideas": (("t00_*/runs/r*_reason_*/result/chains.yaml", "each topic's chain"),
                         ("t00_*/runs/r*_reason_*/result/ideas.yaml", "the ideas")),
        "Design display": (("t*_d*/", "one card per design"), ("t*_d*/elements.yaml", "its process"), ("t*_d*/runs/*/", "generate · verify")),
        "Review whole": (("t99_*/runs/r*_rank_*/result/ranking.csv", "rank the N + 5, keep N"),),
        "Predicted vs observed": (("t*_d*/prediction.yaml", "frozen at release"), ("../observed/", "the Block's: what the Exp returned"),
                                  ("../runs/", "the Block's run-score-eNN")),
        "Performance": (("runs/*/run.yaml", "the Job's Runs: time"), ("t*_d*/runs/*/run.yaml", "each design's Runs"),
                        ("t*_d*/prediction.yaml", "predicted")),
        "WD Reason ideas": (("t00_*/", "step ②: the ideas"),),
        "WD Conduct & review": (("t*_d*/", "steps ③ ④: one design each"),),
        "WD Review whole": (("t99_*/", "step ⑤: the ranking"),),
        "Setup": (("runs/run-setup-*/", "goal · method · inputs"), ("runs/run-open-designs-*/", "opens one Task per idea")),
        "Runs Reason ideas": (("t00_*/runs/*/", "hard: reason"),),
        "Runs Conduct & review": (("t*_d*/runs/*/", "generate · verify · revise"),),
        "Runs Review whole": (("t99_*/runs/*/", "hard: rank"), ("runs/run-freeze-predictions-*/", "a person signs"),
                              ("runs/run-release-*/", "a person signs")),
        "designs.md": (("delivery/designs.md", "for people, written from designs.json"),),
        "designs.json": (("delivery/designs.json", "for machines: one entry per design, its pins"),),
    },
    "t00": {"Task": (("{face}", "state"), ("runs/r*_reason_*/", "the reasoning Run")),
            "Topics": (("runs/r*_reason_*/result/chains.yaml", "each topic's chain"),),
            "Ideas": (("runs/r*_reason_*/result/ideas.yaml", "the ideas, each with its design"),),
            "Chains": (("runs/r*_reason_*/result/chains.yaml", "a row per step"),),
            "Runs": (("runs/*/", "hard: reason"),),
            "Delivery": (("runs/r*_reason_*/result/ideas.yaml", "handed to the Job"),)},
    "design": {"Design": (("{face}", "## Design: the message"), ("elements.yaml", "its process"), ("prediction.yaml", "expected")),
               "Evaluation": (("runs/r*_verify_*/", "④ review, another agent"),),
               "Tests": (("runs/r*_verify_*/run.yaml", "each test's result"),),
               "Drafts": (("runs/r*_generate_*/result/design.md", "draft 1"), ("runs/run-revise-*/result/design.md", "later drafts")),
               "Performance": (("runs/*/run.yaml", "time"), ("prediction.yaml", "predicted"), ("../../observed/", "the Block's: the Exp")),
               "Elements": (("elements.yaml", "words · from · because · step"),),
               "Runs": (("runs/*/", "generate · verify · revise"),),
               "Delivery": (("../delivery/designs.json", "released with the Job"),)},
    "t99": {"Task": (("{face}", "state"), ("runs/r*_rank_*/", "the ranking Run")),
            "Ranking": (("runs/r*_rank_*/result/ranking.csv", "rank · design · predicted · why · kept"),),
            "Coverage": (("runs/r*_rank_*/result/ranking.csv", "the kept N"),),
            "Kept · Dropped": (("runs/r*_rank_*/result/ranking.csv", "kept or dropped"),),
            "Runs": (("runs/*/", "hard: rank"),),
            "Delivery": (("runs/r*_rank_*/result/ranking.csv", "handed to the Job's release"),)},
}


def _disk(level: str, view: str, folder: Path) -> tuple:
    return tuple((p.replace("{face}", folder.name + ".md"), m) for p, m in DISK.get(level, {}).get(view, ()))

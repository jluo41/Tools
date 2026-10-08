"""s31 · the Job level of the insight Guide: one Job, one Prototype release run on one data version.

Read live: the Space cards from s12's screens, today's step 3 from method.md, the cards and papers from the
Guide's files. Typed here, as the proposal (red): the Job's own steps under plan C (launch, power, compare,
close), with the compare rule fixed in the release before any outcome.
"""
import insight_guide_live as G

WORDS = {"Description": ("its two pins: the Prototype release and the data version", "j0N_pN_<d>vM.md · the release · <d>vM"),
         "Idea Studio": ("optional: a drawing about this pair", "studio/"),
         "Audience Report": ("Question │ Work │ Report by D · I · K · W, filtered by Partition × Period",
                             "tNN_<L><NN>_<q>.md · reports/vs-<prev>.md"),
         "Work Details": ("the J-T-R tree: its Tasks, each open to its Runs", "tNN_<L><NN>_<q>/runs/"),
         "Runs": ("its own soft Runs, then its Tasks' hard and soft", "runs/ · tNN_…/runs/"),
         "Delivery": ("? only the latest Job's Wisdom counsel, to the Board", "→ Board › Delivery")}
STEPS = [("? 1 · Launch the Job", "start every Task's hard Runs, one per partition", "where: Runs (Run the Job)   signs: —"),
         ("? 2 · Check the power", "n and power per cut, before any outcome: which cells are refused",
          "where: Description › Dataset · Runs (run-power)   methods: By partition and power   signs: —"),
         G.step_card(3, "Job"),
         ("? 4 · Compare with the previous Job", "new question · new finding · held · changed · dropped · not comparable",
          "where: Audience Report › vs previous (run-compare)   rule: the release's thresholds.yaml   signs: —"),
         ("? 5 · Propose questions", "new or changed questions, from the statuses and the gaps, to the Prototype's proposals/",
          "where: Audience Report › vs previous · Runs (run-propose)   then: the next release, then a new Job   signs: —"),
         ("? 6 · Close the Job", "after every check, the comparison and the proposals: frozen",
          "where: Description (Close the Job)   signs: —")]

LEVEL = {
    "Description": [("t", G.role("Job", "one Prototype release run on one data version; frozen once closed")),
                    ("c", G.space_cards("Job", WORDS)),
                    ("t", "the Job's line, atop Description › Prototype: pN × <d>vM · closed, frozen · moved from <prev>: code | data"),
                    ("t", "✎ 261007  the Job's line moved into Description › Prototype (was: a band beside the tab)")],
    "Method": [("c", STEPS), ("t", "method cards"),
               ("c", G.method_cards(["By partition and power", "By heterogeneity"])),
               ("t", "? no card yet for comparing two Jobs (what 'held' means)")],
    "RoadMap Draw": [("w", G.drawings(["s12-job-level", "s00-insight-structure"])),
                     ("t", "? guide.yaml roadmap: Job")],
    "Related Paper": [("c", G.papers(["by partition and power", "by heterogeneity; by partition and power", "by heterogeneity"])[0]),
                      ("t", "? none yet behind comparing two Jobs")],
}

ON_DISK = {
    "Description": [("Tools/designs/b11_theme_insight/studio/s12-job-level/", "the Job's six Spaces, as designed"),
                    ("j0N_pN_<d>vM/j0N_pN_<d>vM.md", "the Job's line: its pins and state")],
    "Method": [("? method.md **Job · …** table", "? launch · power · run · compare · propose · close"),
               ("? work/…_prototype/j0N_pN/thresholds.yaml › compare", "? the rule for held, fixed before any outcome")],
    "RoadMap Draw": [("? guide.yaml roadmap: Job", "? s12 · s00")],
    "Related Paper": [("servers/workbench-insight/related/papers.md", "groups: by partition and power · by heterogeneity")],
}

OPEN = ["? run-power: a Job step before any outcome, or each Task's own check?",
        "? held = same direction and the intervals overlap (D: counts within a tolerance): the release's rule",
        "? Delivery at the Job: only the latest Job's Wisdom counsel goes to the Board"]

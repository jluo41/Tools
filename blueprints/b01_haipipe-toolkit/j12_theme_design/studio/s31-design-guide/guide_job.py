"""s31 · the Job level of the design Guide: what a design Job's tab shows in its Guide's Job section.

Read live from the design Guide's files (design_guide_live.py), then the Job-level proposals, each marked
"?" (261007, after s00 and s12): a Job is one goal × one method version × one inputs version → N designs;
the method is pinned, not copied; check overall (the method's part 5) runs on the N together; a card
grows from three parts to the design unit's five.
"""
import design_guide_live as G

SKILLS = "skills   haipipe-design-workflow: commission · generate · verify runs · haipipe-design-unit: one design · workbench-design shows"
AIM = ("? 1b · Set the goal's aim and N", "this goal's aim, who, venue, N; the rules it keeps",
       "where: Description › Goal   runs: Set the goal · Commission   signs: a person")
OVERALL = ("? 4b · Check overall", "the N together: they cover the goal, no two alike",
           "where: Audience Report › Check overall   ? a Run, or computed")
GROUPS = G.method_groups()
BY = G.papers(GROUPS)

LEVEL = {
    "Description": [("t", "? one goal × one method version × one inputs version → N designs  (base: " + G.role("Job") + ")"),
                    ("c", G.space_cards("Job")), ("m", SKILLS),
                    ("t", "? Description: Goal · Method · Inputs, no Map (s12); live today: Goal · Method")],
    "Method": [("c", [AIM] + G.steps({2, 3}) + [OVERALL] + G.steps({5})),
               ("t", "the thirteen method cards"), ("c", G.method_cards()),
               ("t", "? a card has 3 parts (see · conduct · check); the unit has 5: one shape (s00)"),
               ("t", "? the Job pins a method version (path + hash); method.md is not copied in")],
    "RoadMap Draw": [("w", G.drawings([("s12-design-job", "s12 · the Job", "a Job's screens"),
                                       ("s03-design-methods", "s03 · the methods", "the methods canvas and the design unit")])),
                     ("t", "the methods canvas and the design unit open at the top of Guide › Method today")],
    "Related Paper": [("c", BY[:8]), ("t", f"… {len(BY)} papers, one group per method ({len(GROUPS)} groups)"),
                      ("t", "? under each method card, its own papers, rather than one long list")],
}

ON_DISK = {
    "Description": [("servers/workbench-design/design_theme.py", "_job: Goal · Method; each card's runs"),
                    ("? design_theme.py _job: Inputs", "? the Job's inputs/: the fence it sees (symlinks + manifest)")],
    "Method": [("servers/workbench-design/guide/method.md", "§ 1 steps 2, 3, 5 · § 2.3 the 13 cards"),
               ("servers/workbench-design/guide/methods/NN-by-<method>.md", "one card each"),
               ("? methods/NN-by-<method>.md: five parts", "? see input · reason ideas · conduct process · review item · review whole")],
    "RoadMap Draw": [("Tools/blueprints/b01_haipipe-toolkit/j12_theme_design/studio/s12-design-job/", "the Job's screens"),
                     ("Tools/blueprints/b01_haipipe-toolkit/j12_theme_design/studio/s03-design-methods/", "design-methods · design-unit-methods")],
    "Related Paper": [("servers/workbench-design/related/papers.md", f"group = a method: {len(BY)} papers")],
}

OPEN = ["? Step 1 split: each goal's aim and N set on its Job (Description › Goal), the goal list on the Block?",
        "? Check overall (part 5): its own Run, or computed in the Audience Report?",
        "? The method card grows to five parts, the same shape as the design unit and a method version?",
        "? A Job pins a method version by path and hash; method.md is no longer copied into the Job?"]

"""s31 · the Block level of the design Guide: what the design Board's Guide shows in its Block section.

Read live from the design Guide's files (design_guide_live.py), then the Block-level proposals, each
marked "?" so it draws red until JL settles it (261007, after s00 and s11):

1. A Block step 0, Set the inputs: rules · theory · handoff as one version (i1, i2 …) that a Job pins.
2. Step 1 splits: the Block holds the goal list; each goal's aim and N are set on its Job.
3. A Block step 7, Score the predictions: predicted against observed, per method version (Audience
   Report › Method scorecard), sending proposals to the methods Block.
4. The six steps' "where today" names the old board and page; the new places are the Block · Job · Task tabs.
"""
import design_guide_live as G

SKILLS = ("? skills   haipipe-design owns · haipipe-design-goal: goals, rules · haipipe-design-brief: retire into the "
          "goal list ? · workbench-design shows")
INPUTS = ("? 0 · Set the inputs", "rules · theory · handoff, one version; a Job fences it in its inputs/",
          "where: Description › Inputs   runs: Add an inputs version   signs: a person")
GOALS = ("? 1 · Set the goals", "the goal list; each goal's aim and N go on its Job",
         "where: Description › Goals (the Brief merged in ?)   signs: a person")
SCORE = ("? 7 · Score the predictions", "predicted against observed, per method version",
         "where: Audience Report › Method scorecard   runs: Score predictions   sends: proposals to the methods Block")
ALL = G.papers(["all methods"])

LEVEL = {
    "Description": [("t", "? one application, one channel: its goals, inputs and Jobs  (base: " + G.role("Block") + ")"),
                    ("c", G.space_cards("Block")), ("m", SKILLS),
                    ("t", "? Description: Map · Goals · Methods · Inputs (s11); live today: Goal list · Theory · Rules")],
    "Method": [("c", [INPUTS, GOALS] + G.steps({6}) + [SCORE]),
               ("t", "the three families: where a method's rule comes from"), ("c", G.family_cards()),
               ("t", "? each step's 'where today' names the old board and page; the new: Block · Job · Task tabs")],
    "RoadMap Draw": [("w", G.drawings([("s00-design-structure", "s00 · design structure", "what a method is, how it evolves"),
                                       ("s01-design", "s01 · the ladder", "the ladder at a glance"),
                                       ("s11-design-block", "s11 · the Block", "the Board's screens"),
                                       ("s02-workbench-ui", "s02 · workbench UI", "the old page's drawing")])),
                     ("t", "? guide.yaml names one drawing (s02) today; the Block section would list these four")],
    "Related Paper": [("c", ALL[:6]), ("t", f"… {len(ALL)} papers in group 'all methods' (taxonomies, guidance, reviews)"),
                      ("t", "? none yet behind step 7: forecasting and calibration of predicted effects")],
}

ON_DISK = {
    "Description": [("servers/workbench-design/guide/guide.yaml", "description · skills (one list today)"),
                    ("servers/workbench-design/design_theme.py", "each card's sub · runs, read live"),
                    ("servers/workbench/guide/levels.yaml", "the base's words: design has no levels: yet"),
                    ("? guide.yaml levels: Block: role · spaces · skills", "? the design Block's own words")],
    "Method": [("servers/workbench-design/guide/method.md", "§ 1 the six steps · § 2.1 the families"),
               ("? method.md § 1: steps 0 and 7, a level column", "? Set the inputs · Score the predictions")],
    "RoadMap Draw": [("servers/workbench-design/guide/guide.yaml", "explain: roadmap-draw, one drawing"),
                     ("Tools/blueprints/b12_theme_design/studio/s00 · s01 · s11/", "the Block's drawings"),
                     ("? guide.yaml roadmap: Block: [s00, s01, s11, s02]", "? one list per level")],
    "Related Paper": [("servers/workbench-design/related/papers.md", f"group 'all methods': {len(ALL)} papers"),
                      ("? a level column in papers.md", "? as paper's: Block · Job · Task")],
}

OPEN = ["? Step 0, Set the inputs: a versioned inputs folder (i1, i2 …) a Job pins, signed by a person?",
        "? Step 1 split: the goal list on the Block, each goal's aim and N on its Job; the Brief retires into the list?",
        "? Step 7, Score the predictions: a Block hard Run, its verdicts sent to the methods Block as proposals?",
        "? guide.yaml levels: and a level column in method.md and papers.md, as the paper Guide has?"]
